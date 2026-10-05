# Rubric — 2.3 Loop Control

**Module 2: Control Flow and Loops**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| exercises.ipynb | 40% | All 10 exercises implemented and edge-cased. |
| mini_project.ipynb | 25% | scanner.py plus its test suite. |
| robotics_challenge.ipynb | 25% | Scanner degrades safely. |
| research.ipynb | 10% | Real measurements with a defensible conclusion. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 30 | Early exit, skipping and the else all behave as specified. |
| Control flow clarity | 25 | No flag drift; the exit path is obvious to a reader. |
| Code quality | 25 | PEP 8 naming, docstrings, small focused functions. |
| Reasoning | 20 | Cost and complexity claims explained in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — Every exercise implemented, the not-found path is tested, and the scan reports the first genuine fault while skipping junk ahead of it.
* **Merit** — Most exercises correct; the scan works but uses a flag variable reset by hand, and the reset is untested.
* **Pass** — Core requirements met, but continue is used where break was meant, so the scan reports a later match or none at all.
* **Fail** — The loop reports the last match instead of the first, or a malformed sample raises and aborts the scan.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
