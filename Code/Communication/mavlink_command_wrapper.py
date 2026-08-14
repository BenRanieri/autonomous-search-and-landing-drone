import time
from pymavlink import mavutil

from Code.Communication.command_safety import command_safety_check


ENABLE_REAL_COMMANDS = False
PROPS_REMOVED_CONFIRMED = False
PILOT_READY_CONFIRMED = False

REQUIRED_MODE = "GUIDED"
MAX_ALLOWED_COMMAND = 0.25


def send_velocity_command_safely(
    vehicle,
    mode,
    armed,
    x_command,
    y_command,
    z_command,
):
    allowed, block_reasons = command_safety_check(
        mode=mode,
        armed=armed,
        x_command=x_command,
        y_command=y_command,
        z_command=z_command,
        enable_real_commands=ENABLE_REAL_COMMANDS,
        props_removed_confirmed=PROPS_REMOVED_CONFIRMED,
        pilot_ready_confirmed=PILOT_READY_CONFIRMED,
        required_mode=REQUIRED_MODE,
        max_allowed_command=MAX_ALLOWED_COMMAND,
    )

    if not allowed:
        return {
            "sent": False,
            "allowed": False,
            "reasons": block_reasons,
        }

    # This is the only place real velocity commands should be sent.
    # It should only execute if every safety gate above passes.
    vehicle.mav.set_position_target_local_ned_send(
        int(time.time() * 1000),
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
