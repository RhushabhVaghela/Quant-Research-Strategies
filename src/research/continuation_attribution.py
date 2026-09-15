"""Attribution diagnostics for the Strategy 001 continuation lead.

This module does not define a trading strategy. It asks whether the
continuation-like event behavior observed in Strategy 001 remains after
conditioning on recent trend and ordinary intraday drift.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "close",
    "event",
    "positive_event",
    "negative_event",
    "event_direction",
    "prior_return_6bar",
    "time_of_day",
    "non_overlapping_event",
}


def _validate(df: pd.DataFrame) -> None:
    missing = sorted(REQUIRED_COLUMNS.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("DataFrame index must be a pandas DatetimeIndex")
    if not df.index.is_monotonic_increasing or df.index.has_duplicates:
        raise ValueError("DataFrame index must be increasing and unique")


def add_attribution_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add fixed conditioning labels using information known at the event bar."""
    _validate(df)
    out = df.copy()
    out["trend_regime"] = np.select(
        [out["prior_return_6bar"] < 0, out["prior_return_6bar"] > 0],
        ["down", "up"],
        default="flat",
    )
    out["event_direction_label"] = np.select(
        [out["event_direction"] > 0, out["event_direction"] < 0],
        ["positive_deviation", "negative_deviation"],
        default="none",
    )
    return out


def _aligned_return(values: pd.Series, directions: pd.Series) -> pd.Series:
    return -directions.astype(float) * values


def event_vs_non_event_summary(
    df: pd.DataFrame,
    horizon: int = 6,
    event_column: str = "non_overlapping_event",
) -> pd.DataFrame:
    """Compare directional event outcomes with descriptive non-event baselines.

    The non-event baseline is matched on predefined time-of-day and prior-trend
    buckets. It is an attribution benchmark, not a prospective signal: it is
    computed over the full research sample and must not be used to construct a
    trading rule without a separate point-in-time validation experiment.
    """
    _validate(df)
    forward_column = f"forward_return_{horizon}bar"
    if forward_column not in df.columns:
        raise ValueError(f"Missing required column: {forward_column}")

    working = df.dropna(subset=[forward_column]).copy()
    working["trend_regime"] = np.select(
        [working["prior_return_6bar"] < 0, working["prior_return_6bar"] > 0],
        ["down", "up"],
        default="flat",
    )
    working["direction_group"] = np.select(
        [working["event_direction"] > 0, working["event_direction"] < 0],
        ["positive", "negative"],
        default="none",
    )

    event_mask = working[event_column].astype(bool)
    baseline_mask = ~working["event"].astype(bool)
    baseline = working.loc[baseline_mask]
    rows: list[dict[str, object]] = []

    for direction in ("positive", "negative"):
        events = working.loc[event_mask & (working["direction_group"] == direction)]
        for trend in ("down", "flat", "up"):
            event_subset = events.loc[events["trend_regime"] == trend]
            for time_of_day in working["time_of_day"].dropna().unique():
                e = event_subset.loc[event_subset["time_of_day"] == time_of_day]
                b = baseline.loc[
                    (baseline["trend_regime"] == trend)
                    & (baseline["time_of_day"] == time_of_day)
                ]
                if len(e) == 0 or len(b) == 0:
                    continue
                event_values = e[forward_column]
                baseline_values = b[forward_column]
                event_aligned = _aligned_return(
                    event_values, e["event_direction"]
                )
                baseline_mean = baseline_values.mean()
                event_mean = event_values.mean()
                rows.append(
                    {
                        "event_set": event_column,
                        "direction": direction,
                        "trend_regime": trend,
                        "time_of_day": time_of_day,
                        "horizon_bars": horizon,
                        "event_observations": int(len(event_values)),
                        "baseline_observations": int(len(baseline_values)),
                        "event_mean_forward_return": event_mean,
                        "baseline_mean_forward_return": baseline_mean,
                        "incremental_raw_return": event_mean - baseline_mean,
                        "event_mean_reversion_aligned_return": event_aligned.mean(),
                        "event_win_rate_raw": (event_values > 0).mean(),
                        "baseline_win_rate_raw": (baseline_values > 0).mean(),
                    }
                )

    return pd.DataFrame(rows).sort_values(
        ["event_set", "direction", "trend_regime", "time_of_day"]
    ).reset_index(drop=True)


def directional_trend_summary(
    df: pd.DataFrame,
    horizon: int = 6,
    event_column: str = "non_overlapping_event",
) -> pd.DataFrame:
    """Summarize event outcomes by deviation direction and prior trend."""
    _validate(df)
    forward_column = f"forward_return_{horizon}bar"
    if forward_column not in df.columns:
        raise ValueError(f"Missing required column: {forward_column}")

    working = df.loc[df[event_column].astype(bool)].dropna(subset=[forward_column]).copy()
    working["trend_regime"] = np.select(
        [working["prior_return_6bar"] < 0, working["prior_return_6bar"] > 0],
        ["down", "up"],
        default="flat",
    )
    working["direction"] = np.select(
        [working["event_direction"] > 0, working["event_direction"] < 0],
        ["positive", "negative"],
        default="none",
    )

    rows = []
    for (direction, trend), subset in working.groupby(
        ["direction", "trend_regime"], observed=False
    ):
        values = subset[forward_column]
        aligned = _aligned_return(values, subset["event_direction"])
        rows.append(
            {
                "event_set": event_column,
                "direction": direction,
                "trend_regime": trend,
                "horizon_bars": horizon,
                "events": int(len(values)),
                "mean_forward_return": values.mean(),
                "median_forward_return": values.median(),
                "mean_reversion_aligned_return": aligned.mean(),
                "win_rate_raw": (values > 0).mean(),
            }
        )
    return pd.DataFrame(rows).sort_values(["direction", "trend_regime"]).reset_index(drop=True)


def build_attribution_report(
    df: pd.DataFrame, horizons: tuple[int, ...] = (1, 3, 6, 12)
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build fixed continuation-attribution tables without parameter search."""
    direction_frames = []
    benchmark_frames = []
    for horizon in horizons:
        direction_frames.append(directional_trend_summary(df, horizon))
        benchmark_frames.append(event_vs_non_event_summary(df, horizon))
    return (
        pd.concat(direction_frames, ignore_index=True),
        pd.concat(benchmark_frames, ignore_index=True),
    )
