import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from Code.Communication.command_safety import command_safety_check


print("Command safety gate test")
print("No Pixhawk connection is used")
print("No movement commands are sent")

tests = [
    {
        "name": "default blocked case",
        "enable_real_commands": False,
        "flight_test_confirmed": False,
        "pilot_ready_confirmed": False,
        "mode": "STABILIZE",
        "armed": False,
        "x_command": 0.1,
        "y_command": 0.0,
        "z_command": 0.0,
    },
    {
        "name": "wrong mode blocked case",
        "enable_real_commands": True,
        "flight_test_confirmed": True,
        "pilot_ready_confirmed": True,
        "mode": "LOITER",
        "armed": True,
        "x_command": 0.1,
        "y_command": 0.0,
        "z_command": 0.0,
    },
    {
        "name": "not armed blocked case",
        "enable_real_commands": True,
        "flight_test_confirmed": True,
        "pilot_ready_confirmed": True,
        "mode": "GUIDED",
        "armed": False,
        "x_command": 0.1,
        "y_command": 0.0,
        "z_command": 0.0,
    },
    {
        "name": "oversized command blocked case",
        "enable_real_commands": True,
        "flight_test_confirmed": True,
        "pilot_ready_confirmed": True,
        "mode": "GUIDED",
        "armed": True,
        "x_command": 0.4,
        "y_command": 0.0,
        "z_command": 0.0,
    },
    {
        "name": "fully allowed case",
        "enable_real_commands": True,
        "flight_test_confirmed": True,
        "pilot_ready_confirmed": True,
        "mode": "GUIDED",
        "armed": True,
        "x_command": 0.1,
        "y_command": -0.1,
        "z_command": 0.0,
    },
]

for test in tests:
    allowed, reasons = command_safety_check(
        enable_real_commands=test["enable_real_commands"],
        flight_test_confirmed=test["flight_test_confirmed"],
        pilot_ready_confirmed=test["pilot_ready_confirmed"],
        mode=test["mode"],
        armed=test["armed"],
        x_command=test["x_command"],
        y_command=test["y_command"],
        z_command=test["z_command"],
    )

    print()
    print(test["name"])
    print("allowed:", allowed)
    print("reasons:", reasons)

print()
print("Command safety gate test complete")
