"""Topic 3.2 - Tuples.

Hand-authored to the Course Content Standard. The spine: a tuple is an
immutable *binding* of references - which makes it Python's record type and
its currency for keys - and the one thing it cannot promise is that its
contents are immutable too.
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
        "A tuple is an ordered, **immutable** sequence. Immutability here is a "
        "promise about the *binding*: once the tuple is created you cannot "
        "append to it, reassign an element, or remove one. That single property "
        "is what makes tuples usable as dictionary keys and set members, and it "
        "is why functions use them to return several values without inventing a "
        "class."
    ),
    MD(
        "The subtlety that matters in production code is that immutability is "
        "shallow. A tuple stores references, exactly like a list, so a tuple "
        "that contains a list is immutable in its structure but not in its "
        "data: the list inside it can still grow, shrink or be rewritten. "
        "\"The tuple changed\" is almost always this - the binding never "
        "changed, one of its referents did."
    ),
    CODE_CELL(
        "pose = (0.0, 0.0, 90.0)\n"
        "print('pose:', pose)\n"
        "\n"
        "try:\n"
        "    pose[0] = 5.0\n"
        "except TypeError as exc:\n"
        "    print('assignment rejected:', exc)\n"
        "\n"
        "record = ([1.0, 2.0], 'calibration')\n"
        "record[0].append(3.0)          # mutates the LIST inside\n"
        "print('record after append:', record)"
    ),
    MD(
        "Assignment still aliases: `alias = pose` binds a second name to one "
        "tuple. Because the tuple itself cannot change, the aliasing is "
        "harmless - but the moment a mutable object sits inside, two names "
        "once again share one object, and the list bug from Topic 3.1 returns "
        "in tuple's clothing."
    ),
    MD(
        "Tuples are also the type Python reaches for when data is a *record* - "
        "a fixed set of fields that belong together. `(name, x, y)` reads as "
        "one thing with three parts; a three-element list reads as three "
        "things that happen to be adjacent. Choosing tuple signals \"these "
        "values are a unit and will not be edited in place\", and every reader "
        "of your code gets that message for free."
    ),
]

LESSON["formal_theory"] = [
    MD(
        "The tuple supports the same sequence protocol as a list - indexing, "
        "negative indices, slicing, `len`, concatenation, repetition, "
        "membership, iteration - with every operation that would mutate "
        "removed. What it adds is **hashability**: a tuple whose every element "
        "is hashable is itself hashable, and hashability is the price of "
        "admission for dictionary keys and set elements."
    ),
    EQUATION("hashable(tuple) <=> every element is hashable   |   immutable does NOT imply deeply immutable"),
    CODE_CELL(
        "key = ('rover-01', 3)\n"
        "registry = {key: 'active'}\n"
        "print('lookup:', registry[key])\n"
        "\n"
        "try:\n"
        "    bad = ([1, 2],)          # list inside - unhashable\n"
        "    {bad}\n"
        "except TypeError as exc:\n"
        "    print('set rejected:', exc)"
    ),
    MD(
        "Two identities keep the model precise. First, tuple construction "
        "packs references; it does not copy the elements. Second, equality is "
        "by value: two tuples built separately are `==` if their elements are, "
        "even though they are different objects (and for small interned ints "
        "and short strings they may even be `is`)."
    ),
    TABLE(
        ["Property", "tuple", "list"],
        [
            ["Ordered", "yes", "yes"],
            ["Mutable elements", "no", "yes"],
            ["Hashable (when elements are)", "yes", "no"],
            ["Suitable as dict key", "yes", "no"],
            ["Method surface", "index, count", "11 mutating + sorted helpers"],
            ["Typical role", "record, key, fixed shape", "buffer, log, worklist"],
        ],
    ),
    MD(
        "Packing and unpacking are one operation seen from two sides: "
        "`point = (x, y)` packs; `x, y = point` unpacks. The left side of an "
        "unpacking assignment is always a tuple target, which is why "
        "`a, b = b, a` swaps without a temporary variable - Python evaluates "
        "the right side completely before binding, so no name is overwritten "
        "mid-swap."
    ),
]

LESSON["syntax"] = [
    MD("Construction, unpacking, and the comma that makes a one-element tuple."),
    CODE_CELL(
        "point = (3.0, 4.0)             # two elements - parentheses suffice\n"
        "single = (42,)                 # ONE element needs the trailing comma\n"
        "bare = 42,                     # parentheses are optional when packing\n"
        "empty = ()\n"
        "\n"
        "print('point :', point)\n"
        "print('single:', single, ' type:', type(single))\n"
        "print('bare  :', bare, ' empty:', empty)\n"
        "\n"
        "x, y = point                   # unpack\n"
        "print('x =', x, ' y =', y)\n"
        "x, y = y, x                    # swap via re-packing\n"
        "print('swapped:', x, y)"
    ),
    MD("The anti-pattern - treating a single-element tuple like a bare value:"),
    CODE(
        "not_a_tuple = (42)        # just an int, parentheses were grouping\n"
        "is_a_tuple = (42,)        # a tuple of one\n"
        "type(not_a_tuple)         # <class 'int'>\n"
        "type(is_a_tuple)          # <class 'tuple'>\n"
        "\n"
        "for item in (42):         # iterates the INT - TypeError\n"
        "    ...\n"
        "for item in (42,):        # iterates one item, correctly\n"
        "    ...",
        lang="text",
    ),
    WARN(
        "the missing-comma bug",
        "`coordinates = (1 2 3)` is a syntax error, but `x = (1)` silently "
        "produces an int and `d = {1, 2} (3)` does stranger things still. When "
        "a tuple seems to have \"lost\" an element, check for the forgotten "
        "comma before blaming the logic.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - a coordinate record and its unpacking.**"),
    CODE_CELL(
        "origin = (0.0, 0.0)\n"
        "target = (3.0, 4.0)\n"
        "\n"
        "dx, dy = target[0] - origin[0], target[1] - origin[1]\n"
        "print('delta:', (dx, dy))\n"
        "\n"
        "for label, value in (('dx', dx), ('dy', dy)):\n"
        "    print(f'{label} = {value}')"
    ),
    MD("**Example 2 - returning several values without a class.**"),
    CODE_CELL(
        "def bounds(values):\n"
        "    \"\"\"Return (minimum, maximum, span) of a non-empty sequence.\"\"\"\n"
        "    lo, hi = min(values), max(values)\n"
        "    return lo, hi, hi - lo        # implicitly packed into a tuple\n"
        "\n"
        "lo, hi, span = bounds([4, 1, 9, 2])\n"
        "print('lo:', lo, ' hi:', hi, ' span:', span)"
    ),
    MD("**Example 3 - tuples as dictionary keys, the capability lists have.**"),
    CODE_CELL(
        "route = {}\n"
        "route[('alpha', 'beta')] = 12.5\n"
        "route[('alpha', 'gamma')] = 8.0\n"
        "\n"
        "for (start, end), metres in sorted(route.items()):\n"
        "    print(f'{start} -> {end}: {metres} m')"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "**Named fields without a class.** Unpacking by position is clear while "
        "the shape is stable; the moment a record grows a field, positional "
        "unpacking breaks everywhere at once - the signal to reach for a "
        "namedtuple or a class."
    ),
    CODE_CELL(
        "def locate(readings):\n"
        "    best = max(readings, key=lambda r: r[1])\n"
        "    return best[0], best[1], readings.index(best)\n"
        "\n"
        "tag, value, idx = locate([('a', 0.4), ('b', 0.9), ('c', 0.7)])\n"
        "print(f'peak {tag} = {value} at index {idx}')"
    ),
    MD(
        "**Tuple comprehensions do not exist** - `(... for x in ...)` is a "
        "generator expression, not a tuple. Materialise deliberately with "
        "`tuple(...)`, and notice the memory difference: a tuple built eagerly "
        "costs exactly as much as the list would."
    ),
    CODE_CELL(
        "squares_gen = (i * i for i in range(5))      # a GENERATOR, not a tuple\n"
        "print('generator type:', type(squares_gen))\n"
        "\n"
        "squares_tup = tuple(i * i for i in range(5))  # eager materialisation\n"
        "print('tuple:', squares_tup, ' len:', len(squares_tup))\n"
        "print('walked once:', list(squares_gen))      # still full - unvisited"
    ),
    MD(
        "**Fixed-size fields favour tuples in dataclass-like returns.** "
        "`min`, `max` and `divmod` all return tuples for exactly this reason: "
        "the shape is documented, the values cannot be edited in place, and "
        "callers can unpack or index."
    ),
    CODE_CELL(
        "quotient, remainder = divmod(17, 5)\n"
        "print('divmod(17, 5):', quotient, remainder)\n"
        "\n"
        "first, *middle, last = (1, 2, 3, 4)\n"
        "print('star unpack:', first, middle, last)"
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "**A tuple that is not immutable.** The binding is fixed; the list "
        "inside it is not. This is the failure that surprises teams most, "
        "because the type checker and the `try` block both say \"immutable\" "
        "while the data changes under a log entry."
    ),
    CODE_CELL(
        "entry = ([0.4, 0.9], 'raw')\n"
        "before = entry\n"
        "entry[0].append(0.7)              # legal - mutates the inner list\n"
        "print('same entry object?', entry is before)\n"
        "print('content changed  :', entry[0])\n"
        "\n"
        "frozen = (tuple([0.4, 0.9]), 'raw')\n"
        "try:\n"
        "    frozen[0].append(0.7)\n"
        "except AttributeError as exc:\n"
        "    print('deep freeze holds:', exc)"
    ),
    MD(
        "**Hashability decides keys.** A tuple is hashable only if every "
        "element is. One list, one dict, or one set anywhere inside makes the "
        "whole tuple unhashable - and the TypeError names the inner type, "
        "which is the fastest debugging handle you have for this class of bug."
    ),
    CODE_CELL(
        "good = ('rover-01', (3.0, 4.0), 90.0)\n"
        "print('hashable:', hash(good) is not None)\n"
        "\n"
        "bad = ('rover-01', [3.0, 4.0])\n"
        "try:\n"
        "    hash(bad)\n"
        "except TypeError as exc:\n"
        "    print('unhashable:', exc)\n"
        "\n"
        "frozen_bad = ('rover-01', (3.0, 4.0))   # inner tuple: hashable again\n"
        "print('fixed by inner tuple:', hash(frozen_bad) is not None)"
    ),
    TIP(
        "freeze before keying",
        "To use structured data as a key, convert containers to tuples "
        "recursively - or store a `json.dumps(obj, sort_keys=True)` string when "
        "the structure is deep. Both trades are explicit; both are testable.",
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "**A calibration record that cannot drift.** Sensor calibration is a "
        "fixed record: offset, scale, timestamp. Returning it as a tuple makes "
        "accidental in-place edits impossible, and validating on construction "
        "catches bad data at the boundary rather than deep in a pipeline."
    ),
    CODE_CELL(
        "def make_calibration(offset, scale, timestamp):\n"
        "    \"\"\"Return a validated (offset, scale, timestamp) record.\"\"\"\n"
        "    if not isinstance(timestamp, (int, float)):\n"
        "        raise TypeError('timestamp must be numeric')\n"
        "    if scale == 0:\n"
        "        raise ValueError('scale must be non-zero')\n"
        "    return (float(offset), float(scale), float(timestamp))\n"
        "\n"
        "cal = make_calibration(0.02, 1.5, 1712000000.0)\n"
        "print('calibration:', cal)\n"
        "offset, scale, ts = cal\n"
        "print('corrected  :', round((1.0 * scale) + offset, 4))"
    ),
    BULLETS(
        [
            "The tuple's fixed shape is the function's documented contract - "
            "three fields, always in this order.",
            "Validation runs before packing, so a bad record never escapes the "
            "constructor.",
            "`float(...)` normalises types once, at the boundary, so downstream "
            "math never sees a string.",
            "Callers may unpack (`offset, scale, ts = cal`) or index "
            "(`cal[1]`) - both are stable because the shape never changes.",
        ]
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "`def make_calibration(offset, scale, timestamp):` - three scalar "
            "parameters; the tuple is built only at the return.",
            "`if not isinstance(timestamp, (int, float)):` - rejects strings "
            "before any arithmetic can fail later with a confusing TypeError.",
            "`if scale == 0:` - a zero scale would silently erase every "
            "corrected reading, so it must fail loudly here.",
            "`return (float(offset), float(scale), float(timestamp))` - one "
            "packing expression; the parentheses document the record's shape.",
            "`offset, scale, ts = cal` - unpacking is by position; if the "
            "return shape ever changed, this line is where it would break, "
            "loudly and locally.",
            "`round((1.0 * scale) + offset, 4)` - the corrected value uses "
            "both fields, proving the record carries everything a consumer "
            "needs.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - forgetting the comma on a one-element tuple.**"),
    CODE(
        "a = (42)          # int 42\n"
        "b = (42,)         # tuple of one\n"
        "c = 42,           # also a tuple of one - parentheses are optional\n"
        "print(type(a), type(b), type(c))",
        lang="text",
    ),
    MD("**Mistake 2 - expecting a tuple's contents to be immutable.**"),
    CODE(
        "config = ([1, 2], 'mode')\n"
        "config[0].append(3)     # succeeds - the LIST inside changed\n"
        "print(config)           # ([1, 2, 3], 'mode')\n"
        "\n"
        "safe = (tuple([1, 2]), 'mode')\n"
        "# safe[0].append(3)     # AttributeError: 'tuple' object has no attribute",
        lang="text",
    ),
    MD("**Mistake 3 - using a list where a key is needed.**"),
    CODE(
        "route = {}\n"
        "route[['a', 'b']] = 12     # TypeError: unhashable type: 'list'\n"
        "route[('a', 'b')] = 12     # tuples are the key type",
        lang="text",
    ),
    MD("**Mistake 4 - building a 'tuple comprehension' that is a generator.**"),
    CODE(
        "squares = (i * i for i in range(4))   # a generator object!\n"
        "print(len(squares))                   # TypeError\n"
        "squares = tuple(i * i for i in range(4))   # the tuple you meant",
        lang="text",
    ),
    MD("**Mistake 5 - unpacking the wrong number of values.**"),
    CODE(
        "point = (1, 2, 3)\n"
        "x, y = point            # ValueError: too many values to unpack\n"
        "x, y, z = point         # correct: three targets for three values\n"
        "x, *rest = point        # correct: absorb the tail",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "When a tuple is rejected as a key, print `type()` of each element - "
        "the innermost unhashable element is always the culprit, and the error "
        "message names it if you let it raise fully."
    ),
    CODE_CELL(
        "record = ('rover-01', [3.0, 4.0], 90.0)\n"
        "for i, item in enumerate(record):\n"
        "    try:\n"
        "        hash(item)\n"
        "        print(f'element {i}: {type(item).__name__} is hashable')\n"
        "    except TypeError as exc:\n"
        "        print(f'element {i}: {type(item).__name__} FAILS - {exc}')"
    ),
    MD(
        "When \"immutable\" data seems to change, capture `id()` before and "
        "after, and check whether the tuple object itself moved (it should "
        "not) or only its contents (an inner mutable did)."
    ),
    CODE_CELL(
        "entry = ([1.0], 'raw')\n"
        "before_id, before_content = id(entry), list(entry[0])\n"
        "entry[0].append(2.0)\n"
        "\n"
        "print('tuple object moved?', id(entry) != before_id)     # False\n"
        "print('contents changed ?', entry[0] != before_content)  # True\n"
        "print('diagnosis: inner list mutated, tuple binding intact')"
    ),
    NOTE(
        "Unpacking ValueError messages are exact",
        "`too many values to unpack` and `not enough values to unpack` tell you "
        "the shape on the left and right disagree - print `len()` of both "
        "sides instead of re-reading the code by eye.",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Use a tuple for records with a fixed field set; use a list for "
            "data that will grow or be reordered.",
            "Always write the trailing comma: `(x,)` - and review any `(x)` for "
            "the same reason.",
            "Return `a, b` (bare comma) from functions - it reads as multiple "
            "values and packs itself.",
            "Never rely on a tuple for deep immutability; freeze inner "
            "containers if you need real read-only data.",
            "Prefer unpacking to indexing when the shape is fixed and known - "
            "`x, y, z = record` documents the arity.",
            "Reach for `collections.namedtuple` or a dataclass before a tuple "
            "exceeds about three positional fields.",
            "Convert lists to tuples before using them as dict keys or set "
            "members, and test that conversion with `hash()`.",
            "Do not build tuples with comprehensions - use `tuple(gen)` and "
            "know you are materialising eagerly.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "Tuples are marginally smaller and faster than lists - they are "
        "allocated once with an exact size, while lists over-allocate to make "
        "appends cheap. The gap is real but small (typically 10-20% on "
        "iteration); the *architectural* win is larger: a hashable tuple can be "
        "a key, which turns a linear scan into a hash lookup."
    ),
    TABLE(
        ["Operation", "tuple", "list"],
        [
            ["iteration", "slightly faster (no over-allocation bookkeeping)", "baseline"],
            ["membership `x in t`", "O(n) - same as list", "O(n)"],
            ["as dict key", "O(1) lookup after hashing", "TypeError - not allowed"],
            ["append during build", "impossible - rebuild with + (O(n) each)", "amortised O(1)"],
            ["memory per element", "lower (exact allocation)", "higher (spare slots)"],
        ],
    ),
    CODE_CELL(
        "import sys\n"
        "\n"
        "data_list = list(range(1000))\n"
        "data_tuple = tuple(range(1000))\n"
        "\n"
        "print('list bytes  :', sys.getsizeof(data_list))\n"
        "print('tuple bytes :', sys.getsizeof(data_tuple))\n"
        "\n"
        "index = {value: i for i, value in enumerate(data_tuple)}\n"
        "print('tuple as key: index[999] =', index[999])"
    ),
    MD(
        "One pattern genuinely is quadratic with tuples: accumulating with "
        "`acc = acc + (item,)` inside a loop recopies the whole tuple every "
        "pass. If you are building a sequence incrementally, build a list and "
        "`tuple()` it once at the end - that is the idiom in standard-library "
        "code for exactly this reason."
    ),
    CODE_CELL(
        "import time\n"
        "\n"
        "n = 8000\n"
        "start = time.perf_counter()\n"
        "acc_t = ()\n"
        "for i in range(n):\n"
        "    acc_t = acc_t + (i,)          # recopies every pass\n"
        "t_concat = time.perf_counter() - start\n"
        "\n"
        "start = time.perf_counter()\n"
        "acc_l = []\n"
        "for i in range(n):\n"
        "    acc_l.append(i)\n"
        "acc_t2 = tuple(acc_l)            # one materialisation at the end\n"
        "t_list = time.perf_counter() - start\n"
        "\n"
        "print(f'tuple += {t_concat:.4f}s vs list+tuple() {t_list:.4f}s')\n"
        "print('equal result?', acc_t == acc_t2)"
    ),
]

LESSON["pythonic_approaches"] = [
    MD(
        "Idiomatic tuple use is about *signalling*: bare-comma returns, unpacking "
        "instead of indexing, and swapping without a temporary - all of which "
        "tell the reader what the data's shape means."
    ),
    CODE_CELL(
        "def centroid(points):\n"
        "    xs = [p[0] for p in points]\n"
        "    ys = [p[1] for p in points]\n"
        "    return sum(xs) / len(xs), sum(ys) / len(ys)   # bare-comma return\n"
        "\n"
        "cx, cy = centroid([(0.0, 0.0), (3.0, 4.0)])\n"
        "print(f'centroid: ({cx:.2f}, {cy:.2f})')\n"
        "\n"
        "left, right = 'stop', 'go'       # swap - no temp variable\n"
        "left, right = right, left\n"
        "print('swapped:', left, right)"
    ),
    BULLETS(
        [
            "Return `a, b` rather than `return (a, b)` - both pack, the first "
            "reads as \"two values\".",
            "Unpack on assignment (`x, y = record`) instead of indexing when "
            "the arity is fixed.",
            "Use `_` for unpacked values you intend to ignore: `_, status = "
            "probe()`.",
            "`a, b = b, a` beats a temporary variable for swaps - Python "
            "evaluates the whole right side first.",
            "Iterate tuple fields with zip: `for name, value in zip(names, "
            "values)` pairs records without indices.",
            "Wrap a generator with `tuple(...)` explicitly when you need "
            "random access or a hashable snapshot.",
        ]
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "A pose - position and heading - is the canonical robotics record. It "
        "never grows mid-run, every subsystem needs it, and keys like "
        "`(cell_x, cell_y)` turn occupancy grids into dictionaries. Tuples are "
        "the natural currency of that data."
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
        "robot.move(2.0, speed_mps=0.5)\n"
        "\n"
        "pose = tuple(robot.status()['position'])          # (x, y) snapshot\n"
        "cell = (round(pose[0]), round(pose[1]))           # hashable grid key\n"
        "visited = {cell: 'explored'}\n"
        "\n"
        "print('pose :', pose)\n"
        "print('cell :', cell, '->', visited[cell])\n"
        "print('battery:', round(robot.status()['battery_pct'], 1), '%')"
    ),
    MD(
        "Two habits make this safe in practice. First, snapshot mutable state "
        "into a tuple at the boundary (`tuple(status['position'])`) so later "
        "simulator ticks cannot rewrite history held by the planner. Second, "
        "derive keys as tuples of primitives - `(cell_x, cell_y)` - so the "
        "visited set stays hashable no matter how the pose type evolves."
    ),
]

LESSON["engineering_example"] = [
    MD(
        "Version comparisons are tuple comparisons: Python compares sequences "
        "lexicographically, element by element, which makes `(major, minor, "
        "patch)` ordering correct with no parsing code at all - provided the "
        "numeric fields are really numeric."
    ),
    CODE_CELL(
        "def parse_version(text):\n"
        "    \"\"\"'3.12.1' -> (3, 12, 1); malformed parts raise ValueError.\"\"\"\n"
        "    parts = text.strip().split('.')\n"
        "    if len(parts) != 3:\n"
        "        raise ValueError(f'expected major.minor.patch, got {text!r}')\n"
        "    return tuple(int(p) for p in parts)\n"
        "\n"
        "current = parse_version('3.12.1')\n"
        "minimum = (3, 10, 0)\n"
        "print('current:', current, ' meets minimum?', current >= minimum)\n"
        "print('(3, 9, 99) < current?', (3, 9, 99) < current)"
    ),
    MD(
        "The tuple comparison does the work: it scans left to right and stops "
        "at the first difference, so `(3, 12, 1) >= (3, 10, 0)` is decided at "
        "the second element. The one trap is comparing across types - a string "
        "field compared against an int raises TypeError - which is exactly why "
        "`parse_version` converts every part before the tuple is built."
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Create a one-element tuple two ways - `(42,)` and `42,` - and "
            "print both types to confirm they match.",
            "Unpack a three-field record with `a, b, c = record`, then unpack "
            "again using `a, *rest` and compare the results.",
            "Use a tuple of two ints as a dictionary key and prove a list of "
            "the same values raises TypeError.",
            "Build a tuple containing a list, mutate the list, and explain "
            "using the words 'binding' and 'referent' why nothing about the "
            "tuple itself changed.",
            "Swap two names without a temporary, then time `acc = acc + (i,)` "
            "against list-append plus `tuple()` for n = 5000.",
        ]
    ),
    CODE_CELL(
        "single_a = (42,)\n"
        "single_b = 42,                 # same one-element tuple, no parens\n"
        "print('types:', type(single_a).__name__, type(single_b).__name__)\n"
        "print('equal:', single_a == single_b)\n"
        "\n"
        "record = ('alpha', 0.4, 1712000000)\n"
        "first, *rest = record\n"
        "print('first:', first, ' rest:', rest)\n"
        "\n"
        "registry = {('cell', 3): 'occupied'}\n"
        "try:\n"
        "    {['cell', 3]}\n"
        "except TypeError as exc:\n"
        "    print('list rejected:', exc)\n"
        "\n"
        "container = ([1.0], 'raw')\n"
        "container[0].append(2.0)\n"
        "print('binding intact, contents now:', container)"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: a tuple is a sealed envelope of addresses.** You "
        "cannot add, remove or rewrite what is inside the envelope's list of "
        "addresses - but if one of those addresses points at a notebook, "
        "somebody can still write in the notebook. The envelope is sealed; the "
        "notebooks it names are whatever they are."
    ),
    TABLE(
        ["Question", "Answer", "Consequence"],
        [
            ["Can I change `t[i]`?", "never - the binding is fixed", "tuple = record, key, snapshot"],
            ["Can the object at `t[i]` change?", "if it is mutable, yes", "deep-freeze before trusting it"],
            ["Is `t` hashable?", "if every element is", "usable as dict key / set member"],
            ["Does `t == u` compare identity?", "no - value equality", "records compare by content"],
            ["How do I build one incrementally?", "build a list, `tuple()` once", "avoids quadratic `+`"],
        ],
    ),
]

TERMS = [
    ["Tuple", "An ordered, immutable sequence - Python's record type."],
    ["Immutable binding", "The assignment of elements cannot change after creation."],
    ["Packing", "Gathering values into a tuple, usually via commas."],
    ["Unpacking", "Assigning tuple elements to names in one statement."],
    ["Hashable", "An object with a stable hash usable as a dict key or set member."],
    ["Shallow immutability", "The tuple is fixed but its mutable elements are not."],
    ["Record", "A fixed set of fields that logically belong together."],
    ["Sequence protocol", "Indexing, slicing, len, membership and iteration."],
    ["Lexicographic order", "Element-wise comparison that stops at the first difference."],
    ["Snapshot", "A copy of state taken at one instant, isolated from later change."],
]

LESSON["summary"] = [
    MD(
        "A tuple is an ordered sequence with a sealed binding: once created, "
        "its elements cannot be added, removed or replaced. That makes it the "
        "record type of the language - `(name, x, y)` states its own shape - "
        "and, when every element is hashable, the key type too: dictionary keys "
        "and set members are tuples' natural habitat."
    ),
    MD(
        "Immutability is shallow, which is the one fact that must survive the "
        "lesson. A tuple holding a list is fixed in structure and open in "
        "content, so 'the tuple changed' almost always means a referent did. "
        "Freeze inner containers with `tuple(...)` when genuine read-only data "
        "is required, and test it with `hash()` rather than trusting the type "
        "name."
    ),
    MD(
        "Operationally, tuples are cheap to iterate and impossible to extend - "
        "accumulate into a list and convert once, never `acc = acc + (x,)`. "
        "Unpack instead of index while the arity is fixed, switch to a "
        "namedtuple or dataclass the moment a record outgrows three fields, "
        "and snapshot mutable state into tuples at module boundaries so "
        "history cannot be rewritten under a planner's feet."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "Tuples are ordered and immutable in their binding; assignment "
            "still aliases.",
            "One element needs a comma: `(42,)` - `(42)` is just 42.",
            "Immutability is shallow: a tuple containing a list is not deeply "
            "immutable.",
            "Hashable tuples (all elements hashable) become dict keys and set "
            "members; lists cannot.",
            "Unpack by position for fixed records; index when the arity is "
            "variable.",
            "There is no tuple comprehension - `tuple(gen)` materialises "
            "eagerly.",
            "Accumulate with a list, convert once; `acc + (x,)` in a loop is "
            "quadratic.",
            "`a, b = b, a` swaps safely because the right side is fully "
            "evaluated before binding.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "Read about `collections.namedtuple` and compare it with a plain "
            "tuple at three fields and at six.",
            "Investigate why `sys.getsizeof((1, 2, 3))` beats the equivalent "
            "list - over-allocation is the answer.",
            "Time `acc = acc + (i,)` against list-append plus `tuple()` for "
            "n = 10^4, 10^5 and confirm the quadratic curve.",
            "Explore tuple equality across types: what does `(1, 2) == (1.0, "
            "2.0)` return, and why does that matter for version keys?",
            "Look up PEP 435 (enum) to see how Python formalised the "
            "'immutable record' idea.",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Normalise a coordinate tuple",
        difficulty="MEDIUM",
        learning_objectives=["Rebuild a tuple from transformed fields.", "Return records rather than mutating them."],
        concepts_tested=["tuple rebuilding", "rounding", "immutability"],
        problem_statement=(
            "Write `normalize(point)` taking an `(x, y)` tuple and returning a "
            "NEW tuple with both fields rounded to two decimals. The input must "
            "be unchanged (it cannot change, but prove you did not mutate an "
            "inner list either)."
        ),
        requirements=["Return a tuple of two floats rounded to 2 dp.", "Accept tuples of exactly two numbers."],
        constraints=["Do not convert the input to a list and back without rounding."],
        input_description="An (x, y) tuple of numbers.",
        expected_output="A new (x, y) tuple rounded to 2 decimals.",
        example_input="normalize((3.14159, 2.71828))",
        example_output="(3.14, 2.72)",
        edge_cases=[
            "Negative coordinates round correctly (-0.001 -> -0.0).",
            "Integer inputs return floats.",
            "A wrong-length tuple raises ValueError.",
        ],
        hints=["Unpack, round, and repack: return round(x, 2), round(y, 2)."],
        success_criteria=["The example matches.", "type(result) is tuple and len == 2."],
        optional_extension="Accept a third heading field and round it to 1 dp.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Swap two records without a temporary variable",
        difficulty="MEDIUM",
        learning_objectives=["Use tuple unpacking for swapping.", "Explain why the right side evaluates first."],
        concepts_tested=["unpacking", "swap", "evaluation order"],
        problem_statement=(
            "Write `swap_positions(a, b)` returning the pair `(b, a)` using "
            "tuple unpacking only - no intermediate name other than the two "
            "parameters and the return."
        ),
        requirements=["Use a single unpacking statement.", "Return a tuple."],
        constraints=["No third variable such as temp may appear."],
        input_description="Two values of any type.",
        expected_output="The pair in reversed order.",
        example_input="swap_positions(('a', 1), ('b', 2))",
        example_output="(('b', 2), ('a', 1))",
        edge_cases=[
            "Swapping identical values returns an equal pair.",
            "Works for mixed types.",
        ],
        hints=["`return b, a` is itself a packed tuple."],
        success_criteria=["The example matches.", "No local other than a and b is created."],
        optional_extension="Do it in place for a mutable two-element list instead.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Pack measurement metadata into a validated record",
        difficulty="MEDIUM",
        learning_objectives=["Validate before packing.", "Return a fixed-shape tuple contract."],
        concepts_tested=["record construction", "validation", "type coercion"],
        problem_statement=(
            "Write `make_reading(value, unit, timestamp)` returning a validated "
            "`(float value, str unit, float timestamp)` record. Raise ValueError "
            "for an empty unit and TypeError for a non-numeric timestamp."
        ),
        requirements=[
            "Coerce value and timestamp to float.",
            "Reject unit == '' with ValueError.",
            "Return exactly a 3-tuple.",
        ],
        constraints=["No third-party libraries."],
        input_description="A numeric value, a non-empty unit string, and a numeric timestamp.",
        expected_output="(float, str, float).",
        example_input="make_reading(21, 'C', 1712000000)",
        example_output="(21.0, 'C', 1712000000.0)",
        edge_cases=[
            "Bool value raises TypeError (bool subclasses int).",
            "Negative values are legal.",
            "Unit with only spaces is rejected after strip.",
        ],
        hints=["Validate first, coerce second, pack last - the constructor pattern."],
        success_criteria=["The example matches.", "Both error paths raise the specified exceptions."],
        optional_extension="Default timestamp to time.time() when omitted.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Unpack a heterogeneous log record safely",
        difficulty="MEDIUM",
        learning_objectives=["Unpack fixed-arity records.", "Ignore fields intentionally with _."],
        concepts_tested=["unpacking", "star unpacking", "sentinel names"],
        problem_statement=(
            "Write `summarise(record)` where record is `(tag, value, unit, "
            "timestamp)`. Return `(tag, total)` where total is value * 1000 if "
            "unit is 'm' else value unchanged, discarding the other fields with "
            "explicit `_` targets."
        ),
        requirements=["Use one unpacking statement with _ for unused fields.", "Return a 2-tuple."],
        constraints=["Do not index the record with [0], [1]."],
        input_description="A 4-tuple (str, float, str, float).",
        expected_output="(tag, possibly-scaled value).",
        example_input="summarise(('depth', 2.5, 'm', 1712000000.0))",
        example_output="('depth', 2500.0)",
        edge_cases=[
            "unit 's' returns the value unchanged.",
            "Value zero scales to zero.",
        ],
        hints=["tag, val, unit, _ = record then scale conditionally."],
        success_criteria=["The example matches.", "No positional indexing is used."],
        optional_extension="Accept records of length 3 by defaulting the timestamp.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Build an index from coordinate tuples",
        difficulty="MEDIUM",
        learning_objectives=["Use tuples as dictionary keys.", "Detect duplicate keys."],
        concepts_tested=["hashable keys", "dict from pairs", "duplicate detection"],
        problem_statement=(
            "Write `build_index(cells)` taking a list of `((x, y), label)` "
            "pairs and returning a dict mapping each coordinate tuple to its "
            "label. A duplicate coordinate must raise ValueError rather than "
            "silently overwrite."
        ),
        requirements=["Use the coordinate tuple directly as the key.", "Raise ValueError on duplicates."],
        constraints=["Do not convert the key to a string."],
        input_description="A list of ((x, y), label) tuples.",
        expected_output="A dict keyed by coordinate tuples.",
        example_input="build_index([((0, 0), 'free'), ((1, 0), 'wall')])",
        example_output="{(0, 0): 'free', (1, 0): 'wall'}",
        edge_cases=[
            "An empty input gives an empty dict.",
            "The duplicate case names the offending coordinate in the message.",
        ],
        hints=["Check `if key in index` before assignment to catch duplicates."],
        success_criteria=["The example matches.", "Duplicate coordinates raise with the key in the message."],
        optional_extension="Return also a sorted list of coordinates for deterministic output.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Compare semantic versions as tuples",
        difficulty="HARD",
        learning_objectives=["Parse into structured tuples.", "Compare records lexicographically."],
        concepts_tested=["parsing", "lexicographic comparison", "tuple equality"],
        problem_statement=(
            "Write `meets_minimum(version, minimum)` parsing two 'major.minor.patch' "
            "strings into int tuples and returning True when version >= minimum. "
            "A malformed version (not exactly three dot-separated integers) must "
            "raise ValueError."
        ),
        requirements=["Parse both arguments.", "Compare as int tuples, not as strings.", "Raise ValueError on malformed input."],
        constraints=["No packaging or semver libraries."],
        input_description="Two version strings in major.minor.patch form.",
        expected_output="A bool.",
        example_input="meets_minimum('3.12.1', '3.10.0')",
        example_output="True",
        edge_cases=[
            "'3.9.99' < '3.10.0' - string comparison would wrongly say otherwise.",
            "A two-part version raises ValueError.",
            "Non-numeric parts such as '3.x.0' raise ValueError.",
        ],
        hints=["split('.'), int() each part, tuple() the result, then compare with >=."],
        success_criteria=["The example matches.", "The 3.9 vs 3.10 case returns True correctly."],
        optional_extension="Support a pre-release suffix like '3.12.0-rc1' by splitting it off first.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Make a nested structure hashable",
        difficulty="HARD",
        learning_objectives=["Freeze recursive structures.", "Distinguish shallow from deep immutability."],
        concepts_tested=["deep freeze", "recursion", "hashability"],
        problem_statement=(
            "Write `freeze(value)` recursively converting lists to tuples and "
            "dicts to tuples of sorted items, so the result is hashable. "
            "Scalars, tuples and frozensets pass through unchanged."
        ),
        requirements=["Return a hashable object for any nested mix of list/dict/tuple/scalar.", "Sort dict items by key before packing."],
        constraints=["Do not use json."],
        input_description="An arbitrarily nested structure of list, dict, tuple, str, int, float, bool, None.",
        expected_output="A deeply immutable, hashable equivalent.",
        example_input="freeze({'b': [1, 2], 'a': 3})",
        example_output="(('a', 3), ('b', (1, 2)))",
        edge_cases=[
            "freeze(42) is 42.",
            "An empty dict becomes ().",
            "Nested dicts inside lists are frozen at every level.",
        ],
        hints=["Recurse on isinstance checks; dict items must be sorted for a stable hash."],
        success_criteria=["hash(freeze(x)) succeeds for the example.", "freeze preserves == against a second frozen copy."],
        optional_extension="Handle sets by sorting their elements when comparable, else by hashing the frozenset.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Swap-free rotation of field order",
        difficulty="HARD",
        learning_objectives=["Rotate unpacking patterns.", "Generalise fixed-arity reshaping."],
        concepts_tested=["unpacking", "cyclic shift", "field rotation"],
        problem_statement=(
            "Write `rotate_fields(record, k)` rotating an n-field tuple right by "
            "k using unpacking and concatenation - for 3-field records "
            "`rotate_fields(('a','b','c'), 1)` yields `('c','a','b')`."
        ),
        requirements=["Work for any tuple length >= 1.", "Normalise k with modulo."],
        constraints=["No indexing assignment (tuples cannot mutate) and no list conversion of the whole record."],
        input_description="A tuple and an int k.",
        expected_output="A rotated tuple.",
        example_input="rotate_fields(('a', 'b', 'c'), 1)",
        example_output="('c', 'a', 'b')",
        edge_cases=[
            "k = 0 returns an equal tuple.",
            "A 1-field tuple always returns itself.",
            "Negative k rotates left.",
        ],
        hints=["Slicing works on tuples: record[-k:] + record[:-k]."],
        success_criteria=["The example matches.", "The result is always a tuple."],
        optional_extension="Implement it with star-unpacking: `last, *head = record` then rebuild.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Group readings into (min, max, mean) summary tuples",
        difficulty="HARD",
        learning_objectives=["Emit fixed-shape tuples from aggregation.", "Handle empty groups explicitly."],
        concepts_tested=["aggregation", "record emission", "empty input"],
        problem_statement=(
            "Write `summarise_groups(groups)` taking a list of numeric groups "
            "and returning a list of `(min, max, mean)` tuples in the same "
            "order. An empty group yields `(0.0, 0.0, 0.0)` rather than raising."
        ),
        requirements=["One summary tuple per group, order preserved.", "All three fields are floats."],
        constraints=["Do not mutate the input groups."],
        input_description="A list of lists of numbers.",
        expected_output="A list of (min, max, mean) tuples.",
        example_input="summarise_groups([[1, 2, 3], []])",
        example_output="[(1, 3, 2.0), (0.0, 0.0, 0.0)]",
        edge_cases=[
            "A single-element group gives (x, x, x).",
            "Negative values summarise correctly.",
            "An empty outer list returns [].",
        ],
        hints=["Early-return the zero tuple when a group is empty; use min/max/sum."],
        success_criteria=["The example matches.", "Return type is list[tuple[float, float, float]]."],
        optional_extension="Also return the count as a fourth field.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Diff two record streams field by field",
        difficulty="HARD",
        learning_objectives=["Zip records for comparison.", "Report the first differing field by name."],
        concepts_tested=["zip", "field-wise diff", "named reporting"],
        problem_statement=(
            "Write `first_difference(a, b, fields)` comparing two equal-length "
            "tuples field by field against a tuple of field names, returning "
            "`(field_name, value_a, value_b)` for the FIRST difference, or None "
            "when the records are equal. Values compare with `!=`."
        ),
        requirements=["Stop at the first difference.", "Return None when all fields are equal.", "Raise ValueError when lengths disagree."],
        constraints=["Do not compare the whole tuples with == alone - the field name is required."],
        input_description="Two tuples of equal length and a tuple of field-name strings of the same length.",
        expected_output="A 3-tuple or None.",
        example_input="first_difference((1.0, 'm'), (2.0, 'm'), ('value', 'unit'))",
        example_output="('value', 1.0, 2.0)",
        edge_cases=[
            "Equal records return None.",
            "A difference in the LAST field is still reported.",
            "Mismatched lengths raise ValueError.",
        ],
        hints=["zip(a, b, fields) aligns all three - loop and return on the first !=."],
        success_criteria=["The example matches.", "A last-field difference is found before returning None."],
        optional_extension="Return ALL differences as a list instead of the first.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "def normalize(point):\n"
            "    \"\"\"Return (x, y) rounded to 2 decimals as a new tuple.\"\"\"\n"
            "    if len(point) != 2:\n"
            "        raise ValueError('expected an (x, y) pair')\n"
            "    x, y = point\n"
            "    return (round(float(x), 2), round(float(y), 2))"
        ),
        explanation=(
            "Unpack, coerce, round, repack - every step produces a new value, "
            "so nothing about the original record can change. Validating the "
            "arity first means a caller passing a 3-tuple gets a precise error "
            "instead of silently ignoring the third field."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="Integer inputs become floats. Wrong-length tuples raise ValueError.",
        alternative_approaches="A comprehension over the pair is shorter but loses the named x, y clarity.",
        testing=(
            "assert normalize((3.14159, 2.71828)) == (3.14, 2.72)\n"
            "assert normalize((1, 2)) == (1.0, 2.0)\n"
            "try:\n"
            "    normalize((1, 2, 3))\n"
            "    raise AssertionError('should raise')\n"
            "except ValueError:\n"
            "    pass"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def swap_positions(a, b):\n"
            "    \"\"\"Return the pair reversed, without a temporary.\"\"\"\n"
            "    return b, a"
        ),
        explanation=(
            "`return b, a` packs the two names into a fresh tuple in one step. "
            "The same unpacking trick `a, b = b, a` works in place because "
            "Python evaluates the entire right-hand side - producing (b, a) - "
            "before binding any name on the left, so nothing is clobbered "
            "mid-swap."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="Identical values return an equal pair; mixed types are unaffected.",
        alternative_approaches="A temp variable works but adds a line and a name for no benefit.",
        testing=(
            "assert swap_positions(('a', 1), ('b', 2)) == (('b', 2), ('a', 1))\n"
            "assert swap_positions(0, 0) == (0, 0)"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "def make_reading(value, unit, timestamp):\n"
            "    \"\"\"Validate, coerce, and pack a (float, str, float) record.\"\"\"\n"
            "    if isinstance(value, bool) or not isinstance(value, (int, float)):\n"
            "        raise TypeError('value must be numeric')\n"
            "    if not unit or not unit.strip():\n"
            "        raise ValueError('unit must be non-empty')\n"
            "    if isinstance(timestamp, bool) or not isinstance(timestamp, (int, float)):\n"
            "        raise TypeError('timestamp must be numeric')\n"
            "    return (float(value), unit.strip(), float(timestamp))"
        ),
        explanation=(
            "Validation runs before coercion so the TypeError and ValueError "
            "messages name the caller's actual mistake rather than a float() "
            "conversion failure. The bool guard precedes the numeric check for "
            "the same reason as in Topic 3.1 - bool subclasses int, and a True "
            "slipping through would silently read as 1.0."
        ),
        complexity="Time O(len(unit)); space O(len(unit)).",
        edge_cases="Empty and whitespace-only units raise. Negative values are legal.",
        alternative_approaches="A dataclass with __post_init__ scales to more fields but is heavyweight at three.",
        testing=(
            "assert make_reading(21, 'C', 1712000000) == (21.0, 'C', 1712000000.0)\n"
            "try:\n"
            "    make_reading(1, '', 0)\n"
            "    raise AssertionError('should raise')\n"
            "except ValueError:\n"
            "    pass"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "def summarise(record):\n"
            "    \"\"\"Scale metres to millimetres; discard unit and timestamp.\"\"\"\n"
            "    tag, value, unit, _timestamp = record\n"
            "    scaled = value * 1000.0 if unit == 'm' else float(value)\n"
            "    return tag, scaled"
        ),
        explanation=(
            "One unpacking statement with an explicit `_timestamp` target "
            "documents exactly which fields matter; the reader never has to "
            "count brackets. The conditional scales only metres, and returning "
            "a bare `tag, scaled` packs the promised two-tuple."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="value 0 scales to 0.0. Non-'m' units pass through unchanged.",
        alternative_approaches="record[1] * 1000 works but hides which field is which - the very cost unpacking removes.",
        testing=(
            "assert summarise(('depth', 2.5, 'm', 1712000000.0)) == ('depth', 2500.0)\n"
            "assert summarise(('time', 5.0, 's', 0)) == ('time', 5.0)"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "def build_index(cells):\n"
            "    \"\"\"Map coordinate tuples to labels, rejecting duplicates.\"\"\"\n"
            "    index = {}\n"
            "    for coordinate, label in cells:\n"
            "        if coordinate in index:\n"
            "            raise ValueError(f'duplicate coordinate {coordinate!r}')\n"
            "        index[coordinate] = label\n"
            "    return index"
        ),
        explanation=(
            "The coordinate tuple is already hashable, so it becomes the key "
            "directly - converting it to a string would work but destroys the "
            "structure and makes later range queries impossible. Checking "
            "`in index` before assignment turns Python's silent dict "
            "overwrite-previous-value behaviour into an explicit failure."
        ),
        complexity="Time O(n) expected (hash lookups); space O(n).",
        edge_cases="Empty input returns {}. The duplicate message contains the offending key.",
        alternative_approaches="dict(pairs) is one line but cannot detect duplicates - it overwrites silently.",
        testing=(
            "idx = build_index([((0, 0), 'free'), ((1, 0), 'wall')])\n"
            "assert idx[(0, 0)] == 'free'\n"
            "try:\n"
            "    build_index([((0, 0), 'a'), ((0, 0), 'b')])\n"
            "    raise AssertionError('should raise')\n"
            "except ValueError as exc:\n"
            "    assert '(0, 0)' in str(exc)"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "def _parse(version):\n"
            "    parts = version.split('.')\n"
            "    if len(parts) != 3:\n"
            "        raise ValueError(f'expected major.minor.patch, got {version!r}')\n"
            "    try:\n"
            "        return tuple(int(p) for p in parts)\n"
            "    except ValueError as exc:\n"
            "        raise ValueError(f'non-numeric part in {version!r}') from exc\n"
            "\n"
            "\n"
            "def meets_minimum(version, minimum):\n"
            "    \"\"\"True when version >= minimum, compared numerically.\"\"\"\n"
            "    return _parse(version) >= _parse(minimum)"
        ),
        explanation=(
            "Parsing to int tuples first is the whole fix: '(3, 9, 99)' as "
            "strings would compare '9' > '10' and give the wrong answer, while "
            "the int tuple compares 9 < 10 correctly. The try/except around "
            "int() re-raises with context so the exact bad part is visible in "
            "the traceback."
        ),
        complexity="Time O(len of both strings); space O(1) beyond the 3-tuples.",
        edge_cases="'3.9.99' vs '3.10.0' returns True. Two-part or non-numeric versions raise ValueError.",
        alternative_approaches="packaging.version.parse is production-grade but hides the tuple lesson entirely.",
        testing=(
            "assert meets_minimum('3.12.1', '3.10.0') is True\n"
            "assert meets_minimum('3.9.99', '3.10.0') is False\n"
            "for bad in ('3.9', '3.x.0'):\n"
            "    try:\n"
            "        meets_minimum(bad, '1.0.0')\n"
            "        raise AssertionError('should raise')\n"
            "    except ValueError:\n"
            "        pass"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "def freeze(value):\n"
            "    \"\"\"Recursively convert lists/dicts into hashable tuples.\"\"\"\n"
            "    if isinstance(value, dict):\n"
            "        items = sorted(value.items(), key=lambda kv: repr(kv[0]))\n"
            "        return tuple((k, freeze(v)) for k, v in items)\n"
            "    if isinstance(value, list):\n"
            "        return tuple(freeze(v) for v in value)\n"
            "    if isinstance(value, (set, frozenset)):\n"
            "        return tuple(sorted((freeze(v) for v in value), key=repr))\n"
            "    return value   # scalars and tuples pass through"
        ),
        explanation=(
            "Each container type is rebuilt as a tuple of recursively frozen "
            "parts, so hashability holds at every depth - the property `hash()` "
            "actually needs. Sorting dict items by a repr key gives a stable "
            "order even for mixed key types, which plain sorted() would refuse "
            "to compare."
        ),
        complexity="Time O(n log n) from the sorts; space O(n).",
        edge_cases="Scalars pass through unchanged. Empty dict/list become ().",
        alternative_approaches="json.dumps(..., sort_keys=True) yields a hashable string but loses type fidelity.",
        testing=(
            "f = freeze({'b': [1, 2], 'a': 3})\n"
            "assert f == (('a', 3), ('b', (1, 2)))\n"
            "hash(f)\n"
            "assert freeze(42) == 42\n"
            "assert freeze({}) == ()"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "def rotate_fields(record, k):\n"
            "    \"\"\"Rotate an n-field tuple right by k.\"\"\"\n"
            "    if not record:\n"
            "        return record\n"
            "    k %= len(record)\n"
            "    if k == 0:\n"
            "        return record\n"
            "    return record[-k:] + record[:-k]"
        ),
        explanation=(
            "Slicing works on tuples exactly as on lists and concatenation "
            "builds a new tuple, so the rotation is pure functional arithmetic "
            "with no mutation possible. Modulo first makes any k - negative or "
            "oversized - safe before the slices are taken."
        ),
        complexity="Time O(n); space O(n).",
        edge_cases="Empty tuple returns itself. k = 0 returns the original object. Single field never changes.",
        alternative_approaches="Star-unpacking (last, *head = record) is elegant for k == 1 only; slicing generalises.",
        testing=(
            "assert rotate_fields(('a', 'b', 'c'), 1) == ('c', 'a', 'b')\n"
            "assert rotate_fields(('a', 'b', 'c'), 0) == ('a', 'b', 'c')\n"
            "assert rotate_fields(('a',), 5) == ('a',)"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "def summarise_groups(groups):\n"
            "    \"\"\"One (min, max, mean) tuple per group, zeros when empty.\"\"\"\n"
            "    summaries = []\n"
            "    for group in groups:\n"
            "        if not group:\n"
            "            summaries.append((0.0, 0.0, 0.0))\n"
            "            continue\n"
            "        lo, hi = min(group), max(group)\n"
            "        mean = float(sum(group)) / len(group)\n"
            "        summaries.append((float(lo), float(hi), mean))\n"
            "    return summaries"
        ),
        explanation=(
            "The empty guard runs before min/max, which would otherwise raise "
            "on an empty sequence - the documented zero tuple is a deliberate "
            "policy rather than a crash. Casting all three fields to float "
            "keeps the return type uniform even when a group holds ints."
        ),
        complexity="Time O(total elements); space O(number of groups).",
        edge_cases="Empty outer list returns []. Single-element groups give (x, x, x).",
        alternative_approaches="A comprehension with a helper function is flatter but splits the guard across scopes.",
        testing=(
            "assert summarise_groups([[1, 2, 3], []]) == [(1.0, 3.0, 2.0), (0.0, 0.0, 0.0)]\n"
            "assert summarise_groups([]) == []\n"
            "assert summarise_groups([[5]]) == [(5.0, 5.0, 5.0)]"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "def first_difference(a, b, fields):\n"
            "    \"\"\"(name, a, b) for the first mismatched field; None if equal.\"\"\"\n"
            "    if len(a) != len(b) or len(a) != len(fields):\n"
            "        raise ValueError('records and field names must align')\n"
            "    for name, va, vb in zip(fields, a, b):\n"
            "        if va != vb:\n"
            "            return (name, va, vb)\n"
            "    return None"
        ),
        explanation=(
            "zip(fields, a, b) aligns names with values in lockstep, so the "
            "report always carries the human-readable field name - something a "
            "plain `a != b` can never provide. The loop returns on the first "
            "difference, guaranteeing 'first' rather than 'any', and the "
            "explicit None return distinguishes equality from a missing result."
        ),
        complexity="Time O(k) for k fields (stops early); space O(1).",
        edge_cases="Equal records return None. A last-field difference is still caught. Length mismatch raises.",
        alternative_approaches="next(((n, x, y) for n, x, y in zip(...) if x != y), None) is a one-liner but harder to test.",
        testing=(
            "assert first_difference((1.0, 'm'), (2.0, 'm'), ('value', 'unit')) == ('value', 1.0, 2.0)\n"
            "assert first_difference((1, 'a'), (1, 'a'), ('n', 'u')) is None\n"
            "assert first_difference((1, 0), (1, 1), ('n', 'k')) == ('k', 0, 1)"
        ),
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="What is the type of `(42)` versus `(42,)`?",
        choices=[
            "Both are tuples of one element.",
            "(42) is a list; (42,) is a tuple.",
            "Both are ints - parentheses only group.",
            "(42) is an int; (42,) is a tuple.",
        ],
        answer=3,
        kind="conceptual",
        explanation=(
            "Parentheses around a single expression just group it, so (42) is "
            "the int 42. The trailing comma is what constructs the tuple - "
            "which is why the missing comma is the most common tuple bug in "
            "Python code review."
        ),
        reference="lesson.ipynb - Syntax",
    )
)

QUIZ.append(
    quiz(
        question="What happens here? `t = ([1, 2], 'x'); t[0].append(3)`",
        choices=[
            "TypeError: tuples do not support item assignment.",
            "A new tuple is created with the appended value.",
            "The inner list grows; the tuple binding itself is unchanged.",
            "The tuple is silently converted to a list.",
        ],
        answer=2,
        kind="code_output",
        explanation=(
            "Immutability covers the tuple's own slots, not the objects those "
            "slots reference. The list inside is a normal mutable object, so "
            "append succeeds and the tuple still points at the same - now "
            "longer - list."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="Why does `hash(('a', [1, 2]))` raise TypeError?",
        choices=[
            "The inner list is unhashable, and a tuple is hashable only if every element is.",
            "Strings cannot be hashed inside tuples.",
            "Tuples are never hashable.",
            "Lists are hashed first, then discarded.",
        ],
        answer=0,
        kind="reasoning",
        explanation=(
            "Hashability of a tuple is the conjunction of its elements' "
            "hashability. A list is mutable, its hash is undefined by design "
            "(mutating a key would break every dict it sits in), so the tuple "
            "inherits the rejection."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="What does `x, y = y, x` do when x=1, y=2?",
        choices=[
            "Raises NameError because y is used before assignment.",
            "Binds x=2 and y=1 - the right side packs before any left-side binding.",
            "Binds x=1 and y=1 - sequential left-to-right overwrite.",
            "Creates a tuple (2, 1) assigned only to x.",
        ],
        answer=1,
        kind="code_output",
        explanation=(
            "Python evaluates the entire right-hand side first, producing the "
            "tuple (2, 1), and only then unpacks it onto the left. No name is "
            "overwritten during evaluation, which is exactly why the swap needs "
            "no temporary variable."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="A 'tuple comprehension' `(x for x in items)` is actually:",
        choices=[
            "A tuple, built eagerly like list comprehension.",
            "A syntax error in Python 3.",
            "A generator expression; wrap it with tuple(...) to get a tuple.",
            "A frozenset comprehension.",
        ],
        answer=2,
        kind="identify_error",
        explanation=(
            "Round parentheses over a comprehension with no inner commas form a "
            "generator expression - lazy and single-pass. Only tuple(...) or "
            "the presence of a comma materialises an actual tuple, which is why "
            "len() on the generator raises."
        ),
        reference="lesson.ipynb - Intermediate Examples",
    )
)

QUIZ.append(
    quiz(
        question="Which is the correct way to accumulate items into a tuple inside a loop?",
        choices=[
            "acc.append(item) - tuples have append.",
            "acc = acc + (item,) each pass - tuples support +.",
            "acc += item - in-place add works for tuples.",
            "Build a list with append, then call tuple(acc) once after the loop.",
        ],
        answer=3,
        kind="implementation_choice",
        explanation=(
            "Tuple concatenation copies the whole accumulator every pass, "
            "making the loop quadratic, while list append is amortised O(1). "
            "The list-then-convert idiom keeps the O(n) profile and still ends "
            "with a genuine tuple; acc.append does not exist at all."
        ),
        reference="lesson.ipynb - Performance Considerations",
    )
)

QUIZ.append(
    quiz(
        question="Why are coordinate tuples preferred over lists as occupancy-grid keys?",
        choices=[
            "Tuples are hashable, so they can live in dicts and sets; lists cannot.",
            "Tuples are faster to build than lists.",
            "Tuples compare lexicographically while lists do not.",
            "Tuples use less code to index.",
        ],
        answer=0,
        kind="robotics",
        explanation=(
            "Dict keys must be hashable. A tuple of ints hashes structurally, "
            "so (cell_x, cell_y) gives O(1) lookups, while the equivalent list "
            "raises TypeError the moment it is used as a key - the entire "
            "visited-set design depends on this property."
        ),
        reference="lesson.ipynb - Robotics Connection",
    )
)

QUIZ.append(
    quiz(
        question="After `t = ((1, [2]), 3); t[0][1].append(4)`, what is `t`?",
        choices=[
            "((1, [2]), 3) - nested tuples fully protect the data.",
            "TypeError because tuples cannot nest.",
            "((1, [2, 4]), 3) - the inner list mutated through two levels.",
            "((1, (2, 4)), 3) - append converted it to a tuple.",
        ],
        answer=2,
        kind="code_output",
        explanation=(
            "Indexing walks to the inner tuple (1, [2]), then to its second "
            "element - the list - where append is perfectly legal. Neither "
            "tuple level can stop a mutation of an object they reference; only "
            "freezing the inner list itself would."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="Which version comparison is correct, and why?",
        choices=[
            "'3.9.99' >= '3.10.0' as strings, because '9' > '1'.",
            "(3, 9, 99) >= (3, 10, 0) as int tuples, because comparison stops at the first differing field numerically.",
            "Both are correct - strings and tuples compare identically.",
            "Neither; version strings must be compared with regex.",
        ],
        answer=1,
        kind="reasoning",
        explanation=(
            "String comparison sees '9' > '1' at the minor field and answers "
            "wrongly. Parsed as int tuples, Python compares 9 against 10 "
            "numerically and stops at that field, giving the lexicographic "
            "order versions actually need."
        ),
        reference="lesson.ipynb - Engineering Example",
    )
)

QUIZ.append(
    quiz(
        question="Your function must return three related values. What is the idiomatic choice?",
        choices=[
            "Return a, b, c as a bare comma tuple, or a namedtuple if fields need names.",
            "Print them separated by spaces and re-parse at the call site.",
            "Append them to a module-level list the caller reads.",
            "Return a string 'a,b,c' and split it downstream.",
        ],
        answer=0,
        kind="implementation_choice",
        explanation=(
            "Bare-comma return packs a tuple in one expression and the caller "
            "can unpack it directly. When the field count grows or names "
            "matter, a namedtuple keeps the same ergonomics while documenting "
            "each field - the string and global-list options both discard type "
            "information and invite parsing bugs."
        ),
        reference="lesson.ipynb - Best Practices",
    )
)

RESEARCH = {
    "question": (
        "Does using tuples instead of lists as dictionary keys measurably "
        "change lookup time, and how does each compare with stringified keys?"
    ),
    "hypothesis": (
        "Tuple keys are fastest for repeated lookups because they hash "
        "structurally without building a string, so they should beat "
        "str(x) + ',' + str(y) keys by a consistent margin at every size."
    ),
    "experiment": [
        STEPS(
            [
                "Generate 50000 distinct (x, y) coordinate pairs.",
                "Build three dicts: tuple-keyed, string-keyed ('x,y'), and "
                "nested dict-of-dicts.",
                "Time 50000 successful lookups in each, ten runs, recording "
                "every raw timing.",
                "Also time construction of each dict, since string keys must "
                "be formatted up front.",
            ]
        ),
    ],
    "data": [
        CODE_CELL(
            "# Record your raw timings - one row per variant per run.\n"
            "# Copy real values from your actual runs; do not invent them.\n"
            "#\n"
            "# | variant | run | construct_s | lookup_s |"
        ),
    ],
    "analysis": [
        MD(
            "Compare lookup distributions first (that is the steady-state cost) "
            "and construction separately (the up-front cost). If string keys "
            "are slower on both, the hypothesis is doubly supported; if they "
            "tie on lookup but lose on construction, say so precisely."
        ),
    ],
    "result": [
        MD(
            "State the median lookup time per variant at the largest size and "
            "the ratio between tuple and string keys. Report any run where "
            "string keys won, and consider why (interning, hash caching)."
        ),
    ],
    "interpretation": [
        MD(
            "Explain that tuple hashing recurses over elements while string "
            "hashing walks every character, and that both are cached after "
            "first computation. Name two threats to validity, including dict "
            "insertion-order effects on cache locality."
        ),
    ],
    "conclusion": [
        MD(
            "Verdict: which key type should an occupancy-grid tracker use, and "
            "does the answer change when keys are built once and read a "
            "million times versus built and discarded?"
        ),
    ],
    "extensions": [
        "Add frozenset keys for unordered features and compare their hashing cost.",
        "Measure memory with sys.getsizeof on each dict at the largest size.",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Immutable Telemetry Envelope",
    "context": (
        "Downstream analysers receive batches of telemetry. If a batch is a "
        "list, an analyser can accidentally mutate it and corrupt what every "
        "later analyser sees. The envelope must be structurally immutable and "
        "hashable so batches can themselves be deduplicated in a set."
    ),
    "mission": (
        "Implement `pack_batch(readings, mission_id)` returning a nested tuple "
        "`((value, timestamp), ...)` plus mission id, validated and frozen, "
        "with a `batch_key` suitable for set membership."
    ),
    "requirements": [
        "Return ((value, timestamp), ...) with mission_id as a 2-tuple: "
        "(mission_id, frozen_readings).",
        "Reject non-numeric values and non-monotonic timestamps with ValueError.",
        "The result must satisfy hash(result) without raising.",
        "Provide `dedupe(batches)` returning a list of unique batches in "
        "first-seen order using a set internally.",
    ],
    "constraints": [
        "No list may survive inside the returned structure.",
        "Standard library only.",
        "dedupe must be O(n) expected, not O(n^2).",
    ],
    "interface": "def pack_batch(readings, mission_id) -> tuple; def dedupe(batches) -> list",
    "success_criteria": [
        "A list input cannot be mutated through the returned envelope.",
        "Out-of-order timestamps raise with the offending index in the message.",
        "dedupe preserves first-seen order while removing exact duplicates.",
        "hash() succeeds on a packed batch.",
    ],
    "extension": (
        "Add a `verify_frozen(obj)` helper that walks an arbitrary structure "
        "and returns the path of the first mutable object it finds, then state "
        "where you would call it in a production pipeline."
    ),
}

MINI_PROJECT = {
    "title": "Mini-Project: Mission Record Store",
    "brief": (
        "Build a record store where every mission is an immutable tuple "
        "record, records are keyed by coordinate tuples, and consumers can "
        "never corrupt stored history."
    ),
    "scenario": (
        "A rover fleet logs waypoints, battery samples and event codes. "
        "Operations staff need exact historical records - a log line that "
        "changes after the fact is a compliance failure, not a bug fix."
    ),
    "rationale": (
        "The project forces every tuple skill into one design: records as "
        "tuples, tuple keys in the index, deep-freezing for nested payloads, "
        "and unpacking for reads - with hashability enabling O(1) dedupe."
    ),
    "requirements": [
        "Represent each mission as (mission_id, ((waypoint...),), started_at).",
        "Index missions by mission_id in a dict; reject duplicate ids with "
        "ValueError.",
        "Expose `waypoints(mission_id)` returning a fresh tuple each call.",
        "Provide `freeze(payload)` converting nested lists/dicts to tuples so "
        "arbitrary payloads are hashable.",
        "Provide `dedupe(events)` removing duplicate event tuples, order "
        "preserved.",
    ],
    "constraints": [
        "Standard library only.",
        "No method may return a structure containing a list or dict.",
        "All lookups O(1) expected; dedupe O(n) expected.",
    ],
    "deliverables": [
        "`record_store.py` with the MissionRecordStore class.",
        "`test_record_store.py` with at least twelve assertions, including one "
        "that proves a returned waypoint tuple cannot be mutated and one that "
        "proves hash() works on a frozen payload.",
        "A README section explaining why records are tuples and where a "
        "namedtuple would be the next step.",
    ],
    "steps": [
        "Implement record() with duplicate-id detection; test the ValueError path.",
        "Implement waypoints() returning tuple snapshots; test mutation "
        "isolation by attempting item assignment.",
        "Implement freeze() recursively; test hash() on a nested mixed payload.",
        "Add dedupe() with a seen set; test order preservation on duplicates.",
        "Write an integration test that records two missions, indexes them, "
        "and verifies both remain intact after consumer access.",
    ],
    "expected_behavior": (
        "Duplicate mission ids fail loudly, every returned waypoint structure "
        "is a tuple, frozen payloads hash without error, and dedupe keeps the "
        "first occurrence of each event tuple."
    ),
    "acceptance": [
        "All assertions pass from a clean kernel.",
        "Attempted mutation of any returned structure raises TypeError.",
        "freeze({'a': [1]}) hashes and equals freeze({'a': [1]}) for two "
        "separately built inputs.",
        "The README names the exact point at which namedtuple would replace "
        "the plain tuple.",
    ],
    "extensions": [
        "Add mission versioning: each edit appends to a tuple of versions "
        "rather than mutating the original.",
        "Time dedupe on 100000 events and confirm it stays linear.",
        "Compare tuple-key and string-key index performance on 50000 missions.",
    ],
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Establish 'immutable binding, mutable contents' as the tuple model.",
        "Make hashability concrete through dict-key failures students see live.",
        "Build the list-then-tuple() habit before students discover the "
        "quadratic accident themselves.",
    ],
    "misconceptions": [
        [
            "A tuple is deeply immutable.",
            "Only its slots are fixed; inner lists still mutate.",
        ],
        [
            "(x) is a one-element tuple.",
            "It is just x in parentheses - the comma makes the tuple.",
        ],
        [
            "Any tuple can be a dict key.",
            "Only hashable tuples - all elements hashable - qualify.",
        ],
        [
            "There is a tuple comprehension.",
            "The parentheses build a generator; tuple(...) materialises it.",
        ],
    ],
    "difficult_concepts": [
        "Why hashability follows from immutability, element by element.",
        "Evaluation order in `a, b = b, a`.",
        "When a record should graduate from tuple to namedtuple to dataclass.",
    ],
    "demonstrations": [
        "Live: t = ([1],); t[0].append(2); print(t) - watch 'immutable' data change.",
        "Live: {[1, 2]} raises TypeError, {tuple([1, 2])} succeeds.",
        "Time acc = acc + (i,) against list-append + tuple() at n = 20000.",
    ],
    "discussion": [
        "Should mission logs be tuples end-to-end, or is a frozen dataclass "
        "the professional answer? What does each cost?",
        "Where does 'immutable by convention' break down in a team codebase?",
    ],
    "student_errors": [
        [
            "TypeError: unhashable type: 'list'",
            "A list sits inside the key tuple",
            "Freeze it with tuple() or keep keys to primitives",
        ],
        [
            "Tuple 'changed' after a function ran",
            "An inner mutable was modified through an alias",
            "Deep-freeze or copy the payload at the boundary",
        ],
        [
            "Loop over a tuple raises TypeError: not iterable",
            "The value is an int, not a 1-tuple - comma missing",
            "Write (x,) or x,",
        ],
    ],
    "pacing": (
        "55 min: record model and unpacking (15), hashability live demo (10), "
        "shallow immutability trap (15), practice start (15). Performance and "
        "freeze/recursion exercises go to homework."
    ),
    "extensions": [
        "Compare sys.getsizeof tuple vs list for 1000 elements.",
        "Explore dataclasses.replace as the mutable-record escape hatch.",
    ],
    "assessment": (
        "Exercise 7 (deep freeze) and Exercise 6 (version tuples) separate "
        "students who understand hashability from those who memorised the "
        "syntax."
    ),
    "support": (
        "Use the sealed-envelope diagram: draw addresses inside an envelope "
        "and notebooks outside. If hash() still confuses it, hash three "
        "objects live and show dict[key] lookup succeeding and failing."
    ),
    "extension_fast": (
        "Fast finishers implement freeze() handling sets with sorted-by-repr "
        "elements and prove hash stability across two builds.",
    ),
}

RUBRIC = {
    "artifacts": [
        ["[`exercises.ipynb`](exercises.ipynb)", "40%", "All 10 exercises with validation and unpacking shown."],
        ["[`mini_project.ipynb`](mini_project.ipynb)", "25%", "MissionRecordStore with hashable, isolated records."],
        ["[`robotics_challenge.ipynb`](robotics_challenge.ipynb)", "25%", "Frozen envelope dedupes in O(n) and cannot be mutated."],
        ["[`research.ipynb`](research.ipynb)", "10%", "Tuple vs string key timings with a defensible verdict."],
    ],
    "criteria": [
        ["Correctness", "30", "Every example, error path and edge case behaves as specified."],
        ["Immutability reasoning", "25", "Shallow-vs-deep immutability explained and enforced in code."],
        ["Code quality", "25", "PEP 8, docstrings, validation at boundaries."],
        ["Reasoning", "20", "Hashability and quadratic accumulation justified in writing."],
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
            "All exercises correct, freeze proven by hash() assertions, and the "
            "version comparison handles the 3.9-vs-3.10 trap explicitly.",
        ],
        [
            "Merit",
            "Most exercises correct; one validation path missing or the "
            "quadratic accumulation not discussed.",
        ],
        [
            "Pass",
            "Core behaviour right but a list survives inside a returned "
            "structure, or duplicate-id detection is absent.",
        ],
        [
            "Fail",
            "Records returned as lists, or hashability never demonstrated.",
        ],
    ],
}

TOPIC = topic(
    topic_id="3.2",
    title="Tuples",
    module=3,
    module_title="Core Data Structures",
    directory="02_tuples",
    summary=(
        "Python's record type: an immutable binding of references that "
        "unlocks hashable keys, safe unpacking, and the one trap - shallow "
        "immutability - that teams discover in production."
    ),
    why_it_matters=(
        "Returns of several values, dictionary keys, coordinate grids and "
        "mission records are all tuples in real Python systems. The failure "
        "students must not carry into industry is trusting 'immutable' data "
        "that contains a mutable list - a corrupted audit trail that raises no "
        "error at all."
    ),
    objectives=[
        "Construct and unpack tuples, including the one-element comma form.",
        "Explain why assignment still aliases immutable objects.",
        "Distinguish shallow from deep immutability with a live example.",
        "Predict which objects are hashable and use tuples as dict keys.",
        "Choose tuple returns over out-parameter mutation for multi-value results.",
        "Accumulate into lists and convert once instead of concatenating tuples.",
    ],
    prerequisites=["Topic 3.1 Lists"],
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
