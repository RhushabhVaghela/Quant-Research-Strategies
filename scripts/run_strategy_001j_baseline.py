"""Run the frozen 001D-parameter baseline across Strategy 001J U1 data.

This is a transfer baseline, not an optimizer. The caller must supply the
frozen experiment window so the run cannot silently expand to all available
history in the local U1 files.
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


def _window_timestamp(value: str, end_of_day: bool = False) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    if ts.tzinfo is None:
        ts = ts.tz_localize("Asia/Kolkata")
    else:
        ts = ts.tz_convert("Asia/Kolkata")
    if end_of_day and len(value) == 10:
        ts = ts + pd.Timedelta(days=1)
    return ts


def load_symbol_csv(
    path: Path,
    source_timezone: str | None,
    start: pd.Timestamp,
    end_exclusive: pd.Timestamp,
) -> pd.DataFrame:
    frame = pd.read_csv(path)
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")

    ts = pd.to_datetime(frame["timestamp"], errors="raise")
    if ts.dt.tz is None:
        if not source_timezone:
            raise ValueError(f"{path}: timestamps are naive; provide --source-timezone explicitly")
        ts = ts.dt.tz_localize(source_timezone)
    ts = ts.dt.tz_convert("Asia/Kolkata")

    frame = frame.copy()
    frame["timestamp"] = ts
    frame = frame.set_index("timestamp").sort_index()
    if frame.index.has_duplicates:
        raise ValueError(f"{path}: duplicate timestamps")
    return frame.loc[(frame.index >= start) & (frame.index < end_exclusive)]


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
    parser.add_argument("--start", default="2026-05-12", help="Inclusive frozen experiment start date")
    parser.add_argument("--end", default="2026-09-17", help="Inclusive frozen experiment end date")
    parser.add_argument("--source-timezone", default=None)
    args = parser.parse_args()

    start = _window_timestamp(args.start)
    end_exclusive = _window_timestamp(args.end, end_of_day=True)
    if end_exclusive <= start:
        raise SystemExit("Experiment end must be on or after experiment start.")

    membership = load_membership(Path(args.membership))
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    frames: dict[str, pd.DataFrame] = {}
    for symbol in sorted(membership["symbol"].unique()):
        path = input_dir / f"{symbol}.csv"
        if not path.exists():
            raise SystemExit(f"Missing U1 data for {symbol}: {path}")
        raw = load_symbol_csv(path, args.source_timezone, start, end_exclusive)
        frames[symbol] = apply_point_in_time_membership(symbol, raw, membership)

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
    print(f"Frozen experiment window: {start.date()} through {(end_exclusive - pd.Timedelta(days=1)).date()}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
