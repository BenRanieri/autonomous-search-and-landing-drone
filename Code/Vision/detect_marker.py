import cv2
from cv2 import aruco
import sys
from pathlib import Path
projectRoot = Path(__file__).resolve().parents[2]
sys.path.append(str(projectRoot))
from Code.Guidance.guidance_logic import get_guidance_command

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

markerImage = cv2.imread("Code/Vision/aruco_marker_border.png")

detector = aruco.ArucoDetector(dictionary)

corners, ids, rejectedImgPoints = detector.detectMarkers(markerImage)

print("IDs:", ids)

topLeftX = corners[0][0][0][0]
topLeftY = corners[0][0][0][1]
topRightX = corners[0][0][1][0]
topRightY = corners[0][0][1][1]
bottomRightX = corners[0][0][2][0]
bottomRightY = corners[0][0][2][1]
bottomLeftX = corners[0][0][3][0]
bottomLeftY = corners[0][0][3][1]

markerCenterX = (topLeftX + topRightX + bottomLeftX + bottomRightX) / 4
markerCenterY = (topLeftY + topRightY + bottomLeftY + bottomRightY) / 4
markerCenterCoords = [round(markerCenterX), round(markerCenterY)]

imageSize = markerImage.shape
imageCenterX = imageSize[1] / 2
imageCenterY = imageSize[0] / 2

errorX = markerCenterX - imageCenterX
errorY = markerCenterY - imageCenterY

commandX, commandY = get_guidance_command(errorX, errorY, 10)
print("errorX: ", errorX)
print("errorY: ", errorY)
print("commandX: ", commandX)
print("commandY: ", commandY)

markerImageCopy = markerImage.copy()
markerOutline = aruco.drawDetectedMarkers(markerImageCopy, corners)
markerOutline = cv2.circle(markerImageCopy, markerCenterCoords, 10, (0, 255, 0))

cv2.imwrite("Code/Vision/detected_marker_output.png", markerOutline)