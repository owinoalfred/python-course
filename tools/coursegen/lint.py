"""Content linter for the Python Master Course.

This turns the "Constitution" (see the rebuild plan) into executable checks so
boilerplate cannot creep back in. It inspects the *authored* :class:`Topic`
objects (not the rendered notebooks) and reports findings by severity.

Design
------
* Report mode (default) always exits 0 and prints a dashboard.
* ``--strict`` exits non-zero if any CRITICAL or HIGH finding exists — this is
  what CI will gate on once the content is authored to standard.
* ``--topic <id>`` restricts the run (e.g. to verify a single golden topic).

Severities
----------
* CRITICAL — the artifact is unusable as teaching material (e.g. every quiz
  answer is index 0, or a lesson has no executable code).
* HIGH     — materially degrades quality (banned filler, no lesson code cells).
* MEDIUM   — improves quality (thin sections, weak diversification).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.coursegen.dsl import Block  # noqa: E402
from tools.coursegen.render import block_text  # noqa: E402
from tools.coursegen.schema import LESSON_SECTIONS, Topic  # noqa: E402

CRITICAL = "CRITICAL"
HIGH = "HIGH"
MEDIUM = "MEDIUM"
_ORDER = {CRITICAL: 0, HIGH: 1, MEDIUM: 2}

#: Minimum executable code cells in a lesson (Constitution §0.2).
MIN_CODE_CELLS = 12
#: Minimum lesson word count (Constitution §0.2).
MIN_LESSON_WORDS = 2500
#: No single quiz answer index may exceed this share (Constitution §0.4).
MAX_ANSWER_SHARE = 0.40
#: Minimum distinct quiz kinds per topic (Constitution §0.4).
MIN_QUIZ_KINDS = 4

#: Placeholder / boilerplate phrases that must never ship (Constitution §0.7).
BANNED_PHRASES: tuple[str, ...] = (
    "Sample raw input payload",
    "Sample complex input payload",
    "Expected output matching problem specification",
    "Validated or processed output matching task specifications",
    "Validated and sanitized output payload",
    "Passes all tests.",
    "Passes edge-case assertion verifications.",
    "cannot be used in Python",
    "causes a syntax error unconditionally",
    "is only supported in C++",
    "Definition for ",
    "Term ",
    "Python 3.14",
    "Provide starter template.",
)


@dataclass(frozen=True)
class Finding:
    severity: str
    topic_id: str
    check: str
    message: str


def _sorted(findings: Iterable[Finding]) -> list[Finding]:
    return sorted(findings, key=lambda f: (_ORDER[f.severity], f.topic_id, f.check))


# --------------------------------------------------------------------------- #
# Metric helpers
# --------------------------------------------------------------------------- #
def _lesson_blocks(t: Topic) -> list[Block]:
    blocks: list[Block] = []
    for section_blocks in t.lesson.values():
        blocks.extend(section_blocks)
    blocks.extend(t.mental_model)
    return blocks


def count_code_cells(t: Topic) -> int:
    return sum(1 for b in _lesson_blocks(t) if b.kind == "code_cell")


def lesson_word_count(t: Topic) -> int:
    words = len(t.summary.split()) + len(t.why_it_matters.split())
    for group in (t.learning_objectives, t.prerequisites):
        words += sum(len(item.split()) for item in group)
    for term, definition in t.terminology:
        words += len(term.split()) + len(definition.split())
    for block in _lesson_blocks(t):
        words += len(block_text(block).split())
    return words


def lesson_text(t: Topic) -> str:
    parts = [block_text(b) for b in _lesson_blocks(t)]
    for term, definition in t.terminology:
        parts.append(f"{term}: {definition}")
    return "\n".join(parts)


def _find_banned(text: str) -> list[str]:
    return [phrase for phrase in BANNED_PHRASES if phrase in text]


# --------------------------------------------------------------------------- #
# Per-topic checks
# --------------------------------------------------------------------------- #
def check_lesson(t: Topic) -> list[Finding]:
    findings: list[Finding] = []
    cells = count_code_cells(t)
    if cells < MIN_CODE_CELLS:
        severity = CRITICAL if cells == 0 else HIGH
        findings.append(
            Finding(
                severity,
                t.topic_id,
                "lesson.code_cells",
                f"lesson has {cells} executable code cells (need >= {MIN_CODE_CELLS})",
            )
        )
    words = lesson_word_count(t)
    if words < MIN_LESSON_WORDS:
        findings.append(
            Finding(
                HIGH,
                t.topic_id,
                "lesson.words",
                f"lesson is ~{words} words (need >= {MIN_LESSON_WORDS})",
            )
        )
    banned = _find_banned(lesson_text(t))
    if banned:
        findings.append(
            Finding(
                HIGH,
                t.topic_id,
                "lesson.banned_phrases",
                f"banned filler present: {', '.join(sorted(set(banned)))}",
            )
        )
    return findings


def check_quiz(t: Topic) -> list[Finding]:
    findings: list[Finding] = []
    if not t.quiz:
        return [Finding(CRITICAL, t.topic_id, "quiz.empty", "topic has no quiz questions")]

    answers = Counter(q.answer for q in t.quiz)
    top_index, top_count = answers.most_common(1)[0]
    share = top_count / len(t.quiz)
    if share > MAX_ANSWER_SHARE:
        letter = chr(ord("A") + top_index)
        findings.append(
            Finding(
                CRITICAL,
                t.topic_id,
                "quiz.answer_distribution",
                f"{top_count}/{len(t.quiz)} answers are '{letter}' "
                f"({share:.0%} > {MAX_ANSWER_SHARE:.0%} allowed)",
            )
        )

    kinds = {q.kind for q in t.quiz}
    if len(kinds) < MIN_QUIZ_KINDS:
        findings.append(
            Finding(
                MEDIUM,
                t.topic_id,
                "quiz.kinds",
                f"only {len(kinds)} quiz kind(s) used (need >= {MIN_QUIZ_KINDS})",
            )
        )

    if any(len(q.explanation.split()) < 15 for q in t.quiz):
        findings.append(
            Finding(
                MEDIUM,
                t.topic_id,
                "quiz.explanation",
                "one or more quiz explanations are under 15 words",
            )
        )

    banned = _find_banned("\n".join(c for q in t.quiz for c in q.choices))
    if banned:
        findings.append(
            Finding(
                CRITICAL,
                t.topic_id,
                "quiz.banned_distractors",
                f"nonsense distractors present: {', '.join(sorted(set(banned)))}",
            )
        )
    return findings


def check_exercises(t: Topic) -> list[Finding]:
    findings: list[Finding] = []
    for ex in t.exercises:
        blob = "\n".join(
            [
                ex.example_input,
                ex.example_output,
                ex.expected_output,
                "\n".join(ex.edge_cases),
                "\n".join(ex.requirements),
                "\n".join(ex.constraints),
                "\n".join(ex.hints),
            ]
        )
        banned = _find_banned(blob)
        if banned:
            findings.append(
                Finding(
                    HIGH,
                    t.topic_id,
                    "exercises.banned_phrases",
                    f"exercise {ex.number} uses placeholder text: "
                    f"{', '.join(sorted(set(banned)))}",
                )
            )
            break
    return findings


def check_research(t: Topic) -> list[Finding]:
    """Flag research sections that ship fabricated measurement tables."""
    data_blocks = t.research.get("data") or []
    if isinstance(data_blocks, str):
        data_blocks = [data_blocks]
    has_numbers = False
    for block in data_blocks:
        text = block_text(block) if isinstance(block, Block) else str(block)
        if re.search(r"\|\s*\d", text):
            has_numbers = True
            break
    if has_numbers:
        return [
            Finding(
                CRITICAL,
                t.topic_id,
                "research.fabricated_data",
                "research ships a pre-filled data table — measurements must be "
                "produced by the learner, not invented",
            )
        ]
    return []


def check_version(t: Topic) -> list[Finding]:
    if "Python 3.14" in lesson_text(t):
        return [
            Finding(
                HIGH,
                t.topic_id,
                "version",
                "references Python 3.14 (the course targets 3.12)",
            )
        ]
    return []


# --------------------------------------------------------------------------- #
# Cross-topic checks (catch copy-paste boilerplate)
# --------------------------------------------------------------------------- #
def check_boilerplate(topics: Sequence[Topic]) -> list[Finding]:
    """Flag question/exercise text that is reused verbatim across many topics."""
    findings: list[Finding] = []

    quiz_signatures: Counter[str] = Counter()
    for t in topics:
        for q in t.quiz:
            # Strip the topic noun so "Question N regarding <topic>" collapses.
            signature = re.sub(r"regarding [^:]+:", "regarding <topic>:", q.question)
            quiz_signatures[signature] += 1
    shared_quiz = [(sig, c) for sig, c in quiz_signatures.items() if c >= 5]
    if shared_quiz:
        sig, count = max(shared_quiz, key=lambda item: item[1])
        findings.append(
            Finding(
                CRITICAL,
                "<course>",
                "boilerplate.quiz",
                f"quiz template reused {count} times, e.g. {sig[:70]!r}",
            )
        )

    exercise_signatures: Counter[str] = Counter()
    for t in topics:
        for ex in t.exercises:
            signature = re.sub(r"solve_[a-z0-9]+", "solve_X", ex.problem_statement)
            signature = re.sub(r"`?[A-Z][A-Za-z ]{3,40}`?", "<topic>", signature)
            exercise_signatures[signature] += 1
    shared_ex = [(sig, c) for sig, c in exercise_signatures.items() if c >= 5]
    if shared_ex:
        sig, count = max(shared_ex, key=lambda item: item[1])
        findings.append(
            Finding(
                CRITICAL,
                "<course>",
                "boilerplate.exercises",
                f"exercise template reused {count} times, e.g. {sig[:70]!r}",
            )
        )
    return findings


# --------------------------------------------------------------------------- #
# Aggregation and reporting
# --------------------------------------------------------------------------- #
def lint_topic(t: Topic) -> list[Finding]:
    findings: list[Finding] = []
    findings += check_lesson(t)
    findings += check_quiz(t)
    findings += check_exercises(t)
    findings += check_research(t)
    findings += check_version(t)
    return findings


def lint_topics(topics: Sequence[Topic]) -> list[Finding]:
    findings: list[Finding] = []
    for t in topics:
        findings += lint_topic(t)
    findings += check_boilerplate(topics)
    return findings


def _failing_topic_ids(findings: Sequence[Finding]) -> set[str]:
    return {
        f.topic_id
        for f in findings
        if f.severity in {CRITICAL, HIGH} and f.topic_id != "<course>"
    }


def render_report(findings: Sequence[Finding], topics: Sequence[Topic]) -> str:
    ordered = _sorted(findings)
    by_severity = Counter(f.severity for f in findings)
    by_check = Counter(f.check for f in findings)
    failing = _failing_topic_ids(findings)
    passed = [t.topic_id for t in topics if t.topic_id not in failing]

    lines = [
        "=" * 62,
        "COURSE CONTENT LINT",
        "=" * 62,
        f"Topics scanned: {len(topics)}",
        f"Findings: {by_severity.get(CRITICAL, 0)} CRITICAL / "
        f"{by_severity.get(HIGH, 0)} HIGH / {by_severity.get(MEDIUM, 0)} MEDIUM",
        "-" * 62,
        "By check:",
    ]
    for check, count in by_check.most_common():
        lines.append(f"  {check:<32} {count}")

    lines += ["-" * 62, "Sample findings:"]
    for finding in ordered[:15]:
        lines.append(
            f"  [{finding.severity:<8}] {finding.topic_id:<8} "
            f"{finding.check}: {finding.message}"
        )

    lines += [
        "-" * 62,
        f"Topics passing (no CRITICAL/HIGH): {len(passed)}/{len(topics)}",
    ]
    if passed:
        lines.append("  PASS " + ", ".join(passed))

    lines.append("=" * 62)
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint the authored course content.")
    parser.add_argument("--topic", help="lint only this topic id (e.g. 1.1)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit non-zero if any CRITICAL/HIGH finding exists",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = parser.parse_args(argv)

    from course_content import TOPICS

    topics = list(TOPICS)
    if args.topic:
        topics = [t for t in topics if t.topic_id == args.topic]
        if not topics:
            print(f"No topic with id {args.topic!r}", file=sys.stderr)
            return 2

    findings = lint_topics(topics)

    if args.json:
        import json

        print(
            json.dumps(
                [
                    {
                        "severity": f.severity,
                        "topic_id": f.topic_id,
                        "check": f.check,
                        "message": f.message,
                    }
                    for f in _sorted(findings)
                ],
                indent=2,
            )
        )
    else:
        print(render_report(findings, topics))

    if args.strict and any(f.severity in {CRITICAL, HIGH} for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



