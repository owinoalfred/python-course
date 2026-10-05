# 1.2 — Installing Python, IDEs, and the REPL

**Module 1: Getting Started with Python**

Turn 'it works on my machine' into a fact you can print. This topic covers how an installation is actually put together, how to identify the running interpreter, and how to build a pre-flight check any deployment can call.

## Why this topic matters

Most Python problems that are not logic problems are environment problems. Knowing exactly which interpreter runs, which packages it can see, and how to prove both in one command is the difference between a five-minute fix and an afternoon of guessing.

## Learning objectives

1. Identify the running interpreter and its version programmatically.
2. Explain how PATH and sys.path decide which program and module wins.
3. Create and inspect a virtual environment using the standard library.
4. Detect an optional dependency without importing it.
5. Build a pre-flight readiness check that returns an exit status.

## Prerequisites

- Topic 1.1 Introduction to Python
- Ability to open a terminal and run a command.

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Machine Readiness Checker | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Bring-Up Readiness Gate | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Format an environment report line | MEDIUM | f-strings, tuples, sys |
| 2 | Tuple-safe version comparison | MEDIUM | tuples, comparison, validation |
| 3 | Describe the running interpreter | MEDIUM | sys, dicts, modules |
| 4 | Check an optional dependency safely | MEDIUM | importlib, modules, booleans |
| 5 | Join path segments portably | MEDIUM | pathlib, strings, composition |
| 6 | Parse a pinned dependency block | HARD | strings, dicts, parsing |
| 7 | Verify required modules against what is present | HARD | sets, dicts, validation |
| 8 | Resolve the first available interpreter launcher | HARD | shutil.which, loops, error reporting |
| 9 | Summarise the module search path | HARD | sys.path, sets, ordering |
| 10 | Assemble a machine pre-flight report | HARD | dicts, composition, validation, sys |

## Robotics challenge — ROBO-X Challenge: Bring-Up Readiness Gate

Implement `check_readiness(channels)` that combines an environment report with a live sensor read from the simulator and returns a single decision the fleet supervisor can gate on.

**ROBO-X milestone:** M1

## Research task

How much does interpreter start-up time change between a bare script and a script that imports common data-science libraries?

## Recommended workflow

1. Read `lesson.ipynb` end to end, running every code cell.
2. Answer the knowledge checks without looking back.
3. Attempt `exercises.ipynb` — all eleven tasks.
4. Run the research experiment and record real measurements.
5. Take the quiz; re-read any section you failed.
6. Build the mini-project and write its tests.
7. Implement the ROBO-X challenge and commit it to the project repo.

## Navigation

* Module index: [`01_getting_started/README.md`](../README.md)
* Course path: [`LEARNING_PATH.md`](../../../LEARNING_PATH.md)
