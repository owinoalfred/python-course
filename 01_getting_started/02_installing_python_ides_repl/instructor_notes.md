# Instructor notes — 1.2 Installing Python, IDEs, and the REPL

**Module 1: Getting Started with Python**

## Teaching objectives

- Make the three-ring model of an installation concrete.
- Convert 'which Python am I' from guesswork into a single command.
- Give students a reusable pre-flight check they keep for the whole course.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| There is only one Python on the machine. | System, user, venv and bundled-IDE interpreters routinely coexist. |
| Activating a venv changes the interpreter binary. | It usually reuses the base binary and overrides sys.prefix instead. |
| 'No module named' means the package is not installed. | It can equally mean it is installed in a different environment. |
| A guarded import is the cleanest optional-dependency test. | It runs the module's code; find_spec does not. |

## Difficult concepts

- Reading PATH order and understanding why the first match wins.
- Accepting that sys.prefix and sys.executable can disagree.
- Seeing sys.path as a search order rather than a set of folders.

## Demonstration suggestions

- Run the same import under the system interpreter and inside a venv to show the divergence.
- Create random.py in the working directory and show it shadowing the stdlib.
- Print sys.path before and after inserting an entry to show the search order changing.

## Discussion questions

- Why does an IDE let you choose an interpreter, and what goes wrong when that choice is wrong?
- Should a pre-flight check ever raise, or only report? Where is the line?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| ModuleNotFoundError after a successful install | pip and python point at different environments | Always install with `python -m pip` and verify with `python -m pip list` |
| SyntaxError on code they know is valid | The editor is running an old interpreter | Check sys.executable from inside the failing process |
| Tests pass locally, fail on the build machine | Different interpreter version or missing dependency on CI | Run the pre-flight check as the first CI step |

## Recommended pacing

90 minutes of lesson, with a live venv creation, then 2 hours of exercises and the mini-project. Insist that every student runs the three diagnostic commands on their own machine before moving on.

## Extension activities

- Have students diff sys.path between a terminal and a notebook kernel.
- Ask what changes when a package is installed with --user.

## Assessment advice

Grade against rubric.md. Exercises 8 to 10 carry the real signal: they require composing checks into one machine-readable decision.

## Differentiation

**If students are struggling:** Provide the finished preflight() function from the engineering example and ask students to extend it rather than write it from scratch.

**If students finish early:** Ask students to write the CI job that consumes the readiness exit code.
