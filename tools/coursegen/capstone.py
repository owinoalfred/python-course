"""Generate the capstone-projects index README.

The eight capstone projects live in ``10_capstone_projects/``. This module
generates their index (``10_capstone_projects/README.md``) from the canonical
directory list so navigation can never drift from the projects that exist.
"""

from __future__ import annotations

from pathlib import Path

from .catalogue import CAPSTONE_DIRS

#: Human-readable title per capstone directory.
CAPSTONE_TITLES: dict[str, str] = {
    "project_01_robot_monitor": "Robot Monitor System",
    "project_02_sensor_analyzer": "Sensor Data Analyzer",
    "project_03_robot_fleet_manager": "Robot Fleet Manager",
    "project_04_robot_database": "Robot Database System",
    "project_05_robot_api": "Robot Fleet REST API",
    "project_06_telemetry_analytics": "Telemetry Analytics Engine",
    "project_07_robot_simulator": "Robot Physics Simulator",
    "final_robo_x": "Final Integrated ROBO-X System",
}

#: One-line description per capstone directory.
CAPSTONE_BLURBS: dict[str, str] = {
    "project_01_robot_monitor": (
        "Build a real-time monitor that tracks robot battery and status from a "
        "telemetry stream and raises alerts on threshold breaches."
    ),
    "project_02_sensor_analyzer": (
        "Load raw sensor logs and produce descriptive statistics, trends and "
        "anomaly flags."
    ),
    "project_03_robot_fleet_manager": (
        "Model a fleet of robots, assign tasks and track each machine's state "
        "through a dispatch lifecycle."
    ),
    "project_04_robot_database": (
        "Design a relational schema and implement CRUD, constraints and "
        "transactions for fleet data in SQLite."
    ),
    "project_05_robot_api": (
        "Expose fleet operations over an HTTP API with validated requests and "
        "meaningful status codes."
    ),
    "project_06_telemetry_analytics": (
        "Ingest, aggregate and visualise telemetry to answer operational "
        "questions about robot performance."
    ),
    "project_07_robot_simulator": (
        "Extend the ROBO-X simulator with obstacle avoidance and a deterministic "
        "physics step, backed by tests."
    ),
    "final_robo_x": (
        "Integrate every subsystem built across the course into one tested, "
        "documented ROBO-X platform — the graduation project."
    ),
}


def build_capstone_index() -> str:
    """Render ``10_capstone_projects/README.md``."""
    parts: list[str] = [
        "# Module 10 — Capstone Projects & Final ROBO-X System",
        "",
        "The eight capstone projects turn the isolated skills from Modules 1–9 "
        "into complete, tested applications. Each project ships a specification, "
        "a starter package with failing tests, a reference solution and a rubric.",
        "",
        "Work them in order: every project reuses assets built by the previous one.",
        "",
        "## Projects",
        "",
        "| # | Project | Focus |",
        "| --- | --- | --- |",
    ]
    for index, directory in enumerate(CAPSTONE_DIRS, start=1):
        title = CAPSTONE_TITLES.get(directory, directory)
        blurb = CAPSTONE_BLURBS.get(directory, "")
        parts.append(f"| {index} | [{title}]({directory}/README.md) | {blurb} |")

    parts += [
        "",
        "## Anatomy of a capstone",
        "",
        "| Path | Purpose |",
        "| --- | --- |",
        "| `README.md` | Overview and the problem being solved. |",
        "| `requirements.md` | Numbered, testable requirements. |",
        "| `research.md` | Design trade-offs and investigation notes. |",
        "| `rubric.md` | How the project is graded. |",
        "| `starter/` | Skeleton package with `TODO`s and failing tests. |",
        "| `tests/` | Automated tests that define \"done\". |",
        "| `solution/` | Reference implementation that passes the tests. |",
        "",
        "## How to work a capstone",
        "",
        "1. Read `requirements.md` and restate each requirement as a test.",
        "2. Run the starter tests — they should fail; that is the target.",
        "3. Implement in `starter/` until the tests pass, then harden with edge cases.",
        "4. Compare with `solution/` and grade yourself against `rubric.md`.",
        "",
        "## Navigation",
        "",
        "* Previous module: [`09_practical_skills/README.md`](../09_practical_skills/README.md)",
        "* Course path: [`LEARNING_PATH.md`](../LEARNING_PATH.md)",
        "",
    ]
    return "\n".join(parts)


def write_capstone_index(root: Path) -> Path:
    """Write ``10_capstone_projects/README.md``. Returns the path written."""
    path = root / "10_capstone_projects" / "README.md"
    path.write_text(build_capstone_index(), encoding="utf-8")
    return path
