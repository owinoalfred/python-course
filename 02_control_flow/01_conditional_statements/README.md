# 2.1 — Conditional Statements

**Module 2: Control Flow and Loops**

How a condition is evaluated, why truthiness is the source of most conditional bugs, and how to structure a safety-critical decision so it can be tested and reasoned about.

## Why this topic matters

Every control decision a robot makes is a conditional: whether to drive, whether to arm, whether a reading is trustworthy. A condition that is quietly wrong produces no error - it simply takes the wrong branch, which is far more dangerous than a crash.

## Learning objectives

1. Explain that an if header accepts any expression and applies truthiness.
2. List the falsy values and predict the outcome for each.
3. Use elif to express mutually exclusive bands with a defined priority.
4. Distinguish a missing reading from a reading of zero.
5. Structure a multi-check decision as a severity-ordered guard chain.
6. Encode a growing policy as a decision table rather than control flow.

## Prerequisites

- Topic 1.5 Core Data Types and Type Conversion
- Topic 1.6 Operators and Expressions

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Safety Policy Evaluator | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Field Robot Drive Interlock | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Classify a value by its kind and emptiness | MEDIUM | truthiness, is None, isinstance |
| 2 | Assign a battery band | MEDIUM | elif, comparisons, thresholds |
| 3 | Test strictly for a positive number | MEDIUM | isinstance, bool, comparison |
| 4 | Supply the first usable option | MEDIUM | or, falsy, defaults |
| 5 | Report the sign of a number | MEDIUM | if/elif/else, comparison |
| 6 | Test a point against a geofence | HARD | and, chained comparison, tuples |
| 7 | Build a safety interlock | HARD | guard clauses, elif, dicts |
| 8 | Grade a score against bands | HARD | dictionaries, iteration, validation |
| 9 | Report every failed check at once | HARD | comprehensions, filtering, aggregation |
| 10 | Validate a state-machine transition | HARD | dicts, sets, validation |

## Robotics challenge — ROBO-X Challenge: Field Robot Drive Interlock

Implement `may_drive(state)` that returns a decision dict naming the first failing check in severity order, using the simulator's live readings.

**ROBO-X milestone:** M2

## Research task

How often does a threshold comparison on a simulated sensor reading land exactly on the boundary value?

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
