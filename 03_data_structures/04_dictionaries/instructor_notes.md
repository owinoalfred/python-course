# Instructor notes — 3.4 Dictionaries

**Module 3: Core Data Structures**

## Teaching objectives

- Make the []-versus-get contract a conscious choice, never a habit.
- Have students draw the shared-inner-dict picture before they meet the bug in code.
- Turn 'snapshot then rebind' into their default update pattern.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| copy() gives a fully independent dict. | It is shallow - inner dicts remain shared objects. |
| get() is the safe version of []. | It is a different contract; unsafe when absence is a real error. |
| Dicts keep sorted order. | They keep insertion order; sort() only when you need sorted. |
| Mutating during iteration sometimes works. | It raises RuntimeError the moment the table resizes - never rely on it. |

## Difficult concepts

- Why hashability is required of keys but not values.
- Atomic publication by rebinding versus in-place mutation.
- The cost model: what is O(1), what is O(n), and why values scans are the latter.

## Demonstration suggestions

- Live shallow-copy corruption: clone = d.copy(); clone['cfg']['x'] = 1; print(d).
- Time dict lookup against linear scan at 100000 keys on the projector.
- Trigger RuntimeError by adding a key mid-loop, then fix with list(d).

## Discussion questions

- When is a KeyError better than a default? Argue both sides using the config example.
- Is a dict ever the wrong structure for a record? (Ordered fields with methods -> dataclass; schema validation -> pydantic.)

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| None appears where a value should be | get() without a meaningful default on a required key | Use [] for required keys and let KeyError name it |
| Editing a clone changed the original | Shallow copy shared the inner dict | deepcopy or rebuild inner levels at the boundary |
| RuntimeError: dictionary changed size | Key added/removed during iteration | Snapshot with list(d) or rebuild with a comprehension |

## Recommended pacing

65 min: pigeonhole model and access contracts (15), shallow-copy corruption live (10), views and mutation guard (10), counting and grouping idioms (10), atomic-update pattern (10), practice start (10).

## Extension activities

- Compare dict insertion-order guarantee with set's arbitrary order.
- Explore collections.defaultdict and Counter for the counting idiom.

## Assessment advice

Exercise 6 (deep copy without the module) and Exercise 10 (atomic merge) separate dict users from dict understanders.

## Differentiation

**If students are struggling:** ('Give struggling students the pigeonhole diagram and have them draw hash, slot and key check before writing lookups. For copy issues, require id() prints as evidence before any prose explanation.',)

**If students finish early:** ('Fast finishers implement a tiny JSON-like serialiser for nested dicts and prove a round trip preserves insertion order.',)
