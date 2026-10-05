# Instructor notes — 2.2 for Loops and while Loops

**Module 2: Control Flow and Loops**

## Teaching objectives

- Contrast sequence-driven and condition-driven iteration concretely.
- Make the iterator protocol explicit rather than treating for as magic.
- Install bounded iteration as a habit for every retry.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| A for loop is a while loop with a built-in counter. | It is driven by the sequence asking for elements, not by a counter. |
| An iterator can be used as many times as you like. | It is single-use; a second pass yields nothing. |
| while True is fine as long as there is a break somewhere. | A break that depends on external state is exactly what fails silently. |
| Iterating by index is more efficient. | Direct iteration avoids a bounds check and an attribute lookup per pass. |

## Difficult concepts

- Seeing the exhaustion model rather than a magic stop condition.
- Accepting that for and while have fundamentally different termination logic.
- Writing a custom iterator and reasoning about when it is drained.

## Demonstration suggestions

- Sum the same list twice, then sum an iterator of it twice, and compare.
- Run a while loop whose body forgets to change the condition, and interrupt it.
- Build a tiny iterator and show that list() consumes it permanently.

## Discussion questions

- What should a supervisor see when a retry loop exhausts its budget?
- When is a while loop genuinely better than a for loop?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| The program hangs with no output | A while loop whose body never changes the condition | Add the increment, or use a bounded for loop |
| The second pass returns nothing | An iterator was reused after exhaustion | Materialise the list, or call iter() again on the source |
| An off-by-one drops the last waypoint | The loop skipped the final element with a manual index bound | Iterate the sequence, or slice correctly |

## Recommended pacing

90 minutes of lesson with the iterator demonstration, then 2 hours of exercises. Give real time to writing a custom iterator; it is the first time students define a protocol rather than use one.

## Extension activities

- Ask students to implement a reverse iterator and compare it with reversed().
- Have them measure the index loop against direct iteration and explain the gap.

## Assessment advice

Grade against rubric.md. Exercises 8 to 10 carry the signal: they require bounded early exit, a bounded retry and a real API call from a loop.

## Differentiation

**If students are struggling:** Provide the Countdown class from the lesson and ask students to change the stop condition, so they see exhaustion rather than a magic number.

**If students finish early:** ('Ask for a design note on how a telemetry consumer should handle an infinite stream without buffering it all.',)
