"""The content linter must be clean for every hand-authored topic.

This is the regression guard for the rebuild: as topics are migrated out of
boilerplate they are registered in ``course_content._authored.AUTHORED``, and
this test fails if any of them regresses below the Course Content Standard.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from course_content import TOPICS  # noqa: E402
from course_content._authored import AUTHORED  # noqa: E402
from tools.coursegen.lint import CRITICAL, HIGH, lint_topics  # noqa: E402


def test_at_least_one_topic_is_authored() -> None:
    assert AUTHORED, "no hand-authored topics are registered yet"


def test_authored_topics_pass_the_linter() -> None:
    findings = lint_topics(list(AUTHORED.values()))
    blocking = [f for f in findings if f.severity in {CRITICAL, HIGH}]
    report = "\n".join(f"{f.severity} {f.topic_id} {f.check}: {f.message}" for f in blocking)
    assert not blocking, report


def test_authored_topics_are_wired_into_the_course() -> None:
    live_ids = {t.topic_id for t in TOPICS}
    for topic_id in AUTHORED:
        assert topic_id in live_ids, f"authored topic {topic_id} is not in the course"


def test_authored_lessons_contain_executable_code() -> None:
    from tools.coursegen.lint import count_code_cells

    for topic_id, topic in AUTHORED.items():
        assert count_code_cells(topic) >= 12, (
            f"topic {topic_id} has only {count_code_cells(topic)} executable code cells"
        )