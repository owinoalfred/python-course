# Instructor notes — 3.2 Tuples

**Module 3: Core Data Structures**

## Teaching objectives

- Establish 'immutable binding, mutable contents' as the tuple model.
- Make hashability concrete through dict-key failures students see live.
- Build the list-then-tuple() habit before students discover the quadratic accident themselves.

## Likely misconceptions

| Misconception | Correction to drive home |
| --- | --- |
| A tuple is deeply immutable. | Only its slots are fixed; inner lists still mutate. |
| (x) is a one-element tuple. | It is just x in parentheses - the comma makes the tuple. |
| Any tuple can be a dict key. | Only hashable tuples - all elements hashable - qualify. |
| There is a tuple comprehension. | The parentheses build a generator; tuple(...) materialises it. |

## Difficult concepts

- Why hashability follows from immutability, element by element.
- Evaluation order in `a, b = b, a`.
- When a record should graduate from tuple to namedtuple to dataclass.

## Demonstration suggestions

- Live: t = ([1],); t[0].append(2); print(t) - watch 'immutable' data change.
- Live: {[1, 2]} raises TypeError, {tuple([1, 2])} succeeds.
- Time acc = acc + (i,) against list-append + tuple() at n = 20000.

## Discussion questions

- Should mission logs be tuples end-to-end, or is a frozen dataclass the professional answer? What does each cost?
- Where does 'immutable by convention' break down in a team codebase?

## Common student errors

| Error | Why it happens | Intervention |
| --- | --- | --- |
| TypeError: unhashable type: 'list' | A list sits inside the key tuple | Freeze it with tuple() or keep keys to primitives |
| Tuple 'changed' after a function ran | An inner mutable was modified through an alias | Deep-freeze or copy the payload at the boundary |
| Loop over a tuple raises TypeError: not iterable | The value is an int, not a 1-tuple - comma missing | Write (x,) or x, |

## Recommended pacing

55 min: record model and unpacking (15), hashability live demo (10), shallow immutability trap (15), practice start (15). Performance and freeze/recursion exercises go to homework.

## Extension activities

- Compare sys.getsizeof tuple vs list for 1000 elements.
- Explore dataclasses.replace as the mutable-record escape hatch.

## Assessment advice

Exercise 7 (deep freeze) and Exercise 6 (version tuples) separate students who understand hashability from those who memorised the syntax.

## Differentiation

**If students are struggling:** Use the sealed-envelope diagram: draw addresses inside an envelope and notebooks outside. If hash() still confuses it, hash three objects live and show dict[key] lookup succeeding and failing.

**If students finish early:** ('Fast finishers implement freeze() handling sets with sorted-by-repr elements and prove hash stability across two builds.',)
