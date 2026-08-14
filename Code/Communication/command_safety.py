MAX_ALLOWED_COMMAND = 0.25
REQUIRED_MODE = "GUIDED"


def command_safety_check(
    mode,
    armed,
    x_command,
    y_command,
    z_command,
    enable_real_commands,
    props_removed_confirmed,
    pilot_ready_confirmed,
    required_mode=REQUIRED_MODE,
    max_allowed_command=MAX_ALLOWED_COMMAND,
):
    block_reasons = []

    if not enable_real_commands:
        block_reasons.append("ENABLE_REAL_COMMANDS is False")

    if not props_removed_confirmed:
        block_reasons.append("PROPS_REMOVED_CONFIRMED is False")

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
