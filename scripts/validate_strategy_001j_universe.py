"""Validate the Strategy 001J point-in-time U1 membership table."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

REQUIRED = {"symbol", "effective_from", "effective_to"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", default="data/universe/u1_nifty100_membership.csv", nargs="?")
    args = parser.parse_args()

    path = Path(args.path)
    frame = pd.read_csv(path)
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {sorted(missing)}")

    frame["symbol"] = frame["symbol"].astype(str).str.upper().str.strip()
    frame["effective_from"] = pd.to_datetime(frame["effective_from"], errors="raise").dt.date
    frame["effective_to"] = pd.to_datetime(frame["effective_to"], errors="raise").dt.date

    if (frame["effective_from"] > frame["effective_to"]).any():
        raise SystemExit("Invalid membership interval: effective_from > effective_to")

    overlaps = []
    for symbol, group in frame.sort_values(["symbol", "effective_from"]).groupby("symbol"):
        previous_end = None
        for row in group.itertuples(index=False):
            if previous_end is not None and row.effective_from <= previous_end:
                overlaps.append(symbol)
            previous_end = row.effective_to

    if overlaps:
        raise SystemExit(f"Overlapping membership intervals: {sorted(set(overlaps))}")

    if frame["symbol"].eq("").any():
        raise SystemExit("Blank symbol found")

    print(f"Strategy 001J U1 membership validation PASSED: {len(frame)} intervals")


if __name__ == "__main__":
    main()
