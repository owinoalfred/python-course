"""Topic 2.1 - Conditional Statements.

Hand-authored to the Course Content Standard. The spine: a condition is an
expression that produces a bool, and almost every bug in a branch is a question
about what that expression actually evaluated to.
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
        "A conditional is an expression that produces a value, and a conditional "
        "*statement* applies a rule using that value. Python's `if` takes any value, "
        "not only a bool: it applies its truthiness. That is why `if value:` and "
        "`if value is not None:` are not interchangeable, and why a legitimate reading "
        "of zero can vanish without any error being raised."
    ),
    CODE_CELL(
        "battery_pct = 0.0\n"
        "\n"
        "if battery_pct:\n"
        "    print('has charge')\n"
        "else:\n"
        "    print('exactly empty - still a valid reading')\n"
        "\n"
        "if battery_pct is not None:\n"
        "    print('the sensor reported a value')\n"
        "\n"
        "print('bool(0.0) =', bool(battery_pct), '- falsy')"
    ),
    MD(
        "Only a small set of values are falsy: `False`, `None`, zero of any numeric "
        "type, the empty string, and empty containers. Everything else is truthy, "
        "including `0.0`, `'0'` and `[0]`. That last pair is the trap - a non-empty "
        "list containing zero is truthy, and a string containing the character 0 is "
        "truthy, so a 'zero' check on text silently passes."
    ),
    CODE_CELL(
        "values = [0, 0.0, '', '0', [], [0], {}, {'a': 0}, None, False, True]\n"
        "for value in values:\n"
        "    print(f'{value!r:<10} -> {\"truthy\" if value else \"falsy\"}')"
    ),
    NOTE(
        "Prefer the explicit question",
        "Write the condition you mean. `if count > 0` says what you are testing; "
        "`if count` asks a different question and answers it differently for `0`, "
        "`'0'` and `[]`.",
    ),
]

LESSON["formal_theory"] = [
    MD(
        "An `if` statement is a header ending in a colon followed by a suite. The header "
        "is any expression; the interpreter applies truthiness to its value. `elif` "
        "branches are not independent tests - they are only reached when every earlier "
        "condition was false, which is why their order encodes a priority."
    ),
    EQUATION(
        "if E1 -> suite1 ; elif E2 -> suite2 ; else -> suite_n   (first match wins)"
    ),
    MD(
        "The conditional expression `a if condition else b` is an expression, so it can "
        "appear inside a call, an f-string or an assignment. It is the idiomatic way to "
        "choose between two values, and it should be used only when both branches are "
        "equally simple - a chain of nested conditionals expressions is harder to read "
        "than an `if` statement."
    ),
    CODE_CELL(
        "LOW, MEDIUM = 20, 50\n"
        "\n"
        "\n"
        "def verdict(pct: float) -> str:\n"
        "    return 'LOW' if pct < LOW else 'MEDIUM' if pct < MEDIUM else 'OK'\n"
        "\n"
        "\n"
        "for pct in (10, 35, 90):\n"
        "    print(f'{pct:>3}% -> {verdict(pct)}')\n"
        "\n"
        "# a chain of comparisons in one expression\n"
        "print('in range:', 0 <= 10 <= 100)\n"
        "print('out of range:', 0 <= 101 <= 100)"
    ),
    TABLE(
        ["Value", "Truthiness", "Typical robotics meaning"],
        [
            ["`0`", "falsy", "a count of zero events"],
            ["`0.0`", "falsy", "a battery reading of exactly zero volts"],
            ["`''`", "falsy", "an empty operator comment"],
            ["`[]`", "falsy", "no queued commands"],
            ["`'0'`", "**truthy**", "text that looks numeric but is not"],
            ["`None`", "falsy", "the sensor has not reported"],
        ],
    ),
]

LESSON["syntax"] = [
    MD(
        "The canonical form tests the most specific case first and ends with the "
        "general fallback, so each boundary appears exactly once."
    ),
    CODE_CELL(
        "LOW_BATTERY_PCT = 20\n"
        "CRITICAL_BATTERY_PCT = 8\n"
        "\n"
        "\n"
        "def verdict(pct: float) -> str:\n"
        "    if pct <= CRITICAL_BATTERY_PCT:\n"
        "        return 'CRITICAL'\n"
        "    elif pct < LOW_BATTERY_PCT:\n"
        "        return 'LOW'\n"
        "    else:\n"
        "        return 'OK'\n"
        "\n"
        "\n"
        "for pct in (5, 15, 80):\n"
        "    print(f'{pct:>3}% -> {verdict(pct)}')"
    ),
    MD("The anti-pattern - a chain of independently evaluated `if`s:"),
    CODE(
        "if pct < 20:\n"
        "    level = 'LOW'\n"
        "if pct < 50:            # also true when pct is 10\n"
        "    level = 'MEDIUM'      # silently overwrites the first answer\n"
        "\n"
        "if pct < 20:            # elif makes the priority explicit\n"
        "    level = 'LOW'\n"
        "elif pct < 50:\n"
        "    level = 'MEDIUM'",
        lang="text",
    ),
    WARN(
        "elif is not else-if",
        "`elif` is only evaluated when every earlier condition was false. A chain of "
        "separate `if` statements re-tests the value each time and the last match wins, "
        "which is rarely what the author intended.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - comparisons and membership.**"),
    CODE_CELL(
        "battery_pct = 18.0\n"
        "state = {'status': 'ACTIVE', 'mode': 'auto'}\n"
        "\n"
        "print('less    :', battery_pct < 20)\n"
        "print('chained :', 0 <= battery_pct <= 100)\n"
        "print('equal   :', battery_pct == 18.0)\n"
        "print('not     :', not (battery_pct > 20))\n"
        "print('membership:', state['status'] in {'ACTIVE', 'IDLE'})\n"
        "print('identity:', state.get('mode') is None)"
    ),
    MD("**Example 2 - combining conditions without nesting.**"),
    CODE_CELL(
        "def can_drive(battery_pct: float, estop: bool) -> bool:\n"
        "    return battery_pct > 20 and not estop\n"
        "\n"
        "\n"
        "for pct, stop in ((50, False), (50, True), (5, False)):\n"
        "    print(f'pct={pct:<3} estop={stop!s:<6} -> {can_drive(pct, stop)}')\n"
        "\n"
        "# 'or' returns an operand, so it can supply a default\n"
        "print('default  :', '' or 'rover-01')"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "A geofence is the canonical robotics conditional: four bounds, one decision, "
        "and a rule about what to do when the robot is outside them."
    ),
    CODE_CELL(
        "def in_geofence(x: float, y: float, bounds: tuple) -> bool:\n"
        "    \"\"\"Return True when (x, y) is inside the axis-aligned rectangle.\"\"\"\n"
        "    x_min, x_max, y_min, y_max = bounds\n"
        "    return x_min <= x <= x_max and y_min <= y <= y_max\n"
        "\n"
        "\n"
        "FIELD = (0.0, 50.0, 0.0, 30.0)\n"
        "for x, y in ((10, 10), (60, 10), (10, 35)):\n"
        "    print(f'({x:>3}, {y:>3}) inside: {in_geofence(x, y, FIELD)}')"
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "A decision table scales better than a growing `elif` chain, because adding a "
        "case means adding data rather than editing control flow. This is the shape a "
        "safety policy should take."
    ),
    CODE_CELL(
        "RULES = (\n"
        "    (lambda pct, stop: stop, 'ESTOP active'),\n"
        "    (lambda pct, stop: pct <= 8, 'battery critical'),\n"
        "    (lambda pct, stop: pct < 20, 'battery low'),\n"
        ")\n"
        "\n"
        "\n"
        "def first_problem(pct: float, stop: bool):\n"
        "    for test, message in RULES:\n"
        "        if test(pct, stop):\n"
        "            return message\n"
        "    return None\n"
        "\n"
        "\n"
        "for pct, stop in ((50, True), (5, False), (15, False), (90, False)):\n"
        "    print(f'pct={pct:<3} stop={stop!s:<5} -> {first_problem(pct, stop)}')"
    ),
    MD(
        "The `match` statement added in Python 3.10 is another way to express "
        "multi-way branching, and it is worth knowing about - but a table of predicates "
        "scales the same way and is easier to unit test."
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "Below is a safety interlock for an agricultural field robot: the decision that "
        "says whether the drive circuit may be energised at all."
    ),
    CODE_CELL(
        "\"\"\"interlock.py - may the drive circuit be energised?\"\"\"\n"
        "from __future__ import annotations\n"
        "\n"
        "CRITICAL_BATTERY_PCT = 8.0\n"
        "LOW_BATTERY_PCT = 20.0\n"
        "MAX_TILT_DEG = 15.0\n"
        "\n"
        "\n"
        "def interlock(state: dict) -> tuple[bool, str]:\n"
        "    \"\"\"Return (permitted, reason). The first failing check wins.\n"
        "\n"
        "    Checks are ordered from most to least severe so the reported\n"
        "    reason is the one an operator should act on first.\n"
        "    \"\"\"\n"
        "    if state.get('estop'):\n"
        "        return False, 'emergency stop is engaged'\n"
        "    battery = state.get('battery_pct')\n"
        "    if battery is None:\n"
        "        return False, 'battery reading is missing'\n"
        "    if battery <= CRITICAL_BATTERY_PCT:\n"
        "        return False, 'battery is critical'\n"
        "    if battery < LOW_BATTERY_PCT:\n"
        "        return False, 'battery is low'\n"
        "    tilt = state.get('tilt_deg', 0.0)\n"
        "    if tilt > MAX_TILT_DEG:\n"
        "        return False, 'robot is tilted beyond the limit'\n"
        "    if not state.get('link_ok', True):\n"
        "        return False, 'radio link is down'\n"
        "    return True, 'all checks passed'"
    ),
    MD(
        "The ordering is the safety property: an engaged emergency stop short-circuits "
        "every later check, so the reason reported is always the most urgent one. "
        "Returning a tuple rather than printing means a test can assert the exact "
        "reason, and a supervisor can log it without parsing text."
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "The thresholds are module-level constants so the safety policy lives in one "
            "place and can be reviewed or tuned without reading logic.",
            "The estop check is first and returns immediately, so no later check can "
            "override the most severe condition.",
            "Using .get with an explicit None test distinguishes 'no reading' from "
            "'reading of zero', which a truthiness check could not.",
            "The critical check uses <= while the low check uses <, so the boundary value "
            "is reported as critical rather than low - the boundary is defined once.",
            "The tilt check uses state.get with a zero default, because a missing tilt "
            "reading means level rather than missing.",
            "Every branch returns the same shape, a (bool, str) tuple, so the caller "
            "never has to handle a special case.",
            "The final return is the success case, written last so adding a new check "
            "requires no edit to it.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - a chain of independent `if` statements.**"),
    CODE(
        "if pct < 20: level = 'LOW'\n"
        "if pct < 50: level = 'MEDIUM'   # also true when pct is 10\n"
        "\n"
        "if pct < 20: level = 'LOW'\n"
        "elif pct < 50: level = 'MEDIUM' # mutually exclusive",
        lang="text",
    ),
    MD("**Mistake 2 - truthiness where an explicit test was meant.**"),
    CODE(
        "if battery_pct:            # 0.0 is skipped\n"
        "    publish(battery_pct)\n"
        "\n"
        "if battery_pct is not None:\n"
        "    publish(battery_pct)",
        lang="text",
    ),
    MD("**Mistake 3 - chaining with `and` instead of `elif` when the bands overlap.**"),
    CODE(
        "if 0 <= pct < 20: level = 'LOW'\n"
        "if 20 <= pct < 50: level = 'MEDIUM'\n"
        "\n"
        "if pct < 50: level = 'LOW'      # catches 30 as LOW\n"
        "elif pct < 20: level = 'MEDIUM' # unreachable for 30",
        lang="text",
    ),
    MD("**Mistake 4 - using `==` for floats read from a sensor.**"),
    CODE(
        "if battery_pct == 20.0:   # exact equality on a measured value\n"
        "\n"
        "if abs(battery_pct - 20.0) < 0.01:   # compare with a tolerance",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "When a branch behaves unexpectedly, print what the condition actually "
        "evaluated to. Nine times in ten the answer is that the value is not the type or "
        "the value the author assumed."
    ),
    CODE_CELL(
        "samples = [0.0, 0, '', '0', None, [], [0]]\n"
        "for value in samples:\n"
        "    print(f'{value!r:<8} bool={bool(value)!s:<6} is None={value is None}')"
    ),
    MD(
        "For a chain of branches, a truth table is faster than adding prints. Enumerate "
        "the cases that matter and state what each should return."
    ),
    CODE_CELL(
        "CRITICAL, LOW = 8.0, 20.0\n"
        "\n"
        "def expected(pct):\n"
        "    if pct <= CRITICAL:\n"
        "        return 'CRITICAL'\n"
        "    if pct < LOW:\n"
        "        return 'LOW'\n"
        "    return 'OK'\n"
        "\n"
        "\n"
        "for pct in (7.9, 8.0, 19.9, 20.0, 50.0):\n"
        "    print(f'{pct:>5} -> {expected(pct)}')"
    ),
    NOTE(
        "Boundaries are where bugs live",
        "A value exactly on a threshold is the single most common source of off-by-one "
        "defects. Test 7.9, 8.0 and 8.1 before you trust a threshold.",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Use `elif` for mutually exclusive bands so only one branch can win.",
            "Order branches from most to least severe so the first match is the most urgent.",
            "Prefer an explicit comparison over truthiness whenever zero is legitimate.",
            "Use `is None` to test for absence; use `==` to test for a value.",
            "Compare measured floats with a tolerance, never with `==`.",
            "Return a value from a decision function instead of printing inside it.",
            "Give every branch the same return shape so callers never special-case.",
            "Keep thresholds in named constants, not in the middle of the logic.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "A branch is cheap. Python evaluates the condition, compares truthiness, and "
        "either enters the suite or does not - nanoseconds, with no allocation. Five "
        "thousand iterations of a five-branch chain are not a performance problem; the "
        "work inside the branches is what costs."
    ),
    MD(
        "Where branch structure does matter is in a long chain. Because each `elif` is "
        "only tested when the earlier ones failed, ordering by likelihood is a real - if "
        "small - optimisation for a hot path. It matters far more for readability: a "
        "chain ordered by severity documents the policy, and a decision table makes the "
        "same policy data rather than control flow."
    ),
    TIP(
        "Measure the branch, not the body",
        "If a conditional is suspected of being slow, the work inside it is the reason. "
        "Time the body, not the `if`.",
    ),
]

LESSON["pythonic_approaches"] = [
    MD("Nested blocks versus a single boolean expression."),
    CODE_CELL(
        "battery_pct, tilt, link_ok = 18.0, 4.0, True\n"
        "\n"
        "# before: nested blocks for one combined decision\n"
        "if battery_pct > 20:\n"
        "    if tilt < 15:\n"
        "        if link_ok:\n"
        "            permitted = True\n"
        "        else:\n"
        "            permitted = False\n"
        "    else:\n"
        "        permitted = False\n"
        "else:\n"
        "    permitted = False\n"
        "\n"
        "# after: one expression, one meaning\n"
        "permitted = battery_pct > 20 and tilt < 15 and link_ok\n"
        "print('permitted:', permitted)"
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "The field robot's drive circuit is gated by exactly the kind of chain this "
        "topic teaches: a set of conditions, each with a different severity, combined "
        "into one permission. The simulator supplies the readings so the policy can be "
        "tested against real values rather than invented ones."
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
        "robot = SimulatedRobot(name='field-01', battery_wh=48.0)\n"
        "state = robot.status()\n"
        "\n"
        "battery = state['battery_pct']\n"
        "permitted = battery > 20\n"
        "print(f'battery {battery:.1f}% -> permitted: {permitted}')\n"
        "\n"
        "empty_robot = SimulatedRobot(name='field-02', battery_wh=1.0)\n"
        "print('depleted robot permitted:', empty_robot.status()['battery_pct'] > 20)"
    ),
]

LESSON["engineering_example"] = [
    MD(
        "A decision helper that reports which check failed, so a log line can explain "
        "the outcome rather than just recording it."
    ),
    CODE_CELL(
        "def check_all(*pairs) -> tuple[bool, list[str]]:\n"
        "    \"\"\"Evaluate (passed, label) pairs and collect the failed labels.\"\"\"\n"
        "    failures = [label for passed, label in pairs if not passed]\n"
        "    return (not failures), failures"
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Predict the truthiness of 0, 0.0, '', '0', [] and [0] before running them.",
            "Write `band(pct)` returning 'CRITICAL', 'LOW' or 'OK', then test the four "
            "boundary values around each threshold.",
            "Write a two-condition guard with `and`, then the same logic with nested `if` "
            "blocks, and compare the two versions.",
            "Write `classify(value)` returning 'missing', 'empty', 'number' or 'other', "
            "handling None and empty containers correctly.",
        ]
    ),
    CODE_CELL(
        "CRITICAL, LOW = 8.0, 20.0\n"
        "\n"
        "\n"
        "def band(pct):\n"
        "    if pct <= CRITICAL:\n"
        "        return 'CRITICAL'\n"
        "    if pct < LOW:\n"
        "        return 'LOW'\n"
        "    return 'OK'\n"
        "\n"
        "\n"
        "for pct in (7.9, 8.0, 19.9, 20.0, 50.0):\n"
        "    print(f'{pct:>5} -> {band(pct)}')\n"
        "\n"
        "def classify(value):\n"
        "    if value is None:\n"
        "        return 'missing'\n"
        "    if not value:\n"
        "        return 'empty'\n"
        "    if isinstance(value, (int, float)) and not isinstance(value, bool):\n"
        "        return 'number'\n"
        "    return 'other'"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: a guard, not a switch.** An `if` does not enable or disable a "
        "capability; it either performs one action or skips it. That is why the safe "
        "pattern is to write the failing check first and return immediately: the first "
        "problem found is the one that stops the robot, so it is the one the operator "
        "needs to read."
    ),
    TABLE(
        ["You write", "The interpreter does", "Common surprise"],
        [
            ["`if value:`", "apply truthiness", "0.0 and '0' are not what you assumed"],
            ["`elif x:`", "test only if every earlier test failed", "order encodes priority"],
            ["`x is None`", "compare identity with the None singleton", "`== None` is a style smell"],
            ["`a if c else b`", "produce one of two values", "it is an expression, not a statement"],
        ],
    ),
]

TERMS = [
    ["Conditional statement", "A header and suite that runs when a condition is truthy."],
    ["Condition", "Any expression whose truthiness selects a branch."],
    ["Truthiness", "The boolean value Python assigns to any object."],
    ["Falsy", "One of the few values that evaluate as False."],
    ["Branch", "One of the alternative paths a conditional offers."],
    ["elif", "An additional branch tested only if the earlier ones failed."],
    ["Conditional expression", "`a if condition else b`, usable as a value."],
    ["Guard clause", "An early return that rejects invalid input early."],
    ["Decision table", "Data that encodes a policy instead of control flow."],
    ["Off-by-one", "A boundary error, e.g. `<` where `<=` was meant."],
]

LESSON["summary"] = [
    MD(
        "A conditional in Python tests truthiness, not truth. Only `False`, `None`, "
        "zero, the empty string and empty containers are falsy, and that small set is "
        "where most conditional bugs live - a battery reading of `0.0` is a perfectly "
        "valid value that a bare `if battery_pct:` will silently discard."
    ),
    MD(
        "The `elif` chain encodes a priority, not a set of independent tests. Writing "
        "separate `if` statements instead means the last match wins, which is almost "
        "never the intent, and it becomes a real defect the moment two conditions "
        "overlap. Ordering branches from most to least severe is what makes the first "
        "reported problem the one an operator should act on."
    ),
    MD(
        "The professional pattern for anything safety-relevant is the guard chain: test "
        "the most severe condition, return immediately with a reason, and return the "
        "same shape from every branch. That structure is testable - a test asserts the "
        "exact reason, not just a boolean - and it scales: adding a new case means "
        "adding a check, not editing a growing tangle of nesting. When the branches stop "
        "fitting comfortably in an `elif` chain, move the policy into a table of "
        "predicates so it becomes data you can unit test and review."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "Python tests truthiness, so 0.0, '' and [] are all falsy.",
            "Use `elif` for mutually exclusive bands; the first match wins.",
            "Order branches by severity so the first failure is the most urgent one.",
            "Use `is None` to test absence, not `== None` or truthiness.",
            "Compare measured floats with a tolerance, never with `==`.",
            "Return a value from a decision function instead of printing inside it.",
            "Give every branch the same return shape so callers never special-case.",
            "Move a growing policy into a decision table once the chain gets long.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "[Compound statements - the if statement](https://docs.python.org/3/reference/compound_stmts.html#the-if-statement)",
            "[Conditional expressions](https://docs.python.org/3/reference/expressions.html#conditional-expressions)",
            "[Truth value testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)",
            "[PEP 8 - use a maximum line length of 79](https://peps.python.org/pep-0008/)",
            "[Structural pattern matching](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement)",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Classify a value by its kind and emptiness",
        difficulty="MEDIUM",
        learning_objectives=["Distinguish absence from emptiness.", "Apply truthiness deliberately."],
        concepts_tested=["truthiness", "is None", "isinstance"],
        problem_statement=(
            "Write `classify(value)` returning 'missing' for None, 'empty' for a falsy "
            "value that is not None, 'number' for a real int or float, and 'other' "
            "otherwise. Bools must not be classified as numbers."
        ),
        requirements=["Test None first.", "Exclude bool explicitly."],
        constraints=["Never raise for any object."],
        input_description="Any Python object.",
        expected_output="One of four labels.",
        example_input="classify(0.0)",
        example_output="'empty'",
        edge_cases=["None gives 'missing'.", "[] gives 'empty'.", "True gives 'other'.", "'0' gives 'other' because it is truthy text."],
        hints=["Order the branches: None, then falsy, then numeric, then fallback."],
        success_criteria=["0.0 gives 'empty'.", "None gives 'missing'.", "True gives 'other'."],
        optional_extension="Return 'empty' only for containers, not for zero numbers.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Assign a battery band",
        difficulty="MEDIUM",
        learning_objectives=["Write an elif chain.", "Define boundaries exactly."],
        concepts_tested=["elif", "comparisons", "thresholds"],
        problem_statement=(
            "Write `band(pct)` returning 'CRITICAL' at or below 8, 'LOW' below 20, and "
            "'OK' otherwise. Use a single chain so exactly one band applies."
        ),
        requirements=["Use elif, not separate if statements.", "Define each boundary once."],
        constraints=["Reject non-numeric input with TypeError."],
        input_description="A numeric battery percentage.",
        expected_output="One of three band labels.",
        example_input="band(8.0)",
        example_output="'CRITICAL'",
        edge_cases=["8.0 is CRITICAL because the first test is <=.", "19.9 is LOW.", "20.0 is OK."],
        hints=["The most severe test comes first and returns immediately."],
        success_criteria=["8.0 gives 'CRITICAL'.", "20.0 gives 'OK'."],
        optional_extension="Add a 'CHARGING' band for values above 95.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Test strictly for a positive number",
        difficulty="MEDIUM",
        learning_objectives=["Avoid truthiness for numbers.", "Validate the type."],
        concepts_tested=["isinstance", "bool", "comparison"],
        problem_statement=(
            "Write `is_positive(value)` returning True only for a real int or float "
            "greater than zero. Reject bools and non-numeric types with TypeError."
        ),
        requirements=["Exclude bool before the numeric check.", "Use > 0, not truthiness."],
        constraints=["Raise TypeError rather than returning False for bad types."],
        input_description="Any object.",
        expected_output="True, or a raised TypeError.",
        example_input="is_positive(0.5)",
        example_output="True",
        edge_cases=["0.0 raises nothing but returns False.", "True raises TypeError.", "'5' raises TypeError."],
        hints=["Check bool first because it is a subclass of int."],
        success_criteria=["0.5 returns True.", "0.0 returns False.", "True raises TypeError."],
        optional_extension="Return None instead of raising, controlled by a keyword.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Supply the first usable option",
        difficulty="MEDIUM",
        learning_objectives=["Use or for defaults.", "Chain alternatives."],
        concepts_tested=["or", "falsy", "defaults"],
        problem_statement=(
            "Write `first_of(*options)` returning the first truthy option, or None if "
            "every option is falsy."
        ),
        requirements=["Use or, not a loop or a conditional expression.", "Return None when nothing is usable."],
        constraints=["No more than a single return expression is allowed."],
        input_description="Any number of candidate values.",
        expected_output="The first truthy option, or None.",
        example_input="first_of('', None, 'rover-01', 'spare')",
        example_output="'rover-01'",
        edge_cases=["No arguments returns None.", "All falsy returns None.", "The first option wins even if later ones differ."],
        hints=["Fold the values together with or, starting from None."],
        success_criteria=["The example returns 'rover-01'.", "first_of() returns None."],
        optional_extension="Add a final fallback argument.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Report the sign of a number",
        difficulty="MEDIUM",
        learning_objectives=["Use a three-way branch.", "Handle zero explicitly."],
        concepts_tested=["if/elif/else", "comparison"],
        problem_statement=(
            "Write `sign_of(n)` returning 'positive', 'zero' or 'negative'. The zero "
            "case must be reached by every negative value failing the first test, not "
            "by truthiness."
        ),
        requirements=["Use a single chain.", "Return strings, not numbers."],
        constraints=["Reject non-numeric input with TypeError."],
        input_description="A real number.",
        expected_output="One of three words.",
        example_input="sign_of(-2.5)",
        example_output="'negative'",
        edge_cases=["0 gives 'zero'.", "-0.0 gives 'zero'.", "True raises TypeError."],
        hints=["Test > 0, then < 0, and let everything else fall through."],
        success_criteria=["-2.5 gives 'negative'.", "0.0 gives 'zero'."],
        optional_extension="Return the sign as an int: 1, 0 or -1.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Test a point against a geofence",
        difficulty="HARD",
        learning_objectives=["Combine conditions.", "Validate structured input."],
        concepts_tested=["and", "chained comparison", "tuples"],
        problem_statement=(
            "Write `in_geofence(x, y, bounds)` where bounds is "
            "`(x_min, x_max, y_min, y_max)`, returning True when the point is inside the "
            "rectangle. Raise ValueError when the bounds are malformed or inverted."
        ),
        requirements=["Use two chained comparisons joined by and.", "The boundaries are inclusive."],
        constraints=["Do not mutate bounds."],
        input_description="Two numbers and a four-element tuple.",
        expected_output="A boolean, or a raised ValueError.",
        example_input="in_geofence(10, 10, (0, 50, 0, 30))",
        example_output="True",
        edge_cases=["A point exactly on an edge is inside.", "A tuple of the wrong length raises ValueError.", "Inverted bounds raise ValueError."],
        hints=["Unpack the tuple first, then compare."],
        success_criteria=["(10, 10) in the example field returns True.", "A wrong-length tuple raises ValueError."],
        optional_extension="Support a circular fence using a distance calculation.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Build a safety interlock",
        difficulty="HARD",
        learning_objectives=["Order checks by severity.", "Return one consistent shape."],
        concepts_tested=["guard clauses", "elif", "dicts"],
        problem_statement=(
            "Write `interlock(state)` returning `(permitted, reason)`. Check, in order: "
            "an engaged estop, a missing battery reading, a critical battery at or below "
            "8, a low battery below 20, and tilt above 15 degrees. Every failure returns "
            "a specific reason; success returns True with 'all checks passed'."
        ),
        requirements=["The first failing check determines the reason.", "Return a tuple of (bool, str)."],
        constraints=["Missing readings are failures, not silent passes.", "Thresholds are module constants."],
        input_description="A dict of robot state.",
        expected_output="A tuple of (bool, str).",
        example_input="interlock({'estop': True, 'battery_pct': 90})",
        example_output="(False, 'emergency stop is engaged')",
        edge_cases=["A missing battery_pct is a failure.", "estop True outranks a low battery.", "An empty state dict fails on the missing reading."],
        hints=["Return immediately from each failure; the order is the policy."],
        success_criteria=["estop True gives the estop reason even with a flat battery.", "A healthy state returns True."],
        optional_extension="Return every failed check as a list instead of the first.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Grade a score against bands",
        difficulty="HARD",
        learning_objectives=["Data-driven banding.", "Validate then decide."],
        concepts_tested=["dictionaries", "iteration", "validation"],
        problem_statement=(
            "Write `grade(score, bands)` where bands is a tuple of "
            "`(minimum, label)` pairs in descending order, returning the label of the "
            "first band whose minimum the score meets. Raise ValueError for a score "
            "outside 0 to 100."
        ),
        requirements=["Bands are data, not a chain of ifs.", "Return the first match."],
        constraints=["Do not hard-code the band values."],
        input_description="A numeric score and a tuple of bands.",
        expected_output="A label string.",
        example_input="grade(85, ((85, 'A'), (70, 'B'), (50, 'C')))",
        example_output="'A'",
        edge_cases=["A score below every band raises ValueError.", "A score of exactly 70 gives 'B'.", "0 gives the lowest band."],
        hints=["Loop over the bands and return on the first match."],
        success_criteria=["85 gives 'A'.", "70 gives 'B'."],
        optional_extension="Return the next band needed to pass.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Report every failed check at once",
        difficulty="HARD",
        learning_objectives=["Collect rather than stop.", "Keep a uniform shape."],
        concepts_tested=["comprehensions", "filtering", "aggregation"],
        problem_statement=(
            "Write `failed_checks(checks)` where checks is a sequence of "
            "`(label, passed)` pairs, returning a sorted list of the labels whose value "
            "is falsy. Return an empty list when everything passed."
        ),
        requirements=["One pass, no early return.", "The result is sorted."],
        constraints=["Do not mutate the input."],
        input_description="A sequence of (label, passed) pairs.",
        expected_output="A sorted list of failed labels.",
        example_input="failed_checks([('battery', False), ('link', True), ('tilt', False)])",
        example_output="['battery', 'tilt']",
        edge_cases=["An empty sequence gives an empty list.", "All passing gives an empty list.", "Duplicate labels both appear."],
        hints=["A list comprehension with a condition is the whole answer."],
        success_criteria=["The example returns ['battery', 'tilt']."],
        optional_extension="Return the labels sorted by severity given an ordering table.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Validate a state-machine transition",
        difficulty="HARD",
        learning_objectives=["Model a policy as data.", "Reject invalid moves."],
        concepts_tested=["dicts", "sets", "validation"],
        problem_statement=(
            "Write `can_transition(current, target, rules)` where rules maps each state "
            "to a set of allowed next states, returning True when the move is allowed. "
            "An unknown state in either position returns False rather than raising."
        ),
        requirements=["Use the rules table only.", "Never raise for an unknown state."],
        constraints=["Do not hard-code any state name."],
        input_description="Two state names and a rules dict.",
        expected_output="A boolean.",
        example_input="can_transition('IDLE', 'ACTIVE', {'IDLE': {'ACTIVE'}, 'ACTIVE': {'IDLE'}})",
        example_output="True",
        edge_cases=["A self-transition that is not listed returns False.", "An unknown state returns False.", "An empty rules table returns False."],
        hints=["A get with an empty set default makes unknown states fall through safely."],
        success_criteria=["IDLE to ACTIVE returns True.", "IDLE to STOPPED returns False."],
        optional_extension="Return the sorted list of legal targets from a state.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "def classify(value) -> str:\n"
            "    if value is None:\n"
            "        return 'missing'\n"
            "    if not value:\n"
            "        return 'empty'\n"
            "    if isinstance(value, bool):\n"
            "        return 'other'\n"
            "    if isinstance(value, (int, float)):\n"
            "        return 'number'\n"
            "    return 'other'"
        ),
        explanation=(
            "The branch order carries the whole design. None must be tested before the "
            "falsy check because None is itself falsy and would otherwise be reported as "
            "empty. The bool test sits between the two numeric checks because bool "
            "inherits from int and would otherwise be reported as a number."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="'0' is truthy text, so it reaches the final branch and is 'other'.",
        alternative_approaches="A table of (test, label) pairs keeps the order visible in data.",
        testing="assert classify(0.0) == 'empty'\nassert classify(None) == 'missing'\nassert classify(True) == 'other'\nassert classify([0]) == 'other'",
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "CRITICAL_PCT = 8.0\n"
            "LOW_PCT = 20.0\n"
            "\n"
            "\n"
            "def band(pct) -> str:\n"
            "    if isinstance(pct, bool) or not isinstance(pct, (int, float)):\n"
            "        raise TypeError(f'battery must be a number, got {type(pct).__name__}')\n"
            "    if pct <= CRITICAL_PCT:\n"
            "        return 'CRITICAL'\n"
            "    if pct < LOW_PCT:\n"
            "        return 'LOW'\n"
            "    return 'OK'"
        ),
        explanation=(
            "Each threshold appears exactly once, so the boundary between CRITICAL and "
            "LOW is defined by the first test alone. Using <= for the critical band and "
            "< for the low band means the value 8.0 has one unambiguous home rather than "
            "belonging to both or neither."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="A value above 100 is still 'OK'; the function bands, it does not validate range.",
        alternative_approaches="bisect over a sorted band table is faster for many bands.",
        testing="assert band(8.0) == 'CRITICAL'\nassert band(19.9) == 'LOW'\nassert band(20.0) == 'OK'\nassert band(7.9) == 'CRITICAL'",
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "def is_positive(value) -> bool:\n"
            "    if isinstance(value, bool) or not isinstance(value, (int, float)):\n"
            "        raise TypeError(f'expected a real number, got {type(value).__name__}')\n"
            "    return value > 0"
        ),
        explanation=(
            "The explicit comparison `> 0` is the point of the exercise: truthiness would "
            "answer a different question and would return False for -1 and 0 alike. "
            "Rejecting bool explicitly is required because bool is a subclass of int and "
            "would otherwise pass the numeric check."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="-0.0 is not greater than zero, so it returns False rather than raising.",
        alternative_approaches="numbers.Real excludes complex but still admits bool.",
        testing="assert is_positive(0.5) is True\nassert is_positive(0.0) is False\nassert is_positive(-1.0) is False",
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "def first_of(*options):\n"
            "    for option in options:\n"
            "        if option:\n"
            "            return option\n"
            "    return None"
        ),
        explanation=(
            "The explicit loop is used here rather than a clever fold because it keeps "
            "the result assignment visible and returns the *value*, not a bool. Falsy "
            "options are skipped without short-circuiting, so the function still "
            "examines every candidate."
        ),
        complexity="Time O(n) in the options; space O(1).",
        edge_cases="No arguments leaves the result as None.",
        alternative_approaches="itertools.chain plus filter is shorter but obscures the default.",
        testing="assert first_of('', None, 'rover-01', 'spare') == 'rover-01'\nassert first_of() is None\nassert first_of(0, False) is None",
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "def sign_of(n) -> str:\n"
            "    if isinstance(n, bool) or not isinstance(n, (int, float)):\n"
            "        raise TypeError(f'expected a real number, got {type(n).__name__}')\n"
            "    if n > 0:\n"
            "        return 'positive'\n"
            "    if n < 0:\n"
            "        return 'negative'\n"
            "    return 'zero'"
        ),
        explanation=(
            "Testing both signs explicitly leaves zero as the fall-through case, which "
            "is the only value that satisfies neither. Deriving zero from a falsy check "
            "would be shorter and wrong: it would also catch values that are merely "
            "falsy, such as an empty string."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="-0.0 satisfies neither test and correctly returns 'zero'.",
        alternative_approaches="math.copysign distinguishes negative zero, which the words cannot.",
        testing="assert sign_of(-2.5) == 'negative'\nassert sign_of(0.0) == 'zero'\nassert sign_of(1) == 'positive'",
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "def in_geofence(x, y, bounds) -> bool:\n"
            "    if not isinstance(bounds, (tuple, list)) or len(bounds) != 4:\n"
            "        raise ValueError(f'bounds must be four numbers, got {bounds!r}')\n"
            "    x_min, x_max, y_min, y_max = (float(v) for v in bounds)\n"
            "    if x_min > x_max or y_min > y_max:\n"
            "        raise ValueError('bounds are inverted')\n"
            "    return x_min <= x <= x_max and y_min <= y <= y_max"
        ),
        explanation=(
            "Validating the shape before unpacking means a malformed fence produces a "
            "clear ValueError instead of an unpacking error from the interpreter. Two "
            "chained comparisons joined by and express the rectangle directly, with "
            "inclusive edges as the specification requires."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="A point exactly on a corner is inside the fence.",
        alternative_approaches="A dataclass would give the bounds named fields and better errors.",
        testing="FIELD = (0.0, 50.0, 0.0, 30.0)\nassert in_geofence(10, 10, FIELD) is True\nassert in_geofence(60, 10, FIELD) is False\nassert in_geofence(0, 0, FIELD) is True",
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "CRITICAL_BATTERY_PCT = 8.0\n"
            "LOW_BATTERY_PCT = 20.0\n"
            "MAX_TILT_DEG = 15.0\n"
            "\n"
            "\n"
            "def interlock(state: dict) -> tuple[bool, str]:\n"
            "    if state.get('estop'):\n"
            "        return False, 'emergency stop is engaged'\n"
            "    battery = state.get('battery_pct')\n"
            "    if battery is None:\n"
            "        return False, 'battery reading is missing'\n"
            "    if battery <= CRITICAL_BATTERY_PCT:\n"
            "        return False, 'battery is critical'\n"
            "    if battery < LOW_BATTERY_PCT:\n"
            "        return False, 'battery is low'\n"
            "    if state.get('tilt_deg', 0.0) > MAX_TILT_DEG:\n"
            "        return False, 'robot is tilted beyond the limit'\n"
            "    if not state.get('link_ok', True):\n"
            "        return False, 'radio link is down'\n"
            "    return True, 'all checks passed'"
        ),
        explanation=(
            "Each guard returns immediately, so the most severe condition is always the "
            "one reported. Using state.get for battery and an explicit None test is what "
            "distinguishes a missing reading from a reading of zero - a falsy check "
            "would report a flat battery as missing, or worse, let it through."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="An empty state dict fails on the missing battery reading, not on a crash.",
        alternative_approaches="A list of (test, message) pairs makes the ordering data rather than code.",
        testing="assert interlock({'estop': True, 'battery_pct': 90}) == (False, 'emergency stop is engaged')\nassert interlock({'battery_pct': 90}) == (True, 'all checks passed')\nassert interlock({})[0] is False",
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "def grade(score, bands) -> str:\n"
            "    if isinstance(score, bool) or not isinstance(score, (int, float)):\n"
            "        raise TypeError('score must be a number')\n"
            "    if not 0 <= score <= 100:\n"
            "        raise ValueError(f'score out of range: {score!r}')\n"
            "    for minimum, label in bands:\n"
            "        if score >= minimum:\n"
            "            return label\n"
            "    raise ValueError(f'score {score!r} is below every band')"
        ),
        explanation=(
            "The bands are data, so adding a grade means adding a tuple rather than "
            "editing control flow - which is what makes the policy testable. Iterating "
            "in descending order and returning on the first match gives the usual "
            "'highest band reached' semantics without any comparison logic."
        ),
        complexity="Time O(b) for b bands; space O(1).",
        edge_cases="A score of exactly a band minimum receives that band, because the test is >=.",
        alternative_approaches="bisect_right over a sorted list of minimums is logarithmic.",
        testing="BANDS = ((85, 'A'), (70, 'B'), (50, 'C'))\nassert grade(85, BANDS) == 'A'\nassert grade(70, BANDS) == 'B'\nassert grade(50, BANDS) == 'C'",
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "def failed_checks(checks) -> list[str]:\n"
            "    failures = [label for label, passed in checks if not passed]\n"
            "    return sorted(failures)"
        ),
        explanation=(
            "A single comprehension collects every failure, which is the whole point: a "
            "guard chain would report only the first problem and force the operator "
            "through several repair cycles. Sorting makes the output deterministic so it "
            "can be compared in a test or sent as a stable log field."
        ),
        complexity="Time O(n log n) in the checks; space O(f) for failures.",
        edge_cases="An empty input produces an empty list rather than raising.",
        alternative_approaches="Return a count as well when only the volume matters.",
        testing="assert failed_checks([('battery', False), ('link', True), ('tilt', False)]) == ['battery', 'tilt']\nassert failed_checks([]) == []\nassert failed_checks([('a', True)]) == []",
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "def can_transition(current, target, rules: dict) -> bool:\n"
            "    allowed = rules.get(current, set())\n"
            "    return target in allowed"
        ),
        explanation=(
            "The get with an empty-set default makes an unknown state a legal no-op "
            "rather than a KeyError, which is the right behaviour for a policy check: "
            "an unrecognised state is not a permitted move. The rules table is the only "
            "source of truth, so the state machine is data a test can inspect."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="A self-transition is only allowed when the rules list it explicitly.",
        alternative_approaches="Validating the state names and raising is stricter but breaks the fail-safe property.",
        testing="RULES = {'IDLE': {'ACTIVE'}, 'ACTIVE': {'IDLE'}}\nassert can_transition('IDLE', 'ACTIVE', RULES) is True\nassert can_transition('IDLE', 'STOPPED', RULES) is False\nassert can_transition('NOPE', 'IDLE', RULES) is False",
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
            "CRITICAL_PCT, LOW_PCT, MAX_TILT_DEG = 8.0, 20.0, 15.0\n"
            "\n"
            "\n"
            "def interlock(state: dict) -> tuple[bool, str]:\n"
            "    \"\"\"Severity-ordered guard chain, self-contained.\"\"\"\n"
            "    if state.get('estop'):\n"
            "        return False, 'emergency stop is engaged'\n"
            "    battery = state.get('battery_pct')\n"
            "    if battery is None:\n"
            "        return False, 'battery reading is missing'\n"
            "    if battery <= CRITICAL_PCT:\n"
            "        return False, 'battery is critical'\n"
            "    if battery < LOW_PCT:\n"
            "        return False, 'battery is low'\n"
            "    if state.get('tilt_deg', 0.0) > MAX_TILT_DEG:\n"
            "        return False, 'robot is tilted beyond the limit'\n"
            "    return True, 'all checks passed'\n"
            "\n"
            "\n"
            "def field_state(robot, tilt_deg: float = 2.0) -> dict:\n"
            "    \"\"\"Build an interlock input from live telemetry.\"\"\"\n"
            "    state = robot.status()\n"
            "    return {\n"
            "        'estop': False,\n"
            "        'battery_pct': state['battery_pct'],\n"
            "        'tilt_deg': tilt_deg,\n"
            "    }"
        ),
        explanation=(
            "Building the interlock input from the simulator means the policy is tested "
            "against the real values the course already uses, not against invented "
            "numbers. The guard chain is inlined so this solution stands alone, and the "
            "return shape means the caller can log the reason without parsing text."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="A robot constructed with a tiny battery is rejected as critical.",
        alternative_approaches="Reusing the lesson's interlock avoids duplication in a real codebase.",
        testing="robot = SimulatedRobot(name='field-01', battery_wh=48.0)\npermitted, reason = interlock(field_state(robot))\nassert permitted is True\ndrained = SimulatedRobot(name='field-02', battery_wh=48.0)\ndrained.move(distance_m=40.0, speed_mps=1.0)\nassert interlock(field_state(drained))[0] is False",
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="What does `if value:` actually test?",
        choices=[
            "Whether value is literally True.",
            "The truthiness of value.",
            "Whether value is not None.",
            "Whether value is a number.",
        ],
        answer=1,
        kind="conceptual",
        explanation=(
            "The header is any expression, and the interpreter applies truthiness to its "
            "result. A value can be truthy without being True, and falsy without being "
            "False, which is the source of most conditional bugs."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="What does this print?\n\nx = 0\nif x:\n    print('yes')\nelse:\n    print('no')",
        choices=[
            "no",
            "yes",
            "0",
            "It raises a NameError.",
        ],
        answer=0,
        kind="code_output",
        explanation=(
            "Zero is falsy, so the else suite runs. Note that no error is raised: the "
            "branch is simply skipped, which is exactly why the failure is so quiet."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question=(
            "Given pct = 10, what is `level` after this code runs?\n\n"
            "if pct < 20:\n    level = 'LOW'\nif pct < 50:\n    level = 'MEDIUM'"
        ),
        choices=[
            "'LOW'",
            "None, because level was never defined in that path",
            "'MEDIUM'",
            "It raises an UnboundLocalError.",
        ],
        answer=2,
        kind="debugging",
        explanation=(
            "Both conditions are evaluated independently and 10 satisfies both, so the "
            "second assignment overwrites the first. Using elif makes the branches "
            "mutually exclusive and the last match no longer wins by accident."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="Why does `if battery_pct:` skip a battery reading of exactly 0.0?",
        choices=[
            "Because a float cannot be compared for truthiness.",
            "Because Python treats 0.0 as False and refuses to evaluate it.",
            "Because the variable is not defined at that point.",
            "Because 0.0 is falsy, so the branch is simply not entered.",
        ],
        answer=3,
        kind="identify_error",
        explanation=(
            "Zero of any numeric type is falsy. The branch is skipped without any error, "
            "so a legitimately empty battery is treated as though the check did not "
            "apply at all."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="What does `elif` do that a second `if` statement does not?",
        choices=[
            "It tests a branch only when every earlier condition was false, so the first match wins.",
            "It runs every branch and keeps the last result.",
            "It executes the branches in parallel.",
            "It is required by the syntax after an if.",
        ],
        answer=0,
        kind="reasoning",
        explanation=(
            "elif makes the branches mutually exclusive and encodes a priority. A "
            "separate if re-tests the value and the last match wins, which turns "
            "overlapping bands into a silent defect."
        ),
        reference="lesson.ipynb - Syntax",
    )
)

QUIZ.append(
    quiz(
        question="Which condition correctly tests whether a sensor reading is missing?",
        choices=[
            "`if not reading:`",
            "`if reading is None:`",
            "`if reading == None:`",
            "`if reading:`",
        ],
        answer=1,
        kind="multiple_choice",
        explanation=(
            "`is None` compares identity with the None singleton and says exactly what "
            "it means. The truthiness forms also reject a legitimate reading of zero, "
            "and `== None` is a style smell that linters flag."
        ),
        reference="lesson.ipynb - Best Practices",
    )
)

QUIZ.append(
    quiz(
        question=(
            "What does this print?\n\n"
            "def band(pct):\n"
            "    if pct <= 8:\n"
            "        return 'CRITICAL'\n"
            "    elif pct < 20:\n"
            "        return 'LOW'\n"
            "    return 'OK'\n\n"
            "print(band(8))"
        ),
        choices=[
            "'LOW'",
            "'OK'",
            "It raises a TypeError.",
            "'CRITICAL'",
        ],
        answer=3,
        kind="code_output",
        explanation=(
            "The first test uses <= so the boundary value 8 belongs to the critical "
            "band. Had it used <, the value would fall into the low band - a one "
            "character difference that changes a safety outcome."
        ),
        reference="lesson.ipynb - Syntax",
    )
)

QUIZ.append(
    quiz(
        question="Why compare a measured float against a threshold with a tolerance?",
        choices=[
            "Because equality on floats is slow.",
            "Because floats are stored as text in memory.",
            "Because a measured value rarely lands exactly on the literal.",
            "Because tolerance makes the comparison cheaper.",
        ],
        answer=2,
        kind="reasoning",
        explanation=(
            "Binary floating point represents most decimal values only approximately, "
            "so a reading intended to be exactly 20.0 is usually very slightly off it. "
            "The problem is the representation, not the measurement."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="Why does the interlock check for an engaged estop before anything else?",
        choices=[
            "So the most severe condition is the one reported, which is the one to act on.",
            "Because Python requires the first check to be a boolean.",
            "Because it makes the function faster.",
            "Because elif cannot follow an if with a return.",
        ],
        answer=0,
        kind="robotics",
        explanation=(
            "Each guard returns immediately, so ordering by severity means the operator "
            "always reads the most urgent fault first rather than whichever condition "
            "happened to be written at the top."
        ),
        reference="lesson.ipynb - Code Walkthrough",
    )
)

QUIZ.append(
    quiz(
        question="Which structure scales best as a safety policy grows?",
        choices=[
            "A deeply nested if/else block.",
            "A table of (predicate, message) pairs iterated in severity order.",
            "The same long elif chain copied into every module.",
            "Printing a message and returning None from each branch.",
        ],
        answer=1,
        kind="implementation_choice",
        explanation=(
            "A table makes the policy data, so a new check is a new entry rather than "
            "new control flow, and each rule can be tested on its own. A growing chain "
            "copied between modules drifts immediately."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

MINI_PROJECT = {
    "title": "Mini-Project: Safety Policy Evaluator",
    "brief": (
        "Build a small safety policy engine for a field robot. Given a dict of state, "
        "it must report whether the drive circuit may be energised and exactly which "
        "check failed first."
    ),
    "scenario": (
        "A delivery cart must not move with a flat battery, an engaged estop, an unsafe "
        "tilt or a dead radio link. The operator sees one line in the log and needs it to "
        "name the actual problem."
    ),
    "rationale": (
        "Encoding the policy as data with an explicit severity order is the pattern "
        "every safety-critical service in this course will reuse."
    ),
    "requirements": [
        "Keep the rules in a table of (label, predicate, message) in severity order.",
        "Evaluate the table and return the first failure with its message.",
        "Return a dict with `permitted`, `reason` and the battery percentage.",
        "Treat a missing battery reading as a failure, not as a pass.",
        "Never raise for any dict the simulator can produce.",
    ],
    "constraints": [
        "Standard library only.",
        "No printing inside the policy function.",
        "Thresholds live in module constants, not in the rule table.",
    ],
    "deliverables": [
        "`policy.py` with the rules table and the evaluation function.",
        "`test_policy.py` with at least twelve assertions.",
        "A README section listing each rule, its threshold and its severity.",
    ],
    "steps": [
        "Define the thresholds as module constants.",
        "Build the rules table in severity order.",
        "Implement evaluate(state) returning the report dict.",
        "Write tests for each individual rule.",
        "Write a test proving the first failure wins when several are violated.",
    ],
    "expected_behavior": (
        "A healthy state returns permitted True. Any violation returns permitted False "
        "with the reason naming the most severe rule that failed."
    ),
    "acceptance": [
        "All assertions pass from a clean run.",
        "Each rule is covered by at least one test.",
        "The severity ordering is proven by a test with multiple failures.",
        "A missing reading is reported, never silently permitted.",
    ],
    "extensions": [
        "Return every failed rule rather than only the first.",
        "Add a `strict` mode that also requires a recent link check.",
        "Serialise the report as JSON for the fleet dashboard.",
    ],
}

RESEARCH = {
    "question": (
        "How often does a threshold comparison on a simulated sensor reading land "
        "exactly on the boundary value?"
    ),
    "hypothesis": (
        "Readings generated by a continuous physical model essentially never equal a "
        "boundary exactly, so the choice between < and <= changes no real outcomes."
    ),
    "experiment": [
        STEPS(
            [
                "Read a large number of simulated sensor readings using shared/robo_x_sim.",
                "Count how many equal a chosen threshold value exactly.",
                "Count how many differ from it by less than 1e-9.",
                "Record the raw counts below before drawing any conclusion.",
            ]
        ),
    ],
    "data": [
        CODE_CELL(
            "# Record your raw counts - one row per threshold tested.\n"
            "# Copy real values from your actual runs; do not invent them.\n"
            "#\n"
            "# | threshold | readings | exact matches | within 1e-9 |"
        ),
    ],
    "analysis": [
        MD(
            "Report the fraction of exact matches. If it is zero, say so plainly: the "
            "practical consequence is that the boundary choice matters only for inputs "
            "a human typed, not for sensor data."
        ),
    ],
    "result": [
        MD(
            "State the observed fraction and whether the hypothesis held. Record any "
            "threshold that did produce exact matches, such as a value supplied "
            "directly by a test fixture."
        ),
    ],
    "interpretation": [
        MD(
            "Explain why simulated continuous quantities rarely land exactly on a "
            "decimal boundary, and name at least two threats to validity, including the "
            "seed and the resolution of the underlying model."
        ),
    ],
    "conclusion": [
        MD(
            "Give your verdict and state the boundary rule you would adopt for a "
            "production safety threshold, justifying it in one sentence."
        ),
    ],
    "extensions": [
        "Repeat with a discrete sensor whose readings are integers.",
        "Measure how close the nearest readings get to the threshold.",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Field Robot Drive Interlock",
    "context": (
        "An agricultural field robot may only drive when its battery, tilt and radio "
        "link are all within limits. The operator must be told which check failed."
    ),
    "mission": (
        "Implement `may_drive(state)` that returns a decision dict naming the first "
        "failing check in severity order, using the simulator's live readings."
    ),
    "requirements": [
        "Reject an engaged estop before any other consideration.",
        "Reject a missing battery reading, a critical battery and a low battery in order.",
        "Reject tilt above 15 degrees and a dead radio link.",
        "Return a dict with `permitted` (bool) and `reason` (str).",
    ],
    "constraints": [
        "Keep the rules in a table iterated in severity order.",
        "Never raise for any dict the simulator can produce.",
        "Complete well inside the 10 ms control budget.",
    ],
    "interface": "def may_drive(state: dict) -> dict:",
    "success_criteria": [
        "A healthy robot returns permitted True with reason 'all checks passed'.",
        "An estop outranks a low battery in the reported reason.",
        "A depleted battery returns permitted False naming the battery.",
    ],
    "extension": (
        "Return every failed rule in severity order instead of only the first, and "
        "explain which one a supervisor should act on immediately."
    ),
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Replace 'a condition is a bool' with 'a condition is truthiness'.",
        "Make elif's priority semantics explicit and contrast it with repeated ifs.",
        "Install the guard chain as the shape for any safety decision.",
    ],
    "misconceptions": [
        [
            "An if condition must be a boolean.",
            "Any expression is allowed; the interpreter applies truthiness to it.",
        ],
        [
            "Zero is truthy because it is a real value.",
            "Every zero is falsy, so a legitimate reading of 0.0 is skipped.",
        ],
        [
            "Several if statements are equivalent to elif.",
            "They are not: the last match wins rather than the first.",
        ],
        [
            "== None works for testing absence.",
            "Use `is None`; equality against a singleton is a style smell linters flag.",
        ],
    ],
    "difficult_concepts": [
        "Trusting that a measured value never lands on a threshold.",
        "Ordering branches by severity and understanding why it is a policy statement.",
        "Moving a growing elif chain into a decision table.",
    ],
    "demonstrations": [
        "Print the truthiness of a table of values including 0.0, '0' and [0].",
        "Run the two independent-if version and the elif version for an overlapping band.",
        "Build a decision table and add a rule without touching any control flow.",
    ],
    "discussion": [
        "Should a missing sensor reading be treated as 'nominal' or as 'failed'?",
        "When is a deeply nested if more readable than a flat chain?",
    ],
    "student_errors": [
        [
            "A flat battery is allowed to drive",
            "The check used truthiness and 0.0 was falsy",
            "Compare explicitly, or test `is not None` for presence",
        ],
        [
            "A reading of 30 is reported as LOW",
            "Two independent if statements; the second overwrote the first",
            "Use elif so only one branch can win",
        ],
        [
            "The wrong reason is logged",
            "Checks were ordered by convenience rather than by severity",
            "Order the guard chain most severe first",
        ],
    ],
    "pacing": (
        "90 minutes of lesson with live demonstrations, then 2 hours of exercises. Do not "
        "rush the truthiness table: it is the single idea this topic exists to install."
    ),
    "extensions": [
        "Ask students to write a truth table for a three-band function and find the bugs.",
        "Have them convert their elif chain into a decision table and compare the tests.",
    ],
    "assessment": (
        "Grade against rubric.md. Exercises 7 and 10 carry the signal: they require the "
        "student to encode a policy as ordered data."
    ),
    "support": (
        "Give students the finished interlock from the walkthrough and ask them to add "
        "one new rule, so the severity ordering is visible before they write it."
    ),
    "extension_fast": (
        "Ask for a short note on how the policy table would be validated against a "
        "changing set of safety requirements."
    ),
}

RUBRIC = {
    "artifacts": [
        ["exercises.ipynb", "40%", "All 10 exercises implemented and edge-cased."],
        ["mini_project.ipynb", "25%", "policy.py plus its test suite."],
        ["robotics_challenge.ipynb", "25%", "Drive interlock fails safe."],
        ["research.ipynb", "10%", "Real measurements with a defensible conclusion."],
    ],
    "criteria": [
        ["Correctness", "30", "Every band, boundary and missing-input case is handled."],
        ["Policy structure", "25", "Severity order is explicit and provably first-wins."],
        ["Code quality", "25", "PEP 8 naming, docstrings, small focused functions."],
        ["Reasoning", "20", "Truthiness and boundary claims explained in writing."],
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
            "Every exercise implemented, boundaries tested on both sides, and the "
            "severity ordering is proven by a test with several simultaneous failures.",
        ],
        [
            "Merit",
            "Most exercises correct; the policy is correct but a truthiness check is used "
            "for a value where zero is legitimate, and that case is untested.",
        ],
        [
            "Pass",
            "Core requirements met, but the branches overlap or the reason reported is not "
            "the most severe failure.",
        ],
        [
            "Fail",
            "Repeated if statements with overlapping bands, or a missing reading is "
            "treated as a pass.",
        ],
    ],
}

TOPIC = topic(
    topic_id="2.1",
    title="Conditional Statements",
    module=2,
    module_title="Control Flow and Loops",
    directory="01_conditional_statements",
    summary=(
        "How a condition is evaluated, why truthiness is the source of most "
        "conditional bugs, and how to structure a safety-critical decision so it can "
        "be tested and reasoned about."
    ),
    why_it_matters=(
        "Every control decision a robot makes is a conditional: whether to drive, whether "
        "to arm, whether a reading is trustworthy. A condition that is quietly wrong "
        "produces no error - it simply takes the wrong branch, which is far more "
        "dangerous than a crash."
    ),
    objectives=[
        "Explain that an if header accepts any expression and applies truthiness.",
        "List the falsy values and predict the outcome for each.",
        "Use elif to express mutually exclusive bands with a defined priority.",
        "Distinguish a missing reading from a reading of zero.",
        "Structure a multi-check decision as a severity-ordered guard chain.",
        "Encode a growing policy as a decision table rather than control flow.",
    ],
    prerequisites=[
        "Topic 1.5 Core Data Types and Type Conversion",
        "Topic 1.6 Operators and Expressions",
    ],
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
