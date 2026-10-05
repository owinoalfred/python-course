"""Topic 1.1 — Introduction to Python.

Hand-authored to the Course Content Standard (see the rebuild plan): a full
25-section lesson with 14 executable code cells, ten topic-specific exercises
with real examples, a diversified quiz, and a research scaffold that ships no
fabricated data.
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
        "Python is a **general-purpose, high-level programming language** created by "
        "Guido van Rossum and first released in 1991. Its design was guided by a "
        "single persistent idea: code is read far more often than it is written, so "
        "the language should make the *reading* easy. That idea is why Python uses "
        "indentation for structure, why its syntax avoids ceremony, and why it ships "
        "a large *standard library* rather than pushing everything to third parties."
    ),
    MD(
        "Python is **interpreted**, or more precisely *compiled to bytecode and then "
        "interpreted*. When you run a `.py` file, CPython parses your source into an "
        "abstract syntax tree, compiles that into a compact set of instructions, and "
        "then executes those instructions in a loop. You never see this bytecode, but "
        "it is the reason a Python program starts instantly without a separate build "
        "step — and the reason runtime errors and syntax errors currently feel "
        "different from each other."
    ),
    MD(
        "Python is also **dynamically typed**. A name is a *label* bound to an object, "
        "not a box with a fixed type. The same name can refer to an integer now and a "
        "string a moment later; the type lives on the object, and it is checked while "
        "the program runs."
    ),
    CODE_CELL(
        "import sys\n"
        "\n"
        "print(f\"Interpreter : {sys.implementation.name}\")\n"
        "print(f\"Version     : {sys.version.split()[0]}\")\n"
        "print(f\"Executable  : {sys.executable}\")"
    ),
    CODE_CELL(
        "value = 42\n"
        "print(value, type(value))\n"
        "\n"
        "value = \"rover-01\"   # rebinding: the name now points at a str\n"
        "print(value, type(value))"
    ),
    NOTE(
        "Robotics context",
        "Modern robotics leans on Python for orchestration, perception glue, "
        "telemetry and tooling. ROS 2's Python client, numpy, OpenCV bindings and "
        "most fleet dashboards are Python. The low-level control loop may be C++, but "
        "the code that decides *what the robot should do next* is very often Python.",
    ),
    MD(
        "Three further design decisions shape everything you write. First, "
        "**indentation is syntax**: Python removed braces precisely so that the "
        "visual structure of a program and its meaning could not drift apart. "
        "Second, the language is **batteries-included** — file handling, dates, "
        "JSON, sockets and unit testing all ship with the interpreter, so a small "
        "robot utility rarely needs a third-party dependency. Third, Python is a "
        "**glue language**: it is usually at the top of a stack, calling into C, "
        "C++ or Fortran for the parts where raw speed matters, which is exactly the "
        "trade-off a robotics stack makes."
    ),
    MD(
        "One consequence deserves emphasis early. Because there is no compile-time "
        "type declaration, a name can silently change type part-way through a "
        "program, and nothing will complain until an operation is attempted on the "
        "value. That is not sloppiness in the language; it is the price of the "
        "flexibility that makes Python productive. Throughout this course you will "
        "learn to manage that flexibility deliberately: convert types explicitly at "
        "the boundaries where data enters your program, annotate the functions that "
        "others depend on, and test the cases where a value might be missing or of "
        "an unexpected type."
    ),
]

LESSON["formal_theory"] = [
    MD(
        "Formally, an **interpreter** executes a program by repeatedly reading a unit "
        "of work and performing it, whereas a **compiler** translates a whole program "
        "into another language before any of it runs. CPython is a hybrid: it compiles "
        "to an intermediate *bytecode* and then interprets that bytecode. The pipeline "
        "has four observable stages."
    ),
    EQUATION(
        "source (.py)  ->  tokens  ->  AST  ->  bytecode  ->  evaluation loop (CPython VM)"
    ),
    STEPS(
        [
            "The **lexer** turns characters into tokens (names, numbers, operators).",
            "The **parser** builds an Abstract Syntax Tree that encodes structure.",
            "The **compiler** emits bytecode — a flat list of instructions.",
            "The **evaluation loop** executes those instructions one at a time.",
        ]
    ),
    MD(
        "Because the AST is built before execution, *syntax errors* are raised before "
        "anything runs, while *runtime errors* (like dividing by zero) happen in the "
        "evaluation loop. You can observe the compiled form directly:"
    ),
    CODE_CELL(
        "import dis\n"
        "\n"
        "\n"
        "def cruise_control(target_speed_mps: float) -> float:\n"
        "    return target_speed_mps * 1.0\n"
        "\n"
        "\n"
        "dis.dis(cruise_control)"
    ),
    TABLE(
        ["Term", "Meaning"],
        [
            ["CPython", "The reference implementation written in C."],
            ["Bytecode", "Portable instructions executed by the CPython VM."],
            ["AST", "Tree representation of source structure, built before running."],
            ["Duck typing", "Behaviour matters more than declared type at runtime."],
        ],
    ),
]

LESSON["syntax"] = [
    MD(
        "Python's surface syntax is deliberately small. An **assignment** binds a name "
        "to the value on the right with a single `=`. A **statement** occupies a line, "
        "and indentation (four spaces is the convention) defines blocks. There are no "
        "braces and no mandatory semicolons."
    ),
    MD("The canonical form:"),
    CODE_CELL(
        "# canonical: one statement per line, four-space indentation\n"
        "robot_name = \"rover-01\"\n"
        "max_speed_mps = 1.5\n"
        "print(robot_name, max_speed_mps)"
    ),
    MD(
        "The anti-pattern — legal, but it fights the language and hides bugs:"
    ),
    CODE(
        "robot_name = \"rover-01\"; max_speed_mps = 1.5;   # semicolons: legal, unidiomatic\n"
        "print( robot_name ,  max_speed_mps )            # irregular spacing"
    ),
    WARN(
        "Whitespace is significant",
        "Indentation is part of the grammar, not decoration. Mixing tabs and spaces "
        "raises `TabError`; a stray space can silently change which block a line "
        "belongs to.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 — names, values and f-strings.**"),
    CODE_CELL(
        "robot = \"rover-01\"\n"
        "battery_pct = 87.5\n"
        "print(f\"{robot}: battery at {battery_pct}%\")"
    ),
    MD("**Example 2 — arithmetic and division.**"),
    CODE_CELL(
        "distance_m = 3.0\n"
        "speed_mps = 1.5\n"
        "print(distance_m / speed_mps, \"seconds\")"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "Because typing is dynamic, the *type of a value* is itself something you can "
        "inspect at runtime. This one-liner is the fastest way to see Python's dynamic "
        "typing in action:"
    ),
    CODE_CELL(
        "def describe(obj):\n"
        "    return f\"{obj!r} -> {type(obj).__name__}\"\n"
        "\n"
        "\n"
        "for sample in (7, 3.14, \"dock\", True, None):\n"
        "    print(describe(sample))"
    ),
    TIP(
        "repr vs str",
        "The `!r` conversion calls `repr()`, which shows a value the way you would "
        "write it in code (`'dock'` with quotes). Plain `{}` uses `str()`. In "
        "debugging output, prefer `!r`.",
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "Python's bytecode carries a *cache tag* that ties it to a specific CPython "
        "version. This is why a `.pyc` compiled by 3.11 is ignored by 3.12 — an "
        "engineering detail worth knowing when shipping to a fleet of machines."
    ),
    CODE_CELL(
        "import sys\n"
        "\n"
        "print(\"bytecode cache tag:\", sys.implementation.cache_tag)\n"
        "print(\"supports hash randomisation:\", sys.flags.hash_randomization)"
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "Here is the smallest *useful* ROBO-X bring-up script. It reads the running "
        "interpreter, formats a boot banner, and only executes when run as a program "
        "— not when imported."
    ),
    CODE_CELL(
        "\"\"\"robo_boot.py — the smallest useful ROBO-X bring-up script.\"\"\"\n"
        "from __future__ import annotations\n"
        "\n"
        "import sys\n"
        "\n"
        "ROBOT_NAME = \"rover-01\"\n"
        "\n"
        "\n"
        "def boot_banner(name: str) -> str:\n"
        "    version = sys.version.split()[0]\n"
        "    return (\n"
        "        f\"ROBO-X '{name}' booting\\n\"\n"
        "        f\"  python : {version}\\n\"\n"
        "        f\"  status : READY\"\n"
        "    )\n"
        "\n"
        "\n"
        "def main() -> int:\n"
        "    print(boot_banner(ROBOT_NAME))\n"
        "    return 0\n"
        "\n"
        "\n"
        "if __name__ == \"__main__\":\n"
        "    main()"
    ),
]

LESSON["line_by_line"] = [
    MD("Line by line, matching the walkthrough above:"),
    STEPS(
        [
            "`from __future__ import annotations` makes type hints lazy strings — free "
            "forward compatibility for annotations.",
            "`import sys` imports the module holding interpreter metadata.",
            "`ROBOT_NAME = \"rover-01\"` is a module-level constant; UPPER_CASE signals "
            "\"do not rebind\".",
            "`def boot_banner(name: str) -> str:` declares a function with a parameter "
            "and a return annotation.",
            "The f-string builds a multi-line banner; `sys.version.split()[0]` extracts "
            "just the version number.",
            "`main()` is the program entry point; returning an `int` exit code is a "
            "Unix convention.",
            "The `if __name__ == \"__main__\":` guard runs `main()` only when the file "
            "is executed directly, not when it is imported.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 — using `=` (assign) where `==` (compare) is meant.**"),
    CODE(
        "# wrong: this rebinds battery_pct instead of testing it\n"
        "if battery_pct = 0:\n"
        "    print('flat')",
        lang="text",
    ),
    CODE(
        "# right\n"
        "if battery_pct == 0:\n"
        "    print('flat')"
    ),
    MD("**Mistake 2 — shadowing a built-in name.**"),
    CODE(
        "# wrong: 'list' now refers to your variable, not the built-in\n"
        "list = [1, 2, 3]\n"
        "more = list((4, 5))        # TypeError: 'list' object is not callable\n"
        "\n"
        "# right\n"
        "waypoints = [1, 2, 3]\n"
        "more = list((4, 5))"
    ),
    MD("**Mistake 3 — inconsistent indentation across an editor change.**"),
    CODE(
        "# wrong: mixing tabs and spaces in the same block\n"
        "for i in range(2):\n"
        "\tprint(i)        # a tab\n"
        "        print(i)  # spaces -> TabError",
        lang="text",
    ),
    CODE(
        "# right: four spaces everywhere\n"
        "for i in range(2):\n"
        "    print(i)"
    ),
    MD("**Mistake 4 — expecting an implicit return.**"),
    CODE(
        "# wrong: this returns None\n"
        "def battery_ok(pct):\n"
        "    pct > 20\n"
        "\n"
        "# right\n"
        "def battery_ok(pct):\n"
        "    return pct > 20"
    ),
    MD(
        "These four share a pattern worth naming: each one is *syntactically* "
        "valid, so the interpreter accepts the file without complaint. Nothing warns "
        "you at load time that a condition was written as an assignment, that a "
        "built-in has been shadowed, that two indentation styles disagree, or that a "
        "comparison was evaluated and thrown away. Python will run the program and "
        "let the consequences appear later — often far from the line that caused "
        "them. This is precisely why the debugging techniques below exist, and why "
        "tests that assert on returned values catch defects that reading the source "
        "line by line sometimes misses."
    ),
]

LESSON["debugging_techniques"] = [
    MD("Three techniques you will use constantly, in order of cost:"),
    STEPS(
        [
            "**Type inspection.** Print `type(x)` and `repr(x)` — most beginner bugs "
            "are \"this is a string when I assumed an int\".",
            "**Read the traceback bottom-up.** The last line names the exception; the "
            "frames above it name the code path.",
            "**`breakpoint()`.** Insert `breakpoint()` to drop into pdb and inspect "
            "live values.",
        ]
    ),
    CODE(
        "value = \"12\"\n"
        "print(type(value))     # <class 'str'>\n"
        "print(repr(value))     # '12'\n"
        "value = int(value)     # now safe to do arithmetic"
    ),
    NOTE(
        "Interpreter identity",
        "`import sys; print(sys.implementation.name)` proves which interpreter runs "
        "your code. A surprising number of \"Python is broken\" reports are really "
        "\"I am running a different Python than I think\".",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Follow **PEP 8**: four-space indents, `snake_case` for functions and "
            "variables, `UPPER_CASE` for constants.",
            "Give names meaning: `battery_pct` beats `b`.",
            "Keep one statement per line; drop the semicolons.",
            "Add short docstrings to modules and functions.",
            "Prefer small, testable functions over long scripts.",
            "Never shadow built-ins (`list`, `dict`, `id`, `type`).",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "At this stage, performance is about *knowing what costs what*, not "
        "micro-optimising. Starting the interpreter costs milliseconds; in CPython, "
        "attribute lookups and interpreted loop iterations dominate in hot paths. "
        "Worry about asymptotics first (an O(n^2) loop over 5,000 telemetry rows "
        "matters; a single extra function call does not), and reach for numpy or a "
        "C extension only after you have measured."
    ),
    TIP(
        "Measure, do not guess",
        "Use `time.perf_counter()` around the small piece of code you suspect. The "
        "`timeit` module automates repeats. Never optimise before measuring.",
    ),
    MD(
        "A concrete illustration. Summing one column of a 5,000-row telemetry file "
        "with a Python loop performs roughly one interpreted operation per element; "
        "the same arithmetic delegated to a library routine performs the loop inside "
        "compiled code. The gap between those two approaches is usually large enough "
        "to matter, while the gap between two differently written Python loops on the "
        "same data is usually not. Measure which case you are in before spending "
        "effort on it, and prefer the clearest implementation until measurement "
        "proves otherwise."
    ),
]

LESSON["pythonic_approaches"] = [
    MD("The same intent, written the way an experienced Python engineer would:"),
    CODE_CELL(
        "# Before: manual index bookkeeping\n"
        "names = [\"front\", \"rear\", \"left\"]\n"
        "i = 0\n"
        "while i < len(names):\n"
        "    print(i, names[i])\n"
        "    i += 1\n"
        "\n"
        "# After: iterate directly, with enumerate when you need the index\n"
        "for index, name in enumerate(names):\n"
        "    print(index, name)"
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "Python is the language of robotics *glue*: it reads sensors, decides an "
        "action, and logs what happened. The course ships a deterministic simulator, "
        "so you never need hardware to practise. The snippet below is the smallest "
        "interaction with a ROBO-X robot."
    ),
    CODE_CELL(
        "import sys\n"
        "from pathlib import Path\n"
        "\n"
        "# Locate the course root (the folder containing `shared/`) and import the sim.\n"
        "here = Path.cwd()\n"
        "root = next((p for p in [here, *here.parents] if (p / \"shared\").is_dir()), None)\n"
        "if root is not None:\n"
        "    sys.path.insert(0, str(root))\n"
        "\n"
        "from shared.robo_x_sim import SimulatedRobot  # noqa: E402\n"
        "\n"
        "robot = SimulatedRobot(name=\"rover-01\", battery_wh=48.0)\n"
        "print(robot.status())"
    ),
    NOTE(
        "Reproducible by design",
        "The simulator is seeded, so the readings above are identical on your machine "
        "and on mine. That is what makes the exercises gradeable without hardware.",
    ),
]

LESSON["engineering_example"] = [
    MD(
        "A complete, runnable utility that a fleet engineer would actually write: "
        "summarise a robot's state into one line for a status dashboard."
    ),
    CODE_CELL(
        "def status_line(state: dict) -> str:\n"
        "    name = state[\"name\"]\n"
        "    pct = state[\"battery_pct\"]\n"
        "    pos = state[\"position\"]\n"
        "    flag = \"LOW\" if pct < 20 else \"OK\"\n"
        "    return f\"{name:<10} {pct:5.1f}%  ({pos[0]:.1f}, {pos[1]:.1f})  {flag}\"\n"
        "\n"
        "\n"
        "sample = {\n"
        "    \"name\": \"rover-01\",\n"
        "    \"battery_pct\": 18.4,\n"
        "    \"position\": (12.0, 3.5),\n"
        "}\n"
        "print(status_line(sample))"
    ),
]

LESSON["guided_practice"] = [
    MD(
        "Follow along in your own notebook. Each step is runnable before the next "
        "begins."
    ),
    STEPS(
        [
            "Bind a variable `robot_name` to a short string and print it.",
            "Bind `battery_pct` to a float and print an f-string that includes it.",
            "Print `type()` and `repr()` of both variables.",
            "Rebind `battery_pct` to the string `\"unknown\"` and observe that Python "
            "allows it — then argue why that is dangerous for a robot.",
        ]
    ),
    CODE_CELL(
        "# Your turn — complete the steps above.\n"
        "robot_name = \"rover-02\"\n"
        "battery_pct = 91.0\n"
        "print(f\"{robot_name}: {battery_pct}%\")\n"
        "print(type(battery_pct), repr(battery_pct))"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: Python as a very fast, very literal assistant.** You write "
        "instructions in order; the assistant reads them top to bottom and does "
        "exactly what each line says — including the surprising things. It does not "
        "guess intent, so the burden of being precise is on you."
    ),
    TABLE(
        ["You are used to", "In Python"],
        [
            ["A variable is a box with a type", "A name is a label for an object"],
            ["Braces define blocks", "Indentation defines blocks"],
            ["Code is compiled ahead of time", "Code is compiled to bytecode at import"],
            ["Types are declared", "Types are dynamic and checked at runtime"],
        ],
    ),
]

TERMS = [
    ["Interpreter", "A program that executes source code instruction by instruction."],
    ["CPython", "The reference Python implementation, written in C."],
    ["Bytecode", "Compact instructions produced by the compiler and run by the VM."],
    ["REPL", "Read-Eval-Print Loop: the interactive prompt."],
    ["Name binding", "Attaching a name to an object with `=`."],
    ["Dynamic typing", "Types are attached to objects and checked at runtime."],
    ["PEP 8", "The style guide for Python code."],
    ["Duck typing", "If it walks and quacks like a duck, treat it as one."],
    ["Standard library", "The batteries-included modules shipped with Python."],
]

LESSON["summary"] = [
    MD(
        "Python is an interpreted, dynamically typed, general-purpose language built "
        "around readability. CPython compiles your source to bytecode and interprets "
        "that; names are labels bound to objects; types live on objects and are "
        "checked at runtime. These three facts explain almost every beginner "
        "surprise — from why syntax errors appear before runtime errors, to why a "
        "variable can change type mid-program."
    ),
    MD(
        "In robotics, Python is the orchestration layer: it reads sensors, makes "
        "decisions and logs results, often calling into faster C or C++ code for the "
        "tightest control loops. Everything that follows in this course builds on the "
        "interpreter model and the naming rules introduced here."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "Python is read-optimised: indentation and small syntax are deliberate.",
            "CPython compiles to bytecode, then interprets it — errors are either "
            "pre-execution (syntax) or in the evaluation loop (runtime).",
            "Names are labels; objects carry types; typing is dynamic.",
            "`if __name__ == \"__main__\":` separates \"run as program\" from \"import\".",
            "PEP 8 names and conventions make code predictable for teams.",
            "Python is the robotics glue layer; the seeded simulator lets you practise "
            "with no hardware.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "[The Python Tutorial](https://docs.python.org/3/tutorial/) — official and "
            "excellent.",
            "[PEP 8 — Style Guide](https://peps.python.org/pep-0008/) — the conventions "
            "this course follows.",
            "[Python Developer's Guide: the CPython interpreter](https://devguide.python.org/) "
            "— how the interpreter is built.",
            "[`dis` module docs](https://docs.python.org/3/library/dis.html) — inspect "
            "bytecode yourself.",
            "[The Zen of Python](https://peps.python.org/pep-0020/) — `import this`.",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Boot banner formatter",
        difficulty="MEDIUM",
        learning_objectives=[
            "Bind variables and build an f-string.",
            "Return a value from a function.",
        ],
        concepts_tested=["variables", "f-strings", "functions"],
        problem_statement=(
            "Write `boot_banner(name, version)` that returns the single line "
            "`ROBO-X '<name>' ready on Python <version>`. Every ROBO-X service prints "
            "this at start-up."
        ),
        requirements=[
            "Return a string (do not print inside the function).",
            "Use a single f-string to assemble the result.",
        ],
        constraints=["No third-party libraries.", "Pure function: same input, same output."],
        input_description="`name` is a non-empty string; `version` is a version string.",
        expected_output="A single formatted string.",
        example_input='name="rover-01", version="3.12.3"',
        example_output="ROBO-X 'rover-01' ready on Python 3.12.3",
        edge_cases=["Empty name raises ValueError.", "Name containing spaces is preserved."],
        hints=["Concatenate the pieces inside one f-string.", "Validate the name first."],
        success_criteria=["Exact string match for the example.", "Rejects an empty name."],
        optional_extension="Add an optional `role` argument defaulting to 'rover'.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Sensor string to float",
        difficulty="MEDIUM",
        learning_objectives=["Convert types safely.", "Return a fallback on bad input."],
        concepts_tested=["type conversion", "exception handling", "defaults"],
        problem_statement=(
            "Write `reading(raw, default=0.0)` that converts a sensor string such as "
            "`'12.5'` to a float, returning `default` when the text is not a valid "
            "number."
        ),
        requirements=[
            "Use `float()` inside a try/except.",
            "Never raise for malformed input; return `default` instead.",
        ],
        constraints=["Catch only ValueError, not a bare except."],
        input_description="`raw` is a string (possibly `''` or `'n/a'`).",
        expected_output="A float, or `default` when conversion fails.",
        example_input="reading('12.5')",
        example_output="12.5",
        edge_cases=["Empty string.", "Text such as 'n/a'.", "Leading/trailing whitespace."],
        hints=["`float(' 3 ')` works — whitespace is stripped by the parser."],
        success_criteria=["Returns 12.5 for '12.5'.", "Returns 0.0 for 'n/a'."],
        optional_extension="Accept a unit suffix like '12.5cm' by stripping it first.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Total distance travelled",
        difficulty="MEDIUM",
        learning_objectives=["Iterate a sequence.", "Accumulate a running total."],
        concepts_tested=["loops", "accumulators", "floats"],
        problem_statement=(
            "Write `total_distance(segments)` that sums a list of metre values and "
            "returns the total rounded to two decimals."
        ),
        requirements=["Handle an empty list.", "Return a float."],
        constraints=["Use a loop or `sum()`, not a manual index."],
        input_description="`segments` is a list of non-negative numbers.",
        expected_output="A float rounded to two decimals.",
        example_input="total_distance([1.5, 2.0, 3.25])",
        example_output="6.75",
        edge_cases=["Empty list returns 0.0.", "Single segment.", "Large lists."],
        hints=["`round(total, 2)` controls the precision."],
        success_criteria=["Returns 6.75 for the example.", "Returns 0.0 for []."],
        optional_extension="Raise ValueError if any segment is negative.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Clamp a battery percentage",
        difficulty="MEDIUM",
        learning_objectives=["Apply conditional logic.", "Clamp a numeric value."],
        concepts_tested=["conditionals", "comparison", "clamping"],
        problem_statement=(
            "Write `clamp_pct(value)` that limits a battery percentage to the range "
            "0–100, returning the nearest bound for out-of-range values."
        ),
        requirements=["Return 0 for values below 0.", "Return 100 for values above 100."],
        constraints=["Show the branches explicitly — do not hide them behind min/max."],
        input_description="`value` is a number (possibly negative or above 100).",
        expected_output="A number within [0, 100].",
        example_input="clamp_pct(118.0)",
        example_output="100",
        edge_cases=["Exactly 0 and 100.", "Negative values.", "Floating point values."],
        hints=["Two `if` branches are enough."],
        success_criteria=["Clamps 118 to 100 and -5 to 0.", "Leaves 42 unchanged."],
        optional_extension="Also return how much the value was clamped by.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Pair sensor names with readings",
        difficulty="MEDIUM",
        learning_objectives=["Build a dict from parallel lists.", "Use zip."],
        concepts_tested=["dictionaries", "zip", "iteration"],
        problem_statement=(
            "Write `pairs(names, readings)` that returns a dict mapping each name to "
            "its reading, stopping at the shorter list."
        ),
        requirements=["Use `zip` or index-together logic.", "Do not raise on unequal lengths."],
        constraints=["Return a plain dict."],
        input_description="Two sequences of equal or unequal length.",
        expected_output="A dict of name to reading.",
        example_input="pairs(['imu', 'batt'], [0.3, 12.6])",
        example_output="{'imu': 0.3, 'batt': 12.6}",
        edge_cases=["Unequal lengths truncate.", "Empty lists.", "Duplicate names."],
        hints=["`dict(zip(names, readings))` is the one-liner."],
        success_criteria=["Matches the example.", "Empty inputs give {}."],
        optional_extension="Also return the names that had no reading.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Parse a configuration line",
        difficulty="HARD",
        learning_objectives=["Parse structured text.", "Validate and report errors."],
        concepts_tested=["strings", "dictionaries", "validation"],
        problem_statement=(
            "Write `parse_config(line)` that turns `'max_speed=1.5; battery=48'` into "
            "`{'max_speed': 1.5, 'battery': 48}`. Values that look numeric become int "
            "or float; everything else stays a string. Raise `ValueError` on a "
            "malformed pair."
        ),
        requirements=[
            "Split on ';' then on '=' preserving at most one split per pair.",
            "Skip blank segments; reject pairs without '='.",
        ],
        constraints=["No regular expressions — plain string methods only."],
        input_description="A single string with `key=value` chunks separated by `;`.",
        expected_output="A dict with numeric values converted where possible.",
        example_input="parse_config('max_speed=1.5; mode=auto')",
        example_output="{'max_speed': 1.5, 'mode': 'auto'}",
        edge_cases=["Trailing ';'.", "Whitespace around keys.", "Segment without '='."],
        hints=["Write a small `_convert(token)` helper.", "`int` then `float` then str."],
        success_criteria=["Parses the example.", "Raises ValueError on 'oops'."],
        optional_extension="Support quoted values containing ';'.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Distance between two waypoints",
        difficulty="HARD",
        learning_objectives=["Work with tuples.", "Apply the Pythagorean theorem."],
        concepts_tested=["tuples", "arithmetic", "math"],
        problem_statement=(
            "Write `distance(p, q)` returning the Euclidean distance between 2-D "
            "points `p` and `q` given as `(x, y)` tuples, rounded to three decimals."
        ),
        requirements=["Accept any sequences of length 2.", "Return a float."],
        constraints=["Use `math.hypot` or `** 0.5`; no numpy."],
        input_description="Two 2-tuples of numbers.",
        expected_output="A float rounded to three decimals.",
        example_input="distance((0, 0), (3, 4))",
        example_output="5.0",
        edge_cases=["Identical points give 0.0.", "Negative coordinates.", "Floats."],
        hints=["`dx = q[0] - p[0]` before squaring."],
        success_criteria=["Returns 5.0 for (0,0)-(3,4).", "Returns 0.0 for identical points."],
        optional_extension="Add a `manhattan(p, q)` function for comparison.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Run-length encode a string",
        difficulty="HARD",
        learning_objectives=["Scan a sequence.", "Build a result incrementally."],
        concepts_tested=["strings", "loops", "state"],
        problem_statement=(
            "Write `rle(text)` returning the run-length encoding of `text`, e.g. "
            "`'aaabbc'` becomes `'a3b2c1'`."
        ),
        requirements=["Count consecutive equal characters.", "Handle an empty string."],
        constraints=["Single pass; no regex."],
        input_description="A string (possibly empty).",
        expected_output="A string of `char+count` chunks.",
        example_input="rle('aaabbc')",
        example_output="'a3b2c1'",
        edge_cases=["Empty string gives ''.", "All identical characters.", "Single character."],
        hints=["Track the current character and a counter; flush on change."],
        success_criteria=["Encodes 'aaabbc' as 'a3b2c1'.", "Empty input gives ''."],
        optional_extension="Also write the decoder `unrle`.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Word frequency table",
        difficulty="HARD",
        learning_objectives=["Normalise text.", "Aggregate counts in a dict."],
        concepts_tested=["strings", "dictionaries", "sorting"],
        problem_statement=(
            "Write `word_counts(text)` returning a dict of lower-cased words to their "
            "count, ignoring punctuation and empty tokens."
        ),
        requirements=["Split on non-alphabetic characters.", "Sort the result by count "
                       "(descending) then word (ascending)."],
        constraints=["Standard library only."],
        input_description="A sentence or paragraph.",
        expected_output="A dict ordered by frequency then alphabetically.",
        example_input="word_counts('Dock dock; rover!')",
        example_output="{'dock': 2, 'rover': 1}",
        edge_cases=["Empty string.", "Only punctuation.", "Mixed case."],
        hints=["Use a list comprehension to keep alphabetic characters."],
        success_criteria=["Counts 'dock' twice in the example.", "Empty input gives {}."],
        optional_extension="Return the top-N words as a list of tuples.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Validate robot state records",
        difficulty="HARD",
        learning_objectives=["Validate records.", "Collect and report failures."],
        concepts_tested=["dictionaries", "validation", "error reporting"],
        problem_statement=(
            "Write `validate_states(records)` returning `(valid, errors)` where each "
            "record needs `id` (str) and `battery_pct` (number in 0–100). `errors` maps "
            "the record index to a reason string."
        ),
        requirements=["Separate valid records from invalid ones.", "Never raise."],
        constraints=["Return a tuple `(list, dict)`."],
        input_description="A list of dicts.",
        expected_output="A tuple of (valid_records, errors_by_index).",
        example_input="validate_states([{'id': 'r1', 'battery_pct': 50}, {'id': 'r2'}])",
        example_output="([{'id': 'r1', 'battery_pct': 50}], {1: 'missing battery_pct'})",
        edge_cases=["Empty list.", "battery_pct out of range.", "Wrong types."],
        hints=["Check `id` first, then `battery_pct`, appending a specific reason."],
        success_criteria=["Splits the example correctly.", "Empty input gives ([], {})."],
        optional_extension="Also flag duplicate ids across the batch.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "def boot_banner(name: str, version: str) -> str:\n"
            '    if not name:\n'
            '        raise ValueError("name must be non-empty")\n'
            '    return f"ROBO-X \'{name}\' ready on Python {version}"'
        ),
        explanation=(
            "The function validates its input before formatting, so an empty name "
            "fails loudly instead of producing a misleading banner. The f-string "
            "assembles the whole line in one expression, which keeps the embedded "
            "quotes readable."
        ),
        complexity="Time O(n) in the length of the strings; space O(n) for the result.",
        edge_cases="An empty name raises ValueError; spaces inside the name survive intact.",
        alternative_approaches="'...'.format(...) or string concatenation are equivalent here.",
        testing=(
            'assert boot_banner("rover-01", "3.12.3") == '
            '"ROBO-X \'rover-01\' ready on Python 3.12.3"'
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def reading(raw, default: float = 0.0) -> float:\n"
            "    try:\n"
            "        return float(raw)\n"
            "    except ValueError:\n"
            "        return default"
        ),
        explanation=(
            "float() raises ValueError for text it cannot parse, and catching that "
            "specific exception keeps genuine bugs such as TypeError visible. The "
            "default argument supplies the fallback without a second parameter."
        ),
        complexity="Time O(n) in the length of the input string; space O(1).",
        edge_cases="'n/a' and '' both fall back to the default; surrounding whitespace is tolerated.",
        alternative_approaches="str.strip() plus an explicit numeric check is longer but clearer to beginners.",
        testing=(
            "assert reading('12.5') == 12.5\n"
            "assert reading('n/a') == 0.0\n"
            "assert reading('n/a', default=-1.0) == -1.0"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code="def total_distance(segments) -> float:\n    return round(sum(segments), 2)",
        explanation=(
            "sum() runs in a single C-level pass, which is both the clearest and the "
            "fastest option here. round() at the boundary keeps float accumulation "
            "error out of the returned value, and an empty list sums to 0 naturally."
        ),
        complexity="Time O(n); space O(1) beyond the input.",
        edge_cases="An empty list returns 0.0 because the sum of nothing is 0.",
        alternative_approaches="An explicit for-loop with a running total makes the accumulation visible for teaching.",
        testing="assert total_distance([1.5, 2.0, 3.25]) == 6.75\nassert total_distance([]) == 0.0",
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "def clamp_pct(value):\n"
            "    if value < 0:\n"
            "        return 0\n"
            "    if value > 100:\n"
            "        return 100\n"
            "    return value"
        ),
        explanation=(
            "Two early-return guards make the clamp explicit: each bound is checked "
            "and returned immediately, so the happy path is the fall-through. That is "
            "easier to read and to debug than nested conditionals."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="Exactly 0 and exactly 100 pass through unchanged.",
        alternative_approaches="max(0, min(100, value)) is shorter but hides the two distinct rules.",
        testing="assert clamp_pct(118.0) == 100\nassert clamp_pct(-5) == 0\nassert clamp_pct(42) == 42",
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code="def pairs(names, readings):\n    return dict(zip(names, readings))",
        explanation=(
            "zip() yields pairs lazily and stops at the shorter sequence, which is "
            "exactly the required truncation behaviour, so no length check is needed. "
            "dict() then consumes those pairs as key/value entries."
        ),
        complexity="Time O(n); space O(n) for the resulting dict.",
        edge_cases="Duplicate names collapse, keeping the last reading; empty inputs give an empty dict.",
        alternative_approaches="A for-loop over range(min(len(a), len(b))) states the truncation rule explicitly.",
        testing=(
            "assert pairs(['imu', 'batt'], [0.3, 12.6]) == {'imu': 0.3, 'batt': 12.6}\n"
            "assert pairs([], []) == {}\n"
            "assert pairs(['a', 'b'], [1]) == {'a': 1}"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "def _convert(token: str):\n"
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
            "def parse_config(line: str) -> dict:\n"
            "    config: dict = {}\n"
            "    for chunk in line.split(';'):\n"
            "        chunk = chunk.strip()\n"
            "        if not chunk:\n"
            "            continue\n"
            "        if '=' not in chunk:\n"
            "            raise ValueError(f'malformed pair: {chunk!r}')\n"
            "        key, _, value = chunk.partition('=')\n"
            "        config[key.strip()] = _convert(value.strip())\n"
            "    return config"
        ),
        explanation=(
            "_convert() tries the narrowest type first, then float, and finally falls "
            "back to the original string, so the ordering drives correctness. "
            "partition('=') splits on the first separator only, which keeps values "
            "containing '=' intact, and blank segments are skipped before validation."
        ),
        complexity="Time O(n) in the line length; space O(k) for k parsed pairs.",
        edge_cases="Trailing ';' is skipped; whitespace is stripped; a missing '=' raises ValueError.",
        alternative_approaches="A regular expression with named groups is concise but hides the parsing steps.",
        testing=(
            "assert parse_config('max_speed=1.5; mode=auto') == "
            "{'max_speed': 1.5, 'mode': 'auto'}\n"
            "assert parse_config('battery=48') == {'battery': 48}"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "import math\n"
            "\n"
            "\n"
            "def distance(p, q) -> float:\n"
            "    dx = q[0] - p[0]\n"
            "    dy = q[1] - p[1]\n"
            "    return round(math.hypot(dx, dy), 3)"
        ),
        explanation=(
            "math.hypot computes sqrt(dx*dx + dy*dy) while avoiding intermediate "
            "overflow for very large coordinates, so it is safer than squaring by "
            "hand. Destructuring the two sequences first keeps the arithmetic tied "
            "to the geometry rather than the container type."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="Identical points give 0.0; negative coordinates are handled without special cases.",
        alternative_approaches="math.dist(p, q) does the same thing in one call from Python 3.8 onwards.",
        testing=(
            "assert distance((0, 0), (3, 4)) == 5.0\n"
            "assert distance((1.5, -2.0), (1.5, -2.0)) == 0.0"
        ),
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "def rle(text: str) -> str:\n"
            "    if not text:\n"
            "        return ''\n"
            "    parts = []\n"
            "    current = text[0]\n"
            "    count = 1\n"
            "    for ch in text[1:]:\n"
            "        if ch == current:\n"
            "            count += 1\n"
            "        else:\n"
            "            parts.append(f'{current}{count}')\n"
            "            current, count = ch, 1\n"
            "    parts.append(f'{current}{count}')\n"
            "    return ''.join(parts)"
        ),
        explanation=(
            "The encoder keeps the current character and its run length as state, and "
            "flushes the chunk whenever the character changes. The final flush after "
            "the loop is required, otherwise the last run is silently dropped. "
            "Joining at the end avoids quadratic string concatenation."
        ),
        complexity="Time O(n) in one pass; space O(n) in the number of runs.",
        edge_cases="Empty input returns ''; a single-character string returns that character with count 1.",
        alternative_approaches="itertools.groupby produces the same encoding more compactly.",
        testing="assert rle('aaabbc') == 'a3b2c1'\nassert rle('') == ''\nassert rle('zzzz') == 'z4'",
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "def word_counts(text: str) -> dict:\n"
            "    counts: dict = {}\n"
            "    for token in text.split():\n"
            "        word = ''.join(ch for ch in token.lower() if ch.isalpha())\n"
            "        if word:\n"
            "            counts[word] = counts.get(word, 0) + 1\n"
            "    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))\n"
            "    return dict(ordered)"
        ),
        explanation=(
            "Each token is lower-cased and stripped of non-alphabetic characters, "
            "which normalises punctuation without needing a regex. The sort key "
            "negates the count so the most frequent word comes first, with the word "
            "itself breaking ties alphabetically for deterministic output."
        ),
        complexity="Time O(n log k) for k distinct words; space O(k).",
        edge_cases="Empty or punctuation-only input returns an empty dict.",
        alternative_approaches="collections.Counter is shorter; the explicit loop shows the counting step for teaching.",
        testing="assert word_counts('Dock dock; rover!') == {'dock': 2, 'rover': 1}\nassert word_counts('') == {}",
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "def validate_states(records):\n"
            "    valid, errors = [], {}\n"
            "    for index, record in enumerate(records):\n"
            "        if not isinstance(record, dict):\n"
            "            errors[index] = 'record is not a mapping'\n"
            "            continue\n"
            "        if 'id' not in record:\n"
            "            errors[index] = 'missing id'\n"
            "            continue\n"
            "        pct = record.get('battery_pct')\n"
            "        if pct is None:\n"
            "            errors[index] = 'missing battery_pct'\n"
            "            continue\n"
            "        if isinstance(pct, bool) or not isinstance(pct, (int, float)):\n"
            "            errors[index] = 'battery_pct is not numeric'\n"
            "            continue\n"
            "        if not 0 <= pct <= 100:\n"
            "            errors[index] = 'battery_pct out of range'\n"
            "            continue\n"
            "        valid.append(record)\n"
            "    return valid, errors"
        ),
        explanation=(
            "Each record is checked with an early continue, so a failure records one "
            "precise reason and moves on rather than aborting the batch. The bool "
            "check comes first because bool is a subclass of int in Python and would "
            "otherwise pass the numeric test."
        ),
        complexity="Time O(n) in the number of records; space O(n) worst case.",
        edge_cases="An empty list gives ([], {}); non-dict entries are reported by index.",
        alternative_approaches="A dataclass with __post_init__ validation pushes the checks into the type.",
        testing=(
            "valid, errors = validate_states([{'id': 'r1', 'battery_pct': 50}, {'id': 'r2'}])\n"
            "assert valid == [{'id': 'r1', 'battery_pct': 50}]\n"
            "assert errors == {1: 'missing battery_pct'}\n"
            "assert validate_states([]) == ([], {})"
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
            "from shared.robo_x_sim import SimulatedRobot, SensorError  # noqa: E402\n"
            "\n"
            "DEFAULT_CHANNELS = ('distance', 'temperature', 'battery_voltage')\n"
            "\n"
            "\n"
            "def process_telemetry(data=None) -> dict:\n"
            "    channels = list(data) if data else list(DEFAULT_CHANNELS)\n"
            "    robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\n"
            "    readings = {}\n"
            "    for channel in channels:\n"
            "        try:\n"
            "            readings[channel] = robot.read_sensor(channel)\n"
            "        except SensorError:\n"
            "            readings[channel] = None\n"
            "    state = robot.status()\n"
            "    return {\n"
            "        'readings': readings,\n"
            "        'battery_pct': state['battery_pct'],\n"
            "        'ok': all(v is not None for v in readings.values()),\n"
            "    }"
        ),
        explanation=(
            "The controller reads each requested channel and catches SensorError so a "
            "single failed sensor degrades the result instead of crashing the "
            "telemetry loop. The summary field is derived from the readings, and the "
            "ok flag reports whether every channel produced a value."
        ),
        complexity="Time O(c) for c channels; space O(c).",
        edge_cases="An unknown channel raises SensorError and is recorded as None; an empty request uses the defaults.",
        alternative_approaches="Logging the failure and re-raising is better for a safety-critical controller.",
        testing=(
            "result = process_telemetry([])\n"
            "assert result['ok'] is True\n"
            "assert result['battery_pct'] > 0"
        ),
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="Why does a Python program start running without a separate build step?",
        choices=[
            "Python source is executed directly by the CPU.",
            "CPython compiles source to bytecode and then interprets that bytecode.",
            "Python is a compiled language, exactly like Java.",
            "A separate tool must be run before any Python file will work.",
        ],
        answer=1,
        kind="conceptual",
        explanation=(
            "CPython translates your source into a compact set of bytecode instructions "
            "and then executes those instructions in an evaluation loop. Because both "
            "steps happen automatically at import time, you never invoke a separate "
            "build command."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="What does `print(type(3 / 1))` display?",
        choices=[
            "<class 'float'>",
            "<class 'int'>",
            "<class 'str'>",
            "It raises a TypeError.",
        ],
        answer=0,
        kind="code_output",
        explanation=(
            "The division operator always produces a float in Python 3, even when both "
            "operands are integers and the mathematical result is a whole number. If "
            "you want an integer result you must use the floor division operator."
        ),
        reference="lesson.ipynb - Intermediate Examples",
    )
)

QUIZ.append(
    quiz(
        question=(
            "This code was meant to test a value but misbehaves. Which single change "
            "fixes it?\n\n    if battery_pct = 0:\n        print('flat')"
        ),
        choices=[
            "Replace `=` with `:=`.",
            "Wrap the condition in square brackets.",
            "Replace `=` with `==`.",
            "Add an exclamation mark before `if`.",
        ],
        answer=2,
        kind="debugging",
        explanation=(
            "A single equals sign is an assignment, so the condition stores zero into "
            "the name and always succeeds. Two equals signs perform the comparison the "
            "author intended, making the branch test the battery level correctly."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question=(
            "What is wrong with `list = [1, 2, 3]` followed by "
            "`more = list((4, 5))`?"
        ),
        choices=[
            "Lists cannot be assigned to a variable.",
            "The list literal has the wrong number of elements.",
            "Tuples cannot be converted into lists.",
            "The name `list` shadows the built-in list type.",
        ],
        answer=3,
        kind="identify_error",
        explanation=(
            "Assigning to `list` rebinds the name to your new object, so the built-in "
            "type is no longer reachable under that name. Calling it therefore raises a "
            "TypeError, and any later code in the module that expected a list breaks."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question=(
            "Renaming a variable to `d` in one function but not another breaks the "
            "program. Which principle does this best illustrate?"
        ),
        choices=[
            "Meaningful names prevent real defects, not just style complaints.",
            "Dynamic typing means renaming is always safe.",
            "Names are resolved at compile time, so a rename cannot break anything.",
            "Type hints would have caught this at compile time.",
        ],
        answer=0,
        kind="reasoning",
        explanation=(
            "A half-completed rename is a genuine defect that readable names would have "
            "made obvious during review. Short, meaningless identifiers are therefore an "
            "engineering risk rather than a matter of taste."
        ),
        reference="lesson.ipynb - Best Practices",
    )
)

QUIZ.append(
    quiz(
        question="What does the `if __name__ == '__main__':` guard accomplish?",
        choices=[
            "It makes the script start faster.",
            "It runs the block only when the file is executed directly, not when imported.",
            "It marks the file as an installable Python package.",
            "It forces Python to compile the file ahead of time.",
        ],
        answer=1,
        kind="multiple_choice",
        explanation=(
            "The guard compares the module's name against the string '__main__', which "
            "is true only during direct execution. An import sees the module's real "
            "name instead, so the guarded block is skipped and the module stays reusable."
        ),
        reference="lesson.ipynb - Code Walkthrough",
    )
)

QUIZ.append(
    quiz(
        question=(
            "What does this print?\n\nvalue = 42\nvalue = 'forty-two'\n"
            "print(type(value).__name__)"
        ),
        choices=[
            "int",
            "NameError",
            "It raises a SyntaxError.",
            "str",
        ],
        answer=3,
        kind="code_output",
        explanation=(
            "Assigning to an existing name rebinds it to the new object, so the string "
            "now carries the type information. No error is raised because Python checks "
            "types dynamically at runtime rather than when the line is parsed."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question=(
            "Why do the course exercises run against a seeded simulator rather than "
            "against real robot hardware?"
        ),
        choices=[
            "Real robots are too expensive to include in a teaching course.",
            "Simulators are always more accurate than real sensors.",
            "A seeded simulator gives identical results everywhere, so answers can be graded fairly.",
            "It removes the need for any programming experience.",
        ],
        answer=2,
        kind="robotics",
        explanation=(
            "Seeding the random number generator makes every sensor reading reproducible "
            "across machines and runs. That determinism is what allows an exercise to "
            "have one correct, automatically checkable answer without physical hardware."
        ),
        reference="lesson.ipynb - Robotics Connection",
    )
)

QUIZ.append(
    quiz(
        question=(
            "In the ROBO-X telemetry controller, why catch `SensorError` and record "
            "`None` instead of letting the exception propagate?"
        ),
        choices=[
            "A failed sensor should degrade the report rather than stop the control loop.",
            "`None` is the physically correct value for a distance reading.",
            "Catching exceptions makes the loop run measurably faster.",
            "Handling the error guarantees the sensor recovers on the next call.",
        ],
        answer=0,
        kind="robotics",
        explanation=(
            "Robotics services are expected to keep operating with degraded "
            "information. Recording which channel failed and continuing preserves "
            "availability, and the caller can still decide the failure is fatal."
        ),
        reference="solution.ipynb - Solution 11",
    )
)

QUIZ.append(
    quiz(
        question="Which function correctly clamps a battery percentage to the range 0-100?",
        choices=[
            "return 100 if value > 100 else value",
            "Two guards returning 0 and 100, then returning value",
            "return min(100, value)",
            "return value % 101",
        ],
        answer=1,
        kind="implementation_choice",
        explanation=(
            "Only option B constrains the lower bound as well as the upper one. "
            "Option C leaves negative values untouched, and option D wraps values "
            "instead of clamping them, which is a different operation altogether."
        ),
        reference="exercises.ipynb - Exercise 4",
    )
)

MINI_PROJECT = {
    "title": "Mini-Project: ROBO-X Boot Diagnostics",
    "brief": (
        "Build a small diagnostics tool that inspects the running Python "
        "environment and prints a readiness report for a robot about to be "
        "deployed."
    ),
    "scenario": (
        "You are the first engineer on shift. The fleet's other services have "
        "started, and you must confirm that the machine you are about to run on "
        "has a usable interpreter before arming the robot."
    ),
    "rationale": (
        "This is the function a robotics team actually needs on day one: a single "
        "command that turns a scattered set of environment facts into an explicit "
        "pass or fail decision."
    ),
    "requirements": [
        "Read the interpreter name and version with the `sys` module.",
        "Report whether the running version satisfies Python 3.12 or newer.",
        "Read and report three configuration values from a small dict.",
        "Return a report dict with a boolean `ready` key and a list of `problems`.",
        "Raise a clear error when a required configuration key is missing.",
    ],
    "constraints": [
        "Standard library only.",
        "No module-level code with side effects; everything goes through functions.",
        "Follow PEP 8 and add docstrings to each public function.",
    ],
    "deliverables": [
        "`diagnostics.py` with the implementation.",
        "`test_diagnostics.py` with at least six assertions.",
        "A short README section explaining the pass/fail decision rules.",
    ],
    "steps": [
        "Sketch the report dict shape and the rules that set `ready`.",
        "Implement `environment_report()` reading only the `sys` module.",
        "Implement `config_report(config)` validating the required keys.",
        "Combine both into `diagnostics(config)` returning the final report.",
        "Write the tests, starting with the happy path.",
        "Add tests for a missing key and for an old Python version.",
    ],
    "expected_behavior": (
        "Running the tool on a correct machine prints 'READY' and returns a "
        "report whose `ready` value is True; on a machine missing configuration it "
        "lists exactly which keys are absent."
    ),
    "acceptance": [
        "Every assertion passes from a clean run.",
        "A missing configuration key produces a specific message, not a bare traceback.",
        "No function exceeds roughly 25 lines.",
        "Every public function has a docstring.",
    ],
    "extensions": [
        "Add a check for available disk space using `shutil.disk_usage`.",
        "Add a `--json` flag that prints the report for machine consumption.",
        "Emit a warning when the interpreter is a nightly build.",
    ],
}

RESEARCH = {
    "question": (
        "How does interpreter start-up time change with the size of the modules "
        "a program imports?"
    ),
    "hypothesis": (
        "Import time grows measurably with the number of modules imported, and "
        "roughly linearly once the module count is above about fifty."
    ),
    "experiment": [
        STEPS(
            [
                "Create three scripts that import 0, 50 and 200 trivial modules.",
                "Run each ten times with `python -X importtime` and capture the totals.",
                "Record the raw milliseconds for every run in the table below.",
                "Repeat on a second machine to check the trend generalises.",
            ]
        ),
    ],
    "data": [
        CODE_CELL(
            "# Record your raw measurements here. One row per run.\n"
            "# Do not invent numbers — copy them from your actual output.\n"
            "#\n"
            "# | modules | run | milliseconds |\n"
            "# |---------|-----|-------------|\n"
            "# | 0       | 1   |             |\n"
            "# | 50      | 1   |             |"
        ),
    ],
    "analysis": [
        MD(
            "Compute the mean and spread for each module count, then plot or tabulate "
            "them. Compare the slope of the 0-to-50 segment with the 50-to-200 "
            "segment."
        ),
    ],
    "result": [
        MD(
            "State whether the hypothesis survived. Report the numbers that decided "
            "it, and explicitly note anything that contradicted your expectation."
        ),
    ],
    "interpretation": [
        MD(
            "Explain the mechanism behind your numbers: why does the cost appear "
            "linear, and which part of import (finding, reading, compiling, executing) "
            "dominates? Name at least two threats to the validity of your result."
        ),
    ],
    "conclusion": [
        MD(
            "Give your verdict, then name the next experiment you would run to test "
            "it more sharply."
        ),
    ],
    "extensions": [
        "Compare the total import time against file size rather than module count.",
        "Measure the effect of a warm operating-system page cache.",
        "Investigate whether `python -OO` changes import time.",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Telemetry Readiness Controller",
    "context": (
        "ROBO-X must publish a telemetry readiness report before it accepts "
        "missions. The report is produced during mobile robot bring-up, on a "
        "machine whose sensor bus may be degraded."
    ),
    "mission": (
        "Implement `process_telemetry(data)` so it reads the requested sensor "
        "channels from the simulator, survives individual sensor failures, and "
        "returns a report the fleet supervisor can act on."
    ),
    "requirements": [
        "Read every channel named in `data`, defaulting to distance, temperature and battery_voltage.",
        "Catch `SensorError` per channel and record `None` rather than aborting.",
        "Return a dict with `readings`, `battery_pct` and a boolean `ok` flag.",
        "Set `ok` to False when any channel failed to produce a value.",
    ],
    "constraints": [
        "No hardware required: use `shared.robo_x_sim`.",
        "Must complete well inside the 10 ms control budget.",
        "Never raise for an unknown channel name; report it as a failed reading.",
    ],
    "interface": "def process_telemetry(data: list | None = None) -> dict:",
    "success_criteria": [
        "Returns `ok` True when every requested channel reads successfully.",
        "Returns `ok` False and a None entry after injecting a sensor fault.",
        "Never raises for an unknown channel name.",
    ],
    "extension": (
        "Add a `retry` argument that re-reads a failed channel up to n times "
        "before recording None, and report the retry count."
    ),
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Establish the interpreter model: source, bytecode, evaluation loop.",
        "Make name binding concrete so later modules can rely on it.",
        "Install the habit of inspecting types before trusting a value.",
    ],
    "misconceptions": [
        [
            "Python is interpreted, therefore simply slow.",
            "CPython compiles to bytecode first; the cost profile is not that of a pure interpreter.",
        ],
        [
            "A variable has a type that is declared once.",
            "Types belong to objects and are checked when the operation runs.",
        ],
        [
            "Naming a variable `list` is only a style issue.",
            "It rebinds the built-in and causes real TypeErrors later in the module.",
        ],
        [
            "A function that prints is equivalent to one that returns.",
            "Returning keeps the logic testable; printing hides it inside the function.",
        ],
    ],
    "difficult_concepts": [
        "Separating syntax errors, raised before execution, from runtime errors.",
        "Seeing a name as a label rather than a fixed container.",
        "Understanding why the main guard exists at all.",
    ],
    "demonstrations": [
        "Run `dis.dis()` live on a one-line function and read the instructions aloud.",
        "Assign to `list` in the REPL, then call `list(...)` and read the TypeError.",
        "Show `sys.executable` differing from the interpreter the student expected.",
    ],
    "discussion": [
        "Which parts of a robot controller would you never write in Python, and why?",
        "If types are checked only at runtime, what could you add to catch problems earlier?",
    ],
    "student_errors": [
        [
            "TypeError where a number was expected",
            "Input arrived from a sensor or file as text and was never converted",
            "Inspect with type() and convert explicitly at the boundary",
        ],
        [
            "IndentationError after editing in another editor",
            "That editor inserted tabs while the file used spaces",
            "Convert the file to spaces on save and enable trim-trailing-whitespace",
        ],
        [
            "Nothing happens when the file is imported",
            "Side effects sit at module level instead of behind the main guard",
            "Wrap side effects in main() and guard the call",
        ],
    ],
    "pacing": (
        "90 minutes of lesson with live demonstrations, then 2 hours of exercises "
        "and the mini-project. Do not rush the REPL demonstration: beginners must "
        "see an error happen before they can read one."
    ),
    "extensions": [
        "Disassemble a loop and count the bytecodes per iteration.",
        "Compare `sys.implementation.cache_tag` across two Python versions.",
    ],
    "assessment": (
        "Grade against rubric.md. Expect weak reasoning on exercises 6 to 10; "
        "the parsing and validation tasks are the real signal of learning."
    ),
    "support": (
        "Provide the first exercise fully worked, and pair students so the "
        "stronger partner explains the type conversion out loud."
    ),
    "extension_fast": (
        "Ask for a one-paragraph design note on where Python should stop and a "
        "compiled language should begin inside a control loop."
    ),
}

RUBRIC = {
    "artifacts": [
        ["exercises.ipynb", "40%", "All 10 exercises implemented and edge-cased."],
        ["mini_project.ipynb", "25%", "Diagnostics tool plus its test suite."],
        ["robotics_challenge.ipynb", "25%", "Telemetry controller degrades safely."],
        ["research.ipynb", "10%", "Real measurements with a defensible conclusion."],
    ],
    "criteria": [
        ["Correctness", "35", "Every documented edge case is handled and tested."],
        ["Code quality", "25", "PEP 8 naming, docstrings, small focused functions."],
        ["Testing", "25", "Assertions cover the happy path, edge cases and failure."],
        ["Reasoning", "15", "Complexity claims are true and explained in writing."],
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
            "Every exercise implemented, every listed edge case tested, and the "
            "telemetry controller degrades safely under an injected fault.",
        ],
        [
            "Merit",
            "Most exercises correct; testing covers the main paths and several edge "
            "cases; reasoning is present but not always justified.",
        ],
        [
            "Pass",
            "Core requirements met on the main paths, but testing is thin or some "
            "edge cases are unhandled.",
        ],
        [
            "Fail",
            "Multiple exercises missing or non-functional, no tests, or edge cases "
            "ignored entirely.",
        ],
    ],
}

TOPIC = topic(
    topic_id="1.1",
    title="Introduction to Python",
    module=1,
    module_title="Getting Started with Python",
    directory="01_introduction_to_python",
    summary=(
        "Where Python came from, how CPython actually runs your code, and why a "
        "language built for readability ended up running most of modern robotics."
    ),
    why_it_matters=(
        "Choosing a language is a long-term commitment. Python powers ROS 2 client "
        "code, most perception tooling, and every fleet dashboard you will ever be "
        "on call for. The interpreter model you learn here also explains every "
        "surprising error message you will meet in this course."
    ),
    objectives=[
        "Explain CPython's four-stage execution pipeline from source to bytecode.",
        "Distinguish name binding from typed assignment, and predict rebinding.",
        "Write a PEP 8 script with a docstring and a main guard.",
        "Read a traceback and locate the failing line and expression.",
        "Explain why robotics orchestration is written in Python.",
    ],
    prerequisites=[
        "No programming experience assumed.",
        "Basic familiarity with installing software and using a terminal.",
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








