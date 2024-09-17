import socket
import threading
from flight_control.flight_control import FlightControl
from camera.camera import Camera
from sensors.gps import GPS
from sensors.imu import IMU
from sensors.obstacle_detection import ObstacleDetection

class DroneServer:
    def __init__(self, host='0.0.0.0', port=8000):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.flight_control = FlightControl('/dev/ttyAMA0')
        self.camera = Camera()
        self.gps = GPS()
        self.imu = IMU()
        self.obstacle_detection = ObstacleDetection(trigger_pin=23, echo_pin=24)

    def handle_client(self, client_socket):
        while True:
            try:
                command = client_socket.recv(1024).decode()
                if command == 'TAKEOFF':
                    self.flight_control.arm_and_takeoff(10)
                elif command == 'LAND':
                    self.flight_control.land()
                elif command.startswith('MOVE'):
                    _, vx, vy, vz = command.split()
                    self.flight_control.set_velocity(float(vx), float(vy), float(vz))
                elif command == 'START_VIDEO':
                    self.camera.stream_video(client_socket.getpeername()[0], 8001)
                elif command == 'STOP_VIDEO':
                    self.camera.stop_recording()
                elif command == 'GET_GPS':
                    gps_data = self.gps.read_data()
                    client_socket.send(gps_data.encode())
                elif command == 'GET_IMU':
                    accel_x, accel_y, accel_z = self.imu.read_accel()
                    imu_data = f"{accel_x},{accel_y},{accel_z}"
                    client_socket.send(imu_data.encode())
                elif command == 'GET_OBSTACLE':
                    distance = self.obstacle_detection.get_distance()
                    client_socket.send(str(distance).encode())
                elif command.startswith('GOTO'):
                    _, lat, lon, alt = command.split()
                    self.flight_control.goto(float(lat), float(lon), float(alt))
            except Exception as e:
                print(f"Error handling client command: {e}")
                break

    def start(self):
        print("Drone server started")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    server = DroneServer()
    server.start()
