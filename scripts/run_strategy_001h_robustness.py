"""Run Strategy 001H predefined robustness and chronological validation."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.research.strategy_001h_robustness import run_robustness
from src.research.strategy_001g_replay import load_ohlcv


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_csv", type=Path)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/reports/goldbees_strategy_001h_robustness"),
    )
    args = parser.parse_args()

    data = load_ohlcv(args.data_csv)
    report = run_robustness(data)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for name, frame in report.items():
        frame.to_csv(args.output_dir / f"{name}.csv", index=False)

    trades = report["trades"]
    print(f"Ran frozen Strategy 001D across {len(trades):,} trades")
    print("\nChronological performance:")
    print(report["chronological_performance"].to_string(index=False))
    print("\nDevelopment vs chronological holdout:")
    print(report["development_vs_holdout"].to_string(index=False))
    print("\nCost sensitivity:")
    print(report["cost_sensitivity"].to_string(index=False))
    print(f"\nWrote Strategy 001H outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
