# Instructor notes — 2.3 Loop Control

**Module 2: Control Flow and Loops**

## Teaching objectives

- Separate the three loop exits clearly in students' minds.
- Make the loop else replace the flag variable as a habit.
- Explain why break is only ever one level deep.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| break leaves all the loops it is inside. | It leaves only the innermost loop; use a helper and return for more. |
| The loop else runs whenever the loop ends. | It runs only when the loop ended without a break or return. |
| continue and break are two spellings of exit. | continue skips to the next iteration; break leaves the loop. |
| A found flag is always simpler than a for/else. | The flag has to be reset; the else cannot drift out of sync. |

## Difficult concepts

- Reading a loop else as a completion handler rather than a fallback.
- Accepting that return also suppresses the else.
- Rewriting a flag-based search without regressing readability.

## Demonstration suggestions

- Run a nested loop with a break and show the outer loop continuing.
- Show a for/else where the break suppresses the else, side by side.
- Introduce a flag that is never reset and show the second batch behaving wrongly.

## Discussion questions

- When is a flag clearer than a loop else?
- Should a fault scanner stop at the first problem or collect them all?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| The search returns the last match, not the first | continue was used where break was meant | Break at the match and return immediately |
| The else runs when it should not | The body returns before the loop completes | Decide explicitly between return and break for the found case |
| A flag stays True across two batches | It was never reset inside the outer loop | Use the loop else or reset it explicitly |

## Recommended pacing

90 minutes of lesson with the nested-loop demonstration, then 2 hours of exercises. Insist on rewriting one flag solution as a for/else so the contrast is felt rather than just described.

## Extension activities

- Ask students to find a break that leaves the wrong loop and fix it.
- Have them convert a for/else back into a flag and explain what is lost.

## Assessment advice

Grade against rubric.md. Exercises 7 to 9 carry the signal: they require correct early exit, a budget boundary, and a stateful grouping pass.

## Differentiation

**If students are struggling:** Provide the first_fault function from exercise 9 with the first two branches written, and ask students to complete the loop else.

**If students finish early:** Ask for a short note on how a flat index loop could replace a nested search, and what it costs in readability.
