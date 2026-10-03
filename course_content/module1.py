"""Module 1 — Getting Started with Python (topics 1.1 - 1.8)."""

from __future__ import annotations

from tools.coursegen.dsl import (
    BULLETS,
    CODE,
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

TOPICS = []

TOPICS.append(
    topic(
        topic_id="1.1",
        title="Introduction to Python",
        module=1,
        module_title="Getting Started with Python",
        directory="01_introduction_to_python",
        summary=(
            "Where Python came from, why an entire industry chose it, and how to "
            "think about it as a language designed to be read."
        ),
        why_it_matters=(
            "Choosing a language is a long-term commitment. Most of the software you "
            "will write in the next decade — fleet managers, control loops, data "
            "pipelines, model-serving services — is Python. Understanding *why* the "
            "language looks the way it does turns syntax from arbitrary rules into "
            "predictable engineering outcomes: you will stop fighting the language and "
            "start using its trade-offs deliberately."
        ),
        objectives=[
            "Explain where Python came from and which design decisions follow from its origins.",
            "Justify Python for at least four classes of engineering problem, and name one domain where you would not choose it.",
            "Predict how Python's design choices affect real cost: readability, iteration speed, and deployment.",
            "Explain how the interpreter, source code and bytecode relate to each other.",
            "Set expectations correctly about what Python is and is not in a robotics stack.",
        ],
        prerequisites=[
            "No programming experience is assumed.",
            "Ability to install software and open a terminal (topic 1.2 covers this in detail).",
        ],
        mental_model=[
            MD(
                "Python is a **specification implemented by an interpreter**. That "
                "distinction explains almost everything you will observe: why there is "
                "no compilation step you can see, why errors surface at runtime rather "
                "than build time, and why the same code can behave differently on "
                "different machines with different versions."
            ),
            MD(
                "A useful second model is the **batteries-included, glue-language** "
                "idea. Python does not try to be the fastest language; it tries to be "
                "the fastest language *to write correct software in*, and then delegates "
                "the hot inner loops to libraries written in C, C++ or Fortran."
            ),
            CODE(
                '''
# Three layers you are really working with
#
#  1. YOUR SOURCE     robot_distance = 3.5          <- you write this
#  2. BYTECODE        a compact, fast-to-execute form produced by the compiler
#  3. MACHINE CODE    what the CPU actually runs (inside CPython's C engine)
#
# Only layer 3 is native. Layers 1 and 2 are portable, which is exactly why a
# Python program written on a laptop runs unchanged on a Raspberry Pi.

import dis

def euclidean_distance(dx: float, dy: float) -> float:
    """Return the straight-line distance between two points."""
    return (dx ** 2 + dy ** 2) ** 0.5

dis.dis(euclidean_distance)
'''
            ),
            NOTE(
                "Why this matters later",
                "When you profile a robot loop in Module 9 and discover that a "
                "pure-Python hot path is too slow, this model tells you the answer: "
                "move that code down a layer, do not abandon the language.",
            ),
        ],
        terminology=[
            ["Interpreter", "The program that reads and executes your Python source, one instruction at a time (CPython) or from compiled bytecode (PyPy)."],
            ["Source code (.py)", "The human-readable text you write. This is the artefact under version control and the artefact reviewed in code review."],
            ["Bytecode (.pyc)", "An intermediate, compact instruction set produced by the compiler and cached in __pycache__ so start-up is fast."],
            ["CPython", "The reference implementation of Python, written in C. It is what `python3` almost always means."],
            ["PyPy", "An alternative implementation that JIT-compiles bytecode to native code; faster for long-running, compute-heavy loops."],
            ["Implementation", "A program that conforms to the Python language specification. There are several; CPython dominates."],
            ["High-level language", "A language that abstracts away memory management and machine details, in exchange for less direct control."],
            ["Garbage collector", "The runtime component that reclaims memory for objects you no longer reference."],
            ["Batteries included", "Design philosophy: the standard library ships solutions for common tasks so you write less code and depend on less."],
            ["Duck typing", "Using an object based on what it can do rather than the class it belongs to: if it has .move() and .read_sensor(), drive it."],
        ],
        lesson={
            "conceptual_explanation": [
                MD(
                    "Python was created by **Guido van Rossum** at CWI in the late 1980s "
                    "as a successor to ABC, a language built for teaching programming. "
                    "Van Rossum's goal was not novelty: it was to design a language that a "
                    "programmer could *read* six months after writing it, and that could "
                    "be learned in an afternoon."
                ),
                MD(
                    "That single goal explains the features you will meet in this course:"
                ),
                TABLE(
                    ["Design decision", "What it buys you", "What it costs you"],
                    [
                        [
                            "Indentation is syntax, not style",
                            "Blocks are visible with no braces; no dangling-brace bugs",
                            "Tab/space mistakes become syntax errors",
                        ],
                        [
                            "Everything is an object",
                            "Uniform operations: `5 .bit_length()`, `[1,2].count(1)`",
                            "Some operations are slower than specialised types",
                        ],
                        [
                            "Dynamic typing",
                            "Fast iteration; no type declarations to maintain",
                            "Errors found at runtime, not compile time (fixed in 9.1)",
                        ],
                        [
                            "Batteries included",
                            "`json`, `sqlite3`, `logging`, `unittest` in the stdlib",
                            "Some standard-library choices are conservative",
                        ],
                        [
                            "Zero-cost-ish abstractions",
                            "`for` works over files, sockets, generators, dict keys",
                            "Iteration protocol is invisible until you read the docs",
                        ],
                    ],
                ),
                MD(
                    "**Where Python is used, concretely.** Robotics is the obvious one for "
                    "this course, but the language's reach explains why so much robotics "
                    "software exists: ROS 2 core packages, G-code generators, SLAM "
                    "tool-chains, flight-stack ground software and every ML framework "
                    "whose research code must be released. Adjacent fields — data "
                    "engineering, scientific computing, web backends, ML training, "
                    "network automation — share the same code, the same libraries and the "
                    "same hiring pool."
                ),
                MD(
                    "**Where Python is the wrong choice.** Be honest about this now, "
                    "because engineering judgement is graded throughout the course:"
                ),
                BULLETS(
                    [
                        "Hard real-time control loops. A Python thread scheduler cannot guarantee a 1 kHz motor tick. Real-time work belongs in C, Rust or an RTOS; Python supervises it.",
                        "Memory-constrained microcontrollers. The interpreter itself needs hundreds of KB; use MicroPython or firmware instead.",
                        "Hot inner loops over large arrays. Fine in NumPy, disastrous in pure Python — measure, then optimise.",
                    ]
                ),
                NOTE(
                    "The honest trade",
                    "Python trades peak speed for development speed and readability. In "
                    "robotics that is usually the correct trade, because the hard part is "
                    "the algorithm, not the arithmetic. It is the wrong trade inside a "
                    "1 kHz servo loop — which is why every serious stack splits the "
                    "system into a fast layer and a smart layer.",
                ),
            ],
            "formal_theory": [
                MD(
                    "Three formal ideas underpin everything in this module."
                ),
                EQUATION(
                    "source code  --compile-->  bytecode  --interpret-->  machine code"
                ),
                STEPS(
                    [
                        "**Compilation step.** The compiler parses your source into an abstract syntax tree, performs a small number of semantic checks (indentation consistency, syntax), and emits bytecode. No type checking happens here.",
                        "**Bytecode caching.** Bytecode is written to `__pycache__/<name>.cpython-312.pyc`. Running the module again skips recompilation, which is why the *second* run of a script is measurably faster.",
                        "**Interpretation / execution.** The interpreter (a C program) walks the bytecode and performs each instruction. This is a single pass with no whole-program optimisation — which is why CPython is fast to start and slower to run.",
                    ]
                ),
                MD(
                    "Second, **the name-binding model**. Python has no declarations. A "
                    "statement such as `distance = 3.5` creates a *binding* — an entry in "
                    "a table mapping a name to an object. Rebinding (`distance = 4.0`) "
                    "replaces the entry; it does not modify the old object. Topic 1.4 "
                    "makes this concrete; it is the root cause of most 'Python mutated my "
                    "variable' confusion."
                ),
                MD(
                    "Third, **object identity and value**. Python objects carry an "
                    "identity (`id()`), a type (`type()`) and a value (`==`). Mutable "
                    "objects (`list`, `dict`, `set`, most class instances) can be changed "
                    "in place; immutable ones (`int`, `float`, `str`, `tuple`, `frozenset`) "
                    "cannot. Nearly every subtle bug in this course traces back to "
                    "confusing identity with value, or passing a mutable object where a "
                    "copy was expected."
                ),
                CODE(
                    '''
# Value vs identity — the distinction that prevents a whole class of bugs
first = [1, 2, 3]
second = [1, 2, 3]

print("equal?      ", first == second)        # True  -> same VALUE
print("identical?  ", first is second)        # False -> different OBJECTS
print("id(first)   ", id(first))
print("id(second)  ", id(second))

alias = first
alias.append(4)
print("first after alias.append(4):", first)  # [1, 2, 3, 4] -> alias IS first
print("second is unaffected:     ", second)   # [1, 2, 3]
'''
                ),
                TIP(
                    "Rule of thumb",
                    "Use `==` to ask 'are these the same contents?' and `is` only to ask "
                    "'is this literally the same object?'. In practice `is` appears "
                    "almost exclusively in `is None` and `is not None` checks.",
                ),
            ],
            "syntax": [
                MD(
                    "Python's surface syntax is small. Almost everything is an "
                    "*expression statement*: evaluate an expression, bind its value, "
                    "discard it. The table below is the whole language at a glance."
                ),
                TABLE(
                    ["Construct", "Syntax", "Meaning"],
                    [
                        ["Binding", "`distance = 3.5`", "Bind the name `distance` to a float"],
                        ["Multiple binding", "`x, y = 1, 2`", "Unpack an iterable into names"],
                        ["Call", "`robot.move(1.5)`", "Call, then discard the return value"],
                        ["Keyword argument", "`robot.move(1.5, speed_mps=0.8)`", "Pass by name"],
                        ["Block", "`if cond:` + indented body", "Colon opens, indentation closes"],
                        ["Loop", "`for x in xs:` / `while cond:`", "Repeat"],
                        ["Function", "`def f(a, b=2):`", "Define; body must be indented"],
                        ["Class", "`class Robot:`", "Define a type and its methods"],
                        ["Import", "`import math` / `from math import pi`", "Bind names from a module"],
                        ["Context manager", "`with open(p) as f:`", "Guaranteed cleanup"],
                    ],
                ),
                CODE(
                    '''
# Every Python program is built from these pieces.
from shared import SimulatedRobot            # import

robot = SimulatedRobot(name="robo-x-01")     # binding + call
distance = robot.read_sensor("distance")    # binding
battery = robot.status()["battery_pct"]     # subscription + binding

if distance < 1.0:                          # conditional
    action = "STOP"
elif distance < 2.5:
    action = "SLOW"
else:
    action = "CRUISE"

while battery > 5.0:                        # loop
    robot.idle(0.1)
    battery = robot.status()["battery_pct"]

print(f"{action=} {distance=} {battery=}")
'''
                ),
                NOTE(
                    "Read that cell as a whole",
                    "Every construct above appears in this course many times. By topic "
                    "4.8 you will be writing it reflexively; by module 9 you will be "
                    "designing APIs around it.",
                ),
            ],
