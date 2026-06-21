import cv2
from cv2 import aruco
import sys
from pathlib import Path
projectRoot = Path(__file__).resolve().parents[2]
sys.path.append(str(projectRoot))
from Code.Guidance.guidance_logic import get_guidance_command, get_proportional_command, get_size_command

# Detects an ArUco marker then returns its markerID and position error relative to image center
# Returns None values if image is not loaded or marker is not detected
# Second input allows saving visualization of the marker
def detect_marker_position(imagePath, saveVisualization):

  dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

  markerImage = cv2.imread(imagePath)
  if markerImage is None: 
    print("Image could not be loaded") 
    return None, None, None, None

  detector = aruco.ArucoDetector(dictionary)

  corners, ids, rejectedImgPoints = detector.detectMarkers(markerImage)

  if ids is None:
    print("No Marker Detected")
    return None, None, None, None
  
  markerID = ids[0][0]

  markerCorners = corners[0][0]  
  markerCenterX = markerCorners[:, 0].mean()
  markerCenterY = markerCorners[:, 1].mean()

  topLeft = markerCorners[0]
  topRight = markerCorners[1]
  bottomRight = markerCorners[2]
  bottomLeft = markerCorners[3]

  topLength = ((topRight[0] - topLeft[0])**2 + (topRight[1] - topLeft[1])**2)**0.5
  bottomLength = ((bottomRight[0] - bottomLeft[0])**2 + (bottomRight[1] - bottomLeft[1])**2)**0.5
  leftLength = ((bottomLeft[0] - topLeft[0])**2 + (bottomLeft[1] - topLeft[1])**2)**0.5
  rightLength = ((bottomRight[0] - topRight[0])**2 + (bottomRight[1] - topRight[1])**2)**0.5

  markerSize = (topLength + bottomLength + leftLength + rightLength) / 4

  imageSize = markerImage.shape
  imageCenterX = imageSize[1] / 2
  imageCenterY = imageSize[0] / 2

  errorX = markerCenterX - imageCenterX
  errorY = markerCenterY - imageCenterY

  if saveVisualization:
    markerImageCopy = markerImage.copy()
    markerOutline = aruco.drawDetectedMarkers(markerImageCopy, corners)
    markerCenterCoords = (round(markerCenterX), round(markerCenterY))
    markerOutline = cv2.circle(markerImageCopy, markerCenterCoords, 10, (0, 255, 0))

    cv2.imwrite("Code/Vision/detected_marker_output.png", markerOutline)
    print("Visualization saved to Code/Vision/detected_marker_output.png")

  return errorX, errorY, markerID, markerSize



if __name__ == "__main__":

  #imagePath = "FakeImage"
  imagePath = "Code/Vision/aruco_marker_border.png"
  saveVisualization = True
  errorX, errorY, markerID, markerSize = detect_marker_position(imagePath, saveVisualization)

  if errorX is None or errorY is None:
    print("No guidance command available")
    
  else:
    tolerance = 10
    commandX, commandY = get_guidance_command(errorX, errorY, tolerance)

    print("Marker detected")
    print("MarkerID:", markerID)
    print("Marker size:", markerSize)
    print("errorX:", errorX)
    print("errorY:", errorY)
    print("commandX:", commandX)
    print("commandY:", commandY)

    kp = 0.01
    maxCommand = 1
    xCommand, yCommand = get_proportional_command(errorX, errorY, tolerance, kp, maxCommand)

    print("xCommand:", xCommand)
    print("yCommand:", yCommand)

    desiredSize = 400
    sizeTolerance = 20
    sizeCommand = get_size_command(markerSize, desiredSize, sizeTolerance)
    print("Size command:", sizeCommand)
