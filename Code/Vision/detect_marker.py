import cv2
from cv2 import aruco

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

markerImage = cv2.imread("Code/Vision/aruco_marker_border.png")

detector = aruco.ArucoDetector(dictionary)

corners, ids, rejectedImgPoints = detector.detectMarkers(markerImage)

print("IDs:", ids)

#Removed after debugging
#print(markerImage is None)
#print(type(dictionary))
#print(type(detector))
#print(markerImage.shape)
#print("Corners:", corners)
#print("Rejected:", len(rejectedImgPoints))
#print(markerImage[0][0])
#print(markerImage[200][200])
