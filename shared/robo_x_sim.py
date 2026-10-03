"""Deterministic robot simulation used by every ROBO-X exercise.

The whole course is completable without physical hardware, so this module
provides a small, well-behaved simulator:

* sensors return values from a fixed random stream (seeded), so results are
  reproducible across runs and machines;
* motion obeys an energy model, so battery behaviour is observable;
* the robot refuses unsafe commands (negative distance, driving with a flat
  battery), so safety logic can actually be exercised.

Design constraints
------------------
* Standard library only, so it works before ``requirements.txt`` is installed.
* Deterministic: the same seed always produces the same readings.
* Explicit failure: invalid input raises ``ValueError`` rather than silently
  returning a plausible-looking wrong number.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

#: Wh consumed per metre, per robot class. Tuned so a mission is possible but
#: not free — energy is the constraint that makes planning interesting.
ENERGY_PER_METRE_WH = 0.8

#: Wh consumed per second while actively driving.
ENERGY_PER_SECOND_WH = 0.35

#: Wh consumed per second while idle (sensors, radio, controller).
IDLE_ENERGY_PER_SECOND_WH = 0.02

#: Sensor ranges, in metres, used for clamping and for realism.
SENSOR_RANGES: dict[str, tuple[float, float]] = {
    "distance": (0.02, 30.0),
    "temperature": (-40.0, 125.0),
    "battery_voltage": (9.0, 16.8),
    "imu_accel": (-16.0, 16.0),
}


class SensorError(RuntimeError):
    """Raised when a simulated sensor fails to produce a reading."""


@dataclass(frozen=True, slots=True)
class SensorSpec:
    """Static description of a simulated sensor channel."""

    name: str
    unit: str
    minimum: float
    maximum: float
    noise: float = 0.0

    def clamp(self, value: float) -> float:
        """Clamp ``value`` into the sensor's physical range."""
        return max(self.minimum, min(self.maximum, value))


@dataclass(slots=True)
class Scenario:
    """A reproducible world: obstacle positions plus sensor noise settings."""

    seed: int = 20260101
    obstacles: list[tuple[float, float, float]] = field(default_factory=list)
    temperature_base: float = 22.0
    temperature_drift: float = 0.35
    voltage_nominal: float = 14.8


class ScenarioBuilder:
    """Fluent builder for :class:`Scenario` objects.

    Example::

        scenario = (
            ScenarioBuilder(seed=7)
            .obstacle(3.0, 0.0, radius=0.4)
            .obstacle(6.5, 2.0, radius=0.8)
            .temperature(base=24.0, drift=0.5)
            .build()
        )
    """

    def __init__(self, seed: int = 20260101) -> None:
        self._seed = seed
        self._obstacles: list[tuple[float, float, float]] = []
        self._temperature_base = 22.0
        self._temperature_drift = 0.35
        self._voltage_nominal = 14.8

    def seed(self, seed: int) -> "ScenarioBuilder":
        self._seed = seed
        return self

    def obstacle(self, x: float, y: float, radius: float = 0.5) -> "ScenarioBuilder":
        """Place a circular obstacle in the world."""
        if radius <= 0:
            raise ValueError("obstacle radius must be positive")
        self._obstacles.append((float(x), float(y), float(radius)))
        return self

    def temperature(self, base: float, drift: float = 0.35) -> "ScenarioBuilder":
        self._temperature_base = float(base)
        self._temperature_drift = float(drift)
        return self

    def voltage(self, nominal: float) -> "ScenarioBuilder":
        self._voltage_nominal = float(nominal)
        return self

    def build(self) -> Scenario:
        return Scenario(
            seed=self._seed,
            obstacles=list(self._obstacles),
            temperature_base=self._temperature_base,
            temperature_drift=self._temperature_drift,
            voltage_nominal=self._voltage_nominal,
        )


def default_scenario(seed: int = 20260101) -> Scenario:
    """A small warehouse-like world used across the course."""
    return (
        ScenarioBuilder(seed=seed)
        .obstacle(3.0, 0.0, radius=0.40)
        .obstacle(6.5, 2.0, radius=0.80)
        .obstacle(9.0, -1.5, radius=0.55)
        .temperature(base=22.0, drift=0.35)
        .build()
    )


class SimulatedRobot:
    """A small differential-drive robot with an energy model.

    The API deliberately mirrors what a real robot API looks like, so code
    written against the simulator transfers to hardware later:

    * :meth:`read_sensor` may raise :class:`SensorError` — callers must handle it;
    * :meth:`move` validates its arguments and rejects unsafe commands;
    * :meth:`status` returns an immutable snapshot, not a live mutable view.
    """

    def __init__(
        self,
        name: str = "robo-x-01",
        battery_wh: float = 48.0,
        scenario: Scenario | None = None,
        position: tuple[float, float] = (0.0, 0.0),
        max_speed_mps: float = 1.2,
    ) -> None:
        if battery_wh <= 0:
            raise ValueError("battery_wh must be positive")
        if max_speed_mps <= 0:
            raise ValueError("max_speed_mps must be positive")

        self.name = name
        self.battery_wh = float(battery_wh)
        self.battery_capacity_wh = float(battery_wh)
        self.scenario = scenario if scenario is not None else default_scenario()
        self.x, self.y = float(position[0]), float(position[1])
        self.heading_rad = 0.0
        self.max_speed_mps = float(max_speed_mps)
        self.travelled_m = 0.0
        self.active_seconds = 0.0
        self.distance_travelled = 0.0
        self.odometry: list[tuple[float, float]] = [(self.x, self.y)]

        self._rng = random.Random(self.scenario.seed)
        self._tick = 0
        self._sensor_specs: dict[str, SensorSpec] = {
            "distance": SensorSpec("distance", "m", *SENSOR_RANGES["distance"], noise=0.01),
            "temperature": SensorSpec(
                "temperature", "C", *SENSOR_RANGES["temperature"], noise=0.15
            ),
            "battery_voltage": SensorSpec(
                "battery_voltage", "V", *SENSOR_RANGES["battery_voltage"], noise=0.01
            ),
            "imu_accel": SensorSpec(
                "imu_accel", "m/s^2", *SENSOR_RANGES["imu_accel"], noise=0.05
            ),
        }
        self._fault_injection = 0.0

    # ------------------------------------------------------------------ #
    # Sensors
    # ------------------------------------------------------------------ #
    def read_sensor(self, channel: str) -> float:
        """Return one simulated sensor reading.

        Raises:
            SensorError: unknown channel, or an injected sensor fault.
        """
        if channel not in self._sensor_specs:
            raise SensorError(f"unknown sensor channel: {channel!r}")
        self._tick += 1

        if self._fault_injection > 0:
            self._fault_injection -= 1
            raise SensorError(f"{channel} sensor temporarily unavailable")

        spec = self._sensor_specs[channel]
        if channel == "distance":
            value = self._nearest_obstacle_distance()
        elif channel == "temperature":
            drift = self.scenario.temperature_drift * math.sin(self._tick / 40.0)
            value = self.scenario.temperature_base + drift + self._rng.uniform(-0.2, 0.2)
        elif channel == "battery_voltage":
            value = self._battery_voltage()
        else:  # imu_accel
            value = self._rng.gauss(0.0, 0.25)

        return round(spec.clamp(value) + self._rng.uniform(-spec.noise, spec.noise), 4)

    def _nearest_obstacle_distance(self) -> float:
        best = SENSOR_RANGES["distance"][1]
        for ox, oy, radius in self.scenario.obstacles:
            distance = math.hypot(self.x - ox, self.y - oy) - radius
            if distance < best:
                best = distance
        return max(best, SENSOR_RANGES["distance"][0])

    def _battery_voltage(self) -> float:
        """Linear-ish discharge curve: 16.8 V full, 12.0 V empty."""
        fraction = max(0.0, self.battery_wh / self.battery_capacity_wh)
        empty, full = 12.0, 16.8
        return empty + (full - empty) * fraction

    def inject_sensor_fault(self, ticks: int = 1) -> None:
        """Make the next ``ticks`` sensor reads fail, to exercise fault handling."""
        if ticks < 0:
            raise ValueError("ticks must be non-negative")
        self._fault_injection = ticks

    # ------------------------------------------------------------------ #
    # Actuators
    # ------------------------------------------------------------------ #
    def move(self, distance_m: float, speed_mps: float | None = None) -> float:
        """Drive forward ``distance_m`` metres. Returns energy consumed in Wh.

        Raises:
            ValueError: negative distance, non-positive speed, or a flat battery.
        """
        if distance_m < 0:
            raise ValueError("distance_m must be non-negative")
        speed = self.max_speed_mps if speed_mps is None else float(speed_mps)
        if speed <= 0:
            raise ValueError("speed_mps must be positive")
        if self.battery_wh <= 0:
            raise ValueError("cannot move: battery is depleted")
        if speed > self.max_speed_mps:
            raise ValueError(f"speed {speed} exceeds max_speed_mps {self.max_speed_mps}")

        seconds = distance_m / speed
        required = distance_m * ENERGY_PER_METRE_WH + seconds * ENERGY_PER_SECOND_WH
        if required > self.battery_wh:
            raise ValueError(
                f"insufficient energy: need {required:.2f} Wh, have {self.battery_wh:.2f} Wh"
            )

        self.x += distance_m * math.cos(self.heading_rad)
        self.y += distance_m * math.sin(self.heading_rad)
        self.travelled_m += distance_m
        self.active_seconds += seconds
        self.battery_wh -= required
        self.odometry.append((round(self.x, 4), round(self.y, 4)))
        return round(required, 4)

    def turn(self, degrees: float) -> None:
        """Rotate in place. Costs energy but does not translate."""
        self.heading_rad = (self.heading_rad + math.radians(degrees)) % (2 * math.pi)
        self.active_seconds += abs(degrees) / 90.0

    def stop(self) -> dict[str, Any]:
        """Emergency stop. Idles the robot and returns the status snapshot."""
        self.active_seconds += 0.0
        return self.status()

    def idle(self, seconds: float) -> float:
        """Consume idle energy for ``seconds``. Returns Wh consumed."""
        if seconds < 0:
            raise ValueError("seconds must be non-negative")
        cost = seconds * IDLE_ENERGY_PER_SECOND_WH
        self.battery_wh = max(0.0, self.battery_wh - cost)
        return round(cost, 5)

    # ------------------------------------------------------------------ #
    # State
    # ------------------------------------------------------------------ #
    def status(self) -> dict[str, Any]:
        """Return an immutable snapshot of the robot's state."""
        return {
            "name": self.name,
            "position": (round(self.x, 4), round(self.y, 4)),
            "heading_deg": round(math.degrees(self.heading_rad), 2),
            "battery_wh": round(self.battery_wh, 4),
            "battery_capacity_wh": self.battery_capacity_wh,
            "battery_pct": round(
                100.0 * self.battery_wh / self.battery_capacity_wh, 2
            ),
            "travelled_m": round(self.travelled_m, 4),
            "active_seconds": round(self.active_seconds, 3),
            "odometry_points": len(self.odometry),
        }

    def is_low_battery(self, threshold_pct: float = 20.0) -> bool:
        """True when remaining charge is below ``threshold_pct``."""
        return (self.battery_wh / self.battery_capacity_wh) * 100.0 < threshold_pct

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return (
            f"SimulatedRobot(name={self.name!r}, x={self.x:.2f}, y={self.y:.2f}, "
            f"battery_wh={self.battery_wh:.2f})"
        )
