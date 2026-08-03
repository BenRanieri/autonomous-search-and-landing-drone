def log_command(commandType, xCommand, yCommand, zCommand, dryRun):
  print("Command Type:", commandType)
  print("Dry Run:", dryRun)
  print("xCommand:", xCommand)
  print("yCommand:", yCommand)
  print("zCommand:", zCommand)
  print()


def send_velocity_command(xCommand, yCommand, zCommand, dryRun=True, maxCommand=1):
  xLimited = limit_command(xCommand, maxCommand)
  yLimited = limit_command(yCommand, maxCommand)
  zLimited = limit_command(zCommand, maxCommand)

  if dryRun:
    log_command("velocity", xLimited, yLimited, zLimited, dryRun)
  else:
    print("Real velocity command mode is not implemented yet")
    log_command("velocity placeholder", xLimited, yLimited, zLimited, dryRun)


def send_stop_command(dryRun=True):
  send_velocity_command(0, 0, 0, dryRun)


def send_emergency_stop(dryRun=True):
  print("Emergency stop requested")
  send_velocity_command(0, 0, 0, dryRun)


def connect_to_vehicle(connectionString, dryRun=True):
  if dryRun:
    print("Dry-run vehicle connection")
    print("Connection String:", connectionString)
    print("No real vehicle connection made")
    print()
    return None
  else:
    print("Real vehicle connection is not implemented yet")
    return None


def send_mission_command(xCommand, yCommand, zCommand, vehicle=None, dryRun=True, maxCommand=1):
  if dryRun:
    send_velocity_command(xCommand, yCommand, zCommand, dryRun, maxCommand)
  else:
    print("Real mission command mode is not implemented yet")
    send_velocity_command(xCommand, yCommand, zCommand, dryRun, maxCommand)


def limit_command(command, maxCommand):
  if command > maxCommand:
    return maxCommand
  elif command < -maxCommand:
    return -maxCommand
  else:
    return command

    
if __name__ == "__main__":

  print("Velocity Command Tests")
  print()

  send_velocity_command(0.5, -0.2, -0.3)
  send_stop_command()
  send_velocity_command(5, -3, 2)

  print("Emergency Stop Test")
  print()

  send_emergency_stop()

  print("Vehicle Connection Test")
  print()

  connect_to_vehicle("udp:127.0.0.1:14550")

  print("Mission Command Test")
  print()

  send_mission_command(0.4, -0.4, -0.2)
  send_mission_command(3, -3, 2)