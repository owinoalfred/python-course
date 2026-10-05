# ROBO-X Software Architecture

Modular Python 3.12 package architecture:

- `robo_x.core`: Central state machine and event dispatcher.
- `robo_x.sensors`: Hardware abstraction for LiDAR, IMU, GPS, and Battery.
- `robo_x.control`: Motion controllers and safety monitors.
- `robo_x.api`: REST endpoints and CLI utilities.
