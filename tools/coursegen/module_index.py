"""Generate the module index README for each module directory.

Every topic README links to ``../README.md`` ("Module index"). Those files were
previously missing, so the whole navigation graph was broken. This module
generates them from the authored content, so they can never drift.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from .catalogue import MODULE_DIRS, MODULE_TITLES
from .schema import Topic

#: One-paragraph overview per module. Written by hand — this is teaching prose,
#: not templated filler.
MODULE_BLURBS: dict[int, str] = {
    1: (
        "Install Python, meet the interpreter, and write your first program. "
        "You will set up a reproducible environment, then learn the syntax, data "
        "types, operators and input/output primitives that every later module "
        "builds on. The module ends with a runnable ROBO-X bring-up script."
    ),
    2: (
        "Learn to direct the flow of a program with conditionals and loops. You "
        "will branch on sensor thresholds, iterate over waypoint lists, use break "
        "and continue deliberately, and pair up data streams with range, "
        "enumerate and zip."
    ),
    3: (
        "Master Python's four workhorse structures — lists, tuples, sets and "
        "dictionaries — plus strings, comprehensions and the collections module. "
        "You will reason about mutability, aliasing and complexity, and choose "
        "the right structure for a robotics data problem."
    ),
    4: (
        "Write functions that are easy to test and reuse: parameters, scope, "
        "closures, higher-order functions, generators and decorators. You will "
        "also package your code into modules and manage dependencies with a "
        "virtual environment."
    ),
    5: (
        "Make programs fail safely. You will distinguish errors from exceptions, "
        "write precise try/except/else/finally blocks, design custom exception "
        "hierarchies, and use the debugger and the logging module to diagnose "
        "problems in a running robot."
    ),
    6: (
        "Model a robotics system with objects: classes, encapsulation, "
        "inheritance, polymorphism, magic methods and properties. You will "
        "refactor toward clean design using composition and the SOLID principles."
    ),
    7: (
        "Read and write real data. You will use pathlib and context managers, "
        "parse and emit JSON and CSV, and apply regular expressions, then join it "
        "all into a small data pipeline for flight-test and telemetry records."
    ),
    8: (
        "Persist and query structured data with SQLite and SQLAlchemy. You will "
        "create schemas, perform CRUD safely with parameterised queries, wrap "
        "work in transactions, and understand when an ORM helps and when raw SQL "
        "is clearer."
    ),
    9: (
        "The professional finish: type hints, dates and times, command-line "
        "interfaces, HTTP APIs, unit testing, code style and packaging. These are "
        "the practices that turn working code into maintainable software."
    ),
}

#: Measurable outcomes per module (what the learner can do afterwards).
MODULE_OUTCOMES: dict[int, list[str]] = {
    1: [
        "Run Python interactively and from a script, and explain the role of the interpreter.",
        "Write correctly indented, PEP 8-aligned code with meaningful comments.",
        "Choose and convert between the core built-in data types.",
        "Use operators and expressions, including f-string formatting.",
        'Structure a script with an ``if __name__ == "__main__"`` guard.',
    ],
    2: [
        "Write branching logic with ``if``/``elif``/``else`` and the conditional expression.",
        "Iterate with ``for`` and ``while``, and choose the right loop for a task.",
        "Control loops deliberately with ``break``, ``continue`` and ``else``.",
        "Use ``range``, ``enumerate`` and ``zip`` to iterate with indices and pair streams.",
    ],
    3: [
        "Create, index, slice and mutate lists, and reason about aliasing.",
        "Use tuples for fixed records and unpacking.",
        "Use sets for membership tests and de-duplication.",
        "Model keyed data with dictionaries and the ``collections`` module.",
        "Express transformations with list/set/dict comprehensions.",
    ],
    4: [
        "Define and call functions with positional, keyword and default arguments.",
        "Reason about scope, closures and the ``nonlocal`` keyword.",
        "Write generators and use decorators such as timing and retry wrappers.",
        "Organise code into importable modules and packages.",
        "Create a virtual environment and declare dependencies.",
    ],
    5: [
        "Distinguish syntax/runtime errors from exceptions and handle them with EAFP.",
        "Write ``try``/``except``/``else``/``finally`` blocks with precise exceptions.",
        "Design a custom exception hierarchy for a robotics subsystem.",
        "Debug a running program with ``breakpoint()`` and read tracebacks.",
        "Configure the ``logging`` module with levels, handlers and formatting.",
    ],
    6: [
        "Define classes with attributes, methods and constructors.",
        "Encapsulate state with properties and understand name mangling.",
        "Reuse behaviour through inheritance and ``super()``.",
        "Apply polymorphism via abstract base classes and duck typing.",
        "Implement magic methods and choose composition over inheritance when appropriate.",
    ],
    7: [
        "Read and write files safely with context managers and the right encodings.",
        "Manipulate filesystem paths portably with ``pathlib``.",
        "Parse and serialise JSON and CSV, including error handling.",
        "Apply regular expressions to extract structured fields from logs.",
        "Assemble a small end-to-end data pipeline.",
    ],
    8: [
        "Explain the relational model and when a database beats a flat file.",
        "Create schemas and tables with SQLite, including constraints.",
        "Perform CRUD operations safely using parameterised queries.",
        "Group multiple statements into atomic transactions.",
        "Use SQLAlchemy to map objects to tables, and connect to external databases.",
    ],
    9: [
        "Annotate functions and classes with type hints and reason about static checking.",
        "Work with dates, times and time zones correctly.",
        "Build a command-line interface with ``argparse`` subcommands.",
        "Consume an HTTP API with ``requests``, handling timeouts and status codes.",
        "Write unit tests with pytest fixtures, parametrisation and mocking.",
        "Structure and package a project for distribution.",
    ],
}



def build_module_index(number: int, topics: Sequence[Topic]) -> str:
    """Render the index README for one module."""
    directory = MODULE_DIRS[number]
    title = MODULE_TITLES[number]
    module_topics = [t for t in topics if t.module == number]

    parts: list[str] = [
        f"# Module {number} — {title}",
        "",
        f"**Directory:** `{directory}/` &nbsp;|&nbsp; "
        f"**ROBO-X milestone:** M{number} &nbsp;|&nbsp; "
        f"**Topics:** {len(module_topics)}",
        "",
        MODULE_BLURBS.get(number, ""),
        "",
        "## What you will be able to do",
        "",
    ]
    parts += [f"- {outcome}" for outcome in MODULE_OUTCOMES.get(number, [])]
    parts += [
        "",
        "## Topics",
        "",
        "| # | Topic | Exercises | Quiz |",
        "| --- | --- | --- | --- |",
    ]
    for topic in sorted(module_topics, key=lambda t: t.topic_id):
        parts.append(
            f"| {topic.topic_id} | "
            f"[{topic.title}]({topic.directory}/README.md) | "
            f"{topic.medium_count} M / {topic.hard_count} H | "
            f"{topic.quiz_count} |"
        )

    parts += [
        "",
        "## How to work through this module",
        "",
        "1. Read each topic's `lesson.ipynb` end to end, running every code cell.",
        "2. Attempt `exercises.ipynb` before opening `solution.ipynb`.",
        "3. Take `quiz.ipynb` and re-read any section you failed.",
        "4. Complete the mini-project and the ROBO-X challenge.",
        "5. Move on only when the topic's self-assessment passes.",
        "",
        "## Navigation",
        "",
    ]
    if number > 1:
        prev_dir = MODULE_DIRS[number - 1]
        parts.append(
            f"* Previous module: [`{prev_dir}/README.md`](../{prev_dir}/README.md)"
        )
    else:
        parts.append(
            "* Start here — see "
            "[`00_course_orientation/README.md`](../00_course_orientation/README.md) first."
        )
    if number < max(MODULE_DIRS):
        next_dir = MODULE_DIRS[number + 1]
        parts.append(f"* Next module: [`{next_dir}/README.md`](../{next_dir}/README.md)")
    else:
        parts.append(
            "* Finish with the [capstone projects](../10_capstone_projects/README.md)."
        )
    parts.append("* Course path: [`LEARNING_PATH.md`](../LEARNING_PATH.md)")
    parts.append("")
    return "\n".join(parts)


def write_module_indexes(root: Path, topics: Sequence[Topic]) -> list[Path]:
    """Write ``README.md`` for every module directory. Returns paths written."""
    written: list[Path] = []
    for number, directory in MODULE_DIRS.items():
        path = root / directory / "README.md"
        path.write_text(build_module_index(number, topics), encoding="utf-8")
        written.append(path)
    return written

