from flight_control.flight_control import FlightControl
from camera.camera import Camera
from sensors.gps import GPS
from sensors.imu import IMU
from sensors.obstacle_detection import ObstacleDetection
from network.server import DroneServer
import threading
import time

def main():
    # Initialize components
    flight_control = FlightControl('/dev/ttyAMA0')
    camera = Camera()
    gps = GPS()
    imu = IMU()
    obstacle_detection = ObstacleDetection(trigger_pin=23, echo_pin=24)

    # Start the server in a separate thread
    server = DroneServer()
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    # Arm and take off
    flight_control.arm_and_takeoff(10)

    # Start recording
    camera.start_recording('/home/pi/video.h264')

    try:
        while True:
            # Read GPS data
            gps_data = gps.read_data()

            # Read IMU data
            accel_x, accel_y, accel_z = imu.read_accel()

            # Check for obstacles
            distance = obstacle_detection.get_distance()

            # Log data
            print(f"GPS: {gps_data}, IMU: {accel_x}, {accel_y}, {accel_z}, Distance: {distance}")

            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop recording and land
        camera.stop_recording()
        flight_control.land()

if __name__ == "__main__":
    main()
