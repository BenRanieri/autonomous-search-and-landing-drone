from guidance_logic import get_guidance_command, get_proportional_command


#For debugging why the controller has a certain output
def classify_command(error, tolerance, kp, maxCommand):
  if abs(error) <= tolerance:
    return "deadband"
  elif abs(error * kp) >= maxCommand:
    return "capped"
  else:
    return "proportional"



tolerance = 10
kp = 0.01
maxCommand = 1

testCases = [
  (0,0),
  (5, -3),
  (100, -50),
  (-100, 50),
  (300, -300),
  (-300, 300),
  (10, 0),
  (11, 0),
  (-10, 0),
  (-11, 0),
  (0, 10),
  (0, 11),
  (0, -10),
  (0, -11),
  (99, 0),
  (100, 0),
  (101, 0),
  (-99, 0),
  (-100, 0),
  (-101, 0)
]

for errorX, errorY in testCases:
  stringX, stringY = get_guidance_command(errorX, errorY, tolerance)
  numberX, numberY = get_proportional_command(errorX, errorY, tolerance, kp, maxCommand)
  regionX = classify_command(errorX, tolerance, kp, maxCommand)
  regionY = classify_command(errorY, tolerance, kp, maxCommand)
  print("Test case:", errorX, errorY)
  print("RegionX:", regionX)
  print("RegionY:", regionY)
  print("StringX:", stringX)
  print("StringY:", stringY)
  print("NumberX:", numberX)
  print("NumberY:", numberY)
  print()