# Rubric — 3.4 Dictionaries

**Module 3: Core Data Structures**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| [`exercises.ipynb`](exercises.ipynb) | 40% | All 10 exercises: contracts, copies and merges proven. |
| [`mini_project.ipynb`](mini_project.ipynb) | 25% | SchemaRegistry with validation-before-aggregation. |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | 25% | ParameterServer publishes atomically by rebinding. |
| [`research.ipynb`](research.ipynb) | 10% | Dict-vs-scan ratios measured across four sizes. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 30 | Every contract, error path and merge rule behaves as specified. |
| Isolation discipline | 25 | No shared inner state escapes; clones proven by identity assertions. |
| Code quality | 25 | PEP 8, docstrings, sorted output, small focused helpers. |
| Reasoning | 20 | Access contracts and atomicity justified in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — All exercises correct, get_all isolation proven by identity, and the parameter server rejects a bad update with zero visible change.
* **Merit** — Most exercises correct; one shallow-copy case untested or one sorted-output boundary missing.
* **Pass** — Core dict use right, but get() appears on required keys or a clone shares inner state.
* **Fail** — Live dict mutated during iteration, or validation partially applies an invalid record.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
