# 2.5 — range, enumerate and zip

**Module 2: Control Flow and Loops**

Three built-ins that remove the bookkeeping loops force on you, and the one silent failure each of them can still produce.

## Why this topic matters

A mission log that silently drops a step, or shifts every timestamp after a dropped reading, is a safety defect rather than a cosmetic one. These built-ins exist because the manual versions of these loops get this wrong.

## Learning objectives

1. Use enumerate instead of a hand-maintained counter and manual indexing.
2. Explain why the stop value of range is exclusive.
3. State why range is lazy and why that matters for large bounds.
4. Predict what zip does when its inputs differ in length.
5. Use strict=True to convert a silent truncation into a loud failure.
6. Derive a time base from the data index so a dropped item leaves a gap.

## Prerequisites

- Topic 2.4 Nested Loops and Common Patterns

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Step-Indexed Telemetry Log | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Step-Indexed Mission Log | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Find a value's index with enumerate | MEDIUM | enumerate, search, search |
| 2 | Take every other item with a stepped range | MEDIUM | range, slicing, stepping |
| 3 | Pair commands with battery readings | MEDIUM | zip, strict, validation |
| 4 | Build a countdown with a negative step | MEDIUM | range, stepping, boundaries |
| 5 | Zip two sequences with a fill value | MEDIUM | zip, itertools, padding |
| 6 | Run-length encode a sequence | HARD | enumerate, grouping, itertools |
| 7 | Transpose a table with zip | HARD | zip, unpacking, transformations |
| 8 | Attach generated timestamps to readings | HARD | zip, generators, validation |
| 9 | Build a mission log from a command schedule | HARD | zip, strict, simulator API |
| 10 | Pair attempts with backoff delays | HARD | range, zip, generators |

## Robotics challenge — ROBO-X Challenge: Step-Indexed Mission Log

Implement `build_mission_log(robot, readings, period_s)` returning a log whose steps are 1-based and whose timestamps come from the batch index.

**ROBO-X milestone:** M2

## Research task

How much does generating the second stream of a zip cost compared with slicing it first?

## Recommended workflow

1. Read `lesson.ipynb` end to end, running every code cell.
2. Answer the knowledge checks without looking back.
3. Attempt `exercises.ipynb` — all eleven tasks.
4. Run the research experiment and record real measurements.
5. Take the quiz; re-read any section you failed.
6. Build the mini-project and write its tests.
7. Implement the ROBO-X challenge and commit it to the project repo.

## Navigation

* Module index: [`02_control_flow/README.md`](../README.md)
* Course path: [`LEARNING_PATH.md`](../../../LEARNING_PATH.md)
