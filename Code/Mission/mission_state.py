import sys
from pathlib import Path
projectRoot = Path(__file__).resolve().parents[2]
sys.path.append(str(projectRoot))
from Code.Control.command_interface import send_velocity_command
from Code.Guidance.guidance_logic import (get_guidance_command, get_proportional_command, get_size_command, get_combined_guidance, get_elevation_command, get_final_movement)


def update_mission_state(currentState, currentAltitude, targetAltitude, markerDetected, readyToTrack=False):
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

  print("TRACK command tests")
  print()

  trackTestCases = [
    ("centered marker", 0, 0),
    ("marker right", 50, 0),
    ("marker left", -50, 0),
    ("marker low", 0, 50),
    ("marker high", 0, -50),
    ("small error inside tolerance", 5, -5),
  ]

  for testName, errorX, errorY in trackTestCases:
    xCommand, yCommand, zCommand = get_track_command(
      errorX,
      errorY,
      tolerance=10,
      kp=0.02,
      maxCommand=1
    )

    print(testName)
    print("xCommand:", xCommand)
    print("yCommand:", yCommand)
    print("zCommand:", zCommand)
    print()

  print("TRACK dry-run command tests")
  print()

  for testName, errorX, errorY in trackTestCases:
    xCommand, yCommand, zCommand = get_track_command(
      errorX,
      errorY,
      tolerance=10,
      kp=0.02,
      maxCommand=1
    )

    print(testName)
    send_velocity_command(xCommand, yCommand, zCommand)

  print("TRACK simulation test")
  print()

  finalErrorX, finalErrorY, trackCentered = run_track_simulation(
    startingErrorX=80,
    startingErrorY=-40,
    tolerance=10,
    kp=0.02,
    maxCommand=1,
    correctionScale=20,
    maxSteps=20
  )

  print("Final errorX:", round(finalErrorX, 2))
  print("Final errorY:", round(finalErrorY, 2))
  print("trackCentered:", trackCentered)