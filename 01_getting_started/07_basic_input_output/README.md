# 1.7 — Basic Input/Output

**Module 1: Getting Started with Python**

I/O in Python is an object you can replace. This topic covers print and the format specification, the stdout/stderr contract, and the redirection technique that makes console programs testable without a terminal.

## Why this topic matters

Every robotics service begins as a console program, and a deployment script usually captures its output. Getting the two streams right is what makes `service > state.json` produce something a parser can read, and passing the stream in is what makes the program testable at all.

## Learning objectives

1. Explain that print writes to sys.stdout and input reads from sys.stdin.
2. Redirect a stream to capture output in a test.
3. Format aligned columns with f-string format specifications.
4. Apply the stdout/stderr contract to a reporting function.
5. Detect end of input correctly in a read loop.
6. Build a report without quadratic string concatenation.

## Prerequisites

- Topic 1.6 Operators and Expressions

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Testable Console Tool | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Dispatch Console | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Render an aligned table | MEDIUM | f-strings, format specs, loops |
| 2 | Parse a percentage from text | MEDIUM | strings, conversion, error handling |
| 3 | Echo lines from a stream | MEDIUM | streams, loops, strings |
| 4 | Centre a title banner | MEDIUM | strings, format specs |
| 5 | Normalise a yes/no answer | MEDIUM | dicts, strings, validation |
| 6 | Process commands from a stream | HARD | streams, loops, dicts |
| 7 | Capture what a function printed | HARD | contextlib, io, testing |
| 8 | Emit a fleet report on two streams | HARD | sys.stderr, f-strings, iteration |
| 9 | Parse simple command-line arguments | HARD | strings, sys.argv, validation |
| 10 | Build a testable command-line entry point | HARD | sys.argv, streams, composition |

## Robotics challenge — ROBO-X Challenge: Dispatch Console

Implement `dispatch(stream, out, errors)` that reads commands from an injected stream, applies them to the simulator, and reports each decision on the correct stream.

**ROBO-X milestone:** M1

## Research task

How much output volume can a console program emit before buffering becomes noticeable to a user?

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
