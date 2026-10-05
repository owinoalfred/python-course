# Rubric — 2.2 for Loops and while Loops

**Module 2: Control Flow and Loops**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| exercises.ipynb | 40% | All 10 exercises implemented and edge-cased. |
| mini_project.ipynb | 25% | poller.py plus its test suite. |
| robotics_challenge.ipynb | 25% | Bounded poller degrades safely. |
| research.ipynb | 10% | Real measurements with a defensible conclusion. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 30 | Accumulation, early exit and boundaries all behave as specified. |
| Bounded iteration | 25 | No loop can exceed its budget, and the reason is stated. |
| Code quality | 25 | PEP 8 naming, docstrings, small focused functions. |
| Reasoning | 20 | Cost and termination claims explained in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — Every exercise implemented, an injected sensor fault is handled inside the retry budget, and the budget itself is proven by a test.
* **Merit** — Most exercises correct; the poller works but reuses an exhausted iterator, which is untested.
* **Pass** — Core requirements met, but a while loop is used for the retry with no bound, so the failure mode is a hang rather than a report.
* **Fail** — An unbounded loop, or a route follower that drops the final waypoint.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
