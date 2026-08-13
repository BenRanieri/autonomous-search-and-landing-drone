import os
os.environ["LIBCAMERA_LOG_LEVELS"] = "*:3"

from picamera2 import Picamera2
import cv2
import time

TARGET_ID = 0

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


picam2 = Picamera2()

config = picam2.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)

picam2.configure(config)
picam2.start()
time.sleep(2)

start_time = time.time()

while time.time() - start_time < 15:
    image_rgb = picam2.capture_array()
    result = detect_marker(image_rgb)

    if result["detected"]:
        print(
            "detected:",
            result["detected"],
            "id:",
            result["id"],
            "error_x:",
            round(result["error_x"], 1),
            "error_y:",
            round(result["error_y"], 1),
        )
    else:
        print("detected: False")

    time.sleep(0.25)

picam2.stop()
