from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.research.continuation_attribution import (
    add_attribution_features,
    directional_trend_summary,
    event_vs_non_event_summary,
)


def make_frame() -> pd.DataFrame:
    index = pd.date_range("2026-01-05 09:15", periods=12, freq="5min", tz="Asia/Kolkata")
    return pd.DataFrame(
        {
            "close": np.arange(100.0, 112.0),
            "event": [False, False, True, False, False, False, True, False, False, False, False, False],
            "positive_event": [False, False, True, False, False, False, True, False, False, False, False, False],
            "negative_event": [False] * 12,
            "event_direction": [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            "prior_return_6bar": [0.01] * 12,
            "time_of_day": ["09:15-10:00"] * 12,
            "non_overlapping_event": [False, False, True, False, False, False, True, False, False, False, False, False],
            "forward_return_1bar": [0.001, 0.002, 0.010, 0.003, 0.002, 0.001, 0.008, 0.002, 0.001, 0.002, 0.001, np.nan],
            "forward_return_3bar": [0.002, 0.003, 0.020, 0.004, 0.003, 0.002, 0.015, 0.003, 0.002, 0.003, 0.002, np.nan],
        },
        index=index,
    )


def test_add_attribution_features_is_point_in_time_labeling() -> None:
    df = make_frame()
    out = add_attribution_features(df)
    assert out.loc[out.index[2], "trend_regime"] == "up"
    assert out.loc[out.index[2], "event_direction_label"] == "positive_deviation"
    assert out.loc[out.index[0], "event_direction_label"] == "none"


def test_directional_summary_separates_positive_events_from_trend() -> None:
    out = directional_trend_summary(make_frame(), horizon=1)
    row = out[(out["direction"] == "positive") & (out["trend_regime"] == "up")].iloc[0]
    assert row["events"] == 2
    assert row["mean_forward_return"] == pytest.approx(0.009)


def test_non_event_baseline_excludes_event_bars() -> None:
    out = event_vs_non_event_summary(make_frame(), horizon=1)
    row = out[(out["direction"] == "positive") & (out["trend_regime"] == "up")].iloc[0]
    assert row["event_observations"] == 2
    assert row["baseline_observations"] == 9
    assert row["baseline_mean_forward_return"] < row["event_mean_forward_return"]


def test_future_change_does_not_change_event_labels() -> None:
    df = make_frame()
    changed = df.copy()
    changed.iloc[2, changed.columns.get_loc("prior_return_6bar")] = 0.50
    assert add_attribution_features(changed).loc[df.index[2], "event_direction_label"] == "positive_deviation"
    assert add_attribution_features(changed).loc[df.index[2], "trend_regime"] == "up"
