import sys
from pathlib import Path
projectRoot = Path(__file__).resolve().parents[2]
sys.path.append(str(projectRoot))
from Code.Control.command_interface import send_velocity_command
from Code.Guidance.guidance_logic import (get_guidance_command, get_proportional_command, get_size_command, get_combined_guidance, get_elevation_command, get_final_movement)


def update_mission_state(currentState, currentAltitude, targetAltitude, markerDetected):
  newState = currentState
  if currentState == "TAKEOFF":
    if currentAltitude < targetAltitude:
      newState = "TAKEOFF"
    else:
      newState = "SEARCH"

  elif currentState == "SEARCH":
    if markerDetected:
      newState = "ACQUIRE"
    else:
      newState = "SEARCH"

  return newState


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


if __name__ == "__main__":

  print("Acquire command tests:")

  testCases = [
    ("Off-center and too far away", 200, -100, 250),
    ("Centered but too far away", 0, 0, 250),
    ("Centered and correct size", 0, 0, 400),
    ("Centered but too close", 0, 0, 500)
  ]

  for testName, errorX, errorY, markerSize in testCases:

    xFinal, yFinal, zFinal, combinedCommand = get_acquire_command(
      errorX, errorY, markerSize,
      10, 0.01, 1.0,
      400, 20, 0.3
    )

    print("Test case:", testName)
    print("Combined command:", combinedCommand)
    print("Final command:", xFinal, yFinal, zFinal)
    send_velocity_command(xFinal, yFinal, zFinal)