from guidance_logic import get_proportional_command

def run_simulation(startingErrorX, startingErrorY, numSteps, correctionScale, tolerance, kp, maxCommand, printSteps):

  errorX = startingErrorX
  errorY = startingErrorY
  targetCentered = False
  for step in range(numSteps):
    xCommand, yCommand = get_proportional_command(errorX, errorY, tolerance, kp, maxCommand)

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

  return errorX, errorY, targetCentered



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
    finalErrorX, finalErrorY, targetCentered = run_simulation(startingErrorX, startingErrorY, numSteps, correctionScale, tolerance, kp, maxCommand, printSteps)

    print("Starting errorX:", startingErrorX)
    print("Starting errorY:", startingErrorY)
    print("Final errorX:", finalErrorX)
    print("Final errorY:", finalErrorY)
    print("Target centered:", targetCentered)
    print()
