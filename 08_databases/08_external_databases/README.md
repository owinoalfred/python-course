# 8.8 — External Databases

**Module 8: Databases**

Connecting to external RDBMS (PostgreSQL, MySQL), psycopg2, mysql-connector, and production deployment patterns.

## Why this topic matters

Production fleet deployments connect to external scaled databases like PostgreSQL or MySQL.

## Learning objectives

1. Understand PostgreSQL and MySQL connectors.
2. Configure connection strings and connection pools.
3. Deploy production database configurations.

## Prerequisites

- Topic 8.7 ORMs

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: External Databases System | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: External Databases Controller | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | External Databases Medium Exercise 1 | MEDIUM | PostgreSQL, MySQL, psycopg2 |
| 2 | External Databases Medium Exercise 2 | MEDIUM | PostgreSQL, MySQL, psycopg2 |
| 3 | External Databases Medium Exercise 3 | MEDIUM | PostgreSQL, MySQL, psycopg2 |
| 4 | External Databases Medium Exercise 4 | MEDIUM | PostgreSQL, MySQL, psycopg2 |
| 5 | External Databases Medium Exercise 5 | MEDIUM | PostgreSQL, MySQL, psycopg2 |
| 6 | External Databases Hard Exercise 1 | HARD | PostgreSQL, MySQL, psycopg2, Connection Pooling |
| 7 | External Databases Hard Exercise 2 | HARD | PostgreSQL, MySQL, psycopg2, Connection Pooling |
| 8 | External Databases Hard Exercise 3 | HARD | PostgreSQL, MySQL, psycopg2, Connection Pooling |
| 9 | External Databases Hard Exercise 4 | HARD | PostgreSQL, MySQL, psycopg2, Connection Pooling |
| 10 | External Databases Hard Exercise 5 | HARD | PostgreSQL, MySQL, psycopg2, Connection Pooling |

## Robotics challenge — ROBO-X Challenge: External Databases Controller

Develop a robust controller function using External Databases.

**ROBO-X milestone:** M8

## Research task

How does the performance of External Databases scale with dataset size?

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
