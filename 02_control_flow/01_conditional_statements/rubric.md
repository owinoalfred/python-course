# Rubric — 2.1 Conditional Statements

**Module 2: Control Flow and Loops**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| exercises.ipynb | 40% | All 10 exercises implemented and edge-cased. |
| mini_project.ipynb | 25% | policy.py plus its test suite. |
| robotics_challenge.ipynb | 25% | Drive interlock fails safe. |
| research.ipynb | 10% | Real measurements with a defensible conclusion. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 30 | Every band, boundary and missing-input case is handled. |
| Policy structure | 25 | Severity order is explicit and provably first-wins. |
| Code quality | 25 | PEP 8 naming, docstrings, small focused functions. |
| Reasoning | 20 | Truthiness and boundary claims explained in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — Every exercise implemented, boundaries tested on both sides, and the severity ordering is proven by a test with several simultaneous failures.
* **Merit** — Most exercises correct; the policy is correct but a truthiness check is used for a value where zero is legitimate, and that case is untested.
* **Pass** — Core requirements met, but the branches overlap or the reason reported is not the most severe failure.
* **Fail** — Repeated if statements with overlapping bands, or a missing reading is treated as a pass.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
