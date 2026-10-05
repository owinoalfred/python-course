# Instructor notes — 1.4 Variables, Naming Conventions, and Dynamic Typing

**Module 1: Getting Started with Python**

## Teaching objectives

- Replace the 'typed box' mental model with 'label bound to an object'.
- Make aliasing and shared mutation a demonstrated, not described, hazard.
- Install PEP 8 naming as habit from the first week.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| Assignment copies the value into the variable. | Assignment binds a name; two names can share one object. |
| A variable has one fixed type for its whole life. | Types belong to objects; rebinding can change the type of a name. |
| Function arguments are passed by value. | Objects are passed by reference, which is why mutation escapes. |
| A leading underscore makes a name private. | It is a convention, not enforcement; the attribute stays accessible. |

## Difficult concepts

- Understanding that `is` is about object identity, not equality.
- Accepting that shallow copying leaves nested state shared.
- Reading a namespace as an ordinary dictionary.

## Demonstration suggestions

- Alias a list, append through one name, and print both.
- Show id() and `is` for a literal, a computed value and an aliased name.
- Bind a module-level `list = []` and call list() to produce the TypeError live.

## Discussion questions

- Where should a telemetry pipeline copy, and what does that cost?
- If Python had declared types, which of today's bugs would have been caught?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| A function mutates the caller's list unexpectedly | The argument was modified in place | Copy at the boundary or return a new value |
| TypeError far from the assignment that caused it | A built-in name was shadowed in module scope | Search for `name =` assignments that reuse built-ins |
| Config defaults change between test runs | A module-level dict was mutated instead of copied | Copy with dict(DEFAULTS) inside the function |

## Recommended pacing

90 minutes of lesson with live demonstrations, then 2 hours on exercises. Spend real time on the aliasing demonstration; it is the concept that makes Modules 3 and 4 make sense.

## Extension activities

- Ask students to find every mutation in a small module and justify each one.
- Introduce dataclasses as the disciplined alternative to loose attribute assignment.

## Assessment advice

Grade against rubric.md. Exercises 9 and 10 carry the signal: they combine copying, casting, validation and ordering.

## Differentiation

**If students are struggling:** ('Give students sticky notes and a physical object so the label model is tangible before they write code.',)

**If students finish early:** ("Ask for a short note on which of today's aliases would be caught by mypy and which would not.",)
