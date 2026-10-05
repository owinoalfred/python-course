"""Topic 1.7 - Basic Input/Output.

Hand-authored to the Course Content Standard. The spine: a program that talks to a
human, and the fact that every stream in Python is just a text target you can
redirect - which is what makes console programs testable.
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
        "Input and output in Python are objects, not language constructs. `print` is a "
        "function that writes to `sys.stdout`; `input` is a function that reads a line "
        "from `sys.stdin`. Because those are ordinary module attributes, you can "
        "replace them. That single fact is what makes an interactive program testable "
        "without a human at the keyboard, and it is the most useful thing in this "
        "topic."
    ),
    CODE_CELL(
        "import sys\n"
        "\n"
        "print('first')\n"
        "print('second')\n"
        "\n"
        "# print takes any number of objects and one separator\n"
        "print('rover-01', 48.0, True, sep=' | ')\n"
        "print('no newline here', end='')\n"
        "print(' - appended')\n"
        "\n"
        "print('stdout is:', sys.stdout.write.__self__ is sys.stdout)"
    ),
    MD(
        "Formatted output is where most console programs earn their keep. The f-string "
        "format specification controls alignment, width, precision and type, and using "
        "it is far more readable than `str.format` or `%` for anything with a column "
        "layout."
    ),
    CODE_CELL(
        "rows = [('rover-01', 48.0), ('rover-02', 12.5), ('rover-03', 99.9)]\n"
        "\n"
        "print(f\"{'ROBOT':<10} {'BATTERY':>8}\")\n"
        "print('-' * 18)\n"
        "for name, pct in rows:\n"
        "    print(f'{name:<10} {pct:>7.1f}%')"
    ),
    NOTE(
        "Why input() is dangerous in a notebook",
        "input() blocks waiting for a human, and in a notebook it will hang the kernel "
        "with no way to recover except interrupting it. Throughout this course, input "
        "is demonstrated by redirecting sys.stdin from an in-memory stream, which runs "
        "deterministically and immediately.",
    ),
]

LESSON["formal_theory"] = [
    MD(
        "Every running Python process has three standard streams, each a text-mode "
        "file object: `sys.stdin` for input, `sys.stdout` for normal output, and "
        "`sys.stderr` for diagnostics. The first two are text streams with a defined "
        "encoding; `sys.stderr` is unbuffered and line-oriented by convention. A "
        "command-line tool is expected to put machine-readable results on stdout and "
        "human-facing diagnostics on stderr, so the two can be redirected independently."
    ),
    EQUATION(
        "process  ->  fd 0 (stdin)   fd 1 (stdout)   fd 2 (stderr)"
    ),
    MD(
        "Because `sys.stdout` is an object, an assignment rebinds the name that `print` "
        "looks up at call time. This is how `contextlib.redirect_stdout` captures output "
        "in a test, and how a program can write to a string, a file or a socket by "
        "changing one attribute."
    ),
    CODE_CELL(
        "import io\n"
        "import sys\n"
        "\n"
        "buffer = io.StringIO()\n"
        "original = sys.stdout\n"
        "sys.stdout = buffer\n"
        "try:\n"
        "    print('captured by the buffer')\n"
        "finally:\n"
        "    sys.stdout = original\n"
        "\n"
        "print('buffered text:', repr(buffer.getvalue()))\n"
        "print('restored  ->', 'print still writes here')"
    ),
    TABLE(
        ["Stream", "Purpose", "Consequence of writing there"],
        [
            ["`sys.stdin`", "Data the program consumes", "Blocks if nothing is piped in"],
            ["`sys.stdout`", "Results a caller may parse", "Breaks `prog > file.json`"],
            ["`sys.stderr`", "Diagnostics for a human", "Bypasses the parsed output"],
        ],
    ),
]

LESSON["syntax"] = [
    MD(
        "`print` accepts any number of objects, one `sep` between them and an `end` "
        "after the last. Both are strings, and both are what make column output "
        "readable without a single concatenation."
    ),
    CODE_CELL(
        "def print_header(title: str, width: int = 24) -> None:\n"
        "    print(title.center(width, '='))\n"
        "\n"
        "\n"
        "print_header('ROBO-X')\n"
        "print('id', 'battery', 'status', sep='\\t')\n"
        "print('rover-01', 48.0, 'ACTIVE', sep='\\t')\n"
        "print()                                   # an empty line\n"
        "print('done', end='\\n', flush=True)      # explicit end and flush"
    ),
    MD("The anti-pattern:"),
    CODE(
        "print('Robot: ' + name + ' battery: ' + str(pct) + '%')\n"
        "\n"
        "print(f'{name}: {pct}%')     # one expression, no conversion calls",
        lang="text",
    ),
    WARN(
        "input() always returns a string",
        "Whatever the user types arrives as text, so a number must be converted before "
        "arithmetic. Forgetting that produces the classic TypeError: can only "
        "concatenate str to str.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - reading from a redirected stdin instead of a human.**"),
    CODE_CELL(
        "import io\n"
        "import sys\n"
        "\n"
        "\n"
        "def read_answer(prompt: str, answers) -> str:\n"
        "    \"\"\"Stand-in for input() that reads from a fixed list of answers.\"\"\"\n"
        "    print(prompt, end=' ')\n"
        "    return next(answers)\n"
        "\n"
        "\n"
        "answers = iter(['rover-01', '48.5'])\n"
        "name = read_answer('robot id?', answers)\n"
        "battery = read_answer('battery pct?', answers)\n"
        "\n"
        "print(f'parsed -> {name} at {float(battery)}%')"
    ),
    MD("**Example 2 - the string methods every parser needs.**"),
    CODE_CELL(
        "raw = '  Rover-01  '\n"
        "print('strip     :', repr(raw.strip()))\n"
        "print('lower     :', raw.strip().lower())\n"
        "print('split     :', 'front,rear,left'.split(','))\n"
        "print('partition :', 'key=value'.partition('='))\n"
        "print('replace   :', 'rover-01'.replace('-', '_'))\n"
        "print('startswith:', raw.strip().startswith('Ro'))\n"
        "print('zfill     :', '7'.zfill(3))"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "Real stdout has the same contract, which is what makes a console tool "
        "composable: print a header to the standard output, and diagnostics to the "
        "error stream, so the two can be separated downstream."
    ),
    CODE_CELL(
        "import sys\n"
        "\n"
        "\n"
        "def report(robot_id: str, battery_pct: float) -> None:\n"
        "    print(f'{robot_id}:{battery_pct:.1f}')          # machine-readable\n"
        "    print(f'warning: {robot_id} battery is low', file=sys.stderr)\n"
        "\n"
        "\n"
        "report('rover-01', 12.5)\n"
        "print('the two streams can be redirected independently')"
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "Capturing output turns a printing function into a testable one. This is the "
        "single most useful technique in this topic, because it means a console "
        "program can be verified in an automated suite without a human present."
    ),
    CODE_CELL(
        "import io\n"
        "import sys\n"
        "from contextlib import redirect_stdout\n"
        "\n"
        "\n"
        "def menu() -> None:\n"
        "    print('1. arm')\n"
        "    print('2. disarm')\n"
        "\n"
        "\n"
        "buffer = io.StringIO()\n"
        "with redirect_stdout(buffer):\n"
        "    menu()\n"
        "\n"
        "captured = buffer.getvalue()\n"
        "print('captured lines:', captured.strip().splitlines())\n"
        "print('contains arm  :', 'arm' in captured)"
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "Below is an interactive dispatch prompt written so it can be tested. It reads "
        "from an injected stream and returns a decision rather than acting on one."
    ),
    CODE_CELL(
        "\"\"\"dispatch.py - ask for a command and turn it into a decision.\"\"\"\n"
        "from __future__ import annotations\n"
        "\n"
        "COMMANDS = {\n"
        "    '1': 'ARM',\n"
        "    '2': 'DISARM',\n"
        "    'q': 'QUIT',\n"
        "}\n"
        "\n"
        "\n"
        "def read_choice(stream) -> str:\n"
        "    \"\"\"Read one line from a file-like object, tolerating EOF.\"\"\"\n"
        "    line = stream.readline()\n"
        "    if not line:\n"
        "        return 'q'\n"
        "    return line.strip().lower()\n"
        "\n"
        "\n"
        "def run(stream) -> list[str]:\n"
        "    \"\"\"Process commands until quit, returning the decisions taken.\"\"\"\n"
        "    print('ROBO-X dispatch: 1=arm 2=disarm q=quit')\n"
        "    history: list[str] = []\n"
        "    while True:\n"
        "        print('> ', end='', flush=True)\n"
        "        choice = read_choice(stream)\n"
        "        action = COMMANDS.get(choice)\n"
        "        if action is None:\n"
        "            print(f'unknown command: {choice!r}')\n"
        "            continue\n"
        "        if action == 'QUIT':\n"
        "            break\n"
        "        history.append(action)\n"
        "        print(f'  -> {action}')\n"
        "    return history"
    ),
    MD(
        "Two design choices make this testable. The stream is a parameter rather than a "
        "global read of `input`, so a test supplies a `StringIO`. And `readline` returning "
        "an empty string is treated as end of input, which means a closed pipe ends the "
        "loop instead of spinning forever."
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "COMMANDS is a module-level lookup table, so adding a command is one entry "
            "rather than another branch in the loop.",
            "read_choice takes the stream as a parameter, which is the whole reason the "
            "program can be tested without a keyboard.",
            "readline returning an empty string is the end-of-input signal and maps to "
            "'q', so a closed pipe terminates the loop instead of spinning.",
            "strip().lower() normalises the input so 'Q' and ' q ' behave like 'q'.",
            "The while loop continues on an unknown command rather than quitting, which "
            "is what a human expects from a prompt.",
            "Actions are appended to history instead of being executed, so the function "
            "is pure with respect to the robot and its output can be asserted directly.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - forgetting that input returns text.**"),
    CODE(
        "value = input('battery: ')   # always a str\n"
        "value * 2                    # TypeError\n"
        "\n"
        "value = float(input('battery: '))",
        lang="text",
    ),
    MD("**Mistake 2 - printing diagnostics to stdout.**"),
    CODE(
        "print('rover-01:48.0')       # result, parseable downstream\n"
        "print('warning: low battery')  # oops, also on stdout\n"
        "\n"
        "print('warning: low battery', file=sys.stderr)",
        lang="text",
    ),
    MD("**Mistake 3 - using input() in a notebook.**"),
    CODE(
        "name = input('id: ')   # blocks the kernel with no visible prompt",
        lang="text",
    ),
    MD("**Mistake 4 - a loop that never terminates on end of input.**"),
    CODE(
        "while input() != 'q':   # raises EOFError at the end, or spins\n"
        "    process()\n"
        "\n"
        "line = stream.readline()\n"
        "if not line:            # explicit end-of-input check\n"
        "    break",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "The first question about any console problem is which stream the text went to. "
        "Redirect each one separately and the answer becomes obvious."
    ),
    CODE_CELL(
        "import sys\n"
        "\n"
        "print('this goes to stdout')\n"
        "print('this goes to stderr', file=sys.stderr)\n"
        "\n"
        "# python -c '...' > out.txt        captures stdout only\n"
        "# python -c '...' 2> err.txt      captures stderr only\n"
        "# python -c '...' > all.txt 2>&1  captures both"
    ),
    MD(
        "When a formatted column looks wrong, print the raw values alongside the "
        "formatted ones. A width specifier silently truncates or pads, so comparing "
        "`repr(value)` with the rendered cell usually reveals the mismatch."
    ),
    CODE_CELL(
        "value = 1234.5678\n"
        "print('raw        :', repr(value))\n"
        "print('8.1f       :', f'{value:8.1f}')\n"
        "print('8.3f       :', f'{value:8.3f}')\n"
        "print('left, 10.4f:', f'{value:<10.4f}|')\n"
        "print('explicit  :', f'[{value:8.1f}]')"
    ),
    NOTE(
        "flush when it matters",
        "Output is buffered when it is not a terminal, so a long-running program may "
        "appear to hang. Pass flush=True to print, or run python with -u, when the user "
        "needs to see progress as it happens.",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Put machine-readable results on stdout and diagnostics on stderr.",
            "Use f-string format specs for columns rather than manual padding.",
            "Convert input to the type you need immediately, at the point of reading.",
            "Read from a stream object passed in, not from a global `input` call.",
            "Treat an empty read as end of input and exit the loop.",
            "Capture output with redirect_stdout so console code can be tested.",
            "Use flush=True for progress output in long-running services.",
            "Keep a prompt on the same line with print(..., end='', flush=True).",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "Console I/O is almost always the bottleneck, and it is a property of the "
        "terminal rather than of Python. A single `print` may trigger a write syscall; a "
        "loop of ten thousand prints will visibly lag, while a loop of a million "
        "in-memory operations will not. If a program must emit a large volume of text, "
        "build one string and write it once rather than calling print repeatedly."
    ),
    MD(
        "The second cost is string concatenation. Building a report with `result += "
        "line` inside a loop is quadratic, because each concatenation copies everything "
        "written so far. A list with `append` followed by a single `join` is linear. This "
        "is one of the few cases where the idiomatic Python version is not merely "
        "prettier but asymptotically faster."
    ),
    TIP(
        "Batch your writes",
        "For a large report, accumulate lines in a list and print the joined result "
        "once, or write to a file handle with a large buffer.",
    ),
]

LESSON["pythonic_approaches"] = [
    MD("Joining a report: accumulating versus collecting then joining."),
    CODE_CELL(
        "rows = [('rover-01', 48.0), ('rover-02', 12.5)]\n"
        "\n"
        "# before: repeated concatenation copies the whole string each time\n"
        "report = ''\n"
        "for name, pct in rows:\n"
        "    report += f'{name} {pct:.1f}\\n'\n"
        "\n"
        "# after: build a list, join once\n"
        "lines = [f'{name} {pct:.1f}' for name, pct in rows]\n"
        "report = '\\n'.join(lines)\n"
        "\n"
        "print(report)"
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "Robot services are console programs. They print a banner at start-up, report "
        "readings while running, and send warnings to stderr so a supervisor can log "
        "them separately from the data stream. Getting the two streams right is what "
        "makes `service > telemetry.json` work."
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
        "print(f\"{state['name']}:{state['battery_pct']:.1f}\")          # data\n"
        "if state['battery_pct'] < 20:\n"
        "    print('warning: low battery', file=sys.stderr)  # diagnostic"
    ),
]

LESSON["engineering_example"] = [
    MD(
        "A reporting function that writes machine-readable output to one stream and "
        "human-readable warnings to the other."
    ),
    CODE_CELL(
        "import sys\n"
        "\n"
        "\n"
        "def report_fleet(robots, stream=sys.stdout, errors=sys.stderr) -> None:\n"
        "    \"\"\"Print one parseable line per robot and warnings to the error stream.\"\"\"\n"
        "    for robot in robots:\n"
        "        name = robot.get('name', '<unnamed>')\n"
        "        pct = robot.get('battery_pct')\n"
        "        if pct is None:\n"
        "            print(f'warning: {name} has no battery reading', file=errors)\n"
        "            continue\n"
        "        print(f'{name}:{pct:.1f}', file=stream)\n"
        "        if pct < 20:\n"
        "            print(f'warning: {name} battery {pct:.1f}%', file=errors)"
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Print a two-column table with the robot name left-aligned and the battery "
            "right-aligned to eight characters.",
            "Capture the output of a small function with redirect_stdout and assert that "
            "it contains what you expect.",
            "Read three lines from a StringIO stream and echo each one with a prefix.",
            "Write a function that prints its data to a stream parameter and its "
            "warnings to sys.stderr, then call it twice.",
        ]
    ),
    CODE_CELL(
        "import io\n"
        "from contextlib import redirect_stdout\n"
        "\n"
        "def banner() -> None:\n"
        "    print('ROBO-X ready')\n"
        "\n"
        "\n"
        "buffer = io.StringIO()\n"
        "with redirect_stdout(buffer):\n"
        "    banner()\n"
        "assert 'ROBO-X ready' in buffer.getvalue()\n"
        "print('captured:', repr(buffer.getvalue()))\n"
        "\n"
        "stream = io.StringIO('rover-01\\nrover-02\\n')\n"
        "while (line := stream.readline()):\n"
        "    print('echo:', line.strip())"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: three pipes, each with a name you can swap.** stdin carries "
        "data in, stdout carries results out, stderr carries complaints out. `print` and "
        "`input` are simply the default functions attached to those pipes. Change the "
        "name on the pipe and every function using it follows - which is why redirecting "
        "output in a test changes the behaviour of the code under test without changing "
        "the code."
    ),
    TABLE(
        ["You write", "Actually happens"],
        [
            ["`print(x)`", "str(x) is written to `sys.stdout`"],
            ["`input(p)`", "p is written to stdout, a line read from `sys.stdin`"],
            ["`print(x, file=sys.stderr)`", "x is written to the error pipe instead"],
            ["`sys.stdout = buffer`", "every later print goes to the buffer"],
        ],
    ),
]

TERMS = [
    ["Stream", "A file-like object carrying text between a program and its environment."],
    ["stdin", "The standard input stream, conventionally file descriptor 0."],
    ["stdout", "The standard output stream, conventionally file descriptor 1."],
    ["stderr", "The standard error stream, conventionally file descriptor 2."],
    ["Buffer", "An in-memory stream that can stand in for a terminal or a file."],
    ["redirect_stdout", "A context manager that swaps sys.stdout for the duration of a block."],
    ["Format specification", "The `:>8.1f` style spec that controls width and precision."],
    ["flush", "Forcing buffered output to be written immediately."],
    ["End of input", "An empty read from a stream, which is not the same as an empty line."],
    ["CLI contract", "The convention that stdout holds results and stderr holds diagnostics."],
]

LESSON["summary"] = [
    MD(
        "Input and output in Python are objects, not language features. `print` writes to "
        "`sys.stdout`, `input` reads from `sys.stdin`, and both are ordinary module "
        "attributes you can replace. That is the central idea of this topic, and it has "
        "an immediate practical consequence: an interactive program can be tested without "
        "a human, by supplying an in-memory stream."
    ),
    MD(
        "The second half of the topic is formatting and the stream contract. The "
        "f-string format specification handles alignment, width and precision well "
        "enough to replace manual padding entirely. And the convention that stdout "
        "carries machine-readable results while stderr carries human diagnostics is what "
        "makes a console tool composable - it is the reason `roboctl status > state.json` "
        "produces a file you can parse."
    ),
    MD(
        "The practical habit to take away is to pass the stream in rather than reaching "
        "for a global. A function that takes a stream is testable, scriptable and "
        "reusable; a function that calls `input` directly is none of those. And when you "
        "write a loop that reads until a sentinel, treat an empty read as end of input - "
        "otherwise a closed pipe turns your prompt into an infinite loop."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "`print` writes to `sys.stdout`; `input` reads from `sys.stdin`.",
            "Both are replaceable objects, which is what makes console code testable.",
            "Redirecting stdout is how a test asserts on printed output.",
            "Format specs control alignment, width and precision without manual padding.",
            "`input()` always returns a string, so convert before arithmetic.",
            "Put results on stdout and diagnostics on stderr.",
            "Pass the stream in as a parameter rather than calling input directly.",
            "An empty read means end of input; always check it in a read loop.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "[input and output](https://docs.python.org/3/tutorial/inputoutput.html)",
            "[sys - standard streams and configuration](https://docs.python.org/3/library/sys.html)",
            "[io - core tools for working with streams](https://docs.python.org/3/library/io.html)",
            "[contextlib.redirect_stdout](https://docs.python.org/3/library/contextlib.html#contextlib.redirect_stdout)",
            "[Format specification mini-language](https://docs.python.org/3/library/string.html#format-specification-mini-language)",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Render an aligned table",
        difficulty="MEDIUM",
        learning_objectives=["Use format specifications.", "Return a display string."],
        concepts_tested=["f-strings", "format specs", "loops"],
        problem_statement=(
            "Write `format_table(rows)` returning a header line and one line per "
            "`(name, battery_pct)` pair, with the name left-aligned in ten columns and "
            "the percentage right-aligned in eight with one decimal."
        ),
        requirements=["Use a single f-string per line.", "Include a dashed separator."],
        constraints=["Return the whole table as one string."],
        input_description="A list of (name, pct) pairs.",
        expected_output="A multi-line string.",
        example_input="format_table([('rover-01', 48.0)])",
        example_output="'ROBOT      BATTERY\\n---------- --------\\nrover-01     48.0'",
        edge_cases=["An empty list still prints the header.", "Long names are not truncated.", "Negative percentages are shown."],
        hints=["Build a list of lines and join them with a newline at the end."],
        success_criteria=["The header is present for an empty list.", "Each row is aligned to the specified widths."],
        optional_extension="Add a right-hand flag column for values below 20.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Parse a percentage from text",
        difficulty="MEDIUM",
        learning_objectives=["Normalise text.", "Convert safely."],
        concepts_tested=["strings", "conversion", "error handling"],
        problem_statement=(
            "Write `parse_percent(text, default=None)` accepting '48.5%', '48.5' or "
            "' 48.5 % ' and returning a float. Return `default` when the text is not "
            "numeric, and raise TypeError for a non-string."
        ),
        requirements=["Strip whitespace and a trailing percent sign.", "Reject bools and numbers as input."],
        constraints=["Never raise for bad text."],
        input_description="A string, possibly with a percent sign.",
        expected_output="A float, or the default.",
        example_input="parse_percent('48.5%')",
        example_output="48.5",
        edge_cases=["' 48.5 % ' parses to 48.5.", "'n/a' returns the default.", "48.5 as a float raises TypeError."],
        hints=["strip(), then rstrip('%'), then strip() again."],
        success_criteria=["'48.5%' gives 48.5.", "'n/a' returns the default."],
        optional_extension="Reject values outside 0 to 100 by returning the default.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Echo lines from a stream",
        difficulty="MEDIUM",
        learning_objectives=["Read a stream to exhaustion.", "Handle end of input."],
        concepts_tested=["streams", "loops", "strings"],
        problem_statement=(
            "Write `echo_lines(stream, prefix='> ')` returning a list of prefixed, "
            "stripped lines, stopping at end of input rather than on a blank line."
        ),
        requirements=["Use readline in a loop.", "Stop when readline returns an empty string."],
        constraints=["Take the stream as a parameter; never call input."],
        input_description="Any file-like object supporting readline.",
        expected_output="A list of strings.",
        example_input="echo_lines(io.StringIO('a\\nb\\n'))",
        example_output="['> a', '> b']",
        edge_cases=["An empty stream gives an empty list.", "Blank lines are kept as empty entries.", "A final line without a newline is included."],
        hints=["while (line := stream.readline()) is not the test; check for the empty string."],
        success_criteria=["Returns two entries for 'a\\nb\\n'.", "An empty stream returns []."],
        optional_extension="Stop early on a line equal to 'quit'.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Centre a title banner",
        difficulty="MEDIUM",
        learning_objectives=["Use string padding.", "Choose a width policy."],
        concepts_tested=["strings", "format specs"],
        problem_statement=(
            "Write `banner(title, width=24, fill='=')` returning the title centred in a "
            "field of `width`, padded with `fill`. A title longer than the width is "
            "returned unchanged."
        ),
        requirements=["Use the format spec, not manual loops.", "Never truncate."],
        constraints=["Pad only; do not cut."],
        input_description="A title string and an optional width.",
        expected_output="A padded string.",
        example_input="banner('ROBO-X')",
        example_output="'==========ROBO-X==========='",
        edge_cases=["A title longer than the width is returned unchanged.", "A width smaller than 3 raises ValueError."],
        hints=["str.center is the direct answer; a format spec works too."],
        success_criteria=["Centres a short title to the requested width.", "Returns a long title unchanged."],
        optional_extension="Return a multi-line banner with a rule beneath.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Normalise a yes/no answer",
        difficulty="MEDIUM",
        learning_objectives=["Map aliases to one value.", "Reject ambiguity."],
        concepts_tested=["dicts", "strings", "validation"],
        problem_statement=(
            "Write `normalise_choice(text)` mapping y/yes/1/true to 'ARM' and "
            "n/no/0/false to 'DISARM', case-insensitively after stripping. Return None "
            "for anything else."
        ),
        requirements=["Use a lookup table.", "Never raise for unknown text."],
        constraints=["One table, no chain of ifs."],
        input_description="A short text answer.",
        expected_output="'ARM', 'DISARM' or None.",
        example_input="normalise_choice(' Yes ')",
        example_output="'ARM'",
        edge_cases=["'maybe' returns None.", "'Y' returns 'ARM'.", "An empty string returns None."],
        hints=["Normalise with strip().lower(), then look it up in a dict."],
        success_criteria=["' Yes ' returns 'ARM'.", "'maybe' returns None."],
        optional_extension="Accept a default for unrecognised answers.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Process commands from a stream",
        difficulty="HARD",
        learning_objectives=["Loop until end of input.", "Separate data from diagnostics."],
        concepts_tested=["streams", "loops", "dicts"],
        problem_statement=(
            "Write `run_commands(stream, out, errors)` processing '1', '2' and 'q' "
            "until quit or end of input, appending ARM/DISARM decisions to a returned "
            "list and writing unknown commands to the error stream."
        ),
        requirements=["Unknown commands are reported, not fatal.", "End of input ends the loop."],
        constraints=["No global input(); take the stream as a parameter."],
        input_description="A file-like object and two output streams.",
        expected_output="A list of decisions.",
        example_input="run_commands(io.StringIO('1\\nq\\n'), out, err)",
        example_output="['ARM']",
        edge_cases=["An empty stream returns [].", "Unknown commands are skipped.", "Input without a trailing newline still ends cleanly."],
        hints=["readline returning '' is end of input; map the stripped value through a table."],
        success_criteria=["'1\\nq\\n' returns ['ARM'].", "An empty stream returns []."],
        optional_extension="Return a count of the unknown commands as well.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Capture what a function printed",
        difficulty="HARD",
        learning_objectives=["Redirect a stream.", "Test console code."],
        concepts_tested=["contextlib", "io", "testing"],
        problem_statement=(
            "Write `capture_output(func, *args, **kwargs)` calling `func` with "
            "redirected stdout and returning the captured text. The original stream must "
            "be restored even if the function raises."
        ),
        requirements=["Use redirect_stdout.", "Restore the stream on failure."],
        constraints=["Return a string, not a buffer."],
        input_description="A callable and its arguments.",
        expected_output="The text the function printed.",
        example_input="capture_output(lambda: print('hi'))",
        example_output="'hi\\n'",
        edge_cases=["A function that prints nothing returns ''.", "An exception propagates after the stream is restored."],
        hints=["A StringIO plus a with-block handles the restore automatically."],
        success_criteria=["Captures 'hi\\n' for a one-line print.", "A raising function still leaves stdout intact."],
        optional_extension="Also capture stderr and return both streams.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Emit a fleet report on two streams",
        difficulty="HARD",
        learning_objectives=["Respect the CLI contract.", "Format machine output."],
        concepts_tested=["sys.stderr", "f-strings", "iteration"],
        problem_statement=(
            "Write `report_fleet(robots, out, errors)` printing 'name:pct' for each "
            "robot with a numeric battery reading, sending a warning to `errors` for "
            "each robot missing one and for each reading below 20."
        ),
        requirements=["Never print data to the error stream.", "Round to one decimal."],
        constraints=["Both streams are parameters."],
        input_description="A list of dicts and two streams.",
        expected_output="No return value; the streams carry the result.",
        example_input="report_fleet([{'name': 'r1', 'battery_pct': 12.0}], out, err)",
        example_output="out gets 'r1:12.0'; err gets a low-battery warning",
        edge_cases=["A missing name is reported as '<unnamed>'.", "A missing battery sends no data line.", "An empty list writes nothing."],
        hints=["Send the data line and the warning in separate statements, to different streams."],
        success_criteria=["Data appears only on out.", "A low battery produces a warning on err."],
        optional_extension="Add a final summary count to the error stream.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Parse simple command-line arguments",
        difficulty="HARD",
        learning_objectives=["Parse argv by hand.", "Report errors clearly."],
        concepts_tested=["strings", "sys.argv", "validation"],
        problem_statement=(
            "Write `parse_args(args)` returning a dict for '--name VALUE', '--count N' "
            "and a bare '--verbose'. Raise SystemExit with a message for an unknown "
            "flag or a missing value."
        ),
        requirements=["Iterate argv with an index, not slicing.", "Validate the count is a non-negative int."],
        constraints=["No argparse; parse by hand."],
        input_description="A list of argument strings, excluding the program name.",
        expected_output="A dict with keys name, count and verbose.",
        example_input="parse_args(['--name', 'rover-01'])",
        example_output="{'name': 'rover-01', 'count': 1, 'verbose': False}",
        edge_cases=["No arguments gives the defaults.", "'--count' with no value exits.", "'--count', 'x' exits."],
        hints=["Advance the index manually after consuming a value."],
        success_criteria=["['--name', 'rover-01'] parses correctly.", "An unknown flag exits with a message."],
        optional_extension="Support '--flag=value' as a single token.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Build a testable command-line entry point",
        difficulty="HARD",
        learning_objectives=["Compose parsing, I/O and exit codes.", "Keep the core pure."],
        concepts_tested=["sys.argv", "streams", "composition"],
        problem_statement=(
            "Write `main(argv, out, errors)` returning an exit code: 0 on success, 1 on "
            "an unknown command, 2 on a bad argument. It must print nothing directly, "
            "writing only to the streams it is given."
        ),
        requirements=["Map the result to an exit code.", "Never read sys.argv inside main."],
        constraints=["No global state; argv is a parameter."],
        input_description="Argument list and two streams.",
        expected_output="An integer exit code.",
        example_input="main(['status'], out, err)",
        example_output="0",
        edge_cases=["An empty argv returns 2.", "An unknown command returns 1.", "Success writes a line to out."],
        hints=["Parse first, then act, then return a code derived from the outcome."],
        success_criteria=["['status'] returns 0.", "An empty list returns 2."],
        optional_extension="Add a '--json' flag that emits machine-readable output.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "def format_table(rows) -> str:\n"
            "    lines = [f\"{'ROBOT':<10}{'BATTERY':>8}\", '-' * 18]\n"
            "    for name, pct in rows:\n"
            "        lines.append(f'{name:<10}{pct:>8.1f}')\n"
            "    return '\\n'.join(lines)"
        ),
        explanation=(
            "Each line is one f-string whose format spec states the alignment and width "
            "explicitly, so no manual padding is needed. Collecting the lines and joining "
            "once avoids the quadratic cost of repeated concatenation, and the header is "
            "emitted unconditionally so an empty table still has its labels."
        ),
        complexity="Time O(n) in the number of rows; space O(n).",
        edge_cases="An empty list returns just the header and separator.",
        alternative_approaches="Column widths could be computed from the data to right-size the table.",
        testing="out = format_table([('rover-01', 48.0)])\nassert 'ROBOT' in out and 'rover-01' in out\nassert format_table([]).startswith('ROBOT')",
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def parse_percent(text, default=None):\n"
            "    if isinstance(text, bool) or not isinstance(text, str):\n"
            "        raise TypeError(f'expected a string, got {type(text).__name__}')\n"
            "    cleaned = text.strip()\n"
            "    if cleaned.endswith('%'):\n"
            "        cleaned = cleaned[:-1].strip()\n"
            "    try:\n"
            "        return float(cleaned)\n"
            "    except ValueError:\n"
            "        return default"
        ),
        explanation=(
            "The type guard comes first so a float argument fails loudly rather than "
            "being silently stringified. Stripping the percent sign and then "
            "re-stripping handles ' 48.5 % ' where a single strip would leave a space "
            "that float() would then reject."
        ),
        complexity="Time O(n) in the text length; space O(n).",
        edge_cases="'n/a' returns the default; '48.5' without a sign parses normally.",
        alternative_approaches="Using str.removesuffix(' %') handles the spaced variant in one call.",
        testing="assert parse_percent('48.5%') == 48.5\nassert parse_percent(' 48.5 % ') == 48.5\nassert parse_percent('n/a', default=0.0) == 0.0",
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "def echo_lines(stream, prefix: str = '> ') -> list[str]:\n"
            "    echoed: list[str] = []\n"
            "    while True:\n"
            "        line = stream.readline()\n"
            "        if not line:\n"
            "            break\n"
            "        echoed.append(prefix + line.strip())\n"
            "    return echoed"
        ),
        explanation=(
            "The explicit read-then-check loop is clearer than a walrus condition here, "
            "because the end-of-input test is the interesting part and deserves its own "
            "line. A blank line yields an empty entry rather than terminating, so a file "
            "with intentional blank lines round-trips faithfully."
        ),
        complexity="Time O(n) in the stream; space O(n).",
        edge_cases="A final line without a trailing newline is still returned.",
        alternative_approaches="Iterating the stream directly avoids repeated readline calls.",
        testing="import io\nassert echo_lines(io.StringIO('a\\nb\\n')) == ['> a', '> b']\nassert echo_lines(io.StringIO('')) == []\nassert echo_lines(io.StringIO('a\\n\\nb\\n')) == ['> a', '> ', '> b']",
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "def banner(title: str, width: int = 24, fill: str = '=') -> str:\n"
            "    if width < 3:\n"
            "        raise ValueError('width must be at least 3')\n"
            "    if len(title) >= width:\n"
            "        return title\n"
            "    return title.center(width, fill)"
        ),
        explanation=(
            "The length guard returns the title untouched rather than truncating it, "
            "because a banner that silently drops part of a robot's name is worse than "
            "one that overflows its column. centre handles the padding, including the "
            "uneven left-right split for odd differences."
        ),
        complexity="Time O(n) in the width; space O(n).",
        edge_cases="A title exactly as long as the width is returned unchanged.",
        alternative_approaches="A format spec of ^<width also centres and never truncates.",
        testing="assert banner('ROBO-X') == '=========ROBO-X========='\nassert len(banner('x', 7)) == 7\nassert banner('a-very-long-title', 8) == 'a-very-long-title'",
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "CHOICES = {\n"
            "    'y': 'ARM',\n"
            "    'yes': 'ARM',\n"
            "    '1': 'ARM',\n"
            "    'true': 'ARM',\n"
            "    'n': 'DISARM',\n"
            "    'no': 'DISARM',\n"
            "    '0': 'DISARM',\n"
            "    'false': 'DISARM',\n"
            "}\n"
            "\n"
            "\n"
            "def normalise_choice(text: str):\n"
            "    if not isinstance(text, str):\n"
            "        return None\n"
            "    return CHOICES.get(text.strip().lower())"
        ),
        explanation=(
            "Normalising with strip().lower() before the lookup means aliases are "
            "written once in the table rather than in every comparison. dict.get "
            "returns None for an unrecognised answer, which lets the caller ask again "
            "instead of crashing on a typo."
        ),
        complexity="Time O(n) in the text length; space O(1).",
        edge_cases="An empty string returns None rather than raising.",
        alternative_approaches="A set of affirmative answers is enough if only yes/no is needed.",
        testing="assert normalise_choice(' Yes ') == 'ARM'\nassert normalise_choice('maybe') is None\nassert normalise_choice('') is None",
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "import io\n"
            "\n"
            "COMMANDS = {'1': 'ARM', '2': 'DISARM', 'q': 'QUIT'}\n"
            "\n"
            "\n"
            "def run_commands(stream, out, errors) -> list[str]:\n"
            "    history: list[str] = []\n"
            "    while True:\n"
            "        line = stream.readline()\n"
            "        if not line:\n"
            "            break\n"
            "        choice = line.strip().lower()\n"
            "        action = COMMANDS.get(choice)\n"
            "        if action is None:\n"
            "            print(f'unknown command: {choice!r}', file=errors)\n"
            "            continue\n"
            "        if action == 'QUIT':\n"
            "            break\n"
            "        history.append(action)\n"
            "        print(action, file=out)\n"
            "    return history"
        ),
        explanation=(
            "End of input is detected by the empty string readline returns, which is "
            "distinct from a blank line and correctly terminates the loop. Unknown "
            "commands write to the error stream and continue, so a typo never discards "
            "the decisions already made."
        ),
        complexity="Time O(n) in the commands; space O(n) in the history.",
        edge_cases="A stream with no trailing newline still terminates cleanly.",
        alternative_approaches="Iterating the stream directly is shorter and equally correct.",
        testing="out, err = io.StringIO(), io.StringIO()\nassert run_commands(io.StringIO('1\\nq\\n'), out, err) == ['ARM']\nassert run_commands(io.StringIO(''), out, err) == []",
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "import io\n"
            "from contextlib import redirect_stdout\n"
            "\n"
            "\n"
            "def capture_output(func, *args, **kwargs) -> str:\n"
            "    \"\"\"Run func with stdout redirected and return everything it printed.\"\"\"\n"
            "    buffer = io.StringIO()\n"
            "    with redirect_stdout(buffer):\n"
            "        func(*args, **kwargs)\n"
            "    return buffer.getvalue()"
        ),
        explanation=(
            "The context manager restores the original stream in a finally block, so an "
            "exception inside func leaves sys.stdout exactly as it was - which is the "
            "reason to prefer it over a manual save-and-restore. Taking *args and "
            "**kwargs lets the helper wrap any function, not just zero-argument ones."
        ),
        complexity="Time and space proportional to the output produced.",
        edge_cases="A function that prints nothing returns an empty string.",
        alternative_approaches="capsys in pytest does the same thing for test functions.",
        testing="assert capture_output(lambda: print('hi')) == 'hi\\n'\nassert capture_output(lambda: None) == ''",
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "import sys\n"
            "\n"
            "\n"
            "def report_fleet(robots, out=sys.stdout, errors=sys.stderr) -> None:\n"
            "    for robot in robots:\n"
            "        name = robot.get('name', '<unnamed>')\n"
            "        pct = robot.get('battery_pct')\n"
            "        if pct is None:\n"
            "            print(f'warning: {name} has no battery reading', file=errors)\n"
            "            continue\n"
            "        print(f'{name}:{pct:.1f}', file=out)\n"
            "        if pct < 20:\n"
            "            print(f'warning: {name} battery {pct:.1f}%', file=errors)"
        ),
        explanation=(
            "The data line and the warning go to different streams in separate "
            "statements, so a caller piping stdout to a file never captures a warning as "
            "if it were data. Continuing after a missing reading keeps one incomplete "
            "record from suppressing the rest of the fleet."
        ),
        complexity="Time O(n); space O(1).",
        edge_cases="A robot with no name is reported as '<unnamed>' rather than raising.",
        alternative_approaches="A generator of lines would be more testable but defers the stream decision.",
        testing="import io\nout, err = io.StringIO(), io.StringIO()\nreport_fleet([{'name': 'r1', 'battery_pct': 12.0}], out, err)\nassert out.getvalue() == 'r1:12.0\\n'\nassert 'low' in err.getvalue() or '12.0' in err.getvalue()",
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "import sys\n"
            "\n"
            "DEFAULTS = {'name': 'rover-01', 'count': 1, 'verbose': False}\n"
            "\n"
            "\n"
            "def parse_args(args) -> dict:\n"
            "    options = dict(DEFAULTS)\n"
            "    index = 0\n"
            "    while index < len(args):\n"
            "        token = args[index]\n"
            "        if token == '--verbose':\n"
            "            options['verbose'] = True\n"
            "        elif token in {'--name', '--count'}:\n"
            "            if index + 1 >= len(args):\n"
            "                sys.exit(f'{token} requires a value')\n"
            "            value = args[index + 1]\n"
            "            if token == '--name':\n"
            "                options['name'] = value\n"
            "            else:\n"
            "                try:\n"
            "                    count = int(value)\n"
            "                except ValueError:\n"
            "                    sys.exit(f'--count must be an integer, got {value!r}')\n"
            "                if count < 0:\n"
            "                    sys.exit('--count must not be negative')\n"
            "                options['count'] = count\n"
            "            index += 2\n"
            "            continue\n"
            "        else:\n"
            "            sys.exit(f'unknown argument: {token!r}')\n"
            "        index += 1\n"
            "    return options"
        ),
        explanation=(
            "Advancing the index by two after consuming a value is the part that is easy "
            "to get wrong with a naive increment; the continue keeps the two paths "
            "explicit. Validating the count separately from the conversion means a "
            "non-numeric and a negative value each get their own message."
        ),
        complexity="Time O(n) in the number of arguments; space O(1).",
        edge_cases="Repeating a flag is harmless; the last value wins for valued options.",
        alternative_approaches="argparse handles all of this, and is the right tool in Module 9.",
        testing="options = parse_args(['--name', 'rover-01'])\nassert options == {'name': 'rover-01', 'count': 1, 'verbose': False}\nassert parse_args([]) == DEFAULTS",
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "import sys\n"
            "\n"
            "EXIT_OK, EXIT_UNKNOWN, EXIT_USAGE = 0, 1, 2\n"
            "\n"
            "\n"
            "def main(argv, out=sys.stdout, errors=sys.stderr) -> int:\n"
            "    if not argv:\n"
            "        print('usage: roboctl <command>', file=errors)\n"
            "        return EXIT_USAGE\n"
            "    command = argv[0]\n"
            "    if command == 'status':\n"
            "        print('STATUS ACTIVE', file=out)\n"
            "        return EXIT_OK\n"
            "    if command == 'stop':\n"
            "        print('STOPPED', file=out)\n"
            "        return EXIT_OK\n"
            "    print(f'unknown command: {command!r}', file=errors)\n"
            "    return EXIT_UNKNOWN"
        ),
        explanation=(
            "Taking argv as a parameter is what makes this testable: a test supplies a "
            "list instead of mutating sys.argv. Returning distinct codes for usage "
            "errors and unknown commands lets a shell distinguish 'you called me wrong' "
            "from 'I do not know that'."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="An empty argv returns the usage code without touching stdout.",
        alternative_approaches="argparse would also set the exit code, at the cost of a global.",
        testing="import io\nout, err = io.StringIO(), io.StringIO()\nassert main(['status'], out, err) == 0\nassert main([], out, err) == 2\nassert main(['nope'], out, err) == 1",
    )
)

SOLUTIONS.append(
    solution(
        number=11,
        code=(
            "import io\n"
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
            "def rover_lines(robot) -> list[str]:\n"
            "    \"\"\"Render a machine-readable line per robot, ready to print.\"\"\"\n"
            "    state = robot.status()\n"
            "    return [f\"{state['name']}:{state['battery_pct']:.1f}\"]\n"
            "\n"
            "\n"
            "def dispatch(argv, out, errors) -> int:\n"
            "    \"\"\"Print the requested view; return an exit code. No globals touched.\"\"\"\n"
            "    if not argv:\n"
            "        print('usage: roverctl status', file=errors)\n"
            "        return 2\n"
            "    if argv[0] != 'status':\n"
            "        print(f\"unknown command: {argv[0]!r}\", file=errors)\n"
            "        return 1\n"
            "    robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\n"
            "    for line in rover_lines(robot):\n"
            "        print(line, file=out)\n"
            "    return 0"
        ),
        explanation=(
            "Separating rendering from printing means rover_lines can be asserted on "
            "without capturing any output at all, while dispatch owns the stream and "
            "exit-code decisions. The command never reads sys.argv itself, so the whole "
            "entry point is a pure function of its arguments."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="A missing argument returns 2 without producing output.",
        alternative_approaches="Passing the robot in as a parameter would make it testable with a double.",
        testing="out, err = io.StringIO(), io.StringIO()\nassert dispatch(['status'], out, err) == 0\nassert 'rover-01' in out.getvalue()\nassert dispatch([], out, err) == 2",
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="Where does `print('x')` send its text?",
        choices=[
            "Directly to the terminal hardware.",
            "To the object referenced by sys.stdout.",
            "To the standard error stream by default.",
            "To a file named out.txt in the working directory.",
        ],
        answer=1,
        kind="conceptual",
        explanation=(
            "print looks up sys.stdout at call time and writes to whatever object it "
            "currently references. Because that attribute can be rebound, redirecting "
            "it changes where every later print lands."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="What does `input('name: ')` return if the user types `42` and presses Enter?",
        choices=[
            "The string '42'.",
            "The integer 42.",
            "A float, because input converts automatically.",
            "None, because no name was supplied.",
        ],
        answer=0,
        kind="code_output",
        explanation=(
            "input always returns a string regardless of what was typed. The value must "
            "be converted explicitly before arithmetic, which is the source of the "
            "classic can-only-concatenate-str-to-str error."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="A script's output ends up inside telemetry.json along with its data. What is the fix?",
        choices=[
            "Call flush before every print.",
            "Send diagnostics to sys.stderr instead of stdout.",
            "Use f-strings for the messages.",
            "Close sys.stdout when finished.",
        ],
        answer=2,
        kind="debugging",
        explanation=(
            "The redirect captured everything on stdout, so the diagnostics became part "
            "of the data. The fix is the CLI contract: stdout carries results, stderr "
            "carries messages meant for a human."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="Why is a read loop that checks `if not line: break` necessary?",
        choices=[
            "It removes trailing whitespace from each line.",
            "It converts the line to a string.",
            "It skips blank lines in the middle of the input.",
            "An empty read is how end of input is signalled, distinct from a blank line.",
        ],
        answer=3,
        kind="identify_error",
        explanation=(
            "readline returns the empty string only at end of input; a blank line is "
            "returned as a newline. Without the check, a closed pipe turns a read loop "
            "into an infinite loop."
        ),
        reference="lesson.ipynb - Code Walkthrough",
    )
)

QUIZ.append(
    quiz(
        question="What does `contextlib.redirect_stdout` do?",
        choices=[
            "It permanently replaces sys.stdout for the process.",
            "It buffers printed output and discards it.",
            "It sends everything printed to sys.stderr.",
            "It swaps sys.stdout for a buffer for the duration of a with block.",
        ],
        answer=0,
        kind="reasoning",
        explanation=(
            "It rebinds sys.stdout for the block and restores it afterwards, even if the "
            "block raises. That is exactly what a test needs to assert on printed "
            "output without a terminal."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="Which format spec right-aligns a float in eight columns with one decimal?",
        choices=[
            "'>8f'",
            "'8.1f'",
            "'>8.1f'",
            "'*^8f'",
        ],
        answer=2,
        kind="multiple_choice",
        explanation=(
            "The alignment character comes first, then the minimum width, then the "
            "precision. '>8f' omits the precision and '8.1f' omits the alignment, so "
            "only '>8.1f' produces right alignment with a single decimal place."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="What is the correct way to build a large report line by line?",
        choices=[
            "Append each line to a string with += inside the loop.",
            "Append each line to a list and join once at the end.",
            "Call print inside the loop with end=''.",
            "Build a nested tuple of characters and flatten it.",
        ],
        answer=1,
        kind="code_output",
        explanation=(
            "Repeated += copies the accumulated string each time, making the loop "
            "quadratic in the number of lines. A list with append is amortised linear and "
            "a single join produces the same result."
        ),
        reference="lesson.ipynb - Pythonic Approaches",
    )
)

QUIZ.append(
    quiz(
        question="Which reason best justifies passing a stream as a parameter rather than calling print directly?",
        choices=[
            "It makes the function faster.",
            "It avoids the overhead of the print function.",
            "It lets a test capture the output without a terminal.",
            "It removes the need for string formatting.",
        ],
        answer=2,
        kind="implementation_choice",
        explanation=(
            "A stream parameter is the seam that makes console code testable: a test "
            "supplies a StringIO and asserts on the result. Performance is a side effect "
            "of the pattern, not its purpose."
        ),
        reference="exercises.ipynb - Exercise 10",
    )
)

QUIZ.append(
    quiz(
        question="Why does a long-running service appear to hang when its output is redirected to a file?",
        choices=[
            "File descriptors cannot be reused.",
            "Output is buffered and not flushed until the buffer fills or the process exits.",
            "Printing to a file is always slow.",
            "The interpreter disables buffering for files.",
        ],
        answer=1,
        kind="robotics",
        explanation=(
            "When stdout is not a terminal Python block-buffers it, so a service can sit "
            "in a sleep loop with nothing written yet. Passing flush=True, or running "
            "with python -u, restores the interactive behaviour."
        ),
        reference="lesson.ipynb - Debugging Techniques",
    )
)

QUIZ.append(
    quiz(
        question="A robot supervisor parses the output of a status command. Where should human warnings go?",
        choices=[
            "To sys.stderr, so the parsed stdout stays clean.",
            "To stdout, so the operator sees them in the terminal.",
            "To a third stream opened at the module level.",
            "To whichever stream is faster to write to.",
        ],
        answer=0,
        kind="robotics",
        explanation=(
            "The supervisor parses stdout, so any warning written there corrupts the "
            "data stream. stderr is not captured by the standard redirect, which makes it "
            "the correct home for diagnostics in a service."
        ),
        reference="solution.ipynb - Solution 8",
    )
)

MINI_PROJECT = {
    "title": "Mini-Project: Testable Console Tool",
    "brief": (
        "Build a small command-line tool for robot status that writes machine-readable "
        "results to stdout, human warnings to stderr, and can be tested with no terminal "
        "and no hardware."
    ),
    "scenario": (
        "You are writing the `roboctl` tool that a deployment script calls. The script "
        "redirects stdout to a file, so anything printed there is treated as data and a "
        "stray warning corrupts the report."
    ),
    "rationale": (
        "Nearly every robotics service begins as a console program. Designing it so that "
        "its streams and its arguments are injectable from the start is what keeps it "
        "testable as it grows."
    ),
    "requirements": [
        "Accept argv and both output streams as parameters.",
        "Support a 'status' command that prints one line per robot.",
        "Print warnings for low battery and for missing readings to stderr.",
        "Return exit code 0 for success, 1 for an unknown command, 2 for a usage error.",
        "Never read sys.argv or call input inside the tool's functions.",
    ],
    "constraints": [
        "Standard library only.",
        "No global state between calls.",
        "One line of stdout per robot, with no decoration.",
    ],
    "deliverables": [
        "`roboctl.py` with the command dispatch and the renderers.",
        "`test_roboctl.py` with at least ten assertions.",
        "A README section documenting the exit codes and the stream contract.",
    ],
    "steps": [
        "Write a renderer that turns a robot into a list of output lines.",
        "Write the command dispatch returning an exit code and writing only to streams.",
        "Capture stdout and stderr with StringIO in your tests.",
        "Test the success path, the unknown command and the usage error.",
        "Add a low-battery warning and a test for it.",
    ],
    "expected_behavior": (
        "roboctl status prints one parseable line per robot on stdout, any warnings on "
        "stderr, and exits 0. An unknown command exits 1; no arguments exits 2."
    ),
    "acceptance": [
        "All assertions pass from a clean run.",
        "stdout contains no warning text.",
        "Each exit code is verified by asserting on the return value.",
        "No function reads sys.argv or calls input.",
    ],
    "extensions": [
        "Add a --json flag that emits a machine-readable document.",
        "Add a 'watch' command that repeats until interrupted.",
        "Read the robot list from a JSON file rather than the simulator.",
    ],
}

RESEARCH = {
    "question": (
        "How much output volume can a console program emit before buffering becomes "
        "noticeable to a user?"
    ),
    "hypothesis": (
        "When stdout is redirected rather than attached to a terminal, a program must "
        "flush explicitly or the last output stays invisible until the process exits."
    ),
    "experiment": [
        STEPS(
            [
                "Write a script that prints a line every 50 milliseconds for three seconds.",
                "Run it once in a terminal and once with stdout redirected to a file.",
                "Record when each line actually appears using timestamps on the output.",
                "Repeat with flush=True on every print and record the difference.",
            ]
        ),
    ],
    "data": [
        CODE_CELL(
            "# Record your raw observations - one row per run variant.\n"
            "# Copy real values from your actual runs; do not invent them.\n"
            "#\n"
            "# | variant | lines visible at 1s | lines visible at exit |"
        ),
    ],
    "analysis": [
        MD(
            "Compare the three variants and state whether the hypothesis is supported. "
            "The interesting number is not the total but how much output was invisible "
            "while the process was still running."
        ),
    ],
    "result": [
        MD(
            "Report what you observed for each variant, including any case where the "
            "hypothesis did not hold, such as a short script that finished before the "
            "buffer filled."
        ),
    ],
    "interpretation": [
        MD(
            "Explain line buffering versus block buffering, and why a terminal gets one "
            "and a file gets the other. Name at least two threats to validity, "
            "including the write speed of the destination."
        ),
    ],
    "conclusion": [
        MD(
            "Give your verdict and state the rule you would adopt for a long-running "
            "robot service."
        ),
    ],
    "extensions": [
        "Compare PYTHONUNBUFFERED=1 with per-call flush.",
        "Measure the throughput cost of flushing on every line.",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Dispatch Console",
    "context": (
        "During warehouse AGV dispatch an operator drives the fleet from a console. "
        "The tool must never block on a human in a test, and its output must stay "
        "parseable for the supervisor that reads it."
    ),
    "mission": (
        "Implement `dispatch(stream, out, errors)` that reads commands from an injected "
        "stream, applies them to the simulator, and reports each decision on the "
        "correct stream."
    ),
    "requirements": [
        "Read commands from the supplied stream until quit or end of input.",
        "Print each applied command to stdout and each rejection to stderr.",
        "Return the list of decisions taken.",
        "Never call input() or read sys.stdin directly.",
    ],
    "constraints": [
        "No hardware required; use `shared/robo_x_sim`.",
        "An unreadable sensor must be reported, not swallowed.",
        "Complete well inside the 10 ms control budget per command.",
    ],
    "interface": "def dispatch(stream, out, errors) -> list[str]:",
    "success_criteria": [
        "A stream of 'status' then 'q' returns ['status'].",
        "An unknown command appears on the error stream only.",
        "An empty stream returns an empty list without raising.",
    ],
    "extension": (
        "Add a 'set-speed VALUE' command that validates the value and reports a "
        "rejection to stderr rather than crashing."
    ),
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Reframe I/O as objects that can be replaced.",
        "Install the stdout/stderr contract as a habit.",
        "Show that a console program can be fully tested with no terminal present.",
    ],
    "misconceptions": [
        [
            "print writes to the screen.",
            "It writes to sys.stdout, which is usually the screen but need not be.",
        ],
        [
            "input converts what the user types to a number.",
            "It always returns a string, whatever was typed.",
        ],
        [
            "A blank line ends a read loop.",
            "Only an empty read signals end of input; a blank line is data.",
        ],
        [
            "Building a report with += is fine.",
            "Repeated concatenation is quadratic; collect and join instead.",
        ],
    ],
    "difficult_concepts": [
        "Understanding that rebinding sys.stdout changes every later print.",
        "Distinguishing an empty read from an empty line.",
        "Seeing why stream parameters make a function testable rather than merely tidy.",
    ],
    "demonstrations": [
        "Redirect stdout to a StringIO, print, and show the terminal stays empty.",
        "Show a read loop that spins forever on a closed pipe without the empty check.",
        "Run a script with 1> and 2> to show the two streams separating.",
    ],
    "discussion": [
        "Why do operating systems provide two output streams instead of one?",
        "When would printing a warning to stdout be the right choice?",
    ],
    "student_errors": [
        [
            "The kernel hangs in a notebook",
            "input() is waiting for a human who is not there",
            "Read from a StringIO instead",
        ],
        [
            "A JSON file contains warning text",
            "Diagnostics were printed to stdout",
            "Send warnings to sys.stderr",
        ],
        [
            "A loop never terminates on piped input",
            "No end-of-input check",
            "Break when readline returns the empty string",
        ],
    ],
    "pacing": (
        "90 minutes of lesson with live redirection, then 2 hours on exercises. Spend "
        "time on the redirect_stdout demonstration; it reframes testing for the whole course."
    ),
    "extensions": [
        "Ask students to add a --json flag and assert on parsed output in a test.",
        "Have them measure the quadratic versus linear cost of building a report.",
    ],
    "assessment": (
        "Grade against rubric.md. Exercises 7 to 10 carry the signal: they require the "
        "student to inject streams and think in terms of the CLI contract."
    ),
    "support": (
        "Provide a helper that runs a function with both streams captured, so students "
        "can assert on output from their very first attempt.",
    ),
    "extension_fast": (
        "Ask for a design note on how the same tool would behave when stdout is a pipe "
        "to another process rather than a file.",
    ),
}

RUBRIC = {
    "artifacts": [
        ["exercises.ipynb", "40%", "All 10 exercises implemented and edge-cased."],
        ["mini_project.ipynb", "25%", "roboctl.py plus its test suite."],
        ["robotics_challenge.ipynb", "25%", "Dispatch console stays parseable."],
        ["research.ipynb", "10%", "Real measurements with a defensible conclusion."],
    ],
    "criteria": [
        ["Correctness", "30", "Rendering, parsing and exit codes behave as specified."],
        ["Stream discipline", "25", "Data on stdout, diagnostics on stderr, both injectable."],
        ["Code quality", "25", "PEP 8 naming, docstrings, small focused functions."],
        ["Reasoning", "20", "Buffering and quadratic-cost claims explained in writing."],
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
            "Every exercise implemented, stdout stays free of warnings, and every exit "
            "code is asserted without touching sys.argv or input.",
        ],
        [
            "Merit",
            "Most exercises correct; streams are injected but one warning path still "
            "writes to stdout and is untested.",
        ],
        [
            "Pass",
            "Core requirements met, but the code calls input directly and therefore "
            "cannot be tested.",
        ],
        [
            "Fail",
            "Output streams are mixed, or a read loop spins forever on end of input.",
        ],
    ],
}

TOPIC = topic(
    topic_id="1.7",
    title="Basic Input/Output",
    module=1,
    module_title="Getting Started with Python",
    directory="07_basic_input_output",
    summary=(
        "I/O in Python is an object you can replace. This topic covers print and the "
        "format specification, the stdout/stderr contract, and the redirection technique "
        "that makes console programs testable without a terminal."
    ),
    why_it_matters=(
        "Every robotics service begins as a console program, and a deployment script "
        "usually captures its output. Getting the two streams right is what makes "
        "`service > state.json` produce something a parser can read, and passing the "
        "stream in is what makes the program testable at all."
    ),
    objectives=[
        "Explain that print writes to sys.stdout and input reads from sys.stdin.",
        "Redirect a stream to capture output in a test.",
        "Format aligned columns with f-string format specifications.",
        "Apply the stdout/stderr contract to a reporting function.",
        "Detect end of input correctly in a read loop.",
        "Build a report without quadratic string concatenation.",
    ],
    prerequisites=[
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
    robo_x_milestone="M1",
    robo_x_package="robo_x.core",
)
