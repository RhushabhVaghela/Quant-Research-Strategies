"""Run the frozen Strategy 001D baseline backtest.

Example:
    python scripts/run_strategy_001_backtest.py data/raw/NSE_GOLDBEES_5minute.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

from run_mean_reversion_event_study import load_ohlcv
from src.research.continuation_backtest import CostScenario, run_scenarios


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/reports/goldbees_strategy_001d_backtest"),
    )
    args = parser.parse_args()

    df = load_ohlcv(args.csv)
    scenarios = [
        CostScenario("gross", 0.0, 0.0),
        # Transparent sensitivity scenarios only; they are not claimed to be
        # measured historical execution costs.
        CostScenario("moderate_cost_sensitivity", 5.0, 2.0),
        CostScenario("stress_cost_sensitivity", 10.0, 5.0),
    ]
    summary, trades = run_scenarios(df, scenarios)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output_dir / "performance_summary.csv", index=False)
    for name, table in trades.items():
        table.to_csv(args.output_dir / f"trades_{name}.csv", index=False)

    print(f"Rows: {len(df):,}")
    print(f"Wrote Strategy 001D backtest outputs to {args.output_dir}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
