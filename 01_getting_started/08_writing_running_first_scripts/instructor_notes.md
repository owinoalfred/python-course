# Instructor notes — 1.8 Writing and Running Your First Scripts

**Module 1: Getting Started with Python**

## Teaching objectives

- Reframe every file as a module with two personalities and one switch.
- Make the process contract - code, stdout, stderr - explicit and testable.
- Show that import safety is a safety property, not a style preference.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| argv[0] is the first argument. | It is the path used to invoke the program; arguments start at index 1. |
| Wrapping code in main() prevents it running on import. | It does not; only the __name__ guard prevents that. |
| sys.exit is a tidy way to stop a function early. | It raises an exception that unwinds the stack and skips cleanup. |
| A script that prints correctly must be correct. | Printing without an exit status gives a caller nothing to branch on. |

## Difficult concepts

- Accepting that a caller can only see three channels.
- Understanding that a return value and a printed message serve different readers.
- Writing a test that reproduces an import rather than a script run.

## Demonstration suggestions

- Import a module with an unguarded print and watch it run.
- Run a script that exits 3 and observe $? in a shell.
- Run the same tool as a subprocess and read returncode, stdout and stderr.

## Discussion questions

- What should a tool do when it has nothing useful to report - print nothing, or print an empty result?
- Why is a distinct exit code for usage errors worth the extra branch?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| A test starts the robot unexpectedly | Top-level side effects with no main guard | Wrap side effects and guard them |
| A supervisor cannot tell success from failure | The script prints but always exits 0 | Return a status and exit with it once |
| An index error only with zero arguments | argv[0] was treated as an argument | Slice from index 1, or pass sys.argv[1:] in |

## Recommended pacing

90 minutes of lesson, then 2 hours on exercises. The subprocess exercise is the bridge to Module 9; make sure everyone runs the file from a real shell at least once.

## Extension activities

- Ask students to write a test that fails if the guard is removed.
- Have them run the tool with a broken PATH to see which error appears first.

## Assessment advice

Grade against rubric.md. Exercises 7 to 10 carry the signal: they require the student to own the full process contract.

## Differentiation

**If students are struggling:** ('Provide a finished main() skeleton and ask students to fill in the run() function, so the process plumbing is never the blocker.',)

**If students finish early:** ('Ask for a design note on how the same tool would report to a systemd unit versus a human at a terminal.',)
