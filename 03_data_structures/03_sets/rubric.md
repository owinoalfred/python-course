# Rubric — 3.3 Sets

**Module 3: Core Data Structures**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| [`exercises.ipynb`](exercises.ipynb) | 40% | All 10 exercises with set algebra and seen-set idiom. |
| [`mini_project.ipynb`](mini_project.ipynb) | 25% | AnomalyAuditor: linear, reproducible, sorted output. |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | 25% | FaultSupervisor meets the 10 ms query budget. |
| [`research.ipynb`](research.ipynb) | 10% | List-vs-set crossover measured with real timings. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 30 | Every example, direction of difference and edge case correct. |
| Complexity discipline | 25 | No hot-path membership scans; complexity stated and true. |
| Code quality | 25 | PEP 8, docstrings, sorted output at boundaries. |
| Reasoning | 20 | Hashing, orderlessness and algebra justified in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — All exercises correct, reproducibility proven by shuffled-input test, and the crossover from research is quoted with numbers.
* **Merit** — Most exercises correct; one direction-of-difference error or a missing sort at the output boundary.
* **Pass** — Core algebra right, but a linear membership scan survives in a hot path or {} appears as the empty set.
* **Fail** — Set algebra replaced by nested loops, or mutation-during-iteration left unhandled.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
