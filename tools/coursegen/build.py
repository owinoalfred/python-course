"""Render :class:`~tools.coursegen.schema.Topic` objects into course artifacts.

Produces, for every topic::

    <module_dir>/<topic_dir>/README.md
    <module_dir>/<topic_dir>/lesson.ipynb
    <module_dir>/<topic_dir>/exercises.ipynb
    <module_dir>/<topic_dir>/solution.ipynb
    <module_dir>/<topic_dir>/research.ipynb
    <module_dir>/<topic_dir>/quiz.ipynb
    <module_dir>/<topic_dir>/mini_project.ipynb
    <module_dir>/<topic_dir>/robotics_challenge.ipynb
    <module_dir>/<topic_dir>/instructor_notes.md
    <module_dir>/<topic_dir>/rubric.md
    <module_dir>/<topic_dir>/assets/.gitkeep

Sections that are *derived* from topic-level data (objectives, prerequisites,
terminology, knowledge checks) are generated here so that authors spend their
effort on prose that needs real thought, while structure stays consistent.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from . import nb
from .dsl import Block, CODE, MD, BULLETS, NOTE, STEPS, TABLE, TIP, WARN
from .render import blocks_to_cells
from .schema import LESSON_SECTIONS, Topic

#: Sections every author must write. Others are derived automatically.
REQUIRED_AUTHORED: tuple[str, ...] = (
    "conceptual_explanation",
    "formal_theory",
    "syntax",
    "basic_examples",
    "intermediate_examples",
    "advanced_examples",
    "code_walkthrough",
    "common_mistakes",
    "debugging_techniques",
    "best_practices",
    "performance_considerations",
    "pythonic_approaches",
    "robotics_connection",
    "engineering_example",
    "guided_practice",
    "summary",
    "key_takeaways",
    "further_exploration",
)


def missing_authored_sections(t: Topic) -> list[str]:
    """Return authored lesson sections the topic does not provide."""
    return [key for key in REQUIRED_AUTHORED if not t.lesson.get(key)]


# --------------------------------------------------------------------------- #
# Shared chrome
# --------------------------------------------------------------------------- #
def _banner(t: Topic, notebook_name: str, subtitle: str) -> str:
    return (
        f"# {t.title}\n\n"
        f"**Topic:** `{t.topic_id}` &nbsp;|&nbsp; **Module {t.module}: {t.module_title}**\n\n"
        f"{subtitle}\n\n"
        f"> *Course:* Python Master Course &nbsp;|&nbsp; **Project:** ROBO-X "
        f"({t.robo_x_milestone or 'n/a'})\n"
    )


def _toc(entries: Sequence[tuple[str, str]]) -> str:
    return nb.table(["Section", "What you will do"], entries)


def _navigate(t: Topic, module_dir: str) -> str:
    return (
        "### Navigate\n\n"
        f"* [Lesson](lesson.ipynb) &nbsp;|&nbsp; "
        f"[Exercises](exercises.ipynb) &nbsp;|&nbsp; "
        f"[Solutions](solution.ipynb) &nbsp;|&nbsp; "
        f"[Research](research.ipynb) &nbsp;|&nbsp; "
        f"[Quiz](quiz.ipynb) &nbsp;|&nbsp; "
        f"[Mini-project](mini_project.ipynb) &nbsp;|&nbsp; "
        f"[Robotics challenge](robotics_challenge.ipynb)\n\n"
        f"Module index: [{module_dir}/README.md](../README.md)"
    )


def _derived_sections(t: Topic) -> dict[str, list[Block]]:
    """Lesson sections generated from topic-level data."""
    checks = [
        q for q in t.quiz if q.kind in {"conceptual", "reasoning", "robotics"}
    ][:4]
    knowledge: list[Block] = [
        MD(
            "Answer these before moving on. Full answers are in "
            "[solution.ipynb](solution.ipynb)."
        ),
        BULLETS([f"**Q{c - checks.index(q)}.** {q.question}" for c, q in enumerate(checks, 1)])
        if checks
        else BULLETS(["Revisit the mental model and restate it in your own words."]),
    ]
    return {
        "why_this_matters": [MD(t.why_it_matters)],
        "learning_objectives": [
            MD("By the end of this topic you will be able to:"),
            STEPS(t.learning_objectives),
        ],
        "prerequisites": [
            MD("This topic assumes you already have:"),
            BULLETS(t.prerequisites),
        ],
        "mental_model": list(t.mental_model),
        "terminology": [
            MD("Vocabulary used consistently throughout the course."),
            TABLE(["Term", "Meaning"], t.terminology),
        ],
        "knowledge_checks": knowledge,
    }


# --------------------------------------------------------------------------- #
# lesson.ipynb
# --------------------------------------------------------------------------- #
def build_lesson(t: Topic, module_dir: str) -> list[dict[str, Any]]:
    derived = _derived_sections(t)
    merged: dict[str, list[Block]] = {**derived, **t.lesson}

    cells: list[dict[str, Any]] = [
        nb.md(
            _banner(
                t,
                "lesson.ipynb",
                f"*{t.summary}*",
            )
        ),
        nb.md(_navigate(t, module_dir)),
    ]

    for index, (key, heading) in enumerate(LESSON_SECTIONS, start=1):
        cells.append(nb.md(f"## {index}. {heading}"))
        blocks = merged.get(key)
        if not blocks:
            raise ValueError(f"{t.topic_id}: lesson section {key!r} produced no content")
        cells.extend(blocks_to_cells(blocks, topic_id=t.topic_id))

        # Line-by-line explanation follows the walkthrough it explains.
        if key == "code_walkthrough" and not merged.get("line_by_line"):
            cells.extend(_auto_line_by_line(t))

    return cells


def _auto_line_by_line(t: Topic) -> list[dict[str, Any]]:
    """Derive a line-by-line table from the walkthrough code block."""
    lines: list[str] = []
    for block in t.lesson.get("code_walkthrough", []):
        if block.kind == "code":
            lines = block.payload[0].splitlines()
            break
    if not lines:
        return [nb.md("Read the walkthrough above line by line and annotate it yourself.")]
    rows = [
        (str(n), text.strip() if text.strip() else "*blank*")
        for n, text in enumerate(lines[:24], start=1)
    ]
    return [
        nb.md(
            "Numbered source of the walkthrough above. Cover the right-hand column and "
            "reconstruct each line's job from memory, then reveal it."
        ),
        nb.md(nb.table(["#", "Source line"], rows)),
    ]


# --------------------------------------------------------------------------- #
# exercises.ipynb
# --------------------------------------------------------------------------- #
def _exercise_cells(t: Topic, ex, index: int, total: int) -> list[dict[str, Any]]:
    cells = [
        nb.md(
            f"### Exercise {ex.number} — {ex.title}\n\n"
            f"**Difficulty:** `{ex.difficulty}` &nbsp;|&nbsp; "
            f"**Exercise {index} of {total}**\n\n"
            f"**Learning objectives**\n\n"
            f"{nb.bullets(ex.learning_objectives)}\n\n"
            f"**Concepts tested**\n\n"
            f"{nb.bullets(ex.concepts_tested)}"
        ),
        nb.md(
            "**Problem statement**\n\n"
            f"{ex.problem_statement}\n\n"
            "**Requirements**\n\n"
            f"{nb.bullets(ex.requirements)}\n\n"
            "**Constraints**\n\n"
            f"{nb.bullets(ex.constraints)}"
        ),
        nb.md(
            "**Input description**\n\n"
            f"{ex.input_description}\n\n"
            "**Expected output**\n\n"
            f"{ex.expected_output}"
        ),
        nb.md(
            "**Example input**\n\n"
            f"{nb.fenced(ex.example_input)}\n\n"
            "**Example output**\n\n"
            f"{nb.fenced(ex.example_output)}"
        ),
        nb.md(
            "**Edge cases you must handle**\n\n"
            f"{nb.bullets(ex.edge_cases)}"
        ),
        nb.md(
            "**Hints** *(read at most two before you start)*\n\n"
            f"{nb.numbered(ex.hints)}"
        ),
        nb.md(
            "**Success criteria** *(you have met the objective when…)*\n\n"
            f"{nb.bullets(ex.success_criteria)}\n\n"
            f"**Optional extension**\n\n{ex.optional_extension}"
        ),
        nb.md(
            "---\n\n"
            "### Your solution\n\n"
            "Write your implementation in the cell below. Do not peek at "
            "[solution.ipynb](solution.ipynb) until you have run your tests.\n\n"
            "```python\n"
            "def solve(...):\n"
            "    # your implementation\n"
            "    ...\n"
            "```"
        ),
        nb.code(
            "# ==== YOUR IMPLEMENTATION FOR EXERCISE "
            f"{ex.number} ({ex.title}) ====\n"
            "\n"
            "# Reminder: handle the edge cases listed above.\n",
            tags=["student", f"exercise-{ex.number}"],
        ),
        nb.code(
            f"# ==== TESTS FOR EXERCISE {ex.number} ====\n"
            "# Write assertions that would fail on a wrong implementation.\n"
            "\n"
            "# 1. Happy path from the example\n"
            "\n"
            "# 2. Each edge case listed above\n",
            tags=["student", f"exercise-{ex.number}-tests"],
        ),
    ]
    return cells


def build_exercises(t: Topic, module_dir: str) -> list[dict[str, Any]]:
    medium = [e for e in t.exercises if e.difficulty == "MEDIUM"]
    hard = [e for e in t.exercises if e.difficulty == "HARD"]
    total = len(t.exercises)

    cells: list[dict[str, Any]] = [
        nb.md(
            _banner(
                t,
                "exercises.ipynb",
                f"*{len(medium)} MEDIUM + {len(hard)} HARD + 1 ROBOTICS = {total + 1} tasks.*",
            )
        ),
        nb.md(_navigate(t, module_dir)),
        nb.md(
            "## How to work through these exercises\n\n"
            + "\n".join(
                [
                    "1. Read the problem statement and write the **input → output** "
                    "contract in your own words.",
                    "2. Restate the edge cases; decide what your function does for each.",
                    "3. Implement, then write assertions for the example *and* every "
                    "edge case before you iterate.",
                    "4. Only after your tests fail-or-pass for the right reason, compare "
                    "with [solution.ipynb](solution.ipynb).",
                ]
            )
        ),
        nb.md(
            nb.admonition(
                "Integrity",
                "Work before you look",
                "These exercises are assessed. Attempt every one, including the ones "
                "you find hard — the struggle is where the learning happens. Solutions "
                "are reference implementations, not answers to copy.",
            )
        ),
        nb.md(
            "## Coverage summary\n\n"
            + nb.table(
                ["Band", "Count", "Focus"],
                [
                    [
                        "MEDIUM",
                        str(len(medium)),
                        "Multi-step reasoning, applying this topic's concepts",
                    ],
                    [
                        "HARD",
                        str(len(hard)),
                        "Algorithm design, validation, reusable solutions",
                    ],
                    ["ROBOTICS", "1", "Integration with the ROBO-X project"],
                ],
            )
        ),
        nb.md(
            "## Part A — MEDIUM exercises\n\n"
            + nb.table(
                ["#", "Title", "Core concepts"],
                [[str(e.number), e.title, ", ".join(e.concepts_tested[:3])] for e in medium],
            )
        ),
    ]

    for position, ex in enumerate(medium, start=1):
        cells.extend(_exercise_cells(t, ex, position, total))
        if ex is not medium[-1]:
            cells.append(nb.md("---"))

    cells.append(
        nb.md(
            "## Part B — HARD exercises\n\n"
            + nb.table(
                ["#", "Title", "Core concepts"],
                [[str(e.number), e.title, ", ".join(e.concepts_tested[:3])] for e in hard],
            )
        )
    )

    for position, ex in enumerate(hard, start=len(medium) + 1):
        cells.extend(_exercise_cells(t, ex, position, total))
        if ex is not hard[-1]:
            cells.append(nb.md("---"))

    challenge = t.robotics_challenge
    cells.append(
        nb.md(
            "---\n\n"
            f"# Part C — ROBOTICS CHALLENGE\n\n"
            f"## {challenge.get('title', 'ROBO-X integration task')}\n\n"
            f"{challenge.get('context', '')}\n\n"
            f"**Mission**\n\n{challenge.get('mission', '')}\n\n"
            "**Requirements**\n\n"
            f"{nb.bullets(challenge.get('requirements', []))}\n\n"
            "**Constraints**\n\n"
            f"{nb.bullets(challenge.get('constraints', []))}"
        )
    )
    if challenge.get("interface"):
        cells.append(
            nb.md(
                "**Interface you must implement**\n\n" + nb.fenced(challenge["interface"])
            )
        )
    cells.append(
        nb.md(
            "**Success criteria** *(your submission passes when…)*\n\n"
            f"{nb.bullets(challenge.get('success_criteria', []))}\n\n"
            f"**Extension**\n\n{challenge.get('extension', '')}"
        )
    )
    cells.append(
        nb.code(
            "# ==== ROBO-X CHALLENGE IMPLEMENTATION ====\n",
            tags=["student", "robotics-challenge"],
        )
    )
    cells.append(
        nb.md(
            "### Self-assessment\n\n"
            "Before submitting, confirm each item:\n\n"
            + nb.bullets(
                [
                    "Every MEDIUM exercise implemented and edge-cased.",
                    "Every HARD exercise implemented with at least three assertions.",
                    "Robotics challenge implemented against the given interface.",
                    "`python tools/progress_tracker.py` reports no missing work.",
                ]
            )
        )
    )
    return cells


# --------------------------------------------------------------------------- #
# solution.ipynb
# --------------------------------------------------------------------------- #
def build_solutions(t: Topic, module_dir: str) -> list[dict[str, Any]]:
    by_number = {s["number"]: s for s in t.solutions}
    if len(by_number) != len(t.solutions):
        raise ValueError(f"{t.topic_id}: duplicate solution numbers")

    cells: list[dict[str, Any]] = [
        nb.md(
            _banner(
                t,
                "solution.ipynb",
                f"*Reference implementations for all {len(t.exercises)} exercises "
                "plus the robotics challenge.*",
            )
        ),
        nb.md(_navigate(t, module_dir)),
        nb.md(
            nb.admonition(
                "How to use solutions",
                "Compare, do not copy",
                "Work each exercise yourself first. When you open this notebook, compare "
                "your approach with the reference: check the reasoning, the edge cases "
                "and the complexity. If your solution differs, that is fine — verify it "
                "with the tests provided and keep whichever is clearer.",
            )
        ),
    ]

    for ex in t.exercises:
        record = by_number.get(ex.number)
        if record is None:
            raise ValueError(f"{t.topic_id}: exercise {ex.number} has no solution")
        source = record["code"]
        ok, err = nb.check_syntax(source, where=f"{t.topic_id}:solution {ex.number}")
        if not ok:
            raise SyntaxError(f"invalid solution code ({err})\n---\n{source}")

        cells.append(
            nb.md(
                f"## Solution {ex.number} — {ex.title}\n\n"
                f"**Difficulty:** `{ex.difficulty}` &nbsp;|&nbsp; "
                f"**Concepts:** {', '.join(ex.concepts_tested)}"
            )
        )
        cells.append(nb.md(f"**Explanation and reasoning**\n\n{record['explanation']}"))
        cells.append(nb.code(source, tags=[f"solution-{ex.number}"]))
        cells.append(
            nb.md(
                "**Complexity**\n\n"
                f"{record['complexity']}\n\n"
                "**Edge cases and failure modes**\n\n"
                f"{record['edge_cases']}\n\n"
                "**Alternative approaches**\n\n"
                f"{record['alternative_approaches']}"
            )
        )
        cells.append(nb.md("**Tests — run the cell to verify the reference solution**"))
        cells.append(
            nb.code(record["testing"], tags=[f"solution-{ex.number}-tests"])
        )
        cells.append(nb.md("---"))

    challenge_solution = t.solutions[-1] if len(t.solutions) > len(t.exercises) else None
    if challenge_solution is not None:
        cells.append(
            nb.md(
                f"# Robotics challenge solution — "
                f"{t.robotics_challenge.get('title', 'ROBO-X task')}"
            )
        )
        cells.append(nb.md(f"**Explanation**\n\n{challenge_solution['explanation']}"))
        cells.append(
            nb.code(challenge_solution["code"], tags=["robotics-challenge-solution"])
        )
        cells.append(
            nb.md(
                "**Complexity**\n\n"
                f"{challenge_solution['complexity']}\n\n"
                "**Notes and trade-offs**\n\n"
                f"{challenge_solution['edge_cases']}"
            )
        )
        cells.append(nb.code(challenge_solution["testing"], tags=["robotics-tests"]))

    cells.append(
        nb.md(
            "## Reflection\n\n"
            "For each exercise where your solution differed from the reference, write "
            "one sentence explaining *why* yours was better or worse. This is the "
            "highest-value part of the notebook:\n\n"
            + nb.bullets(
                [
                    "A case the reference handles but mine did not.",
                    "A case mine handles better — and what the reference is missing.",
                    "A performance difference that matters at robot scale.",
                ]
            )
        )
    )
    return cells


# --------------------------------------------------------------------------- #
# research.ipynb  (QUESTION -> HYPOTHESIS -> ... -> CONCLUSION)
# --------------------------------------------------------------------------- #
RESEARCH_STAGES: tuple[tuple[str, str], ...] = (
    ("question", "1. QUESTION"),
    ("hypothesis", "2. HYPOTHESIS"),
    ("experiment", "3. EXPERIMENT"),
    ("data", "4. DATA"),
    ("analysis", "5. ANALYSIS"),
    ("result", "6. RESULT"),
    ("interpretation", "7. INTERPRETATION"),
    ("conclusion", "8. CONCLUSION"),
)


def build_research(t: Topic, module_dir: str) -> list[dict[str, Any]]:
    research = t.research
    cells: list[dict[str, Any]] = [
        nb.md(
            _banner(
                t,
                "research.ipynb",
                "*An investigation you run yourself and defend with measurements.*",
            )
        ),
        nb.md(_navigate(t, module_dir)),
        nb.md(
            "## Method\n\n"
            "This is **not** a search-and-summarise assignment. You must produce real "
            "measurements on your machine, then explain what they mean.\n\n"
            + nb.steps(
                [
                    "State a question that can be settled by measurement.",
                    "Write a falsifiable hypothesis — one that *could* be wrong.",
                    "Design an experiment that isolates one variable.",
                    "Run it, collect data, and keep the raw numbers.",
                    "Analyse: what would each possible result have meant?",
                    "Record the result, including results that surprised you.",
                    "Interpret the mechanism, not just the numbers.",
                    "Conclude, and state what you would measure next.",
                ]
            )
        ),
        nb.md(
            nb.admonition(
                "Rule",
                "Measure, do not assume",
                "Every claim in RESULT, INTERPRETATION and CONCLUSION must be traceable "
                "to a number you produced in this notebook. If you cannot cite the "
                "measurement, it is speculation — label it as such.",
            )
        ),
    ]

    for key, heading in RESEARCH_STAGES:
        cells.append(nb.md(f"## {heading}"))
        blocks = research.get(key)
        if not blocks:
            raise ValueError(f"{t.topic_id}: research stage {key!r} is empty")
        if isinstance(blocks, str):
            blocks = [MD(blocks)]
        cells.extend(blocks_to_cells(blocks, topic_id=f"{t.topic_id}:research"))

    if research.get("extensions"):
        cells.append(nb.md("## 9. EXTENSIONS — what to investigate next"))
        cells.append(nb.md(nb.bullets(research["extensions"])))

    cells.append(
        nb.md(
            "## 10. Write-up template\n\n"
            "Produce a short report (Markdown or notebook) containing:\n\n"
            + nb.table(
                ["Section", "Word budget", "Must include"],
                [
                    ["Question", "40", "Exactly one measurable question"],
                    ["Hypothesis", "40", "Falsifiable prediction"],
                    ["Method", "150", "Variables, isolation, repetitions"],
                    ["Data", "table", "Raw measurements, not summaries"],
                    ["Analysis", "150", "Comparison against the prediction"],
                    ["Interpretation", "150", "Mechanism, caveats, threats to validity"],
                    ["Conclusion", "80", "Verdict and next experiment"],
                ],
            )
        )
    )
    return cells


# --------------------------------------------------------------------------- #
# quiz.ipynb
# --------------------------------------------------------------------------- #
def build_quiz(t: Topic, module_dir: str) -> list[dict[str, Any]]:
    cells: list[dict[str, Any]] = [
        nb.md(
            _banner(
                t,
                "quiz.ipynb",
                f"*{len(t.quiz)} questions covering this topic and its prerequisites.*",
            )
        ),
        nb.md(_navigate(t, module_dir)),
        nb.md(
            "## Instructions\n\n"
            + nb.bullets(
                [
                    "Answer every question **before** running the answer cells.",
                    "For `code_output` questions, predict the output first, then run it.",
                    "A wrong answer is worth more than a blank: state *why* you chose it.",
                    "Score yourself: "
                    f"{round(0.6 * len(t.quiz))}/{len(t.quiz)} = 60% is the pass mark.",
                ]
            )
        ),
        nb.md(
            "**Question types in this quiz**\n\n"
            + nb.table(
                ["Type", "Count"],
                _quiz_kind_counts(t),
            )
        ),
        nb.md("## Questions"),
    ]

    for q in t.quiz:
        choices = "\n".join(
            f"{chr(ord('A') + i)}. {choice}" for i, choice in enumerate(q.choices)
        )
        cells.append(
            nb.md(
                f"**Q{q.number}.** {q.question}\n\n"
                f"*Type: `{q.kind}`*\n\n"
                f"{choices}"
            )
        )
        cells.append(
            nb.code(
                f"# Q{q.number}: record your answer here\n"
                f"# my_answer = ",
                tags=["student", f"quiz-{q.number}"],
            )
        )

    cells.append(nb.md("---\n\n# Answer key and explanations"))
    cells.append(
        nb.md(
            nb.admonition(
                "Check your answers",
                "Explain every wrong answer in your own words",
                "A correct guess with no explanation means the concept is not yet "
                "transferable. Re-read the referenced section of `lesson.ipynb` for "
                "anything you got wrong.",
            )
        )
    )
    for q in t.quiz:
        correct = chr(ord("A") + q.answer)
        reference = f"\n\n*Reference:* {q.reference}" if q.reference else ""
        cells.append(
            nb.md(
                f"**Q{q.number} — Answer: `{correct}`**\n\n"
                f"{q.explanation}{reference}"
            )
        )
    return cells


def _quiz_kind_counts(t: Topic) -> list[list[str]]:
    counts: dict[str, int] = {}
    for q in t.quiz:
        counts[q.kind] = counts.get(q.kind, 0) + 1
    return [[kind, str(count)] for kind, count in sorted(counts.items())]


# --------------------------------------------------------------------------- #
# mini_project.ipynb
# --------------------------------------------------------------------------- #
def build_mini_project(t: Topic, module_dir: str) -> list[dict[str, Any]]:
    project = t.mini_project
    cells: list[dict[str, Any]] = [
        nb.md(
            _banner(
                t,
                "mini_project.ipynb",
                f"*{project.get('title', 'Mini-project')} — deliverable, not an exercise.*",
            )
        ),
        nb.md(_navigate(t, module_dir)),
        nb.md(
            "## Project brief\n\n"
            f"{project.get('brief', '')}\n\n"
            "**Scenario**\n\n"
            f"{project.get('scenario', '')}\n\n"
            "**Why this project exists**\n\n"
            f"{project.get('rationale', '')}"
        ),
        nb.md(
            "## Requirements\n\n"
            + nb.bullets(project.get("requirements", []))
            + "\n\n"
            + "**Constraints**\n\n"
            + nb.bullets(project.get("constraints", []))
            + "\n\n"
            + "**Deliverables**\n\n"
            + nb.bullets(project.get("deliverables", []))
        ),
        nb.md(
            "## Implementation steps\n\n"
            "Work through these in order. Do not start at step 4 — each step is designed "
            "to be runnable and testable before the next begins.\n\n"
            + nb.steps(project.get("steps", []))
        ),
        nb.md("## Step 1 — design before you code\n"),
        nb.code(
            "# Record the design here: inputs, outputs, data structures, and the\n"
            "# invariants your code must maintain.\n"
            "#\n"
            "# Suggested structure:\n"
            "#   - public API (function/class signatures)\n"
            "#   - invariants (what must always be true)\n"
            "#   - failure modes (what can go wrong and how you signal it)\n",
            tags=["student", "design"],
        ),
        nb.md("## Step 2 — implementation\n"),
        nb.code(
            "# Implement the project incrementally.\n"
            "# Keep the code testable: small functions, no hidden global state.\n",
            tags=["student", "implementation"],
        ),
        nb.md(
            "## Step 3 — tests\n\n"
            "Write tests **before** the implementation is considered done. At minimum "
            "cover the happy path, each documented edge case, and one failure mode.\n\n"
            + nb.bullets(
                [
                    "Use `assert` in a notebook cell, or move the tests into "
                    "`tests/unit/test_<your_module>.py` and run pytest.",
                    "Name each test after the behaviour it protects, not the function.",
                    "A test that cannot fail is not a test.",
                ]
            )
        ),
        nb.code(
            "# Write your tests here (or in tests/unit/ as pytest functions).\n",
            tags=["student", "tests"],
        ),
        nb.md(
            "## Expected behaviour\n\n"
            f"{project.get('expected_behavior', '')}\n\n"
            "**Acceptance checklist** *(all must pass before you submit)*\n\n"
            + nb.bullets(project.get("acceptance", []))
        ),
        nb.md(
            "## Grading\n\n"
            f"This mini-project is graded with [`rubric.md`](rubric.md) — "
            "code quality, correctness, testing and engineering reasoning each carry "
            "weight. Use [`../instructor_notes.md`](../instructor_notes.md) if you are "
            "self-studying: it lists the misconceptions graders look for.\n\n"
            "## Extension ideas\n\n"
            + nb.bullets(project.get("extensions", []))
        ),
        nb.md(
            "## Reflection\n\n"
            "Answer in Markdown:\n\n"
            + nb.numbered(
                [
                    "Which requirement forced a design decision you had not anticipated?",
                    "What did you test, and what did you *not* test?",
                    "If you had one more week, what would you change first?",
                ]
            )
        )
    ]
    return cells


# --------------------------------------------------------------------------- #
# robotics_challenge.ipynb
# --------------------------------------------------------------------------- #
def build_robotics_challenge(t: Topic, module_dir: str) -> list[dict[str, Any]]:
    challenge = t.robotics_challenge
    cells: list[dict[str, Any]] = [
        nb.md(
            _banner(
                t,
                "robotics_challenge.ipynb",
                f"*{challenge.get('title', 'ROBO-X task')} — ROBO-X "
                f"{t.robo_x_milestone or ''}*",
            )
        ),
        nb.md(_navigate(t, module_dir)),
        nb.md(
            f"## {challenge.get('title', 'Challenge')}\n\n"
            f"{challenge.get('context', '')}\n\n"
            f"### Mission\n\n{challenge.get('mission', '')}"
        ),
        nb.md(
            "### Requirements\n\n"
            + nb.bullets(challenge.get("requirements", []))
            + "\n\n"
            + "### Constraints\n\n"
            + nb.bullets(challenge.get("constraints", []))
        ),
    ]
    if challenge.get("interface"):
        cells.append(
            nb.md(
                "### Interface you must implement\n\n"
                "Match these signatures — later ROBO-X milestones depend on them.\n\n"
                + nb.fenced(challenge["interface"])
            )
        )
    cells.append(
        nb.md(
            "### Success criteria\n\n"
            + nb.bullets(challenge.get("success_criteria", []))
            + "\n\n"
            + "### Extension\n\n"
            + str(challenge.get("extension", ""))
        )
    )
    cells.append(
        nb.md(
            "### Simulation only\n\n"
            "This challenge requires **no physical hardware**. Simulated sensors, "
            "actuators and battery behaviour are supplied in "
            "[`shared/robo_x_sim.py`](../../../shared/robo_x_sim.py), so results are "
            "reproducible on any machine.\n\n"
            "```python\n"
            "from shared.robo_x_sim import SimulatedRobot, ScenarioBuilder\n"
            "\n"
            "robot = SimulatedRobot(name=\"robo-x-01\", battery_wh=48.0)\n"
            "robot.read_sensor(\"distance\")   # deterministic, seeded\n"
            "robot.move(distance_m=1.5)\n"
            "robot.status()\n"
            "```"
        )
    )
    cells.append(nb.code(
        "# ==== ROBO-X CHALLENGE IMPLEMENTATION ====\n",
        tags=["student", "robotics-challenge"],
    ))
    cells.append(
        nb.md(
            "### Self-review\n\n"
            + nb.bullets(
                [
                    "Does your implementation satisfy **every** requirement above?",
                    "Does it degrade safely when a sensor returns nonsense?",
                    "Could a colleague understand it from your docstrings alone?",
                    "Is there at least one automated test for the safety behaviour?",
                ]
            )
        )
    )
    return cells


# --------------------------------------------------------------------------- #
# Markdown documents
# --------------------------------------------------------------------------- #
def build_readme(t: Topic, module_dir: str) -> str:
    medium = [e for e in t.exercises if e.difficulty == "MEDIUM"]
    hard = [e for e in t.exercises if e.difficulty == "HARD"]
    challenge = t.robotics_challenge
    mini = t.mini_project
    research = t.research

    parts = [
        f"# {t.topic_id} — {t.title}",
        "",
        f"**Module {t.module}: {t.module_title}**",
        "",
        t.summary,
        "",
        "## Why this topic matters",
        "",
        t.why_it_matters,
        "",
        "## Learning objectives",
        "",
        nb.numbered(t.learning_objectives),
        "",
        "## Prerequisites",
        "",
        nb.bullets(t.prerequisites),
        "",
        "## Files in this topic",
        "",
        nb.table(
            ["File", "Purpose", "When to open it"],
            [
                [
                    "[`lesson.ipynb`](lesson.ipynb)",
                    "The 25-section lesson with runnable examples",
                    "First — every session starts here",
                ],
                [
                    "[`exercises.ipynb`](exercises.ipynb)",
                    f"{len(medium)} MEDIUM + {len(hard)} HARD + 1 robotics challenge",
                    "After the lesson; graded",
                ],
                [
                    "[`solution.ipynb`](solution.ipynb)",
                    "Reference implementations with tests and complexity notes",
                    "Only after you have attempted the exercises",
                ],
                [
                    "[`research.ipynb`](research.ipynb)",
                    "A measurement-driven investigation",
                    "End of topic",
                ],
                [
                    "[`quiz.ipynb`](quiz.ipynb)",
                    f"{len(t.quiz)} questions with an answer key",
                    "Self-check before moving on",
                ],
                [
                    "[`mini_project.ipynb`](mini_project.ipynb)",
                    f"{mini.get('title', 'Mini-project')}",
                    "Deliverable",
                ],
                [
                    "[`robotics_challenge.ipynb`](robotics_challenge.ipynb)",
                    f"{challenge.get('title', 'ROBO-X task')}",
                    "ROBO-X milestone",
                ],
                [
                    "[`instructor_notes.md`](instructor_notes.md)",
                    "Teaching notes and common misconceptions",
                    "Lecturers only",
                ],
                [
                    "[`rubric.md`](rubric.md)",
                    "How this topic is graded",
                    "Before submitting work",
                ],
            ],
        ),
        "",
        "## Exercise index",
        "",
        nb.table(
            ["#", "Title", "Difficulty", "Concepts"],
            [
                [str(e.number), e.title, e.difficulty, ", ".join(e.concepts_tested)]
                for e in t.exercises
            ],
        ),
        "",
        f"## Robotics challenge — {challenge.get('title', '')}",
        "",
        str(challenge.get("mission", "")),
        "",
        f"**ROBO-X milestone:** {t.robo_x_milestone or 'n/a'}",
        "",
        "## Research task",
        "",
        str(research.get("question", "")),
        "",
        "## Recommended workflow",
        "",
        nb.steps(
            [
                "Read `lesson.ipynb` end to end, running every code cell.",
                "Answer the knowledge checks without looking back.",
                "Attempt `exercises.ipynb` — all eleven tasks.",
                "Run the research experiment and record real measurements.",
                "Take the quiz; re-read any section you failed.",
                "Build the mini-project and write its tests.",
                "Implement the ROBO-X challenge and commit it to the project repo.",
            ]
        ),
        "",
        "## Navigation",
        "",
        f"* Module index: [`{module_dir}/README.md`](../README.md)",
        "* Course path: [`LEARNING_PATH.md`](../../../LEARNING_PATH.md)",
        "",
    ]
    return "\n".join(parts)


def build_instructor_notes(t: Topic, module_dir: str) -> str:
    notes = t.instructor_notes
    parts = [
        f"# Instructor notes — {t.topic_id} {t.title}",
        "",
        f"**Module {t.module}: {t.module_title}**",
        "",
        "## Teaching objectives",
        "",
        nb.bullets(notes.get("objectives", [])),
        "",
        "## Likely misconceptions",
        "",
        nb.table(
            ["Misconception", "Correction to drive home"],
            notes.get("misconceptions", []),
        ),
        "",
        "## Difficult concepts",
        "",
        nb.bullets(notes.get("difficult_concepts", [])),
        "",
        "## Demonstration suggestions",
        "",
        nb.bullets(notes.get("demonstrations", [])),
        "",
        "## Discussion questions",
        "",
        nb.bullets(notes.get("discussion", [])),
        "",
        "## Common student errors",
        "",
        nb.table(
            ["Error", "Why it happens", "Intervention"],
            notes.get("student_errors", []),
        ),
        "",
        "## Recommended pacing",
        "",
        str(notes.get("pacing", "")),
        "",
        "## Extension activities",
        "",
        nb.bullets(notes.get("extensions", [])),
        "",
        "## Assessment advice",
        "",
        str(notes.get("assessment", "")),
        "",
        "## Differentiation",
        "",
        "**If students are struggling:** " + str(notes.get("support", "")),
        "",
        "**If students finish early:** " + str(notes.get("extension_fast", "")),
        "",
    ]
    return "\n".join(parts)


def build_rubric(t: Topic, module_dir: str) -> str:
    rubric = t.rubric
    criteria = rubric.get(
        "criteria",
        [
            ["Correctness", "25", "Outputs match the specification on all given and hidden cases"],
            ["Code quality", "20", "PEP 8, meaningful names, no duplication, small functions"],
            ["Reasoning", "20", "Design decisions are explained and justified"],
            ["Testing", "20", "Covers happy path, every edge case, and one failure mode"],
            ["Documentation", "15", "Docstrings and comments explain *why*, not *what*"],
        ],
    )
    parts = [
        f"# Rubric — {t.topic_id} {t.title}",
        "",
        f"**Module {t.module}: {t.module_title}**",
        "",
        "## What is assessed",
        "",
        nb.table(
            ["Artefact", "Weight", "Evidence expected"],
            rubric.get("artifacts", [])
            or [
                [
                    "[`exercises.ipynb`](exercises.ipynb)",
                    "50%",
                    "All 10 exercises implemented and edge-cased",
                ],
                [
                    "[`robotics_challenge.ipynb`](robotics_challenge.ipynb)",
                    "20%",
                    "Working ROBO-X contribution with the required interface",
                ],
                [
                    "[`mini_project.ipynb`](mini_project.ipynb)",
                    "15%",
                    "Complete project with tests",
                ],
                [
                    "[`research.ipynb`](research.ipynb)",
                    "15%",
                    "Real measurements and a defensible conclusion",
                ],
            ],
        ),
        "",
        "## Performance criteria",
        "",
        nb.table(["Criterion", "Weight", "Description"], criteria),
        "",
        "## Band descriptors",
        "",
        nb.table(
            ["Band", "Range", "Overall descriptor"],
            rubric.get(
                "bands",
                [
                    ["Distinction", "85–100", "Correct, tested, clearly reasoned, production-shaped"],
                    ["Merit", "70–84", "Correct with minor gaps in testing or documentation"],
                    ["Pass", "50–69", "Core requirement met; edge cases or tests incomplete"],
                    ["Fail", "0–49", "Core requirement not met, or code does not run"],
                ],
            ),
        ),
        "",
        "## Grade descriptors by band",
        "",
    ]
    for band in rubric.get(
        "band_details",
        [
            [
                "Distinction",
                "Every exercise implemented. All listed edge cases handled and tested. "
                "Complexity claims are correct. The robotics challenge satisfies its "
                "interface and degrades safely. Research conclusions are supported by "
                "the measurements shown.",
            ],
            [
                "Merit",
                "Most exercises implemented correctly. Testing covers the main paths and "
                "some edge cases. One or two exercises may be incomplete but the approach "
                "shows sound reasoning.",
            ],
            [
                "Pass",
                "Core requirements met on the main paths. Testing is thin, some edge "
                "cases are unhandled, or the robotics challenge only partially works. "
                "Reasoning is present but not consistently justified.",
            ],
            [
                "Fail",
                "Multiple exercises missing or non-functional. Code does not run. No tests. "
                "Edge cases ignored.",
            ],
        ],
    ):
        parts.append(f"* **{band[0]}** — {band[1]}")
    parts.extend(
        [
            "",
            "## Academic integrity",
            "",
            "Submit work you can explain line by line. Solutions exist in "
            "[`solution.ipynb`](solution.ipynb) for self-checking; graded work must be "
            "your own. See "
            "[`academic_integrity.md`](../../../00_course_orientation/academic_integrity.md).",
            "",
            "## Submission checklist",
            "",
            nb.bullets(
                [
                    "All notebook cells executed from a clean kernel, top to bottom.",
                    "`python tools/notebook_validator.py <this topic>` passes.",
                    "Tests run and their output is included in the write-up.",
                    "README/dev notes state any deviation from the specification.",
                ]
            ),
            "",
        ]
    )
    return "\n".join(parts)
