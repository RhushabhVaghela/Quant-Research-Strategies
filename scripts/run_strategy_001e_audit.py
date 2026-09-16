"""Run the frozen Strategy 001D trade-distribution and execution audit.

This script is diagnostic only. It does not search for profitable parameters.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from research.strategy_001e_audit import run_audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("trade_csv", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("data/reports/goldbees_strategy_001e_audit"))
    args = parser.parse_args()

    trades = pd.read_csv(args.trade_csv, parse_dates=["signal_timestamp", "entry_timestamp", "exit_timestamp"])
    report = run_audit(trades)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for name, frame in report.items():
        frame.to_csv(args.output_dir / f"{name}.csv", index=False)

    print(f"Audited {len(trades):,} trades")
    print(f"Wrote Strategy 001E audit outputs to {args.output_dir}")
    print(report["summary"].to_string(index=False))


if __name__ == "__main__":
    main()
