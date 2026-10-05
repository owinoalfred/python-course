# 1.6 — Operators and Expressions

**Module 1: Getting Started with Python**

The small set of symbols Python puts between values, what each one returns, how precedence groups them, and how a packed status word is read and written with bitwise operators.

## Why this topic matters

Operators are the vocabulary of every expression you will write, and two of them - `and` and `or` - do not behave the way their names suggest. On top of that, firmware communicates state as a single packed integer, so the bitwise family is a practical requirement for anyone working with a real robot.

## Learning objectives

1. Predict the return type of every operator family.
2. Explain how precedence groups a mixed expression, and parenthesise deliberately.
3. Use `and` and `or` as value-producing expressions, not just booleans.
4. Apply bitwise masks to set, clear, toggle and test individual flags.
5. Build a defined-bit mask so unknown flags are reported rather than lost.
6. Interpret an expression safely with ast instead of eval.

## Prerequisites

- Topic 1.5 Core Data Types and Type Conversion

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Status Word Toolkit | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Status Word Controller | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Divide without raising on zero | MEDIUM | arithmetic, conditionals, defaults |
| 2 | Test a value against an inclusive range | MEDIUM | comparisons, chaining |
| 3 | Choose a battery verdict | MEDIUM | conditional expression, comparisons |
| 4 | Count vowels in a label | MEDIUM | strings, in, membership |
| 5 | Average readings, ignoring junk | MEDIUM | comprehensions, builtins, validation |
| 6 | Decode a packed status word | HARD | bitwise, dicts, validation |
| 7 | Encode flag names into a word | HARD | bitwise, dicts, sets |
| 8 | Set, clear and test a single flag | HARD | bitwise, tuples, composition |
| 9 | Evaluate a simple arithmetic expression safely | HARD | ast, recursion, validation |
| 10 | Report how an expression was grouped | HARD | ast, precedence, reporting |

## Robotics challenge — ROBO-X Challenge: Status Word Controller

Implement `status_for(robot, thresholds)` that builds a status word from live telemetry, decodes it back into named flags, and reports any undefined bits.

**ROBO-X milestone:** M1

## Research task

How much does operator choice change the runtime of a tight numeric loop compared with the loop overhead itself?

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
