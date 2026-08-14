import os
import sys
import time
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from pymavlink import mavutil

from Code.Communication.mavlink_command_wrapper import send_velocity_command_safely
from Code.Mission.basic_search_pattern import get_basic_search_command


CONNECTION_STRING = "/dev/ttyAMA0"
BAUD_RATE = 921600
RUN_TIME_SECONDS = 15


print("Connecting to Pixhawk...")
vehicle = mavutil.mavlink_connection(CONNECTION_STRING, baud=BAUD_RATE)

print("Waiting for heartbeat...")
heartbeat = vehicle.wait_heartbeat(timeout=10)

if heartbeat is None:
    print("No heartbeat received")
    raise SystemExit

print("Heartbeat received")
print("System ID:", vehicle.target_system)
print("Component ID:", vehicle.target_component)

print("Running command wrapper + search dry-run test for", RUN_TIME_SECONDS, "seconds...")
print("No commands should be sent to the Pixhawk.")
print("Expected result: search commands are generated but safety gate blocks them.")

last_mode = "unknown"
last_armed = False
start_time = time.time()

while time.time() - start_time < RUN_TIME_SECONDS:
    msg = vehicle.recv_match(type="HEARTBEAT", blocking=True, timeout=1)

    if msg is not None:
        last_mode = mavutil.mode_string_v10(msg)
        last_armed = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)

    elapsed = time.time() - start_time

    x_command, y_command, z_command, search_action = get_basic_search_command(elapsed)

    result = send_velocity_command_safely(
        vehicle=vehicle,
        mode=last_mode,
        armed=last_armed,
        x_command=x_command,
        y_command=y_command,
        z_command=z_command,
    )

    print(
        "mode:",
        last_mode,
        "armed:",
        last_armed,
        "search_action:",
        search_action,
        "command:",
        round(x_command, 3),
        round(y_command, 3),
        round(z_command, 3),
        "sent:",
        result["sent"],
        "allowed:",
        result["allowed"],
        "reasons:",
        result["reasons"],
    )

print("Command wrapper + search dry-run test complete")
