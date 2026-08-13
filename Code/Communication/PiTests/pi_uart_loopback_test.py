import serial
import time

port = "/dev/ttyAMA0"
baud = 115200

print("Opening", port)

ser = serial.Serial(port, baud, timeout=1)
time.sleep(0.5)

message = b"uart_loopback_test\n"

print("Writing:", message.decode().strip())
ser.write(message)
ser.flush()

received = ser.readline()

print("Received:", received.decode(errors="replace").strip())

ser.close()

if received == message:
    print("Loopback passed")
else:
    print("Loopback failed")
