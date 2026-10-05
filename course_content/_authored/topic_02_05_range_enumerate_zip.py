"""Topic 2.5 - range, enumerate and zip.

Hand-authored to the Course Content Standard. The spine: three built-ins that remove
the bookkeeping loops usually force on you, and the one silent failure each of them
can still produce.
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
        "Three built-ins remove almost all the bookkeeping a loop normally needs. "
        "`range` generates the index values, so you never maintain a counter by hand. "
        "`enumerate` pairs an index with its value, so a loop can use both without "
        "indexing. `zip` walks two sequences in step, so related data does not have to "
        "be indexed in parallel by hand."
    ),
    CODE_CELL(
        "names = ('ada', 'grace', 'alan')\n"
        "scores = (0.91, 0.88, 0.95)\n"
        "\n"
        "print('range   :', list(range(1, 4)))\n"
        "print('enum    :', list(enumerate(names)))\n"
        "print('zip     :', list(zip(names, scores)))"
    ),
    MD(
        "The reason to reach for them is not brevity, it is **removing a class of bug**. "
        "A hand-maintained counter can drift from the data it is supposed to index. "
        "`enumerate` cannot, because the index comes from the same object as the value "
        "- which is exactly the bug a rover's logging loop would have when a reading is "
        "dropped partway through a batch."
    ),
    CODE_CELL(
        "readings = (0.4, 0.9, 0.7)\n"
        "\n"
        "for index, reading in enumerate(readings, start=1):\n"
        "    print(f'sample {index}: {reading}')"
    ),
    NOTE(
        "range is lazy",
        "range does not build a list. It produces its values on demand, so "
        "`range(10**9)` is instant and costs nothing until you iterate it.",
    ),
]

LESSON["formal_theory"] = [
    MD(
        "`range` has three forms. `range(stop)` starts at zero, `range(start, stop)` "
        "excludes the stop value, and `range(start, stop, step)` steps by `step`. The "
        "stop is always **exclusive**, which is the source of nearly every off-by-one "
        "in a range-based loop."
    ),
    EQUATION("range(stop) == range(0, stop, 1)   and   the stop value is never produced"),
    MD(
        "`enumerate` wraps an iterable and yields `(index, value)` pairs, optionally "
        "starting from a given number. It is the only way to get an index without "
        "counting, and because the index is produced by the same iteration it can never "
        "desynchronise from the value."
    ),
    CODE_CELL(
        "print(list(range(0, 10, 3)))\n"
        "print(list(range(5, 0, -2)))\n"
        "print(list(range(3)))\n"
        "print('exclusive stop:', list(range(1, 4)))"
    ),
    MD(
        "`zip` yields tuples drawn from several iterables in step and **stops at the "
        "shortest**. That is the safe default - a mismatch truncates rather than "
        "crashing - but it is silent, and Python 3.10 added `strict=True` precisely "
        "because the silent case causes real defects."
    ),
    CODE_CELL(
        "left = ('a', 'b', 'c')\n"
        "right = (1, 2)\n"
        "print('default  :', list(zip(left, right)))\n"
        "try:\n"
        "    list(zip(left, right, strict=True))\n"
        "except ValueError as exc:\n"
        "    print('strict   : ValueError -', exc)"
    ),
    TABLE(
        ["Built-in", "Yields", "Stops when"],
        [
            ["range(n)", "integers 0 to n-1", "the last value is produced"],
            ["enumerate(s)", "(index, value) pairs", "the sequence is exhausted"],
            ["zip(a, b)", "tuples of one item per input", "the shortest input is exhausted"],
        ],
    ),
]

LESSON["syntax"] = [
    MD("The canonical forms, each removing a hand-maintained counter."),
    CODE_CELL(
        "readings = (0.4, 0.9, 0.7)\n"
        "\n"
        "for index in range(len(readings)):\n"
        "    print(index, readings[index])       # indexing by hand\n"
        "\n"
        "for index, reading in enumerate(readings):\n"
        "    print(index, reading)               # the index comes for free"
    ),
    MD("The anti-pattern - zipping against a hand-built index range, which can truncate:"),
    CODE(
        "values = (0.4, 0.9, 0.7)\n"
        "for i, value in zip(range(len(values)), values):\n"
        "    ...                      # same result, more to get wrong\n"
        "\n"
        "for i, value in enumerate(values):\n"
        "    ...                      # the index cannot drift from the value",
        lang="text",
    ),
    WARN(
        "zip truncates silently",
        "zip stops at the shortest input without complaining. If two sequences are "
        "meant to correspond, pass strict=True so a mismatch raises instead of quietly "
        "discarding data.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - indices without a counter.**"),
    CODE_CELL(
        "commands = ('stop', 'hold', 'go')\n"
        "for step, command in enumerate(commands, start=1):\n"
        "    print(f'step {step}: {command}')"
    ),
    MD("**Example 2 - zipping two logs.**"),
    CODE_CELL(
        "timestamps = (0.0, 1.5, 3.0)\n"
        "battery = (100.0, 92.0, 88.0)\n"
        "for t, pct in zip(timestamps, battery):\n"
        "    print(f't={t:>4}s  battery={pct:.1f}%')"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "Enumerate is what keeps a log entry attached to the sample it came from, even "
        "when the batch is ragged and no single index would work."
    ),
    CODE_CELL(
        "batches = ((0.1, 0.2), (0.3,), (0.4, 0.5, 0.6))\n"
        "\n"
        "for step, batch in enumerate(batches):\n"
        "    print(f'batch {step}: {len(batch)} readings')"
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "`zip` is lazy and composable, so it streams rather than materialises. That "
        "matters when one side is a generator that should not be fully consumed - for "
        "example a live sensor stream paired with a fixed command schedule."
    ),
    CODE_CELL(
        "def readings(count: int):\n"
        "    for i in range(count):\n"
        "        yield round(0.5 + i * 0.1, 2)\n"
        "\n"
        "\n"
        "commands = ('start', 'log', 'stop')\n"
        "paired = zip(commands, readings(len(commands)))\n"
        "print('lazy zip:', list(paired))\n"
        "print('exhausted:', list(paired))"
    ),
    MD(
        "The second call is empty because the generator is now consumed. A lazily zipped "
        "stream can only be walked once, which is worth stating in a docstring whenever "
        "the result is not materialised immediately."
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "Below is a telemetry log builder. It pairs a timestamp sequence with a reading "
        "sequence, attaches 1-based step numbers, and refuses to build a log from "
        "mismatched data rather than silently truncating it."
    ),
    CODE_CELL(
        "\"\"\"telemetry.py - build a timestamped, step-numbered log.\"\"\"\n"
        "from __future__ import annotations\n"
        "\n"
        "SAMPLE_PERIOD_S = 0.5\n"
        "\n"
        "\n"
        "def build_log(readings, period_s: float = SAMPLE_PERIOD_S, strict: bool = True) -> list[dict]:\n"
        "    \"\"\"Return one dict per reading: step, t_s and value.\n"
        "\n"
        "    strict=True raises when the reading sequence contains a\n"
        "    non-numeric entry rather than quietly dropping it, because a\n"
        "    log that loses a sample is worse than one that fails loudly.\n"
        "    \"\"\"\n"
        "    log: list[dict] = []\n"
        "    for step, (t_s, value) in enumerate(\n"
        "        zip((index * period_s for index in range(len(readings))), readings, strict=strict)\n"
        "    ):\n"
        "        if not isinstance(value, (int, float)) or isinstance(value, bool):\n"
        "            if strict:\n"
        "                raise TypeError(f'step {step}: non-numeric reading {value!r}')\n"
        "            continue\n"
        "        log.append({'step': step, 't_s': round(t_s, 3), 'value': value})\n"
        "    return log"
    ),
    MD(
        "Two choices matter here. The timestamps come from a generator sized to the "
        "readings, so they can never be longer or shorter, and the numeric check is "
        "policy rather than accident: a malformed sample either raises or is skipped, "
        "and which one happens is stated in the docstring rather than left to chance. "
        "Together these remove the two ways a log of this kind usually goes quietly "
        "wrong, which is a truncated tail and a time base that drifts once a sample is "
        "dropped."
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "SAMPLE_PERIOD_S is a constant so the logging cadence is auditable without "
            "reading the loop.",
            "The timestamp generator is sized from len(readings), so it can never "
            "desynchronise from the values being logged.",
            "strict on zip is the default here because a truncated log is a silent "
            "defect, and a loud one is preferable.",
            "enumerate starts at zero, so the step number and the list index agree - "
            "adding 1 later would be a separate, explicit decision.",
            "The type check is placed before the append so a bad sample never reaches "
            "the log.",
            "strict decides whether a bad sample raises or is skipped, and the "
            "docstring states which, so the caller is never guessing.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - a range that drops the last element.**"),
    CODE(
        "values = (1, 2, 3)\n"
        "for i in range(len(values)):\n"
        "    ...            # correct, but awkward next to enumerate\n"
        "\n"
        "for i, value in enumerate(values):\n"
        "    ...            # the same three items, no counting",
        lang="text",
    ),
    MD("**Mistake 2 - assuming range includes its stop value.**"),
    CODE(
        "list(range(1, 4))    # [1, 2, 3] - 4 is NOT included\n"
        "len(range(1, 4))     # 3, not 4\n"
        "range(0, 10, 3)      # [0, 3, 6, 9] - stops before exceeding 10",
        lang="text",
    ),
    MD("**Mistake 3 - zip truncating without complaint.**"),
    CODE(
        "left = ('a', 'b', 'c')\n"
        "right = (1, 2)\n"
        "list(zip(left, right))                  # [(a,1), (b,2)] - c is lost\n"
        "list(zip(left, right, strict=True))     # raises ValueError",
        lang="text",
    ),
    MD("**Mistake 4 - a lazy zip consumed twice.**"),
    CODE(
        "paired = zip(a, b)\n"
        "list(paired)     # the first walk consumes the inputs\n"
        "list(paired)     # empty the second time",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "When a range-based loop visits the wrong elements, print the range itself. "
        "Seeing the exact sequence removes any guesswork about the exclusive stop."
    ),
    CODE_CELL(
        "print('range(1, 4) ->', list(range(1, 4)))\n"
        "print('range(0, 10, 3) ->', list(range(0, 10, 3)))\n"
        "print('len', len(range(1, 4)))"
    ),
    MD(
        "When a zip loses data, compare the lengths before trusting the pairing. A "
        "mismatch is the whole explanation in one line."
    ),
    CODE_CELL(
        "left = ('a', 'b', 'c')\n"
        "right = (1, 2)\n"
        "print('lengths:', len(left), len(right))\n"
        "print('paired :', list(zip(left, right)))\n"
        "try:\n"
        "    list(zip(left, right, strict=True))\n"
        "except ValueError as exc:\n"
        "    print('strict  :', exc)"
    ),
    NOTE(
        "len() on a range is O(1)",
        "range knows its own length without being materialised, so comparing len(range(n)) "
        "with len(sequence) is free even for very large n.",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Prefer enumerate over range(len(seq)) and indexing.",
            "Use range for counting, not for indexing a sequence.",
            "Remember the stop value of range is exclusive.",
            "Pass strict=True to zip when lengths are meant to correspond.",
            "Materialise a lazy zip once, and do not walk it twice.",
            "Generate the second side of a zip rather than slicing it.",
            "Keep enumerate and zip together readable; two levels of nesting is the limit.",
            "Name the pairing in a variable rather than repeating the zip call.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "All three built-ins are lazy, which is the performance point that matters. "
        "`range(10**9)` allocates nothing; it is a small object that computes each "
        "value when asked. `zip` likewise holds no intermediate list, so pairing two "
        "ten-million-element sequences costs one tuple per step rather than a "
        "materialised result."
    ),
    CODE_CELL(
        "big = range(10**9)\n"
        "print('len is O(1):', len(big))\n"
        "print('first three :', [next(iter(big))] and list(big)[:3])\n"
        "\n"
        "a = range(1_000_000)\n"
        "b = range(1_000_000)\n"
        "total = sum(1 for pair in zip(a, b) if pair[0] == pair[1])\n"
        "print('matching pairs:', total)"
    ),
    MD(
        "The practical consequence is that you should not materialise these results "
        "unless you need to. Wrapping a lazy generator in list() to \"be safe\" both "
        "costs memory and forecloses a second traversal, which is almost never what "
        "was wanted."
    ),
    TIP(
        "islice for early termination",
        "itertools.islice walks only as much of a lazy iterator as you ask for, so "
        "taking the first n zip pairs costs n steps rather than the whole sequence.",
    ),
]

LESSON["pythonic_approaches"] = [
    MD("Three hand-rolled loops against their built-in equivalents."),
    CODE_CELL(
        "values = (0.4, 0.9, 0.7)\n"
        "\n"
        "# before: a counter maintained alongside the data\n"
        "index = 0\n"
        "for value in values:\n"
        "    print(index, value)\n"
        "    index += 1\n"
        "\n"
        "# after: the index comes from the iteration\n"
        "for index, value in enumerate(values):\n"
        "    print(index, value)"
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "Pairing a rover's live battery trace with a fixed command schedule is exactly "
        "what zip is for - and exactly where silent truncation would be a safety "
        "problem rather than a curiosity."
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
        "schedule = ('start', 'log', 'hold', 'stop')\n"
        "battery = (robot.status()['battery_pct'] for _ in schedule)\n"
        "\n"
        "for step, (command, pct) in enumerate(zip(schedule, battery, strict=True), 1):\n"
        "    print(f'step {step}: {command:<6} battery {pct:.1f}%')"
    ),
]

LESSON["engineering_example"] = [
    MD(
        "A range is the right tool when you genuinely want indices - for example to "
        "produce move commands of a known length, where no sequence is being indexed."
    ),
    CODE_CELL(
        "def retry_delays(attempts: int, base_s: float = 0.5):\n"
        "    \"\"\"Exponential backoff as a range-driven generator.\"\"\"\n"
        "    for attempt in range(1, attempts + 1):\n"
        "        yield round(base_s * (2 ** (attempt - 1)), 3)"
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Print range(1, 4) and confirm the stop is excluded.",
            "Loop over a tuple with enumerate and print 1-based step numbers.",
            "Zip a three-item sequence with a two-item one and observe the truncation, "
            "then repeat with strict=True.",
            "Build a timestamp sequence with a generator and pair it with a reading list.",
        ]
    ),
    CODE_CELL(
        "print('range(1, 4):', list(range(1, 4)))\n"
        "\n"
        "for step, name in enumerate(('ada', 'grace'), start=1):\n"
        "    print('step', step, name)\n"
        "\n"
        "print('zip default:', list(zip((1, 2, 3), ('a', 'b'))))\n"
        "try:\n"
        "    list(zip((1, 2, 3), ('a', 'b'), strict=True))\n"
        "except ValueError as exc:\n"
        "    print('zip strict :', exc)\n"
        "\n"
        "times = (i * 0.5 for i in range(3))\n"
        "for t, value in zip(times, (0.1, 0.2, 0.3), strict=True):\n"
        "    print('log', t, value)"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: three handles onto the same data.** `range` is a counter that "
        "can be asked to yield its own index. `enumerate` is the data plus its position, "
        "fused into one object. `zip` is several data streams braided into one - but a "
        "braid that ends as soon as any strand runs out."
    ),
    TABLE(
        ["Built-in", "Answers the question", "Silent failure"],
        [
            ["range", "How many times?", "Forgetting the stop is exclusive"],
            ["enumerate", "Which item is this, and where?", "Off-by-one start values"],
            ["zip", "What goes with this item?", "Stops at the shortest input"],
        ],
    ),
]

TERMS = [
    ["range", "A lazy sequence of integers with an exclusive stop."],
    ["Exclusive stop", "range never produces its stop value."],
    ["enumerate", "Iterate an iterable yielding (index, value) pairs."],
    ["start", "The optional first index yielded by enumerate."],
    ["zip", "Iterate several iterables in step, stopping at the shortest."],
    ["strict", "A zip option that raises on a length mismatch."],
    ["Truncation", "Silent loss of the excess items of the longer input."],
    ["Lazy iterator", "An object that produces values on demand."],
    ["Generator", "A function that yields, producing a lazy iterator."],
    ["Pairing", "Attaching a value from one stream to a value from another."],
]

LESSON["summary"] = [
    MD(
        "`range`, `enumerate` and `zip` are not shorthand for the bookkeeping a loop "
        "normally needs - they remove the bookkeeping itself. A hand-maintained counter "
        "can drift from the data it indexes, whereas the index `enumerate` yields comes "
        "from the same iteration as the value, so the two cannot disagree. That is the "
        "argument for the built-in over the shorter-looking manual loop."
    ),
    MD(
        "Each carries one silent failure, and knowing it is the practical skill. `range` "
        "has an **exclusive stop**, so `range(1, 4)` yields three values rather than "
        "four, and an off-by-one there quietly drops the last element. `zip` stops at "
        "the **shortest** input, which is the safe default but discards the excess "
        "without complaint; `strict=True` turns that silent truncation into a `ValueError` "
        "that says exactly what was lost. And because all three are lazy, a result built "
        "with `zip` can be walked only once unless it is materialised first."
    ),
    MD(
        "For robotics work the difference is practical rather than stylistic. Pairing a "
        "rover's live battery trace with a fixed command schedule is what `zip` is for, "
        "and a truncated pairing in a mission log is a safety defect rather than an "
        "inconvenience. Generating the second stream - so its length is derived from the "
        "first - removes the mismatch instead of merely detecting it."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "Prefer enumerate over range(len(seq)) and indexing.",
            "Use range for counting, never for indexing a sequence.",
            "range stops exclusively; range(1, 4) has three values.",
            "zip stops at the shortest input, silently.",
            "Pass strict=True to zip when lengths must correspond.",
            "A lazy zip can be walked once; materialise it deliberately.",
            "Generate the second stream so lengths cannot disagree.",
            "Use zip to attach a value, not to build a list by hand.",
        ]
    ),
]

LESSON["further_exploration"] = [
    MD(
        "Read further: the official documentation for "
        "[`range`](https://docs.python.org/3/library/stdtypes.html#range), "
        "[`enumerate`](https://docs.python.org/3/library/functions.html#enumerate) "
        "and [`zip`](https://docs.python.org/3/library/functions.html#zip), plus "
        "[`itertools.islice`](https://docs.python.org/3/library/itertools.html#itertools.islice) "
        "for taking a prefix of a lazy iterator."
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Find a value's index with enumerate",
        difficulty="MEDIUM",
        learning_objectives=["Use enumerate instead of a counter.", "Report a not-found index."],
        concepts_tested=["enumerate", "search", "search"],
        problem_statement=(
            "Write `index_of(values, target)` returning the index of the first matching "
            "value, or None, using enumerate rather than a manual counter."
        ),
        requirements=["Use enumerate.", "Return the first match only."],
        constraints=["Do not use range(len(values))."],
        input_description="A sequence and a target.",
        expected_output="An index, or None.",
        example_input="index_of(('a', 'b', 'a'), 'a')",
        example_output="0",
        edge_cases=["An empty sequence returns None.", "Only the first match is returned."],
        hints=["Iterate enumerate(values) and return the index on a match."],
        success_criteria=["The example returns 0.", "An empty sequence returns None."],
        optional_extension="Return every matching index.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Take every other item with a stepped range",
        difficulty="MEDIUM",
        learning_objectives=["Use a range step.", "Respect the exclusive stop."],
        concepts_tested=["range", "slicing", "stepping"],
        problem_statement=(
            "Write `every_other(values)` returning the items at even indices, built "
            "with a stepped range rather than slicing."
        ),
        requirements=["Use range with a step of 2 starting at 0."],
        constraints=["Do not use values[::2]."],
        input_description="A sequence.",
        expected_output="A list.",
        example_input="every_other((1, 2, 3, 4, 5))",
        example_output="[1, 3, 5]",
        edge_cases=["An empty sequence gives an empty list.", "A one-item sequence gives one item."],
        hints=["range(0, len(values), 2) visits exactly the even indices."],
        success_criteria=["The example returns [1, 3, 5].", "range stepping is used."],
        optional_extension="Add a start parameter.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Pair commands with battery readings",
        difficulty="MEDIUM",
        learning_objectives=["Use zip.", "Detect a length mismatch."],
        concepts_tested=["zip", "strict", "validation"],
        problem_statement=(
            "Write `pair_commands(commands, readings, strict=True)` pairing each command "
            "with a reading. With strict set, a length mismatch must raise ValueError."
        ),
        requirements=["Use zip.", "Pass strict through to zip."],
        constraints=["Do not pad silently."],
        input_description="Two sequences of equal or differing length.",
        expected_output="A list of tuples, or ValueError.",
        example_input="pair_commands(('go',), (98.0,))",
        example_output="[('go', 98.0)]",
        edge_cases=["A mismatch raises ValueError when strict is True.", "strict False truncates silently."],
        hints=["zip(commands, readings, strict=strict) already raises for you."],
        success_criteria=["The example returns the pair.", "A mismatch raises when strict."],
        optional_extension="Return dicts instead of tuples.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Build a countdown with a negative step",
        difficulty="MEDIUM",
        learning_objectives=["Use a negative range step.", "Handle an empty range."],
        concepts_tested=["range", "stepping", "boundaries"],
        problem_statement=(
            "Write `countdown(n)` returning the integers from n down to 1 inclusive, "
            "using a negative range step."
        ),
        requirements=["Use a negative step.", "Include both n and 1."],
        constraints=["n of 0 or less gives an empty list."],
        input_description="A non-negative integer.",
        expected_output="A list of integers.",
        example_input="countdown(3)",
        example_output="[3, 2, 1]",
        edge_cases=["countdown(0) gives an empty list.", "countdown(1) gives [1]."],
        hints=["range(n, 0, -1) stops before 0, so 1 is the last value."],
        success_criteria=["The example returns [3, 2, 1].", "countdown(0) returns []."],
        optional_extension="Add a starting suffix such as 'launch'.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Zip two sequences with a fill value",
        difficulty="MEDIUM",
        learning_objectives=["Pad a short sequence.", "Use a generator for the fill."],
        concepts_tested=["zip", "itertools", "padding"],
        problem_statement=(
            "Write `zip_pad(a, b, fill=None)` pairing two sequences of different lengths, "
            "substituting `fill` for the missing items."
        ),
        requirements=["Pad the shorter sequence.", "Return a list of tuples."],
        constraints=["Do not build the padding by hand in a loop."],
        input_description="Two sequences of differing length.",
        expected_output="A list of tuples.",
        example_input="zip_pad((1, 2, 3), ('a',))",
        example_output="[(1, 'a'), (2, None), (3, None)]",
        edge_cases=["Two empty sequences give an empty list.", "Equal lengths need no padding."],
        hints=["itertools.zip_longest pads the short side for you."],
        success_criteria=["The example matches exactly.", "An empty pair gives []."],
        optional_extension="Pad with a distinct sentinel rather than None.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Run-length encode a sequence",
        difficulty="HARD",
        learning_objectives=["Group consecutive equal values.", "Use enumerate for counting."],
        concepts_tested=["enumerate", "grouping", "itertools"],
        problem_statement=(
            "Write `run_length(values)` returning `(value, count)` pairs for each run of "
            "consecutive equal values, using itertools.groupby."
        ),
        requirements=["Use groupby.", "Return a list of tuples."],
        constraints=["Empty input gives an empty list."],
        input_description="A sequence of comparable values.",
        expected_output="A list of (value, count) tuples.",
        example_input="run_length(('a', 'a', 'b', 'b', 'b'))",
        example_output="[('a', 2), ('b', 3)]",
        edge_cases=["Empty input gives an empty list.", "All equal gives one pair."],
        hints=["sum(1 for _ in group) counts each run."],
        success_criteria=["The example matches exactly.", "Empty input gives []."],
        optional_extension="Implement the same result without groupby.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Transpose a table with zip",
        difficulty="HARD",
        learning_objectives=["Use the star-unpack form of zip.", "Reject ragged input."],
        concepts_tested=["zip", "unpacking", "transformations"],
        problem_statement=(
            "Write `transpose(rows)` returning the columns as tuples, using zip with "
            "star unpacking, and rejecting ragged input."
        ),
        requirements=["Use zip(*rows).", "Raise ValueError for rows of differing length."],
        constraints=["No nested loops."],
        input_description="A sequence of equally long rows.",
        expected_output="A list of tuples, one per column.",
        example_input="transpose(((1, 2), (3, 4)))",
        example_output="[(1, 3), (2, 4)]",
        edge_cases=["An empty table gives an empty list.", "Ragged rows raise ValueError."],
        hints=["zip(*rows) takes the rows as separate arguments."],
        success_criteria=["The example matches exactly.", "Ragged rows raise ValueError."],
        optional_extension="Pad ragged rows before transposing.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Attach generated timestamps to readings",
        difficulty="HARD",
        learning_objectives=["Generate a matching stream.", "Validate while pairing."],
        concepts_tested=["zip", "generators", "validation"],
        problem_statement=(
            "Write `timestamped(readings, period_s)` returning `(t_s, value)` pairs with "
            "generated timestamps, skipping non-numeric readings without disturbing the "
            "time base."
        ),
        requirements=["Generate timestamps rather than slicing them.", "Skip non-numeric values."],
        constraints=["No hard-coded index loop.", "The period must be respected."],
        input_description="A sequence of readings and a period in seconds.",
        expected_output="A list of (float, number) tuples.",
        example_input="timestamped((0.1, 'x', 0.3), 0.5)",
        example_output="[(0.0, 0.1), (1.0, 0.3)]",
        edge_cases=["An empty sequence gives an empty list.", "All-junk input gives an empty list."],
        hints=["Timestamps come from enumerate over the readings, so skipping does not shift the clock."],
        success_criteria=["The example matches exactly.", "A skipped value does not shift later timestamps."],
        optional_extension="Raise instead of skipping when strict is set.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Build a mission log from a command schedule",
        difficulty="HARD",
        learning_objectives=["Pair a schedule with live readings.", "Fail loudly on mismatch."],
        concepts_tested=["zip", "strict", "simulator API"],
        problem_statement=(
            "Write `mission_log(robot, schedule)` returning one dict per command with "
            "`step`, `command` and `battery_pct`, pairing a fixed schedule with readings "
            "read from the simulator."
        ),
        requirements=["Use strict pairing so a mismatch raises.", "Read the battery from status()."],
        constraints=["Never silently truncate the log.", "Steps are 1-based."],
        input_description="A SimulatedRobot and a sequence of command names.",
        expected_output="A list of dicts.",
        example_input="mission_log(robot, ('start', 'stop'))",
        example_output="[{'step': 1, 'command': 'start', 'battery_pct': 100.0}, {'step': 2, 'command': 'stop', 'battery_pct': 100.0}]",
        edge_cases=["An empty schedule gives an empty log.", "The battery is read once per step."],
        hints=["Generate one reading per command so the lengths cannot disagree."],
        success_criteria=["The log has one dict per command.", "Steps start at 1."],
        optional_extension="Return the battery at the end of the mission as well.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Pair attempts with backoff delays",
        difficulty="HARD",
        learning_objectives=["Combine range with zip.", "Generate one stream from the other."],
        concepts_tested=["range", "zip", "generators"],
        problem_statement=(
            "Write `retry_plan(attempts, base_s=0.5)` returning `(attempt, delay_s)` pairs "
            "with exponential backoff, generating the attempt numbers with range."
        ),
        requirements=["Use range for the attempt numbers.", "Pair with the delays using zip."],
        constraints=["No hard-coded list of attempts.", "Delays double each attempt."],
        input_description="A positive attempt count and a base delay.",
        expected_output="A list of (int, float) tuples.",
        example_input="retry_plan(3)",
        example_output="[(1, 0.5), (2, 1.0), (3, 2.0)]",
        edge_cases=["Zero attempts gives an empty list.", "A negative count gives an empty list."],
        hints=["A generator that yields delays keeps the two streams in step by construction."],
        success_criteria=["The example matches exactly.", "Zero attempts gives an empty list."],
        optional_extension="Cap the delay at a maximum value.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "def index_of(values, target):\n"
            "    for index, value in enumerate(values):\n"
            "        if value == target:\n"
            "            return index\n"
            "    return None"
        ),
        explanation=(
            "enumerate supplies the index from the same iteration as the value, so the "
            "two cannot drift apart - the failure mode a hand-maintained counter has "
            "once a value is skipped."
        ),
        complexity="Time O(n); space O(1).",
        edge_cases="An empty sequence returns None without an error.",
        alternative_approaches="values.index(target) is the built-in, but it raises rather than returning None.",
        testing="assert index_of(('a', 'b', 'a'), 'a') == 0\nassert index_of((), 'a') is None",
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def every_other(values) -> list:\n"
            "    return [values[i] for i in range(0, len(values), 2)]"
        ),
        explanation=(
            "range(0, len(values), 2) produces exactly the even indices, and the "
            "exclusive stop means the last index is only included when it really is at "
            "an even position - which is the property that makes the step reliable."
        ),
        complexity="Time O(n); space O(n/2).",
        edge_cases="A one-item sequence returns that item; an empty sequence returns [].",
        alternative_approaches="values[::2] is the same result in one character pair.",
        testing="assert every_other((1, 2, 3, 4, 5)) == [1, 3, 5]\nassert every_other(()) == []\nassert every_other((9,)) == [9]",
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "def pair_commands(commands, readings, strict: bool = True) -> list[tuple]:\n"
            "    return list(zip(commands, readings, strict=strict))"
        ),
        explanation=(
            "zip's own strict mode is the check, so there is nothing to write. The value "
            "of the exercise is noticing that the silent default is a truncation that "
            "loses a command's reading without any signal."
        ),
        complexity="Time O(min(len(a), len(b))); space proportional to the result.",
        edge_cases="With strict False a mismatch truncates silently, which is the behaviour the exercise warns about.",
        alternative_approaches="A length check before zipping gives a clearer error message but races on generators.",
        testing="assert pair_commands(('go',), (98.0,)) == [('go', 98.0)]\nimport pytest\ntry:\n    pair_commands(('a', 'b'), (1,))\nexcept ValueError:\n    pass",
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "def countdown(n: int) -> list[int]:\n"
            "    return list(range(n, 0, -1))"
        ),
        explanation=(
            "The stop of 0 combined with a negative step is what makes 1 the final "
            "value: range stops before it would reach the stop, so 0 is never produced. "
            "A stop of 1 would drop the last element."
        ),
        complexity="Time O(n); space O(n).",
        edge_cases="countdown(0) gives an empty list, and so does a negative n.",
        alternative_approaches="range(n - 1, -1, -1) gives a 0-based countdown from n down to 0.",
        testing="assert countdown(3) == [3, 2, 1]\nassert countdown(0) == []\nassert countdown(1) == [1]",
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "from itertools import zip_longest\n"
            "\n"
            "\n"
            "def zip_pad(a, b, fill=None) -> list[tuple]:\n"
            "    return list(zip_longest(a, b, fillvalue=fill))"
        ),
        explanation=(
            "zip_longest is the explicit counterpart to zip: instead of stopping at the "
            "shortest input it pads it. Using it makes the padding decision visible in "
            "the call rather than hiding it behind a manual loop."
        ),
        complexity="Time O(max(len(a), len(b))).",
        edge_cases="Two empty sequences give an empty list.",
        alternative_approaches="Pad the shorter side by hand, then use plain zip.",
        testing="assert zip_pad((1, 2, 3), ('a',)) == [(1, 'a'), (2, None), (3, None)]\nassert zip_pad((), ()) == []",
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "from itertools import groupby\n"
            "\n"
            "\n"
            "def run_length(values) -> list[tuple]:\n"
            "    return [(value, sum(1 for _ in group)) for value, group in groupby(values)]"
        ),
        explanation=(
            "groupby yields runs, not individual items, which is exactly the abstraction "
            "this exercise is about. Counting each group with a small generator sum "
            "keeps the whole thing a single comprehension."
        ),
        complexity="Time O(n); space O(r) for r runs.",
        edge_cases="Empty input gives an empty list without special handling.",
        alternative_approaches="Tracking the previous value in a loop is the manual equivalent.",
        testing="assert run_length(('a', 'a', 'b', 'b', 'b')) == [('a', 2), ('b', 3)]\nassert run_length(()) == []",
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "def transpose(rows) -> list[tuple]:\n"
            "    rows = list(rows)\n"
            "    if not rows:\n"
            "        return []\n"
            "    if len({len(row) for row in rows}) != 1:\n"
            "        raise ValueError('rows must all be the same length')\n"
            "    return list(zip(*rows))"
        ),
        explanation=(
            "The star unpacking is the whole trick: zip(*rows) treats each row as a "
            "separate iterable and yields one column at a time. The length check comes "
            "first because zip would otherwise silently drop the short row's extras."
        ),
        complexity="Time O(rows * cols); space O(rows * cols).",
        edge_cases="An empty table returns an empty list rather than raising on the unpack.",
        alternative_approaches="itertools.zip_longest pads ragged rows instead of rejecting them.",
        testing="assert transpose(((1, 2), (3, 4))) == [(1, 3), (2, 4)]\nassert transpose(()) == []\ntry:\n    transpose(((1, 2), (3,)))\nexcept ValueError:\n    pass",
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "def timestamped(readings, period_s: float) -> list[tuple]:\n"
            "    pairs: list[tuple] = []\n"
            "    for index, value in enumerate(readings):\n"
            "        if isinstance(value, bool) or not isinstance(value, (int, float)):\n"
            "            continue\n"
            "        pairs.append((round(index * period_s, 6), value))\n"
            "    return pairs"
        ),
        explanation=(
            "Taking the timestamp from the index before the skip is deliberate: the time "
            "base describes when the sample was taken, so a dropped reading must leave a "
            "gap rather than shift every later time. Slicing the readings to build times "
            "would have produced the wrong answer here."
        ),
        complexity="Time O(n); space O(n).",
        edge_cases="All-junk input gives an empty list with no timestamps consumed.",
        alternative_approaches="A generator expression is the streaming form of the same idea.",
        testing="assert timestamped((0.1, 'x', 0.3), 0.5) == [(0.0, 0.1), (1.0, 0.3)]\nassert timestamped((), 0.5) == []",
    )
)

SOLUTIONS.append(
    solution(
        number=9,
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
            "def mission_log(robot, schedule) -> list[dict]:\n"
            "    \"\"\"One dict per command, pairing the schedule with a live reading.\"\"\"\n"
            "    battery = (robot.status()['battery_pct'] for _ in schedule)\n"
            "    return [\n"
            "        {'step': step, 'command': command, 'battery_pct': round(pct, 2)}\n"
            "        for step, (command, pct) in enumerate(zip(schedule, battery, strict=True), 1)\n"
            "    ]"
        ),
        explanation=(
            "The battery stream is generated from the schedule, so it is exactly as long "
            "as the commands and the two can never disagree - strict is then belt and "
            "braces rather than the primary defence. enumerate with start=1 makes the "
            "step numbers match what an operator calls step 1."
        ),
        complexity="Time O(len(schedule)); space O(len(schedule)).",
        edge_cases="An empty schedule gives an empty log and reads the battery zero times.",
        alternative_approaches="Reading the battery once and reusing it is faster but records a fiction.",
        testing="robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\nlog = mission_log(robot, ('start', 'stop'))\nassert [row['step'] for row in log] == [1, 2]\nassert mission_log(robot, ()) == []",
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "def retry_plan(attempts: int, base_s: float = 0.5) -> list[tuple]:\n"
            "    if attempts < 0:\n"
            "        raise ValueError('attempts must not be negative')\n"
            "    numbers = range(1, attempts + 1)\n"
            "    delays = (round(base_s * (2 ** (attempt - 1)), 6) for attempt in numbers)\n"
            "    return list(zip(numbers, delays, strict=True))"
        ),
        explanation=(
            "range produces the attempt numbers and the generator derives one delay per "
            "attempt, so the streams cannot disagree in length. strict=True still guards "
            "the pairing, and the generator stays lazy until list() consumes it."
        ),
        complexity="Time O(attempts); space O(attempts).",
        edge_cases="Zero attempts gives an empty list; a negative count raises ValueError.",
        alternative_approaches="An explicit loop is clearer when the delay has a cap applied per step.",
        testing="assert retry_plan(3) == [(1, 0.5), (2, 1.0), (3, 2.0)]\nassert retry_plan(0) == []",
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
            "SAMPLE_PERIOD_S = 0.5\n"
            "\n"
            "\n"
            "def build_mission_log(robot, readings, period_s: float = SAMPLE_PERIOD_S) -> dict:\n"
            "    \"\"\"Log a fixed reading batch against a live battery trace.\"\"\"\n"
            "    battery = (robot.status()['battery_pct'] for _ in readings)\n"
            "    entries: list[dict] = []\n"
            "    for step, (value, pct) in enumerate(zip(readings, battery, strict=True), 1):\n"
            "        if isinstance(value, bool) or not isinstance(value, (int, float)):\n"
            "            continue\n"
            "        entries.append({\n"
            "            'step': step,\n"
            "            't_s': round((step - 1) * period_s, 3),\n"
            "            'value': value,\n"
            "            'battery_pct': round(pct, 2),\n"
            "        })\n"
            "    return {'period_s': period_s, 'entries': entries}"
        ),
        explanation=(
            "The battery stream is generated from the readings, so strict pairing has "
            "nothing to catch and a truncated log is impossible by construction rather "
            "than by checking. The validation test happens after the pairing so a "
            "malformed reading still consumed its step, which keeps the log's step "
            "numbers aligned with the batch indices."
        ),
        complexity="Time O(len(readings)); space O(len(readings)).",
        edge_cases="An empty batch gives an empty entries list and reads the battery zero times.",
        alternative_approaches="Building a dict of columns then zipping is faster to write and harder to read.",
        testing="robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\nout = build_mission_log(robot, (0.1, 0.2))\nassert [e['step'] for e in out['entries']] == [1, 2]\nassert build_mission_log(robot, ())['entries'] == []",
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="What does `list(range(1, 4))` produce?",
        choices=[
            "[1, 2, 3]",
            "[1, 2, 3, 4]",
            "[0, 1, 2, 3]",
            "[1, 2, 3, 4, 5]",
        ],
        answer=0,
        kind="code_output",
        explanation=(
            "The stop is exclusive, so 4 is never produced. This single property causes "
            "most off-by-one errors in range-based loops."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="Which statement about range is true?",
        choices=[
            "It builds a list immediately, so len() is O(n).",
            "It always starts at 1.",
            "It cannot be used with a negative step.",
            "It is lazy, so range(10**9) is instant and costs nothing until iterated.",
        ],
        answer=3,
        kind="conceptual",
        explanation=(
            "range computes each value on demand and knows its own length without "
            "materialising, so both construction and len() are effectively free. A "
            "negative step is fully supported and is how a countdown is written."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="Why prefer `enumerate(seq)` over `range(len(seq))`?",
        choices=[
            "Because enumerate is faster in every case.",
            "Because range cannot index a sequence.",
            "Because the index comes from the same iteration, so it cannot drift from the value.",
            "Because enumerate allows a negative step.",
        ],
        answer=2,
        kind="reasoning",
        explanation=(
            "A hand-maintained counter drifts whenever a value is skipped. enumerate "
            "derives the index from the iteration itself, so the pairing is structural "
            "rather than something the programmer maintains."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="What does `zip` do when its inputs have different lengths?",
        choices=[
            "It raises ValueError immediately.",
            "It pads the shorter input with None.",
            "It stops at the shortest input and discards the excess silently.",
            "It repeats the shorter input until both are exhausted.",
        ],
        answer=2,
        kind="code_output",
        explanation=(
            "The default is the safe one - a mismatch truncates rather than crashes - but "
            "it is silent, which is why strict=True exists to turn the truncation into a "
            "loud ValueError."
        ),
        reference="lesson.ipynb - Syntax",
    )
)

QUIZ.append(
    quiz(
        question="What does `zip(a, b, strict=True)` do on a length mismatch?",
        choices=[
            "It raises a ValueError naming the mismatch.",
            "It truncates, as the default does.",
            "It pads the shorter input with None.",
            "It returns an empty result.",
        ],
        answer=0,
        kind="reasoning",
        explanation=(
            "strict=True makes the assumption explicit: it raises a ValueError naming how "
            "far the two diverged, so the defect is locatable rather than merely detected."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="Which construct gives both an index and a value without counting?",
        choices=[
            "range(len(seq))",
            "enumerate(seq)",
            "zip(range(len(seq)), seq)",
            "reversed(seq)",
        ],
        answer=1,
        kind="implementation_choice",
        explanation=(
            "enumerate is the built-in for exactly this. The third option produces the "
            "same pairs but constructs them by hand, which is the bookkeeping the "
            "built-in exists to remove."
        ),
        reference="lesson.ipynb - Pythonic Approaches",
    )
)

QUIZ.append(
    quiz(
        question="What does `list(transpose_rows)` give after a second full walk?",
        choices=[
            "The same rows again.",
            "An empty result, because the first walk consumed the inputs.",
            "Only the first row.",
            "A ValueError, because the streams are exhausted.",
        ],
        answer=1,
        kind="debugging",
        explanation=(
            "A lazy zip holds no result of its own: walking it drives the underlying "
            "iterators forward, and once they are exhausted there is nothing left. "
            "Materialising with list() is the deliberate fix."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="Why must the timestamp come from the index rather than from a counter of kept readings?",
        choices=[
            "It is faster to compute.",
            "Because range cannot be combined with a skip.",
            "Because enumerate only works on numbers.",
            "So a skipped reading leaves a time gap instead of shifting every later time.",
        ],
        answer=3,
        kind="robotics",
        explanation=(
            "A timestamp records when a sample was taken, not when it happened to be "
            "stored. Counting only the kept readings compresses the time base and makes "
            "every later log entry wrong by an increasing amount."
        ),
        reference="exercises.ipynb - Exercise 8",
    )
)

QUIZ.append(
    quiz(
        question="Why is `range(10**9)` created instantly?",
        choices=[
            "Because range stores a formula and computes each value only when asked.",
            "Because Python skips large ranges.",
            "Because it is an empty object until iterated.",
            "Because 10**9 is a small number.",
        ],
        answer=0,
        kind="reasoning",
        explanation=(
            "range is lazy: it holds its start, stop and step, and derives each value on "
            "demand. It is neither precomputed nor a generator, which is why it can "
            "still report its own length in constant time."
        ),
        reference="lesson.ipynb - Performance Considerations",
    )
)

QUIZ.append(
    quiz(
        question="Which pairing is the safest way to log a fixed batch against live readings?",
        choices=[
            "zip(batch, live_readings) with no strict flag.",
            "index live_readings[i] inside a range(len(batch)) loop.",
            "zip(batch, (read_once for _ in batch), strict=True).",
            "zip(batch, live_readings, strict=False).",
        ],
        answer=2,
        kind="implementation_choice",
        explanation=(
            "Generating one reading per item makes the lengths agree by construction, so "
            "truncation is impossible rather than merely detectable, and strict=True keeps "
            "the check in place as a second line of defence."
        ),
        reference="solution.ipynb - Solution 11",
    )
)

RESEARCH = {
    "question": (
        "How much does generating the second stream of a zip cost compared with "
        "slicing it first?"
    ),
    "hypothesis": (
        "Generating the second stream is at least as fast as slicing and uses "
        "constant extra memory, so it should match or beat the slicing version."
    ),
    "experiment": [
        STEPS(
            [
                "Build two sequences of 500000 numeric items.",
                "Time a zip that slices the second sequence up front.",
                "Time a zip whose second stream is a generator expression.",
                "Run each ten times and record every raw measurement.",
            ]
        ),
    ],
    "data": [
        CODE_CELL(
            "# Record your raw timings - one row per variant per run.\n"
            "# Copy real values from your actual runs; do not invent them.\n"
            "#\n"
            "# | variant | run | seconds |"
        ),
    ],
    "analysis": [
        MD(
            "Compare the two distributions. The hypothesis predicts the generator is no "
            "slower, because building the slice costs a full pass and an allocation that "
            "the generator avoids."
        ),
    ],
    "result": [
        MD(
            "State the observed difference and whether it was within run-to-run noise. "
            "Report any run where the slicing version was faster rather than discarding "
            "it."
        ),
    ],
    "interpretation": [
        MD(
            "Explain the memory difference as well as the time, since a 500000-item slice "
            "is a real allocation. Name at least two threats to validity, including "
            "garbage collection timing."
        ),
    ],
    "conclusion": [
        MD(
            "Give your verdict: when is generating a stream worth it, and when would "
            "slicing be acceptable?"
        ),
    ],
    "extensions": [
        "Compare both against itertools.islice for a prefix of the sequence.",
        "Measure the cost of materialising the zip with list() in each variant.",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Step-Indexed Mission Log",
    "context": (
        "A mission log must pair a fixed reading batch with a live battery trace. The "
        "log must never silently lose a step, and a malformed reading must not shift "
        "the timestamps of everything after it."
    ),
    "mission": (
        "Implement `build_mission_log(robot, readings, period_s)` returning a log whose "
        "steps are 1-based and whose timestamps come from the batch index."
    ),
    "requirements": [
        "Pair readings with a generated battery stream using strict=True.",
        "Derive each timestamp from the step index, not from a kept-reading counter.",
        "Skip malformed readings without renumbering later steps.",
        "Return the period alongside the entries.",
    ],
    "constraints": [
        "Never truncate the log silently.",
        "The step numbers must match the batch indices exactly.",
        "Complete well inside the 10 ms control budget per log build.",
    ],
    "interface": "def build_mission_log(robot, readings, period_s=0.5) -> dict:",
    "success_criteria": [
        "A clean batch logs one entry per reading with steps 1..n.",
        "A malformed reading is skipped and later steps keep their original numbers.",
        "The battery in every entry comes from a real status() call.",
    ],
    "extension": (
        "Add a mode that raises on a malformed reading rather than skipping it, and "
        "state which mode a mission supervisor should prefer."
    ),
}

MINI_PROJECT = {
    "title": "Mini-Project: Step-Indexed Telemetry Log",
    "brief": (
        "Build a telemetry logger that pairs a reading batch with a live battery "
        "trace, numbers its steps, and refuses to lose a sample silently."
    ),
    "scenario": (
        "A rover records a batch during a mission. Readings can be malformed, and a log "
        "that silently drops or renumbers a step is worse than one that fails loudly."
    ),
    "rationale": (
        "This is where the three built-ins meet: enumerate for step numbers, range for "
        "the time base, and zip with strict=True for pairing."
    ),
    "requirements": [
        "Pair each reading with a generated battery reading using strict=True.",
        "Number steps from 1 with enumerate(start=1).",
        "Derive timestamps from the step index so a skipped reading leaves a gap.",
        "Skip malformed readings, and offer a strict mode that raises instead.",
    ],
    "constraints": [
        "Standard library only.",
        "No hand-maintained counter.",
        "The log must never be silently truncated.",
    ],
    "deliverables": [
        "`telemetry.py` with the logger and both modes.",
        "`test_telemetry.py` with at least twelve assertions.",
        "A README section explaining the timestamp rule and why it is not optional.",
    ],
    "steps": [
        "Implement build_mission_log(robot, readings, period_s).",
        "Test a clean batch, a batch with junk, and an empty batch.",
        "Add the strict mode and test that it raises on the same input.",
        "Add a test asserting that a skipped reading leaves a gap in the timestamps.",
    ],
    "expected_behavior": (
        "A clean batch logs one entry per reading. A batch with junk logs the rest with "
        "their original step numbers and a gap in the time base."
    ),
    "acceptance": [
        "All assertions pass from a clean run.",
        "Step numbers always match the batch indices.",
        "The truncation guard is tested by deliberately mismatching a stream.",
        "The timestamp rule is stated in the docstring.",
    ],
    "extensions": [
        "Add a rolling average of the battery across the logged steps.",
        "Return the log as a lazy iterator instead of a list, and test single-walk use.",
        "Compare the generated stream against a sliced one and report the timings.",
    ],
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Replace hand-maintained counters with enumerate as a habit.",
        "Make the exclusive stop of range concrete before anything else.",
        "Turn silent zip truncation into something students can hear.",
    ],
    "misconceptions": [
        [
            "range includes its stop value.",
            "The stop is exclusive; range(1, 4) has three values.",
        ],
        [
            "range builds a list, so a big range is expensive.",
            "It is lazy and knows its own length in constant time.",
        ],
        [
            "zip pads the shorter input with None.",
            "That is zip_longest; plain zip stops at the shortest input.",
        ],
        [
            "enumerate is just tidier style.",
            "It removes a whole class of index-desynchronisation bug.",
        ],
    ],
    "difficult_concepts": [
        "Accepting that a lazy zip can only be walked once.",
        "Deriving a timestamp from the index rather than from a kept-items counter.",
        "Seeing strict=True as detection rather than as a fix.",
    ],
    "demonstrations": [
        "Print range(1, 4) and range(0, 10, 3) and have the class call out the stop.",
        "Build a zip over mismatched inputs, then repeat with strict=True and read the "
        "error message.",
        "Walk a lazy zip twice to show the second result is empty.",
    ],
    "discussion": [
        "Is silent truncation ever the right default?",
        "When should a malformed reading raise rather than be skipped?",
    ],
    "student_errors": [
        [
            "The last element is missing",
            "The range stop was treated as inclusive",
            "Step the range or use enumerate",
        ],
        [
            "Log entries shift after a dropped reading",
            "Timestamps came from a counter of kept readings",
            "Take the time from the index before the skip",
        ],
        [
            "A log is shorter than the batch",
            "zip truncated the two streams",
            "Generate the second stream and use strict=True",
        ],
    ],
    "pacing": (
        "75 minutes of lesson with the live demonstrations, then 2 hours of exercises. "
        "Exercise 8 is the pivot of the topic: the timestamp rule is the idea that "
        "carries into the data-handling modules later in the course."
    ),
    "extensions": [
        "Ask students to prove the timestamp rule with a failing test before the fix.",
        "Have them convert a sliced second stream into a generated one and time both.",
    ],
    "assessment": (
        "Grade against rubric.md. Exercises 8, 9 and 10 carry the signal: they require "
        "an index-derived time base, strict pairing, and a generated stream."
    ),
    "support": (
        "Provide the solution for exercise 2 and ask students to rewrite it as a "
        "stepped range over a different start value, so the stop and step are explicit."
    ),
    "extension_fast": (
        "Ask for a short note on when a lazy iterator is worth materialising with list()."
    ),
}

RUBRIC = {
    "artifacts": [
        ["exercises.ipynb", "40%", "All 10 exercises implemented and edge-cased."],
        ["mini_project.ipynb", "25%", "telemetry.py plus its test suite."],
        ["robotics_challenge.ipynb", "25%", "Log never truncates silently."],
        ["research.ipynb", "10%", "Real measurements with a defensible conclusion."],
    ],
    "criteria": [
        ["Correctness", "30", "Steps, timestamps and pairing all agree."],
        ["Idiom", "25", "enumerate, range and zip are used rather than hand-rolled."],
        ["Code quality", "25", "PEP 8 naming, docstrings, small focused functions."],
        ["Reasoning", "20", "Truncation and laziness explained in writing."],
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
            "Every exercise implemented, the log cannot truncate silently, and a dropped "
            "reading leaves a gap rather than renumbering later steps.",
        ],
        [
            "Merit",
            "Most exercises correct; the log is built with a hand-maintained counter and "
            "the drift case is untested.",
        ],
        [
            "Pass",
            "Core requirements met, but the two streams are zipped without strict and a "
            "deliberate mismatch is not detected.",
        ],
        [
            "Fail",
            "The log is shorter than the batch and the lost steps are never reported.",
        ],
    ],
}

TOPIC = topic(
    topic_id="2.5",
    title="range, enumerate and zip",
    module=2,
    module_title="Control Flow and Loops",
    directory="05_range_enumerate_zip",
    summary=(
        "Three built-ins that remove the bookkeeping loops force on you, and the one "
        "silent failure each of them can still produce."
    ),
    why_it_matters=(
        "A mission log that silently drops a step, or shifts every timestamp after a "
        "dropped reading, is a safety defect rather than a cosmetic one. These built-ins "
        "exist because the manual versions of these loops get this wrong."
    ),
    objectives=[
        "Use enumerate instead of a hand-maintained counter and manual indexing.",
        "Explain why the stop value of range is exclusive.",
        "State why range is lazy and why that matters for large bounds.",
        "Predict what zip does when its inputs differ in length.",
        "Use strict=True to convert a silent truncation into a loud failure.",
        "Derive a time base from the data index so a dropped item leaves a gap.",
    ],
    prerequisites=["Topic 2.4 Nested Loops and Common Patterns"],
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
    robo_x_milestone="M2",
    robo_x_package="robo_x.core",
)
