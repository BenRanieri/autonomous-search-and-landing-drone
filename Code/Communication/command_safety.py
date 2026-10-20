import math

MAX_ALLOWED_COMMAND = 0.25
REQUIRED_MODE = "GUIDED"


def command_safety_check(
    enable_real_commands,
    flight_test_confirmed,
    pilot_ready_confirmed,
    mode,
    armed,
    x_command,
    y_command,
    z_command,
    max_allowed_command=MAX_ALLOWED_COMMAND,
    required_mode=REQUIRED_MODE,
):
    block_reasons = []

    # Reject invalid numbers before comparing command magnitudes.
    values = (
        ("x_command", x_command),
        ("y_command", y_command),
        ("z_command", z_command),
        ("max_allowed_command", max_allowed_command),
    )
    for name, value in values:
        try:
            valid = not isinstance(value, bool) and math.isfinite(value)
        except (TypeError, ValueError, OverflowError):
            valid = False
        if not valid:
            block_reasons.append(f"{name} must be a finite number")

    if block_reasons:
        return False, block_reasons

    if max_allowed_command <= 0:
        return False, ["max_allowed_command must be positive"]

    if not enable_real_commands:
        block_reasons.append("ENABLE_REAL_COMMANDS is False")

    if not flight_test_confirmed:
        block_reasons.append("FLIGHT_TEST_CONFIRMED is False")

    if not pilot_ready_confirmed:
        block_reasons.append("PILOT_READY_CONFIRMED is False")

    if mode != required_mode:
        block_reasons.append(f"mode is {mode}, not {required_mode}")

    if not armed:
        block_reasons.append("vehicle is not armed")

    if abs(x_command) > max_allowed_command:
        block_reasons.append("x_command is too large")

    if abs(y_command) > max_allowed_command:
        block_reasons.append("y_command is too large")

    if abs(z_command) > max_allowed_command:
        block_reasons.append("z_command is too large")

    allowed = len(block_reasons) == 0

    return allowed, block_reasons
