# 8.6 — Transactions

**Module 8: Databases**

ACID properties, commit, rollback, and transaction context managers.

## Why this topic matters

Transactions guarantee atomic state transitions, preventing partial updates during failures.

## Learning objectives

1. Understand ACID properties.
2. Commit and rollback database transactions.
3. Use connection as context manager for auto-commit/rollback.

## Prerequisites

- Topic 8.5 Parameterized Queries

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Transactions System | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Transactions Controller | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Transactions Medium Task 1 | MEDIUM | Transactions, ACID, Commit |
| 2 | Transactions Medium Task 2 | MEDIUM | Transactions, ACID, Commit |
| 3 | Transactions Medium Task 3 | MEDIUM | Transactions, ACID, Commit |
| 4 | Transactions Medium Task 4 | MEDIUM | Transactions, ACID, Commit |
| 5 | Transactions Medium Task 5 | MEDIUM | Transactions, ACID, Commit |
| 6 | Transactions Hard Task 1 | HARD | Transactions, ACID, Commit, Rollback |
| 7 | Transactions Hard Task 2 | HARD | Transactions, ACID, Commit, Rollback |
| 8 | Transactions Hard Task 3 | HARD | Transactions, ACID, Commit, Rollback |
| 9 | Transactions Hard Task 4 | HARD | Transactions, ACID, Commit, Rollback |
| 10 | Transactions Hard Task 5 | HARD | Transactions, ACID, Commit, Rollback |

## Robotics challenge — ROBO-X Challenge: Transactions Controller

Develop a robust controller function using Transactions.

**ROBO-X milestone:** M8

## Research task

How does the performance of Transactions scale with dataset size?

## Recommended workflow

1. Read `lesson.ipynb` end to end, running every code cell.
2. Answer the knowledge checks without looking back.
3. Attempt `exercises.ipynb` — all eleven tasks.
4. Run the research experiment and record real measurements.
5. Take the quiz; re-read any section you failed.
6. Build the mini-project and write its tests.
7. Implement the ROBO-X challenge and commit it to the project repo.

## Navigation

* Module index: [`08_databases/README.md`](../README.md)
* Course path: [`LEARNING_PATH.md`](../../../LEARNING_PATH.md)
