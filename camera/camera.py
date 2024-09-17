from picamera import PiCamera
from time import sleep
from utils.logger import Logger
import io
import socket
import struct
import time
import picamera

class Camera:
    def __init__(self):
        self.logger = Logger()
        self.camera = PiCamera()
        self.logger.log("Camera initialized")

    def start_recording(self, filepath):
        self.camera.start_preview()
        self.camera.start_recording(filepath)
        self.logger.log(f"Recording started: {filepath}")

    def stop_recording(self):
        self.camera.stop_recording()
        self.camera.stop_preview()
        self.logger.log("Recording stopped")

    def stream_video(self, host, port):
        self.camera.start_preview()
        self.logger.log("Video streaming started")
        with socket.socket() as client_socket:
            client_socket.connect((host, port))
            connection = client_socket.makefile('wb')
            try:
                self.camera.start_recording(connection, format='mjpeg')
                self.camera.wait_recording(60)
            finally:
                self.camera.stop_recording()
                connection.close()
                self.logger.log("Video streaming stopped")
