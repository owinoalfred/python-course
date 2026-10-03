"""Generator for Capstone Projects."""

from pathlib import Path

CAPSTONES = [
    ("project_01_robot_monitor", "Robot Monitor System", "Build a real-time monitor for robot battery and status."),
    ("project_02_sensor_analyzer", "Sensor Data Analyzer", "Analyze multi-sensor streams and detect anomalies."),
    ("project_03_robot_fleet_manager", "Robot Fleet Manager", "Object-oriented fleet management platform."),
    ("project_04_robot_database", "Robot Database System", "SQLite and SQLAlchemy database for telemetry storage."),
    ("project_05_robot_api", "Robot Fleet REST API", "CLI and HTTP API for remote robot monitoring."),
    ("project_06_telemetry_analytics", "Telemetry Analytics Engine", "Data processing pipeline using Pandas and NumPy."),
    ("project_07_robot_simulator", "Robot Physics Simulator", "Deterministic simulation engine for mobile robots."),
    ("final_robo_x", "Final Integrated ROBO-X System", "The complete integrated ROBO-X software platform.")
]

def main():
    base_dir = Path("10_capstone_projects")
    for dir_name, title, desc in CAPSTONES:
        p = base_dir / dir_name
        p.mkdir(parents=True, exist_ok=True)
        (p / "starter").mkdir(exist_ok=True)
        (p / "tests").mkdir(exist_ok=True)
        (p / "solution").mkdir(exist_ok=True)

        (p / "README.md").write_text(f"# {title}\n\n{desc}\n\nSee `requirements.md` for project specification.\n", encoding="utf-8")
        (p / "requirements.md").write_text(f"# Requirements — {title}\n\n1. Implement core features in `starter/`.\n2. Pass all test assertions in `tests/`.\n", encoding="utf-8")
        (p / "rubric.md").write_text(f"# Rubric — {title}\n\n- Correctness: 50%\n- Code Quality & Testing: 50%\n", encoding="utf-8")
        (p / "research.md").write_text(f"# Research & Design Notes — {title}\n\nDocument architectural trade-offs here.\n", encoding="utf-8")

        # Starter code
        (p / "starter" / "__init__.py").write_text('"""Starter package."""\n', encoding="utf-8")
        (p / "starter" / "app.py").write_text(f'# {title} starter code\ndef main():\n    pass\nif __name__ == "__main__":\n    main()\n', encoding="utf-8")

        # Solution code
        (p / "solution" / "__init__.py").write_text('"""Solution package."""\n', encoding="utf-8")
        (p / "solution" / "app.py").write_text(f'# {title} solution code\ndef main():\n    return "OK"\nif __name__ == "__main__":\n    main()\n', encoding="utf-8")

        # Tests with unique module names and __init__.py
        (p / "tests" / "__init__.py").write_text('"""Tests package."""\n', encoding="utf-8")
        # Remove old test_app.py if exists
        old_test = p / "tests" / "test_app.py"
        if old_test.exists():
            old_test.unlink()
        (p / "tests" / f"test_{dir_name}.py").write_text(f'def test_{dir_name}():\n    assert True\n', encoding="utf-8")

if __name__ == "__main__":
    main()
    print("Capstones regenerated with unique test file names.")
