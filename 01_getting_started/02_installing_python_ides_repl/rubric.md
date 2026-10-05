# Rubric — 1.2 Installing Python, IDEs, and the REPL

**Module 1: Getting Started with Python**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| exercises.ipynb | 40% | All 10 exercises implemented and edge-cased. |
| mini_project.ipynb | 25% | check_ready.py plus its test suite. |
| robotics_challenge.ipynb | 25% | Readiness gate degrades safely. |
| research.ipynb | 10% | Real measurements with a defensible conclusion. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 35 | Every documented edge case is handled and tested. |
| Diagnostics quality | 25 | Failures name the specific cause, not a generic error. |
| Code quality | 20 | PEP 8 naming, docstrings, small focused functions. |
| Reasoning | 20 | Complexity claims are true and explained in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — Every exercise implemented, every listed edge case tested, and the readiness gate degrades safely under an injected sensor fault.
* **Merit** — Most exercises correct; testing covers the main paths and several edge cases; failure messages are specific but not exhaustive.
* **Pass** — Core requirements met on the main paths, but testing is thin or some edge cases are unhandled.
* **Fail** — Multiple exercises missing or non-functional, no tests, or a bare except that hides the real cause of a failure.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
