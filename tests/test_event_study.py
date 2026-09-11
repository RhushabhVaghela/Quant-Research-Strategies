from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.research.event_study import (
    EventStudyConfig,
    add_forward_returns,
    make_momentum_volume_events,
    run_event_study,
)


def _sample_ohlcv() -> pd.DataFrame:
    index = pd.DatetimeIndex(
        [
            "2026-08-03 09:15",
            "2026-08-03 09:20",
            "2026-08-03 09:25",
            "2026-08-03 09:30",
            "2026-08-03 09:35",
            "2026-08-03 09:40",
            "2026-08-04 09:15",
            "2026-08-04 09:20",
            "2026-08-04 09:25",
        ],
        tz="Asia/Kolkata",
    )
    close = [100, 101, 102, 103, 104, 105, 110, 111, 112]
    return pd.DataFrame(
        {
            "open": close,
            "high": np.array(close) + 0.5,
            "low": np.array(close) - 0.5,
            "close": close,
            "volume": [10, 10, 10, 10, 10, 10, 10, 10, 10],
        },
        index=index,
    )


def test_forward_returns_do_not_cross_session_boundary() -> None:
    df = _sample_ohlcv()
    result = add_forward_returns(df, horizons=(1, 3))

    assert result.loc[df.index[4], "forward_return_1bar"] == pytest.approx(105 / 104 - 1)
    assert pd.isna(result.loc[df.index[4], "forward_return_3bar"])
    assert result.loc[df.index[5], "forward_return_1bar"] != pytest.approx(110 / 105 - 1)


def test_event_study_summarizes_only_event_rows() -> None:
    df = _sample_ohlcv()
    events = pd.Series(False, index=df.index)
    events.iloc[[1, 2]] = True

    result = run_event_study(df, events, EventStudyConfig(horizons=(1, 2), min_events=2))

    expected = ((102 / 101 - 1) + (103 / 102 - 1)) / 2
    assert result.loc[1, "events"] == 2
    assert result.loc[1, "mean_forward_return"] == pytest.approx(expected)
    assert result.loc[1, "win_rate"] == 1.0


def test_event_study_requires_matching_boolean_event_index() -> None:
    df = _sample_ohlcv()
    events = pd.Series(1, index=df.index)
    with pytest.raises(TypeError, match="boolean"):
        run_event_study(df, events)


def test_momentum_volume_events_use_prior_volume_window() -> None:
    df = _sample_ohlcv().copy()
    df.loc[df.index[5], "close"] = 110
    df.loc[df.index[5], "volume"] = 100

    events = make_momentum_volume_events(
        df,
        lookback_bars=2,
        return_threshold=0.05,
        volume_lookback_bars=2,
        volume_multiplier=5,
    )

    assert events.dtype == bool
    assert events.iloc[5]
    assert not events.iloc[0]


def test_config_rejects_invalid_horizons() -> None:
    with pytest.raises(ValueError):
        EventStudyConfig(horizons=(3, 1))
    with pytest.raises(ValueError):
        EventStudyConfig(horizons=(0, 1))
