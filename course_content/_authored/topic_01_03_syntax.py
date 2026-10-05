"""Topic 1.3 - Python Syntax, Indentation, Comments, and Code Structure.

Hand-authored to the Course Content Standard. The spine: in Python the visual
layout of a program *is* part of its grammar, so structure and appearance can
never drift apart.
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
        "Most languages treat whitespace as insignificant: you may indent or not "
        "indent, and the meaning is carried by braces or keywords. Python inverts "
        "this. **Indentation is the grammar.** A suite of statements is defined by "
        "their common indentation, and the compiler rejects any file in which the "
        "indentation does not describe a consistent tree. The consequence is that a "
        "programmer reading your code sees the same structure the interpreter sees, "
        "with no chance of the two disagreeing."
    ),
    MD(
        "The practical rule is simply four spaces per nesting level, consistently, "
        "everywhere. Python does not require four spaces - any consistent width "
        "parses - but four spaces is the PEP 8 convention, and mixing tabs with "
        "spaces is rejected outright because the width of a tab depends on the "
        "reader. Editors can therefore re-indent a file mechanically and produce the "
        "same structure the author intended."
    ),
    CODE_CELL(
        "def report(battery_pct: float) -> str:\n"
        "    if battery_pct < 20:\n"
        "        verdict = 'LOW'\n"
        "    elif battery_pct < 50:\n"
        "        verdict = 'MEDIUM'\n"
        "    else:\n"
        "        verdict = 'OK'\n"
        "    return verdict\n"
        "\n"
        "\n"
        "for level in (10, 35, 90):\n"
        "    print(f'{level:>3}% -> {report(level)}')"
    ),
    MD(
        "Comments are for the reader and are discarded entirely by the parser. A "
        "comment begins with `#` and runs to the end of the line. Docstrings are "
        "different: they are ordinary string expressions placed as the first "
        "statement of a module, class or function, which is why they can be read "
        "back at runtime with `__doc__`. Comments answer *why*; docstrings answer "
        "*what*."
    ),
    CODE_CELL(
        "# A comment: explains why the threshold is what it is.\n"
        "LOW_BATTERY_PCT = 20   # matches the fleet safety policy\n"
        "\n"
        "\n"
        "def verdict(pct: float) -> str:\n"
        "    \"\"\"Return OK, MEDIUM or LOW for a battery percentage.\n"
        "\n"
        "    This is a docstring: it is a real object attached to the function,\n"
        "    retrievable at runtime and visible to help() and type checkers.\n"
        "    \"\"\"\n"
        "    return 'LOW' if pct < LOW_BATTERY_PCT else 'OK'\n"
        "\n"
        "\n"
        "print(verdict.__doc__.splitlines()[0])\n"
        "print('docstring is a', type(verdict.__doc__).__name__)"
    ),
    NOTE(
        "Comments are not free",
        "Because the parser discards them, a comment can drift out of date without "
        "any test failing. If code disagrees with its comment, delete the comment and "
        "write better code.",
    ),
]

LESSON["formal_theory"] = [
    MD(
        "The grammar describes an indented block as a **suite**: a sequence of simple "
        "statements followed by either a nested suite or a colon and nothing. Formally, "
        "a header line ends with a colon and its suite is everything indented further "
        "than the header. That is the whole rule, and every block form in the language "
        "- `if`, `for`, `while`, `def`, `class`, `with`, `match` - obeys it."
    ),
    EQUATION(
        "header ':' NEWLINE INDENT statement+ DEDENT"
    ),
    STEPS(
        [
            "The **lexer** produces INDENT and DEDENT tokens when the indentation of a "
            "line increases or decreases relative to the previous one.",
            "The **parser** accepts a suite only after such a token, so inconsistent "
            "indentation is rejected before a single statement runs.",
            "The compiler records the resulting nesting in a code object, which is why "
            "`inspect` and `dis` can report line numbers and nesting later.",
        ]
    ),
    CODE_CELL(
        "import dis\n"
        "\n"
        "\n"
        "def verdict(pct):\n"
        "    if pct < 20:\n"
        "        return 'LOW'\n"
        "    return 'OK'\n"
        "\n"
        "\n"
        "code = verdict.__code__\n"
        "print('first line :', code.co_firstlineno)\n"
        "print('constants  :', code.co_consts)"
    ),
    TABLE(
        ["Construct", "Header ends with", "Suite is"],
        [
            ["`if` / `elif` / `else`", "colon", "the indented block that follows"],
            ["`for` / `while`", "colon", "the indented block that follows"],
            ["`def` / `class`", "colon", "the indented block that follows"],
            ["`with`", "colon", "the indented block that follows"],
            ["Simple statement", "no colon", "the single statement on the line"],
        ],
    ),
]

LESSON["syntax"] = [
    MD(
        "The surface syntax is small on purpose. One statement per line, four-space "
        "indentation, `#` for comments, and a colon to open a block."
    ),
    CODE_CELL(
        "# canonical structure\n"
        "LOW_BATTERY_PCT = 20\n"
        "\n"
        "\n"
        "def verdict(pct: float) -> str:\n"
        "    \"\"\"Return a battery verdict.\"\"\"\n"
        "    if pct < LOW_BATTERY_PCT:\n"
        "        return 'LOW'\n"
        "    return 'OK'"
    ),
    MD("The anti-pattern - legal Python, but it fights the language:"),
    CODE(
        "pct = 10; verdict = 'LOW'      # packed onto one line with a semicolon\n"
        "if pct < 20: print(verdict)    # inline body hides the block\n"
        "\tprint('tab indent')            # a tab, not four spaces",
        lang="text",
    ),
    WARN(
        "Semicolons and one-liners",
        "Every semicolon in real code is a line the reader must mentally split again. "
        "Use them in a REPL for brevity, not in a file.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - continuing a statement across lines.**"),
    CODE_CELL(
        "message = (\n"
        "    'ROBO-X '\n"
        "    'ready'\n"
        ")\n"
        "\n"
        "coordinates = (12.0,\n"
        "               3.5)\n"
        "\n"
        "print(message)\n"
        "print(coordinates)"
    ),
    MD(
        "Inside brackets a line break is insignificant, so a long call or literal can "
        "be wrapped freely. Outside brackets you need an explicit backslash, which is "
        "almost always a sign the line should be restructured instead."
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "Wrapping a long call chain so that each argument sits on its own line keeps "
        "diff small and readable. This is the formatting that black produces."
    ),
    CODE_CELL(
        "def send(robot_id: str, channel: str, value: float, *, timeout: float = 1.0) -> str:\n"
        "    return f'{robot_id}:{channel}={value}@{timeout}s'\n"
        "\n"
        "\n"
        "print(send(\n"
        "    'rover-01',\n"
        "    'temperature',\n"
        "    22.5,\n"
        "    timeout=2.5,\n"
        "))"
    ),
    TIP(
        "Trailing commas",
        "A trailing comma inside brackets lets you add one item per line and keeps the "
        "formatter from collapsing the call back onto a single long line.",
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "Because comments and docstrings survive into the compiled code object as "
        "constants, the parser can be asked what a source file contains without "
        "executing it. That is how documentation generators and linters work."
    ),
    CODE_CELL(
        "import ast\n"
        "\n"
        "\n"
        "source = '''\n"
        "def send(robot_id, channel):\n"
        "    \"\"\"Publish one reading.\"\"\"\n"
        "    return robot_id, channel\n"
        "'''\n"
        "\n"
        "tree = ast.parse(source)\n"
        "func = tree.body[0]\n"
        "print('name  :', func.name)\n"
        "print('args  :', [a.arg for a in func.args.args])\n"
        "print('doc   :', ast.get_docstring(func))"
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "Below is a complete utility: a parser for indented log blocks. It is the "
        "shape of code you would write if a robot emitted structured, indented "
        "diagnostics and you needed them as data."
    ),
    CODE_CELL(
        "\"\"\"parse_blocks.py - turn an indented log into nested dictionaries.\"\"\"\n"
        "from __future__ import annotations\n"
        "\n"
        "def _width(line: str) -> int:\n"
        "    return len(line) - len(line.lstrip(' '))\n"
        "\n"
        "\n"
        "def parse_blocks(text: str) -> list[dict]:\n"
        "    \"\"\"Parse '  ' indented log lines into a tree of dicts.\n"
        "\n"
        "    Each leaf line becomes {'text': ...} keyed by indentation depth.\n"
        "    Blank lines and '#' comments are ignored.\n"
        "    \"\"\"\n"
        "    roots: list[dict] = []\n"
        "    stack: list[tuple[int, dict]] = []\n"
        "    for raw in text.splitlines():\n"
        "        if not raw.strip() or raw.lstrip().startswith('#'):\n"
        "            continue\n"
        "        width = _width(raw)\n"
        "        node: dict = {'text': raw.strip()}\n"
        "        while stack and stack[-1][0] >= width:\n"
        "            stack.pop()\n"
        "        if stack:\n"
        "            stack[-1][1].setdefault('children', []).append(node)\n"
        "        else:\n"
        "            roots.append(node)\n"
        "        stack.append((width, node))\n"
        "    return roots"
    ),
    MD(
        "The algorithm is a single pass with an explicit stack. Each line pops every "
        "open level whose indentation is not shallower, then attaches the new node to "
        "whatever remains on top. That is the same idea the interpreter itself uses "
        "to turn INDENT and DEDENT tokens into nested blocks."
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "The docstring states the contract before any code, so a reader knows what "
            "the function returns without reading the body.",
            "`_width` counts leading spaces only; `lstrip(' ')` with an explicit "
            "character avoids surprising behaviour on tab characters.",
            "`roots` collects top-level nodes; `stack` holds (indent, node) pairs for "
            "the levels currently open.",
            "Blank lines and comment lines are skipped *before* any width is computed, "
            "so a comment at column zero cannot corrupt the tree.",
            "The `while stack and stack[-1][0] >= width` loop closes every level that "
            "is not shallower than the new line - this is the dedent operation.",
            "Attaching to `stack[-1][1]` nests the node; otherwise it starts a new root.",
            "Pushing the new node keeps the invariant that the stack mirrors the open "
            "blocks, which is what makes one pass sufficient.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - mixing tabs and spaces inside one block.**"),
    CODE(
        "for i in range(2):\n"
        "\tif i:\n"
        "            print(i)      # TabError / inconsistent use of tabs",
        lang="text",
    ),
    MD("**Mistake 2 - an inline body after a colon.**"),
    CODE(
        "if ready: print('go')   # legal, but the block is invisible\n"
        "\n"
        "if ready:\n"
        "    print('go')       # the block is obvious at a glance",
        lang="text",
    ),
    MD("**Mistake 3 - a comment that contradicts the code.**"),
    CODE(
        "# decrement the counter before use   <- left over from an older version\n"
        "battery_pct -= 1",
        lang="text",
    ),
    MD("**Mistake 4 - using a docstring where a comment belongs.**"),
    CODE(
        "def send(value):\n"
        "    '''Calls the actuator.'''   # docstring: public API documentation\n"
        "    # actuator.publish(value)    # comment: disabled for safety review\n"
        "    return value",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "Structure bugs are easy to locate because Python refuses to run the file. "
        "Read the traceback from the bottom: the final line names the problem, and the "
        "line number is where the parser gave up."
    ),
    CODE_CELL(
        "import ast\n"
        "\n"
        "broken = 'def f():\\n    return 1\\n   return 2\\n'\n"
        "try:\n"
        "    ast.parse(broken)\n"
        "except SyntaxError as exc:\n"
        "    print('problem :', exc.msg)\n"
        "    print('line     :', exc.lineno)\n"
        "    print('offset   :', exc.offset)"
    ),
    MD(
        "Turning an unexpected `IndentationError` into an `unexpected indent` is almost "
        "always a matter of deleting a block header or un-indenting a line by hand. "
        "Editors can re-indent a whole selection mechanically, which is safer than "
        "adjusting whitespace one line at a time."
    ),
    NOTE(
        "Read-only checks",
        "`python -m py_compile file.py` and `ast.parse(source)` both validate "
        "structure without executing anything, so they are safe to run against code "
        "you do not trust.",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Indent with four spaces; never mix tabs and spaces.",
            "One statement per line; reserve semicolons for the REPL.",
            "Put a colon at the end of a block header and nothing else.",
            "Use a docstring on every module, class and public function.",
            "Use `#` comments for the reason a decision was made, not for restating code.",
            "Wrap long lines at around 88 characters, one argument per line.",
            "Prefer implicit line joining inside brackets over explicit backslashes.",
            "Re-indent mechanically rather than by hand when fixing whitespace.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "Indentation has no direct runtime cost: the parser discards whitespace after "
        "building the tree, so a deeply indented function is no slower than a flat one. "
        "What does cost is nesting *depth* in the algorithms you write. A recursive "
        "function that descends one level per frame is bounded by Python's recursion "
        "limit, which defaults to 1000, and a deeply nested data structure walked "
        "recursively will hit it. In this course you will meet recursion in Module 4 "
        "and iterative alternatives in Module 2, so it is worth forming the habit early: "
        "when a structure has an obvious depth, write a loop with an explicit stack, as "
        "`parse_blocks` does, rather than a recursive descent."
    ),
    MD(
        "The other measurable cost is re-parsing. `ast.parse` on a large source file is "
        "not free, so a tool that parses the same file repeatedly should cache the tree "
        "rather than re-parsing. In practice this rarely matters because tools run once "
        "per invocation, but it is the right instinct for anything long-lived."
    ),
]

LESSON["pythonic_approaches"] = [
    MD("Splitting text: explicit loop versus the method that says what it means."),
    CODE_CELL(
        "text = 'alpha\\nbeta\\ngamma'\n"
        "\n"
        "# before: manual scanning for the newline character\n"
        "lines, current = [], ''\n"
        "for ch in text:\n"
        "    if ch == '\\n':\n"
        "        lines.append(current)\n"
        "        current = ''\n"
        "    else:\n"
        "        current += ch\n"
        "if current:\n"
        "    lines.append(current)\n"
        "\n"
        "# after: the intent, stated directly\n"
        "print(text.splitlines())\n"
        "print(lines == text.splitlines())"
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "Robot diagnostics are almost always emitted as indented text so that a human "
        "can read them, and a supervisor process frequently needs the same information "
        "as data. The parser from the walkthrough is exactly that bridge, and it runs "
        "against the simulator's own status output in the exercise that follows."
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
        "log = (f\"robot {state['name']}\\n\"\n"
        "       f\"    battery {state['battery_pct']:.1f}%\\n\"\n"
        "       f\"    position {state['position']}\\n\")\n"
        "print(log)"
    ),
]

LESSON["engineering_example"] = [
    MD(
        "A small formatter used by every command-line tool in the course: it rejects "
        "mixed indentation and reports the offending lines rather than guessing."
    ),
    CODE_CELL(
        "def check_indentation(source: str, width: int = 4) -> list[str]:\n"
        "    problems: list[str] = []\n"
        "    for number, line in enumerate(source.splitlines(), start=1):\n"
        "        if not line.strip():\n"
        "            continue\n"
        "        if '\\t' in line[:len(line) - len(line.lstrip())]:\n"
        "            problems.append(f'line {number}: tab in indentation')\n"
        "            continue\n"
        "        lead = len(line) - len(line.lstrip(' '))\n"
        "        if lead % width:\n"
        "            problems.append(f'line {number}: indent {lead} is not a multiple of {width}')\n"
        "    return problems\n"
        "\n"
        "\n"
        "sample = 'def f():\\n    return 1\\n'\n"
        "print(check_indentation(sample) or 'indentation OK')"
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Write a four-line function with a docstring and a nested `if` block.",
            "Use `ast.parse` on your own function and print the docstring back.",
            "Deliberately break the indentation and read the SyntaxError message.",
            "Write `strip_comments(line)` that removes a trailing `#` comment and "
            "returns the code part, stripping trailing whitespace.",
        ]
    ),
    CODE_CELL(
        "import ast\n"
        "\n"
        "\n"
        "def strip_comments(line: str) -> str:\n"
        "    \"\"\"Remove a trailing '#' comment from a line of code.\"\"\"\n"
        "    code = line.split('#', 1)[0]\n"
        "    return code.rstrip()\n"
        "\n"
        "\n"
        "print(repr(strip_comments('x = 1  # set the reading  # not a string')))\n"
        "tree = ast.parse('def f():\\n    \"\"\"Doc.\"\"\"\\n    return 1\\n')\n"
        "print('docstring:', ast.get_docstring(tree.body[0]))"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: indentation is the syntax tree, drawn.** Every other language "
        "keeps structure somewhere you must consult - braces, keywords, a separate "
        "declaration. Python draws the structure in the left margin, so the file you "
        "read *is* the parse tree you are about to execute. When in doubt, re-indent "
        "the selection and the intended structure appears."
    ),
    TABLE(
        ["You write", "The interpreter receives"],
        [
            ["Four spaces at the start of a line", "An INDENT token"],
            ["A line back at the outer level", "A DEDENT token"],
            ["`if ready:`", "A header, a colon, then a suite"],
            ["`# note`", "Nothing at all - it is discarded"],
            ["`\"\"\"Doc\"\"\"` first in a function", "A string expression bound to `__doc__`"],
        ],
    ),
]

TERMS = [
    ["Indentation", "Leading whitespace that defines block structure in Python."],
    ["Suite", "The set of statements belonging to one block header."],
    ["Header", "The line ending in a colon that opens a block."],
    ["Block", "A header plus its indented suite."],
    ["Comment", "Text after `#`, discarded entirely by the parser."],
    ["Docstring", "A string literal as the first statement of a module, class or function."],
    ["Implicit joining", "A line break inside brackets, which the parser ignores."],
    ["Explicit joining", "A trailing backslash, which continues the logical line."],
    ["PEP 8", "The Python style guide, which mandates four-space indentation."],
    ["TabError", "Raised when tabs and spaces are mixed within one block."],
]

LESSON["summary"] = [
    MD(
        "Python's syntax is defined by layout. A header ending in a colon is followed by "
        "a suite of statements indented further than the header; the lexer emits "
        "INDENT and DEDENT tokens as the left margin moves, and the parser builds the "
        "tree from them. Because indentation is meaningful, the appearance of a program "
        "and its structure cannot disagree, which is the single most important "
        "consequence of the language's design."
    ),
    MD(
        "Comments and docstrings occupy different roles and are implemented "
        "differently. A comment is discarded by the parser before anything is built, so "
        "it exists purely for a human reader and can rot silently. A docstring is an "
        "ordinary string expression placed first in a module, class or function; it "
        "survives into the compiled code object and is retrievable through `__doc__`, "
        "which is why tooling can read documentation without running your code."
    ),
    MD(
        "For structure that is long or machine-oriented, prefer implicit line joining "
        "inside brackets and let the layout show the shape of the data. One statement "
        "per line keeps diffs honest. And when Python raises `IndentationError` or "
        "`TabError`, believe the parser: it has already proved your file's structure "
        "does not describe the tree you meant, and the fastest fix is usually a "
        "mechanical re-indent rather than an edit by hand."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "Indentation is grammar, not decoration.",
            "A block is a colon-terminated header plus a more-indented suite.",
            "Four spaces per level, consistently, never mixed with tabs.",
            "Comments are discarded; docstrings are real objects on `__doc__`.",
            "Inside brackets, line breaks are free; outside, avoid backslashes.",
            "One statement per line keeps diffs readable and review cheap.",
            "Structure bugs are parse errors, so they surface before any code runs.",
            "Use `ast.parse` to inspect code without executing it.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "[PEP 8 - Style Guide](https://peps.python.org/pep-0008/) - indentation, "
            "line length and naming.",
            "[The Python reference: compound statements](https://docs.python.org/3/reference/compound_stmts.html)",
            "[tokenize - tokenize Python source](https://docs.python.org/3/library/tokenize.html) - "
            "shows INDENT and DEDENT directly.",
            "[ast - Abstract syntax trees](https://docs.python.org/3/library/ast.html)",
            "[black - the uncompromising formatter](https://black.readthedocs.io/) - "
            "settles layout arguments once.",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Strip a trailing comment from a line",
        difficulty="MEDIUM",
        learning_objectives=["Remove comments from code.", "Handle strings that contain '#'."],
        concepts_tested=["strings", "comments", "parsing"],
        problem_statement=(
            "Write `strip_comments(line)` returning the code portion of a line with "
            "any `#` comment removed and trailing whitespace stripped. A `#` inside a "
            "string literal must be preserved."
        ),
        requirements=["Return the code part only.", "Strip trailing whitespace from the result."],
        constraints=["Standard library only.", "Do not use ast for this task."],
        input_description="A single line of source code.",
        expected_output="The line without its comment.",
        example_input="strip_comments(\"x = 1  # set reading\")",
        example_output="'x = 1'",
        edge_cases=["A line with no comment is returned stripped.", "'#' inside a string is kept.", "A line that is only a comment becomes ''."],
        hints=["Scan the characters and track whether you are inside quotes."],
        success_criteria=["Removes the trailing comment.", "Preserves '#' inside quotes."],
        optional_extension="Return None when the line has no comment at all.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Measure indentation width",
        difficulty="MEDIUM",
        learning_objectives=["Count leading whitespace.", "Distinguish tabs from spaces."],
        concepts_tested=["strings", "indentation", "counting"],
        problem_statement=(
            "Write `indent_width(line)` returning the number of leading space "
            "characters, or -1 when the indentation contains a tab. Blank or "
            "whitespace-only lines return 0."
        ),
        requirements=["Count spaces only.", "Return -1 for any tab in the indentation."],
        constraints=["Do not strip the line before measuring."],
        input_description="A single line of source code.",
        expected_output="An integer width.",
        example_input="indent_width('    return 1')",
        example_output="4",
        edge_cases=["Empty line returns 0.", "A leading tab returns -1.", "Trailing whitespace is irrelevant."],
        hints=["Compare the length of the line with the length of its lstripped form."],
        success_criteria=["Returns 4 for the example.", "Returns -1 for a tab-indented line."],
        optional_extension="Also return the number of trailing whitespace characters.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Normalise a block to a fixed indent width",
        difficulty="MEDIUM",
        learning_objectives=["Rewrite indentation.", "Preserve relative nesting."],
        concepts_tested=["indentation", "strings", "mapping"],
        problem_statement=(
            "Write `reindent(lines, width=4)` that rewrites each line so its leading "
            "whitespace is the original nesting depth multiplied by `width`. Preserve "
            "the content after the indentation exactly."
        ),
        requirements=["Derive depth from the original leading-space count.", "Blank lines stay empty."],
        constraints=["Never use tabs in the output."],
        input_description="A list of source lines.",
        expected_output="A list of re-indented lines.",
        example_input="reindent(['if ready:', '  return 1'])",
        example_output="['if ready:', '    return 1']",
        edge_cases=["Empty input.", "Already-correct indentation.", "Blank and whitespace-only lines."],
        hints=["Round the original width up to the nearest depth, then multiply by width."],
        success_criteria=["Doubles the indent in the example.", "Blank lines stay blank."],
        optional_extension="Preserve a blank line between every pair of top-level blocks.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Build a multi-line banner",
        difficulty="MEDIUM",
        learning_objectives=["Assemble a readable string.", "Wrap a literal across lines."],
        concepts_tested=["strings", "f-strings", "implicit joining"],
        problem_statement=(
            "Write `banner(robot, level)` returning three lines: the robot name, the "
            "level, and a READY line, each right-aligned to twelve characters."
        ),
        requirements=["Use implicit line joining inside parentheses.", "Pad with the format spec."],
        constraints=["No explicit backslashes."],
        input_description="A robot name string and a level string.",
        expected_output="A three-line string.",
        example_input="banner('rover-01', 'M1')",
        example_output="'    rover-01\\n          M1\\n       READY'",
        edge_cases=["Names longer than twelve characters are not truncated.", "Empty level still prints."],
        hints=["Wrap the f-string in parentheses and break it between the three parts."],
        success_criteria=["Exactly three lines.", "Each line is right-aligned to twelve."],
        optional_extension="Add a trailing line with the current date.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Count code, comment and blank lines",
        difficulty="MEDIUM",
        learning_objectives=["Classify lines.", "Use tokenize or string logic."],
        concepts_tested=["tokenize", "strings", "classification"],
        problem_statement=(
            "Write `line_census(source)` returning a dict with `code`, `comment`, "
            "`blank` and `total` counts. A line is blank when it is whitespace only, "
            "and comment when its first non-space character is `#`."
        ),
        requirements=["Count every line exactly once.", "Return integers."],
        constraints=["Blank and comment lines are mutually exclusive."],
        input_description="A multi-line source string.",
        expected_output="A dict with the four counts.",
        example_input="line_census('# note\\nx = 1\\n\\n')",
        example_output="{'code': 1, 'comment': 1, 'blank': 1, 'total': 3}",
        edge_cases=["Empty input gives all zeros.", "A line with code then a comment counts as code.", "Trailing newline does not create an extra line."],
        hints=["Strip each line and branch on whether it is empty or starts with '#'."],
        success_criteria=["Counts match the example.", "total equals the sum of the three."],
        optional_extension="Ignore docstrings when counting code lines.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Report indentation problems",
        difficulty="HARD",
        learning_objectives=["Validate style.", "Report precisely, never guess."],
        concepts_tested=["indentation", "validation", "strings"],
        problem_statement=(
            "Write `check_indentation(source, width=4)` returning a list of problem "
            "strings, one per offending line, each naming the 1-based line number. "
            "Flag a tab in the indentation and any indent that is not a multiple of "
            "`width`."
        ),
        requirements=["Never raise on bad input.", "Message format: 'line N: reason'."],
        constraints=["Check at most one problem per line."],
        input_description="Source text and an indent width.",
        expected_output="A list of problem descriptions.",
        example_input="check_indentation('if ready:\\n  return 1\\n')",
        example_output="[\"line 2: indent 2 is not a multiple of 4\"]",
        edge_cases=["Clean source gives an empty list.", "A tab-indented line is flagged once.", "Blank lines never produce a problem."],
        hints=["Reuse indent_width from exercise 2 rather than duplicating the logic."],
        success_criteria=["Flags the 2-space line in the example.", "Returns [] for clean source."],
        optional_extension="Also flag lines indented deeper than the previous non-blank line plus one level.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Parse an indented log into a tree",
        difficulty="HARD",
        learning_objectives=["Use an explicit stack.", "Build nested structure from text."],
        concepts_tested=["stacks", "indentation", "dicts"],
        problem_statement=(
            "Write `parse_blocks(text)` returning a list of nested dictionaries, one "
            "per top-level line, where each node has a `text` key and optionally a "
            "`children` list. Indentation determines nesting; blank lines and `#` "
            "comment lines are ignored."
        ),
        requirements=["One pass, explicit stack.", "Siblings at equal depth share a parent."],
        constraints=["Do not use recursion.", "Never raise on ragged input."],
        input_description="A multi-line string of space-indented text.",
        expected_output="A list of dicts with 'text' and nested 'children'.",
        example_input="parse_blocks('a\\n  b\\n  c\\nd')",
        example_output="[{'text': 'a', 'children': [{'text': 'b'}, {'text': 'c'}]}, {'text': 'd'}]",
        edge_cases=["Empty input gives [].", "Deeper jumps in indentation still attach to the last open level.", "Comment lines vanish entirely."],
        hints=["Pop while the top of the stack is not shallower than the new line."],
        success_criteria=["Matches the example exactly.", "Empty input gives []."],
        optional_extension="Attach a 1-based source line number to each node.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Extract docstrings without importing",
        difficulty="HARD",
        learning_objectives=["Use the ast module.", "Read code as data."],
        concepts_tested=["ast", "docstrings", "dicts"],
        problem_statement=(
            "Write `extract_docstrings(source)` returning a dict mapping each function "
            "name to its docstring, using ast so the module is never executed. "
            "Functions without a docstring map to None."
        ),
        requirements=["Use ast.parse and ast.get_docstring.", "Return top-level functions only."],
        constraints=["Never import or exec the source."],
        input_description="A Python source string.",
        expected_output="A dict of name to docstring or None.",
        example_input="extract_docstrings('def f():\\n    \"\"\"Doc.\"\"\"\\n')",
        example_output="{'f': 'Doc.'}",
        edge_cases=["A function with no docstring maps to None.", "Source with no functions gives {}.", "Invalid source raises SyntaxError."],
        hints=["Walk tree.body and filter for ast.FunctionDef."],
        success_criteria=["Extracts the docstring in the example.", "Returns {} when there are no functions."],
        optional_extension="Include the line number of each definition.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Split semicolon-packed statements safely",
        difficulty="HARD",
        learning_objectives=["Parse statements.", "Respect string literals."],
        concepts_tested=["parsing", "strings", "tokenize"],
        problem_statement=(
            "Write `split_statements(line)` returning the individual simple statements "
            "on a line, split on semicolons that are not inside quotes. Raise "
            "ValueError when the line contains a compound statement such as `if`."
        ),
        requirements=["Ignore semicolons inside string literals.", "Strip each statement."],
        constraints=["Do not use exec or eval."],
        input_description="A single source line.",
        expected_output="A list of statement strings.",
        example_input="split_statements(\"a = 1; b = 2\")",
        example_output="['a = 1', 'b = 2']",
        edge_cases=["Trailing semicolon produces no empty statement.", "';' inside a string is preserved.", "A line starting with 'if' raises ValueError."],
        hints=["Track quote state character by character."],
        success_criteria=["Splits the example correctly.", "Raises ValueError for a compound statement."],
        optional_extension="Preserve the indentation of each split statement.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Produce a module outline",
        difficulty="HARD",
        learning_objectives=["Walk an AST.", "Report structure as data."],
        concepts_tested=["ast", "tuples", "reporting"],
        problem_statement=(
            "Write `outline(source)` returning a list of `(kind, name, line, "
            "summary)` tuples for every top-level function and class, where `summary` "
            "is the first line of the docstring or an empty string."
        ),
        requirements=["kind is 'def' or 'class'.", "line is the 1-based definition line."],
        constraints=["Never execute the source.", "Preserve definition order."],
        input_description="A Python source string.",
        expected_output="A list of tuples in source order.",
        example_input="outline('def f():\\n    \"\"\"One.\\n    More.\"\"\"\\n')",
        example_output="[('def', 'f', 1, 'One.')]",
        edge_cases=["A class with no docstring gives an empty summary.", "Source with no definitions gives []."],
        hints=["node.lineno gives the 1-based line; ast.get_docstring gives the full docstring."],
        success_criteria=["Matches the example exactly.", "Handles a class as well as a function."],
        optional_extension="Include nested functions of classes at depth 1.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "def strip_comments(line: str) -> str:\n"
            "    quote = None\n"
            "    previous = ''\n"
            "    for index, ch in enumerate(line):\n"
            "        if quote:\n"
            "            if ch == quote and previous != '\\\\':\n"
            "                quote = None\n"
            "        elif ch in ('\"', \"'\"):\n"
            "            quote = ch\n"
            "        elif ch == '#':\n"
            "            return line[:index].rstrip()\n"
            "        previous = ch\n"
            "    return line.rstrip()"
        ),
        explanation=(
            "The scan tracks the active quote character so a '#' inside a string is "
            "never treated as a comment. Tracking the previous character distinguishes "
            "an escaped quote from a closing one, and returning the prefix keeps the "
            "code that precedes the comment intact."
        ),
        complexity="Time O(n) in the line length; space O(1) beyond the result.",
        edge_cases="A comment-only line returns an empty string; a trailing backslash escape is respected.",
        alternative_approaches="tokenize handles this correctly but requires a full source context.",
        testing="assert strip_comments('x = 1  # note') == 'x = 1'\nassert strip_comments(\"s = '# not a comment'\") == \"s = '# not a comment'\"\nassert strip_comments('# only') == ''",
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def indent_width(line: str) -> int:\n"
            "    stripped = line.lstrip()\n"
            "    if not stripped:\n"
            "        return 0\n"
            "    lead = line[:len(line) - len(stripped)]\n"
            "    if '\\t' in lead:\n"
            "        return -1\n"
            "    return len(lead)"
        ),
        explanation=(
            "Comparing lengths recovers the indentation without mutating the line. "
            "The tab check comes first so a mixed line reports -1 rather than a "
            "misleading count, and the blank case is handled before any counting so "
            "whitespace-only lines never produce a width."
        ),
        complexity="Time O(n) in the line length; space O(n) for the stripped copy.",
        edge_cases="A whitespace-only line returns 0; a line with trailing tabs is unaffected.",
        alternative_approaches="re.match(r'^[ ]*', line) avoids creating the stripped copy.",
        testing="assert indent_width('    return 1') == 4\nassert indent_width('\\treturn 1') == -1\nassert indent_width('   ') == 0",
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "def reindent(lines, width: int = 4) -> list[str]:\n"
            "    depth_of = {}\n"
            "    for line in lines:\n"
            "        if not line.strip():\n"
            "            continue\n"
            "        lead = len(line) - len(line.lstrip(' '))\n"
            "        depth_of.setdefault(lead, len(depth_of))\n"
            "    out = []\n"
            "    for line in lines:\n"
            "        if not line.strip():\n"
            "            out.append('')\n"
            "            continue\n"
            "        lead = len(line) - len(line.lstrip(' '))\n"
            "        out.append(' ' * (depth_of[lead] * width) + line.lstrip(' '))\n"
            "    return out"
        ),
        explanation=(
            "The first pass assigns each distinct original indent a depth, in the "
            "order the widths are first seen, so nesting is preserved without counting "
            "block headers. The second pass rewrites each line using that depth, which "
            "means input that is already correct comes back unchanged."
        ),
        complexity="Time O(n) in the number of lines; space O(k) for k distinct widths.",
        edge_cases="Blank lines become empty strings; already-correct input is unchanged.",
        alternative_approaches="Walking the AST gives exact nesting but requires valid input.",
        testing="assert reindent(['if ready:', '  return 1']) == ['if ready:', '    return 1']\nassert reindent(['a', '    b']) == ['a', '    b']",
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "def banner(robot: str, level: str) -> str:\n"
            "    return (\n"
            "        f'{robot:>12}\\n'\n"
            "        f'{level:>12}\\n'\n"
            "        f\"{'READY':>12}\"\n"
            "    )"
        ),
        explanation=(
            "The whole banner is one expression wrapped in parentheses, so the three "
            "parts sit on separate source lines without any concatenation operator. "
            "The '>12' format spec right-aligns each field, which is what produces the "
            "fixed-width column layout."
        ),
        complexity="Time O(n) in the input lengths; space O(n).",
        edge_cases="Names longer than twelve characters widen the column rather than truncating.",
        alternative_approaches="A triple-quoted f-string is shorter but keeps the newlines in the literal.",
        testing="assert banner('rover-01', 'M1').splitlines() == ['    rover-01', '          M1', '       READY']\nassert len(banner('r', 'M1').splitlines()) == 3",
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "def line_census(source: str) -> dict:\n"
            "    counts = {'code': 0, 'comment': 0, 'blank': 0}\n"
            "    lines = source.splitlines()\n"
            "    for line in lines:\n"
            "        stripped = line.strip()\n"
            "        if not stripped:\n"
            "            counts['blank'] += 1\n"
            "        elif stripped.startswith('#'):\n"
            "            counts['comment'] += 1\n"
            "        else:\n"
            "            counts['code'] += 1\n"
            "    counts['total'] = len(lines)\n"
            "    return counts"
        ),
        explanation=(
            "Branching on the stripped form makes the three categories mutually "
            "exclusive, so every line increments exactly one counter. Computing total "
            "from the line list rather than by summing keeps the invariant total equals "
            "the sum of the parts even when the input is empty."
        ),
        complexity="Time O(n) in the number of lines; space O(1).",
        edge_cases="A trailing newline does not create an extra line because splitlines handles it.",
        alternative_approaches="tokenize distinguishes comments precisely but treats docstrings as strings, not comments.",
        testing="assert line_census('# note\\nx = 1\\n\\n') == {'code': 1, 'comment': 1, 'blank': 1, 'total': 3}\nassert line_census('')['total'] == 0",
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "def check_indentation(source: str, width: int = 4) -> list[str]:\n"
            "    problems: list[str] = []\n"
            "    for number, line in enumerate(source.splitlines(), start=1):\n"
            "        if not line.strip():\n"
            "            continue\n"
            "        lead = line[:len(line) - len(line.lstrip())]\n"
            "        if '\\t' in lead:\n"
            "            problems.append(f'line {number}: tab in indentation')\n"
            "            continue\n"
            "        spaces = len(lead)\n"
            "        if spaces % width:\n"
            "            problems.append(\n"
            "                f'line {number}: indent {spaces} is not a multiple of {width}'\n"
            "            )\n"
            "    return problems"
        ),
        explanation=(
            "The continue after the tab check enforces at most one problem per line, "
            "which keeps the report unambiguous. Blank lines are skipped before any "
            "measurement so trailing whitespace at the end of a file never produces "
            "noise."
        ),
        complexity="Time O(n) in the number of lines; space O(p) for p problems.",
        edge_cases="Clean source returns an empty list; a tab line is reported only once.",
        alternative_approaches="Delegating to indent_width from exercise 2 keeps the measurement in one place.",
        testing="assert check_indentation('if ready:\\n  return 1\\n') == [\"line 2: indent 2 is not a multiple of 4\"]\nassert check_indentation('def f():\\n    return 1\\n') == []",
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "def parse_blocks(text: str) -> list[dict]:\n"
            "    roots: list[dict] = []\n"
            "    stack: list[tuple[int, dict]] = []\n"
            "    for raw in text.splitlines():\n"
            "        if not raw.strip() or raw.lstrip().startswith('#'):\n"
            "            continue\n"
            "        width = len(raw) - len(raw.lstrip(' '))\n"
            "        node: dict = {'text': raw.strip()}\n"
            "        while stack and stack[-1][0] >= width:\n"
            "            stack.pop()\n"
            "        if stack:\n"
            "            stack[-1][1].setdefault('children', []).append(node)\n"
            "        else:\n"
            "            roots.append(node)\n"
            "        stack.append((width, node))\n"
            "    return roots"
        ),
        explanation=(
            "The pop loop closes every open level that is not shallower than the new "
            "line, which is exactly the dedent rule. Using setdefault means a parent "
            "gains a children key only once it actually has a child, so leaves stay "
            "clean."
        ),
        complexity="Time O(n) amortised over all lines; space O(d) for the maximum depth.",
        edge_cases="Ragged input cannot crash the loop because every pop is guarded.",
        alternative_approaches="A recursive descent version is shorter but risks RecursionError on deep input.",
        testing="out = parse_blocks('a\\n  b\\n  c\\nd')\nassert out == [{'text': 'a', 'children': [{'text': 'b'}, {'text': 'c'}]}, {'text': 'd'}]\nassert parse_blocks('') == []",
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "import ast\n"
            "\n"
            "\n"
            "def extract_docstrings(source: str) -> dict:\n"
            "    tree = ast.parse(source)\n"
            "    found: dict = {}\n"
            "    for node in tree.body:\n"
            "        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):\n"
            "            found[node.name] = ast.get_docstring(node)\n"
            "    return found"
        ),
        explanation=(
            "Parsing rather than importing means the source is inspected as data and "
            "never executes. ast.get_docstring handles the indentation cleanup that a "
            "raw __doc__ would not, and filtering on the node type restricts the result "
            "to functions as required."
        ),
        complexity="Time O(n) in the source length; space O(f) for f functions.",
        edge_cases="A function without a docstring maps to None; invalid source raises SyntaxError.",
        alternative_approaches="inspect would require importing the module and running its code.",
        testing="assert extract_docstrings('def f():\\n    \"\"\"Doc.\"\"\"\\n') == {'f': 'Doc.'}\nassert extract_docstrings('x = 1\\n') == {}",
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "COMPOUND = ('if', 'for', 'while', 'def', 'class', 'with', 'try', 'match')\n"
            "\n"
            "\n"
            "def split_statements(line: str) -> list[str]:\n"
            "    quote = None\n"
            "    previous = ''\n"
            "    parts, current = [], []\n"
            "    for ch in line:\n"
            "        if quote:\n"
            "            current.append(ch)\n"
            "            if ch == quote and previous != '\\\\':\n"
            "                quote = None\n"
            "        elif ch in ('\"', \"'\"):\n"
            "            quote = ch\n"
            "            current.append(ch)\n"
            "        elif ch == ';':\n"
            "            parts.append(''.join(current))\n"
            "            current = []\n"
            "        else:\n"
            "            current.append(ch)\n"
            "        previous = ch\n"
            "    parts.append(''.join(current))\n"
            "    statements = [s.strip() for s in parts if s.strip()]\n"
            "    if statements and statements[0].startswith(COMPOUND):\n"
            "        raise ValueError('compound statement cannot be split safely')\n"
            "    return statements"
        ),
        explanation=(
            "The same quote-tracking scan from exercise 1 is reused, so a semicolon "
            "inside a string never splits a statement. Empty fragments are dropped "
            "before the compound check, which means a trailing semicolon is harmless "
            "while a genuine if or for is still rejected."
        ),
        complexity="Time O(n) in the line length; space O(n).",
        edge_cases="A trailing semicolon produces no empty statement; leading whitespace does not mask the keyword check.",
        alternative_approaches="tokenize is exact but needs a complete source document.",
        testing="assert split_statements('a = 1; b = 2') == ['a = 1', 'b = 2']\nassert split_statements(\"s = ';' ; t = 2\") == [\"s = ';'\", 't = 2']",
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "import ast\n"
            "\n"
            "\n"
            "def outline(source: str) -> list[tuple]:\n"
            "    tree = ast.parse(source)\n"
            "    rows: list[tuple] = []\n"
            "    kinds = {ast.FunctionDef: 'def', ast.AsyncFunctionDef: 'def', ast.ClassDef: 'class'}\n"
            "    for node in tree.body:\n"
            "        kind = kinds.get(type(node))\n"
            "        if kind is None:\n"
            "            continue\n"
            "        doc = ast.get_docstring(node) or ''\n"
            "        summary = doc.strip().splitlines()[0] if doc.strip() else ''\n"
            "        rows.append((kind, node.name, node.lineno, summary))\n"
            "    return rows"
        ),
        explanation=(
            "Mapping node classes to labels avoids a chain of isinstance checks and "
            "keeps the filter table visible. The summary is taken from the first "
            "non-empty docstring line, which gives a usable outline without dumping "
            "whole paragraphs into the report."
        ),
        complexity="Time O(n) in the source length; space O(d) for d top-level definitions.",
        edge_cases="A definition without a docstring yields an empty summary rather than None.",
        alternative_approaches="tokenize plus a line scan is simpler but cannot tell a class from a function.",
        testing="assert outline('def f():\\n    \"\"\"One.\\n    More.\"\"\"\\n') == [('def', 'f', 1, 'One.')]\nassert outline('x = 1\\n') == []",
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
            "\n"
            "def parse_blocks(text):\n"
            "    \"\"\"Parse space-indented lines into nested dicts (self-contained).\"\"\"\n"
            "    roots, stack = [], []\n"
            "    for raw in text.splitlines():\n"
            "        if not raw.strip() or raw.lstrip().startswith('#'):\n"
            "            continue\n"
            "        width = len(raw) - len(raw.lstrip(' '))\n"
            "        node = {'text': raw.strip()}\n"
            "        while stack and stack[-1][0] >= width:\n"
            "            stack.pop()\n"
            "        (stack[-1][1].setdefault('children', []).append(node)\n"
            "         if stack else roots.append(node))\n"
            "        stack.append((width, node))\n"
            "    return roots\n"
            "\n"
            "\n"
            "def render_status(robot) -> str:\n"
            "    state = robot.status()\n"
            "    return (f\"robot {state['name']}\\n\"\n"
            "            f\"    battery {state['battery_pct']:.1f}%\\n\"\n"
            "            f\"    distance {state['travelled_m']:.2f} m\")\n"
            "\n"
            "\n"
            "def summarise(robot) -> dict:\n"
            "    \"\"\"Parse our own indented status log back into data.\"\"\"\n"
            "    blocks = parse_blocks(render_status(robot))\n"
            "    return {\n"
            "        'name': blocks[0]['text'].split(' ', 1)[1],\n"
            "        'fields': [c['text'] for c in blocks[0].get('children', [])],\n"
            "    }\n"
        ),
        explanation=(
            "Rendering structured text and parsing it straight back proves the parser "
            "works on the exact shape the system emits. Splitting the first block's "
            "text recovers the robot name while keeping the child lines as raw field "
            "strings for the caller to interpret."
        ),
        complexity="Time O(n) in the log length; space O(n).",
        edge_cases="A robot with no movement reports a zero distance line that still parses.",
        alternative_approaches="Returning a dict from status() directly avoids the round trip entirely.",
        testing="robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\nout = summarise(robot)\nassert out['name'] == 'rover-01'\nassert len(out['fields']) == 2",
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="What does the interpreter do with the suite that follows a colon-terminated header?",
        choices=[
            "It ignores any block containing a colon.",
            "It treats the more-indented lines as the body of that block.",
            "It requires the suite to be enclosed in braces.",
            "It converts the indentation into tabs before compiling.",
        ],
        answer=1,
        kind="conceptual",
        explanation=(
            "A header ending in a colon is followed by an indented suite, and those "
            "lines become the body. There is no bracket to match and no keyword to "
            "declare the block, so the left margin is the only thing that delimits it."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question=(
            "What does this print?\n\n"
            "def f():\n    if True:\n        return 'yes'\n    return 'no'\n\n"
            "print(f())"
        ),
        choices=[
            "yes",
            "no",
            "It returns None.",
            "It raises an IndentationError.",
        ],
        answer=0,
        kind="code_output",
        explanation=(
            "The return inside the if block executes first because the condition holds, "
            "so the later return is unreachable for this call. The extra indentation is "
            "what places the return inside the if rather than after it."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="A file fails to parse with `IndentationError: unexpected indent`. What is the most likely cause?",
        choices=[
            "A line uses spaces where the rest of the block uses tabs.",
            "The file has no trailing newline.",
            "A variable name is longer than the line limit.",
            "The module lacks a docstring.",
        ],
        answer=0,
        kind="debugging",
        explanation=(
            "Mixed indentation makes the width of a block ambiguous, so the lexer "
            "cannot decide which block the line belongs to and raises before parsing. "
            "Converting the whole file to one style resolves it immediately."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="What is the essential difference between a comment and a docstring?",
        choices=[
            "Comments must be indented; docstrings must not.",
            "Comments are shorter than docstrings.",
            "A docstring must be the first line of the file.",
            "A comment is discarded by the parser; a docstring is a real object on __doc__.",
        ],
        answer=3,
        kind="identify_error",
        explanation=(
            "The parser throws comments away entirely, so they exist only for a human. "
            "A docstring is an ordinary string expression that survives compilation and "
            "can be read back at runtime, which is why documentation tools can show it "
            "without importing the module."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="What is the main engineering benefit of deriving block structure from indentation?",
        choices=[
            "The code a reader sees has exactly the structure the interpreter uses.",
            "It makes the source file smaller.",
            "It lets Python skip parsing entirely.",
            "It allows blocks to be written on a single line.",
        ],
        answer=0,
        kind="reasoning",
        explanation=(
            "In a bracketed language the braces and the indentation are two separate "
            "descriptions of the same structure, and they can disagree. Deriving "
            "structure from layout removes that possibility, so a reviewer reading the "
            "margin is reading the actual control flow."
        ),
        reference="lesson.ipynb - Mental Model",
    )
)

QUIZ.append(
    quiz(
        question="What happens to a `#` comment before the program runs?",
        choices=[
            "It is stored in the compiled code for later inspection.",
            "It is discarded by the parser and never reaches the code object.",
            "It is evaluated as a string expression.",
            "It becomes the module docstring when it is the first line.",
        ],
        answer=1,
        kind="multiple_choice",
        explanation=(
            "The lexer recognises the hash and skips to the end of the line without "
            "emitting a token, so nothing survives into the code object. A string "
            "literal is required for anything that must persist."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question=(
            "What is `type(f.__doc__).__name__` when a function begins with a "
            "triple-quoted description?"
        ),
        choices=[
            "NoneType, because docstrings are discarded.",
            "bytes, because source is read as bytes.",
            "str, because the docstring is an ordinary string object.",
            "function, because it is callable.",
        ],
        answer=2,
        kind="code_output",
        explanation=(
            "A docstring is a normal string expression evaluated at definition time and "
            "stored on the function's __doc__ attribute. That is why it survives into "
            "the compiled code object and can be inspected at runtime."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="Which change most reliably fixes a file that mixes tabs and spaces?",
        choices=[
            "Replace every tab with eight spaces using a text editor's find and replace.",
            "Add a `# -*- coding: utf-8 -*-` line at the top.",
            "Convert the whole file to one indentation style in a single mechanical pass.",
            "Wrap the file contents in a triple-quoted string.",
        ],
        answer=2,
        kind="reasoning",
        explanation=(
            "The problem is inconsistency, not the specific character, so a single "
            "mechanical conversion settles every line at once. Manual editing leaves "
            "the risk that one line is missed, which is the situation that produced "
            "the error in the first place."
        ),
        reference="lesson.ipynb - Best Practices",
    )
)

QUIZ.append(
    quiz(
        question="Why might a fleet team parse a robot's indented status log into nested data?",
        choices=[
            "Human-readable logs and machine-readable structures can share one source.",
            "Indentation makes the log smaller on disk.",
            "Parsing removes the need for a simulator.",
            "The parser runs faster than the robot.",
        ],
        answer=0,
        kind="robotics",
        explanation=(
            "A single indented text form serves both audiences: an engineer reads the "
            "margin to understand the structure, and a supervisor process parses the "
            "same text into dicts. One source of truth avoids the drift that comes from "
            "maintaining a human format and a machine format separately."
        ),
        reference="lesson.ipynb - Robotics Connection",
    )
)

QUIZ.append(
    quiz(
        question="Which tool should you use to read docstrings from a module without executing it?",
        choices=[
            "import the module, then read __doc__ from each function.",
            "ast.parse the source and call ast.get_docstring on each definition.",
            "run the file with python and capture stdout.",
            "call help() on the module.",
        ],
        answer=1,
        kind="implementation_choice",
        explanation=(
            "Parsing treats the source as data and never runs it, which is both safe "
            "and sufficient. Importing executes the module's top-level code, running it "
            "has side effects, and help() requires the module to be imported first."
        ),
        reference="solution.ipynb - Solution 8",
    )
)

MINI_PROJECT = {
    "title": "Mini-Project: Structured Diagnostics Reader",
    "brief": (
        "Build a small reader for the indented diagnostics that ROBO-X services emit. "
        "It must validate the formatting, parse the hierarchy, and summarise the "
        "values a supervisor cares about."
    ),
    "scenario": (
        "Several fleet services write indented diagnostics to rotating log files. You "
        "need one component that turns that text into validated data so alerting can "
        "run on structured fields instead of regular expressions."
    ),
    "rationale": (
        "Diagnostics are the first thing an engineer reads and the first thing "
        "automation needs, so a single well-tested reader removes an entire class of "
        "fragile text processing."
    ),
    "requirements": [
        "Parse indented text into nested dictionaries using an explicit stack.",
        "Ignore blank lines and comment lines.",
        "Validate indentation and report problems with line numbers.",
        "Extract a numeric field from a child line such as 'battery 87.5%'.",
        "Return a summary dict with the entity name and its numeric fields.",
    ],
    "constraints": [
        "Standard library only.",
        "No recursion; use an explicit stack.",
        "Every public function carries a docstring.",
    ],
    "deliverables": [
        "`diagnostics.py` with the parser, validator and summariser.",
        "`test_diagnostics.py` with at least ten assertions.",
        "A README section showing one input log and its parsed form.",
    ],
    "steps": [
        "Implement `parse_blocks` and prove it on a hand-written sample log.",
        "Implement `check_indentation` and confirm it rejects a tab-indented file.",
        "Implement `field_value` to extract a number from a child line.",
        "Compose the three in `summarise(log_text)`.",
        "Write tests for empty input, comments, ragged indentation and a missing field.",
    ],
    "expected_behavior": (
        "Feeding a well-formed log returns a dict with the entity name and a mapping of "
        "numeric fields; a badly indented log returns a specific problem message "
        "naming the line."
    ),
    "acceptance": [
        "All assertions pass from a clean run.",
        "Ragged and comment-heavy input never raises.",
        "Indentation problems name the 1-based line number.",
        "No function exceeds roughly 30 lines.",
    ],
    "extensions": [
        "Emit the summary as JSON for the alerting pipeline.",
        "Track the source line number on every parsed node.",
        "Reject logs whose indentation jumps by more than one level.",
    ],
}

RESEARCH = {
    "question": (
        "How much does comment density correlate with defect rate in a small body of "
        "Python source?"
    ),
    "hypothesis": (
        "Files with comments explaining decisions have fewer defects than files with "
        "few or no comments, once size is held roughly constant."
    ),
    "experiment": [
        STEPS(
            [
                "Choose ten Python files of similar length from this repository or your own work.",
                "For each file compute the comment ratio with the line_census function from this topic.",
                "For each file count defects as failing tests or open rework items you can identify.",
                "Record every raw measurement in the table below before analysing anything.",
            ]
        ),
    ],
    "data": [
        CODE_CELL(
            "# Record your raw measurements - one row per file.\n"
            "# Copy real values; do not invent them.\n"
            "#\n"
            "# | file | lines | comment ratio | defects |"
        ),
    ],
    "analysis": [
        MD(
            "Group the files by comment ratio and compare mean defects per group. With "
            "only ten samples, treat the result as a prompt for a larger study rather "
            "than a conclusion, and state that limitation explicitly."
        ),
    ],
    "result": [
        MD(
            "Report whether the hypothesis survived, with the numbers that decided it. "
            "Record any file that contradicted the trend rather than dropping it."
        ),
    ],
    "interpretation": [
        MD(
            "Offer a mechanism, and consider confounding factors seriously: file age, "
            "author, and how much the file is tested all move with defect rate "
            "independently of comments. Name at least two of these."
        ),
    ],
    "conclusion": [
        MD(
            "Give your verdict and propose a follow-up study that would control for the "
            "confounders you identified."
        ),
    ],
    "extensions": [
        "Repeat the analysis using docstring coverage instead of comment ratio.",
        "Separate explanatory comments from comments that merely restate code.",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Bring-Up Log Reader",
    "context": (
        "During mobile robot bring-up the controller emits an indented diagnostics "
        "block. The fleet supervisor needs the same information as structured data "
        "before it will allow the robot to leave the bench."
    ),
    "mission": (
        "Implement `read_diagnostics(robot)` that renders the simulator's state as an "
        "indented log, parses it straight back, and returns a validated summary."
    ),
    "requirements": [
        "Render at least the robot name, battery percentage and distance travelled.",
        "Parse the rendered log into nested dictionaries with an explicit stack.",
        "Return a dict with `name` and a `fields` mapping of numeric values.",
        "Validate indentation and report problems rather than guessing.",
    ],
    "constraints": [
        "No recursion; use an explicit stack.",
        "No hardware required; use `shared/robo_x_sim`.",
        "Never raise on empty or comment-only input.",
    ],
    "interface": "def read_diagnostics(robot) -> dict:",
    "success_criteria": [
        "The returned name matches the robot's name.",
        "Battery and distance are present as floats.",
        "Empty input returns an empty result rather than raising.",
    ],
    "extension": (
        "Add a `strict` flag that rejects a log whose indentation jumps by more than "
        "one level, and explain which deployments need it."
    ),
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Make indentation-as-grammar explicit rather than assumed.",
        "Distinguish comments, which vanish, from docstrings, which persist.",
        "Show that Python's parser is a tool for reading code as data.",
    ],
    "misconceptions": [
        [
            "Indentation is only cosmetic in Python.",
            "It is part of the grammar; inconsistent indentation is a parse error.",
        ],
        [
            "Docstrings are just comments with nicer formatting.",
            "They are real string objects retrievable at runtime via __doc__.",
        ],
        [
            "Semicolons make code more compact and therefore better.",
            "They make every line a line the reader must mentally split again.",
        ],
        [
            "An IndentationError means the file has stray spaces at the end.",
            "It usually means tabs and spaces are mixed within one block.",
        ],
    ],
    "difficult_concepts": [
        "Believing that structure lives in brackets rather than in the margin.",
        "Using an explicit stack to mirror what the parser does with INDENT and DEDENT.",
        "Reading an AST as data rather than as a curiosity.",
    ],
    "demonstrations": [
        "Deliberately break indentation in a file and let Python refuse to parse it.",
        "Run tokenize over a small file and show INDENT and DEDENT tokens directly.",
        "Print a function's __doc__ after defining it, then show that a comment cannot be retrieved at all.",
    ],
    "discussion": [
        "Why did Python's designers give up braces? What did they gain and what did they lose?",
        "When would you accept a machine-generated file that uses a different indent width?",
    ],
    "student_errors": [
        [
            "TabError after pasting code from somewhere else",
            "The source used tabs while the file uses spaces",
            "Convert the file to spaces in one mechanical pass",
        ],
        [
            "Unexpected indent on a line that looks correct",
            "A previous block header was deleted, leaving the body dangling",
            "Re-indent the selection and inspect the block above",
        ],
        [
            "Docstring appears in the class but not the function",
            "It was written as a comment, or placed after another statement",
            "Place the string first in the body, with no preceding statement",
        ],
    ],
    "pacing": (
        "90 minutes of lesson with live demonstrations, then 2 hours on exercises. "
        "Give extra time to the stack-based parser: it is the first genuinely "
        "algorithmic task in the course."
    ),
    "extensions": [
        "Have students implement the parser recursively and compare stack usage on deep input.",
        "Ask them to write a formatter that re-indents a whole file using ast.",
    ],
    "assessment": (
        "Grade against rubric.md. Exercises 7 to 10 carry the signal; a student who can "
        "explain the pop loop has understood the grammar in operational terms."
    ),
    "support": (
        "Draw the stack on paper with them for a three-level sample before they write "
        "any code.",
    ),
    "extension_fast": (
        "Ask for a tokenize-based version of parse_blocks and a short comparison of the two.",
    ),
}

RUBRIC = {
    "artifacts": [
        ["exercises.ipynb", "40%", "All 10 exercises implemented and edge-cased."],
        ["mini_project.ipynb", "25%", "diagnostics.py plus its test suite."],
        ["robotics_challenge.ipynb", "25%", "Log reader degrades safely."],
        ["research.ipynb", "10%", "Real measurements with a defensible conclusion."],
    ],
    "criteria": [
        ["Correctness", "35", "Parsing handles ragged, empty and comment-heavy input."],
        ["Code quality", "25", "PEP 8 naming, docstrings, small focused functions."],
        ["Testing", "25", "Assertions cover happy path, edge cases and failure."],
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
            "Every exercise implemented, ragged input handled without raising, and the "
            "log reader round-trips the simulator's own output correctly.",
        ],
        [
            "Merit",
            "Most exercises correct; testing covers the main paths and several edge "
            "cases; the stack logic is correct on well-formed input.",
        ],
        [
            "Pass",
            "Core requirements met on well-formed input, but ragged indentation or "
            "comment-only input is unhandled and untested.",
        ],
        [
            "Fail",
            "The parser cannot handle nesting, or uses recursion and overflows on deep "
            "input without any test covering it.",
        ],
    ],
}

TOPIC = topic(
    topic_id="1.3",
    title="Python Syntax, Indentation, Comments, and Code Structure",
    module=1,
    module_title="Getting Started with Python",
    directory="03_syntax_indentation_comments",
    summary=(
        "Why the left margin is part of the grammar: indentation as structure, the "
        "difference between comments and docstrings, and how to parse code without "
        "running it."
    ),
    why_it_matters=(
        "In every other language you learned, whitespace was decoration. In Python it "
        "is syntax, which means a formatting mistake is a parse error and a readable "
        "file is a correct file. Robotics teams also rely on structured, indented "
        "diagnostics, so this topic is where layout becomes data."
    ),
    objectives=[
        "Explain how INDENT and DEDENT tokens produce block structure.",
        "Apply PEP 8 indentation consistently and repair a mixed-indentation file.",
        "Distinguish comments from docstrings and use each correctly.",
        "Use implicit line joining to wrap long expressions readably.",
        "Parse an indented log into nested data with an explicit stack.",
        "Read docstrings from source with ast without importing the module.",
    ],
    prerequisites=[
        "Topic 1.1 Introduction to Python",
        "Topic 1.2 Installing Python, IDEs, and the REPL",
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
