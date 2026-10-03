"""Shared support code for the Python Master Course.

The modules here are deliberately dependency-light so they can be imported from
a notebook, a pytest run, or the ``robo_x`` package without extra setup.
"""

from shared.robo_x_sim import (
    SimulatedRobot,
    ScenarioBuilder,
    SensorSpec,
    default_scenario,
)

__all__ = [
    "SimulatedRobot",
    "ScenarioBuilder",
    "SensorSpec",
    "default_scenario",
]
