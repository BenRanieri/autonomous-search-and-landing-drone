from pymavlink import mavutil
import time

connection_string = "/dev/ttyAMA0"
baud_rate = 921600

print("Connecting to Pixhawk...")
print("Connection:", connection_string)
print("Baud:", baud_rate)

vehicle = mavutil.mavlink_connection(
    connection_string,
    baud=baud_rate
)

print("Waiting for heartbeat...")

heartbeat = vehicle.wait_heartbeat(timeout=10)

if heartbeat is None:
    print("No heartbeat received")
else:
    print("Heartbeat received")
    print("System ID:", vehicle.target_system)
    print("Component ID:", vehicle.target_component)
    print("MAV type:", heartbeat.type)
    print("Autopilot:", heartbeat.autopilot)
    print("Base mode:", heartbeat.base_mode)
    print("System status:", heartbeat.system_status)

print("Test complete")
