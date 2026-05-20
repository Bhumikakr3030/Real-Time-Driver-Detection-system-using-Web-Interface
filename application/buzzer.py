import serial
import time

class BuzzerController:
    def __init__(self, port='COM5', baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Wait for ESP32 to reset

    def buzzer(self, condition):
        """
        condition = True  -> Turn ON
        condition = False -> Turn OFF
        """
        if condition:
            self.ser.write(b'1')
            print("Buzzer ON")
        else:
            self.ser.write(b'2')
            print("Buzzer OFF")

    def close(self):
        self.ser.close()

buzzer = BuzzerController('COM5')

buzzer.buzzer(True)   # ON
time.sleep(3)

buzzer.buzzer(False)  # OFF

buzzer.close()