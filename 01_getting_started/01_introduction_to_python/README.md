# 1.1 — Introduction to Python

**Module 1: Getting Started with Python**

Where Python came from, how CPython actually runs your code, and why a language built for readability ended up running most of modern robotics.

## Why this topic matters

Choosing a language is a long-term commitment. Python powers ROS 2 client code, most perception tooling, and every fleet dashboard you will ever be on call for. The interpreter model you learn here also explains every surprising error message you will meet in this course.

## Learning objectives

1. Explain CPython's four-stage execution pipeline from source to bytecode.
2. Distinguish name binding from typed assignment, and predict rebinding.
3. Write a PEP 8 script with a docstring and a main guard.
4. Read a traceback and locate the failing line and expression.
5. Explain why robotics orchestration is written in Python.

## Prerequisites

- No programming experience assumed.
- Basic familiarity with installing software and using a terminal.

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: ROBO-X Boot Diagnostics | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Telemetry Readiness Controller | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Boot banner formatter | MEDIUM | variables, f-strings, functions |
| 2 | Sensor string to float | MEDIUM | type conversion, exception handling, defaults |
| 3 | Total distance travelled | MEDIUM | loops, accumulators, floats |
| 4 | Clamp a battery percentage | MEDIUM | conditionals, comparison, clamping |
| 5 | Pair sensor names with readings | MEDIUM | dictionaries, zip, iteration |
| 6 | Parse a configuration line | HARD | strings, dictionaries, validation |
| 7 | Distance between two waypoints | HARD | tuples, arithmetic, math |
| 8 | Run-length encode a string | HARD | strings, loops, state |
| 9 | Word frequency table | HARD | strings, dictionaries, sorting |
| 10 | Validate robot state records | HARD | dictionaries, validation, error reporting |

## Robotics challenge — ROBO-X Challenge: Telemetry Readiness Controller

Implement `process_telemetry(data)` so it reads the requested sensor channels from the simulator, survives individual sensor failures, and returns a report the fleet supervisor can act on.

**ROBO-X milestone:** M1

## Research task

How does interpreter start-up time change with the size of the modules a program imports?

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
