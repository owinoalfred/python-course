# 2.2 — for Loops and while Loops

**Module 2: Control Flow and Loops**

Iteration as a protocol: a for loop asks the sequence for the next element, a while loop asks a question - and only one of the two can stop on its own.

## Why this topic matters

Telemetry, routes and retry policies are all loops, and the difference between a loop that stops and a loop that hangs is the difference between a robot that degrades and a robot that is stuck holding a live process. Choosing the right loop is a safety decision, not a style preference.

## Learning objectives

1. Explain why a for loop cannot run away over a finite sequence.
2. Give every while loop a bound, a break, or visible progress.
3. Implement __iter__ and __next__ to make an object loopable.
4. Explain why an exhausted iterator stays exhausted.
5. Choose direct iteration over index iteration and say why.
6. Express a retry policy as a bounded for loop.

## Prerequisites

- Topic 2.1 Conditional Statements
- Topic 1.8 Writing and Running Your First Scripts

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Bounded Sensor Poller | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Bounded Telemetry Poller | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Total the distance of a route | MEDIUM | for, accumulators, floats |
| 2 | Count the positive readings | MEDIUM | for, conditionals, counting |
| 3 | Track the running maximum | MEDIUM | for, comparisons, accumulators |
| 4 | Count down with a bounded while loop | MEDIUM | while, countdown, termination |
| 5 | Find the first reading above a threshold | MEDIUM | for, return, search |
| 6 | Total the length of a path | HARD | for, math.dist, accumulators |
| 7 | Split a sequence into fixed-size chunks | HARD | for, slicing, range |
| 8 | Scan readings until the first drop | HARD | for, state, early exit |
| 9 | Poll a condition with a bounded retry | HARD | for over range, callables, retry |
| 10 | Follow a waypoint route with the simulator | HARD | for, simulator API, aggregation |

## Robotics challenge — ROBO-X Challenge: Bounded Telemetry Poller

Implement `poll_channels(robot, channels, attempts)` that reads each channel with a bounded retry and reports which channels failed.

**ROBO-X milestone:** M2

## Research task

How much faster is direct iteration over a list than the equivalent manual index loop?

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
