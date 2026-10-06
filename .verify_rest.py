#!/usr/bin/env python3
"""Execute non-student code cells of exercises/mini_project/robotics/research notebooks."""
from __future__ import annotations

import json
import signal
import sys
from pathlib import Path

ROOT = Path("/home/alfredo/Documents/python course")
DIRS = {
    "2.1": "02_control_flow/01_conditional_statements",
    "2.2": "02_control_flow/02_for_and_while_loops",
    "2.3": "02_control_flow/03_loop_control",
    "2.4": "02_control_flow/04_nested_loops_patterns",
    "2.5": "02_control_flow/05_range_enumerate_zip",
}
FILES = ["exercises.ipynb", "mini_project.ipynb", "robotics_challenge.ipynb", "research.ipynb", "quiz.ipynb"]

failures: list[str] = []


def _alarm(signum, frame):  # noqa: ARG001
    raise TimeoutError("cell exceeded 20s")


signal.signal(signal.SIGALRM, _alarm)

answers = iter(["42", "alice", "10", "5", "hello", "3", "7", "2", "100", "0", "1", "9", "4", "6", "8"])


def _fake_input(prompt: object = "") -> str:
    try:
        return next(answers)
    except StopIteration:
        return "1"


for topic_id in sys.argv[1:] or list(DIRS):
    topic_dir = ROOT / DIRS[topic_id]
    for fname in FILES:
        nb = json.loads((topic_dir / fname).read_text(encoding="utf-8"))
        ns: dict = {"__name__": "__main__", "input": _fake_input}
        cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
        ran = 0
        for i, cell in enumerate(cells, 1):
            if "student" in cell.get("metadata", {}).get("tags", []):
                continue
            src = "".join(cell["source"])
            print(f"  > {topic_id}:{fname} cell {i} ...", flush=True)
            signal.alarm(20)
            try:
                exec(compile(src, f"{topic_id}:{fname}:{i}", "exec"), ns)
                ran += 1
            except SystemExit:
                ran += 1
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{topic_id}:{fname} cell {i}: {type(exc).__name__}: {exc}\n    {src.strip()[:160]}")
            finally:
                signal.alarm(0)
        print(f"{topic_id} {fname}: {ran}/{len(cells)} cells ran", flush=True)

print()
print("ALL CHECKS PASSED" if not failures else f"{len(failures)} FAILURES")
for f in failures:
    print("  -", f)
sys.exit(1 if failures else 0)
