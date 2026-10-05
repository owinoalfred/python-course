# Module 10 — Capstone Projects & Final ROBO-X System

The eight capstone projects turn the isolated skills from Modules 1–9 into complete, tested applications. Each project ships a specification, a starter package with failing tests, a reference solution and a rubric.

Work them in order: every project reuses assets built by the previous one.

## Projects

| # | Project | Focus |
| --- | --- | --- |
| 1 | [Robot Monitor System](project_01_robot_monitor/README.md) | Build a real-time monitor that tracks robot battery and status from a telemetry stream and raises alerts on threshold breaches. |
| 2 | [Sensor Data Analyzer](project_02_sensor_analyzer/README.md) | Load raw sensor logs and produce descriptive statistics, trends and anomaly flags. |
| 3 | [Robot Fleet Manager](project_03_robot_fleet_manager/README.md) | Model a fleet of robots, assign tasks and track each machine's state through a dispatch lifecycle. |
| 4 | [Robot Database System](project_04_robot_database/README.md) | Design a relational schema and implement CRUD, constraints and transactions for fleet data in SQLite. |
| 5 | [Robot Fleet REST API](project_05_robot_api/README.md) | Expose fleet operations over an HTTP API with validated requests and meaningful status codes. |
| 6 | [Telemetry Analytics Engine](project_06_telemetry_analytics/README.md) | Ingest, aggregate and visualise telemetry to answer operational questions about robot performance. |
| 7 | [Robot Physics Simulator](project_07_robot_simulator/README.md) | Extend the ROBO-X simulator with obstacle avoidance and a deterministic physics step, backed by tests. |
| 8 | [Final Integrated ROBO-X System](final_robo_x/README.md) | Integrate every subsystem built across the course into one tested, documented ROBO-X platform — the graduation project. |

## Anatomy of a capstone

| Path | Purpose |
| --- | --- |
| `README.md` | Overview and the problem being solved. |
| `requirements.md` | Numbered, testable requirements. |
| `research.md` | Design trade-offs and investigation notes. |
| `rubric.md` | How the project is graded. |
| `starter/` | Skeleton package with `TODO`s and failing tests. |
| `tests/` | Automated tests that define "done". |
| `solution/` | Reference implementation that passes the tests. |

## How to work a capstone

1. Read `requirements.md` and restate each requirement as a test.
2. Run the starter tests — they should fail; that is the target.
3. Implement in `starter/` until the tests pass, then harden with edge cases.
4. Compare with `solution/` and grade yourself against `rubric.md`.

## Navigation

* Previous module: [`09_practical_skills/README.md`](../09_practical_skills/README.md)
* Course path: [`LEARNING_PATH.md`](../LEARNING_PATH.md)
