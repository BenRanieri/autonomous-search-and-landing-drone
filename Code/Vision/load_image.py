import cv2

image = cv2.imread("Code/Vision/test_image.jpg")  

if image is None:
    print("Image not found")
else:
    print("Image loaded successfully")
    print("Shape:", image.shape)