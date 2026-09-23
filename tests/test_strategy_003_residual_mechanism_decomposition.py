"""Tests for Strategy 003 residual mechanism decomposition."""

from __future__ import annotations

import pandas as pd

from scripts.run_strategy_003_residual_mechanism_decomposition import (
    BASE_FEATURES,
    FAMILY_BLOCKS,
    time_bucket,
)

def test_base_features_are_locked() -> None:
    assert BASE_FEATURES == [
        "close_location_1bar",
        "intraday_position_60bar",
        "bars_since_session_open",
    ]

def test_family_blocks_are_pre_registered_and_raw() -> None:
    assert set(FAMILY_BLOCKS) == {"activity", "volatility", "market_context"}
    assert all(
        not feature.endswith("_rank") and not feature.endswith("_cs_z")
        for features in FAMILY_BLOCKS.values()
        for feature in features
    )

def test_time_bucket_boundaries() -> None:
    timestamps = pd.Series(
        pd.to_datetime([
            "2026-06-10 09:15", "2026-06-10 09:59",
            "2026-06-10 10:00", "2026-06-10 11:59",
            "2026-06-10 12:00", "2026-06-10 13:59",
            "2026-06-10 14:00", "2026-06-10 15:30",
        ]).tz_localize("Asia/Kolkata")
    )
    assert time_bucket(timestamps).tolist() == [
        "09:15-09:59", "09:15-09:59",
        "10:00-11:59", "10:00-11:59",
        "12:00-13:59", "12:00-13:59",
        "14:00-15:30", "14:00-15:30",
    ]
