import matplotlib.pyplot as plt
from guidance_logic import get_proportional_command

def run_simulation(startingErrorX, startingErrorY, numSteps, correctionScale, tolerance, kp, maxCommand, printSteps):

  errorX = startingErrorX
  errorY = startingErrorY
  targetCentered = False

  stepHistory = []
  errorXHistory = []
  errorYHistory = []
  xCommandHistory = []
  yCommandHistory = []

  for step in range(numSteps):
    xCommand, yCommand = get_proportional_command(errorX, errorY, tolerance, kp, maxCommand)

    stepHistory.append(step)
    errorXHistory.append(errorX)
    errorYHistory.append(errorY)
    xCommandHistory.append(xCommand)
    yCommandHistory.append(yCommand)

    if printSteps:
      print("step:", step)
      print("errorX:", errorX)
      print("errorY:", errorY)
      print("xCommand:", xCommand)
      print("yCommand:", yCommand)
      print()

    if abs(errorX) <= tolerance and abs(errorY) <= tolerance:
      targetCentered = True
      break

    errorX = errorX - xCommand * correctionScale
    errorY = errorY - yCommand * correctionScale

  return errorX, errorY, targetCentered, stepHistory, errorXHistory, errorYHistory, xCommandHistory, yCommandHistory



if __name__ == "__main__":
  tolerance = 10
  kp = 0.01
  maxCommand = 1.0
  numSteps = 50
  correctionScale = 20
  printSteps = False

  testCases = [
    (200, -100),
    (-200, 100),
    (50, 300),
    (8, -6),
    (300, 300),
    (-300, -300)
  ]

  for startingErrorX, startingErrorY in testCases:
    finalErrorX, finalErrorY, targetCentered,  stepHistory, errorXHistory, errorYHistory, xCommandHistory, yCommandHistory = run_simulation(startingErrorX, startingErrorY, numSteps, correctionScale, tolerance, kp, maxCommand, printSteps)

    print("Starting errorX:", startingErrorX)
    print("Starting errorY:", startingErrorY)
    print("Final errorX:", finalErrorX)
    print("Final errorY:", finalErrorY)
    print("Target centered:", targetCentered)
    print()

  plotErrorX = 200
  plotErrorY = -100
  finalErrorX, finalErrorY, targetCentered,  stepHistory, errorXHistory, errorYHistory, xCommandHistory, yCommandHistory = run_simulation(startingErrorX, startingErrorY, numSteps, correctionScale, tolerance, kp, maxCommand, printSteps)
  plt.figure()
  plt.plot(stepHistory, errorXHistory, label="errorX")
  plt.plot(stepHistory, errorYHistory, label="errorY")
  plt.axhline(tolerance, linestyle="--", label="positive tolerance")
  plt.axhline(-tolerance, linestyle="--", label="negative tolerance")
  plt.xlabel("Step")
  plt.ylabel("Error")
  plt.title("Controller Error Over Time")
  plt.legend()
  plt.grid(True)
  plt.savefig("Code/Guidance/controller_error_plot.png")
  plt.close()
  print("Saved controller error plot")

  plt.figure()
  plt.plot(stepHistory, xCommandHistory, label="xCommand")
  plt.plot(stepHistory, yCommandHistory, label="yCommand")
  plt.xlabel("Step")
  plt.ylabel("Command")
  plt.title("Controller Commands Over Time")
  plt.legend()
  plt.grid(True)
  plt.savefig("Code/Guidance/controller_command_plot.png")
  plt.close()
  print("Saved controller command plot")
