# 8.7 — ORMs

**Module 8: Databases**

SQLAlchemy core and ORM declarative mapping, Base, Session, and mapped models.

## Why this topic matters

ORMs map database tables directly to Python classes, providing high-level data abstractions.

## Learning objectives

1. Define SQLAlchemy models with declarative base.
2. Manage sessions and query objects.
3. Understand ORM vs raw SQL trade-offs.

## Prerequisites

- Topic 8.6 Transactions

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: ORMs System | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: ORMs Controller | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | ORMs Medium Task 1 | MEDIUM | ORM, SQLAlchemy, Declarative Base |
| 2 | ORMs Medium Task 2 | MEDIUM | ORM, SQLAlchemy, Declarative Base |
| 3 | ORMs Medium Task 3 | MEDIUM | ORM, SQLAlchemy, Declarative Base |
| 4 | ORMs Medium Task 4 | MEDIUM | ORM, SQLAlchemy, Declarative Base |
| 5 | ORMs Medium Task 5 | MEDIUM | ORM, SQLAlchemy, Declarative Base |
| 6 | ORMs Hard Task 1 | HARD | ORM, SQLAlchemy, Declarative Base, Session |
| 7 | ORMs Hard Task 2 | HARD | ORM, SQLAlchemy, Declarative Base, Session |
| 8 | ORMs Hard Task 3 | HARD | ORM, SQLAlchemy, Declarative Base, Session |
| 9 | ORMs Hard Task 4 | HARD | ORM, SQLAlchemy, Declarative Base, Session |
| 10 | ORMs Hard Task 5 | HARD | ORM, SQLAlchemy, Declarative Base, Session |

## Robotics challenge — ROBO-X Challenge: ORMs Controller

Develop a robust controller function using ORMs.

**ROBO-X milestone:** M8

## Research task

How does the performance of ORMs scale with dataset size?

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
