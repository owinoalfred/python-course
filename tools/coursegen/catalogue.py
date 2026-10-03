"""Course catalogue: the 9 modules and their directory layout.

This is the single source of truth for module numbering and folder names.
``course_manifest.yaml`` is generated from this plus the authored content, and
every validator reads the manifest.
"""

from __future__ import annotations

from dataclasses import dataclass

MODULE_DIRS: dict[int, str] = {
    1: "01_getting_started",
    2: "02_control_flow",
    3: "03_data_structures",
    4: "04_functions_modules",
    5: "05_error_handling_debugging",
    6: "06_object_oriented_programming",
    7: "07_files_data",
    8: "08_databases",
    9: "09_practical_skills",
}

MODULE_TITLES: dict[int, str] = {
    1: "Getting Started with Python",
    2: "Control Flow and Loops",
    3: "Core Data Structures",
    4: "Functions and Modules",
    5: "Error Handling and Debugging",
    6: "Object-Oriented Programming",
    7: "File Handling and Working with Data",
    8: "Databases",
    9: "Intermediate Practical Skills and Best Practices",
}

#: Module number -> ROBO-X milestone produced by that module.
MODULE_MILESTONES: dict[int, str] = {i: f"M{i}" for i in range(1, 10)}

#: Robotics domains rotated across the course so exercises never repeat a
#: scenario. Each module draws from its own band, in order.
MODULE_DOMAINS: dict[int, list[str]] = {
    1: [
        "mobile robot bring-up",
        "drone pre-flight checklist",
        "warehouse AGV dispatch",
    ],
    2: [
        "agricultural field robot",
        "medical delivery cart",
        "underground inspection rover",
    ],
    3: [
        "autonomous vehicle perception",
        "port crane telemetry",
        "cleanroom material handler",
    ],
    4: [
        "manufacturing cell controller",
        "subsea ROV",
        "last-mile logistics fleet",
    ],
    5: [
        "patient-care robot monitoring",
        "satellite ground station",
        "mining haulage truck",
    ],
    6: [
        "modular robotic arm",
        "swarm robotics",
        "exoskeleton actuator bank",
    ],
    7: [
        "flight-test data pipeline",
        "greenhouse climate control",
        "rail inspection unit",
    ],
    8: [
        "fleet operations centre",
        "research data archive",
        "asset maintenance system",
    ],
    9: [
        "robotics-as-a-service platform",
        "autonomous yard mover",
        "smart building robotics",
    ],
}

CAPSTONE_DIRS: tuple[str, ...] = (
    "project_01_robot_monitor",
    "project_02_sensor_analyzer",
    "project_03_robot_fleet_manager",
    "project_04_robot_database",
    "project_05_robot_api",
    "project_06_telemetry_analytics",
    "project_07_robot_simulator",
    "final_robo_x",
)


@dataclass(frozen=True, slots=True)
class Module:
    number: int
    title: str
    directory: str
    milestone: str


def modules() -> list[Module]:
    """Return all nine modules in teaching order."""
    return [
        Module(
            number=number,
            title=MODULE_TITLES[number],
            directory=MODULE_DIRS[number],
            milestone=MODULE_MILESTONES[number],
        )
        for number in sorted(MODULE_DIRS)
    ]


def module_dir(number: int) -> str:
    try:
        return MODULE_DIRS[number]
    except KeyError as exc:  # pragma: no cover - programming error
        raise KeyError(f"unknown module {number}") from exc


def module_title(number: int) -> str:
    return MODULE_TITLES[number]
