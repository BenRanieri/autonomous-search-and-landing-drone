import sys
from pathlib import Path
projectRoot = Path(__file__).resolve().parents[2]
sys.path.append(str(projectRoot))
from Code.Control.command_interface import send_velocity_command
from Code.Guidance.guidance_logic import (get_guidance_command, get_proportional_command, get_size_command, get_combined_guidance, get_elevation_command, get_final_movement)


def update_mission_state(currentState, currentAltitude, targetAltitude, markerDetected, readyToTrack=False, markerLost=False, readyForApproach=False):
    if currentState == "TAKEOFF":
        if currentAltitude >= targetAltitude:
            return "SEARCH"
        else:
            return "TAKEOFF"

    elif currentState == "SEARCH":
        if markerDetected:
            return "ACQUIRE"
        else:
            return "SEARCH"

    elif currentState == "ACQUIRE":
        if readyToTrack:
            return "TRACK"
        else:
            return "ACQUIRE"

    elif currentState == "TRACK":
       if markerLost:
          return "SEARCH"
       elif readyForApproach:
          return "APPROACH"
       else:
          return "TRACK"

    else:
        return currentState


def update_altitude(currentAlt, zCommand, altScale):
  newAlt = currentAlt + zCommand * altScale
  return newAlt


def get_state_command(currentState):

  if currentState == "TAKEOFF":
    xCommand = 0
    yCommand = 0
    zCommand = 0.5
  elif currentState == "SEARCH":
    xCommand = 0
    yCommand = 0.2
    zCommand = 0
  elif currentState == "TRACK":
    xCommand = 0
    yCommand = 0
    zCommand = 0
  else:
    xCommand = 0
    yCommand = 0
    zCommand = 0

  return xCommand, yCommand, zCommand


def get_acquire_command(errorX, errorY, markerSize, tolerance, kp, maxCommand, desiredSize, sizeTolerance, approachCommand):
  commandX, commandY = get_guidance_command(errorX, errorY, tolerance)
  xCommand, yCommand = get_proportional_command(errorX, errorY, tolerance, kp, maxCommand)
  sizeCommand = get_size_command(markerSize, desiredSize, sizeTolerance)
  combinedCommand = get_combined_guidance(commandX, commandY, sizeCommand)
  zCommand = get_elevation_command(sizeCommand, approachCommand)
  xFinal, yFinal, zFinal = get_final_movement(combinedCommand, xCommand, yCommand, zCommand)

  return xFinal, yFinal, zFinal, combinedCommand


def get_track_command(errorX, errorY, tolerance, kp, maxCommand):
  xCommand, yCommand = get_proportional_command(errorX, errorY, tolerance, kp, maxCommand)
  zCommand = 0

  return xCommand, yCommand, zCommand


def is_marker_acquired(errorX, errorY, markerSize, tolerance, desiredSize, sizeTolerance):
    xCentered = abs(errorX) <= tolerance
    yCentered = abs(errorY) <= tolerance
    sizeCorrect = abs(markerSize - desiredSize) <= sizeTolerance

    if xCentered and yCentered and sizeCorrect:
        return True
    else:
        return False
    

def update_acquire_stability(acquired, stableCount, requiredStableCount):
    if acquired:
        stableCount = stableCount + 1
    else:
        stableCount = 0

    if stableCount >= requiredStableCount:
        readyToTrack = True
    else:
        readyToTrack = False

    return stableCount, readyToTrack


def update_track_marker_loss(markerDetected, lostMarkerCount, maxLostMarkerCount):
  if not markerDetected:
    lostMarkerCount = lostMarkerCount + 1
    if lostMarkerCount >= maxLostMarkerCount:
      markerLost = True
    else:
      markerLost = False
  else:
      lostMarkerCount = 0
      markerLost = False

  return lostMarkerCount, markerLost


def is_track_ready_for_approach(errorX, errorY, tolerance):
  if errorX < tolerance or -errorX > tolerance:
    if errorY < tolerance or -errorY > tolerance:
      return True
  return False


def update_track_stability(trackReady, trackStableCount, requiredStableCount):
  if trackReady:
    trackStableCount = trackStableCount + 1
  else:
    trackStableCount = 0
  if trackStableCount >= requiredStableCount:
    readyToApproach = True
  else:
     readyToApproach = False
  return trackStableCount, readyToApproach 

         
def run_takeoff_simulation(startingAltitude, targetAltitude, altitudeScale, maxsteps):

  currentState = "TAKEOFF"
  currentAltitude = startingAltitude
  step = 0

  while currentState == "TAKEOFF" and step < maxsteps:

    xCommand, yCommand, zCommand = get_state_command(currentState)
    send_velocity_command(xCommand, yCommand, zCommand)

    currentAltitude = update_altitude(currentAltitude, zCommand, altitudeScale)
    currentState = update_mission_state(currentState, currentAltitude, targetAltitude, False)

    print("Step:", step)
    print("Altitude:", round(currentAltitude,2))
    print("State:", currentState)
    print()

    step = step + 1

  if currentState == "TAKEOFF":
    print("Takeoff simulation stopped before reaching target altitude")
    xCommand = 0
    yCommand = 0
    zCommand = 0
  else:
    xCommand, yCommand, zCommand = get_state_command(currentState)

  send_velocity_command(xCommand, yCommand, zCommand)
  takeoffComplete = currentState != "TAKEOFF"
  return currentState, currentAltitude, takeoffComplete
  

def run_basic_mission_simulation(startingAltitude, targetAltitude, altitudeScale, maxSteps, markerDetectionStep):

  currentState = "TAKEOFF"
  currentAltitude = startingAltitude
  step = 0
  markerDetected = False

  while currentState != "ACQUIRE" and step < maxSteps:

    if step >= markerDetectionStep:
      markerDetected = True

    xCommand, yCommand, zCommand = get_state_command(currentState)
    send_velocity_command(xCommand, yCommand, zCommand)

    if currentState == "TAKEOFF":
      currentAltitude = update_altitude(currentAltitude, zCommand, altitudeScale)

    currentState = update_mission_state(currentState, currentAltitude, targetAltitude, markerDetected)

    print("Step:", step)
    print("Altitude:", round(currentAltitude, 2))
    print("Marker detected:", markerDetected)
    print("State:", currentState)
    print()

    step = step + 1

  xCommand, yCommand, zCommand = get_state_command(currentState)
  send_velocity_command(xCommand, yCommand, zCommand)

  missionReachedAcquire = currentState == "ACQUIRE"
  if currentState != "ACQUIRE":
    print("Mission simulation stopped before reaching ACQUIRE")

  return currentState, currentAltitude, missionReachedAcquire


def run_track_simulation(startingErrorX, startingErrorY, tolerance, kp, maxCommand, correctionScale, maxSteps):

  errorX = startingErrorX
  errorY = startingErrorY
  step = 0

  while step < maxSteps:

    xCommand, yCommand, zCommand = get_track_command(errorX, errorY, tolerance, kp, maxCommand)
    send_velocity_command(xCommand, yCommand, zCommand)

    print("Step:", step)
    print("errorX:", round(errorX, 2))
    print("errorY:", round(errorY, 2))
    print("xCommand:", xCommand)
    print("yCommand:", yCommand)
    print("zCommand:", zCommand)
    print()

    if xCommand == 0 and yCommand == 0:
      print("TRACK centered")
      return errorX, errorY, True

    errorX = errorX - xCommand * correctionScale
    errorY = errorY - yCommand * correctionScale

    step = step + 1

  print("TRACK simulation stopped before centering")
  return errorX, errorY, False


if __name__ == "__main__":

  print("Track Stability Tests")
  print()

  tolerance = 10
  requiredTrackStableCount = 3
  trackStableCount = 0
  trackErrorSequence = [
    ("off center", 40, -20),
    ("almost centered", 12, -8),
    ("centered once", 5, 4),
    ("centered twice", 3, -2),
    ("bad frame", 30, 0),
    ("centered again 1", 2, 1),
    ("centered again 2", 0, 0),
    ("centered again 3", -4, 3),
  ]

  for frame, errorX, errorY in trackErrorSequence:
    trackReady = is_track_ready_for_approach(errorX, errorY, tolerance)
    trackStableCount, readyForApproach = update_track_stability(trackReady, trackStableCount, requiredTrackStableCount)
    print("Frame:", frame)
    print("ErrorX:", errorX)
    print("ErrorY:", errorY)
    print("Track Ready:", trackReady)
    print("Track Stable Count:", trackStableCount)
    print("Ready For Approach:", readyForApproach)
    print()


  print("Update Mission State tests")
  print()
  missionState = update_mission_state("TRACK", 10, 10, True, False, True, False)
  print(missionState)
  print()
  missionState = update_mission_state("TRACK", 10, 10, True, False, False, True)
  print(missionState)
  print()
  missionState = update_mission_state("TRACK", 10, 10, True, False, False, False)
  print(missionState)
  print()


  print("Final Combined Test")
  print()
  
  tolerance = 10
  requiredTrackStableCount = 3
  trackStableCount = 0
  currentState = "TRACK"
  trackErrorSequence = [
    ("off center", 40, -20),
    ("almost centered", 12, -8),
    ("centered once", 5, 4),
    ("centered twice", 3, -2),
    ("bad frame", 30, 0),
    ("centered again 1", 2, 1),
    ("centered again 2", 0, 0),
    ("centered again 3", -4, 3),
  ]

  for frame, errorX, errorY in trackErrorSequence:
    trackReady = is_track_ready_for_approach(errorX, errorY, tolerance)
    trackStableCount, readyForApproach = update_track_stability(trackReady, trackStableCount, requiredTrackStableCount)
    currentState = update_mission_state(currentState, 10, 10, True, False, False, readyForApproach)
    print("Frame:", frame)
    print("ErrorX:", errorX)
    print("ErrorY:", errorY)
    print("Track Ready:", trackReady)
    print("Track Stable Count:", trackStableCount)
    print("Ready For Approach:", readyForApproach)
    print("Current State:", currentState)
    print()