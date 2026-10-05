"""Pytest bootstrap: make the repository root importable for every test.

The course packages (``shared``, ``course_content``, ``tools``, ``robo_x``) are
imported by tests from all over the tree. Adding the repository root here keeps
``pytest`` working regardless of the working directory it is launched from.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
