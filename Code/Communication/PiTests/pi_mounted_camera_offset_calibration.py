import os
import sys
import time
from pathlib import Path

os.environ["LIBCAMERA_LOG_LEVELS"] = "*:3"

project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from picamera2 import Picamera2
import cv2


TARGET_ID = 0
SAMPLE_SECONDS = 8

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
        return None

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
            "id": marker_id,
            "error_x": error_x,
            "error_y": error_y,
            "marker_size": marker_size,
        }

    return None


def collect_samples(picam2, label):
    print()
    input("Place marker " + label + ", then press Enter...")

    samples = []
    start_time = time.time()

    while time.time() - start_time < SAMPLE_SECONDS:
        image_rgb = picam2.capture_array()
        marker = detect_marker(image_rgb)

        if marker is None:
            print(label, "marker: not detected")
        else:
            samples.append(marker)

            print(
                label,
                "marker:",
                marker["id"],
                "error_x:",
                round(marker["error_x"], 1),
                "error_y:",
                round(marker["error_y"], 1),
                "marker_size:",
                round(marker["marker_size"], 1),
            )

        time.sleep(0.25)

    if len(samples) == 0:
        return None

    avg_error_x = sum(sample["error_x"] for sample in samples) / len(samples)
    avg_error_y = sum(sample["error_y"] for sample in samples) / len(samples)
    avg_marker_size = sum(sample["marker_size"] for sample in samples) / len(samples)
    max_marker_size = max(sample["marker_size"] for sample in samples)

    return {
        "count": len(samples),
        "avg_error_x": avg_error_x,
        "avg_error_y": avg_error_y,
        "avg_marker_size": avg_marker_size,
        "max_marker_size": max_marker_size,
    }


picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)

picam2.configure(config)
picam2.start()
time.sleep(2)

print("Mounted camera offset calibration")
print("No Pixhawk commands are sent")
print("This test measures camera offset caused by the camera not being centered")

camera_result = collect_samples(
    picam2,
    "directly under the camera lens",
)

center_result = collect_samples(
    picam2,
    "under the desired drone landing center",
)

picam2.stop()

print()
print("Calibration summary")

if camera_result is None:
    print("Camera-lens sample: no marker detections")
else:
    print(
        "Camera-lens sample:",
        "detections:",
        camera_result["count"],
        "avg_error_x:",
        round(camera_result["avg_error_x"], 1),
        "avg_error_y:",
        round(camera_result["avg_error_y"], 1),
        "avg_marker_size:",
        round(camera_result["avg_marker_size"], 1),
        "max_marker_size:",
        round(camera_result["max_marker_size"], 1),
    )

if center_result is None:
    print("Drone-center sample: no marker detections")
else:
    print(
        "Drone-center sample:",
        "detections:",
        center_result["count"],
        "avg_error_x:",
        round(center_result["avg_error_x"], 1),
        "avg_error_y:",
        round(center_result["avg_error_y"], 1),
        "avg_marker_size:",
        round(center_result["avg_marker_size"], 1),
        "max_marker_size:",
        round(center_result["max_marker_size"], 1),
    )

print("Calibration complete")
