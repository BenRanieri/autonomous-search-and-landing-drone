def send_velocity_command(xCommand, yCommand, zCommand, dryRun=True, maxCommand=1):
  if dryRun:
    print("Dry-run velocity command")
    print("xCommand:", limit_command(xCommand,maxCommand))
    print("yCommand:", limit_command(yCommand, maxCommand))
    print("zCommand:", limit_command(zCommand, maxCommand))
    print()
  else:
    print("Real command mode is not implemented yet")


def send_stop_command(dryRun=True):
  send_velocity_command(0, 0, 0, dryRun)


def limit_command(command, maxCommand):
  if command > maxCommand:
    return maxCommand
  elif -command > maxCommand:
    return -maxCommand
  else:
    return command

    
if __name__ == "__main__":

  send_velocity_command(0.5, -0.2, -0.3)
  send_stop_command()
  send_velocity_command(5, -3, 2)