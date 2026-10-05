# Complete Professional Python Master Course

Welcome to the **Python Master Course** — a complete, professional, university-quality Python curriculum built around a continuous robotics engineering project called **ROBO-X**.

## Course Structure

- **00_course_orientation/**: Welcome, setup guides, learning methodology, troubleshooting.
- **01_getting_started/** through **09_practical_skills/**: 65 topics covering Beginner to Advanced Python & Software Engineering. Each module has a generated index README.
- **10_capstone_projects/**: 8 comprehensive capstone projects including `final_robo_x`.
- **robo_x/**: The continuous ROBO-X autonomous robotics system.
- **datasets/**: Realistic sensor, telemetry, and fleet datasets.
- **assessments/**: Question bank, quizzes, programming assessments, and rubrics.
- **shared/**: Shared simulation engine (`robo_x_sim.py`).
- **tests/**: Unit, integration, and course validation tests.
- **tools/**: Build automation, content linter, and integrity checkers.

## Content standard

Every topic must satisfy the Course Content Standard, and it is **enforced by
code** rather than by review:

| Rule | Requirement |
| --- | --- |
| Lesson size | ≥ 2,500 words across all 25 sections |
| Runnable code | ≥ 12 executable code cells in `lesson.ipynb` |
| Quiz integrity | 10 questions, ≥ 4 kinds, no answer letter above 40 % |
| Exercise quality | Real examples; no placeholder or duplicated filler text |
| Research integrity | No pre-filled measurement tables — the learner measures |
| Version | Python 3.12 everywhere (content, manifest, notebooks) |

## Getting Started

1. **Install Dependencies:**
   ```bash
   python3 -m pip install -r requirements.txt
   ```

2. **Build all notebooks, docs and indexes:**
   ```bash
   python tools/build_course.py
   ```

3. **Run Course Validation:**
   ```bash
   python tools/course_integrity_checker.py
   python tools/notebook_validator.py
   ```

4. **Check content quality:**
   ```bash
   python tools/build_course.py --lint          # dashboard for the whole course
   python tools/coursegen/lint.py --topic 1.1   # one topic
   python tools/coursegen/lint.py --strict      # non-zero exit if anything fails
   ```

5. **Run Tests:**
   ```bash
   python -m pytest
   ```

6. **Everything at once:**
   ```bash
   python run_all.py
   ```
