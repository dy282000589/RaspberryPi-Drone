import socket
import cv2
import numpy as np
from pynput import keyboard

class DroneClient:
    def __init__(self, host, port=8000):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def send_command(self, command):
        self.client_socket.send(command.encode())

    def receive_data(self):
        return self.client_socket.recv(1024).decode()

    def stream_video(self):
        cap = cv2.VideoCapture('http://<drone_ip>:8001/stream.mjpg')
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Drone Video Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def on_press(self, key):
        try:
            if key.char == 'w':
                self.vx = 1
            elif key.char == 's':
                self.vx = -1
            elif key.char == 'a':
                self.vy = -1
            elif key.char == 'd':
                self.vy = 1
            elif key.char == 'r':
                self.vz = 1
            elif key.char == 'f':
                self.vz = -1
            self.send_command(f'MOVE {self.vx} {self.vy} {self.vz}')
        except AttributeError:
            pass

    def on_release(self, key):
        if key.char in ['w', 's', 'a', 'd', 'r', 'f']:
            self.vx = 0
            self.vy = 0
            self.vz = 0
            self.send_command(f'MOVE {self.vx} {self.vy} {self.vz}')

    def start_keyboard_control(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

if __name__ == "__main__":
    client = DroneClient('<drone_ip>')
    client.send_command('TAKEOFF')
    client.start_keyboard_control()
    client.stream_video()
    client.send_command('LAND')
