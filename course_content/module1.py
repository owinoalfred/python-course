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
            "basic_examples": [
                MD("Start by using Python as a calculator on real robot numbers."),
                CODE(
                    '''
# Battery endurance: how long can this robot work?
battery_wh = 48.0            # watt-hours available
robot_mass_kg = 12.5
drive_efficiency = 0.72      # fraction of electrical energy that becomes motion

specific_energy_wh_per_kg = battery_wh / robot_mass_kg
usable_wh = battery_wh * drive_efficiency
runtime_hours = usable_wh / 15.0            # 15 W average draw while driving

print(f"Specific energy : {specific_energy_wh_per_kg:.2f} Wh/kg")
print(f"Usable energy   : {usable_wh:.1f} Wh")
print(f"Drive endurance : {runtime_hours:.2f} h ({runtime_hours * 60:.0f} min)")
'''
                ),
                MD(
                    "Note the deliberate choice: the names carry units. "
                    "`battery_wh` says *what unit* the number is in. In engineering code, "
                    "a unitless name like `battery` is a latent bug — someone will "
                    "eventually write `robot.move(battery)`."
                ),
                CODE(
                    '''
# Comparing two candidate robots on several criteria at once.
candidates = {
    "robo-x-mini":  {"wh": 48.0,  "mass_kg": 12.5, "draw_w": 15.0},
    "robo-x-heavy": {"wh": 96.0,  "mass_kg": 30.0, "draw_w": 22.0},
    "robo-x-mini2": {"wh": 24.0,  "mass_kg": 7.5,  "draw_w": 11.0},
}

for name, spec in candidates.items():
    endurance_h = (spec["wh"] * 0.72) / spec["draw_w"]
    print(f"{name:<14} mass={spec['mass_kg']:>5.1f} kg  endurance={endurance_h:>4.2f} h")

# Which robot gives the most endurance per kilogram?
best = max(
    candidates.items(),
    key=lambda item: (item[1]["wh"] * 0.72) / item[1]["draw_w"] / item[1]["mass_kg"],
)
print(f"\\nBest energy density: {best[0]}")
'''
                ),
                WARN(
                    "A trap you have not met yet",
                    "`name` is bound inside the `for` loop, and `spec` too. After the "
                    "loop, both still hold the *last* values. This is correct Python, and "
                    "it surprises almost everyone once. Topic 2.2 covers loop variable "
                    "scope; topic 4.3 covers it properly.",
                ),
            ],
            "intermediate_examples": [
                MD(
                    "Real programs compute, compare and decide. The next example is the "
                    "kind of function you would extract on day two of a real project."
                ),
                CODE(
                    '''
def endurance_hours(battery_wh: float, mass_kg: float, draw_w: float,
                    efficiency: float = 0.72) -> float:
    """Return drive endurance in hours.

    Args:
        battery_wh: usable battery capacity in watt-hours.
        mass_kg: robot mass in kilograms (used for a sanity warning, not the formula).
        draw_w: average electrical draw while driving, in watts.
        efficiency: drivetrain efficiency in [0, 1].

    Returns:
        Estimated driving hours.

    Raises:
        ValueError: if any argument is non-positive or efficiency is out of range.
    """
    if battery_wh <= 0 or draw_w <= 0 or mass_kg <= 0:
        raise ValueError("battery, draw and mass must all be positive")
    if not 0.0 < efficiency <= 1.0:
        raise ValueError("efficiency must be in (0, 1]")
    return (battery_wh * efficiency) / draw_w


print(f"{endurance_hours(48.0, 12.5, 15.0):.2f} h")

try:
    endurance_hours(48.0, 12.5, 0.0)
except ValueError as exc:
    print(f"rejected bad input: {exc}")
'''
                ),
                MD(
                    "Notice three decisions an engineer made, not a coder:"
                ),
                BULLETS(
                    [
                        "The docstring states *what the number means and in what unit* — the single most useful comment in a robotics codebase.",
                        "Invalid input raises instead of returning a wrong number. A silent `-1.0` would propagate into mission planning.",
                        "`mass_kg` is accepted but unused in the formula. It is there so the signature stays stable when the model gains a payload term later — and so the sanity check has context.",
                    ]
                ),
                CODE(
                    '''
# Turning a pile of readings into a decision — the shape of most robot logic.
readings = [2.9, 2.7, 2.4, 1.8, 1.2, 0.7, 0.6, 2.1]

def clearance_action(clearances, stop_m: float = 0.8, slow_m: float = 2.0) -> str:
    """Return the motion command for the worst reading in `clearances`."""
    if not clearances:
        return "HALT"                      # no data -> fail safe
    nearest = min(clearances)
    if nearest < stop_m:
        return "STOP"
    if nearest < slow_m:
        return "SLOW"
    return "CRUISE"


print("worst-case clearance:", min(readings))
print("action              :", clearance_action(readings))

# Mean would have said CRUISE — the classic "averaging away a hazard" bug.
print("mean clearance      :", round(sum(readings) / len(readings), 2))
print("action if averaged  :", clearance_action([sum(readings) / len(readings)]))
'''
                ),
                NOTE(
                    "Engineering judgement",
                    "Robotics code is full of places where the statistically 'correct' "
                    "summary is the unsafe choice. Obstacles, battery levels and "
                    "temperature are all cases where the worst reading, not the average, "
                    "is what the safety system must see.",
                ),
            ],
            "advanced_examples": [
                MD(
                    "At the advanced end of Module 1 there is no new syntax — only "
                    "better structure. The example below previews several later topics: "
                    "duck typing, defensive defaults, and separating policy from "
                    "mechanism."
                ),
                CODE(
                    '''
from dataclasses import dataclass          # topic 9.1: dataclasses
from typing import Protocol                  # topic 9.1: typing


@dataclass(frozen=True, slots=True)
class Waypoint:
    """A navigation goal. Immutable, so it can be shared safely."""
    name: str
    x_m: float
    y_m: float


class Drivable(Protocol):
    """Anything with these two methods can be commanded (topic 9.1)."""

    def move(self, distance_m: float) -> float: ...
    def read_sensor(self, channel: str) -> float: ...


def drive_to_next_waypoint(vehicle: Drivable, waypoints, clearance_limit_m: float = 1.0):
    """Advance through `waypoints`, stopping before any clearance violation.

    Returns the list of waypoint names actually reached.

    This is policy; `vehicle` is mechanism. Separating them is what makes the
    logic testable without hardware (topic 4.1, 6.7).
    """
    reached: list[str] = []
    for waypoint in waypoints:
        clearance = vehicle.read_sensor("distance")
        if clearance < clearance_limit_m:
            break                              # fail safe, do not raise here
        vehicle.move(float(abs(waypoint.x_m)))
        reached.append(waypoint.name)
    return reached


from shared import SimulatedRobot            # the mechanism
robot = SimulatedRobot(name="robo-x-01", battery_wh=200.0)
plan = [Waypoint("dock-a", 1.0, 0.0), Waypoint("aisle-4", 2.0, 0.0), Waypoint("bay-7", 2.0, 0.0)]

print("reached:", drive_to_next_waypoint(robot, plan))
print("battery used: %.2f Wh" % (200.0 - robot.status()["battery_wh"]))
'''
                ),
                TIP(
                    "Read it twice",
                    "First read: note that `vehicle` is never type-checked. Second "
                    "read: note *why* that is deliberate — it lets you substitute a real "
                    "robot, a simulator, or a mock in tests without changing a line. "
                    "Duck typing is not laziness; it is a design decision with costs, "
                    "which you will price in topic 9.1.",
                ),
            ],
            "code_walkthrough": [
                MD(
                    "One complete program, then dissected. Run it first, then read the "
                    "annotation table that follows it."
                ),
                CODE(
                    '''
"""robo_x_preflight.py — run the robot's pre-flight checks.

Kept as a script (not a notebook) on purpose: this is what a
pre-flight check actually looks like on a real robot.
"""
from shared import SimulatedRobot


def preflight(name: str, battery_wh: float) -> tuple[bool, list[str]]:
    """Run pre-flight checks. Return (ok, list of failure messages)."""
    failures: list[str] = []
    robot = SimulatedRobot(name=name, battery_wh=battery_wh)

    if battery_wh < 20.0:
        failures.append(f"battery {battery_wh:.1f} Wh below 20 Wh minimum")
    if robot.read_sensor("distance") < 0.5:
        failures.append("obstacle within 0.5 m at start")
    temp = robot.read_sensor("temperature")
    if temp > 45.0:
        failures.append(f"controller too hot: {temp:.1f} C")

    return (not failures), failures


if __name__ == "__main__":
    ok, failures = preflight("robo-x-01", battery_wh=48.0)
    print(f"pre-flight: {'PASS' if ok else 'FAIL'}")
    for failure in failures:
        print(f"  - {failure}")
'''
                ),
            ],
            "line_by_line": [
                TABLE(
                    ["Line", "What it does", "Why it is written that way"],
                    [
                        [
                            "`from shared import SimulatedRobot`",
                            "Binds one name from a module",
                            "Explicit import; `import shared` would force `shared.SimulatedRobot(...)` everywhere",
                        ],
                        [
                            "`def preflight(...) -> tuple[bool, list[str]]:`",
                            "Defines a function with a declared return shape",
                            "The annotation documents the contract; it is also checked by tools in topic 9.1",
                        ],
                        [
                            "`failures: list[str] = []`",
                            "Creates an empty list and binds it to `failures`",
                            "Accumulating messages beats returning on the first failure: an operator wants the whole list",
                        ],
                        [
                            "`return (not failures), failures`",
                            "Returns a 2-tuple of (ok, messages)",
                            "`not failures` is True only for an empty list — idiomatic and short",
                        ],
                        [
                            "`if __name__ == \"__main__\":`",
                            "Runs only when executed as a script",
                            "Lets the file be imported by tests without side effects (topic 4.8)",
                        ],
                        [
                            "`f\"battery {battery_wh:.1f} Wh below...\"`",
                            "f-string with a format spec",
                            "The number is formatted once, where it is produced — not by the caller",
                        ],
                    ],
                ),
            ],
            "common_mistakes": [
                TABLE(
                    ["Mistake", "What happens", "Fix"],
                    [
                        [
                            "Forgetting that Python is case-sensitive",
                            "`Distance` and `distance` are different names; `NameError` later",
                            "Use `snake_case` for variables/functions, `PascalCase` for classes",
                        ],
                        [
                            "Comparing floats with `==`",
                            "`0.1 + 0.2 == 0.3` is False — binary floating point cannot represent these exactly",
                            "Use `math.isclose(a, b)` or compare rounded values with a tolerance",
                        ],
                        [
                            "Assigning to a name before defining it in a notebook cell",
                            "`NameError` — or worse, a stale value from an earlier run",
                            "Restart the kernel and run top to bottom before trusting output",
                        ],
                        [
                            "Using `type(x) == int` instead of `isinstance(x, int)`",
                            "Fails for subclasses, e.g. `bool` is a subclass of `int`",
                            "`isinstance()` respects inheritance; it is almost always what you want",
                        ],
                        [
                            "Mutating a loop variable inside the loop",
                            "Results depend on the last iteration, and the bug is invisible until data changes",
                            "Bind a new name: `for _, robot in fleet: robot_id = robot.name`",
                        ],
                        [
                            "Printing to debug inside a loop",
                            "Output becomes unreadable exactly when you need it",
                            "Collect into a list and print once at the end",
                        ],
                    ],
                ),
            ],
            "debugging_techniques": [
                MD(
                    "Debugging is a skill with techniques, not a personality trait. Start "
                    "with these four, in this order:"
                ),
                STEPS(
                    [
                        "**Read the traceback properly.** The last line names the exception; the line above it (file and line number) is where it happened. Python tracebacks point at the *call site*, not always the cause — this is normal, not a bug.",
                        "**Reproduce with the smallest input.** If a 200-reading list fails, try 2 readings. Shrinking a failing case is most of debugging.",
                        "**Check the type and value, not just the variable.** `print(repr(x))` shows the type; `print(f'{x!r} {type(x)}')` also catches `3` vs `3.0` vs `'3'`.",
                        "**Form one hypothesis and test it.** Do not change three things at once; you will not know which fixed it.",
                    ]
                ),
                CODE(
                    '''
# A deliberate bug, then a diagnosis.
def average_readings(readings):
    """Return the mean of `readings`, or 0.0 when empty."""
    return sum(readings) / len(readings)


print(average_readings([2.0, 4.0, 6.0]))   # 4.0 - correct
try:
    print(average_readings([]))
except ZeroDivisionError as exc:
    # The traceback names average_readings, line 3: len(readings) was 0.
    print(f"diagnosis: {exc} -> empty input divides by zero")
'''
                ),
                CODE(
                    '''
# Inspect values the way that actually finds bugs.
samples = [1, 2.0, "3", None, 4.5]

for value in samples:
    print(f"{value!r:<10} type={type(value).__name__:<8} bool={bool(value)}")

# Which of these can be added safely? (topic 5.1 formalises the answer)
for value in samples:
    try:
        total = 1 + value          # type: ignore[operator]
        print(f"1 + {value!r} = {total!r}")
    except TypeError:
        print(f"1 + {value!r} -> TypeError (guard this at the boundary)")
'''
                ),
                TIP(
                    "In a notebook",
                    "Run *Restart Kernel and Run All* before believing any output. Most "
                    "'impossible' notebook bugs are stale state from an earlier cell.",
                ),
            ],
            "best_practices": [
                MD("Habits worth forming in week one. Each is checked later in the course."),
                BULLETS(
                    [
                        "**Name things after what they mean, not what they are.** `distance_m`, not `d`; `battery_wh`, not `b`. Include the unit in the name when the value has one.",
                        "**Prefer the smallest thing that works.** Python has four ways to build a list; the obvious loop beats the clever comprehension until the comprehension is genuinely clearer.",
                        "**Fail loudly at boundaries.** Validate arguments where data enters the system (user input, sensor, file, network), not everywhere. Internal code can trust its own invariants.",
                        "**Keep functions short enough to name.** If you cannot summarise a function in one line, it is doing two jobs.",
                        "**No magic numbers.** `0.72` is a drivetrain efficiency; name it or comment it.",
                        "**Write the docstring for the caller.** Say what the function returns and what raises — not how the loop works.",
                        "**Use the standard library first.** `math`, `statistics`, `json`, `datetime` and `pathlib` are faster to write, faster to run and better tested than your reimplementation.",
                        "**Format with f-strings.** No `.format()`, no `%` operator, no manual `str()` concatenation.",
                    ]
                ),
                CODE(
                    '''
# Before: unclear names, magic numbers, no validation.
def calc(a, b, c):
    return a * 0.72 / c


# After: the name explains itself, the unit is visible, the bound is checked.
DRIVETRAIN_EFFICIENCY = 0.72


def endurance_hours(battery_wh: float, draw_w: float,
                    efficiency: float = DRIVETRAIN_EFFICIENCY) -> float:
    """Return estimated driving hours.

    Args:
        battery_wh: Battery capacity in watt-hours.
        draw_w: Average electrical draw while driving, in watts.
        efficiency: Drivetrain efficiency as a fraction in (0, 1].

    Returns:
        Estimated hours of driving.

    Raises:
        ValueError: If battery_wh or draw_w is not positive.
    """
    if battery_wh <= 0 or draw_w <= 0:
        raise ValueError("battery_wh and draw_w must be positive")
    return (battery_wh * efficiency) / draw_w
'''
                ),
                NOTE(
                    "PEP 8, briefly",
                    "4-space indents, 79-character lines, `snake_case` for functions and "
                    "variables, `PascalCase` for classes, `UPPER_CASE` for constants. "
                    "Consistency beats personal preference, because the reader is always "
                    "someone else — often you, at 2 a.m., during a field failure. "
                    "Topic 9.6 covers tooling for this.",
                ),
            ],
            "performance_considerations": [
                MD(
                    "Module 1 barely touches performance, and that is deliberate — but "
                    "two facts belong in your head from day one."
                ),
                CODE(
                    '''
import time

def bench(fn, *, repeats: int = 100_000) -> float:
    """Return the wall-clock seconds for `repeats` calls of `fn`."""
    start = time.perf_counter()
    for _ in range(repeats):
        fn()
    return time.perf_counter() - start

# Fact 1: function call overhead is real and measurable.
no_op = lambda: None                      # noqa: E731 - benchmarking only
print(f"100k empty calls : {bench(no_op, repeats=100_000) * 1000:8.2f} ms")

# Fact 2: `import` at module scope is cached; importing inside a hot function is not free.
import math
def use_math_inside():
    import math
    return math.sqrt(2.0)

def use_math_outside():
    return math.sqrt(2.0)

print(f"import inside    : {bench(use_math_inside, repeats=100_000) * 1000:8.2f} ms")
print(f"import at top    : {bench(use_math_outside, repeats=100_000) * 1000:8.2f} ms")
'''
                ),
                BULLETS(
                    [
                        "**Measure before optimising.** Topic 1.1's research task has you do this properly; the instinct to guess is the expensive habit.",
                        "**Imports belong at the top of the module** (PEP 8), unless you are deliberately deferring an expensive import to control start-up time.",
                        "**Do not optimise in Module 1.** Write the clearest version. You will profile properly in Module 7 and 9, with real data and real tools.",
                    ]
                ),
                WARN(
                    "The trap",
                    "Micro-optimising before you can explain the algorithm's complexity is "
                    "the single most common way beginners waste a project. An O(n²) "
                    "algorithm rewritten in clever O(n) style still loses to an O(n log n) "
                    "rewrite.",
                ),
            ],
            "pythonic_approaches": [
                MD(
                    "\"Pythonic\" means using the language's strengths — not avoiding "
                    "loops, not being clever. In this module, that means two habits."
                ),
                CODE(
                    '''
# Habit 1: build a value directly instead of starting empty and appending.
readings = [2.9, 2.7, 2.4, 1.8, 1.2]

squares_loop = []
for value in readings:
    squares_loop.append(value ** 2)

squares_direct = [value ** 2 for value in readings]

print(squares_loop)
print(squares_direct)
print("same result:", squares_loop == squares_direct)

# Habit 2: let a function do the work instead of hand-rolling the loop.
print("min/max/sum:", min(readings), max(readings), sum(readings))

# Unpacking beats indexing.
first, *middle, last = readings
print(f"first={first} last={last} middle={middle}")

# enumerate() gives you the index without a manual counter (topic 2.5).
for index, value in enumerate(readings, start=1):
    print(f"  sample {index}: {value}")
'''
                ),
                NOTE(
                    "Calibrate this",
                    "Comprehensions (topic 3.7) are excellent for a single transformation. "
                    "For anything with conditionals, early exits or multiple steps, a plain "
                    "loop is clearer. The test is whether a colleague understands your "
                    "code on first reading — not how compact it is.",
                ),
            ],
            "robotics_connection": [
                MD(
                    "Everything in this topic shows up in a real robot stack within the "
                    "first hour of a deployment:"
                ),
                TABLE(
                    ["Concept", "Where it lives in a robot system"],
                    [
                        ["Interpreter / bytecode", "The Python process on the robot's companion computer"],
                        ["Names and bindings", "Configuration values, live sensor readings, mission state"],
                        ["Value vs identity", "Deciding whether to copy a telemetry list or pass it along"],
                        ["ValueError on bad input", "Rejecting an out-of-range speed before it reaches a motor"],
                        ["Type inspection", "Refusing to average a list that contains `None` from a failed read"],
                        ["Docstring", "The interface contract the rest of the team codes against"],
                        ["Deterministic ordering", "Reproducible logs and reproducible test failures"],
                    ],
                ),
                MD(
                    "**The ROBO-X connection.** In this topic you write ROBO-X's very "
                    "first configuration: the robot's name, battery capacity and a "
                    "pre-flight check. It looks trivial — that is the point. The pattern "
                    "you practise here (read configuration → validate → report → act) is "
                    "the pattern you repeat at every milestone for the rest of the course, "
                    "and it is the pattern that keeps a robot safe when a human makes a "
                    "mistake."
                ),
            ],
            "engineering_example": [
                MD(
                    "**Scenario: a mobile robot's pre-flight decision.** Before ROBO-X "
                    "accepts a mission, three independent things must be true: enough "
                    "battery, a clear path, and a healthy controller. Note the shape of "
                    "the solution: *check everything, report everything, then decide "
                    "once*."
                ),
                CODE(
                    '''
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Outcome of one pre-flight check."""

    name: str
    passed: bool
    detail: str

    def __str__(self) -> str:
        mark = "PASS" if self.passed else "FAIL"
        return f"[{mark}] {self.name}: {self.detail}"


def check_battery(battery_wh: float, minimum_wh: float = 20.0) -> CheckResult:
    """Check that the battery holds enough charge for a mission."""
    return CheckResult(
        "battery",
        battery_wh >= minimum_wh,
        f"{battery_wh:.1f} Wh (need {minimum_wh:.1f} Wh)",
    )


def check_clearance(robot, minimum_m: float = 0.5) -> CheckResult:
    """Check that no obstacle is within `minimum_m` of the robot."""
    clearance = robot.read_sensor("distance")
    return CheckResult(
        "clearance",
        clearance >= minimum_m,
        f"{clearance:.2f} m (need {minimum_m:.2f} m)",
    )


def check_thermal(robot, maximum_c: float = 45.0) -> CheckResult:
    """Check that the controller is below its thermal limit."""
    temp = robot.read_sensor("temperature")
    return CheckResult(
        "thermal",
        temp <= maximum_c,
        f"{temp:.1f} C (limit {maximum_c:.1f} C)",
    )


from shared import SimulatedRobot

robot = SimulatedRobot(name="robo-x-01", battery_wh=48.0)
results = [check_battery(48.0), check_clearance(robot), check_thermal(robot)]

for result in results:
    print(result)

ok = all(result.passed for result in results)
print(f"\\npre-flight {'PASS' if ok else 'FAIL'} - "
      f"{sum(r.passed for r in results)}/{len(results)} checks passed")
'''
                ),
                MD(
                    "**Why this is engineered rather than scripted.** Four decisions carry "
                    "the weight:"
                ),
                BULLETS(
                    [
                        "**Checks do not print; they return.** `check_battery` returns data. The caller decides how to display it, which is what makes the checks testable and reusable in a different UI later.",
                        "**Every check runs.** An `if` chain that stops at the first failure would hide two problems at once. An operator wants the full list before dispatching a technician.",
                        "**The threshold is a parameter with a default**, not a literal buried in the logic. Tuning the fleet becomes a configuration change.",
                        "**Results are immutable** (`frozen=True`), so nobody can mutate a passing result into a failing one downstream.",
                    ]
                ),
                WARN(
                    "The pattern to steal",
                    "This — *collect structured results, then decide once* — is exactly "
                    "what the safety controller in topic 2.1, the fault handler in module "
                    "5 and the telemetry pipeline in module 7 will each be built from.",
                ),
            ],
            "guided_practice": [
                MD(
                    "Do these in order. They take about 15 minutes and prepare you for the "
                    "exercises."
                ),
                STEPS(
                    [
                        "Predict, then run. Before executing the cell below, write down what you expect each line prints. Checking your prediction against reality is where the learning happens.",
                    ]
                ),
                CODE(
                    '''
from shared import SimulatedRobot

robot = SimulatedRobot(name="robo-x-01", battery_wh=48.0)
status = robot.status()

# 1. Predict the type of each expression before running:
print(type(status["battery_pct"]))
print(f"{status['battery_pct']:.0f}%")
print(type(f"{status['battery_pct']:.0f}%"))

# 2. Why does this work?
energy = robot.move(2.0)
print(f"moved 2 m, cost {energy:.3f} Wh")
print(f"remaining: {robot.status()['battery_wh']:.3f} Wh")

# 3. What happens if you ask for a sensor that does not exist?
try:
    robot.read_sensor("pressure")
except Exception as exc:
    print(f"{type(exc).__name__}: {exc}")
'''
                ),
                STEPS(
                    [
                        "Change `robot.move(2.0)` to `robot.move(20.0)` and predict whether it succeeds. Then run it and explain the answer using the energy model (topic 1.5 returns to this).",
                        "Write a two-line function `is_ready_to_move(robot)` that returns `True` only when the robot has more than 25% battery **and** more than 1 m clearance. Test it against the simulator.",
                    ]
                ),
                TIP(
                    "Self-check",
                    "If you cannot explain why `type(f\"{x:.0f}%\")` is `str` while "
                    "`type(x)` is `float`, re-read the *Formal Theory* section on f-strings "
                    "in topic 1.7 before continuing.",
                ),
            ],
            "summary": [
                MD(
                    "Python is an interpreted, dynamically typed, general-purpose language "
                    "whose design goal was readability. It reached that goal well enough "
                    "that it became the dominant language for robotics software, data "
                    "engineering, scientific computing and machine learning."
                ),
                MD(
                    "For this course, three ideas matter most:"
                ),
                STEPS(
                    [
                        "**Names bind to objects.** Assignment creates a binding, not a variable in the C sense. This explains aliasing, default-argument bugs and why mutating an argument does not always surprise you the same way.",
                        "**The language is small, the standard library is large.** You need few built-in statements and many well-tested modules.",
                        "**Every trade-off is a choice.** Python gives up peak speed and static guarantees in exchange for development speed and readability. Knowing which trade you made — and when it stops being the right one — is the skill being assessed in every topic of this course.",
                    ]
                ),
            ],
            "key_takeaways": [
                MD("If you remember nothing else from topic 1.1:"),
                BULLETS(
                    [
                        "Python is a **specification**; CPython is the reference **implementation** you will run.",
                        "`==` compares values; `is` compares object identity. Use `is` almost exclusively for `None` checks.",
                        "Assignment binds a name. It does not copy an object, which is why aliasing matters.",
                        "Validate at system boundaries and raise on bad input; never return a plausible-but-wrong number.",
                        "Name variables with their units (`distance_m`, `battery_wh`) — a unitless name is a latent bug.",
                        "Measure before optimising, and never micro-optimise before you have profiled.",
                        "Python is the right choice for supervision, data and integration; it is the wrong choice inside a hard real-time loop.",
                    ]
                ),
            ],
            "further_exploration": [
                BULLETS(
                    [
                        "[The official tutorial](https://docs.python.org/3/tutorial/) — the canonical introduction; read sections 3-5 alongside this topic.",
                        "[PEP 8 — Style Guide](https://peps.python.org/pep-0008/) — the style rules you will be held to in module 9.",
                        "[PEP 20 — the Zen of Python](https://peps.python.org/pep-0020/) — short, and genuinely useful when two styles compete.",
                        "[CPython source layout](https://github.com/python/cpython/tree/main/Lib) — skim `Lib/` to see how much of Python's power is standard library, not language.",
                        "**Next:** topic 1.2 installs the toolchain and makes this all reproducible on your machine.",
                    ]
                ),
            ],
        },
        exercises=[
            exercise(
                number=1,
                title="Battery endurance estimator with validation",
                difficulty="MEDIUM",
                learning_objectives=[
                    "Combine arithmetic operators into a meaningful engineering formula",
                    "Validate inputs and raise informative errors",
                    "Document a function's contract with a docstring",
                ],
                concepts_tested=[
                    "arithmetic operators",
                    "comparison operators",
                    "functions (introductory)",
                    "value validation",
                ],
                problem_statement=(
                    "ROBO-X needs an endurance estimate before it accepts a mission. Given a "
                    "battery capacity, a robot mass and an average electrical draw while "
                    "driving, compute how many hours the robot can drive. The drivetrain is "
                    "72% efficient, so only that fraction of stored energy becomes motion."
                ),
                requirements=[
                    "Define `endurance_hours(battery_wh, mass_kg, draw_w, efficiency=0.72)`.",
                    "Return a float: `(battery_wh * efficiency) / draw_w`.",
                    "Raise `ValueError` with a message naming the offending argument if `battery_wh`, `mass_kg` or `draw_w` is not positive.",
                    "Raise `ValueError` if `efficiency` is outside the range (0, 1].",
                    "Include a docstring stating units, the return value and the exception raised.",
                ],
                constraints=[
                    "Use no external libraries.",
                    "Do not use `print()` inside the function; return values.",
                    "Mass affects the sanity warning only, not the formula.",
                ],
                input_description=(
                    "`battery_wh`: float, watt-hours. `mass_kg`: float, kilograms. "
                    "`draw_w`: float, watts. `efficiency`: float in (0, 1]."
                ),
                expected_output=(
                    "A float number of hours. Raises `ValueError` for non-positive "
                    "arguments or an out-of-range efficiency."
                ),
                example_input="endurance_hours(48.0, 12.5, 15.0)",
                example_output="2.304",
                edge_cases=[
                    "`battery_wh == 0` — must raise, not return `0.0` (an estimate of zero runtime is a false claim).",
                    "`efficiency == 1.0` — valid; the boundary is inclusive.",
                    "`efficiency == 0.0` — invalid.",
                    "`mass_kg` unused in the formula but still validated.",
                ],
                hints=[
                    "Write the validation first, before the calculation.",
                    "A single `if` can check several arguments at once.",
                    "`not 0.0 < efficiency <= 1.0` expresses the exclusive-inclusive range compactly.",
                ],
                success_criteria=[
                    "Returns 2.304 for the example.",
                    "All four validation cases raise `ValueError` with distinct messages.",
                    "A docstring documents units, return and raises.",
                    "No `print()` inside the function.",
                ],
                optional_extension=(
                    "Return a `(hours, warnings)` tuple where warnings flags "
                    "endurance under 1 hour, and update the callers."
                ),
            ),
            exercise(
                number=2,
                title="Value-versus-identity: telemetry aliasing detector",
                difficulty="MEDIUM",
                learning_objectives=[
                    "Distinguish `==` from `is` and explain the difference",
                    "Predict how rebinding and in-place mutation affect other names",
                    "Write assertions that distinguish the two behaviours",
                ],
                concepts_tested=[
                    "object identity",
                    "mutable vs immutable types",
                    "rebinding",
                    "assert statements",
                ],
                problem_statement=(
                    "A telemetry pipeline passes lists between functions. Determine whether "
                    "two names refer to the same underlying object or merely to equal "
                    "contents, and report what happens when one is mutated in place."
                ),
                requirements=[
                    "Define `same_object(a, b)` returning `True` only if `a is b`.",
                    "Define `equal_contents(a, b)` returning `True` only if `a == b`.",
                    "Define `mutation_effect(first, second)` that returns `\"shared\"` if "
                    "mutating `first` changes `second`, else `\"independent\"`.",
                    "Return the *string* `'independent'` when the two lists are unaffected by each other.",
                    "Assert the behaviour on at least four cases including two aliases of one list.",
                ],
                constraints=[
                    "Do not use `id()` in the returned values.",
                    "`mutation_effect` must perform the mutation on a *copy*, so the caller's data is unchanged.",
                ],
                input_description="Two Python objects of any type.",
                expected_output=(
                    "Three booleans/strings describing identity, equality and mutation coupling."
                ),
                example_input=(
                    "a = [1, 2, 3]\nb = [1, 2, 3]\n"
                    "same_object(a, b)      -> False\n"
                    "equal_contents(a, b)   -> True\n"
                    "mutation_effect(a, b)  -> 'independent'"
                ),
                example_output="False\nTrue\n'independent'",
                edge_cases=[
                    "Two names bound to the same list must report `'shared'`.",
                    "Empty lists: `[], []` are equal but not identical.",
                    "Integers: `x = 1000; y = 1000` may or may not be identical (small-int caching) — your code must not assume either.",
                    "Immutable values (`5` and `5.0`) can never be 'shared' by mutation.",
                ],
                hints=[
                    "`list(first)` makes a shallow copy; use it before mutating.",
                    "`a is b` is the identity operator, not a comparison function.",
                ],
                success_criteria=[
                    "All four identity cases behave correctly.",
                    "`mutation_effect` does not modify its arguments.",
                    "Each returned value is explained in a one-line comment.",
                ],
                optional_extension=(
                    "Add `deep_copy_report(a, b)` that detects nested aliasing (lists inside "
                    "lists) using `copy.deepcopy`."
                ),
            ),
            exercise(
                number=3,
                title="Worst-case safety rule versus statistical average",
                difficulty="MEDIUM",
                learning_objectives=[
                    "Apply conditionals to encode a safety policy",
                    "Argue why averaging hides hazards in sensor data",
                    "Compare two decision functions on the same data",
                ],
                concepts_tested=[
                    "if/elif/else",
                    "min vs mean",
                    "fail-safe defaults",
                    "safety engineering reasoning",
                ],
                problem_statement=(
                    "A drone's forward-collision rule must trigger on the **worst** reading "
                    "in a scan window, never the average. Implement both policies and show "
                    "on real data why the average is unsafe."
                ),
                requirements=[
                    "Define `clearance_action(readings, stop_m=0.8, slow_m=2.0)` using the worst reading.",
                    "Return exactly one of `'STOP'`, `'SLOW'`, `'CRUISE'` or `'HALT'`.",
                    "Return `'HALT'` when `readings` is empty or all values are `None` — no data means fail safe.",
                    "Define `average_action(readings, stop_m=0.8, slow_m=2.0)` using the mean.",
                    "Demonstrate on a window where the two disagree, and assert that the worst-case rule is the stricter one.",
                ],
                constraints=[
                    "`HALT` must take priority over any computed action.",
                    "Ignore `None` values only in `average_action`; the safety rule must consider a `None` as a reason to `HALT`.",
                ],
                input_description=(
                    "`readings`: a sequence of distances in metres, possibly containing "
                    "`None` for failed reads."
                ),
                expected_output="One action string per function, from the fixed vocabulary.",
                example_input="clearance_action([2.9, 2.4, 1.9, 1.1, 0.6, 0.5])",
                example_output="'STOP'",
                edge_cases=[
                    "Empty list -> `'HALT'`.",
                    "All readings `None` -> `'HALT'`.",
                    "Exactly at `stop_m` -> not a stop (boundary is exclusive below).",
                    "Exactly at `slow_m` -> `'CRUISE'` (boundary is exclusive below).",
                ],
                hints=[
                    "Compute the worst reading with `min()` *after* validating that the list is usable.",
                    "Write the disagreeing example by hand first: pick a long run of far readings and one very close reading.",
                ],
                success_criteria=[
                    "All four boundary and empty cases behave as specified.",
                    "A demonstration shows the mean giving `'CRUISE'` where the worst case gives `'STOP'`.",
                    "The `None` handling differs correctly between the two functions.",
                ],
                optional_extension=(
                    "Add a third policy `consecutive_stop_action` that requires two "
                    "consecutive readings below `stop_m` before stopping, to model filter lag."
                ),
            ),
            exercise(
                number=4,
                title="Configuration validator for robot commissioning",
                difficulty="MEDIUM",
                learning_objectives=[
                    "Validate a set of configuration values and report all problems at once",
                    "Use boolean logic to combine independent checks",
                    "Design a report format an operator can act on",
                ],
                concepts_tested=[
                    "boolean operators (and/or/not)",
                    "accumulating errors",
                    "dictionary access",
                    "input validation",
                ],
                problem_statement=(
                    "ROBO-X ships a configuration dictionary. A single missing or invalid "
                    "key must not stop validation: an operator commissioning ten robots "
                    "wants the complete list of problems in one pass."
                ),
                requirements=[
                    "Define `validate_config(config)` taking a dict and returning a list of human-readable error strings.",
                    "Check: `name` non-empty string; `battery_wh` a number in (0, 200]; `max_speed_mps` in (0, 3.0]; `sensors` a list containing `'distance'`.",
                    "Check: every key in `REQUIRED_KEYS` is present; report missing keys as `'missing key: <name>'`.",
                    "An empty list means no errors.",
                    "Return errors in a deterministic order: missing keys first, then value errors in the order of `REQUIRED_KEYS`.",
                ],
                constraints=[
                    "Do not raise; collect and return.",
                    "Do not mutate the input dictionary.",
                    "Use `isinstance(x, (int, float))` and explicitly reject `bool`.",
                ],
                input_description=(
                    "A dict that may be missing keys, may contain wrong types, and may "
                    "contain `True` where a number is required."
                ),
                expected_output="A list of zero or more error strings, in deterministic order.",
                example_input="validate_config({'name': '', 'battery_wh': 500, 'sensors': ['temperature']})",
                example_output="['missing key: max_speed_mps', 'name must be a non-empty string', 'battery_wh must be in (0, 200]', 'sensors must include distance']",
                edge_cases=[
                    "`battery_wh=True` — `bool` is a subclass of `int` in Python and must be rejected.",
                    "`name=123` — wrong type, not merely empty.",
                    "A config with extra unknown keys must not produce errors.",
                    "Value `0` and value `200` are both out of range (exclusive bounds).",
                ],
                hints=[
                    "Loop over `REQUIRED_KEYS` and use `continue` after recording a missing key.",
                    "`isinstance(x, bool)` is True for `True` and `False`; check it first.",
                    "Sorting is unnecessary — iterate over `REQUIRED_KEYS`, not over `config`.",
                ],
                success_criteria=[
                    "Example produces exactly the four errors shown, in that order.",
                    "`True` as a numeric value is rejected.",
                    "Extra keys produce no errors.",
                    "Input dictionary is unchanged after the call.",
                ],
                optional_extension=(
                    "Return a `(errors, warnings)` tuple, where a battery above 150 Wh "
                    "produces a warning rather than an error."
                ),
            ),
            exercise(
                number=5,
                title="Worst-case planning from a distance scan",
                difficulty="MEDIUM",
                learning_objectives=[
                    "Iterate over data to derive a decision",
                    "Combine loop, condition and arithmetic",
                    "Express a safety invariant as an assertion",
                ],
                concepts_tested=[
                    "for loops",
                    "if statements",
                    "min/max built-ins",
                    "assertions",
                ],
                problem_statement=(
                    "Given a forward scan of distances, produce the safe travel distance "
                    "for this cycle: stop one metre short of the nearest obstacle, never "
                    "exceed the configured maximum, and never go negative."
                ),
                requirements=[
                    "Define `safe_travel_m(readings, max_step_m=0.5, margin_m=1.0)`.",
                    "Return `min(max_step_m, nearest - margin_m)` clamped at `0.0`.",
                    "Return `0.0` when `readings` is empty (fail safe).",
                    "Ignore readings that are `None`; if all are `None`, return `0.0`.",
                    "Assert in a test that the result is never greater than `max_step_m` for any input.",
                ],
                constraints=[
                    "Do not use `max()` to clamp — write the conditional explicitly at least once so the logic is visible.",
                    "The function must not mutate `readings`.",
                ],
                input_description="A sequence of metres-to-obstacle readings; `None` marks a failed read.",
                expected_output="A float in `[0.0, max_step_m]`.",
                example_input="safe_travel_m([4.2, 3.8, 3.1, None, 2.9], max_step_m=0.5, margin_m=1.0)",
                example_output="0.5",
                edge_cases=[
                    "Nearest obstacle closer than the margin -> `0.0`.",
                    "Empty list -> `0.0`.",
                    "All `None` -> `0.0`.",
                    "Very distant obstacle -> exactly `max_step_m`, not more.",
                ],
                hints=[
                    "Filter the `None` values first, then decide whether anything remains.",
                    "`min(a, b)` handles the two-way cap; the negative clamp still needs a conditional.",
                ],
                success_criteria=[
                    "Example returns `0.5`.",
                    "Obstacle at 0.9 m with a 1.0 m margin returns `0.0`.",
                    "Empty and all-`None` inputs both return `0.0`.",
                    "A loop over many random scans asserts the upper bound never breaks.",
                ],
                optional_extension=(
                    "Return `(distance, reason)` so telemetry can record *why* the robot "
                    "stopped, then log the reason distribution."
                ),
            ),
            exercise(
                number=6,
                title="Reusable safety envelope across heterogeneous robots",
                difficulty="HARD",
                learning_objectives=[
                    "Design a reusable interface that works for any robot-like object",
                    "Compose small validated units into a policy",
                    "Handle heterogeneous failure modes without hiding them",
                ],
                concepts_tested=[
                    "duck typing",
                    "function composition",
                    "defensive programming",
                    "API design",
                ],
                problem_statement=(
                    "ROBO-X will command ground rovers, drones and conveyor carriers. They "
                    "share no base class, only capabilities. Write a safety envelope that "
                    "works with **any** object exposing `status()` and `read_sensor(channel)`, "
                    "and refuses to issue motion when the envelope is violated."
                ),
                requirements=[
                    "Define `evaluate_envelope(robot, min_battery_pct=20.0, min_clearance_m=1.0, max_temp_c=45.0)` returning a list of violated rule strings.",
                    "Use only duck typing — do not import or isinstance-check any robot class.",
                    "Rules are independent; collect all violations, never short-circuit.",
                    "Handle a robot whose `read_sensor` raises an exception: record `'sensor failure: distance'` as a violation instead of propagating.",
                    "Define `guard_move(robot, distance_m, ...)` that returns `(moved, violations)` and calls `robot.move()` only when there are no violations.",
                ],
                constraints=[
                    "Do not assume `robot.move` exists until you have checked with `hasattr`.",
                    "Must work with the `SimulatedRobot` from `shared` and with a hand-written mock.",
                    "Do not catch `Exception` broadly to silence errors — catch the specific error your mock raises.",
                ],
                input_description=(
                    "Any object with `status()` -> dict containing `battery_pct`, and "
                    "`read_sensor(channel)` -> float, optionally raising."
                ),
                expected_output=(
                    "`evaluate_envelope` returns `[]` when safe, otherwise one string per "
                    "violated rule."
                ),
                example_input="evaluate_envelope(SimulatedRobot(battery_wh=10.0))",
                example_output="['battery 20.8% below 20.0%', 'clearance 2.59 m below 1.00 m' and nothing else]",
                edge_cases=[
                    "A robot with no `move` attribute must produce a violation, not `AttributeError`.",
                    "A sensor raising must become a recorded violation and must stop motion.",
                    "A healthy robot must produce an empty list.",
                    "Missing `battery_pct` in `status()` must be recorded, not crash.",
                ],
                hints=[
                    "Collect rules as small functions returning `str | None`, then filter.",
                    "`hasattr(robot, 'move')` is the capability check; do not import the class.",
                    "Call `robot.move()` inside the `if not violations` branch only.",
                ],
                success_criteria=[
                    "Works unchanged against `SimulatedRobot` and a locally defined mock with a different shape.",
                    "A failing sensor prevents motion and is recorded as a violation.",
                    "A robot lacking `move` produces a violation instead of raising.",
                    "At least six assertions covering every rule and every failure mode.",
                ],
                optional_extension=(
                    "Return a `SafetyReport` dataclass carrying `violations`, `allowed`, "
                    "and `evaluated_at_tick`, and add a `strict` flag that raises instead "
                    "of returning."
                ),
            ),
            exercise(
                number=7,
                title="Energy-aware mission planner with backtracking",
                difficulty="HARD",
                learning_objectives=[
                    "Design an algorithm rather than a script",
                    "Reason about termination and worst-case behaviour",
                    "Prove correctness properties with assertions",
                ],
                concepts_tested=[
                    "algorithm design",
                    "loop invariants",
                    "termination reasoning",
                    "greedy vs backtracking",
                ],
                problem_statement=(
                    "A mission is a sequence of waypoints. Each leg costs energy "
                    "proportional to its distance. Plan the longest prefix of the mission "
                    "the robot can complete, given its remaining charge and a mandatory "
                    "return to the dock."
                ),
                requirements=[
                    "Define `plan_mission(legs, battery_wh, reserve_wh=5.0, wh_per_m=0.8)` where `legs` is a list of `(name, distance_m)` tuples.",
                    "Return the list of waypoint names reachable, the leg count, and the energy left on return.",
                    "Stop planning at the first leg that cannot be completed — do not skip it.",
                    "Always reserve `reserve_wh` for the return trip; if `battery_wh <= reserve_wh`, return an empty plan.",
                    "Guarantee via assertion that the returned energy is never negative.",
                ],
                constraints=[
                    "Handle an empty `legs` list.",
                    "Reject legs with negative distance by raising `ValueError`.",
                    "Do not use floating-point accumulation beyond the necessary arithmetic; round consistently.",
                ],
                input_description=(
                    "`legs`: ordered `(name, distance_m)` tuples. `battery_wh`: remaining "
                    "charge. `reserve_wh`: energy that must remain for docking."
                ),
                expected_output="`(reached_names, legs_completed, energy_left_wh)`.",
                example_input="plan_mission([('aisle-1', 3.0), ('aisle-2', 4.0), ('dock-run', 20.0)], battery_wh=20.0)",
                example_output="(['aisle-1', 'aisle-2'], 2, 3.8)",
                edge_cases=[
                    "Empty `legs` -> `([], 0, battery_wh)`.",
                    "`battery_wh <= reserve_wh` -> empty plan even if legs exist.",
                    "A leg that exactly consumes the remaining usable energy must be included.",
                    "Negative distance in any leg -> `ValueError`.",
                ],
                hints=[
                    "Compute `usable = battery_wh - reserve_wh` once, before the loop.",
                    "Track a running `spent` total and compare `spent + leg_cost <= usable`.",
                    "Write the loop invariant as a comment: *after each iteration, `spent` is the cost of exactly the legs already accepted*.",
                ],
                success_criteria=[
                    "The example returns exactly the three expected values.",
                    "All five edge cases behave as specified.",
                    "A property test over 500 randomised missions asserts energy is never negative and the returned prefix is maximal.",
                    "The loop invariant is documented in a comment.",
                ],
                optional_extension=(
                    "Support an optional detour flag per leg (a 1.4x cost multiplier) and "
                    "prove the planner still terminates and remains maximal."
                ),
            ),
            exercise(
                number=8,
                title="Deterministic telemetry pipeline with fault injection",
                difficulty="HARD",
                learning_objectives=[
                    "Build a multi-stage pipeline with an explicit contract per stage",
                    "Handle partial failure without corrupting output",
                    "Make results reproducible across runs",
                ],
                concepts_tested=[
                    "pipeline design",
                    "exception handling (introductory)",
                    "determinism",
                    "data validation",
                ],
                problem_statement=(
                    "Telemetry arrives as raw tuples, some fields missing and some reads "
                    "failed. Build a three-stage pipeline — parse, validate, summarise — "
                    "that produces a report even when individual records are corrupt, and "
                    "produces the *same* report on every run."
                ),
                requirements=[
                    "Define `parse_record(raw)` returning a dict with keys `robot_id`, `timestamp`, `battery_pct`, `temp_c`, or `None` when the record is unparseable.",
                    "Define `validate_record(record)` returning a list of problems; a record with any problem is quarantined, not dropped silently.",
                    "Define `summarise(records, problems)` returning a dict with `count`, `mean_battery`, `max_temp`, `quarantined`.",
                    "Corrupt records must appear in the quarantine count *and* in the problem list.",
                    "Re-running the pipeline on the same input must produce byte-identical output.",
                ],
                constraints=[
                    "Do not print inside the pipeline functions.",
                    "Do not use randomness or wall-clock time anywhere.",
                    "Missing fields must be treated as problems, not as zero.",
                ],
                input_description=(
                    "`raw` records are tuples `(robot_id, timestamp, battery_pct, temp_c)` "
                    "where any element may be `None`, the wrong type, or out of range."
                ),
                expected_output="A report dict with the four specified keys.",
                example_input=(
                    "records = [('rx-01', 101, 88.0, 31.2), ('rx-02', 102, None, 30.0), "
                    "('bad', 'x', 50, 20)]"
                ),
                example_output="{'count': 1, 'mean_battery': 88.0, 'max_temp': 31.2, 'quarantined': 2}",
                edge_cases=[
                    "All records corrupt -> `count == 0`, `mean_battery is None`, `quarantined` equals the input length.",
                    "Empty input -> the same as all-corrupt, without raising.",
                    "`battery_pct` of `150.0` is out of range (0, 100] and must be quarantined.",
                    "A `robot_id` of `0` is valid; only empty strings are invalid.",
                ],
                hints=[
                    "Stage 1 catches malformed structure; stage 2 catches semantic problems.",
                    "Use `float(x)` inside a `try` and convert the failure into a problem string.",
                    "Determinism comes free if you never iterate a `set` when building the report.",
                ],
                success_criteria=[
                    "The example returns exactly the shown report.",
                    "All five edge cases behave as specified.",
                    "Running the pipeline twice on the same input produces equal reports, asserted in a test.",
                    "No function prints; problems are returned as data.",
                ],
                optional_extension=(
                    "Add a fourth stage that writes the report to a JSON string using "
                    "`json.dumps(..., sort_keys=True)` to prove the byte-identical claim."
                ),
            ),
            exercise(
                number=9,
                title="Operator-facing pre-flight report with exit semantics",
                difficulty="HARD",
                learning_objectives=[
                    "Design a multi-rule checker with a clear pass/fail contract",
                    "Separate collection from presentation",
                    "Make behaviour testable without side effects",
                ],
                concepts_tested=[
                    "separation of concerns",
                    "aggregate reporting",
                    "testing seams",
                    "operator ergonomics",
                ],
                problem_statement=(
                    "Commissioning engineers need one screen that answers 'can this robot "
                    "start?' and, if not, exactly what is wrong. Build the checker and the "
                    "renderer separately, so the checker can be tested without parsing "
                    "strings."
                ),
                requirements=[
                    "Define `run_checks(robot, thresholds)` returning a list of `(check_name, passed, measured, limit)` tuples; at least six checks.",
                    "Thresholds are a dict so a different robot class can pass different limits; every threshold key must be honoured.",
                    "Define `render_report(results)` returning a formatted multi-line string with a header line and one line per check.",
                    "Define `can_start(results)` returning `True` only when every check passed.",
                    "The renderer must be pure: calling it twice with the same results returns equal strings.",
                ],
                constraints=[
                    "`run_checks` must not print or format strings.",
                    "A missing threshold key must raise `KeyError` naming the key — silently using a default would hide a configuration bug.",
                    "Include a check that the robot has a `move` capability.",
                ],
                input_description=(
                    "A robot object plus a thresholds dict with keys `min_battery_pct`, "
                    "`min_clearance_m`, `max_temp_c`, `max_speed_mps`, `min_voltage_v`."
                ),
                expected_output=(
                    "A report string beginning `ROBO-X PRE-FLIGHT` ending in `RESULT: PASS` or `RESULT: FAIL`."
                ),
                example_input="render_report(run_checks(robot, thresholds))",
                example_output="ROBO-X PRE-FLIGHT (5 checks)\n[PASS] battery      100.0%   >= 20.0%\n...\nRESULT: PASS",
                edge_cases=[
                    "A failing sensor must fail its check, not abort the whole report.",
                    "A robot missing `move` must produce a failed check line.",
                    "Zero checks is impossible — assert at least six.",
                    "A missing threshold key raises `KeyError`.",
                ],
                hints=[
                    "Build `results` with a list comprehension over `(name, lambda)` pairs.",
                    "Use `>=`/`<=` for limits so the printed comparison matches the logic exactly.",
                    "Test `render_report` with hand-built tuples — no robot needed.",
                ],
                success_criteria=[
                    "At least six checks run even when the robot is unhealthy.",
                    "`render_report` is pure and deterministic, asserted twice.",
                    "A missing threshold key raises `KeyError` naming it.",
                    "The report's final line always states PASS or FAIL correctly.",
                ],
                optional_extension=(
                    "Add a `verbose` flag that appends a remediation hint per failure, "
                    "and assert every failure line has a hint."
                ),
            ),
            exercise(
                number=10,
                title="Reusable numeric guard library with property checks",
                difficulty="HARD",
                learning_objectives=[
                    "Design a small, general library rather than a one-off script",
                    "Reason about the contract of each guard",
                    "Use property-style assertions over many inputs",
                ],
                concepts_tested=[
                    "library design",
                    "invariants",
                    "property-based reasoning",
                    "API consistency",
                ],
                problem_statement=(
                    "Every ROBO-X subsystem needs the same numeric guards: clamp, "
                    "require-in-range, and safe-divide. Design them as a small, consistent "
                    "API and demonstrate the invariants hold across randomised inputs."
                ),
                requirements=[
                    "Define `clamp(value, low, high)`; raise `ValueError` if `low > high`; return `value` when already inside the range.",
                    "Define `require_in_range(value, low, high, name)`; raise `ValueError` naming `name` when outside.",
                    "Define `safe_divide(numerator, denominator, default=0.0)`; return `default` when the denominator is `0.0`.",
                    "Every function must handle `int` and `float` inputs and return the same type family as its input.",
                    "Write a property test using a seeded `random.Random` over 1000 cases asserting `low <= clamp(v, low, high) <= high`.",
                ],
                constraints=[
                    "No library may silently swap its arguments to fix a reversed range — raise instead.",
                    "`safe_divide` must not raise `ZeroDivisionError`.",
                    "Guard names must appear in error messages so logs are diagnosable.",
                ],
                input_description="Numeric values and bounds as described per function.",
                expected_output="Clamped values, validated values, or quotients as specified.",
                example_input="safe_divide(10.0, 0.0, default=float('inf'))",
                example_output="inf",
                edge_cases=[
                    "`clamp(5, 10, 0)` -> raises `ValueError` about the reversed range, not a silent swap.",
                    "`clamp` with `low == high` returns that single value for every input.",
                    "`safe_divide(0.0, 0.0)` returns `default`, not `nan`.",
                    "Negative zero denominators behave like zero.",
                ],
                hints=[
                    "Write the reversed-range check before the comparison.",
                    "Use `random.Random(20260101)` so the property test is reproducible.",
                    "`default=float('inf')` is a legitimate choice for safe division in control code.",
                ],
                success_criteria=[
                    "All functions satisfy the documented contract.",
                    "The 1000-case property test passes and is seeded for reproducibility.",
                    "Every error message names the offending parameter.",
                    "`safe_divide` never raises `ZeroDivisionError`.",
                ],
                optional_extension=(
                    "Add `clamp_all(values, low, high)` returning a new list, and prove "
                    "the input list is unmutated."
                ),
            ),
        ],
        solutions=[
            solution(
                number=1,
                code='''
DRIVETRAIN_EFFICIENCY = 0.72


def endurance_hours(
    battery_wh: float,
    mass_kg: float,
    draw_w: float,
    efficiency: float = DRIVETRAIN_EFFICIENCY,
) -> float:
    """Return estimated driving hours for a robot.

    Args:
        battery_wh: Battery capacity in watt-hours.
        mass_kg: Robot mass in kilograms. Validated but not used in the formula;
            it is retained so the signature stays stable when a payload term is
            added later.
        draw_w: Average electrical draw while driving, in watts.
        efficiency: Drivetrain efficiency as a fraction in (0, 1].

    Returns:
        Estimated hours of continuous driving.

    Raises:
        ValueError: If a magnitude argument is not positive, or if `efficiency`
            lies outside (0, 1].
    """
    if battery_wh <= 0:
        raise ValueError(f"battery_wh must be positive, got {battery_wh}")
    if mass_kg <= 0:
        raise ValueError(f"mass_kg must be positive, got {mass_kg}")
    if draw_w <= 0:
        raise ValueError(f"draw_w must be positive, got {draw_w}")
    if not 0.0 < efficiency <= 1.0:
        raise ValueError(f"efficiency must be in (0, 1], got {efficiency}")

    return (battery_wh * efficiency) / draw_w
''',
                explanation=(
                    "Validation comes first and is *per-argument*, so the error message names "
                    "the exact parameter that is wrong. A single combined `if` would be "
                    "shorter but would produce a message like `'battery, draw and mass must "
                    "all be positive'`, which an operator cannot act on.\n\n"
                    "The efficiency bound is written `not 0.0 < efficiency <= 1.0`, which is "
                    "the exclusive lower bound and inclusive upper bound in one expression. "
                    "Chained comparisons are a Python feature worth internalising.\n\n"
                    "`mass_kg` is validated but unused. That is a deliberate API decision, "
                    "not an oversight: the argument documents the robot being described and "
                    "gives future model terms a stable home. The docstring says so, because "
                    "an undocumented unused parameter is indistinguishable from a bug."
                ),
                complexity=(
                    "O(1) time, O(1) space. Four comparisons and one division, regardless of input."
                ),
                edge_cases=(
                    "`battery_wh=0` raises rather than returning `0.0`. A zero-endurance "
                    "estimate is a *claim* that the robot cannot work at all; that is a "
                    "different statement from 'not enough data', and conflating them in "
                    "mission planning is how a robot gets dispatched with a flat pack.\n\n"
                    "`efficiency=1.0` is valid (a perfect drivetrain). `efficiency=0.0` "
                    "raises.\n\n"
                    "Floating point: `(48.0 * 0.72) / 15.0` is `2.3039999999999996`, not "
                    "`2.304`. Compare with `math.isclose`, or round at the presentation "
                    "boundary — never round inside the calculation."
                ),
                alternative_approaches=(
                    "A dataclass `EnergyModel(battery_wh, mass_kg, draw_w, efficiency)` with "
                    "a method is the right shape once several models share the same maths "
                    "(the simulator uses a per-second term too). At this stage a function "
                    "with four parameters is simpler and equally correct.\n\n"
                    "You could also return `None` instead of raising. Rejected: callers "
                    "would have to remember to check, and a missed check produces a wrong "
                    "number silently."
                ),
                testing='''
import math

from shared import SimulatedRobot  # noqa: F401  (import proves the shared package loads)

assert math.isclose(endurance_hours(48.0, 12.5, 15.0), 2.304, rel_tol=1e-9)
assert math.isclose(endurance_hours(48.0, 12.5, 15.0, efficiency=1.0), 3.2)

# Every validation case raises, with a message naming the parameter.
cases = [
    ((0.0, 12.5, 15.0), "battery_wh"),
    ((48.0, 0.0, 15.0), "mass_kg"),
    ((48.0, 12.5, 0.0), "draw_w"),
    ((48.0, 12.5, 15.0, 0.0), "efficiency"),
    ((48.0, 12.5, 15.0, 1.5), "efficiency"),
]
for args, expected_name in cases:
    try:
        endurance_hours(*args)
    except ValueError as exc:
        assert expected_name in str(exc), f"{expected_name!r} missing from {exc!r}"
    else:
        raise AssertionError(f"expected ValueError for {args}")

print("Exercise 1: all solution tests passed")
''',
            ),
            solution(
                number=2,
                code='''
def same_object(a, b) -> bool:
    """Return True only when `a` and `b` are literally the same object."""
    return a is b


def equal_contents(a, b) -> bool:
    """Return True when `a == b`, i.e. they hold the same value."""
    return a == b


def mutation_effect(first, second) -> str:
    """Return 'shared' if mutating a copy of `first` would change `second`.

    Both arguments are copied before any mutation, so the caller's data is
    untouched.
    """
    if not isinstance(first, list):
        # Immutable values (int, float, str, tuple) cannot be mutated at all.
        return "independent"

    probe = list(first)          # shallow copy: the caller's list is safe
    probe.append("__mutation_probe__")

    if "__mutation_probe__" in probe:
        # An alias shares the underlying object, so the probe also appears in it.
        if isinstance(second, list) and "__mutation_probe__" in second:
            return "shared"
    return "independent"
''',
                explanation=(
                    "`same_object` is `a is b` and `equal_contents` is `a == b`. That is the "
                    "whole distinction; the functions exist so the *intent* is named at the "
                    "call site, which is what makes the difference reviewable.\n\n"
                    "`mutation_effect` copies `first` with `list(first)` before appending, so "
                    "no caller data is modified. The probe string is deliberately unlikely "
                    "to occur naturally, so `'shared' in second` cannot false-positive.\n\n"
                    "The implementation is intentionally simple rather than clever. A "
                    "general solution would compare `id()` before and after, but that leaks "
                    "identity into the return value and adds nothing at this level."
                ),
                complexity="O(1) time and space: one copy of `first`, one membership test.",
                edge_cases=(
                    "Small-integer caching means `x = 1000; y = 1000` may or may not be "
                    "identical across interpreters. A correct implementation must not assert "
                    "either way — hence the guidance to avoid asserting on integers.\n\n"
                    "Tuples and strings are immutable: `mutation_effect` returns "
                    "`'independent'` immediately without attempting a mutation.\n\n"
                    "Nested aliasing (a list inside a list) needs a deep copy; that is the "
                    "extension, not the baseline."
                ),
                alternative_approaches=(
                    "`import copy; copy.deepcopy(first)` handles nesting but costs more and "
                    "hides the intent. The probe-and-compare method makes the test visible.\n\n"
                    "A third option is to inspect `id(first) == id(second)` directly, which "
                    "answers 'are they the same object' but not 'would a mutation be visible' "
                    "— different questions, and only the second one matches the function name."
                ),
                testing='''
# Equal but not identical
a = [1, 2, 3]
b = [1, 2, 3]
assert same_object(a, b) is False
assert equal_contents(a, b) is True
assert mutation_effect(a, b) == "independent"

# Aliases share the object
c = a
assert same_object(a, c) is True
assert mutation_effect(a, c) == "shared"

# Caller data untouched by mutation_effect
before = list(a)
mutation_effect(a, b)
assert a == before, "mutation_effect must not modify its arguments"

# Immutables
assert mutation_effect(5, 5) == "independent"
assert mutation_effect((1, 2), (1, 2)) == "independent"
assert equal_contents((), ()) is True

# Empty lists are equal but not identical
assert equal_contents([], []) is True
assert same_object([], []) is False

print("Exercise 2: all solution tests passed")
''',
            ),
            solution(
                number=3,
                code='''
def clearance_action(
    readings, stop_m: float = 0.8, slow_m: float = 2.0
) -> str:
    """Return the motion command for the worst reading in `readings`.

    Any `None` (failed read) or an empty input means we cannot prove the path is
    clear, so the robot halts. Failing safe is the whole point of this policy.
    """
    if not readings:
        return "HALT"
    if any(value is None for value in readings):
        return "HALT"

    nearest = min(readings)
    if nearest < stop_m:
        return "STOP"
    if nearest < slow_m:
        return "SLOW"
    return "CRUISE"


def average_action(readings, stop_m: float = 0.8, slow_m: float = 2.0) -> str:
    """Return the motion command using the mean reading instead of the worst.

    Provided only to demonstrate why it is unsafe: a long run of far readings
    can average into CRUISE while an obstacle is centimetres away.
    """
    usable = [value for value in readings if value is not None]
    if not usable:
        return "HALT"

    mean = sum(usable) / len(usable)
    if mean < stop_m:
        return "STOP"
    if mean < slow_m:
        return "SLOW"
    return "CRUISE"
''',
                explanation=(
                    "The safety rule computes `min(readings)` — the worst case — while the "
                    "comparison rule computes the mean. That single difference is the entire "
                    "lesson.\n\n"
                    "`HALT` is checked first and unconditionally, because a failed read "
                    "(`None`) or an empty window means the safety system has *no evidence* "
                    "that the path is clear. Absent evidence is not evidence of safety.\n\n"
                    "Boundaries are strict `<` rather than `<=`: a reading of exactly 0.8 m "
                    "means the robot is 0.8 m from the obstacle, which is at the limit, not "
                    "past it. Writing the boundary rule down in the function's contract "
                    "prevents an argument later about whether 0.8 should stop."
                ),
                complexity="O(n) time per call, O(1) extra space. Both functions scan the window.",
                edge_cases=(
                    "`readings=[0.5, 3.0, 3.0, 3.0, 3.0]` is the demonstration case: the mean "
                    "is 2.5 (CRUISE) while the worst case is STOP.\n\n"
                    "`None` is treated differently by the two functions on purpose: the "
                    "safety rule halts, the comparison rule ignores it and continues. That "
                    "asymmetry is the argument for the safety rule.\n\n"
                    "The minimum scan is O(n); for a 16-channel depth camera at 30 Hz this "
                    "is irrelevant. If it ever mattered, you would keep a running minimum "
                    "instead of storing the whole window."
                ),
                alternative_approaches=(
                    "A percentile (5th percentile rather than the minimum) is a reasonable "
                    "compromise when sensor noise produces occasional wild outliers: it "
                    "survives a single bad sample without averaging away a real hazard. In "
                    "safety-critical code, though, the conservative minimum plus a "
                    "filter-plaintext-time argument is usually easier to defend.\n\n"
                    "A hysteresis band (stop below 0.8, resume above 1.2) prevents "
                    "oscillation at the threshold. That is an important refinement, and it "
                    "is the optional extension."
                ),
                testing='''
# Boundaries and empties
assert clearance_action([2.9, 2.4, 1.9, 1.1, 0.6, 0.5]) == "STOP"
assert clearance_action([]) == "HALT"
assert clearance_action([None, None]) == "HALT"
assert clearance_action([0.9, 3.0]) == "SLOW"
assert clearance_action([3.0, 3.0]) == "CRUISE"

# Boundary is exclusive below
assert clearance_action([0.8]) == "SLOW"
assert clearance_action([2.0]) == "CRUISE"

# The hazard hidden by averaging
window = [0.5, 3.0, 3.0, 3.0, 3.0]
assert clearance_action(window) == "STOP"
assert average_action(window) == "CRUISE"   # <- the unsafe conclusion
assert sum(window) / len(window) == 2.5

# The safety rule is never more permissive than the mean rule
import random
rng = random.Random(20260101)
rank = {"HALT": 0, "STOP": 1, "SLOW": 2, "CRUISE": 3}
for _ in range(500):
    window = [round(rng.uniform(0.1, 5.0), 2) for _ in range(rng.randint(1, 12))]
    assert rank[clearance_action(window)] <= rank[average_action(window)]

print("Exercise 3: all solution tests passed")
''',
            ),
            solution(
                number=4,
                code='''
REQUIRED_KEYS = ("name", "battery_wh", "max_speed_mps", "sensors")


def _is_number(value) -> bool:
    """Return True for real numbers, explicitly excluding bool."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_config(config: dict) -> list[str]:
    """Return a list of configuration errors; empty means valid.

    Errors are returned in a deterministic order so that two runs on the same
    config produce identical output (which matters when the result is logged
    or diffed in review).
    """
    errors: list[str] = []

    for key in REQUIRED_KEYS:
        if key not in config:
            errors.append(f"missing key: {key}")

    if "name" in config:
        name = config["name"]
        if not isinstance(name, str) or not name.strip():
            errors.append("name must be a non-empty string")

    if "battery_wh" in config:
        value = config["battery_wh"]
        if not _is_number(value) or not (0 < value <= 200):
            errors.append("battery_wh must be in (0, 200]")

    if "max_speed_mps" in config:
        value = config["max_speed_mps"]
        if not _is_number(value) or not (0 < value <= 3.0):
            errors.append("max_speed_mps must be in (0, 3.0]")

    if "sensors" in config:
        sensors = config["sensors"]
        if not isinstance(sensors, list) or "distance" not in sensors:
            errors.append("sensors must include distance")

    return errors
''',
                explanation=(
                    "The function iterates `REQUIRED_KEYS`, not the config's own keys. That "
                    "single decision buys deterministic ordering and means extra keys are "
                    "never validated or reported.\n\n"
                    "Each value check is guarded by `if key in config`, so a missing key "
                    "produces exactly one error (the missing-key one) rather than a cascade. "
                    "Cascading errors are a common complaint about naive validators: the "
                    "operator sees five messages for one mistake.\n\n"
                    "`_is_number` exists solely to exclude `bool`. Because `bool` subclasses "
                    "`int` in Python, `isinstance(True, int)` is `True` — so "
                    "`battery_wh=True` would otherwise pass every numeric check."
                ),
                complexity="O(k) time in the number of required keys (constant, k=4); O(1) space.",
                edge_cases=(
                    "`battery_wh=True` — rejected by `_is_number`. Without that helper this "
                    "is a genuine bug that passes review, because `True` sorts as 1.\n\n"
                    "Bounds are exclusive at 0 and inclusive at 200, matching the "
                    "specification `in (0, 200]`.\n\n"
                    "`name='   '` is rejected: a whitespace-only name is not a name. This is "
                    "the kind of rule that is cheap now and expensive after a fleet is "
                    "deployed.\n\n"
                    "The config dict is never mutated — verified in the tests by comparing "
                    "a deep copy before and after."
                ),
                alternative_approaches=(
                    "A dataclass with `__post_init__` validation (topic 6.1) would make "
                    "invalid states unrepresentable, which is strictly better. It also "
                    "requires converting the dict, which is why the dict-validating version "
                    "is taught first: config files and CLI flags arrive as dicts.\n\n"
                    "Schema libraries (`pydantic`, `jsonschema`) do this generically at "
                    "scale. Worth knowing; unnecessary for four keys."
                ),
                testing='''
from copy import deepcopy

assert validate_config({
    "name": "robo-x-01",
    "battery_wh": 48.0,
    "max_speed_mps": 1.2,
    "sensors": ["distance", "temperature"],
}) == []

errors = validate_config({
    "name": "", "battery_wh": 500, "sensors": ["temperature"],
})
assert errors == [
    "missing key: max_speed_mps",
    "name must be a non-empty string",
    "battery_wh must be in (0, 200]",
    "sensors must include distance",
], errors

# bool must not pass as a number
assert "battery_wh must be in (0, 200]" in validate_config(
    {"name": "a", "battery_wh": True, "max_speed_mps": 1.0, "sensors": ["distance"]}
)

# wrong types and whitespace-only names
assert "name must be a non-empty string" in validate_config(
    {"name": 123, "battery_wh": 10, "max_speed_mps": 1.0, "sensors": ["distance"]}
)
assert "name must be a non-empty string" in validate_config(
    {"name": "   ", "battery_wh": 10, "max_speed_mps": 1.0, "sensors": ["distance"]}
)

# extra keys are ignored
assert validate_config({
    "name": "rx", "battery_wh": 10, "max_speed_mps": 1.0,
    "sensors": ["distance"], "experimental_lidar": True,
}) == []

# boundaries: 0 and 200 out, 200 ok
base = {"name": "rx", "max_speed_mps": 1.0, "sensors": ["distance"]}
assert validate_config({**base, "battery_wh": 0})
assert not validate_config({**base, "battery_wh": 200})
assert not validate_config({**base, "battery_wh": 0.001})

# determinism and non-mutation
config = {"name": "", "battery_wh": 500, "sensors": []}
snapshot = deepcopy(config)
assert validate_config(config) == validate_config(config)
assert config == snapshot

print("Exercise 4: all solution tests passed")
''',
            ),
            solution(
                number=5,
                code='''
def safe_travel_m(readings, max_step_m: float = 0.5, margin_m: float = 1.0) -> float:
    """Return the distance this cycle may safely travel, in metres.

    The result is never negative and never exceeds `max_step_m`. An empty
    window, or one with no usable readings, yields 0.0: with no evidence that
    the path is clear, the robot does not move.
    """
    usable = [value for value in readings if value is not None]

    if not usable:
        return 0.0

    nearest = min(usable)
    step = min(max_step_m, nearest - margin_m)

    if step < 0.0:            # obstacle closer than the safety margin
        step = 0.0
    return step
''',
                explanation=(
                    "Three decisions, in order: filter unusable readings, compute the capped "
                    "step, then clamp the negative case.\n\n"
                    "`min(max_step_m, nearest - margin_m)` expresses the policy directly — "
                    "travel at most one cycle's worth, and never closer than the margin. "
                    "Because `margin_m` defaults to 1.0 m and obstacles are reported as "
                    "distance-to-surface, `nearest - margin_m` is the gap to keep.\n\n"
                    "The explicit `if step < 0.0` is kept even though `max(0.0, step)` would "
                    "do, because the specification asks for the conditional to be visible. "
                    "In review, seeing the clamp written out is clearer than inferring it."
                ),
                complexity="O(n) time in the number of readings; O(n) space for the filtered list.",
                edge_cases=(
                    "Obstacle at 0.9 m with a 1.0 m margin gives `nearest - margin_m == -0.1`, "
                    "clamped to `0.0`.\n\n"
                    "A distant obstacle gives `nearest - margin_m > max_step_m`, so `min()` "
                    "selects `max_step_m` exactly — the robot never exceeds its cycle budget.\n\n"
                    "All-`None` and empty windows return `0.0` without touching `min()`, which "
                    "would otherwise raise on an empty sequence."
                ),
                alternative_approaches=(
                    "For a rolling sensor stream, keeping a running minimum over the last N "
                    "frames is O(1) amortised per frame instead of O(N). At 30 Hz with N=16 "
                    "the difference is irrelevant, which is exactly why the simple version is "
                    "correct here.\n\n"
                    "Using a percentile instead of the minimum trades a little safety for "
                    "immunity to single-frame sensor outliers. A production system usually "
                    "runs both: a minimum for the hard stop, a percentile for the cruise "
                    "decision."
                ),
                testing='''
import random

assert safe_travel_m([4.2, 3.8, 3.1, None, 2.9], max_step_m=0.5, margin_m=1.0) == 0.5
assert safe_travel_m([]) == 0.0
assert safe_travel_m([None, None]) == 0.0
assert safe_travel_m([0.9, 5.0]) == 0.0          # closer than the margin
assert safe_travel_m([1.9, 5.0]) == 0.5          # 0.9 usable, capped at 0.5
assert safe_travel_m([0.2]) == 0.0

# The input list is untouched
original = [4.2, 3.8, None, 2.9]
snapshot = list(original)
safe_travel_m(original)
assert original == snapshot

# Property: never exceeds the cycle budget, never negative
rng = random.Random(20260101)
for _ in range(500):
    window = [round(rng.uniform(0.05, 6.0), 2) for _ in range(rng.randint(0, 10))]
    window += [None] * rng.randint(0, 2)
    cap = round(rng.uniform(0.1, 1.0), 2)
    result = safe_travel_m(window, max_step_m=cap, margin_m=1.0)
    assert 0.0 <= result <= cap, (window, cap, result)

print("Exercise 5: all solution tests passed")
''',
            ),
            solution(
                number=6,
                code='''
from shared import SensorError


def _rule_battery(robot, thresholds) -> str | None:
    """Return a violation string when battery is too low, else None."""
    status = robot.status()
    if not isinstance(status, dict) or "battery_pct" not in status:
        return "status() missing battery_pct"
    if status["battery_pct"] < thresholds["min_battery_pct"]:
        return (
            f"battery {status['battery_pct']:.1f}% below "
            f"{thresholds['min_battery_pct']:.1f}%"
        )
    return None


def _rule_clearance(robot, thresholds) -> str | None:
    """Return a violation string when an obstacle is too close."""
    try:
        clearance = robot.read_sensor("distance")
    except SensorError as exc:
        return f"sensor failure: distance ({exc})"
    if clearance < thresholds["min_clearance_m"]:
        return (
            f"clearance {clearance:.2f} m below {thresholds['min_clearance_m']:.2f} m"
        )
    return None


def _rule_temperature(robot, thresholds) -> str | None:
    """Return a violation string when the controller is too hot."""
    try:
        temp = robot.read_sensor("temperature")
    except SensorError as exc:
        return f"sensor failure: temperature ({exc})"
    if temp > thresholds["max_temp_c"]:
        return f"temperature {temp:.1f} C above {thresholds['max_temp_c']:.1f} C"
    return None


def _rule_driveable(robot, thresholds) -> str | None:
    """Return a violation string when the robot cannot be commanded."""
    if not hasattr(robot, "move"):
        return "robot has no move() capability"
    return None


def evaluate_envelope(
    robot,
    min_battery_pct: float = 20.0,
    min_clearance_m: float = 1.0,
    max_temp_c: float = 45.0,
) -> list[str]:
    """Return every safety-envelope violation for `robot` (empty means safe).

    Uses duck typing only: anything exposing `status()` and `read_sensor()`
    works, including test doubles with a completely different shape.
    """
    thresholds = {
        "min_battery_pct": min_battery_pct,
        "min_clearance_m": min_clearance_m,
        "max_temp_c": max_temp_c,
    }

    rules = (_rule_battery, _rule_clearance, _rule_temperature, _rule_driveable)

    violations: list[str] = []
    for rule in rules:
        violation = rule(robot, thresholds)
        if violation is not None:
            violations.append(violation)
    return violations


def guard_move(robot, distance_m: float, **limits) -> tuple[bool, list[str]]:
    """Move only if the envelope is satisfied.

    Returns `(moved, violations)`. On violation the robot is never commanded,
    which is the behaviour the safety requirement demands.
    """
    violations = evaluate_envelope(robot, **limits)
    if violations:
        return False, violations
    robot.move(distance_m)
    return True, []
''',
                explanation=(
                    "Each rule is a small function returning `str | None`. That shape is what "
                    "makes the envelope extensible: adding a rule means writing one function "
                    "and adding it to the `rules` tuple — no change to the control flow.\n\n"
                    "The loop never short-circuits. An operator commissioning a robot wants "
                    "all four problems, not the first one.\n\n"
                    "Sensor failures are converted into violations rather than propagated. "
                    "The distinction is important: an *unknown* clearance is a reason to "
                    "refuse motion, exactly like a known-too-small clearance.\n\n"
                    "Duck typing is enforced by *absence* — no import of any robot class and "
                    "no `isinstance` check. The only structural assumptions are the capability "
                    "checks the rules themselves make."
                ),
                complexity=(
                    "O(1) time — a fixed number of rules, each O(1). O(1) space apart from the "
                    "violation strings. This matters: the envelope runs on every control cycle."
                ),
                edge_cases=(
                    "A robot lacking `move` yields `'robot has no move() capability'` and "
                    "`guard_move` returns `(False, [...])` without raising.\n\n"
                    "`status()` missing `battery_pct` yields a specific violation instead of "
                    "a `KeyError`.\n\n"
                    "Catching `SensorError` specifically (not `Exception`) means a genuine "
                    "programming error inside a rule still propagates and is debugged, rather "
                    "than being silently reclassified as a sensor fault. This is the "
                    "difference the course spec means by 'do not hide errors'.\n\n"
                    "A mock that raises a different exception type will propagate — by design. "
                    "Broaden the `except` clause only when you know the concrete failure mode."
                ),
                alternative_approaches=(
                    "An `abc.ABC` base class with abstract `move`/`read_sensor` would give "
                    "compile-time structure and better error messages, at the cost of "
                    "requiring every implementation — including third-party ones — to "
                    "inherit. Duck typing is the better trade when you integrate hardware you "
                    "do not control.\n\n"
                    "`typing.Protocol` gives the structural guarantee without inheritance and "
                    "without runtime cost; it is introduced properly in topic 9.1 and is the "
                    "recommended production answer."
                ),
                testing='''
from shared import SensorError, SimulatedRobot


class MockRover:
    """A test double with a deliberately different shape."""

    def __init__(self, battery_pct, clearance_m, temp_c):
        self._battery_pct = battery_pct
        self._clearance_m = clearance_m
        self._temp_c = temp_c
        self.moved_m = 0.0

    def status(self):
        return {"battery_pct": self._battery_pct}

    def read_sensor(self, channel):
        if channel == "distance":
            return self._clearance_m
        if channel == "temperature":
            return self._temp_c
        raise SensorError(f"no channel {channel}")

    def move(self, distance_m):
        self.moved_m += distance_m
        return 0.8 * distance_m


class NoMoveThing:
    def status(self):
        return {"battery_pct": 90.0}

    def read_sensor(self, channel):
        return 5.0


class BrokenStatus:
    def status(self):
        return {"voltage_v": 12.0}

    def read_sensor(self, channel):
        return 5.0

    def move(self, distance_m):
        return 0.0


# healthy: real simulator and an unrelated class shape
robot = SimulatedRobot(name="robo-x-01", battery_wh=200.0)
assert evaluate_envelope(robot) == []
assert guard_move(robot, 1.0) == (True, [])

mock = MockRover(90.0, 5.0, 20.0)
assert evaluate_envelope(mock) == []
assert guard_move(mock, 2.0) == (True, [])
assert mock.moved_m == 2.0

# multiple independent violations are all reported
weak = SimulatedRobot(name="weak", battery_wh=4.0)
violations = evaluate_envelope(weak, min_battery_pct=50.0)
assert any(v.startswith("battery") for v in violations)
assert len(violations) >= 1

# a failing sensor blocks motion and is recorded
flaky = SimulatedRobot(name="flaky", battery_wh=200.0)
flaky.inject_sensor_fault(1)
moved, violations = guard_move(flaky, 1.0)
assert moved is False
assert any(v.startswith("sensor failure") for v in violations)
assert flaky.status()["travelled_m"] == 0.0, "robot must not move when unsafe"

# no move capability
violations = evaluate_envelope(NoMoveThing())
assert violations == ["robot has no move() capability"]
assert guard_move(NoMoveThing(), 1.0)[0] is False

# unusable status
assert evaluate_envelope(BrokenStatus()) == ["status() missing battery_pct"]

print("Exercise 6: all solution tests passed")
''',
            ),
            solution(
                number=7,
                code='''
def plan_mission(legs, battery_wh: float, reserve_wh: float = 5.0,
                 wh_per_m: float = 0.8):
    """Plan the longest reachable prefix of a mission.

    Args:
        legs: ordered ``(name, distance_m)`` tuples.
        battery_wh: remaining charge in watt-hours.
        reserve_wh: energy that must remain in hand for the return to dock.
        wh_per_m: energy cost per metre of travel.

    Returns:
        ``(reached_names, legs_completed, energy_left_wh)``.

    Raises:
        ValueError: if a leg distance is negative, or ``reserve_wh`` is negative.
    """
    if reserve_wh < 0:
        raise ValueError(f"reserve_wh must be non-negative, got {reserve_wh}")

    for name, distance_m in legs:
        if distance_m < 0:
            raise ValueError(f"leg {name!r} has negative distance {distance_m}")

    usable = battery_wh - reserve_wh
    if usable <= 0:
        return ([], 0, round(battery_wh, 4))

    spent = 0.0
    reached: list[str] = []

    # Invariant: `spent` is exactly the energy cost of the legs already accepted,
    # and every leg in `reached` is affordable within `usable`.
    for name, distance_m in legs:
        cost = distance_m * wh_per_m
        if spent + cost > usable:
            break                       # first unaffordable leg ends the plan
        spent += cost
        reached.append(name)

    energy_left = battery_wh - spent
    assert energy_left >= 0.0, "planned energy must never exceed available charge"
    return (reached, len(reached), round(energy_left, 4))
''',
                explanation=(
                    "This is a greedy prefix algorithm, and the specification *is* the "
                    "algorithm: take legs in order, stop at the first one that does not fit. "
                    "There is no search because no reordering is permitted.\n\n"
                    "`usable = battery_wh - reserve_wh` is computed once, before the loop. "
                    "Folding the reserve into the budget is what makes the reserve unbypassable "
                    "— every subsequent comparison automatically respects it.\n\n"
                    "The `break` (rather than `continue`) enforces 'do not skip'. Skipping "
                    "would produce a plan that teleports past an obstacle the robot cannot "
                    "physically cross.\n\n"
                    "The assertion is not decoration: it encodes the safety property that the "
                    "planner must never schedule more energy than the robot holds."
                ),
                complexity="O(n) time, O(k) space for the returned names (k <= n).",
                edge_cases=(
                    "A leg costing exactly the remaining usable energy is **included** "
                    "(`spent + cost > usable` is False when they are equal). This is the "
                    "correct inclusive boundary for a planner: the robot arrives with "
                    "exactly its reserve.\n\n"
                    "`battery_wh <= reserve_wh` short-circuits to an empty plan, and the "
                    "returned energy is the untouched battery, not zero.\n\n"
                    "Rounding: `energy_left` is rounded once at the boundary with "
                    "`round(..., 4)`. Rounding inside the loop would accumulate error and "
                    "could flip a boundary comparison."
                ),
                alternative_approaches=(
                    "A binary search over the prefix length would also be correct but is "
                    "pointless here: prefix costs are monotone increasing, so a single "
                    "forward scan is already optimal. Worth recognising — reach for binary "
                    "search only when the structure justifies it.\n\n"
                    "A real planner adds detours (topology-aware routing), payload-dependent "
                    "costs and multi-robot contention. The greedy prefix remains the "
                    "innermost, always-correct layer."
                ),
                testing='''
import random

# Documented example
assert plan_mission(
    [("aisle-1", 3.0), ("aisle-2", 4.0), ("dock-run", 20.0)], battery_wh=20.0
) == (["aisle-1", "aisle-2"], 2, 3.8)

# Empty mission
assert plan_mission([], battery_wh=20.0) == ([], 0, 20.0)

# Not enough above the reserve
assert plan_mission([("a", 1.0)], battery_wh=5.0, reserve_wh=5.0) == ([], 0, 5.0)

# Exact-boundary leg is included
assert plan_mission([("a", 5.0)], battery_wh=9.0, reserve_wh=5.0, wh_per_m=0.8) == (
    ["a"], 1, 4.0,
)

# Negative distance raises
try:
    plan_mission([("backwards", -1.0)], battery_wh=20.0)
except ValueError as exc:
    assert "backwards" in str(exc)
else:
    raise AssertionError("expected ValueError for a negative leg")

# Property: never negative, never skips a leg, always maximal
rng = random.Random(20260101)
for _ in range(500):
    legs = [(f"w{i}", round(rng.uniform(0.1, 12.0), 2)) for i in range(rng.randint(0, 8))]
    battery = round(rng.uniform(0.0, 40.0), 2)
    reserve = round(rng.uniform(0.0, 6.0), 2)
    per_m = round(rng.uniform(0.2, 2.0), 2)

    reached, count, left = plan_mission(legs, battery, reserve, per_m)

    assert left >= 0.0, (legs, battery, reserve, per_m, left)
    assert count == len(reached) <= len(legs)

    # maximality: the next leg must be unaffordable
    if count < len(legs):
        next_cost = legs[count][1] * per_m
        assert battery - reserve - next_cost < sum(d * per_m for _, d in legs[:count])
    # prefix property: reached is exactly the first `count` legs
    assert [name for name, _ in legs[:count]] == reached

print("Exercise 7: all solution tests passed")
''',
            ),
            solution(
                number=8,
                code='''
def parse_record(raw) -> dict | None:
    """Parse one raw telemetry tuple into a dict, or return None if malformed.

    Returns None for structural problems (wrong shape, unconvertible fields)
    rather than raising: a corrupt record is an expected condition in the field,
    not an exceptional one.
    """
    if not isinstance(raw, (tuple, list)) or len(raw) != 4:
        return None

    robot_id, timestamp, battery_pct, temp_c = raw

    if not isinstance(robot_id, str) or not robot_id.strip():
        return None
    if not isinstance(timestamp, int) or isinstance(timestamp, bool) or timestamp < 0:
        return None

    try:
        battery_pct = float(battery_pct)
        temp_c = float(temp_c)
    except (TypeError, ValueError):
        return None

    return {
        "robot_id": robot_id,
        "timestamp": timestamp,
        "battery_pct": battery_pct,
        "temp_c": temp_c,
    }


def validate_record(record: dict | None) -> list[str]:
    """Return the list of semantic problems with `record` (empty means valid)."""
    if record is None:
        return ["unparseable record"]

    problems: list[str] = []
    if not 0.0 <= record["battery_pct"] <= 100.0:
        problems.append(f"battery_pct {record['battery_pct']} outside [0, 100]")
    if not -40.0 <= record["temp_c"] <= 125.0:
        problems.append(f"temp_c {record['temp_c']} outside [-40, 125]")
    return problems


def summarise(records, problems: list[str]) -> dict:
    """Aggregate validated records into a report.

    Corrupt records appear both in the quarantine count and in `problems`.
    """
    valid = [r for r in records if r is not None and not validate_record(r)]

    if not valid:
        return {"count": 0, "mean_battery": None, "max_temp": None,
                "quarantined": len(problems)}

    return {
        "count": len(valid),
        "mean_battery": round(sum(r["battery_pct"] for r in valid) / len(valid), 4),
        "max_temp": round(max(r["temp_c"] for r in valid), 4),
        "quarantined": len(problems),
    }
''',
                explanation=(
                    "The pipeline separates *structural* failure (stage 1: is this even a "
                    "record?) from *semantic* failure (stage 2: is it a plausible record?). "
                    "Both quarantine; keeping them apart means the problem list can say "
                    "'unparseable' versus 'battery 150 outside [0, 100]', which is the "
                    "difference between a data-pipeline bug and a failing sensor.\n\n"
                    "Missing fields become **problems**, never zeros. Substituting 0.0 for a "
                    "missing battery reading would drag the mean down and look like a fleet "
                    "issue — a genuinely dangerous class of silent corruption.\n\n"
                    "`parse_record` returns `None` instead of raising because malformed input "
                    "is expected in this domain. Raising would force a try/except at every "
                    "call site for a condition that is normal.\n\n"
                    "Determinism comes from never iterating a `set` when building output, "
                    "and from using no clock or randomness."
                ),
                complexity="O(n) time across three stages; O(k) space for valid records and problems.",
                edge_cases=(
                    "All records corrupt yields `count == 0` and `None` for both aggregates — "
                    "never `ZeroDivisionError` from `max()`/`sum()` on an empty sequence, "
                    "which is why the `if not valid` branch exists.\n\n"
                    "`battery_pct = 150.0` parses fine (it is a float) then fails validation, "
                    "so it is quarantined as an out-of-range value, not as unparseable.\n\n"
                    "`robot_id = '0'` is valid; only empty or whitespace-only strings fail.\n\n"
                    "`validate_record` is called twice per record (once in `summarise`'s "
                    "comprehension, once if a caller inspects it). At telemetry volumes that "
                    "is wasteful — the extension shows the fix."
                ),
                alternative_approaches=(
                    "A dataclass with `__post_init__` validation (topic 6.1) makes invalid "
                    "records unrepresentable, but requires the parse step to construct them, "
                    "which partially defeats the point of tolerant parsing.\n\n"
                    "Using `collections.namedtuple` or a `TypedDict` (topics 3.2 and 9.1) "
                    "gives the same record shape with less ceremony than a full class.\n\n"
                    "For very large streams, `itertools.islice` + a bounded deque keeps "
                    "memory flat; the three-stage structure is unchanged."
                ),
                testing='''
raw_records = [
    ("rx-01", 101, 88.0, 31.2),
    ("rx-02", 102, None, 30.0),
    ("bad", "x", 50, 20),
]
parsed = [parse_record(raw) for raw in raw_records]
problems = [p for rec in parsed for p in validate_record(rec)]

assert parsed[0] == {"robot_id": "rx-01", "timestamp": 101,
                     "battery_pct": 88.0, "temp_c": 31.2}
assert parsed[1] is None, "None battery is unparseable"
assert parsed[2] is None, "non-int timestamp is unparseable"
assert summarise(parsed[:1], problems) == {
    "count": 1, "mean_battery": 88.0, "max_temp": 31.2, "quarantined": 2,
}

# semantic quarantine: parses but out of range
out_of_range = parse_record(("rx-09", 5, 150.0, 20.0))
assert out_of_range is not None
assert validate_record(out_of_range) == ["battery_pct 150.0 outside [0, 100]"]

# everything corrupt
assert summarise([None, None], ["unparseable record"] * 2) == {
    "count": 0, "mean_battery": None, "max_temp": None, "quarantined": 2,
}

# empty input
assert summarise([], []) == {
    "count": 0, "mean_battery": None, "max_temp": None, "quarantined": 0,
}

# '0' is a valid robot id; '' is not
assert parse_record(("0", 1, 50.0, 20.0)) is not None
assert parse_record(("", 1, 50.0, 20.0)) is None

# temperature bounds
assert validate_record(parse_record(("rx", 1, 50.0, 200.0)))

# determinism: identical report every run
first = summarise(parsed[:1], problems)
second = summarise([parse_record(r) for r in raw_records][:1], problems)
assert first == second == {
    "count": 1, "mean_battery": 88.0, "max_temp": 31.2, "quarantined": 2,
}

print("Exercise 8: all solution tests passed")
''',
            ),
            solution(
                number=9,
                code='''
from shared import SensorError


def _check_battery(robot, limits):
    value = robot.status().get("battery_pct")
    limit = limits["min_battery_pct"]
    passed = value is not None and value >= limit
    return ("battery", passed, value, f">= {limit}")


def _check_clearance(robot, limits):
    limit = limits["min_clearance_m"]
    try:
        value = robot.read_sensor("distance")
    except SensorError as exc:
        return ("clearance", False, str(exc), "sensor ok")
    return ("clearance", value >= limit, value, f">= {limit}")


def _check_thermal(robot, limits):
    limit = limits["max_temp_c"]
    try:
        value = robot.read_sensor("temperature")
    except SensorError as exc:
        return ("thermal", False, str(exc), "sensor ok")
    return ("thermal", value <= limit, value, f"<= {limit}")


def _check_voltage(robot, limits):
    limit = limits["min_voltage_v"]
    value = robot.status().get("battery_voltage", robot.read_sensor("battery_voltage"))
    return ("voltage", value >= limit, value, f">= {limit}")


def _check_speed(robot, limits):
    limit = limits["max_speed_mps"]
    value = getattr(robot, "max_speed_mps", None)
    return ("speed", value is not None and value <= limit, value, f"<= {limit}")


def _check_driveable(robot, limits):
    value = hasattr(robot, "move")
    return ("driveable", value, "move()" if value else "no move()", "present")


def run_checks(robot, limits: dict) -> list[tuple]:
    """Run every pre-flight check. Returns (name, passed, measured, limit) tuples.

    Never prints and never formats strings: the renderer owns presentation, so
    this function is testable without capturing stdout.
    """
    checks = (
        _check_battery, _check_clearance, _check_thermal,
        _check_voltage, _check_speed, _check_driveable,
    )
    results = []
    for check in checks:
        results.append(check(robot, limits))
    assert len(results) >= 6, "a pre-flight report needs at least six checks"
    return results


def can_start(results) -> bool:
    """True only when every check passed."""
    return all(result[1] for result in results)


def render_report(results) -> str:
    """Render pre-flight results as an operator-facing report. Pure function."""
    lines = [f"ROBO-X PRE-FLIGHT ({len(results)} checks)"]
    width = max((len(name) for name, *_ in results), default=8)
    for name, passed, measured, limit in results:
        mark = "PASS" if passed else "FAIL"
        lines.append(f"[{mark}] {name:<{width}}  {measured!s:<18} {limit}")
    verdict = "PASS" if can_start(results) else "FAIL"
    lines.append(f"RESULT: {verdict}")
    return "\\n".join(lines)
''',
                explanation=(
                    "The design splits cleanly into three layers: `run_checks` *collects* "
                    "structured results, `can_start` *decides*, `render_report` *presents*. "
                    "Only the third knows about strings, which means the first two are "
                    "testable with plain assertions and no output capture.\n\n"
                    "Each check is a tiny function returning a 4-tuple. That uniformity is "
                    "what lets the loop stay a loop, and what lets the renderer stay a "
                    "renderer.\n\n"
                    "`_check_voltage` reads from `status()` first and falls back to the "
                    "sensor, because different robot classes expose battery voltage "
                    "differently — duck typing applied to a real difference.\n\n"
                    "A failing sensor becomes a failed *check line*, not an aborted report. "
                    "That is the behaviour an operator needs at 3 a.m."
                ),
                complexity=(
                    "O(c) in the number of checks (c = 6, constant), plus O(1) per check. "
                    "Rendering is O(total characters)."
                ),
                edge_cases=(
                    "A `SensorError` from either sensor check yields `passed=False` with the "
                    "error text in the `measured` column, and the remaining checks still run.\n\n"
                    "A robot without `move` produces `[FAIL] driveable  no move()  present`.\n\n"
                    "A missing threshold key raises `KeyError` naming it — deliberately, "
                    "because a silent default hides a configuration bug until it causes an "
                    "incident.\n\n"
                    "`measured` may be a float, a string or `None`; `!s` formatting handles "
                    "all three without a special case."
                ),
                alternative_approaches=(
                    "Returning a list of dataclasses (`Check(name, passed, measured, limit)`) "
                    "is better as the project grows: field access beats tuple indexing, and "
                    "`dataclasses` are introduced in topic 6.1. The tuple keeps this exercise "
                    "focused on separation of concerns.\n\n"
                    "A `verbose` flag adding remediation hints is the extension, and it is "
                    "worth doing: `'low battery: recharge before dispatch'` tells an operator "
                    "what to *do*, not just what is wrong."
                ),
                testing='''
from shared import SimulatedRobot


class NoMoveRover:
    def status(self):
        return {"battery_pct": 90.0, "battery_voltage": 14.0}

    def read_sensor(self, channel):
        return 5.0


LIMITS = {
    "min_battery_pct": 20.0,
    "min_clearance_m": 1.0,
    "max_temp_c": 45.0,
    "min_voltage_v": 12.0,
    "max_speed_mps": 3.0,
}

robot = SimulatedRobot(name="robo-x-01", battery_wh=200.0)
results = run_checks(robot, LIMITS)

assert len(results) == 6
assert can_start(results) is True
report = render_report(results)
assert report.startswith("ROBO-X PRE-FLIGHT (6 checks)")
assert report.rstrip().endswith("RESULT: PASS")
assert report.count("[PASS]") == 6

# purity: same results -> same string
assert render_report(results) == render_report(results)
assert render_report(run_checks(robot, LIMITS)) == report

# a failing sensor fails its check without aborting the report
robot.inject_sensor_fault(1)
flaky = run_checks(robot, LIMITS)
assert len(flaky) == 6, "all six checks must still run"
assert can_start(flaky) is False
assert "[FAIL]" in render_report(flaky)

# missing move capability
nomove = run_checks(NoMoveRover(), LIMITS)
assert dict((r[0], r[1]) for r in nomove)["driveable"] is False
assert "RESULT: FAIL" in render_report(nomove)

# low battery is a failure with the value visible
weak = run_checks(SimulatedRobot(name="weak", battery_wh=8.0), LIMITS)
assert dict((r[0], r[1]) for r in weak)["battery"] is False
assert "8.0" in render_report(weak)

# missing threshold raises KeyError naming the key
try:
    run_checks(robot, {"min_battery_pct": 20.0})
except KeyError as exc:
    assert "min_clearance_m" in str(exc)
else:
    raise AssertionError("expected KeyError for a missing threshold")

# run_checks must not print
assert all(len(r) == 4 for r in results), "each result is a 4-tuple"

print("Exercise 9: all solution tests passed")
''',
            ),
            solution(
                number=10,
                code='''
def clamp(value: float, low: float, high: float) -> float:
    """Return `value` constrained to [low, high].

    Raises:
        ValueError: if `low > high`. A reversed range is a caller bug and is
            never silently corrected, because guessing the intent can mask a
            logic error in the caller.
    """
    if low > high:
        raise ValueError(f"low {low} must not exceed high {high}")
    if value < low:
        return low
    if value > high:
        return high
    return value


def require_in_range(value: float, low: float, high: float, name: str = "value") -> float:
    """Return `value` if it lies within [low, high], else raise ValueError.

    Raises:
        ValueError: naming `name` so the log line identifies the offending field.
    """
    if low > high:
        raise ValueError(f"low {low} must not exceed high {high}")
    if not (low <= value <= high):
        raise ValueError(f"{name}={value} outside [{low}, {high}]")
    return value


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Return numerator / denominator, or `default` when the denominator is zero."""
    if denominator == 0.0:
        return default
    return numerator / denominator
''',
                explanation=(
                    "Three small functions with one job each, one consistent error style, "
                    "and consistent parameter naming. That consistency *is* the library — a "
                    "guard set that surprises you in one place will surprise you in all.\n\n"
                    "`clamp` writes both comparisons explicitly rather than using "
                    "`max(low, min(value, high))`. The explicit version shows the "
                    "inclusive-bounds behaviour directly and is easier to extend (topic 3.7's "
                    "comprehension version is the alternative).\n\n"
                    "`require_in_range` takes a `name` parameter purely so error messages "
                    "identify the field. This is a small design decision with a large "
                    "operational payoff: a log line saying `speed_mps=12.0 outside [0, 3.0]` "
                    "is diagnosable in seconds; `value=12.0 outside...` is not."
                ),
                complexity="O(1) time and space for all three functions.",
                edge_cases=(
                    "`clamp(v, 5, 5)` returns 5 for every `v` — the range is a single point "
                    "and the implementation handles it without a special case.\n\n"
                    "`safe_divide(0.0, 0.0)` returns `default`, never `nan`. In control code "
                    "`float('inf')` is often the better default: it propagates loudly through "
                    "subsequent comparisons instead of silently becoming 0.0.\n\n"
                    "`-0.0 == 0.0` is True in Python, so `safe_divide(x, -0.0)` correctly "
                    "returns the default.\n\n"
                    "A reversed range raises in *both* clamp and require_in_range. Swapping "
                    "the arguments would 'work' but would hide the caller's bug."
                ),
                alternative_approaches=(
                    "`functools.reduce` with `min`/`max` is a one-liner for `clamp`, but it "
                    "allocates a function call per comparison and is less readable. At this "
                    "scale that is a stylistic wash; at 10 kHz it is measurable.\n\n"
                    "Type annotations (topic 9.1) can express `def clamp(value: float, low: "
                    "float, high: float) -> float` and let a checker verify call sites. The "
                    "annotations were omitted here to keep the exercise about contracts "
                    "rather than typing."
                ),
                testing='''
import random

# clamp
assert clamp(5, 0, 10) == 5
assert clamp(-1, 0, 10) == 0
assert clamp(11, 0, 10) == 10
assert clamp(7, 7, 7) == 7            # degenerate single-point range
assert clamp(0.0, 0.0, 1.0) == 0.0   # boundary values are inclusive
assert clamp(1.0, 0.0, 1.0) == 1.0

# clamp rejects a reversed range rather than swapping
try:
    clamp(5, 10, 0)
except ValueError as exc:
    assert "10" in str(exc) and "0" in str(exc)
else:
    raise AssertionError("expected ValueError for a reversed range")

# require_in_range
assert require_in_range(5, 0, 10, "speed_mps") == 5
assert require_in_range(0, 0, 10, "speed_mps") == 0
for bad in (-0.1, 10.1):
    try:
        require_in_range(bad, 0, 10, "speed_mps")
    except ValueError as exc:
        assert "speed_mps" in str(exc), "error must name the parameter"
    else:
        raise AssertionError(f"expected ValueError for {bad}")

# safe_divide
import math
assert safe_divide(10.0, 2.0) == 5.0
assert safe_divide(10.0, 0.0) == 0.0
assert safe_divide(10.0, -0.0) == 0.0            # negative zero behaves as zero
assert math.isinf(safe_divide(1.0, 0.0, default=float("inf")))
assert safe_divide(0.0, 0.0) == 0.0              # never NaN

# Property test over 1000 seeded cases
rng = random.Random(20260101)
for _ in range(1000):
    low = round(rng.uniform(-50, 50), 3)
    high = low + round(rng.uniform(0, 25), 3)
    value = round(rng.uniform(-60, 60), 3)
    result = clamp(value, low, high)
    assert low <= result <= high, (value, low, high, result)
    assert clamp(value, low, high) == result    # deterministic

# Type family is preserved
assert isinstance(clamp(5, 0, 10), int)
assert isinstance(clamp(5.0, 0.0, 10.0), float)
assert isinstance(safe_divide(1, 2), float)

print("Exercise 10: all solution tests passed")
''',
            ),
        ],
