from pathlib import Path

import pandas as pd
import pytest

from scripts.characterize_strategy_002_patterns import (
    END,
    START,
    conditional_table,
    exploratory_slice,
)


def _frame(timestamps):
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(timestamps),
            "open": [100.0] * len(timestamps),
            "high": [101.0] * len(timestamps),
            "low": [99.0] * len(timestamps),
            "close": [100.0 + i for i in range(len(timestamps))],
            "volume": [1000] * len(timestamps),
        }
    )


def test_exploratory_slice_accepts_full_history_with_pre_start_rows() -> None:
    frame = _frame(
        [
            "2025-09-17 15:30:00+05:30",
            "2025-09-18 09:15:00+05:30",
            "2025-09-18 09:20:00+05:30",
            "2026-06-09 15:30:00+05:30",
            "2026-06-10 09:15:00+05:30",
        ]
    )

    out = exploratory_slice(frame)

    assert out["timestamp"].min() >= START
    assert out["timestamp"].max() <= END
    assert len(out) == 3


def test_exploratory_slice_rejects_empty_window() -> None:
    frame = _frame(
        [
            "2025-09-17 15:30:00+05:30",
            "2026-06-10 09:15:00+05:30",
        ]
    )

    with pytest.raises(ValueError, match="No observations"):
        exploratory_slice(frame)


def test_conditional_table_produces_rows_for_valid_exploratory_data() -> None:
    timestamps = pd.date_range(
        "2026-01-02 09:15:00",
        periods=100,
        freq="5min",
        tz="Asia/Kolkata",
    )
    frame = pd.DataFrame(
        {
            "timestamp": timestamps,
            "close": [100.0 + i * 0.1 for i in range(100)],
        }
    )

    result = conditional_table(frame, "TEST")

    assert not result.empty
    assert result["symbol"].eq("TEST").all()
    assert set(result["horizon"].unique()) == {1, 2, 3, 6, 12}


def test_protocol_file_exists() -> None:
    assert Path("research/journal/002_pattern_discovery_protocol.md").exists()
