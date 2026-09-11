"""Audit a downloaded intraday OHLCV CSV.

Example:
    python scripts/audit_historical.py data/raw/NSE_NIFTYBEES_5minute.csv
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.audit import audit_ohlcv, daily_bar_counts, load_ohlcv_csv, time_of_day_profile
from src.data.validation import assert_valid


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit an intraday OHLCV dataset")
    parser.add_argument("path", type=Path)
    parser.add_argument("--interval", type=int, default=5)
    args = parser.parse_args()

    df = load_ohlcv_csv(args.path)
    assert_valid(df)
    report = audit_ohlcv(df, expected_minutes=args.interval)

    print(json.dumps(report.to_dict(), indent=2))
    print("\nDaily session summary:")
    print(daily_bar_counts(df).to_string())
    print("\nTime-of-day profile:")
    print(time_of_day_profile(df).to_string())


if __name__ == "__main__":
    main()
