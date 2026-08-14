SEARCH_SPEED = 0.20
SEARCH_LEG_TIME = 3.0
SEARCH_MAX_TIME = 25.0


def get_basic_search_command(search_elapsed_time):
    if search_elapsed_time >= SEARCH_MAX_TIME:
        return 0, 0, 0, "SEARCH_TIMEOUT_HOVER"

    leg_index = int(search_elapsed_time // SEARCH_LEG_TIME) % 4

    if leg_index == 0:
        return SEARCH_SPEED, 0, 0, "SEARCH_FORWARD"

    if leg_index == 1:
        return 0, SEARCH_SPEED, 0, "SEARCH_RIGHT"

    if leg_index == 2:
        return -SEARCH_SPEED, 0, 0, "SEARCH_BACKWARD"

    return 0, -SEARCH_SPEED, 0, "SEARCH_LEFT"
