"""Run the frozen 001D-parameter baseline across Strategy 001J U1 data.

This is a transfer baseline, not an optimizer. Point-in-time membership is
applied before signal construction so the current Nifty 100 list cannot leak
into historical periods.

Expected local layout:
    data/universe/strategy_001j_u1_membership.csv
    data/raw/strategy_001j_u1/<SYMBOL>.csv

CSV columns:
    timestamp,open,high,low,close,volume
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


def load_membership(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"symbol", "effective_from", "effective_to"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")
    df["symbol"] = df["symbol"].astype(str).str.upper().str.strip()
    df["effective_from"] = pd.to_datetime(df["effective_from"], utc=True, errors="raise")
    df["effective_to"] = pd.to_datetime(df["effective_to"], utc=True, errors="raise")
    return df


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


def apply_point_in_time_membership(
    symbol: str, frame: pd.DataFrame, membership: pd.DataFrame
) -> pd.DataFrame:
    intervals = membership[membership["symbol"] == symbol]
    if intervals.empty:
        raise ValueError(f"No point-in-time membership interval found for {symbol}")

    keep = pd.Series(False, index=frame.index)
    for row in intervals.itertuples(index=False):
        keep |= (frame.index >= row.effective_from) & (frame.index < row.effective_to)
    return frame.loc[keep]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--membership", default="data/universe/strategy_001j_u1_membership.csv")
    parser.add_argument("--input-dir", default="data/raw/strategy_001j_u1")
    parser.add_argument("--output-dir", default="data/reports/strategy_001j_baseline")
    parser.add_argument("--source-timezone", default=None)
    args = parser.parse_args()

    membership = load_membership(Path(args.membership))
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    frames: dict[str, pd.DataFrame] = {}
    for symbol in sorted(membership["symbol"].unique()):
        path = input_dir / f"{symbol}.csv"
        if not path.exists():
            raise SystemExit(f"Missing U1 data for {symbol}: {path}")
        raw = load_symbol_csv(path, args.source_timezone)
        frames[symbol] = apply_point_in_time_membership(symbol, raw, membership)

    # Exact frozen 001D parameter set. This is a transfer baseline, not a
    # parameter-selection run.
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
    print("Strategy 001J frozen-001D baseline complete.")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
