# Contributing Guidelines

Thank you for contributing to the Python Master Course!

## Content Authoring Workflow

1. Edit or add topics in `course_content/moduleN.py`.
2. Validate topic schema:
   ```bash
   python tools/build_course.py --check
   ```
3. Build notebooks:
   ```bash
   python tools/build_course.py
   ```
4. Audit integrity:
   ```bash
   python tools/course_integrity_checker.py
   ```
5. Run unit tests:
   ```bash
   python -m pytest
   ```
