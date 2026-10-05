# 1.8 — Writing and Running Your First Scripts

**Module 1: Getting Started with Python**

Turning a module into a program: the main guard, sys.argv, exit codes and the three-channel contract between a script and whoever started it.

## Why this topic matters

A fleet supervisor launches robot services as child processes and decides what happens next from the exit code alone. Getting that contract right is the difference between a tool that composes with a system and one that is run by hand and hoped over.

## Learning objectives

1. Explain how __name__ distinguishes a module from a program.
2. Guard side effects so importing a script cannot start a robot.
3. Pass sys.argv[1:] into logic instead of indexing it inline.
4. Return an exit status and call sys.exit exactly once.
5. Keep results on stdout, diagnostics on stderr, and decisions in the exit code.
6. Test a tool without a shell by injecting argv and the streams.

## Prerequisites

- Topic 1.7 Basic Input/Output

## Files in this topic

| File | Purpose | When to open it |
| --- | --- | --- |
| [`lesson.ipynb`](lesson.ipynb) | The 25-section lesson with runnable examples | First — every session starts here |
| [`exercises.ipynb`](exercises.ipynb) | 5 MEDIUM + 5 HARD + 1 robotics challenge | After the lesson; graded |
| [`solution.ipynb`](solution.ipynb) | Reference implementations with tests and complexity notes | Only after you have attempted the exercises |
| [`research.ipynb`](research.ipynb) | A measurement-driven investigation | End of topic |
| [`quiz.ipynb`](quiz.ipynb) | 10 questions with an answer key | Self-check before moving on |
| [`mini_project.ipynb`](mini_project.ipynb) | Mini-Project: Fleet Control Tool | Deliverable |
| [`robotics_challenge.ipynb`](robotics_challenge.ipynb) | ROBO-X Challenge: Fleet Bring-Up Tool | ROBO-X milestone |
| [`instructor_notes.md`](instructor_notes.md) | Teaching notes and common misconceptions | Lecturers only |
| [`rubric.md`](rubric.md) | How this topic is graded | Before submitting work |

## Exercise index

| # | Title | Difficulty | Concepts |
| --- | --- | --- | --- |
| 1 | Separate the program path from the arguments | MEDIUM | sys.argv, slicing, lists |
| 2 | Report the program name | MEDIUM | pathlib, strings |
| 3 | Detect a boolean flag | MEDIUM | membership, lists, validation |
| 4 | Map a status name to an exit code | MEDIUM | dicts, error handling |
| 5 | Build a usage line | MEDIUM | strings, join, f-strings |
| 6 | Split an inline option token | HARD | strings, partition, validation |
| 7 | Parse flags and options with an index | HARD | loops, indexing, validation |
| 8 | Run a child process and observe its result | HARD | subprocess, sys, streams |
| 9 | Dispatch a command and return an exit status | HARD | dispatch, streams, exit codes |
| 10 | Prove a module is import-safe | HARD | import, __name__, subprocess |

## Robotics challenge — ROBO-X Challenge: Fleet Bring-Up Tool

Implement `bringup(argv, out, errors)` returning the exit status a shell would observe, with every decision expressed on the correct channel.

**ROBO-X milestone:** M1

## Research task

How much does the main guard reduce the risk of accidental side effects when a module is imported?

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
