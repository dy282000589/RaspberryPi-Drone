import serial
from utils.logger import Logger

class GPS:
    def __init__(self, port='/dev/ttyAMA0', baudrate=9600):
        self.logger = Logger()
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.logger.log("GPS initialized")

    def read_data(self):
        data = self.ser.readline().decode('ascii', errors='replace')
        self.logger.log(f"GPS Data: {data}")
        return data
