# 2.3 — Loop Control

**Module 2: Control Flow and Loops**

break, continue and the under-used loop else: three ways a loop says how it finished, and why that is usually more expressive than a flag variable.

## Why this topic matters

A fault scanner that keeps reading after it has found the fault spends the control cycle it needed for a stop command, and a search that forgets to break reports the wrong answer with no error at all. Loop control is where a small mistake becomes a silent one.

## Learning objectives

1. Distinguish break, continue and return by what each one leaves.
2. Explain that break affects only the innermost loop.
3. Use the loop else to express a not-found result without a flag.
4. Recognise that return also suppresses the else clause.
5. Rewrite a flag-based search as an early-exit loop.
6. Use early exit deliberately as a performance and safety measure.

## Prerequisites

- Topic 2.2 for Loops and while Loops

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Telemetry Fault Scanner | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Mission Fault Scanner | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Find the first negative reading | MEDIUM | break, for, search |
| 2 | Sum only the usable readings | MEDIUM | continue, for, filtering |
| 3 | Find the first multiple of n | MEDIUM | for/else, modulo, search |
| 4 | Stop scanning at a sentinel | MEDIUM | break, sentinel, search |
| 5 | Detect duplicates with for/else | MEDIUM | for/else, membership, sets |
| 6 | Locate a target in a grid | HARD | nested loops, return, enumeration |
| 7 | Take readings until the budget is spent | HARD | break, accumulator, budget |
| 8 | Group consecutive equal readings | HARD | state, loops, grouping |
| 9 | Scan a telemetry batch for the first fault | HARD | continue, break, validation |
| 10 | Drive until the battery is too low | HARD | break, simulator API, safety |

## Robotics challenge — ROBO-X Challenge: Mission Fault Scanner

Implement `scan_batch(robot, batch, limits)` that walks the batch with the right loop control and returns a verdict the mission supervisor can gate on.

**ROBO-X milestone:** M2

## Research task

How much time does early exit save when a search usually finds its match early?

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
