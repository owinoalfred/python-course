# ROBO-X System Architecture

The ROBO-X system follows a layered software architecture:

1. **Hardware / Simulator Layer**: Provides raw sensor reads and accepts motor commands.
2. **Sensor & Perception Layer**: Filters noise and produces high-level world representations.
3. **Control & Navigation Layer**: Computes motion plans, kinematics, and safety overrides.
4. **Telemetry & Storage Layer**: Logs events, updates fleet database, and exposes REST/CLI APIs.
