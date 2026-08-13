from picamera2 import Picamera2
import cv2
import time

picam2 = Picamera2()

config = picam2.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)

picam2.configure(config)
picam2.start()
time.sleep(2)

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector = cv2.aruco.ArucoDetector(dictionary)

start_time = time.time()
last_print_time = 0
last_image_bgr = None

while time.time() - start_time < 12:
    image_rgb = picam2.capture_array()

    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    corners, ids, rejected = detector.detectMarkers(gray)

    image_height, image_width = image_bgr.shape[:2]
    image_center_x = image_width / 2
    image_center_y = image_height / 2

    now = time.time()

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(image_bgr, corners, ids)

        marker_corners = corners[0][0]
        marker_id = int(ids[0][0])

        center_x = marker_corners[:, 0].mean()
        center_y = marker_corners[:, 1].mean()

        error_x = center_x - image_center_x
        error_y = center_y - image_center_y

        cv2.circle(image_bgr, (int(center_x), int(center_y)), 5, (0, 255, 0), -1)
        cv2.circle(image_bgr, (int(image_center_x), int(image_center_y)), 5, (255, 0, 0), -1)

        if now - last_print_time > 0.5:
            print(
                "id:",
                marker_id,
                "center:",
                round(center_x, 1),
                round(center_y, 1),
                "error:",
                round(error_x, 1),
                round(error_y, 1),
            )
            last_print_time = now
    else:
        if now - last_print_time > 0.5:
            print("no marker detected")
            last_print_time = now

    last_image_bgr = image_bgr
    time.sleep(0.1)

picam2.stop()

if last_image_bgr is not None:
    cv2.imwrite("pi_aruco_live_last.jpg", last_image_bgr)
    print("Saved pi_aruco_live_last.jpg")
