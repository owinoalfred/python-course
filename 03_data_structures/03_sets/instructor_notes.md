# Instructor notes — 3.3 Sets

**Module 3: Core Data Structures**

## Teaching objectives

- Make O(1) membership measurable, not asserted - the timing demo is the lesson's spine.
- Get `set()` for the empty set and sorted-before-print into habit.
- Show set algebra as validation logic, not as puzzle operations.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| Sets remember insertion order. | They do not - sort explicitly whenever output matters. |
| {} is the empty set. | It is an empty dict; the empty set is set(). |
| Any value can go in a set. | Only hashables; lists and dicts raise TypeError. |
| Mutating during iteration just skips elements. | It raises RuntimeError - the guard is deliberate. |

## Difficult concepts

- Why hashability is required but order is not stored.
- The mutating (|=) versus new-set (|) distinction under aliasing.
- Reading difference direction as meaning, not syntax.

## Demonstration suggestions

- Time 20000 membership probes against list vs set on the projector; let the class predict the ratio first.
- Live: add during iteration, read the RuntimeError, then iterate a copy.
- Build the anagram groups with frozenset keys live to connect hashing to dict keys.

## Discussion questions

- When is losing order actually unacceptable - and what is the ordered, deduplicated alternative? (dict.fromkeys.)
- Is `try/except RuntimeError` around a mutating loop every acceptable? What would it hide?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| AttributeError: 'dict' object has no attribute 'add' | Wrote {} instead of set() | Use set() for empties; test with type() |
| TypeError: unhashable type: 'list' | A list was used as a set element | Convert to tuple, or keep primitives |
| Report order changes between runs | Printed the set directly | Wrap in sorted() at the output boundary |

## Recommended pacing

60 min: membership timing demo (10), construction and {} trap (10), algebra and direction (15), seen-set idiom walkthrough (10), practice start (15). Algebra-heavy exercises to homework.

## Extension activities

- Time frozenset vs tuple as dict keys for 50000 lookups.
- Investigate dict.fromkeys as an order-preserving deduplicator.

## Assessment advice

Exercise 5 (duplicate frames with order) and Exercise 6 (coverage report) jointly test whether students can convert prose into set relations.

## Differentiation

**If students are struggling:** ("Draw two overlapping circles per algebra example and shade the answer; require the drawing before the code. If direction confuses them, insist on reading `a - b` aloud as 'a without b'.",)

**If students finish early:** ('Fast finishers prove a ^ b == (a | b) - (a & b) on ten random pairs and write the Venn argument for why it must hold.',)
