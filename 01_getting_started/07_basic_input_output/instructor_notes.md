# Instructor notes — 1.7 Basic Input/Output

**Module 1: Getting Started with Python**

## Teaching objectives

- Reframe I/O as objects that can be replaced.
- Install the stdout/stderr contract as a habit.
- Show that a console program can be fully tested with no terminal present.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| print writes to the screen. | It writes to sys.stdout, which is usually the screen but need not be. |
| input converts what the user types to a number. | It always returns a string, whatever was typed. |
| A blank line ends a read loop. | Only an empty read signals end of input; a blank line is data. |
| Building a report with += is fine. | Repeated concatenation is quadratic; collect and join instead. |

## Difficult concepts

- Understanding that rebinding sys.stdout changes every later print.
- Distinguishing an empty read from an empty line.
- Seeing why stream parameters make a function testable rather than merely tidy.

## Demonstration suggestions

- Redirect stdout to a StringIO, print, and show the terminal stays empty.
- Show a read loop that spins forever on a closed pipe without the empty check.
- Run a script with 1> and 2> to show the two streams separating.

## Discussion questions

- Why do operating systems provide two output streams instead of one?
- When would printing a warning to stdout be the right choice?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| The kernel hangs in a notebook | input() is waiting for a human who is not there | Read from a StringIO instead |
| A JSON file contains warning text | Diagnostics were printed to stdout | Send warnings to sys.stderr |
| A loop never terminates on piped input | No end-of-input check | Break when readline returns the empty string |

## Recommended pacing

90 minutes of lesson with live redirection, then 2 hours on exercises. Spend time on the redirect_stdout demonstration; it reframes testing for the whole course.

## Extension activities

- Ask students to add a --json flag and assert on parsed output in a test.
- Have them measure the quadratic versus linear cost of building a report.

## Assessment advice

Grade against rubric.md. Exercises 7 to 10 carry the signal: they require the student to inject streams and think in terms of the CLI contract.

## Differentiation

**If students are struggling:** ('Provide a helper that runs a function with both streams captured, so students can assert on output from their very first attempt.',)

**If students finish early:** ('Ask for a design note on how the same tool would behave when stdout is a pipe to another process rather than a file.',)
