"""Topic 1.2 - Installing Python, IDEs, and the REPL.

Hand-authored to the Course Content Standard. The spine of this topic is a
*reproducible environment*: a learner's machine, a CI runner and a robot on a
bench must all agree about which interpreter is running and where its packages
come from.
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
        "Installing Python is not one action but three separate decisions, and most "
        "\"Python does not work\" problems are really arguments between them. The first "
        "decision is **which interpreter**: the system package, a version manager, a "
        "container, or a bundled copy inside an IDE. The second is **which "
        "environment**: the base installation or an isolated virtual environment that "
        "owns its own site-packages directory. The third is **which launcher**: on "
        "many systems `python` and `python3` are different executables, and only one "
        "of them is yours."
    ),
    MD(
        "These three decisions are not cosmetic. If your editor runs the system "
        "interpreter while your terminal activates a virtual environment, your tests "
        "will pass locally and fail on the build machine, or your newly installed "
        "package will appear to vanish. Every experienced engineer has lost an hour to "
        "this, so the goal of this topic is to make the interpreter *identifiable* "
        "rather than assumed."
    ),
    MD(
        "Python is a cross-platform language, which means the same source runs on "
        "Linux, macOS and Windows, but the surrounding tooling is not identical. On "
        "Linux and macOS the conventional launcher is `python3`; on Windows the "
        "conventional launcher is `python`, and the official installer additionally "
        "offers `py`. The language itself is identical in all cases; only the paths, "
        "separators and launcher names differ. Anything you write that must run "
        "everywhere should therefore avoid hard-coded separators and prefer the "
        "`pathlib` module introduced in Module 7."
    ),
    CODE_CELL(
        "import sys\n"
        "import platform\n"
        "\n"
        "print('executable :', sys.executable)\n"
        "print('version    :', sys.version.split()[0])\n"
        "print('platform   :', platform.system(), platform.machine())\n"
        "print('max unicode:', sys.maxunicode)"
    ),
    CODE_CELL(
        "import sys\n"
        "\n"
        "print('interactive (REPL):', hasattr(sys, 'ps1'))\n"
        "print('frozen (packaged) :', getattr(sys, 'frozen', False))\n"
        "print('prefix            :', sys.prefix)\n"
        "print('base_prefix       :', sys.base_prefix)"
    ),
    NOTE(
        "Why base_prefix exists",
        "In a standard virtual environment `sys.prefix` equals `sys.base_prefix`, "
        "because the environment shares the base installation's interpreter. Inside a "
        "venv the two values differ in the opposite direction on some platforms, and "
        "an activated venv normally does *not* change `sys.executable` at all - which "
        "is exactly why checking it in every script is so useful.",
    ),
]

LESSON["formal_theory"] = [
    MD(
        "When you type a command, the operating system resolves the name to a file "
        "using the **PATH** environment variable, an ordered list of directories. "
        "The first matching executable wins. This single rule explains an enormous "
        "number of confusing behaviours: a second Python installed later in the PATH "
        "silently shadows an earlier one, and `pip install` may target a different "
        "interpreter than the `python` you just verified."
    ),
    EQUATION(
        "command name  ->  scan $PATH left to right  ->  first executable match  ->  run"
    ),
    MD(
        "Inside the interpreter, a parallel mechanism governs imports. `sys.path` is "
        "an ordered list of directories searched for modules; the current directory is "
        "typically first when you run a script, which is why a local file named "
        "`random.py` can shadow the standard library's `random` module. Module search "
        "order, not the filesystem, decides what `import random` actually loads."
    ),
    CODE_CELL(
        "import sys\n"
        "import shutil\n"
        "\n"
        "print('which python :', shutil.which('python3'))\n"
        "print('sys.path[0]  :', sys.path[0])\n"
        "print('entries      :', len(sys.path))\n"
        "for index, entry in enumerate(sys.path[:4]):\n"
        "    print(f'  [{index}] {entry}')"
    ),
    TABLE(
        ["Concept", "What it controls", "Symptom when wrong"],
        [
            ["Interpreter", "Which Python binary runs", "Version mismatch errors"],
            ["Environment (venv)", "Which packages are visible", "'Module not found' for an installed library"],
            ["PATH order", "Which launcher wins", "Wrong version silently used"],
            ["sys.path", "Which module wins an import", "Your file shadows a stdlib module"],
        ],
    ),
]

LESSON["syntax"] = [
    MD(
        "There is no special syntax for environments, but there are two idioms you "
        "will use constantly: comparing version tuples, and asking the interpreter a "
        "question at runtime."
    ),
    CODE_CELL(
        "import sys\n"
        "\n"
        "REQUIRED = (3, 12)          # this course requires 3.12 or newer\n"
        "running = tuple(sys.version_info[:2])\n"
        "if running >= REQUIRED:\n"
        "    print(f'OK: {running} satisfies {REQUIRED}')\n"
        "else:\n"
        "    print(f'TOO OLD: {running} does not satisfy {REQUIRED}')"
    ),
    MD(
        "Note that `sys.version_info` compares correctly as a tuple, so `>=` needs no "
        "string comparison. Comparing `str(sys.version_info[:2])` lexicographically is "
        "a real bug: `'3.9'` sorts above `'3.12'` because `9` follows `1`."
    ),
    WARN(
        "Never compare versions as strings",
        "'3.10' < '3.9' is True for strings and False for tuples. Always compare "
        "`sys.version_info[:2]` as a tuple, or use `packaging.version` for real "
        "dependency specifications.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - confirm which interpreter is running.**"),
    CODE_CELL(
        "import sys\n"
        "\n"
        "print('running:', sys.executable)\n"
        "print('version:', '.'.join(map(str, sys.version_info[:3])))"
    ),
    MD("**Example 2 - inspect where packages come from.**"),
    CODE_CELL(
        "import site\n"
        "\n"
        "for path in site.getsitepackages():\n"
        "    print('site-packages:', path)"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "An environment manager is just a program that creates a directory and points "
        "an interpreter at it. You can drive the standard library's `venv` module from "
        "Python, which is exactly what an IDE does when it creates an environment for "
        "you."
    ),
    CODE_CELL(
        "import subprocess\n"
        "import sys\n"
        "import tempfile\n"
        "from pathlib import Path\n"
        "\n"
        "target = Path(tempfile.gettempdir()) / 'demo_env'\n"
        "result = subprocess.run(\n"
        "    [sys.executable, '-m', 'venv', str(target)],\n"
        "    capture_output=True,\n"
        "    text=True,\n"
        ")\n"
        "print('returncode:', result.returncode)\n"
        "print('created   :', (target / 'bin').exists() or (target / 'Scripts').exists())"
    ),
    TIP(
        "Standard library only",
        "Everything in this topic uses the standard library, so it works before any "
        "third-party package is installed. That is deliberate: environment problems "
        "are exactly when you cannot rely on your packages.",
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "When a module cannot be imported, the useful question is not \"is it "
        "installed?\" but \"would this import resolve, and from where?\". "
        "`importlib.util.find_spec` answers the first without executing the module, "
        "which is the safe way to make optional-dependency decisions."
    ),
    CODE_CELL(
        "import importlib.util\n"
        "\n"
        "for name in ('json', 'requests', 'definitely_not_installed'):\n"
        "    spec = importlib.util.find_spec(name)\n"
        "    origin = spec.origin if spec else None\n"
        "    print(f'{name:<26} -> {origin}')"
    ),
    MD(
        "Note that `find_spec` can return a value for a module that will still fail to "
        "import, because a parent package may raise during its own initialisation. It "
        "answers \"where would this be loaded from\", which is a question about search "
        "order rather than about runtime health."
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "The programme below is a real pre-flight check. It is the kind of script a "
        "robotics team runs on every machine before arming hardware, and it is small "
        "enough to read in one screen and strict enough to be useful."
    ),
    CODE_CELL(
        "\"\"\"verify_env.py - report whether this machine can run ROBO-X.\"\"\"\n"
        "from __future__ import annotations\n"
        "\n"
        "import importlib.util\n"
        "import shutil\n"
        "import sys\n"
        "\n"
        "REQUIRED_VERSION = (3, 12)\n"
        "REQUIRED_MODULES = ('json', 'sqlite3', 'unittest.mock')\n"
        "\n"
        "\n"
        "def check_version() -> tuple[bool, str]:\n"
        "    running = tuple(sys.version_info[:2])\n"
        "    return running >= REQUIRED_VERSION, '.'.join(map(str, running))\n"
        "\n"
        "\n"
        "def check_modules() -> tuple[list[str], list[str]]:\n"
        "    found = [name for name in REQUIRED_MODULES\n"
        "             if importlib.util.find_spec(name) is not None]\n"
        "    missing = [name for name in REQUIRED_MODULES if name not in found]\n"
        "    return found, missing\n"
        "\n"
        "\n"
        "def main() -> int:\n"
        "    ok_version, version = check_version()\n"
        "    found, missing = check_modules()\n"
        "    print(f'interpreter : {sys.executable}')\n"
        "    print(f'version     : {version} ({\"ok\" if ok_version else \"too old\"})')\n"
        "    print(f'modules     : {len(found)}/{len(REQUIRED_MODULES)} present')\n"
        "    for name in missing:\n"
        "        print(f'  MISSING {name}')\n"
        "    ready = ok_version and not missing\n"
        "    print('READY' if ready else 'NOT READY')\n"
        "    return 0 if ready else 1\n"
        "\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    raise SystemExit(main())"
    ),
    MD(
        "The important property is that `main()` returns a status code rather than "
        "calling `sys.exit` deep inside a helper. A shell script can therefore use "
        "the exit code to decide whether to arm the robot, and a test can assert on "
        "the same integer without spawning a process."
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "`REQUIRED_VERSION` and `REQUIRED_MODULES` are module-level constants: the "
            "policy lives in exactly one place and is easy to audit or change.",
            "`check_version()` compares tuples, never strings, and returns both a "
            "verdict and the version string so the caller can report it.",
            "`check_modules()` uses `find_spec`, which inspects the search path "
            "without importing, so a missing optional dependency cannot crash the check.",
            "A list comprehension keeps the found/missing computation to one readable "
            "pass each.",
            "`main()` prints a human-readable report and reduces the two checks to one "
            "boolean named `ready`.",
            "The `raise SystemExit(main())` guard at the bottom turns that boolean into "
            "a process exit status, while keeping `main()` importable and testable.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD(
        "**Mistake 1 - installing into the base interpreter and expecting a venv to "
        "see it.** A virtual environment created with `--system-site-packages` does "
        "inherit the base packages; the default, isolated one does not."
    ),
    CODE(
        "# wrong: pip may target a different interpreter than the one you tested\n"
        "$ pip install requests\n"
        "$ python -c \"import requests\"    # ModuleNotFoundError\n"
        "\n"
        "# right: bind the installer to the interpreter explicitly\n"
        "$ python -m pip install requests\n"
        "$ python -c \"import requests\"    # succeeds",
        lang="text",
    ),
    MD(
        "**Mistake 2 - assuming `python` and `python3` are the same executable.**"
    ),
    CODE(
        "# wrong: bare 'python' may be absent, or may be Python 2 on old systems\n"
        "python --version\n"
        "\n"
        "# right: ask the interpreter you are actually going to use\n"
        "python3 --version\n"
        "python3 -c \"import sys; print(sys.executable)\"",
        lang="text",
    ),
    MD("**Mistake 3 - shadowing a standard library module with a local file.**"),
    CODE(
        "# a file called random.py in the working directory\n"
        "import random          # imports YOUR file, not the standard library\n"
        "print(random.__file__) # reveals the truth immediately",
        lang="text",
    ),
    MD("**Mistake 4 - comparing versions as strings.**"),
    CODE(
        "# wrong\n"
        "if '3.9' > '3.12':      # True - string comparison\n"
        "\n"
        "# right\n"
        "if (3, 9) > (3, 12):    # False - tuple comparison",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "Environment problems are diagnosed by *observation*, not by guessing. Three "
        "commands answer almost every question."
    ),
    STEPS(
        [
            "**Who am I?** `python -c \"import sys; print(sys.executable)\"` identifies "
            "the interpreter.",
            "**What can I see?** `python -c \"import sys; print(*sys.path, sep='\\n')\"` "
            "shows the module search order.",
            "**What got installed?** `python -m pip list` shows packages for *that* "
            "interpreter, not for whatever `pip` happens to point at.",
        ]
    ),
    CODE_CELL(
        "import sys\n"
        "\n"
        "print('first three search paths:')\n"
        "for entry in sys.path[:3]:\n"
        "    print('   ', entry)\n"
        "\n"
        "print('current dir first?', sys.path and sys.path[0] in ('', '.', None))"
    ),
    NOTE(
        "Read the REPL prompt",
        "A prompt containing `(...venv)` means a virtual environment is active. "
        "Python exposes this programmatically as `hasattr(sys, 'ps1')`, which is a "
        "reliable way for a script to refuse to run inside the wrong environment.",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Pin the interpreter, not just the package: record `python_requires` in "
            "`pyproject.toml`.",
            "Always install with `python -m pip`, never bare `pip`, so the installer "
            "and the interpreter cannot disagree.",
            "Keep one virtual environment per project, created from a committed "
            "requirements file.",
            "Use `shutil.which('name')` to resolve a launcher instead of guessing a path.",
            "Avoid hard-coded separators such as `/` or `\\\\`; let `pathlib` build paths.",
            "Put environment checks in a script that returns an exit code, so CI can "
            "call it too.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "Import time is the one performance concern that belongs in an introductory "
        "topic, because a slow start is felt on every single run of a robotics service. "
        "Importing a large library such as `pandas` costs hundreds of milliseconds "
        "before your first line of logic executes. Two rules follow. First, import at "
        "module level rather than inside a function: a function-local import re-runs "
        "the search on every call and defeats the module cache. Second, delay genuinely "
        "optional imports until the feature that needs them is actually used, so a "
        "program that never reads a CSV never pays for the dataframe stack."
    ),
    MD(
        "The trade-off is readability. A single top-level `import pandas` at the top of "
        "a notebook is clearer than a lazy loader, and for analysis code the cost is "
        "irrelevant. It is the small, frequently started command-line tools - the ones "
        "a robot launches on every mission - where import discipline genuinely "
        "changes what the user experiences."
    ),
    TIP(
        "Measure with the flag",
        "`python -X importtime script.py` prints the time spent importing every "
        "module, largest first. It is the fastest way to find an unexpected heavy "
        "dependency.",
    ),
]

LESSON["pythonic_approaches"] = [
    MD("Building the same path two ways:"),
    CODE_CELL(
        "import os\n"
        "from pathlib import Path\n"
        "\n"
        "home = os.path.expanduser('~')\n"
        "\n"
        "# string concatenation with a hard-coded separator\n"
        "old = home + '/' + 'venvs' + '/' + 'robo'\n"
        "\n"
        "# pathlib composes and normalises the same path\n"
        "new = Path(home) / 'venvs' / 'robo'\n"
        "\n"
        "print('old:', old)\n"
        "print('new:', new)\n"
        "print('equal:', Path(old) == new)"
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "Every robot in a fleet runs on a machine whose environment someone verified. "
        "The simulator is deterministic by construction - it fixes a seed - but it is "
        "still Python code running on a real interpreter, so the environment checks "
        "from this topic apply unchanged. The snippet below builds the pre-flight "
        "report the fleet supervisor reads before it dispatches a mission."
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
        "print(f\"{state['name']}: {state['battery_pct']:.1f}% \"\n"
        "      f\"on {sys.version.split()[0]}\")"
    ),
]

LESSON["engineering_example"] = [
    MD(
        "A reusable pre-flight function, with the policy separated from the "
        "reporting so a fleet operator can override the thresholds."
    ),
    CODE_CELL(
        "REQUIRED = (3, 12)\n"
        "\n"
        "\n"
        "def preflight(required=REQUIRED) -> dict:\n"
        "    import sys\n"
        "\n"
        "    problems = []\n"
        "    running = tuple(sys.version_info[:2])\n"
        "    if running < required:\n"
        "        problems.append(f'version {running} older than {required}')\n"
        "    if not sys.executable:\n"
        "        problems.append('interpreter path is empty')\n"
        "    return {'ready': not problems, 'problems': problems,\n"
        "            'version': '.'.join(map(str, running))}\n"
        "\n"
        "\n"
        "report = preflight()\n"
        "print(report['version'], 'READY' if report['ready'] else report['problems'])"
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Print `sys.executable`, `sys.prefix` and `sys.base_prefix`.",
            "Compare `sys.prefix` with `sys.base_prefix` and state what the result "
            "tells you about the current environment.",
            "Use `importlib.util.find_spec('sqlite3')` to confirm the database module "
            "is available without importing it.",
            "Write `version_ok(minimum)` returning a boolean, then call it with "
            "`(3, 12)` and with `(4, 0)`.",
        ]
    ),
    CODE_CELL(
        "# Your turn.\n"
        "import sys\n"
        "import importlib.util\n"
        "\n"
        "print('prefix      :', sys.prefix)\n"
        "print('base_prefix :', sys.base_prefix)\n"
        "print('sqlite3     :', importlib.util.find_spec('sqlite3') is not None)\n"
        "\n"
        "\n"
        "def version_ok(minimum):\n"
        "    return tuple(sys.version_info[:2]) >= tuple(minimum)"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: an installation is a stack of three rings.** The innermost "
        "ring is the *interpreter binary*. Around it sits an *environment* that owns "
        "its own package directory. Outside both is the *PATH*, which decides which "
        "of many possible binaries answers when you type a name. A command reaches "
        "your code only if it passes all three rings, and it can be shadowed at any "
        "one of them."
    ),
    TABLE(
        ["If this is wrong", "The symptom you will see"],
        [
            ["Interpreter ring", "Wrong version reported, or a syntax error on valid code"],
            ["Environment ring", "'ModuleNotFoundError' for a library you just installed"],
            ["PATH ring", "`python3` runs, `python` is missing or is a different version"],
            ["sys.path order", "A local file shadows a standard library module"],
        ],
    ),
]

TERMS = [
    ["Interpreter", "The program that reads and executes Python source code."],
    ["Launcher", "The command such as `python3` that finds and starts an interpreter."],
    ["PATH", "Ordered list of directories searched for an executable by name."],
    ["Virtual environment (venv)", "A directory holding its own package tree and config."],
    ["site-packages", "The directory inside an environment where packages are installed."],
    ["sys.path", "The ordered list of directories searched for importable modules."],
    ["sys.executable", "Absolute path of the interpreter currently running your code."],
    ["sys.prefix", "Installation prefix of the active environment."],
    ["REPL", "Read-Eval-Print Loop: the interactive prompt."],
    ["find_spec", "Locate a module without importing it, used for optional dependencies."],
    ["PEP 405", "The specification that defines Python virtual environments."],
]

LESSON["summary"] = [
    MD(
        "Installing Python is a three-part decision: which interpreter runs, which "
        "environment owns the packages, and which launcher the PATH selects. Every "
        "environment bug you will meet traces back to one of those three rings being "
        "different from what you assumed."
    ),
    MD(
        "The practical habits from this topic are short and non-negotiable. Identify "
        "the interpreter with `sys.executable` instead of trusting the prompt. Install "
        "with `python -m pip` so the installer and the interpreter cannot diverge. "
        "Check optional dependencies with `importlib.util.find_spec` rather than a "
        "guarded `try: import`, because a guarded import can raise for reasons that "
        "have nothing to do with the package being present. Compare versions as "
        "tuples, never as strings. And build paths with `pathlib` so the same code "
        "works on every platform."
    ),
    MD(
        "Above all, make the environment *observable*. A pre-flight script that "
        "reports the interpreter path, the version and the resolved module locations, "
        "then exits non-zero when something is wrong, turns an hour of guessing into "
        "a single command. That script is the first deliverable of this module, and "
        "it is exactly the kind of tool a robotics team puts on every machine."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "Three decisions: interpreter, environment, launcher.",
            "`sys.executable` is the authoritative answer to 'which Python am I'.",
            "`python -m pip` guarantees the installer matches the interpreter.",
            "PATH order decides which launcher wins; the first match is taken.",
            "`sys.path` decides which module wins an import.",
            "`find_spec` checks availability without executing the module.",
            "Compare `sys.version_info[:2]` as a tuple, never as a string.",
            "Return exit codes from checks so CI and shells can consume them.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "[venv - Creating virtual environments](https://docs.python.org/3/library/venv.html)",
            "[sys - Access to the Python runtime](https://docs.python.org/3/library/sys.html)",
            "[importlib.util.find_spec](https://docs.python.org/3/library/importlib.html#importlib.util.find_spec)",
            "[PEP 405 - Virtual Environments](https://peps.python.org/pep-0405/)",
            "[PEP 723 - Inline script metadata](https://peps.python.org/pep-0723/) - "
            "declaring dependencies directly in a script.",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Format an environment report line",
        difficulty="MEDIUM",
        learning_objectives=["Build a string from a tuple.", "Use f-string formatting."],
        concepts_tested=["f-strings", "tuples", "sys"],
        problem_statement=(
            "Write `report_line(version_tuple)` returning "
            "`'python 3.12 OK'` for `(3, 12)` and `'python 3.9 TOO OLD'` for "
            "`(3, 9)`, treating anything below 3.12 as too old."
        ),
        requirements=["Join the tuple with dots.", "Compare as a tuple, never as a string."],
        constraints=["Do not import sys; the version arrives as an argument."],
        input_description="A tuple such as `(3, 12)`.",
        expected_output="A single status line.",
        example_input="report_line((3, 12))",
        example_output="'python 3.12 OK'",
        edge_cases=["(4, 0) counts as new enough.", "(3, 9) is too old.", "(3, 12, 1) ignores the micro."],
        hints=["Use '.'.join(map(str, version)) to render it."],
        success_criteria=["Exact string for the example.", "(3, 9) reports TOO OLD."],
        optional_extension="Accept a minimum as a second argument.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Tuple-safe version comparison",
        difficulty="MEDIUM",
        learning_objectives=["Compare versions correctly.", "Normalise input."],
        concepts_tested=["tuples", "comparison", "validation"],
        problem_statement=(
            "Write `version_ok(running, minimum)` returning True when the two "
            "2-tuples compare as expected. Accept strings such as `'3.12'` and "
            "convert them first."
        ),
        requirements=["Accept tuples or dotted strings.", "Raise TypeError on anything else."],
        constraints=["Comparison must be numeric, not lexicographic."],
        input_description="Two versions, each a tuple or a dotted string.",
        expected_output="A boolean.",
        example_input="version_ok('3.12', (3, 12))",
        example_output="True",
        edge_cases=["'3.9' versus '3.12' must be False.", "Extra components are truncated.", "None raises TypeError."],
        hints=["Split on '.' and cast each part to int."],
        success_criteria=["'3.9' vs '3.12' returns False.", "Equal versions return True."],
        optional_extension="Return the difference as a tuple.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Describe the running interpreter",
        difficulty="MEDIUM",
        learning_objectives=["Collect runtime facts.", "Return a structured dict."],
        concepts_tested=["sys", "dicts", "modules"],
        problem_statement=(
            "Write `describe_environment()` returning a dict with keys `executable`, "
            "`version`, `platform` and `interactive` describing the running "
            "interpreter."
        ),
        requirements=["Use sys and platform only.", "Return strings and a bool."],
        constraints=["No printing; return the data."],
        input_description="Nothing; read from the running process.",
        expected_output="A dict with exactly those four keys.",
        example_input="describe_environment()",
        example_output="{'executable': '/usr/bin/python3', 'version': '3.12.3', ...}",
        edge_cases=["An embedded interpreter may have an empty executable path.", "Version must be the short form."],
        hints=["sys.version.split()[0] gives the short version string."],
        success_criteria=["All four keys present.", "interactive is a bool."],
        optional_extension="Add the number of entries in sys.path.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Check an optional dependency safely",
        difficulty="MEDIUM",
        learning_objectives=["Detect availability without importing.", "Return tri-state results."],
        concepts_tested=["importlib", "modules", "booleans"],
        problem_statement=(
            "Write `is_available(name)` returning True when the module could be "
            "imported, False when it is not, and raising TypeError for a non-string "
            "argument. Do not actually import the module."
        ),
        requirements=["Use importlib.util.find_spec.", "Never execute the module's code."],
        constraints=["No try/except around a real import."],
        input_description="A module name such as `'sqlite3'`.",
        expected_output="True, False, or a raised TypeError.",
        example_input="is_available('sqlite3')",
        example_output="True",
        edge_cases=["A name that is not a module returns False.", "None raises TypeError.", "Dotted names are allowed."],
        hints=["find_spec returns None rather than raising for a missing module."],
        success_criteria=["Returns True for sqlite3.", "Returns False for a nonsense name."],
        optional_extension="Return the origin path when the module is found.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Join path segments portably",
        difficulty="MEDIUM",
        learning_objectives=["Build paths without string concatenation.", "Use pathlib."],
        concepts_tested=["pathlib", "strings", "composition"],
        problem_statement=(
            "Write `build_path(base, *parts)` that joins a base directory with any "
            "number of segments using pathlib, ignoring empty segments and never "
            "producing a doubled separator."
        ),
        requirements=["Use the pathlib operator, not string concatenation.", "Return a Path."],
        constraints=["Empty or whitespace-only segments are dropped."],
        input_description="A base string and one or more segment strings.",
        expected_output="A pathlib.Path.",
        example_input="build_path('/opt/robo', 'venvs', 'main')",
        example_output="PosixPath('/opt/robo/venvs/main')",
        edge_cases=["No segments returns the base.", "Empty segments are skipped.", "Trailing slashes are normalised."],
        hints=["The / operator on Path accepts any number of operands in a loop."],
        success_criteria=["No doubled separators in the result.", "Empty segments dropped."],
        optional_extension="Reject absolute segments with ValueError.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Parse a pinned dependency block",
        difficulty="HARD",
        learning_objectives=["Parse configuration text.", "Validate and report errors."],
        concepts_tested=["strings", "dicts", "parsing"],
        problem_statement=(
            "Write `parse_pins(text)` that turns a block such as "
            "`'numpy==2.1.0; requests>=2.31'` into "
            "`{'numpy': '==2.1.0', 'requests': '>=2.31'}`. Ignore blank lines and "
            "`#` comments; raise ValueError on an entry with no operator."
        ),
        requirements=["Split on whitespace and newlines.", "Reject malformed entries explicitly."],
        constraints=["Standard library only.", "No regular expressions."],
        input_description="A multi-line string of name/operator/version entries.",
        expected_output="A dict mapping name to its version constraint.",
        example_input="parse_pins('numpy==2.1.0; requests>=2.31')",
        example_output="{'numpy': '==2.1.0', 'requests': '>=2.31'}",
        edge_cases=["Trailing semicolons and blank lines.", "'#' comment lines.", "A bare name with no operator."],
        hints=["Find the first occurrence of an operator character and slice around it."],
        success_criteria=["Parses the example exactly.", "Raises ValueError on 'numpy'."],
        optional_extension="Return duplicates as a list of conflicts.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Verify required modules against what is present",
        difficulty="HARD",
        learning_objectives=["Compare required against available.", "Return a summary and a diff."],
        concepts_tested=["sets", "dicts", "validation"],
        problem_statement=(
            "Write `verify_modules(required, available)` returning "
            "`(ok, missing)` where `missing` is a sorted list of required names not "
            "present, and `ok` is True only when that list is empty."
        ),
        requirements=["Return a tuple of (bool, sorted list).", "Ignore duplicates."],
        constraints=["Do not mutate the inputs."],
        input_description="Two iterables of module names.",
        expected_output="A tuple (ok, missing).",
        example_input="verify_modules(['json', 'requests'], ['json'])",
        example_output="(False, ['requests'])",
        edge_cases=["No requirements means ok is True.", "Case sensitivity is exact.", "Duplicates in required."],
        hints=["Set difference gives you the missing names for free."],
        success_criteria=["(False, ['requests']) for the example.", "Empty required gives (True, [])."],
        optional_extension="Also return the extras that are available but not required.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Resolve the first available interpreter launcher",
        difficulty="HARD",
        learning_objectives=["Resolve a command through PATH.", "Fail explicitly."],
        concepts_tested=["shutil.which", "loops", "error reporting"],
        problem_statement=(
            "Write `pick_interpreter(candidates)` that returns the absolute path of "
            "the first launcher found on PATH, trying candidates in order. Raise "
            "FileNotFoundError listing every candidate when none is found."
        ),
        requirements=["Use shutil.which rather than guessing directories.", "Preserve candidate order."],
        constraints=["Do not call subprocess."],
        input_description="A sequence of launcher names such as ('python3.12', 'python3').",
        expected_output="An absolute path string, or a raised FileNotFoundError.",
        example_input="pick_interpreter(['python3.12', 'python3'])",
        example_output="'/usr/bin/python3.12'",
        edge_cases=["No candidate resolves.", "A candidate that is not executable is skipped.", "Duplicate names."],
        hints=["shutil.which returns None rather than raising when nothing is found."],
        success_criteria=["Finds a real launcher on this machine.", "Raises with all names in the message."],
        optional_extension="Return a tuple of (path, which_name) for reporting.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Summarise the module search path",
        difficulty="HARD",
        learning_objectives=["De-duplicate while preserving order.", "Classify entries."],
        concepts_tested=["sys.path", "sets", "ordering"],
        problem_statement=(
            "Write `summarise_search_path(entries)` returning a dict with `total` "
            "(count including duplicates), `unique` (count after de-duplication) and "
            "`duplicates` (the repeated entries in first-seen order)."
        ),
        requirements=["Preserve first-seen order in `duplicates`.", "Do not reorder `entries`."],
        constraints=["Treat entries as opaque strings."],
        input_description="A sequence of directory strings such as sys.path.",
        expected_output="A dict with the three keys.",
        example_input="summarise_search_path(['a', 'b', 'a', 'c', 'b'])",
        example_output="{'total': 5, 'unique': 3, 'duplicates': ['a', 'b']}",
        edge_cases=["Empty input gives zeros and an empty list.", "A single repeated entry.", "Identical strings from different sources."],
        hints=["One pass with a seen-set and a counter is enough."],
        success_criteria=["Matches the example exactly.", "Empty input does not raise."],
        optional_extension="Classify each entry as stdlib, site-packages or unknown.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Assemble a machine pre-flight report",
        difficulty="HARD",
        learning_objectives=["Compose checks into a decision.", "Return machine-readable results."],
        concepts_tested=["dicts", "composition", "validation", "sys"],
        problem_statement=(
            "Write `preflight_report(minimum=(3, 12), required=('json', 'sqlite3'))` "
            "returning a dict with `ready` (bool), `version` (str) and `problems` "
            "(list of strings). Each failing check appends one specific message."
        ),
        requirements=["Compose the version check and the module check.", "Never raise."],
        constraints=["Read the running interpreter from sys.", "problems is empty when ready is True."],
        input_description="Optional minimum version tuple and required module names.",
        expected_output="A dict with the three keys.",
        example_input="preflight_report()",
        example_output="{'ready': True, 'version': '3.12.3', 'problems': []}",
        edge_cases=["An old interpreter still returns a report rather than raising.", "A missing module is named.", "Both checks fail at once."],
        hints=["Build problems as a list, then derive ready from its emptiness."],
        success_criteria=["ready is True on this machine.", "problems names each missing module."],
        optional_extension="Add an elapsed-time field measured with time.perf_counter.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "MINIMUM = (3, 12)\n"
            "\n"
            "\n"
            "def report_line(version_tuple) -> str:\n"
            "    version = '.'.join(str(part) for part in version_tuple[:2])\n"
            "    verdict = 'OK' if tuple(version_tuple[:2]) >= MINIMUM else 'TOO OLD'\n"
            "    return f'python {version} {verdict}'"
        ),
        explanation=(
            "Slicing to two components drops the micro version so (3, 12, 1) is "
            "treated the same as (3, 12). The verdict comes from a tuple comparison, "
            "which orders numerically, and the rendered string is built separately so "
            "display and comparison cannot drift apart."
        ),
        complexity="Time O(k) in the number of components; space O(1).",
        edge_cases="A one-element tuple renders as a single number and compares as expected.",
        alternative_approaches="An f-string with the tuple unpacked inline is shorter but harder to read.",
        testing="assert report_line((3, 12)) == 'python 3.12 OK'\nassert report_line((3, 9)) == 'python 3.9 TOO OLD'\nassert report_line((4, 0)) == 'python 4.0 OK'",
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def _as_tuple(version):\n"
            "    if isinstance(version, str):\n"
            "        return tuple(int(part) for part in version.split('.'))\n"
            "    if isinstance(version, (tuple, list)):\n"
            "        return tuple(int(part) for part in version)\n"
            "    raise TypeError(f'unsupported version: {version!r}')\n"
            "\n"
            "\n"
            "def version_ok(running, minimum) -> bool:\n"
            "    return _as_tuple(running)[:2] >= _as_tuple(minimum)[:2]"
        ),
        explanation=(
            "Normalising both arguments in one helper guarantees the comparison is "
            "numeric on both sides. Slicing to two components means '3.12.1' and "
            "'3.12' agree, and raising TypeError for anything else keeps a silent "
            "misinterpretation impossible."
        ),
        complexity="Time O(k) in the number of components; space O(k).",
        edge_cases="An empty string raises ValueError from int(''), which is the correct signal.",
        alternative_approaches="packaging.version handles pre-release suffixes that this simple form ignores.",
        testing="assert version_ok('3.12', (3, 12)) is True\nassert version_ok('3.9', '3.12') is False\nassert version_ok((3, 12, 1), (3, 12)) is True",
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "import platform\n"
            "import sys\n"
            "\n"
            "\n"
            "def describe_environment() -> dict:\n"
            "    return {\n"
            "        'executable': sys.executable,\n"
            "        'version': sys.version.split()[0],\n"
            "        'platform': f'{platform.system()} {platform.machine()}',\n"
            "        'interactive': hasattr(sys, 'ps1'),\n"
            "    }"
        ),
        explanation=(
            "Each field is read directly from the runtime rather than recomputed. "
            "hasattr(sys, 'ps1') is the documented way to detect an interactive "
            "session, and splitting sys.version gives the short form without the "
            "build metadata."
        ),
        complexity="Time O(1); space O(1).",
        edge_cases="An embedded interpreter may report an empty executable path; the key is still present.",
        alternative_approaches="platform.uname() gives richer detail but returns a named tuple.",
        testing="d = describe_environment()\nassert set(d) == {'executable', 'version', 'platform', 'interactive'}\nassert isinstance(d['interactive'], bool)\nassert d['version'].count('.') >= 1",
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "import importlib.util\n"
            "\n"
            "\n"
            "def is_available(name) -> bool:\n"
            "    if not isinstance(name, str):\n"
            "        raise TypeError(f'module name must be a string, got {type(name).__name__}')\n"
            "    if not name:\n"
            "        return False\n"
            "    try:\n"
            "        return importlib.util.find_spec(name) is not None\n"
            "    except (ImportError, ValueError):\n"
            "        return False"
        ),
        explanation=(
            "find_spec answers whether an import would resolve without executing the "
            "module, which is the behaviour the task requires. A parent package that "
            "fails during initialisation raises ImportError or ValueError rather than "
            "returning None, so those are caught and reported as unavailable."
        ),
        complexity="Time O(n) in sys.path length; space O(1).",
        edge_cases="An empty name returns False; a dotted name such as 'os.path' resolves.",
        alternative_approaches="A guarded import inside try/except is simpler but executes the module's code.",
        testing="assert is_available('sqlite3') is True\nassert is_available('definitely_not_a_module_xyz') is False",
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "from pathlib import Path\n"
            "\n"
            "\n"
            "def build_path(base, *parts) -> Path:\n"
            "    path = Path(base)\n"
            "    for part in parts:\n"
            "        if part and part.strip():\n"
            "            path = path / part.strip()\n"
            "    return path"
        ),
        explanation=(
            "The pathlib operator performs the platform-specific joining and "
            "normalisation, so a doubled separator cannot be produced on any system. "
            "Falsy and whitespace-only segments are skipped rather than appended, "
            "which keeps a stray empty argument from creating a confusing path."
        ),
        complexity="Time O(n) in the number of segments; space O(n) in path length.",
        edge_cases="A base with a trailing slash is normalised; no segments returns the base Path.",
        alternative_approaches="pathlib.PurePath handles the same logic for virtual filesystems.",
        testing="assert str(build_path('/opt/robo', 'venvs', 'main')) == '/opt/robo/venvs/main'\nassert str(build_path('/opt/robo', '', '  ', 'main')) == '/opt/robo/main'",
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "OPERATORS = ('==', '>=', '<=', '~=', '!=', '>', '<')\n"
            "\n"
            "\n"
            "def parse_pins(text: str) -> dict:\n"
            "    pins: dict = {}\n"
            "    for raw in text.replace(';', '\\n').splitlines():\n"
            "        line = raw.split('#', 1)[0].strip()\n"
            "        if not line:\n"
            "            continue\n"
            "        for op in OPERATORS:\n"
            "            if op in line:\n"
            "                name, _, constraint = line.partition(op)\n"
            "                name = name.strip()\n"
            "                if not name:\n"
            "                    raise ValueError(f'missing package name: {raw!r}')\n"
            "                pins[name] = op + constraint.strip()\n"
            "                break\n"
            "        else:\n"
            "            raise ValueError(f'no version operator in {raw!r}')\n"
            "    return pins"
        ),
        explanation=(
            "Semicolons are normalised to newlines first so one parser handles both "
            "layouts. The for/else construct raises only when no operator was found in "
            "a line, which is exactly the malformed case, and stripping comments before "
            "parsing means a trailing comment never splits a constraint."
        ),
        complexity="Time O(n) in the input length; space O(k) for k packages.",
        edge_cases="Blank and comment-only lines are skipped; 'numpy' with no operator raises ValueError.",
        alternative_approaches="A regular expression with a named group is shorter but less explicit.",
        testing="assert parse_pins('numpy==2.1.0; requests>=2.31') == {'numpy': '==2.1.0', 'requests': '>=2.31'}\nassert parse_pins('# comment\\nnumpy==2.1.0') == {'numpy': '==2.1.0'}",
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "def verify_modules(required, available) -> tuple[bool, list[str]]:\n"
            "    missing = sorted(set(required) - set(available))\n"
            "    return (not missing), missing"
        ),
        explanation=(
            "Set difference removes duplicates on both sides and computes the missing "
            "names in one operation. Sorting makes the result deterministic, which "
            "matters because this list is printed in reports and compared in tests."
        ),
        complexity="Time O(n + m) in the input sizes; space O(n).",
        edge_cases="An empty `required` yields an empty list and therefore True.",
        alternative_approaches="A comprehension over required with a membership test is equivalent.",
        testing="assert verify_modules(['json', 'requests'], ['json']) == (False, ['requests'])\nassert verify_modules([], []) == (True, [])",
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "import shutil\n"
            "\n"
            "\n"
            "def pick_interpreter(candidates) -> str:\n"
            "    tried = []\n"
            "    for name in candidates:\n"
            "        tried.append(name)\n"
            "        found = shutil.which(name)\n"
            "        if found:\n"
            "            return found\n"
            "    raise FileNotFoundError(\n"
            "        'no interpreter found; tried: ' + ', '.join(tried)\n"
            "    )"
        ),
        explanation=(
            "which() implements the same PATH scan the operating system uses, so the "
            "result matches what actually happens when the launcher is typed. Building "
            "the tried list as we go means the error names every candidate, which is "
            "the information needed to diagnose a broken PATH."
        ),
        complexity="Time O(n * p) for n candidates over p PATH entries; space O(n).",
        edge_cases="A non-executable file with a matching name is skipped by which().",
        alternative_approaches="shutil.which on a single name is simpler but cannot express a preference order.",
        testing="import shutil\nname = pick_interpreter(['python3.12', 'python3'])\nassert name == shutil.which(name) or name == shutil.which('python3.12')",
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "def summarise_search_path(entries) -> dict:\n"
            "    entries = list(entries)\n"
            "    seen: set = set()\n"
            "    duplicates: list[str] = []\n"
            "    for entry in entries:\n"
            "        if entry in seen:\n"
            "            if entry not in duplicates:\n"
            "                duplicates.append(entry)\n"
            "        else:\n"
            "            seen.add(entry)\n"
            "    return {'total': len(entries), 'unique': len(seen), 'duplicates': duplicates}"
        ),
        explanation=(
            "A single pass with a seen-set gives the unique count, while a separate "
            "list preserves the first-seen order of repeated entries. Checking "
            "membership in the duplicates list as well keeps that list unique without "
            "a second set."
        ),
        complexity="Time O(n) in the number of entries; space O(n).",
        edge_cases="An empty input returns zero counts and an empty duplicate list.",
        alternative_approaches="Counter preserves insertion order in modern Python and is shorter.",
        testing="assert summarise_search_path(['a', 'b', 'a', 'c', 'b']) == {'total': 5, 'unique': 3, 'duplicates': ['a', 'b']}\nassert summarise_search_path([]) == {'total': 0, 'unique': 0, 'duplicates': []}",
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "import importlib.util\n"
            "import sys\n"
            "\n"
            "DEFAULT_MINIMUM = (3, 12)\n"
            "DEFAULT_REQUIRED = ('json', 'sqlite3')\n"
            "\n"
            "\n"
            "def preflight_report(minimum=DEFAULT_MINIMUM, required=DEFAULT_REQUIRED) -> dict:\n"
            "    problems: list[str] = []\n"
            "    running = tuple(sys.version_info[:2])\n"
            "    version = '.'.join(str(part) for part in running)\n"
            "    if running < tuple(minimum[:2]):\n"
            "        problems.append(f'version {version} older than {minimum}')\n"
            "    for name in required:\n"
            "        try:\n"
            "            present = importlib.util.find_spec(name) is not None\n"
            "        except (ImportError, ValueError):\n"
            "            present = False\n"
            "        if not present:\n"
            "            problems.append(f'missing module: {name}')\n"
            "    return {'ready': not problems, 'version': version, 'problems': problems}"
        ),
        explanation=(
            "The function collects problems instead of raising, because a check that "
            "reports every fault at once is far more useful than one that stops at the "
            "first. ready is then derived from the emptiness of problems, which makes "
            "it impossible for the flag to disagree with the list it summarises."
        ),
        complexity="Time O(m) for m required modules; space O(m).",
        edge_cases="An old interpreter still returns a report with ready False.",
        alternative_approaches="A dataclass result type would be clearer in larger codebases.",
        testing="report = preflight_report()\nassert report['ready'] is True\nassert report['problems'] == []\nassert report['version'].count('.') == 2",
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
            "REQUIRED_CHANNELS = ('distance', 'temperature', 'battery_voltage')\n"
            "\n"
            "\n"
            "def environment_readiness(channels=None) -> dict:\n"
            "    wanted = list(channels) if channels else list(REQUIRED_CHANNELS)\n"
            "    robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\n"
            "    readings, failed = {}, []\n"
            "    for channel in wanted:\n"
            "        try:\n"
            "            readings[channel] = robot.read_sensor(channel)\n"
            "        except Exception:  # SensorError, or an unknown channel name\n"
            "            readings[channel] = None\n"
            "            failed.append(channel)\n"
            "    state = robot.status()\n"
            "    return {\n"
            "        'ready': not failed,\n"
            "        'version': sys.version.split()[0],\n"
            "        'battery_pct': state['battery_pct'],\n"
            "        'readings': readings,\n"
            "        'failed_channels': failed,\n"
            "    }"
        ),
        explanation=(
            "Combining the environment facts with a live simulator read shows both "
            "halves of pre-flight: the machine is new enough, and the subsystems it "
            "must drive actually answer. Each channel is isolated so one failing "
            "sensor degrades the report instead of destroying it."
        ),
        complexity="Time O(c) for c channels; space O(c).",
        edge_cases="An unknown channel name is recorded as failed rather than raising.",
        alternative_approaches="Catching SensorError specifically is stricter and better in production code.",
        testing="report = environment_readiness()\nassert report['ready'] is True\nassert report['failed_channels'] == []\nassert report['battery_pct'] > 0",
    )
)
