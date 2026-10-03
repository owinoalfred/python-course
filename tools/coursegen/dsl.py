"""Authoring DSL for course content.

Course content is authored as Python source (see ``course_content/``) and
rendered into notebooks by :mod:`tools.coursegen.build`. The DSL keeps that
source compact and readable while guaranteeing structure.

Block language
--------------
A *block* is one of:

* ``str``                     -> markdown paragraph
* ``MD(text)``                -> markdown paragraph
* ``CODE(src)``               -> fenced, syntax-checked code block
* ``BULLETS([...])``          -> unordered list
* ``STEPS([...])``            -> ordered list
* ``TABLE(headers, rows)``    -> markdown table
* ``NOTE(title, body)``       -> info callout
* ``WARN(title, body)``       -> warning callout
* ``TIP(title, body)``        -> tip callout
* ``EQUATION(text)``          -> monospaced math-ish block

Notebook files are assembled from blocks, so markdown and executable code stay
interleaved in the correct order.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence

from .schema import Exercise, QuizQuestion, Topic


# --------------------------------------------------------------------------- #
# Block types
# --------------------------------------------------------------------------- #
@dataclass(frozen=True, slots=True)
class Block:
    kind: str
    payload: Any


def MD(text: str) -> Block:
    """Markdown paragraph (may contain blank-line separated paragraphs)."""
    return Block("md", text.strip("\n"))


def CODE(source: str, lang: str = "python") -> Block:
    """Fenced code block. Python blocks are syntax-checked at build time."""
    return Block("code", (source.strip("\n"), lang))


def BULLETS(items: Iterable[str]) -> Block:
    return Block("bullets", [str(i) for i in items])


def STEPS(items: Iterable[str], start: int = 1) -> Block:
    return Block("steps", ([str(i) for i in items], start))


def TABLE(headers: Sequence[str], rows: Iterable[Sequence[Any]]) -> Block:
    return Block("table", ([str(h) for h in headers], [list(r) for r in rows]))


def NOTE(title: str, body: str) -> Block:
    return Block("note", (title, body.strip("\n")))


def WARN(title: str, body: str) -> Block:
    return Block("warn", (title, body.strip("\n")))


def TIP(title: str, body: str) -> Block:
    return Block("tip", (title, body.strip("\n")))


def EQUATION(text: str) -> Block:
    return Block("equation", text.strip("\n"))


def RAW(markdown: str) -> Block:
    """Markdown emitted verbatim (for cell tags, anchors, HTML)."""
    return Block("raw_md", markdown.strip("\n"))


# --------------------------------------------------------------------------- #
# Exercise / solution / quiz shorthands
# --------------------------------------------------------------------------- #
def exercise(**kwargs: Any) -> Exercise:
    """Build an :class:`Exercise`, validating every required field."""
    return Exercise.from_dict(kwargs)


def solution(
    number: int,
    code: str,
    explanation: str,
    complexity: str,
    edge_cases: str,
    alternative_approaches: str,
    testing: str,
) -> dict[str, Any]:
    """Build a solution record. ``code`` is syntax-checked at build time."""
    return {
        "number": number,
        "code": code.strip("\n"),
        "explanation": explanation.strip("\n"),
        "complexity": complexity.strip("\n"),
        "edge_cases": edge_cases.strip("\n"),
        "alternative_approaches": alternative_approaches.strip("\n"),
        "testing": testing.strip("\n"),
    }


def quiz(
    question: str,
    choices: Sequence[str],
    answer: int,
    explanation: str,
    kind: str = "multiple_choice",
    reference: str = "",
) -> dict[str, Any]:
    """Build a quiz question. ``answer`` is the zero-based correct index."""
    return {
        "question": question.strip("\n"),
        "choices": [str(c) for c in choices],
        "answer": answer,
        "explanation": explanation.strip("\n"),
        "kind": kind,
        "reference": reference,
    }


# --------------------------------------------------------------------------- #
# Topic assembly
# --------------------------------------------------------------------------- #
def topic(
    *,
    topic_id: str,
    title: str,
    module: int,
    module_title: str,
    directory: str,
    summary: str,
    why_it_matters: str,
    objectives: Sequence[str],
    prerequisites: Sequence[str],
    mental_model: Sequence[Block],
    terminology: Sequence[Sequence[str]],
    lesson: dict[str, Sequence[Block]],
    exercises: Sequence[Exercise],
    solutions: Sequence[dict[str, Any]],
    mini_project: dict[str, Any],
    research: dict[str, Any],
    quiz_questions: Sequence[dict[str, Any]],
    robotics_challenge: dict[str, Any],
    instructor_notes: dict[str, Any],
    rubric: dict[str, Any] | None = None,
    robo_x_milestone: str = "",
    robo_x_package: str = "",
) -> Topic:
    """Assemble a validated :class:`Topic`.

    ``lesson`` maps the keys declared in ``schema.LESSON_SECTIONS`` to blocks.
    Missing optional sections are filled from topic-level data by the builder,
    so authors only write the sections that need real prose.
    """
    from .schema import ContentError

    unknown = set(lesson) - {key for key, _ in _LESSON_KEYS}
    if unknown:
        raise ContentError(f"topic {topic_id}: unknown lesson sections {sorted(unknown)}")

    questions = []
    for index, raw in enumerate(quiz_questions, start=1):
        payload = dict(raw)
        payload.setdefault("number", index)
        questions.append(QuizQuestion.from_dict(payload))

    for index, record in enumerate(solutions, start=1):
        record.setdefault("number", index)

    return Topic(
        topic_id=topic_id,
        title=title,
        module=module,
        module_title=module_title,
        directory=directory,
        summary=summary.strip("\n"),
        why_it_matters=why_it_matters.strip("\n"),
        learning_objectives=[str(o) for o in objectives],
        prerequisites=[str(p) for p in prerequisites],
        mental_model=list(mental_model),
        terminology=[(str(k), str(v)) for k, v in terminology],
        lesson={key: list(blocks) for key, blocks in lesson.items()},
        exercises=list(exercises),
        solutions=list(solutions),
        mini_project=mini_project,
        research=research,
        quiz=questions,
        robotics_challenge=robotics_challenge,
        instructor_notes=instructor_notes,
        rubric=rubric or {},
        robo_x_milestone=robo_x_milestone,
        robo_x_package=robo_x_package,
    )


from .schema import LESSON_SECTIONS as _LESSON_KEYS  # noqa: E402  (cycle-free)
