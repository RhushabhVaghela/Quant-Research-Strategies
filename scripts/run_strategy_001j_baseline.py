"""Run the frozen 001D-parameter baseline across Strategy 001J U1 data.

Expected local layout:
    data/raw/strategy_001j_u1/<SYMBOL>.csv

CSV columns:
    timestamp,open,high,low,close,volume

The loader treats timezone-aware timestamps correctly. Naive timestamps are
rejected unless --source-timezone is supplied explicitly, preventing silent
UTC/local-time corruption.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.research.strategy_001j_cross_sectional import (
    Strategy001JConfig,
    run_universe,
    summarize_cross_section,
)


def load_symbol_csv(path: Path, source_timezone: str | None) -> pd.DataFrame:
    frame = pd.read_csv(path)
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")

    ts = pd.to_datetime(frame["timestamp"], errors="raise")
    if ts.dt.tz is None:
        if not source_timezone:
            raise ValueError(
                f"{path}: timestamps are naive; provide --source-timezone explicitly"
            )
        ts = ts.dt.tz_localize(source_timezone)
    ts = ts.dt.tz_convert("Asia/Kolkata")

    frame = frame.copy()
    frame["timestamp"] = ts
    frame = frame.set_index("timestamp").sort_index()
    if frame.index.has_duplicates:
        raise ValueError(f"{path}: duplicate timestamps")
    return frame


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/raw/strategy_001j_u1")
    parser.add_argument("--output-dir", default="data/reports/strategy_001j_baseline")
    parser.add_argument("--source-timezone", default=None)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    frames: dict[str, pd.DataFrame] = {}
    for path in sorted(input_dir.glob("*.csv")):
        symbol = path.stem.upper()
        frames[symbol] = load_symbol_csv(path, args.source_timezone)

    if not frames:
        raise SystemExit(f"No CSV files found in {input_dir}")

    # This is deliberately the exact 001D parameter set. It is a transfer
    # baseline, not a parameter-selection run.
    config = Strategy001JConfig(
        lookback_bars=30,
        z_threshold=2.0,
        trend_bars=6,
        holding_bars=6,
        cooldown_bars=12,
    )
    trades = run_universe(frames, config=config)
    summary = summarize_cross_section(trades)

    trades.to_csv(output_dir / "trades.csv", index=False)
    summary.to_csv(output_dir / "summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
