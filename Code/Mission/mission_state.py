import sys
from pathlib import Path
projectRoot = Path(__file__).resolve().parents[2]
sys.path.append(str(projectRoot))
from Code.Control.command_interface import send_velocity_command


def update_mission_state(currentState, currentAltitude, targetAltitude):
  newState = currentState
  if currentState == "TAKEOFF":
    if currentAltitude < targetAltitude:
      newState = "TAKEOFF"
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
  else:
    xCommand = 0
    yCommand = 0
    zCommand = 0

  return xCommand, yCommand, zCommand


def run_takeoff_simulation(startingAltitude, targetAltitude, altitudeScale, maxsteps):

  currentState = "TAKEOFF"
  currentAltitude = startingAltitude
  step = 0

  while currentState == "TAKEOFF" and step < maxsteps:

    xCommand, yCommand, zCommand = get_state_command(currentState)
    send_velocity_command(xCommand, yCommand, zCommand)

    currentAltitude = update_altitude(currentAltitude, zCommand, altitudeScale)
    currentState = update_mission_state(currentState, currentAltitude, targetAltitude)

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
  


if __name__ == "__main__":

  print("Takeoff simulation:")
  finalState, finalAltitude, takeoffComplete = run_takeoff_simulation(0, 2, 0.2, 50)
  print("Final state:", finalState)
  print("Final altitude:", round(finalAltitude,2))
  print("Takeoff complete:", takeoffComplete)