from pymavlink import mavutil

connection_string = "/dev/serial0"
baud_rates = [921600, 57600, 115200, 230400, 460800]

for baud_rate in baud_rates:
    print("Trying baud:", baud_rate)

    vehicle = mavutil.mavlink_connection(
        connection_string,
        baud=baud_rate
    )

    heartbeat = vehicle.wait_heartbeat(timeout=8)

    if heartbeat is not None:
        print("Heartbeat received")
        print("Baud:", baud_rate)
        print("System ID:", vehicle.target_system)
        print("Component ID:", vehicle.target_component)
        print("MAV type:", heartbeat.type)
        print("Autopilot:", heartbeat.autopilot)
        break

    print("No heartbeat at", baud_rate)
    vehicle.close()
else:
    print("No heartbeat found at any tested baud rate")
