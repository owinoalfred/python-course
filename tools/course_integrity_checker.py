#!/usr/bin/env python3
"""Course integrity checker tool.

Audits the entire course repository against requirements.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.coursegen import catalogue
from tools.coursegen.schema import REQUIRED_DOCS, REQUIRED_NOTEBOOKS


def audit_repository() -> int:
    print("=" * 60)
    print("COURSE INTEGRITY REPORT")
    print("=" * 60)

    try:
        from course_content import TOPICS
    except Exception as exc:
        print(f"CRITICAL ERROR loading course content: {exc}")
        return 1

    total_modules = len(catalogue.MODULE_DIRS)
    total_topics = len(TOPICS)

    missing_notebooks = 0
    missing_docs = 0
    total_medium = sum(t.medium_count for t in TOPICS)
    total_hard = sum(t.hard_count for t in TOPICS)
    total_quiz = sum(t.quiz_count for t in TOPICS)
    total_research = sum(1 for t in TOPICS if t.research)
    total_robotics = sum(1 for t in TOPICS if t.robotics_challenge)

    print(f"Modules: {total_modules}")
    print(f"Topics: {total_topics}")
    print(f"Medium Exercises: {total_medium}")
    print(f"Hard Exercises: {total_hard}")
    print(f"Quiz Questions: {total_quiz}")
    print(f"Research Activities: {total_research}")
    print(f"Robotics Challenges: {total_robotics}")

    # Check directory structure for built topics
    for topic in TOPICS:
        mod_dir = catalogue.module_dir(topic.module)
        topic_path = ROOT / mod_dir / topic.directory
        if not topic_path.exists():
            print(f"MISSING DIRECTORY: {topic_path}")
            missing_docs += 1
            continue
        for nb_name in REQUIRED_NOTEBOOKS:
            if not (topic_path / nb_name).exists():
                missing_notebooks += 1
        for doc_name in REQUIRED_DOCS:
            if not (topic_path / doc_name).exists():
                missing_docs += 1

    print("-" * 60)
    print(f"Missing Notebooks: {missing_notebooks}")
    print(f"Missing Docs/Dirs: {missing_docs}")

    status = "PASS" if (missing_notebooks == 0 and missing_docs == 0 and total_topics > 0) else "FAIL"
    print(f"Overall Status: {status}")
    print("=" * 60)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(audit_repository())
