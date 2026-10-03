"""Low-level Jupyter Notebook (nbformat v4) construction helpers.

This module is deliberately dependency-free: the course must be buildable with
a bare Python 3.10+ interpreter, so notebooks are emitted as plain JSON that
exactly matches the nbformat v4 schema.

Every notebook produced here validates with::

    python tools/notebook_validator.py <notebook.ipynb>
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Sequence

Cell = dict[str, Any]


# --------------------------------------------------------------------------- #
# Cell builders
# --------------------------------------------------------------------------- #
def _as_source(text: str) -> list[str]:
    """Split text into nbformat source lines (last line has no newline)."""
    if text == "":
        return []
    lines = text.rstrip("\n").split("\n")
    return [line + "\n" for line in lines[:-1]] + [lines[-1]]


def md(text: str) -> Cell:
    """Build a markdown cell."""
    return {"cell_type": "markdown", "metadata": {}, "source": _as_source(text.rstrip())}


def code(text: str, *, tags: Sequence[str] = ()) -> Cell:
    """Build a code cell, optionally tagged for nbconvert/grader tooling."""
    metadata: dict[str, Any] = {}
    if tags:
        metadata["tags"] = list(tags)
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": metadata,
        "outputs": [],
        "source": _as_source(text.strip("\n")),
    }


def raw(text: str) -> Cell:
    """Build an unformatted-cell (used rarely, e.g. for hidden solution keys)."""
    return {"cell_type": "raw", "metadata": {}, "source": _as_source(text.rstrip())}


# --------------------------------------------------------------------------- #
# Composite markdown helpers
# --------------------------------------------------------------------------- #
def bullets(items: Iterable[str], *, indent: int = 0) -> str:
    """Render an iterable as a markdown bullet list."""
    pad = " " * indent
    return "\n".join(f"{pad}- {item}" for item in items)


def numbered(items: Iterable[str], *, start: int = 1, indent: int = 0) -> str:
    """Render an iterable as a markdown ordered list."""
    pad = " " * indent
    return "\n".join(f"{pad}{i}. {item}" for i, item in enumerate(items, start=start))


def table(headers: Sequence[str], rows: Iterable[Sequence[Any]]) -> str:
    """Render a GitHub-flavoured markdown table."""
    def clean(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    head = "| " + " | ".join(clean(h) for h in headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(clean(c) for c in row) + " |" for row in rows]
    return "\n".join([head, sep, *body])


def fenced(block: str, lang: str = "python") -> str:
    """Wrap a block of text in a fenced code block."""
    return f"```{lang}\n{block.rstrip()}\n```"


def admonition(kind: str, title: str, body: str) -> str:
    """Render a callout box using blockquote + bold label."""
    lines = [f"> **{title}**", ">"]
    lines.extend(f"> {line}" if line else ">" for line in body.strip().split("\n"))
    return "\n".join(lines)


def hr() -> str:
    return "\n---\n"


# --------------------------------------------------------------------------- #
# Notebook assembly
# --------------------------------------------------------------------------- #
def notebook(cells: Sequence[Cell], *, kernel: str = "python3") -> dict[str, Any]:
    """Wrap cells into a complete nbformat v4 document."""
    return {
        "cells": list(cells),
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": kernel,
            },
            "language_info": {
                "name": "python",
                "version": "3.12",
                "mimetype": "text/x-python",
                "file_extension": ".py",
                "pygments_lexer": "ipython3",
                "codemirror_mode": {"name": "ipython", "version": 3},
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_notebook(path: Path, nb: dict[str, Any]) -> Path:
    """Serialise a notebook to disk, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def save(path: Path, cells: Sequence[Cell]) -> Path:
    """Convenience: build + write in one call."""
    return write_notebook(path, notebook(cells))


def check_syntax(source: str, *, where: str = "cell") -> tuple[bool, str]:
    """Compile-check a code string. Returns ``(ok, error_message)``."""
    import ast

    try:
        ast.parse(source)
    except SyntaxError as exc:  # pragma: no cover - exercised by validators
        return False, f"{where}: line {exc.lineno}: {exc.msg}"
    return True, ""
