import numpy as np
import pandas as pd
import pytest

from src.research.mean_reversion import make_mean_reversion_events
from src.research.mean_reversion_diagnostics import (
    add_diagnostic_features,
    mark_non_overlapping_events,
    summarize_dependence,
)


def make_frame(n: int = 80) -> pd.DataFrame:
    index = pd.date_range(
        "2026-08-03 09:15:00", periods=n, freq="5min", tz="Asia/Kolkata"
    )
    close = 100.0 + np.arange(n, dtype=float) * 0.01
    volume = np.full(n, 1000.0)
    return pd.DataFrame({"close": close, "volume": volume}, index=index)


def make_two_session_frame() -> pd.DataFrame:
    first = pd.date_range(
        "2026-08-03 09:15:00", periods=75, freq="5min", tz="Asia/Kolkata"
    )
    second = pd.date_range(
        "2026-08-04 09:15:00", periods=75, freq="5min", tz="Asia/Kolkata"
    )
    index = first.append(second)
    # Vary returns so the rolling volatility is non-constant while keeping
    # the fixture deterministic.
    steps = np.tile(np.array([0.01, 0.03, -0.015, 0.02, -0.005]), 30)
    close = 100.0 + np.cumsum(steps[:150])
    volume = np.full(150, 1000.0)
    return pd.DataFrame({"close": close, "volume": volume}, index=index)


def test_diagnostic_features_are_point_in_time() -> None:
    df = make_frame()
    events = make_mean_reversion_events(df, lookback_bars=30, z_threshold=2.0)
    out = add_diagnostic_features(events)

    assert pd.isna(out["prior_return_6bar"].iloc[6])
    assert pd.isna(out["prior_volatility_30bar"].iloc[30])
    assert out["volume_ratio_30bar"].iloc[31] == pytest.approx(1.0)


def test_volatility_regime_uses_prior_completed_observations_across_sessions() -> None:
    df = make_two_session_frame()
    # Use the smallest valid positive threshold so event generation remains
    # subject to the production function's input contract.
    events = make_mean_reversion_events(df, lookback_bars=30, z_threshold=1e-9)
    out = add_diagnostic_features(events)

    second_session_start = 75
    # A 30-observation rolling std of returns needs 30 prior returns, and the
    # feature also shifts by one bar. Therefore the first defined observation
    # is session start + 31, not + 30.
    first_event_bar = second_session_start + 31
    assert pd.notna(out["prior_volatility_30bar"].iloc[first_event_bar])
    assert out["volatility_regime"].iloc[first_event_bar] in {"high", "low"}

    # Changing a future observation must not change the regime at the earlier
    # second-session event bar.
    changed = df.copy()
    changed.iloc[first_event_bar + 1, changed.columns.get_loc("close")] *= 1.20
    changed_events = make_mean_reversion_events(
        changed, lookback_bars=30, z_threshold=1e-9
    )
    changed_out = add_diagnostic_features(changed_events)
    assert (
        changed_out["volatility_regime"].iloc[first_event_bar]
        == out["volatility_regime"].iloc[first_event_bar]
    )


def test_non_overlapping_filter_enforces_cooldown_within_session() -> None:
    df = make_frame(40)
    df["event"] = False
    df["positive_event"] = False
    df["negative_event"] = False
    df["event_direction"] = 0
    df["z_score"] = 0.0
    for position in (30, 31, 39):
        df.iloc[position, df.columns.get_loc("event")] = True
        df.iloc[position, df.columns.get_loc("positive_event")] = True
        df.iloc[position, df.columns.get_loc("event_direction")] = 1

    out = mark_non_overlapping_events(df, cooldown_bars=3)
    selected = out.index[out["non_overlapping_event"]]
    assert list(selected) == [df.index[30], df.index[39]]


def test_dependence_summary_counts_filtered_events() -> None:
    df = make_frame(50)
    df["event"] = False
    df["positive_event"] = False
    df["negative_event"] = False
    df["event_direction"] = 0
    df["z_score"] = 0.0
    for position in (30, 31, 32, 40):
        df.iloc[position, df.columns.get_loc("event")] = True
        df.iloc[position, df.columns.get_loc("positive_event")] = True
        df.iloc[position, df.columns.get_loc("event_direction")] = 1
    out = mark_non_overlapping_events(df, cooldown_bars=3)

    summary = summarize_dependence(out)
    all_row = summary.loc[summary["event_set"] == "all_events"].iloc[0]
    filtered_row = summary.loc[summary["event_set"] == "non_overlapping"].iloc[0]
    assert all_row["events"] == 4
    assert filtered_row["events"] == 2
    # The test deliberately uses a 3-bar cooldown, so the retained
    # 30->40 gap is 10 bars and is correctly below the 12-bar horizon.
    assert filtered_row["same_session_gap_lt_12_bars_pct"] == pytest.approx(1.0)
