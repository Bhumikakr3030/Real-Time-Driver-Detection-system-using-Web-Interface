import serial
import time

# Change COM port accordingly
ser = serial.Serial('COM5', 115200, timeout=1)

time.sleep(2)  # Wait for ESP32 to reset

while True:
    value = input("Enter 1 (ON) or 2 (OFF): ")

    if value in ['1', '2']:
        ser.write(value.encode())  # Send data
        print("Sent:", value)

    else:
        print("Invalid input")