from picamera2 import Picamera2
import cv2
import time

picam2 = Picamera2()

config = picam2.create_still_configuration(
    main={"size": (1280, 720), "format": "RGB888"}
)

picam2.configure(config)
picam2.start()

time.sleep(2)

image_rgb = picam2.capture_array()
picam2.stop()

image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector = cv2.aruco.ArucoDetector(dictionary)

corners, ids, rejected = detector.detectMarkers(gray)

print("ids:", ids)
print("number of rejected candidates:", len(rejected))

if ids is not None:
    cv2.aruco.drawDetectedMarkers(image_bgr, corners, ids)

    for i in range(len(ids)):
        marker_id = int(ids[i][0])
        marker_corners = corners[i][0]

        center_x = marker_corners[:, 0].mean()
        center_y = marker_corners[:, 1].mean()

        image_height, image_width = image_bgr.shape[:2]
        image_center_x = image_width / 2
        image_center_y = image_height / 2

        error_x = center_x - image_center_x
        error_y = center_y - image_center_y

        print("marker id:", marker_id)
        print("marker center:", center_x, center_y)
        print("image center:", image_center_x, image_center_y)
        print("error:", error_x, error_y)

cv2.imwrite("pi_aruco_detection.jpg", image_bgr)
print("Saved pi_aruco_detection.jpg")
