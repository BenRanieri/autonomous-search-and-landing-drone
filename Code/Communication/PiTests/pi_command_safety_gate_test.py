import time
from pymavlink import mavutil

CONNECTION_STRING = "/dev/ttyAMA0"
BAUD_RATE = 921600

RUN_TIME_SECONDS = 12

# Master lock.
# This must stay False for now.
ENABLE_REAL_COMMANDS = False

# These are extra human-confirmed safety flags.
# They are intentionally False for this test.
PROPS_REMOVED_CONFIRMED = False
PILOT_READY_CONFIRMED = False

# Future real velocity commands should only happen in GUIDED.
# Today we are only checking that the gate blocks commands.
REQUIRED_MODE = "GUIDED"

MAX_ALLOWED_COMMAND = 0.25


def command_safety_check(mode, armed, x_command, y_command, z_command):
    block_reasons = []

    if not ENABLE_REAL_COMMANDS:
        block_reasons.append("ENABLE_REAL_COMMANDS is False")

    if not PROPS_REMOVED_CONFIRMED:
        block_reasons.append("PROPS_REMOVED_CONFIRMED is False")

    if not PILOT_READY_CONFIRMED:
        block_reasons.append("PILOT_READY_CONFIRMED is False")

    if mode != REQUIRED_MODE:
        block_reasons.append(f"mode is {mode}, not {REQUIRED_MODE}")

    if not armed:
        block_reasons.append("vehicle is not armed")

    if abs(x_command) > MAX_ALLOWED_COMMAND:
        block_reasons.append("x_command is too large")

    if abs(y_command) > MAX_ALLOWED_COMMAND:
        block_reasons.append("y_command is too large")

    if abs(z_command) > MAX_ALLOWED_COMMAND:
        block_reasons.append("z_command is too large")

    allowed = len(block_reasons) == 0

    return allowed, block_reasons


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

print("Running command safety gate dry-run for", RUN_TIME_SECONDS, "seconds...")
print("No commands will be sent to the Pixhawk.")
print("Expected result: every command should be BLOCKED.")

last_mode = "unknown"
last_armed = False
start_time = time.time()

while time.time() - start_time < RUN_TIME_SECONDS:
    msg = vehicle.recv_match(type="HEARTBEAT", blocking=True, timeout=1)

    if msg is not None:
        last_mode = mavutil.mode_string_v10(msg)
        last_armed = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)

    # Fake command from guidance code.
    # This is only a pretend command for checking the gate.
    x_command = 0.10
    y_command = -0.05
    z_command = 0.00

    allowed, block_reasons = command_safety_check(
        last_mode,
        last_armed,
        x_command,
        y_command,
        z_command,
    )

    if allowed:
        print(
            "mode:",
            last_mode,
            "armed:",
            last_armed,
            "command:",
            x_command,
            y_command,
            z_command,
            "SAFETY_GATE: ALLOWED",
        )
    else:
        print(
            "mode:",
            last_mode,
            "armed:",
            last_armed,
            "command:",
            x_command,
            y_command,
            z_command,
            "SAFETY_GATE: BLOCKED",
            "reasons:",
            block_reasons,
        )

print("Command safety gate dry-run complete")
