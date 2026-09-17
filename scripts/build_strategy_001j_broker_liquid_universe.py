"""Build the tactical Strategy 001J universe from Kite-native NSE equities.

The universe is formed from a pre-strategy liquidity window, not from Strategy
001J returns. It selects the top-N currently tradable NSE EQ symbols by median
daily traded value during the formation window. This is a fast, broker-native
fallback for the PIT Nifty 100 data problem.

Important limitation: Kite's current instrument dump is not a historical index
membership database, so this universe has survivorship/current-instrument bias.
It is therefore a tactical research experiment and cannot be treated as a fully
PIT-clean replacement for the deferred Nifty 100 universe without qualification.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def _daily_traded_value(path: Path, start: pd.Timestamp, end: pd.Timestamp) -> pd.Series:
    frame = pd.read_csv(path, usecols=["timestamp", "close", "volume"])
    ts = pd.to_datetime(frame["timestamp"], errors="raise", utc=True).dt.tz_convert("Asia/Kolkata")
    frame = frame.assign(timestamp=ts)
    frame = frame[(frame["timestamp"] >= start) & (frame["timestamp"] <= end)]
    frame["close"] = pd.to_numeric(frame["close"], errors="coerce")
    frame["volume"] = pd.to_numeric(frame["volume"], errors="coerce")
    frame = frame[(frame["close"] > 0) & (frame["volume"] >= 0)]
    frame["traded_value"] = frame["close"] * frame["volume"]
    return frame.groupby(frame["timestamp"].dt.normalize())["traded_value"].sum()


def build(input_dir: Path, formation_start: str, formation_end: str, research_end: str, top_n: int, min_days: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    start = pd.Timestamp(formation_start).tz_convert("Asia/Kolkata") if pd.Timestamp(formation_start).tzinfo else pd.Timestamp(formation_start).tz_localize("Asia/Kolkata")
    end = pd.Timestamp(formation_end).tz_convert("Asia/Kolkata") if pd.Timestamp(formation_end).tzinfo else pd.Timestamp(formation_end).tz_localize("Asia/Kolkata")
    research_end_ts = pd.Timestamp(research_end).tz_convert("Asia/Kolkata") if pd.Timestamp(research_end).tzinfo else pd.Timestamp(research_end).tz_localize("Asia/Kolkata")
    if not (start < end < research_end_ts):
        raise ValueError("Require formation_start < formation_end < research_end")
    if top_n < 1:
        raise ValueError("top_n must be >= 1")
    if min_days < 1:
        raise ValueError("min_days must be >= 1")

    rows = []
    for path in sorted(input_dir.glob("*.csv")):
        daily = _daily_traded_value(path, start, end)
        if len(daily) < min_days:
            continue
        rows.append({
            "symbol": path.stem.upper(),
            "formation_days": int(len(daily)),
            "median_daily_traded_value": float(daily.median()),
            "mean_daily_traded_value": float(daily.mean()),
        })

    if not rows:
        raise ValueError("No symbols satisfy the formation-window data requirement")

    ranking = pd.DataFrame(rows).sort_values(
        ["median_daily_traded_value", "symbol"], ascending=[False, True]
    ).reset_index(drop=True)
    selected = ranking.head(top_n).copy()

    # Membership begins after the formation window. The interval is half-open.
    membership_start = end + pd.Timedelta(5, unit="min")
    membership = pd.DataFrame({
        "symbol": selected["symbol"],
        "effective_from": membership_start.isoformat(),
        "effective_to": research_end_ts.isoformat(),
    })
    return selected, membership


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default="data/raw/strategy_001j_candidates")
    parser.add_argument("--formation-start", required=True)
    parser.add_argument("--formation-end", required=True)
    parser.add_argument("--research-end", required=True)
    parser.add_argument("--top-n", type=int, default=50)
    parser.add_argument("--min-days", type=int, default=15)
    parser.add_argument("--ranking-output", default="data/reports/strategy_001j_broker_universe_ranking.csv")
    parser.add_argument("--membership-output", default="data/universe/strategy_001j_u1_membership.csv")
    parser.add_argument("--metadata-output", default="data/universe/strategy_001j_u1_membership_metadata.json")
    args = parser.parse_args()

    ranking, membership = build(
        Path(args.input_dir),
        args.formation_start,
        args.formation_end,
        args.research_end,
        args.top_n,
        args.min_days,
    )
    Path(args.ranking_output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.membership_output).parent.mkdir(parents=True, exist_ok=True)
    ranking.to_csv(args.ranking_output, index=False)
    membership.to_csv(args.membership_output, index=False)
    Path(args.metadata_output).write_text(json.dumps({
        "universe_id": "U1",
        "strategy_id": "001J",
        "name": "Kite-native liquid NSE EQ tactical universe",
        "source": "Zerodha Kite Connect current NSE instrument dump + pre-strategy liquidity formation window",
        "formation_start": args.formation_start,
        "formation_end": args.formation_end,
        "research_end": args.research_end,
        "selection_metric": "median daily traded value = sum(5-minute close * volume) per day, median across formation days",
        "top_n": args.top_n,
        "minimum_formation_days": args.min_days,
        "strategy_outcomes_used": False,
        "survivorship_bias": "present: current Kite-tradable instrument universe does not reconstruct historical delistings/membership",
        "status": "tactical_broker_native_universe",
        "deferred_clean_universe": "PIT Nifty 100 remains a separate deferred data acquisition path",
    }, indent=2), encoding="utf-8")
    print(f"Selected {len(membership)} symbols.")
    print(ranking.head(args.top_n).to_string(index=False))


if __name__ == "__main__":
    main()
