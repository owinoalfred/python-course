# Complete Professional Python Master Course

Welcome to the **Python Master Course** — a complete, professional, university-quality Python curriculum built around a continuous robotics engineering project called **ROBO-X**.

## Course Structure

- **00_course_orientation/**: Welcome, setup guides, learning methodology, troubleshooting.
- **01_getting_started/** through **09_practical_skills/**: 50+ topics covering Beginner to Advanced Python & Software Engineering.
- **10_capstone_projects/**: 8 comprehensive capstone projects including `final_robo_x`.
- **robo_x/**: The continuous ROBO-X autonomous robotics system.
- **datasets/**: Realistic sensor, telemetry, and fleet datasets.
- **assessments/**: Question bank, quizzes, programming assessments, and rubrics.
- **shared/**: Shared simulation engine (`robo_x_sim.py`).
- **tests/**: Unit, integration, and course validation tests.
- **tools/**: Build automation and course integrity checkers.

## Getting Started

1. **Install Dependencies:**
   ```bash
   python3 -m pip install -r requirements.txt
   ```

2. **Run Course Validation:**
   ```bash
   python tools/course_integrity_checker.py
   ```

3. **Build Notebooks:**
   ```bash
   python tools/build_course.py
   ```

4. **Run Tests:**
   ```bash
   python -m pytest
   ```
