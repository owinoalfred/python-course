#!/usr/bin/env python3
"""Custom tool to check Python files for syntax errors across the repo."""

import ast
import sys
from pathlib import Path

def main():
    root = Path.cwd()
    errors = 0
    py_files = list(root.rglob("*.py"))
    print(f"Checking {len(py_files)} python files...")
    for path in py_files:
        if ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except Exception as e:
            print(f"SYNTAX ERROR in {path.relative_to(root)}: {e}")
            errors += 1
    if errors == 0:
        print("All Python files parsed successfully!")
    sys.exit(errors)

if __name__ == "__main__":
    main()
