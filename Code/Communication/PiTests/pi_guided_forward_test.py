import argparse
import time

from pymavlink import mavutil
from Code.Communication import mavlink_command_wrapper as wrapper


parser = argparse.ArgumentParser()
parser.add_argument("--live", action="store_true")
args = parser.parse_args()

if args.live:
    print("LIVE TEST: 2s hold, 2s forward at 0.1 m/s, 3s stop")
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
    heartbeat = vehicle.wait_heartbeat(timeout=10)
    if heartbeat is None:
        raise RuntimeError("No heartbeat")

    system_id = heartbeat.get_srcSystem()
    component_id = heartbeat.get_srcComponent()

    def read_state(msg):
        return (
            mavutil.mode_string_v10(msg),
            bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED),
        )

    mode, armed = read_state(heartbeat)
    if armed:
        raise RuntimeError("Start this test while DISARMED")

    last_heartbeat = time.monotonic()
    deadline = last_heartbeat + (120 if args.live else 15)
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

        if args.live:
            if active_since is None:
                if saw_armed_loiter and armed and mode == "GUIDED":
                    active_since = now
                    deadline = now + 10
                    print("START: 2s hold, 2s forward, 3s stop", flush=True)

            if active_since is not None:
                if now - active_since >= 7:
                    print("COMPLETE: return to Loiter, then land", flush=True)
                    break

                elapsed = now - active_since
                vx = 0.1 if 2 <= elapsed < 4 else 0.0
                result = wrapper.send_velocity_command_safely(
                    vehicle, mode, armed, vx, 0.0, 0.0
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
                f"vx={vx if active_since is not None else 0.0:.2f}",
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
