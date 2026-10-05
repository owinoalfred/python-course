"""Topic 2.4 - Nested Loops and Common Patterns.

Hand-authored to the Course Content Standard. The spine: a nested loop multiplies
the work, and almost every bug in one is a boundary error rather than a logic error.
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
        "A loop inside a loop runs its body once for every pass of the outer loop. That "
        "single fact explains both the usefulness and the danger: nested loops are how "
        "you visit every cell of a grid or every pair of items, and they are also how a "
        "program that should do one hundred operations quietly does ten thousand."
    ),
    CODE_CELL(
        "grid = ((0, 1, 0),\n"
        "        (0, 0, 1),\n"
        "        (1, 0, 0))\n"
        "\n"
        "rows = cols = 0\n"
        "for row in grid:\n"
        "    rows += 1\n"
        "    for cell in row:\n"
        "        cols += 1\n"
        "print(f'outer ran {rows} times, inner ran {cols} times')"
    ),
    MD(
        "The cost multiplies. An outer loop of *n* iterations containing an inner loop "
        "of *m* iterations performs *n × m* steps. With three passes each that is nine "
        "steps; add a third level and it becomes a cubic cost, which is how a routine "
        "that handles a small table becomes unusable on a full sensor grid."
    ),
    CODE_CELL(
        "def steps_two_levels(n, m) -> int:\n"
        "    steps = 0\n"
        "    for _ in range(n):\n"
        "        for _ in range(m):\n"
        "            steps += 1\n"
        "    return steps\n"
        "\n"
        "\n"
        "def steps_three_levels(n, m, k) -> int:\n"
        "    steps = 0\n"
        "    for _ in range(n):\n"
        "        for _ in range(m):\n"
        "            for _ in range(k):\n"
        "                steps += 1\n"
        "    return steps\n"
        "\n"
        "\n"
        "print('two levels 100:', steps_two_levels(100, 100))\n"
        "print('three levels 20:', steps_three_levels(20, 20, 20))"
    ),
    NOTE(
        "Early exit cuts the work",
        "A `break` in the inner loop does not reduce the outer count, but a `return` "
        "from inside a nested search removes the remaining outer iterations entirely - "
        "which is why search helpers return rather than set a flag.",
    ),
]

LESSON["formal_theory"] = [
    MD(
        "Nested iteration composes. The outer loop produces an element, and the inner "
        "loop produces one element for each of *its* sequence - so the body of the inner "
        "loop runs once per ordered **pair**. That is the right way to think about it: "
        "the inner loop restarts from the beginning on every pass of the outer one."
    ),
    EQUATION(
        "for a in A:  for b in B:  ...   ==   visit every (a, b) pair, |A| * |B| of them"
    ),
    MD(
        "The classical patterns that matter here each reduce this to a different shape. "
        "Diagonal iteration adds an offset so the two indices move together. Sliding "
        "windows slice a fixed-size window along a sequence. A running comparison "
        "carries one value from the previous pass. Recognising which pattern a problem "
        "wants is the real skill - it is what separates a cubic loop from a linear pass."
    ),
    CODE_CELL(
        "def diagonal(size: int) -> list[tuple]:\n"
        "    return [(r, c) for r in range(size) for c in range(r, size)]\n"
        "\n"
        "\n"
        "def window(values, size: int) -> list[tuple]:\n"
        "    return [\n"
        "        tuple(values[i:i + size])\n"
        "        for i in range(len(values) - size + 1)\n"
        "    ]\n"
        "\n"
        "\n"
        "print('diagonal(3):', diagonal(3))\n"
        "print('window(4, 2):', window((1, 2, 3, 4), 2))"
    ),
    TABLE(
        ["Pattern", "Shape", "Cost"],
        [
            ["Full nested scan", "every (a, b) pair", "O(n * m)"],
            ["Early-exit search", "until the first match", "O(n * m) worst, often far less"],
            ["Sliding window", "each window of size k", "O(n)"],
            ["Carried value", "one value from the previous pass", "O(n)"],
        ],
    ),
]

LESSON["syntax"] = [
    MD(
        "The canonical nested scan enumerates both levels, so the reader can see the "
        "coordinates rather than inferring them."
    ),
    CODE_CELL(
        "GRID = ((0, 1, 0),\n"
        "        (0, 0, 1),\n"
        "        (1, 0, 0))\n"
        "\n"
        "for row_index, row in enumerate(GRID):\n"
        "    for col_index, cell in enumerate(row):\n"
        "        if cell:\n"
        "            print(f'occupied at ({row_index}, {col_index})')"
    ),
    MD("The anti-pattern - a hard-coded bound that quietly breaks on short rows:"),
    CODE(
        "grid = ((0, 1),\n"
        "        (0, 0, 1))     # ragged: the second row is longer\n"
        "for row_index in range(3):\n"
        "    for col_index in range(3):   # IndexError on a smaller grid\n"
        "        print(grid[row_index][col_index])\n"
        "\n"
        "for row_index, row in enumerate(grid):\n"
        "    for col_index, cell in enumerate(row):   # safe for any shape\n"
        "        print(row_index, col_index, cell)",
        lang="text",
    ),
    WARN(
        "Never index a nested loop by a hard-coded bound",
        "Iterate the rows themselves. A hard-coded column count raises IndexError on a "
        "smaller grid and silently ignores extra cells on a larger one.",
    ),
]

LESSON["basic_examples"] = [
    MD("**Example 1 - counting with a nested loop.**"),
    CODE_CELL(
        "pairs = ('a', 'b')\n"
        "count = 0\n"
        "for first in pairs:\n"
        "    for second in pairs:\n"
        "        count += 1\n"
        "print(f'{len(pairs)} * {len(pairs)} = {count} pairs')"
    ),
    MD("**Example 2 - a linear alternative to a nested sum.**"),
    CODE_CELL(
        "values = [1, 2, 3, 4]\n"
        "\n"
        "pairs_sum = 0\n"
        "for a in values:\n"
        "    for b in values:\n"
        "        pairs_sum += a * b\n"
        "\n"
        "flat_sum = sum(values)\n"
        "print('nested :', pairs_sum)\n"
        "print('flat   :', flat_sum * flat_sum)\n"
        "print('equal  :', pairs_sum == flat_sum * flat_sum)"
    ),
]

LESSON["intermediate_examples"] = [
    MD(
        "Scanning an occupancy grid is the canonical nested search. The `return` on the "
        "first hit is what keeps it from walking the whole grid once a match is found."
    ),
    CODE_CELL(
        "GRID = ((0, 0, 1),\n"
        "        (0, 1, 0),\n"
        "        (0, 0, 0))\n"
        "\n"
        "\n"
        "def first_obstacle(grid):\n"
        "    for row_index, row in enumerate(grid):\n"
        "        for col_index, cell in enumerate(row):\n"
        "            if cell:\n"
        "                return row_index, col_index\n"
        "    return None\n"
        "\n"
        "\n"
        "print('first obstacle:', first_obstacle(GRID))\n"
        "print('clear grid    :', first_obstacle(((0, 0), (0, 0))))"
    ),
]

LESSON["advanced_examples"] = [
    MD(
        "Some nested-loop problems are not really nested. A pairwise sum over a list is "
        "the square of the sum, and a sliding window is one pass with a slice. Knowing "
        "which is which turns an O(n^2) routine into an O(n) one."
    ),
    CODE_CELL(
        "values = (1, 2, 3, 4)\n"
        "\n"
        "\n"
        "def every_pair_sum(values):\n"
        "    \"\"\"O(n^2): the direct translation of 'for each pair'.\"\"\"\n"
        "    total = 0\n"
        "    for a in values:\n"
        "        for b in values:\n"
        "            total += a * b\n"
        "    return total\n"
        "\n"
        "\n"
        "def every_pair_sum_fast(values):\n"
        "    \"\"\"O(n): the same number, derived rather than enumerated.\"\"\"\n"
        "    return sum(values) ** 2\n"
        "\n"
        "\n"
        "print('direct:', every_pair_sum(values))\n"
        "print('fast  :', every_pair_sum_fast(values))"
    ),
    MD(
        "The two are equal because expanding `(a1 + a2 + ...)^2` produces exactly the "
        "cross terms the double loop accumulates. Recognising that identity is worth "
        "more than any micro-optimisation."
    ),
]

LESSON["code_walkthrough"] = [
    MD(
        "Below is a coverage checker for a survey grid. It walks every cell, applies a "
        "predicate, and reports what was and was not covered - with an explicit guard "
        "so a ragged grid cannot raise."
    ),
    CODE_CELL(
        "\"\"\"coverage.py - check a survey grid against a minimum sampling rule.\"\"\"\n"
        "from __future__ import annotations\n"
        "\n"
        "MIN_COVERAGE = 0.5\n"
        "\n"
        "\n"
        "def check_coverage(grid, is_covered, min_coverage=MIN_COVERAGE) -> dict:\n"
        "    \"\"\"Return coverage statistics for a grid of any rectangular shape.\n"
        "\n"
        "    Iterating the rows rather than a fixed width means a ragged or\n"
        "    empty grid is measured as it actually is, not assumed away.\n"
        "    \"\"\"\n"
        "    total = 0\n"
        "    covered = 0\n"
        "    uncovered: list[tuple] = []\n"
        "    for row_index, row in enumerate(grid):\n"
        "        for col_index, cell in enumerate(row):\n"
        "            total += 1\n"
        "            if is_covered(cell):\n"
        "                covered += 1\n"
        "            else:\n"
        "                uncovered.append((row_index, col_index))\n"
        "    ratio = (covered / total) if total else 0.0\n"
        "    return {\n"
        "        'total': total,\n"
        "        'covered': covered,\n"
        "        'ratio': round(ratio, 3),\n"
        "        'ok': ratio >= min_coverage,\n"
        "        'uncovered': uncovered,\n"
        "    }"
    ),
    MD(
        "The `total` counter is what makes the empty-grid case honest: dividing by a "
        "zero cell count would raise, and silently returning 1.0 would claim a full "
        "survey of nothing. Reporting `uncovered` coordinates means the caller learns "
        "*where* to send the robot, not merely that the grid failed."
    ),
]

LESSON["line_by_line"] = [
    STEPS(
        [
            "MIN_COVERAGE is a module constant so the survey policy is visible above the "
            "loop rather than buried in a comparison.",
            "Iterating each row rather than a fixed width means the function works for "
            "ragged and empty grids without a guard at every level.",
            "total is incremented before any classification, so the denominator counts "
            "every cell that exists.",
            "The else-style branch collects uncovered coordinates rather than just "
            "counting them, which tells the caller where to send the robot.",
            "The conditional expression handles the empty grid explicitly instead of "
            "letting a division by zero escape.",
            "ok is derived from the ratio, so the verdict cannot disagree with the "
            "measurement it came from.",
        ]
    ),
]

LESSON["common_mistakes"] = [
    MD("**Mistake 1 - a hard-coded inner bound.**"),
    CODE(
        "grid = ((0, 1),\n"
        "        (0, 0, 1))          # ragged\n"
        "for r in range(3):\n"
        "    for c in range(3):\n"
        "        print(grid[r][c])      # IndexError on a short row\n"
        "\n"
        "for r, row in enumerate(grid):\n"
        "    for c, cell in enumerate(row):\n"
        "        print(r, c, cell)     # safe for any shape",
        lang="text",
    ),
    MD("**Mistake 2 - assuming the inner loop restarts the outer one.**"),
    CODE(
        "total = 0\n"
        "for a in (1, 2):\n"
        "    for b in (1, 2, 3):\n"
        "        total += 1\n"
        "print(total)          # 6, not 3: the inner loop restarts each pass",
        lang="text",
    ),
    MD("**Mistake 3 - an off-by-one that drops the last row or column.**"),
    CODE(
        "for r in range(len(grid) - 1):        # drops the final row\n"
        "    for c in range(len(grid[0]) - 1): # drops the final column\n"
        "        ...\n"
        "\n"
        "for r, row in enumerate(grid):        # visits every cell\n"
        "    for c, cell in enumerate(row):\n"
        "        ...",
        lang="text",
    ),
    MD("**Mistake 4 - a third level where a second would do.**"),
    CODE(
        "for a in A:\n"
        "    for b in B:\n"
        "        for c in C:      # O(n^3) where O(n^2) suffices\n"
        "            ...",
        lang="text",
    ),
]

LESSON["debugging_techniques"] = [
    MD(
        "For a nested loop, print the pair on each pass. Seeing every (row, col) the "
        "body visits turns a suspected off-by-one into a visible list."
    ),
    CODE_CELL(
        "grid = ((0, 1, 0), (0, 0))\n"
        "visits = []\n"
        "for r, row in enumerate(grid):\n"
        "    for c, cell in enumerate(row):\n"
        "        visits.append((r, c))\n"
        "print('visited:', visits)\n"
        "print('expected:', [(r, c) for r in range(2) for c in (2, 3)])"
    ),
    MD(
        "For a suspected cost problem, count the passes rather than timing them. If the "
        "pass count is far larger than the data would suggest, the bound is wrong before "
        "the performance is."
    ),
    CODE_CELL(
        "def count_steps_two(n, m) -> int:\n"
        "    steps = 0\n"
        "    for _ in range(n):\n"
        "        for _ in range(m):\n"
        "            steps += 1\n"
        "    return steps\n"
        "\n"
        "\n"
        "for n in (10, 100, 1000):\n"
        "    steps = count_steps_two(n, n)\n"
        "    print(f'n={n:<5} steps={steps:<9} ratio_vs_n={steps / n:.0f}')"
    ),
    NOTE(
        "Compare against the derived value",
        "For an n by n grid the step count should be exactly n squared. Any other number "
        "means the loop is not doing what the problem statement asked.",
    ),
]

LESSON["best_practices"] = [
    BULLETS(
        [
            "Iterate the rows themselves; never hard-code an inner bound.",
            "Use enumerate at both levels so coordinates are visible.",
            "Return from a nested search rather than setting a flag.",
            "Check whether a nested loop is really needed before writing one.",
            "Derive a closed form when the pair sum or count is algebraically known.",
            "Test with a ragged grid as well as a rectangular one.",
            "Count steps first, then time them, when cost is in doubt.",
            "Prefer a sliding window over repeated slicing inside a loop.",
        ]
    ),
]

LESSON["performance_considerations"] = [
    MD(
        "Nested loops multiply cost, and the multiplier is easy to underestimate. Three "
        "levels of a thousand elements each is a billion steps - not a slow program, an "
        "unfinished one. Before writing the second loop, ask what the body actually has "
        "to do, and whether the same result is available from a single pass."
    ),
    MD(
        "Two transformations remove most nested loops in practice. A sliding window "
        "replaces a nested scan of every k-sized window with one pass and a slice per "
        "position, turning O(n*k) into O(n). A closed form replaces enumeration with "
        "algebra: the sum of all pairwise products is the square of the sum, and a count "
        "of pairs above a threshold can often be computed from sorted data in one pass."
    ),
    TIP(
        "Measure the step count, not the clock",
        "Instrumenting a counter tells you the shape of the cost immediately and without "
        "the noise of a real machine. If the count is right, the time usually is too.",
    ),
]

LESSON["pythonic_approaches"] = [
    MD("A nested pair scan against its linear equivalent."),
    CODE_CELL(
        "values = (1, 2, 3, 4)\n"
        "\n"
        "# before: enumerate every ordered pair\n"
        "pairs = [(a, b) for a in values for b in values]\n"
        "print('pair count:', len(pairs))\n"
        "\n"
        "# after: the count is derived, not enumerated\n"
        "print('derived   :', len(values) ** 2)\n"
        "\n"
        "# and the product sum is the square of the total\n"
        "print('sum of products:', sum(values) ** 2)"
    ),
]

LESSON["robotics_connection"] = [
    MD(
        "A coverage grid is the shape almost every mapping task takes: nested loops "
        "over rows and cells, with an early exit when a cell already answers the "
        "question."
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
        "GRID = ((0, 0, 1), (0, 1, 0), (0, 0, 0))\n"
        "visited = 0\n"
        "for row_index, row in enumerate(GRID):\n"
        "    for col_index, cell in enumerate(row):\n"
        "        visited += 1\n"
        "        if cell:\n"
        "            print(f'obstacle at ({row_index}, {col_index})')\n"
        "print(f'visited {visited} cells, battery {state[\"battery_pct\"]:.1f}%')"
    ),
]

LESSON["engineering_example"] = [
    MD(
        "A nested neighbour scan returning the strongest match rather than every match - "
        "the common shape of a local planner step."
    ),
    CODE_CELL(
        "def strongest_neighbour(grid, row, col, default=None):\n"
        "    \"\"\"Return the (dr, dc) step toward the largest neighbouring cell.\"\"\"\n"
        "    best = None\n"
        "    best_value = default\n"
        "    for dr in (-1, 0, 1):\n"
        "        for dc in (-1, 0, 1):\n"
        "            if dr == 0 and dc == 0:\n"
        "                continue\n"
        "            r, c = row + dr, col + dc\n"
        "            if not (0 <= r < len(grid) and 0 <= c < len(grid[r])):\n"
        "                continue\n"
        "            if grid[r][c] > best_value:\n"
        "                best_value = grid[r][c]\n"
        "                best = (dr, dc)\n"
        "    return best"
    ),
]

LESSON["guided_practice"] = [
    STEPS(
        [
            "Count the iterations of a 3 by 4 nested loop and confirm it is 12.",
            "Write a nested scan that prints every coordinate of a ragged grid.",
            "Write a sliding window of size 2 over a five-element list.",
            "Write a nested search returning the first (row, col) matching a value.",
        ]
    ),
    CODE_CELL(
        "grid = ((0, 1, 0), (0, 0))\n"
        "\n"
        "count = 0\n"
        "for r, row in enumerate(grid):\n"
        "    for c, cell in enumerate(row):\n"
        "        count += 1\n"
        "print('cells visited:', count)\n"
        "\n"
        "values = (1, 2, 3, 4, 5)\n"
        "for start in range(len(values) - 1):\n"
        "    print('window:', values[start:start + 2])\n"
        "\n"
        "def find(grid, target):\n"
        "    for r, row in enumerate(grid):\n"
        "        for c, cell in enumerate(row):\n"
        "            if cell == target:\n"
        "                return (r, c)\n"
        "    return None\n"
        "\n"
        "print('find 1 ->', find(grid, 1))\n"
        "print('find 9 ->', find(grid, 9))"
    ),
]

LESSON["mental_model"] = [
    MD(
        "**Mental model: a clock, not a matrix.** The outer loop is the slow hand and the "
        "inner loop is the fast one. The fast hand sweeps all the way round once for "
        "every tick of the slow hand, and it never remembers where it was - it always "
        "restarts from the beginning."
    ),
    TABLE(
        ["", "Outer loop", "Inner loop"],
        [
            ["Restarts", "once", "on every outer pass"],
            ["Cost", "n iterations", "m per outer pass, so n*m total"],
            ["Knows its index", "only if enumerated", "only if enumerated"],
            ["Best replaced by", "a single pass", "a slice or a derived value"],
        ],
    ),
]

TERMS = [
    ["Nested loop", "A loop inside another loop."],
    ["Iteration count", "The product of the loop lengths."],
    ["Ragged grid", "Rows of differing lengths, which break hard-coded bounds."],
    ["enumerate", "Iterate a sequence while also yielding its index."],
    ["Sliding window", "Each window of fixed size along a sequence, in one pass."],
    ["Off-by-one", "A bound error that visits one element too few or too many."],
    ["Closed form", "An algebraic expression replacing an enumeration."],
    ["Early exit", "Returning from inside a nested search to stop the outer loop too."],
    ["Cartesian product", "Every ordered pair drawn from two sequences."],
    ["Pairwise sum", "The sum of all products of pairs, equal to the square of the sum."],
]

EXERCISES = []

EXERCISES.append(
    exercise(
        number=1,
        title="Count the cells of a grid",
        difficulty="MEDIUM",
        learning_objectives=["Use a nested loop.", "Count without assuming shape."],
        concepts_tested=["nested loops", "counting", "ragged data"],
        problem_statement=(
            "Write `count_cells(grid)` counting every cell with a nested loop that "
            "works for a ragged grid of differing row lengths."
        ),
        requirements=["Iterate each row, never a fixed width.", "Return an integer."],
        constraints=["Do not use len() on the grid."],
        input_description="A sequence of rows.",
        expected_output="An integer.",
        example_input="count_cells(((0, 1), (0,), (1, 1, 1)))",
        example_output="6",
        edge_cases=["An empty grid returns 0.", "A grid of empty rows returns 0."],
        hints=["Nested loop over rows, then over each row's own values."],
        success_criteria=["The example returns 6.", "An empty grid returns 0."],
        optional_extension="Also return the number of rows.",
    )
)

EXERCISES.append(
    exercise(
        number=2,
        title="Sum every cell with a nested loop",
        difficulty="MEDIUM",
        learning_objectives=["Accumulate across two levels.", "Handle ragged input."],
        concepts_tested=["nested loops", "accumulators"],
        problem_statement=(
            "Write `sum_grid(grid)` summing every numeric cell with an explicit nested "
            "loop, ignoring values that are not numbers."
        ),
        requirements=["Two nested loops.", "Skip non-numeric cells."],
        constraints=["Do not use a comprehension or flatten()."],
        input_description="A sequence of rows of arbitrary values.",
        expected_output="A number.",
        example_input="sum_grid(((1, 2), (3, 'x'), ()))",
        example_output="6",
        edge_cases=["An empty grid returns 0.", "A grid of only junk returns 0."],
        hints=["Accumulate inside the inner loop."],
        success_criteria=["The example returns 6.", "An empty grid returns 0."],
        optional_extension="Return a per-row sum list as well.",
    )
)

EXERCISES.append(
    exercise(
        number=3,
        title="Enumerate every coordinate",
        difficulty="MEDIUM",
        learning_objectives=["Yield coordinates from a nested loop.", "Use enumerate twice."],
        concepts_tested=["enumerate", "generators", "nested loops"],
        problem_statement=(
            "Write `coordinates(grid)` returning a list of `(row, col)` pairs for "
            "every cell, produced by a generator that uses nested loops."
        ),
        requirements=["Use nested loops with enumerate.", "Handle a ragged grid."],
        constraints=["Yield rather than append, then materialise with list()."],
        input_description="A sequence of rows.",
        expected_output="A list of tuples.",
        example_input="coordinates(((0, 1), (2,)))",
        example_output="[(0, 0), (0, 1), (1, 0)]",
        edge_cases=["An empty grid gives an empty list.", "A row of length 0 contributes nothing."],
        hints=["A generator with two nested yields produces the pairs lazily."],
        success_criteria=["The example matches exactly.", "An empty grid gives []."],
        optional_extension="Add a value filter argument.",
    )
)

EXERCISES.append(
    exercise(
        number=4,
        title="Sliding window of fixed size",
        difficulty="MEDIUM",
        learning_objectives=["Use a sliding window.", "Replace a nested scan."],
        concepts_tested=["slicing", "range", "single pass"],
        problem_statement=(
            "Write `windows(values, size)` returning each window of `size` consecutive "
            "items as a tuple, in a single pass rather than a nested scan."
        ),
        requirements=["One pass over the values.", "Raise ValueError for size below 1."],
        constraints=["No nested loops."],
        input_description="A sequence and a positive size.",
        expected_output="A list of tuples.",
        example_input="windows((1, 2, 3, 4), 2)",
        example_output="[(1, 2), (2, 3), (3, 4)]",
        edge_cases=["A size larger than the data gives an empty list.", "A size of 0 raises ValueError."],
        hints=["Step a start index by one and slice a window each time."],
        success_criteria=["The example matches exactly.", "No nested loops appear."],
        optional_extension="Compute the window sum in the same pass.",
    )
)

EXERCISES.append(
    exercise(
        number=5,
        title="Derive the pairwise product sum",
        difficulty="MEDIUM",
        learning_objectives=["Recognise a closed form.", "Replace a nested loop."],
        concepts_tested=["algebra", "nested loops", "optimisation"],
        problem_statement=(
            "Write `pair_product_sum(values)` returning the sum of `a * b` over every "
            "ordered pair, computed in O(n) rather than with a nested loop. Verify it "
            "against a naive implementation in your tests."
        ),
        requirements=["Use the identity that the sum of all pairwise products is the "
                      "square of the total."],
        constraints=["No nested loops in the implementation."],
        input_description="A sequence of numbers.",
        expected_output="A number.",
        example_input="pair_product_sum((1, 2, 3))",
        example_output="36",
        edge_cases=["An empty sequence returns 0.", "Negative values still satisfy the identity."],
        hints=["The identity is (sum of all values) squared."],
        success_criteria=["(1, 2, 3) returns 36.", "An empty sequence returns 0."],
        optional_extension="Return the naive result as well for comparison.",
    )
)

EXERCISES.append(
    exercise(
        number=6,
        title="Find the first occupied cell",
        difficulty="HARD",
        learning_objectives=["Search a grid and exit early.", "Return coordinates."],
        concepts_tested=["nested loops", "return", "early exit"],
        problem_statement=(
            "Write `first_occupied(grid)` returning the `(row, col)` of the first truthy "
            "cell, or None, returning from inside the inner loop."
        ),
        requirements=["Use nested loops with enumerate.", "Return on the first match."],
        constraints=["No flag variable.", "Never raise for a ragged grid."],
        input_description="A sequence of rows.",
        expected_output="A tuple, or None.",
        example_input="first_occupied(((0, 0), (0, 1)))",
        example_output="(1, 1)",
        edge_cases=["An empty grid returns None.", "A cell of 0 is not occupied."],
        hints=["Return the pair as soon as the cell is truthy."],
        success_criteria=["The example returns (1, 1).", "An empty grid returns None."],
        optional_extension="Return every occupied coordinate instead.",
    )
)

EXERCISES.append(
    exercise(
        number=7,
        title="Count row and column totals",
        difficulty="HARD",
        learning_objectives=["Accumulate per row and per column.", "Handle ragged input."],
        concepts_tested=["nested loops", "aggregation", "ragged data"],
        problem_statement=(
            "Write `grid_totals(grid)` returning a dict with `rows`, `cols` and `sum`, "
            "where `cols` is the length of the longest row."
        ),
        requirements=["Use a nested loop to sum.", "Track the longest row."],
        constraints=["Do not assume rows have equal length."],
        input_description="A sequence of rows of numbers.",
        expected_output="A dict with three keys.",
        example_input="grid_totals(((1, 2), (3,)))",
        example_output="{'rows': 2, 'cols': 2, 'sum': 6}",
        edge_cases=["An empty grid gives zeros.", "A grid of empty rows gives cols 0."],
        hints=["Track the maximum row length as you go."],
        success_criteria=["The example gives the three expected values.", "An empty grid gives zeros."],
        optional_extension="Return per-row sums as a list.",
    )
)

EXERCISES.append(
    exercise(
        number=8,
        title="Find the strongest neighbour",
        difficulty="HARD",
        learning_objectives=["Scan a neighbourhood.", "Respect boundaries."],
        concepts_tested=["nested loops", "bounds checks", "max selection"],
        problem_statement=(
            "Write `strongest_neighbour(grid, row, col)` returning the `(dr, dc)` step "
            "toward the largest in-bounds neighbour, or None. Skip the centre cell."
        ),
        requirements=["Check bounds before indexing.", "Never index outside the grid."],
        constraints=["Skip the (0, 0) offset."],
        input_description="A grid, and the row and column to inspect.",
        expected_output="A tuple, or None.",
        example_input="strongest_neighbour(((1, 9), (0, 0)), 0, 0)",
        example_output="(0, 1)",
        edge_cases=["A cell with no in-bounds neighbours returns None.", "Ties return the first found."],
        hints=["Loop over the -1, 0, 1 offsets and test each coordinate."],
        success_criteria=["The example returns (0, 1).", "A corner with no neighbours returns None."],
        optional_extension="Return the neighbour value as well as the step.",
    )
)

EXERCISES.append(
    exercise(
        number=9,
        title="Check survey coverage against a threshold",
        difficulty="HARD",
        learning_objectives=["Accumulate a ratio.", "Handle the empty case."],
        concepts_tested=["nested loops", "division", "validation"],
        problem_statement=(
            "Write `coverage(grid, is_covered, min_ratio=0.5)` returning a dict with "
            "`total`, `covered`, `ratio` and `ok`. An empty grid must give ratio 0.0 "
            "rather than raising."
        ),
        requirements=["Use a nested loop.", "Never divide by zero."],
        constraints=["is_covered is a callable taking one cell."],
        input_description="A grid, a predicate and a threshold.",
        expected_output="A dict with four keys.",
        example_input="coverage(((1, 0), (1, 0)), lambda c: c == 1)",
        example_output="{'total': 4, 'covered': 2, 'ratio': 0.5, 'ok': True}",
        edge_cases=["An empty grid gives ratio 0.0 and ok False.", "A ratio of exactly the threshold passes."],
        hints=["Count total and covered, then divide conditionally."],
        success_criteria=["The example reports ratio 0.5.", "An empty grid gives 0.0."],
        optional_extension="Return the uncovered coordinates.",
    )
)

EXERCISES.append(
    exercise(
        number=10,
        title="Plan a route across a terrain grid",
        difficulty="HARD",
        learning_objectives=["Drive a grid with a simulator.", "Combine search and safety."],
        concepts_tested=["nested loops", "simulator API", "planning"],
        problem_statement=(
            "Write `plan_cells(grid, robot, min_battery_pct=20.0)` returning the "
            "passable coordinates in row-major order, where a cell is passable when it "
            "is 0 and the battery is above the limit."
        ),
        requirements=["Use a nested loop over the grid.", "Read the battery once from status()."],
        constraints=["Never index outside the grid.", "No flag variable."],
        input_description="A terrain grid and a SimulatedRobot.",
        expected_output="A list of coordinate tuples.",
        example_input="plan_cells(((0, 1), (0, 0)), robot)",
        example_output="[(0, 0), (1, 0), (1, 1)]",
        edge_cases=["An empty grid gives an empty list.", "A depleted robot gives an empty list."],
        hints=["Read the battery once, then scan with nested loops."],
        success_criteria=["The example lists the three passable cells.", "An empty grid gives []."],
        optional_extension="Return the count of blocked cells as well.",
    )
)

SOLUTIONS = []

SOLUTIONS.append(
    solution(
        number=1,
        code=(
            "def count_cells(grid) -> int:\n"
            "    total = 0\n"
            "    for row in grid:\n"
            "        for cell in row:\n"
            "            total += 1\n"
            "    return total"
        ),
        explanation=(
            "Iterating the rows themselves is what makes this correct for a ragged "
            "grid: the inner loop's length comes from the row in front of it, so no "
            "cell is missed and none is invented. A hard-coded width would count a "
            "short row incorrectly or raise on it."
        ),
        complexity="Time O(total cells); space O(1).",
        edge_cases="A grid of empty rows gives 0, because no inner iteration runs.",
        alternative_approaches="sum(len(row) for row in grid) is the same answer in one line.",
        testing="assert count_cells(((0, 1), (0,), (1, 1, 1))) == 6\nassert count_cells(()) == 0",
    )
)

SOLUTIONS.append(
    solution(
        number=2,
        code=(
            "def sum_grid(grid) -> float:\n"
            "    total = 0.0\n"
            "    for row in grid:\n"
            "        for cell in row:\n"
            "            if isinstance(cell, bool) or not isinstance(cell, (int, float)):\n"
            "                continue\n"
            "            total += cell\n"
            "    return total"
        ),
        explanation=(
            "The continue keeps the accumulation on one unindented line, which is the "
            "reason to prefer it over an else block here. Rejecting bool matters "
            "because True would otherwise contribute 1 to a physical total."
        ),
        complexity="Time O(total cells); space O(1).",
        edge_cases="A grid of only junk returns 0.0 rather than raising.",
        alternative_approaches="A nested comprehension is shorter but hides the skip rule.",
        testing="assert sum_grid(((1, 2), (3, 'x'), ())) == 6\nassert sum_grid(()) == 0.0",
    )
)

SOLUTIONS.append(
    solution(
        number=3,
        code=(
            "def coordinates(grid):\n"
            "    for row_index, row in enumerate(grid):\n"
            "        for col_index, cell in enumerate(row):\n"
            "            yield row_index, col_index"
        ),
        explanation=(
            "A generator function is itself an iterator, so the nested yields produce "
            "the pairs lazily and list() materialises them at the end. Using enumerate "
            "at both levels means the coordinates are computed rather than tracked in a "
            "counter."
        ),
        complexity="Time O(total cells); space O(1) before list() consumes it.",
        edge_cases="An empty grid yields nothing, so list() gives an empty list.",
        alternative_approaches="A nested comprehension is the eager equivalent.",
        testing="assert list(coordinates(((0, 1), (2,)))) == [(0, 0), (0, 1), (1, 0)]\nassert list(coordinates(())) == []",
    )
)

SOLUTIONS.append(
    solution(
        number=4,
        code=(
            "def windows(values, size: int) -> list[tuple]:\n"
            "    if not isinstance(size, int) or isinstance(size, bool) or size < 1:\n"
            "        raise ValueError(f'size must be a positive integer, got {size!r}')\n"
            "    return [\n"
            "        tuple(values[start:start + size])\n"
            "        for start in range(len(values) - size + 1)\n"
            "    ]"
        ),
        explanation=(
            "Stepping the start index by one and slicing a window gives every window "
            "in a single pass, where the nested version would re-scan the whole prefix "
            "for each start. The range bound of len - size + 1 is what makes a size "
            "larger than the data produce no windows rather than a short one."
        ),
        complexity="Time O(n * size) for the copies; space O(n * size).",
        edge_cases="A size equal to the length gives exactly one window.",
        alternative_approaches="collections.deque(maxlen=size) gives O(n) with a bounded buffer.",
        testing="assert windows((1, 2, 3, 4), 2) == [(1, 2), (2, 3), (3, 4)]\nassert windows((1, 2), 5) == []",
    )
)

SOLUTIONS.append(
    solution(
        number=5,
        code=(
            "def pair_product_sum(values):\n"
            "    total = sum(values)\n"
            "    return total * total\n"
            "\n"
            "\n"
            "def pair_product_sum_naive(values):\n"
            "    \"\"\"The O(n^2) reference, kept only for the tests.\"\"\"\n"
            "    total = 0\n"
            "    for a in values:\n"
            "        for b in values:\n"
            "            total += a * b\n"
            "    return total"
        ),
        explanation=(
            "Expanding the square of a sum produces exactly the cross terms the double "
            "loop accumulates, so the identity gives the same number in O(n). Keeping "
            "the naive version makes the equivalence testable rather than asserted."
        ),
        complexity="Time O(n) for the fast version, O(n^2) for the naive one.",
        edge_cases="An empty sequence sums to 0, so the square is 0.",
        alternative_approaches="math.fsum reduces float error when the values are large.",
        testing="assert pair_product_sum((1, 2, 3)) == 36\nassert pair_product_sum(()) == 0\nassert pair_product_sum((1, -2, 3)) == pair_product_sum_naive((1, -2, 3))",
    )
)

SOLUTIONS.append(
    solution(
        number=6,
        code=(
            "def first_occupied(grid):\n"
            "    for row_index, row in enumerate(grid):\n"
            "        for col_index, cell in enumerate(row):\n"
            "            if cell:\n"
            "                return row_index, col_index\n"
            "    return None"
        ),
        explanation=(
            "Returning from inside the inner loop leaves both loops at once, which a "
            "break could not do - it would only end the inner loop and let the outer one "
            "carry on. Iterating the rows keeps the search safe on a ragged grid."
        ),
        complexity="Time O(total cells) worst case; space O(1).",
        edge_cases="A cell of 0 is falsy, so it is not treated as occupied.",
        alternative_approaches="next() over a coordinate generator is the lazy form.",
        testing="assert first_occupied(((0, 0), (0, 1))) == (1, 1)\nassert first_occupied(()) is None",
    )
)

SOLUTIONS.append(
    solution(
        number=7,
        code=(
            "def grid_totals(grid) -> dict:\n"
            "    rows = 0\n"
            "    cols = 0\n"
            "    total = 0.0\n"
            "    for row in grid:\n"
            "        rows += 1\n"
            "        if len(row) > cols:\n"
            "            cols = len(row)\n"
            "        for cell in row:\n"
            "            total += cell\n"
            "    return {'rows': rows, 'cols': cols, 'sum': total}"
        ),
        explanation=(
            "Tracking the maximum row length as the scan proceeds is what makes the "
            "column count true for a ragged grid, where len(grid[0]) would understate "
            "it and range(len(grid[0])) would miss cells entirely."
        ),
        complexity="Time O(total cells); space O(1).",
        edge_cases="A grid of empty rows gives cols 0 and a sum of 0.0.",
        alternative_approaches="Per-row sums plus a max() give the same answer.",
        testing="assert grid_totals(((1, 2), (3,))) == {'rows': 2, 'cols': 2, 'sum': 6.0}\nassert grid_totals(()) == {'rows': 0, 'cols': 0, 'sum': 0.0}",
    )
)

SOLUTIONS.append(
    solution(
        number=8,
        code=(
            "def strongest_neighbour(grid, row, col):\n"
            "    best = None\n"
            "    best_value = None\n"
            "    for dr in (-1, 0, 1):\n"
            "        for dc in (-1, 0, 1):\n"
            "            if dr == 0 and dc == 0:\n"
            "                continue\n"
            "            r, c = row + dr, col + dc\n"
            "            if not (0 <= r < len(grid) and 0 <= c < len(grid[r])):\n"
            "                continue\n"
            "            value = grid[r][c]\n"
            "            if best_value is None or value > best_value:\n"
            "                best_value = value\n"
            "                best = (dr, dc)\n"
            "    return best"
        ),
        explanation=(
            "The bounds check must come before the indexing, because the offset loop "
            "deliberately walks off the edge of the grid. Seeding best_value with None "
            "rather than 0 is what lets a grid of all-negative values still produce a "
            "result."
        ),
        complexity="Time O(9) regardless of grid size; space O(1).",
        edge_cases="A one-cell grid has no in-bounds neighbours and returns None.",
        alternative_approaches="max() with a generator over the offsets is the one-liner.",
        testing="assert strongest_neighbour(((1, 9), (0, 0)), 0, 0) == (0, 1)\nassert strongest_neighbour(((5,),), 0, 0) is None",
    )
)

SOLUTIONS.append(
    solution(
        number=9,
        code=(
            "def coverage(grid, is_covered, min_ratio: float = 0.5) -> dict:\n"
            "    total = 0\n"
            "    covered = 0\n"
            "    for row in grid:\n"
            "        for cell in row:\n"
            "            total += 1\n"
            "            if is_covered(cell):\n"
            "                covered += 1\n"
            "    ratio = (covered / total) if total else 0.0\n"
            "    return {\n"
            "        'total': total,\n"
            "        'covered': covered,\n"
            "        'ratio': round(ratio, 3),\n"
            "        'ok': ratio >= min_ratio,\n"
            "    }"
        ),
        explanation=(
            "Counting total inside the loop is what makes the denominator honest for a "
            "ragged grid, and the conditional expression is what keeps an empty grid "
            "from dividing by zero. Reporting zero rather than a perfect 1.0 is the "
            "honest answer for a survey of nothing."
        ),
        complexity="Time O(total cells); space O(1).",
        edge_cases="An empty grid gives ratio 0.0 and ok False.",
        alternative_approaches="Returning the uncovered coordinates tells the caller where to go.",
        testing="out = coverage(((1, 0), (1, 0)), lambda c: c == 1)\nassert out['ratio'] == 0.5 and out['ok'] is True\nassert coverage((), lambda c: True)['ratio'] == 0.0",
    )
)

SOLUTIONS.append(
    solution(
        number=10,
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
            "def plan_cells(grid, robot, min_battery_pct: float = 20.0) -> list[tuple]:\n"
            "    \"\"\"Return passable cells in row-major order.\"\"\"\n"
            "    battery = robot.status()['battery_pct']\n"
            "    if battery <= min_battery_pct:\n"
            "        return []\n"
            "    plan: list[tuple] = []\n"
            "    for row_index, row in enumerate(grid):\n"
            "        for col_index, cell in enumerate(row):\n"
            "            if cell == 0:\n"
            "                plan.append((row_index, col_index))\n"
            "    return plan"
        ),
        explanation=(
            "Reading the battery once before the scan keeps the API call out of the inner "
            "loop and makes the depleted case a single early return rather than a "
            "condition repeated per cell. The nested scan then only classifies terrain, "
            "which is the part that genuinely needs two levels."
        ),
        complexity="Time O(total cells); space O(passable cells).",
        edge_cases="A depleted robot returns an empty list rather than a partial plan.",
        alternative_approaches="A comprehension over enumerate produces the same list more tersely.",
        testing="robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\nassert plan_cells(((0, 1), (0, 0)), robot) == [(0, 0), (1, 0), (1, 1)]\nassert plan_cells((), robot) == []",
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
            "def survey_coverage(robot, grid, min_ratio: float = 0.5) -> dict:\n"
            "    \"\"\"Combine a live battery reading with a grid coverage check.\"\"\"\n"
            "    battery = robot.status()['battery_pct']\n"
            "    total = 0\n"
            "    covered = 0\n"
            "    for row_index, row in enumerate(grid):\n"
            "        for col_index, cell in enumerate(row):\n"
            "            total += 1\n"
            "            if cell:\n"
            "                covered += 1\n"
            "    ratio = (covered / total) if total else 0.0\n"
            "    ready = ratio >= min_ratio and battery > min_ratio\n"
            "    return {\n"
            "        'battery_pct': round(battery, 2),\n"
            "        'total': total,\n"
            "        'covered': covered,\n"
            "        'ratio': round(ratio, 3),\n"
            "        'ready': ready,\n"
            "    }"
        ),
        explanation=(
            "The nested scan is used only where two levels are genuinely needed, and "
            "the battery is read once so the API call stays out of the inner loop. The "
            "readiness verdict combines two independent conditions, so a high coverage "
            "ratio cannot mask a flat battery."
        ),
        complexity="Time O(total cells); space O(1).",
        edge_cases="An empty grid gives ratio 0.0, which fails the coverage test.",
        alternative_approaches="A comprehension over enumerate keeps the same result shorter.",
        testing="robot = SimulatedRobot(name='rover-01', battery_wh=48.0)\nout = survey_coverage(robot, ((1, 1), (1, 0)))\nassert out['ready'] is True\nassert out['total'] == 4",
    )
)

QUIZ = []

QUIZ.append(
    quiz(
        question="How many times does the body of a 3-by-4 nested loop run?",
        choices=[
            "12",
            "7",
            "3",
            "4",
        ],
        answer=0,
        kind="code_output",
        explanation=(
            "The inner loop runs four times for each of the three outer passes, so the "
            "body executes twelve times. Adding the counts is the mistake; the costs "
            "multiply."
        ),
        reference="lesson.ipynb - Conceptual Explanation",
    )
)

QUIZ.append(
    quiz(
        question="Why does the inner loop appear to 'start over' on every outer pass?",
        choices=[
            "Because the outer loop resets the inner sequence's index.",
            "Because the interpreter caches the previous position and reuses it.",
            "Because the inner sequence is exhausted and re-entered each pass.",
            "It does not - the inner loop continues where it stopped.",
        ],
        answer=2,
        kind="conceptual",
        explanation=(
            "Each pass of the outer loop begins a fresh traversal of the inner sequence, "
            "which is exhausted and then re-entered. That is why a nested loop visits "
            "every ordered pair rather than a staircase."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="What does a `break` inside an inner loop leave?",
        choices=[
            "Both loops and the function.",
            "The inner loop only; the outer loop continues.",
            "The outer loop only.",
            "Nothing - it pauses the inner loop.",
        ],
        answer=1,
        kind="debugging",
        explanation=(
            "break acts on the innermost enclosing loop. The outer loop proceeds to its "
            "next iteration, which is often exactly what a grid scan needs - and is the "
            "reason a flag-free search returns instead."
        ),
        reference="lesson.ipynb - Formal Theory",
    )
)

QUIZ.append(
    quiz(
        question="Why does a hard-coded inner bound such as `range(3)` fail on a ragged grid?",
        choices=[
            "Because it is slower than enumerate.",
            "Because it counts the wrong cells in a square grid.",
            "Because ragged rows cannot be sliced.",
            "Because it indexes past a short row, or ignores extra cells in a long one.",
        ],
        answer=3,
        kind="identify_error",
        explanation=(
            "A fixed width assumes every row is the same length. On a shorter row it "
            "raises IndexError; on a longer one it silently skips the extra cells. "
            "Iterating the rows removes the assumption entirely."
        ),
        reference="lesson.ipynb - Common Mistakes",
    )
)

QUIZ.append(
    quiz(
        question="What is the total cost of n outer iterations containing m inner ones?",
        choices=[
            "n + m",
            "n * m",
            "max(n, m)",
            "n ** m",
        ],
        answer=1,
        kind="reasoning",
        explanation=(
            "The costs multiply rather than accumulate, because the inner loop is fully "
            "re-traversed on every outer pass. A third level makes it cubic, which is "
            "how a routine that handles a small table stops being usable."
        ),
        reference="lesson.ipynb - Performance Considerations",
    )
)

QUIZ.append(
    quiz(
        question="The sum of `a * b` over every ordered pair equals what?",
        choices=[
            "The square of the sum of all values.",
            "The sum of the squares of all values.",
            "The sum of all values, doubled.",
            "The product of the largest and smallest values.",
        ],
        answer=0,
        kind="reasoning",
        explanation=(
            "Expanding (a1 + a2 + ...)^2 produces exactly the cross terms the double "
            "loop accumulates. The identity turns an O(n^2) loop into one addition and "
            "one multiplication."
        ),
        reference="solution.ipynb - Solution 5",
    )
)

QUIZ.append(
    quiz(
        question="What does a sliding window replace?",
        choices=[
            "The need for a nested loop over a grid.",
            "The need to validate input before scanning.",
            "The need to report a not-found result.",
            "A nested scan of every k-sized window, in a single pass.",
        ],
        answer=3,
        kind="multiple_choice",
        explanation=(
            "Each window can be produced by slicing at advancing start indices, so the "
            "O(n*k) nested scan becomes O(n) windows. The windows are still built, just "
            "without re-scanning the prefix each time."
        ),
        reference="lesson.ipynb - Performance Considerations",
    )
)

QUIZ.append(
    quiz(
        question="Why iterate `for row in grid` rather than `range(len(grid[0]))`?",
        choices=[
            "Because len() on a list of lists is slow.",
            "Because range() cannot be nested.",
            "Because each row supplies its own correct length, so any shape works.",
            "Because enumerate only works on rows.",
        ],
        answer=2,
        kind="code_output",
        explanation=(
            "Taking the length from the row itself removes the assumption that every row "
            "matches the first - the assumption that breaks on ragged data and silently "
            "truncates longer rows."
        ),
        reference="lesson.ipynb - Syntax",
    )
)

QUIZ.append(
    quiz(
        question="Why does a rover's nested grid search return rather than break?",
        choices=[
            "Returning leaves both loops, so the remaining grid is never scanned.",
            "Returning is faster than break for a single loop.",
            "break cannot be used inside a for loop.",
            "Returning converts the search into a generator.",
        ],
        answer=0,
        kind="robotics",
        explanation=(
            "break would only end the inner loop and the rover would keep walking the "
            "rest of the grid. Returning leaves the whole scan at once, freeing the "
            "control cycle for the next command."
        ),
        reference="solution.ipynb - Solution 6",
    )
)

QUIZ.append(
    quiz(
        question="Which change turns an O(n^2) pairwise scan into O(n)?",
        choices=[
            "Adding an enumerate to the outer loop.",
            "Sorting the values first.",
            "Using the identity that the pairwise product sum is the square of the sum.",
            "Breaking out of the inner loop early.",
        ],
        answer=2,
        kind="implementation_choice",
        explanation=(
            "The algebraic identity removes the enumeration entirely. enumerate only "
            "changes what the loop knows, not how many steps it takes, and an early "
            "break is simply incorrect when every pair is required."
        ),
        reference="exercises.ipynb - Exercise 5",
    )
)

RESEARCH = {
    "question": (
        "How much faster is a single-pass sliding window than a nested scan of the "
        "same windows?"
    ),
    "hypothesis": (
        "The sliding window is faster by a factor close to the window size, because the "
        "nested version rescans the prefix for every start position."
    ),
    "experiment": [
        STEPS(
            [
                "Build a list of 20000 integers.",
                "Time a nested scan that checks every window of size 8 for a property.",
                "Time a single pass that maintains a rolling window of the same size.",
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
            "Compare the distributions and report the ratio. The hypothesis predicts a "
            "ratio near the window size, so a ratio close to 1 would mean the property "
            "being checked short-circuits in the nested version."
        ),
    ],
    "result": [
        MD(
            "State the observed ratio and whether it matched the prediction. If the "
            "nested version sometimes returned early, report how often rather than "
            "discarding those runs."
        ),
    ],
    "interpretation": [
        MD(
            "Explain the cost difference in terms of how many elements each version "
            "touches per window, and name at least two threats to validity, including "
            "the property short-circuiting."
        ),
    ],
    "conclusion": [
        MD(
            "Give your verdict and state when the sliding window is worth the extra "
            "bookkeeping, in one sentence."
        ),
    ],
    "extensions": [
        "Repeat with a window size of 32 to see whether the ratio tracks the size.",
        "Use a rolling sum to make the property check O(1) per position.",
    ],
}

CHALLENGE = {
    "title": "ROBO-X Challenge: Survey Grid Planner",
    "context": (
        "An underground rover must survey a grid before a mission. The grid may be "
        "ragged, and a depleted battery must stop the plan before any cell is listed."
    ),
    "mission": (
        "Implement `plan_survey(robot, grid, limits)` that returns the passable cells "
        "in row-major order and a readiness verdict, using a nested scan."
    ),
    "requirements": [
        "Return an empty plan when the battery is at or below the limit.",
        "Scan rows and cells with nested loops, tolerating ragged input.",
        "Return the passable coordinates plus total and covered counts.",
        "Report a readiness verdict combining battery and coverage.",
    ],
    "constraints": [
        "No hard-coded inner bound; no flag variable.",
        "Never raise for any grid shape.",
        "Complete well inside the 10 ms control budget per plan.",
    ],
    "interface": "def plan_survey(robot, grid, limits=None) -> dict:",
    "success_criteria": [
        "A healthy robot on a clean grid returns every cell as passable.",
        "A ragged grid is scanned without raising.",
        "A depleted robot returns an empty plan and ready False.",
    ],
    "extension": (
        "Return the sequence of moves between consecutive passable cells, and explain "
        "why that is a path rather than a set."
    ),
}

MINI_PROJECT = {
    "title": "Mini-Project: Survey Coverage Checker",
    "brief": (
        "Build a coverage checker for a survey grid. It must measure coverage "
        "correctly for a ragged grid, report which cells were missed, and stay linear "
        "rather than quadratic."
    ),
    "scenario": (
        "Before a mission the rover must confirm that enough of an area was surveyed. "
        "The grid comes from a sensor that occasionally drops a row, so it may be "
        "ragged."
    ),
    "rationale": (
        "Coverage checking is where nested loops meet correctness: the shape of the grid "
        "must not change the answer, and the operator needs to know where to send the "
        "robot next."
    ),
    "requirements": [
        "Measure total, covered and the ratio with one nested pass.",
        "Return the coordinates of every uncovered cell.",
        "Handle an empty grid by reporting ratio 0.0.",
        "Derive the verdict from the ratio rather than setting it directly.",
    ],
    "constraints": [
        "Standard library only.",
        "No hard-coded inner bound.",
        "Exactly one nested pass; no repeated slicing of the whole grid.",
    ],
    "deliverables": [
        "`coverage.py` with the checker.",
        "`test_coverage.py` with at least twelve assertions.",
        "A README section explaining how a ragged grid is measured.",
    ],
    "steps": [
        "Implement check_coverage(grid, is_covered, min_ratio).",
        "Test on a square grid, a ragged grid and an empty grid.",
        "Add the uncovered coordinate list and a test for it.",
        "Add the sliding-window variant for a fixed-size neighbourhood and compare the "
        "two results.",
    ],
    "expected_behavior": (
        "A square grid reports its true ratio. A ragged grid reports every cell that "
        "exists. An empty grid reports ratio 0.0 and ok False."
    ),
    "acceptance": [
        "All assertions pass from a clean run.",
        "A ragged grid is measured, not truncated.",
        "The uncovered list matches the cells the predicate rejected.",
        "An empty grid does not raise.",
    ],
    "extensions": [
        "Add a sliding-window neighbourhood average for smoothing.",
        "Return a per-row coverage breakdown for a dashboard.",
        "Integrate the check with a live simulator battery reading.",
    ],
}

INSTRUCTOR_NOTES = {
    "objectives": [
        "Make cost multiplication concrete before students optimise anything.",
        "Kill the hard-coded inner bound as a habit, not a warning.",
        "Introduce the closed form and the sliding window as replacements.",
    ],
    "misconceptions": [
        [
            "A nested loop adds the counts of the two levels.",
            "It multiplies them: n by m is n*m body executions.",
        ],
        [
            "The inner loop continues from where it stopped.",
            "It restarts from the beginning of its sequence each outer pass.",
        ],
        [
            "Every grid is rectangular, so a fixed width is fine.",
            "Sensor data is often ragged; iterate the rows instead.",
        ],
        [
            "A third level is needed for a 2-D problem.",
            "Two levels plus enumerate cover most grids; the third is usually waste.",
        ],
    ],
    "difficult_concepts": [
        "Accepting that a nested loop is sometimes the wrong tool.",
        "Deriving the pairwise product sum rather than enumerating it.",
        "Handling a ragged grid without defensive guards at every level.",
    ],
    "demonstrations": [
        "Count the body executions for a 3 by 4 grid and compare with 3 + 4.",
        "Break out of a fixed-width loop on a ragged grid and read the IndexError.",
        "Time a pairwise sum against its closed form on 10000 values.",
    ],
    "discussion": [
        "Which problems genuinely need two levels of iteration?",
        "Is a closed form always better, even when it is less obvious?",
    ],
    "student_errors": [
        [
            "IndexError on a ragged grid",
            "A hard-coded inner bound assumed a fixed width",
            "Iterate the rows themselves",
        ],
        [
            "A cell is counted twice",
            "range(len(grid) - 1) drops the last index, or a flag was never reset",
            "Enumerate both levels and test with a ragged grid",
        ],
        [
            "The routine takes minutes on a full grid",
            "A third level was added, or a window was scanned nested",
            "Count the steps first, then apply a closed form or a sliding window",
        ],
    ],
    "pacing": (
        "90 minutes of lesson with a live step count, then 2 hours of exercises. Spend "
        "real time on the closed form: it is the first time a student replaces code "
        "with algebra, and that idea recurs for the rest of the course."
    ),
    "extensions": [
        "Ask students to derive the count of distinct pairs from the sequence length.",
        "Have them convert a nested window scan into a sliding window and time both.",
    ],
    "assessment": (
        "Grade against rubric.md. Exercises 7, 8 and 10 carry the signal: they require "
        "ragged-safe accumulation, bounds-checked neighbour scans and a real API call."
    ),
    "support": (
        "Provide the count_cells solution and ask students to add a cols field, so the "
        "ragged case is visible before they write the harder functions."
    ),
    "extension_fast": (
        "Ask for a short note on how to bound the cost of a three-level scan over a "
        "fixed-size kernel."
    ),
}


LESSON["summary"] = [
    MD(
        "A nested loop runs its body once for every pass of the outer loop, so the work "
        "multiplies: *n* outer iterations with *m* inner ones perform *n × m* steps. That "
        "single fact is both why nested loops are the natural way to visit every cell of "
        "a grid or every pair of items, and why an extra level turns a routine that "
        "handles a small table into one that never finishes."
    ),
    MD(
        "Two properties cause most of the bugs. The inner loop **restarts** on every "
        "outer pass, so it never continues where it left off - which surprises people "
        "who expect a matrix traversal. And a hard-coded inner bound such as "
        "`range(3)` raises on a smaller grid and silently ignores extra cells on a "
        "larger one. Iterating the rows themselves removes both problems, and a ragged "
        "grid becomes an ordinary input rather than a crash."
    ),
    MD(
        "The most valuable skill here is recognising when a nested loop is not needed. "
        "A sliding window turns every k-sized window into one pass with a slice. A "
        "closed form replaces enumeration with algebra - the sum of all pairwise "
        "products is exactly the square of the sum, which takes an O(n²) loop and "
        "replaces it with one addition and one multiplication. And for searches, "
        "returning from inside the nested loop removes the remaining outer iterations "
        "entirely, which a `break` alone does not do."
    ),
]

LESSON["key_takeaways"] = [
    BULLETS(
        [
            "Nested loops multiply: n outer by m inner is n*m steps.",
            "The inner loop restarts on every outer pass.",
            "Never hard-code an inner bound; iterate the rows themselves.",
            "Use enumerate at both levels so coordinates are visible.",
            "Return from a nested search to stop both loops at once.",
            "A sliding window replaces a nested window scan with one pass.",
            "The pairwise product sum equals the square of the sum.",
            "Test with a ragged grid, not only a rectangular one.",
        ]
    ),
]

LESSON["further_exploration"] = [
    BULLETS(
        [
            "[The for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement)",
            "[Nested comprehensions](https://docs.python.org/3/tutorial/datastructures.html#nested-list-comprehensions)",
            "[itertools.product - the cartesian product without a nested loop](https://docs.python.org/3/library/itertools.html#itertools.product)",
            "[collections.Counter for grid statistics](https://docs.python.org/3/library/collections.html#collections.Counter)",
        ]
    ),
]

RUBRIC = {
    "artifacts": [
        ["exercises.ipynb", "40%", "All 10 exercises implemented and edge-cased."],
        ["mini_project.ipynb", "25%", "coverage.py plus its test suite."],
        ["robotics_challenge.ipynb", "25%", "Planner degrades safely."],
        ["research.ipynb", "10%", "Real measurements with a defensible conclusion."],
    ],
    "criteria": [
        ["Correctness", "30", "Ragged grids, empty grids and boundaries are all handled."],
        ["Cost awareness", "25", "Cost is derived or measured, not assumed."],
        ["Code quality", "25", "PEP 8 naming, docstrings, small focused functions."],
        ["Reasoning", "20", "Complexity claims explained in writing."],
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
            "Every exercise implemented, a ragged grid is measured rather than truncated, "
            "and the cost of the scan is stated in the write-up.",
        ],
        [
            "Merit",
            "Most exercises correct; the grid logic is right but a fixed inner bound is "
            "guarded rather than removed, and the ragged case is untested.",
        ],
        [
            "Pass",
            "Core requirements met, but the nested scan is quadratic where a linear one "
            "was available, and the empty grid case raises.",
        ],
        [
            "Fail",
            "A hard-coded inner bound is used, so the program crashes on real sensor data.",
        ],
    ],
}

TOPIC = topic(
    topic_id="2.4",
    title="Nested Loops and Common Patterns",
    module=2,
    module_title="Control Flow and Loops",
    directory="04_nested_loops_patterns",
    summary=(
        "Nested loops multiply the work: when they are the right tool, when a "
        "sliding window or a closed form replaces them, and why almost every bug in "
        "one is a boundary error."
    ),
    why_it_matters=(
        "Grid mapping, coverage surveys and neighbour planning are all nested loops "
        "over real sensor data that is rarely the tidy shape a textbook draws. A loop "
        "that assumes a fixed width crashes the moment a row comes back short."
    ),
    objectives=[
        "Compute the cost of nested loops as a product, and count the passes to prove it.",
        "Iterate rows rather than a hard-coded inner bound so ragged data is safe.",
        "Explain why the inner loop restarts on every outer pass.",
        "Replace a nested window scan with a sliding window in one pass.",
        "Recognise a closed form, such as the square of the sum for a pairwise product.",
        "Return from a nested search to stop both loops at once.",
    ],
    prerequisites=["Topic 2.3 Loop Control"],
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
