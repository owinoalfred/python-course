# Rubric — 1.4 Variables, Naming Conventions, and Dynamic Typing

**Module 1: Getting Started with Python**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| exercises.ipynb | 40% | All 10 exercises implemented and edge-cased. |
| mini_project.ipynb | 25% | settings.py plus its test suite. |
| robotics_challenge.ipynb | 25% | Settings gate reports every problem. |
| research.ipynb | 10% | Real measurements with a defensible conclusion. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 30 | Every documented edge case is handled and tested. |
| Naming discipline | 25 | PEP 8 conventions applied consistently; no shadowing. |
| State safety | 25 | No accidental mutation of arguments or module state. |
| Reasoning | 20 | Complexity claims are true and explained in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — Every exercise implemented, no shared-state leakage between calls, and the settings gate reports every malformed key without raising.
* **Merit** — Most exercises correct; testing covers the main paths; arguments are not mutated but the docstrings do not document the aliasing behaviour.
* **Pass** — Core requirements met, but a shared default or an in-place mutation leaks between calls and is not covered by a test.
* **Fail** — Module-level state is mutated across calls, or a built-in is shadowed and the resulting error is not diagnosed.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
