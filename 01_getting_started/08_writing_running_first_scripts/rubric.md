# Rubric — 1.8 Writing and Running Your First Scripts

**Module 1: Getting Started with Python**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| exercises.ipynb | 40% | All 10 exercises implemented and edge-cased. |
| mini_project.ipynb | 25% | roboctl.py plus its test suite. |
| robotics_challenge.ipynb | 25% | Bring-up tool honours its exit codes. |
| research.ipynb | 10% | Real measurements with a defensible conclusion. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Process contract | 30 | Exit codes, stream separation and argv handling are correct. |
| Import safety | 25 | Importing the module starts nothing and prints nothing. |
| Code quality | 25 | PEP 8 naming, docstrings, small focused functions. |
| Reasoning | 20 | Cost and trade-off claims explained in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — Every exercise implemented, importing the module is proven harmless, and every exit code is verified both in-process and through a subprocess.
* **Merit** — Most exercises correct; the guard is in place but import safety is asserted only by reading the code, not by a test.
* **Pass** — Core requirements met, but the tool prints diagnostics to stdout so a supervisor parsing it gets corrupted data.
* **Fail** — No main guard, or sys.exit is called from inside the logic so the exit code cannot be asserted.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
