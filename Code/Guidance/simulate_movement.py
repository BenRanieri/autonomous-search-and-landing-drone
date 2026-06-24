from guidance_logic import get_elevation_command, get_combined_guidance, get_final_movement, get_guidance_command, get_proportional_command, get_size_command

errorX = -150
errorY = 120
markerSize = 500
tolerance = 10
kp = 0.01
maxCommand = 1
desiredSize = 400
sizeTolerance = 20
approachCommand = 0.3
xyCorrectionScale = 20
zCorrectionScale = 50
maxSteps = 50
printSteps = True
step = 0

while step < maxSteps:

  commandX, commandY = get_guidance_command(errorX, errorY, tolerance)
  xCommand, yCommand = get_proportional_command(errorX, errorY, tolerance, kp, maxCommand)
  sizeCommand = get_size_command(markerSize, desiredSize, sizeTolerance)
  combinedCommand = get_combined_guidance(commandX, commandY, sizeCommand)
  zCommand = get_elevation_command(sizeCommand, approachCommand)
  xFinal, yFinal, zFinal = get_final_movement(combinedCommand, xCommand, yCommand, zCommand)

  if printSteps:
    print("step:", step )
    print("errorX:", errorX)
    print("errorY:", errorY)
    print("markerSize:", markerSize)
    print("commandX:", commandX)
    print("commandY:", commandY)
    print("xCommand:", xCommand)
    print("yCommand:", yCommand)
    print("sizeCommand:", sizeCommand)
    print("combinedCommand:", combinedCommand)
    print("zCommand:", zCommand)
    print("xFinal:", xFinal)
    print("yFinal:", yFinal)
    print("zFinal:", zFinal)
    print()
  
  if xFinal == 0 and yFinal == 0 and zFinal == 0:
    print("Target centered and correct distance")
    break
  
  if step == maxSteps - 1:
    print("Simulation ended before reaching final position")

  errorX = errorX - xFinal * xyCorrectionScale
  errorY = errorY - yFinal * xyCorrectionScale
  markerSize = markerSize - zFinal * zCorrectionScale
  step = step + 1