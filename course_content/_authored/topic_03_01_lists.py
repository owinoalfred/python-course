"""Topic 3.1 - Lists.

Hand-authored to the Course Content Standard. The spine: a list is a mutable
sequence of *references*, so the two failure modes that follow are aliasing
(two names, one list) and in-place mutation (methods that change the list and
return None) - both silent until they are not.
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
        "A list is Python's general-purpose **ordered, mutable** sequence. Ordered "
        "means position is meaningful and stable: `list[0]` is always the first "
        "element you put there until you move it. Mutable means the same list "
        "object can grow, shrink and change while every name bound to it observes "
        "the change. That second property is the whole topic, because it is where "
        "both of the classic list bugs come from."
    ),
    MD(
        "Under the hood a list is an array of pointers: a contiguous block of "
        "references to objects that live elsewhere in memory. This is why "
        "indexing is O(1) regardless of size, why appending is amortised O(1), "
        "and why inserting at the front is O(n) - every later reference must be "
        "shifted. It also explains a subtlety beginners miss: a list stores "
        "*references*, not values, so `[0] * 3` builds three references to the "
        "**same** integer object, and a nested `[row] * n` builds n references to "
        "the **same** row."
    ),
    CODE_CELL(
        "waypoints = [(0.0, 0.0), (3.0, 0.0), (3.0, 4.0)]\n"
        "print('before:', waypoints)\n"
        "\n"
        "alias = waypoints            # a second name for the SAME list\n"
        "alias.append((6.0, 4.0))\n"
        "print('alias appended:', alias)\n"
        "print('waypoints now :', waypoints)   # changed too - aliasing"
    ),
    MD(
        "Assignment never copies. `alias = waypoints` binds a second name to one "
        "list object, so every mutation through either name is visible through "
        "both. This is not a defect - sharing is how Python avoids copying large "
        "data - but code that *intends* an independent copy must ask for one with "
        "`list(waypoints)`, `waypoints[:]` or `waypoints.copy()`, and must "
        "understand that all three are **shallow**: the outer list is new, the "
        "elements are the same references as before."
    ),
]

LESSON["formal_theory"] = [
    MD(
        "A list is a sequence supporting the full sequence protocol: indexing "
        "`a[i]`, negative indexing `a[-1]`, slicing `a[i:j:k]`, `len(a)`, `a + b`, "
        "`a * n`, membership `x in a`, and iteration. Two defining identities keep "
        "the mental model honest:"
    ),
    EQUATION("a[i:j] builds a NEW list   |   for names x, y:  x is y  <=>  x and y reference the same object"),
    MD(
        "Slicing always allocates. `window = readings[2:5]` copies three "
        "references into a fresh list, so later mutations of `readings` do not "
        "change `window`, and vice versa. The cost of a slice is O(k) in the "
        "number of elements copied - cheap for a window over a log, but a "
        "`readings[:]` of a million-element list is a million references moved."
    ),
    CODE_CELL(
        "readings = [0.4, 0.9, 0.7]\n"
        "window = readings[1:]\n"
        "window.append(0.2)\n"
        "print('window:', window)\n"
        "print('source:', readings)          # the slice was a copy\n"
        "print('same object?', window is readings)"
    ),
    TABLE(
        ["Operation", "Time", "Notes"],
        [
            ["a[i]", "O(1)", "direct pointer read"],
            ["a.append(x)", "amortised O(1)", "occasional resize, still linear overall"],
            ["a + b / a * n", "O(n + m)", "builds a new list"],
            ["a.insert(0, x)", "O(n)", "every reference shifts by one"],
            ["x in a", "O(n)", "linear scan - use a set for repeated tests"],
            ["a[i:j]", "O(j - i)", "copies the references in the window"],
            ["del a[i] / a.pop(i)", "O(n - i)", "cheap at the end, costly at the front"],
        ],
    ),
    MD(
        "Mutating methods are the contract students must memorise: `append`, "
        "`extend`, `insert`, `remove`, `pop`, `sort`, `reverse` and `clear` all "
        "modify the list **in place** and return `None`. The one non-mutating "
        "counterpart is the free function `sorted(a)`, which returns a new list "
        "and leaves the original untouched. Code that writes `readings = "
        "readings.sort()` therefore binds the name to `None` and destroys the "
        "list on the next line that uses it."
    ),
]

LESSON["syntax"] = [
    MD("The canonical forms - literal construction, in-place methods, and the non-mutating alternatives."),
    CODE_CELL(
        "commands = ['stop', 'hold', 'go']\n"
        "\n"
        "commands.append('log')            # in place, returns None\n"
        "commands.extend(['rest', 'idle'])  # splice every item of the argument\n"
        "top = commands.pop()              # remove AND return the last item\n"
        "commands.insert(0, 'boot')\n"
        "commands.remove('hold')           # removes the FIRST match by value\n"
        "\n"
        "print('commands :', commands)\n"
        "print('popped   :', top)\n"
        "\n"
        "original = [3, 1, 2]\n"
        "ordered = sorted(original)        # new list, original untouched\n"
        "original.sort()                   # in place\n"
        "print('sorted() :', ordered, ' list.sort():', original)"
    ),
    MD("The anti-pattern - assigning the result of a mutating method, which is always `None`:"),
    CODE(
        "readings = [0.4, 0.9, 0.7]\n"
        "readings = readings.sort()        # None - the list is gone\n"
        "readings.append(0.1)              # AttributeError: 'NoneType'\n"
        "\n"
        "readings.sort()                   # correct: call for the side effect\n"
        "ordered = sorted(readings)        # correct: call for the new list",
        lang="text",
    ),
    WARN(
        "append is not extend",
        "`append(x)` adds x as a single element, even when x is a list; `extend(xs)` "
        "splices every element of xs. `a.append([1, 2])` grows the list by one - a "
        "nested list - while `a.extend([1, 2])` grows it by two.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - build and read a waypoint list.**"),
    CODE_CELL(
        "waypoints = []\n"
        "for x, y in ((0, 0), (3, 0), (3, 4)):\n"
        "    waypoints.append((x, y))\n"
        "\n"
        "print('first :', waypoints[0])\n"
        "print('last  :', waypoints[-1])\n"
        "print('count :', len(waypoints))\n"
        "print('slice :', waypoints[1:])"
    ),
    MD("**Example 2 - a running log with membership tests.**"),
    CODE_CELL(
        "log = []\n"
        "for value in (0.4, 0.9, 0.7):\n"
        "    log.append(round(value, 2))\n"
        "\n"
        "print('log contains 0.9?', 0.9 in log)\n"
        "print('first index of 0.7:', log.index(0.7))\n"
        "print('total readings:', len(log))"
    ),
    MD(
        "**Example 3 - unpacking, which reads better than indexing.** The star "
        "pattern captures \"everything else\" without a slice argument."
    ),
    CODE_CELL(
        "first, *rest, last = [10, 20, 30, 40]\n"
        "print('first:', first, ' rest:', rest, ' last:', last)\n"
        "\n"
        "head, tail = commands[:1], commands[1:]\n"
        "print('head:', head, ' tail:', tail)"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "**Windows over a log.** Slicing by computed bounds is the readable way to "
        "walk a fixed-width window; the indices come from `range`, so the window "
        "size and the stop value stay in one place."
    ),
    CODE_CELL(
        "readings = [0.4, 0.9, 0.7, 0.2, 0.8, 0.5]\n"
        "size = 3\n"
        "windows = [readings[i:i + size] for i in range(len(readings) - size + 1)]\n"
        "print('windows:', windows)\n"
        "print('last window:', windows[-1], ' is a copy?', windows[-1] is readings)"
    ),
    MD(
        "**Sorting with intent.** `list.sort()` mutates; `sorted()` returns a new "
        "list; `reverse=True` inverts; a `key` extracts the ranking criterion so "
        "the data itself is never rewritten to be sortable."
    ),
    CODE_CELL(
        "telemetry = [('alpha', 0.42), ('beta', 0.19), ('gamma', 0.75)]\n"
        "\n"
        "by_value = sorted(telemetry, key=lambda row: row[1], reverse=True)\n"
        "print('ranked :', by_value)\n"
        "print('source :', telemetry)          # unchanged by sorted()"
    ),
    MD(
        "**Copying deliberately.** When a function must not disturb the caller's "
        "list, copy at the boundary - and remember the copy is shallow."
    ),
    CODE_CELL(
        "def clamp(readings, limit=1.0):\n"
        "    data = list(readings)             # own the copy\n"
        "    data = [min(value, limit) for value in data]\n"
        "    return data\n"
        "\n"
        "source = [0.4, 1.3, 0.7]\n"
        "safe = clamp(source)\n"
        "print('safe  :', safe)\n"
        "print('source:', source)              # caller's list untouched"
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "**Aliasing inside nested structures.** `[row] * n` repeats the *same* "
        "reference n times, so writing to one row writes to all of them. The fix "
        "is a comprehension that builds each row fresh."
    ),
    CODE_CELL(
        "broken = [[0] * 3] * 3\n"
        "broken[0][1] = 7\n"
        "print('broken:', broken)              # every row changed\n"
        "\n"
        "grid = [[0] * 3 for _ in range(3)]\n"
        "grid[0][1] = 7\n"
        "print('grid  :', grid)                # only row 0 changed"
    ),
    WARN(
        "shallow copies share their elements",
        "`a = [[1], [2]]; b = a.copy()` gives two outer lists that still point at "
        "the same inner lists. Mutating `b[0]` changes `a[0]`. For independent "
        "nested data use `copy.deepcopy(a)` - and pay its cost deliberately.",
    ),
    MD(
        "**Mutation during iteration** silently skips elements, because the loop "
        "reads by position while the list shifts underneath it. Iterate a copy "
        "(or build a new list) instead."
    ),
    CODE_CELL(
        "targets = [1, 2, 3, 4, 5]\n"
        "\n"
        "naive = list(targets)\n"
        "for value in naive:\n"
        "    if value % 2 == 0:\n"
        "        naive.remove(value)\n"
        "print('naive filter:', naive)         # 2 and 4 still present\n"
        "\n"
        "filtered = [v for v in targets if v % 2 != 0]\n"
        "print('clean filter:', filtered)"
    ),
    TIP(
        "identity tools",
        "`x is y` asks whether two names share one object; `id(x)` prints that "
        "object's identity. Use them to prove aliasing in tests: `assert a is not "
        "b` is the cheapest guard against an accidental shared reference.",
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "**A telemetry cleaner that refuses to damage its input.** This is the "
        "shape every list-processing function should have: copy first, transform "
        "into a new list, return it - the caller's data is never a side effect."
    ),
    CODE_CELL(
        "def clean_readings(raw, low=0.0, high=1.0):\n"
        "    \"\"\"Clamp readings into [low, high] and drop non-numeric entries.\n"
        "\n"
        "    Returns a new list; the input is never modified.\n"
        "    \"\"\"\n"
        "    cleaned = []\n"
        "    for value in raw:\n"
        "        if isinstance(value, bool) or not isinstance(value, (int, float)):\n"
        "            continue                       # skip junk before clamping\n"
        "        cleaned.append(min(max(value, low), high))\n"
        "    return cleaned\n"
        "\n"
        "raw = [0.4, 1.3, 'junk', -0.2, 0.7]\n"
        "print('cleaned:', clean_readings(raw))\n"
        "print('raw    :', raw)                # identical to before the call"
    ),
    BULLETS(
        [
            "`cleaned = []` gives the function its own list, so no caller state is "
            "at risk.",
            "The type guard runs before the clamp, so junk never reaches "
            "`min`/`max` and never raises.",
            "`min(max(v, low), high)` clamps in one expression - readable once you "
            "name it.",
            "Returning the new list makes the function composable: the result can "
            "be chained, stored or discarded without touching `raw`.",
        ]
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "`def clean_readings(raw, low=0.0, high=1.0):` - `raw` is bound to the "
            "caller's list; nothing here copies it yet.",
            "`cleaned = []` - the function now owns a list no one else can see.",
            "`for value in raw:` - iteration reads `raw` by position and never "
            "mutates it, so the loop is safe.",
            "`if isinstance(value, bool) ...: continue` - `bool` subclasses `int`, "
            "so the explicit bool check comes first or `True` would clamp to 1.",
            "`cleaned.append(...)` - in-place growth of the private list; `append` "
            "returns `None`, so it must stand alone as a statement.",
            "`return cleaned` - hand back the new list; `raw` has not been touched "
            "at any point, which the final print proves.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - assuming assignment copies a list.**"),
    CODE(
        "a = [1, 2, 3]\n"
        "b = a                 # same object\n"
        "b.append(4)\n"
        "print(a)              # [1, 2, 3, 4] - a changed too\n"
        "\n"
        "b = a.copy()          # independent outer list\n"
        "b.append(5)\n"
        "print(a)              # [1, 2, 3, 4] - now stable",
        lang="text",
    ),
    MD("**Mistake 2 - assigning a mutating method's return value.**"),
    CODE(
        "readings = [0.4, 0.9]\n"
        "readings = readings.sort()     # None\n"
        "readings = readings.reverse()  # would fail the same way",
        lang="text",
    ),
    MD("**Mistake 3 - append when you meant extend (or the reverse).**"),
    CODE(
        "parts = ['ro']\n"
        "parts.append('ver')            # ['ro', 'ver'] - two elements\n"
        "parts.extend(['-', '01'])      # ['ro', 'ver', '-', '01'] - spliced",
        lang="text",
    ),
    MD("**Mistake 4 - `[x] * n` for nested or mutable elements.**"),
    CODE(
        "row = [[0]] * 2\n"
        "row[0].append(1)\n"
        "print(row)        # [[0, 1], [0, 1]] - ONE inner list, two names\n"
        "\n"
        "row2 = [[0] for _ in range(2)]   # two independent inner lists",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "When a list changes that you never touched, print identity, not value. "
        "`id()` plus a membership check on `is` shows instantly whether two names "
        "share one object."
    ),
    CODE_CELL(
        "a = [(0, 0)]\n"
        "b = a\n"
        "c = list(a)\n"
        "\n"
        "print('a id:', id(a))\n"
        "print('b id:', id(b), ' shares with a?', b is a)\n"
        "print('c id:', id(c), ' shares with a?', c is a)\n"
        "\n"
        "b.append((1, 1))\n"
        "print('after b.append -> a:', a)\n"
        "print('after b.append -> c:', c)      # c stayed independent"
    ),
    MD(
        "When a loop drops the wrong elements, the list is probably moving under "
        "the iteration. Print the list each pass and the skipped elements become "
        "obvious."
    ),
    CODE_CELL(
        "targets = [1, 2, 3, 4]\n"
        "for pass_no, value in enumerate(list(targets)):\n"
        "    print(f'pass {pass_no}: seeing {value}, list is {targets}')\n"
        "    if value % 2 == 0:\n"
        "        targets.remove(value)\n"
        "print('result:', targets)             # 4 was never visited"
    ),
    NOTE(
        "`None` returned from a list method is a fingerprint",
        "If a variable that should hold a list is `None`, search for an assignment "
        "from `.sort()`, `.reverse()` or `.pop()` - one of them wrote `None` into "
        "the name.",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Decide at every assignment whether you want sharing or a copy, and "
            "make the copy explicit with `list(x)` when you do.",
            "Never assign the return value of `append`, `extend`, `sort`, "
            "`reverse`, `insert`, `remove` or `clear` - they return `None`.",
            "Prefer `sorted(x)` when you need the result; use `x.sort()` only "
            "when you deliberately want to reorder in place.",
            "Iterate a copy (`for v in list(items):`) when removing during "
            "iteration, or build a new list with a comprehension.",
            "Use `extend` or `+=` to splice many items; `append` is for exactly "
            "one item, including one list you mean to nest.",
            "Test membership repeatedly against a `set`, not a list - `in` on a "
            "list is O(n) per call.",
            "Return new lists from helpers; treat the caller's list as read-only "
            "unless the function name says it mutates.",
            "Reach for `collections.deque` when you genuinely queue from the "
            "front - `insert(0, x)` and `pop(0)` are O(n) by construction.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "A list is an array of references, so its performance profile follows "
        "directly: random access and tail growth are cheap, front edits and "
        "membership scans are not. The table below is the version worth "
        "memorising - it explains every surprising slowdown in list-heavy code."
    ),
    TABLE(
        ["Pattern", "Cost", "Preferred alternative"],
        [
            ["`for _ in range(n): a.append(x)`", "amortised O(n)", "a comprehension builds it in C"],
            ["`a.insert(0, x)` / `a.pop(0)`", "O(n) each", "`collections.deque` - O(1) at both ends"],
            ["`x in a` inside a loop", "O(n) per test", "hoist into `seen = set(a)` once"],
            ["`a = a + [x]` in a loop", "O(n) per copy - quadratic", "`a.append(x)` or `a += [x]`"],
            ["`a[:]` of a huge list", "O(n) always", "share it read-only, or copy lazily"],
        ],
    ),
    CODE_CELL(
        "import time\n"
        "\n"
        "n = 40_000\n"
        "\n"
        "start = time.perf_counter()\n"
        "acc = []\n"
        "for i in range(n):\n"
        "    acc = acc + [i]                 # reallocates every pass\n"
        "concat_s = time.perf_counter() - start\n"
        "\n"
        "start = time.perf_counter()\n"
        "acc = []\n"
        "for i in range(n):\n"
        "    acc.append(i)                   # grows in place\n"
        "append_s = time.perf_counter() - start\n"
        "\n"
        "print(f'concat {concat_s:.4f}s vs append {append_s:.4f}s')\n"
        "print(f'append is {concat_s / append_s:.1f}x faster here')"
    ),
    MD(
        "The difference is not a constant factor: `a = a + [x]` copies the whole "
        "accumulated list every pass, which is O(n^2) work overall, while "
        "`append` is amortised O(1) per call. For a ten-thousand-element log "
        "built the wrong way the gap is the difference between milliseconds and "
        "seconds."
    ),
]

LESSON["pythonic_approaches"] = [
    MD(
        "Idiomatic list code reads as *what* rather than *how*: build with a "
        "comprehension instead of an empty list plus `append`, iterate the list "
        "rather than its indices, and let unpacking replace manual slicing."
    ),
    CODE_CELL(
        "readings = [0.4, 0.9, 0.7]\n"
        "\n"
        "# not pythonic\n"
        "doubled = []\n"
        "for value in readings:\n"
        "    doubled.append(value * 2)\n"
        "\n"
        "# pythonic - one expression, no manual bookkeeping\n"
        "doubled = [value * 2 for value in readings]\n"
        "print('doubled:', doubled)\n"
        "\n"
        "first, *middle, last = readings\n"
        "print('unpack :', first, middle, last)      # instead of [0], [1:-1], [-1]"
    ),
    BULLETS(
        [
            "`for value in items:` not `for i in range(len(items)):` - the index "
            "is only needed when you use it.",
            "Build with comprehensions; reach for `append` inside a loop only "
            "when each iteration adds zero or one item conditionally.",
            "Use `any(...)` and `all(...)` for existence checks over a list - "
            "they short-circuit.",
            "`items += other` (in place) and `items + other` (new list) differ in "
            "both result identity and cost; pick deliberately.",
            "Sort with `key=` instead of pre-transforming the data.",
        ]
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "A rover's waypoint list is shared by the planner, the logger and the "
        "safety monitor. If one component aliases the list and tidies it in "
        "place, the others silently see a different mission - which is exactly "
        "how a route loses a waypoint without any error being raised."
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
        "plan = [(0.0, 0.0), (3.0, 0.0), (3.0, 4.0)]\n"
        "logger_view = plan                 # alias, not a copy\n"
        "\n"
        "for leg in range(2):\n"
        "    robot.move(1.0, speed_mps=0.4)\n"
        "    status = robot.status()\n"
        "    logger_view.append(tuple(round(c, 2) for c in status['position']))\n"
        "\n"
        "print('plan after drive:', plan)    # the plan GREW via the logger\n"
        "print('battery:', round(robot.status()['battery_pct'], 1), '%')"
    ),
    MD(
        "The fix is a boundary copy: a component that only *reads* the plan gets "
        "`plan.copy()`, and a component that must publish a new plan returns a new "
        "list rather than editing the shared one. The rule - copy on the way in, "
        "return on the way out - is what keeps list sharing safe between modules."
    ),
]

LESSON["engineering_example"] = [
    MD(
        "Batching a sensor stream into fixed-size chunks is a list routine that "
        "appears in every telemetry pipeline. Slicing by a computed stride keeps "
        "the loop index and the window size in one expression, and the final "
        "partial window is preserved rather than dropped."
    ),
    CODE_CELL(
        "def batch(values, size):\n"
        "    \"\"\"Split values into consecutive chunks of at most size items.\"\"\"\n"
        "    if size <= 0:\n"
        "        raise ValueError('size must be positive')\n"
        "    return [values[i:i + size] for i in range(0, len(values), size)]\n"
        "\n"
        "stream = [0.1, 0.2, 0.3, 0.4, 0.5]\n"
        "print('batches of 2:', batch(stream, 2))\n"
        "print('batches of 4:', batch(stream, 4))\n"
        "print('source intact:', stream)"
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Build a list with `append`, then print its length, first and last "
            "elements using positive and negative indexing.",
            "Slice a window from a list of readings and prove the slice is a copy "
            "by mutating it and reprinting the source.",
            "Reproduce the aliasing bug (`b = a; b.append(...)`) and then fix it "
            "with `list(a)`.",
            "Sort a list of `(name, value)` tuples two ways: in place with a key, "
            "and into a new list with `sorted` - confirm which one changed the "
            "original.",
            "Filter even numbers out of a list twice: by mutating during "
            "iteration (watch it fail) and with a comprehension (watch it work).",
        ]
    ),
    CODE_CELL(
        "readings = [0.4, 0.9, 0.7, 0.2]\n"
        "print('len:', len(readings), ' first:', readings[0], ' last:', readings[-1])\n"
        "\n"
        "window = readings[1:3]\n"
        "window.append(9.9)\n"
        "print('window:', window, ' source:', readings)   # copy proven\n"
        "\n"
        "a, b = [1, 2], None\n"
        "b = a\n"
        "b.append(3)\n"
        "print('aliasing made a =', a)\n"
        "\n"
        "original = [3, 1, 2]\n"
        "ordered = sorted(original)\n"
        "print('sorted():', ordered, ' original:', original)"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: a list is a row of labeled boxes, and a variable is only "
        "a label pointing at the row.** Indexing reads one box. In-place methods "
        "write into boxes, so every label pointing at the row sees the change. "
        "Assignment of one name to another just prints a second label - it never "
        "photographs the row."
    ),
    TABLE(
        ["Statement", "What it does", "Independent copy?"],
        [
            ["`b = a`", "second label on the same row", "no - aliasing"],
            ["`b = a.copy()`", "new row, same element references", "outer yes, elements no"],
            ["`b = a[:]` / `list(a)`", "same as `.copy()`", "outer yes, elements no"],
            ["`b = a[i:j]`", "new row from a window", "yes for the window"],
            ["`a.append(x)`", "writes into the row", "n/a - mutates in place"],
            ["`b = sorted(a)`", "new row in ranking order", "yes - `a` is untouched"],
        ],
    ),
]

TERMS = [
    ["List", "An ordered, mutable sequence backed by an array of references."],
    ["Mutability", "The ability of an object to change after it is created."],
    ["Aliasing", "Two or more names bound to the same object."],
    ["Shallow copy", "A new outer container whose elements are the same references."],
    ["Deep copy", "A fully independent clone, including every nested object."],
    ["In-place", "An operation that modifies its target and returns None."],
    ["Amortised O(1)", "Average constant cost per append despite occasional resizing."],
    ["Sequence protocol", "Indexing, slicing, len, membership and iteration on a container."],
    ["Reference", "A name's pointer to an object stored elsewhere in memory."],
    ["Slice", "A window of a sequence that always produces a new list."],
]

LESSON["summary"] = [
    MD(
        "A list is an ordered, mutable sequence backed by an array of references. "
        "That single sentence explains the performance table - O(1) indexing, "
        "amortised O(1) appends, O(n) front edits and membership scans - and it "
        "explains the two failure modes the topic is really about."
    ),
    MD(
        "The first failure mode is **aliasing**: `b = a` creates a second name, "
        "not a second list, so a mutation through either name is seen by both. "
        "Copies must be requested explicitly, and every built-in copy is shallow. "
        "The second is **in-place mutation**: `append`, `extend`, `insert`, "
        "`remove`, `pop`, `sort`, `reverse` and `clear` all change the list and "
        "return `None`, so assigning their result destroys the data, and "
        "mutating during iteration skips elements."
    ),
    MD(
        "The engineering discipline that follows is simple and universal: decide "
        "at every line whether you intend sharing or independence, copy "
        "deliberately at module boundaries, iterate a copy when you remove, and "
        "return new lists from helpers. Applied consistently, list bugs stop being "
        "silent - which, for a waypoint plan shared by three components of a "
        "rover, is the only acceptable outcome."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "Lists are ordered and mutable; assignment aliases, it never copies.",
            "`list(x)`, `x.copy()` and `x[:]` are shallow copies - inner objects "
            "are still shared.",
            "Mutating methods change the list in place and return `None`; "
            "`sorted(x)` returns a new list.",
            "`append` adds one element, `extend` splices many - confusing them "
            "changes the data's shape.",
            "`[x] * n` repeats references; use a comprehension for nested or "
            "mutable elements.",
            "Never remove from a list while iterating it directly - iterate a "
            "copy or build a new list.",
            "Indexing and tail appends are cheap; front edits and `x in a` are "
            "linear - use a `deque` or a `set` instead.",
            "Copy on the way into shared code, return new lists on the way out.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "Read `collections.deque` in the standard library docs and note which "
            "list operations it makes O(1).",
            "Time `a = a + [x]` against `a.append(x)` for n = 10^4, 10^5 and "
            "10^6, and confirm the quadratic curve.",
            "Investigate `copy.deepcopy` versus `copy.copy` on a list of dicts, "
            "and write the assertion that proves the difference.",
            "Look up `list.clear()`, `list.remove()` and `list.index()` edge "
            "cases - what does `remove` do when the value is absent?",
            "Preview `bisect.insort`: how does Python keep a sorted list "
            "balanced between insertion cost and search cost?",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Clamp readings without touching the caller's list",
        difficulty="MEDIUM",
        learning_objectives=["Copy an input before transforming it.", "Clamp numeric values into a range."],
        concepts_tested=["copying", "append", "range clamping", "immutability of inputs"],
        problem_statement=(
            "Write `clamp_readings(readings, low=0.0, high=1.0)` returning a new "
            "list with every numeric value clamped into `[low, high]`. The input "
            "list must be unchanged after the call."
        ),
        requirements=[
            "Return a new list, never the input.",
            "Skip values that are not int or float (bools count as not numeric).",
            "Preserve the original order of the kept values.",
        ],
        constraints=["Do not mutate the argument in place."],
        input_description="A list of arbitrary Python values.",
        expected_output="A new list of floats clamped into the given range.",
        example_input="clamp_readings([0.4, 1.3, 'x', -0.2])",
        example_output="[0.4, 1.0, 0.0]",
        edge_cases=[
            "An empty input returns an empty list.",
            "A bool value is skipped even though bool subclasses int.",
            "low greater than high raises ValueError.",
        ],
        hints=["Copy first with list(readings), then filter and clamp while appending."],
        success_criteria=["The example output matches exactly.", "The input list is byte-identical after the call."],
        optional_extension="Accept an iterable of readings and return a list.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Rotate a command list with slicing",
        difficulty="MEDIUM",
        learning_objectives=["Use slicing with computed bounds.", "Handle wrap-around indices."],
        concepts_tested=["slicing", "rotation", "modulo indexing"],
        problem_statement=(
            "Write `rotate(commands, k)` returning a new list rotated right by k "
            "positions: the last k items move to the front, wrapping as needed."
        ),
        requirements=["Build the result with slicing, not a loop.", "Return a new list."],
        constraints=["Do not use collections.deque."],
        input_description="A list of commands and a (possibly negative or oversized) int k.",
        expected_output="A new rotated list.",
        example_input="rotate(['a', 'b', 'c', 'd'], 2)",
        example_output="['c', 'd', 'a', 'b']",
        edge_cases=[
            "k = 0 returns an equal (but new) list.",
            "k larger than len(commands) wraps via modulo.",
            "A negative k rotates left.",
            "An empty list returns an empty list.",
        ],
        hints=["Normalise k with k % len(commands), then slice tail + head."],
        success_criteria=["The example output matches.", "rotate(xs, len(xs)) returns a copy equal to xs."],
        optional_extension="Rotate left in place using only reversals.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Running totals for a battery drain log",
        difficulty="MEDIUM",
        learning_objectives=["Accumulate derived values in a list.", "Pair two lists by index safely."],
        concepts_tested=["accumulation", "append", "zip"],
        problem_statement=(
            "Write `running_totals(deltas)` returning a list where element i is "
            "the sum of deltas[0..i] inclusive."
        ),
        requirements=["Return a list of the same length as the input.", "Use a single pass."],
        constraints=["Do not import itertools."],
        input_description="A list of numeric deltas (may contain negatives).",
        expected_output="A list of cumulative sums.",
        example_input="running_totals([1.0, -0.5, 2.0])",
        example_output="[1.0, 0.5, 2.5]",
        edge_cases=[
            "An empty input returns an empty list.",
            "A single element returns a one-element list.",
            "All-negative deltas produce a decreasing list.",
        ],
        hints=["Keep a running total and append it after each update."],
        success_criteria=["The example matches.", "running_totals([]) returns []."],
        optional_extension="Also return the maximum running total seen.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Batch a telemetry stream into fixed-size chunks",
        difficulty="MEDIUM",
        learning_objectives=["Slice with a stride from range.", "Preserve a partial final batch."],
        concepts_tested=["slicing", "range with step", "batching"],
        problem_statement=(
            "Write `batch(values, size)` splitting values into consecutive chunks "
            "of at most `size` items, keeping any short final chunk."
        ),
        requirements=[
            "Use slicing inside a range-stride loop or comprehension.",
            "Raise ValueError for size < 1.",
        ],
        constraints=["Do not import itertools."],
        input_description="A sequence of values and a positive int size.",
        expected_output="A list of lists whose concatenation equals the input.",
        example_input="batch([1, 2, 3, 4, 5], 2)",
        example_output="[[1, 2], [3, 4], [5]]",
        edge_cases=[
            "size equal to len(values) yields one chunk.",
            "An empty input yields an empty list.",
            "size = 1 yields one singleton chunk per item.",
        ],
        hints=["range(0, len(values), size) gives the start of each chunk."],
        success_criteria=["Concatenating the output reproduces the input exactly."],
        optional_extension="Accept a step parameter so chunks may overlap.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Split evens and odds while keeping their order",
        difficulty="MEDIUM",
        learning_objectives=["Partition one list into two.", "Preserve relative order within each side."],
        concepts_tested=["conditional append", "stability", "two accumulators"],
        problem_statement=(
            "Write `split_parity(values)` returning a tuple `(evens, odds)` where "
            "each sublist keeps the relative order it had in the input."
        ),
        requirements=["Return a tuple of two new lists.", "Do not sort."],
        constraints=["Single pass over the input."],
        input_description="A list of integers.",
        expected_output="(evens, odds) - both lists in original relative order.",
        example_input="split_parity([1, 2, 3, 4, 5, 6])",
        example_output="([2, 4, 6], [1, 3, 5])",
        edge_cases=[
            "An empty input gives ([], []).",
            "All-even input gives (a copy of the input, []).",
            "Negative odds belong to odds (-3 % 2 == 1 in Python).",
        ],
        hints=["Two empty lists, append into the right one per element, return the tuple."],
        success_criteria=["The example matches.", "No input list is mutated."],
        optional_extension="Return a dict keyed by value % 3 for three-way partitioning.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Merge two sorted lists in linear time",
        difficulty="HARD",
        learning_objectives=["Merge two sorted inputs without re-sorting.", "Reason about loop invariants."],
        concepts_tested=["two-pointer merge", "sorted input", "amortised append"],
        problem_statement=(
            "Write `merge_sorted(left, right)` combining two ascending lists into "
            "one ascending list in O(n + m) time, without calling `sorted` or "
            "appending to the whole result each step."
        ),
        requirements=[
            "Single pass with two index pointers.",
            "Stable: equal elements come from left first.",
        ],
        constraints=["Do not call sorted() or list.sort() on the combined result."],
        input_description="Two lists already sorted in ascending order.",
        expected_output="One new sorted list containing every element of both inputs.",
        example_input="merge_sorted([1, 3, 5], [2, 4])",
        example_output="[1, 2, 3, 4, 5]",
        edge_cases=[
            "One input empty returns a copy of the other.",
            "Both empty returns [].",
            "Duplicate values across inputs are all retained.",
            "Inputs of wildly different lengths still run in O(n + m).",
        ],
        hints=["Compare the heads, append the smaller, advance only that pointer, then extend with the tail."],
        success_criteria=["The example matches.", "merge_sorted(a, b) equals sorted(a + b) for random sorted a, b."],
        optional_extension="Merge k sorted lists using a heap.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Transpose a rectangular matrix into a new one",
        difficulty="HARD",
        learning_objectives=["Map rows to columns with indexing.", "Detect ragged input explicitly."],
        concepts_tested=["nested lists", "index swapping", "validation", "new-list construction"],
        problem_statement=(
            "Write `transpose(matrix)` returning a NEW matrix whose rows are the "
            "input's columns. The input must not be modified, and a ragged matrix "
            "(rows of differing length) must raise ValueError."
        ),
        requirements=[
            "Return a list of new lists.",
            "Raise ValueError on ragged rows.",
            "Handle the empty matrix.",
        ],
        constraints=["Do not import numpy."],
        input_description="A list of equal-length lists (possibly empty).",
        expected_output="The transposed matrix.",
        example_input="transpose([[1, 2, 3], [4, 5, 6]])",
        example_output="[[1, 4], [2, 5], [3, 6]]",
        edge_cases=[
            "[] transposes to [].",
            "[[]] transposes to [].",
            "A single row becomes a single column.",
            "[[1, 2], [3]] raises ValueError.",
        ],
        hints=[
            "zip(*matrix) transposes but returns tuples and silently truncates "
            "ragged rows - validate row lengths first, or index manually.",
        ],
        success_criteria=["The example matches.", "The input matrix is unchanged after the call."],
        optional_extension="Support a sparse representation where missing cells default to 0.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Rotate a list in place with O(1) extra memory",
        difficulty="HARD",
        learning_objectives=["Reverse three slices conceptually.", "Trade readability for memory deliberately."],
        concepts_tested=["in-place algorithm", "reversal", "index arithmetic"],
        problem_statement=(
            "Write `rotate_in_place(values, k)` rotating the list right by k using "
            "only O(1) extra memory - no new list of the same length may be built."
        ),
        requirements=["Mutate the argument in place.", "Normalise oversized and negative k."],
        constraints=["Extra memory must not scale with len(values)."],
        input_description="A list of elements and an int k.",
        expected_output="None (the list is rotated in place).",
        example_input="xs = [1, 2, 3, 4, 5]; rotate_in_place(xs, 2); xs",
        example_output="[4, 5, 1, 2, 3]",
        edge_cases=[
            "k = 0 is a no-op.",
            "k negative rotates left.",
            "An empty list does nothing.",
        ],
        hints=["Reverse the whole list, then reverse the two segments - or index-swap with a modulo."],
        success_criteria=["The example matches.", "No allocation proportional to len(xs) is made."],
        optional_extension="Implement the juggling algorithm and compare readability.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Sliding windows with a custom step",
        difficulty="HARD",
        learning_objectives=["Generalise windowing with start and stride.", "Derive the exact window count."],
        concepts_tested=["slicing", "range strides", "window arithmetic"],
        problem_statement=(
            "Write `windows(values, size, step=1)` returning every window of "
            "`size` consecutive elements taken every `step` positions."
        ),
        requirements=[
            "Return a list of new lists.",
            "Raise ValueError when size < 1 or step < 1.",
            "Stop at the last complete window.",
        ],
        constraints=["No itertools.islice."],
        input_description="A sequence, a positive size, and a positive step.",
        expected_output="A list of windows in ascending start order.",
        example_input="windows([1, 2, 3, 4, 5], 3, step=2)",
        example_output="[[1, 2, 3], [3, 4, 5]]",
        edge_cases=[
            "size greater than len(values) yields [].",
            "step equal to size yields non-overlapping windows.",
            "An empty input yields [].",
        ],
        hints=["Starts are range(0, len(values) - size + 1, step); each window is a slice from each start."],
        success_criteria=["The example matches.", "Concatenating windows with step == size reproduces the input."],
        optional_extension="Return a generator so huge inputs stream instead of building a list.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Run-length encode a command stream",
        difficulty="HARD",
        learning_objectives=["Group consecutive equal items.", "Encode runs without losing boundaries."],
        concepts_tested=["run-length encoding", "run detection", "tuples in lists"],
        problem_statement=(
            "Write `run_length(values)` returning a list of `(value, count)` "
            "tuples describing consecutive runs - only *consecutive* repeats "
            "merge; equal values separated by a different value form two runs."
        ),
        requirements=["Return a list of tuples.", "Preserve the original order of runs."],
        constraints=["Single pass; do not use groupby - implement the grouping yourself."],
        input_description="A list of hashable values (e.g. strings or ints).",
        expected_output="A list of (value, run-length) tuples.",
        example_input="run_length(['go', 'go', 'hold', 'go'])",
        example_output="[('go', 2), ('hold', 1), ('go', 1)]",
        edge_cases=[
            "An empty input returns [].",
            "A list of all identical values yields one tuple with the full count.",
            "Single-element runs are emitted with count 1.",
        ],
        hints=["Track the current run's value and count; append and reset when the value changes."],
        success_criteria=["The example matches.", "Summing the counts equals len(input)."],
        optional_extension="Decode the encoding back to the original list and test the round trip.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "def clamp_readings(readings, low=0.0, high=1.0):\n"
            "    \"\"\"Return a clamped copy; the input list is never modified.\"\"\"\n"
            "    if low > high:\n"
            "        raise ValueError('low must not exceed high')\n"
            "    clamped = []\n"
            "    for value in readings:\n"
            "        if isinstance(value, bool) or not isinstance(value, (int, float)):\n"
            "            continue\n"
            "        clamped.append(min(max(value, low), high))\n"
            "    return clamped"
        ),
        explanation=(
            "Copying is the contract: nothing in the function writes to the "
            "argument, and clamped starts life as a private list. The bool guard "
            "precedes the numeric check because bool subclasses int in Python - "
            "without it, True would clamp to 1.0 and silently pollute the log."
        ),
        complexity="Time O(n); space O(k) for the k numeric values kept.",
        edge_cases="Empty input returns []. low > high raises. bools are skipped, not clamped.",
        alternative_approaches="A list comprehension with an inline guard is shorter but buries the validation policy.",
        testing=(
            "src = [0.4, 1.3, 'x', -0.2]\n"
            "out = clamp_readings(src)\n"
            "assert out == [0.4, 1.0, 0.0]\n"
            "assert src == [0.4, 1.3, 'x', -0.2]"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def rotate(commands, k):\n"
            "    \"\"\"Rotate right by k with wrap-around; returns a new list.\"\"\"\n"
            "    if not commands:\n"
            "        return []\n"
            "    k = k % len(commands)\n"
            "    if k == 0:\n"
            "        return list(commands)\n"
            "    return commands[-k:] + commands[:-k]"
        ),
        explanation=(
            "Modulo normalises any k - negative or huge - into [0, len), so the "
            "slice arithmetic only ever sees a valid offset. The tail slice "
            "commands[-k:] is the part that wraps, and concatenating the two "
            "slices builds a fresh list, leaving the original untouched."
        ),
        complexity="Time O(n); space O(n) for the new list.",
        edge_cases="Empty list returns []. k = 0 returns a copy via the early return plus the modulo branch.",
        alternative_approaches="collections.deque.rotated exists in 3.2+ but hides the slicing lesson.",
        testing=(
            "assert rotate(['a', 'b', 'c', 'd'], 2) == ['c', 'd', 'a', 'b']\n"
            "assert rotate([1, 2, 3], 0) == [1, 2, 3]\n"
            "assert rotate([1, 2, 3], -1) == [2, 3, 1]"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "def running_totals(deltas):\n"
            "    \"\"\"Cumulative sums: element i is the sum of deltas[0..i].\"\"\"\n"
            "    total = 0.0\n"
            "    totals = []\n"
            "    for delta in deltas:\n"
            "        total += delta\n"
            "        totals.append(total)\n"
            "    return totals"
        ),
        explanation=(
            "The accumulator starts at zero before the loop, so the first append "
            "is exactly deltas[0] and every later append adds one more delta. "
            "Building the result with append in the same pass keeps the whole "
            "computation linear - a naive nested-sum version would be quadratic."
        ),
        complexity="Time O(n); space O(n).",
        edge_cases="Empty input never enters the loop and returns []. A single delta returns [delta].",
        alternative_approaches="itertools.accumulate does this in C, but the explicit loop shows the invariant.",
        testing=(
            "assert running_totals([1.0, -0.5, 2.0]) == [1.0, 0.5, 2.5]\n"
            "assert running_totals([]) == []\n"
            "assert running_totals([-1, -2]) == [-1, -3]"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "def batch(values, size):\n"
            "    \"\"\"Split into consecutive chunks of at most size items.\"\"\"\n"
            "    if size < 1:\n"
            "        raise ValueError('size must be at least 1')\n"
            "    return [values[i:i + size] for i in range(0, len(values), size)]"
        ),
        explanation=(
            "range(0, len(values), size) yields exactly the start offsets 0, size, "
            "2*size, ... while the last start is below len(values); slicing from "
            "each start clamps automatically at the end of the sequence, so the "
            "short final chunk falls out without a special case."
        ),
        complexity="Time O(n); space O(n) across all chunks.",
        edge_cases="Empty input yields []. size greater than len(values) yields one chunk equal to a copy of the input.",
        alternative_approaches="A while loop with pop(0) destroys the input; a deque-based splitter trades clarity.",
        testing=(
            "assert batch([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]\n"
            "assert batch([], 3) == []\n"
            "flat = [x for chunk in batch(list(range(10)), 3) for x in chunk]\n"
            "assert flat == list(range(10))"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "def split_parity(values):\n"
            "    \"\"\"Split into (evens, odds), each preserving input order.\"\"\"\n"
            "    evens, odds = [], []\n"
            "    for value in values:\n"
            "        (evens if value % 2 == 0 else odds).append(value)\n"
            "    return evens, odds"
        ),
        explanation=(
            "One pass, two accumulators, one conditional append - relative order "
            "within each side is preserved because appends happen in input order. "
            "Python's modulo gives -3 % 2 == 1, so negative odds land on the odds "
            "side without special-casing the sign."
        ),
        complexity="Time O(n); space O(n).",
        edge_cases="Empty input returns ([], []). All-even input puts a copy of everything in evens.",
        alternative_approaches="Two comprehensions are shorter but scan the input twice.",
        testing=(
            "assert split_parity([1, 2, 3, 4, 5, 6]) == ([2, 4, 6], [1, 3, 5])\n"
            "assert split_parity([]) == ([], [])\n"
            "assert split_parity([-3, -2]) == ([-2], [-3])"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "def merge_sorted(left, right):\n"
            "    \"\"\"Stable merge of two ascending lists in O(n + m).\"\"\"\n"
            "    merged = []\n"
            "    i = j = 0\n"
            "    while i < len(left) and j < len(right):\n"
            "        if left[i] <= right[j]:\n"
            "            merged.append(left[i])   # <= keeps left-first stability\n"
            "            i += 1\n"
            "        else:\n"
            "            merged.append(right[j])\n"
            "            j += 1\n"
            "    merged.extend(left[i:])\n"
            "    merged.extend(right[j:])\n"
            "    return merged"
        ),
        explanation=(
            "Two pointers walk the inputs once, each element is appended exactly "
            "once, and the leftover tail of whichever input still has elements is "
            "spliced with extend. Using <= on the left comparison makes ties come "
            "from left, which is what makes the merge stable."
        ),
        complexity="Time O(n + m); space O(n + m).",
        edge_cases="Either input empty reduces the loop to a single extend. Duplicates are all retained.",
        alternative_approaches="heapq.merge is lazy and allocation-free per step, but returns an iterator.",
        testing=(
            "assert merge_sorted([1, 3, 5], [2, 4]) == [1, 2, 3, 4, 5]\n"
            "assert merge_sorted([], [1]) == [1]\n"
            "assert merge_sorted([1, 1], [1]) == [1, 1, 1]"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "def transpose(matrix):\n"
            "    \"\"\"Return a new transposed matrix; ragged input raises.\"\"\"\n"
            "    if not matrix:\n"
            "        return []\n"
            "    width = len(matrix[0])\n"
            "    if any(len(row) != width for row in matrix):\n"
            "        raise ValueError('ragged matrix: rows differ in length')\n"
            "    return [[matrix[r][c] for r in range(len(matrix))] for c in range(width)]"
        ),
        explanation=(
            "Validating every row against the first row's width before any work "
            "happens turns zip's silent truncation on ragged input into an "
            "explicit failure. The nested comprehension then builds each column "
            "as a fresh list, so neither the rows nor the cells of the input are "
            "ever shared with the result."
        ),
        complexity="Time O(rows * cols); space O(rows * cols) for the result.",
        edge_cases="[].  [[]].  A single row becomes a single column. [[1, 2], [3]] raises ValueError.",
        alternative_approaches="zip(*matrix) is one line but returns tuples and truncates ragged rows silently.",
        testing=(
            "assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]\n"
            "assert transpose([]) == []\n"
            "try:\n"
            "    transpose([[1, 2], [3]])\n"
            "    raise AssertionError('should have raised')\n"
            "except ValueError:\n"
            "    pass"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "def rotate_in_place(values, k):\n"
            "    \"\"\"Rotate right by k using reversal - O(1) extra memory.\"\"\"\n"
            "    n = len(values)\n"
            "    if n < 2:\n"
            "        return None\n"
            "    k %= n\n"
            "    if k == 0:\n"
            "        return None\n"
            "\n"
            "    def reverse(lo, hi):\n"
            "        while lo < hi:\n"
            "            values[lo], values[hi] = values[hi], values[lo]\n"
            "            lo, hi = lo + 1, hi - 1\n"
            "\n"
            "    reverse(0, n - 1)      # [5, 4, 3, 2, 1]\n"
            "    reverse(0, k - 1)      # [4, 5, 3, 2, 1]\n"
            "    reverse(k, n - 1)      # [4, 5, 1, 2, 3]"
        ),
        explanation=(
            "Three reversals compose a rotation: reversing everything brings the "
            "rotating tail to the front but backwards, and reversing each half "
            "puts both halves back in order. Only index swaps occur, so memory "
            "stays constant regardless of list length. The modulo first makes the "
            "algorithm safe for any k."
        ),
        complexity="Time O(n) (each element moves twice); space O(1).",
        edge_cases="n < 2 or k % n == 0 are no-ops. Negative k works after modulo.",
        alternative_approaches="Cycling via juggling is also O(1) memory but far harder to prove correct.",
        testing=(
            "xs = [1, 2, 3, 4, 5]\n"
            "rotate_in_place(xs, 2)\n"
            "assert xs == [4, 5, 1, 2, 3]\n"
            "ys = [1, 2, 3]\n"
            "rotate_in_place(ys, 3)\n"
            "assert ys == [1, 2, 3]"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "def windows(values, size, step=1):\n"
            "    \"\"\"Every size-wide window, taken every step positions.\"\"\"\n"
            "    if size < 1 or step < 1:\n"
            "        raise ValueError('size and step must be at least 1')\n"
            "    starts = range(0, len(values) - size + 1, step)\n"
            "    return [list(values[s:s + size]) for s in starts]"
        ),
        explanation=(
            "The last legal start is len(values) - size; range stops before "
            "exceeding it, so incomplete windows are impossible by construction "
            "rather than by a filter. Each window is materialised as its own list "
            "so callers cannot mutate the source through a shared slice."
        ),
        complexity="Time O(num_windows * size); space O(num_windows * size).",
        edge_cases="size > len(values) makes the range empty, returning []. Empty input returns [].",
        alternative_approaches="itertools.islice over indices streams, but the list form is simpler to test.",
        testing=(
            "assert windows([1, 2, 3, 4, 5], 3, step=2) == [[1, 2, 3], [3, 4, 5]]\n"
            "assert windows([1, 2], 5) == []\n"
            "assert windows([], 2) == []"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "def run_length(values):\n"
            "    \"\"\"Encode consecutive runs as (value, count) tuples.\"\"\"\n"
            "    if not values:\n"
            "        return []\n"
            "    runs = []\n"
            "    current, count = values[0], 1\n"
            "    for value in values[1:]:\n"
            "        if value == current:\n"
            "            count += 1\n"
            "        else:\n"
            "            runs.append((current, count))\n"
            "            current, count = value, 1\n"
            "    runs.append((current, count))\n"
            "    return runs"
        ),
        explanation=(
            "The loop compares each value against the current run's value and "
            "only closes the run on a change, so equal values separated by a "
            "different value correctly form two runs. The final append after the "
            "loop flushes the last run - the classic off-by-one to forget, and "
            "the reason the all-identical case must be tested."
        ),
        complexity="Time O(n); space O(number of runs).",
        edge_cases="Empty input returns []. A single value yields [(value, 1)]. All-identical yields one tuple.",
        alternative_approaches="itertools.groupby is equivalent but hides the grouping you are being asked to implement.",
        testing=(
            "assert run_length(['go', 'go', 'hold', 'go']) == [('go', 2), ('hold', 1), ('go', 1)]\n"
            "assert run_length([]) == []\n"
            "total = sum(count for _, count in run_length([1, 1, 2]))\n"
            "assert total == 3"
        ),
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="What does `b = a` do when `a` is a list?",
        choices=[
            "Creates an independent copy of every element.",
            "Creates a copy of the outer list only.",
            "Raises TypeError unless a is converted first.",
            "Binds b to the same list object, so mutations through either name are visible in both.",
        ],
        answer=3,
        kind="conceptual",
        explanation=(
            "Assignment binds a name to an object; it never copies. Both names "
            "now point at one list, which is why a later append through b shows "
            "up in a - the single most common list bug in shared-code teams."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="What does this print? `xs = [1, 2, 3]; ys = xs.sort(); print(ys)`",
        choices=["[1, 2, 3]", "None", "[3, 2, 1]", "An AttributeError at the print."],
        answer=1,
        kind="code_output",
        explanation=(
            "list.sort() sorts in place and returns None, so ys is bound to None "
            "while xs itself is sorted. Printing ys therefore shows None - the "
            "fingerprint of assigning a mutating method's return value."
        ),
        reference="lesson.ipynb - Syntax",
    )
)

QUIZ.append(
    quiz(
        question="After `a = [[0]] * 2; a[0].append(1)`, what is `a`?",
        choices=[
            "[[0, 1], [0]]",
            "[[0], [0, 1]]",
            "[[0, 1], [0, 1]]",
            "[[0], [0]]",
        ],
        answer=2,
        kind="code_output",
        explanation=(
            "Multiplying a list repeats the reference, so both outer slots hold "
            "ONE inner list. Appending through a[0] mutates that shared inner "
            "list, and both slots display the same mutated content."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="A loop removes every even number from a list while iterating over it, yet evens remain. Why?",
        choices=[
            "Removing shifts later elements left, so the loop skips the element after each removal.",
            "The list.remove method only removes odd numbers.",
            "Iteration over a list always stops after the first removal.",
            "remove() deletes the first match, which is always odd.",
        ],
        answer=0,
        kind="debugging",
        explanation=(
            "The loop reads by position while removals shift everything after "
            "the deleted item one slot left, so the next index now holds the "
            "element that followed it and is never examined. Iterate over "
            "list(xs) or build a new list instead."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="Which expression guarantees the caller's list is unchanged after your function runs?",
        choices=[
            "data = readings",
            "data = readings[:] then only mutating data",
            "readings.sort() at the start so it is deterministic",
            "data = [] then appending from readings with indexing by hand",
        ],
        answer=1,
        kind="implementation_choice",
        explanation=(
            "Slicing the input into a fresh list means every later mutation "
            "touches only that copy. Aliasing with `=` shares the object, "
            "sorting the argument mutates the caller's data directly, and the "
            "manual indexing variant rebuilds what slicing states in one line."
        ),
        reference="exercises.ipynb - Exercise 1",
    )
)

QUIZ.append(
    quiz(
        question="What is the cost of `xs.insert(0, value)` on a list of n elements?",
        choices=[
            "O(1) - insertion at a known position is always constant.",
            "O(log n) - the list is searched like a binary tree.",
            "O(n) - the backing array is reallocated twice.",
            "O(n) - every later reference must be shifted one slot.",
        ],
        answer=3,
        kind="reasoning",
        explanation=(
            "A list stores references in order, so making room at the front "
            "shifts all n existing references one position. That is why front "
            "insertions in a loop are quadratic and why deque exists for queue "
            "workloads."
        ),
        reference="lesson.ipynb - Performance Considerations",
    )
)

QUIZ.append(
    quiz(
        question="Which statement about `xs.copy()` on `xs = [[1], [2]]` is true?",
        choices=[
            "The outer list is new, but both outer lists still reference the same inner lists.",
            "The copy is fully independent; deepcopy is never needed here.",
            "It raises TypeError because nested lists cannot be copied.",
            "The copy shares the outer list and clones only the inner lists.",
        ],
        answer=0,
        kind="conceptual",
        explanation=(
            "All built-in list copies are shallow: they build a new outer "
            "container of the same element references. Mutating xs[0] through "
            "the copy is visible in the original, so truly independent nested "
            "data requires copy.deepcopy."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="A colleague writes `total = total + running.append(delta)`. What happens?",
        choices=[
            "total grows by delta each pass.",
            "It silently skips the first delta.",
            "append returns None, so total becomes None after the first pass.",
            "It raises ValueError because append needs an index.",
        ],
        answer=2,
        kind="identify_error",
        explanation=(
            "append mutates in place and returns None, so the expression "
            "evaluates to None and rebinds total to it. The very next arithmetic "
            "on total then raises TypeError - the classic None-assignment defect "
            "in one line."
        ),
        reference="lesson.ipynb - Syntax",
    )
)

QUIZ.append(
    quiz(
        question="The rover's logger holds `plan = mission.plan` and then appends a waypoint. What is the safest fix?",
        choices=[
            "Wrap the append in try/except so the failure is contained.",
            "Give the logger `mission.plan.copy()` so it cannot mutate the shared plan.",
            "Call mission.plan.sort() after appending to keep it deterministic.",
            "Convert plan to a tuple before the logger sees it.",
        ],
        answer=1,
        kind="robotics",
        explanation=(
            "The bug is aliasing, not the append: the logger must not share the "
            "mission's list object. A boundary copy lets the logger keep its "
            "own history while the mission plan stays exactly as planned; "
            "exception handling would only hide the corruption."
        ),
        reference="lesson.ipynb - Robotics Connection",
    )
)

QUIZ.append(
    quiz(
        question="Which correctly splices two lists so the result has all elements of both?",
        choices=[
            "a.insert(b) - insert takes a value and an index only.",
            "a + b where a is reassigned inside a loop over b.",
            "a.append(b) - appends b as one nested element.",
            "a.extend(b) or a += b - adds each element of b.",
        ],
        answer=3,
        kind="implementation_choice",
        explanation=(
            "extend and += both splice every element of the iterable into the "
            "target. append nests the whole argument as a single element, "
            "insert requires an index, and repeated a + b rebuilding is the "
            "quadratic anti-pattern this choice avoids."
        ),
        reference="lesson.ipynb - Pythonic Approaches",
    )
)

RESEARCH = {
    "question": (
        "How much slower is building a large list with `a = a + [x]` compared "
        "with `a.append(x)`, and does the gap grow with n?"
    ),
    "hypothesis": (
        "Concatenation is quadratic because it recopies the whole accumulator "
        "each pass, so it should fall further behind append as n increases - "
        "roughly four times worse each time n doubles."
    ),
    "experiment": [
        STEPS(
            [
                "Build lists of n = 10000, 20000, 40000 and 80000 elements two ways: "
                "rebinding with `a = a + [i]`, and `a.append(i)`.",
                "Time each variant with time.perf_counter(), ten runs per size, "
                "recording every raw measurement - not just the best.",
                "Compute the median per n and the ratio concat/append at each size.",
                "Plot or tabulate ratio against n and compare the growth to your "
                "hypothesis's four-times-per-doubling prediction.",
            ]
        ),
    ],
    "data": [
        CODE_CELL(
            "# Record your raw timings - one row per variant per run.\n"
            "# Copy real values from your actual runs; do not invent them.\n"
            "#\n"
            "# | n | variant | run | seconds |"
        ),
    ],
    "analysis": [
        MD(
            "Compare medians rather than minima: garbage collection and scheduler "
            "noise punish the fastest single run. If the ratio roughly doubles "
            "each time n doubles, the measurements support the quadratic model; "
            "a flat ratio would suggest both variants are linear in practice."
        ),
    ],
    "result": [
        MD(
            "State the measured ratio at each n and whether it grew with n. Report "
            "any run where append was slower rather than discarding it as noise - "
            "outliers are data too, and naming them is what makes the result "
            "reproducible."
        ),
    ],
    "interpretation": [
        MD(
            "Explain WHY concatenation recopies: `a + [x]` allocates a new list "
            "and copies every reference each pass, so total work is 1+2+...+n. "
            "Name at least two threats to validity, including interpreter warm-up "
            "on the first run and background processes on the machine."
        ),
    ],
    "conclusion": [
        MD(
            "Give your verdict: is the hypothesis supported at all four sizes? "
            "State the n at which the difference would become operationally "
            "noticeable in a real telemetry pipeline, and defend that number."
        ),
    ],
    "extensions": [
        "Repeat with `a += [x]` to confirm in-place extension matches append.",
        "Measure `list.append` against building via a comprehension from a range.",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Waypoint Plan Custodian",
    "context": (
        "Three components share a rover's waypoint plan: the planner builds it, "
        "the logger appends observed positions, and the safety monitor checks "
        "it. If any component aliases the plan and edits it in place, the other "
        "two silently observe a different mission - a corrupted plan that never "
        "raises an error."
    ),
    "mission": (
        "Implement `PlanRegistry` - a small custodian that hands out snapshots, "
        "accepts revisions as new lists, and guarantees no subscriber can mutate "
        "the canonical plan."
    ),
    "requirements": [
        "Expose `plan()` returning a fresh shallow copy each call.",
        "Expose `revise(new_waypoints)` replacing the plan only after validating "
        "it is a list of at least one coordinate pair.",
        "Expose `append_observed(point)` that extends an internal history WITHOUT "
        "touching the canonical plan.",
        "Keep an immutable audit trail of every accepted revision's length.",
    ],
    "constraints": [
        "No subscriber reference may ever be the canonical list object.",
        "Standard library only; no third-party validation libraries.",
        "Every method must complete in O(n) where n is the plan length.",
    ],
    "interface": "class PlanRegistry: def plan(self) -> list; def revise(self, new_waypoints: list) -> None; ...",
    "success_criteria": [
        "Mutating a returned copy leaves the canonical plan unchanged.",
        "append_observed grows the history but never the plan.",
        "Revise with a non-list or empty input raises ValueError.",
        "The audit trail records one entry per accepted revision.",
    ],
    "extension": (
        "Add `subscribe()` returning a view that cannot be mutated at all - e.g. "
        "a tuple of tuples - and state which interface a safety monitor should "
        "be given and why."
    ),
}

MINI_PROJECT = {
    "title": "Mini-Project: Flight Recorder Slice Service",
    "brief": (
        "Build a service that stores a rover's telemetry as one canonical list "
        "and serves windows of it to consumers who must never be able to corrupt "
        "the store."
    ),
    "scenario": (
        "A rover streams readings into an on-board recorder. Analysis tools ask "
        "for windows of recent data, and the recorder itself must survive tools "
        "that accidentally mutate what they receive. A corrupted recording is "
        "worse than a missing one."
    ),
    "rationale": (
        "This is where the topic's two failure modes meet in one design: every "
        "read path must return copies (aliasing), and every write path must "
        "decide explicitly between in-place growth and rebuild (mutation)."
    ),
    "requirements": [
        "Store readings in ONE canonical list; expose it only via copying reads.",
        "Serve `window(start, size)` returning an independent slice, validating "
        "bounds and raising IndexError on a bad start.",
        "Serve `stats()` computing count, min, max and mean WITHOUT exposing the "
        "raw list.",
        "Accept new readings with `record(value)`, clamping them into range and "
        "skipping non-numeric input.",
        "Provide `history()` returning the full copy so a tool can export it.",
    ],
    "constraints": [
        "Standard library only.",
        "No method may return the canonical list object itself.",
        "Recording must be O(1) amortised; window reads O(size).",
    ],
    "deliverables": [
        "`recorder.py` with the `FlightRecorder` class.",
        "`test_recorder.py` with at least twelve assertions, including one that "
        "proves mutating a returned window does not change the store.",
        "A README section explaining the copy-on-read rule and the clamp policy.",
    ],
    "steps": [
        "Implement record() with clamping and type guards; test junk and empty input.",
        "Implement window() with bounds validation; test the mutation-isolation case.",
        "Implement stats() and history(); assert history() is a copy, not an alias.",
        "Add an integration test: record ten readings, take two overlapping "
        "windows, mutate one, and prove the store and the other window are intact.",
    ],
    "expected_behavior": (
        "A junk reading is skipped without shifting later timestamps, a mutated "
        "export window leaves the store byte-identical, and stats() reports the "
        "true count of accepted readings."
    ),
    "acceptance": [
        "All assertions pass from a clean kernel.",
        "Mutating any returned list is proven harmless by a dedicated test.",
        "window() rejects a start beyond the end with IndexError, not a silent "
        "short result.",
        "The README states the copy-on-read rule and why it exists.",
    ],
    "extensions": [
        "Add a maximum capacity so recording evicts the oldest reading, and test "
        "that eviction order is correct.",
        "Return windows as tuples to make immutability structural rather than "
        "conventional, and compare the two designs.",
        "Time record() over 100000 readings and confirm it stays linear.",
    ],
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Make aliasing visible before any method is taught - the mental model "
        "comes first.",
        "Turn 'methods return None' into a memorised fact, not a surprise.",
        "Get students copying deliberately at boundaries, not defensively "
        "everywhere.",
    ],
    "misconceptions": [
        [
            "Assignment copies the list.",
            "It binds a second name to one object; only list(x)/copy()/slice do.",
        ],
        [
            "copy() gives fully independent data.",
            "It is shallow - inner objects are still shared with the original.",
        ],
        [
            "sort() returns the sorted list.",
            "It returns None; sorted() is the one that returns a list.",
        ],
        [
            "Mutating while iterating is fine if you only remove a few items.",
            "Removals shift positions, so elements get skipped unpredictably.",
        ],
    ],
    "difficult_concepts": [
        "Why [x] * n shares references but a comprehension does not.",
        "That append is amortised O(1) while insert(0) is O(n) per call.",
        "Deciding, line by line, between sharing and copying.",
    ],
    "demonstrations": [
        "Run the aliasing demo live: b = a; b.append(...); print(a) and watch "
        "the class predict before running.",
        "Build [[0]] * 2, mutate row 0, and let the class see both rows change.",
        "Time a = a + [x] against a.append(x) for increasing n on the projector.",
    ],
    "discussion": [
        "Is defensive copying everywhere a virtue, or does it hide design "
        "problems? When is sharing the right choice?",
        "Who owns a list passed across a module boundary - the caller or the "
        "callee?",
    ],
    "student_errors": [
        [
            "The list mysteriously changed elsewhere",
            "A second name aliased it and was mutated",
            "Prove identity with `is` and copy at the boundary",
        ],
        [
            "Variable became None after sorting",
            "readings = readings.sort() assigned the return value",
            "Call .sort() alone or use sorted()",
        ],
        [
            "Loop deleted only some of the matching items",
            "Removal during direct iteration skipped elements",
            "Iterate a copy or build a filtered list",
        ],
    ],
    "pacing": (
        "60 min: aliasing demo and mental model (20), method contract and None "
        "(15), copies and shallowness (15), practice start (10). The exercises "
        "carry performance and in-place algorithms for homework."
    ),
    "extensions": [
        "Compare list versus deque timings for queue workloads.",
        "Explore copy.deepcopy on a structure containing tuples and dicts.",
    ],
    "assessment": (
        "Exercise 1 (copy discipline) and Exercise 8 (in-place rotation) together "
        "separate students who understand mutation from those who have memorised "
        "syntax."
    ),
    "support": (
        "Give struggling students the box-and-label diagram and have them draw "
        "every assignment before writing code; if `is` still confuses them, use "
        "id() printed values as concrete evidence."
    ),
    "extension_fast": (
        "Fast finishers implement rotate_in_place with the juggling algorithm and "
        "prove it matches the reversal version on random inputs."
    ),
}

RUBRIC = {
    "artifacts": [
        ["[`exercises.ipynb`](exercises.ipynb)", "40%", "All 10 exercises implemented with copy discipline proven."],
        ["[`mini_project.ipynb`](mini_project.ipynb)", "25%", "FlightRecorder with copy-on-read tests."],
        ["[`robotics_challenge.ipynb`](robotics_challenge.ipynb)", "25%", "PlanRegistry isolates subscribers from the canonical plan."],
        ["[`research.ipynb`](research.ipynb)", "10%", "Real concat-vs-append timings with a defensible conclusion."],
    ],
    "criteria": [
        ["Correctness", "30", "Every example and edge case behaves exactly as specified."],
        ["Mutation discipline", "25", "No alias leaks; every boundary copy is deliberate and tested."],
        ["Code quality", "25", "PEP 8 naming, docstrings, small focused helpers."],
        ["Reasoning", "20", "Aliasing and None-assignment explained in writing, not guessed."],
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
            "Every exercise correct, mutation isolation proven by assertion, and "
            "the in-place rotation demonstrably uses O(1) extra memory.",
        ],
        [
            "Merit",
            "Most exercises correct; one boundary returns an alias or one test "
            "skips the shallow-copy case.",
        ],
        [
            "Pass",
            "Core behaviour right, but copies are made defensively everywhere "
            "without justification, or sort() None-assignment still appears once.",
        ],
        [
            "Fail",
            "The canonical store is mutated through a returned reference, or "
            "several exercises are missing entirely.",
        ],
    ],
}

TOPIC = topic(
    topic_id="3.1",
    title="Lists",
    module=3,
    module_title="Core Data Structures",
    directory="01_lists",
    summary=(
        "Python's ordered, mutable sequence: reference semantics, the two classic "
        "list bugs - aliasing and None-returning methods - and the performance "
        "profile that follows from an array of pointers."
    ),
    why_it_matters=(
        "Every pipeline in the course accumulates data into lists, and the two "
        "list bugs strike silently: a shared waypoint plan changes under every "
        "component that reads it, and a sorted-assigned-to-None log vanishes one "
        "line before it is needed. Mastering reference semantics here is what "
        "makes every later collection safe to touch."
    ),
    objectives=[
        "Explain that assignment aliases and that list copies are shallow.",
        "Predict which list methods mutate in place and what they return.",
        "Copy deliberately at module boundaries with list(), copy() or slicing.",
        "Choose between append, extend and concatenation by cost, not habit.",
        "Process a list safely when elements must be removed or replaced.",
        "State the time complexity of indexing, appending, inserting and scanning.",
    ],
    prerequisites=["Topic 2.5 range, enumerate and zip"],
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
