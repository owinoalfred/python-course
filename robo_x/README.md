# ROBO-X Continuous Autonomous Robotics Platform

ROBO-X is the continuous robotics engineering project running throughout the Python Master Course.

## System Architecture

```
Sensors -> Sensor Layer -> Robot State -> Decision / Control -> Actuators -> Telemetry -> Storage -> API / CLI -> Monitoring
```

## Packages & Core Modules

- `robo_x/core`: Core robot model and state machine.
- `robo_x/sensors`: Sensor drivers (LiDAR, IMU, battery, camera, temperature).
- `robo_x/actuators`: Motor drivers and joint actuators.
- `robo_x/navigation`: Waypoint navigation, kinematics, SLAM basics.
- `robo_x/control`: PID and safety controllers.
- `robo_x/perception`: Obstacle detection and filtering.
- `robo_x/telemetry`: Logging and network telemetry streaming.
- `robo_x/simulation`: Deterministic physics and hardware simulator.
- `robo_x/configuration`: System parameters and YAML/JSON config loaders.
- `robo_x/database`: SQLite / SQLAlchemy fleet tracking database.
- `robo_x/api`: REST and CLI interfaces for fleet supervision.

## Milestones

- `M1`: Robot configuration & bring-up CLI.
- `M2`: Decision engine and state machine.
- `M3`: Sensor data structures & buffer management.
- `M4`: Modular software architecture & functional utilities.
- `M5`: Fault handling, logging & diagnostics.
- `M6`: Object-oriented robot and sensor stack.
- `M7`: File telemetry data storage & analytics.
- `M8`: Fleet management database.
- `M9`: Professional CLI, REST API & automated test suite.
- `M10`: Integrated ROBO-X autonomous system.
