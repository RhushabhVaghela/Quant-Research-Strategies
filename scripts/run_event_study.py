"""Run the first exploratory intraday event study on a saved OHLCV CSV."""

from __future__ import annotations

import argparse

from src.data.audit import load_ohlcv_csv
from src.research.event_study import (
    EventStudyConfig,
    make_momentum_volume_events,
    run_event_study,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", help="Path to a saved OHLCV CSV")
    parser.add_argument("--lookback-bars", type=int, default=6)
    parser.add_argument("--return-threshold", type=float, default=0.002)
    parser.add_argument("--volume-lookback-bars", type=int, default=20)
    parser.add_argument("--volume-multiplier", type=float, default=1.5)
    parser.add_argument(
        "--horizons",
        type=int,
        nargs="+",
        default=[1, 3, 6, 12],
        help="Forward horizons in 5-minute bars",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = load_ohlcv_csv(args.csv_path)
    events = make_momentum_volume_events(
        df,
        lookback_bars=args.lookback_bars,
        return_threshold=args.return_threshold,
        volume_lookback_bars=args.volume_lookback_bars,
        volume_multiplier=args.volume_multiplier,
    )
    result = run_event_study(
        df,
        events,
        EventStudyConfig(horizons=tuple(args.horizons)),
    )

    print(f"Event count: {int(events.sum())}")
    print("\nForward-return study:")
    print(result.to_string(float_format=lambda value: f"{value:.6f}"))
    print(
        "\nNote: this is an exploratory event study, not a backtest or a claim "
        "of profitability."
    )


if __name__ == "__main__":
    main()
