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

image = picam2.capture_array()

print("Image shape:", image.shape)

image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
cv2.imwrite("python_camera_test.jpg", image_bgr)

picam2.stop()

print("Saved python_camera_test.jpg")
