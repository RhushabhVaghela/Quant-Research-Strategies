import numpy as np
import pandas as pd
import pytest

from src.research.point_in_time_baseline import (
    add_point_in_time_benchmark,
    summarize_point_in_time_benchmark,
)


def make_frame() -> pd.DataFrame:
    idx = pd.date_range("2026-01-05 09:15", periods=12, freq="5min", tz="Asia/Kolkata")
    return pd.DataFrame(
        {
            "close": np.arange(100.0, 112.0),
            "event": [False] * 6 + [True, False, False, False, False, False],
            "prior_return_6bar": [0.01] * 12,
            "time_of_day": ["09:15-10:00"] * 12,
            "forward_return_2bar": [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.20, 0.08, 0.09, 0.10, 0.11, np.nan],
            "event_direction": [0] * 6 + [1] + [0] * 5,
            "non_overlapping_event": [False] * 6 + [True] + [False] * 5,
        },
        index=idx,
    )


def test_baseline_excludes_event_itself_and_future_outcomes():
    df = make_frame()
    out = add_point_in_time_benchmark(df, horizon=2, min_baseline_observations=1)
    event_time = df.index[6]

    # Rows 0-3 have outcomes completed strictly before row 6.
    assert out.at[event_time, "pit_baseline_observations"] == 4
    assert out.at[event_time, "pit_baseline_mean_forward_return"] == pytest.approx(0.025)
    assert out.at[event_time, "pit_incremental_forward_return"] == pytest.approx(0.175)


def test_baseline_is_not_available_until_minimum_history_exists():
    df = make_frame()
    out = add_point_in_time_benchmark(df, horizon=2, min_baseline_observations=5)
    event_time = df.index[6]
    assert out.at[event_time, "pit_baseline_observations"] == 4
    assert not bool(out.at[event_time, "pit_baseline_available"])
    assert pd.isna(out.at[event_time, "pit_baseline_mean_forward_return"])


def test_summary_uses_only_events_with_available_point_in_time_baseline():
    df = make_frame()
    out = add_point_in_time_benchmark(df, horizon=2, min_baseline_observations=1)
    summary = summarize_point_in_time_benchmark(out, horizon=2)
    row = summary.iloc[0]
    assert row["direction"] == "positive"
    assert row["trend_regime"] == "up"
    assert row["events_with_pit_baseline"] == 1
    assert row["mean_pit_incremental_forward_return"] == pytest.approx(0.175)
