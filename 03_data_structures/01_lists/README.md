# 3.1 — Lists

**Module 3: Core Data Structures**

Python's ordered, mutable sequence: reference semantics, the two classic list bugs - aliasing and None-returning methods - and the performance profile that follows from an array of pointers.

## Why this topic matters

Every pipeline in the course accumulates data into lists, and the two list bugs strike silently: a shared waypoint plan changes under every component that reads it, and a sorted-assigned-to-None log vanishes one line before it is needed. Mastering reference semantics here is what makes every later collection safe to touch.

## Learning objectives

1. Explain that assignment aliases and that list copies are shallow.
2. Predict which list methods mutate in place and what they return.
3. Copy deliberately at module boundaries with list(), copy() or slicing.
4. Choose between append, extend and concatenation by cost, not habit.
5. Process a list safely when elements must be removed or replaced.
6. State the time complexity of indexing, appending, inserting and scanning.

## Prerequisites

- Topic 2.5 range, enumerate and zip

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Flight Recorder Slice Service | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Waypoint Plan Custodian | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Clamp readings without touching the caller's list | MEDIUM | copying, append, range clamping, immutability of inputs |
| 2 | Rotate a command list with slicing | MEDIUM | slicing, rotation, modulo indexing |
| 3 | Running totals for a battery drain log | MEDIUM | accumulation, append, zip |
| 4 | Batch a telemetry stream into fixed-size chunks | MEDIUM | slicing, range with step, batching |
| 5 | Split evens and odds while keeping their order | MEDIUM | conditional append, stability, two accumulators |
| 6 | Merge two sorted lists in linear time | HARD | two-pointer merge, sorted input, amortised append |
| 7 | Transpose a rectangular matrix into a new one | HARD | nested lists, index swapping, validation, new-list construction |
| 8 | Rotate a list in place with O(1) extra memory | HARD | in-place algorithm, reversal, index arithmetic |
| 9 | Sliding windows with a custom step | HARD | slicing, range strides, window arithmetic |
| 10 | Run-length encode a command stream | HARD | run-length encoding, run detection, tuples in lists |

## Robotics challenge — ROBO-X Challenge: Waypoint Plan Custodian

Implement `PlanRegistry` - a small custodian that hands out snapshots, accepts revisions as new lists, and guarantees no subscriber can mutate the canonical plan.

**ROBO-X milestone:** M3

## Research task

How much slower is building a large list with `a = a + [x]` compared with `a.append(x)`, and does the gap grow with n?

## Recommended workflow

1. Read `lesson.ipynb` end to end, running every code cell.
2. Answer the knowledge checks without looking back.
3. Attempt `exercises.ipynb` — all eleven tasks.
4. Run the research experiment and record real measurements.
5. Take the quiz; re-read any section you failed.
6. Build the mini-project and write its tests.
7. Implement the ROBO-X challenge and commit it to the project repo.

## Navigation

* Module index: [`03_data_structures/README.md`](../README.md)
* Course path: [`LEARNING_PATH.md`](../../../LEARNING_PATH.md)
