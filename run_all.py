#!/usr/bin/env python3
"""Run All / Complete Course Build & Audit Tool.

Executing this script builds all Jupyter notebooks (.ipynb files), regenerates
the course manifest, audits repository integrity, and executes unit tests.

Usage::

    python3 run_all.py
"""

import sys
import subprocess
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent
    print("=" * 60)
    print("RUNNING COMPLETE PYTHON MASTER COURSE BUILD & AUDIT")
    print("=" * 60)

    # 1. Build all course notebooks and docs
    print("\n[1/3] Building all course notebooks (.ipynb) and documentation...")
    build_cmd = [sys.executable, str(root / "tools" / "build_course.py")]
    res = subprocess.run(build_cmd, cwd=root)
    if res.returncode != 0:
        print("ERROR: Course build failed!", file=sys.stderr)
        return res.returncode

    # 2. Run course integrity audit
    print("\n[2/3] Auditing course repository integrity...")
    audit_cmd = [sys.executable, str(root / "tools" / "course_integrity_checker.py")]
    res = subprocess.run(audit_cmd, cwd=root)
    if res.returncode != 0:
        print("ERROR: Course integrity check failed!", file=sys.stderr)
        return res.returncode

    # 3. Execute unit tests
    print("\n[3/3] Executing test suite with pytest...")
    test_cmd = [sys.executable, "-m", "pytest"]
    res = subprocess.run(test_cmd, cwd=root)
    if res.returncode != 0:
        print("ERROR: Test suite failed!", file=sys.stderr)
        return res.returncode

    print("\n" + "=" * 60)
    print("SUCCESS: ALL NOTEBOOKS CREATED, AUDITED, AND VERIFIED!")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
