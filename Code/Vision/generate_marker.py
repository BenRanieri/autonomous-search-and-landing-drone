import cv2
from cv2 import aruco

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

marker = aruco.generateImageMarker(dictionary, 0, 400)

cv2.imwrite("Code/Vision/aruco_marker.png", marker)

print("Marker saved.")