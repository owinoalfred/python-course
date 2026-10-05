#!/usr/bin/env python3
"""Build every course artefact from the authored content in ``course_content/``.

Usage::

    python tools/build_course.py                 # build everything
    python tools/build_course.py --module 3      # one module
    python tools/build_course.py --topic 3.4     # one topic
    python tools/build_course.py --check         # validate only, write nothing
    python tools/build_course.py --list          # show the topic inventory

The build is deterministic: same content in, byte-identical notebooks out. This
matters because the generated notebooks are committed to the repository.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.coursegen import catalogue  # noqa: E402
from tools.coursegen.build import validate_topic, write_topic  # noqa: E402
from tools.coursegen.capstone import write_capstone_index  # noqa: E402
from tools.coursegen.manifest import write_manifest  # noqa: E402
from tools.coursegen.module_index import write_module_indexes  # noqa: E402
from tools.coursegen.schema import ContentError  # noqa: E402


def load_topics(module_filter: int | None = None, topic_filter: str | None = None):
    """Import and return the authored topics, optionally filtered."""
    from course_content import TOPICS

    topics = list(TOPICS)
    if module_filter is not None:
        topics = [t for t in topics if t.module == module_filter]
    if topic_filter is not None:
        wanted = topic_filter.strip()
        topics = [
            t
            for t in topics
            if t.topic_id == wanted or t.directory == wanted or t.directory.startswith(wanted)
        ]
    return topics


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--module", type=int, help="build only this module number")
    parser.add_argument("--topic", help="build only this topic id or directory")
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate content without writing any files",
    )
    parser.add_argument(
        "--list", action="store_true", help="print the topic inventory and exit"
    )
    parser.add_argument(
        "--lint",
        action="store_true",
        help="run the content linter and print the quality dashboard",
    )
    args = parser.parse_args(argv)

    if args.list:
        return _list_topics()

    started = time.perf_counter()
    try:
        topics = load_topics(args.module, args.topic)
    except ContentError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if not topics:
        print("No topics matched the given filters.", file=sys.stderr)
        return 2

    failures: list[str] = []
    written = 0
    for topic in topics:
        try:
            validate_topic(topic)
            if not args.check:
                module_dir = catalogue.module_dir(topic.module)
                write_topic(topic, ROOT, module_dir)
                written += 1
        except (ContentError, SyntaxError, ValueError) as exc:
            failures.append(str(exc))
            print(f"FAIL  {topic.topic_id} {topic.title}", file=sys.stderr)
            print(f"      {exc}", file=sys.stderr)

    if not args.check and not args.topic:
        all_topics = load_topics()
        write_manifest(all_topics, ROOT)
        write_module_indexes(ROOT, all_topics)
        write_capstone_index(ROOT)

    elapsed = time.perf_counter() - started
    mode = "validated" if args.check else "built"
    print(f"{mode} {len(topics) - len(failures)}/{len(topics)} topics in {elapsed:.2f}s")
    if written:
        print(f"wrote {written} topic directories under {ROOT}")
    if failures:
        print(f"\n{len(failures)} topic(s) failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure.splitlines()[0]}", file=sys.stderr)
        return 1

    if args.lint:
        from tools.coursegen.lint import lint_topics, render_report

        all_topics = load_topics()
        findings = lint_topics(all_topics)
        print("\n" + render_report(findings, all_topics))

    return 0


def _list_topics() -> int:
    topics = load_topics()
    current = None
    for topic in topics:
        if topic.module != current:
            current = topic.module
            print(
                f"\nModule {current}: {catalogue.module_title(current)} "
                f"[{catalogue.module_dir(current)}]"
            )
        print(
            f"  {topic.topic_id:<5} {topic.directory:<38} "
            f"MED={topic.medium_count} HARD={topic.hard_count} "
            f"QUIZ={topic.quiz_count} {topic.title}"
        )
    total_medium = sum(t.medium_count for t in topics)
    total_hard = sum(t.hard_count for t in topics)
    total_quiz = sum(t.quiz_count for t in topics)
    print(
        f"\n{len(topics)} topics | {total_medium} MEDIUM | {total_hard} HARD | "
        f"{total_quiz} quiz questions"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
