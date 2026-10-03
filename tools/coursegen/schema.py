"""Declarative schema for course topics.

A *topic* is the atomic learning unit of the course. Every topic produces a
directory containing::

    README.md
    lesson.ipynb
    mini_project.ipynb
    exercises.ipynb
    research.ipynb
    quiz.ipynb
    robotics_challenge.ipynb
    solution.ipynb
    instructor_notes.md
    rubric.md
    assets/

This module defines the data contract for a topic and validates it. The
contract is intentionally strict: the build fails loudly on incomplete content
rather than emitting a notebook with a placeholder section.

Nothing here imports third-party libraries, so the course can be validated with
a bare interpreter.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

# --------------------------------------------------------------------------- #
# Notebook / doc names produced for every topic
# --------------------------------------------------------------------------- #
REQUIRED_NOTEBOOKS: tuple[str, ...] = (
    "lesson.ipynb",
    "mini_project.ipynb",
    "exercises.ipynb",
    "research.ipynb",
    "quiz.ipynb",
    "robotics_challenge.ipynb",
    "solution.ipynb",
)

REQUIRED_DOCS: tuple[str, ...] = ("README.md", "instructor_notes.md", "rubric.md")

DIFFICULTIES: tuple[str, ...] = ("MEDIUM", "HARD")

MEDIUM_PER_TOPIC = 5
HARD_PER_TOPIC = 5
MIN_QUIZ_QUESTIONS = 10
MAX_QUIZ_QUESTIONS = 20

#: Required lesson sections, in order. Defined once and consumed by both the
#: generator and the validators, so "required" can never drift between them.
LESSON_SECTIONS: tuple[tuple[str, str], ...] = (
    ("why_this_matters", "Why This Topic Matters"),
    ("learning_objectives", "Learning Objectives"),
    ("prerequisites", "Prerequisites"),
    ("mental_model", "Mental Model"),
    ("terminology", "Terminology"),
    ("conceptual_explanation", "Conceptual Explanation"),
    ("formal_theory", "Formal Theory"),
    ("syntax", "Syntax"),
    ("basic_examples", "Basic Examples"),
    ("intermediate_examples", "Intermediate Examples"),
    ("advanced_examples", "Advanced Examples"),
    ("code_walkthrough", "Code Walkthrough"),
    ("line_by_line", "Line-by-Line Explanation"),
    ("common_mistakes", "Common Mistakes"),
    ("debugging_techniques", "Debugging Techniques"),
    ("best_practices", "Best Practices"),
    ("performance_considerations", "Performance Considerations"),
    ("pythonic_approaches", "Pythonic Approaches"),
    ("robotics_connection", "Robotics Connection"),
    ("engineering_example", "Engineering Example"),
    ("guided_practice", "Guided Practice"),
    ("knowledge_checks", "Knowledge Checks"),
    ("summary", "Summary"),
    ("key_takeaways", "Key Takeaways"),
    ("further_exploration", "Further Exploration"),
)

#: Every exercise must carry these fields (course spec, section 10).
EXERCISE_FIELDS: tuple[str, ...] = (
    "number",
    "title",
    "difficulty",
    "learning_objectives",
    "concepts_tested",
    "problem_statement",
    "requirements",
    "constraints",
    "input_description",
    "expected_output",
    "example_input",
    "example_output",
    "edge_cases",
    "hints",
    "success_criteria",
    "optional_extension",
)

QUIZ_KINDS: tuple[str, ...] = (
    "multiple_choice",
    "code_output",
    "conceptual",
    "debugging",
    "identify_error",
    "implementation_choice",
    "reasoning",
    "robotics",
)

SOLUTION_FIELDS: tuple[str, ...] = (
    "number",
    "code",
    "explanation",
    "complexity",
    "edge_cases",
    "alternative_approaches",
    "testing",
)


# --------------------------------------------------------------------------- #
# Errors and small validation helpers
# --------------------------------------------------------------------------- #
class ContentError(ValueError):
    """Raised when authored content violates the course contract."""


def require(mapping: dict[str, Any], key: str, where: str) -> Any:
    """Fetch ``key`` from ``mapping`` or raise a descriptive error."""
    if key not in mapping:
        raise ContentError(f"{where}: missing required key {key!r}")
    return mapping[key]


def require_non_empty(value: Any, where: str, *, min_len: int = 1) -> Any:
    """Reject empty strings and too-short / empty sequences."""
    if isinstance(value, str):
        if len(value.strip()) < min_len:
            raise ContentError(f"{where}: empty or too-short text")
        return value
    if isinstance(value, Sequence):
        if len(value) < min_len:
            raise ContentError(
                f"{where}: expected at least {min_len} item(s), got {len(value)}"
            )
        return value
    if value is None:
        raise ContentError(f"{where}: value is None")
    return value


# --------------------------------------------------------------------------- #
# Data classes
# --------------------------------------------------------------------------- #
@dataclass(slots=True)
class Exercise:
    """One programming exercise. Field order mirrors ``EXERCISE_FIELDS``."""

    number: int
    title: str
    difficulty: str
    learning_objectives: list[str]
    concepts_tested: list[str]
    problem_statement: str
    requirements: list[str]
    constraints: list[str]
    input_description: str
    expected_output: str
    example_input: str
    example_output: str
    edge_cases: list[str]
    hints: list[str]
    success_criteria: list[str]
    optional_extension: str

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Exercise":
        where = f"exercise {raw.get('number', '?')}"
        difficulty = raw.get("difficulty")
        if difficulty not in DIFFICULTIES:
            raise ContentError(
                f"{where}: difficulty must be one of {DIFFICULTIES}, got {difficulty!r}"
            )
        data = {name: require(raw, name, where) for name in EXERCISE_FIELDS}
        for name in EXERCISE_FIELDS:
            require_non_empty(data[name], f"{where}.{name}")
        return cls(**data)


@dataclass(slots=True)
class QuizQuestion:
    """One quiz question with exactly one correct answer index."""

    number: int
    question: str
    kind: str
    choices: list[str]
    answer: int
    explanation: str
    reference: str = ""

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "QuizQuestion":
        where = f"quiz question {raw.get('number', '?')}"
        require_non_empty(raw.get("question", ""), f"{where}.question")
        kind = raw.get("kind", "multiple_choice")
        if kind not in QUIZ_KINDS:
            raise ContentError(f"{where}: unknown kind {kind!r}")
        choices = require(raw, "choices", where)
        if not isinstance(choices, list) or len(choices) < 2:
            raise ContentError(f"{where}: needs at least 2 choices")
        answer = require(raw, "answer", where)
        if not isinstance(answer, int) or isinstance(answer, bool):
            raise ContentError(f"{where}: answer must be an int index")
        if not (0 <= answer < len(choices)):
            raise ContentError(f"{where}: answer index {answer} out of range")
        require_non_empty(raw.get("explanation", ""), f"{where}.explanation")
        return cls(
            number=int(raw.get("number", 0)),
            question=str(raw["question"]),
            kind=kind,
            choices=[str(c) for c in choices],
            answer=answer,
            explanation=str(raw["explanation"]),
            reference=str(raw.get("reference", "")),
        )


@dataclass(slots=True)
class Topic:
    """A complete learning unit: everything needed to emit a topic directory."""

    topic_id: str
    title: str
    module: int
    module_title: str
    directory: str
    summary: str
    why_it_matters: str
    learning_objectives: list[str]
    prerequisites: list[str]
    mental_model: str
    terminology: list[tuple[str, str]]
    lesson: dict[str, dict[str, Any]]
    exercises: list[Exercise]
    solutions: list[dict[str, Any]]
    mini_project: dict[str, Any]
    research: dict[str, Any]
    quiz: list[QuizQuestion]
    robotics_challenge: dict[str, Any]
    instructor_notes: dict[str, Any]
    rubric: dict[str, Any]
    robo_x_milestone: str = ""
    robo_x_package: str = ""

    # -- derived counts (consumed by validators and the integrity report) --- #
    @property
    def medium_count(self) -> int:
        return sum(1 for e in self.exercises if e.difficulty == "MEDIUM")

    @property
    def hard_count(self) -> int:
        return sum(1 for e in self.exercises if e.difficulty == "HARD")

    @property
    def total_exercises(self) -> int:
        return len(self.exercises)

    @property
    def quiz_count(self) -> int:
        return len(self.quiz)
