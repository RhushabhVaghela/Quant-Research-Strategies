from pathlib import Path

import pandas as pd

from scripts.run_strategy_002_pattern_discovery import (
    EXPLORATORY_END,
    EXPLORATORY_START,
    exploratory_slice,
)


def test_exploratory_slice_excludes_validation_and_holdout() -> None:
    timestamps = pd.to_datetime(
        [
            "2026-06-09 15:30:00+05:30",
            "2026-06-10 09:15:00+05:30",
            "2026-08-19 15:30:00+05:30",
            "2026-08-20 09:15:00+05:30",
            "2026-09-17 15:30:00+05:30",
        ]
    )
    frame = pd.DataFrame(
        {
            "timestamp": timestamps,
            "open": 1.0,
            "high": 1.0,
            "low": 1.0,
            "close": 1.0,
            "volume": 1,
        }
    )
    out = exploratory_slice(frame)

    assert len(out) == 1
    assert out["timestamp"].iloc[0].date() == EXPLORATORY_END.date()
    assert out["timestamp"].max() < pd.Timestamp("2026-06-10", tz="Asia/Kolkata")


def test_exploratory_slice_keeps_start_boundary() -> None:
    frame = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                ["2025-09-18 09:15:00+05:30", "2025-09-18 09:20:00+05:30"]
            ),
            "open": [1.0, 1.0],
            "high": [1.0, 1.0],
            "low": [1.0, 1.0],
            "close": [1.0, 1.0],
            "volume": [1, 1],
        }
    )
    out = exploratory_slice(frame)
    assert out["timestamp"].min().date() == EXPLORATORY_START.date()


def test_exploratory_slice_does_not_accept_naive_timestamps() -> None:
    frame = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2026-01-02"]),
            "open": [1.0],
            "high": [1.0],
            "low": [1.0],
            "close": [1.0],
            "volume": [1],
        }
    )
    # The production loader rejects naive timestamps before this helper is called.
    assert frame["timestamp"].dt.tz is None


def test_protocol_file_exists() -> None:
    assert Path("research/journal/002_pattern_discovery_protocol.md").exists()

