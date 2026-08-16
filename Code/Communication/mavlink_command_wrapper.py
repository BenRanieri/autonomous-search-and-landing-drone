import time

from pymavlink import mavutil

from Code.Communication.command_safety import command_safety_check


ENABLE_REAL_COMMANDS = False

# This should only be changed for a controlled real flight test after:
# correct props are installed, the pilot is ready, the area is clear,
# and the test plan has been reviewed.
FLIGHT_TEST_CONFIRMED = False

PILOT_READY_CONFIRMED = False

COMMAND_START_TIME = time.time()


def send_velocity_command_safely(
    vehicle,
    mode,
    armed,
    x_command,
    y_command,
    z_command,
):
    allowed, block_reasons = command_safety_check(
        enable_real_commands=ENABLE_REAL_COMMANDS,
        flight_test_confirmed=FLIGHT_TEST_CONFIRMED,
        pilot_ready_confirmed=PILOT_READY_CONFIRMED,
        mode=mode,
        armed=armed,
        x_command=x_command,
        y_command=y_command,
        z_command=z_command,
    )

    if not allowed:
        return {
            "sent": False,
            "allowed": False,
            "reasons": block_reasons,
        }

    time_boot_ms = int((time.time() - COMMAND_START_TIME) * 1000)

    vehicle.mav.set_position_target_local_ned_send(
        time_boot_ms,
        vehicle.target_system,
        vehicle.target_component,
        mavutil.mavlink.MAV_FRAME_BODY_NED,
        0b0000111111000111,
        0,
        0,
        0,
        x_command,
        y_command,
        z_command,
        0,
        0,
        0,
        0,
        0,
    )

    return {
        "sent": True,
        "allowed": True,
        "reasons": [],
    }
