# 3.4 — Dictionaries

**Module 3: Core Data Structures**

Python's hash map: unique hashable keys to values in amortised O(1), insertion-ordered iteration, and the three silent failures - get() masking absence, shallow copies sharing state, mutation during iteration.

## Why this topic matters

Config, counters, indices, JSON payloads and parameter servers are all dicts, and the bugs are silent ones: a get() typo produces plausible garbage, a shallow copy corrupts live settings through a shared inner object, and a half-applied update is visible to every reader. The dict is where reference semantics meets production data.

## Learning objectives

1. Choose [] versus .get based on whether absence is an error.
2. Count, group and index with dict idioms in linear time.
3. Explain why keys must be hashable and how lookup stays O(1).
4. Diagnose and repair shallow-copy aliasing in nested records.
5. Iterate safely by snapshotting or rebuilding instead of mutating.
6. Publish updated mappings atomically by building then rebinding.

## Prerequisites

- Topic 3.3 Sets

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Telemetry Schema Registry | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Parameter Server with Atomic Updates | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Fetch required and optional config keys correctly | MEDIUM | KeyError, get defaults, contract design |
| 2 | Count frequencies with a dict | MEDIUM | counting idiom, get, max with key |
| 3 | Merge parameter sets with override semantics | MEDIUM | merge operator, update, immutability of inputs |
| 4 | Group events into a dict of lists | MEDIUM | grouping, setdefault, append |
| 5 | Invert a mapping with an explicit collision policy | MEDIUM | dict comprehension, collision policy, reverse index |
| 6 | Deep-copy a nested record without sharing state | HARD | shallow vs deep copy, recursion, isolation |
| 7 | Build an O(1) reverse lookup with collision handling | HARD | reverse index, precomputation, collision lists |
| 8 | Detect and repair aliasing in a settings tree | HARD | identity testing, alias detection, repair |
| 9 | Implement a typed settings table with validation | HARD | schema-driven validation, type checks, error accumulation |
| 10 | Simulate a parameter-server update cycle | HARD | snapshot isolation, staged updates, nested merge |

## Robotics challenge — ROBO-X Challenge: Parameter Server with Atomic Updates

Implement `ParameterServer` supporting snapshot reads, staged updates validated in full before publication, and deletion via a None sentinel - publishing by rebinding, never by in-place edits.

**ROBO-X milestone:** M3

## Research task

How much faster is a dict lookup than a linear scan over items for membership, and does the gap follow the O(1)-versus-O(n) model as n grows?

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
