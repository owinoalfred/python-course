"""Topic 1.5 - Core Data Types and Type Conversion.

Hand-authored to the Course Content Standard. The spine: every value that enters a
robot from the outside world arrives as text, and converting it safely is the job
this topic is about.
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
        "Python ships a small set of built-in types that cover almost everything a "
        "robot needs. `int` and `float` for measurements, `str` for text arriving from "
        "sensors and operators, `bool` for decisions, and `None` for *absent*. "
        "`list`, `tuple`, `dict` and `set` are covered in Module 3. Every value is an "
        "object with a type, and `type()` will always tell you which one you are "
        "holding - which makes introspection a practical debugging tool rather than a "
        "curiosity."
    ),
    CODE_CELL(
        "samples = [42, 3.14, 'rover-01', True, False, None, (1, 2), {'a': 1}, {1, 2}]\n"
        "for value in samples:\n"
        "    print(f'{repr(value):<12} {type(value).__name__}')"
    ),
    MD(
        "Two properties matter more than the rest at this stage. First, **immutability**: "
        "`int`, `float`, `str` and `bool` cannot be modified in place, so a function "
        "receiving one can never damage it. Second, **truthiness**: every value has a "
        "truth value, and only a small set of them are falsy. That is why `if value:` "
        "is almost always a bug when the value is a number and zero is legitimate."
    ),
    CODE_CELL(
        "falsy = [0, 0.0, '', [], {}, set(), None, False]\n"
        "truthy = [1, -1, 0.5, '0', [0], {'k': 0}, True]\n"
        "\n"
        "print('falsy  :', [bool(v) for v in falsy])\n"
        "print('truthy :', [bool(v) for v in truthy])\n"
        "\n"
        "distance_m = 0.0\n"
        "if distance_m:               # a robot that has not moved yet\n"
        "    print('moving')\n"
        "else:\n"
        "    print('stationary (distance is exactly zero)')"
    ),
    NOTE(
        "bool is a subclass of int",
        "Because True is 1 and False is 0 under the hood, isinstance(True, int) is True. "
        "That bit of inheritance is a frequent source of validation bugs: a check that "
        "accepts any number will also accept a boolean unless you exclude it explicitly.",
    ),
]

LESSON["formal_theory"] = [
    MD(
        "Python implements a **numeric tower**: `bool` is a subclass of `int`, and `int` "
        "is conceptually a parent of `float`. Mixing an `int` and a `float` in an "
        "arithmetic operation promotes the `int` to a `float` rather than raising. This "
        "is why `1 + 2.0` is `3.0` and not `3`, and why a division always produces a "
        "float."
    ),
    EQUATION(
        "int + float  ->  float        (the int is promoted, never truncated)"
    ),
    MD(
        "Integers are arbitrary precision: Python will represent an integer of any "
        "length, so overflow is not a failure mode for `int`. Floats are IEEE 754 "
        "double-precision, which means they use binary floating point and therefore "
        "cannot represent most decimal fractions exactly. That is the origin of results "
        "that surprise beginners."
    ),
    CODE_CELL(
        "print('0.1 + 0.2 =', 0.1 + 0.2)\n"
        "print('equal to 0.3?', 0.1 + 0.2 == 0.3)\n"
        "print('close enough?', abs((0.1 + 0.2) - 0.3) < 1e-9)\n"
        "\n"
        "from decimal import Decimal\n"
        "print('Decimal     :', Decimal('0.1') + Decimal('0.2'))\n"
        "\n"
        "huge = 2 ** 100\n"
        "print('2 ** 100    :', huge)\n"
        "print('as float    :', float(huge))"
    ),
    TABLE(
        ["Type", "Mutable", "Example", "Typical robotics use"],
        [
            ["`int`", "no", "48", "counts, identifiers, whole Wh"],
            ["`float`", "no", "48.5", "sensor readings, power"],
            ["`str`", "no", "'48.5'", "raw sensor and operator text"],
            ["`bool`", "no", "True", "flags and decisions"],
            ["`NoneType`", "n/a", "None", "'no value yet'"],
            ["`list`", "yes", "[1, 2]", "sequences of readings"],
            ["`dict`", "yes", "{'a': 1}", "keyed channel data"],
        ],
    ),
]

LESSON["syntax"] = [
    MD("Conversion is always explicit. There is no implicit cast in Python."),
    CODE_CELL(
        "battery_pct = '87.5'      # text from a sensor bus\n"
        "\n"
        "print('as text :', battery_pct)\n"
        "print('to float:', float(battery_pct))\n"
        "print('to int  :', int(float(battery_pct)))   # int() alone would raise\n"
        "print('to str  :', str(48.0))\n"
        "print('to bool :', bool(battery_pct))        # a non-empty string is True\n"
        "\n"
        "try:\n"
        "    int('87.5')\n"
        "except ValueError as exc:\n"
        "    print('int on a decimal string raises:', exc)"
    ),
    MD("The anti-pattern:"),
    CODE(
        "pct = '87.5'\n"
        "pct = pct * 2          # string repetition! '87.587.5', not 175.0\n"
        "\n"
        "pct = float(pct) * 2   # convert first, then compute",
        lang="text",
    ),
    WARN(
        "int() does not round",
        "int(87.5) raises ValueError rather than returning 87. It also truncates "
        "silently for floats: int(-1.9) is -1, not -2. Use round() when you mean "
        "nearest.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - the four scalar types in use.**"),
    CODE_CELL(
        "count = 3                    # int\n"
        "voltage = 12.6               # float\n"
        "label = 'front-left'         # str\n"
        "active = True                # bool\n"
        "missing = None               # NoneType\n"
        "\n"
        "for name, value in (\n"
        "    ('count', count), ('voltage', voltage), ('label', label),\n"
        "    ('active', active), ('missing', missing),\n"
        "):\n"
        "    print(f'{name:<8} {type(value).__name__:<9} {value!r}')"
    ),
    MD("**Example 2 - useful string methods for parsing.**"),
    CODE_CELL(
        "raw = '  12.60 m '\n"
        "print('stripped :', repr(raw.strip()))\n"
        "print('numeric  :', raw.strip().rstrip('m').strip())\n"
        "print('parsed   :', float(raw.strip().rstrip('m').strip()))\n"
        "print('split    :', 'a,b,c'.split(','))\n"
        "print('joined   :', '-'.join(['a', 'b', 'c']))"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "The reliable pattern for external data is a **conversion ladder**: try the "
        "narrowest type first, widen on failure, and finish with the string itself. "
        "This is what turns a configuration value into something your code can trust."
    ),
    CODE_CELL(
        "def coerce(token: str):\n"
        "    try:\n"
        "        return int(token)\n"
        "    except ValueError:\n"
        "        pass\n"
        "    try:\n"
        "        return float(token)\n"
        "    except ValueError:\n"
        "        return token\n"
        "\n"
        "\n"
        "for token in ('48', '48.5', 'auto', ''):\n"
        "    value = coerce(token)\n"
        "    print(f'{token!r:<8} -> {type(value).__name__:<5} {value!r}')"
    ),
    TIP(
        "Order matters",
        "Trying int first means '48' becomes an int rather than 48.0. That is usually "
        "what a configuration reader wants, because a whole number of Wh should not "
        "gain a spurious decimal point.",
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "Decimals that look exact are not exact in binary floating point, so equality "
        "checks against a literal can fail. Two correct responses exist: compare with a "
        "tolerance, or use `decimal.Decimal` when the decimal representation is the "
        "point."
    ),
    CODE_CELL(
        "from decimal import Decimal\n"
        "\n"
        "left, right = 0.1, 0.2\n"
        "print('float sum      :', repr(left + right))\n"
        "print('float == 0.3   :', left + right == 0.3)\n"
        "\n"
        "print('within 1e-9    :', abs((left + right) - 0.3) < 1e-9)\n"
        "\n"
        "exact = Decimal('0.1') + Decimal('0.2')\n"
        "print('decimal sum    :', exact)\n"
        "print('decimal == 0.3 :', exact == Decimal('0.3'))"
    ),
    MD(
        "Use `Decimal` for money-like accounting and for measurements where the "
        "decimal value is contractual. Use floats for ordinary sensor readings, and "
        "compare them with a tolerance rather than with `==`."
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "Below is a parsing function for raw telemetry text - the exact shape a robot "
        "receives over a serial line or an HTTP query string."
    ),
    CODE_CELL(
        "\"\"\"readings.py - turn raw telemetry text into validated floats.\"\"\"\n"
        "from __future__ import annotations\n"
        "\n"
        "MISSING = None\n"
        "\n"
        "\n"
        "def parse_readings(text: str) -> tuple[dict, list[str]]:\n"
        "    \"\"\"Parse 'channel=value' pairs into floats.\n"
        "\n"
        "    Returns (readings, problems). A malformed pair is reported by\n"
        "    name and excluded, so one bad sensor never loses the good ones.\n"
        "    \"\"\"\n"
        "    readings: dict = {}\n"
        "    problems: list[str] = []\n"
        "    for chunk in text.split(';'):\n"
        "        chunk = chunk.strip()\n"
        "        if not chunk:\n"
        "            continue\n"
        "        name, separator, raw = chunk.partition('=')\n"
        "        if not separator:\n"
        "            problems.append(f'{chunk!r}: missing =')\n"
        "            continue\n"
        "        name = name.strip()\n"
        "        try:\n"
        "            readings[name] = float(raw.strip())\n"
        "        except ValueError:\n"
        "            problems.append(f'{name}: {raw.strip()!r} is not a number')\n"
        "    return readings, problems"
    ),
    MD(
        "The key decision is to **not raise**. A telemetry stream will eventually "
        "contain a corrupt field, and a parser that dies on the first bad value takes "
        "down every other channel with it. Recording the problem and continuing keeps "
        "the rest of the data usable."
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "The docstring states the partial-success contract up front: the caller is "
            "told it gets usable data plus a list of complaints.",
            "`text.split(';')` produces the chunks; blank chunks are skipped so a "
            "trailing separator is harmless.",
            "`partition('=')` splits on the first equals sign only, so a value "
            "containing '=' is not torn apart.",
            "A chunk without '=' is reported rather than parsed, because there is no "
            "name to attach the value to.",
            "float() is called inside try/except ValueError only, so a genuinely wrong "
            "type elsewhere in the program still surfaces as an error.",
            "Only successfully converted channels enter `readings`, so downstream code "
            "can trust every value it contains.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - multiplying a numeric string.**"),
    CODE(
        "pct = '87.5'\n"
        "pct * 2            # '87.587.5' - string repetition\n"
        "\n"
        "float(pct) * 2     # 175.0",
        lang="text",
    ),
    MD("**Mistake 2 - int() on a decimal string.**"),
    CODE(
        "int('87.5')        # ValueError: invalid literal for int()\n"
        "\n"
        "int(float('87.5')) # 87 - converts first, then truncates",
        lang="text",
    ),
    MD("**Mistake 3 - trusting a value because a bool check passed.**"),
    CODE(
        "if value:                  # 0.0 and '' both skip the branch\n"
        "    publish(value)\n"
        "\n"
        "if value is not None:      # explicit absence check\n"
        "    publish(value)",
        lang="text",
    ),
    MD("**Mistake 4 - comparing floats with ==.**"),
    CODE(
        "0.1 + 0.2 == 0.3          # False\n"
        "\n"
        "abs(0.1 + 0.2 - 0.3) < 1e-9   # True - compare with a tolerance",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "When a conversion misbehaves, the useful questions are: what type is it, what "
        "does it look like when printed, and what does the conversion actually do?"
    ),
    CODE_CELL(
        "samples = ['87.5', '  87.5  ', '87,5', 'n/a', '', None, True]\n"
        "for value in samples:\n"
        "    try:\n"
        "        converted = float(value)\n"
        "        print(f'{value!r:<10} -> {converted!r}')\n"
        "    except (TypeError, ValueError) as exc:\n"
        "        print(f'{value!r:<10} -> {type(exc).__name__}: {exc}')"
    ),
    MD(
        "Note the two exception types. `ValueError` means the text is not a number, "
        "while `TypeError` means the object has no sensible numeric interpretation at "
        "all. Catching both is right at a system boundary and wrong in the middle of "
        "your own logic, where a TypeError is a bug you want to see."
    ),
    NOTE(
        "Locate the boundary",
        "When a value has the wrong type, the bug is almost never where the error was "
        "raised. It is where the value entered the program. Trace backwards to the "
        "first place it was created, not the last place it was used.",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Convert external text exactly once, at the boundary where it enters.",
            "Use a conversion ladder (int, then float, then str) for configuration.",
            "Never rely on truthiness for numeric values; compare explicitly.",
            "Check `value is not None` when None is a legitimate value.",
            "Compare floats with a tolerance, never with ==.",
            "Remember bool is a subclass of int when validating numbers.",
            "Report conversion failures with the offending name and text.",
            "Keep one bad value from destroying the whole batch.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "Type conversion is not free, but it is cheap relative to I/O: parsing a few "
        "thousand sensor readings is dominated by the file or socket read that produced "
        "them. Optimising the `float()` call itself is almost never the right "
        "investment. The optimisation that *does* pay is avoiding repeated conversion of "
        "the same value - if a channel is read in a thousand iterations, convert once "
        "outside the loop and reuse the result."
    ),
    MD(
        "`Decimal` is an order of magnitude slower than `float` because it performs "
        "arbitrary-precision decimal arithmetic. Use it where correctness demands it - "
        "accounting, contractual tolerances - and measure before applying it to a "
        "high-rate telemetry path, where a float with an explicit tolerance is both "
        "faster and more honest about the precision you actually have."
    ),
    TIP(
        "Batch, do not stream-convert",
        "If you must convert a very large batch, prefer a library routine that parses "
        "the whole column at once over a Python-level loop calling float() per item.",
    ),
]

LESSON["pythonic_approaches"] = [
    MD("Type checks: comparing against type objects versus isinstance."),
    CODE_CELL(
        "value = 48.0\n"
        "\n"
        "# before: an exact type comparison\n"
        "print('exact  :', type(value) == float)\n"
        "\n"
        "# after: isinstance, which also accepts subclasses\n"
        "print('isinstance:', isinstance(value, float))\n"
        "print('bool is an int:', isinstance(True, int))\n"
        "\n"
        "# excluding bool explicitly when a number is required\n"
        "def numeric(value):\n"
        "    return isinstance(value, (int, float)) and not isinstance(value, bool)\n"
        "\n"
        "\n"
        "print('numeric(48.0):', numeric(48.0))\n"
        "print('numeric(True):', numeric(True))"
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "Every value a robot receives from the world is text first: a serial line, an "
        "HTTP query parameter, a YAML file. The simulator returns real floats, which is "
        "precisely why the conversion step must be exercised separately - it is the one "
        "part of the pipeline that never gets tested by the hardware."
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
        "# render a real reading as text, then parse it back\n"
        "wire = f\"battery_pct={state['battery_pct']};travelled_m={state['travelled_m']}\"\n"
        "print('on the wire:', wire)\n"
        "readings, problems = parse_readings(wire)\n"
        "print('parsed      :', readings)\n"
        "print('problems    :', problems)"
    ),
]

LESSON["engineering_example"] = [
    MD(
        "A validating converter suitable for a system boundary: it reports what failed, "
        "applies an optional range, and never raises for bad external data."
    ),
    CODE_CELL(
        "def read_number(raw, *, low=None, high=None, default=None):\n"
        "    \"\"\"Convert external text to a float, reporting rather than raising.\"\"\"\n"
        "    if raw is None:\n"
        "        return default\n"
        "    if isinstance(raw, bool):\n"
        "        return default\n"
        "    if isinstance(raw, (int, float)):\n"
        "        value = float(raw)\n"
        "    else:\n"
        "        try:\n"
        "            value = float(str(raw).strip())\n"
        "        except ValueError:\n"
        "            return default\n"
        "    if low is not None and value < low:\n"
        "        return default\n"
        "    if high is not None and value > high:\n"
        "        return default\n"
        "    return value"
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Print type() and bool() for 0, 0.0, '', '0', None and False, and explain "
            "each result.",
            "Try int(), float() and bool() on the string '48.5' and record which "
            "succeed.",
            "Compute 0.1 + 0.2 - 0.3 and print it in full precision before rounding.",
            "Write `is_number(value)` that returns True for int and float but False for "
            "bool, then test it on five values.",
        ]
    ),
    CODE_CELL(
        "import math\n"
        "\n"
        "for value in (0, 0.0, '', '0', None, False):\n"
        "    print(f'{value!r:<8} bool={bool(value)}')\n"
        "\n"
        "print('int(48.5) raises:', end=' ')\n"
        "try:\n"
        "    int('48.5')\n"
        "except ValueError:\n"
        "    print('yes')\n"
        "\n"
        "print('residual:', math.fsum([0.1, 0.2]) - 0.3)\n"
        "\n"
        "def is_number(value):\n"
        "    return isinstance(value, (int, float)) and not isinstance(value, bool)"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: a typed slot, but the slot can be re-labelled.** Built-in "
        "values are sealed - an `int` or a `str` cannot be modified in place, so "
        "handing one to a function is safe. But the *name* holding the value is not "
        "sealed: you can point it at a different type at any moment. Safety comes from "
        "converting deliberately at the edges, not from the language preventing a "
        "mistake."
    ),
    TABLE(
        ["Value", "Falsy?", "Mutable?", "Safe to share?"],
        [
            ["`48`", "no", "no", "yes"],
            ["`0`", "yes", "no", "yes, but beware `if value:`"],
            ["`'48.5'`", "no", "no", "yes"],
            ["`''`", "yes", "no", "yes"],
            ["`None`", "yes", "n/a", "yes - the standard 'no value' marker"],
            ["`[1]`", "no", "yes", "only if copied or not mutated"],
        ],
    ),
]

TERMS = [
    ["Type", "The class of a value, reported by type()."],
    ["Built-in type", "A type implemented by the interpreter, such as int or str."],
    ["Conversion", "Explicitly producing a new value of another type."],
    ["Mutability", "Whether a value's contents can be changed in place."],
    ["Truthiness", "The implicit boolean value Python assigns to any object."],
    ["Falsy", "One of the few values that evaluate as False."],
    ["None", "The singleton marker for 'no value'."],
    ["Arithmetic promotion", "Mixing int and float promotes the int to float."],
    ["IEEE 754 double", "The binary floating-point format Python floats use."],
    ["Decimal", "A standard-library decimal type for exact base-10 arithmetic."],
]

LESSON["summary"] = [
    MD(
        "Python's core types are few and deliberately blunt: `int`, `float`, `str`, "
        "`bool` and `None`, with the containers following in Module 3. Four of these "
        "are immutable, which makes them safe to pass around freely; the type lives on "
        "the value rather than the name, so typing is dynamic and conversion is always "
        "explicit."
    ),
    MD(
        "Two traps account for most beginner bugs here. Truthiness bites because every "
        "value has a boolean interpretation and only a small set are falsy, so `if "
        "value:` silently skips a legitimate reading of `0.0`. And floats bite because "
        "binary floating point cannot represent most decimal fractions exactly, so "
        "`0.1 + 0.2 == 0.3` is False and must be replaced by a tolerance comparison or "
        "by `Decimal`."
    ),
    MD(
        "The professional pattern is the conversion ladder: at every system boundary, "
        "try the narrowest type, widen on failure, finish with the string, and record "
        "what failed rather than raising. A telemetry stream will eventually contain a "
        "corrupt field, and a parser that dies on it takes every other channel down with "
        "it. Parse defensively once, at the edge, and let the rest of the program trust "
        "its inputs."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "int, float, str, bool and None cover most robotics logic.",
            "Type lives on the value; the name can be rebound freely.",
            "Conversion in Python is always explicit - there are no implicit casts.",
            "A conversion ladder handles mixed configuration values safely.",
            "Only 0, 0.0, '', empty containers, None and False are falsy.",
            "bool is a subclass of int, so exclude it explicitly when validating numbers.",
            "Compare floats with a tolerance, or use Decimal where exactness is required.",
            "At a system boundary, report conversion failures instead of raising.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "[Built-in types reference](https://docs.python.org/3/library/stdtypes.html)",
            "[numeric tower - the type hierarchy](https://docs.python.org/3/reference/numerictypes.html)",
            "[decimal - fixed-point and floating-point decimal](https://docs.python.org/3/library/decimal.html)",
            "[Truth value testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)",
            "[PEP 484 - Type hints](https://peps.python.org/pep-0484/) - catching this class of bug statically.",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Name the type of a value",
        difficulty="MEDIUM",
        learning_objectives=["Use type().", "Return a readable name."],
        concepts_tested=["type()", "builtins"],
        problem_statement=(
            "Write `type_name(value)` returning the name of the value's type as a "
            "string, so `type_name(None)` gives 'NoneType' and `type_name(48.0)` gives "
            "'float'."
        ),
        requirements=["Use type() rather than a hand-written mapping.", "Return a string."],
        constraints=["Handle every type, not just the ones you tested."],
        input_description="Any Python object.",
        expected_output="A string naming the type.",
        example_input="type_name(48.0)",
        example_output="'float'",
        edge_cases=["None gives 'NoneType'.", "A list gives 'list'.", "A custom class gives its class name."],
        hints=["type(value).__name__ is the whole answer."],
        success_criteria=["Correct for int, str, list and None.", "Works for a custom class."],
        optional_extension="Add a `describe(value)` returning a human sentence.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Convert external text to a float safely",
        difficulty="MEDIUM",
        learning_objectives=["Convert defensively.", "Provide a fallback."],
        concepts_tested=["float()", "exceptions", "defaults"],
        problem_statement=(
            "Write `to_float(raw, default=0.0)` that converts text or a number to a "
            "float, returning `default` for anything that is not numeric. Booleans "
            "must be rejected."
        ),
        requirements=["Catch ValueError and TypeError.", "Reject bool explicitly."],
        constraints=["Never raise for external input."],
        input_description="A string, number, None or boolean.",
        expected_output="A float, or the default.",
        example_input="to_float('87.5')",
        example_output="87.5",
        edge_cases=["None returns the default.", "True returns the default, not 1.0.", "'  12  ' converts to 12.0.", "'n/a' returns the default."],
        hints=["Convert with str(raw).strip() after handling the numeric case."],
        success_criteria=["'87.5' gives 87.5.", "True gives the default."],
        optional_extension="Add a low and high bound that also return the default.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Clamp a value into a range",
        difficulty="MEDIUM",
        learning_objectives=["Apply bounds.", "Preserve the value type."],
        concepts_tested=["comparisons", "conditionals", "types"],
        problem_statement=(
            "Write `clamp(value, low, high)` limiting `value` to the inclusive range. "
            "Return the value unchanged when it is already inside the range."
        ),
        requirements=["Handle low == high.", "Return a number of the same kind as value."],
        constraints=["Do not mutate the arguments."],
        input_description="A number and its two bounds.",
        expected_output="A number within the range.",
        example_input="clamp(118.0, 0, 100)",
        example_output="100",
        edge_cases=["A value equal to a bound is unchanged.", "An int input returns an int.", "Reversed bounds raise ValueError."],
        hints=["Two early-return guards keep the logic flat."],
        success_criteria=["118 clamps to 100.", "42 passes through unchanged."],
        optional_extension="Raise ValueError when low > high instead of returning a value.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Describe a value in words",
        difficulty="MEDIUM",
        learning_objectives=["Branch on type.", "Produce readable output."],
        concepts_tested=["isinstance", "strings", "dispatch"],
        problem_statement=(
            "Write `describe(value)` returning a short human phrase: 'missing' for "
            "None, 'flag: True', 'number: 48.0', 'text: rover-01', 'sequence of 3' "
            "for a list or tuple, and 'mapping of 2' for a dict."
        ),
        requirements=["Check None first.", "Use isinstance for the numeric check."],
        constraints=["One branch per broad category."],
        input_description="Any Python object.",
        expected_output="A descriptive string.",
        example_input="describe(48.0)",
        example_output="'number: 48.0'",
        edge_cases=["None gives 'missing'.", "An empty list gives 'sequence of 0'.", "A dict gives 'mapping of 2'."],
        hints=["Check bool before the numeric branch so True is described as a flag."],
        success_criteria=["Produces 'flag: True' for True.", "Describes a 3-item list as 'sequence of 3'."],
        optional_extension="Fall back to the type name for unsupported objects.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Validate a sensor reading strictly",
        difficulty="MEDIUM",
        learning_objectives=["Reject the wrong type.", "Apply a range check."],
        concepts_tested=["isinstance", "bool", "validation"],
        problem_statement=(
            "Write `is_valid_reading(value, low, high)` returning True only when the "
            "value is a real int or float, is not a bool, and lies within the "
            "inclusive range."
        ),
        requirements=["Exclude bool explicitly.", "Never raise."],
        constraints=["Return False for any non-numeric type."],
        input_description="Any object plus bounds.",
        expected_output="A boolean.",
        example_input="is_valid_reading(48.0, 0, 100)",
        example_output="True",
        edge_cases=["True is rejected.", "'48' is rejected.", "0 and 100 are accepted."],
        hints=["isinstance(value, bool) must be checked before the numeric test."],
        success_criteria=["True returns False.", "'48' returns False.", "48.0 returns True."],
        optional_extension="Return a reason string instead of a bool.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Parse a telemetry line without losing good channels",
        difficulty="HARD",
        learning_objectives=["Partial success.", "Report and continue."],
        concepts_tested=["strings", "exceptions", "error reporting"],
        problem_statement=(
            "Write `parse_readings(text)` for 'a=1.5;b=bad;c=2' returning "
            "`({'a': 1.5, 'c': 2.0}, ['b is not a number'])`. Malformed chunks are "
            "reported and skipped; good ones survive."
        ),
        requirements=["Never raise for malformed input.", "Split on the first '=' only."],
        constraints=["Return a tuple of (dict, sorted list of messages)."],
        input_description="A semicolon-separated string of channel=value pairs.",
        expected_output="A tuple of readings and problems.",
        example_input="parse_readings('a=1.5;b=bad;c=2')",
        example_output="({'a': 1.5, 'c': 2.0}, [\"b: 'bad' is not a number\"])",
        edge_cases=["Empty input gives ({}, []).", "A trailing ';' is ignored.", "A chunk with no '=' is reported."],
        hints=["partition('=') gives the channel name and the raw value."],
        success_criteria=["Matches the example exactly.", "Never raises."],
        optional_extension="Add an allowed-channel list and reject unexpected names.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Normalise units to metres",
        difficulty="HARD",
        learning_objectives=["Apply a conversion table.", "Validate the unit."],
        concepts_tested=["dicts", "arithmetic", "validation"],
        problem_statement=(
            "Write `to_metres(value, unit)` converting mm, cm, m, km, in and ft to "
            "metres. Raise ValueError for an unknown unit and for a non-numeric value."
        ),
        requirements=["Use a lookup table of factors.", "Return a float."],
        constraints=["Do not use a chain of if/elif per unit."],
        input_description="A number and a unit string.",
        expected_output="The distance in metres.",
        example_input="to_metres(250, 'cm')",
        example_output="2.5",
        edge_cases=["An unknown unit raises ValueError.", "A string number raises ValueError.", "in uses exactly 0.0254."],
        hints=["A dict from unit to factor turns the whole table into one multiplication."],
        success_criteria=["250 cm gives 2.5.", "'nautical' raises ValueError."],
        optional_extension="Return the value unchanged when the unit is already 'm'.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Summarise the types in a batch",
        difficulty="HARD",
        learning_objectives=["Aggregate counts.", "Preserve information."],
        concepts_tested=["collections.Counter", "dicts", "type()"],
        problem_statement=(
            "Write `summarise_types(values)` returning a dict mapping type name to "
            "count, plus the key 'total' with the number of values. Names are sorted "
            "when the dict is built."
        ),
        requirements=["Use type(value).__name__ for the label.", "Include a 'total' key."],
        constraints=["Do not modify the input sequence."],
        input_description="A sequence of arbitrary objects.",
        expected_output="A dict of counts plus a total.",
        example_input="summarise_types([1, 2.0, 'x'])",
        example_output="{'float': 1, 'int': 1, 'str': 1, 'total': 3}",
        edge_cases=["An empty sequence gives {'total': 0}.", "bool and int are counted separately."],
        hints=["collections.Counter over the type names does the counting."],
        success_criteria=["Counts match the example.", "Counts bool separately from int."],
        optional_extension="Also report the distinct values of each type.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Compare floats with a tolerance",
        difficulty="HARD",
        learning_objectives=["Handle representation error.", "Design an API."],
        concepts_tested=["floats", "abs", "math.isclose"],
        problem_statement=(
            "Write `close_enough(a, b, tolerance=1e-9)` returning True when two floats "
            "differ by no more than the tolerance. Raise TypeError if either argument "
            "is not a real number."
        ),
        requirements=["Reject bool.", "Use abs() or math.isclose."],
        constraints=["Default tolerance is 1e-9."],
        input_description="Two numbers and an optional tolerance.",
        expected_output="A boolean.",
        example_input="close_enough(0.1 + 0.2, 0.3)",
        example_output="True",
        edge_cases=["Exact equality returns True.", "A large difference returns False.", "True is rejected as a number."],
        hints=["math.isclose(a, b, abs_tol=tolerance) is the library equivalent."],
        success_criteria=["0.1+0.2 versus 0.3 returns True.", "1.0 versus 1.1 with 1e-9 returns False."],
        optional_extension="Return the absolute difference instead of a bool.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Coerce a value through an ordered list of types",
        difficulty="HARD",
        learning_objectives=["Ordered fallback.", "Report exhaustion."],
        concepts_tested=["try/except", "callables", "error reporting"],
        problem_statement=(
            "Write `coerce(value, kinds)` that tries each callable in `kinds` in order "
            "and returns the first success. Raise ValueError naming every attempted "
            "type if all fail."
        ),
        requirements=["Catch TypeError and ValueError.", "Preserve the original exception as the cause."],
        constraints=["Try in the order given; do not sort."],
        input_description="A value and a sequence of callables.",
        expected_output="The first successful conversion.",
        example_input="coerce('48.5', [int, float, str])",
        example_output="48.5",
        edge_cases=["All failures raise ValueError listing the attempts.", "A bool input passes int() unless int is excluded."],
        hints=["Loop, try, and break out with the converted value."],
        success_criteria=["'48.5' with [int, float] returns 48.5.", "Failure message names every type tried."],
        optional_extension="Return None instead of raising when raise_on_failure is False.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code="def type_name(value) -> str:\n    return type(value).__name__",
        explanation=(
            "type() returns the class object and __name__ reads its name, so the answer "
            "is derived from the value rather than from a mapping the author maintained. "
            "That means custom classes and future built-ins are reported correctly "
            "without any extra code."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="NoneType is reported for None because its class is named NoneType.",
        alternative_approaches="type(value).__qualname__ distinguishes nested classes.",
        testing="assert type_name(48.0) == 'float'\nassert type_name(None) == 'NoneType'\nassert type_name([]) == 'list'",
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def to_float(raw, default: float = 0.0) -> float:\n"
            "    if isinstance(raw, bool):\n"
            "        return default\n"
            "    if isinstance(raw, (int, float)):\n"
            "        return float(raw)\n"
            "    try:\n"
            "        return float(str(raw).strip())\n"
            "    except (TypeError, ValueError):\n"
            "        return default"
        ),
        explanation=(
            "The bool guard comes first precisely because bool is a subclass of int, so "
            "without it True would silently become 1.0. Passing real numbers through "
            "avoids a pointless string round trip, and stripping handles the whitespace "
            "that serial output usually carries."
        ),
        complexity="Time O(n) in the text length; space O(n).",
        edge_cases="'  12  ' converts to 12.0; 'n/a' and None both return the default.",
        alternative_approaches="A single try/except around float(raw) is shorter but mishandles booleans.",
        testing="assert to_float('87.5') == 87.5\nassert to_float('  12  ') == 12.0\nassert to_float(True) == 0.0\nassert to_float('n/a', default=-1.0) == -1.0",
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "def clamp(value, low, high):\n"
            "    if low > high:\n"
            "        raise ValueError(f'low {low} is above high {high}')\n"
            "    if value < low:\n"
            "        return low\n"
            "    if value > high:\n"
            "        return high\n"
            "    return value"
        ),
        explanation=(
            "Validating the bounds before clamping means a reversed range is reported as "
            "the programming error it is, rather than silently returning a value that "
            "satisfies neither constraint. Returning the bound objects themselves "
            "preserves the numeric type of the caller."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="low equal to high returns that value for everything in range.",
        alternative_approaches="max(low, min(high, value)) is shorter but hides the reversed-bounds bug.",
        testing="assert clamp(118.0, 0, 100) == 100\nassert clamp(42, 0, 100) == 42\nassert isinstance(clamp(42, 0, 100), int)",
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "from collections.abc import Mapping, Sequence\n"
            "\n"
            "\n"
            "def describe(value) -> str:\n"
            "    if value is None:\n"
            "        return 'missing'\n"
            "    if isinstance(value, bool):\n"
            "        return f'flag: {value}'\n"
            "    if isinstance(value, (int, float)):\n"
            "        return f'number: {value}'\n"
            "    if isinstance(value, str):\n"
            "        return f'text: {value}'\n"
            "    if isinstance(value, Mapping):\n"
            "        return f'mapping of {len(value)}'\n"
            "    if isinstance(value, Sequence):\n"
            "        return f'sequence of {len(value)}'\n"
            "    return type(value).__name__"
        ),
        explanation=(
            "The ordering is the design: None and bool are tested before the general "
            "cases so they are described precisely rather than lumped in with numbers. "
            "Mapping is checked before Sequence because a dict is not a Sequence, and "
            "the final fallback keeps the function total for any object."
        ),
        complexity="Time O(1) apart from formatting the value; space O(1).",
        edge_cases="An empty list yields 'sequence of 0'; bytes yield 'bytes'.",
        alternative_approaches="A match statement on type(value) is faster but cannot cover subclasses.",
        testing="assert describe(48.0) == 'number: 48.0'\nassert describe(None) == 'missing'\nassert describe(True) == 'flag: True'\nassert describe([1, 2, 3]) == 'sequence of 3'\nassert describe({'a': 1}) == 'mapping of 1'",
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "def is_valid_reading(value, low, high) -> bool:\n"
            "    if isinstance(value, bool):\n"
            "        return False\n"
            "    if not isinstance(value, (int, float)):\n"
            "        return False\n"
            "    return low <= value <= high"
        ),
        explanation=(
            "Excluding bool explicitly is the whole point of this function: because bool "
            "inherits from int, a naive numeric check would accept True for a battery "
            "reading. Chained comparison then expresses the inclusive range in one "
            "readable expression."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="A numeric string returns False because it is not a number at all.",
        alternative_approaches="numbers.Real excludes complex numbers but still admits bool.",
        testing="assert is_valid_reading(48.0, 0, 100) is True\nassert is_valid_reading(True, 0, 100) is False\nassert is_valid_reading('48', 0, 100) is False\nassert is_valid_reading(100, 0, 100) is True",
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "def parse_readings(text: str) -> tuple[dict, list[str]]:\n"
            "    readings: dict = {}\n"
            "    problems: list[str] = []\n"
            "    for chunk in text.split(';'):\n"
            "        chunk = chunk.strip()\n"
            "        if not chunk:\n"
            "            continue\n"
            "        name, separator, raw = chunk.partition('=')\n"
            "        if not separator:\n"
            "            problems.append(f'{chunk!r}: missing =')\n"
            "            continue\n"
            "        name = name.strip()\n"
            "        try:\n"
            "            readings[name] = float(raw.strip())\n"
            "        except ValueError:\n"
            "            problems.append(f\"{name}: {raw.strip()!r} is not a number\")\n"
            "    return readings, sorted(problems)"
        ),
        explanation=(
            "Continuing after a failure is the whole point: a single corrupt channel must "
            "not discard the valid ones. partition limits the split to the first equals "
            "sign, so a value containing '=' survives, and sorting the problems makes "
            "the report stable for comparison."
        ),
        complexity="Time O(n) in the input length; space O(k) for k channels.",
        edge_cases="Empty input returns ({}, []) without raising.",
        alternative_approaches="Raising on the first error loses every other reading.",
        testing="readings, problems = parse_readings('a=1.5;b=bad;c=2')\nassert readings == {'a': 1.5, 'c': 2.0}\nassert problems == [\"b: 'bad' is not a number\"]\nassert parse_readings('') == ({}, [])",
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "FACTORS = {\n"
            "    'mm': 0.001,\n"
            "    'cm': 0.01,\n"
            "    'm': 1.0,\n"
            "    'km': 1000.0,\n"
            "    'in': 0.0254,\n"
            "    'ft': 0.3048,\n"
            "}\n"
            "\n"
            "\n"
            "def to_metres(value, unit: str) -> float:\n"
            "    if not isinstance(value, (int, float)) or isinstance(value, bool):\n"
            "        raise ValueError(f'not a number: {value!r}')\n"
            "    try:\n"
            "        factor = FACTORS[unit]\n"
            "    except KeyError:\n"
            "        raise ValueError(f'unknown unit: {unit!r}') from None\n"
            "    return float(value) * factor"
        ),
        explanation=(
            "A lookup table replaces a chain of conditionals with a single dictionary "
            "access, so adding a unit is a one-line change. The bool guard prevents True "
            "becoming 1.0 metres, and `from None` suppresses the KeyError traceback so "
            "the caller sees only the clear message."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="An empty string unit raises ValueError; 'm' returns the value unchanged as a float.",
        alternative_approaches="The pint library handles arbitrary units but is a heavy dependency here.",
        testing="assert to_metres(250, 'cm') == 2.5\nassert to_metres(1, 'in') == 0.0254\nassert to_metres(3, 'm') == 3.0",
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "from collections import Counter\n"
            "\n"
            "\n"
            "def summarise_types(values) -> dict:\n"
            "    counts = Counter(type(value).__name__ for value in values)\n"
            "    summary = {name: counts[name] for name in sorted(counts)}\n"
            "    summary['total'] = sum(counts.values())\n"
            "    return summary"
        ),
        explanation=(
            "Counter tallies the type names in a single pass and keeps bool and int "
            "distinct because their type names differ. Building the dict from sorted "
            "keys makes the output deterministic, which matters when it is compared in a "
            "test or serialised."
        ),
        complexity="Time O(n log k); space O(k) for k distinct types.",
        edge_cases="An empty sequence yields {'total': 0}.",
        alternative_approaches="A plain dict with incrementing counts avoids the import.",
        testing="assert summarise_types([1, 2.0, 'x']) == {'float': 1, 'int': 1, 'str': 1, 'total': 3}\nassert summarise_types([]) == {'total': 0}\nassert summarise_types([True, 1]) == {'bool': 1, 'int': 1, 'total': 2}",
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "import math\n"
            "\n"
            "\n"
            "def close_enough(a, b, tolerance: float = 1e-9) -> bool:\n"
            "    for value in (a, b):\n"
            "        if isinstance(value, bool) or not isinstance(value, (int, float)):\n"
            "            raise TypeError(f'not a real number: {value!r}')\n"
            "    return math.isclose(a, b, rel_tol=0.0, abs_tol=tolerance)"
        ),
        explanation=(
            "math.isclose with rel_tol set to zero makes the comparison purely absolute, "
            "so the tolerance means the same thing at 0.001 and at 10,000. Rejecting bool "
            "explicitly prevents True from comparing equal to 1."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="Exactly equal values return True regardless of the tolerance.",
        alternative_approaches="abs(a - b) <= tolerance is equivalent and needs no import.",
        testing="assert close_enough(0.1 + 0.2, 0.3) is True\nassert close_enough(1.0, 1.1) is False\nassert close_enough(1.0, 1.0000000001, 1e-9) is True",
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "def coerce(value, kinds):\n"
            "    attempts: list[str] = []\n"
            "    last: Exception | None = None\n"
            "    for kind in kinds:\n"
            "        attempts.append(getattr(kind, '__name__', repr(kind)))\n"
            "        try:\n"
            "            return kind(value)\n"
            "        except (TypeError, ValueError) as exc:\n"
            "            last = exc\n"
            "    raise ValueError(\n"
            "        f'could not convert {value!r} using: {\", \".join(attempts)}'\n"
            "    ) from last"
        ),
        explanation=(
            "Iterating in the caller's order is what makes the ladder configurable: int "
            "before float turns '48' into an int rather than 48.0. The final raise "
            "chains the last underlying exception with `from`, so the original failure is "
            "still visible in the traceback."
        ),
        complexity="Time O(k * n) for k attempted conversions; space O(k).",
        edge_cases="An empty kinds list raises ValueError naming no attempts.",
        alternative_approaches="A lookup of expected input types chooses one converter but cannot fall back.",
        testing="assert coerce('48.5', [int, float, str]) == 48.5\nassert coerce('48', [int, float]) == 48\nassert coerce('48', [int]) == 48",
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
            "RANGES = {'distance': (0.0, 30.0), 'temperature': (-40.0, 125.0)}\n"
            "\n"
            "\n"
            "def parse_readings(text):\n"
            "    \"\"\"Parse 'name=value' pairs into floats, reporting bad ones.\"\"\"\n"
            "    readings, problems = {}, []\n"
            "    for chunk in text.split(';'):\n"
            "        chunk = chunk.strip()\n"
            "        if not chunk:\n"
            "            continue\n"
            "        name, separator, raw = chunk.partition('=')\n"
            "        if not separator:\n"
            "            problems.append(f'{chunk!r}: missing =')\n"
            "            continue\n"
            "        name = name.strip()\n"
            "        try:\n"
            "            readings[name] = float(raw.strip())\n"
            "        except ValueError:\n"
            "            problems.append(f\"{name}: {raw.strip()!r} is not a number\")\n"
            "    return readings, sorted(problems)\n"
            "\n"
            "\n"
            "def wire_frame(robot, channels) -> str:\n"
            "    \"\"\"Render live readings as the semicolon text a real bus would send.\"\"\"\n"
            "    parts = []\n"
            "    for channel in channels:\n"
            "        try:\n"
            "            parts.append(f'{channel}={robot.read_sensor(channel)}')\n"
            "        except SensorError:\n"
            "            parts.append(f'{channel}=ERR')\n"
            "    return ';'.join(parts)\n"
            "\n"
            "\n"
            "def read_frame(robot, channels) -> dict:\n"
            "    \"\"\"Parse the wire frame back, validating each reading's range.\"\"\"\n"
            "    readings, problems = parse_readings(wire_frame(robot, channels))\n"
            "    good = {k: v for k, v in readings.items()\n"
            "            if k not in RANGES or RANGES[k][0] <= v <= RANGES[k][1]}\n"
            "    return {'readings': good, 'problems': problems, 'count': len(good)}"
        ),
        explanation=(
            "Rendering and then re-parsing exercises the conversion path that hardware "
            "would normally provide. The injected ERR value becomes a reported problem "
            "rather than a raised exception, and the range filter applies the physical "
            "limits that the simulator's own clamping would otherwise hide."
        ),
        complexity="Time O(c); space O(c).",
        edge_cases="A failed sensor appears in problems and is absent from readings.",
        alternative_approaches="Skipping the text round trip is faster but never tests the parser.",
        testing="robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\nframe = read_frame(robot, ['distance', 'temperature'])\nassert frame['count'] == 2\nassert frame['problems'] == []",
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="What does `type(0.1 + 0.2 == 0.3)` report?",
        choices=[
            "float",
            "bool",
            "int",
            "It raises a ValueError.",
        ],
        answer=1,
        kind="code_output",
        explanation=(
            "The comparison produces a boolean, and its value is False because binary "
            "floating point cannot represent 0.3 exactly. The type is bool regardless of "
            "the operands being floats."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="Why is `isinstance(True, int)` True in Python?",
        choices=[
            "Because True is stored as the integer 1.",
            "Because bool is declared a subclass of int.",
            "Because all values in Python are integers internally.",
            "Because isinstance performs numeric coercion.",
        ],
        answer=1,
        kind="conceptual",
        explanation=(
            "bool inherits from int in the type hierarchy, so isinstance accepts it. That "
            "is why a naive numeric validation must exclude bool explicitly."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="A telemetry value of 0.0 is skipped by `if value:`. What is the fix?",
        choices=[
            "Convert the value to a string before testing it.",
            "Cast every reading to bool on arrival.",
            "Compare explicitly, for example `if value is not None:` or `if value > 0:`.",
            "Reverse the test with `if not value is None:`.",
        ],
        answer=2,
        kind="debugging",
        explanation=(
            "0.0 is falsy, so truthiness conflates 'zero' with 'absent'. An explicit "
            "comparison states the actual condition and keeps a legitimate zero reading."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="What happens when you call `int('87.5')`?",
        choices=[
            "It returns 87.",
            "It returns 88.",
            "It returns 87.5.",
            "It raises a ValueError.",
        ],
        answer=3,
        kind="identify_error",
        explanation=(
            "int() parses a whole-number literal only. Given a decimal string it raises "
            "rather than truncating, which is why you convert with int(float(text)) when "
            "you genuinely mean truncation."
        ),
        reference="lesson.ipynb - Syntax",
    )
)

QUIZ.append(
    quiz(
        question="Why should a telemetry parser report a bad channel rather than raise?",
        choices=[
            "Raising is slower and harder to log.",
            "Python forbids exceptions inside loops.",
            "Reporting makes the code shorter.",
            "One corrupt channel would otherwise discard every valid reading.",
        ],
        answer=3,
        kind="reasoning",
        explanation=(
            "External data is unreliable by nature. Failing on the first bad value turns "
            "a single sensor glitch into a total outage of the telemetry pipeline; "
            "collecting problems keeps the good data usable and still surfaces the fault."
        ),
        reference="lesson.ipynb - Code Walkthrough",
    )
)

QUIZ.append(
    quiz(
        question="Which comparison is the correct way to test two floats for approximate equality?",
        choices=[
            "abs(a - b) < 1e-9",
            "a == b",
            "str(a) == str(b)",
            "a is b",
        ],
        answer=0,
        kind="multiple_choice",
        explanation=(
            "A tolerance comparison expresses the intent that the values differ by less "
            "than an acceptable amount. Exact equality fails for most decimal fractions, "
            "and is tests object identity, which floats never share."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="What does `int('42') + 1.0` evaluate to?",
        choices=[
            "43",
            "42.0",
            "43.0",
            "It raises a TypeError.",
        ],
        answer=2,
        kind="code_output",
        explanation=(
            "Mixing an int with a float promotes the int to a float rather than "
            "truncating, so the result is 43.0. This numeric-tower behaviour is why an "
            "int result can unexpectedly gain a decimal point."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="Why does the standard library provide decimal.Decimal?",
        choices=[
            "Because binary floating point cannot represent most decimal fractions exactly.",
            "Because Decimal arithmetic is faster than float.",
            "Because Decimal stores values as text on disk.",
            "Because Decimal removes the need for input validation.",
        ],
        answer=0,
        kind="reasoning",
        explanation=(
            "Decimal performs base-10 arithmetic, so 0.1 is stored as exactly one tenth. "
            "It is slower and only worth using where the decimal value is contractual, "
            "such as accounting or specified tolerances."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="Why validate ranges after parsing when the simulator already clamps readings?",
        choices=[
            "The simulator's clamping is known to be incorrect.",
            "Range checks make the parsing loop faster.",
            "Real sensors can emit out-of-range values that clamping would hide.",
            "Range checks are unnecessary once a value is a float.",
        ],
        answer=2,
        kind="robotics",
        explanation=(
            "The simulator clamps because it is a teaching model; a real sensor can "
            "report a physically impossible value, and a fault is far better detected "
            "than silently normalised. Testing the validation logic is the reason to keep "
            "it even though the simulator would never trigger it."
        ),
        reference="solution.ipynb - Solution 11",
    )
)

QUIZ.append(
    quiz(
        question="Which implementation correctly reads a numeric field and rejects booleans?",
        choices=[
            "Check isinstance(raw, bool) first, then float(raw) inside a try/except "
            "catching TypeError and ValueError.",
            "float(raw) on its own.",
            "int(raw) on its own.",
            "bool(raw) and then compare against 1.",
        ],
        answer=0,
        kind="implementation_choice",
        explanation=(
            "The explicit bool guard is required because bool is a subclass of int, so "
            "float(True) would otherwise silently succeed as 1.0. The try/except then "
            "handles the text that cannot be parsed at all."
        ),
        reference="exercises.ipynb - Exercise 2",
    )
)

MINI_PROJECT = {
    "title": "Mini-Project: Telemetry Frame Validator",
    "brief": (
        "Build a validator for the semicolon-separated text frames a robot receives "
        "over its serial bus. It must parse every channel, validate the physical range "
        "of each, and report every problem instead of raising."
    ),
    "scenario": (
        "The fleet controller receives one text frame per second from each robot. A "
        "corrupt field must not cost you the rest of the frame, and the operator needs "
        "to know exactly which channel was wrong."
    ),
    "rationale": (
        "This is the boundary component of every telemetry system: it is the one place "
        "where untrusted text becomes trusted numbers, and everything downstream depends "
        "on it being both forgiving and precise."
    ),
    "requirements": [
        "Parse 'channel=value' pairs split on ';' into floats.",
        "Validate each reading against a per-channel minimum and maximum.",
        "Return a dict with `readings`, `problems` and `count`.",
        "Never raise for malformed text.",
        "Reject booleans when validating numeric fields.",
    ],
    "constraints": [
        "Standard library only.",
        "Keep the channel ranges in a module-level table.",
        "Problems must name the channel they refer to.",
    ],
    "deliverables": [
        "`telemetry.py` with the parser and validator.",
        "`test_telemetry.py` with at least ten assertions.",
        "A README section listing every channel and its valid range.",
    ],
    "steps": [
        "Define RANGES for the channels you support.",
        "Implement parse_readings returning readings and problems.",
        "Add validate_readings applying RANGES and dropping failures.",
        "Compose them into validate_frame(text).",
        "Write tests for a clean frame, a bad value, an unknown channel and empty text.",
    ],
    "expected_behavior": (
        "A clean frame returns every reading with an empty problem list. A frame with a "
        "corrupt channel returns the good readings plus a message naming the bad one."
    ),
    "acceptance": [
        "All assertions pass from a clean run.",
        "Malformed text never raises.",
        "Every problem message names its channel.",
        "An empty frame returns count 0 with no problems.",
    ],
    "extensions": [
        "Add a timestamp to every frame and reject stale ones.",
        "Emit the result as JSON for the fleet dashboard.",
        "Track a rolling count of failures per channel.",
    ],
}

RESEARCH = {
    "question": (
        "How often do floating-point comparisons of the form a == b fail for values "
        "that should be equal?"
    ),
    "hypothesis": (
        "Decimal arithmetic, as used in currency, fails exact equality frequently, while "
        "tolerance-based comparison succeeds almost always."
    ),
    "experiment": [
        STEPS(
            [
                "Generate a few hundred pairs of values that are mathematically equal but computed differently.",
                "Compare each pair with == , with a 1e-9 tolerance, and with Decimal equality.",
                "Record every raw result in the table below before computing any rate.",
            ]
        ),
    ],
    "data": [
        CODE_CELL(
            "# Record your raw results - one row per comparison strategy.\n"
            "# Copy real values from your actual runs; do not invent them.\n"
            "#\n"
            "# | strategy | comparisons | exact matches | tolerance matches |"
        ),
    ],
    "analysis": [
        MD(
            "Compute the failure rate of each strategy and compare them. With a few "
            "hundred samples the difference is usually unambiguous; state the sample "
            "size alongside the rate so the reader can judge it."
        ),
    ],
    "result": [
        MD(
            "State which strategy failed, how often, and under what circumstances. Record "
            "any case that surprised you rather than discarding it."
        ),
    ],
    "interpretation": [
        MD(
            "Explain the mechanism in terms of binary versus decimal representation, and "
            "note that exact equality is still the correct test for values that were never "
            "rounded. Name at least two threats to the validity of the comparison."
        ),
    ],
    "conclusion": [
        MD(
            "Give your verdict and state the rule you would adopt for a production "
            "tolerance pipeline."
        ),
    ],
    "extensions": [
        "Repeat with values of very different magnitudes to expose relative tolerance issues.",
        "Measure the cost of Decimal against float on the same workload.",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Telemetry Frame Gate",
    "context": (
        "During drone pre-flight the controller receives semicolon-separated text "
        "frames from the sensor bus. Each frame must be converted to trusted numbers "
        "before any control decision is taken."
    ),
    "mission": (
        "Implement `validate_frame(text)` that parses a raw frame, validates every "
        "channel against its physical range, and returns a readiness decision naming "
        "each problem found."
    ),
    "requirements": [
        "Parse 'channel=value' pairs split on ';' into floats.",
        "Validate each reading against a per-channel range table.",
        "Reject booleans in the numeric path.",
        "Return a dict with `readings`, `problems` and `count`.",
    ],
    "constraints": [
        "Never raise for malformed text.",
        "No hardware required; use `shared/robo_x_sim` to produce a real frame.",
        "Complete well inside the 10 ms control budget.",
    ],
    "interface": "def validate_frame(text: str) -> dict:",
    "success_criteria": [
        "A clean frame returns count equal to the number of channels and no problems.",
        "A frame containing ERR reports that channel by name.",
        "Malformed text never raises.",
    ],
    "extension": (
        "Add a timestamp field to every frame and reject frames older than a supplied "
        "threshold, explaining the choice of threshold."
    ),
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Make external-text conversion the centrepiece of the topic.",
        "Install the conversion ladder as the default reflex for configuration.",
        "Show that bool being a subclass of int is a real, not theoretical, hazard.",
    ],
    "misconceptions": [
        [
            "Python converts types automatically when arithmetic needs them.",
            "Only int and float promote; everything else needs an explicit call.",
        ],
        [
            "0 is truthy because it is a number.",
            "Zero is falsy, which is why `if value:` skips a legitimate zero reading.",
        ],
        [
            "0.1 + 0.2 equals 0.3.",
            "Binary floating point cannot represent either value exactly.",
        ],
        [
            "A numeric check automatically rejects booleans.",
            "bool inherits from int, so True passes an int check unless excluded.",
        ],
    ],
    "difficult_concepts": [
        "Convincing students that partial success beats raising at a system boundary.",
        "Reasoning about representation error rather than treating it as a quirk.",
        "Seeing where the type boundary is in their own pipeline.",
    ],
    "demonstrations": [
        "Print 0.1 + 0.2 at full precision and then compare with 0.3.",
        "Show float(True) returning 1.0 while isinstance(True, int) is True.",
        "Parse a deliberately corrupt telemetry frame and show the good channels survive.",
    ],
    "discussion": [
        "Where in a real robot system would you place the conversion boundary?",
        "When is Decimal worth its cost, and when is a tolerance sufficient?",
    ],
    "student_errors": [
        [
            "A zero reading is ignored by a guard",
            "Truthiness was used where an explicit comparison was meant",
            "Test with `value is not None` or compare to a bound",
        ],
        [
            "ValueError raised on a text sensor field",
            "Conversion happened inside the control loop rather than at the boundary",
            "Parse once at the edge and pass typed values downstream",
        ],
        [
            "A boolean passes a numeric range check",
            "isinstance(value, int) also admits bool",
            "Exclude bool before the numeric check",
        ],
    ],
    "pacing": (
        "90 minutes of lesson, then 2 hours on exercises. Spend time on the conversion "
        "ladder; it recurs in Modules 4, 7, 8 and 9."
    ),
    "extensions": [
        "Ask students to write a validator for their own domain's units.",
        "Introduce the difference between float and Decimal for a billing use case.",
    ],
    "assessment": (
        "Grade against rubric.md. Exercises 6, 9 and 10 carry the signal: they require "
        "partial success, tolerance reasoning and ordered fallback."
    ),
    "support": (
        "Give students a table of values with their type, repr and bool result, and have "
        "them predict the missing column before running anything.",
    ),
    "extension_fast": (
        "Ask for a short design note on how the same validator would handle binary "
        "protobuf payloads instead of text.",
    ),
}

RUBRIC = {
    "artifacts": [
        ["exercises.ipynb", "40%", "All 10 exercises implemented and edge-cased."],
        ["mini_project.ipynb", "25%", "telemetry.py plus its test suite."],
        ["robotics_challenge.ipynb", "25%", "Frame gate reports every problem."],
        ["research.ipynb", "10%", "Real measurements with a defensible conclusion."],
    ],
    "criteria": [
        ["Correctness", "30", "Conversions, ranges and fallbacks all behave as specified."],
        ["Boundary discipline", "25", "Parsing happens once, at the edge, and never raises."],
        ["Code quality", "25", "PEP 8 naming, docstrings, small focused functions."],
        ["Reasoning", "20", "Float and Decimal trade-offs explained in writing."],
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
            "Every exercise implemented, a corrupt channel is reported by name while the "
            "rest survive, and the float comparison uses a justified tolerance.",
        ],
        [
            "Merit",
            "Most exercises correct; testing covers the main paths; malformed input is "
            "handled but the boolean edge case is untested.",
        ],
        [
            "Pass",
            "Core requirements met, but the parser raises on one bad channel, or floats "
            "are compared with ==.",
        ],
        [
            "Fail",
            "Conversion happens inside the control loop with no validation, or booleans "
            "silently pass as sensor readings.",
        ],
    ],
}

TOPIC = topic(
    topic_id="1.5",
    title="Core Data Types and Type Conversion",
    module=1,
    module_title="Getting Started with Python",
    directory="05_core_data_types_conversion",
    summary=(
        "Everything that enters a robot arrives as text. This topic covers the core "
        "built-in types, the traps of truthiness and floating point, and the "
        "conversion ladder that makes external data safe to use."
    ),
    why_it_matters=(
        "Type conversion is the seam where a robot meets the outside world: serial "
        "lines, HTTP parameters, configuration files and operator input all produce "
        "text. Get this boundary right and the rest of a system can trust its inputs; "
        "get it wrong and a single corrupt field silently becomes a wrong motor command."
    ),
    objectives=[
        "Name the core built-in types and say which are mutable.",
        "Convert external text safely with a conversion ladder.",
        "Explain why bool is a subclass of int and what it breaks.",
        "Avoid truthiness bugs on numeric values.",
        "Compare floats with a tolerance and know when Decimal is worth it.",
        "Parse a telemetry frame without losing the valid channels.",
    ],
    prerequisites=[
        "Topic 1.4 Variables, Naming Conventions, and Dynamic Typing",
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
