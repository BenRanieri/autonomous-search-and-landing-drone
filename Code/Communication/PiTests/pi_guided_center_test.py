import argparse
import time

from pymavlink import mavutil
from Code.Communication import mavlink_command_wrapper as wrapper



import math
import threading

from Code.Mission.mounted_camera_guidance import get_mounted_track_command

vision_lock = threading.Lock()
vision_stop = threading.Event()
vision_state = {"sample": None, "failure": None}


def camera_worker():
    camera = None
    try:
        from picamera2 import Picamera2
        import cv2

        detector = cv2.aruco.ArucoDetector(
            cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        )
        camera = Picamera2()
        camera.configure(camera.create_video_configuration(
            main={"size": (640, 480), "format": "RGB888"},
            queue=False,
        ))
        camera.start()
        consecutive = 0

        while not vision_stop.is_set():
            capture_started = time.monotonic()
            frame = camera.capture_array()
            bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            corners, ids, _ = detector.detectMarkers(gray)
            sample = None

            if ids is not None:
                for points, marker_id in zip(corners, ids.flatten()):
                    if int(marker_id) != 0:
                        continue
                    center = points[0].mean(axis=0)
                    ex = float(center[0]) - 320.0
                    ey = float(center[1]) - 240.0
                    if math.isfinite(ex) and math.isfinite(ey):
                        consecutive += 1
                        sample = (capture_started, ex, ey, consecutive)
                    break

            if sample is None:
                consecutive = 0

            with vision_lock:
                vision_state["sample"] = sample

            time.sleep(0.02)

    except Exception as exc:
        with vision_lock:
            vision_state["failure"] = repr(exc)
            vision_state["sample"] = None
    finally:
        if camera is not None:
            camera.stop()
            camera.close()


def vision_command():
    with vision_lock:
        sample = vision_state["sample"]
        failure = vision_state["failure"]

    if failure is not None:
        raise RuntimeError(f"Camera failed: {failure}")
    if sample is None:
        return 0.0, 0.0, "marker missing"

    timestamp, ex, ey, count = sample
    if time.monotonic() - timestamp > 0.4:
        return 0.0, 0.0, "camera sample stale"
    if count < 3:
        return 0.0, 0.0, "confirming marker"

    vx, vy, _, ax, ay = get_mounted_track_command(ex, ey)
    if not all(math.isfinite(v) for v in (vx, vy, ax, ay)):
        raise RuntimeError("Non-finite guidance output")

    speed = math.hypot(vx, vy)
    if speed > 0.1:
        vx *= 0.1 / speed
        vy *= 0.1 / speed

    return vx, vy, f"adjusted=({ax:.1f},{ay:.1f})"


vision_thread = threading.Thread(target=camera_worker, daemon=True)

parser = argparse.ArgumentParser()
parser.add_argument("--live", action="store_true")
args = parser.parse_args()

if args.live:
    print("LIVE CENTERING: 2s hold, 8s center at max 0.1 m/s, 3s stop")
    print("Start disarmed. Take off manually, establish Loiter, then select GUIDED.")
    print("Keep the transmitter ready to leave GUIDED.")
    if input("Type READY to confirm the aircraft, area, and pilot are ready: ") != "READY":
        raise SystemExit("Cancelled")

wrapper.ENABLE_REAL_COMMANDS = args.live
wrapper.FLIGHT_TEST_CONFIRMED = args.live
wrapper.PILOT_READY_CONFIRMED = args.live

vehicle = mavutil.mavlink_connection("/dev/ttyAMA0", baud=921600)

try:
    print("Waiting for Pixhawk heartbeat...", flush=True)
    heartbeat = None
    connect_deadline = time.monotonic() + 10

    while time.monotonic() < connect_deadline:
        candidate = vehicle.recv_match(
            type="HEARTBEAT", blocking=True, timeout=1
        )
        if candidate is None:
            continue

        if (
            candidate.autopilot == mavutil.mavlink.MAV_AUTOPILOT_ARDUPILOTMEGA
            and candidate.type == mavutil.mavlink.MAV_TYPE_QUADROTOR
            and candidate.get_srcSystem() != 0
        ):
            heartbeat = candidate
            break

        print(
            f"Ignoring heartbeat: sys={candidate.get_srcSystem()} "
            f"comp={candidate.get_srcComponent()} "
            f"type={candidate.type} autopilot={candidate.autopilot}",
            flush=True,
        )

    if heartbeat is None:
        raise RuntimeError("No ArduPilot quadrotor heartbeat")

    system_id = heartbeat.get_srcSystem()
    component_id = heartbeat.get_srcComponent()
    vehicle.target_system = system_id
    vehicle.target_component = component_id

    print(
        f"Selected flight controller: sys={system_id} comp={component_id} "
        f"mode={mavutil.mode_string_v10(heartbeat)}",
        flush=True,
    )

    def read_state(msg):
        return (
            mavutil.mode_string_v10(msg),
            bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED),
        )

    mode, armed = read_state(heartbeat)
    if armed:
        raise RuntimeError("Start this test while DISARMED")

    vision_thread.start()
    last_heartbeat = time.monotonic()
    deadline = last_heartbeat + (300 if args.live else 60)
    active_since = None
    saw_armed_loiter = False
    last_print = 0
    sent_count = 0

    print(
        "Waiting for manual takeoff, Loiter, then GUIDED..."
        if args.live else "DRY RUN: checking gate for 15 seconds; nothing will be sent",
        flush=True,
    )

    while time.monotonic() < deadline:
        for _ in range(1000):
            msg = vehicle.recv_match(blocking=False)
            if msg is None:
                break
            if (
                msg.get_type() == "HEARTBEAT"
                and msg.get_srcSystem() == system_id
                and msg.get_srcComponent() == component_id
            ):
                mode, armed = read_state(msg)
                last_heartbeat = time.monotonic()

                if armed and mode == "LOITER":
                    saw_armed_loiter = True

                if active_since is not None and (mode != "GUIDED" or not armed):
                    raise RuntimeError("Left GUIDED or disarmed: test stopped")
        else:
            raise RuntimeError("Telemetry backlog: test stopped")

        now = time.monotonic()
        if now - last_heartbeat > 2:
            raise RuntimeError("Heartbeat stale: test stopped")

        desired_x, desired_y, vision_status = vision_command()

        if args.live:
            if active_since is None:
                if saw_armed_loiter and armed and mode == "GUIDED":
                    active_since = now
                    deadline = now + 16
                    print("START: 2s hold, 8s camera centering, 3s stop", flush=True)

            if active_since is not None:
                if now - active_since >= 13:
                    print("COMPLETE: return to Loiter, then land", flush=True)
                    break

                elapsed = now - active_since
                vx = desired_x if 2 <= elapsed < 10 else 0.0
                vy = desired_y if 2 <= elapsed < 10 else 0.0
                result = wrapper.send_velocity_command_safely(
                    vehicle, mode, armed, vx, vy, 0.0
                )
                if not result["sent"]:
                    raise RuntimeError(f"Safety gate blocked: {result['reasons']}")
                sent_count += 1
        else:
            result = wrapper.send_velocity_command_safely(
                vehicle, mode, armed, 0.0, 0.0, 0.0
            )
            if result["sent"]:
                raise RuntimeError("Unexpected send during dry run")

        if now - last_print >= 1:
            print(
                f"mode={mode} armed={armed} "
                f"active={active_since is not None} sent={sent_count} "
                f"vx={vx if active_since is not None else 0.0:.2f} "
                f"vy={vy if active_since is not None else 0.0:.2f} "
                f"{vision_status} "
                f"suggested=({desired_x:.2f},{desired_y:.2f})",
                flush=True,
            )
            last_print = now

        time.sleep(0.1)
    else:
        print("Time limit reached; test ended", flush=True)

except (RuntimeError, KeyboardInterrupt) as exc:
    print(f"STOP: {exc}. If airborne, use the transmitter to take over.", flush=True)
finally:
    wrapper.ENABLE_REAL_COMMANDS = False
    wrapper.FLIGHT_TEST_CONFIRMED = False
    wrapper.PILOT_READY_CONFIRMED = False
    vehicle.close()
    vision_stop.set()
    if vision_thread.ident is not None:
        vision_thread.join(timeout=2)
