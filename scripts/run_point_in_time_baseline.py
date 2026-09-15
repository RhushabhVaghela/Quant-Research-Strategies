"""Run the frozen 001C point-in-time benchmark on one OHLCV file."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from run_mean_reversion_event_study import load_ohlcv
from src.research.event_study import add_forward_returns
from src.research.mean_reversion_diagnostics import add_diagnostic_features, mark_non_overlapping_events
from src.research.point_in_time_baseline import add_point_in_time_benchmark, summarize_point_in_time_benchmark


def build_frozen_events(df: pd.DataFrame) -> pd.DataFrame:
    """Build the frozen 001C event without parameter search."""
    lookback = 30
    z_threshold = 2.0
    session = pd.Series(df.index.normalize(), index=df.index)
    grouped = df["close"].groupby(session)
    prior_mean = grouped.transform(lambda s: s.shift(1).rolling(lookback, min_periods=lookback).mean())
    prior_std = grouped.transform(lambda s: s.shift(1).rolling(lookback, min_periods=lookback).std(ddof=1))
    z_score = df["close"].sub(prior_mean).div(prior_std.replace(0.0, pd.NA))
    prior_return_6bar = grouped.transform(lambda s: s.shift(1).div(s.shift(7)).sub(1.0))

    out = df.copy()
    out["prior_return_6bar"] = prior_return_6bar
    out["z_score"] = z_score
    out["event"] = z_score.ge(z_threshold).fillna(False).astype(bool) & prior_return_6bar.gt(0).fillna(False).astype(bool)
    out["positive_event"] = out["event"]
    out["negative_event"] = False
    out["event_direction"] = out["event"].astype(int)
    out = add_forward_returns(out, (1, 3, 6, 12))
    out = add_diagnostic_features(out)
    out = mark_non_overlapping_events(out, cooldown_bars=12)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("data/reports/goldbees_001c_pit"))
    args = parser.parse_args()

    df = load_ohlcv(args.csv)
    frozen = build_frozen_events(df)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for horizon in (1, 3, 6, 12):
        enriched = add_point_in_time_benchmark(frozen, horizon=horizon, min_baseline_observations=30)
        summary = summarize_point_in_time_benchmark(enriched, horizon=horizon)
        summary.to_csv(args.output_dir / f"pit_summary_{horizon}bar.csv", index=False)
        if horizon == 6:
            enriched.to_csv(args.output_dir / "events_with_pit_baseline_6bar.csv")

    metadata = pd.DataFrame([
        {"lookback_bars": 30, "z_threshold": 2.0, "trend_definition": "prior_return_6bar > 0", "primary_horizon_bars": 6, "cooldown_bars": 12, "min_baseline_observations": 30}
    ])
    metadata.to_csv(args.output_dir / "metadata.csv", index=False)
    print(f"Frozen 001C events: {int(frozen['event'].sum())}")
    print(f"Selected non-overlapping events: {int(frozen['non_overlapping_event'].sum())}")
    print(f"Wrote point-in-time benchmark outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
