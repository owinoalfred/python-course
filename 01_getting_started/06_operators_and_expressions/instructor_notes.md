# Instructor notes — 1.6 Operators and Expressions

**Module 1: Getting Started with Python**

## Teaching objectives

- Make operator return types explicit, especially for and/or.
- Install the habit of parenthesising mixed-precedence expressions.
- Give bitwise flags a concrete robotics home in the firmware status word.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| `and` and `or` produce True or False. | They return one of their operands, which is why `or` works as a default. |
| Bitwise operators bind more loosely than comparison, as in C. | In Python they bind more tightly, which is the reverse of C. |
| `/` rounds down like `//`. | True division always returns a float and does not truncate. |
| `value & ~value` is a useful mask. | It is always zero and is never what the author meant. |

## Difficult concepts

- Reasoning about which grouping the parser actually chose.
- Understanding ~ as an infinite-bit complement and why the AND fixes it.
- Accepting that operators are dunder methods, not built-in syntax.

## Demonstration suggestions

- Run precedence_report on '1 + 2 * 3' and show the grouping from the tree.
- Build a status word, clear one flag, and show the other bits are untouched.
- Toggle a flag twice to show the operation is its own inverse.

## Discussion questions

- Why does firmware use packed words instead of a struct of booleans?
- When would a dict of flags be a better representation than a bitmask?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| A safety condition fires on the wrong values | The comparison was written backwards | Read the condition aloud and check the direction |
| Clearing a flag also cleared others | The code used `& ~word` or XOR on several bits at once | Clear with `& ~mask` for exactly one named mask |
| A result differs from another language they know | Assuming C precedence or integer division semantics | Check the Python precedence table and remember `/` always returns a float |

## Recommended pacing

90 minutes of lesson with live bit arithmetic, then 2 hours on exercises. The ast-based exercises are the stretch; accept a table-dispatch solution for a student who is stuck on the recursion.

## Extension activities

- Ask students to extend the flag table and prove the round trip still holds.
- Introduce operator overloading by implementing __lt__ on a wrapper class.

## Assessment advice

Grade against rubric.md. Exercises 6 to 10 carry the signal; a student who can explain the defined mask has understood the real engineering problem.

## Differentiation

**If students are struggling:** Provide a printed bit-position table for 0 to 15 and have students decode a few by hand before coding anything.

**If students finish early:** ('Ask for a design note on how the flag table should grow as firmware adds bits, without breaking older decoders.',)
