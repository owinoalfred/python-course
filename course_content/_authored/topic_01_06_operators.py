"""Topic 1.6 - Operators and Expressions.

Hand-authored to the Course Content Standard. The spine: operators are ordinary
syntax with a precedence order, two of them return values rather than booleans,
and bitwise flags are how a compact status word is decoded.
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
        "Python's operators fall into a small number of families, and each family has "
        "a different return type. Arithmetic operators return numbers. Comparison "
        "operators return a bool. The membership tests return a bool. The bitwise "
        "operators work on integers bit by bit. The logical operators `and`, `or` and "
        "`not` are the odd ones out: they return one of their *operands*, not "
        "necessarily a bool. That single fact explains a great deal of otherwise "
        "mysterious behaviour."
    ),
    CODE_CELL(
        "a, b = 48, 16\n"
        "print('arithmetic :', a + b, a - b, a * b, a / b, a // b, a % b, a ** 2)\n"
        "print('division   : 48 / 16 =', 48 / 16, type(48 / 16).__name__)\n"
        "print('comparison :', a > b, a == b, a != b)\n"
        "print('membership :', 16 in (16, 32), 64 in (16, 32))\n"
        "print('bitwise    :', a & b, a | b, a ^ b, a << 1, a >> 1)"
    ),
    MD(
        "`and` and `or` short-circuit and return an operand. That is a feature, not a "
        "quirk: it is how Python expresses a default value without a ternary, and how "
        "a guard clause protects an expression from a division that would fail."
    ),
    CODE_CELL(
        "label = ''\n"
        "print('or returns  :', repr(label or 'unnamed'))   # returns the right operand\n"
        "name = 'rover-01'\n"
        "print('and returns :', repr(name and name.upper()))\n"
        "\n"
        "print('bool() them :', bool(label or 'unnamed'), bool(name and name.upper()))\n"
        "\n"
        "total = 0\n"
        "print('short circuit:', total or 1 / 0 if False else (total or 'default'))\n"
        "print('division safe:', (total or 1) and 'computed')"
    ),
    NOTE(
        "The walrus operator",
        "`:=` binds a name as part of an expression, so `if (n := len(items)) > 10:` "
        "computes a length once and tests it. Use it when it removes a duplicated "
        "computation, not because it is shorter.",
    ),
]

LESSON["formal_theory"] = [
    MD(
        "Precedence determines grouping. In Python it follows one rule: **everything "
        "else binds tighter than comparison**. So `1 + 2 == 3` is `(1 + 2) == 3`, and "
        "`not a == b` is `not (a == b)`, not `(not a) == b`. Bitwise `&`, `|` and `^` "
        "bind *tighter* than comparison but *looser* than arithmetic - the reverse of "
        "C, which surprises programmers arriving from other languages."
    ),
    EQUATION(
        "lambda < or < and < not < in/is/<=/>/!=/== < | < ^ < & < <<,>> "
        "< +,- < *,/,//,% < ** < unary < ()"
    ),
    MD(
        "Operators are not built into the language. Each one is a method call: `a + b` "
        "invokes `a.__add__(b)`, and `a < b` invokes `a.__lt__(b)`. That is why a class "
        "you write can support `+` by defining `__add__`, and it is also why operator "
        "overloading can surprise a reader who assumes `+` always means addition."
    ),
    CODE_CELL(
        "import dis\n"
        "\n"
        "\n"
        "def add_then_compare(a, b):\n"
        "    return a + b == 3\n"
        "\n"
        "\n"
        "print('source :', 'a + b == 3')\n"
        "print('values :', add_then_compare(1, 2))\n"
        "print('co_names:', add_then_compare.__code__.co_names)\n"
        "\n"
        "for instruction in dis.get_instructions(add_then_compare):\n"
        "    if instruction.opname in {'BINARY_OP', 'COMPARE_OP'}:\n"
        "        print('  ', instruction.opname, instruction.argval)"
    ),
    TABLE(
        ["Family", "Operators", "Returns"],
        [
            ["Arithmetic", "`+ - * / // % **`", "a number"],
            ["Comparison", "`== != < <= > >=`", "a bool"],
            ["Chained", "`0 <= x <= 100`", "a bool"],
            ["Logical", "`and or not`", "**an operand**"],
            ["Membership", "`in`, `not in`", "a bool"],
            ["Bitwise", "`& | ^ ~ << >>`", "an int"],
            ["Identity", "`is`, `is not`", "a bool"],
        ],
    ),
]

LESSON["syntax"] = [
    MD(
        "An **expression** produces a value; a **statement** does something with it. "
        "Almost every operator is part of an expression, and most expressions can be "
        "used as a statement - but a statement is not an expression, which is why you "
        "cannot write `x = if a else b`."
    ),
    CODE_CELL(
        "battery_wh = 48.0\n"
        "max_speed_mps = 1.5\n"
        "\n"
        "# comparison chains read as mathematics does\n"
        "in_range = 0 < battery_wh <= 100\n"
        "print('chain       :', in_range)\n"
        "\n"
        "# the conditional expression, used as a value\n"
        "verdict = 'LOW' if battery_wh < 20 else 'OK'\n"
        "print('conditional :', verdict)\n"
        "\n"
        "# the walrus operator binds a name inside the expression\n"
        "if (n := len('rover-01')) > 3:\n"
        "    print('walrus      :', n)"
    ),
    MD("The anti-pattern:"),
    CODE(
        "if not battery_wh > 20:      # double negative: hard to read\n"
        "    alert()\n"
        "\n"
        "if battery_wh <= 20:         # say what you mean\n"
        "    alert()\n"
        "\n"
        "a & b == 0                   # binds as (a & b) == 0, NOT a & (b == 0)\n"
        "a & (b == 0)                 # what C programmers often expect",
        lang="text",
    ),
    WARN(
        "Not is a keyword, not an operator",
        "`not x` binds more loosely than comparison, so `not a == b` means "
        "`not (a == b)`. If you want the other grouping you must parenthesise it.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - the arithmetic family in context.**"),
    CODE_CELL(
        "distance_m = 30.0\n"
        "speed_mps = 1.5\n"
        "elapsed_s = 20.0\n"
        "\n"
        "print('time needed  :', distance_m / speed_mps)\n"
        "print('whole seconds:', distance_m // speed_mps)\n"
        "print('remainder    :', distance_m % speed_mps)\n"
        "print('scale x2     :', distance_m * 2, speed_mps ** 2)\n"
        "print('unary minus  :', -distance_m, +distance_m)"
    ),
    MD("**Example 2 - string operators.**"),
    CODE_CELL(
        "name = 'rover-01'\n"
        "print('concatenate :', name + '-ready')\n"
        "print('repeat      :', 'ab' * 3)\n"
        "print('membership  :', 'rover' in name, 'truck' in name)\n"
        "print('slice       :', name[0:5], name[-2:])\n"
        "print('reverse     :', name[::-1])"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "Two things that surprise newcomers: division always returns a float, and a "
        "comparison chain is a single chained call that short-circuits, so "
        "`0 < x < 1` cannot blow up in the middle."
    ),
    CODE_CELL(
        "print('7 / 2  ->', 7 / 2, type(7 / 2).__name__)\n"
        "print('7 // 2 ->', 7 // 2, type(7 // 2).__name__)\n"
        "print('7 % 2  ->', 7 % 2)\n"
        "\n"
        "battery_pct = 50\n"
        "print('0 < 50 <= 100 :', 0 < battery_pct <= 100)\n"
        "print('0 < 500 <= 100:', 0 < 500 <= 100)\n"
        "\n"
        "# negative floor division rounds towards minus infinity, not to zero\n"
        "print('-7 // 2 :', -7 // 2)\n"
        "print('-7 % 2  :', -7 % 2)"
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "Bitwise operators let a compact integer carry several status flags at once, "
        "which is how firmware status words are normally stored. This is exactly the "
        "shape of a robotics status register."
    ),
    CODE_CELL(
        "CHARGING = 0b0001\n"
        "LOW_BATTERY = 0b0010\n"
        "OBSTACLE = 0b0100\n"
        "ESTOP = 0b1000\n"
        "\n"
        "status = CHARGING | LOW_BATTERY\n"
        "print('status      :', bin(status))\n"
        "print('charging?   :', bool(status & CHARGING))\n"
        "print('obstacle?   :', bool(status & OBSTACLE))\n"
        "print('set a flag  :', bin(status | OBSTACLE))\n"
        "print('clear a flag:', bin(status & ~OBSTACLE))\n"
        "print('toggle      :', bin(status ^ OBSTACLE))"
    ),
    MD(
        "The three operations to remember: `| value` sets bits, `& ~value` clears them, "
        "and `^ value` toggles them. A mask is simply an integer whose set bits mark the "
        "positions of interest."
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "Below is a status-word decoder. It is the standard pattern for turning a "
        "packed firmware register into a dictionary a supervisor can reason about."
    ),
    CODE_CELL(
        "\"\"\"status_flags.py - decode a packed status word into named flags.\"\"\"\n"
        "from __future__ import annotations\n"
        "\n"
        "CHARGING = 0b0001\n"
        "LOW_BATTERY = 0b0010\n"
        "OBSTACLE = 0b0100\n"
        "ESTOP = 0b1000\n"
        "\n"
        "KNOWN = {\n"
        "    'CHARGING': CHARGING,\n"
        "    'LOW_BATTERY': LOW_BATTERY,\n"
        "    'OBSTACLE': OBSTACLE,\n"
        "    'ESTOP': ESTOP,\n"
        "}\n"
        "\n"
        "\n"
        "def decode_status(word: int) -> dict:\n"
        "    \"\"\"Split a status word into active flags and unused bits.\n"
        "\n"
        "    Returns a dict with the active flag names, the raw word, and\n"
        "    any bits that are set but not defined in KNOWN.\n"
        "    \"\"\"\n"
        "    if not isinstance(word, int) or isinstance(word, bool):\n"
        "        raise TypeError('status word must be an int')\n"
        "    if word < 0:\n"
        "        raise ValueError('status word must not be negative')\n"
        "    active = [name for name, mask in KNOWN.items() if word & mask]\n"
        "    defined = 0\n"
        "    for mask in KNOWN.values():\n"
        "        defined |= mask\n"
        "    unknown = word & ~defined\n"
        "    return {\n"
        "        'word': word,\n"
        "        'flags': active,\n"
        "        'unknown_bits': bin(unknown),\n"
        "        'estop': bool(word & ESTOP),\n"
        "    }"
    ),
    MD(
        "Building the `defined` mask by OR-ing every known flag is what lets the "
        "decoder report *undefined* bits. Without it, a firmware word from a newer "
        "revision would decode silently and the extra bits would vanish - one of the "
        "most expensive kinds of interoperability bug."
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "The flag constants are module-level integers written in binary so the bit "
            "layout is visible to a reader.",
            "`KNOWN` maps names to masks, so decoding and encoding can share one table "
            "and the names appear in a consistent order.",
            "The isinstance guard rejects bool, which would otherwise pass as an int and "
            "silently decode to no flags.",
            "The negative check happens before any bit arithmetic, because `&` with a "
            "negative number produces a surprising result rather than an error.",
            "The active list comprehension applies a mask per flag, which is the standard "
            "test-and-set idiom.",
            "`defined` is built by OR-ing every known mask so undefined bits can be "
            "detected rather than discarded.",
            "`~defined` flips all the bits, so `word & ~defined` isolates exactly the "
            "bits nobody has a name for.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - assuming bitwise and comparison have the same precedence.**"),
    CODE(
        "flag & mask == 0        # parsed as (flag & mask) == 0\n"
        "flag & (mask == 0)      # a completely different expression\n"
        "\n"
        "flag & mask == 0        # usually what you meant; parenthesise anyway",
        lang="text",
    ),
    MD("**Mistake 2 - using `~` without masking.**"),
    CODE(
        "value & ~OBSTACLE       # correct: clears the bit\n"
        "value ^ OBSTACLE        # correct: toggles the bit\n"
        "\n"
        "value & ~value          # always 0 - a common but pointless idiom",
        lang="text",
    ),
    MD("**Mistake 3 - double negatives.**"),
    CODE(
        "if not battery_pct > 20:     # hard to read and easy to get wrong\n"
        "    alert()\n"
        "\n"
        "if battery_pct <= 20:        # states the rule directly\n"
        "    alert()",
        lang="text",
    ),
    MD("**Mistake 4 - forgetting that `/` always returns a float.**"),
    CODE(
        "7 / 2    # 3.5  (float)\n"
        "7 // 2   # 3    (int)\n"
        "\n"
        "int(7 / 2)  # 3 - convert deliberately when you mean truncation",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "When an expression gives the wrong answer, the fault is nearly always "
        "precedence. Print the value of each sub-expression separately, or parenthesise "
        "explicitly and see whether the answer changes."
    ),
    CODE_CELL(
        "flag, mask = 0b0110, 0b0010\n"
        "print('flag          :', bin(flag))\n"
        "print('flag & mask   :', bin(flag & mask))\n"
        "print('mask == 0     :', mask == 0)\n"
        "print('precedence    :', flag & mask == 0)\n"
        "print('parenthesised :', (flag & mask) == 0)\n"
        "print('other grouping:', flag & (mask == 0))"
    ),
    CODE_CELL(
        "import ast\n"
        "\n"
        "source = 'not a == b'\n"
        "tree = ast.parse(source, mode='eval')\n"
        "print('source  :', source)\n"
        "print('structure:', ast.dump(tree.body, indent=2)[:200])"
    ),
    NOTE(
        "The AST shows the grouping",
        "ast.parse with mode='eval' builds the tree without evaluating anything. "
        "Printing the node types tells you exactly how the parser grouped the "
        "expression, which settles any precedence argument immediately.",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Parenthesise mixed-precedence expressions; do not rely on the reader's memory.",
            "Use `//` and `%` deliberately rather than casting the result of `/`.",
            "Prefer a comparison chain to `a >= b and b <= c` when it reads the same.",
            "Never use a bare `except` around an expression that can divide by zero.",
            "Name every bit constant and build masks from a single table.",
            "Mask with `& ~flag` when clearing; avoid the `& ~value` idiom.",
            "Keep the conditional expression in an assignment, not inside a call.",
            "Use the walrus operator only when it removes a genuine duplicate computation.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "Operators are not where optimisation opportunities usually live. A bitwise "
        "test on an int is constant time; a division costs a little more than an "
        "addition but is still nanoseconds. The expression that costs you is almost "
        "always the one that calls a function or builds a collection inside a loop."
    ),
    MD(
        "Two genuine micro-patterns are worth knowing. Replacing repeated "
        "`len(x) > 0` with a direct truth test saves a function call, and hoisting an "
        "invariant sub-expression out of a loop avoids recomputing it. Neither matters "
        "until the loop runs millions of iterations. In a robotics control loop the "
        "cost that dominates is usually I/O or the sleep at the end of the cycle, not "
        "the arithmetic, so measure before touching the expression at all."
    ),
    TIP(
        "Prefer clarity, then measure",
        "Write the clearest correct expression, profile the surrounding code, and only "
        "then consider rewriting the arithmetic.",
    ),
]

LESSON["pythonic_approaches"] = [
    MD("Accumulating with a loop versus the builtins that say what you mean."),
    CODE_CELL(
        "readings = [0.4, 0.6, 0.5, 0.9]\n"
        "\n"
        "# before: an explicit accumulator\n"
        "total = 0.0\n"
        "for value in readings:\n"
        "    total += value\n"
        "\n"
        "# after: the intent, named\n"
        "print('total :', sum(readings))\n"
        "print('any   :', any(v > 0.8 for v in readings))\n"
        "print('all   :', all(0 <= v <= 1 for v in readings))\n"
        "\n"
        "# a default without a ternary\n"
        "label = ''\n"
        "print('label :', label or 'unnamed')"
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "Firmware reports state as a packed word precisely so that one integer carries "
        "many independent facts. The bitwise operators are how a Python supervisor "
        "reads and writes that word, and how it must do so without disturbing the flags "
        "it does not own."
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
        "CHARGING, LOW_BATTERY, OBSTACLE, ESTOP = 1, 2, 4, 8\n"
        "\n"
        "robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\n"
        "state = robot.status()\n"
        "\n"
        "word = 0\n"
        "if state['battery_pct'] < 20:\n"
        "    word |= LOW_BATTERY\n"
        "if robot.read_sensor('distance') < 1.0:\n"
        "    word |= OBSTACLE\n"
        "\n"
        "print('status word :', bin(word))\n"
        "print('low battery :', bool(word & LOW_BATTERY))\n"
        "print('obstacle    :', bool(word & OBSTACLE))"
    ),
]

LESSON["engineering_example"] = [
    MD(
        "A guarded division that never raises, written so the intent is obvious at the "
        "call site."
    ),
    CODE_CELL(
        "def safe_divide(numerator, denominator, default=0.0):\n"
        "    \"\"\"Divide, returning `default` instead of raising on a zero divisor.\"\"\"\n"
        "    if denominator == 0:\n"
        "        return default\n"
        "    return numerator / denominator\n"
        "\n"
        "\n"
        "def mean_or_zero(values):\n"
        "    return safe_divide(sum(values), len(values))\n"
        "\n"
        "\n"
        "print('mean of three :', mean_or_zero([1.0, 2.0, 3.0]))\n"
        "print('mean of empty :', mean_or_zero([]))"
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Predict the type of `7 / 2`, `7 // 2` and `7 % 2` before running them.",
            "Write a chained comparison that is True only for values in 0 to 100, and "
            "verify it against several inputs.",
            "Build a status word with two flags set, print it in binary, then clear one "
            "flag and print it again.",
            "Write an expression using `or` that supplies a default name without an "
            "`if` statement.",
        ]
    ),
    CODE_CELL(
        "print(7 / 2, 7 // 2, 7 % 2)\n"
        "\n"
        "for value in (-1, 0, 50, 100, 101):\n"
        "    print(f'{value:>4} in range:', 0 <= value <= 100)\n"
        "\n"
        "word = 0b0110\n"
        "print('word       :', bin(word))\n"
        "print('cleared    :', bin(word & ~0b0010))\n"
        "\n"
        "name = ''\n"
        "print('default    :', name or 'unnamed')"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: an expression is a small machine with one output.** Each "
        "operator is a stage. Precedence decides the order the stages run, and the "
        "type of the value leaving each stage decides what the next stage is allowed "
        "to accept. When an expression gives the wrong answer, you are looking for a "
        "stage running in the wrong order, or a stage fed the wrong kind of value."
    ),
    TABLE(
        ["You write", "Runs as", "Easy to miss"],
        [
            ["`a + b == c`", "`(a + b) == c`", "comparison binds loosest"],
            ["`not a == b`", "`not (a == b)`", "`not` is looser than `==`"],
            ["`x and y`", "returns `x` or `y`", "an operand, not a bool"],
            ["`x or y`", "returns `x` or `y`", "short-circuits"],
            ["`a & b == 0`", "`(a & b) == 0`", "bitwise binds tighter than `==`"],
            ["`a if cond else b`", "one of the two values", "an expression, not a statement"],
        ],
    ),
]

TERMS = [
    ["Operator", "A symbol performing an operation, such as `+` or `==`."],
    ["Expression", "Code that produces a value."],
    ["Statement", "Code that performs an action; does not necessarily produce a value."],
    ["Precedence", "The rules that decide how operators group."],
    ["Short-circuit", "Stopping evaluation once the result is known."],
    ["Floor division", "`//`, which rounds towards minus infinity."],
    ["Modulo", "`%`, the remainder after floor division."],
    ["Chained comparison", "`0 <= x <= 100`, evaluated as a single chained call."],
    ["Bitmask", "An integer whose set bits mark positions of interest."],
    ["Walrus operator", "`:=`, which binds a name inside an expression."],
    ["Operator overloading", "Defining dunder methods so your class supports an operator."],
]

LESSON["summary"] = [
    MD(
        "Operators group into families that agree on their return type. Arithmetic "
        "returns numbers, comparison and membership return bools, bitwise operators "
        "return ints - and `and`, `or` and `not` return *operands*. That last fact is "
        "not a quirk: it is what makes `value or default` the shortest correct way to "
        "express a default, and what makes `total or 1` a safe guard before a division."
    ),
    MD(
        "Precedence in Python has one memorable rule: everything else binds tighter "
        "than comparison. That is why `1 + 2 == 3` is `(1 + 2) == 3` and `not a == b` "
        "is `not (a == b)`. Bitwise operators sit between arithmetic and comparison, the "
        "reverse of C. Parenthesising mixed expressions costs nothing and removes a "
        "whole class of reading errors, so treat it as a habit rather than an admission "
        "that you forgot the table."
    ),
    MD(
        "For robotics, the bitwise family deserves particular attention. Firmware packs "
        "many independent facts into one integer, and reading or writing one flag without "
        "disturbing the others is a masking exercise: `value | FLAG` sets, "
        "`value & ~FLAG` clears, `value ^ FLAG` toggles, and `value & FLAG` tests. The "
        "discipline that makes this safe is building the defined-bit mask from a single "
        "table, so an unknown bit from a newer firmware revision is reported rather than "
        "silently discarded."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "`/` always returns a float; use `//` and `%` when you mean whole numbers.",
            "`and` and `or` return an operand, not necessarily a bool.",
            "Comparison binds looser than arithmetic and than the bitwise operators.",
            "`not` binds looser than comparison, so `not a == b` means `not (a == b)`.",
            "Chained comparisons read like mathematics and short-circuit safely.",
            "Bitwise: `|` sets, `& ~` clears, `^` toggles, `&` tests.",
            "Parenthesise mixed-precedence expressions for the reader.",
            "Build the defined-bit mask from one table so unknown bits are reported.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "[Expressions and simple statements](https://docs.python.org/3/reference/expressions.html)",
            "[Operator precedence table](https://docs.python.org/3/reference/expressions.html#operator-precedence)",
            "[Truth value testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)",
            "[PEP 572 - Assignment expressions](https://peps.python.org/pep-0572/) - the walrus operator.",
            "[Python in a Nutshell: operators](https://github.com/dabeaz/1706dab4700b25ed0b73544bd54334b8c4c8d2b1)",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Divide without raising on zero",
        difficulty="MEDIUM",
        learning_objectives=["Guard a division.", "Return a documented default."],
        concepts_tested=["arithmetic", "conditionals", "defaults"],
        problem_statement=(
            "Write `safe_divide(numerator, denominator, default=0.0)` that divides and "
            "returns `default` when the denominator is zero. Non-numeric arguments "
            "must raise TypeError."
        ),
        requirements=["Check the denominator before dividing.", "Reject bool."],
        constraints=["Never let ZeroDivisionError escape."],
        input_description="Two numbers and an optional default.",
        expected_output="A float, or the default.",
        example_input="safe_divide(10, 4)",
        example_output="2.5",
        edge_cases=["A zero denominator returns the default.", "A negative denominator works normally.", "A string argument raises TypeError."],
        hints=["Test `denominator == 0` before the division."],
        success_criteria=["10 / 4 gives 2.5.", "1 / 0 gives 0.0."],
        optional_extension="Return None instead when default is None.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Test a value against an inclusive range",
        difficulty="MEDIUM",
        learning_objectives=["Use a comparison chain.", "Express a range rule."],
        concepts_tested=["comparisons", "chaining"],
        problem_statement=(
            "Write `in_range(value, low, high)` returning True when `low <= value <= "
            "high`, using a single chained comparison rather than an `and`."
        ),
        requirements=["Use one chained comparison.", "Return a bool."],
        constraints=["Reject non-numeric input by returning False."],
        input_description="A value and two bounds.",
        expected_output="A boolean.",
        example_input="in_range(50, 0, 100)",
        example_output="True",
        edge_cases=["The bounds are inclusive.", "A non-numeric value returns False.", "low equal to high works."],
        hints=["`low <= value <= high` is already the whole answer."],
        success_criteria=["0 and 100 are both inside the range.", "'50' returns False."],
        optional_extension="Swap the bounds automatically so low is never above high.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Choose a battery verdict",
        difficulty="MEDIUM",
        learning_objectives=["Use a conditional expression.", "Keep the result a value."],
        concepts_tested=["conditional expression", "comparisons"],
        problem_statement=(
            "Write `battery_verdict(pct)` returning 'LOW' below 20, 'MEDIUM' below 50, "
            "and 'OK' otherwise, using a chained comparison to test the ranges."
        ),
        requirements=["Return a string, never print.", "Handle the boundaries."],
        constraints=["Use the conditional expression, not an if statement."],
        input_description="A numeric battery percentage.",
        expected_output="One of the three labels.",
        example_input="battery_verdict(35)",
        example_output="'MEDIUM'",
        edge_cases=["Exactly 20 is MEDIUM.", "Exactly 50 is OK.", "Values above 100 are OK."],
        hints=["Two conditional expressions, one nested inside the other."],
        success_criteria=["35 gives 'MEDIUM'.", "10 gives 'LOW'."],
        optional_extension="Return a dict with the label and the distance to the next band.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Count vowels in a label",
        difficulty="MEDIUM",
        learning_objectives=["Iterate a string.", "Test membership."],
        concepts_tested=["strings", "in", "membership"],
        problem_statement=(
            "Write `count_vowels(text)` returning how many of a, e, i, o and u appear, "
            "ignoring case. Non-alphabetic characters are skipped automatically."
        ),
        requirements=["Count both cases.", "Return an int."],
        constraints=["No regular expressions.", "Do not use text.count in a loop."],
        input_description="Any string.",
        expected_output="An integer count.",
        example_input="count_vowels('Rover-01')",
        example_output="2",
        edge_cases=["Empty string gives 0.", "Uppercase vowels are counted.", "Digits and punctuation are ignored."],
        hints=["A generator expression with sum() counts in one pass."],
        success_criteria=["'Rover-01' gives 2.", "'' gives 0."],
        optional_extension="Also return which vowels were present.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Average readings, ignoring junk",
        difficulty="MEDIUM",
        learning_objectives=["Filter then aggregate.", "Handle an empty result."],
        concepts_tested=["comprehensions", "builtins", "validation"],
        problem_statement=(
            "Write `average(values)` returning the mean of the numeric entries, "
            "ignoring anything that is not a real number. Return None for an empty or "
            "fully filtered list."
        ),
        requirements=["Exclude bools.", "Never raise for a mixed list."],
        constraints=["Use sum and len, or a comprehension."],
        input_description="A list of arbitrary objects.",
        expected_output="A float mean, or None.",
        example_input="average([1.0, 2.0, 'x', 3.0])",
        example_output="2.0",
        edge_cases=["Empty list returns None.", "A list of only non-numbers returns None.", "Bools are excluded."],
        hints=["Filter first with isinstance, then apply safe_divide."],
        success_criteria=["[1.0, 2.0, 'x', 3.0] gives 2.0.", "['a'] gives None."],
        optional_extension="Return the count of discarded values as well.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Decode a packed status word",
        difficulty="HARD",
        learning_objectives=["Apply bit masks.", "Report unknown bits."],
        concepts_tested=["bitwise", "dicts", "validation"],
        problem_statement=(
            "Write `decode_status(word, known)` for 'CHARGING' 1, 'LOW_BATTERY' 2, "
            "'OBSTACLE' 4 and 'ESTOP' 8, returning the active flag names, the raw word, "
            "and any bits set that `known` does not define."
        ),
        requirements=["Reject bool and negative input.", "Build the defined mask from the table."],
        constraints=["Never modify the known table."],
        input_description="A non-negative integer and a name-to-mask dict.",
        expected_output="A dict with word, flags and unknown_bits.",
        example_input="decode_status(0b0011, {'CHARGING': 1, 'LOW_BATTERY': 2, 'OBSTACLE': 4, 'ESTOP': 8})",
        example_output="{'word': 3, 'flags': ['CHARGING', 'LOW_BATTERY'], 'unknown_bits': 0}",
        edge_cases=["Zero gives no flags.", "An unknown bit such as 16 is reported.", "A bool raises TypeError."],
        hints=["OR every mask together to get the defined mask, then AND with ~defined."],
        success_criteria=["Decodes 0b0011 into two named flags.", "Reports bit 16 as unknown."],
        optional_extension="Return the unknown bit names when a name table is supplied.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Encode flag names into a word",
        difficulty="HARD",
        learning_objectives=["Build from a table.", "Validate input."],
        concepts_tested=["bitwise", "dicts", "sets"],
        problem_statement=(
            "Write `encode_flags(names, known)` returning the OR of the masks for each "
            "name. Ignore duplicates and raise ValueError for a name that is not in the "
            "table."
        ),
        requirements=["Preserve the caller's order in the result word.", "Reject unknown names."],
        constraints=["Do not mutate the known table."],
        input_description="A sequence of names and a name-to-mask dict.",
        expected_output="An integer status word.",
        example_input="encode_flags(['OBSTACLE', 'CHARGING'], {'CHARGING': 1, 'LOW_BATTERY': 2, 'OBSTACLE': 4, 'ESTOP': 8})",
        example_output="5",
        edge_cases=["An empty list gives 0.", "Duplicate names are harmless.", "An unknown name raises ValueError."],
        hints=["Fold the list with a single OR, starting from 0."],
        success_criteria=["['OBSTACLE', 'CHARGING'] gives 5.", "[] gives 0."],
        optional_extension="Return the subset of names actually recognised instead of raising.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Set, clear and test a single flag",
        difficulty="HARD",
        learning_objectives=["Read-modify-write a word.", "Be precise about the mask."],
        concepts_tested=["bitwise", "tuples", "composition"],
        problem_statement=(
            "Write `set_flag`, `clear_flag`, `toggle_flag` and `test_flag`, each taking "
            "a word and a mask, using the correct bitwise operator for its name. "
            "`clear_flag` must not disturb other bits."
        ),
        requirements=["Use |, & ~, ^ and & respectively.", "Never disturb unrelated bits."],
        constraints=["Each function is a single return statement."],
        input_description="A non-negative integer word and a non-zero mask.",
        expected_output="An integer, except test_flag which returns a bool.",
        example_input="clear_flag(0b1111, 0b0010)",
        example_output="13",
        edge_cases=["Clearing an unset bit changes nothing.", "Toggling twice restores the word.", "test_flag returns a bool."],
        hints=["Clearing means AND with the complement of the mask."],
        success_criteria=["clear_flag(0b1111, 0b0010) gives 13.", "toggle_flag applied twice is the identity."],
        optional_extension="Add a function that clears every bit except the mask.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Evaluate a simple arithmetic expression safely",
        difficulty="HARD",
        learning_objectives=["Use ast instead of eval.", "Validate an expression."],
        concepts_tested=["ast", "recursion", "validation"],
        problem_statement=(
            "Write `eval_arithmetic(text)` that evaluates an expression built from "
            "numbers, `+ - * / // % **` and parentheses. Use ast to walk the tree, and "
            "raise ValueError for anything else - in particular never call eval."
        ),
        requirements=["Support unary minus.", "Reject names, calls and attribute access."],
        constraints=["Do not use eval or exec."],
        input_description="An arithmetic expression string.",
        expected_output="The numeric result.",
        example_input="eval_arithmetic('2 + 3 * 4')",
        example_output="14",
        edge_cases=["Parentheses change the result.", "Division by zero raises ValueError.", "A name such as 'x' raises ValueError."],
        hints=["Recurse on ast.BinOp, unwrap ast.Constant, and map operators by class."],
        success_criteria=["'2 + 3 * 4' gives 14.", "'__import__(1)' raises ValueError."],
        optional_extension="Return the parsed tree alongside the value.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Report how an expression was grouped",
        difficulty="HARD",
        learning_objectives=["Inspect the parse tree.", "Explain precedence."],
        concepts_tested=["ast", "precedence", "reporting"],
        problem_statement=(
            "Write `precedence_report(text)` returning a list of "
            "`(operator, left_source, right_source)` tuples for every binary operation "
            "in the expression, in left-to-right source order."
        ),
        requirements=["Use ast.unparse to render each sub-expression.", "Do not evaluate."],
        constraints=["The input must parse; SyntaxError propagates."],
        input_description="An expression string.",
        expected_output="A list of operator descriptions.",
        example_input="precedence_report('1 + 2 * 3')",
        example_output="[('+', '1', '2 * 3'), ('*', '2', '3')]",
        edge_cases=["A single literal gives an empty list.", "Nested parentheses are all reported."],
        hints=["Walk the tree recursively, appending the parent before its children."],
        success_criteria=["'1 + 2 * 3' shows + grouping with '2 * 3' on the right.", "A literal gives []."],
        optional_extension="Return the operator depth so the nesting order is explicit.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "def safe_divide(numerator, denominator, default=0.0):\n"
            "    for value in (numerator, denominator):\n"
            "        if isinstance(value, bool) or not isinstance(value, (int, float)):\n"
            "            raise TypeError(f'not a number: {value!r}')\n"
            "    if denominator == 0:\n"
            "        return default\n"
            "    return numerator / denominator"
        ),
        explanation=(
            "The zero check must come before the division, and the type check must come "
            "before both so a string produces a clear TypeError rather than an obscure "
            "one. Rejecting bool explicitly keeps True from being used as 1."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="A negative denominator divides normally; a fractional divisor works too.",
        alternative_approaches="Using fractions.Fraction avoids the float result entirely.",
        testing="assert safe_divide(10, 4) == 2.5\nassert safe_divide(1, 0) == 0.0\nassert safe_divide(1, 0, default=None) is None",
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def in_range(value, low, high) -> bool:\n"
            "    if isinstance(value, bool) or not isinstance(value, (int, float)):\n"
            "        return False\n"
            "    return low <= value <= high"
        ),
        explanation=(
            "The chained comparison is a single expression that the interpreter "
            "rewrites into a method-chained test, so it short-circuits and cannot "
            "evaluate the second comparison when the first already fails. The type "
            "guard is required because comparing a string with a number raises."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="low equal to high accepts only that exact value.",
        alternative_approaches="Swapping the bounds first makes the function total for reversed input.",
        testing="assert in_range(50, 0, 100) is True\nassert in_range(0, 0, 100) is True\nassert in_range('50', 0, 100) is False",
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "def battery_verdict(pct) -> str:\n"
            "    return (\n"
            "        'LOW'\n"
            "        if pct < 20\n"
            "        else 'MEDIUM' if pct < 50 else 'OK'\n"
            "    )"
        ),
        explanation=(
            "The two boundary tests are ordered from most restrictive to least, so the "
            "first one that matches decides the label. Returning a string rather than "
            "printing keeps the function usable in a larger expression."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="Exactly 20 falls into MEDIUM because the test is strictly less than 20.",
        alternative_approaches="A dict of thresholds with a loop is clearer for five or more bands.",
        testing="assert battery_verdict(35) == 'MEDIUM'\nassert battery_verdict(10) == 'LOW'\nassert battery_verdict(50) == 'OK'\nassert battery_verdict(20) == 'MEDIUM'",
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "VOWELS = frozenset('aeiou')\n"
            "\n"
            "\n"
            "def count_vowels(text: str) -> int:\n"
            "    return sum(1 for ch in text.lower() if ch in VOWELS)"
        ),
        explanation=(
            "A frozenset gives O(1) membership tests, so the cost is linear in the "
            "length of the string. Lower-casing first means only lowercase letters need "
            "to be listed, and the generator expression avoids building an intermediate list."
        ),
        complexity="Time O(n); space O(1).",
        edge_cases="Digits and punctuation are simply not in the set, so they are skipped.",
        alternative_approaches="len(text) - count of consonants is equivalent but more work.",
        testing="assert count_vowels('Rover-01') == 2\nassert count_vowels('') == 0\nassert count_vowels('AEIOU') == 5",
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "def safe_divide(numerator, denominator, default=None):\n"
            "    if denominator == 0:\n"
            "        return default\n"
            "    return numerator / denominator\n"
            "\n"
            "\n"
            "def average(values) -> float | None:\n"
            "    numbers = [\n"
            "        v for v in values\n"
            "        if isinstance(v, (int, float)) and not isinstance(v, bool)\n"
            "    ]\n"
            "    if not numbers:\n"
            "        return None\n"
            "    return safe_divide(sum(numbers), len(numbers))"
        ),
        explanation=(
            "Filtering first means sum never sees a value it cannot add, so the function "
            "is total over any input list. Returning None for an empty or fully filtered "
            "result distinguishes 'no data' from 'an average of zero', which is a "
            "distinction a caller genuinely needs."
        ),
        complexity="Time O(n); space O(n) for the filtered list.",
        edge_cases="A list of only strings returns None rather than raising.",
        alternative_approaches="A generator with sum() avoids the intermediate list at the cost of a separate length.",
        testing="assert average([1.0, 2.0, 'x', 3.0]) == 2.0\nassert average([]) is None\nassert average(['a']) is None\nassert average([True, 2.0]) == 2.0",
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "def decode_status(word: int, known: dict) -> dict:\n"
            "    if isinstance(word, bool) or not isinstance(word, int):\n"
            "        raise TypeError('status word must be an int')\n"
            "    if word < 0:\n"
            "        raise ValueError('status word must not be negative')\n"
            "    active = [name for name, mask in known.items() if word & mask]\n"
            "    defined = 0\n"
            "    for mask in known.values():\n"
            "        defined |= mask\n"
            "    return {\n"
            "        'word': word,\n"
            "        'flags': active,\n"
            "        'unknown_bits': word & ~defined,\n"
            "    }"
        ),
        explanation=(
            "Folding every known mask together gives the set of bits this decoder "
            "understands, so ANDing its complement with the word isolates exactly the "
            "bits that are set but unrecognised. Reporting them is what turns a silent "
            "interoperability failure into a visible warning."
        ),
        complexity="Time O(k) for k known flags; space O(k).",
        edge_cases="Zero gives an empty flag list and zero unknown bits.",
        alternative_approaches="A dataclass return type is clearer in a larger codebase.",
        testing="KNOWN = {'CHARGING': 1, 'LOW_BATTERY': 2, 'OBSTACLE': 4, 'ESTOP': 8}\nout = decode_status(0b0011, KNOWN)\nassert out['flags'] == ['CHARGING', 'LOW_BATTERY']\nassert decode_status(0b10000, KNOWN)['unknown_bits'] == 16",
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "def encode_flags(names, known: dict) -> int:\n"
            "    word = 0\n"
            "    for name in names:\n"
            "        if name not in known:\n"
            "            raise ValueError(f'unknown flag: {name!r}')\n"
            "        word |= known[name]\n"
            "    return word"
        ),
        explanation=(
            "Folding the masks together with OR is commutative and idempotent, so "
            "duplicate names are harmless and the caller's order does not affect the "
            "result. Validating inside the loop means the error names the offending flag "
            "rather than the whole batch."
        ),
        complexity="Time O(n) for n names; space O(1).",
        edge_cases="An empty name list returns 0, which is the natural empty word.",
        alternative_approaches="Using functools.reduce with operator.or_ is shorter but cannot validate.",
        testing="KNOWN = {'CHARGING': 1, 'LOW_BATTERY': 2, 'OBSTACLE': 4, 'ESTOP': 8}\nassert encode_flags(['OBSTACLE', 'CHARGING'], KNOWN) == 5\nassert encode_flags([], KNOWN) == 0\nassert encode_flags(['CHARGING', 'CHARGING'], KNOWN) == 1",
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "def set_flag(word: int, mask: int) -> int:\n"
            "    return word | mask\n"
            "\n"
            "\n"
            "def clear_flag(word: int, mask: int) -> int:\n"
            "    return word & ~mask\n"
            "\n"
            "\n"
            "def toggle_flag(word: int, mask: int) -> int:\n"
            "    return word ^ mask\n"
            "\n"
            "\n"
            "def test_flag(word: int, mask: int) -> bool:\n"
            "    return bool(word & mask)"
        ),
        explanation=(
            "Each function is the single operator whose name describes it, which makes "
            "the set of four read as a specification. Clearing uses the complement of the "
            "mask so only the named bits are zeroed and every other bit in the word is "
            "preserved exactly."
        ),
        complexity="Time O(1) for all four; space O(1).",
        edge_cases="Clearing a bit that is not set returns the word unchanged.",
        alternative_approaches="A class wrapping the word gives the same four operations with less call-site noise.",
        testing="assert clear_flag(0b1111, 0b0010) == 13\nassert set_flag(0b1111, 0b10000) == 31\nassert toggle_flag(toggle_flag(5, 2), 2) == 5\nassert test_flag(0b0010, 0b0010) is True",
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "import ast\n"
            "\n"
            "OPS = {\n"
            "    ast.Add: lambda a, b: a + b,\n"
            "    ast.Sub: lambda a, b: a - b,\n"
            "    ast.Mult: lambda a, b: a * b,\n"
            "    ast.Div: lambda a, b: a / b,\n"
            "    ast.FloorDiv: lambda a, b: a // b,\n"
            "    ast.Mod: lambda a, b: a % b,\n"
            "    ast.Pow: lambda a, b: a ** b,\n"
            "}\n"
            "\n"
            "\n"
            "def _value(node):\n"
            "    if isinstance(node, ast.Constant):\n"
            "        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):\n"
            "            raise ValueError('only numeric literals are allowed')\n"
            "        return node.value\n"
            "    if isinstance(node, ast.UnaryOp):\n"
            "        operand = _value(node.operand)\n"
            "        return -operand if isinstance(node.op, ast.USub) else operand\n"
            "    if isinstance(node, ast.BinOp) and type(node.op) in OPS:\n"
            "        left, right = _value(node.left), _value(node.right)\n"
            "        try:\n"
            "            return OPS[type(node.op)](left, right)\n"
            "        except ZeroDivisionError as exc:\n"
            "            raise ValueError('division by zero') from exc\n"
            "    raise ValueError(f'unsupported expression node: {type(node).__name__}')"
        ),
        explanation=(
            "Walking the tree means only the node types we explicitly handle can be "
            "evaluated, so a call, an attribute access or a name is rejected rather than "
            "executed. The operator dispatch table is the complete allow-list, which is "
            "what makes this safe where eval would not be."
        ),
        complexity="Time O(n) in the number of nodes; space O(d) for tree depth.",
        edge_cases="Division by zero is converted into a ValueError so callers see one failure type.",
        alternative_approaches="ast.literal_eval handles only literals, not arithmetic.",
        testing="assert _value(ast.parse('2 + 3 * 4', mode='eval').body) == 14\nassert _value(ast.parse('-5 + 1', mode='eval').body) == -4",
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "import ast\n"
            "\n"
            "SYMBOLS = {\n"
            "    ast.Add: '+',\n"
            "    ast.Sub: '-',\n"
            "    ast.Mult: '*',\n"
            "    ast.Div: '/',\n"
            "    ast.FloorDiv: '//',\n"
            "    ast.Mod: '%',\n"
            "    ast.Pow: '**',\n"
            "}\n"
            "\n"
            "\n"
            "def precedence_report(text: str) -> list[tuple]:\n"
            "    report: list[tuple] = []\n"
            "\n"
            "    def walk(node):\n"
            "        if isinstance(node, ast.BinOp) and type(node.op) in SYMBOLS:\n"
            "            report.append((\n"
            "                SYMBOLS[type(node.op)],\n"
            "                ast.unparse(node.left),\n"
            "                ast.unparse(node.right),\n"
            "            ))\n"
            "            walk(node.left)\n"
            "            walk(node.right)\n"
            "\n"
            "    walk(ast.parse(text, mode='eval').body)\n"
            "    return report"
        ),
        explanation=(
            "Appending the parent before recursing produces pre-order, so the report "
            "reads from the outermost operation inwards. ast.unparse renders each "
            "sub-expression exactly as the parser understood it, which is what makes the "
            "grouping visible without evaluating anything."
        ),
        complexity="Time O(n) in the tree size; space O(d) for depth.",
        edge_cases="A bare literal has no BinOp nodes, so the report is empty.",
        alternative_approaches="Printing the tree with ast.dump is faster but far less readable for teaching.",
        testing="assert precedence_report('1 + 2 * 3') == [('+', '1', '2 * 3'), ('*', '2', '3')]\nassert precedence_report('1') == []",
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
            "CHARGING, LOW_BATTERY, OBSTACLE, ESTOP = 1, 2, 4, 8\n"
            "KNOWN = {'CHARGING': CHARGING, 'LOW_BATTERY': LOW_BATTERY, 'OBSTACLE': OBSTACLE, 'ESTOP': ESTOP}\n"
            "\n"
            "\n"
            "def read_status(robot, obstacle_threshold: float = 1.0) -> dict:\n"
            "    \"\"\"Build a status word from live telemetry, without raising.\"\"\"\n"
            "    state = robot.status()\n"
            "    word = 0\n"
            "    if state['battery_pct'] < 20:\n"
            "        word |= LOW_BATTERY\n"
            "    try:\n"
            "        if robot.read_sensor('distance') < obstacle_threshold:\n"
            "            word |= OBSTACLE\n"
            "    except SensorError:\n"
            "        word |= OBSTACLE          # an unreadable sensor is not a clear path\n"
            "    active = [name for name, mask in KNOWN.items() if word & mask]\n"
            "    return {'word': word, 'flags': active, 'battery_pct': state['battery_pct']}"
        ),
        explanation=(
            "Folding each condition into the word with OR means the caller receives one "
            "value they can forward to firmware unchanged. Treating a sensor read error "
            "as an obstacle is the safety-critical decision here: an unknown distance is "
            "treated as the dangerous case, never as a clear path."
        ),
        complexity="Time O(1) for a fixed number of flags; space O(1).",
        edge_cases="A faulty distance sensor sets OBSTACLE rather than silently clearing it.",
        alternative_approaches="Returning the individual booleans instead of a word loses the firmware compatibility.",
        testing="robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\nout = read_status(robot)\nassert out['word'] == 0\nassert out['flags'] == []",
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="What does the expression `'' or 'unnamed'` evaluate to?",
        choices=[
            "False",
            "'unnamed'",
            "''",
            "It raises a SyntaxError.",
        ],
        answer=1,
        kind="conceptual",
        explanation=(
            "`or` returns one of its operands, not a bool: the left side is falsy, so the "
            "right side is returned unchanged. Wrapping it in bool() would give True, "
            "which is almost never what the caller wanted."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="What is the value of `7 / 2` in Python 3?",
        choices=[
            "3.5",
            "3",
            "3.0",
            "It raises a ZeroDivisionError.",
        ],
        answer=0,
        kind="code_output",
        explanation=(
            "The division operator always produces a float, and true division does not "
            "truncate. Use 7 // 2 for 3 when whole-number division is what you want."
        ),
        reference="lesson.ipynb - Intermediate Examples",
    )
)

QUIZ.append(
    quiz(
        question=(
            "A safety check `if battery_pct < 20 and distance_m < 0.5:` fires when it "
            "should not. What is the most likely cause?"
        ),
        choices=[
            "The battery reading is stored as a string.",
            "The distance sensor is returning noise.",
            "The author meant the battery to be above 20 percent, not below.",
            "Python does not support and in an if statement.",
        ],
        answer=2,
        kind="debugging",
        explanation=(
            "Both operands are compared correctly; the fault is the comparison operator "
            "itself, because a low battery is the warning condition rather than the "
            "safe one. Reading the condition aloud is the fastest check."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="What is the value of `value & ~value` for any non-negative integer?",
        choices=[
            "The original value.",
            "The complement of the value.",
            "1.",
            "Always 0.",
        ],
        answer=3,
        kind="identify_error",
        explanation=(
            "Every bit that is set in the value is cleared by its own complement, and no "
            "other bit is set, so the result is always zero. It is a pointless idiom that "
            "appears in code written by analogy with a real mask operation."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="Why build a mask of all defined bits before decoding a status word?",
        choices=[
            "So unknown bits can be reported rather than silently discarded.",
            "Because bitwise operations only work on masked values.",
            "To make the decoder faster on large words.",
            "Because a negative word is otherwise unrepresentable.",
        ],
        answer=0,
        kind="reasoning",
        explanation=(
            "Firmware revisions add flags. Without a defined mask, a word from a newer "
            "revision decodes into the flags we know and the new information vanishes, "
            "which is a silent interoperability failure rather than a visible one."
        ),
        reference="lesson.ipynb - Code Walkthrough",
    )
)

QUIZ.append(
    quiz(
        question="Which expression clears a single flag from a status word without touching the others?",
        choices=[
            "word | flag",
            "word & ~flag",
            "word ^ flag",
            "word & flag",
        ],
        answer=1,
        kind="multiple_choice",
        explanation=(
            "ANDing with the complement of the mask zeroes exactly the named bits and "
            "leaves every other bit as it was. OR sets them, XOR toggles them, and AND "
            "alone only tests them."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="What is `0b1010 & 0b0110`?",
        choices=[
            "14",
            "10",
            "6",
            "2",
        ],
        answer=3,
        kind="code_output",
        explanation=(
            "Bitwise AND keeps only positions set in both operands: 1010 AND 0110 is "
            "0010, which is 2 in decimal. This is the standard test-and-set idiom used to "
            "check whether a specific flag is present."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="Why does this course use ast rather than eval to interpret an expression?",
        choices=[
            "ast is faster at arithmetic.",
            "ast enforces precedence that eval ignores.",
            "ast evaluates only the node types we explicitly allow.",
            "eval cannot handle parentheses.",
        ],
        answer=2,
        kind="implementation_choice",
        explanation=(
            "Walking the tree means names, calls and attribute access are rejected by "
            "construction, so the allow-list is the code itself. eval would execute "
            "anything the expression can reach."
        ),
        reference="solution.ipynb - Solution 9",
    )
)

QUIZ.append(
    quiz(
        question="Why should a failed distance-sensor read set the OBSTACLE flag?",
        choices=[
            "An unknown distance must be treated as the dangerous case, not a clear path.",
            "It makes the status word a larger number.",
            "It simplifies the decoder.",
            "Sensor errors are more common than obstacles.",
        ],
        answer=0,
        kind="robotics",
        explanation=(
            "Failing safe means assuming the worst state when the evidence is missing. "
            "Treating an unreadable sensor as clear would let a robot drive into an "
            "obstacle it simply failed to see."
        ),
        reference="solution.ipynb - Solution 11",
    )
)

QUIZ.append(
    quiz(
        question="Which is the idiomatic way to supply a default for an empty name?",
        choices=[
            "if not name:\n    name = 'unnamed'",
            "display = name or 'unnamed'",
            "display = name if name else 'unnamed'",
            "display = 'unnamed'.join([name])",
        ],
        answer=1,
        kind="implementation_choice",
        explanation=(
            "`or` returns the right operand when the left is falsy, which states the "
            "default in one expression. The conditional form is equivalent but longer, "
            "and the join form does not do what it looks like."
        ),
        reference="lesson.ipynb - Pythonic Approaches",
    )
)

MINI_PROJECT = {
    "title": "Mini-Project: Status Word Toolkit",
    "brief": (
        "Build a small toolkit for reading and writing a packed robot status word: "
        "encode flags from names, decode a word into names, and report any bits the "
        "toolkit does not recognise."
    ),
    "scenario": (
        "A supervisor process exchanges one integer with firmware. You need a module "
        "that both sides can rely on, and that fails loudly rather than silently when a "
        "newer firmware sets a bit you do not know."
    ),
    "rationale": (
        "Packed status words are compact, fast and easy to corrupt. A tested toolkit for "
        "them removes an entire class of intermittent, hardware-dependent bugs."
    ),
    "requirements": [
        "Define the known flags as named module-level constants.",
        "Encode a list of flag names into an integer word.",
        "Decode a word into active flag names plus any unknown bits.",
        "Provide set, clear, toggle and test operations for a single mask.",
        "Raise ValueError for a flag name that is not defined.",
    ],
    "constraints": [
        "Standard library only.",
        "Never mutate the flag table.",
        "Reject bool and negative words with a clear error.",
    ],
    "deliverables": [
        "`status_word.py` with constants, encode, decode and the four operations.",
        "`test_status_word.py` with at least twelve assertions.",
        "A README section listing each flag, its bit and its meaning.",
    ],
    "steps": [
        "Define CHARGING, LOW_BATTERY, OBSTACLE and ESTOP in binary.",
        "Implement encode_flags and decode_status against a shared table.",
        "Implement set_flag, clear_flag, toggle_flag and test_flag.",
        "Write the round-trip test: encode names, decode, compare.",
        "Add tests for an unknown bit, a negative word and a bad name.",
    ],
    "expected_behavior": (
        "Encoding a set of names and decoding the result returns the same names. A word "
        "carrying an undefined bit decodes the known flags and reports the extra bit."
    ),
    "acceptance": [
        "All assertions pass from a clean run.",
        "The round trip is exact for every subset of the known flags.",
        "Unknown bits are reported, never dropped.",
        "Every error message names the offending flag or word.",
    ],
    "extensions": [
        "Add a reverse lookup that decodes a word into names with their bit positions.",
        "Add a function that returns the flags present in one word but not another.",
        "Serialise the decoded result as JSON for the dashboard.",
    ],
}

RESEARCH = {
    "question": (
        "How much does operator choice change the runtime of a tight numeric loop "
        "compared with the loop overhead itself?"
    ),
    "hypothesis": (
        "Replacing arithmetic with bitwise equivalents, or vice versa, changes the "
        "runtime by far less than the cost of the surrounding loop."
    ),
    "experiment": [
        STEPS(
            [
                "Write a loop that sums a list of one million floats using plain addition.",
                "Write an equivalent loop using sum() and one using a generator expression.",
                "Write a version using integer bit tricks where the arithmetic allows it.",
                "Run each at least ten times and record the raw timings below.",
            ]
        ),
    ],
    "data": [
        CODE_CELL(
            "# Record your raw measurements - one row per variant per run.\n"
            "# Copy real values from your actual runs; do not invent them.\n"
            "#\n"
            "# | variant | run | seconds |"
        ),
    ],
    "analysis": [
        MD(
            "Compare the distributions rather than the means alone, and report the "
            "spread. With a noisy machine the run-to-run variation may exceed the "
            "difference between variants, which is itself the finding."
        ),
    ],
    "result": [
        MD(
            "State whether the hypothesis survived. If the differences fall inside the "
            "noise, say so directly rather than presenting a mean difference as if it "
            "were real."
        ),
    ],
    "interpretation": [
        MD(
            "Explain what dominates the measurement: the per-iteration interpreter "
            "overhead, the arithmetic itself, or the measurement harness. Name at "
            "least two threats to validity, including CPU frequency scaling."
        ),
    ],
    "conclusion": [
        MD(
            "Give your verdict and state whether you would ever rewrite working "
            "arithmetic for speed, with the measurement that would justify it."
        ),
    ],
    "extensions": [
        "Repeat with a smaller list to expose fixed setup costs.",
        "Compare against a single numpy operation on the same data.",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Status Word Controller",
    "context": (
        "During mobile robot bring-up the controller must exchange a packed status "
        "word with firmware and act on it safely, including when a sensor fails."
    ),
    "mission": (
        "Implement `status_for(robot, thresholds)` that builds a status word from live "
        "telemetry, decodes it back into named flags, and reports any undefined bits."
    ),
    "requirements": [
        "Set LOW_BATTERY when the battery percentage is below its threshold.",
        "Set OBSTACLE when the distance reading is below its threshold.",
        "Treat a sensor read failure as an obstacle, never as a clear path.",
        "Return the word, the active flag names, and any unknown bits.",
    ],
    "constraints": [
        "Build masks from a single flag table; never hard-code integers at the call site.",
        "Never raise for a failed sensor read.",
        "Complete well inside the 10 ms control budget.",
    ],
    "interface": "def status_for(robot, thresholds: dict | None = None) -> dict:",
    "success_criteria": [
        "A healthy, distant robot returns word 0 and no flags.",
        "A low battery sets exactly LOW_BATTERY.",
        "An injected sensor fault sets OBSTACLE rather than raising.",
    ],
    "extension": (
        "Add a CHARGING flag driven by the battery voltage rising between two samples, "
        "and explain how you avoid oscillation."
    ),
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Make operator return types explicit, especially for and/or.",
        "Install the habit of parenthesising mixed-precedence expressions.",
        "Give bitwise flags a concrete robotics home in the firmware status word.",
    ],
    "misconceptions": [
        [
            "`and` and `or` produce True or False.",
            "They return one of their operands, which is why `or` works as a default.",
        ],
        [
            "Bitwise operators bind more loosely than comparison, as in C.",
            "In Python they bind more tightly, which is the reverse of C.",
        ],
        [
            "`/` rounds down like `//`.",
            "True division always returns a float and does not truncate.",
        ],
        [
            "`value & ~value` is a useful mask.",
            "It is always zero and is never what the author meant.",
        ],
    ],
    "difficult_concepts": [
        "Reasoning about which grouping the parser actually chose.",
        "Understanding ~ as an infinite-bit complement and why the AND fixes it.",
        "Accepting that operators are dunder methods, not built-in syntax.",
    ],
    "demonstrations": [
        "Run precedence_report on '1 + 2 * 3' and show the grouping from the tree.",
        "Build a status word, clear one flag, and show the other bits are untouched.",
        "Toggle a flag twice to show the operation is its own inverse.",
    ],
    "discussion": [
        "Why does firmware use packed words instead of a struct of booleans?",
        "When would a dict of flags be a better representation than a bitmask?",
    ],
    "student_errors": [
        [
            "A safety condition fires on the wrong values",
            "The comparison was written backwards",
            "Read the condition aloud and check the direction",
        ],
        [
            "Clearing a flag also cleared others",
            "The code used `& ~word` or XOR on several bits at once",
            "Clear with `& ~mask` for exactly one named mask",
        ],
        [
            "A result differs from another language they know",
            "Assuming C precedence or integer division semantics",
            "Check the Python precedence table and remember `/` always returns a float",
        ],
    ],
    "pacing": (
        "90 minutes of lesson with live bit arithmetic, then 2 hours on exercises. The "
        "ast-based exercises are the stretch; accept a table-dispatch solution for a "
        "student who is stuck on the recursion."
    ),
    "extensions": [
        "Ask students to extend the flag table and prove the round trip still holds.",
        "Introduce operator overloading by implementing __lt__ on a wrapper class.",
    ],
    "assessment": (
        "Grade against rubric.md. Exercises 6 to 10 carry the signal; a student who can "
        "explain the defined mask has understood the real engineering problem."
    ),
    "support": (
        "Provide a printed bit-position table for 0 to 15 and have students decode a few "
        "by hand before coding anything."
    ),
    "extension_fast": (
        "Ask for a design note on how the flag table should grow as firmware adds bits, "
        "without breaking older decoders.",
    ),
}

RUBRIC = {
    "artifacts": [
        ["exercises.ipynb", "40%", "All 10 exercises implemented and edge-cased."],
        ["mini_project.ipynb", "25%", "status_word.py plus its test suite."],
        ["robotics_challenge.ipynb", "25%", "Status controller fails safe."],
        ["research.ipynb", "10%", "Real measurements with a defensible conclusion."],
    ],
    "criteria": [
        ["Correctness", "30", "Masking, precedence and round trips all behave as specified."],
        ["Safety behaviour", "25", "Failed sensors take the dangerous path, never the safe one."],
        ["Code quality", "25", "PEP 8 naming, docstrings, small focused functions."],
        ["Reasoning", "20", "Precedence and complexity claims explained in writing."],
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
            "Every exercise implemented, the flag round trip is exact, and an injected "
            "sensor fault produces OBSTACLE rather than an exception.",
        ],
        [
            "Merit",
            "Most exercises correct; the decoder is right but unknown bits are dropped "
            "instead of reported, and that gap is untested.",
        ],
        [
            "Pass",
            "Core requirements met, but a sensor error is swallowed and the robot is "
            "treated as having a clear path.",
        ],
        [
            "Fail",
            "Masking is wrong so flags are corrupted, or the ast exercises call eval.",
        ],
    ],
}

TOPIC = topic(
    topic_id="1.6",
    title="Operators and Expressions",
    module=1,
    module_title="Getting Started with Python",
    directory="06_operators_and_expressions",
    summary=(
        "The small set of symbols Python puts between values, what each one returns, "
        "how precedence groups them, and how a packed status word is read and written "
        "with bitwise operators."
    ),
    why_it_matters=(
        "Operators are the vocabulary of every expression you will write, and two of "
        "them - `and` and `or` - do not behave the way their names suggest. On top of "
        "that, firmware communicates state as a single packed integer, so the bitwise "
        "family is a practical requirement for anyone working with a real robot."
    ),
    objectives=[
        "Predict the return type of every operator family.",
        "Explain how precedence groups a mixed expression, and parenthesise deliberately.",
        "Use `and` and `or` as value-producing expressions, not just booleans.",
        "Apply bitwise masks to set, clear, toggle and test individual flags.",
        "Build a defined-bit mask so unknown flags are reported rather than lost.",
        "Interpret an expression safely with ast instead of eval.",
    ],
    prerequisites=[
        "Topic 1.5 Core Data Types and Type Conversion",
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
    robo_x_milestone="M1",
    robo_x_package="robo_x.core",
)
