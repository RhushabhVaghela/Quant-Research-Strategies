from pathlib import Path

import pandas as pd
import pytest

from scripts.run_mean_reversion_event_study import load_ohlcv


def test_load_ohlcv_accepts_canonical_timestamp_schema(tmp_path: Path) -> None:
    path = tmp_path / "timestamp.csv"
    pd.DataFrame(
        {
            "timestamp": ["2026-08-03 09:15:00+05:30", "2026-08-03 09:20:00+05:30"],
            "open": [100.0, 101.0],
            "high": [101.0, 102.0],
            "low": [99.0, 100.0],
            "close": [100.5, 101.5],
            "volume": [1000, 1100],
        }
    ).to_csv(path, index=False)

    out = load_ohlcv(path)

    assert out.index.name == "timestamp"
    assert str(out.index.tz) == "Asia/Kolkata"
    assert list(out["close"]) == [100.5, 101.5]


def test_load_ohlcv_keeps_legacy_date_schema_compatible(tmp_path: Path) -> None:
    path = tmp_path / "date.csv"
    pd.DataFrame(
        {
            "date": ["2026-08-03 09:15:00+05:30", "2026-08-03 09:20:00+05:30"],
            "open": [100.0, 101.0],
            "high": [101.0, 102.0],
            "low": [99.0, 100.0],
            "close": [100.5, 101.5],
            "volume": [1000, 1100],
        }
    ).to_csv(path, index=False)

    out = load_ohlcv(path)

    assert out.index.name == "timestamp"
    assert str(out.index.tz) == "Asia/Kolkata"
    assert list(out["close"]) == [100.5, 101.5]


def test_load_ohlcv_rejects_missing_timestamp_columns(tmp_path: Path) -> None:
    path = tmp_path / "invalid.csv"
    pd.DataFrame({"time": ["2026-08-03 09:15:00+05:30"], "close": [100.0]}).to_csv(
        path, index=False
    )

    with pytest.raises(ValueError, match="timestamp.*date"):
        load_ohlcv(path)
