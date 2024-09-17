import smbus
import time
from utils.logger import Logger

class IMU:
    def __init__(self, bus=1, address=0x68):
        self.logger = Logger()
        self.bus = smbus.SMBus(bus)
        self.address = address
        self.bus.write_byte_data(self.address, 0x6B, 0)
        self.logger.log("IMU initialized")

    def read_accel(self):
        accel_x = self.read_word_2c(0x3B)
        accel_y = self.read_word_2c(0x3D)
        accel_z = self.read_word_2c(0x3F)
        self.logger.log(f"IMU Data: {accel_x}, {accel_y}, {accel_z}")
        return accel_x, accel_y, accel_z

    def read_word_2c(self, addr):
        high = self.bus.read_byte_data(self.address, addr)
        low = self.bus.read_byte_data(self.address, addr+1)
        val = (high << 8) + low
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val
