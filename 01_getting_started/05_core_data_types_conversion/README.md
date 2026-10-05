# 1.5 — Core Data Types and Type Conversion

**Module 1: Getting Started with Python**

Everything that enters a robot arrives as text. This topic covers the core built-in types, the traps of truthiness and floating point, and the conversion ladder that makes external data safe to use.

## Why this topic matters

Type conversion is the seam where a robot meets the outside world: serial lines, HTTP parameters, configuration files and operator input all produce text. Get this boundary right and the rest of a system can trust its inputs; get it wrong and a single corrupt field silently becomes a wrong motor command.

## Learning objectives

1. Name the core built-in types and say which are mutable.
2. Convert external text safely with a conversion ladder.
3. Explain why bool is a subclass of int and what it breaks.
4. Avoid truthiness bugs on numeric values.
5. Compare floats with a tolerance and know when Decimal is worth it.
6. Parse a telemetry frame without losing the valid channels.

## Prerequisites

- Topic 1.4 Variables, Naming Conventions, and Dynamic Typing

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Telemetry Frame Validator | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Telemetry Frame Gate | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Name the type of a value | MEDIUM | type(), builtins |
| 2 | Convert external text to a float safely | MEDIUM | float(), exceptions, defaults |
| 3 | Clamp a value into a range | MEDIUM | comparisons, conditionals, types |
| 4 | Describe a value in words | MEDIUM | isinstance, strings, dispatch |
| 5 | Validate a sensor reading strictly | MEDIUM | isinstance, bool, validation |
| 6 | Parse a telemetry line without losing good channels | HARD | strings, exceptions, error reporting |
| 7 | Normalise units to metres | HARD | dicts, arithmetic, validation |
| 8 | Summarise the types in a batch | HARD | collections.Counter, dicts, type() |
| 9 | Compare floats with a tolerance | HARD | floats, abs, math.isclose |
| 10 | Coerce a value through an ordered list of types | HARD | try/except, callables, error reporting |

## Robotics challenge — ROBO-X Challenge: Telemetry Frame Gate

Implement `validate_frame(text)` that parses a raw frame, validates every channel against its physical range, and returns a readiness decision naming each problem found.

**ROBO-X milestone:** M1

## Research task

How often do floating-point comparisons of the form a == b fail for values that should be equal?

## Recommended workflow

1. Read `lesson.ipynb` end to end, running every code cell.
2. Answer the knowledge checks without looking back.
3. Attempt `exercises.ipynb` — all eleven tasks.
4. Run the research experiment and record real measurements.
5. Take the quiz; re-read any section you failed.
6. Build the mini-project and write its tests.
7. Implement the ROBO-X challenge and commit it to the project repo.

## Navigation

* Module index: [`01_getting_started/README.md`](../README.md)
* Course path: [`LEARNING_PATH.md`](../../../LEARNING_PATH.md)
