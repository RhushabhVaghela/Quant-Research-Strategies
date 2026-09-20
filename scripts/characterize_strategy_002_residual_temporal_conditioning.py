"""Characterize leave-one-out residual reversal across chronological subperiods."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from run_strategy_002_leave_one_out_residual import (
    END,
    HORIZONS,
    START,
    VALIDATION_START,
    leave_one_out,
    load,
)

PERIOD_LABELS = ("Q1_time", "Q2_time", "Q3_time", "Q4_time")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument(
        "--audit-report",
        type=Path,
        default=Path("data/reports/strategy_002_universe_audit.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/reports/strategy_002_residual_temporal_conditioning"),
    )
    return parser.parse_args()


def build_periods(index: pd.DatetimeIndex) -> pd.Series:
    time_index = pd.Series(index.astype("int64"), index=index)
    periods = pd.qcut(
        time_index,
        4,
        labels=PERIOD_LABELS,
        duplicates="drop",
    )
    return periods


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    audit = pd.read_csv(args.audit_report)
    eligible = set(
        audit.loc[
            (audit.unexpected_interval_count == 0)
            & (audit.zero_volume_rows == 0),
            "symbol",
        ].astype(str)
    )

    series = {}
    excluded = []
    for path in sorted(args.directory.glob("*_5minute.csv")):
        symbol = path.name.removeprefix("NSE_").removesuffix("_5minute.csv")
        if symbol not in eligible:
            excluded.append(
                {"symbol": symbol, "reason": "failed structural universe audit"}
            )
            continue
        try:
            series[symbol] = load(path)
        except (ValueError, AssertionError) as exc:
            excluded.append({"symbol": symbol, "reason": str(exc)})

    if len(series) < 4:
        raise SystemExit("Need at least four eligible instruments")

    components = ("close_to_close", "close_to_open", "open_to_close")
    panels = {
        component: pd.DataFrame(
            {symbol: data[component] for symbol, data in series.items()}
        ).sort_index()
        for component in components
    }
    residuals = {
        component: leave_one_out(panels[component])
        for component in components
    }

    prior = residuals["close_to_close"]
    periods = build_periods(prior.index)

    rows = []
    for period in periods.cat.categories:
        period_mask = periods == period

        for horizon in HORIZONS:
            future = residuals["close_to_close"].shift(-horizon)
            for condition, sign_mask in {
                "prior_negative": prior < 0,
                "prior_positive": prior > 0,
            }.items():
                values = future.where(period_mask & sign_mask)
                for symbol in prior.columns:
                    sample = values[symbol].dropna()
                    rows.append(
                        {
                            "period": str(period),
                            "symbol": symbol,
                            "condition": condition,
                            "component": "close_to_close",
                            "horizon_bars": horizon,
                            "observations": len(sample),
                            "mean": sample.mean(),
                            "median": sample.median(),
                            "positive_fraction": (
                                (sample > 0).mean() if len(sample) else np.nan
                            ),
                        }
                    )

        for component in ("close_to_open", "open_to_close"):
            future = residuals[component].shift(-1)
            for condition, sign_mask in {
                "prior_negative": prior < 0,
                "prior_positive": prior > 0,
            }.items():
                values = future.where(period_mask & sign_mask)
                for symbol in prior.columns:
                    sample = values[symbol].dropna()
                    rows.append(
                        {
                            "period": str(period),
                            "symbol": symbol,
                            "condition": condition,
                            "component": component,
                            "horizon_bars": 1,
                            "observations": len(sample),
                            "mean": sample.mean(),
                            "median": sample.median(),
                            "positive_fraction": (
                                (sample > 0).mean() if len(sample) else np.nan
                            ),
                        }
                    )

    detail = pd.DataFrame(rows)
    breadth = (
        detail.groupby(
            ["period", "condition", "component", "horizon_bars"],
            as_index=False,
        )
        .agg(
            instruments=("symbol", "nunique"),
            median_instrument_mean=("mean", "median"),
            q25_instrument_mean=("mean", lambda x: x.quantile(0.25)),
            q75_instrument_mean=("mean", lambda x: x.quantile(0.75)),
            positive_instrument_fraction=("mean", lambda x: (x > 0).mean()),
        )
    )

    detail.to_csv(
        args.output_dir / "per_instrument_residual_temporal_conditioning.csv",
        index=False,
    )
    breadth.to_csv(
        args.output_dir / "residual_temporal_conditioning_breadth.csv",
        index=False,
    )
    pd.DataFrame(excluded).to_csv(
        args.output_dir / "excluded_instruments.csv",
        index=False,
    )
    pd.Series(
        {
            "exploratory_start": str(START),
            "exploratory_end": str(END),
            "validation_start": str(VALIDATION_START),
            "periods": list(PERIOD_LABELS),
            "included_instruments": sorted(series),
            "excluded_instruments": excluded,
            "holdout_used": False,
            "strategy_pnl_calculated": False,
            "optimization_performed": False,
        },
        dtype="object",
    ).to_json(args.output_dir / "run_manifest.json", indent=2)

    print(f"Included instruments: {len(series)}")
    print(f"Excluded instruments: {len(excluded)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
