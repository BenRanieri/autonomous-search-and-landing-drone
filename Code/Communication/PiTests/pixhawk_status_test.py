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

print("Listening for Pixhawk messages for 10 seconds...")

start_time = time.time()

seen_messages = set()

while time.time() - start_time < 10:
    msg = vehicle.recv_match(blocking=True, timeout=1)

    if msg is None:
        continue

    msg_type = msg.get_type()
    seen_messages.add(msg_type)

    if msg_type == "HEARTBEAT":
        print("HEARTBEAT mode:", mavutil.mode_string_v10(msg), "armed:", bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED))

    elif msg_type == "SYS_STATUS":
        print("SYS_STATUS battery voltage mV:", msg.voltage_battery, "battery remaining:", msg.battery_remaining)

    elif msg_type == "ATTITUDE":
        print("ATTITUDE roll:", round(msg.roll, 3), "pitch:", round(msg.pitch, 3), "yaw:", round(msg.yaw, 3))

print("Seen message types:", sorted(seen_messages))
print("Status test complete")
