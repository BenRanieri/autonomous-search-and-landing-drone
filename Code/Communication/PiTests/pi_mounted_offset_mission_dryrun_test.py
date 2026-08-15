import os
import sys
import time
from pathlib import Path

os.environ["LIBCAMERA_LOG_LEVELS"] = "*:3"

project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from picamera2 import Picamera2
from pymavlink import mavutil
import cv2

from Code.Mission.mission_state import (
    update_mission_state,
    update_acquire_stability,
    update_track_marker_loss,
    update_track_stability,
    is_landing_complete,
)

from Code.Mission.basic_search_pattern import get_basic_search_command

from Code.Mission.mounted_camera_guidance import (
    TARGET_ERROR_X,
    TARGET_ERROR_Y,
    TOLERANCE,
    LAND_TRIGGER_MARKER_SIZE,
    get_adjusted_error,
    is_marker_at_target,
    is_marker_large_enough,
    get_mounted_track_command,
)

from Code.Communication.mavlink_command_wrapper import send_velocity_command_safely


TARGET_ID = 0

CONNECTION_STRING = "/dev/ttyAMA0"
BAUD_RATE = 921600

RUN_TIME_SECONDS = 45

current_state = "SEARCH"

stable_count = 0
required_stable_count = 4

lost_marker_count = 0
max_lost_marker_count = 6

track_stable_count = 0
required_track_stable_count = 4

target_altitude = 1.5
current_altitude = 1.5
landing_altitude = 0.05
fake_land_step = 0.15

search_start_time = None

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector = cv2.aruco.ArucoDetector(dictionary)


def detect_marker(image_rgb):
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    corners, ids, rejected = detector.detectMarkers(gray)

    image_height, image_width = image_bgr.shape[:2]
    image_center_x = image_width / 2
    image_center_y = image_height / 2

    if ids is None:
        return {
            "detected": False,
            "id": None,
            "error_x": None,
            "error_y": None,
            "marker_size": None,
        }

    for i in range(len(ids)):
        marker_id = int(ids[i][0])

        if marker_id != TARGET_ID:
            continue

        marker_corners = corners[i][0]

        center_x = marker_corners[:, 0].mean()
        center_y = marker_corners[:, 1].mean()

        error_x = center_x - image_center_x
        error_y = center_y - image_center_y

        top_width = marker_corners[1][0] - marker_corners[0][0]
        bottom_width = marker_corners[2][0] - marker_corners[3][0]
        left_height = marker_corners[3][1] - marker_corners[0][1]
        right_height = marker_corners[2][1] - marker_corners[1][1]

        marker_size = (
            abs(top_width)
            + abs(bottom_width)
            + abs(left_height)
            + abs(right_height)
        ) / 4

        return {
            "detected": True,
            "id": marker_id,
            "error_x": error_x,
            "error_y": error_y,
            "marker_size": marker_size,
        }

    return {
        "detected": False,
        "id": None,
        "error_x": None,
        "error_y": None,
        "marker_size": None,
    }


print("Mounted offset mission dry-run test")
print("No real movement commands should be sent.")
print("TARGET_ERROR_X:", TARGET_ERROR_X)
print("TARGET_ERROR_Y:", TARGET_ERROR_Y)
print("TOLERANCE:", TOLERANCE)
print("LAND_TRIGGER_MARKER_SIZE:", LAND_TRIGGER_MARKER_SIZE)

print("Connecting to Pixhawk...")
vehicle = mavutil.mavlink_connection(CONNECTION_STRING, baud=BAUD_RATE)

print("Waiting for heartbeat...")
heartbeat = vehicle.wait_heartbeat(timeout=10)

if heartbeat is None:
    print("No heartbeat received")
    raise SystemExit

print("Heartbeat received")
print("System ID:", vehicle.target_system)
print("Component ID:", vehicle.target_component)

picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)

picam2.configure(config)
picam2.start()
time.sleep(2)

print("Running mounted offset mission dry-run for", RUN_TIME_SECONDS, "seconds...")
print("Start with marker out of view, then place it on the drone-center floor mark.")

last_mode = "unknown"
last_armed = False
start_time = time.time()

while time.time() - start_time < RUN_TIME_SECONDS:
    image_rgb = picam2.capture_array()
    marker = detect_marker(image_rgb)

    msg = vehicle.recv_match(type="HEARTBEAT", blocking=False)

    if msg is not None:
        last_mode = mavutil.mode_string_v10(msg)
        last_armed = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)

    marker_detected = marker["detected"]
    error_x = marker["error_x"]
    error_y = marker["error_y"]
    marker_size = marker["marker_size"]

    ready_to_track = False
    marker_lost = False
    ready_for_approach = False
    approach_complete = False
    landing_complete = False

    marker_centered = False
    size_good = False
    adjusted_error_x = None
    adjusted_error_y = None

    if marker_detected:
        adjusted_error_x, adjusted_error_y = get_adjusted_error(error_x, error_y)
        marker_centered = is_marker_at_target(error_x, error_y)
        size_good = is_marker_large_enough(marker_size)

    if current_state == "ACQUIRE":
        stable_count, ready_to_track = update_acquire_stability(
            marker_centered,
            stable_count,
            required_stable_count,
        )
    else:
        stable_count = 0

    if current_state in ["TRACK", "APPROACH"]:
        lost_marker_count, marker_lost = update_track_marker_loss(
            marker_detected,
            lost_marker_count,
            max_lost_marker_count,
        )
    else:
        lost_marker_count = 0

    if current_state == "TRACK":
        track_stable_count, ready_for_approach = update_track_stability(
            marker_centered,
            track_stable_count,
            required_track_stable_count,
        )
    else:
        track_stable_count = 0

    if current_state == "APPROACH":
        approach_complete = marker_detected and marker_centered and size_good

    if current_state == "LAND":
        current_altitude = current_altitude - fake_land_step

        if current_altitude < landing_altitude:
            current_altitude = landing_altitude

        landing_complete = is_landing_complete(
            current_altitude,
            landing_altitude,
        )

    previous_state = current_state

    current_state = update_mission_state(
        current_state,
        current_altitude,
        target_altitude,
        marker_detected,
        readyToTrack=ready_to_track,
        markerLost=marker_lost,
        readyForApproach=ready_for_approach,
        approachComplete=approach_complete,
        landingComplete=landing_complete,
    )

    search_action = "NONE"

    if current_state == "SEARCH" and not marker_detected:
        if search_start_time is None:
            search_start_time = time.time()

        search_elapsed_time = time.time() - search_start_time

        x_command, y_command, z_command, search_action = get_basic_search_command(
            search_elapsed_time
        )

    elif marker_detected and current_state in ["ACQUIRE", "TRACK", "APPROACH"]:
        search_start_time = None
        search_action = "MARKER_FOUND_STOP_SEARCH"

        (
            x_command,
            y_command,
            z_command,
            adjusted_error_x,
            adjusted_error_y,
        ) = get_mounted_track_command(error_x, error_y)

    elif current_state == "LAND":
        search_start_time = None
        search_action = "LAND_FAKE_DESCENT"
        x_command = 0
        y_command = 0
        z_command = 0.2

    else:
        x_command = 0
        y_command = 0
        z_command = 0

    result = send_velocity_command_safely(
        vehicle=vehicle,
        mode=last_mode,
        armed=last_armed,
        x_command=x_command,
        y_command=y_command,
        z_command=z_command,
    )

    if marker_detected:
        print(
            "mode:",
            last_mode,
            "armed:",
            last_armed,
            "state:",
            current_state,
            "previous:",
            previous_state,
            "search_action:",
            search_action,
            "marker:",
            marker["id"],
            "error_x:",
            round(error_x, 1),
            "error_y:",
            round(error_y, 1),
            "adjusted_x:",
            round(adjusted_error_x, 1),
            "adjusted_y:",
            round(adjusted_error_y, 1),
            "marker_size:",
            round(marker_size, 1),
            "centered:",
            marker_centered,
            "size_good:",
            size_good,
            "altitude:",
            round(current_altitude, 2),
            "stable_count:",
            stable_count,
            "track_stable_count:",
            track_stable_count,
            "approach_complete:",
            approach_complete,
            "landing_complete:",
            landing_complete,
            "command:",
            round(x_command, 3),
            round(y_command, 3),
            round(z_command, 3),
            "sent:",
            result["sent"],
            "allowed:",
            result["allowed"],
            "reasons:",
            result["reasons"],
        )
    else:
        print(
            "mode:",
            last_mode,
            "armed:",
            last_armed,
            "state:",
            current_state,
            "previous:",
            previous_state,
            "search_action:",
            search_action,
            "marker: not detected",
            "altitude:",
            round(current_altitude, 2),
            "command:",
            round(x_command, 3),
            round(y_command, 3),
            round(z_command, 3),
            "sent:",
            result["sent"],
            "allowed:",
            result["allowed"],
            "reasons:",
            result["reasons"],
        )

    if current_state == "DISARM":
        print("Reached DISARM in mounted offset dry-run. Ending test.")
        break

    time.sleep(0.25)

picam2.stop()

print("Mounted offset mission dry-run complete")
