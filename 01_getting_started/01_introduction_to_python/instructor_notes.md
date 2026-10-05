# Instructor notes — 1.1 Introduction to Python

**Module 1: Getting Started with Python**

## Teaching objectives

- Establish the interpreter model: source, bytecode, evaluation loop.
- Make name binding concrete so later modules can rely on it.
- Install the habit of inspecting types before trusting a value.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| Python is interpreted, therefore simply slow. | CPython compiles to bytecode first; the cost profile is not that of a pure interpreter. |
| A variable has a type that is declared once. | Types belong to objects and are checked when the operation runs. |
| Naming a variable `list` is only a style issue. | It rebinds the built-in and causes real TypeErrors later in the module. |
| A function that prints is equivalent to one that returns. | Returning keeps the logic testable; printing hides it inside the function. |

## Difficult concepts

- Separating syntax errors, raised before execution, from runtime errors.
- Seeing a name as a label rather than a fixed container.
- Understanding why the main guard exists at all.

## Demonstration suggestions

- Run `dis.dis()` live on a one-line function and read the instructions aloud.
- Assign to `list` in the REPL, then call `list(...)` and read the TypeError.
- Show `sys.executable` differing from the interpreter the student expected.

## Discussion questions

- Which parts of a robot controller would you never write in Python, and why?
- If types are checked only at runtime, what could you add to catch problems earlier?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| TypeError where a number was expected | Input arrived from a sensor or file as text and was never converted | Inspect with type() and convert explicitly at the boundary |
| IndentationError after editing in another editor | That editor inserted tabs while the file used spaces | Convert the file to spaces on save and enable trim-trailing-whitespace |
| Nothing happens when the file is imported | Side effects sit at module level instead of behind the main guard | Wrap side effects in main() and guard the call |

## Recommended pacing

90 minutes of lesson with live demonstrations, then 2 hours of exercises and the mini-project. Do not rush the REPL demonstration: beginners must see an error happen before they can read one.

## Extension activities

- Disassemble a loop and count the bytecodes per iteration.
- Compare `sys.implementation.cache_tag` across two Python versions.

## Assessment advice

Grade against rubric.md. Expect weak reasoning on exercises 6 to 10; the parsing and validation tasks are the real signal of learning.

## Differentiation

**If students are struggling:** Provide the first exercise fully worked, and pair students so the stronger partner explains the type conversion out loud.

**If students finish early:** Ask for a one-paragraph design note on where Python should stop and a compiled language should begin inside a control loop.
