import cv2
from cv2 import aruco
import numpy as np

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

marker = aruco.generateImageMarker(dictionary, 0, 640)

canvas = np.ones((960, 960), dtype=np.uint8) * 255
canvas[160:800, 160:800] = marker

cv2.imwrite("Code/Vision/aruco_marker_border_8in.png", canvas)

print("Saved 8x8 marker image")