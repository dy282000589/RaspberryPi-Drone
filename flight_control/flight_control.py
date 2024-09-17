from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil
from utils.logger import Logger

class FlightControl:
    def __init__(self, connection_string):
        self.logger = Logger()
        self.logger.log("Connecting to vehicle...")
        self.vehicle = connect(connection_string, wait_ready=True)
        self.logger.log("Vehicle connected")

    def arm_and_takeoff(self, target_altitude):
        self.logger.log("Arming motors")
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True

        while not self.vehicle.armed:
            self.logger.log("Waiting for arming...")
            time.sleep(1)

        self.logger.log("Taking off!")
        self.vehicle.simple_takeoff(target_altitude)

        while True:
            self.logger.log(f"Altitude: {self.vehicle.location.global_relative_frame.alt}")
            if self.vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
                self.logger.log("Reached target altitude")
                break
            time.sleep(1)

    def land(self):
        self.logger.log("Landing")
        self.vehicle.mode = VehicleMode("LAND")
        self.vehicle.close()
        self.logger.log("Vehicle landed and connection closed")

    def set_velocity(self, vx, vy, vz):
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0, 0, 0, mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111,
            0, 0, 0,
            vx, vy, vz,
            0, 0, 0, 0, 0)
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()

    def goto(self, lat, lon, alt):
        location = LocationGlobalRelative(lat, lon, alt)
        self.vehicle.simple_goto(location)
        self.logger.log(f"Going to location: {lat}, {lon}, {alt}")
