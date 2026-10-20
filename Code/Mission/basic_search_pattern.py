import math

SEARCH_SPEED = 0.10
SEARCH_LEG_TIME = 3.0
SEARCH_MAX_TIME = 12.0


def get_basic_search_command(search_elapsed_time):
    try:
        valid = (
            not isinstance(search_elapsed_time, bool)
            and math.isfinite(search_elapsed_time)
            and search_elapsed_time >= 0
        )
    except (TypeError, ValueError, OverflowError):
        valid = False

    if not valid:
        return 0, 0, 0, "SEARCH_INVALID_TIME_HOVER"

    if search_elapsed_time >= SEARCH_MAX_TIME:
        return 0, 0, 0, "SEARCH_TIMEOUT_HOVER"

    leg_index = int(search_elapsed_time // SEARCH_LEG_TIME)

    if leg_index == 0:
        return SEARCH_SPEED, 0, 0, "SEARCH_FORWARD"
    if leg_index == 1:
        return 0, SEARCH_SPEED, 0, "SEARCH_RIGHT"
    if leg_index == 2:
        return -SEARCH_SPEED, 0, 0, "SEARCH_BACKWARD"
    return 0, -SEARCH_SPEED, 0, "SEARCH_LEFT"
