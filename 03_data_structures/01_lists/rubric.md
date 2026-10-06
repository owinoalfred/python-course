# Rubric — 3.1 Lists

**Module 3: Core Data Structures**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| [`exercises.ipynb`](exercises.ipynb) | 40% | All 10 exercises implemented with copy discipline proven. |
| [`mini_project.ipynb`](mini_project.ipynb) | 25% | FlightRecorder with copy-on-read tests. |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | 25% | PlanRegistry isolates subscribers from the canonical plan. |
| [`research.ipynb`](research.ipynb) | 10% | Real concat-vs-append timings with a defensible conclusion. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 30 | Every example and edge case behaves exactly as specified. |
| Mutation discipline | 25 | No alias leaks; every boundary copy is deliberate and tested. |
| Code quality | 25 | PEP 8 naming, docstrings, small focused helpers. |
| Reasoning | 20 | Aliasing and None-assignment explained in writing, not guessed. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — Every exercise correct, mutation isolation proven by assertion, and the in-place rotation demonstrably uses O(1) extra memory.
* **Merit** — Most exercises correct; one boundary returns an alias or one test skips the shallow-copy case.
* **Pass** — Core behaviour right, but copies are made defensively everywhere without justification, or sort() None-assignment still appears once.
* **Fail** — The canonical store is mutated through a returned reference, or several exercises are missing entirely.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
