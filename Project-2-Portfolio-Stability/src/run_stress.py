"""Command-line runner for a single, non-locked Project 2 stress case."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

SRC_DIRECTORY = Path(__file__).resolve().parent
if str(SRC_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SRC_DIRECTORY))

from stress_tests import StressCase, StressInputs, run_project_stress_case


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run one analytical-only Project 2 stress case. Do not use this command for the locked case until its record is committed."
    )
    parser.add_argument("--name", required=True, help="Descriptive case name.")
    parser.add_argument("--description", required=True, help="One-input-at-a-time rationale.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--window-returns", type=int, help="Trailing approved monthly returns for estimation-window sensitivity.")
    group.add_argument("--return-shift-bps", type=float, help="Hypothetical monthly return shift in basis points.")
    group.add_argument("--risk-multiplier", type=float, help="Hypothetical multiplier for monthly deviations around the sample mean.")
    group.add_argument("--hypothetical-cost-bps", type=float, help="Unsourced one-way cost sensitivity in basis points per turnover unit.")
    group.add_argument("--turnover-cap", type=float, help="Constraint sensitivity: maximum one-way turnover as a decimal.")
    group.add_argument("--bil-scenario-floor", type=float, help="Student-proposed BIL scenario floor as a decimal.")
    return parser.parse_args()


def inputs_from_args(args: argparse.Namespace) -> StressInputs:
    if args.window_returns is not None:
        return StressInputs(estimation_window_returns=args.window_returns)
    if args.return_shift_bps is not None:
        return StressInputs(monthly_return_shift=args.return_shift_bps / 10_000)
    if args.risk_multiplier is not None:
        return StressInputs(monthly_risk_multiplier=args.risk_multiplier)
    if args.hypothetical_cost_bps is not None:
        return StressInputs(hypothetical_one_way_cost_bps=args.hypothetical_cost_bps)
    if args.turnover_cap is not None:
        return StressInputs(turnover_cap=args.turnover_cap)
    return StressInputs(bil_scenario_floor=args.bil_scenario_floor)


def main() -> None:
    args = parse_args()
    run = run_project_stress_case(StressCase(args.name, inputs_from_args(args), args.description))
    print(json.dumps(asdict(run), indent=2, default=str))


if __name__ == "__main__":
    main()
