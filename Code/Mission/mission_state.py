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


if __name__ == "__main__":

  print(update_mission_state("TAKEOFF", 0, 2))
  print(update_mission_state("TAKEOFF", 1.5, 2))
  print(update_mission_state("TAKEOFF", 2, 2))
  print(update_mission_state("SEARCH", 0, 2))
  print(update_mission_state("LAND", 0, 2))
  print(get_state_command("TAKEOFF"))
  print(get_state_command("SEARCH"))
  print(get_state_command("LAND"))

  print("Dry-run mission command:")
  xCommand, yCommand, zCommand = get_state_command("TAKEOFF")
  send_velocity_command(xCommand, yCommand, zCommand)

  print("Mission transition command test:")
  currentState = "TAKEOFF"
  currentAltitude = 2
  targetAltitude = 2
  newState = update_mission_state(currentState, currentAltitude, targetAltitude)
  print("New state:", newState)
  xCommand, yCommand, zCommand = get_state_command(newState)
  send_velocity_command(xCommand, yCommand, zCommand)