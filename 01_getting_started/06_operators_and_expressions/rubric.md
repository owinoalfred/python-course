# Rubric — 1.6 Operators and Expressions

**Module 1: Getting Started with Python**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| exercises.ipynb | 40% | All 10 exercises implemented and edge-cased. |
| mini_project.ipynb | 25% | status_word.py plus its test suite. |
| robotics_challenge.ipynb | 25% | Status controller fails safe. |
| research.ipynb | 10% | Real measurements with a defensible conclusion. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 30 | Masking, precedence and round trips all behave as specified. |
| Safety behaviour | 25 | Failed sensors take the dangerous path, never the safe one. |
| Code quality | 25 | PEP 8 naming, docstrings, small focused functions. |
| Reasoning | 20 | Precedence and complexity claims explained in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — Every exercise implemented, the flag round trip is exact, and an injected sensor fault produces OBSTACLE rather than an exception.
* **Merit** — Most exercises correct; the decoder is right but unknown bits are dropped instead of reported, and that gap is untested.
* **Pass** — Core requirements met, but a sensor error is swallowed and the robot is treated as having a clear path.
* **Fail** — Masking is wrong so flags are corrupted, or the ast exercises call eval.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
