#import cv2
#from cv2 import aruco

#dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

#marker = aruco.generateImageMarker(dictionary, 0, 400)

#cv2.imwrite("Code/Vision/aruco_marker.png", marker)

#print("Marker saved.") 

import cv2
from cv2 import aruco
import numpy as np

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

marker = aruco.generateImageMarker(dictionary, 0, 400)

canvas = np.ones((600, 600), dtype=np.uint8) * 255
canvas[100:500, 100:500] = marker

cv2.imwrite("Code/Vision/aruco_marker_border.png", canvas)

print("Saved")