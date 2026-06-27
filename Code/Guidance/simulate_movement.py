from guidance_logic import get_elevation_command, get_combined_guidance, get_final_movement, get_guidance_command, get_proportional_command, get_size_command
import matplotlib.pyplot as plt

def run_movement_simulation(startingErrorX, startingErrorY, startingMarkerSize, tolerance, kp, maxCommand, desiredSize, sizeTolerance, approachCommand, xyCorrectionScale, zCorrectionScale, maxSteps, printSteps):
 
  errorX = startingErrorX
  errorY = startingErrorY
  markerSize = startingMarkerSize  
  step = 0
  stepHistory = []
  errorXHistory = []
  errorYHistory = []
  markerSizeHistory = []
  xFinalHistory = []
  yFinalHistory = []
  zFinalHistory = []
  combinedCommandHistory = []
  while step < maxSteps:

    commandX, commandY = get_guidance_command(errorX, errorY, tolerance)
    xCommand, yCommand = get_proportional_command(errorX, errorY, tolerance, kp, maxCommand)
    sizeCommand = get_size_command(markerSize, desiredSize, sizeTolerance)
    combinedCommand = get_combined_guidance(commandX, commandY, sizeCommand)
    zCommand = get_elevation_command(sizeCommand, approachCommand)
    xFinal, yFinal, zFinal = get_final_movement(combinedCommand, xCommand, yCommand, zCommand)
    stepHistory.append(step)
    errorXHistory.append(errorX)
    errorYHistory.append(errorY)
    markerSizeHistory.append(markerSize)
    xFinalHistory.append(xFinal)
    yFinalHistory.append(yFinal)
    zFinalHistory.append(zFinal)
    combinedCommandHistory.append(combinedCommand)

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
      return errorX, errorY, markerSize, xFinal, yFinal, zFinal, stepHistory, errorXHistory, errorYHistory, markerSizeHistory, xFinalHistory, yFinalHistory, zFinalHistory, combinedCommandHistory
  
    if step == maxSteps - 1:
      print("Simulation ended before reaching final position")
      return errorX, errorY, markerSize, xFinal, yFinal, zFinal, stepHistory, errorXHistory, errorYHistory, markerSizeHistory, xFinalHistory, yFinalHistory, zFinalHistory, combinedCommandHistory

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
    errorX, errorY, markerSize, xFinal, yFinal, zFinal, stepHistory, errorXHistory, errorYHistory, markerSizeHistory, xFinalHistory, yFinalHistory, zFinalHistory, combinedCommandHistory = run_movement_simulation(startingErrorX, startingErrorY, startingMarkerSize, tolerance, kp, maxCommand, desiredSize, sizeTolerance, approachCommand, xyCorrectionScale, zCorrectionScale, maxSteps, printSteps)

    print("Starting errorX:", startingErrorX)
    print("Starting errorY:", startingErrorY)
    print("Starting markerSize:", startingMarkerSize)
    print("Final errorX:", errorX)
    print("Final errorY:", errorY)
    print("Final markerSize:", markerSize)
    print("Final movement:", xFinal, yFinal, zFinal)
    print()




  plotStartingErrorX = 200
  plotStartingErrorY = -100
  plotStartingMarkerSize = 250
  errorX, errorY, markerSize, xFinal, yFinal, zFinal, stepHistory, errorXHistory, errorYHistory, markerSizeHistory, xFinalHistory, yFinalHistory, zFinalHistory, combinedCommandHistory = run_movement_simulation(plotStartingErrorX, plotStartingErrorY, startingMarkerSize, tolerance, kp, maxCommand, desiredSize, sizeTolerance, approachCommand, xyCorrectionScale, zCorrectionScale, maxSteps, printSteps)

  plt.figure()
  plt.plot(stepHistory, errorXHistory, label="errorX")
  plt.plot(stepHistory, errorYHistory, label="errorY")
  plt.axhline(tolerance, linestyle="--", label="positive tolerance")
  plt.axhline(-tolerance, linestyle="--", label="negative tolerance")
  plt.xlabel("Step")
  plt.ylabel("Position Error")
  plt.title("Final Movement Position Error Over Time")
  plt.legend()
  plt.grid(True)
  plt.savefig("Code/Guidance/final_movement_error_plot.png")
  plt.close()
  print("Saved final movement error plot")

  plt.figure()
  plt.plot(stepHistory, markerSizeHistory, label="markerSize")
  plt.axhline(desiredSize + sizeTolerance, linestyle="--", label="upper size tolerance")
  plt.axhline(desiredSize - sizeTolerance, linestyle="--", label="lower size tolerance")
  plt.xlabel("Step")
  plt.ylabel("Marker Size")
  plt.title("Final Movement Marker Size Over Time")
  plt.legend()
  plt.grid(True)
  plt.savefig("Code/Guidance/final_movement_marker_size_plot.png")
  plt.close()
  print("Saved final movement marker size plot")

  plt.plot(stepHistory, xFinalHistory, label="xFinal")
  plt.plot(stepHistory, yFinalHistory, label="yFinal")
  plt.plot(stepHistory, zFinalHistory, label="zFinal")
  plt.xlabel("Step")
  plt.ylabel("Final Command")
  plt.title("Final Movement Commands Over Time")
  plt.legend()
  plt.grid(True)
  plt.savefig("Code/Guidance/final_movement_command_plot.png")
  plt.close()
  print("Saved final movement command plot")