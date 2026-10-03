"""Generate ``course_manifest.yaml`` from authored content.

The manifest is the machine-readable source of truth consumed by the
validators. It is *generated* so it can never drift from the content, but it is
committed to the repository so external tooling can read it without importing
the build system.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from .catalogue import CAPSTONE_DIRS, modules
from .schema import Topic


def _yaml_str(value: str) -> str:
    """Quote a scalar safely for YAML output."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return f'"{escaped}"'


def _yaml_list(values: Sequence[Any], indent: int = 4) -> list[str]:
    pad = " " * indent
    return [f"{pad}- {_yaml_scalar(v)}" for v in values]


def _yaml_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(_yaml_scalar(v) for v in value) + "]"
    return _yaml_str(str(value))


def build_manifest(topics: Sequence[Topic]) -> str:
    """Render the manifest for a list of topics."""
    lines: list[str] = [
        "# course_manifest.yaml",
        "#",
        "# GENERATED FILE - do not edit by hand.",
        "# Source of truth: course_content/ (authored) -> tools/coursegen/build.py.",
        "# Regenerate with:  python tools/build_course.py",
        "#",
        "# Every validator in tools/ reads this file. If a topic is added to",
        "# course_content/, it appears here automatically on the next build.",
        "",
        "course:",
        f"  title: {_yaml_str('Python Master Course')}",
        f"  subtitle: {_yaml_str('Notebook-Based Python + Software Engineering + Robotics')}",
        "  project: ROBO-X",
        "  python_requires: \">=3.10\"",
        f"  module_count: {len(modules())}",
        f"  topic_count: {len(topics)}",
        "",
        "required_notebooks:",
    ]
    from .schema import REQUIRED_NOTEBOOKS, REQUIRED_DOCS

    lines += _yaml_list(REQUIRED_NOTEBOOKS)
    lines.append("required_docs:")
    lines += _yaml_list(REQUIRED_DOCS)
    lines.append("")
    lines.append("modules:")
    lines.append("")

    for module in modules():
        module_topics = [t for t in topics if t.module == module.number]
        lines.append(f"  - number: {module.number}")
        lines.append(f"    id: M{module.number}")
        lines.append(f"    title: {_yaml_str(module.title)}")
        lines.append(f"    directory: {_yaml_str(module.directory)}")
        lines.append(f"    robo_x_milestone: {_yaml_str(module.milestone)}")
        lines.append(f"    topic_count: {len(module_topics)}")
        lines.append("    topics:")
        for topic in module_topics:
            directory = f"{module.directory}/{topic.directory}"
            lines.append(f"      - id: {_yaml_str(topic.topic_id)}")
            lines.append(f"        title: {_yaml_str(topic.title)}")
            lines.append(f"        directory: {_yaml_str(directory)}")
            lines.append(
                "        prerequisites: "
                + _yaml_scalar([p.split(" ")[0] for p in topic.prerequisites])
            )
            lines.append(
                "        learning_objectives: "
                + _yaml_scalar([o.split(" ")[0] for o in topic.learning_objectives])
            )
            lines.append(f"        exercise_count: {topic.total_exercises}")
            lines.append(f"        medium_count: {topic.medium_count}")
            lines.append(f"        hard_count: {topic.hard_count}")
            lines.append(f"        quiz_count: {topic.quiz_count}")
            lines.append("        notebooks:")
            for name in REQUIRED_NOTEBOOKS:
                lines.append(f"          - {_yaml_str(f'{directory}/{name}')}")
            lines.append(
                f"        mini_project: {_yaml_str(f'{directory}/mini_project.ipynb')}"
            )
            lines.append(
                "        research_task: "
                + _yaml_str(topic.research.get("question", "")[:160])
            )
            lines.append(
                f"        robotics_challenge: "
                f"{_yaml_str(topic.robotics_challenge.get('title', ''))}"
            )
            lines.append(
                f"        robo_x_milestone: {_yaml_str(topic.robo_x_milestone)}"
            )
        lines.append("")

    lines.append("capstones:")
    for name in CAPSTONE_DIRS:
        lines.append(f"  - directory: {_yaml_str(f'10_capstone_projects/{name}')}")
        lines.append(
            f"    required: [{_yaml_str('README.md')}, {_yaml_str('requirements.md')}, "
            f"{_yaml_str('rubric.md')}, {_yaml_str('research.md')}, "
            f"{_yaml_str('starter/')}, {_yaml_str('tests/')}, {_yaml_str('solution/')}]"
        )
    lines.append("")
    return "\n".join(lines)


def write_manifest(topics: Sequence[Topic], root: Path) -> Path:
    path = root / "course_manifest.yaml"
    path.write_text(build_manifest(topics), encoding="utf-8")
    return path
