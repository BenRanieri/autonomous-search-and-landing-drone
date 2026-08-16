import os
import sys
import time
import csv
import math
from pathlib import Path

os.environ["LIBCAMERA_LOG_LEVELS"] = "*:3"

project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from picamera2 import Picamera2
from pymavlink import mavutil
import cv2

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


TARGET_ID = 0

CONNECTION_STRING = "/dev/ttyAMA0"
BAUD_RATE = 921600

DEFAULT_RUN_TIME_SECONDS = 110

PHASE_PLAN = [
    (0, 10, "GROUND_CHECK", "Keep drone still and confirm logger is running"),
    (10, 25, "CENTER_HOVER", "Hover over/near the marker"),
    (25, 35, "MOVE_FORWARD", "Move drone slightly forward relative to its nose"),
    (35, 45, "CENTER_HOVER", "Return near marker center"),
    (45, 55, "MOVE_BACKWARD", "Move drone slightly backward relative to its nose"),
    (55, 65, "CENTER_HOVER", "Return near marker center"),
    (65, 75, "MOVE_RIGHT", "Move drone slightly right relative to its nose"),
    (75, 85, "CENTER_HOVER", "Return near marker center"),
    (85, 95, "MOVE_LEFT", "Move drone slightly left relative to its nose"),
    (95, 110, "MANUAL_LAND", "Land manually"),
]

CSV_COLUMNS = [
    "elapsed_s",
    "phase",
    "instruction",
    "mode",
    "armed",
    "relative_alt_m",
    "roll_deg",
    "pitch_deg",
    "yaw_deg",
    "marker_detected",
    "marker_id",
    "error_x",
    "error_y",
    "adjusted_error_x",
    "adjusted_error_y",
    "marker_size",
    "centered",
    "large_enough",
    "suggested_x_command",
    "suggested_y_command",
    "suggested_z_command",
]


dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector = cv2.aruco.ArucoDetector(dictionary)


def get_phase(elapsed_s):
    for start_s, end_s, phase, instruction in PHASE_PLAN:
        if start_s <= elapsed_s < end_s:
            return phase, instruction

    return "COMPLETE", "End the flight or keep landed"


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


def request_telemetry_streams(vehicle):
    vehicle.mav.request_data_stream_send(
        vehicle.target_system,
        vehicle.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_EXTRA1,
        5,
        1,
    )

    vehicle.mav.request_data_stream_send(
        vehicle.target_system,
        vehicle.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_POSITION,
        5,
        1,
    )


def get_run_time_seconds():
    if len(sys.argv) < 2:
        return DEFAULT_RUN_TIME_SECONDS

    try:
        return float(sys.argv[1])
    except ValueError:
        print("Invalid run time argument. Using default.")
        return DEFAULT_RUN_TIME_SECONDS


run_time_seconds = get_run_time_seconds()

logs_dir = project_root / "logs"
logs_dir.mkdir(exist_ok=True)

log_path = logs_dir / f"sign_mapping_readonly_{time.strftime('%Y%m%d_%H%M%S')}.csv"

print("Sign-mapping read-only logger")
print("No movement commands are sent by this script.")
print("Use during manual flight to label forward/back/right/left movements.")
print("TARGET_ERROR_X:", TARGET_ERROR_X)
print("TARGET_ERROR_Y:", TARGET_ERROR_Y)
print("TOLERANCE:", TOLERANCE)
print("LAND_TRIGGER_MARKER_SIZE:", LAND_TRIGGER_MARKER_SIZE)
print("Run time seconds:", run_time_seconds)
print("Log path:", log_path)

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

request_telemetry_streams(vehicle)

picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)

picam2.configure(config)
picam2.start()
time.sleep(2)

last_mode = "unknown"
last_armed = False

relative_alt_m = None
roll_deg = None
pitch_deg = None
yaw_deg = None

start_time = time.time()
last_print_time = 0
last_phase = None

with open(log_path, "w", newline="") as log_file:
    writer = csv.DictWriter(log_file, fieldnames=CSV_COLUMNS)
    writer.writeheader()

    while time.time() - start_time < run_time_seconds:
        elapsed_s = time.time() - start_time
        phase, instruction = get_phase(elapsed_s)

        if phase != last_phase:
            print()
            print("PHASE:", phase)
            print("INSTRUCTION:", instruction)
            last_phase = phase

        while True:
            msg = vehicle.recv_match(blocking=False)

            if msg is None:
                break

            msg_type = msg.get_type()

            if msg_type == "HEARTBEAT":
                last_mode = mavutil.mode_string_v10(msg)
                last_armed = bool(
                    msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
                )

            elif msg_type == "GLOBAL_POSITION_INT":
                relative_alt_m = msg.relative_alt / 1000.0

            elif msg_type == "ATTITUDE":
                roll_deg = math.degrees(msg.roll)
                pitch_deg = math.degrees(msg.pitch)
                yaw_deg = math.degrees(msg.yaw)

        image_rgb = picam2.capture_array()
        marker = detect_marker(image_rgb)

        marker_detected = marker["detected"]

        adjusted_error_x = None
        adjusted_error_y = None
        centered = False
        large_enough = False

        suggested_x_command = 0
        suggested_y_command = 0
        suggested_z_command = 0

        if marker_detected:
            adjusted_error_x, adjusted_error_y = get_adjusted_error(
                marker["error_x"],
                marker["error_y"],
            )

            centered = is_marker_at_target(
                marker["error_x"],
                marker["error_y"],
            )

            large_enough = is_marker_large_enough(marker["marker_size"])

            (
                suggested_x_command,
                suggested_y_command,
                suggested_z_command,
                adjusted_error_x,
                adjusted_error_y,
            ) = get_mounted_track_command(
                marker["error_x"],
                marker["error_y"],
            )

        row = {
            "elapsed_s": round(elapsed_s, 3),
            "phase": phase,
            "instruction": instruction,
            "mode": last_mode,
            "armed": last_armed,
            "relative_alt_m": None if relative_alt_m is None else round(relative_alt_m, 3),
            "roll_deg": None if roll_deg is None else round(roll_deg, 2),
            "pitch_deg": None if pitch_deg is None else round(pitch_deg, 2),
            "yaw_deg": None if yaw_deg is None else round(yaw_deg, 2),
            "marker_detected": marker_detected,
            "marker_id": marker["id"],
            "error_x": None if marker["error_x"] is None else round(marker["error_x"], 2),
            "error_y": None if marker["error_y"] is None else round(marker["error_y"], 2),
            "adjusted_error_x": None if adjusted_error_x is None else round(adjusted_error_x, 2),
            "adjusted_error_y": None if adjusted_error_y is None else round(adjusted_error_y, 2),
            "marker_size": None if marker["marker_size"] is None else round(marker["marker_size"], 2),
            "centered": centered,
            "large_enough": large_enough,
            "suggested_x_command": round(suggested_x_command, 3),
            "suggested_y_command": round(suggested_y_command, 3),
            "suggested_z_command": round(suggested_z_command, 3),
        }

        writer.writerow(row)

        if time.time() - last_print_time >= 0.5:
            if marker_detected:
                print(
                    "phase:",
                    phase,
                    "mode:",
                    last_mode,
                    "armed:",
                    last_armed,
                    "alt:",
                    row["relative_alt_m"],
                    "marker:",
                    marker["id"],
                    "error_x:",
                    row["error_x"],
                    "error_y:",
                    row["error_y"],
                    "adjusted_x:",
                    row["adjusted_error_x"],
                    "adjusted_y:",
                    row["adjusted_error_y"],
                    "size:",
                    row["marker_size"],
                    "centered:",
                    centered,
                    "large_enough:",
                    large_enough,
                    "suggested:",
                    row["suggested_x_command"],
                    row["suggested_y_command"],
                    row["suggested_z_command"],
                )
            else:
                print(
                    "phase:",
                    phase,
                    "mode:",
                    last_mode,
                    "armed:",
                    last_armed,
                    "alt:",
                    row["relative_alt_m"],
                    "marker: not detected",
                    "suggested:",
                    row["suggested_x_command"],
                    row["suggested_y_command"],
                    row["suggested_z_command"],
                )

            last_print_time = time.time()

        time.sleep(0.1)

picam2.stop()

print("Sign-mapping read-only logger complete")
print("Saved log:", log_path)
