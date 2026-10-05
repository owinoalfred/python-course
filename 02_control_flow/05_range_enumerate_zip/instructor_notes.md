# Instructor notes — 2.5 range, enumerate and zip

**Module 2: Control Flow and Loops**

## Teaching objectives

- Replace hand-maintained counters with enumerate as a habit.
- Make the exclusive stop of range concrete before anything else.
- Turn silent zip truncation into something students can hear.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| range includes its stop value. | The stop is exclusive; range(1, 4) has three values. |
| range builds a list, so a big range is expensive. | It is lazy and knows its own length in constant time. |
| zip pads the shorter input with None. | That is zip_longest; plain zip stops at the shortest input. |
| enumerate is just tidier style. | It removes a whole class of index-desynchronisation bug. |

## Difficult concepts

- Accepting that a lazy zip can only be walked once.
- Deriving a timestamp from the index rather than from a kept-items counter.
- Seeing strict=True as detection rather than as a fix.

## Demonstration suggestions

- Print range(1, 4) and range(0, 10, 3) and have the class call out the stop.
- Build a zip over mismatched inputs, then repeat with strict=True and read the error message.
- Walk a lazy zip twice to show the second result is empty.

## Discussion questions

- Is silent truncation ever the right default?
- When should a malformed reading raise rather than be skipped?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| The last element is missing | The range stop was treated as inclusive | Step the range or use enumerate |
| Log entries shift after a dropped reading | Timestamps came from a counter of kept readings | Take the time from the index before the skip |
| A log is shorter than the batch | zip truncated the two streams | Generate the second stream and use strict=True |

## Recommended pacing

75 minutes of lesson with the live demonstrations, then 2 hours of exercises. Exercise 8 is the pivot of the topic: the timestamp rule is the idea that carries into the data-handling modules later in the course.

## Extension activities

- Ask students to prove the timestamp rule with a failing test before the fix.
- Have them convert a sliced second stream into a generated one and time both.

## Assessment advice

Grade against rubric.md. Exercises 8, 9 and 10 carry the signal: they require an index-derived time base, strict pairing, and a generated stream.

## Differentiation

**If students are struggling:** Provide the solution for exercise 2 and ask students to rewrite it as a stepped range over a different start value, so the stop and step are explicit.

**If students finish early:** Ask for a short note on when a lazy iterator is worth materialising with list().
