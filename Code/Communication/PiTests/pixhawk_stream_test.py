from pymavlink import mavutil
import time

connection_string = "/dev/ttyAMA0"
baud_rate = 921600

print("Connecting to Pixhawk...")
vehicle = mavutil.mavlink_connection(connection_string, baud=baud_rate)

print("Waiting for heartbeat...")
heartbeat = vehicle.wait_heartbeat(timeout=10)

if heartbeat is None:
    print("No heartbeat received")
    raise SystemExit

print("Heartbeat received")
print("System ID:", vehicle.target_system)
print("Component ID:", vehicle.target_component)

target_system = vehicle.target_system
target_component = 1

def request_message(message_id, frequency_hz):
    interval_us = int(1_000_000 / frequency_hz)

    vehicle.mav.command_long_send(
        target_system,
        target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
        0,
        message_id,
        interval_us,
        0,
        0,
        0,
        0,
        0,
    )

request_message(mavutil.mavlink.MAVLINK_MSG_ID_SYS_STATUS, 2)
request_message(mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE, 5)
request_message(mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT, 2)

print("Requested SYS_STATUS, ATTITUDE, and GLOBAL_POSITION_INT")
print("Listening for messages for 12 seconds...")

start_time = time.time()
seen_messages = set()

while time.time() - start_time < 12:
    msg = vehicle.recv_match(blocking=True, timeout=1)

    if msg is None:
        continue

    msg_type = msg.get_type()
    seen_messages.add(msg_type)

    if msg_type == "HEARTBEAT":
        armed = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
        print("HEARTBEAT mode:", mavutil.mode_string_v10(msg), "armed:", armed)

    elif msg_type == "SYS_STATUS":
        print(
            "SYS_STATUS voltage mV:",
            msg.voltage_battery,
            "battery remaining:",
            msg.battery_remaining,
        )

    elif msg_type == "ATTITUDE":
        print(
            "ATTITUDE roll:",
            round(msg.roll, 3),
            "pitch:",
            round(msg.pitch, 3),
            "yaw:",
            round(msg.yaw, 3),
        )

    elif msg_type == "GLOBAL_POSITION_INT":
        print(
            "GLOBAL_POSITION_INT relative_alt_mm:",
            msg.relative_alt,
            "heading:",
            msg.hdg,
        )

print("Seen message types:", sorted(seen_messages))
print("Stream test complete")
