"""Authored course content — the single source of truth for the curriculum.

Each ``course_content/moduleN.py`` module exports a ``TOPICS`` list of
:class:`~tools.coursegen.schema.Topic` objects. ``python tools/build_course.py``
renders them into notebooks and docs; the validators check the *rendered*
artefacts, so a gap between content and output is always caught.

To add a topic:

1. Create a :func:`tools.coursegen.dsl.topic` entry in the right module file.
2. Run ``python tools/build_course.py --topic <id> --check`` to validate.
3. Run ``python tools/build_course.py`` to regenerate notebooks + manifest.
4. Run ``python tools/course_integrity_checker.py``.

Modules are imported defensively so a partially built course still loads.
"""

from __future__ import annotations

import importlib
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from tools.coursegen.schema import Topic

_MODULE_NAMES = [f"module{n}" for n in range(1, 10)]


def _apply_authored(topics: list["Topic"]) -> list["Topic"]:
    """Swap placeholder topics for hand-authored ones (see ``_authored``).

    The course is being migrated topic by topic from generated boilerplate to
    real teaching material. Anything listed in ``course_content._authored.AUTHORED``
    wins; everything else keeps the generated baseline until it is authored.
    """
    try:
        from course_content._authored import AUTHORED
    except ImportError:  # pragma: no cover - authored package is optional
        return topics
    if not AUTHORED:
        return topics
    replaced = [t.topic_id for t in topics if t.topic_id in AUTHORED]
    if replaced:
        print(
            f"content: {len(replaced)} hand-authored topic(s) active: "
            f"{', '.join(sorted(replaced))}",
            file=sys.stderr,
        )
    return [AUTHORED.get(t.topic_id, t) for t in topics]


def _load_all() -> list["Topic"]:
    topics: list[Topic] = []
    for name in _MODULE_NAMES:
        try:
            module = importlib.import_module(f"course_content.{name}")
        except ModuleNotFoundError:
            continue
        topics.extend(getattr(module, "TOPICS", []))
    return _apply_authored(topics)


TOPICS = _load_all()

__all__ = ["TOPICS"]
