"""Point-in-time benchmarks for continuation-event research.

The benchmark answers a narrow question: at an event timestamp, was the
historical forward return of comparable non-event observations already known
to be smaller? Only observations whose forward outcome completed strictly
before the event timestamp are eligible. This prevents look-ahead leakage.

This module is a research benchmark, not a trading signal.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "event",
    "prior_return_6bar",
    "time_of_day",
}


def _validate(df: pd.DataFrame) -> None:
    missing = sorted(REQUIRED_COLUMNS.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("DataFrame index must be a pandas DatetimeIndex")
    if not df.index.is_monotonic_increasing or df.index.has_duplicates:
        raise ValueError("DataFrame index must be increasing and unique")


def add_point_in_time_benchmark(
    df: pd.DataFrame,
    horizon: int = 6,
    min_baseline_observations: int = 30,
) -> pd.DataFrame:
    """Attach a strictly point-in-time matched non-event baseline.

    For every row t, the baseline mean is calculated from prior non-event rows
    in the same predefined time-of-day and prior-trend bucket whose forward
    return at horizon h was fully observed before t. Thus an observation at
    timestamp s is eligible for t only when s + h bars is before t.

    The function expects ``forward_return_{horizon}bar`` to already exist.
    The benchmark uses the fixed trend labels from Strategy 001A/001B and does
    not search thresholds or choose the best historical subgroup.
    """
    _validate(df)
    if horizon < 1:
        raise ValueError("horizon must be positive")
    if min_baseline_observations < 1:
        raise ValueError("min_baseline_observations must be at least 1")

    forward_column = f"forward_return_{horizon}bar"
    if forward_column not in df.columns:
        raise ValueError(f"Missing required column: {forward_column}")

    out = df.copy()
    out["trend_regime"] = np.select(
        [out["prior_return_6bar"] < 0, out["prior_return_6bar"] > 0],
        ["down", "up"],
        default="flat",
    )
    out["pit_baseline_observations"] = 0
    out["pit_baseline_mean_forward_return"] = np.nan
    out["pit_incremental_forward_return"] = np.nan
    out["pit_baseline_available"] = False

    # A forward return is complete only at the timestamp of its future bar.
    # Use the actual future timestamp rather than assuming calendar continuity.
    timestamps = pd.Series(out.index, index=out.index)
    future_timestamps = timestamps.shift(-horizon)
    sessions = pd.Series(out.index.normalize(), index=out.index)
    future_sessions = sessions.shift(-horizon)
    completed = future_timestamps.notna() & sessions.eq(future_sessions)

    eligible = out.loc[
        (~out["event"].astype(bool)) & completed & out[forward_column].notna(),
        ["trend_regime", "time_of_day", forward_column],
    ].copy()
    eligible["outcome_completed_at"] = future_timestamps.loc[eligible.index]
    eligible = eligible.sort_values("outcome_completed_at")

    # Process events in chronological order. For an event at t, only outcomes
    # with completion timestamp strictly before t are added to the benchmark.
    for event_time, row in out.loc[out["event"].astype(bool)].iterrows():
        eligible_now = eligible.loc[eligible["outcome_completed_at"] < event_time]
        matched = eligible_now.loc[
            (eligible_now["trend_regime"] == row["trend_regime"])
            & (eligible_now["time_of_day"] == row["time_of_day"])
        ]
        count = len(matched)
        out.at[event_time, "pit_baseline_observations"] = count
        if count >= min_baseline_observations:
            baseline_mean = float(matched[forward_column].mean())
            out.at[event_time, "pit_baseline_mean_forward_return"] = baseline_mean
            out.at[event_time, "pit_incremental_forward_return"] = (
                float(row[forward_column]) - baseline_mean
                if pd.notna(row[forward_column]) else np.nan
            )
            out.at[event_time, "pit_baseline_available"] = True

    return out


def summarize_point_in_time_benchmark(
    df: pd.DataFrame,
    horizon: int = 6,
    event_column: str = "non_overlapping_event",
) -> pd.DataFrame:
    """Summarize available point-in-time benchmark observations by direction/trend."""
    _validate(df)
    forward_column = f"forward_return_{horizon}bar"
    required = {forward_column, event_column, "event_direction"}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    work = df.loc[
        df[event_column].astype(bool) & df["pit_baseline_available"],
        [forward_column, "pit_baseline_mean_forward_return", "pit_incremental_forward_return", "event_direction", "trend_regime"],
    ].dropna(subset=[forward_column, "pit_incremental_forward_return"]).copy()
    work["direction"] = np.select(
        [work["event_direction"] > 0, work["event_direction"] < 0],
        ["positive", "negative"],
        default="none",
    )

    rows: list[dict[str, object]] = []
    for (direction, trend), subset in work.groupby(["direction", "trend_regime"], observed=False):
        rows.append({
            "event_set": event_column,
            "horizon_bars": horizon,
            "direction": direction,
            "trend_regime": trend,
            "events_with_pit_baseline": int(len(subset)),
            "mean_event_forward_return": float(subset[forward_column].mean()),
            "mean_pit_baseline_forward_return": float(subset["pit_baseline_mean_forward_return"].mean()),
            "mean_pit_incremental_forward_return": float(subset["pit_incremental_forward_return"].mean()),
            "positive_incremental_rate": float((subset["pit_incremental_forward_return"] > 0).mean()),
        })
    return pd.DataFrame(rows).sort_values(["direction", "trend_regime"]).reset_index(drop=True)
