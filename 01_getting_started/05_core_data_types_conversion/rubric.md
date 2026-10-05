# Rubric — 1.5 Core Data Types and Type Conversion

**Module 1: Getting Started with Python**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| exercises.ipynb | 40% | All 10 exercises implemented and edge-cased. |
| mini_project.ipynb | 25% | telemetry.py plus its test suite. |
| robotics_challenge.ipynb | 25% | Frame gate reports every problem. |
| research.ipynb | 10% | Real measurements with a defensible conclusion. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 30 | Conversions, ranges and fallbacks all behave as specified. |
| Boundary discipline | 25 | Parsing happens once, at the edge, and never raises. |
| Code quality | 25 | PEP 8 naming, docstrings, small focused functions. |
| Reasoning | 20 | Float and Decimal trade-offs explained in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — Every exercise implemented, a corrupt channel is reported by name while the rest survive, and the float comparison uses a justified tolerance.
* **Merit** — Most exercises correct; testing covers the main paths; malformed input is handled but the boolean edge case is untested.
* **Pass** — Core requirements met, but the parser raises on one bad channel, or floats are compared with ==.
* **Fail** — Conversion happens inside the control loop with no validation, or booleans silently pass as sensor readings.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
