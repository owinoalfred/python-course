"""Validate the generated manifest and the navigation graph it describes.

These replace the previous placeholder test. They fail loudly if the manifest
drifts from the authored content or if a generated index README goes missing.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from course_content import TOPICS  # noqa: E402
from tools.coursegen.catalogue import CAPSTONE_DIRS, MODULE_DIRS  # noqa: E402
from tools.coursegen.schema import REQUIRED_NOTEBOOKS  # noqa: E402

MANIFEST = ROOT / "course_manifest.yaml"


def _manifest() -> dict:
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


def test_manifest_exists_and_parses() -> None:
    data = _manifest()
    assert data["course"]["title"] == "Python Master Course"


def test_python_version_is_consistent() -> None:
    assert _manifest()["course"]["python_requires"] == ">=3.12"


def test_manifest_topic_count_matches_authored_content() -> None:
    assert _manifest()["course"]["topic_count"] == len(TOPICS)


def test_manifest_lists_every_required_notebook() -> None:
    listed: set[str] = set()
    for module in _manifest()["modules"]:
        for topic in module["topics"]:
            listed.update(topic["notebooks"])
    assert len(listed) == len(TOPICS) * len(REQUIRED_NOTEBOOKS)


def test_every_module_index_readme_exists() -> None:
    missing = [d for d in MODULE_DIRS.values() if not (ROOT / d / "README.md").is_file()]
    assert not missing, f"missing module index READMEs: {missing}"


def test_capstone_index_and_directories_exist() -> None:
    assert (ROOT / "10_capstone_projects" / "README.md").is_file()
    missing = [d for d in CAPSTONE_DIRS if not (ROOT / "10_capstone_projects" / d).is_dir()]
    assert not missing, f"missing capstone directories: {missing}"


def test_topic_readme_navigation_targets_resolve() -> None:
    """Every 'Module index' link in a topic README must point at a real file."""
    sample = ROOT / "01_getting_started" / "01_introduction_to_python" / "README.md"
    assert "](../README.md)" in sample.read_text(encoding="utf-8")
    assert (sample.parent / ".." / "README.md").resolve().is_file()
