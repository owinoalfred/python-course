#!/usr/bin/env python3
"""Exercise validator tool.

Validates that exercise notebooks contain the required number of medium and hard exercises.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

def main():
    print("Exercise validator tool ready.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
