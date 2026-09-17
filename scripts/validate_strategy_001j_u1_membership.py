"""Validate Strategy 001J U1 point-in-time membership data.

The validator intentionally fails while the repository still contains only the
empty template. This prevents a current-only constituent list from silently
entering historical research.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

REQUIRED = ["symbol", "effective_from", "effective_to"]


def validate(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Membership file not found: {path}")

    df = pd.read_csv(path)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing required columns: {missing}")
    if df.empty:
        raise SystemExit(
            "U1 membership is empty. Load point-in-time historical Nifty 100 "
            "membership before running Strategy 001J research."
        )

    df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()
    if (df["symbol"] == "").any():
        raise SystemExit("Membership contains blank symbols.")

    start = pd.to_datetime(df["effective_from"], errors="coerce")
    end = pd.to_datetime(df["effective_to"], errors="coerce")
    if start.isna().any() or end.isna().any():
        raise SystemExit("Membership contains invalid effective dates.")
    if (end <= start).any():
        raise SystemExit("Every effective_to must be later than effective_from.")

    # Treat intervals as half-open: [effective_from, effective_to).
    # This permits adjacent reconstitution periods without overlap.
    for symbol, group in df.assign(_start=start, _end=end).groupby("symbol"):
        g = group.sort_values("_start")
        if g["_start"].duplicated().any():
            raise SystemExit(f"Duplicate effective_from for {symbol}.")
        if (g["_start"].iloc[1:].to_numpy() < g["_end"].iloc[:-1].to_numpy()).any():
            raise SystemExit(f"Overlapping membership intervals for {symbol}.")

    print(f"Strategy 001J U1 membership validation PASSED: {len(df)} intervals, {df['symbol'].nunique()} symbols.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default="data/universe/strategy_001j_u1_membership.csv",
    )
    args = parser.parse_args()
    validate(Path(args.path))
