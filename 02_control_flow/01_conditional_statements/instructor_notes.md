# Instructor notes — 2.1 Conditional Statements

**Module 2: Control Flow and Loops**

## Teaching objectives

- Replace 'a condition is a bool' with 'a condition is truthiness'.
- Make elif's priority semantics explicit and contrast it with repeated ifs.
- Install the guard chain as the shape for any safety decision.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| An if condition must be a boolean. | Any expression is allowed; the interpreter applies truthiness to it. |
| Zero is truthy because it is a real value. | Every zero is falsy, so a legitimate reading of 0.0 is skipped. |
| Several if statements are equivalent to elif. | They are not: the last match wins rather than the first. |
| == None works for testing absence. | Use `is None`; equality against a singleton is a style smell linters flag. |

## Difficult concepts

- Trusting that a measured value never lands on a threshold.
- Ordering branches by severity and understanding why it is a policy statement.
- Moving a growing elif chain into a decision table.

## Demonstration suggestions

- Print the truthiness of a table of values including 0.0, '0' and [0].
- Run the two independent-if version and the elif version for an overlapping band.
- Build a decision table and add a rule without touching any control flow.

## Discussion questions

- Should a missing sensor reading be treated as 'nominal' or as 'failed'?
- When is a deeply nested if more readable than a flat chain?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| A flat battery is allowed to drive | The check used truthiness and 0.0 was falsy | Compare explicitly, or test `is not None` for presence |
| A reading of 30 is reported as LOW | Two independent if statements; the second overwrote the first | Use elif so only one branch can win |
| The wrong reason is logged | Checks were ordered by convenience rather than by severity | Order the guard chain most severe first |

## Recommended pacing

90 minutes of lesson with live demonstrations, then 2 hours of exercises. Do not rush the truthiness table: it is the single idea this topic exists to install.

## Extension activities

- Ask students to write a truth table for a three-band function and find the bugs.
- Have them convert their elif chain into a decision table and compare the tests.

## Assessment advice

Grade against rubric.md. Exercises 7 and 10 carry the signal: they require the student to encode a policy as ordered data.

## Differentiation

**If students are struggling:** Give students the finished interlock from the walkthrough and ask them to add one new rule, so the severity ordering is visible before they write it.

**If students finish early:** Ask for a short note on how the policy table would be validated against a changing set of safety requirements.
