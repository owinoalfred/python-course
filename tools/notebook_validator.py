"""Notebook validation for the Python Master Course.

Validates individual notebooks and whole topic directories against the
structural contract in ``tools.coursegen.schema``.

Usage::

    python tools/notebook_validator.py                        # every topic
    python tools/notebook_validator.py 01_getting_started/01_introduction_to_python
    python tools/notebook_validator.py path/to/lesson.ipynb
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.coursegen.schema import REQUIRED_DOCS, REQUIRED_NOTEBOOKS  # noqa: E402


def validate_notebook_file(path: Path) -> tuple[bool, list[str]]:
    """Verify that a notebook file is valid JSON with a usable cell array."""
    errors: list[str] = []
    if not path.exists():
        return False, [f"File missing: {path}"]
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:  # noqa: BLE001
        return False, [f"Invalid JSON in {path}: {exc}"]

    if "cells" not in data or not isinstance(data["cells"], list):
        errors.append("Notebook missing 'cells' array")
    elif len(data["cells"]) == 0:
        errors.append("Notebook is empty (0 cells)")

    for cell in data.get("cells", []):
        if cell.get("cell_type") not in {"markdown", "code", "raw"}:
            errors.append(f"Unknown cell type: {cell.get('cell_type')!r}")
            break
        if not isinstance(cell.get("source"), (list, str)):
            errors.append("Cell 'source' must be a string or list of lines")
            break
    return not errors, errors


def validate_topic_directory(path: Path) -> tuple[bool, list[str]]:
    """Verify that a topic directory contains every required artefact."""
    errors: list[str] = []
    if not path.is_dir():
        return False, [f"Not a directory: {path}"]
    for nb_name in REQUIRED_NOTEBOOKS:
        ok, nb_errors = validate_notebook_file(path / nb_name)
        if not ok:
            errors.extend(nb_errors)
    for doc_name in REQUIRED_DOCS:
        if not (path / doc_name).is_file():
            errors.append(f"Missing document: {path / doc_name}")
    return not errors, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate course notebooks.")
    parser.add_argument("paths", nargs="*", help="notebook files or topic directories")
    parser.add_argument(
        "--all", action="store_true", help="validate every built topic directory"
    )
    args = parser.parse_args(argv)

    targets: list[Path] = []
    if args.all or not args.paths:
        # Discover topics from the authored content rather than by walking the
        # filesystem, so renamed directories are caught immediately.
        from course_content import TOPICS
        from tools.coursegen.catalogue import module_dir

        targets = [ROOT / module_dir(t.module) / t.directory for t in TOPICS]
    else:
        targets = [Path(p) for p in args.paths]

    failures = 0
    for target in targets:
        if target.is_dir():
            ok, errors = validate_topic_directory(target)
            label = f"{target.relative_to(ROOT)}/"
        else:
            ok, errors = validate_notebook_file(target)
            label = target.name
        if ok:
            print(f"OK    {label}")
        else:
            failures += 1
            print(f"FAIL  {label}")
            for error in errors:
                print(f"      {error}")

    print("-" * 60)
    print(f"Validated {len(targets)} target(s); {failures} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
