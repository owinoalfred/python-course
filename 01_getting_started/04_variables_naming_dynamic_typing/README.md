# 1.4 — Variables, Naming Conventions, and Dynamic Typing

**Module 1: Getting Started with Python**

A name is a label, not a box. Binding, aliasing, shared mutation and the naming conventions that keep a fleet's code readable to the next engineer.

## Why this topic matters

Almost every confusing bug in a Python codebase comes from one of three facts on this page: assignment does not copy, names can be rebound to a different type, and two names can share one object. Robotics code passes values between stages constantly, so these three facts decide whether a pipeline is predictable.

## Learning objectives

1. Explain the difference between a name and the object it refers to.
2. Predict the effect of rebinding a name to a value of another type.
3. Demonstrate aliasing and choose correctly between copy and reference.
4. Apply PEP 8 naming for functions, classes, constants and internals.
5. Avoid shadowing built-ins and identify the failure mode when it happens.
6. Validate and cast configuration values once at a system boundary.

## Prerequisites

- Topic 1.1 Introduction to Python
- Topic 1.3 Syntax, Indentation and Comments

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Robot Settings Registry | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Telemetry Settings Gate | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Validate a snake_case name | MEDIUM | strings, naming, validation |
| 2 | Describe a binding | MEDIUM | type(), repr(), id() |
| 3 | Swap two values with unpacking | MEDIUM | tuples, unpacking, assignment |
| 4 | Parse an assignment line | MEDIUM | strings, split, validation |
| 5 | Convert a label to snake_case | MEDIUM | strings, case conversion, loops |
| 6 | Find duplicate names with their positions | HARD | dicts, sets, enumeration |
| 7 | Make an independent copy of a sequence | HARD | copying, lists, mutability |
| 8 | List the public names in a namespace | HARD | globals, dicts, filtering |
| 9 | Build a validated configuration | HARD | dicts, validation, error reporting |
| 10 | Apply symbol renames without collisions | HARD | dicts, ordering, strings |

## Robotics challenge — ROBO-X Challenge: Telemetry Settings Gate

Implement `load_settings(raw, robot)` that merges settings, casts them, reads a sample from the simulator, and returns a readiness decision that names every problem found.

**ROBO-X milestone:** M1

## Research task

How much do copy-on-boundary practices change the observable behaviour of a small data pipeline?

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
