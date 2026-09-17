"""Validate PIT membership and raw-data coverage for a frozen 001J window.

This is a pre-backtest gate. It does not create membership, infer missing
symbols, or select a universe. A window must be supplied so data sufficiency
is evaluated against the exact research period rather than an arbitrary file
coverage claim.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

REQUIRED_MEMBERSHIP = {"symbol", "effective_from", "effective_to"}
REQUIRED_BARS = {"timestamp", "open", "high", "low", "close", "volume"}


def _parse_window(start: str, end: str) -> tuple[pd.Timestamp, pd.Timestamp]:
    left = pd.Timestamp(start)
    right = pd.Timestamp(end)
    if left.tzinfo is None:
        left = left.tz_localize("Asia/Kolkata")
    else:
        left = left.tz_convert("Asia/Kolkata")
    if right.tzinfo is None:
        right = right.tz_localize("Asia/Kolkata")
    else:
        right = right.tz_convert("Asia/Kolkata")
    if right <= left:
        raise SystemExit("Research end must be later than research start.")
    return left, right


def _load_membership(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise SystemExit(f"Membership file not found: {path}")
    df = pd.read_csv(path)
    missing = REQUIRED_MEMBERSHIP - set(df.columns)
    if missing:
        raise SystemExit(f"Membership missing columns: {sorted(missing)}")
    if df.empty:
        raise SystemExit("U1 membership is empty; load PIT historical membership first.")
    df = df.copy()
    df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()
    df["effective_from"] = pd.to_datetime(df["effective_from"], errors="raise")
    df["effective_to"] = pd.to_datetime(df["effective_to"], errors="raise")
    return df


def _load_bar_bounds(path: Path) -> tuple[pd.Timestamp, pd.Timestamp]:
    frame = pd.read_csv(path, usecols=lambda c: c in REQUIRED_BARS)
    missing = REQUIRED_BARS - set(frame.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")
    ts = pd.to_datetime(frame["timestamp"], errors="raise")
    if ts.dt.tz is None:
        ts = ts.dt.tz_localize("Asia/Kolkata")
    else:
        ts = ts.dt.tz_convert("Asia/Kolkata")
    if ts.empty:
        raise ValueError(f"{path}: no rows")
    return ts.min(), ts.max()


def validate(membership_path: Path, data_dir: Path, start: str, end: str) -> pd.DataFrame:
    window_start, window_end = _parse_window(start, end)
    membership = _load_membership(membership_path)
    membership["_start"] = membership["effective_from"].apply(lambda x: x.tz_localize("Asia/Kolkata") if x.tzinfo is None else x.tz_convert("Asia/Kolkata"))
    membership["_end"] = membership["effective_to"].apply(lambda x: x.tz_localize("Asia/Kolkata") if x.tzinfo is None else x.tz_convert("Asia/Kolkata"))

    active = membership[(membership["_start"] < window_end) & (membership["_end"] > window_start)]
    required_symbols = sorted(active["symbol"].unique())
    if not required_symbols:
        raise SystemExit("No U1 symbols are active in the requested research window.")

    rows: list[dict] = []
    for symbol in required_symbols:
        path = data_dir / f"{symbol}.csv"
        if not path.exists():
            rows.append({"symbol": symbol, "status": "missing_file", "first_timestamp": None, "last_timestamp": None})
            continue
        try:
            first, last = _load_bar_bounds(path)
            status = "ok" if first <= window_start and last >= window_end else "insufficient_window_coverage"
            rows.append({"symbol": symbol, "status": status, "first_timestamp": first.isoformat(), "last_timestamp": last.isoformat()})
        except (ValueError, pd.errors.ParserError) as exc:
            rows.append({"symbol": symbol, "status": f"invalid_data: {exc}", "first_timestamp": None, "last_timestamp": None})

    report = pd.DataFrame(rows).sort_values("symbol").reset_index(drop=True)
    failed = report[report["status"] != "ok"]
    if not failed.empty:
        raise SystemExit(f"001J data gate FAILED for {len(failed)} of {len(report)} required symbols.")
    print(f"001J data gate PASSED: {len(report)} required U1 symbols cover {window_start.isoformat()} to {window_end.isoformat()}.")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--membership", default="data/universe/strategy_001j_u1_membership.csv")
    parser.add_argument("--data-dir", default="data/raw/strategy_001j_u1")
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--output", default="data/reports/strategy_001j_data_gate.csv")
    args = parser.parse_args()
    report = validate(Path(args.membership), Path(args.data_dir), args.start, args.end)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(output, index=False)


if __name__ == "__main__":
    main()
