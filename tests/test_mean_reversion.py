import numpy as np
import pandas as pd
import pytest

from src.research.mean_reversion import add_mean_reversion_features, make_mean_reversion_events


def sample_df() -> pd.DataFrame:
    idx = pd.date_range("2026-08-03 09:15", periods=8, freq="5min", tz="Asia/Kolkata")
    return pd.DataFrame({"close": [100, 101, 100, 99, 100, 101, 103, 104]}, index=idx)


def test_features_use_only_prior_bars() -> None:
    df = sample_df()
    out = add_mean_reversion_features(df, lookback_bars=3)
    assert out.loc[df.index[3], "prior_mean"] == pytest.approx((100 + 101 + 100) / 3)
    assert out.loc[df.index[3], "prior_std"] == pytest.approx(np.std([100, 101, 100], ddof=1))
    assert pd.isna(out.loc[df.index[0], "prior_mean"])


def test_events_are_directional() -> None:
    idx = pd.date_range("2026-08-03 09:15", periods=6, freq="5min", tz="Asia/Kolkata")
    # Use non-zero prior dispersion so the z-score is defined. The final 110
    # close should be an unambiguous positive deviation from the prior window.
    df = pd.DataFrame({"close": [100, 101, 99, 100, 100, 110]}, index=idx)
    out = make_mean_reversion_events(df, lookback_bars=4, z_threshold=2.0)
    assert out.loc[idx[-1], "positive_event"]
    assert not out.loc[idx[-1], "negative_event"]
    assert out.loc[idx[-1], "event_direction"] == 1


def test_session_boundary_resets_lookback() -> None:
    idx = pd.DatetimeIndex([
        "2026-08-03 15:25+05:30", "2026-08-04 09:15+05:30", "2026-08-04 09:20+05:30",
        "2026-08-04 09:25+05:30", "2026-08-04 09:30+05:30",
    ])
    df = pd.DataFrame({"close": [100, 200, 201, 202, 203]}, index=idx)
    out = add_mean_reversion_features(df, lookback_bars=3)
    assert pd.isna(out.loc[idx[1], "prior_mean"])


def test_invalid_input() -> None:
    with pytest.raises(ValueError):
        make_mean_reversion_events(sample_df(), lookback_bars=1)
    with pytest.raises(ValueError):
        make_mean_reversion_events(sample_df(), z_threshold=0)
