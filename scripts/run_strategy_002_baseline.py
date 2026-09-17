"""Run the Strategy 002 cross-sectional baseline on local per-symbol 5-minute CSVs.

Expected layout:
    data/raw/strategy_002_u1/<SYMBOL>.csv

Each CSV must contain timestamp, open, high, low, close, volume.
The script deliberately does not optimize parameters.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.research.strategy_002_cross_sectional import (
    Strategy002Config,
    run_universe,
    summarize_cross_section,
)


def _load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True).dt.tz_convert("Asia/Kolkata")
    df = df.sort_values("timestamp").drop_duplicates("timestamp", keep="last").set_index("timestamp")
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"])
    return df


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/raw/strategy_002_u1")
    parser.add_argument("--output-dir", default="data/reports/strategy_002_baseline")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    paths = sorted(input_dir.glob("*.csv"))
    if not paths:
        raise SystemExit(f"No CSV files found in {input_dir}")

    frames = {path.stem.upper(): _load_csv(path) for path in paths}
    config = Strategy002Config()
    trades = run_universe(frames, config=config)
    summary = summarize_cross_section(trades)

    output_dir.mkdir(parents=True, exist_ok=True)
    trades.to_csv(output_dir / "trades.csv", index=False)
    summary.to_csv(output_dir / "summary.csv", index=False)

    print("Strategy 002 baseline complete")
    print(f"Symbols loaded: {len(frames)}")
    print(f"Trades: {len(trades)}")
    print(summary.to_string(index=False))
    print(f"Trade table: {output_dir / 'trades.csv'}")
    print(f"Summary: {output_dir / 'summary.csv'}")


if __name__ == "__main__":
    main()
