"""Run Strategy 001A event-structure and conditioning diagnostics."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from scripts.run_mean_reversion_event_study import load_ohlcv
from src.research.event_study import add_forward_returns
from src.research.mean_reversion import make_mean_reversion_events
from src.research.mean_reversion_diagnostics import (
    _summary_rows,
    add_diagnostic_features,
    build_conditioning_report,
    mark_non_overlapping_events,
    summarize_dependence,
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
        default=Path("data/reports/goldbees_mean_reversion_diagnostics"),
    )
    args = parser.parse_args()

    horizons = (1, 3, 6, 12)
    df = load_ohlcv(args.csv)
    events = make_mean_reversion_events(df, args.lookback, args.z_threshold)
    events = add_forward_returns(events, horizons)
    events = add_diagnostic_features(events)
    events = mark_non_overlapping_events(events, args.cooldown)

    dependence = summarize_dependence(events)
    outcome_summary = pd.concat(
        [
            _summary_rows(events, horizons, "event"),
            _summary_rows(events, horizons, "non_overlapping_event"),
        ],
        ignore_index=True,
    )
    conditioning = build_conditioning_report(events, horizons)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    events.to_csv(args.output_dir / "diagnostic_event_observations.csv")
    dependence.to_csv(args.output_dir / "event_dependence.csv", index=False)
    outcome_summary.to_csv(args.output_dir / "outcome_summary.csv", index=False)
    conditioning.to_csv(args.output_dir / "conditioning_summary.csv", index=False)
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
            }
        ]
    )
    metadata.to_csv(args.output_dir / "metadata.csv", index=False)

    print("\nEvent dependence:")
    print(dependence.to_string(index=False))
    print("\nOutcome summary:")
    print(outcome_summary.to_string(index=False))
    print("\nConditioning summary:")
    print(conditioning.to_string(index=False))
    print(f"\nWrote research outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
