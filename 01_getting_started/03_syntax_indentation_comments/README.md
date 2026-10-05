# 1.3 — Python Syntax, Indentation, Comments, and Code Structure

**Module 1: Getting Started with Python**

Why the left margin is part of the grammar: indentation as structure, the difference between comments and docstrings, and how to parse code without running it.

## Why this topic matters

In every other language you learned, whitespace was decoration. In Python it is syntax, which means a formatting mistake is a parse error and a readable file is a correct file. Robotics teams also rely on structured, indented diagnostics, so this topic is where layout becomes data.

## Learning objectives

1. Explain how INDENT and DEDENT tokens produce block structure.
2. Apply PEP 8 indentation consistently and repair a mixed-indentation file.
3. Distinguish comments from docstrings and use each correctly.
4. Use implicit line joining to wrap long expressions readably.
5. Parse an indented log into nested data with an explicit stack.
6. Read docstrings from source with ast without importing the module.

## Prerequisites

- Topic 1.1 Introduction to Python
- Topic 1.2 Installing Python, IDEs, and the REPL

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Structured Diagnostics Reader | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Bring-Up Log Reader | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Strip a trailing comment from a line | MEDIUM | strings, comments, parsing |
| 2 | Measure indentation width | MEDIUM | strings, indentation, counting |
| 3 | Normalise a block to a fixed indent width | MEDIUM | indentation, strings, mapping |
| 4 | Build a multi-line banner | MEDIUM | strings, f-strings, implicit joining |
| 5 | Count code, comment and blank lines | MEDIUM | tokenize, strings, classification |
| 6 | Report indentation problems | HARD | indentation, validation, strings |
| 7 | Parse an indented log into a tree | HARD | stacks, indentation, dicts |
| 8 | Extract docstrings without importing | HARD | ast, docstrings, dicts |
| 9 | Split semicolon-packed statements safely | HARD | parsing, strings, tokenize |
| 10 | Produce a module outline | HARD | ast, tuples, reporting |

## Robotics challenge — ROBO-X Challenge: Bring-Up Log Reader

Implement `read_diagnostics(robot)` that renders the simulator's state as an indented log, parses it straight back, and returns a validated summary.

**ROBO-X milestone:** M1

## Research task

How much does comment density correlate with defect rate in a small body of Python source?

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
