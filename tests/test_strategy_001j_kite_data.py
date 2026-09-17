import pandas as pd
import pytest

from scripts.fetch_strategy_001j_kite_data import _merge_with_existing


def _bars(start, periods, price=100.0):
    idx = pd.date_range(start, periods=periods, freq="5min", tz="Asia/Kolkata")
    return pd.DataFrame({
        "timestamp": idx,
        "open": price,
        "high": price + 1,
        "low": price - 1,
        "close": price + 0.5,
        "volume": 1000,
    }).set_index("timestamp")


def test_merge_preserves_existing_history_and_adds_repair_range(tmp_path):
    output = tmp_path / "AAA.csv"
    existing = _bars("2026-09-16 09:15", 2)
    existing.reset_index().to_csv(output, index=False)

    fetched = _bars("2026-09-17 09:15", 2)
    merged = _merge_with_existing(output, fetched)

    assert len(merged) == 4
    assert merged["timestamp"].is_monotonic_increasing
    assert merged["timestamp"].nunique() == 4


def test_merge_replaces_overlapping_timestamp_with_fetched_value(tmp_path):
    output = tmp_path / "AAA.csv"
    existing = _bars("2026-09-17 09:15", 2, price=100.0)
    existing.reset_index().to_csv(output, index=False)

    fetched = _bars("2026-09-17 09:20", 2, price=200.0)
    merged = _merge_with_existing(output, fetched)

    assert len(merged) == 3
    overlap = merged.loc[merged["timestamp"] == pd.Timestamp("2026-09-17 09:20", tz="Asia/Kolkata")]
    assert len(overlap) == 1
    assert overlap.iloc[0]["open"] == 200.0


def test_merge_rejects_malformed_existing_file(tmp_path):
    output = tmp_path / "AAA.csv"
    output.write_text("timestamp,open,high,low,close\n2026-09-17 09:15,1,1,1,1\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing columns"):
        _merge_with_existing(output, _bars("2026-09-17 09:20", 1))
