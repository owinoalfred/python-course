"""Topic 2.2 - for Loops and while Loops.

Hand-authored to the Course Content Standard. The spine: a for loop asks a sequence
for its next element, a while loop asks a question - and only one of the two can
stop on its own.
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
        "A `for` loop does not know how many iterations it will run. It asks the object "
        "you gave it for one element at a time until the object is exhausted. That is "
        "why a for loop is safe by construction: there is no counter to get wrong and "
        "no condition to forget, so it cannot run forever."
    ),
    MD(
        "A `while` loop is the opposite. It knows nothing about how many iterations it "
        "will run; it re-evaluates a condition until the condition becomes false. That "
        "flexibility is exactly why a while loop can run forever: if the condition "
        "never becomes false, nothing stops it. Every while loop in production code "
        "therefore needs a bound, a timeout, or a state that provably changes."
    ),
    CODE_CELL(
        "waypoints = [(0.0, 0.0), (3.0, 0.0), (3.0, 4.0)]\n"
        "\n"
        "# for: the sequence decides when to stop\n"
        "for index, (x, y) in enumerate(waypoints):\n"
        "    print(f'  visiting {index}: ({x}, {y})')\n"
        "\n"
        "# while: the condition decides, so it needs a bound\n"
        "remaining = 3\n"
        "while remaining > 0:\n"
        "    remaining -= 1\n"
        "    print(f'  steps left: {remaining}')"
    ),
    MD(
        "The practical rule is simple: reach for `for` when you have a sequence, and "
        "for `while` only when progress depends on a condition that changes inside the "
        "body. If nothing in the loop body changes the state the condition depends on, "
        "the loop cannot terminate - and that is a bug, not a design."
    ),
    NOTE(
        "A range is a sequence, so a for loop over it is still safe",
        "`for i in range(10)` has a definite length even though the loop looks "
        "condition-free. The length comes from the range object, not from a counter in "
        "the loop body.",
    ),
]

LESSON["formal_theory"] = [
    MD(
        "Iteration is a protocol, not a language feature. An object is iterable if it "
        "has an `__iter__` method returning an iterator, and an iterator has "
        "`__next__` returning the next value or raising `StopIteration` when it is "
        "done. A for loop is exactly that protocol driven for you, which is why any "
        "object you write can be used with for once it implements the two methods."
    ),
    EQUATION(
        "for x in it:  ==  it = iter(it); loop { x = next(it) until StopIteration }"
    ),
    MD(
        "The exhaustion rule is what makes the for loop safe. The loop terminates "
        "because the iterator says so, not because a counter reached a limit - so an "
        "infinite sequence such as `itertools.count()` will happily loop forever unless "
        "the body itself breaks out."
    ),
    CODE_CELL(
        "class Countdown:\n"
        "    \"\"\"A minimal iterator: iterable in itself, as Python expects.\"\"\"\n"
        "\n"
        "    def __init__(self, start):\n"
        "        self.current = start\n"
        "\n"
        "    def __iter__(self):\n"
        "        return self\n"
        "\n"
        "    def __next__(self):\n"
        "        if self.current <= 0:\n"
        "            raise StopIteration\n"
        "        self.current -= 1\n"
        "        return self.current + 1\n"
        "\n"
        "\n"
        "for value in Countdown(3):\n"
        "    print(value, end=' ')\n"
        "print()"
    ),
    TABLE(
        ["Loop", "Stops when", "Safe without a bound?", "Typical use"],
        [
            ["`for`", "the sequence is exhausted", "yes", "iterating data"],
            ["`while`", "the condition becomes false", "**no**", "waiting for a state"],
            ["`for ... in range(n)`", "n steps complete", "yes", "fixed counts"],
        ],
    ),
]

LESSON["syntax"] = [
    MD(
        "The canonical for loop names the sequence once and unpacks the element; the "
        "canonical while loop owns a counter it changes in the body."
    ),
    CODE_CELL(
        "def drive_route(waypoints, max_speed_mps: float = 1.2) -> list[tuple]:\n"
        "    \"\"\"Return the waypoints that are within the speed limit.\"\"\"\n"
        "    visited: list[tuple] = []\n"
        "    for index, point in enumerate(waypoints):\n"
        "        if point[0] > max_speed_mps:\n"
        "            continue\n"
        "        visited.append((index, point))\n"
        "    return visited\n"
        "\n"
        "\n"
        "print(drive_route([(0.5, 1.0), (1.9, 2.0), (1.0, 3.0)]))"
    ),
    MD("The anti-pattern - a while loop with no bound and no progress:"),
    CODE(
        "battery = 48.0\n"
        "while battery > 0:      # battery never changes -> infinite loop\n"
        "    print('still driving')\n"
        "\n"
        "while True:\n"
        "    battery -= 0.5       # progress is visible in the body\n"
        "    if battery <= 0:\n"
        "        break",
        lang="text",
    ),
    WARN(
        "Every while loop needs a way out",
        "If the body contains nothing that changes the condition, the loop is infinite. "
        "In a robot that is not a hang, it is a runaway - so every while loop here gets "
        "a bound, a break, or a state that provably moves.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - iterating directly rather than by index.**"),
    CODE_CELL(
        "readings = [0.4, 0.6, 0.5]\n"
        "\n"
        "# for: the sequence supplies the element\n"
        "for reading in readings:\n"
        "    print(f'{reading:.1f}', end=' ')\n"
        "print()\n"
        "\n"
        "# manual index: the loop owns the bookkeeping\n"
        "index = 0\n"
        "while index < len(readings):\n"
        "    print(f'{readings[index]:.1f}', end=' ')\n"
        "    index += 1\n"
        "print()"
    ),
    MD("**Example 2 - the two loops side by side.**"),
    CODE_CELL(
        "target = 7\n"
        "\n"
        "steps = 0\n"
        "while steps < target:\n"
        "    steps += 1\n"
        "print('while ->', steps)\n"
        "\n"
        "count = 0\n"
        "for _ in range(target):\n"
        "    count += 1\n"
        "print('for   ->', count)"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "A waypoint follower is the canonical robotics loop: it walks a route, "
        "accumulates distance, and stops when the route is exhausted. Notice that the "
        "termination comes from the data, not from a counter."
    ),
    CODE_CELL(
        "import math\n"
        "\n"
        "WAYPOINTS = [(0.0, 0.0), (3.0, 0.0), (3.0, 4.0)]\n"
        "\n"
        "\n"
        "def follow(points) -> dict:\n"
        "    travelled = 0.0\n"
        "    position = points[0]\n"
        "    for target in points[1:]:\n"
        "        travelled += math.dist(position, target)\n"
        "        position = target\n"
        "    return {'waypoints': len(points), 'distance_m': round(travelled, 3)}"
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "Once you can write `__iter__` and `__next__`, you can make any object work "
        "with a for loop - which is how lazy sensor streams and infinite retry "
        "generators are built."
    ),
    CODE_CELL(
        "class Readings:\n"
        "    \"\"\"Iterate a fixed list of readings without copying it.\"\"\"\n"
        "\n"
        "    def __init__(self, values):\n"
        "        self._values = values\n"
        "        self._index = 0\n"
        "\n"
        "    def __iter__(self):\n"
        "        return self\n"
        "\n"
        "    def __next__(self):\n"
        "        if self._index >= len(self._values):\n"
        "            raise StopIteration\n"
        "        value = self._values[self._index]\n"
        "        self._index += 1\n"
        "        return value\n"
        "\n"
        "\n"
        "stream = Readings([0.1, 0.2, 0.3])\n"
        "print('sum   :', round(sum(stream), 3))\n"
        "print('drained:', round(sum(stream), 3))"
    ),
    MD(
        "That last line is the point of the protocol: once an iterator is exhausted it "
        "stays exhausted, so summing the same object twice gives zero. Iterating a list "
        "twice gives the same answer, because a list is re-iterable."
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "Below is a mission-step planner: it walks a queue of steps, tracks progress, "
        "and refuses to run unbounded if a step keeps failing."
    ),
    CODE_CELL(
        "\"\"\"planner.py - run mission steps with a bound on retries.\"\"\"\n"
        "from __future__ import annotations\n"
        "\n"
        "MAX_ATTEMPTS = 3\n"
        "\n"
        "\n"
        "def run_steps(steps, should_stop=lambda: False) -> dict:\n"
        "    \"\"\"Run each step, retrying a failure up to MAX_ATTEMPTS.\n"
        "\n"
        "    Returns a report; never raises for a failing step, and stops\n"
        "    early when the stop predicate becomes true.\n"
        "    \"\"\"\n"
        "    completed: list[str] = []\n"
        "    failed: list[str] = []\n"
        "    for step in steps:\n"
        "        if should_stop():\n"
        "            break\n"
        "        for attempt in range(1, MAX_ATTEMPTS + 1):\n"
        "            if attempt == MAX_ATTEMPTS and not step.get('reliable'):\n"
        "                failed.append(step['name'])\n"
        "                break\n"
        "            completed.append(step['name'])\n"
        "            break\n"
        "    return {'completed': completed, 'failed': failed,\n"
        "            'stopped_early': len(completed) + len(failed) < len(steps)}"
    ),
    MD(
        "The outer loop is safe because the sequence is finite. The inner retry loop is "
        "a for over range, so it is bounded by construction - which is the pattern to "
        "copy whenever a retry needs a maximum. The stop predicate is checked at the top "
        "of each outer iteration so a mission can be aborted between steps."
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "MAX_ATTEMPTS is a module constant so the retry policy is visible at the top "
            "of the file rather than buried in a range call.",
            "The outer for loop is finite because steps is a sequence - no condition "
            "involved, so it cannot run away.",
            "The stop predicate is checked at the top of each iteration, so a mission can "
            "be aborted between steps rather than only between retries.",
            "The inner loop is a for over range, which is bounded by construction; this "
            "is the safe way to express a retry.",
            "The attempt counter is compared against MAX_ATTEMPTS explicitly, so the "
            "final failure is a decision rather than an accident.",
            "A reliable step succeeds on the first attempt and breaks immediately, so "
            "the retry budget is only spent where it is needed.",
            "stopped_early is derived by comparing counts, which keeps the report "
            "consistent with the lists rather than needing a separate flag.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - a while loop whose body does not change the condition.**"),
    CODE(
        "battery = 48.0\n"
        "while battery > 0:      # battery is never changed\n"
        "    print('driving')\n"
        "\n"
        "while battery > 0:      # progress is made each pass\n"
        "    battery -= 0.5",
        lang="text",
    ),
    MD("**Mistake 2 - iterating by index when direct iteration will do.**"),
    CODE(
        "for i in range(len(readings)):\n"
        "    print(readings[i])\n"
        "\n"
        "for reading in readings:\n"
        "    print(reading)",
        lang="text",
    ),
    MD("**Mistake 3 - reusing an exhausted iterator.**"),
    CODE(
        "stream = Readings([0.1, 0.2])\n"
        "print(sum(stream))   # 0.3\n"
        "print(sum(stream))   # 0.0 - it is drained\n"
        "\n"
        "print(sum([0.1, 0.2]))   # a list can be re-iterated",
        lang="text",
    ),
    MD("**Mistake 4 - an unbounded retry loop.**"),
    CODE(
        "while not sensor_ok():\n"
        "    retry()\n"
        "\n"
        "for attempt in range(MAX_ATTEMPTS):\n"
        "    if sensor_ok():\n"
        "        break\n"
        "    retry()",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "For a loop that runs the wrong number of times, the fastest diagnosis is to "
        "print the length of the sequence alongside the loop, and to check whether an "
        "iterator has already been consumed."
    ),
    CODE_CELL(
        "readings = [0.4, 0.6, 0.5]\n"
        "print('len  :', len(readings))\n"
        "print('list :', list(readings))\n"
        "\n"
        "iterator = iter(readings)\n"
        "print('next :', next(iterator))\n"
        "print('rest :', list(iterator))\n"
        "print('empty:', list(iterator))"
    ),
    MD(
        "For a loop that never ends, instrument the condition rather than the body. "
        "Printing the values the condition depends on on every pass shows immediately "
        "whether it is changing."
    ),
    CODE_CELL(
        "battery = 3.0\n"
        "passes = 0\n"
        "while battery > 0:\n"
        "    battery -= 0.5\n"
        "    passes += 1\n"
        "    if passes > 10:\n"
        "        print('bailed out: condition not converging')\n"
        "        break\n"
        "print('passes:', passes)"
    ),
    NOTE(
        "A safety bound is not a code smell",
        "Adding a maximum iteration count to a loop you believe terminates costs nothing "
        "and turns a runaway into a diagnosable error.",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Reach for `for` when you have a sequence; it cannot run forever.",
            "Use `while` only when progress depends on a changing condition.",
            "Give every while loop a bound, a break, or a provably changing state.",
            "Iterate the element directly; index only when you need the position.",
            "Use `enumerate` rather than a manual counter.",
            "Do not reuse an iterator that may already be exhausted.",
            "Bound every retry loop with a fixed attempt count.",
            "Prefer a generator for a lazy sequence over building the whole list.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "The for loop over a list is the fastest common loop in Python because the "
        "interpreter holds a direct reference to the list and never calls a method to "
        "fetch the next element. The equivalent manual index loop is measurably slower "
        "at the same asymptotics, and `for x in list` also avoids the bounds check that "
        "an index loop performs on every pass."
    ),
    MD(
        "The real cost is in the body, not the loop. Appending to a list inside a loop "
        "is amortised O(1), but building a new string with `+=` on every iteration is "
        "quadratic because each concatenation copies what has accumulated. A generator "
        "avoids materialising the result at all, which matters when the sequence is long "
        "or infinite - and a sensor stream is often exactly that."
    ),
    TIP(
        "Measure the body",
        "If a loop is slow, time the work inside it. Swapping a for loop for a while "
        "loop never makes anything faster.",
    ),
]

LESSON["pythonic_approaches"] = [
    MD("Accumulating by index versus iterating the element."),
    CODE_CELL(
        "readings = [0.4, 0.9, 0.6]\n"
        "\n"
        "# before: the loop owns the counter and the bound\n"
        "total = 0.0\n"
        "index = 0\n"
        "while index < len(readings):\n"
        "    total += readings[index]\n"
        "    index += 1\n"
        "\n"
        "# after: the sequence owns termination, the loop owns the work\n"
        "total = 0.0\n"
        "for reading in readings:\n"
        "    total += reading\n"
        "\n"
        "print('total:', round(total, 3))"
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "A delivery cart follows a route, and the route is a sequence - so the outer "
        "loop is a for over waypoints. Inside, the cart may retry a motor command, and "
        "that retry is the case where a bound is mandatory."
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
        "ROUTE = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)]\n"
        "\n"
        "robot = SimulatedRobot(name='cart-01', battery_wh=48.0)\n"
        "legs = 0\n"
        "for target in ROUTE[1:]:\n"
        "    robot.move(distance_m=1.0, speed_mps=1.0)\n"
        "    legs += 1\n"
        "print(f'completed {legs} legs, battery {robot.status()[\"battery_pct\"]:.1f}%')"
    ),
]

LESSON["engineering_example"] = [
    MD(
        "A bounded polling loop - the pattern a supervisor uses when it waits for a "
        "condition it cannot observe directly."
    ),
    CODE_CELL(
        "def poll(check, attempts: int = 5, on_retry=None) -> bool:\n"
        "    \"\"\"Call check() up to `attempts` times; return True on the first success.\"\"\"\n"
        "    for attempt in range(1, attempts + 1):\n"
        "        if check():\n"
        "            return True\n"
        "        if on_retry is not None:\n"
        "            on_retry(attempt)\n"
        "    return False"
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Sum a list of readings three ways - a while loop with a counter, a for "
            "loop, and sum() - and confirm all three agree.",
            "Write a for loop over a range that prints only the even indices.",
            "Write a while loop with a counter that stops at 10, and explain what would "
            "make it infinite.",
            "Define a class with __iter__ and __next__ that iterates a list backwards, "
            "then sum it twice to see what happens on the second pass.",
        ]
    ),
    CODE_CELL(
        "readings = [0.4, 0.9, 0.6]\n"
        "\n"
        "total = 0.0\n"
        "index = 0\n"
        "while index < len(readings):\n"
        "    total += readings[index]\n"
        "    index += 1\n"
        "print('while:', round(total, 3))\n"
        "\n"
        "print('for  :', round(sum(readings), 3))\n"
        "print('builtin:', round(sum(readings), 3))\n"
        "\n"
        "count = 0\n"
        "while count < 10:\n"
        "    count += 1\n"
        "print('bounded while reached', count)\n"
        "\n"
        "for position in range(0, 6, 2):\n"
        "    print('even position:', position)"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: the for loop asks the sequence for permission, the while loop "
        "asks the world a question.** A sequence can say 'no more' - that is what "
        "exhaustion means - so a for loop always terminates. A question has no such "
        "guarantee, so a while loop terminates only if something inside the body "
        "changes the answer."
    ),
    TABLE(
        ["", "`for`", "`while`"],
        [
            ["Who decides to stop", "the sequence, by being exhausted", "the condition, by becoming false"],
            ["Can it run forever", "only if the sequence is infinite", "yes, easily"],
            ["Typical bug", "iterating a drained iterator", "a body that never changes the condition"],
            ["Safe form", "`for x in items`", "`while ... : ... ; state changes`"],
        ],
    ),
]

TERMS = [
    ["Loop", "A block that runs once per iteration."],
    ["Iteration", "One pass through a loop body."],
    ["Sequence", "An object yielding elements one at a time, such as a list."],
    ["Iterable", "An object with an __iter__ method."],
    ["Iterator", "An object with __next__, which raises StopIteration when exhausted."],
    ["Exhaustion", "The state of an iterator after it has yielded everything."],
    ["StopIteration", "The exception that ends a for loop."],
    ["Infinite loop", "A loop that never terminates, usually a while with no progress."],
    ["Bound", "A maximum count that guarantees a retry loop terminates."],
    ["Accumulator", "A variable updated on each pass to hold a running total."],
]

LESSON["summary"] = [
    MD(
        "A for loop does not know how many times it will run. It asks the object for one "
        "element at a time until the object says it is exhausted, which is why it is "
        "safe by construction - there is no counter to get wrong and no condition to "
        "forget. A while loop makes no such promise: it re-evaluates a condition, and it "
        "terminates only if something in the body changes the answer."
    ),
    MD(
        "That asymmetry is the practical lesson. Reach for a for loop whenever you have "
        "a sequence, and for a while loop only when progress genuinely depends on a "
        "condition. Every while loop that reaches production needs a bound, a break, or "
        "a state that provably changes - and a retry loop should be a `for` over "
        "`range(MAX_ATTEMPTS)`, which is bounded for free."
    ),
    MD(
        "Understanding iteration as a protocol rather than a language feature is what "
        "makes the rest of the course compose. Because `for` is exactly `iter()` plus "
        "`next()` until `StopIteration`, you can make your own objects work with it by "
        "implementing two methods - and you can see why a generator can be lazy and "
        "infinite, and why a consumed iterator stays consumed. For a telemetry pipeline "
        "this is not academic: sensor streams are long, sometimes endless, and a loop "
        "that cannot stop is a robot that cannot stop."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "A for loop is driven by the sequence and cannot run away.",
            "A while loop is driven by a condition and can run forever.",
            "Every while loop needs a bound, a break, or visible progress.",
            "Iterate the element directly; use enumerate when you need the index.",
            "Implement __iter__ and __next__ to make your own objects loopable.",
            "An exhausted iterator stays exhausted - do not reuse it.",
            "Bound every retry loop with a fixed attempt count.",
            "A for over range(n) is the safe way to express a fixed count.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "The for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement)",
            "Data model - the iterator protocol](https://docs.python.org/3/reference/datamodel.html#object.__iter__)",
            "Writing classes - iterators](https://docs.python.org/3/tutorial/classes.html#iterators)",
            "itertools - fast, memory-efficient iterators](https://docs.python.org/3/library/itertools.html)",
            "PEP 234 - the iterator protocol](https://peps.python.org/pep-0234/)",
        ]
    ),
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Total the distance of a route",
        difficulty="MEDIUM",
        learning_objectives=["Accumulate in a for loop.", "Return a rounded total."],
        concepts_tested=["for", "accumulators", "floats"],
        problem_statement=(
            "Write `total_distance(segments)` summing a list of metre values and "
            "returning the total rounded to three decimals."
        ),
        requirements=["Use a for loop with an accumulator.", "Handle an empty list."],
        constraints=["Do not call sum() in the implementation."],
        input_description="A list of non-negative numbers.",
        expected_output="A float.",
        example_input="total_distance([1.5, 2.25, 0.25])",
        example_output="4.0",
        edge_cases=["An empty list returns 0.0.", "A single segment returns it unchanged."],
        hints=["Start the accumulator at 0.0 so an empty list works."],
        success_criteria=["The example returns 4.0.", "An empty list returns 0.0."],
        optional_extension="Raise ValueError if any segment is negative.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Count the positive readings",
        difficulty="MEDIUM",
        learning_objectives=["Filter while iterating.", "Use a counter accumulator."],
        concepts_tested=["for", "conditionals", "counting"],
        problem_statement=(
            "Write `count_positive(values)` returning how many entries are greater "
            "than zero. Non-numeric entries are ignored rather than raising."
        ),
        requirements=["Count in a single pass.", "Skip anything that is not a real number."],
        constraints=["Reject bools from the count."],
        input_description="A list of arbitrary objects.",
        expected_output="An integer.",
        example_input="count_positive([1.0, -1.0, 0.0, 2.0, 'x'])",
        example_output="2",
        edge_cases=["An empty list returns 0.", "Zero is not positive.", "True is not counted."],
        hints=["An if inside the loop is the whole implementation."],
        success_criteria=["The example returns 2.", "An empty list returns 0."],
        optional_extension="Return the count of negatives as well.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Track the running maximum",
        difficulty="MEDIUM",
        learning_objectives=["Compare each pass.", "Start from the first element."],
        concepts_tested=["for", "comparisons", "accumulators"],
        problem_statement=(
            "Write `running_max(values)` returning the largest value seen, or None for "
            "an empty list."
        ),
        requirements=["Track the maximum in a variable.", "Return None for an empty list."],
        constraints=["Do not call max() inside the loop."],
        input_description="A list of comparable values.",
        expected_output="The maximum, or None.",
        example_input="running_max([3, 9, 4, 9, 1])",
        example_output="9",
        edge_cases=["An empty list returns None.", "All-equal values return that value."],
        hints=["Initialise the tracker to the first element, not to zero."],
        success_criteria=["The example returns 9.", "An empty list returns None."],
        optional_extension="Return the index of the first maximum.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Count down with a bounded while loop",
        difficulty="MEDIUM",
        learning_objectives=["Write a while loop.", "Guarantee termination."],
        concepts_tested=["while", "countdown", "termination"],
        problem_statement=(
            "Write `countdown(start, step=1)` returning a list of the values from "
            "`start` down to (but not including) zero. Raise ValueError for a "
            "non-positive step."
        ),
        requirements=["Use a while loop, not a range.", "Terminate when the counter is non-positive."],
        constraints=["Refuse to loop forever: a step of zero raises."],
        input_description="A starting number and an optional step.",
        expected_output="A list of numbers.",
        example_input="countdown(3)",
        example_output="[3, 2, 1]",
        edge_cases=["A step of 0 raises ValueError.", "A negative step raises ValueError.", "A start of 0 gives an empty list."],
        hints=["Validate the step before the loop, not inside it."],
        success_criteria=["countdown(3) gives [3, 2, 1].", "countdown(0) gives []."],
        optional_extension="Support a step larger than one.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Find the first reading above a threshold",
        difficulty="MEDIUM",
        learning_objectives=["Return early from a loop.", "Handle the not-found case."],
        concepts_tested=["for", "return", "search"],
        problem_statement=(
            "Write `first_above(values, threshold)` returning the first value greater "
            "than `threshold`, or None when there is none."
        ),
        requirements=["Stop iterating as soon as it is found.", "Return None when absent."],
        constraints=["Do not build an intermediate list."],
        input_description="A list of numbers and a threshold.",
        expected_output="A number, or None.",
        example_input="first_above([1.0, 7.5, 9.0], 5.0)",
        example_output="7.5",
        edge_cases=["An empty list returns None.", "A value exactly on the threshold is skipped.", "The first match is returned, not the largest."],
        hints=["Return from inside the loop."],
        success_criteria=["The example returns 7.5.", "An empty list returns None."],
        optional_extension="Return the index instead of the value.",
    )
)


EXERCISES.append(
    exercise(
        number=6,
        title="Total the length of a path",
        difficulty="HARD",
        learning_objectives=["Carry state across iterations.", "Use a geometric helper."],
        concepts_tested=["for", "math.dist", "accumulators"],
        problem_statement=(
            "Write `path_length(points)` returning the total distance along a list of "
            "(x, y) points, rounded to three decimals. A single point has length 0.0."
        ),
        requirements=["Remember the previous point in a variable.", "Use math.dist."],
        constraints=["Do not assume the input is a list of lists."],
        input_description="A list of (x, y) tuples.",
        expected_output="A float distance.",
        example_input="path_length([(0, 0), (3, 4)])",
        example_output="5.0",
        edge_cases=["A single point returns 0.0.", "An empty list returns 0.0.", "Duplicate points add nothing."],
        hints=["Slice with [1:] so the first point is never compared with itself."],
        success_criteria=["(0,0) to (3,4) gives 5.0.", "A single point gives 0.0."],
        optional_extension="Return the cumulative distances as a list.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Split a sequence into fixed-size chunks",
        difficulty="HARD",
        learning_objectives=["Build nested lists.", "Handle a ragged final chunk."],
        concepts_tested=["for", "slicing", "range"],
        problem_statement=(
            "Write `chunk(sequence, size)` returning a list of lists, each holding up to "
            "`size` items in order. The final chunk may be shorter."
        ),
        requirements=["Preserve order.", "Raise ValueError for a size below 1."],
        constraints=["Do not mutate the input."],
        input_description="Any sequence and a positive chunk size.",
        expected_output="A list of lists.",
        example_input="chunk([1, 2, 3, 4, 5], 2)",
        example_output="[[1, 2], [3, 4], [5]]",
        edge_cases=["A size of 0 raises ValueError.", "An empty sequence gives an empty list."],
        hints=["Iterate over range(0, len(sequence), size) and slice each window."],
        success_criteria=["The example gives [[1, 2], [3, 4], [5]].", "An empty sequence gives []."],
        optional_extension="Return leftover items separately when they cannot fill a chunk.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Scan readings until the first drop",
        difficulty="HARD",
        learning_objectives=["Stop at a state change.", "Report what happened."],
        concepts_tested=["for", "state", "early exit"],
        problem_statement=(
            "Write `until_drop(readings, limit)` returning the readings up to but not "
            "including the first value below `limit`, together with a bool saying "
            "whether a drop occurred."
        ),
        requirements=["Stop at the first value below the limit.", "Report whether a drop happened."],
        constraints=["Do not pre-slice the input."],
        input_description="A list of numbers and a limit.",
        expected_output="A tuple of (list, bool).",
        example_input="until_drop([5.0, 4.0, 1.0, 3.0], 2.0)",
        example_output="([5.0, 4.0], True)",
        edge_cases=["No drop returns the whole list and False.", "A drop on the first value gives an empty list and True."],
        hints=["Break the moment you see the drop, then report the flag."],
        success_criteria=["The example returns ([5.0, 4.0, 1.0], True).", "No drop returns False."],
        optional_extension="Return the index at which the drop occurred.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Poll a condition with a bounded retry",
        difficulty="HARD",
        learning_objectives=["Bound a retry loop.", "Return the outcome rather than raising."],
        concepts_tested=["for over range", "callables", "retry"],
        problem_statement=(
            "Write `poll(check, attempts=3)` calling the zero-argument callable until it "
            "returns truthy or the attempts are used up, returning True on success and "
            "False on exhaustion."
        ),
        requirements=["Use a bounded for loop.", "Call check() at most `attempts` times."],
        constraints=["Do not use a while loop."],
        input_description="A callable and an attempt count.",
        expected_output="A boolean.",
        example_input="poll(lambda: True)",
        example_output="True",
        edge_cases=["A check that never succeeds returns False.", "attempts of 0 returns False without calling check."],
        hints=["A for over range(attempts) is bounded for free."],
        success_criteria=["A passing check returns True.", "A failing check returns False."],
        optional_extension="Accept an on_retry callback invoked with the attempt number.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Follow a waypoint route with the simulator",
        difficulty="HARD",
        learning_objectives=["Drive real API calls from a loop.", "Accumulate a report."],
        concepts_tested=["for", "simulator API", "aggregation"],
        problem_statement=(
            "Write `follow_route(robot, points)` moving the robot one metre along each "
            "segment, returning a dict with `legs` completed and the final battery "
            "percentage rounded to two decimals."
        ),
        requirements=["Move exactly one leg per segment.", "Read the battery after the last move."],
        constraints=["Use the simulator's move() and status() only."],
        input_description="A SimulatedRobot and a list of (x, y) waypoints.",
        expected_output="A dict with legs and battery_pct.",
        example_input="follow_route(robot, [(0, 0), (1, 0), (1, 1)])",
        example_output="{'legs': 2, 'battery_pct': 97.7}",
        edge_cases=["A single waypoint completes zero legs.", "A depleted battery raises from move() and propagates."],
        hints=["Slice the points so the first waypoint is not a movement."],
        success_criteria=["Two segments produce legs == 2.", "The battery percentage is a float."],
        optional_extension="Return the distance travelled as well.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "def total_distance(segments) -> float:\n"
            "    total = 0.0\n"
            "    for segment in segments:\n"
            "        total += segment\n"
            "    return round(total, 3)"
        ),
        explanation=(
            "Starting the accumulator at 0.0 rather than 0 matters: an int accumulator "
            "would return an int for a list of floats, and more importantly the empty "
            "list case is handled by construction rather than by a special branch."
        ),
        complexity="Time O(n); space O(1).",
        edge_cases="An empty list returns round(0.0, 3), which is 0.0.",
        alternative_approaches="round(sum(segments), 3) is the same answer in one line.",
        testing="assert total_distance([1.5, 2.25, 0.25]) == 4.0\nassert total_distance([]) == 0.0",
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def count_positive(values) -> int:\n"
            "    count = 0\n"
            "    for value in values:\n"
            "        if isinstance(value, bool) or not isinstance(value, (int, float)):\n"
            "            continue\n"
            "        if value > 0:\n"
            "            count += 1\n"
            "    return count"
        ),
        explanation=(
            "Skipping with continue keeps the counting branch free of nesting, so the "
            "rule being counted - greater than zero - is the only thing on the "
            "indented line. Excluding bool first matters because it is a subclass of "
            "int and would otherwise be counted."
        ),
        complexity="Time O(n); space O(1).",
        edge_cases="Zero is not positive, so it is not counted.",
        alternative_approaches="A generator with sum(1 for v in values if ...) is the idiomatic one-liner.",
        testing="assert count_positive([1.0, -1.0, 0.0, 2.0, 'x']) == 2\nassert count_positive([]) == 0\nassert count_positive([True, 1]) == 1",
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "def running_max(values):\n"
            "    if not values:\n"
            "        return None\n"
            "    best = values[0]\n"
            "    for value in values[1:]:\n"
            "        if value > best:\n"
            "            best = value\n"
            "    return best"
        ),
        explanation=(
            "Seeding the tracker with the first element rather than zero is what makes "
            "the function correct for all-negative input, and it removes the need to "
            "raise or special-case the first pass. Slicing with [1:] avoids comparing "
            "the first element with itself."
        ),
        complexity="Time O(n); space O(n) for the slice; use an index to avoid it.",
        edge_cases="An all-negative list returns the least-negative value, not zero.",
        alternative_approaches="Iterating from index 1 avoids the copy that [1:] makes.",
        testing="assert running_max([3, 9, 4, 9, 1]) == 9\nassert running_max([]) is None\nassert running_max([-5, -2, -9]) == -2",
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "def countdown(start, step: int = 1) -> list:\n"
            "    if not isinstance(step, int) or isinstance(step, bool) or step <= 0:\n"
            "        raise ValueError(f'step must be a positive integer, got {step!r}')\n"
            "    values: list = []\n"
            "    current = start\n"
            "    while current > 0:\n"
            "        values.append(current)\n"
            "        current -= step\n"
            "    return values"
        ),
        explanation=(
            "Validating the step before the loop is the whole safety story: a step of "
            "zero would leave `current` unchanged and the while condition permanently "
            "true. Refusing to enter the loop is better than entering one that cannot "
            "leave it."
        ),
        complexity="Time O(start / step); space O(start / step).",
        edge_cases="A start of 0 or less gives an empty list, because the condition is false immediately.",
        alternative_approaches="list(range(start, 0, -step)) is the one-line equivalent.",
        testing="assert countdown(3) == [3, 2, 1]\nassert countdown(0) == []",
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "def first_above(values, threshold):\n"
            "    for value in values:\n"
            "        if value > threshold:\n"
            "            return value\n"
            "    return None"
        ),
        explanation=(
            "Returning from inside the loop stops the search at the first match, which "
            "is both the correct answer and the fast one. The trailing return handles "
            "the exhausted case without raising, so the caller can test for None."
        ),
        complexity="Time O(n) worst case; space O(1).",
        edge_cases="A value exactly equal to the threshold does not match, because the test is strictly greater.",
        alternative_approaches="next((v for v in values if v > threshold), None) is the generator form.",
        testing="assert first_above([1.0, 7.5, 9.0], 5.0) == 7.5\nassert first_above([], 5.0) is None",
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "import math\n"
            "\n"
            "\n"
            "def path_length(points) -> float:\n"
            "    if not points:\n"
            "        return 0.0\n"
            "    total = 0.0\n"
            "    previous = points[0]\n"
            "    for current in points[1:]:\n"
            "        total += math.dist(previous, current)\n"
            "        previous = current\n"
            "    return round(total, 3)"
        ),
        explanation=(
            "The previous point is the state the loop carries, and updating it at the "
            "end of each pass is what makes the accumulation correct. Starting from the "
            "first point and slicing the rest means no point is ever compared with "
            "itself, which would add a spurious zero-length step."
        ),
        complexity="Time O(n); space O(n) for the slice.",
        edge_cases="Duplicate consecutive points add exactly 0.0, as they should.",
        alternative_approaches="sum(math.dist(a, b) for a, b in zip(points, points[1:])) is a one-liner.",
        testing="assert path_length([(0, 0), (3, 4)]) == 5.0\nassert path_length([(1, 1)]) == 0.0\nassert path_length([]) == 0.0",
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "def chunk(sequence, size: int) -> list[list]:\n"
            "    if not isinstance(size, int) or isinstance(size, bool) or size < 1:\n"
            "        raise ValueError(f'size must be a positive integer, got {size!r}')\n"
            "    return [\n"
            "        list(sequence[start:start + size])\n"
            "        for start in range(0, len(sequence), size)\n"
            "    ]"
        ),
        explanation=(
            "Stepping the start index by size guarantees the windows tile the input "
            "exactly once, with no overlap and no gap. The final window is short "
            "automatically because a slice past the end simply returns fewer items, "
            "so no special case is needed for the remainder."
        ),
        complexity="Time O(n); space O(n).",
        edge_cases="A size larger than the data produces a single chunk containing everything.",
        alternative_approaches="The comprehension over range is the idiomatic fixed-step form.",
        testing="assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]\nassert chunk([], 3) == []\nassert chunk('abcd', 3) == [['a', 'b', 'c'], ['d']]",
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "def until_drop(readings, limit):\n"
            "    kept: list = []\n"
            "    for reading in readings:\n"
            "        if reading < limit:\n"
            "            return kept, True\n"
            "        kept.append(reading)\n"
            "    return kept, False"
        ),
        explanation=(
            "The drop is detected before the value is appended, which is what makes the "
            "result 'up to but not including' the first bad reading. Returning early "
            "avoids scanning data the caller already knows it does not need."
        ),
        complexity="Time O(n) worst case; space O(n).",
        edge_cases="A drop on the first value returns an empty list and True.",
        alternative_approaches="itertools.takewhile avoids the explicit flag entirely.",
        testing="assert until_drop([5.0, 4.0, 1.0, 3.0], 2.0) == ([5.0, 4.0], True)\nassert until_drop([5.0, 4.0], 2.0) == ([5.0, 4.0], False)",
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "def poll(check, attempts: int = 3, on_retry=None) -> bool:\n"
            "    if attempts < 0:\n"
            "        raise ValueError('attempts must not be negative')\n"
            "    for attempt in range(1, attempts + 1):\n"
            "        if check():\n"
            "            return True\n"
            "        if on_retry is not None and attempt < attempts:\n"
            "            on_retry(attempt)\n"
            "    return False"
        ),
        explanation=(
            "A for over range is bounded by construction, which is exactly the property "
            "a retry loop needs and a while loop lacks. Rejecting a negative attempt "
            "count up front prevents a range that silently does nothing, and the "
            "callback is skipped on the final attempt so it reports only genuine retries."
        ),
        complexity="Time O(attempts); space O(1).",
        edge_cases="attempts of 0 returns False without ever calling check.",
        alternative_approaches="tenacity adds backoff and jitter for real networks.",
        testing="calls = []\ndef flaky():\n    calls.append(1)\n    return len(calls) >= 2\nassert poll(flaky) is True\nassert len(calls) == 2\nassert poll(lambda: False, attempts=2) is False",
    )
)

SOLUTIONS.append(
    solution(
        number=10,
        code=(
            "from shared.robo_x_sim import SimulatedRobot  # noqa: E402\n"
            "\n"
            "\n"
            "def follow_route(robot, points) -> dict:\n"
            "    legs = 0\n"
            "    for target in points[1:]:\n"
            "        robot.move(distance_m=1.0, speed_mps=1.0)\n"
            "        legs += 1\n"
            "    battery = robot.status()['battery_pct']\n"
            "    return {'legs': legs, 'battery_pct': round(battery, 2)}"
        ),
        explanation=(
            "Slicing with [1:] makes the first waypoint a starting position rather than "
            "a movement, which is the off-by-one this exercise is really about. Reading "
            "status once after the loop is cheaper than reading it per leg, and it "
            "reports the final state rather than an intermediate one."
        ),
        complexity="Time O(n) legs; space O(1).",
        edge_cases="A single waypoint completes zero legs and leaves the battery untouched.",
        alternative_approaches="math.dist between waypoints would let the robot move real distances.",
        testing="robot = SimulatedRobot(name='cart-01', battery_wh=48.0)\nout = follow_route(robot, [(0, 0), (1, 0), (1, 1)])\nassert out['legs'] == 2\nassert isinstance(out['battery_pct'], float)",
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
            "CHANNELS = ('distance', 'temperature', 'battery_voltage')\n"
            "MAX_ATTEMPTS = 2\n"
            "\n"
            "\n"
            "def sample_channels(robot, channels=CHANNELS) -> dict:\n"
            "    \"\"\"Read each channel with a bounded retry; None on permanent failure.\"\"\"\n"
            "    readings: dict = {}\n"
            "    for channel in channels:\n"
            "        value = None\n"
            "        for _attempt in range(MAX_ATTEMPTS):\n"
            "            try:\n"
            "                value = robot.read_sensor(channel)\n"
            "                break\n"
            "            except SensorError:\n"
            "                continue\n"
            "        readings[channel] = value\n"
            "    return readings"
        ),
        explanation=(
            "The outer loop is bounded by the channel list and the inner retry by "
            "MAX_ATTEMPTS, so neither can run away - which is the property this topic "
            "is about. A channel that never answers becomes None rather than raising, "
            "so one dead sensor degrades the report instead of stopping the mission."
        ),
        complexity="Time O(c * attempts) for c channels; space O(c).",
        edge_cases="An unknown channel name is retried twice and then recorded as None.",
        alternative_approaches="Reading status() once is cheaper when battery voltage is the only field needed.",
        testing="robot = SimulatedRobot(name='cart-01', battery_wh=48.0)\nout = sample_channels(robot, ['distance', 'nope'])\nassert out['distance'] is not None\nassert out['nope'] is None",
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="What makes a for loop unable to run forever over a finite sequence?",
        choices=[
            "It evaluates a condition on every pass.",
            "It stops when the sequence raises StopIteration.",
            "It keeps an internal counter with a default limit.",
            "It refuses to iterate an infinite object.",
        ],
        answer=1,
        kind="conceptual",
        explanation=(
            "The loop is driven by the iterator protocol: it asks for the next element "
            "until the iterator signals exhaustion. There is no counter to overflow and "
            "no condition to get wrong, so a finite sequence always terminates."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="What does this print?\n\ncount = 0\ni = 0\nwhile i < 3:\n    count += i\n    i += 1\nprint(count)",
        choices=[
            "3",
            "6",
            "0",
            "It runs forever.",
        ],
        answer=0,
        kind="code_output",
        explanation=(
            "The body runs three times adding 0, then 1, then 2. The counter is "
            "incremented each pass, which is exactly the progress that guarantees the "
            "loop terminates."
        ),
        reference="lesson.ipynb - Basic Examples",
    )
)

QUIZ.append(
    quiz(
        question="A while loop never terminates. What is the most likely cause?",
        choices=[
            "The condition uses == where < was meant.",
            "The loop body is indented with tabs.",
            "Nothing in the body changes the value the condition tests.",
            "The counter variable holds a float rather than an int.",
        ],
        answer=2,
        kind="debugging",
        explanation=(
            "A while loop re-evaluates the same condition forever unless something in "
            "the body changes it. A missing increment is the classic form, and the fix "
            "is either the increment or a bounded for loop."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="What does the second `print(sum(stream))` output?",
        choices=[
            "0.3 again, because the list is unchanged.",
            "It raises a TypeError.",
            "The name stream is undefined at that point.",
            "0.0, because the iterator is already exhausted.",
        ],
        answer=3,
        kind="identify_error",
        explanation=(
            "An iterator is single-use: once it has raised StopIteration it keeps doing "
            "so, so the second sum sees no elements. A list is re-iterable, which is why "
            "wrapping it in iter() changes the behaviour."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="Why prefer `for x in items` over `for i in range(len(items))`?",
        choices=[
            "It cannot produce an index error and it states the intent directly.",
            "It is always ten times faster.",
            "It accepts more data types than an index loop.",
            "It is the only form that supports early exit.",
        ],
        answer=0,
        kind="reasoning",
        explanation=(
            "The index loop has to maintain a counter and re-check the length on every "
            "pass, which is state the sequence already owns. The direct form also "
            "removes an entire class of off-by-one defect."
        ),
        reference="lesson.ipynb - Pythonic Approaches",
    )
)

QUIZ.append(
    quiz(
        question="Which is the safest way to write a retry loop?",
        choices=[
            "`while not ready():`",
            "`for _ in range(MAX_ATTEMPTS):`",
            "`for item in endless_stream:`",
            "`while True:`",
        ],
        answer=1,
        kind="multiple_choice",
        explanation=(
            "A for over a fixed range is bounded by construction, so it cannot run away "
            "even if the success condition is never met. Every while form listed can "
            "loop indefinitely, which for a motor command is a safety problem."
        ),
        reference="lesson.ipynb - Best Practices",
    )
)

QUIZ.append(
    quiz(
        question=(
            "What does `list(R(2))` return for a class whose `__next__` decrements `n` "
            "and raises StopIteration once `n` reaches zero?"
        ),
        choices=[
            "[0, 1]",
            "It raises StopIteration.",
            "[1, 2]",
            "[1, 0]",
        ],
        answer=3,
        kind="code_output",
        explanation=(
            "The first call decrements 2 to 1 and returns 1; the second decrements 1 to 0 "
            "and returns 0; the third finds n at zero and stops. The value is produced "
            "before the decrement takes effect, the usual off-by-one in a hand-written "
            "iterator."
        ),
        reference="lesson.ipynb - Advanced Examples",
    )
)

QUIZ.append(
    quiz(
        question="A telemetry stream never ends. Which structure is appropriate?",
        choices=[
            "A for loop over the whole stream.",
            "A while loop with no bound.",
            "A for loop over a bounded batch, or a generator consumed with a break.",
            "Recursion over each reading.",
        ],
        answer=2,
        kind="reasoning",
        explanation=(
            "A for loop over an infinite stream never returns. Consuming a generator "
            "with a break, or looping over a bounded slice, keeps the termination "
            "decision where you can see and test it."
        ),
        reference="lesson.ipynb - Summary",
    )
)

QUIZ.append(
    quiz(
        question="Why must a motor-command retry be bounded?",
        choices=[
            "An unbounded retry can hold the robot in a state it cannot escape.",
            "Python forbids loops that never terminate.",
            "Each retry allocates memory that is never released.",
            "Retries drain the battery faster than the drive does.",
        ],
        answer=0,
        kind="robotics",
        explanation=(
            "A retry that never gives up means the robot never proceeds and never "
            "reports failure, so a supervisor sees a live process and a stuck robot. The "
            "bound turns that into a reportable failure."
        ),
        reference="solution.ipynb - Solution 11",
    )
)

QUIZ.append(
    quiz(
        question="Which reports both whether any reading exceeded a limit and which one?",
        choices=[
            "`max(readings) > limit`",
            "A for loop returning the first offending value together with a found flag.",
            "`any(r > limit for r in readings)`",
            "`sum(readings) > limit`",
        ],
        answer=1,
        kind="implementation_choice",
        explanation=(
            "The task asks for two pieces of information, so the answer must carry both. "
            "any() and max() reduce to a single bool, and a sum is not a limit check at "
            "all."
        ),
        reference="exercises.ipynb - Exercise 5",
    )
)

RESEARCH = {
    "question": (
        "How much faster is direct iteration over a list than the equivalent manual "
        "index loop?"
    ),
    "hypothesis": (
        "The index loop is measurably slower at the same asymptotics, because it "
        "performs an extra length check and lookup on every pass."
    ),
    "experiment": [
        STEPS(
            [
                "Build a list of one million floats.",
                "Time a for loop that sums it directly.",
                "Time a while loop that sums it through an index.",
                "Run each ten times and record every raw measurement.",
            ]
        ),
    ],
    "data": [
        CODE_CELL(
            "# Record your raw timings - one row per variant per run.\n"
            "# Copy real values from your actual runs; do not invent them.\n"
            "#\n"
            "# | variant | run | seconds |"
        ),
    ],
    "analysis": [
        MD(
            "Compare the distributions rather than the means, and report the ratio. "
            "The interesting question is whether the difference survives the run-to-run "
            "variation, not whether it is visible in one run."
        ),
    ],
    "result": [
        MD(
            "State the observed ratio and whether the hypothesis held. If the "
            "difference falls inside the noise on your machine, report that honestly."
        ),
    ],
    "interpretation": [
        MD(
            "Explain why CPython's list iteration is specialised: the interpreter holds "
            "a direct reference to the list rather than calling a method per element. "
            "Name at least two threats to validity, including CPU frequency scaling."
        ),
    ],
    "conclusion": [
        MD(
            "Give your verdict and state whether you would ever write the index form, "
            "naming the one case where it is still correct."
        ),
    ],
    "extensions": [
        "Compare both against sum() and against a numpy sum.",
        "Repeat on a much larger list to see whether the ratio grows.",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Bounded Telemetry Poller",
    "context": (
        "During underground inspection the cart samples three channels every cycle. A "
        "sensor occasionally drops a frame, so the read is retried - but the retry must "
        "never hold the cart in place."
    ),
    "mission": (
        "Implement `poll_channels(robot, channels, attempts)` that reads each channel "
        "with a bounded retry and reports which channels failed."
    ),
    "requirements": [
        "Read each channel, retrying on SensorError up to `attempts` times.",
        "Return a dict with `readings` and `failed` channel names.",
        "Record the attempt count actually used for each channel.",
        "Report an unknown channel as failed rather than raising.",
    ],
    "constraints": [
        "Every loop must be bounded; no unbounded while loops.",
        "No hardware required; use `shared/robo_x_sim`.",
        "Complete well inside the 10 ms control budget per cycle.",
    ],
    "interface": "def poll_channels(robot, channels=None, attempts: int = 3) -> dict:",
    "success_criteria": [
        "A healthy robot returns a reading for every channel and an empty failed list.",
        "After inject_sensor_fault the affected channel appears in failed.",
        "No channel is read more than `attempts` times.",
    ],
    "extension": (
        "Add exponential backoff between attempts and measure whether it changes the "
        "success rate, justifying the delay in your write-up."
    ),
}

MINI_PROJECT = {
    "title": "Mini-Project: Bounded Sensor Poller",
    "brief": (
        "Build a polling routine for a robot's sensor bus. It must retry a failing "
        "read a fixed number of times, report which channels failed, and never run away."
    ),
    "scenario": (
        "A delivery cart samples three channels every cycle. A sensor occasionally "
        "drops a frame, so the cart retries - but an unbounded retry would leave the "
        "cart reporting a live process while the robot never moves."
    ),
    "rationale": (
        "Bounded iteration is the difference between a service that degrades and one "
        "that hangs, and the pattern reappears in every robotics module that follows."
    ),
    "requirements": [
        "Accept a list of channels and an attempt budget.",
        "Read each channel, retrying up to the budget on SensorError.",
        "Return a dict with `readings`, `failed` and the attempts actually used.",
        "Never raise for a failing or unknown channel.",
    ],
    "constraints": [
        "Standard library only.",
        "Every loop must be bounded; no unbounded while loops.",
    ],
    "deliverables": [
        "`poller.py` with the polling routine.",
        "`test_poller.py` with at least twelve assertions.",
        "A README section documenting the retry policy and its budget.",
    ],
    "steps": [
        "Define DEFAULT_ATTEMPTS as a module constant.",
        "Write sample_channel(robot, channel, attempts) returning (value, tries).",
        "Write poll(robot, channels) looping over channels and collecting failures.",
        "Test a healthy robot, then inject a fault with inject_sensor_fault().",
        "Test an unknown channel name and confirm it is reported, not raised.",
    ],
    "expected_behavior": (
        "A healthy robot returns a reading for every channel with no failures. After an "
        "injected fault the affected channel is listed in failed with a None reading."
    ),
    "acceptance": [
        "All assertions pass from a clean run.",
        "The attempt count never exceeds the budget for any channel.",
        "An unknown channel is reported rather than raised.",
        "No loop in the module can run more than the budget times.",
    ],
    "extensions": [
        "Add exponential backoff between attempts.",
        "Return a failure count summary across many poll cycles.",
        "Add a deadline so the whole poll respects a time budget.",
    ],
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Contrast sequence-driven and condition-driven iteration concretely.",
        "Make the iterator protocol explicit rather than treating for as magic.",
        "Install bounded iteration as a habit for every retry.",
    ],
    "misconceptions": [
        [
            "A for loop is a while loop with a built-in counter.",
            "It is driven by the sequence asking for elements, not by a counter.",
        ],
        [
            "An iterator can be used as many times as you like.",
            "It is single-use; a second pass yields nothing.",
        ],
        [
            "while True is fine as long as there is a break somewhere.",
            "A break that depends on external state is exactly what fails silently.",
        ],
        [
            "Iterating by index is more efficient.",
            "Direct iteration avoids a bounds check and an attribute lookup per pass.",
        ],
    ],
    "difficult_concepts": [
        "Seeing the exhaustion model rather than a magic stop condition.",
        "Accepting that for and while have fundamentally different termination logic.",
        "Writing a custom iterator and reasoning about when it is drained.",
    ],
    "demonstrations": [
        "Sum the same list twice, then sum an iterator of it twice, and compare.",
        "Run a while loop whose body forgets to change the condition, and interrupt it.",
        "Build a tiny iterator and show that list() consumes it permanently.",
    ],
    "discussion": [
        "What should a supervisor see when a retry loop exhausts its budget?",
        "When is a while loop genuinely better than a for loop?",
    ],
    "student_errors": [
        [
            "The program hangs with no output",
            "A while loop whose body never changes the condition",
            "Add the increment, or use a bounded for loop",
        ],
        [
            "The second pass returns nothing",
            "An iterator was reused after exhaustion",
            "Materialise the list, or call iter() again on the source",
        ],
        [
            "An off-by-one drops the last waypoint",
            "The loop skipped the final element with a manual index bound",
            "Iterate the sequence, or slice correctly",
        ],
    ],
    "pacing": (
        "90 minutes of lesson with the iterator demonstration, then 2 hours of "
        "exercises. Give real time to writing a custom iterator; it is the first time "
        "students define a protocol rather than use one."
    ),
    "extensions": [
        "Ask students to implement a reverse iterator and compare it with reversed().",
        "Have them measure the index loop against direct iteration and explain the gap.",
    ],
    "assessment": (
        "Grade against rubric.md. Exercises 8 to 10 carry the signal: they require "
        "bounded early exit, a bounded retry and a real API call from a loop."
    ),
    "support": (
        "Provide the Countdown class from the lesson and ask students to change the "
        "stop condition, so they see exhaustion rather than a magic number."
    ),
    "extension_fast": (
        "Ask for a design note on how a telemetry consumer should handle an infinite "
        "stream without buffering it all.",
    ),
}

RUBRIC = {
    "artifacts": [
        ["exercises.ipynb", "40%", "All 10 exercises implemented and edge-cased."],
        ["mini_project.ipynb", "25%", "poller.py plus its test suite."],
        ["robotics_challenge.ipynb", "25%", "Bounded poller degrades safely."],
        ["research.ipynb", "10%", "Real measurements with a defensible conclusion."],
    ],
    "criteria": [
        ["Correctness", "30", "Accumulation, early exit and boundaries all behave as specified."],
        ["Bounded iteration", "25", "No loop can exceed its budget, and the reason is stated."],
        ["Code quality", "25", "PEP 8 naming, docstrings, small focused functions."],
        ["Reasoning", "20", "Cost and termination claims explained in writing."],
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
            "Every exercise implemented, an injected sensor fault is handled inside the "
            "retry budget, and the budget itself is proven by a test.",
        ],
        [
            "Merit",
            "Most exercises correct; the poller works but reuses an exhausted iterator, "
            "which is untested.",
        ],
        [
            "Pass",
            "Core requirements met, but a while loop is used for the retry with no bound, "
            "so the failure mode is a hang rather than a report.",
        ],
        [
            "Fail",
            "An unbounded loop, or a route follower that drops the final waypoint.",
        ],
    ],
}

TOPIC = topic(
    topic_id="2.2",
    title="for Loops and while Loops",
    module=2,
    module_title="Control Flow and Loops",
    directory="02_for_and_while_loops",
    summary=(
        "Iteration as a protocol: a for loop asks the sequence for the next element, a "
        "while loop asks a question - and only one of the two can stop on its own."
    ),
    why_it_matters=(
        "Telemetry, routes and retry policies are all loops, and the difference "
        "between a loop that stops and a loop that hangs is the difference between a "
        "robot that degrades and a robot that is stuck holding a live process. Choosing "
        "the right loop is a safety decision, not a style preference."
    ),
    objectives=[
        "Explain why a for loop cannot run away over a finite sequence.",
        "Give every while loop a bound, a break, or visible progress.",
        "Implement __iter__ and __next__ to make an object loopable.",
        "Explain why an exhausted iterator stays exhausted.",
        "Choose direct iteration over index iteration and say why.",
        "Express a retry policy as a bounded for loop.",
    ],
    prerequisites=[
        "Topic 2.1 Conditional Statements",
        "Topic 1.8 Writing and Running Your First Scripts",
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
    robo_x_milestone="M2",
    robo_x_package="robo_x.core",
)
