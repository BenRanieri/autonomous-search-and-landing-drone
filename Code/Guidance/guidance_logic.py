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
