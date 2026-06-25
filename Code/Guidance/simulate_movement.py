from guidance_logic import get_elevation_command, get_combined_guidance, get_final_movement, get_guidance_command, get_proportional_command, get_size_command

def run_movement_simulation(startingErrorX, startingErrorY, startingMarkerSize, tolerance, kp, maxCommand, desiredSize, sizeTolerance, approachCommand, xyCorrectionScale, zCorrectionScale, maxSteps, printSteps):
 
 errorX = startingErrorX
 errorY = startingErrorY
 markerSize = startingMarkerSize  
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
      return errorX, errorY, markerSize, xFinal, yFinal, zFinal
  
    if step == maxSteps - 1:
      print("Simulation ended before reaching final position")
      return errorX, errorY, markerSize, xFinal, yFinal, zFinal

    errorX = errorX - xFinal * xyCorrectionScale
    errorY = errorY - yFinal * xyCorrectionScale
    markerSize = markerSize - zFinal * zCorrectionScale
    step = step + 1

 

if __name__ == "__main__":

  testCases = [
    (200, -100, 250),
    (-150, 120, 500),
    (0, 0, 250),
    (0, 0, 500),
    (5, -5, 400),
    (300, 300, 400),
    (-300, -300, 250)
  ]

  tolerance = 10
  kp = 0.01
  maxCommand = 1
  desiredSize = 400
  sizeTolerance = 20
  approachCommand = 0.3
  xyCorrectionScale = 20
  zCorrectionScale = 50
  maxSteps = 50
  printSteps = False

  for startingErrorX, startingErrorY, startingMarkerSize in testCases:
    errorX, errorY, markerSize, xFinal, yFinal, zFinal = run_movement_simulation(startingErrorX, startingErrorY, startingMarkerSize, tolerance, kp, maxCommand, desiredSize, sizeTolerance, approachCommand, xyCorrectionScale, zCorrectionScale, maxSteps, printSteps)

    print("Starting errorX:", startingErrorX)
    print("Starting errorY:", startingErrorY)
    print("Starting markerSize:", startingMarkerSize)
    print("Final errorX:", errorX)
    print("Final errorY:", errorY)
    print("Final markerSize:", markerSize)
    print("Final movement:", xFinal, yFinal, zFinal)
    print()