"""Topic 1.8 - Writing and Running Your First Scripts.

Hand-authored to the Course Content Standard. The spine: a file becomes a program
only when it is executed directly, and the main guard is what keeps it importable
at the same time.
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
        "Every Python file is a **module**. It only becomes a **program** when the "
        "interpreter runs it as the top-level script, and the interpreter tells you "
        "which case you are in through the module-level name `__name__`. Importing a "
        "file sets it to the module's own name; executing it directly sets it to "
        "`\"__main__\"`. The `if __name__ == \"__main__\":` guard is the idiom that uses "
        "that distinction."
    ),
    CODE_CELL(
        "def demo() -> str:\n"
        "    return f'running as {__name__}'\n"
        "\n"
        "\n"
        "print(demo())\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    print('this block only runs when executed directly')"
    ),
    MD(
        "Without the guard, importing a module runs its top-level code. For a library "
        "that is merely wasteful; for a script that starts a robot, it is dangerous - "
        "a test that imports the module would launch the hardware. The guard is "
        "therefore not a stylistic preference but a safety boundary."
    ),
    CODE_CELL(
        "import sys\n"
        "\n"
        "print('argv as seen by this program:')\n"
        "for index, value in enumerate(sys.argv):\n"
        "    print(f'  [{index}] {value!r}')\n"
        "\n"
        "print('the name this module is running as:', __name__)"
    ),
    NOTE(
        "sys.argv[0] is the program, not a parameter",
        "The first element is the path used to invoke the script, and the rest are the "
        "arguments. Slicing from index 1 is the single most common early mistake, and "
        "it usually shows up as an off-by-one that only appears with zero arguments."
    ),
]

LESSON["formal_theory"] = [
    MD(
        "Running a script has four stages: the interpreter starts, the file is compiled "
        "to bytecode, the module is executed top to bottom with `__name__` set to "
        "`\"__main__\"`, and the resulting exit status is handed back to the shell. The "
        "exit status comes from the value passed to `SystemExit`, or from an uncaught "
        "exception, and defaults to zero."
    ),
    EQUATION(
        "python script.py args...  ->  exit 0 on success, non-zero on SystemExit(n) or an uncaught error"
    ),
    MD(
        "The shell is part of the contract. A script is often launched by another "
        "program rather than a person, and that caller can only see three things: the "
        "exit code, stdout, and stderr. Everything a caller needs to branch on must "
        "appear in one of those three, which is why the exit code and the stream "
        "discipline from Topic 1.7 matter here."
    ),
    CODE_CELL(
        "import subprocess\n"
        "import sys\n"
        "\n"
        "result = subprocess.run(\n"
        "    [sys.executable, '-c', 'import sys; sys.exit(3)'],\n"
        "    capture_output=True,\n"
        "    text=True,\n"
        ")\n"
        "print('returncode:', result.returncode)\n"
        "print('succeeded :', result.returncode == 0)\n"
        "\n"
        "boom = subprocess.run(\n"
        "    [sys.executable, '-c', 'raise SystemExit(\"bad config\")'],\n"
        "    capture_output=True,\n"
        "    text=True,\n"
        ")\n"
        "print('message   :', boom.stderr.strip())"
    ),
    TABLE(
        ["Stage", "What happens", "How to observe it"],
        [
            ["Start", "The interpreter initialises", "`sys.executable`"],
            ["Compile", "Source becomes bytecode", "A SyntaxError stops here"],
            ["Execute", "Top-level statements run", "`__name__` is `'__main__'`"],
            ["Exit", "A status reaches the shell", "The process return code"],
        ],
    ),
]

LESSON["syntax"] = [
    MD(
        "A runnable script has three parts: an optional shebang so the shell knows the "
        "interpreter, a docstring, and a guarded entry point."
    ),
    CODE_CELL(
        "#!/usr/bin/env python3\n"
        "\"\"\"A minimal, well-formed command-line script.\"\"\"\n"
        "from __future__ import annotations\n"
        "\n"
        "import sys\n"
        "\n"
        "\n"
        "def main(argv: list[str]) -> int:\n"
        "    \"\"\"Return the process exit status.\"\"\"\n"
        "    if len(argv) < 2:\n"
        "        print('usage: script.py <name>', file=sys.stderr)\n"
        "        return 2\n"
        "    print(f'hello, {argv[1]}')\n"
        "    return 0\n"
        "\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    main(sys.argv)"
    ),
    NOTE(
        "Why this cell calls main() instead of sys.exit(main())",
        "A real script ends with `sys.exit(main(sys.argv))` so the shell receives the "
        "status. Running that inside a notebook would terminate the kernel, so the cell "
        "calls main() directly. Use the SystemExit form in the scripts you write later.",
    ),
    MD("The anti-pattern:"),
    CODE(
        "import sys\n"
        "robot = SimulatedRobot()\n"
        "robot.move(10)\n"
        "print('done')\n"
        "\n"
        "# everything above runs on import, including the movement\n"
        "def main():\n"
        "    ...\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    main()",
        lang="text",
    ),
    WARN(
        "Do not call sys.exit deep inside logic",
        "SystemExit is an exception: raising it from a helper unwinds the whole stack. "
        "Return a status from main and exit once, at the bottom, where the intent is clear.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - separating the program name from the arguments.**"),
    CODE_CELL(
        "import sys\n"
        "\n"
        "\n"
        "def arguments(argv: list[str]) -> list[str]:\n"
        "    \"\"\"Drop argv[0], which is the program path, not an argument.\"\"\"\n"
        "    return list(argv[1:])\n"
        "\n"
        "\n"
        "print('full   :', sys.argv)\n"
        "print('args   :', arguments(sys.argv))\n"
        "print('joined :', ' '.join(arguments(sys.argv)))"
    ),
    MD("**Example 2 - compiling a source string before running it.**"),
    CODE_CELL(
        "source = 'value = 6 * 7\\nresult = value\\n'\n"
        "namespace: dict = {}\n"
        "code = compile(source, '<demo>', 'exec')\n"
        "exec(code, namespace)\n"
        "print('compiled and executed ->', namespace['result'])"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "Running a child process is how one script launches another, and it is also the "
        "cleanest way to see your own exit-code contract from the outside."
    ),
    CODE_CELL(
        "import subprocess\n"
        "import sys\n"
        "\n"
        "\n"
        "def run(script_args: list[str]) -> tuple[int, str]:\n"
        "    result = subprocess.run(\n"
        "        [sys.executable, '-c', 'import sys; print(sys.argv[1:])'] + script_args,\n"
        "        capture_output=True,\n"
        "        text=True,\n"
        "        timeout=5,\n"
        "    )\n"
        "    return result.returncode, result.stdout.strip()\n"
        "\n"
        "\n"
        "print(run(['a', 'b']))\n"
        "print(run([]))"
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "`runpy` executes a module by name with control over whether it sees itself as "
        "`__main__`, which is exactly what you need to test a script's entry point "
        "without launching it in a shell."
    ),
    CODE_CELL(
        "import runpy\n"
        "import sys\n"
        "\n"
        "captured = {}\n"
        "original = sys.argv\n"
        "sys.argv = ['demo.py']\n"
        "try:\n"
        "    runpy.run_path('01_getting_started/08_writing_running_first_scripts/README.md',\n"
        "                  run_name='__demo__')\n"
        "except (FileNotFoundError, IsADirectoryError, SyntaxError) as exc:\n"
        "    captured['error'] = type(exc).__name__\n"
        "finally:\n"
        "    sys.argv = original\n"
        "\n"
        "print('run_name controls __name__; failures surface as:', captured)"
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "Below is a complete, runnable command-line tool. It is the shape every later "
        "module's exercises eventually take: parse, act, return a status."
    ),
    CODE_CELL(
        "\"\"\"roboctl.py - a small fleet control tool.\"\"\"\n"
        "from __future__ import annotations\n"
        "\n"
        "import sys\n"
        "\n"
        "EXIT_OK, EXIT_UNKNOWN, EXIT_USAGE = 0, 1, 2\n"
        "COMMANDS = ('status', 'stop', 'help')\n"
        "\n"
        "\n"
        "def render_status() -> str:\n"
        "    return 'rover-01:ACTIVE:48.0'\n"
        "\n"
        "\n"
        "def run(argv: list[str], out=sys.stdout, errors=sys.stderr) -> int:\n"
        "    \"\"\"Dispatch one command. Writes only to the streams it is given.\"\"\"\n"
        "    if not argv:\n"
        "        print(f'usage: roboctl <{\"|\".join(COMMANDS)}>', file=errors)\n"
        "        return EXIT_USAGE\n"
        "    command = argv[0]\n"
        "    if command == 'help':\n"
        "        print(f'usage: roboctl <{\"|\".join(COMMANDS)}>', file=out)\n"
        "        return EXIT_OK\n"
        "    if command == 'status':\n"
        "        print(render_status(), file=out)\n"
        "        return EXIT_OK\n"
        "    if command == 'stop':\n"
        "        print('stopped', file=out)\n"
        "        return EXIT_OK\n"
        "    print(f'unknown command: {command!r}', file=errors)\n"
        "    return EXIT_UNKNOWN\n"
        "\n"
        "\n"
        "def main() -> int:\n"
        "    return run(sys.argv[1:])\n"
        "\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    main()"
    ),
    MD(
        "Three properties make this testable. `run` takes argv and both streams as "
        "parameters, so no test needs a subprocess. `render_status` is a pure function "
        "that returns a line, so its output can be asserted directly. And the exit code "
        "is returned rather than raised, so the same function serves a shell and a test."
    ),
    NOTE(
        "Why the guard calls main() and not sys.exit(main())",
        "A real script ends with `sys.exit(main())` so the shell receives the status. "
        "Running that in a notebook would terminate the kernel, so this cell calls "
        "`main()` and simply prints what it returned. Use the SystemExit form in the "
        "command-line tools you build later in the course.",
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "The exit codes are named constants, so a caller and a test refer to the "
            "same meaning rather than to a bare integer.",
            "COMMANDS is a tuple used only for the usage message, keeping the accepted "
            "set visible in one place.",
            "render_status returns a string and prints nothing, which is what makes the "
            "output assertable without capturing a stream.",
            "run takes argv and both streams as parameters, so a test supplies them "
            "directly instead of spawning a process.",
            "argv[0] is the subcommand because the caller already passed sys.argv[1:] - "
            "this is where the off-by-one is avoided.",
            "Each branch returns its own status, so the caller never has to infer success "
            "from printed text.",
            "main is a two-line adapter whose only job is to turn process state into "
            "arguments for run.",
            "The guard at the bottom converts that returned status into the process exit "
            "code, in exactly one place.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - forgetting the main guard.**"),
    CODE(
        "import sys\n"
        "print('starting')\n"
        "sys.exit(main())      # runs on import, killing the importing process\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    sys.exit(main())",
        lang="text",
    ),
    MD("**Mistake 2 - treating argv[0] as an argument.**"),
    CODE(
        "name = sys.argv[0]     # this is the program path\n"
        "name = sys.argv[1]     # only if an argument was actually passed\n"
        "\n"
        "args = sys.argv[1:]    # the correct general form",
        lang="text",
    ),
    MD("**Mistake 3 - calling sys.exit inside a helper.**"),
    CODE(
        "def load(path):\n"
        "    if not exists(path):\n"
        "        sys.exit(1)      # unwinds the whole stack\n"
        "    return open(path)\n"
        "\n"
        "def load(path):\n"
        "    if not exists(path):\n"
        "        raise FileNotFoundError(path)",
        lang="text",
    ),
    MD("**Mistake 4 - printing the only error message.**"),
    CODE(
        "print('error: bad config')          # a caller cannot detect this\n"
        "sys.exit(2)                        # and the status is lost\n"
        "\n"
        "print('error: bad config', file=sys.stderr)\n"
        "sys.exit(2)                        # now both channels say it",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "The first question about a script that behaves oddly when launched is whether "
        "it behaves differently when imported. That single check distinguishes a main "
        "guard bug from everything else."
    ),
    CODE_CELL(
        "def probe() -> dict:\n"
        "    \"\"\"Return what this module believes about its own execution.\"\"\"\n"
        "    import sys\n"
        "    return {'name': __name__, 'argv0': sys.argv[0]}\n"
        "\n"
        "\n"
        "print('as executed:', probe())\n"
        "print('argv0 is the path that started this program')"
    ),
    MD(
        "To see a script's exit code from another program, run it as a subprocess rather "
        "than importing it - that is the only way to observe the contract a shell would "
        "see."
    ),
    CODE_CELL(
        "import subprocess\n"
        "import sys\n"
        "\n"
        "for code in ('0', '2', '7'):\n"
        "    result = subprocess.run(\n"
        "        [sys.executable, '-c', f'import sys; sys.exit({code})'],\n"
        "        capture_output=True,\n"
        "        text=True,\n"
        "    )\n"
        "    print(f'asked for {code} -> shell sees {result.returncode}')"
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Guard the entry point with `if __name__ == '__main__':` in every script.",
            "Pass `sys.argv[1:]` into a function; never index it inside the logic.",
            "Return an exit status from main and call sys.exit exactly once.",
            "Use named exit-code constants so callers and tests share a meaning.",
            "Take streams as parameters so the tool can be tested without a subprocess.",
            "Report errors on stderr *and* return a non-zero status.",
            "Start with a shebang and a docstring so the file is self-describing.",
            "Keep a shebang as `#!/usr/bin/env python3` so it works across machines.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "Interpreter start-up is the fixed cost of every script, and it is larger than "
        "most beginners expect: importing the interpreter and reaching your first "
        "statement typically costs tens of milliseconds. For a script invoked once per "
        "second by a supervisor, that is negligible. For one invoked in a tight loop, or "
        "on a control path, it is not - and the answer is a resident service or a "
        "compiled tool, not a faster script."
    ),
    MD(
        "Within the script, the usual cost centres apply: importing a large library at "
        "module level when the script may exit early, and building a large data structure "
        "before discovering there is nothing to do. Deferring an expensive import into "
        "the branch that needs it, and checking for empty input before building output, "
        "are the two changes that pay off most often in small tools."
    ),
    TIP(
        "Measure start-up, not micro-steps",
        "Time `python -c pass` to establish the floor, then time your script. The "
        "difference is what your code costs, and it is the only number worth discussing.",
    ),
]

LESSON["pythonic_approaches"] = [
    MD("Scanning argv: a manual index loop versus membership tests."),
    CODE_CELL(
        "args = ['--verbose', '--name', 'rover-01', '--count', '3']\n"
        "\n"
        "# before: manual index arithmetic\n"
        "verbose = False\n"
        "name = None\n"
        "index = 0\n"
        "while index < len(args):\n"
        "    if args[index] == '--verbose':\n"
        "        verbose = True\n"
        "        index += 1\n"
        "    elif args[index] == '--name' and index + 1 < len(args):\n"
        "        name = args[index + 1]\n"
        "        index += 2\n"
        "    else:\n"
        "        index += 1\n"
        "\n"
        "# after: say what you are looking for, and let the language scan\n"
        "verbose = '--verbose' in args\n"
        "name = args[args.index('--name') + 1] if '--name' in args else None\n"
        "print('verbose:', verbose, '| name:', name)"
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "A fleet supervisor launches robot services exactly the way a shell does: as "
        "child processes whose exit status decides whether the robot is allowed to "
        "proceed. That is why a correct exit code, and a non-zero one on failure, is a "
        "safety feature rather than a formality."
    ),
    CODE_CELL(
        "import subprocess\n"
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
        "print(f\"{state['name']}:{state['battery_pct']:.1f}\")\n"
        "\n"
        "# a supervisor sees only this: the status and the two streams\n"
        "failed = subprocess.run(\n"
        "    [sys.executable, '-c', 'import sys; sys.exit(1)'],\n"
        "    capture_output=True,\n"
        ")\n"
        "print('child failed ->', failed.returncode != 0)"
    ),
]

LESSON["engineering_example"] = [
    MD(
        "A dispatch function that is pure with respect to the process: everything it "
        "needs arrives as an argument."
    ),
    CODE_CELL(
        "import sys\n"
        "\n"
        "EXIT_OK, EXIT_UNKNOWN, EXIT_USAGE = 0, 1, 2\n"
        "COMMANDS = ('status', 'stop', 'help')\n"
        "\n"
        "\n"
        "def dispatch(argv, out=sys.stdout, errors=sys.stderr) -> int:\n"
        "    \"\"\"Run one command; return the exit status a shell would observe.\"\"\"\n"
        "    if not argv:\n"
        "        print(f'usage: roboctl <{\"|\".join(COMMANDS)}>', file=errors)\n"
        "        return EXIT_USAGE\n"
        "    command = argv[0]\n"
        "    if command not in COMMANDS:\n"
        "        print(f'unknown command: {command!r}', file=errors)\n"
        "        return EXIT_UNKNOWN\n"
        "    if command == 'help':\n"
        "        print(f'usage: roboctl <{\"|\".join(COMMANDS)}>', file=out)\n"
        "    else:\n"
        "        print(f'{command}: ok', file=out)\n"
        "    return EXIT_OK"
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Write a module that prints something at import time, then add the main guard "
            "and import it again to see the difference.",
            "Write `arguments(argv)` that returns everything after the program name, and "
            "test it with an empty list.",
            "Run a child process that exits with 3 and confirm the return code you "
            "observe.",
            "Write `dispatch(argv)` returning 0, 1 and 2 for success, unknown command and "
            "missing argument.",
        ]
    ),
    CODE_CELL(
        "import subprocess\n"
        "import sys\n"
        "\n"
        "\n"
        "def arguments(argv):\n"
        "    return list(argv[1:])\n"
        "\n"
        "\n"
        "print('args of []  ->', arguments([]))\n"
        "print('args of [a] ->', arguments(['prog', 'a']))\n"
        "\n"
        "child = subprocess.run(\n"
        "    [sys.executable, '-c', 'import sys; sys.exit(3)'],\n"
        "    capture_output=True,\n"
        ")\n"
        "print('child exit code ->', child.returncode)\n"
        "\n"
        "print('this module is running as', __name__)"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: a file has two personalities and one switch.** Imported, it is "
        "a library that offers things and does nothing. Executed, it is a program that "
        "acts. `__name__` is the switch, and the main guard is the switch's housing. "
        "Everything else in this topic - argv, exit codes, streams - is the contract "
        "between that program and whoever started it."
    ),
    TABLE(
        ["", "Imported", "Executed directly"],
        [
            ["`__name__`", "the module's own name", "`'__main__'`"],
            ["Top-level code", "runs", "runs"],
            ["Guarded code", "skipped", "runs"],
            ["Exit code", "irrelevant", "handed to the shell"],
            ["Reusable", "yes", "no"],
        ],
    ),
]

TERMS = [
    ["Script", "A file executed directly by the interpreter as a program."],
    ["Module", "Any importable Python file, including a script."],
    ["`__name__`", "The name a module is known by; `'__main__'` when executed directly."],
    ["Main guard", "The `if __name__ == '__main__':` block protecting side effects."],
    ["Shebang", "The first line naming the interpreter for the shell."],
    ["`sys.argv`", "The list of command-line arguments, program path first."],
    ["Exit code", "The integer status a process hands back to the shell."],
    ["`SystemExit`", "The exception that ends a process with a status."],
    ["argv[0]", "The path used to invoke the script, not an argument."],
    ["Subprocess", "A child process, observed through its streams and return code."],
]

LESSON["summary"] = [
    MD(
        "Every Python file is a module; it becomes a program only when executed "
        "directly, and `__name__` is how the interpreter tells the two cases apart. The "
        "main guard is therefore not ceremony. Without it, importing a file runs its "
        "top-level code, which for a robotics script means a test that imports the "
        "module launches the robot."
    ),
    MD(
        "The second half of the topic is the contract with whoever started the process. "
        "That caller - a shell, a supervisor, a CI job - can see only three things: the "
        "exit code, stdout and stderr. So every decision the caller needs to make must "
        "appear in one of them. Return a status from main, call `sys.exit` once at the "
        "bottom, print results to stdout and problems to stderr, and your tool composes "
        "with everything else on the machine."
    ),
    MD(
        "The practical habit is to keep the process at arm's length. Write the real work "
        "as a function that takes its arguments and its streams as parameters, and let a "
        "two-line `main` translate process state into those arguments. That is why the "
        "tool in the walkthrough can be tested with a StringIO and no subprocess, while "
        "still behaving exactly as it would in a shell."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "Every file is a module; only direct execution makes it a program.",
            "`__name__` is `'__main__'` only when executed directly.",
            "Guard side effects so importing a script cannot launch it.",
            "`sys.argv[0]` is the program path, not an argument.",
            "Pass `sys.argv[1:]` into a function rather than indexing it inline.",
            "Return an exit status from main and call sys.exit once.",
            "Results go to stdout, problems to stderr, status to the exit code.",
            "Take streams and argv as parameters so the tool is testable.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "[`if __name__ == '__main__'`: a gotcha](https://stackoverflow.com/questions/419163/what-does-if-name-main-do)",
            "[sys.argv and the command line](https://docs.python.org/3/library/sys.html#sys.argv)",
            "[SystemExit](https://docs.python.org/3/library/exceptions.html#SystemExit)",
            "[subprocess - running child processes](https://docs.python.org/3/library/subprocess.html)",
            "[PEP 8 - shebangs and module structure](https://peps.python.org/pep-0008/)",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Separate the program path from the arguments",
        difficulty="MEDIUM",
        learning_objectives=["Use sys.argv correctly.", "Avoid the off-by-one."],
        concepts_tested=["sys.argv", "slicing", "lists"],
        problem_statement=(
            "Write `arguments(argv)` returning every element after the program path, so "
            "`['script.py', 'a', 'b']` gives `['a', 'b']` and `['script.py']` gives `[]`."
        ),
        requirements=["Never raise for a short list.", "Return a new list."],
        constraints=["Do not mutate the input."],
        input_description="A list shaped like sys.argv.",
        expected_output="A list of the arguments.",
        example_input="arguments(['script.py', 'a', 'b'])",
        example_output="['a', 'b']",
        edge_cases=["A single-element list gives an empty list.", "An empty list gives an empty list."],
        hints=["Slicing from index 1 handles every length without a special case."],
        success_criteria=["['script.py', 'a'] gives ['a'].", "[] gives []."],
        optional_extension="Raise IndexError instead when the program path is missing.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Report the program name",
        difficulty="MEDIUM",
        learning_objectives=["Extract a file name.", "Handle a missing path."],
        concepts_tested=["pathlib", "strings"],
        problem_statement=(
            "Write `program_name(argv)` returning the file name of the program path "
            "with any directory or extension removed, so `['/opt/roboctl.py']` gives "
            "'roboctl' and `[]` gives 'python'."
        ),
        requirements=["Use pathlib rather than string splitting.", "Handle an empty argv."],
        constraints=["Never raise for an empty list."],
        input_description="A list shaped like sys.argv.",
        expected_output="A string.",
        example_input="program_name(['/opt/roboctl.py'])",
        example_output="'roboctl'",
        edge_cases=["An empty argv gives 'python'.", "A path with no extension is returned as-is.", "A bare name is returned unchanged."],
        hints=["Path.stem removes the suffix and Path.name removes the directory."],
        success_criteria=["'/opt/roboctl.py' gives 'roboctl'.", "[] gives 'python'."],
        optional_extension="Return the full path as well.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Detect a boolean flag",
        difficulty="MEDIUM",
        learning_objectives=["Search a sequence.", "Keep a boolean flag separate from values."],
        concepts_tested=["membership", "lists", "validation"],
        problem_statement=(
            "Write `has_flag(args, flag)` returning True when the exact token appears in "
            "the argument list. An empty list or an empty flag returns False."
        ),
        requirements=["Match the whole token, not a substring.", "Never raise."],
        constraints=["Reject non-string arguments with TypeError."],
        input_description="An argument list and a flag string.",
        expected_output="A boolean.",
        example_input="has_flag(['--verbose', '--name'], '--verbose')",
        example_output="True",
        edge_cases=["An empty flag returns False.", "'--verb' is not matched by '--verbose'.", "An empty list returns False."],
        hints=["The `in` operator on a list compares whole elements."],
        success_criteria=["Finds --verbose in the example.", "Does not match a longer token."],
        optional_extension="Return the position of the flag, or -1.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Map a status name to an exit code",
        difficulty="MEDIUM",
        learning_objectives=["Use a lookup table.", "Design a public contract."],
        concepts_tested=["dicts", "error handling"],
        problem_statement=(
            "Write `exit_code_for(name)` mapping 'ok' to 0, 'unknown' to 1 and 'usage' to "
            "2. Raise KeyError for any other name."
        ),
        requirements=["Use a module-level table.", "Return an int."],
        constraints=["Do not special-case individual names in code."],
        input_description="One of the three status names.",
        expected_output="An integer exit code.",
        example_input="exit_code_for('usage')",
        example_output="2",
        edge_cases=["An unknown name raises KeyError.", "The mapping is the same for every call."],
        hints=["A dict from name to code is the whole implementation."],
        success_criteria=["'ok' gives 0.", "'nope' raises KeyError."],
        optional_extension="Add a reverse lookup from code back to name.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Build a usage line",
        difficulty="MEDIUM",
        learning_objectives=["Compose a message.", "Use join."],
        concepts_tested=["strings", "join", "f-strings"],
        problem_statement=(
            "Write `usage_line(program, commands)` returning "
            "`'usage: roboctl <status|stop|help>'` with the commands joined by a pipe."
        ),
        requirements=["Join the commands with '|'.", "Handle an empty command list."],
        constraints=["Return the string; do not print."],
        input_description="A program name and a list of command names.",
        expected_output="A usage line.",
        example_input="usage_line('roboctl', ['status', 'stop'])",
        example_output="'usage: roboctl <status|stop>'",
        edge_cases=["An empty list still shows the angle brackets.", "A long list wraps nothing; it simply grows."],
        hints=["'|'.join(commands) does the work."],
        success_criteria=["Produces the example output exactly.", "An empty list still contains the brackets."],
        optional_extension="Add an optional positional-argument note.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Split an inline option token",
        difficulty="HARD",
        learning_objectives=["Parse a compound token.", "Handle a missing value."],
        concepts_tested=["strings", "partition", "validation"],
        problem_statement=(
            "Write `split_option(token)` returning `(name, value)` for '--name=rover-01' "
            "and `(token, None)` for a bare '--verbose'. Raise ValueError for a token "
            "with an empty name or an empty value."
        ),
        requirements=["Split on the first '=' only.", "Reject a bare token that is not a flag."],
        constraints=["A token not starting with '--' raises ValueError."],
        input_description="A single argument token.",
        expected_output="A tuple of name and value or None.",
        example_input="split_option('--name=rover-01')",
        example_output="('--name', 'rover-01')",
        edge_cases=["'--name=' raises ValueError.", "'name' raises ValueError.", "'--a=b=c' splits at the first '='."],
        hints=["partition('=') splits once and reports whether a separator was found."],
        success_criteria=["Splits the example correctly.", "Raises ValueError for a token with no leading dashes."],
        optional_extension="Accept the ':' separator as well.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Parse flags and options with an index",
        difficulty="HARD",
        learning_objectives=["Walk argv correctly.", "Consume a value safely."],
        concepts_tested=["loops", "indexing", "validation"],
        problem_statement=(
            "Write `parse_args(args)` returning a dict for '--name VALUE', '--count N' "
            "and '--verbose', collecting every message for an unknown flag, a missing "
            "value or a bad count rather than stopping at the first."
        ),
        requirements=["Advance the index manually after a value.", "Report every problem."],
        constraints=["Never raise for bad input."],
        input_description="A list of argument strings.",
        expected_output="A tuple of options dict and sorted error messages.",
        example_input="parse_args(['--verbose', '--name', 'rover-01'])",
        example_output="({'name': 'rover-01', 'count': 1, 'verbose': True}, [])",
        edge_cases=["An empty list gives the defaults.", "'--count' with no value is reported.", "'--count', 'x' is reported."],
        hints=["Keep an index and increment it by two after consuming a value."],
        success_criteria=["Parses the example correctly.", "Reports two problems in one call."],
        optional_extension="Support the '--key=value' form via split_option.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Run a child process and observe its result",
        difficulty="HARD",
        learning_objectives=["Launch a subprocess.", "Read all three channels."],
        concepts_tested=["subprocess", "sys", "streams"],
        problem_statement=(
            "Write `run_python(code, args=())` running the given source in a child "
            "interpreter and returning `(returncode, stdout, stderr)` as strings. Pass "
            "the arguments through sys.argv inside the child."
        ),
        requirements=["Use capture_output and text mode.", "Always return three values."],
        constraints=["Use a timeout so a hang cannot block the caller."],
        input_description="Source code and a list of arguments.",
        expected_output="A tuple of code and two strings.",
        example_input="run_python('import sys; print(sys.argv[1])', ['hello'])",
        example_output="(0, 'hello', '')",
        edge_cases=["Source that raises gives a non-zero code and stderr text.", "Empty stdout is an empty string."],
        hints=["Pass [sys.executable, '-c', code] plus the arguments."],
        success_criteria=["Returns 0 and 'hello' for the example.", "A failing child returns a non-zero code."],
        optional_extension="Accept a timeout parameter and map TimeoutExpired to a code.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Dispatch a command and return an exit status",
        difficulty="HARD",
        learning_objectives=["Compose parsing, I/O and exit codes."],
        concepts_tested=["dispatch", "streams", "exit codes"],
        problem_statement=(
            "Write `dispatch(argv, out, errors)` handling 'status', 'stop' and 'help'. "
            "Return 0 on success, 1 for an unknown command and 2 when no command is "
            "given, writing only to the streams provided."
        ),
        requirements=["Never call print without a stream.", "Never read sys.argv."],
        constraints=["Data goes to out; usage and unknown commands go to errors."],
        input_description="An argument list and two streams.",
        expected_output="An integer exit status.",
        example_input="dispatch(['status'], out, errors)",
        example_output="0",
        edge_cases=["An empty list returns 2.", "An unknown command returns 1.", "Success writes exactly one line to out."],
        hints=["Look the command up in a tuple before branching."],
        success_criteria=["['status'] returns 0.", "[] returns 2."],
        optional_extension="Add a '--json' flag that changes the output format.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Prove a module is import-safe",
        difficulty="HARD",
        learning_objectives=["Test for side effects.", "Guard module-level code."],
        concepts_tested=["import", "__name__", "subprocess"],
        problem_statement=(
            "Write `import_safety(source)` that compiles and executes the source with a "
            "`__name__` other than `'__main__' and returns the recorded output. Then use "
            "it to show that code inside a main guard does not run on import."
        ),
        requirements=["Set __name__ to something other than '__main__'.", "Return the captured output."],
        constraints=["Do not import the module under test; execute the source in a fresh namespace."],
        input_description="Python source as a string.",
        expected_output="The text the module printed at import time.",
        example_input="import_safety(\"print('top level');\\nif __name__ == '__main__':\\n    print('main only')\")",
        example_output="'top level\\n'",
        edge_cases=["Source with no top-level print returns an empty string.", "Syntax errors propagate."],
        hints=["compile() then exec() with a namespace whose __name__ is not '__main__'."],
        success_criteria=["Returns 'top level\\n' for the example.", "The guarded print never appears."],
        optional_extension="Return both the output and the namespace keys the module defined.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code="def arguments(argv) -> list[str]:\n    return list(argv[1:])",
        explanation=(
            "Slicing from index 1 handles every list length without a branch: an empty "
            "list and a single-element list both produce an empty result. Wrapping in "
            "list() gives the caller a new list, so mutating the result cannot corrupt "
            "sys.argv."
        ),
        complexity="Time O(n); space O(n).",
        edge_cases="An empty input returns an empty list without raising.",
        alternative_approaches="argv[1:] alone is equivalent but shares the underlying list.",
        testing="assert arguments(['script.py', 'a', 'b']) == ['a', 'b']\nassert arguments(['script.py']) == []\nassert arguments([]) == []",
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "from pathlib import Path\n"
            "\n"
            "\n"
            "def program_name(argv) -> str:\n"
            "    if not argv:\n"
            "        return 'python'\n"
            "    return Path(argv[0]).stem or 'python'"
        ),
        explanation=(
            "Path.stem strips both the directory and the suffix in one call, so the "
            "same expression works on Windows and POSIX without touching separators. "
            "The `or 'python'` guard covers a path such as '/' whose stem is empty."
        ),
        complexity="Time O(n) in the path length; space O(n).",
        edge_cases="A bare name such as 'roboctl' is returned unchanged.",
        alternative_approaches="os.path.splitext(os.path.basename(p)) is the older equivalent.",
        testing="assert program_name(['/opt/roboctl.py']) == 'roboctl'\nassert program_name([]) == 'python'\nassert program_name(['roboctl']) == 'roboctl'",
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "def has_flag(args, flag: str) -> bool:\n"
            "    if not isinstance(flag, str):\n"
            "        raise TypeError('flag must be a string')\n"
            "    if not flag:\n"
            "        return False\n"
            "    return flag in args"
        ),
        explanation=(
            "Membership on a list compares whole elements, which is exactly the "
            "semantics a command-line flag needs: '--verbose' must not match '--verbose-"
            "mode'. The empty-flag guard prevents `'' in args` from matching an empty "
            "argument, which is always accidental."
        ),
        complexity="Time O(n) in the list length; space O(1).",
        edge_cases="An empty list returns False; a non-string flag raises TypeError.",
        alternative_approaches="args.count(flag) > 0 also works and reports the count.",
        testing="assert has_flag(['--verbose', '--name'], '--verbose') is True\nassert has_flag(['--verbose'], '--verb') is False\nassert has_flag([], '--verbose') is False",
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "EXIT_CODES = {'ok': 0, 'unknown': 1, 'usage': 2}\n"
            "\n"
            "\n"
            "def exit_code_for(name: str) -> int:\n"
            "    return EXIT_CODES[name]"
        ),
        explanation=(
            "The mapping is the contract, so it is written once as a module constant "
            "that a caller, a test and a shell script can all read. Indexing the dict "
            "raises KeyError for an unknown name, which is the correct signal for a "
            "programming error rather than a user error."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="A missing or misspelled name raises KeyError with the name in the message.",
        alternative_approaches="An Enum gives the same guarantee with clearer names in tracebacks.",
        testing="assert exit_code_for('ok') == 0\nassert exit_code_for('usage') == 2",
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "def usage_line(program: str, commands) -> str:\n"
            "    return f\"usage: {program} <{'|'.join(str(c) for c in commands)}>\""
        ),
        explanation=(
            "An f-string composes the whole line in one expression, with the inner "
            "f-string producing the pipe-joined command list. Casting each command to "
            "str keeps the function working for non-string iterables without a special case."
        ),
        complexity="Time O(n) in the command names; space O(n).",
        edge_cases="An empty command list still produces the angle brackets.",
        alternative_approaches="Sorting the commands first makes the usage line deterministic.",
        testing="assert usage_line('roboctl', ['status', 'stop']) == 'usage: roboctl <status|stop>'\nassert usage_line('p', []) == 'usage: p <>'",
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "def split_option(token: str) -> tuple[str, str | None]:\n"
            "    if not isinstance(token, str) or not token.startswith('--'):\n"
            "        raise ValueError(f'not a flag: {token!r}')\n"
            "    name, separator, value = token.partition('=')\n"
            "    if not separator:\n"
            "        if len(name) < 3:\n"
            "            raise ValueError(f'flag has no name: {token!r}')\n"
            "        return name, None\n"
            "    if not name[2:] or not value:\n"
            "        raise ValueError(f'malformed option: {token!r}')\n"
            "    return name, value"
        ),
        explanation=(
            "partition splits on the first '=' only, so '--a=b=c' keeps 'b=c' as the "
            "value. Validating that the flag actually has a name after the dashes "
            "rejects the degenerate '--' case, and returning None for a bare flag lets "
            "the caller distinguish it from a valued option."
        ),
        complexity="Time O(n) in the token length; space O(n).",
        edge_cases="'--name=' raises ValueError; a token without leading dashes raises ValueError.",
        alternative_approaches="argparse accepts both forms, and Module 9 is about that.",
        testing="assert split_option('--name=rover-01') == ('--name', 'rover-01')\nassert split_option('--verbose') == ('--verbose', None)\nassert split_option('--a=b=c') == ('--a', 'b=c')",
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "DEFAULTS = {'name': 'rover-01', 'count': 1, 'verbose': False}\n"
            "\n"
            "\n"
            "def parse_args(args) -> tuple[dict, list[str]]:\n"
            "    options = dict(DEFAULTS)\n"
            "    errors: list[str] = []\n"
            "    index = 0\n"
            "    while index < len(args):\n"
            "        token = args[index]\n"
            "        if token == '--verbose':\n"
            "            options['verbose'] = True\n"
            "            index += 1\n"
            "        elif token in {'--name', '--count'}:\n"
            "            if index + 1 >= len(args):\n"
            "                errors.append(f'{token} requires a value')\n"
            "                index += 1\n"
            "                continue\n"
            "            value = args[index + 1]\n"
            "            if token == '--name':\n"
            "                options['name'] = value\n"
            "            else:\n"
            "                try:\n"
            "                    count = int(value)\n"
            "                except ValueError:\n"
            "                    errors.append(f'--count must be an integer, got {value!r}')\n"
            "                else:\n"
            "                    if count < 0:\n"
            "                        errors.append('--count must not be negative')\n"
            "                    else:\n"
            "                        options['count'] = count\n"
            "            index += 2\n"
            "            continue\n"
            "        else:\n"
            "            errors.append(f'unknown argument: {token!r}')\n"
            "            index += 1\n"
            "    return options, sorted(errors)"
        ),
        explanation=(
            "Two paths advance the index differently - one for a boolean flag, two for "
            "an option with a value - and the explicit continue keeps that visible. "
            "Collecting every problem instead of stopping at the first means the user "
            "fixes all their mistakes in one pass."
        ),
        complexity="Time O(n) in the arguments; space O(e) for errors.",
        edge_cases="A missing value is reported and the loop still advances past the flag.",
        alternative_approaches="argparse does all of this and more; see Module 9.",
        testing="options, errors = parse_args(['--verbose', '--name', 'rover-01'])\nassert options == {'name': 'rover-01', 'count': 1, 'verbose': True}\nassert errors == []\nassert parse_args(['--count'])[1] != []",
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "import subprocess\n"
            "import sys\n"
            "\n"
            "\n"
            "def run_python(code: str, args=(), timeout: float = 5.0) -> tuple[int, str, str]:\n"
            "    result = subprocess.run(\n"
            "        [sys.executable, '-c', code, *args],\n"
            "        capture_output=True,\n"
            "        text=True,\n"
            "        timeout=timeout,\n"
            "    )\n"
            "    return result.returncode, result.stdout, result.stderr"
        ),
        explanation=(
            "Passing sys.executable guarantees the child uses the same interpreter as "
            "the parent, which is the single most common source of confusion when a "
            "package appears to be installed but is not visible. Appending args after "
            "the -c source puts them where the child's sys.argv expects them."
        ),
        complexity="Time is dominated by interpreter start-up in the child; space O(1).",
        edge_cases="A timeout raises TimeoutExpired rather than hanging the caller.",
        alternative_approaches="Writing the code to a temporary file is slower but easier to debug.",
        testing="code, out, err = run_python('import sys; print(sys.argv[1])', ['hello'])\nassert code == 0 and out.strip() == 'hello'\nbad = run_python('raise SystemExit(1)')\nassert bad[0] == 1",
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "import sys\n"
            "\n"
            "EXIT_OK, EXIT_UNKNOWN, EXIT_USAGE = 0, 1, 2\n"
            "COMMANDS = ('status', 'stop', 'help')\n"
            "\n"
            "\n"
            "def dispatch(argv, out=sys.stdout, errors=sys.stderr) -> int:\n"
            "    if not argv:\n"
            "        print('usage: roboctl <status|stop|help>', file=errors)\n"
            "        return EXIT_USAGE\n"
            "    command = argv[0]\n"
            "    if command not in COMMANDS:\n"
            "        print(f'unknown command: {command!r}', file=errors)\n"
            "        return EXIT_UNKNOWN\n"
            "    if command == 'help':\n"
            "        print('usage: roboctl <status|stop|help>', file=out)\n"
            "    else:\n"
            "        print(f'{command}: ok', file=out)\n"
            "    return EXIT_OK"
        ),
        explanation=(
            "Validating the command against a tuple before branching means an unknown "
            "command is rejected in one place rather than falling through to a final "
            "else that has to guess. Every print names its stream, so a test can capture "
            "both and assert the contract."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="An empty argv returns the usage code and writes nothing to stdout.",
        alternative_approaches="A dict of command functions removes the if-chain entirely.",
        testing="import io\nout, err = io.StringIO(), io.StringIO()\nassert dispatch(['status'], out, err) == 0\nassert dispatch([], out, err) == 2\nassert dispatch(['nope'], out, err) == 1",
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "import io\n"
            "from contextlib import redirect_stdout\n"
            "\n"
            "\n"
            "def import_safety(source: str) -> str:\n"
            "    \"\"\"Execute source as if imported, and return what it printed.\"\"\"\n"
            "    buffer = io.StringIO()\n"
            "    namespace = {'__name__': 'imported_module'}\n"
            "    with redirect_stdout(buffer):\n"
            "        exec(compile(source, '<module>', 'exec'), namespace)\n"
            "    return buffer.getvalue()"
        ),
        explanation=(
            "Seeding the namespace with __name__ set to something other than "
            "'__main__' reproduces exactly what the interpreter does on import, so the "
            "main guard correctly skips its block. Executing the source rather than "
            "importing it keeps the test hermetic and leaves no module behind."
        ),
        complexity="Time proportional to the source; space proportional to the output.",
        edge_cases="Source with no top-level print returns an empty string.",
        alternative_approaches="Running the file in a subprocess is the end-to-end version of this test.",
        testing="out = import_safety(\"print('top level')\\nif __name__ == '__main__':\\n    print('main only')\")\nassert out == 'top level\\n'\nassert 'main only' not in out",
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
            "EXIT_OK, EXIT_UNKNOWN, EXIT_USAGE = 0, 1, 2\n"
            "COMMANDS = ('status', 'stop', 'help')\n"
            "\n"
            "\n"
            "def render(robot) -> str:\n"
            "    state = robot.status()\n"
            "    return f\"{state['name']}:{state['battery_pct']:.1f}\"\n"
            "\n"
            "\n"
            "def cli(argv, out=sys.stdout, errors=sys.stderr) -> int:\n"
            "    if not argv:\n"
            "        print('usage: roboctl <status|stop|help>', file=errors)\n"
            "        return EXIT_USAGE\n"
            "    command = argv[0]\n"
            "    if command not in COMMANDS:\n"
            "        print(f'unknown command: {command!r}', file=errors)\n"
            "        return EXIT_UNKNOWN\n"
            "    if command == 'help':\n"
            "        print('usage: roboctl <status|stop|help>', file=out)\n"
            "        return EXIT_OK\n"
            "    robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\n"
            "    print(render(robot) if command == 'status' else 'stopped', file=out)\n"
            "    return EXIT_OK"
        ),
        explanation=(
            "Separating render from cli means the line a supervisor parses can be "
            "asserted on directly, while cli owns the streams and the status. Nothing "
            "here touches sys.argv, so the whole tool is a pure function of its "
            "arguments and a test needs neither a shell nor hardware."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="An unknown command writes only to the error stream and returns 1.",
        alternative_approaches="Passing the robot in as a parameter would allow a test double.",
        testing="out, err = io.StringIO(), io.StringIO()\nassert cli(['status'], out, err) == 0\nassert 'rover-01' in out.getvalue()\nassert cli(['nope'], out, err) == 1",
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="What is the value of `__name__` when a file is executed directly?",
        choices=[
            "The file's base name.",
            "'__main__'",
            "'builtins'",
            "None, until the file is imported.",
        ],
        answer=1,
        kind="conceptual",
        explanation=(
            "The interpreter sets the module name to '__main__' for the file it was asked "
            "to run, and to the module's own name when that file is imported. That single "
            "difference is what the main guard tests."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="What does `sys.argv[0]` contain?",
        choices=[
            "The path used to invoke the program.",
            "The first argument the user typed.",
            "The program name with its extension removed.",
            "An empty string when there are no arguments.",
        ],
        answer=0,
        kind="code_output",
        explanation=(
            "argv[0] is whatever path was used to start the interpreter, which is why it "
            "may be a full path and why arguments always start at index 1. Slicing from "
            "1 is the general form."
        ),
        reference="lesson.ipynb - Basic Examples",
    )
)

QUIZ.append(
    quiz(
        question="A script moves a robot at import time, and a test that imports it hangs. What is the fix?",
        choices=[
            "Move the code into a function called main.",
            "Add a sleep so the import completes.",
            "Import the module inside a try block.",
            "Guard the side effects with `if __name__ == '__main__':`.",
        ],
        answer=3,
        kind="debugging",
        explanation=(
            "The side effect runs on import because nothing checks how the file was "
            "loaded. The main guard skips that block during an import, which is exactly "
            "the situation that made a test launch a robot."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="Why is calling sys.exit() inside a helper function discouraged?",
        choices=[
            "It is slower than returning a value.",
            "It only works at module level.",
            "It raises an exception that unwinds the whole call stack.",
            "It cannot be caught by a test.",
        ],
        answer=3,
        kind="identify_error",
        explanation=(
            "SystemExit inherits from BaseException, so raising it inside a helper skips "
            "the caller's cleanup entirely. Returning a status and exiting once at the "
            "bottom keeps control flow visible and lets tests assert the value."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="What can a shell observe about a running program?",
        choices=[
            "Its exit code, its stdout and its stderr.",
            "Only its exit code.",
            "Every variable it ever assigned.",
            "The source of the file that was executed.",
        ],
        answer=0,
        kind="reasoning",
        explanation=(
            "The three channels are the whole interface. Any decision a caller needs to "
            "make must be expressed in one of them, which is why results go to stdout, "
            "problems to stderr and success to the exit code."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="Which line makes a file directly executable on a POSIX system?",
        choices=[
            "# main guard",
            "#!/usr/bin/env python3",
            "import sys",
            "if __name__:",
        ],
        answer=1,
        kind="multiple_choice",
        explanation=(
            "The shebang must be the very first line so the shell knows which "
            "interpreter to launch. Using env makes the script portable across machines "
            "where python lives in different places."
        ),
        reference="lesson.ipynb - Syntax",
    )
)

QUIZ.append(
    quiz(
        question="Why does the walkthrough pass `sys.argv[1:]` into a function?",
        choices=[
            "So the function can be called from a test with a plain list.",
            "To avoid mutating sys.argv.",
            "Because sys.argv cannot be indexed.",
            "To convert the arguments to strings automatically.",
        ],
        answer=0,
        kind="implementation_choice",
        explanation=(
            "Once the arguments arrive as a parameter, the logic has no dependency on "
            "process state and can be exercised with a list in a unit test. The adapter "
            "at the bottom of the file is then the only place process state appears."
        ),
        reference="lesson.ipynb - Code Walkthrough",
    )
)

QUIZ.append(
    quiz(
        question="A fleet supervisor launches a service and checks its return code. What does a return code of 2 most likely mean here?",
        choices=[
            "The service completed successfully.",
            "The service found an unknown command.",
            "The service was called with a usage error.",
            "The process was killed by a signal.",
        ],
        answer=2,
        kind="robotics",
        explanation=(
            "With distinct codes for success, unknown command and usage error, a caller "
            "can tell 'you asked wrongly' from 'I do not know that'. Conflating them "
            "means the supervisor cannot react appropriately."
        ),
        reference="lesson.ipynb - Robotics Connection",
    )
)

QUIZ.append(
    quiz(
        question="Which technique proves a module is import-safe?",
        choices=[
            "Run it with python and see that it works.",
            "Execute its source with __name__ set to something other than '__main__'.",
            "Check that the file has a shebang.",
            "Count the top-level statements in the file.",
        ],
        answer=1,
        kind="reasoning",
        explanation=(
            "The question is what happens on import, so the test must reproduce an "
            "import: execute the source in a namespace whose __name__ is not "
            "'__main__' and assert that the guarded block stayed silent."
        ),
        reference="solution.ipynb - Solution 10",
    )
)

QUIZ.append(
    quiz(
        question="Why should a script be structured with a thin main() and a testable run()?",
        choices=[
            "It runs faster.",
            "It keeps the process state in one small, obvious place.",
            "It removes the need for an exit code.",
            "It allows the file to be imported without a guard.",
        ],
        answer=1,
        kind="reasoning",
        explanation=(
            "Concentrating sys.argv and sys.exit in two lines at the bottom means every "
            "other function is a pure function of its arguments, which is what makes "
            "them testable and reusable from another program."
        ),
        reference="lesson.ipynb - Summary",
    )
)

MINI_PROJECT = {
    "title": "Mini-Project: Fleet Control Tool",
    "brief": (
        "Build a small, fully tested command-line tool for controlling a simulated "
        "robot fleet. It must be safe to import, exit with meaningful codes, and keep "
        "its data and diagnostics on separate streams."
    ),
    "scenario": (
        "A deployment script calls `roboctl status` and branches on the result. The tool "
        "must be importable by the test suite without starting a robot, and its output "
        "must be machine-readable so the script can parse it."
    ),
    "rationale": (
        "This is the shape of every robotics service that will be written in this "
        "course. Getting the process contract right once means the pattern is already "
        "in place when the code grows."
    ),
    "requirements": [
        "Put the real logic in a function that takes argv and both streams.",
        "Support status, stop and help, returning 0, 1 and 2 as appropriate.",
        "Print one parseable line per robot to stdout.",
        "Send usage and unknown-command messages to stderr only.",
        "Add an `if __name__ == '__main__':` guard that exits once.",
    ],
    "constraints": [
        "Standard library only.",
        "No function may read sys.argv or call print without a stream.",
        "Importing the module must start no robot and print nothing.",
    ],
    "deliverables": [
        "`roboctl.py` with the dispatch logic and a thin main.",
        "`test_roboctl.py` with at least twelve assertions.",
        "A README section documenting every command and every exit code.",
    ],
    "steps": [
        "Write a `render_status(robot)` function that returns a line and prints nothing.",
        "Write `run(argv, out, errors)` returning an exit code.",
        "Add the main guard and confirm `python roboctl.py status` works from a shell.",
        "Write tests that import the module and assert importing printed nothing.",
        "Add a test that runs the file as a subprocess and checks the return code.",
    ],
    "expected_behavior": (
        "roboctl status prints one parseable line and exits 0; roboctl with no arguments "
        "prints usage to stderr and exits 2; an unknown command exits 1."
    ),
    "acceptance": [
        "All assertions pass from a clean run.",
        "Importing the module produces no output and no side effect.",
        "Each exit code is verified both in-process and through a subprocess.",
        "stdout never contains a warning or a usage message.",
    ],
    "extensions": [
        "Add a --json flag that emits a parseable document instead of a line.",
        "Add a 'status --all' variant that reports every robot in the fleet.",
        "Add a --timeout option and honour it in the child processes it spawns.",
    ],
}

RESEARCH = {
    "question": (
        "How much does the main guard reduce the risk of accidental side effects when a "
        "module is imported?"
    ),
    "hypothesis": (
        "A module with unguarded top-level side effects produces measurable output on "
        "import, while the same module with a main guard produces none."
    ),
    "experiment": [
        STEPS(
            [
                "Write two tiny modules: one with a top-level print, one with the same print behind a main guard.",
                "Import each from a fresh interpreter and capture stdout.",
                "Run each as a script and capture stdout and the return code.",
                "Record all four raw results below.",
            ]
        ),
    ],
    "data": [
        CODE_CELL(
            "# Record your raw results - one row per module per mode.\n"
            "# Copy real values from your actual runs; do not invent them.\n"
            "#\n"
            "# | module | mode | stdout | return code |"
        ),
    ],
    "analysis": [
        MD(
            "Compare the import rows with the script rows. The interesting comparison is "
            "unguarded-import against guarded-import, because that is the case a test "
            "suite silently experiences."
        ),
    ],
    "result": [
        MD(
            "State whether the hypothesis survived and give the four observed values. "
            "Note that the difference is invisible until something actually imports the "
            "module, which is why this class of bug survives review."
        ),
    ],
    "interpretation": [
        MD(
            "Explain the mechanism in terms of module execution and __name__, and give "
            "one realistic robotics scenario where an unguarded import would be a "
            "safety problem rather than a nuisance."
        ),
    ],
    "conclusion": [
        MD(
            "Give your verdict and state the rule you will apply to every script you "
            "write from now on."
        ),
    ],
    "extensions": [
        "Repeat with a module whose side effect is a file write, and measure the risk.",
        "Check whether linters can detect a missing guard automatically.",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Fleet Bring-Up Tool",
    "context": (
        "During mobile robot bring-up an operator runs a single command from a shell "
        "and a supervisor script captures its output and exit status to decide whether "
        "the robot may be armed."
    ),
    "mission": (
        "Implement `bringup(argv, out, errors)` returning the exit status a shell would "
        "observe, with every decision expressed on the correct channel."
    ),
    "requirements": [
        "Support status, arm and help commands.",
        "Read live telemetry from the simulator and print one parseable line.",
        "Refuse to arm when the battery is below the safety threshold, returning 1.",
        "Return 2 when no command is given, and write usage to stderr.",
    ],
    "constraints": [
        "Never call sys.exit inside the logic; return the status.",
        "Never read sys.argv inside the function.",
        "Importing this module must start no robot and print nothing.",
    ],
    "interface": "def bringup(argv, out=sys.stdout, errors=sys.stderr) -> int:",
    "success_criteria": [
        "status returns 0 and prints a line containing the robot name and battery.",
        "arm on a healthy robot returns 0; arm on a depleted battery returns 1.",
        "No arguments returns 2 with usage on stderr and nothing on stdout.",
    ],
    "extension": (
        "Add a '--timeout SECONDS' option and validate it, rejecting a non-positive "
        "value with exit code 2."
    ),
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Reframe every file as a module with two personalities and one switch.",
        "Make the process contract - code, stdout, stderr - explicit and testable.",
        "Show that import safety is a safety property, not a style preference.",
    ],
    "misconceptions": [
        [
            "argv[0] is the first argument.",
            "It is the path used to invoke the program; arguments start at index 1.",
        ],
        [
            "Wrapping code in main() prevents it running on import.",
            "It does not; only the __name__ guard prevents that.",
        ],
        [
            "sys.exit is a tidy way to stop a function early.",
            "It raises an exception that unwinds the stack and skips cleanup.",
        ],
        [
            "A script that prints correctly must be correct.",
            "Printing without an exit status gives a caller nothing to branch on.",
        ],
    ],
    "difficult_concepts": [
        "Accepting that a caller can only see three channels.",
        "Understanding that a return value and a printed message serve different readers.",
        "Writing a test that reproduces an import rather than a script run.",
    ],
    "demonstrations": [
        "Import a module with an unguarded print and watch it run.",
        "Run a script that exits 3 and observe $? in a shell.",
        "Run the same tool as a subprocess and read returncode, stdout and stderr.",
    ],
    "discussion": [
        "What should a tool do when it has nothing useful to report - print nothing, or print an empty result?",
        "Why is a distinct exit code for usage errors worth the extra branch?",
    ],
    "student_errors": [
        [
            "A test starts the robot unexpectedly",
            "Top-level side effects with no main guard",
            "Wrap side effects and guard them",
        ],
        [
            "A supervisor cannot tell success from failure",
            "The script prints but always exits 0",
            "Return a status and exit with it once",
        ],
        [
            "An index error only with zero arguments",
            "argv[0] was treated as an argument",
            "Slice from index 1, or pass sys.argv[1:] in",
        ],
    ],
    "pacing": (
        "90 minutes of lesson, then 2 hours on exercises. The subprocess exercise is "
        "the bridge to Module 9; make sure everyone runs the file from a real shell at "
        "least once."
    ),
    "extensions": [
        "Ask students to write a test that fails if the guard is removed.",
        "Have them run the tool with a broken PATH to see which error appears first.",
    ],
    "assessment": (
        "Grade against rubric.md. Exercises 7 to 10 carry the signal: they require the "
        "student to own the full process contract."
    ),
    "support": (
        "Provide a finished main() skeleton and ask students to fill in the run() "
        "function, so the process plumbing is never the blocker.",
    ),
    "extension_fast": (
        "Ask for a design note on how the same tool would report to a systemd unit "
        "versus a human at a terminal.",
    ),
}

RUBRIC = {
    "artifacts": [
        ["exercises.ipynb", "40%", "All 10 exercises implemented and edge-cased."],
        ["mini_project.ipynb", "25%", "roboctl.py plus its test suite."],
        ["robotics_challenge.ipynb", "25%", "Bring-up tool honours its exit codes."],
        ["research.ipynb", "10%", "Real measurements with a defensible conclusion."],
    ],
    "criteria": [
        ["Process contract", "30", "Exit codes, stream separation and argv handling are correct."],
        ["Import safety", "25", "Importing the module starts nothing and prints nothing."],
        ["Code quality", "25", "PEP 8 naming, docstrings, small focused functions."],
        ["Reasoning", "20", "Cost and trade-off claims explained in writing."],
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
            "Every exercise implemented, importing the module is proven harmless, and "
            "every exit code is verified both in-process and through a subprocess.",
        ],
        [
            "Merit",
            "Most exercises correct; the guard is in place but import safety is asserted "
            "only by reading the code, not by a test.",
        ],
        [
            "Pass",
            "Core requirements met, but the tool prints diagnostics to stdout so a "
            "supervisor parsing it gets corrupted data.",
        ],
        [
            "Fail",
            "No main guard, or sys.exit is called from inside the logic so the exit code "
            "cannot be asserted.",
        ],
    ],
}

TOPIC = topic(
    topic_id="1.8",
    title="Writing and Running Your First Scripts",
    module=1,
    module_title="Getting Started with Python",
    directory="08_writing_running_first_scripts",
    summary=(
        "Turning a module into a program: the main guard, sys.argv, exit codes and the "
        "three-channel contract between a script and whoever started it."
    ),
    why_it_matters=(
        "A fleet supervisor launches robot services as child processes and decides what "
        "happens next from the exit code alone. Getting that contract right is the "
        "difference between a tool that composes with a system and one that is run by "
        "hand and hoped over."
    ),
    objectives=[
        "Explain how __name__ distinguishes a module from a program.",
        "Guard side effects so importing a script cannot start a robot.",
        "Pass sys.argv[1:] into logic instead of indexing it inline.",
        "Return an exit status and call sys.exit exactly once.",
        "Keep results on stdout, diagnostics on stderr, and decisions in the exit code.",
        "Test a tool without a shell by injecting argv and the streams.",
    ],
    prerequisites=[
        "Topic 1.7 Basic Input/Output",
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
