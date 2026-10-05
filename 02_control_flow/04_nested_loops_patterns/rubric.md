# Rubric — 2.4 Nested Loops and Common Patterns

**Module 2: Control Flow and Loops**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| exercises.ipynb | 40% | All 10 exercises implemented and edge-cased. |
| mini_project.ipynb | 25% | coverage.py plus its test suite. |
| robotics_challenge.ipynb | 25% | Planner degrades safely. |
| research.ipynb | 10% | Real measurements with a defensible conclusion. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 30 | Ragged grids, empty grids and boundaries are all handled. |
| Cost awareness | 25 | Cost is derived or measured, not assumed. |
| Code quality | 25 | PEP 8 naming, docstrings, small focused functions. |
| Reasoning | 20 | Complexity claims explained in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — Every exercise implemented, a ragged grid is measured rather than truncated, and the cost of the scan is stated in the write-up.
* **Merit** — Most exercises correct; the grid logic is right but a fixed inner bound is guarded rather than removed, and the ragged case is untested.
* **Pass** — Core requirements met, but the nested scan is quadratic where a linear one was available, and the empty grid case raises.
* **Fail** — A hard-coded inner bound is used, so the program crashes on real sensor data.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
