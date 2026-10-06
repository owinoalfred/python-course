# 3.2 — Tuples

**Module 3: Core Data Structures**

Python's record type: an immutable binding of references that unlocks hashable keys, safe unpacking, and the one trap - shallow immutability - that teams discover in production.

## Why this topic matters

Returns of several values, dictionary keys, coordinate grids and mission records are all tuples in real Python systems. The failure students must not carry into industry is trusting 'immutable' data that contains a mutable list - a corrupted audit trail that raises no error at all.

## Learning objectives

1. Construct and unpack tuples, including the one-element comma form.
2. Explain why assignment still aliases immutable objects.
3. Distinguish shallow from deep immutability with a live example.
4. Predict which objects are hashable and use tuples as dict keys.
5. Choose tuple returns over out-parameter mutation for multi-value results.
6. Accumulate into lists and convert once instead of concatenating tuples.

## Prerequisites

- Topic 3.1 Lists

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Mission Record Store | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Immutable Telemetry Envelope | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Normalise a coordinate tuple | MEDIUM | tuple rebuilding, rounding, immutability |
| 2 | Swap two records without a temporary variable | MEDIUM | unpacking, swap, evaluation order |
| 3 | Pack measurement metadata into a validated record | MEDIUM | record construction, validation, type coercion |
| 4 | Unpack a heterogeneous log record safely | MEDIUM | unpacking, star unpacking, sentinel names |
| 5 | Build an index from coordinate tuples | MEDIUM | hashable keys, dict from pairs, duplicate detection |
| 6 | Compare semantic versions as tuples | HARD | parsing, lexicographic comparison, tuple equality |
| 7 | Make a nested structure hashable | HARD | deep freeze, recursion, hashability |
| 8 | Swap-free rotation of field order | HARD | unpacking, cyclic shift, field rotation |
| 9 | Group readings into (min, max, mean) summary tuples | HARD | aggregation, record emission, empty input |
| 10 | Diff two record streams field by field | HARD | zip, field-wise diff, named reporting |

## Robotics challenge — ROBO-X Challenge: Immutable Telemetry Envelope

Implement `pack_batch(readings, mission_id)` returning a nested tuple `((value, timestamp), ...)` plus mission id, validated and frozen, with a `batch_key` suitable for set membership.

**ROBO-X milestone:** M3

## Research task

Does using tuples instead of lists as dictionary keys measurably change lookup time, and how does each compare with stringified keys?

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
