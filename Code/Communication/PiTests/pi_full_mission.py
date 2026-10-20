#!/usr/bin/env python3

import os
import sys
import time
from pathlib import Path

os.environ["LIBCAMERA_LOG_LEVELS"] = "*:3"

project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

import cv2
from picamera2 import Picamera2
from pymavlink import mavutil

from Code.Mission.basic_search_pattern import get_basic_search_command
from Code.Mission.mounted_camera_guidance import (
    TARGET_ERROR_X,
    TARGET_ERROR_Y,
    TOLERANCE,
    LAND_TRIGGER_MARKER_SIZE,
    get_adjusted_error,
    is_marker_at_target,
    is_marker_large_enough,
    get_mounted_track_command,
)
import Code.Communication.mavlink_command_wrapper as wrapper
from Code.Communication.mavlink_command_wrapper import send_velocity_command_safely


TARGET_ID = 0

CONNECTION_STRING = "/dev/ttyAMA0"
BAUD_RATE = 921600

CENTER_HOLD_SECONDS = 3.0
MARKER_LOSS_GRACE_SECONDS = 1.0
HEARTBEAT_STALE_SECONDS = 3.0

LAND_COMMAND_RETRY_SECONDS = 1.0
LAND_COMMAND_MAX_ATTEMPTS = 3

PRINT_PERIOD_SECONDS = 0.5
LOOP_PERIOD_SECONDS = 0.1


dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector = cv2.aruco.ArucoDetector(dictionary)


def detect_marker(image_rgb):
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    corners, ids, _ = detector.detectMarkers(gray)

    image_height, image_width = image_bgr.shape[:2]
    image_center_x = image_width / 2
    image_center_y = image_height / 2

    if ids is None:
        return {
            "detected": False,
            "id": None,
            "error_x": None,
            "error_y": None,
            "marker_size": None,
        }

    for i in range(len(ids)):
        marker_id = int(ids[i][0])

        if marker_id != TARGET_ID:
            continue

        marker_corners = corners[i][0]

        center_x = marker_corners[:, 0].mean()
        center_y = marker_corners[:, 1].mean()

        error_x = center_x - image_center_x
        error_y = center_y - image_center_y

        top_width = marker_corners[1][0] - marker_corners[0][0]
        bottom_width = marker_corners[2][0] - marker_corners[3][0]
        left_height = marker_corners[3][1] - marker_corners[0][1]
        right_height = marker_corners[2][1] - marker_corners[1][1]

        marker_size = (
            abs(top_width)
            + abs(bottom_width)
            + abs(left_height)
            + abs(right_height)
        ) / 4

        return {
            "detected": True,
            "id": marker_id,
            "error_x": float(error_x),
            "error_y": float(error_y),
            "marker_size": float(marker_size),
        }

    return {
        "detected": False,
        "id": None,
        "error_x": None,
        "error_y": None,
        "marker_size": None,
    }


def is_autopilot_heartbeat(msg):
    if msg is None:
        return False

    if msg.get_type() != "HEARTBEAT":
        return False

    # Ignore GCS / routed non-autopilot heartbeats that can appear as Mode(0x00000000)
    if msg.autopilot == mavutil.mavlink.MAV_AUTOPILOT_INVALID:
        return False

    return True


def wait_for_autopilot_heartbeat(vehicle, timeout_seconds=15):
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        msg = vehicle.recv_match(
            type="HEARTBEAT",
            blocking=True,
            timeout=1,
        )

        if not is_autopilot_heartbeat(msg):
            continue

        vehicle.target_system = msg.get_srcSystem()
        vehicle.target_component = msg.get_srcComponent()

        return msg

    return None


def read_vehicle_state(
    vehicle,
    last_mode,
    last_armed,
    last_heartbeat_time,
):
    while True:
        msg = vehicle.recv_match(blocking=False)

        if msg is None:
            break

        if not is_autopilot_heartbeat(msg):
            continue

        last_mode = mavutil.mode_string_v10(msg)
        last_armed = bool(
            msg.base_mode
            & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
        )
        last_heartbeat_time = time.time()

    return last_mode, last_armed, last_heartbeat_time


def send_safe_velocity(
    vehicle,
    mode,
    armed,
    x_command,
    y_command,
    z_command,
):
    result = send_velocity_command_safely(
        vehicle=vehicle,
        mode=mode,
        armed=armed,
        x_command=x_command,
        y_command=y_command,
        z_command=z_command,
    )

    if not result["allowed"]:
        reasons = result.get("reasons", [])
        raise RuntimeError(
            "Safety gate blocked command: " + "; ".join(reasons)
        )

    if not result["sent"]:
        raise RuntimeError(
            "Safety gate allowed the command but the wrapper did not send it"
        )

    return result


def request_land(vehicle):
    vehicle.mav.command_long_send(
        vehicle.target_system,
        vehicle.target_component,
        mavutil.mavlink.MAV_CMD_NAV_LAND,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )


def print_marker_status(
    state,
    mode,
    action,
    marker,
    adjusted_error_x,
    adjusted_error_y,
    centered,
    large_enough,
    x_command,
    y_command,
    z_command,
):
    if marker["detected"]:
        print(
            "state:", state,
            "mode:", mode,
            "action:", action,
            "marker:", marker["id"],
            "error:",
            round(marker["error_x"], 1),
            round(marker["error_y"], 1),
            "adjusted:",
            None
            if adjusted_error_x is None
            else round(adjusted_error_x, 1),
            None
            if adjusted_error_y is None
            else round(adjusted_error_y, 1),
            "size:",
            round(marker["marker_size"], 1),
            "centered:",
            centered,
            "large_enough:",
            large_enough,
            "command:",
            round(x_command, 3),
            round(y_command, 3),
            round(z_command, 3),
        )
    else:
        print(
            "state:", state,
            "mode:", mode,
            "action:", action,
            "marker: not detected",
            "command:",
            round(x_command, 3),
            round(y_command, 3),
            round(z_command, 3),
        )


def main():
    print()
    print("FULL AUTONOMOUS SEARCH -> CENTER -> LAND")
    print()
    print("This program does NOT arm the drone.")
    print("This program does NOT switch the drone into GUIDED.")
    print("Take off manually, establish a stable hover, then select GUIDED.")
    print("Before LAND is requested, leaving GUIDED stops autonomous control.")
    print()
    print("TARGET_ERROR_X:", TARGET_ERROR_X)
    print("TARGET_ERROR_Y:", TARGET_ERROR_Y)
    print("TOLERANCE:", TOLERANCE)
    print("LAND_TRIGGER_MARKER_SIZE:", LAND_TRIGGER_MARKER_SIZE)
    print()

    ready = input(
        "Type READY before takeoff to confirm the aircraft, area, and pilot are ready: "
    ).strip()

    if ready != "READY":
        print("READY not entered. Exiting.")
        return

    # Match the behavior of the previously tested --live GUIDED scripts.
    # These affect only this Python process; the wrapper file itself stays
    # safely disabled by default.
    wrapper.ENABLE_REAL_COMMANDS = True
    wrapper.FLIGHT_TEST_CONFIRMED = True
    wrapper.PILOT_READY_CONFIRMED = True

    print("Live command safety flags enabled for this mission")

    print()
    print("Connecting to Pixhawk...")

    vehicle = mavutil.mavlink_connection(
        CONNECTION_STRING,
        baud=BAUD_RATE,
    )

    print("Waiting for Pixhawk autopilot heartbeat...")

    heartbeat = wait_for_autopilot_heartbeat(vehicle)

    if heartbeat is None:
        raise RuntimeError(
            "No Pixhawk autopilot heartbeat received"
        )

    last_mode = mavutil.mode_string_v10(heartbeat)
    last_armed = bool(
        heartbeat.base_mode
        & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
    )
    last_heartbeat_time = time.time()

    print("Heartbeat received")
    print("System ID:", vehicle.target_system)
    print("Component ID:", vehicle.target_component)
    print("Initial mode:", last_mode)
    print("Initial armed:", last_armed)

    picam2 = Picamera2()

    camera_config = picam2.create_video_configuration(
        main={
            "size": (640, 480),
            "format": "RGB888",
        }
    )

    picam2.configure(camera_config)
    picam2.start()

    # Important for the GUIDED/camera issue:
    # start the camera once before takeoff/GUIDED and never restart it.
    time.sleep(2)

    print()
    print("Camera running")
    print("Waiting for manual takeoff and GUIDED...")
    print()

    state = "WAIT_GUIDED"

    search_start_time = None
    centered_since = None
    last_marker_seen_time = None

    land_attempts = 0
    last_land_command_time = None

    last_print_time = 0

    try:
        while True:
            now = time.time()

            (
                last_mode,
                last_armed,
                last_heartbeat_time,
            ) = read_vehicle_state(
                vehicle,
                last_mode,
                last_armed,
                last_heartbeat_time,
            )

            if (
                now - last_heartbeat_time
                > HEARTBEAT_STALE_SECONDS
            ):
                raise RuntimeError(
                    "Pixhawk autopilot heartbeat became stale"
                )

            image_rgb = picam2.capture_array()
            marker = detect_marker(image_rgb)

            if state == "WAIT_GUIDED":
                if now - last_print_time >= PRINT_PERIOD_SECONDS:
                    if marker["detected"]:
                        print(
                            "WAIT_GUIDED",
                            "mode:", last_mode,
                            "armed:", last_armed,
                            "marker:", marker["id"],
                            "error:",
                            round(marker["error_x"], 1),
                            round(marker["error_y"], 1),
                            "size:",
                            round(marker["marker_size"], 1),
                        )
                    else:
                        print(
                            "WAIT_GUIDED",
                            "mode:", last_mode,
                            "armed:", last_armed,
                            "marker: not detected",
                        )

                    last_print_time = now

                if last_mode == "GUIDED" and last_armed:
                    state = "SEARCH"
                    search_start_time = now
                    centered_since = None
                    last_marker_seen_time = None

                    print()
                    print("GUIDED + armed confirmed")
                    print("STATE: SEARCH")
                    print()
                else:
                    time.sleep(LOOP_PERIOD_SECONDS)
                    continue

            if state in ("SEARCH", "CENTER"):
                if not last_armed:
                    print(
                        "Vehicle disarmed before landing request. "
                        "Ending mission."
                    )
                    break

                if last_mode != "GUIDED":
                    print(
                        "GUIDED exited. Manual override detected. "
                        "Ending autonomous control."
                    )
                    break

            x_command = 0.0
            y_command = 0.0
            z_command = 0.0

            action = "HOVER"
            centered = False
            large_enough = False

            adjusted_error_x = None
            adjusted_error_y = None

            if marker["detected"]:
                (
                    adjusted_error_x,
                    adjusted_error_y,
                ) = get_adjusted_error(
                    marker["error_x"],
                    marker["error_y"],
                )

                centered = is_marker_at_target(
                    marker["error_x"],
                    marker["error_y"],
                )

                large_enough = is_marker_large_enough(
                    marker["marker_size"]
                )

            if state == "SEARCH":
                if marker["detected"]:
                    state = "CENTER"
                    centered_since = None
                    last_marker_seen_time = now

                    print()
                    print("Marker found")
                    print("STATE: CENTER")
                    print()

                else:
                    search_elapsed_time = (
                        now - search_start_time
                    )

                    (
                        x_command,
                        y_command,
                        z_command,
                        action,
                    ) = get_basic_search_command(
                        search_elapsed_time
                    )

            if state == "CENTER":
                if marker["detected"]:
                    last_marker_seen_time = now

                    (
                        x_command,
                        y_command,
                        z_command,
                        adjusted_error_x,
                        adjusted_error_y,
                    ) = get_mounted_track_command(
                        marker["error_x"],
                        marker["error_y"],
                    )

                    centered = is_marker_at_target(
                        marker["error_x"],
                        marker["error_y"],
                    )

                    large_enough = is_marker_large_enough(
                        marker["marker_size"]
                    )

                    action = "CENTERING"

                    if centered:
                        # Hold over the calibrated drone-center point before LAND.
                        x_command = 0.0
                        y_command = 0.0
                        z_command = 0.0
                        action = "CENTERED_HOLD"

                        if centered_since is None:
                            centered_since = now

                        centered_time = (
                            now - centered_since
                        )

                        if (
                            centered_time
                            >= CENTER_HOLD_SECONDS
                        ):
                            # Send one final zero velocity target before
                            # handing control to ArduPilot LAND.
                            send_safe_velocity(
                                vehicle,
                                last_mode,
                                last_armed,
                                0.0,
                                0.0,
                                0.0,
                            )

                            request_land(vehicle)

                            land_attempts = 1
                            last_land_command_time = now
                            state = "LAND_REQUESTED"

                            print()
                            print(
                                "Marker centered for",
                                CENTER_HOLD_SECONDS,
                                "seconds",
                            )
                            print(
                                "LAND command sent to ArduPilot"
                            )
                            print(
                                "STATE: LAND_REQUESTED"
                            )
                            print()
                    else:
                        centered_since = None

                else:
                    x_command = 0.0
                    y_command = 0.0
                    z_command = 0.0
                    action = "MARKER_LOST_HOVER"
                    centered_since = None

                    if last_marker_seen_time is None:
                        last_marker_seen_time = now

                    if (
                        now - last_marker_seen_time
                        >= MARKER_LOSS_GRACE_SECONDS
                    ):
                        state = "SEARCH"
                        search_start_time = now
                        last_marker_seen_time = None

                        print()
                        print("Marker lost")
                        print("STATE: SEARCH")
                        print()

            if state in ("SEARCH", "CENTER"):
                send_safe_velocity(
                    vehicle,
                    last_mode,
                    last_armed,
                    x_command,
                    y_command,
                    z_command,
                )

            elif state == "LAND_REQUESTED":
                action = "WAITING_FOR_LAND_MODE"

                if last_mode == "LAND":
                    state = "LANDING"

                    print()
                    print("LAND mode confirmed")
                    print(
                        "ArduPilot now owns the descent and touchdown"
                    )
                    print("STATE: LANDING")
                    print()

                elif not last_armed:
                    print(
                        "Vehicle disarmed after LAND request"
                    )
                    print("MISSION COMPLETE")
                    break

                elif last_mode != "GUIDED":
                    print(
                        "Flight mode changed to",
                        last_mode,
                        "instead of LAND."
                    )
                    print(
                        "Treating this as manual override. "
                        "Ending mission runner."
                    )
                    break

                elif (
                    now - last_land_command_time
                    >= LAND_COMMAND_RETRY_SECONDS
                ):
                    if (
                        land_attempts
                        >= LAND_COMMAND_MAX_ATTEMPTS
                    ):
                        raise RuntimeError(
                            "LAND mode was not accepted after "
                            f"{LAND_COMMAND_MAX_ATTEMPTS} attempts"
                        )

                    request_land(vehicle)
                    land_attempts += 1
                    last_land_command_time = now

                    print(
                        "LAND command retry",
                        land_attempts,
                    )

            elif state == "LANDING":
                action = "ARDUPILOT_LANDING"

                # Do not send any more GUIDED velocity targets.
                # LAND mode controls the descent.
                if not last_armed:
                    print()
                    print(
                        "Vehicle disarmed after landing"
                    )
                    print("MISSION COMPLETE")
                    break

                if last_mode not in ("LAND",):
                    print(
                        "LAND mode exited to",
                        last_mode,
                        "- manual control/failsafe has taken over"
                    )
                    break

            if (
                now - last_print_time
                >= PRINT_PERIOD_SECONDS
            ):
                print_marker_status(
                    state=state,
                    mode=last_mode,
                    action=action,
                    marker=marker,
                    adjusted_error_x=adjusted_error_x,
                    adjusted_error_y=adjusted_error_y,
                    centered=centered,
                    large_enough=large_enough,
                    x_command=x_command,
                    y_command=y_command,
                    z_command=z_command,
                )

                last_print_time = now

            time.sleep(LOOP_PERIOD_SECONDS)

    finally:
        # Return the in-process wrapper flags to their safe defaults.
        wrapper.ENABLE_REAL_COMMANDS = False
        wrapper.FLIGHT_TEST_CONFIRMED = False
        wrapper.PILOT_READY_CONFIRMED = False

        try:
            picam2.stop()
        except Exception:
            pass

        try:
            vehicle.close()
        except Exception:
            pass

    print("Mission runner stopped")


if __name__ == "__main__":
    main()
