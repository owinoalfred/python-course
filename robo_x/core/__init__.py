"""ROBO-X Core Robot System Package."""

from __future__ import annotations

class RobotCore:
    def __init__(self, robot_id: str = "ROBO-X-01") -> None:
        self.robot_id = robot_id
        self.status = "IDLE"
        self.battery_pct = 100.0

    def get_state(self) -> dict:
        return {
            "robot_id": self.robot_id,
            "status": self.status,
            "battery_pct": self.battery_pct,
        }
