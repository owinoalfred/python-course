# Instructor notes — 3.1 Lists

**Module 3: Core Data Structures**

## Teaching objectives

- Make aliasing visible before any method is taught - the mental model comes first.
- Turn 'methods return None' into a memorised fact, not a surprise.
- Get students copying deliberately at boundaries, not defensively everywhere.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| Assignment copies the list. | It binds a second name to one object; only list(x)/copy()/slice do. |
| copy() gives fully independent data. | It is shallow - inner objects are still shared with the original. |
| sort() returns the sorted list. | It returns None; sorted() is the one that returns a list. |
| Mutating while iterating is fine if you only remove a few items. | Removals shift positions, so elements get skipped unpredictably. |

## Difficult concepts

- Why [x] * n shares references but a comprehension does not.
- That append is amortised O(1) while insert(0) is O(n) per call.
- Deciding, line by line, between sharing and copying.

## Demonstration suggestions

- Run the aliasing demo live: b = a; b.append(...); print(a) and watch the class predict before running.
- Build [[0]] * 2, mutate row 0, and let the class see both rows change.
- Time a = a + [x] against a.append(x) for increasing n on the projector.

## Discussion questions

- Is defensive copying everywhere a virtue, or does it hide design problems? When is sharing the right choice?
- Who owns a list passed across a module boundary - the caller or the callee?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| The list mysteriously changed elsewhere | A second name aliased it and was mutated | Prove identity with `is` and copy at the boundary |
| Variable became None after sorting | readings = readings.sort() assigned the return value | Call .sort() alone or use sorted() |
| Loop deleted only some of the matching items | Removal during direct iteration skipped elements | Iterate a copy or build a filtered list |

## Recommended pacing

60 min: aliasing demo and mental model (20), method contract and None (15), copies and shallowness (15), practice start (10). The exercises carry performance and in-place algorithms for homework.

## Extension activities

- Compare list versus deque timings for queue workloads.
- Explore copy.deepcopy on a structure containing tuples and dicts.

## Assessment advice

Exercise 1 (copy discipline) and Exercise 8 (in-place rotation) together separate students who understand mutation from those who have memorised syntax.

## Differentiation

**If students are struggling:** Give struggling students the box-and-label diagram and have them draw every assignment before writing code; if `is` still confuses them, use id() printed values as concrete evidence.

**If students finish early:** Fast finishers implement rotate_in_place with the juggling algorithm and prove it matches the reversal version on random inputs.
