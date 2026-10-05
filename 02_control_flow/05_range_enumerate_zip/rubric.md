# Rubric — 2.5 range, enumerate and zip

**Module 2: Control Flow and Loops**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| exercises.ipynb | 40% | All 10 exercises implemented and edge-cased. |
| mini_project.ipynb | 25% | telemetry.py plus its test suite. |
| robotics_challenge.ipynb | 25% | Log never truncates silently. |
| research.ipynb | 10% | Real measurements with a defensible conclusion. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 30 | Steps, timestamps and pairing all agree. |
| Idiom | 25 | enumerate, range and zip are used rather than hand-rolled. |
| Code quality | 25 | PEP 8 naming, docstrings, small focused functions. |
| Reasoning | 20 | Truncation and laziness explained in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — Every exercise implemented, the log cannot truncate silently, and a dropped reading leaves a gap rather than renumbering later steps.
* **Merit** — Most exercises correct; the log is built with a hand-maintained counter and the drift case is untested.
* **Pass** — Core requirements met, but the two streams are zipped without strict and a deliberate mismatch is not detected.
* **Fail** — The log is shorter than the batch and the lost steps are never reported.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
