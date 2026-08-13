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
    is_track_ready_for_approach,
    update_track_stability,
    is_landing_complete,
    get_track_command,
)

TARGET_ID = 0

TOLERANCE = 30
KP = 0.002
MAX_COMMAND = 0.25

DESIRED_MARKER_SIZE = 250
SIZE_TOLERANCE = 75

CONNECTION_STRING = "/dev/ttyAMA0"
BAUD_RATE = 921600

RUN_TIME_SECONDS = 35

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

print("Running mission dry-run logger for", RUN_TIME_SECONDS, "seconds...")
print("No commands will be sent to the Pixhawk.")
print("Testing: SEARCH -> ACQUIRE -> TRACK -> APPROACH -> LAND -> DISARM")
print("LAND uses fake software altitude only")

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

    if marker_detected and error_x is not None and error_y is not None:
        marker_centered = abs(error_x) <= TOLERANCE and abs(error_y) <= TOLERANCE

    if marker_detected and marker_size is not None:
        size_good = abs(marker_size - DESIRED_MARKER_SIZE) <= SIZE_TOLERANCE

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
        if marker_detected and error_x is not None and error_y is not None:
            track_ready = is_track_ready_for_approach(
                error_x,
                error_y,
                TOLERANCE,
            )
        else:
            track_ready = False

        track_stable_count, ready_for_approach = update_track_stability(
            track_ready,
            track_stable_count,
            required_track_stable_count,
        )
    else:
        track_stable_count = 0

    if current_state == "APPROACH":
        if marker_detected and marker_centered and size_good:
            approach_complete = True
        else:
            approach_complete = False

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

    if (
        marker_detected
        and error_x is not None
        and error_y is not None
        and current_state in ["ACQUIRE", "TRACK", "APPROACH"]
    ):
        x_command, y_command, z_command = get_track_command(
            error_x,
            error_y,
            TOLERANCE,
            KP,
            MAX_COMMAND,
        )
    elif current_state == "LAND":
        x_command = 0
        y_command = 0
        z_command = -0.2
    else:
        x_command = 0
        y_command = 0
        z_command = 0

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
            "marker:",
            marker["id"],
            "error_x:",
            round(error_x, 1),
            "error_y:",
            round(error_y, 1),
            "marker_size:",
            round(marker_size, 1),
            "altitude:",
            round(current_altitude, 2),
            "centered:",
            marker_centered,
            "size_good:",
            size_good,
            "stable_count:",
            stable_count,
            "track_stable_count:",
            track_stable_count,
            "lost_count:",
            lost_marker_count,
            "ready_to_track:",
            ready_to_track,
            "ready_for_approach:",
            ready_for_approach,
            "approach_complete:",
            approach_complete,
            "landing_complete:",
            landing_complete,
            "DRY_RUN_command:",
            round(x_command, 3),
            round(y_command, 3),
            round(z_command, 3),
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
            "marker: not detected",
            "marker_size:",
            marker_size,
            "altitude:",
            round(current_altitude, 2),
            "centered:",
            marker_centered,
            "size_good:",
            size_good,
            "stable_count:",
            stable_count,
            "track_stable_count:",
            track_stable_count,
            "lost_count:",
            lost_marker_count,
            "ready_to_track:",
            ready_to_track,
            "ready_for_approach:",
            ready_for_approach,
            "approach_complete:",
            approach_complete,
            "landing_complete:",
            landing_complete,
            "DRY_RUN_command:",
            round(x_command, 3),
            round(y_command, 3),
            round(z_command, 3),
        )

    if current_state == "DISARM":
        print("Reached DISARM in dry-run. Ending test.")
        break

    time.sleep(0.25)

picam2.stop()

print("Mission dry-run logger complete")
