# 3.3 — Sets

**Module 3: Core Data Structures**

Unordered collections of unique hashable objects: O(1) membership, set algebra as validation logic, and the traps of orderlessness, unhashable elements and mutation during iteration.

## Why this topic matters

Duplicate detection, fault state, coverage reports and configuration validation all reduce to set operations, and the difference between a quadratic scan and a hash lookup is the difference between an audit that finishes and one that does not. Orderlessness is a real trade, not a defect - provided output is sorted at the boundary.

## Learning objectives

1. Construct sets four ways, including set() for the empty set.
2. State the cost of membership on a set versus a list.
3. Apply union, intersection, difference and symmetric difference with correct direction.
4. Express validation with subset, equality and disjoint relations.
5. Deduplicate with a set while preserving order via the seen-set idiom.
6. Explain why set elements must be hashable and why iteration order must not be relied upon.

## Prerequisites

- Topic 3.2 Tuples

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Mission Anomaly Auditor | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Fault Supervisor Core | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Deduplicate sensor tags with a set | MEDIUM | set construction, deduplication, sorted output |
| 2 | Check whether all required keys were supplied | MEDIUM | subset, difference, validation |
| 3 | Find codes present in both subsystems | MEDIUM | intersection, set conversion, sorted |
| 4 | Remove every occurrence of blacklisted values | MEDIUM | difference, list comprehension with membership, order preservation |
| 5 | Detect duplicate frames in O(n) | MEDIUM | seen set, linear scan, order preservation |
| 6 | Compute a coverage report with set algebra | HARD | union, difference, coverage ratio |
| 7 | Group anagram signatures into sets | HARD | set signatures, default grouping, sorted keys |
| 8 | Find the first value present in exactly one of two streams | HARD | symmetric difference, order recovery, index mapping |
| 9 | Maintain a rolling window of distinct values | HARD | windowing, set per slice, counting distinct |
| 10 | Implement set algebra without the operators | HARD | set semantics, membership loops, complexity reasoning |

## Robotics challenge — ROBO-X Challenge: Fault Supervisor Core

Implement `FaultSupervisor` with O(1) raise/clear, an O(1) critical query, and an idempotent acknowledge that never duplicates state.

**ROBO-X milestone:** M3

## Research task

At what input size does converting a list to a set pay off for repeated membership testing, and does the crossover match the O(n^2) versus O(n) model?

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
