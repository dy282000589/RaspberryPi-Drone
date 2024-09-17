Surveillance Drone Project

Overview
This project is to build a surveillance drone using a Raspberry Pi 3 B+. The drone is equipped with a camera for real-time video streaming, various sensors for telemetry data, and a flight controller for autonomous and manual control. The drone can be controlled wirelessly from a laptop, which also receives the video feed and telemetry data.

Features
- Flight Control: Arm, takeoff, land, set velocity, and navigate to GPS coordinates.
- Camera Handling: Record and stream video.
- Sensor Integration: Read data from GPS, IMU, and obstacle detection sensors.
- Network Communication: Server on the drone and client on the laptop for sending commands and receiving data.
- Real-time Video Streaming: Using MJPEG streaming.
- Telemetry Data: Sending GPS, IMU, and obstacle distance data to the laptop.
- Autonomous Flight Modes: Waypoint navigation.
- Enhanced Obstacle Avoidance: Using multiple sensors.
- Telemetry Data Logging: Logging data for analysis.


Install Dependencies:
```
   sudo apt-get update
   sudo apt-get install python3-pip
   pip3 install -r requirements.txt
```

Usage
On the Drone
```
   python3 main.py
```

On the Laptop
```
   python3 network/client.py
```

Commands
- TAKEOFF: Arm and take off the drone.
- LAND: Land the drone.
- MOVE vx vy vz: Move the drone with specified velocities.
- START_VIDEO: Start video streaming.
- STOP_VIDEO: Stop video streaming.
- GET_GPS: Get GPS data.
- GET_IMU: Get IMU data.
- GET_OBSTACLE: Get obstacle distance.
- GOTO lat lon alt: Navigate to specified GPS coordinates.

Direct Control
Use the following keyboard controls for direct drone movement:
- W: Move forward
- S: Move backward
- A: Move left
- D: Move right
- R: Move up
- F: Move down