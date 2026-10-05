# Rubric — 1.3 Python Syntax, Indentation, Comments, and Code Structure

**Module 1: Getting Started with Python**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| exercises.ipynb | 40% | All 10 exercises implemented and edge-cased. |
| mini_project.ipynb | 25% | diagnostics.py plus its test suite. |
| robotics_challenge.ipynb | 25% | Log reader degrades safely. |
| research.ipynb | 10% | Real measurements with a defensible conclusion. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 35 | Parsing handles ragged, empty and comment-heavy input. |
| Code quality | 25 | PEP 8 naming, docstrings, small focused functions. |
| Testing | 25 | Assertions cover happy path, edge cases and failure. |
| Reasoning | 15 | Complexity claims are true and explained in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — Every exercise implemented, ragged input handled without raising, and the log reader round-trips the simulator's own output correctly.
* **Merit** — Most exercises correct; testing covers the main paths and several edge cases; the stack logic is correct on well-formed input.
* **Pass** — Core requirements met on well-formed input, but ragged indentation or comment-only input is unhandled and untested.
* **Fail** — The parser cannot handle nesting, or uses recursion and overflows on deep input without any test covering it.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
