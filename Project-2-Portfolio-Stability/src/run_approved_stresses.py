"""Run the five documented non-locked, student-proposed approved-data sensitivities."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SRC_DIRECTORY = Path(__file__).resolve().parent
if str(SRC_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SRC_DIRECTORY))

from stress_tests import APPROVED_NONLOCKED_CASES, run_project_stress_case, stress_summary


def main() -> None:
    print(json.dumps([stress_summary(run_project_stress_case(case)) for case in APPROVED_NONLOCKED_CASES], indent=2, default=str))


if __name__ == "__main__":
    main()
