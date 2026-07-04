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
      return errorX, errorY, markerSize, xFinal, yFinal, zFinal, stepHistory, errorXHistory, errorYHistory, markerSizeHistory, xFinalHistory, yFinalHistory, zFinalHistory, combinedCommandHistory, step
  
    if step == maxSteps - 1:
      print("Simulation ended before reaching final position")
      return errorX, errorY, markerSize, xFinal, yFinal, zFinal, stepHistory, errorXHistory, errorYHistory, markerSizeHistory, xFinalHistory, yFinalHistory, zFinalHistory, combinedCommandHistory, step

    errorX = errorX - xFinal * xyCorrectionScale
    errorY = errorY - yFinal * xyCorrectionScale
    markerSize = markerSize - zFinal * zCorrectionScale
    step = step + 1


def save_plot(stepHistory, plottedHistories, labels, xLabel, yLabel, title, savePath, horizontalLines=None, horizontalLabels=None):

  plt.figure()

  for plottedHistory, label in zip(plottedHistories, labels):
    plt.plot(stepHistory, plottedHistory, label=label)

  if horizontalLines is not None:
    for horizontalLine, horizontalLabel in zip(horizontalLines, horizontalLabels):
      plt.axhline(horizontalLine, linestyle="--", label=horizontalLabel)

  plt.xlabel(xLabel)
  plt.ylabel(yLabel)
  plt.title(title)
  plt.legend()
  plt.grid(True)
  plt.savefig(savePath)
  plt.close()

  print("Saved plot:", savePath)


def summarize_command_history(commandHistory):
  commandSummary = {}
  for command in commandHistory:
    if command not in commandSummary:
      commandSummary[command] = 1
    else:
      commandSummary[command] = commandSummary[command] + 1
    
  return commandSummary

 
def print_command_summary(commandSummary):
  print("Command summary:")
  for command, count in commandSummary.items():
    if count == 1:
      print(command + ":", count, "step")
    else:
      print(command + ":", count, "steps")


if __name__ == "__main__":

  testCases = [
    ("normal", "Very far right and too far away", 400, -300, 200),
    ("normal", "Very far left and too close", -400, 300, 650),
    ("normal", "Almost centered but too far away", 30, 30, 200),
    ("normal", "Almost centered but too close", 30, 30, 650),
    ("normal", "Large X/Y error but correct distance", 500, -500, 400),
    ("normal", "Perfect position but too far away", 0, 0, 200),
    ("normal", "Perfect position but too close", 0, 0, 650),

    ("stress", "Extreme right error and very far away", 20000, -100, 50),
    ("stress", "Extreme left error and too close", -15000, 120, 900),
    ("stress", "Centered but extreme marker size", 0, 0, 40000),
    ("stress", "Extreme X/Y error and correct distance", -30000, 20000, 400)
  ]

  tolerance = 10
  kp = 0.01
  maxCommand = 1
  desiredSize = 400
  sizeTolerance = 20
  approachCommand = 0.3
  xyCorrectionScale = 20
  zCorrectionScale = 50
  maxSteps = 5000
  printSteps = False

  parameterSets = [
    ("Current default", 0.01, 1.0, 10, 0.3, 20, 50),
    ("Slower response", 0.005, 1.0, 10, 0.2, 15, 40),
    ("Faster response", 0.02, 1.0, 10, 0.4, 25, 60),
    ("Aggressive response", 0.04, 1.5, 10, 0.6, 35, 80)
  ]

  for testType, testName, startingErrorX, startingErrorY, startingMarkerSize in testCases:
    errorX, errorY, markerSize, xFinal, yFinal, zFinal, stepHistory, errorXHistory, errorYHistory, markerSizeHistory, xFinalHistory, yFinalHistory, zFinalHistory, combinedCommandHistory, step = run_movement_simulation(startingErrorX, startingErrorY, startingMarkerSize, tolerance, kp, maxCommand, desiredSize, sizeTolerance, approachCommand, xyCorrectionScale, zCorrectionScale, maxSteps, printSteps)
    
    print("Test type:", testType)
    print("Test case:", testName)
    print("Starting errorX:", startingErrorX)
    print("Starting errorY:", startingErrorY)
    print("Starting markerSize:", startingMarkerSize)
    print("Final errorX:", errorX)
    print("Final errorY:", errorY)
    print("Final markerSize:", markerSize)
    print("Final movement:", xFinal, yFinal, zFinal)
    print("Steps needed:", step + 1)
    commandSummary = summarize_command_history(combinedCommandHistory)
    print_command_summary(commandSummary)
    print()


  print("Controller Parameter Tuning")
  print()

  tuningStartingErrorX = 400
  tuningStartingErrorY = -300
  tuningStartingMarkerSize = 200
  tuningResults = []

  for parameterName, testKp, testMaxCommand, testTolerance, testApproachCommand, testXyCorrectionScale, testZCorrectionScale in parameterSets:
    errorX, errorY, markerSize, xFinal, yFinal, zFinal, stepHistory, errorXHistory, errorYHistory, markerSizeHistory, xFinalHistory, yFinalHistory, zFinalHistory, combinedCommandHistory, step = run_movement_simulation(tuningStartingErrorX, tuningStartingErrorY, tuningStartingMarkerSize, testTolerance, testKp, testMaxCommand, desiredSize, sizeTolerance, testApproachCommand, testXyCorrectionScale, testZCorrectionScale, maxSteps, printSteps)
    
    print("Parameter set:", parameterName)
    print("kp:", testKp)
    print("maxCommand:", testMaxCommand)
    print("tolerance:", testTolerance)
    print("approachCommand:", testApproachCommand)
    print("xyCorrectionScale:", testXyCorrectionScale)
    print("zCorrectionScale:", testZCorrectionScale)
    print("Final errorX:", errorX)
    print("Final errorY:", errorY)
    print("Final markerSize:", markerSize)
    print("Final movement:", xFinal, yFinal, zFinal)
    print("Steps needed:", step + 1)
    tuningResults.append((parameterName, step + 1))

    commandSummary = summarize_command_history(combinedCommandHistory)
    print_command_summary(commandSummary)
    print()
    print("Tuning step comparison:")
  for parameterName, stepsNeeded in tuningResults:
    print(parameterName + ":", stepsNeeded, "steps")
  print()


  plotStartingErrorX = 200
  plotStartingErrorY = -100
  plotStartingMarkerSize = 250  
  errorX, errorY, markerSize, xFinal, yFinal, zFinal, stepHistory, errorXHistory, errorYHistory, markerSizeHistory, xFinalHistory, yFinalHistory, zFinalHistory, combinedCommandHistory, step = run_movement_simulation(plotStartingErrorX, plotStartingErrorY, plotStartingMarkerSize, tolerance, kp, maxCommand, desiredSize, sizeTolerance, approachCommand, xyCorrectionScale, zCorrectionScale, maxSteps, printSteps)

  save_plot(stepHistory, [errorXHistory, errorYHistory], ["errorX", "errorY"], "Step", "Position Error", "Final Movement Position Error Over Time", "Code/Guidance/final_movement_error_plot.png", [tolerance, -tolerance], ["positive tolerance", "negative tolerance"])
  save_plot(stepHistory, [xFinalHistory, yFinalHistory, zFinalHistory], ["xFinal", "yFinal", "zFinal"], "Step", "Final Command", "Final Movement Commands Over Time","Code/Guidance/final_movement_command_plot.png")
  save_plot(stepHistory, [markerSizeHistory], ["markerSize"], "Step", "Marker Size", "Final Movement Marker Size Over Time", "Code/Guidance/final_movement_marker_size_plot.png", [desiredSize + sizeTolerance, desiredSize - sizeTolerance], ["upper size tolerance", "lower size tolerance"])

  commandSummary = summarize_command_history(combinedCommandHistory)
  print_command_summary(commandSummary)