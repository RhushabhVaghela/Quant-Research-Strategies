"""Run Strategy 001B continuation-attribution diagnostics."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from run_mean_reversion_event_study import load_ohlcv
from src.research.continuation_attribution import build_attribution_report
from src.research.event_study import add_forward_returns
from src.research.mean_reversion import make_mean_reversion_events
from src.research.mean_reversion_diagnostics import (
    add_diagnostic_features,
    mark_non_overlapping_events,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--lookback", type=int, default=30)
    parser.add_argument("--z-threshold", type=float, default=2.0)
    parser.add_argument("--cooldown", type=int, default=12)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/reports/goldbees_continuation_attribution"),
    )
    args = parser.parse_args()

    horizons = (1, 3, 6, 12)
    df = load_ohlcv(args.csv)
    events = make_mean_reversion_events(df, args.lookback, args.z_threshold)
    events = add_forward_returns(events, horizons)
    events = add_diagnostic_features(events)
    events = mark_non_overlapping_events(events, args.cooldown)

    direction_summary, benchmark_summary = build_attribution_report(events, horizons)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    direction_summary.to_csv(args.output_dir / "direction_trend_summary.csv", index=False)
    benchmark_summary.to_csv(args.output_dir / "event_vs_non_event_summary.csv", index=False)
    metadata = pd.DataFrame(
        [
            {
                "input": str(args.csv),
                "rows": len(df),
                "sessions": df.index.normalize().nunique(),
                "lookback_bars": args.lookback,
                "z_threshold": args.z_threshold,
                "cooldown_bars": args.cooldown,
                "total_events": int(events["event"].sum()),
                "non_overlapping_events": int(events["non_overlapping_event"].sum()),
                "baseline_definition": "all non-event observations matched on predefined time-of-day and prior-trend buckets",
                "baseline_note": "descriptive attribution benchmark only; not a prospective trading signal",
            }
        ]
    )
    metadata.to_csv(args.output_dir / "metadata.csv", index=False)

    print("\nDirectional event outcomes by prior trend:")
    print(direction_summary.to_string(index=False))
    print("\nEvent vs matched non-event baseline:")
    print(benchmark_summary.to_string(index=False))
    print(f"\nWrote research outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
