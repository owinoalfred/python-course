# Rubric — 3.2 Tuples

**Module 3: Core Data Structures**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| [`exercises.ipynb`](exercises.ipynb) | 40% | All 10 exercises with validation and unpacking shown. |
| [`mini_project.ipynb`](mini_project.ipynb) | 25% | MissionRecordStore with hashable, isolated records. |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | 25% | Frozen envelope dedupes in O(n) and cannot be mutated. |
| [`research.ipynb`](research.ipynb) | 10% | Tuple vs string key timings with a defensible verdict. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 30 | Every example, error path and edge case behaves as specified. |
| Immutability reasoning | 25 | Shallow-vs-deep immutability explained and enforced in code. |
| Code quality | 25 | PEP 8, docstrings, validation at boundaries. |
| Reasoning | 20 | Hashability and quadratic accumulation justified in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — All exercises correct, freeze proven by hash() assertions, and the version comparison handles the 3.9-vs-3.10 trap explicitly.
* **Merit** — Most exercises correct; one validation path missing or the quadratic accumulation not discussed.
* **Pass** — Core behaviour right but a list survives inside a returned structure, or duplicate-id detection is absent.
* **Fail** — Records returned as lists, or hashability never demonstrated.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
