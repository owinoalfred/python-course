#!/usr/bin/env python3
"""Execute every code cell of an authored topic's lesson and solution notebooks."""
from __future__ import annotations

import json
import signal
import sys
from pathlib import Path

ROOT = Path("/home/alfredo/Documents/python course")
DIRS = {
    "1.1": "01_getting_started/01_introduction_to_python",
    "1.2": "01_getting_started/02_installing_python_ides_repl",
    "1.3": "01_getting_started/03_syntax_indentation_comments",
    "1.4": "01_getting_started/04_variables_naming_dynamic_typing",
    "1.5": "01_getting_started/05_core_data_types_conversion",
    "1.6": "01_getting_started/06_operators_and_expressions",
    "1.7": "01_getting_started/07_basic_input_output",
    "1.8": "01_getting_started/08_writing_running_first_scripts",
    "2.1": "02_control_flow/01_conditional_statements",
    "2.2": "02_control_flow/02_for_and_while_loops",
    "2.3": "02_control_flow/03_loop_control",
    "2.4": "02_control_flow/04_nested_loops_patterns",
    "2.5": "02_control_flow/05_range_enumerate_zip",
    "3.1": "03_data_structures/01_lists",
    "3.2": "03_data_structures/02_tuples",
    "3.3": "03_data_structures/03_sets",
}

failures: list[str] = []
system_exits: list[tuple] = []

def _alarm(signum, frame):  # noqa: ARG001
    raise TimeoutError("cell exceeded 15s")


signal.signal(signal.SIGALRM, _alarm)

_INPUT_ANSWERS = iter(["42", "alice", "10", "5", "hello", "3", "7", "2", "100", "0"])


def _fake_input(prompt: object = "") -> str:
    print(f"[stub input] {prompt}", end="")
    try:
        value = next(_INPUT_ANSWERS)
    except StopIteration:
        value = "1"
    print(value)
    return value


def run_cells(nb: dict, label: str, skip_student: bool = False) -> int:
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    executed = 0
    ns: dict = {"__name__": "__main__", "input": _fake_input}
    for index, cell in enumerate(code_cells, start=1):
        tags = set(cell.get("metadata", {}).get("tags", []))
        if skip_student and "student" in tags:
            continue
        source = "".join(cell["source"])
        print(f"  > {label} cell {index} ...", flush=True)
        signal.alarm(15)
        try:
            exec(compile(source, f"{label}:cell{index}", "exec"), ns)
            executed += 1
        except SystemExit as exc:
            executed += 1
            system_exits.append((label, index, exc.code))
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{label} cell {index}: {type(exc).__name__}: {exc}\n    {source.strip()[:160]}")
        finally:
            signal.alarm(0)
    return executed


for topic_id in sys.argv[1:] or list(DIRS):
    topic_dir = ROOT / DIRS[topic_id]
    lesson = json.loads((topic_dir / "lesson.ipynb").read_text(encoding="utf-8"))
    lesson_code = [c for c in lesson["cells"] if c["cell_type"] == "code"]
    sol = json.loads((topic_dir / "solution.ipynb").read_text(encoding="utf-8"))
    quiz = json.loads((topic_dir / "quiz.ipynb").read_text(encoding="utf-8"))

    n_lesson = run_cells(lesson, f"{topic_id}:lesson")
    n_sol = run_cells(sol, f"{topic_id}:solution", skip_student=True)

    letters = [
        "".join(c["source"]).split("— Answer: `")[1][0]
        for c in quiz["cells"]
        if c["cell_type"] == "markdown" and "— Answer: `" in "".join(c["source"])
    ]
    max_share = max(letters.count(l) for l in set(letters)) / len(letters)
    print(f"{topic_id}: lesson {len(lesson_code)} code cells (ran {n_lesson}), "
          f"solution {n_sol} cells, quiz letters {''.join(letters)} "
          f"(max {max_share:.0%})")

    if len(lesson_code) < 12:
        failures.append(f"{topic_id}: only {len(lesson_code)} code cells")
    if max_share > 0.40:
        failures.append(f"{topic_id}: answer share {max_share:.0%} exceeds 40%")

print()
print("=" * 60)
if system_exits:
    print("SystemExit raised (would kill a notebook kernel):")
    for label, index, code in system_exits:
        print(f"  - {label} cell {index} -> exit code {code}")
print("ALL CHECKS PASSED" if not failures else f"{len(failures)} FAILURES")
if failures:
    print(f"FAILURES ({len(failures)}):")
    for f in failures:
        print("  -", f)
    sys.exit(1)
