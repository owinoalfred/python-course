"""Render DSL blocks into notebook cells.

Kept separate from the builders so that block formatting is defined exactly
once and every generated notebook is structurally identical.
"""

from __future__ import annotations

from typing import Any, Iterable, Sequence

from . import nb
from .dsl import Block

LABELS = {"a": "A", "b": "B", "c": "C", "d": "D", "e": "E", "f": "F"}


def _bullets(items: Iterable[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _steps(items: Sequence[str], start: int) -> str:
    return "\n".join(f"{i}. {item}" for i, item in enumerate(items, start=start))


def _table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    head = "| " + " | ".join(cell(h) for h in headers) + " |"
    rule = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(cell(c) for c in row) + " |" for row in rows]
    return "\n".join([head, rule, *body])


def block_text(block: Block) -> str:
    """Best-effort plain-text extraction from a block (for word counting)."""
    kind = block.kind
    payload = block.payload
    if kind in {"md", "raw_md", "equation"}:
        return str(payload)
    if kind in {"code", "code_cell"}:
        return str(payload[0])
    if kind == "bullets":
        return "\n".join(str(item) for item in payload)
    if kind == "steps":
        items, _start = payload
        return "\n".join(str(item) for item in items)
    if kind == "table":
        headers, rows = payload
        cell = [str(h) for h in headers]
        for row in rows:
            cell.extend(str(c) for c in row)
        return "\n".join(cell)
    if kind in {"note", "warn", "tip"}:
        title, body = payload
        return f"{title}\n{body}"
    return ""


def block_to_cells(block: Block, *, topic_id: str = "") -> list[dict[str, Any]]:
    """Convert one block into zero or more notebook cells."""
    kind = block.kind
    if kind == "md":
        return [nb.md(block.payload)]
    if kind == "raw_md":
        return [nb.md(block.payload)]
    if kind == "code":
        source, lang = block.payload
        if lang == "python":
            ok, err = nb.check_syntax(source, where=f"{topic_id}:code")
            if not ok:
                raise SyntaxError(f"invalid Python in content ({err})\n---\n{source}")
        return [nb.md(nb.fenced(source, lang))]
    if kind == "code_cell":
        source, tags = block.payload
        ok, err = nb.check_syntax(source, where=f"{topic_id}:code_cell")
        if not ok:
            raise SyntaxError(f"invalid Python in code cell ({err})\n---\n{source}")
        return [nb.code(source, tags=tags)]
    if kind == "bullets":
        return [nb.md(_bullets(block.payload))]
    if kind == "steps":
        items, start = block.payload
        return [nb.md(_steps(items, start))]
    if kind == "table":
        headers, rows = block.payload
        return [nb.md(_table(headers, rows))]
    if kind in {"note", "warn", "tip"}:
        title, body = block.payload
        icon = {"note": "Note", "warn": "Warning", "tip": "Tip"}[kind]
        return [nb.md(nb.admonition(icon, title, body))]
    if kind == "equation":
        return [nb.md(nb.fenced(block.payload, "text"))]
    raise ValueError(f"unknown block kind: {kind!r}")


def blocks_to_cells(blocks: Iterable[Block], *, topic_id: str = "") -> list[dict[str, Any]]:
    cells: list[dict[str, Any]] = []
    for block in blocks:
        cells.extend(block_to_cells(block, topic_id=topic_id))
    return cells


def markdown_block(text: str) -> Block:
    """Convenience re-export so builders only import from one module."""
    from .dsl import MD

    return MD(text)
