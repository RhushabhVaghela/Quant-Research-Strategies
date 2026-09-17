"""Validate the Strategy 002 point-in-time universe membership table."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default="data/universe/u1_nifty100_membership.csv",
    )
    args = parser.parse_args()

    path = Path(args.path)
    df = pd.read_csv(path)
    required = {"symbol", "effective_from", "effective_to"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {sorted(missing)}")

    df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()
    df["effective_from"] = pd.to_datetime(df["effective_from"], errors="coerce").dt.normalize()
    df["effective_to"] = pd.to_datetime(df["effective_to"], errors="coerce").dt.normalize()

    if df[["symbol", "effective_from"]].isna().any().any():
        raise SystemExit("Universe contains blank/invalid symbol or effective_from values")
    if (df["effective_to"].notna() & (df["effective_to"] < df["effective_from"])).any():
        raise SystemExit("Universe contains intervals where effective_to precedes effective_from")

    bad_overlap = []
    for symbol, group in df.sort_values(["symbol", "effective_from"]).groupby("symbol"):
        previous_end = None
        for row in group.itertuples(index=False):
            if previous_end is not None and row.effective_from <= previous_end:
                bad_overlap.append(symbol)
                break
            previous_end = row.effective_to

    if bad_overlap:
        raise SystemExit(
            "Overlapping membership intervals found for: " + ", ".join(sorted(set(bad_overlap)))
        )

    print("Strategy 002 U1 universe validation PASSED")
    print(f"Rows: {len(df)}")
    print(f"Distinct symbols: {df['symbol'].nunique()}")
    print(f"First effective date: {df['effective_from'].min().date()}")
    print(f"Last effective date: {df['effective_to'].dropna().max().date() if df['effective_to'].notna().any() else 'open'}")


if __name__ == "__main__":
    main()
