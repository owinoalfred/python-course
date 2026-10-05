# Rubric — 1.7 Basic Input/Output

**Module 1: Getting Started with Python**

## What is assessed

| Artefact | Weight | Evidence expected |
| --- | --- | --- |
| exercises.ipynb | 40% | All 10 exercises implemented and edge-cased. |
| mini_project.ipynb | 25% | roboctl.py plus its test suite. |
| robotics_challenge.ipynb | 25% | Dispatch console stays parseable. |
| research.ipynb | 10% | Real measurements with a defensible conclusion. |

## Performance criteria

| Criterion | Weight | Description |
| --- | --- | --- |
| Correctness | 30 | Rendering, parsing and exit codes behave as specified. |
| Stream discipline | 25 | Data on stdout, diagnostics on stderr, both injectable. |
| Code quality | 25 | PEP 8 naming, docstrings, small focused functions. |
| Reasoning | 20 | Buffering and quadratic-cost claims explained in writing. |

## Band descriptors

| Band | Range | Overall descriptor |
| --- | --- | --- |
| Distinction | 85-100 | Correct, tested, clearly reasoned, production-shaped. |
| Merit | 70-84 | Correct with minor gaps in testing or documentation. |
| Pass | 50-69 | Core requirement met; edge cases or tests incomplete. |
| Fail | 0-49 | Core requirement not met, or the code does not run. |

## Grade descriptors by band

* **Distinction** — Every exercise implemented, stdout stays free of warnings, and every exit code is asserted without touching sys.argv or input.
* **Merit** — Most exercises correct; streams are injected but one warning path still writes to stdout and is untested.
* **Pass** — Core requirements met, but the code calls input directly and therefore cannot be tested.
* **Fail** — Output streams are mixed, or a read loop spins forever on end of input.

## Academic integrity

Submit work you can explain line by line. Solutions exist in [`solution.ipynb`](solution.ipynb) for self-checking; graded work must be your own. See [`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).

## Submission checklist

- All notebook cells executed from a clean kernel, top to bottom.
- `python tools/notebook_validator.py <this topic>` passes.
- Tests run and their output is included in the write-up.
- README/dev notes state any deviation from the specification.
