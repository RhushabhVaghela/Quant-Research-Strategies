"""Audit multiple saved 5-minute OHLCV datasets as a research universe."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.research.universe import apply_minimum_quality_filter, audit_directory


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Directory containing *_5minute.csv files")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path for the full universe audit CSV",
    )
    parser.add_argument("--min-trading-days", type=int, default=20)
    parser.add_argument("--min-rows", type=int, default=1000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = audit_directory(args.directory)

    if report.empty:
        print(f"No *_5minute.csv files found in {args.directory}")
        return

    print("Universe audit:")
    print(report.to_string(index=False))

    eligible = apply_minimum_quality_filter(
        report,
        min_trading_days=args.min_trading_days,
        min_rows=args.min_rows,
    )
    print("\nStructurally eligible candidates:")
    if eligible.empty:
        print("None")
    else:
        print(eligible[["symbol", "rows", "trading_days", "median_abs_5m_return"]].to_string(index=False))

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        report.to_csv(args.output, index=False)
        print(f"\nSaved universe audit to {args.output}")


if __name__ == "__main__":
    main()
