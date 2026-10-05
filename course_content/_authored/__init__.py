"""Hand-authored topics that override the generated baseline.

The rebuild migrates the course **one topic at a time**. Any topic exported here
replaces the placeholder topic of the same ``topic_id`` that is produced by
``course_content/moduleN.py``. That keeps the build green while the migration is
in progress, and the linter reports exactly which topics are still outstanding.

To add a newly authored topic:

1. Create ``topic_<id>_<slug>.py`` exposing a module-level ``TOPIC``.
2. Register it in ``AUTHORED`` below.
"""

from __future__ import annotations

from . import (
    topic_01_introduction,
    topic_01_02_environment,
    topic_01_03_syntax,
    topic_01_04_variables,
    topic_01_05_types,
    topic_01_06_operators,
    topic_01_07_io,
    topic_01_08_scripts,
)

#: topic_id -> authored Topic. This dict is the single migration switchboard.
AUTHORED = {
    topic_01_introduction.TOPIC.topic_id: topic_01_introduction.TOPIC,
    topic_01_02_environment.TOPIC.topic_id: topic_01_02_environment.TOPIC,
    topic_01_03_syntax.TOPIC.topic_id: topic_01_03_syntax.TOPIC,
    topic_01_04_variables.TOPIC.topic_id: topic_01_04_variables.TOPIC,
    topic_01_05_types.TOPIC.topic_id: topic_01_05_types.TOPIC,
    topic_01_06_operators.TOPIC.topic_id: topic_01_06_operators.TOPIC,
    topic_01_07_io.TOPIC.topic_id: topic_01_07_io.TOPIC,
    topic_01_08_scripts.TOPIC.topic_id: topic_01_08_scripts.TOPIC,
}

__all__ = ["AUTHORED"]