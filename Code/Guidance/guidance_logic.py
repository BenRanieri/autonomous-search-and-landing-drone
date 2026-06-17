def get_guidance_command(errorX, errorY, tolerance):
  if errorX > tolerance:
    #print("Move Right")
    commandX = "right"
  elif errorX < -tolerance:
    #print("Move Left")
    commandX = "left"
  else:
    #print("Maintain X")
    commandX = "maintain"

  if errorY > tolerance:
    #print("Move Backward")
    commandY = "backward"
  elif errorY < -tolerance:
    #print("Move Forward")
    commandY = "forward"
  else:
    #print("Maintain Y")
    commandY = "maintain"

  return commandX, commandY


#errorX = 100
#errorY = -100
#tolerance = 10
#commandX, commandY = get_guidance_command(errorX, errorY, tolerance)
#print(commandX)
#print(commandY)




def get_proportional_command(errorX, errorY, tolerance, kp, maxCommand):
  if abs(errorX) <= tolerance:
    commandX = 0
  else:
    commandX = errorX * kp
    if abs(commandX) > maxCommand:
      commandX = (commandX / abs(commandX)) * maxCommand

  if abs(errorY) <= tolerance:
    commandY = 0
  else:
    commandY = errorY * kp
    if abs(commandY) > maxCommand:
      commandY = (commandY / abs(commandY)) * maxCommand

  return commandX, commandY




#errorX = 5
#errorY = -3
#tolerance = 10
#kp = 0.01
#commandX, commandY = get_proportional_command(errorX, errorY, tolerance, kp)
#print("commandX:", commandX)
#print("commandY:", commandY)