# Instructor notes — 2.4 Nested Loops and Common Patterns

**Module 2: Control Flow and Loops**

## Teaching objectives

- Make cost multiplication concrete before students optimise anything.
- Kill the hard-coded inner bound as a habit, not a warning.
- Introduce the closed form and the sliding window as replacements.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| A nested loop adds the counts of the two levels. | It multiplies them: n by m is n*m body executions. |
| The inner loop continues from where it stopped. | It restarts from the beginning of its sequence each outer pass. |
| Every grid is rectangular, so a fixed width is fine. | Sensor data is often ragged; iterate the rows instead. |
| A third level is needed for a 2-D problem. | Two levels plus enumerate cover most grids; the third is usually waste. |

## Difficult concepts

- Accepting that a nested loop is sometimes the wrong tool.
- Deriving the pairwise product sum rather than enumerating it.
- Handling a ragged grid without defensive guards at every level.

## Demonstration suggestions

- Count the body executions for a 3 by 4 grid and compare with 3 + 4.
- Break out of a fixed-width loop on a ragged grid and read the IndexError.
- Time a pairwise sum against its closed form on 10000 values.

## Discussion questions

- Which problems genuinely need two levels of iteration?
- Is a closed form always better, even when it is less obvious?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| IndexError on a ragged grid | A hard-coded inner bound assumed a fixed width | Iterate the rows themselves |
| A cell is counted twice | range(len(grid) - 1) drops the last index, or a flag was never reset | Enumerate both levels and test with a ragged grid |
| The routine takes minutes on a full grid | A third level was added, or a window was scanned nested | Count the steps first, then apply a closed form or a sliding window |

## Recommended pacing

90 minutes of lesson with a live step count, then 2 hours of exercises. Spend real time on the closed form: it is the first time a student replaces code with algebra, and that idea recurs for the rest of the course.

## Extension activities

- Ask students to derive the count of distinct pairs from the sequence length.
- Have them convert a nested window scan into a sliding window and time both.

## Assessment advice

Grade against rubric.md. Exercises 7, 8 and 10 carry the signal: they require ragged-safe accumulation, bounds-checked neighbour scans and a real API call.

## Differentiation

**If students are struggling:** Provide the count_cells solution and ask students to add a cols field, so the ragged case is visible before they write the harder functions.

**If students finish early:** Ask for a short note on how to bound the cost of a three-level scan over a fixed-size kernel.
