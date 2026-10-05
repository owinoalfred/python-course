"""Topic 2.3 - Loop Control.

Hand-authored to the Course Content Standard. The spine: break, continue and the
under-used loop else let a loop say something about *how* it finished, which is
usually more expressive than a flag variable.
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
        "`break` leaves the innermost loop immediately. `continue` jumps to the next "
        "iteration, skipping whatever remains of the body. Both act on the *innermost* "
        "loop only, which is the single most important fact about them: in nested loops "
        "a `break` exits the inner loop and the outer one carries on."
    ),
    CODE_CELL(
        "readings = [0.4, -1.0, 0.9, 0.0, 0.7]\n"
        "\n"
        "for reading in readings:\n"
        "    if reading < 0:\n"
        "        continue          # skip this sample, keep scanning\n"
        "    if reading > 0.95:\n"
        "        break              # stop entirely\n"
        "    print(f'  usable: {reading}')\n"
        "\n"
        "print('scanned the whole list')"
    ),
    MD(
        "The third form is the one beginners never meet: an `else` clause on a loop "
        "runs **only when the loop finished without a `break`**. That turns "
        "\"did I find it?\" into a statement of the loop itself rather than a flag "
        "variable set afterwards."
    ),
    CODE_CELL(
        "def find_dock(readings, threshold: float = 0.5):\n"
        "    for index, reading in enumerate(readings):\n"
        "        if reading > threshold:\n"
        "            return index\n"
        "    else:\n"
        "        return None      # only reached if no break-equivalent fired\n"
        "\n"
        "\n"
        "print(find_dock([0.1, 0.2, 0.9]))\n"
        "print(find_dock([0.1, 0.2]))"
    ),
    NOTE(
        "for/else and while/else",
        "Both forms support the else clause. It is attached to the loop, not to the "
        "if, so it is easy to misread - indent it visibly in real code and add a "
        "comment naming what 'no break' means here.",
    ),
]

LESSON["formal_theory"] = [
    MD(
        "The `else` clause on a loop is not the `else` of an `if`. It is a completion "
        "handler: it runs when the loop exhausts its sequence, or when a while "
        "condition first becomes false. If the loop exits through `break`, or by "
        "`return`, the `else` is skipped entirely. That makes it a direct expression of "
        "\"the loop searched the whole space\"."
    ),
    EQUATION(
        "for x in seq:  ...  else: <runs only if no break and no return>"
    ),
    MD(
        "The two exit routes through a loop body are therefore different in kind. "
        "`return` leaves the *function*, unwinding everything; `break` leaves only the "
        "innermost loop and execution continues immediately afterwards. Choosing the "
        "wrong one is a common source of code that appears to work and quietly skips the "
        "rest of the function."
    ),
    CODE_CELL(
        "def first_over(values, limit):\n"
        "    for value in values:\n"
        "        if value > limit:\n"
        "            return value        # leaves the function, skips the else\n"
        "    else:\n"
        "        return 'none found'\n"
        "\n"
        "\n"
        "print(first_over([1.0, 5.0], 3.0))\n"
        "print(first_over([1.0, 2.0], 3.0))"
    ),
    TABLE(
        ["Statement", "Leaves", "Runs the loop else?"],
        [
            ["`break`", "the innermost loop", "no"],
            ["`continue`", "nothing - next iteration", "yes, if the loop ends normally"],
            ["`return`", "the whole function", "no"],
            ["loop completes", "nothing", "yes"],
        ],
    ),
]

LESSON["syntax"] = [
    MD(
        "The canonical form: one `continue` for the skip case, one `break` for the "
        "search case, and an `else` for the not-found case."
    ),
    CODE_CELL(
        "def first_fault(readings, limit: float):\n"
        "    for index, reading in enumerate(readings):\n"
        "        if reading is None:\n"
        "            continue            # missing sample: not a fault\n"
        "        if reading > limit:\n"
        "            return index        # found it\n"
        "    else:\n"
        "        return None              # scanned everything, found nothing\n"
        "\n"
        "\n"
        "print(first_fault([0.1, 0.8], 0.5))\n"
        "print(first_fault([0.1, 0.2], 0.5))"
    ),
    MD("The anti-pattern - a flag variable doing what the else clause already does:"),
    CODE(
        "found = False\n"
        "for reading in readings:\n"
        "    if reading > limit:\n"
        "        found = True\n"
        "        break\n"
        "if not found:            # the same statement, pushed outside\n"
        "    report('none')\n"
        "\n"
        "for reading in readings:\n"
        "    if reading > limit:\n"
        "        break\n"
        "else:\n"
        "    report('none')        # the loop says it directly",
        lang="text",
    ),
    WARN(
        "break only leaves one loop",
        "In a nested loop a break exits the inner loop only. Reaching the outer loop "
        "from the inner one requires restructuring or a flag - which is usually a sign "
        "the function wants to be split.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - filtering with continue.**"),
    CODE_CELL(
        "readings = [0.4, None, 0.9, -0.1, 0.7]\n"
        "usable = 0.0\n"
        "skipped = 0\n"
        "for reading in readings:\n"
        "    if reading is None:\n"
        "        skipped += 1\n"
        "        continue\n"
        "    usable += reading\n"
        "print(f'sum {usable:.2f} from {len(readings) - skipped} samples')"
    ),
    MD("**Example 2 - searching with break.**"),
    CODE_CELL(
        "queue = ['a', 'b', 'shutdown', 'c', 'd']\n"
        "for index, item in enumerate(queue):\n"
        "    if item == 'shutdown':\n"
        "        print(f'stopping at position {index}')\n"
        "        break\n"
        "else:\n"
        "    print('queue drained without a shutdown command')\n"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "Scanning a grid for the first obstacle is the canonical early-exit search: "
        "the moment you find it, nothing else in the grid matters."
    ),
    CODE_CELL(
        "GRID = (\n"
        "    (0, 0, 0, 0),\n"
        "    (0, 1, 0, 0),\n"
        "    (0, 0, 1, 0),\n"
        ")\n"
        "\n"
        "\n"
        "def first_obstacle(grid):\n"
        "    for row_index, row in enumerate(grid):\n"
        "        for col_index, cell in enumerate(row):\n"
        "            if cell:\n"
        "                return (row_index, col_index)\n"
        "    return None\n"
        "\n"
        "\n"
        "print('first obstacle at', first_obstacle(GRID))\n"
        "print('clear grid      ', first_obstacle(((0, 0), (0, 0))))"
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "When you genuinely need to leave *both* loops, the options are a flag, a helper "
        "function that returns, or a flattened iteration. Returning is usually the "
        "clearest, because the search becomes a value rather than a control-flow "
        "problem."
    ),
    CODE_CELL(
        "def find_pair(grid, target):\n"
        "    \"\"\"Return the first (row, col) whose value equals target.\"\"\"\n"
        "    for row_index, row in enumerate(grid):\n"
        "        for col_index, cell in enumerate(row):\n"
        "            if cell == target:\n"
        "                return row_index, col_index\n"
        "    return None\n"
        "\n"
        "\n"
        "print(find_pair(((1, 2), (3, 4)), 3))    # (1, 0)\n"
        "print(find_pair(((1, 2), (3, 4)), 9))    # None"
    ),
    MD(
        "The same problem with a flag is correct but harder to read, because the reader "
        "must track a variable modified inside two levels of nesting. In robotics code "
        "the helper-and-return form is almost always the better trade."
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "Below is a fault scanner for an underground inspection rover. It walks a "
        "telemetry batch, skips unusable samples, stops at the first real fault, and "
        "reports whether the whole batch was clean."
    ),
    CODE_CELL(
        "\"\"\"scanner.py - find the first genuine fault in a telemetry batch.\"\"\"\n"
        "from __future__ import annotations\n"
        "\n"
        "MAX_TEMPERATURE_C = 60.0\n"
        "MAX_TILT_DEG = 20.0\n"
        "\n"
        "\n"
        "def scan(batch, max_temp=MAX_TEMPERATURE_C, max_tilt=MAX_TILT_DEG) -> dict:\n"
        "    \"\"\"Return the first fault found, or report a clean batch.\n"
        "\n"
        "    Samples that are None or non-numeric are skipped rather than\n"
        "    treated as faults, so a dead sensor does not stop the rover.\n"
        "    \"\"\"\n"
        "    for index, sample in enumerate(batch):\n"
        "        if not isinstance(sample, dict):\n"
        "            continue\n"
        "        temp = sample.get('temperature_c')\n"
        "        tilt = sample.get('tilt_deg')\n"
        "        if temp is not None and temp > max_temp:\n"
        "            return {'fault': 'overheating', 'index': index}\n"
        "        if tilt is not None and tilt > max_tilt:\n"
        "            return {'fault': 'tilted', 'index': index}\n"
        "    else:\n"
        "        return {'fault': None, 'index': None}\n"
        "    return {'fault': 'unreachable', 'index': None}"
    ),
    MD(
        "The trailing `return` exists only to satisfy readers and type checkers: the "
        "`else` always returns, so it is genuinely unreachable. The `continue` for "
        "non-dict samples is the safety-relevant line - a malformed batch entry must not "
        "be reported as an overheating rover."
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "The thresholds are module constants so the safety policy is auditable "
            "without reading the loop.",
            "Skipping non-dict samples with continue keeps a malformed batch entry from "
            "being reported as a hardware fault.",
            "Each fault test returns immediately, so the reported index is the *first* "
            "genuine fault rather than the last one examined.",
            "Using is not None rather than a truthiness test keeps a legitimate reading "
            "of zero from counting as a missing value.",
            "The else clause expresses 'scanned the whole batch without finding "
            "anything', which a flag variable would have to be initialised for.",
            "The final return is unreachable and exists only for readers and type "
            "checkers - a normal, honest pattern in a function that always returns.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - expecting the loop else to run after a return.**"),
    CODE(
        "for value in values:\n"
        "    if value > limit:\n"
        "        return value      # leaves the function; the else never runs\n"
        "else:\n"
        "    return None\n"
        "\n"
        "for value in values:\n"
        "    if value > limit:\n"
        "        break             # leaves the loop only; the else is skipped\n"
        "else:\n"
        "    report('not found')",
        lang="text",
    ),
    MD("**Mistake 2 - assuming break leaves both loops.**"),
    CODE(
        "for row in grid:\n"
        "    for cell in row:\n"
        "        if cell == target:\n"
        "            break         # leaves the inner loop only\n"
        "    # the outer loop carries straight on",
        lang="text",
    ),
    MD("**Mistake 3 - a flag variable that is never reset.**"),
    CODE(
        "found = False\n"
        "for batch in batches:\n"
        "    for sample in batch:\n"
        "        if fault(sample):\n"
        "            found = True\n"
        "            break\n"
        "    if not found:   # never reset between batches\n"
        "        continue",
        lang="text",
    ),
    MD("**Mistake 4 - using continue where break was meant.**"),
    CODE(
        "for reading in readings:\n"
        "    if reading > limit:\n"
        "        continue          # keeps scanning instead of stopping\n"
        "\n"
        "for reading in readings:\n"
        "    if reading > limit:\n"
        "        break              # stop at the first offending sample",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "When a loop-control bug is suspected, the question is always *which loop did "
        "it leave?* Instrumenting with a counter makes the exit path visible."
    ),
    CODE_CELL(
        "grid = ((0, 0), (0, 0))\n"
        "for row_index, row in enumerate(grid):\n"
        "    for col_index, cell in enumerate(row):\n"
        "        if cell == 99:\n"
        "            print(f'  break exits at row {row_index} col {col_index}')\n"
        "            break\n"
        "    else:\n"
        "        print(f'  row {row_index} had no match')\n"
        "else:\n"
        "    print('  whole grid scanned, no match')"
    ),
    MD(
        "A loop that never terminates when a break is expected usually has a condition "
        "that no longer holds by the time it is tested. Printing the value the break "
        "tests shows the change that was not anticipated."
    ),
    CODE_CELL(
        "limit = 0.5\n"
        "for reading in (0.1, 0.9, 0.2):\n"
        "    if reading > limit:\n"
        "        print(f'  breaking on {reading} > {limit}')\n"
        "        break\n"
        "    limit = 0.05   # the limit moves, so later reads may not trigger\n"
        "else:\n"
        "    print('  no break fired')"
    ),
    NOTE(
        "The else clause is easy to misread",
        "Because `else` belongs to the loop rather than to the `if`, it is worth "
        "commenting: `# no break: the search completed` is often worth more than the "
        "indentation.",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Use `continue` to skip an unwanted item; use `break` to stop searching.",
            "Use the loop `else` instead of a flag variable for not-found cases.",
            "Remember `break` leaves only the innermost loop.",
            "Prefer returning from a helper over a flag set inside nested loops.",
            "Add a comment to any loop else, since it is easy to misread.",
            "Do not assume a loop else runs after a `return` from the body.",
            "Keep the loop body short enough that the control flow is visible.",
            "Test the not-found path explicitly; it is the one that is usually missing.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "Early exit is a real optimisation, not just tidier code. A search that breaks "
        "on the first match examines one element; one that scans the whole sequence "
        "examines all of them. On a sensor batch with thousands of samples and an "
        "early fault, that is the difference between O(1) and O(n) in the common case."
    ),
    MD(
        "The cost of `break` itself is nil - it is a jump. The cost of the *pattern* is "
        "what matters: a loop with a `continue` for most items can be slower than a "
        "pre-filtering comprehension, because the branch is evaluated per element. When "
        "most items are skipped, filtering before the loop is both faster and clearer; "
        "when most items are kept, the in-loop check costs almost nothing."
    ),
    TIP(
        "Measure the skip rate",
        "If a loop skips most of its input, build a list of the wanted items first. "
        "If it processes most of them, leave the check where it is.",
    ),
]

LESSON["pythonic_approaches"] = [
    MD("A flag variable versus the loop else."),
    CODE_CELL(
        "readings = [0.1, 0.2, 0.9]\n"
        "limit = 0.5\n"
        "\n"
        "# before: a flag, initialised and checked outside the loop\n"
        "found = False\n"
        "for reading in readings:\n"
        "    if reading > limit:\n"
        "        found = True\n"
        "        break\n"
        "if not found:\n"
        "    print('nothing above the limit')\n"
        "\n"
        "# after: the loop states it directly\n"
        "for reading in readings:\n"
        "    if reading > limit:\n"
        "        print(f'found {reading}')\n"
        "        break\n"
        "else:\n"
        "    print('nothing above the limit')"
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "A rover must stop scanning the moment it finds a fault - continuing would waste "
        "the control cycle that a stop command needs. That is precisely what `break` is "
        "for, and the loop `else` is how it reports that the batch was clean."
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
        "state = robot.status()\n"
        "\n"
        "for key, value in state.items():\n"
        "    if value is None:\n"
        "        continue          # a field the robot has not reported yet\n"
        "    if key == 'battery_pct':\n"
        "        print(f'battery {value:.1f}% - stopping the scan here')\n"
        "        break\n"
        "else:\n"
        "    print('no battery field reported')"
    ),
]

LESSON["engineering_example"] = [
    MD(
        "A consumer that takes a predicate, so the same control flow serves several "
        "different search policies."
    ),
    CODE_CELL(
        "def take_while_ok(items, is_ok) -> list:\n"
        "    \"\"\"Collect leading items while is_ok holds; stop at the first failure.\"\"\"\n"
        "    collected: list = []\n"
        "    for item in items:\n"
        "        if not is_ok(item):\n"
        "            break\n"
        "        collected.append(item)\n"
        "    return collected"
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Write a loop over a list that skips None values with continue and sums the "
            "rest.",
            "Write a search that breaks on the first value above a threshold, and use the "
            "else clause to report that none was found.",
            "Write a two-level nested loop with a break, and count how many times the "
            "outer body runs.",
            "Rewrite a flag-variable search using the loop else and confirm the "
            "behaviour is identical.",
        ]
    ),
    CODE_CELL(
        "readings = [0.4, None, 0.9, -0.1, 0.7]\n"
        "\n"
        "total = 0.0\n"
        "for reading in readings:\n"
        "    if reading is None:\n"
        "        continue\n"
        "    total += reading\n"
        "print('sum:', round(total, 2))\n"
        "\n"
        "limit = 0.6\n"
        "for reading in readings:\n"
        "    if reading is not None and reading > limit:\n"
        "        print('first above limit:', reading)\n"
        "        break\n"
        "else:\n"
        "    print('nothing above the limit')\n"
        "\n"
        "runs = 0\n"
        "for row in ((0, 0), (0, 0)):\n"
        "    runs += 1\n"
        "    for cell in row:\n"
        "        if cell == 9:\n"
        "            break\n"
        "print('outer loop ran', runs, 'times')"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: three exits, one of which is a question.** A loop body can "
        "finish normally, skip to the next item with continue, or leave early with "
        "break. The loop else belongs to the *normal* exit only, which makes it a "
        "compact way to say \"I looked at everything and found nothing\"."
    ),
    TABLE(
        ["You write", "Leaves", "else runs?"],
        [
            ["`continue`", "nothing, next iteration", "yes if the loop ends normally"],
            ["`break`", "the innermost loop", "no"],
            ["`return`", "the whole function", "no"],
            ["body completes", "nothing", "yes"],
        ],
    ),
]

TERMS = [
    ["break", "Exit the innermost loop immediately."],
    ["continue", "Skip the rest of the body and start the next iteration."],
    ["Loop else", "A clause that runs only when the loop ended without a break."],
    ["Early exit", "Leaving a loop as soon as the answer is known."],
    ["Nested loop", "A loop inside another loop; break affects only the inner one."],
    ["Flag variable", "A boolean set inside a loop to record what happened."],
    ["Fall through", "Continuing into the next statement after a loop body."],
    ["Search loop", "A loop that stops at the first match."],
    ["Filter loop", "A loop that skips unwanted items and keeps the rest."],
    ["Unreachable code", "Statements after a return inside a loop that always returns."],
]

LESSON["summary"] = [
    MD(
        "`break` leaves the innermost loop and `continue` starts the next iteration, "
        "and both act on one loop only. In nested loops that fact is the usual source "
        "of confusion: a `break` in the inner loop leaves the outer loop running, which "
        "is correct far more often than beginners expect and occasionally exactly what "
        "you want."
    ),
    MD(
        "The third form is the one that changes how you write searches. An `else` clause "
        "on a loop runs only when the loop completed without a `break`, which is a "
        "direct statement of \"I searched the whole space and found nothing\". It "
        "replaces a flag variable that has to be initialised before the loop and checked "
        "after it, and it removes a whole class of bug where the flag is never reset "
        "between uses."
    ),
    MD(
        "The subtlety to remember is that `return` also skips the loop `else`, because it "
        "leaves the function entirely. The two exits are not interchangeable, and "
        "choosing wrongly produces code that appears to work while quietly skipping the "
        "rest of the function. For a fault scanner - the robotics case this topic is "
        "built around - early exit is not only an optimisation: it is what leaves the "
        "control cycle free to issue a stop command."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "break leaves the innermost loop; continue starts the next iteration.",
            "The loop else runs only when no break (and no return) happened.",
            "Return also skips the else, because it leaves the function.",
            "Prefer the else clause to a flag variable for not-found cases.",
            "break affects one loop level; restructure or use a helper to leave two.",
            "Add a comment to a loop else, because it reads like an if else.",
            "Early exit is a real O(n) to O(1) win for search loops.",
            "Always test the not-found path; it is the one usually missing.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "The for statement and its else clause](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement)",
            "The while statement and its else clause](https://docs.python.org/3/reference/compound_stmts.html#the-while-statement)",
            "itertools - takewhile and dropwhile as loop-level control](https://docs.python.org/3/library/itertools.html)",
            "BREAK and CONTINUE outside a loop](https://docs.python.org/3/reference/simple_stmts.html#the-break-statement)",
            "PEP 709 - comprehension inlining, for future reference](https://peps.python.org/pep-0709/)",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Find the first negative reading",
        difficulty="MEDIUM",
        learning_objectives=["Break on the first match.", "Report the not-found case."],
        concepts_tested=["break", "for", "search"],
        problem_statement=(
            "Write `first_negative(values)` returning the index of the first value "
            "below zero, or None when every value is non-negative."
        ),
        requirements=["Use break to stop at the first match.", "Return None when absent."],
        constraints=["Do not build an intermediate list."],
        input_description="A list of numbers.",
        expected_output="An index, or None.",
        example_input="first_negative([1.0, -0.5, -2.0])",
        example_output="1",
        edge_cases=["An empty list returns None.", "A zero is not negative.", "Only the first match is reported."],
        hints=["Return from inside the loop as soon as the condition holds."],
        success_criteria=["The example returns 1.", "An empty list returns None."],
        optional_extension="Return the value and the index as a tuple.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Sum only the usable readings",
        difficulty="MEDIUM",
        learning_objectives=["Skip items with continue.", "Keep the loop body flat."],
        concepts_tested=["continue", "for", "filtering"],
        problem_statement=(
            "Write `sum_usable(values)` summing every entry that is a real number, "
            "skipping None, strings and booleans with continue."
        ),
        requirements=["Use continue for every skipped item.", "Return a float."],
        constraints=["Reject bools from the sum."],
        input_description="A list of arbitrary objects.",
        expected_output="A float.",
        example_input="sum_usable([1.0, None, 2.0, 'x'])",
        example_output="3.0",
        edge_cases=["No usable values returns 0.0.", "A list of only junk returns 0.0.", "True is skipped."],
        hints=["One continue per skip reason, then a single accumulation line."],
        success_criteria=["The example returns 3.0.", "An empty list returns 0.0."],
        optional_extension="Count the skipped items as well.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Find the first multiple of n",
        difficulty="MEDIUM",
        learning_objectives=["Use the loop else.", "Express a not-found result."],
        concepts_tested=["for/else", "modulo", "search"],
        problem_statement=(
            "Write `first_multiple(values, n)` returning the first value divisible by "
            "`n`. Use the loop else clause to express the not-found case rather than a "
            "flag variable."
        ),
        requirements=["Use the loop else.", "Raise ValueError for n equal to zero."],
        constraints=["No flag variable."],
        input_description="A list of integers and a non-zero divisor.",
        expected_output="A value, or None.",
        example_input="first_multiple([3, 7, 10], 5)",
        example_output="10",
        edge_cases=["n of zero raises ValueError.", "No multiple returns None.", "A negative multiple is a valid match."],
        hints=["Break on the match; let the else return None."],
        success_criteria=["The example returns 10.", "No match returns None."],
        optional_extension="Return the index rather than the value.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Stop scanning at a sentinel",
        difficulty="MEDIUM",
        learning_objectives=["Break on a control value.", "Distinguish sentinel from data."],
        concepts_tested=["break", "sentinel", "search"],
        problem_statement=(
            "Write `scan_until(values, sentinel)` returning the items collected up to "
            "but not including the first occurrence of `sentinel`."
        ),
        requirements=["Break on the sentinel.", "Return the collected items."],
        constraints=["A sentinel after the last item simply ends the scan."],
        input_description="A list and a sentinel value.",
        expected_output="A list of items.",
        example_input="scan_until([1, 2, 9, 3], 9)",
        example_output="[1, 2]",
        edge_cases=["An empty list returns an empty list.", "A sentinel in first position returns an empty list.", "A missing sentinel returns everything."],
        hints=["Collect first, then test, so the sentinel is never included."],
        success_criteria=["The example returns [1, 2].", "A missing sentinel returns the whole list."],
        optional_extension="Report whether the sentinel was found.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Detect duplicates with for/else",
        difficulty="MEDIUM",
        learning_objectives=["Use the else clause to report absence.", "Compare within a loop."],
        concepts_tested=["for/else", "membership", "sets"],
        problem_statement=(
            "Write `has_duplicates(values)` returning True when any value appears twice. "
            "Implement it with a loop and a seen set rather than a Counter."
        ),
        requirements=["Track seen values in a set.", "Break on the first duplicate."],
        constraints=["Do not use len(set(values)) != len(values)."],
        input_description="A list of hashable values.",
        expected_output="A boolean.",
        example_input="has_duplicates([1, 2, 1])",
        example_output="True",
        edge_cases=["An empty list returns False.", "A single value returns False.", "Strings compare by value."],
        hints=["Add to the set only after checking membership."],
        success_criteria=["The example returns True.", "An empty list returns False."],
        optional_extension="Return the duplicated value rather than a bool.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Locate a target in a grid",
        difficulty="HARD",
        learning_objectives=["Nest loops.", "Return rather than set a flag."],
        concepts_tested=["nested loops", "return", "enumeration"],
        problem_statement=(
            "Write `find_target(grid, target)` returning the `(row, col)` of the first "
            "match, or None, without a found flag."
        ),
        requirements=["Return from inside the inner loop.", "Report the first match only."],
        constraints=["Do not use a found flag."],
        input_description="A sequence of rows and a target value.",
        expected_output="A tuple, or None.",
        example_input="find_target(((1, 2), (3, 4)), 3)",
        example_output="(1, 0)",
        edge_cases=["An empty grid returns None.", "A target equal to 0 is found, not skipped."],
        hints=["Enumerate both levels and return the pair directly."],
        success_criteria=["The example returns (1, 0).", "An empty grid returns None."],
        optional_extension="Return a list of every match instead.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Take readings until the budget is spent",
        difficulty="HARD",
        learning_objectives=["Track a budget across iterations.", "Break when exhausted."],
        concepts_tested=["break", "accumulator", "budget"],
        problem_statement=(
            "Write `spend_budget(readings, budget)` consuming readings in order and "
            "returning `(consumed, remaining)`, stopping as soon as the next reading "
            "would exceed the budget."
        ),
        requirements=["Never overspend.", "Stop at the first reading that does not fit."],
        constraints=["A reading larger than the budget stops the scan immediately."],
        input_description="A list of costs and a non-negative budget.",
        expected_output="A tuple of (list, int).",
        example_input="spend_budget([3, 5, 2], 6)",
        example_output="([3], 3)",
        edge_cases=["A zero budget consumes nothing.", "The exact budget may be fully spent."],
        hints=["Check before adding, then break when the check fails."],
        success_criteria=["The example returns ([3], 3).", "A zero budget returns ([], 0)."],
        optional_extension="Report which reading stopped the scan.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Group consecutive equal readings",
        difficulty="HARD",
        learning_objectives=["Compare with the previous item.", "Close a group at the end."],
        concepts_tested=["state", "loops", "grouping"],
        problem_statement=(
            "Write `group_runs(values)` returning `(value, count)` pairs for each run of "
            "consecutive equal values."
        ),
        requirements=["Handle the final run.", "Return an empty list for empty input."],
        constraints=["Single pass."],
        input_description="A list of comparable values.",
        expected_output="A list of (value, count) tuples.",
        example_input="group_runs([1, 1, 2, 2, 2, 1])",
        example_output="[(1, 2), (2, 3), (1, 1)]",
        edge_cases=["Empty input gives an empty list.", "All equal gives one pair."],
        hints=["Flush the pending group when the value changes, and once more at the end."],
        success_criteria=["The example returns [(1, 2), (2, 3), (1, 1)].", "Empty input gives []."],
        optional_extension="Return a dict of value to longest run.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Scan a telemetry batch for the first fault",
        difficulty="HARD",
        learning_objectives=["Combine continue and break.", "Separate bad data from a fault."],
        concepts_tested=["continue", "break", "validation"],
        problem_statement=(
            "Write `first_fault(batch, max_temp)` returning `('overheating', index)` "
            "for the first sample above the limit, `('malformed', index)` for a sample "
            "that is not a dict, or None for a clean batch."
        ),
        requirements=["Report malformed entries rather than crashing.", "Stop at the first overheating sample."],
        constraints=["Malformed entries are reported, not skipped silently."],
        input_description="A list of dicts and a temperature limit.",
        expected_output="A tuple, or None.",
        example_input="first_fault([{'t': 20}, {'t': 80}], 60)",
        example_output="('overheating', 1)",
        edge_cases=["A clean batch returns None.", "A missing temperature key is not overheating."],
        hints=["Test the shape first, then the value, and return on the first fault."],
        success_criteria=["The example returns ('overheating', 1).", "A clean batch returns None."],
        optional_extension="Return every fault rather than the first.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Drive until the battery is too low",
        difficulty="HARD",
        learning_objectives=["Drive the simulator from a loop.", "Break on a safety limit."],
        concepts_tested=["break", "simulator API", "safety"],
        problem_statement=(
            "Write `drive_until_low(robot, limit_pct=20.0, step_m=1.0)` moving one "
            "metre at a time and returning `legs` driven plus the battery percentage "
            "when it stopped."
        ),
        requirements=["Stop as soon as the battery is at or below the limit.", "Never let the battery reach zero."],
        constraints=["Use only move() and status()."],
        input_description="A SimulatedRobot and an optional limit.",
        expected_output="A dict with legs and battery_pct.",
        example_input="drive_until_low(robot, 20.0)",
        example_output="{'legs': 45, 'battery_pct': 20.0}",
        edge_cases=["A robot already below the limit drives zero legs.", "A limit of zero raises ValueError."],
        hints=["Check the battery after each move and break on the limit."],
        success_criteria=["The battery never drops below the limit.", "A fresh robot below the limit drives zero legs."],
        optional_extension="Return the distance travelled as well.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "def first_negative(values):\n"
            "    for index, value in enumerate(values):\n"
            "        if value < 0:\n"
            "            return index\n"
            "    return None"
        ),
        explanation=(
            "Returning from inside the loop stops the search at the first match, which "
            "is both the correct answer and the cheap one. The trailing return handles "
            "exhaustion without a flag variable, which would have to be initialised and "
            "then tested."
        ),
        complexity="Time O(n) worst case; space O(1).",
        edge_cases="A value of exactly zero is not negative, so it does not match.",
        alternative_approaches="next((i for i, v in enumerate(values) if v < 0), None) is the generator form.",
        testing="assert first_negative([1.0, -0.5, -2.0]) == 1\nassert first_negative([]) is None\nassert first_negative([0.0, 1.0]) is None",
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def sum_usable(values) -> float:\n"
            "    total = 0.0\n"
            "    for value in values:\n"
            "        if isinstance(value, bool) or not isinstance(value, (int, float)):\n"
            "            continue\n"
            "        total += value\n"
            "    return total"
        ),
        explanation=(
            "A single continue covers every skip reason, which keeps the accumulation on "
            "one unindented line - the reason to prefer continue over wrapping the rest "
            "of the body in an else. Rejecting bool keeps True out of the total."
        ),
        complexity="Time O(n); space O(1).",
        edge_cases="A list of only junk returns 0.0 rather than raising.",
        alternative_approaches="A generator with sum() is shorter but evaluates the same test per item.",
        testing="assert sum_usable([1.0, None, 2.0, 'x']) == 3.0\nassert sum_usable([]) == 0.0\nassert sum_usable([True, 2.0]) == 2.0",
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "def first_multiple(values, n):\n"
            "    if n == 0:\n"
            "        raise ValueError('cannot divide by zero')\n"
            "    for value in values:\n"
            "        if value % n == 0:\n"
            "            return value\n"
            "    else:\n"
            "        return None"
        ),
        explanation=(
            "The else clause states the not-found case directly, so there is no flag to "
            "initialise and no way for the two paths to disagree. Validating n before the "
            "loop avoids a ZeroDivisionError from deep inside the body."
        ),
        complexity="Time O(n); space O(1).",
        edge_cases="A negative multiple is a valid match because Python's modulo handles signs.",
        alternative_approaches="next((v for v in values if v % n == 0), None) is equivalent.",
        testing="assert first_multiple([3, 7, 10], 5) == 10\nassert first_multiple([3, 7], 5) is None",
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "def scan_until(values, sentinel) -> list:\n"
            "    collected: list = []\n"
            "    for value in values:\n"
            "        if value == sentinel:\n"
            "            break\n"
            "        collected.append(value)\n"
            "    return collected"
        ),
        explanation=(
            "Testing before appending is what keeps the sentinel out of the result, which "
            "is the off-by-one this exercise is really about. A sentinel that never "
            "appears simply leaves the loop to finish normally, so no special case is "
            "needed."
        ),
        complexity="Time O(n); space O(n) for the result.",
        edge_cases="A sentinel in first position returns an empty list.",
        alternative_approaches="index() plus a slice is shorter but builds a new list.",
        testing="assert scan_until([1, 2, 9, 3], 9) == [1, 2]\nassert scan_until([1, 2], 9) == [1, 2]\nassert scan_until([], 9) == []",
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "def has_duplicates(values) -> bool:\n"
            "    seen: set = set()\n"
            "    for value in values:\n"
            "        if value in seen:\n"
            "            return True\n"
            "        seen.add(value)\n"
            "    return False"
        ),
        explanation=(
            "Checking membership before inserting is the whole algorithm: the first "
            "value that is already present is a duplicate, and returning immediately "
            "means the loop never examines the rest of the data."
        ),
        complexity="Time O(n) expected; space O(n).",
        edge_cases="Strings and tuples are compared by value, so equal contents collide as expected.",
        alternative_approaches="len(set(values)) != len(values) is the one-liner this exercise forbids.",
        testing="assert has_duplicates([1, 2, 1]) is True\nassert has_duplicates([1, 2, 3]) is False\nassert has_duplicates([]) is False",
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "def find_target(grid, target):\n"
            "    for row_index, row in enumerate(grid):\n"
            "        for col_index, cell in enumerate(row):\n"
            "            if cell == target:\n"
            "                return row_index, col_index\n"
            "    return None"
        ),
        explanation=(
            "Returning from inside the inner loop leaves both loops at once, which is "
            "what a flag variable inside two levels of nesting cannot do cleanly. Row "
            "major order gives the first match, matching the specification."
        ),
        complexity="Time O(rows * cols) worst case; space O(1).",
        edge_cases="A target of 0 is found rather than skipped, because the test is equality.",
        alternative_approaches="Flattening the grid with an index is faster but loses the coordinates.",
        testing="assert find_target(((1, 2), (3, 4)), 3) == (1, 0)\nassert find_target(((1, 2), (3, 4)), 9) is None\nassert find_target((), 1) is None",
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "def spend_budget(readings, budget):\n"
            "    if budget < 0:\n"
            "        raise ValueError('budget must not be negative')\n"
            "    consumed: list = []\n"
            "    remaining = budget\n"
            "    for cost in readings:\n"
            "        if cost > remaining:\n"
            "            break\n"
            "        consumed.append(cost)\n"
            "        remaining -= cost\n"
            "    return consumed, remaining"
        ),
        explanation=(
            "Testing the cost against the remaining budget *before* consuming it is what "
            "guarantees the budget is never overspent. Deducting after the append keeps "
            "the two variables in step, and break ends the scan at the first item that "
            "does not fit."
        ),
        complexity="Time O(n); space O(n) for the consumed list.",
        edge_cases="A budget of exactly one reading's cost consumes it and leaves zero.",
        alternative_approaches="A running sum with a break gives the same result.",
        testing="assert spend_budget([3, 5, 2], 6) == ([3], 3)\nassert spend_budget([1, 1], 0) == ([], 0)\nassert spend_budget([2, 2], 4) == ([2, 2], 0)",
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "def group_runs(values) -> list[tuple]:\n"
            "    groups: list[tuple] = []\n"
            "    if not values:\n"
            "        return groups\n"
            "    current = values[0]\n"
            "    count = 1\n"
            "    for value in values[1:]:\n"
            "        if value == current:\n"
            "            count += 1\n"
            "        else:\n"
            "            groups.append((current, count))\n"
            "            current, count = value, 1\n"
            "    groups.append((current, count))\n"
            "    return groups"
        ),
        explanation=(
            "The pending group is flushed when the value changes and once more after the "
            "loop, and that final flush is the detail this exercise is really about - "
            "without it the last run is silently lost."
        ),
        complexity="Time O(n); space O(k) for k runs.",
        edge_cases="A single value produces one pair with count 1.",
        alternative_approaches="itertools.groupby produces the same structure in one line.",
        testing="assert group_runs([1, 1, 2, 2, 2, 1]) == [(1, 2), (2, 3), (1, 1)]\nassert group_runs([]) == []\nassert group_runs([5]) == [(5, 1)]",
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "def first_fault(batch, max_temp):\n"
            "    for index, sample in enumerate(batch):\n"
            "        if not isinstance(sample, dict):\n"
            "            return 'malformed', index\n"
            "        temp = sample.get('t')\n"
            "        if temp is not None and temp > max_temp:\n"
            "            return 'overheating', index\n"
            "    return None"
        ),
        explanation=(
            "Returning inside the loop means the first fault wins, whether it is a "
            "malformed entry or an overheating reading, so the report names the earliest "
            "problem rather than a later one. Testing shape before value is what makes "
            "the two fault kinds distinguishable."
        ),
        complexity="Time O(n); space O(1).",
        edge_cases="A sample with no temperature key is not overheating and is skipped.",
        alternative_approaches="A validation pass followed by a search pass is clearer but slower.",
        testing="assert first_fault([{'t': 20}, {'t': 80}], 60) == ('overheating', 1)\nassert first_fault([{'t': 20}], 60) is None\nassert first_fault(['x'], 60) == ('malformed', 0)",
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "from shared.robo_x_sim import SimulatedRobot  # noqa: E402\n"
            "\n"
            "\n"
            "def drive_until_low(robot, limit_pct: float = 20.0, step_m: float = 1.0) -> dict:\n"
            "    if limit_pct <= 0:\n"
            "        raise ValueError('limit_pct must be positive')\n"
            "    legs = 0\n"
            "    while robot.status()['battery_pct'] > limit_pct:\n"
            "        robot.move(distance_m=step_m, speed_mps=1.0)\n"
            "        legs += 1\n"
            "    battery = robot.status()['battery_pct']\n"
            "    return {'legs': legs, 'battery_pct': round(battery, 2)}"
        ),
        explanation=(
            "The condition is checked before each move, so the loop stops at the first "
            "battery level at or below the limit and the battery never reaches zero. "
            "A while loop is genuinely the right choice here because termination depends "
            "on simulator state rather than on a sequence length."
        ),
        complexity="Time O(legs); space O(1).",
        edge_cases="A robot already below the limit completes the loop zero times.",
        alternative_approaches="move() raises on insufficient energy, which would surface as an error rather than a limit.",
        testing="robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\nout = drive_until_low(robot, 20.0)\nassert out['battery_pct'] <= 20.0\nassert out['legs'] > 0",
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
            "from shared.robo_x_sim import SimulatedRobot, SensorError  # noqa: E402\n"
            "\n"
            "MAX_TEMPERATURE_C = 60.0\n"
            "CHANNELS = ('distance', 'temperature', 'battery_voltage')\n"
            "\n"
            "\n"
            "def scan_batch(robot, channels=CHANNELS) -> dict:\n"
            "    \"\"\"Read each channel, stopping at the first genuine fault.\"\"\"\n"
            "    readings: dict = {}\n"
            "    for channel in channels:\n"
            "        try:\n"
            "            value = robot.read_sensor(channel)\n"
            "        except SensorError:\n"
            "            readings[channel] = None\n"
            "            continue\n"
            "        readings[channel] = value\n"
            "        if channel == 'temperature' and value > MAX_TEMPERATURE_C:\n"
            "            return {'fault': 'overheating', 'readings': readings}\n"
            "    else:\n"
            "        return {'fault': None, 'readings': readings}\n"
            "    return {'fault': 'unreachable', 'readings': readings}"
        ),
        explanation=(
            "A failed read is recorded and skipped so one dead sensor does not abort the "
            "batch, while an overheating reading stops the scan immediately. The loop else "
            "reports that the whole batch was read without a fault, which is the outcome "
            "a supervisor most needs to distinguish."
        ),
        complexity="Time O(c) for c channels; space O(c).",
        edge_cases="An unknown channel name is recorded as None and does not stop the scan.",
        alternative_approaches="Reusing the lesson scanner keeps one policy in one place.",
        testing="robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\nout = scan_batch(robot, ['distance', 'temperature'])\nassert out['fault'] is None\nassert out['readings']['distance'] is not None",
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="What does `break` leave?",
        choices=[
            "The innermost loop only.",
            "Every enclosing loop as well.",
            "The whole function, like return.",
            "Nothing - it restarts the loop.",
        ],
        answer=0,
        kind="conceptual",
        explanation=(
            "break exits only the loop it appears in. In nested loops the outer loop "
            "carries on with its next iteration, which is often exactly what you want "
            "and occasionally a surprise."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="When does a loop's `else` clause run?",
        choices=[
            "When the loop body never executed.",
            "Whenever the loop ends, including after a break.",
            "Only in a while loop.",
            "When the loop finished without a break.",
        ],
        answer=3,
        kind="code_output",
        explanation=(
            "The else is a completion handler: it runs when the loop exhausts its "
            "sequence or its condition first fails. A break skips it, which is what "
            "makes it a direct statement of 'searched and found nothing'."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="A nested loop breaks, but the outer loop keeps running. Is that a bug?",
        choices=[
            "Yes - break is supposed to leave every enclosing loop.",
            "Yes, unless the loops are in the same function.",
            "No - break leaves only the innermost loop by design.",
            "No, but only when the inner loop is a for loop.",
        ],
        answer=2,
        kind="debugging",
        explanation=(
            "This is the defined behaviour and it is frequently correct. Reaching the "
            "outer loop from the inner one requires restructuring or a helper that "
            "returns, not a different break."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="What is wrong with using `continue` where `break` was meant?",
        choices=[
            "The loop keeps scanning instead of stopping at the first match.",
            "Nothing - they are interchangeable.",
            "continue cannot appear inside a for loop.",
            "It raises a SyntaxError.",
        ],
        answer=0,
        kind="identify_error",
        explanation=(
            "continue skips to the next item, so the search keeps going and may find a "
            "later match or none at all. The result is wrong without any error, which "
            "is the dangerous part."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="Why prefer the loop `else` to a `found` flag variable?",
        choices=[
            "It is faster.",
            "The loop states the not-found case directly, with no state to reset.",
            "It works with while loops and flags do not.",
            "It allows more than one break per loop.",
        ],
        answer=1,
        kind="reasoning",
        explanation=(
            "A flag has to be initialised before the loop and checked after it, and it "
            "is easy to forget to reset it between uses. The else clause removes both "
            "the state and the reset."
        ),
        reference="lesson.ipynb - Pythonic Approaches",
    )
)

QUIZ.append(
    quiz(
        question="What happens to a loop's `else` clause when the body calls `return`?",
        choices=[
            "It runs, because return is a normal exit.",
            "It raises a SyntaxError.",
            "It runs only if the return value is None.",
            "It is skipped, because return leaves the function entirely.",
        ],
        answer=3,
        kind="reasoning",
        explanation=(
            "return unwinds the whole function, so the loop never completes and its else "
            "is skipped. The two exits are not interchangeable, which is why the lesson "
            "uses return for the found case and break for the loop-else example."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="Which loop is best for a search that stops at the first match?",
        choices=[
            "A while loop with a found flag.",
            "A for loop that iterates the whole sequence and filters afterwards.",
            "A for loop with a break inside.",
            "A while loop with a manual index.",
        ],
        answer=2,
        kind="implementation_choice",
        explanation=(
            "break leaves as soon as the match is known, so the remaining elements are "
            "never examined. The filtering form produces the same answer but pays for "
            "the full traversal."
        ),
        reference="lesson.ipynb - Best Practices",
    )
)

QUIZ.append(
    quiz(
        question="What does this print?\n\nfor n in (1, 2, 3):\n    if n == 2:\n        break\nelse:\n    print('none found')\nprint('done')",
        choices=[
            "done, then none found",
            "none found, then done",
            "done only",
            "none found only",
        ],
        answer=2,
        kind="code_output",
        explanation=(
            "The break on n == 2 skips the else clause, so 'none found' never prints. "
            "The statement after the loop always runs, which is why the only output is "
            "'done'."
        ),
        reference="lesson.ipynb - Basic Examples",
    )
)

QUIZ.append(
    quiz(
        question="Why must a rover stop scanning a telemetry batch at the first fault?",
        choices=[
            "Scanning is expensive, so early exit is faster.",
            "Continuing would leave no control cycle free to issue a stop command.",
            "Python requires a break in every long loop.",
            "The batch would be truncated otherwise.",
        ],
        answer=1,
        kind="robotics",
        explanation=(
            "The scan competes with the control loop for the cycle. Continuing past a "
            "fault spends the time a stop command needs, so early exit is a safety "
            "property rather than only an optimisation."
        ),
        reference="solution.ipynb - Solution 11",
    )
)

QUIZ.append(
    quiz(
        question="Which statement about `continue` is correct?",
        choices=[
            "It leaves the loop, like break.",
            "It skips the rest of the body and runs any else clause immediately.",
            "It skips the rest of the body and starts the next iteration.",
            "It is only valid in a while loop.",
        ],
        answer=2,
        kind="multiple_choice",
        explanation=(
            "continue jumps to the next iteration, so the remaining statements in the "
            "body do not run. The loop still ends normally, which means the else clause "
            "can still run at the end."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

MINI_PROJECT = {
    "title": "Mini-Project: Telemetry Fault Scanner",
    "brief": (
        "Build a scanner that walks a telemetry batch, skips unusable samples, stops "
        "at the first genuine fault, and reports clearly when the batch was clean."
    ),
    "scenario": (
        "An underground rover records a batch before each mission. One sample being "
        "malformed must not stop the scan, but a real fault must stop it immediately so "
        "the control cycle stays free."
    ),
    "rationale": (
        "This combines every tool in the topic: continue for unusable data, break for "
        "the first fault, and the loop else for the clean case."
    ),
    "requirements": [
        "Iterate the batch and skip samples that are not dicts or lack a reading.",
        "Return the first genuine fault with its index.",
        "Use the loop else to report a clean batch.",
        "Accept thresholds as parameters with module-level defaults.",
    ],
    "constraints": [
        "Standard library only.",
        "No flag variable.",
        "Never raise for any sample in a batch.",
    ],
    "deliverables": [
        "`scanner.py` with the scan function.",
        "`test_scanner.py` with at least twelve assertions.",
        "A README section describing which faults are reported and which are skipped.",
    ],
    "steps": [
        "Define MAX_TEMPERATURE_C and MAX_TILT_DEG as constants.",
        "Skip non-dict samples with continue.",
        "Return on the first overheating or tilt fault, with the index.",
        "Add the else clause returning a clean report.",
        "Test a clean batch, a malformed entry, a fault, and a fault after junk.",
    ],
    "expected_behavior": (
        "A clean batch returns a clean report. A batch containing junk and then a fault "
        "reports the fault index, not the junk."
    ),
    "acceptance": [
        "All assertions pass from a clean run.",
        "Junk before a fault does not stop the scan.",
        "The not-found path is covered by a test.",
        "No flag variable appears in the implementation.",
    ],
    "extensions": [
        "Return every fault rather than the first.",
        "Add a fault severity ordering so the most severe is reported first.",
        "Integrate the scan with the simulator's live readings.",
    ],
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Separate the three loop exits clearly in students' minds.",
        "Make the loop else replace the flag variable as a habit.",
        "Explain why break is only ever one level deep.",
    ],
    "misconceptions": [
        [
            "break leaves all the loops it is inside.",
            "It leaves only the innermost loop; use a helper and return for more.",
        ],
        [
            "The loop else runs whenever the loop ends.",
            "It runs only when the loop ended without a break or return.",
        ],
        [
            "continue and break are two spellings of exit.",
            "continue skips to the next iteration; break leaves the loop.",
        ],
        [
            "A found flag is always simpler than a for/else.",
            "The flag has to be reset; the else cannot drift out of sync.",
        ],
    ],
    "difficult_concepts": [
        "Reading a loop else as a completion handler rather than a fallback.",
        "Accepting that return also suppresses the else.",
        "Rewriting a flag-based search without regressing readability.",
    ],
    "demonstrations": [
        "Run a nested loop with a break and show the outer loop continuing.",
        "Show a for/else where the break suppresses the else, side by side.",
        "Introduce a flag that is never reset and show the second batch behaving wrongly.",
    ],
    "discussion": [
        "When is a flag clearer than a loop else?",
        "Should a fault scanner stop at the first problem or collect them all?",
    ],
    "student_errors": [
        [
            "The search returns the last match, not the first",
            "continue was used where break was meant",
            "Break at the match and return immediately",
        ],
        [
            "The else runs when it should not",
            "The body returns before the loop completes",
            "Decide explicitly between return and break for the found case",
        ],
        [
            "A flag stays True across two batches",
            "It was never reset inside the outer loop",
            "Use the loop else or reset it explicitly",
        ],
    ],
    "pacing": (
        "90 minutes of lesson with the nested-loop demonstration, then 2 hours of "
        "exercises. Insist on rewriting one flag solution as a for/else so the contrast "
        "is felt rather than just described."
    ),
    "extensions": [
        "Ask students to find a break that leaves the wrong loop and fix it.",
        "Have them convert a for/else back into a flag and explain what is lost.",
    ],
    "assessment": (
        "Grade against rubric.md. Exercises 7 to 9 carry the signal: they require "
        "correct early exit, a budget boundary, and a stateful grouping pass."
    ),
    "support": (
        "Provide the first_fault function from exercise 9 with the first two branches "
        "written, and ask students to complete the loop else."
    ),
    "extension_fast": (
        "Ask for a short note on how a flat index loop could replace a nested search, "
        "and what it costs in readability."
    ),
}

RESEARCH = {
    "question": (
        "How much time does early exit save when a search usually finds its match early?"
    ),
    "hypothesis": (
        "Breaking at the first match examines a fraction of the data, so average time "
        "falls in proportion to the average match position."
    ),
    "experiment": [
        STEPS(
            [
                "Build a list of 100000 random values and pick a target near the front.",
                "Time a search that breaks at the match.",
                "Time an identical search that scans the whole list and filters.",
                "Repeat for targets at the front, middle and end, ten runs each.",
            ]
        ),
    ],
    "data": [
        CODE_CELL(
            "# Record your raw timings - one row per target position per variant.\n"
            "# Copy real values from your actual runs; do not invent them.\n"
            "#\n"
            "# | target position | variant | run | seconds |"
        ),
    ],
    "analysis": [
        MD(
            "Compare the mean times for each target position. The hypothesis predicts a "
            "ratio roughly equal to the fraction of the list the early-exit version "
            "never examined."
        ),
    ],
    "result": [
        MD(
            "State the observed ratio for each position and whether it matched the "
            "predicted fraction. Report any position where it did not rather than "
            "dropping it."
        ),
    ],
    "interpretation": [
        MD(
            "Explain why the saving is proportional rather than dramatic, given both "
            "versions share asymptotics. Name at least two threats to validity, including "
            "the constant cost of setting up the search itself."
        ),
    ],
    "conclusion": [
        MD(
            "Give your verdict and state when early exit is worth the extra branch - and "
            "when the readability cost is not justified."
        ),
    ],
    "extensions": [
        "Repeat with a target that is usually absent, where both versions scan fully.",
        "Measure the cost of the break branch itself with a very small list.",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Mission Fault Scanner",
    "context": (
        "Before an underground inspection mission the rover scans a telemetry batch. "
        "Junk samples must be skipped, a real fault must stop the scan, and a clean "
        "batch must be reported as clean."
    ),
    "mission": (
        "Implement `scan_batch(robot, batch, limits)` that walks the batch with the "
        "right loop control and returns a verdict the mission supervisor can gate on."
    ),
    "requirements": [
        "Skip samples that are not dicts or lack a reading.",
        "Return the first genuine fault with its batch index.",
        "Use the loop else to report a batch that was read without a fault.",
        "Read one live channel from the simulator so the scan exercises real readings.",
    ],
    "constraints": [
        "No flag variable; use the loop else for the clean case.",
        "Never raise for any sample in a batch.",
        "Complete well inside the 10 ms control budget per scan.",
    ],
    "interface": "def scan_batch(robot, batch, limits=None) -> dict:",
    "success_criteria": [
        "A clean batch returns fault None.",
        "A batch with junk then a fault reports the fault, not the junk.",
        "The simulator reading appears in the result.",
    ],
    "extension": (
        "Return every fault with its index instead of only the first, and state which "
        "one a supervisor should act on."
    ),
}

RUBRIC = {
    "artifacts": [
        ["exercises.ipynb", "40%", "All 10 exercises implemented and edge-cased."],
        ["mini_project.ipynb", "25%", "scanner.py plus its test suite."],
        ["robotics_challenge.ipynb", "25%", "Scanner degrades safely."],
        ["research.ipynb", "10%", "Real measurements with a defensible conclusion."],
    ],
    "criteria": [
        ["Correctness", "30", "Early exit, skipping and the else all behave as specified."],
        ["Control flow clarity", "25", "No flag drift; the exit path is obvious to a reader."],
        ["Code quality", "25", "PEP 8 naming, docstrings, small focused functions."],
        ["Reasoning", "20", "Cost and complexity claims explained in writing."],
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
            "Every exercise implemented, the not-found path is tested, and the scan "
            "reports the first genuine fault while skipping junk ahead of it.",
        ],
        [
            "Merit",
            "Most exercises correct; the scan works but uses a flag variable reset by "
            "hand, and the reset is untested.",
        ],
        [
            "Pass",
            "Core requirements met, but continue is used where break was meant, so the "
            "scan reports a later match or none at all.",
        ],
        [
            "Fail",
            "The loop reports the last match instead of the first, or a malformed sample "
            "raises and aborts the scan.",
        ],
    ],
}

TOPIC = topic(
    topic_id="2.3",
    title="Loop Control",
    module=2,
    module_title="Control Flow and Loops",
    directory="03_loop_control",
    summary=(
        "break, continue and the under-used loop else: three ways a loop says how it "
        "finished, and why that is usually more expressive than a flag variable."
    ),
    why_it_matters=(
        "A fault scanner that keeps reading after it has found the fault spends the "
        "control cycle it needed for a stop command, and a search that forgets to break "
        "reports the wrong answer with no error at all. Loop control is where a small "
        "mistake becomes a silent one."
    ),
    objectives=[
        "Distinguish break, continue and return by what each one leaves.",
        "Explain that break affects only the innermost loop.",
        "Use the loop else to express a not-found result without a flag.",
        "Recognise that return also suppresses the else clause.",
        "Rewrite a flag-based search as an early-exit loop.",
        "Use early exit deliberately as a performance and safety measure.",
    ],
    prerequisites=["Topic 2.2 for Loops and while Loops"],
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
