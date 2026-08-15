TARGET_ERROR_X = -93.5
TARGET_ERROR_Y = 26.2

TOLERANCE = 45

LAND_TRIGGER_MARKER_SIZE = 90

KP = 0.002
MAX_COMMAND = 0.25


def clamp(value, limit):
    if value > limit:
        return limit

    if value < -limit:
        return -limit

    return value


def get_adjusted_error(error_x, error_y):
    adjusted_error_x = error_x - TARGET_ERROR_X
    adjusted_error_y = error_y - TARGET_ERROR_Y

    return adjusted_error_x, adjusted_error_y


def is_marker_at_target(error_x, error_y, tolerance=TOLERANCE):
    adjusted_error_x, adjusted_error_y = get_adjusted_error(error_x, error_y)

    return abs(adjusted_error_x) <= tolerance and abs(adjusted_error_y) <= tolerance


def is_marker_large_enough(marker_size):
    return marker_size >= LAND_TRIGGER_MARKER_SIZE


def get_mounted_track_command(error_x, error_y):
    adjusted_error_x, adjusted_error_y = get_adjusted_error(error_x, error_y)

    if abs(adjusted_error_x) <= TOLERANCE:
        x_command = 0
    else:
        x_command = KP * adjusted_error_x

    if abs(adjusted_error_y) <= TOLERANCE:
        y_command = 0
    else:
        y_command = KP * adjusted_error_y

    x_command = clamp(x_command, MAX_COMMAND)
    y_command = clamp(y_command, MAX_COMMAND)
    z_command = 0

    return x_command, y_command, z_command, adjusted_error_x, adjusted_error_y
