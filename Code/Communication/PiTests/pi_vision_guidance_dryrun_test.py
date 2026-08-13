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

from Code.Mission.mission_state import get_track_command

TARGET_ID = 0
TOLERANCE = 30
KP = 0.002
MAX_COMMAND = 0.25

connection_string = "/dev/ttyAMA0"
baud_rate = 921600

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

        return {
            "detected": True,
            "id": marker_id,
            "error_x": error_x,
            "error_y": error_y,
        }

    return {
        "detected": False,
        "id": None,
        "error_x": None,
        "error_y": None,
    }


print("Connecting to Pixhawk...")
vehicle = mavutil.mavlink_connection(connection_string, baud=baud_rate)

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

print("Running dry-run vision + guidance test for 15 seconds...")
print("No commands will be sent to the Pixhawk.")

last_mode = "unknown"
last_armed = False
start_time = time.time()

while time.time() - start_time < 15:
    image_rgb = picam2.capture_array()
    marker = detect_marker(image_rgb)

    msg = vehicle.recv_match(type="HEARTBEAT", blocking=False)

    if msg is not None:
        last_mode = mavutil.mode_string_v10(msg)
        last_armed = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)

    if marker["detected"]:
        x_command, y_command, z_command = get_track_command(
            marker["error_x"],
            marker["error_y"],
            TOLERANCE,
            KP,
            MAX_COMMAND,
        )

        print(
            "mode:",
            last_mode,
            "armed:",
            last_armed,
            "marker:",
            marker["id"],
            "error_x:",
            round(marker["error_x"], 1),
            "error_y:",
            round(marker["error_y"], 1),
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
            "marker: not detected",
            "DRY_RUN_command: 0 0 0",
        )

    time.sleep(0.25)

picam2.stop()

print("Dry-run guidance test complete")
