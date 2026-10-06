"""Topic 3.3 - Sets.

Hand-authored to the Course Content Standard. The spine: a set is an unordered
collection of unique hashable objects - membership in O(1) is the payoff, and
losing order (and unhashable elements) is the price.
"""

from __future__ import annotations

from tools.coursegen.dsl import (
    BULLETS,
    CODE,
    CODE_CELL,
    EQUATION,
    MD,
    NOTE,
    STEPS,
    TABLE,
    TIP,
    WARN,
    exercise,
    quiz,
    solution,
    topic,
)

LESSON: dict[str, list] = {}

LESSON["conceptual_explanation"] = [
    MD(
        "A set is an **unordered collection of unique, hashable objects**. "
        "Uniqueness is not a feature applied on top - it is the type's "
        "identity: putting the same value into a set twice leaves one element, "
        "because a set has exactly one slot per distinct hash. Unordered means "
        "there is no `set[0]`, no indexing, no slicing: the only sensible ways "
        "to read a set are iteration, membership tests and set algebra."
    ),
    MD(
        "The payoff for dropping order is speed. Membership `x in s` is O(1) "
        "on average - the same hash lookup a dict performs - where the same "
        "test against a list is O(n). That single difference decides which "
        "type belongs in a hot loop: a seen-set turns a quadratic duplicate "
        "scan into a linear one."
    ),
    CODE_CELL(
        "import time\n"
        "\n"
        "values = list(range(20000))\n"
        "member_set = set(values)\n"
        "\n"
        "start = time.perf_counter()\n"
        "hits_list = sum(1 for v in values if v in values)\n"
        "list_s = time.perf_counter() - start\n"
        "\n"
        "start = time.perf_counter()\n"
        "hits_set = sum(1 for v in values if v in member_set)\n"
        "set_s = time.perf_counter() - start\n"
        "\n"
        "print(f'list scan {list_s:.4f}s vs set scan {set_s:.4f}s')\n"
        "print(f'set is {list_s / max(set_s, 1e-9):.0f}x faster here')"
    ),
    MD(
        "Two rules follow from hashability. First, every element must be "
        "hashable - lists and dicts are banned, tuples and strings are fine. "
        "Second, because the set decides placement by hash, it must not be "
        "modified while being iterated; like a dictionary, growing a set "
        "during iteration raises RuntimeError."
    ),
    MD(
        "Sets also carry *relations*: subset, superset and disjoint describe "
        "how two sets overlap, and those relations power the whole family of "
        "set-algebra operations - union, intersection, difference and "
        "symmetric difference - each returning a new set rather than mutating "
        "the operands."
    ),
]

LESSON["formal_theory"] = [
    MD(
        "A set implements the mathematical finite set over hashable elements. "
        "Membership, insertion and deletion are O(1) average (O(n) worst case "
        "under hash collisions); every set-algebra operation is linear in the "
        "size of the operands:"
    ),
    EQUATION("A | B = union   A & B = intersection   A - B = difference   A ^ B = symmetric difference"),
    CODE_CELL(
        "crew = {'ada', 'grace', 'alan'}\n"
        "on_call = {'grace', 'linus'}\n"
        "\n"
        "print('union        :', crew | on_call)\n"
        "print('intersection :', crew & on_call)\n"
        "print('crew - on_call:', crew - on_call)\n"
        "print('symmetric    :', crew ^ on_call)"
    ),
    TABLE(
        ["Expression", "Meaning", "Returns"],
        [
            ["`a | b`", "elements in either", "new set"],
            ["`a & b`", "elements in both", "new set"],
            ["`a - b`", "elements of a missing from b", "new set"],
            ["`a ^ b`", "elements in exactly one", "new set"],
            ["`a <= b`", "a is a subset of b", "bool"],
            ["`a.isdisjoint(b)`", "a and b share nothing", "bool"],
        ],
    ),
    MD(
        "The in-place operators exist too: `a |= b`, `a &= b`, `a -= b` and "
        "`a ^= b` mutate the left operand and return it, exactly like list "
        "methods returning None. The distinction matters in shared code - "
        "`result = a | b` preserves `a`, while `a |= b` rebinds and mutates "
        "`a`, so the caller who passed `a` sees a different set afterward."
    ),
    MD(
        "Construction has four forms, and the set-literal `{...}` is only one "
        "of them - `{}` is an empty **dict**, not an empty set, because braces "
        "are already claimed by dict display. `set(iterable)` converts, "
        "`set()` builds empty, and `{x for x in ...}` is a set comprehension."
    ),
    CODE_CELL(
        "empty_dict = {}                       # a dict, not a set!\n"
        "empty_set = set()                     # the empty set\n"
        "literal = {1, 2, 3}\n"
        "from_comp = {v * 2 for v in range(3)}\n"
        "converted = set(['a', 'a', 'b'])      # duplicates collapse\n"
        "\n"
        "print('dict :', type(empty_dict).__name__)\n"
        "print('set  :', type(empty_set).__name__, empty_set)\n"
        "print('comp :', from_comp)\n"
        "print('dedup:', converted)"
    ),
]

LESSON["syntax"] = [
    MD("Construction, membership, and the mutating algebra - each with its non-mutating twin."),
    CODE_CELL(
        "tags = {'fault', 'warn'}               # set literal\n"
        "tags.add('info')                       # one element, in place\n"
        "tags.update(['fault', 'debug'])        # many; 'fault' is deduped\n"
        "tags.discard('debug')                  # missing element is OK\n"
        "tags.remove('info')                    # missing element raises\n"
        "\n"
        "print('tags  :', tags)\n"
        "print('member:', 'warn' in tags)       # O(1) membership\n"
        "\n"
        "unioned = tags | {'calibrated'}        # NEW set; tags unchanged\n"
        "print('original still:', tags)\n"
        "print('union         :', unioned)"
    ),
    MD("The anti-pattern - building a unique list by hand, which is quadratic:"),
    CODE(
        "seen = []\n"
        "for value in stream:\n"
        "    if value not in seen:   # O(n) per test -> O(n^2) overall\n"
        "        seen.append(value)\n"
        "\n"
        "seen = set()\n"
        "for value in stream:\n"
        "    seen.add(value)         # O(1) per insert -> O(n) overall\n"
        "# order needed later? sort() it, or keep a parallel list.",
        lang="text",
    ),
    WARN(
        "`{}` creates a dict",
        "The empty set must be written `set()`. A bare `{}` is an empty dict, "
        "and the mistake hides until `{}.add(...)` raises AttributeError - "
        "which is why type() in tests catches it faster than reading the code.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - deduplicate a stream in one line.**"),
    CODE_CELL(
        "readings = [0.4, 0.9, 0.4, 0.7, 0.9]\n"
        "unique = set(readings)\n"
        "\n"
        "print('original :', readings, ' len', len(readings))\n"
        "print('unique   :', sorted(unique), ' len', len(unique))\n"
        "print('duplicates removed:', len(readings) - len(unique))"
    ),
    MD("**Example 2 - membership as a fast lookup table.**"),
    CODE_CELL(
        "fault_codes = {'E01', 'E02', 'E17'}\n"
        "\n"
        "for code in ('E01', 'E09'):\n"
        "    print(f'{code} known?', code in fault_codes)\n"
        "\n"
        "try:\n"
        "    fault_codes.add('E01')          # already present: no change\n"
        "    print('add is idempotent:', fault_codes)\n"
        "except Exception as exc:\n"
        "    print('unexpected:', exc)"
    ),
    MD("**Example 3 - a set comprehension for derived collections.**"),
    CODE_CELL(
        "log = ['BOOT', 'WARN', 'BOOT', 'CAL', 'WARN']\n"
        "events = {line.split()[0] for line in log}\n"
        "print('distinct event kinds:', sorted(events))\n"
        "\n"
        "first_letters = {name[0] for name in ('ada', 'alan', 'grace')}\n"
        "print('initials:', sorted(first_letters))"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "**The seen-set idiom.** The single most valuable set pattern in "
        "Python: converting a repeated `not in list` test into an O(1) hash "
        "lookup, usually while preserving first-seen order in a parallel list."
    ),
    CODE_CELL(
        "def first_seen_order(values):\n"
        "    \"\"\"Unique values in first-seen order.\"\"\"\n"
        "    seen = set()\n"
        "    ordered = []\n"
        "    for value in values:\n"
        "        if value not in seen:\n"
        "            seen.add(value)\n"
        "            ordered.append(value)\n"
        "    return ordered\n"
        "\n"
        "print(first_seen_order(['b', 'a', 'b', 'c', 'a']))"
    ),
    MD(
        "**Relations between sets** answer questions list membership cannot: "
        "\"is every subscriber also a crew member?\", \"do these two fault "
        "sets overlap at all?\""
    ),
    CODE_CELL(
        "crew = {'ada', 'grace', 'alan'}\n"
        "pilots = {'grace'}\n"
        "operators = {'linus', 'ada'}\n"
        "\n"
        "print('pilots subset of crew?', pilots <= crew)\n"
        "print('crew covers operators?', crew >= operators)\n"
        "print('disjoint with operators?', crew.isdisjoint(operators))\n"
        "print('shared:', sorted(crew & operators))"
    ),
    MD(
        "**Frozen sets complete the lattice.** Just as tuple is list's "
        "immutable sibling, `frozenset` is set's: hashable, so a frozenset "
        "may live inside a set or serve as a dict key."
    ),
    CODE_CELL(
        "roles = {frozenset({'pilot'}), frozenset({'pilot', 'engineer'})}\n"
        "print('hashable nested sets:', roles)\n"
        "\n"
        "try:\n"
        "    { {'a'} }\n"
        "except TypeError as exc:\n"
        "    print('mutable set rejected:', exc)"
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "**Ordering is not just missing - it is deliberately arbitrary.** A "
        "set's iteration order depends on hash values and insertion history, "
        "so identical sets built in different orders may iterate differently. "
        "Any code that needs reproducible output must sort explicitly."
    ),
    CODE_CELL(
        "a = set(['x', 'y', 'z'])\n"
        "b = set(['z', 'y', 'x'])\n"
        "\n"
        "print('equal sets?', a == b)              # True - equality is content\n"
        "print('same order?', list(a) == list(b))  # NOT guaranteed\n"
        "print('reproducible:', sorted(a))         # sort when order matters"
    ),
    MD(
        "**Set algebra as validation.** 'Exactly these keys were supplied' is "
        "one symmetric difference away: `supplied ^ expected` is empty if and "
        "only if the two sets match, and the difference names precisely what "
        "is extra or missing."
    ),
    CODE_CELL(
        "expected = {'host', 'port', 'timeout'}\n"
        "supplied = {'host', 'port', 'retries'}\n"
        "\n"
        "extra = supplied - expected\n"
        "missing = expected - supplied\n"
        "print('extra   :', sorted(extra))\n"
        "print('missing :', sorted(missing))\n"
        "print('exact match?', supplied == expected)\n"
        "print('symmetric diff:', sorted(supplied ^ expected))"
    ),
    WARN(
        "do not mutate a set while iterating it",
        "Adding or discarding elements during `for x in s` raises "
        "RuntimeError: Set changed size during iteration. Iterate a copy - "
        "`for x in set(s)` or `for x in list(s)` - or rebuild the result with "
        "a comprehension.",
    ),
    CODE_CELL(
        "faults = {'E01', 'E02', 'E03'}\n"
        "try:\n"
        "    for code in faults:\n"
        "        if code == 'E02':\n"
        "            faults.add('E99')\n"
        "except RuntimeError as exc:\n"
        "    print('caught:', exc)\n"
        "\n"
        "cleared = {c for c in faults if c != 'E02'}   # the clean way\n"
        "print('filtered:', sorted(cleared))"
    ),
    TIP(
        "counting with Counter",
        "When uniqueness gives way to counting, `collections.Counter` is a "
        "dict subclass built for exactly that. Reach for a set when you need "
        "*presence*; reach for Counter when you need *how many*.",
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "**A duplicate detector for incoming telemetry frames.** Frames arrive "
        "as `(channel, seq)` tuples; replayed frames must be dropped without "
        "an O(n) scan, and the report says how many were rejected."
    ),
    CODE_CELL(
        "def dedupe_frames(frames):\n"
        "    \"\"\"Drop replayed (channel, seq) frames, preserving first-seen order.\"\"\"\n"
        "    seen = set()\n"
        "    fresh = []\n"
        "    for frame in frames:\n"
        "        if frame in seen:\n"
        "            continue                    # replay - already logged\n"
        "        seen.add(frame)\n"
        "        fresh.append(frame)\n"
        "    rejected = len(frames) - len(fresh)\n"
        "    return fresh, rejected\n"
        "\n"
        "stream = [('imu', 1), ('imu', 2), ('imu', 1), ('gps', 1)]\n"
        "clean, rejected = dedupe_frames(stream)\n"
        "print('fresh    :', clean)\n"
        "print('rejected :', rejected)"
    ),
    BULLETS(
        [
            "`seen = set()` is the O(1) membership table; tuples hash fine, so "
            "frames drop straight in.",
            "`continue` on a hit keeps the happy path flush left - the "
            "membership test is the only branch.",
            "The parallel `fresh` list preserves arrival order, which the set "
            "itself cannot do.",
            "Reporting `rejected` as a count avoids keeping the discarded "
            "frames in memory.",
        ]
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "`seen = set()` - an empty membership table, O(1) per lookup from "
            "the first frame onward.",
            "`for frame in frames:` - one pass over the stream; frames are "
            "tuples, so they are hashable.",
            "`if frame in seen: continue` - the whole duplicate test; with a "
            "list this line would be O(n).",
            "`seen.add(frame)` - registers the frame BEFORE appending, so a "
            "second copy later hits the test.",
            "`fresh.append(frame)` - order-preserving output the set cannot "
            "provide on its own.",
            "`rejected = len(frames) - len(fresh)` - a derived count, cheaper "
            "than storing rejects and consistent by construction.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - writing `{}` for the empty set.**"),
    CODE(
        "tags = {}            # dict!\n"
        "tags.add('x')        # AttributeError: 'dict' object has no attribute 'add'\n"
        "tags = set()         # the empty set",
        lang="text",
    ),
    MD("**Mistake 2 - expecting a set to remember insertion order.**"),
    CODE(
        "s = {'c', 'a', 'b'}\n"
        "print(list(s))       # some order - NOT insertion order, not sorted\n"
        "print(sorted(s))     # ['a', 'b', 'c'] - explicit, reproducible",
        lang="text",
    ),
    MD("**Mistake 3 - putting unhashable elements in a set.**"),
    CODE(
        "bad = {[1, 2]}       # TypeError: unhashable type: 'list'\n"
        "good = {(1, 2)}      # tuples hash fine\n"
        "also = {frozenset({1, 2})}",
        lang="text",
    ),
    MD("**Mistake 4 - mutating a set during iteration.**"),
    CODE(
        "s = {1, 2, 3}\n"
        "for x in s:\n"
        "    s.add(x + 10)    # RuntimeError: Set changed size during iteration\n"
        "\n"
        "for x in set(s):     # iterate a snapshot instead\n"
        "    ...",
        lang="text",
    ),
    MD("**Mistake 5 - using `remove` on a possibly-absent element.**"),
    CODE(
        "s = {'a'}\n"
        "s.remove('b')        # KeyError - remove is strict\n"
        "s.discard('b')       # no error - discard is forgiving",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "When a set seems to lose or invent elements, print sorted() so the "
        "contents are stable, and print the *type* of the container itself - "
        "`{}` vs `set()` and list-vs-set confusions are diagnosed in one line."
    ),
    CODE_CELL(
        "container = {}\n"
        "print('type:', type(container).__name__)\n"
        "\n"
        "tags = set(['a', 'a', 'b'])\n"
        "print('deduped contents:', sorted(tags))\n"
        "print('expected 2, got :', len(tags))\n"
        "\n"
        "unhashable = None\n"
        "try:\n"
        "    {unhashable or [1]}\n"
        "except TypeError as exc:\n"
        "    print('hash failure:', exc)"
    ),
    MD(
        "When two sets 'disagree', compare them with the algebra itself - "
        "symmetric difference names the disagreement, and equality is one "
        "line."
    ),
    CODE_CELL(
        "expected = {'host', 'port'}\n"
        "actual = {'host', 'timeout'}\n"
        "\n"
        "print('equal?', expected == actual)\n"
        "print('only expected:', sorted(expected - actual))\n"
        "print('only actual  :', sorted(actual - expected))\n"
        "print('both         :', sorted(expected & actual))"
    ),
    NOTE(
        "Hash failures name the culprit",
        "TypeError: unhashable type: 'dict' always names the inner type - "
        "walk your structure until you find it. The fix is almost always a "
        "tuple conversion or a frozenset.",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Use a set for membership tests that repeat over a collection - it "
            "is the difference between O(n^2) and O(n).",
            "Write `set()` for the empty set; treat `{}` as a dict always.",
            "Preserve order with a parallel list when order matters; never "
            "rely on set iteration order for output.",
            "Sort (`sorted(s)`) before printing, logging or snapshot testing a "
            "set.",
            "`discard` for optional removals, `remove` when absence is a real "
            "error worth raising.",
            "Validate 'exactly these keys' with `==` on sets or a symmetric "
            "difference, not a chain of `in` checks.",
            "Use frozenset when a set must be a dict key or set element.",
            "Rebuild with comprehensions instead of mutating during iteration.",
            "Convert to a set for deduplication only when order is irrelevant "
            "- otherwise use the seen-set idiom from the walkthrough.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "A set is a hash table: average O(1) membership, insertion and "
        "deletion, O(n) worst case only under hash collisions. Every algebra "
        "operation walks at least one operand, so their cost is linear in the "
        "input sizes - and the smaller operand should usually be the one walked."
    ),
    TABLE(
        ["Pattern", "Cost", "Preferred alternative"],
        [
            ["`x in list` inside a loop", "O(n) per test - quadratic total", "`seen = set(list)` once, then O(1)"],
            ["manual dedup with `if v not in out`", "O(n^2)", "`set(values)` or the seen-set idiom"],
            ["`for x in a: if x in b`", "O(len(a) * len(b))", "`a & b` runs in O(len(a) + len(b))"],
            ["sorted output from a set", "O(n log n)", "unavoidable - order is not stored"],
            ["`set(list)` construction", "O(n) expected", "the right default for dedup"],
        ],
    ),
    CODE_CELL(
        "import time\n"
        "\n"
        "n = 30000\n"
        "values = list(range(n))\n"
        "\n"
        "start = time.perf_counter()\n"
        "naive = []\n"
        "for v in values:\n"
        "    if v not in naive:          # O(n) scan per element\n"
        "        naive.append(v)\n"
        "naive_s = time.perf_counter() - start\n"
        "\n"
        "start = time.perf_counter()\n"
        "seen = set()\n"
        "fast = []\n"
        "for v in values:\n"
        "    if v not in seen:           # O(1) lookup per element\n"
        "        seen.add(v)\n"
        "        fast.append(v)\n"
        "fast_s = time.perf_counter() - start\n"
        "\n"
        "print(f'naive {naive_s:.4f}s vs seen-set {fast_s:.4f}s')\n"
        "print(f'seen-set is {naive_s / max(fast_s, 1e-9):.1f}x faster')"
    ),
    MD(
        "The quadratic term is what the table means in practice: doubling n "
        "quadruples the naive loop's work while doubling the seen-set's. At "
        "30000 elements the gap is already orders of magnitude - and at a "
        "million, the naive version would not finish."
    ),
]

LESSON["pythonic_approaches"] = [
    MD(
        "Sets make whole classes of checkable intent expressible in one "
        "expression: membership relations, exact-set validation and "
        "deduplication - each replacing a loop the reader would have to audit "
        "by eye."
    ),
    CODE_CELL(
        "required = {'host', 'port'}\n"
        "supplied = {'host', 'port', 'timeout'}\n"
        "\n"
        "# not pythonic: a chain of membership checks\n"
        "ok = 'host' in supplied and 'port' in supplied\n"
        "\n"
        "# pythonic: the relation IS the check\n"
        "ok = required <= supplied\n"
        "print('all required supplied?', ok)\n"
        "print('unexpected keys      :', sorted(supplied - required))"
    ),
    BULLETS(
        [
            "`set(xs)` to deduplicate; pair it with `sorted()` when output "
            "must be stable.",
            "`required <= supplied` replaces chains of `in` when validating "
            "presence.",
            "`a ^ b == set()` (or `a == b`) for exact-set equality checks.",
            "`set.isdisjoint` reads better than `not (a & b)` - and short-circuits.",
            "Set comprehensions `{f(x) for x in xs}` dedupe as they map.",
            "`dict.fromkeys(xs).keys()` preserves first-seen order when you "
            "need dedup WITH order (a dict view, not a set).",
            "Complement loops with `seen` sets rather than re-scanning the "
            "accumulator.",
        ]
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "A rover's fault supervisor tracks active fault codes as a set: "
        "duplicates are meaningless (a fault is either present or not), the "
        "supervisor asks 'is E17 active?' thousands of times a second, and "
        "clearing is one discard per code. A list would turn each of those "
        "questions into a scan."
    ),
    CODE_CELL(
        "import sys\n"
        "from pathlib import Path\n"
        "\n"
        "here = Path.cwd()\n"
        "root = next((p for p in [here, *here.parents] if (p / 'shared').is_dir()), None)\n"
        "if root is not None:\n"
        "    sys.path.insert(0, str(root))\n"
        "\n"
        "from shared.robo_x_sim import SimulatedRobot  # noqa: E402\n"
        "\n"
        "robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\n"
        "active = set()\n"
        "\n"
        "if robot.is_low_battery(threshold_pct=100.0):\n"
        "    active.add('E_BATT')\n"
        "active.add('E_BATT')          # repeat report: still one entry\n"
        "\n"
        "print('active faults:', sorted(active))\n"
        "print('E_BATT active?', 'E_BATT' in active)   # the hot-path query\n"
        "print('cleared:')\n"
        "active.discard('E_BATT')\n"
        "print(' ', sorted(active))"
    ),
    MD(
        "The engineering rule: presence questions get sets, order questions "
        "get lists. A fault *log* is a list (events in time order); a fault "
        "*state* is a set (codes present now). Confusing the two either costs "
        "quadratic scans or loses the timeline - and the supervisor's "
        "`isdisjoint` check against a set of critical codes is the kind of "
        "one-line safety test sets make possible."
    ),
]

LESSON["engineering_example"] = [
    MD(
        "Configuration validation is where set relations replace boilerplate: "
        "compare supplied keys against required keys and report both "
        "unexpected and missing entries from one symmetric difference."
    ),
    CODE_CELL(
        "def validate_config(supplied, required):\n"
        "    \"\"\"Return (unexpected, missing) key lists; empty means valid.\"\"\"\n"
        "    supplied, required = set(supplied), set(required)\n"
        "    unexpected = sorted(supplied - required)\n"
        "    missing = sorted(required - supplied)\n"
        "    return unexpected, missing\n"
        "\n"
        "ok_u, ok_m = validate_config(['host', 'port'], {'host', 'port'})\n"
        "bad_u, bad_m = validate_config(['host', 'colour'], {'host', 'port'})\n"
        "print('valid case:', (ok_u, ok_m))\n"
        "print('unexpected:', bad_u, ' missing:', bad_m)"
    ),
    MD(
        "Sorting inside the function makes the report reproducible across "
        "runs - a set's iteration order is not - and converting both sides "
        "with `set(...)` means callers may pass lists, tuples or sets "
        "interchangeably. The whole validation is four lines and has no loop "
        "to get wrong."
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Build a set three ways - literal, `set(list)` and a comprehension "
            "- and print `type()` and `len()` for each to see duplicates "
            "collapse.",
            "Prove `{}` is a dict by calling `.add()` on it and reading the "
            "AttributeError, then use `set()` correctly.",
            "Take two small sets and print union, intersection, difference and "
            "symmetric difference with `sorted()`.",
            "Reproduce the RuntimeError from adding during iteration, then "
            "fix it by iterating `set(s)`.",
            "Time a duplicate scan against a seen-set for 20000 elements and "
            "record the ratio.",
        ]
    ),
    CODE_CELL(
        "tags = {'fault', 'warn', 'fault'}\n"
        "from_list = set(['a', 'b', 'a'])\n"
        "from_comp = {n * n for n in range(4)}\n"
        "print('literal:', sorted(tags), ' from_list:', sorted(from_list), ' comp:', sorted(from_comp))\n"
        "\n"
        "try:\n"
        "    {}\n"
        "    {}.add('x')\n"
        "except AttributeError as exc:\n"
        "    print('braces are a dict:', exc)\n"
        "\n"
        "a, b = {1, 2, 3}, {2, 3, 4}\n"
        "print('union:', sorted(a | b), ' inter:', sorted(a & b))\n"
        "print('a - b:', sorted(a - b), ' sym:', sorted(a ^ b))\n"
        "\n"
        "s = {1, 2}\n"
        "try:\n"
        "    for x in s:\n"
        "        s.add(x + 10)\n"
        "except RuntimeError as exc:\n"
        "    print('mutation guard:', exc)"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: a set is a room with named hooks, and each name may "
        "hang on exactly one hook.** Inserting an already-present name finds "
        "its hook and does nothing; there is no 'first' or 'last' hook, so no "
        "order exists to remember; and a name you cannot hash is a name the "
        "doorkeeper cannot place, so it never gets in."
    ),
    TABLE(
        ["Question", "Answer", "Consequence"],
        [
            ["Duplicates?", "collapsed by construction", "`set(xs)` dedupes in O(n)"],
            ["Order?", "none stored", "`sorted(s)` whenever output matters"],
            ["`s[0]`?", "TypeError - no indexing", "iterate, test membership, or use algebra"],
            ["`x in s` cost?", "O(1) average", "the reason sets exist"],
            ["Lists as elements?", "TypeError - unhashable", "convert to tuples"],
            ["`{}`?", "an empty dict", "empty set is `set()`"],
        ],
    ),
]

TERMS = [
    ["Set", "An unordered collection of unique, hashable objects."],
    ["Membership test", "`x in s` - an O(1) average hash lookup."],
    ["Hashable", "An object with a stable hash; required for set elements."],
    ["Unordered", "No indexing or insertion order; iteration order is arbitrary."],
    ["Union", "`a | b` - elements present in either set."],
    ["Intersection", "`a & b` - elements present in both sets."],
    ["Difference", "`a - b` - elements of a absent from b."],
    ["Symmetric difference", "`a ^ b` - elements in exactly one of the sets."],
    ["Subset / superset", "`a <= b` - every element of a is in b (relations as booleans)."],
    ["frozenset", "The immutable, hashable sibling of set - usable as a set element or key."],
]

LESSON["summary"] = [
    MD(
        "A set is an unordered bag of unique hashable objects, and every "
        "choice it makes follows from that: uniqueness collapses duplicates "
        "the moment they arrive, order is not stored so output must be "
        "sorted, and hashability bans lists and dicts as elements. The "
        "payoff is O(1) average membership - the difference between a "
        "quadratic duplicate scan and a linear one."
    ),
    MD(
        "The algebra is the second half of the topic. Union, intersection, "
        "difference and symmetric difference each build a new set, while the "
        "in-place `|=`, `&=`, `-=` and `^=` mutate the left operand exactly "
        "like list methods returning None. Relations - subset, superset, "
        "disjoint - turn validation questions (`required <= supplied`) into "
        "single expressions that cannot be mis-ordered by hand."
    ),
    MD(
        "In practice: presence questions are set questions. A seen-set "
        "upgrades any repeated membership loop from O(n^2) to O(n); "
        "`set(xs)` deduplicates whenever order does not matter; frozenset "
        "completes the lattice for nested keys. The failure modes - `{}` as "
        "dict, mutation during iteration, unhashable elements - are all "
        "loud, and each one names its own fix in the error message."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "Sets are unordered, unique, and hashable-only; `{}` is a dict, "
            "`set()` is the empty set.",
            "`x in s` is O(1) average - the tool that removes quadratic loops.",
            "`set(xs)` deduplicates in O(n); pair with `sorted()` for stable "
            "output.",
            "Algebra operators return new sets; `|=`, `&=`, `-=` and `^=` "
            "mutate in place.",
            "Use `<=`, `>=`, `isdisjoint` and `==` to express relations "
            "instead of loop chains.",
            "`discard` ignores missing elements; `remove` raises KeyError.",
            "Never mutate a set while iterating it - iterate a snapshot or "
            "rebuild with a comprehension.",
            "frozenset is set's hashable form, for sets inside sets and dict "
            "keys.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "Read the set-method table in the docs: which methods return new "
            "sets and which return None?",
            "Compare `set.add` against `list.append` timing for 10^5 inserts, "
            "then for membership probes.",
            "Investigate `collections.Counter.most_common` as the counting "
            "cousin of the seen-set.",
            "Explore why dict preserves insertion order in CPython while set "
            "does not (PEP 468 and the dict's combined table).",
            "Prove `a ^ b == (a | b) - (a & b)` with two random sets and then "
            "on paper.",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Deduplicate sensor tags with a set",
        difficulty="MEDIUM",
        learning_objectives=["Convert a list to a set for dedup.", "Recover a deterministic order."],
        concepts_tested=["set construction", "deduplication", "sorted output"],
        problem_statement=(
            "Write `unique_tags(tags)` returning the distinct tags sorted "
            "alphabetically. The input list must be unchanged."
        ),
        requirements=["Use a set internally.", "Return a sorted list."],
        constraints=["Do not use a manual seen-list loop."],
        input_description="A list of strings, possibly with duplicates.",
        expected_output="A sorted list of distinct tags.",
        example_input="unique_tags(['warn', 'fault', 'warn'])",
        example_output="['fault', 'warn']",
        edge_cases=[
            "An empty input returns [].",
            "An all-duplicates input returns one element.",
            "Sorting is by normal string order.",
        ],
        hints=["set(tags) then sorted()."],
        success_criteria=["The example matches.", "Input list is unchanged."],
        optional_extension="Return first-seen order instead using the seen-set idiom.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Check whether all required keys were supplied",
        difficulty="MEDIUM",
        learning_objectives=["Express containment with subset relations.", "Report what is missing."],
        concepts_tested=["subset", "difference", "validation"],
        problem_statement=(
            "Write `check_keys(supplied, required)` returning `(ok, missing)` "
            "where ok is True only when every required key is present, and "
            "missing is the sorted list of absent keys."
        ),
        requirements=["Use set comparison, not a chain of `in` checks.", "missing must be sorted."],
        constraints=["No loops over required other than what the algebra does internally."],
        input_description="Two iterables of string keys.",
        expected_output="(bool, sorted list of missing keys).",
        example_input="check_keys(['host'], ['host', 'port'])",
        example_output="(False, ['port'])",
        edge_cases=[
            "Exact match gives (True, []).",
            "Extra supplied keys do not fail the check.",
            "Empty required always passes.",
        ],
        hints=["required - supplied is exactly the missing set."],
        success_criteria=["The example matches.", "Extra keys never cause failure."],
        optional_extension="Also return the sorted unexpected keys as a third element.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Find codes present in both subsystems",
        difficulty="MEDIUM",
        learning_objectives=["Compute set intersections.", "Return sorted results."],
        concepts_tested=["intersection", "set conversion", "sorted"],
        problem_statement=(
            "Write `common_faults(a, b)` returning the sorted list of fault "
            "codes reported by BOTH subsystems."
        ),
        requirements=["Use `&` or intersection().", "Return a sorted list."],
        constraints=["Do not nest membership loops."],
        input_description="Two iterables of fault-code strings.",
        expected_output="A sorted list of shared codes.",
        example_input="common_faults(['E1', 'E2'], ['E2', 'E3'])",
        example_output="['E2']",
        edge_cases=[
            "Disjoint inputs return [].",
            "Duplicates within one input do not duplicate output.",
        ],
        hints=["set(a) & set(b), then sorted()."],
        success_criteria=["The example matches.", "No O(n*m) loop is used."],
        optional_extension="Return the count of shared codes as well.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Remove every occurrence of blacklisted values",
        difficulty="MEDIUM",
        learning_objectives=["Use difference for bulk removal.", "Keep original order."],
        concepts_tested=["difference", "list comprehension with membership", "order preservation"],
        problem_statement=(
            "Write `strip_blacklist(values, blacklist)` returning a list "
            "containing only values NOT in the blacklist, preserving the "
            "original order."
        ),
        requirements=["Membership test must be O(1) via a set.", "Preserve input order."],
        constraints=["The input list must be unchanged."],
        input_description="A list of values and an iterable of blacklisted values.",
        expected_output="A filtered list in original order.",
        example_input="strip_blacklist([1, 2, 3, 4], [2, 4])",
        example_output="[1, 3]",
        edge_cases=[
            "An empty blacklist returns a copy of the input.",
            "An empty input returns [].",
        ],
        hints=["Convert the blacklist to a set once, then filter with a comprehension."],
        success_criteria=["The example matches.", "The membership test is against a set, not a list."],
        optional_extension="Report how many values were stripped.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Detect duplicate frames in O(n)",
        difficulty="MEDIUM",
        learning_objectives=["Apply the seen-set idiom.", "Return duplicates separately."],
        concepts_tested=["seen set", "linear scan", "order preservation"],
        problem_statement=(
            "Write `find_duplicates(frames)` returning `(unique_in_order, "
            "duplicates)` where unique_in_order keeps first occurrences and "
            "duplicates lists later repeats in the order they were seen."
        ),
        requirements=["Single pass with a set.", "Both outputs are lists in encounter order."],
        constraints=["No `x not in list` membership scans."],
        input_description="A list of hashable frames (e.g. tuples).",
        expected_output="(unique list, duplicates list).",
        example_input="find_duplicates([('a', 1), ('b', 2), ('a', 1)])",
        example_output="([('a', 1), ('b', 2)], [('a', 1)])",
        edge_cases=[
            "No duplicates gives ([], []) as duplicates and the full input as unique.",
            "Triplicates append twice to duplicates.",
            "An empty input gives ([], []).",
        ],
        hints=["One set for membership, one list for unique order, one for repeats."],
        success_criteria=["The example matches.", "Lengths satisfy len(unique) + len(duplicates) == len(input)."],
        optional_extension="Return a dict of frame -> occurrence count instead.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Compute a coverage report with set algebra",
        difficulty="HARD",
        learning_objectives=["Combine three set operations in one pass.", "Explain a derived metric."],
        concepts_tested=["union", "difference", "coverage ratio"],
        problem_statement=(
            "Write `coverage(planned, executed)` returning a dict with keys "
            "'missing' (planned - executed, sorted), 'unexpected' (executed - "
            "planned, sorted) and 'ratio' (len(planned & executed) / "
            "max(len(planned), 1) rounded to 2 dp)."
        ),
        requirements=["All three keys always present.", "Ratio is a float rounded to 2 dp."],
        constraints=["Sets only for the comparisons - no nested loops."],
        input_description="Two iterables of waypoint ids.",
        expected_output="A dict with missing, unexpected and ratio.",
        example_input="coverage(['w1', 'w2'], ['w2', 'w3'])",
        example_output="{'missing': ['w1'], 'unexpected': ['w3'], 'ratio': 0.5}",
        edge_cases=[
            "Empty planned gives ratio 0.0 with empty lists.",
            "Exact match gives empty lists and ratio 1.0.",
        ],
        hints=["Convert both first; ratio uses the intersection over planned count."],
        success_criteria=["The example matches exactly (key order not required).", "All three keys present in every case."],
        optional_extension="Add 'extra_ratio' = len(executed - planned) / max(len(executed), 1).",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Group anagram signatures into sets",
        difficulty="HARD",
        learning_objectives=["Derive hashable signatures.", "Group by a computed key."],
        concepts_tested=["set signatures", "default grouping", "sorted keys"],
        problem_statement=(
            "Write `group_anagrams(words)` returning a dict mapping each "
            "anagram signature - the frozenset of its letters - to the sorted "
            "list of words sharing it. Only words with the same letter "
            "multiset share a signature."
        ),
        requirements=["Keys are frozensets of characters.", "Word lists are sorted.", "Single pass over words."],
        constraints=["Use letter counts (sorted string would also work) but keys must be frozensets as specified."],
        input_description="A list of lowercase words.",
        expected_output="A dict of frozenset -> sorted list.",
        example_input="group_anagrams(['bat', 'tab', 'cat'])",
        example_output="{frozenset('abt'): ['bat', 'tab'], frozenset('act'): ['cat']}",
        edge_cases=[
            "An empty input gives an empty dict.",
            "A single word maps to a one-element list.",
            "Duplicate words appear once per occurrence.",
        ],
        hints=["Counter(word) is a dict; freeze it - or use tuple(sorted(word)) as the group, then wrap as frozenset."],
        success_criteria=["The example matches when printed with sorted(...).", "Keys are frozenset instances."],
        optional_extension="Sort groups by their first word for stable reporting.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Find the first value present in exactly one of two streams",
        difficulty="HARD",
        learning_objectives=["Use symmetric difference in arrival order.", "Handle ties by position."],
        concepts_tested=["symmetric difference", "order recovery", "index mapping"],
        problem_statement=(
            "Write `first_exclusive(a, b)` returning the first value in `a` "
            "that is absent from `b`, or the first value in `b` absent from "
            "a, whichever occurs EARLIER in its own stream; ties go to `a`. "
            "Return None when the streams are equal as sets."
        ),
        requirements=["Use set membership for the absent tests.", "Respect arrival order within each stream."],
        constraints=["Do not compute list difference with nested loops."],
        input_description="Two lists of hashable values.",
        expected_output="The chosen value or None.",
        example_input="first_exclusive([1, 2, 3], [3, 4])",
        example_output="1",
        edge_cases=[
            "Equal sets return None even if orders differ.",
            "Only b has exclusives -> returns b's first exclusive.",
            "Empty inputs behave consistently (None if both empty).",
        ],
        hints=["Compute a - b and b - a as sets for the None test, but pick positions by scanning each original list."],
        success_criteria=["The example matches.", "Equal sets in different orders return None."],
        optional_extension="Return (value, 'a'|'b') naming the stream.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Maintain a rolling window of distinct values",
        difficulty="HARD",
        learning_objectives=["Recompute a set per window.", "Handle windows larger than the data."],
        concepts_tested=["windowing", "set per slice", "counting distinct"],
        problem_statement=(
            "Write `distinct_counts(values, size)` returning a list with one "
            "entry per sliding window: the number of DISTINCT values in that "
            "window. Windows start at every index while a full window fits."
        ),
        requirements=["One count per window, in order.", "Use a set per window."],
        constraints=["No counting dictionaries; sets only."],
        input_description="A list of hashable values and a positive int size.",
        expected_output="A list of ints.",
        example_input="distinct_counts([1, 2, 1, 3], 2)",
        example_output="[2, 2, 2]",
        edge_cases=[
            "size > len(values) returns [].",
            "size == 1 returns one count per element (always 1).",
            "All-identical windows count 1.",
        ],
        hints=["Slice each window with values[i:i+size] and len(set(window))."],
        success_criteria=["The example matches.", "len(output) == max(0, len(values) - size + 1)."],
        optional_extension="Report the value with the maximum distinct count, ties to the earliest window.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Implement set algebra without the operators",
        difficulty="HARD",
        learning_objectives=["Rebuild union/intersection/difference manually.", "Compare complexity honestly."],
        concepts_tested=["set semantics", "membership loops", "complexity reasoning"],
        problem_statement=(
            "Write `my_union(a, b)`, `my_intersection(a, b)` and "
            "`my_difference(a, b)` returning NEW sets computed WITHOUT using "
            "|, &, -, or the corresponding methods - only loops, `in`, and "
            "set literal construction."
        ),
        requirements=["Return new sets; inputs unchanged.", "Each result equals the operator version."],
        constraints=["Do not call set.union/intersection/difference or use |, &, -."],
        input_description="Two sets.",
        expected_output="The computed set.",
        example_input="my_union({1, 2}, {2, 3})",
        example_output="{1, 2, 3}",
        edge_cases=[
            "Union preserves uniqueness by construction of a set.",
            "Intersection with disjoint inputs returns set().",
            "Difference is order-independent and non-commutative.",
        ],
        hints=["Loop over one side testing membership in the other; loop over both for union."],
        success_criteria=["assert my_union(x, y) == x | y holds for five random pairs.", "Inputs are unmodified."],
        optional_extension="Implement my_symmetric_difference and prove a ^ b == (a - b) | (b - a).",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "def unique_tags(tags):\n"
            "    \"\"\"Distinct tags, sorted; input untouched.\"\"\"\n"
            "    return sorted(set(tags))"
        ),
        explanation=(
            "set(tags) collapses duplicates in one O(n) pass because "
            "uniqueness is the type's construction semantics, not a filter "
            "applied afterward. sorted() then restores the deterministic order "
            "the set never stored - required for logs and snapshot tests."
        ),
        complexity="Time O(n log n) dominated by the sort; space O(n).",
        edge_cases="Empty input returns []. All-duplicates input yields one element.",
        alternative_approaches="dict.fromkeys(tags) keeps first-seen order without a sort - a useful alternative to name.",
        testing=(
            "assert unique_tags(['warn', 'fault', 'warn']) == ['fault', 'warn']\n"
            "src = ['a', 'a']\n"
            "unique_tags(src)\n"
            "assert src == ['a', 'a']"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def check_keys(supplied, required):\n"
            "    \"\"\"(ok, missing) - ok iff every required key is present.\"\"\"\n"
            "    required, supplied = set(required), set(supplied)\n"
            "    missing = sorted(required - supplied)\n"
            "    return (not missing), missing"
        ),
        explanation=(
            "The difference `required - supplied` IS the definition of missing, "
            "so the boolean and the report come from one computation - there is "
            "no separate loop that could disagree with it. Converting both "
            "sides also means callers may pass lists or sets interchangeably."
        ),
        complexity="Time O(n + m) expected; space O(n + m).",
        edge_cases="Exact match gives (True, []). Extra supplied keys never fail. Empty required passes.",
        alternative_approaches="required <= supplied is the boolean in one operator, but then missing needs the difference anyway.",
        testing=(
            "assert check_keys(['host'], ['host', 'port']) == (False, ['port'])\n"
            "assert check_keys(['a', 'b'], ['a']) == (True, [])\n"
            "assert check_keys([], []) == (True, [])"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "def common_faults(a, b):\n"
            "    \"\"\"Sorted fault codes reported by both subsystems.\"\"\"\n"
            "    return sorted(set(a) & set(b))"
        ),
        explanation=(
            "Intersection is exactly the 'present in both' relation, computed "
            "by walking the smaller operand against a hash table of the larger "
            "- linear rather than the quadratic pair of nested membership "
            "loops it replaces. Sorting happens once, at the end, because set "
            "order is not stored."
        ),
        complexity="Time O((n + m) + k log k) where k is the overlap size; space O(n + m).",
        edge_cases="Disjoint inputs return []. Duplicates within an input never duplicate output.",
        alternative_approaches="sorted(c for c in a if c in set(b)) works but scans and rebuilds without deduping a.",
        testing=(
            "assert common_faults(['E1', 'E2'], ['E2', 'E3']) == ['E2']\n"
            "assert common_faults(['E1'], ['E2']) == []"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "def strip_blacklist(values, blacklist):\n"
            "    \"\"\"Filter blacklisted values, preserving order.\"\"\"\n"
            "    blocked = set(blacklist)          # one O(m) conversion\n"
            "    return [v for v in values if v not in blocked]"
        ),
        explanation=(
            "Converting the blacklist once upgrades every membership test from "
            "a linear scan to a hash lookup, so the whole filter is O(n + m) "
            "instead of O(n * m). The comprehension walks the input in order, "
            "so sequence is preserved - something set difference alone could "
            "not promise."
        ),
        complexity="Time O(n + m) expected; space O(m) for the set plus the output.",
        edge_cases="Empty blacklist returns a copy of the input. Empty input returns [].",
        alternative_approaches="list(set(values) - blocked) dedupes too, which changes semantics - order and duplicates are lost.",
        testing=(
            "assert strip_blacklist([1, 2, 3, 4], [2, 4]) == [1, 3]\n"
            "src = [1, 2]\n"
            "strip_blacklist(src, [1])\n"
            "assert src == [1, 2]"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "def find_duplicates(frames):\n"
            "    \"\"\"(unique in first-seen order, later repeats in order seen).\"\"\"\n"
            "    seen = set()\n"
            "    unique, duplicates = [], []\n"
            "    for frame in frames:\n"
            "        if frame in seen:\n"
            "            duplicates.append(frame)\n"
            "        else:\n"
            "            seen.add(frame)\n"
            "            unique.append(frame)\n"
            "    return unique, duplicates"
        ),
        explanation=(
            "One set answers presence, two lists record the two outcomes in "
            "encounter order - the partition invariant len(unique) + "
            "len(duplicates) == len(frames) holds by construction because every "
            "frame takes exactly one branch."
        ),
        complexity="Time O(n) expected; space O(n).",
        edge_cases="No duplicates gives ([], duplicates). Triplicates append twice. Empty input gives ([], []).",
        alternative_approaches="collections.Counter(frames) then filtering counts > 1 loses encounter order of repeats.",
        testing=(
            "u, d = find_duplicates([('a', 1), ('b', 2), ('a', 1)])\n"
            "assert u == [('a', 1), ('b', 2)] and d == [('a', 1)]\n"
            "u, d = find_duplicates([])\n"
            "assert u == [] and d == []"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "def coverage(planned, executed):\n"
            "    \"\"\"missing, unexpected and executed-coverage ratio.\"\"\"\n"
            "    planned, executed = set(planned), set(executed)\n"
            "    shared = len(planned & executed)\n"
            "    ratio = round(shared / max(len(planned), 1), 2)\n"
            "    return {\n"
            "        'missing': sorted(planned - executed),\n"
            "        'unexpected': sorted(executed - planned),\n"
            "        'ratio': ratio,\n"
            "    }"
        ),
        explanation=(
            "Three algebra expressions answer the three report questions from "
            "one pair of sets. max(len(planned), 1) is the guard that keeps an "
            "empty plan from dividing by zero - and it deliberately reports "
            "0.0 rather than claiming full coverage of nothing."
        ),
        complexity="Time O(n + m + k log k); space O(n + m).",
        edge_cases="Empty planned gives ratio 0.0. Exact match gives ([], [], 1.0).",
        alternative_approaches="Manual counting loops would rebuild what &, - already express in one readable operator each.",
        testing=(
            "out = coverage(['w1', 'w2'], ['w2', 'w3'])\n"
            "assert out == {'missing': ['w1'], 'unexpected': ['w3'], 'ratio': 0.5}\n"
            "assert coverage([], [])['ratio'] == 0.0\n"
            "assert coverage(['a'], ['a'])['ratio'] == 1.0"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "def group_anagrams(words):\n"
            "    \"\"\"frozenset of letters -> sorted words sharing that signature.\"\"\"\n"
            "    groups = {}\n"
            "    for word in words:\n"
            "        signature = frozenset(word)      # hashable group key\n"
            "        groups.setdefault(signature, []).append(word)\n"
            "    return {sig: sorted(ws) for sig, ws in groups.items()}"
        ),
        explanation=(
            "A frozenset of the word's letters is immutable and hashable, so "
            "it can be a dict key - the exact role a plain set cannot play. "
            "setdefault keeps grouping to one line, and the final dict "
            "comprehension sorts each group so the report is reproducible "
            "despite set-keyed iteration order."
        ),
        complexity="Time O(total letters * log word length) from sorting groups; space O(total letters).",
        edge_cases="Empty input gives {}. Single word maps to a one-element list.",
        alternative_approaches="tuple(sorted(word)) as key handles repeated letters more precisely than a frozenset - name this trade-off.",
        testing=(
            "out = group_anagrams(['bat', 'tab', 'cat'])\n"
            "assert out[frozenset('abt')] == ['bat', 'tab']\n"
            "assert out[frozenset('act')] == ['cat']\n"
            "assert group_anagrams([]) == {}"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "def first_exclusive(a, b):\n"
            "    \"\"\"Earliest value present in exactly one stream; ties -> a.\"\"\"\n"
            "    sa, sb = set(a), set(b)\n"
            "    if sa == sb:\n"
            "        return None\n"
            "    for value in a:\n"
            "        if value not in sb:\n"
            "            return value\n"
            "    for value in b:\n"
            "        if value not in sa:\n"
            "            return value\n"
            "    return None   # unreachable when sa != sb"
        ),
        explanation=(
            "The set equality test first collapses the 'no exclusives at all' "
            "case - including equal sets in different orders - into one line. "
            "The scans then respect arrival order within each stream, with "
            "stream a checked first so ties break to a exactly as specified; "
            "membership in the opposite set is O(1) per step."
        ),
        complexity="Time O(n + m) expected; space O(n + m).",
        edge_cases="Equal sets return None. Only-b exclusives fall to the second loop. Empty inputs handled by the equality test.",
        alternative_approaches="sorted(a - b) picks the smallest value, not the earliest - a different and wrong order semantics.",
        testing=(
            "assert first_exclusive([1, 2, 3], [3, 4]) == 1\n"
            "assert first_exclusive([5, 6], [6, 5]) is None\n"
            "assert first_exclusive([], [9]) == 9"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "def distinct_counts(values, size):\n"
            "    \"\"\"Distinct-element count per sliding window.\"\"\"\n"
            "    if size < 1:\n"
            "        raise ValueError('size must be at least 1')\n"
            "    return [\n"
            "        len(set(values[i:i + size]))\n"
            "        for i in range(len(values) - size + 1)\n"
            "        if i + size <= len(values)\n"
            "    ]"
        ),
        explanation=(
            "The range stop `len(values) - size + 1` guarantees every slice is "
            "full, so no partial window is ever counted; when size exceeds the "
            "data the range is empty and the result is []. Each window's set "
            "collapses repeats, making len() the distinct count."
        ),
        complexity="Time O(n * size) for n windows; space O(size) per window plus the output.",
        edge_cases="size > len(values) returns []. size == 1 gives all ones. All-identical windows count 1.",
        alternative_approaches="A counter dict updated incrementally is O(n) total but far more code; sets keep it obvious.",
        testing=(
            "assert distinct_counts([1, 2, 1, 3], 2) == [2, 2, 2]\n"
            "assert distinct_counts([1, 2], 5) == []\n"
            "assert distinct_counts([7, 7, 7], 1) == [1, 1, 1]"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "def my_union(a, b):\n"
            "    out = set()\n"
            "    for value in a:\n"
            "        out.add(value)\n"
            "    for value in b:\n"
            "        out.add(value)\n"
            "    return out\n"
            "\n"
            "\n"
            "def my_intersection(a, b):\n"
            "    return {v for v in a if v in b}\n"
            "\n"
            "\n"
            "def my_difference(a, b):\n"
            "    return {v for v in a if v not in b}"
        ),
        explanation=(
            "Rebuilding the algebra shows what the operators hide: union is "
            "two insertions into a fresh set (uniqueness falls out of the set "
            "itself), intersection and difference are single filters with O(1) "
            "membership probes against the other side. The complexity matches "
            "the built-ins because the built-ins are hash-table walks too."
        ),
        complexity="Union O(n + m); intersection/difference O(n) expected.",
        edge_cases="Disjoint union merges fully. Empty operands yield the other set (union) or set() (the rest).",
        alternative_approaches="Looping both sides for intersection would be O(n * m) - the hash probe is the entire point.",
        testing=(
            "for x, y in [({1, 2}, {2, 3}), (set(), {1}), ({1}, set())]:\n"
            "    assert my_union(x, y) == x | y\n"
            "    assert my_intersection(x, y) == x & y\n"
            "    assert my_difference(x, y) == x - y\n"
            "    assert x == x and y == y   # inputs untouched"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=11,
        code=(
            "import sys\n"
            "from pathlib import Path\n"
            "\n"
            "_here = Path.cwd()\n"
            "_root = next((p for p in [_here, *_here.parents] if (p / 'shared').is_dir()), None)\n"
            "if _root is not None:\n"
            "    sys.path.insert(0, str(_root))\n"
            "\n"
            "from shared.robo_x_sim import SimulatedRobot  # noqa: E402\n"
            "\n"
            "CRITICAL = {'E_STOP', 'E_BATT'}\n"
            "\n"
            "\n"
            "def supervise(robot, reports):\n"
            "    \"\"\"Fold fault reports into active state; flag criticals.\"\"\"\n"
            "    active = set()\n"
            "    for code in reports:\n"
            "        if code.startswith('C'):\n"
            "            active.discard(code[1:])     # clear directive\n"
            "        else:\n"
            "            active.add(code)\n"
            "    breached = active & CRITICAL\n"
            "    return {'active': sorted(active),\n"
            "            'critical': sorted(breached),\n"
            "            'halt': bool(breached)}"
        ),
        explanation=(
            "Fault state is a set because presence is binary and queries are "
            "hot. Clearing maps to discard (idempotent - clearing an inactive "
            "code is not an error), and the criticality question is one "
            "intersection whose truthiness becomes the halt decision - the "
            "kind of expression sets make trivial to test."
        ),
        complexity="Time O(r + c) for r reports and c critical codes; space O(active faults).",
        edge_cases="Clearing an absent code is a no-op. No active faults give halt False with empty lists.",
        alternative_approaches="A dict of code -> bool would work but stores twice the state for no query benefit.",
        testing=(
            "robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\n"
            "out = supervise(robot, ['E_BATT', 'E1', 'CE_BATT'])\n"
            "assert out['active'] == ['E1']\n"
            "assert out['halt'] is False\n"
            "assert supervise(robot, ['E_STOP'])['halt'] is True"
        ),
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="What does `type({})` produce, and why does it matter?",
        choices=[
            "dict - braces are dict display; the empty set needs set().",
            "set - braces always mean set.",
            "tuple - braces are grouping only.",
            "It is ambiguous at runtime.",
        ],
        answer=0,
        kind="conceptual",
        explanation=(
            "Brace display is shared syntax, and dict won the ambiguity, so "
            "{} builds an empty dict. Writing set() is the only correct empty "
            "set, and the mistake surfaces later as an AttributeError on add "
            "rather than at the assignment."
        ),
        reference="lesson.ipynb - Syntax",
    )
)

QUIZ.append(
    quiz(
        question="What is the average cost of `x in my_set` versus `x in my_list`?",
        choices=[
            "Both are O(1).",
            "set O(log n), list O(1).",
            "set O(n), list O(1).",
            "set O(1) average, list O(n).",
        ],
        answer=3,
        kind="reasoning",
        explanation=(
            "A set is a hash table: it hashes x and probes one slot, which is "
            "O(1) average. A list must scan element by element until it finds "
            "x or reaches the end - O(n). Inside a loop this difference is "
            "quadratic versus linear overall."
        ),
        reference="lesson.ipynb - Performance Considerations",
    )
)

QUIZ.append(
    quiz(
        question="What does `{1, 2, 3} & {2, 3, 4}` produce?",
        choices=["{1, 4}", "{2, 3}", "{1, 2, 3, 4}", "set()"],
        answer=1,
        kind="code_output",
        explanation=(
            "& is intersection: elements present in BOTH operands. Only 2 and "
            "3 appear in the two sets, so the result is {2, 3}; union would "
            "have been {1, 2, 3, 4} and difference {1} for the left operand."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="Adding to a set inside `for x in s:` raises RuntimeError. Why?",
        choices=[
            "The iterator's position becomes invalid when the set resizes.",
            "Sets cannot grow after creation.",
            "The value being added is unhashable.",
            "Iteration over a set is forbidden entirely.",
        ],
        answer=0,
        kind="debugging",
        explanation=(
            "The live iterator tracks the table's size and layout; an "
            "insertion can resize or rehash the table, making its next-slot "
            "bookkeeping meaningless, so Python guards by raising. Iterate a "
            "snapshot - set(s) - or rebuild with a comprehension instead."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="Which expression checks that two fault lists cover EXACTLY the same codes?",
        choices=[
            "set(a) <= set(b)",
            "set(a) & set(b)",
            "set(a) == set(b)",
            "sorted(a) == sorted(b)",
        ],
        answer=2,
        kind="implementation_choice",
        explanation=(
            "Set equality ignores order and duplicates, so it compares pure "
            "content - exactly the right semantics for 'same codes'. The "
            "subset check only proves one direction, intersection proves "
            "overlap, and the sorted-list version wrongly treats duplicates as "
            "meaningful."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="A supervisor must not modify a fault set while reporting on it. What is the correct pattern?",
        choices=[
            "Wrap the loop body in try/except RuntimeError.",
            "Iterate a copy with `for code in set(active):` and mutate the original.",
            "Index the set with a while loop.",
            "Convert to a tuple and append to the tuple.",
        ],
        answer=1,
        kind="robotics",
        explanation=(
            "Iterating a snapshot decouples the traversal from the structure, "
            "so adds and discards during the pass cannot invalidate it - no "
            "exception, no skipped elements. Swallowing RuntimeError would "
            "hide half-completed reports, which is worse than the crash."
        ),
        reference="lesson.ipynb - Robotics Connection",
    )
)

QUIZ.append(
    quiz(
        question="Why does `hash({'a', 'b'})` raise TypeError?",
        choices=[
            "Sets are hashable only when empty.",
            "Strings are unhashable inside sets.",
            "Sets are mutable, and mutable objects cannot have a stable hash.",
            "Sets must be sorted before hashing.",
        ],
        answer=2,
        kind="identify_error",
        explanation=(
            "A hash must stay constant while the object sits in a set or "
            "dict; a set can gain or lose elements, which would silently break "
            "every container keyed on it. frozenset is the immutable answer "
            "when you genuinely need a nested key."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="What is the result of `supplied - required` when supplied={'a','b'} and required={'a'}?",
        choices=["{'a'}", "{'b'}", "{'a', 'b'}", "set()"],
        answer=1,
        kind="code_output",
        explanation=(
            "Difference keeps elements of the LEFT operand that are absent "
            "from the right - here 'b', the surprise key that validation "
            "should report. Reverse the operands and you would get the missing "
            "side instead; direction is meaning, not detail."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="Which idiom removes duplicates from a list WHILE preserving first-seen order?",
        choices=[
            "sorted(set(xs)) - sorting is stable by value.",
            "list(set(xs)) - sets keep insertion order.",
            "One pass with a seen set plus an append to an output list.",
            "[x for x in xs if x not in xs[:xs.index(x)]]",
        ],
        answer=2,
        kind="implementation_choice",
        explanation=(
            "A set has no order to preserve, so any set-based one-liner loses "
            "arrival order. The seen-set idiom pairs O(1) membership with an "
            "append-only output list, giving uniqueness and order in one "
            "linear pass; the slice-based guard is quadratic."
        ),
        reference="lesson.ipynb - Intermediate Examples",
    )
)

QUIZ.append(
    quiz(
        question="Why is frozenset the correct key for grouping anagrams by letter-set?",
        choices=[
            "It sorts its elements automatically.",
            "It preserves insertion order.",
            "It converts strings to tuples.",
            "It is the immutable, hashable form of set, so it can be a dict key.",
        ],
        answer=3,
        kind="conceptual",
        explanation=(
            "Dict keys must be hashable, and a plain set is mutable by "
            "definition. frozenset freezes membership at construction, "
            "becoming hashable while still answering 'same letters?' by set "
            "equality - exactly the grouping relation needed."
        ),
        reference="lesson.ipynb - Intermediate Examples",
    )
)

RESEARCH = {
    "question": (
        "At what input size does converting a list to a set pay off for "
        "repeated membership testing, and does the crossover match the O(n^2) "
        "versus O(n) model?"
    ),
    "hypothesis": (
        "For small n the list scan wins (no conversion cost), but the "
        "quadratic term dominates by n around a few thousand, after which the "
        "set version pulls further ahead with every doubling."
    ),
    "experiment": [
        STEPS(
            [
                "Choose sizes n = 100, 500, 1000, 5000, 10000.",
                "For each n, run 20 membership probes against (a) the raw list "
                "and (b) a set built from it, timing each phase separately.",
                "Record both the probe time and the one-off set-construction "
                "time - the crossover depends on both.",
                "Plot probe time against n for both variants and mark where "
                "the set total (build + probes) first beats the list total.",
            ]
        ),
    ],
    "data": [
        CODE_CELL(
            "# Record your raw timings - one row per variant per run.\n"
            "# Copy real values from your actual runs; do not invent them.\n"
            "#\n"
            "# | n | variant | run | build_s | probe_s |"
        ),
    ],
    "analysis": [
        MD(
            "Fit each series to its model: list probes should grow roughly "
            "quadratically (each probe is O(n), constant probe count), set "
            "probes roughly linearly. The crossover n is where build cost "
            "amortises - report it rather than smoothing it away."
        ),
    ],
    "result": [
        MD(
            "State the measured crossover point and whether it moved when the "
            "probe count doubled. Include any size where the list won and "
            "explain it rather than dropping it."
        ),
    ],
    "interpretation": [
        MD(
            "Relate the observed curve to the complexity table: why does "
            "doubling probes double the list time but barely move the set "
            "time? Name two threats to validity - cache effects on the list "
            "scan and hash-table resizing during set build."
        ),
    ],
    "conclusion": [
        MD(
            "Give a rule of thumb for production code: below which n is a list "
            "scan acceptable, and above which a set is mandatory? Defend the "
            "numbers with your own measurements."
        ),
    ],
    "extensions": [
        "Repeat with tuple elements of increasing size to see hashing cost "
        "enter the model.",
        "Compare against dict.fromkeys(xs) membership, which preserves order.",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Fault Supervisor Core",
    "context": (
        "The rover's fault supervisor receives three event streams - raise, "
        "clear, acknowledge - and must answer 'is any critical code active?' "
        "within the 10 ms control cycle. Presence is binary, volume is high, "
        "and a linear scan per query would miss the budget."
    ),
    "mission": (
        "Implement `FaultSupervisor` with O(1) raise/clear, an O(1) critical "
        "query, and an idempotent acknowledge that never duplicates state."
    ),
    "requirements": [
        "raise_code(code) adds to active; duplicates are ignored.",
        "clear_code(code) removes if present; clearing an absent code is a "
        "no-op (use discard semantics).",
        "is_critical() reports whether active intersects the configured "
        "critical set - in O(1) expected per call or better.",
        "snapshot() returns sorted lists of active and acknowledged codes.",
        "Critical set is supplied at construction and never mutated by "
        "events.",
    ],
    "constraints": [
        "All hot-path operations O(1) expected; snapshot O(k log k).",
        "No linear scans of the active set inside raise/clear/is_critical.",
        "Standard library only.",
    ],
    "interface": "class FaultSupervisor: def raise_code(self, code: str) -> None; ...",
    "success_criteria": [
        "Raising the same code twice leaves one entry.",
        "Clearing an inactive code does not raise.",
        "is_critical() agrees with a brute-force scan on 100 random event "
        "sequences.",
        "snapshot() output is sorted and reproducible.",
    ],
    "extension": (
        "Add a per-code first-raised timestamp using a dict alongside the set, "
        "and state why the dict - not the set - must own the timestamps.",
    ),
}

MINI_PROJECT = {
    "title": "Mini-Project: Mission Anomaly Auditor",
    "brief": (
        "Audit a mission's anomaly log: deduplicate repeats, classify "
        "severity with set relations, and report coverage of expected "
        "subsystems - all in linear time."
    ),
    "scenario": (
        "After each sortie, an auditor compares the anomalies observed "
        "against the expected set, flags repeats, and checks whether any "
        "critical combination occurred. A quadratic audit on a long log is "
        "unusable, and an unordered report cannot be filed."
    ),
    "rationale": (
        "Every set skill lands in one deliverable: dedup for the log, "
        "difference and intersection for the expected-vs-actual report, "
        "relations for the critical-combination check, and explicit sorting "
        "because the filed report must be reproducible."
    ),
    "requirements": [
        "`dedupe(log)` returning (unique_in_order, repeat_count).",
        "`report(observed, expected)` returning sorted missing/unexpected "
        "lists and a rounded coverage ratio.",
        "`critical_pairs(observed)` returning sorted pairs (as tuples) from "
        "the observed set whose combination is listed critical.",
        "`file(report)` producing a reproducible string: every list sorted, "
        "keys in fixed order.",
    ],
    "constraints": [
        "Standard library only; no nested membership loops anywhere.",
        "Every membership test goes through a set.",
        "The original log list is never mutated.",
    ],
    "deliverables": [
        "`auditor.py` with the AnomalyAuditor class.",
        "`test_auditor.py` with at least twelve assertions, including one "
        "proving reproducible output across two runs with shuffled input.",
        "A README section naming the complexity of each public method.",
    ],
    "steps": [
        "Implement dedupe with the seen-set idiom; test triplicates.",
        "Implement report with difference/intersection; test the empty-plan "
        "edge case.",
        "Implement critical_pairs via combinations of the observed set; test "
        "a known pair.",
        "Implement file with sorted output; assert byte-identical output for "
        "two shuffled inputs.",
        "Add an integration test replaying a 500-line synthetic log.",
    ],
    "expected_behavior": (
        "Repeats collapse while first-seen order survives, an empty expected "
        "set reports ratio 0.0 rather than crashing, and two shuffled copies "
        "of the same log file identically."
    ),
    "acceptance": [
        "All assertions pass from a clean kernel.",
        "No `x in list` membership test appears in hot paths (verified by "
        "reading the source).",
        "file() output is byte-identical across shuffled inputs.",
        "The README states the big-O of dedupe, report and critical_pairs.",
    ],
    "extensions": [
        "Add a windowed audit: anomalies per leg of the mission, still linear.",
        "Compare runtime of the auditor against a naive nested-loop version "
        "on 100000 lines and record both curves.",
        "Extend critical_pairs to combinations of size 3 and discuss the "
        "combinatorial cost.",
    ],
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Make O(1) membership measurable, not asserted - the timing demo is "
        "the lesson's spine.",
        "Get `set()` for the empty set and sorted-before-print into habit.",
        "Show set algebra as validation logic, not as puzzle operations.",
    ],
    "misconceptions": [
        [
            "Sets remember insertion order.",
            "They do not - sort explicitly whenever output matters.",
        ],
        [
            "{} is the empty set.",
            "It is an empty dict; the empty set is set().",
        ],
        [
            "Any value can go in a set.",
            "Only hashables; lists and dicts raise TypeError.",
        ],
        [
            "Mutating during iteration just skips elements.",
            "It raises RuntimeError - the guard is deliberate.",
        ],
    ],
    "difficult_concepts": [
        "Why hashability is required but order is not stored.",
        "The mutating (|=) versus new-set (|) distinction under aliasing.",
        "Reading difference direction as meaning, not syntax.",
    ],
    "demonstrations": [
        "Time 20000 membership probes against list vs set on the projector; "
        "let the class predict the ratio first.",
        "Live: add during iteration, read the RuntimeError, then iterate a "
        "copy.",
        "Build the anagram groups with frozenset keys live to connect hashing "
        "to dict keys.",
    ],
    "discussion": [
        "When is losing order actually unacceptable - and what is the "
        "ordered, deduplicated alternative? (dict.fromkeys.)",
        "Is `try/except RuntimeError` around a mutating loop every acceptable? "
        "What would it hide?",
    ],
    "student_errors": [
        [
            "AttributeError: 'dict' object has no attribute 'add'",
            "Wrote {} instead of set()",
            "Use set() for empties; test with type()",
        ],
        [
            "TypeError: unhashable type: 'list'",
            "A list was used as a set element",
            "Convert to tuple, or keep primitives",
        ],
        [
            "Report order changes between runs",
            "Printed the set directly",
            "Wrap in sorted() at the output boundary",
        ],
    ],
    "pacing": (
        "60 min: membership timing demo (10), construction and {} trap (10), "
        "algebra and direction (15), seen-set idiom walkthrough (10), practice "
        "start (15). Algebra-heavy exercises to homework."
    ),
    "extensions": [
        "Time frozenset vs tuple as dict keys for 50000 lookups.",
        "Investigate dict.fromkeys as an order-preserving deduplicator.",
    ],
    "assessment": (
        "Exercise 5 (duplicate frames with order) and Exercise 6 (coverage "
        "report) jointly test whether students can convert prose into set "
        "relations."
    ),
    "support": (
        "Draw two overlapping circles per algebra example and shade the "
        "answer; require the drawing before the code. If direction confuses "
        "them, insist on reading `a - b` aloud as 'a without b'.",
    ),
    "extension_fast": (
        "Fast finishers prove a ^ b == (a | b) - (a & b) on ten random pairs "
        "and write the Venn argument for why it must hold.",
    ),
}

RUBRIC = {
    "artifacts": [
        ["[`exercises.ipynb`](exercises.ipynb)", "40%", "All 10 exercises with set algebra and seen-set idiom."],
        ["[`mini_project.ipynb`](mini_project.ipynb)", "25%", "AnomalyAuditor: linear, reproducible, sorted output."],
        ["[`robotics_challenge.ipynb`](robotics_challenge.ipynb)", "25%", "FaultSupervisor meets the 10 ms query budget."],
        ["[`research.ipynb`](research.ipynb)", "10%", "List-vs-set crossover measured with real timings."],
    ],
    "criteria": [
        ["Correctness", "30", "Every example, direction of difference and edge case correct."],
        ["Complexity discipline", "25", "No hot-path membership scans; complexity stated and true."],
        ["Code quality", "25", "PEP 8, docstrings, sorted output at boundaries."],
        ["Reasoning", "20", "Hashing, orderlessness and algebra justified in writing."],
    ],
    "bands": [
        ["Distinction", "85-100", "Correct, tested, clearly reasoned, production-shaped."],
        ["Merit", "70-84", "Correct with minor gaps in testing or documentation."],
        ["Pass", "50-69", "Core requirement met; edge cases or tests incomplete."],
        ["Fail", "0-49", "Core requirement not met, or the code does not run."],
    ],
    "band_details": [
        [
            "Distinction",
            "All exercises correct, reproducibility proven by shuffled-input "
            "test, and the crossover from research is quoted with numbers.",
        ],
        [
            "Merit",
            "Most exercises correct; one direction-of-difference error or a "
            "missing sort at the output boundary.",
        ],
        [
            "Pass",
            "Core algebra right, but a linear membership scan survives in a "
            "hot path or {} appears as the empty set.",
        ],
        [
            "Fail",
            "Set algebra replaced by nested loops, or mutation-during-iteration "
            "left unhandled.",
        ],
    ],
}

TOPIC = topic(
    topic_id="3.3",
    title="Sets",
    module=3,
    module_title="Core Data Structures",
    directory="03_sets",
    summary=(
        "Unordered collections of unique hashable objects: O(1) membership, "
        "set algebra as validation logic, and the traps of orderlessness, "
        "unhashable elements and mutation during iteration."
    ),
    why_it_matters=(
        "Duplicate detection, fault state, coverage reports and configuration "
        "validation all reduce to set operations, and the difference between "
        "a quadratic scan and a hash lookup is the difference between an "
        "audit that finishes and one that does not. Orderlessness is a real "
        "trade, not a defect - provided output is sorted at the boundary."
    ),
    objectives=[
        "Construct sets four ways, including set() for the empty set.",
        "State the cost of membership on a set versus a list.",
        "Apply union, intersection, difference and symmetric difference with "
        "correct direction.",
        "Express validation with subset, equality and disjoint relations.",
        "Deduplicate with a set while preserving order via the seen-set idiom.",
        "Explain why set elements must be hashable and why iteration order "
        "must not be relied upon.",
    ],
    prerequisites=["Topic 3.2 Tuples"],
    mental_model=LESSON["mental_model"],
    terminology=TERMS,
    lesson=LESSON,
    exercises=EXERCISES,
    solutions=SOLUTIONS,
    mini_project=MINI_PROJECT,
    research=RESEARCH,
    quiz_questions=QUIZ,
    robotics_challenge=CHALLENGE,
    instructor_notes=INSTRUCTOR_NOTES,
    rubric=RUBRIC,
    robo_x_milestone="M3",
    robo_x_package="robo_x.core",
)
