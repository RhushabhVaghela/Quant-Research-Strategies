"""Audit local 001J U1 5-minute OHLCV coverage before backtesting."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def audit_file(path: Path, source_timezone: str | None) -> dict:
    frame = pd.read_csv(path)
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")

    ts = pd.to_datetime(frame["timestamp"], errors="raise")
    if ts.dt.tz is None:
        if not source_timezone:
            raise ValueError(f"{path}: naive timestamps; provide --source-timezone")
        ts = ts.dt.tz_localize(source_timezone)
    ts = ts.dt.tz_convert("Asia/Kolkata")

    duplicate_count = int(ts.duplicated().sum())
    ordered = ts.is_monotonic_increasing
    positive_ohlc = (frame[["open", "high", "low", "close"]] > 0).all().all()
    volume_nonnegative = (frame["volume"] >= 0).all()

    return {
        "symbol": path.stem.upper(),
        "rows": len(frame),
        "first_timestamp": ts.min().isoformat(),
        "last_timestamp": ts.max().isoformat(),
        "duplicate_timestamps": duplicate_count,
        "chronological": bool(ordered),
        "positive_ohlc": bool(positive_ohlc),
        "nonnegative_volume": bool(volume_nonnegative),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/raw/strategy_001j_u1")
    parser.add_argument("--output", default="data/reports/strategy_001j_u1_data_audit.csv")
    parser.add_argument("--source-timezone", default=None)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    paths = sorted(input_dir.glob("*.csv"))
    if not paths:
        raise SystemExit(f"No CSV files found in {input_dir}")

    rows = [audit_file(path, args.source_timezone) for path in paths]
    report = pd.DataFrame(rows)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(args.output, index=False)

    failed = report[
        (report["duplicate_timestamps"] > 0)
        | (~report["chronological"])
        | (~report["positive_ohlc"])
        | (~report["nonnegative_volume"])
    ]
    print(report.to_string(index=False))
    if not failed.empty:
        raise SystemExit(f"U1 data audit FAILED for {len(failed)} symbol(s)")
    print(f"U1 data audit PASSED for {len(report)} symbol(s).")


if __name__ == "__main__":
    main()
