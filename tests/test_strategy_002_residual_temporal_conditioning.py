from pathlib import Path

import pandas as pd

from scripts.characterize_strategy_002_residual_temporal_conditioning import build_periods


def test_build_periods_is_chronological_and_complete():
    index = pd.date_range(
        "2025-09-18 09:15",
        periods=20,
        freq="5min",
        tz="Asia/Kolkata",
    )
    periods = build_periods(index)

    assert periods.notna().all()
    assert list(periods.cat.categories) == [
        "Q1_time",
        "Q2_time",
        "Q3_time",
        "Q4_time",
    ]

    labels = periods.astype(str).tolist()
    assert labels[:5] == ["Q1_time"] * 5
    assert labels[-5:] == ["Q4_time"] * 5
    assert index.is_monotonic_increasing
