"""Topic 1.4 - Variables, Naming Conventions, and Dynamic Typing.

Hand-authored to the Course Content Standard. The spine: a name is a *label* bound
to an object, not a typed box, and everything surprising about Python variables
follows from that single idea.
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
        "In Python a variable is not a container that holds a value. It is a **name** "
        "bound to an **object**. The object carries its type and its data; the name is "
        "a label the interpreter can re-point at any time. Assignment is therefore a "
        "binding operation, not a copy. This one distinction explains why two names can "
        "refer to the same object, why rebinding a name to a different type is "
        "perfectly legal, and why mutating an object through one name is visible through "
        "another."
    ),
    CODE_CELL(
        "battery = 48.0\n"
        "print(type(battery).__name__, battery)\n"
        "\n"
        "# rebinding the same name to a different type is legal\n"
        "battery = 'unknown'\n"
        "print(type(battery).__name__, battery)\n"
        "\n"
        "# and back again\n"
        "battery = 12.0\n"
        "print(type(battery).__name__, battery)"
    ),
    MD(
        "Two names can point at one object. When that happens, mutating the object "
        "through either name is visible through the other, which is the classic source "
        "of a class of bugs where a function unexpectedly modifies its argument."
    ),
    CODE_CELL(
        "original = [1.0, 2.0, 3.0]\n"
        "alias = original\n"
        "alias.append(4.0)\n"
        "\n"
        "print('original:', original)   # also has 4.0\n"
        "print('same object?', original is alias)\n"
        "\n"
        "copy = original.copy()\n"
        "copy.append(5.0)\n"
        "print('after copy:', original)  # unchanged"
    ),
    NOTE(
        "is versus ==",
        "`is` asks whether two names point at the *same object*. `==` asks whether two "
        "objects *compare equal*. Small integers and short strings are interned, so "
        "`a is b` can be true for two separately written literals. In your own code, "
        "prefer `==` for values and reserve `is` for identity checks against None or "
        "sentinel objects.",
    ),
]

LESSON["formal_theory"] = [
    MD(
        "A Python program maintains two structures at runtime: an **object heap**, "
        "where each object stores its type and data, and a **namespace**, a mapping "
        "from names to objects. Assignment writes one entry into a namespace. `del` "
        "removes it. The object's lifetime is governed by how many names (or "
        "container slots) refer to it, not by the name itself."
    ),
    EQUATION(
        "namespace[name] -> object  (the object owns type + data)"
    ),
    STEPS(
        [
            "The expression on the right of `=` is evaluated first, producing a reference "
            "to an object.",
            "The name on the left is created or rebound to that object in its namespace.",
            "The object is freed only when no namespace entry and no container slot "
            "refers to it.",
        ]
    ),
    CODE_CELL(
        "def show(label, value):\n"
        "    print(f'{label:<12} id={id(value):<16} type={type(value).__name__}')\n"
        "\n"
        "\n"
        "a = 48.0\n"
        "b = a\n"
        "c = 48.0\n"
        "show('a', a)\n"
        "show('b', b)\n"
        "show('c', c)\n"
        "print('a is b:', a is b, '| a is c:', a is c, '| a == c:', a == c)"
    ),
    TABLE(
        ["Operation", "Effect on the namespace"],
        [
            ["`x = value`", "Create or rebind the name `x`"],
            ["`x += value`", "Read `x`, mutate or rebind, write `x` back"],
            ["`del x`", "Remove the name; the object may survive elsewhere"],
            ["`x: int = 5`", "Bind, plus record a type hint in `__annotations__`"],
        ],
    ),
]

LESSON["syntax"] = [
    MD(
        "PEP 8 defines four naming styles, and choosing the right one is most of the "
        "job of writing readable Python."
    ),
    CODE_CELL(
        "# snake_case for functions and variables\n"
        "max_speed_mps = 1.5\n"
        "\n"
        "\n"
        "def clamp_pct(value):\n"
        "    return max(0, min(100, value))\n"
        "\n"
        "\n"
        "# UPPER_CASE for module-level constants\n"
        "LOW_BATTERY_PCT = 20\n"
        "\n"
        "\n"
        "# CapWords for classes; _leading_underscore marks internals\n"
        "class TelemetryChannel:\n"
        "    _counter = 0\n"
        "\n"
        "    def __init__(self, name):\n"
        "        self.name = name"
    ),
    MD("The anti-pattern:"),
    CODE(
        "MaxSpeed = 1.5        # CapWords for a constant\n"
        "def getValue(x):    # camelCase for a function\n"
        "    return x\n"
        "X = 2                # one-letter module constant",
        lang="text",
    ),
    WARN(
        "Never shadow a built-in",
        "`list = [1, 2]` silently rebinds the built-in for the whole module scope. The "
        "error then appears far away as `TypeError: 'list' object is not callable`.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - several names bound in one statement.**"),
    CODE_CELL(
        "robot_id, battery_pct, status = 'rover-01', 48.0, 'ACTIVE'\n"
        "print(robot_id, battery_pct, status)\n"
        "\n"
        "# swapping without a temporary variable\n"
        "x, y = 1, 2\n"
        "x, y = y, x\n"
        "print('after swap:', x, y)"
    ),
    MD("**Example 2 - augmented assignment.**"),
    CODE_CELL(
        "distance_m = 0.0\n"
        "distance_m += 1.5\n"
        "distance_m *= 2\n"
        "print('distance:', distance_m)\n"
        "\n"
        "tags = ['front']\n"
        "tags += ['rear']      # extends in place; same object\n"
        "print('tags:', tags)"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "Unpacking turns a tuple of values into a set of named variables in one step, "
        "which is why it reads so well when the source is already structured - a "
        "coordinate pair, a status snapshot, a tuple returned by a function."
    ),
    CODE_CELL(
        "position = (12.0, 3.5)\n"
        "x, y = position\n"
        "print(f'x={x} y={y}')\n"
        "\n"
        "state = {'name': 'rover-01', 'battery_pct': 48.0, 'status': 'ACTIVE'}\n"
        "name, pct, status = state['name'], state['battery_pct'], state['status']\n"
        "print(f'{name} {pct}% {status}')\n"
        "\n"
        "# swapping is the clearest use of simultaneous assignment\n"
        "low, high = 10, 20\n"
        "low, high = high, low\n"
        "print('low:', low, 'high:', high)"
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "Because names live in dictionaries, a module's public surface can be inspected "
        "rather than remembered. This is how documentation tools and test frameworks "
        "discover what a module offers."
    ),
    CODE_CELL(
        "MAX_SPEED_MPS = 1.5\n"
        "\n"
        "\n"
        "def clamp_pct(value):\n"
        "    return max(0, min(100, value))\n"
        "\n"
        "\n"
        "public = sorted(\n"
        "    name for name in globals()\n"
        "    if not name.startswith('_') and name.isidentifier()\n"
        ")\n"
        "print('public names:', public)"
    ),
    MD(
        "Note that the private convention is *by agreement*, not enforcement: "
        "`_name` is still fully accessible. It signals intent to other engineers, "
        "which is a real but weaker guarantee than a compiler check."
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "Below is a small configuration loader. It is the first place where naming and "
        "binding discipline matter together: the loader converts values once, at the "
        "boundary, so that everything downstream can trust what it receives."
    ),
    CODE_CELL(
        "\"\"\"config_loader.py - turn raw settings into trusted values.\"\"\"\n"
        "from __future__ import annotations\n"
        "\n"
        "DEFAULTS = {\n"
        "    'robot_id': 'rover-01',\n"
        "    'max_speed_mps': 1.5,\n"
        "    'battery_wh': 48.0,\n"
        "}\n"
        "\n"
        "CASTS = {\n"
        "    'robot_id': str,\n"
        "    'max_speed_mps': float,\n"
        "    'battery_wh': float,\n"
        "}\n"
        "\n"
        "\n"
        "class ConfigError(ValueError):\n"
        "    \"\"\"Raised when a setting cannot be converted or is out of range.\"\"\"\n"
        "\n"
        "\n"
        "def load_config(raw: dict) -> dict:\n"
        "    \"\"\"Merge raw settings over the defaults and validate each value.\"\"\"\n"
        "    config = dict(DEFAULTS)\n"
        "    config.update(raw)\n"
        "    for key in list(config):\n"
        "        cast = CASTS.get(key)\n"
        "        if cast is None:\n"
        "            raise ConfigError(f'unknown setting: {key}')\n"
        "        try:\n"
        "            config[key] = cast(config[key])\n"
        "        except (TypeError, ValueError) as exc:\n"
        "            raise ConfigError(f'{key}: cannot convert {config[key]!r}') from exc\n"
        "    if not 0 < config['max_speed_mps'] <= 3.0:\n"
        "        raise ConfigError('max_speed_mps must be in (0, 3.0]')\n"
        "    return config"
    ),
    MD(
        "Two details matter. `config = dict(DEFAULTS)` copies, so the module-level "
        "default is never mutated by a caller. And the explicit `from exc` chain "
        "preserves the original conversion error, which is what makes a bad setting "
        "diagnosable instead of merely reported."
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "`DEFAULTS` holds the shipped settings; `dict(DEFAULTS)` inside the function "
            "copies them so a caller cannot corrupt the module state.",
            "`CASTS` records the target type per setting, which makes the conversion "
            "table explicit rather than buried in the code path.",
            "`ConfigError` subclasses ValueError so callers can catch either the "
            "specific error or the standard one.",
            "`config.update(raw)` applies overrides before validation, so validation "
            "always sees the final effective value.",
            "Iterating over `list(config)` allows the loop body to reassign keys safely.",
            "`raise ... from exc` keeps the underlying conversion error in the "
            "traceback, which is essential for diagnosing a bad settings file.",
            "The final range check on max_speed_mps enforces a policy that no type "
            "conversion can express.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - assuming assignment copies the object.**"),
    CODE(
        "a = [1.0, 2.0]\n"
        "b = a            # same object, not a copy\n"
        "b.append(3.0)\n"
        "print(a)         # [1.0, 2.0, 3.0]\n"
        "\n"
        "b = a.copy()     # explicit copy when independence is intended",
        lang="text",
    ),
    MD("**Mistake 2 - mutating a caller's argument in place.**"),
    CODE(
        "def extend_log(log, entry):\n"
        "    log.append(entry)      # caller sees the change\n"
        "\n"
        "def extend_log(log, entry):\n"
        "    return log + [entry]   # caller is unaffected",
        lang="text",
    ),
    MD("**Mistake 3 - shadowing a built-in.**"),
    CODE(
        "list = [1, 2, 3]\n"
        "more = list((4, 5))   # TypeError: 'list' object is not callable\n"
        "\n"
        "# the shadowing lasts for the whole enclosing scope",
        lang="text",
    ),
    MD("**Mistake 4 - reusing a single-letter name across an entire module.**"),
    CODE(
        "def area(w, h):\n"
        "    return w * h\n"
        "\n"
        "# at the call site: area(w, h) tells the reader nothing",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "When a value is not what you expected, three prints settle almost every case: "
        "its type, its representation, and its identity."
    ),
    CODE_CELL(
        "config = {'max_speed_mps': '1.5'}\n"
        "raw = config['max_speed_mps']\n"
        "\n"
        "print('type :', type(raw).__name__)\n"
        "print('repr :', repr(raw))\n"
        "print('id   :', id(raw))\n"
        "\n"
        "# a string that looks like a number is still a string\n"
        "try:\n"
        "    print(raw * 2)\n"
        "except TypeError as exc:\n"
        "    print('TypeError:', exc)"
    ),
    MD(
        "To find out who rebound a name, print the namespace rather than guessing: "
        "`globals()`, `locals()` and `vars(obj)` are ordinary dictionaries, so they "
        "support the full set of inspection tools."
    ),
    CODE_CELL(
        "def inspect_scope() -> dict:\n"
        "    local_var = 1\n"
        "    return {k: v for k, v in locals().items() if not k.startswith('_')}\n"
        "\n"
        "\n"
        "print(inspect_scope())"
    ),
    NOTE(
        "id() is not an identity you can rely on",
        "CPython reuses memory addresses after an object is freed, so two objects can "
        "share an id at different times. Use `is` for the question you care about, not "
        "`id(a) == id(b)`.",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "snake_case for functions and variables; CapWords for classes.",
            "UPPER_CASE for module-level constants that must not be rebound.",
            "A single leading underscore marks a name as internal by convention.",
            "Names should read as prose in context: `battery_pct`, not `b`.",
            "Never shadow a built-in; check the list before naming anything.",
            "Copy before mutating when the caller may still hold a reference.",
            "Convert types once at the boundary, not at every use site.",
            "Return a value rather than relying on a side effect the caller cannot see.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "Binding a name is cheap: it is a dictionary write. What is *not* cheap is the "
        "repeated attribute lookup inside a hot loop, because each `obj.attr` is a "
        "second dictionary lookup after the name is resolved. Hoisting a value out of a "
        "loop is a legitimate micro-optimisation, but only when measurement shows the "
        "loop is hot enough to care."
    ),
    MD(
        "The optimisation that reliably matters in this topic is avoiding accidental "
        "copies. Rebinding a name to an immutable object costs nothing, but "
        "`config = dict(DEFAULTS)` inside a function called ten thousand times creates "
        "ten thousand dictionaries. When a default must not be mutated across calls, use "
        "`collections.defaultdict` or `functools.cached_property`, or make the copy once "
        "at module scope and treat it as immutable by convention."
    ),
    TIP(
        "Measure the loop, not the line",
        "Use time.perf_counter around a realistic workload. A micro-optimisation that "
        "shaves 2% from a loop executed once per mission is not worth the readability "
        "cost it buys.",
    ),
]

LESSON["pythonic_approaches"] = [
    MD("Swapping and copying, the idiomatic way and the way that bites."),
    CODE_CELL(
        "# swapping: temporary variable versus simultaneous assignment\n"
        "a, b = 'front', 'rear'\n"
        "a, b = b, a\n"
        "\n"
        "# copying a list: slice versus copy versus list()\n"
        "readings = [0.1, 0.2]\n"
        "shallow = readings[:]\n"
        "explicit = readings.copy()\n"
        "via_ctor = list(readings)\n"
        "print(shallow, explicit, via_ctor)\n"
        "\n"
        "# building a string from pieces\n"
        "parts = ['rover-01', 'ready']\n"
        "print('-'.join(parts))\n"
        "print(''.join(['batt', 'ery']))"
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "Robot state flows between names constantly: a sensor read is bound to a name, "
        "passed to a function, and compared against a threshold. Because binding does "
        "not copy, a function that mutates a list argument changes the caller's data - "
        "which is why the telemetry pipeline in the course always copies at the "
        "boundary."
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
        "snapshot = robot.status()\n"
        "\n"
        "# two names, one object - mutating the snapshot changes what we hold\n"
        "alias = snapshot\n"
        "print('same object?', alias is snapshot)\n"
        "snapshot['note'] = 'captured at boot'\n"
        "print('visible via alias:', alias.get('note'))"
    ),
]

LESSON["engineering_example"] = [
    MD(
        "A small helper that records every name a function bound, which is the "
        "practical form of 'what changed in here?'"
    ),
    CODE_CELL(
        "def bound_names(func) -> set[str]:\n"
        "    \"\"\"Return the local names a function binds, via its code object.\"\"\"\n"
        "    import dis\n"
        "    names = set()\n"
        "    for instruction in dis.get_instructions(func):\n"
        "        if instruction.opname in {'STORE_NAME', 'STORE_FAST'}:\n"
        "            names.add(instruction.argval)\n"
        "    return names\n"
        "\n"
        "\n"
        "def sample():\n"
        "    battery_pct = 48.0\n"
        "    status = 'READY'\n"
        "    return battery_pct, status\n"
        "\n"
        "\n"
        "print(sorted(bound_names(sample)))"
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Bind `robot_id` to a string and `battery_pct` to a float; print type, repr "
            "and id for both.",
            "Create two names for the same list, append through one, and print both to "
            "show the change is shared.",
            "Create a genuine copy and repeat the append to show independence.",
            "Rebind `battery_pct` to the string 'unknown' and explain why nothing "
            "complains until it is used in arithmetic.",
        ]
    ),
    CODE_CELL(
        "# Your turn.\n"
        "robot_id = 'rover-01'\n"
        "battery_pct = 48.0\n"
        "print(type(robot_id).__name__, repr(robot_id))\n"
        "print(type(battery_pct).__name__, repr(battery_pct))\n"
        "\n"
        "shared = [0.1]\n"
        "also_shared = shared\n"
        "also_shared.append(0.2)\n"
        "print('shared:', shared)\n"
        "\n"
        "independent = shared.copy()\n"
        "independent.append(0.3)\n"
        "print('shared after copy:', shared)"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: sticky notes on objects.** The object is the thing with the "
        "data. A name is a sticky note you attach to it. You can move a sticky note to "
        "another object at any time, and you can attach several notes to the same "
        "object. Nothing is ever put *into* the name."
    ),
    TABLE(
        ["Operation", "What a beginner imagines", "What actually happens"],
        [
            ["`b = 48.0`", "A box of type float is created for b", "b now labels one float object"],
            ["`b = 'x'`", "The box changes type", "b is re-pointed at a str object"],
            ["`a = b`", "A second box is filled", "a and b label the same object"],
            ["`a.append(...)`", "Only a changes", "the shared object changes"],
        ],
    ),
]

TERMS = [
    ["Variable", "A name bound to an object; not a typed container."],
    ["Object", "The thing that holds data and carries a type."],
    ["Binding", "Attaching a name to an object, or re-pointing it elsewhere."],
    ["Namespace", "The mapping from names to objects, such as globals or locals."],
    ["Rebinding", "Pointing an existing name at a different object."],
    ["Alias", "A second name referring to the same object as a first."],
    ["Mutability", "Whether an object's contents can be changed in place."],
    ["PEP 8 naming", "snake_case for functions, CapWords for classes, UPPER_CASE for constants."],
    ["is operator", "Identity comparison: do two names refer to one object?"],
    ["id()", "The memory address of an object; not a durable identity."],
]

LESSON["summary"] = [
    MD(
        "A Python variable is a name bound to an object. Assignment binds or rebinds; it "
        "never copies. Because of that, two names can refer to one object, mutating "
        "through one name is visible through the other, and rebinding a name to a value "
        "of a different type is completely legal. Dynamic typing is the direct "
        "consequence: the type lives on the object and is checked when an operation is "
        "attempted, not when the name is created."
    ),
    MD(
        "The discipline that keeps this safe is boring and effective. Name things so a "
        "reader understands them from context alone. Never shadow a built-in. Copy "
        "before mutating when the caller may still hold a reference. Convert types once "
        "at the boundary where data enters your program, and then trust them "
        "downstream. And when a value is not what you expected, print its type, its "
        "representation and its identity before changing any code - nine times in ten "
        "the answer is there."
    ),
    MD(
        "For robotics specifically, this topic is where a control loop stops being "
        "fragile. A sensor read bound to a name, copied at the boundary and compared "
        "against a threshold is a pattern that scales to a fleet; the same value "
        "passed around by reference and mutated in place is how a battery percentage "
        "ends up wrong on one robot and not another."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "A name is a label bound to an object, never a typed box.",
            "Assignment binds or rebinds; it does not copy.",
            "Two names can share one object, so mutation is shared.",
            "Types belong to objects and are checked when an operation runs.",
            "snake_case for functions, CapWords for classes, UPPER_CASE for constants.",
            "Never shadow built-ins; the failure surfaces far from its cause.",
            "Copy explicitly when the caller must keep its own data.",
            "Diagnose with type(), repr() and `is` before editing code.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "[PEP 8 - Style Guide](https://peps.python.org/pep-0008/) - the naming "
            "conventions used throughout this course.",
            "[Naming and binding in Python](https://realpython.com/python-names-and-scoping/)",
            "[dataclasses - immutable-ish records](https://docs.python.org/3/library/dataclasses.html)",
            "[copy - shallow and deep copying](https://docs.python.org/3/library/copy.html)",
            "[dis - inspecting bytecode and bound names](https://docs.python.org/3/library/dis.html)",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Validate a snake_case name",
        difficulty="MEDIUM",
        learning_objectives=["Apply naming rules.", "Report why a name is invalid."],
        concepts_tested=["strings", "naming", "validation"],
        problem_statement=(
            "Write `safe_name(name)` returning True when `name` is a valid snake_case "
            "identifier: lowercase, digits and underscores only, not starting with a "
            "digit, and not empty."
        ),
        requirements=["Use str.isidentifier() plus a case check.", "Return a boolean."],
        constraints=["Do not use a regular expression."],
        input_description="A candidate name string.",
        expected_output="True or False.",
        example_input="safe_name('battery_pct_2')",
        example_output="True",
        edge_cases=["Empty string is False.", "'_private' starts with an underscore and is acceptable.", "'2fast' is False because it starts with a digit."],
        hints=["isidentifier() handles the character rules; check name.islower() or all(c.islower() ...) for the rest."],
        success_criteria=["True for battery_pct_2.", "False for BatteryPct."],
        optional_extension="Also reject Python keywords by consulting keyword.kwlist.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Describe a binding",
        difficulty="MEDIUM",
        learning_objectives=["Inspect an object.", "Return structured data."],
        concepts_tested=["type()", "repr()", "id()"],
        problem_statement=(
            "Write `describe_binding(value)` returning a dict with keys `type` (the "
            "type's name), `repr` (its representation) and `length` (len(value) when "
            "the object supports it, otherwise None)."
        ),
        requirements=["Never raise for an object without a length.", "Type must be a string."],
        constraints=["Do not special-case specific types."],
        input_description="Any Python object.",
        expected_output="A dict with three keys.",
        example_input="describe_binding(48.0)",
        example_output="{'type': 'float', 'repr': '48.0', 'length': None}",
        edge_cases=["An int has no len, so length is None.", "A list reports its length.", "A string reports its length."],
        hints=["try/except TypeError around len() is the portable approach."],
        success_criteria=["Reports 'float' for 48.0.", "length is None for an int."],
        optional_extension="Add an 'identity' field from id(value).",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Swap two values with unpacking",
        difficulty="MEDIUM",
        learning_objectives=["Use simultaneous assignment.", "Return a swapped pair."],
        concepts_tested=["tuples", "unpacking", "assignment"],
        problem_statement=(
            "Write `swap(a, b)` returning `(b, a)` using simultaneous assignment "
            "rather than a temporary variable."
        ),
        requirements=["Do not use a third name.", "Return a tuple."],
        constraints=["The implementation must be a single return statement."],
        input_description="Any two values.",
        expected_output="A tuple with the values reversed.",
        example_input="swap('front', 'rear')",
        example_output="('rear', 'front')",
        edge_cases=["Equal values still return a two-tuple.", "Works for any types, not just strings."],
        hints=["a, b = b, a inside the tuple literal does the work."],
        success_criteria=["Returns ('rear', 'front') for the example.", "Works for mixed types."],
        optional_extension="Write an in-place version for two-element lists.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Parse an assignment line",
        difficulty="MEDIUM",
        learning_objectives=["Split structured text.", "Validate the target name."],
        concepts_tested=["strings", "split", "validation"],
        problem_statement=(
            "Write `parse_assignment(line)` returning `(name, raw_value)` for a line "
            "such as `'battery_pct = 48.0'`. Strip whitespace. Raise ValueError when "
            "there is no '=' or the name is not a valid identifier."
        ),
        requirements=["Split on '=' at most once.", "Strip both halves."],
        constraints=["Preserve the value exactly as written, minus surrounding spaces."],
        input_description="A single line of source text.",
        expected_output="A tuple of name and raw value strings.",
        example_input="parse_assignment('battery_pct = 48.0')",
        example_output="('battery_pct', '48.0')",
        edge_cases=["A value containing '=' is preserved after the first one.", "A line with no '=' raises ValueError.", "Empty name raises ValueError."],
        hints=["str.partition('=') splits on the first separator only."],
        success_criteria=["Parses the example exactly.", "Raises ValueError for 'battery_pct'."],
        optional_extension="Return None for blank lines instead of raising.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Convert a label to snake_case",
        difficulty="MEDIUM",
        learning_objectives=["Transform text.", "Insert separators."],
        concepts_tested=["strings", "case conversion", "loops"],
        problem_statement=(
            "Write `to_snake(text)` converting 'MaxSpeedMPS' or 'max speed mps' into "
            "'max_speed_mps'. Handle runs of separators and digits."
        ),
        requirements=["Lower-case the result.", "Collapse repeated underscores."],
        constraints=["No regular expressions.", "Must not leave a leading or trailing underscore."],
        input_description="A label in CamelCase, with spaces, or with underscores.",
        expected_output="A snake_case string.",
        example_input="to_snake('MaxSpeedMPS')",
        example_output="'max_speed_mps'",
        edge_cases=["Already-snake input is unchanged.", "Consecutive spaces collapse to one underscore.", "Empty input returns an empty string."],
        hints=["Insert a separator before an upper-case letter that follows a lower-case letter or a digit."],
        success_criteria=["Converts MaxSpeedMPS correctly.", "Is idempotent on snake_case input."],
        optional_extension="Add to_camel_case as the inverse operation.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Find duplicate names with their positions",
        difficulty="HARD",
        learning_objectives=["Aggregate occurrences.", "Preserve order."],
        concepts_tested=["dicts", "sets", "enumeration"],
        problem_statement=(
            "Write `find_duplicates(names)` returning a dict mapping each name that "
            "appears more than once to the sorted list of its 1-based positions."
        ),
        requirements=["Names appearing once are omitted.", "Positions are sorted."],
        constraints=["Do not mutate the input."],
        input_description="A sequence of names.",
        expected_output="A dict of duplicates to position lists.",
        example_input="find_duplicates(['a', 'b', 'a', 'c', 'a'])",
        example_output="{'a': [1, 3, 5]}",
        edge_cases=["Empty input gives {}.", "Every name unique gives {}.", "All identical gives one key with all positions."],
        hints=["Collect positions per name, then filter to those with more than one."],
        success_criteria=["Matches the example exactly.", "Omits unique names."],
        optional_extension="Also report names that shadow a Python built-in.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Make an independent copy of a sequence",
        difficulty="HARD",
        learning_objectives=["Copy deliberately.", "Explain shallow semantics."],
        concepts_tested=["copying", "lists", "mutability"],
        problem_statement=(
            "Write `clone(sequence)` returning a shallow copy that is independent for "
            "top-level mutation. Nested mutable objects are shared, and the docstring "
            "must say so."
        ),
        requirements=["Never mutate the argument.", "Return a new list."],
        constraints=["Shallow copy only; document the limitation."],
        input_description="Any sequence such as a list.",
        expected_output="A new list that can be mutated safely.",
        example_input="clone([1, 2, 3])",
        example_output="[1, 2, 3]",
        edge_cases=["Empty input gives a new empty list, not the same object.", "Nested lists are shared, not copied.", "Tuples return a list."],
        hints=["list(sequence) always produces a fresh list."],
        success_criteria=["Appending to the copy leaves the original unchanged.", "Nested elements are shared."],
        optional_extension="Add deep_clone using copy.deepcopy and compare the results.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="List the public names in a namespace",
        difficulty="HARD",
        learning_objectives=["Inspect a namespace.", "Apply a visibility convention."],
        concepts_tested=["globals", "dicts", "filtering"],
        problem_statement=(
            "Write `public_names(namespace)` returning a sorted list of names that do "
            "not start with an underscore, are identifiers, and are not modules."
        ),
        requirements=["Do not mutate the namespace.", "Sort the result."],
        constraints=["Do not inspect names for being modules."],
        input_description="A namespace dictionary such as globals().",
        expected_output="A sorted list of public names.",
        example_input="public_names({'_hidden': 1, 'robot_id': 'r1', 'MAX_SPEED': 1.5})",
        example_output="['MAX_SPEED', 'robot_id']",
        edge_cases=["An empty namespace gives [].", "Module objects are excluded.", "Names that are not identifiers are excluded."],
        hints=["Filter with a set comprehension, then sort."],
        success_criteria=["Excludes _hidden.", "Returns a sorted list."],
        optional_extension="Add a 'public_doc' mapping of name to its docstring.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Build a validated configuration",
        difficulty="HARD",
        learning_objectives=["Merge defaults.", "Cast and validate."],
        concepts_tested=["dicts", "validation", "error reporting"],
        problem_statement=(
            "Write `build_config(raw, defaults, casts)` returning `(config, errors)`. "
            "Merge `raw` over `defaults`, cast each known key with its callable, and "
            "collect a message per failure rather than raising. Unknown keys are an "
            "error."
        ),
        requirements=["Never mutate defaults or raw.", "One message per problem key."],
        constraints=["Keep processing after the first failure."],
        input_description="A raw dict, a defaults dict and a dict of callables.",
        expected_output="A tuple of config dict and sorted error messages.",
        example_input="build_config({'robot_id': 'r2'}, {'robot_id': 'r1', 'battery_wh': 48.0}, {'robot_id': str, 'battery_wh': float})",
        example_output="({'robot_id': 'r2', 'battery_wh': 48.0}, [])",
        edge_cases=["An uncastable value adds an error and keeps the default.", "An unknown key adds an error.", "Empty raw input yields the defaults."],
        hints=["Copy defaults first, then loop over keys collecting messages."],
        success_criteria=["Matches the example.", "Does not mutate its arguments."],
        optional_extension="Add a range check per key and report out-of-range values.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Apply symbol renames without collisions",
        difficulty="HARD",
        learning_objectives=["Order-dependent transformation.", "Reason about collisions."],
        concepts_tested=["dicts", "ordering", "strings"],
        problem_statement=(
            "Write `rename_symbol(mapping, text)` replacing whole-word occurrences of "
            "each key with its value. Apply the **longest** key first so that renaming "
            "`b` does not corrupt `battery`."
        ),
        requirements=["Match whole words only, not substrings.", "Longest key first."],
        constraints=["Pure text transform; do not use ast."],
        input_description="A rename mapping and a block of text.",
        expected_output="The transformed text.",
        example_input="rename_symbol({'b': 'battery', 'battery': 'level'}, 'b and battery')",
        example_output="'battery and level'",
        edge_cases=["A key that is a substring of another must not corrupt it.", "Text with no matches is returned unchanged.", "Punctuation around words is preserved."],
        hints=["Sort keys by length descending, then replace with word boundaries."],
        success_criteria=["Produces the example output exactly.", "Handles keys that are substrings of each other."],
        optional_extension="Detect a mapping cycle such as {'a': 'b', 'b': 'a'} and report it.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "import keyword\n"
            "\n"
            "\n"
            "def safe_name(name: str) -> bool:\n"
            "    if not isinstance(name, str) or not name:\n"
            "        return False\n"
            "    if keyword.iskeyword(name):\n"
            "        return False\n"
            "    if not name.isidentifier():\n"
            "        return False\n"
            "    return name == name.lower()"
        ),
        explanation=(
            "isidentifier() enforces the character rules and rejects a leading digit, "
            "while the lower-case comparison rejects CapWords and mixed case. "
            "Rejecting keywords is a bonus check: a name that is a legal identifier can "
            "still be unusable as a variable."
        ),
        complexity="Time O(n) in the name length; space O(1).",
        edge_cases="'_private' passes because it is a legal identifier that is already lower case.",
        alternative_approaches="A regular expression expresses the same rule in one line.",
        testing="assert safe_name('battery_pct_2') is True\nassert safe_name('BatteryPct') is False\nassert safe_name('2fast') is False\nassert safe_name('class') is False",
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def describe_binding(value) -> dict:\n"
            "    try:\n"
            "        length = len(value)\n"
            "    except TypeError:\n"
            "        length = None\n"
            "    return {\n"
            "        'type': type(value).__name__,\n"
            "        'repr': repr(value),\n"
            "        'length': length,\n"
            "    }"
        ),
        explanation=(
            "Catching TypeError from len() is the portable way to ask 'does this object "
            "have a length' without enumerating the types that do. The type name comes "
            "from the class rather than a hard-coded mapping, so new types are handled "
            "automatically."
        ),
        complexity="Time O(n) for repr on a large object; space O(n).",
        edge_cases="An object whose __len__ raises ValueError would propagate; that is deliberate.",
        alternative_approaches="A match statement on type(value) is explicit but needs a branch per type.",
        testing="d = describe_binding(48.0)\nassert d['type'] == 'float'\nassert d['length'] is None\nassert describe_binding([1, 2])['length'] == 2",
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code="def swap(a, b):\n    return (b, a)",
        explanation=(
            "The parentheses turn the two simultaneous assignments into a tuple that "
            "can be returned. Both right-hand sides are evaluated before either name is "
            "rebound, which is what makes the swap correct without a temporary."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="Equal values return a two-tuple unchanged, as expected.",
        alternative_approaches="temp = a; a = b; b = temp works but is three lines and needs a third name.",
        testing="assert swap('front', 'rear') == ('rear', 'front')\nassert swap(1, 1) == (1, 1)\nassert swap(1, 'x') == ('x', 1)",
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "def parse_assignment(line: str) -> tuple[str, str]:\n"
            "    if not isinstance(line, str) or not line.strip():\n"
            "        raise ValueError('empty assignment line')\n"
            "    name, separator, value = line.partition('=')\n"
            "    if not separator:\n"
            "        raise ValueError(f'no assignment in {line!r}')\n"
            "    name, value = name.strip(), value.strip()\n"
            "    if not name.isidentifier():\n"
            "        raise ValueError(f'invalid name: {name!r}')\n"
            "    return name, value"
        ),
        explanation=(
            "partition splits on the first '=' only, so a value that itself contains an "
            "equals sign survives intact. Stripping both halves removes the whitespace "
            "around the operator, and validating the name before returning stops a "
            "malformed target from reaching the caller."
        ),
        complexity="Time O(n) in the line length; space O(n).",
        edge_cases="A line with no '=' raises ValueError; an empty name raises ValueError.",
        alternative_approaches="str.split('=', 1) is equivalent but discards the separator flag.",
        testing="assert parse_assignment('battery_pct = 48.0') == ('battery_pct', '48.0')\nassert parse_assignment('a = 1 = 2') == ('a', '1 = 2')",
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "def to_snake(text: str) -> str:\n"
            "    chars = [c if c.isalnum() else ' ' for c in text]\n"
            "    out: list[str] = []\n"
            "    for index, ch in enumerate(chars):\n"
            "        if ch == ' ':\n"
            "            out.append('_')\n"
            "            continue\n"
            "        if ch.isupper():\n"
            "            prev = chars[index - 1] if index else ''\n"
            "            nxt = chars[index + 1] if index + 1 < len(chars) else ''\n"
            "            boundary = prev.islower() or prev.isdigit()\n"
            "            acronym = prev.isupper() and nxt.islower()\n"
            "            if prev and prev != ' ' and (boundary or acronym):\n"
            "                out.append('_')\n"
            "        out.append(ch.lower())\n"
            "    parts = [p for p in ''.join(out).split('_') if p]\n"
            "    return '_'.join(parts)"
        ),
        explanation=(
            "Non-alphanumeric characters become spaces first, so separators are handled "
            "uniformly. A separator is inserted before an upper-case letter when the "
            "previous character is lower-case or a digit, or when we are leaving an "
            "acronym - that second rule is what turns 'SpeedMPS' into 'speed_mps' "
            "instead of 'speedmps'. Filtering empty parts collapses repeated separators."
        ),
        complexity="Time O(n) in the text length; space O(n).",
        edge_cases="Empty input returns an empty string; already-snake input is unchanged.",
        alternative_approaches="Two regular-expression passes are shorter but less explicit about the acronym rule.",
        testing="assert to_snake('MaxSpeedMPS') == 'max_speed_mps'\nassert to_snake('max speed mps') == 'max_speed_mps'\nassert to_snake('battery_pct') == 'battery_pct'",
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "def find_duplicates(names) -> dict:\n"
            "    positions: dict = {}\n"
            "    for index, name in enumerate(names, start=1):\n"
            "        positions.setdefault(name, []).append(index)\n"
            "    return {n: sorted(p) for n, p in positions.items() if len(p) > 1}"
        ),
        explanation=(
            "setdefault creates the empty list on first sight and appends thereafter, so "
            "one pass collects every position. Filtering to lists longer than one keeps "
            "unique names out of the result, and sorting makes the output stable."
        ),
        complexity="Time O(n log n) in the worst case from sorting; space O(n).",
        edge_cases="An empty input returns an empty dict; all-identical input yields one key with every position.",
        alternative_approaches="collections.Counter plus a second pass is shorter and slower.",
        testing="assert find_duplicates(['a', 'b', 'a', 'c', 'a']) == {'a': [1, 3, 5]}\nassert find_duplicates([]) == {}\nassert find_duplicates(['a', 'b']) == {}",
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "def clone(sequence):\n"
            "    \"\"\"Return a shallow copy that is safe to mutate at the top level.\n"
            "\n"
            "    Nested mutable objects are shared with the original; use\n"
            "    copy.deepcopy when independent nested state is required.\n"
            "    \"\"\"\n"
            "    return list(sequence)"
        ),
        explanation=(
            "list() always allocates a new container, so appending or removing at the "
            "top level cannot affect the caller's data. The docstring is explicit that "
            "this is shallow, which is the detail most often missed when a nested list "
            "appears to mutate unexpectedly."
        ),
        complexity="Time O(n); space O(n).",
        edge_cases="An empty input produces a new list rather than the same object.",
        alternative_approaches="sequence[:] and sequence.copy() are equivalent for list inputs.",
        testing="src = [1, 2]\ncopy = clone(src)\ncopy.append(3)\nassert src == [1, 2]\nassert copy == [1, 2, 3]",
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "import types\n"
            "\n"
            "\n"
            "def public_names(namespace: dict) -> list[str]:\n"
            "    return sorted(\n"
            "        name\n"
            "        for name, value in namespace.items()\n"
            "        if not name.startswith('_')\n"
            "        and name.isidentifier()\n"
            "        and not isinstance(value, types.ModuleType)\n"
            "    )"
        ),
        explanation=(
            "The filter expresses the three independent exclusions: private by "
            "convention, not a valid identifier, and not an imported module. Sorting "
            "gives a deterministic result, which matters when the list is compared "
            "against an expected value in a test."
        ),
        complexity="Time O(n log n); space O(n).",
        edge_cases="An empty namespace returns an empty list without raising.",
        alternative_approaches="vars(module) is often a more convenient input than globals().",
        testing="assert public_names({'_hidden': 1, 'robot_id': 'r1', 'MAX_SPEED': 1.5}) == ['MAX_SPEED', 'robot_id']\nassert public_names({}) == []",
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "def build_config(raw: dict, defaults: dict, casts: dict) -> tuple[dict, list[str]]:\n"
            "    config = dict(defaults)\n"
            "    config.update(raw)\n"
            "    errors: list[str] = []\n"
            "    for key in sorted(config):\n"
            "        cast = casts.get(key)\n"
            "        if cast is None:\n"
            "            errors.append(f'unknown setting: {key}')\n"
            "            continue\n"
            "        try:\n"
            "            config[key] = cast(config[key])\n"
            "        except (TypeError, ValueError):\n"
            "            config[key] = defaults.get(key)\n"
            "            errors.append(f'cannot convert {key}')\n"
            "    return config, sorted(errors)"
        ),
        explanation=(
            "Copying the defaults first means neither argument is mutated, and update() "
            "applies overrides before any validation so every check sees the final "
            "value. On a failed cast the default is restored and a message is appended, "
            "which keeps the function total: it reports every problem rather than "
            "stopping at the first."
        ),
        complexity="Time O(k log k) for k keys; space O(k).",
        edge_cases="An unknown key adds an error and leaves the value untouched.",
        alternative_approaches="A dataclass with __post_init__ validation enforces this at construction time.",
        testing="cfg, errs = build_config({'robot_id': 'r2'}, {'robot_id': 'r1', 'battery_wh': 48.0}, {'robot_id': str, 'battery_wh': float})\nassert cfg == {'robot_id': 'r2', 'battery_wh': 48.0}\nassert errs == []",
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "import re\n"
            "\n"
            "\n"
            "def rename_symbol(mapping: dict, text: str) -> str:\n"
            "    out = text\n"
            "    for old in sorted(mapping, key=len, reverse=True):\n"
            "        pattern = rf'\\b{re.escape(old)}\\b'\n"
            "        out = re.sub(pattern, mapping[old], out)\n"
            "    return out"
        ),
        explanation=(
            "Sorting keys by descending length is the whole trick: replacing the longer "
            "name first stops a short alias from corrupting it. Word boundaries ensure "
            "only whole identifiers are touched, and re.escape protects names that "
            "contain regex metacharacters."
        ),
        complexity="Time O(k * n) for k keys over n characters; space O(n).",
        edge_cases="Text with no matches is returned unchanged; punctuation around words is preserved.",
        alternative_approaches="An ast-based rename is safer for real refactoring but cannot rewrite comments or strings.",
        testing="assert rename_symbol({'b': 'battery', 'battery': 'level'}, 'b and battery') == 'battery and level'\nassert rename_symbol({'x': 'y'}, 'no match') == 'no match'",
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
            "DEFAULTS = {'battery_wh': 48.0, 'name': 'rover-01'}\n"
            "CASTS = {'battery_wh': float, 'name': str}\n"
            "\n"
            "\n"
            "def telemetry_config(robot) -> dict:\n"
            "    \"\"\"Merge the robot's own state over the shipped defaults.\"\"\"\n"
            "    state = robot.status()\n"
            "    raw = {'battery_wh': state['battery_wh'], 'name': state['name']}\n"
            "    config = dict(DEFAULTS)\n"
            "    config.update(raw)\n"
            "    return {key: CASTS[key](value) for key, value in config.items()}\n"
            "\n"
            "\n"
            "def safe_readings(robot, channels) -> dict:\n"
            "    readings = {}\n"
            "    for channel in channels:\n"
            "        try:\n"
            "            readings[channel] = robot.read_sensor(channel)\n"
            "        except SensorError:\n"
            "            readings[channel] = None\n"
            "    return readings"
        ),
        explanation=(
            "dict(DEFAULTS) protects the shipped defaults from being overwritten, and the "
            "comprehension applies every declared cast in one place so the values leaving "
            "this function are already the right type. safe_readings isolates each channel "
            "so a single faulty sensor degrades one entry rather than the whole report."
        ),
        complexity="Time O(k + c) for k settings and c channels; space O(k + c).",
        edge_cases="An unknown channel records None rather than raising.",
        alternative_approaches="Reuse build_config from exercise 9 instead of re-implementing the merge.",
        testing="robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\ncfg = telemetry_config(robot)\nassert cfg['name'] == 'rover-01'\nassert isinstance(cfg['battery_wh'], float)\nassert safe_readings(robot, ['nope'])['nope'] is None",
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="After `b = a` where `a` is a list, what is true?",
        choices=[
            "b is an independent copy of a.",
            "a and b name the same list object.",
            "b is a tuple converted from a.",
            "a is discarded and replaced by b.",
        ],
        answer=1,
        kind="conceptual",
        explanation=(
            "Assignment binds a second name to the object already referenced; it never "
            "copies. Both names therefore reach the same object, so a mutation through "
            "either is visible through the other."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="What does this print?\n\nbattery = 48.0\nbattery = 'unknown'\nprint(type(battery).__name__)",
        choices=[
            "str",
            "float",
            "It raises a TypeError.",
            "NoneType",
        ],
        answer=0,
        kind="code_output",
        explanation=(
            "The second assignment rebinds the name to a string object, and the type "
            "reported is the type of the object the name now points at. Nothing is "
            "raised because the type of a name is never fixed at assignment time."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="A function unexpectedly changes a list the caller still needs. What is the cause?",
        choices=[
            "Python copies list arguments lazily, so the copy is incomplete.",
            "The caller must have passed a tuple.",
            "The function mutated the argument in place; assignment does not copy.",
            "The list was sorted rather than mutated.",
        ],
        answer=2,
        kind="debugging",
        explanation=(
            "A mutable object passed as an argument is passed by reference, so "
            "appending inside the function changes the caller's list. Returning a new "
            "list, or copying at the boundary, restores the caller's independence."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="What is the consequence of executing `list = [1, 2, 3]` at module level?",
        choices=[
            "Python deletes the built-in list for everyone.",
            "It raises a SyntaxError at import time.",
            "It makes the list built-in faster.",
            "The name list now refers to the new object for the rest of that scope.",
        ],
        answer=3,
        kind="identify_error",
        explanation=(
            "The name is rebound in the module namespace, so every later use of list in "
            "that scope resolves to your object. The error surfaces only when the name is "
            "called, as a TypeError, often far from the assignment."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="Why convert values to their final types once, at the boundary of a program?",
        choices=[
            "So the rest of the program can rely on the type without repeating checks.",
            "Because Python forbids mixed types in a single expression.",
            "To make the program use less memory.",
            "Because conversion is faster than reading a value.",
        ],
        answer=0,
        kind="reasoning",
        explanation=(
            "Converting at the boundary means every function downstream receives a value "
            "it can use without re-checking, which removes both duplicated logic and the "
            "type errors that appear deep inside a pipeline."
        ),
        reference="lesson.ipynb - Summary",
    )
)

QUIZ.append(
    quiz(
        question="Which name follows PEP 8 for a module-level constant?",
        choices=[
            "maxSpeedMps",
            "MAX_SPEED_MPS",
            "Max_Speed_Mps",
            "max speed mps",
        ],
        answer=1,
        kind="multiple_choice",
        explanation=(
            "PEP 8 reserves UPPER_SNAKE_CASE for constants that must not be rebound. "
            "camelCase is not a Python convention, and a name containing spaces is not "
            "a valid identifier at all."
        ),
        reference="lesson.ipynb - Syntax",
    )
)
