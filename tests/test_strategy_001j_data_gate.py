import pandas as pd
import pytest

from scripts.validate_strategy_001j_data_gate import validate


def _write_membership(path):
    pd.DataFrame([{
        "symbol": "AAA",
        "effective_from": "2026-01-01",
        "effective_to": "2026-02-01",
    }]).to_csv(path, index=False)


def _write_bars(path, start="2026-01-01 09:15", periods=3):
    idx = pd.date_range(start, periods=periods, freq="5min", tz="Asia/Kolkata")
    pd.DataFrame({
        "timestamp": idx,
        "open": 100.0,
        "high": 101.0,
        "low": 99.0,
        "close": 100.5,
        "volume": 1000,
    }).to_csv(path, index=False)


def test_empty_membership_is_rejected(tmp_path):
    membership = tmp_path / "membership.csv"
    membership.write_text("symbol,effective_from,effective_to\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="membership is empty"):
        validate(membership, tmp_path / "data", "2026-01-01", "2026-01-02")


def test_missing_symbol_data_is_rejected(tmp_path):
    membership = tmp_path / "membership.csv"
    data = tmp_path / "data"
    data.mkdir()
    _write_membership(membership)
    with pytest.raises(SystemExit, match="FAILED"):
        validate(membership, data, "2026-01-01", "2026-01-01 09:25")


def test_sufficient_symbol_data_passes(tmp_path):
    membership = tmp_path / "membership.csv"
    data = tmp_path / "data"
    data.mkdir()
    _write_membership(membership)
    _write_bars(data / "AAA.csv", periods=4)
    report = validate(membership, data, "2026-01-01 09:15", "2026-01-01 09:30")
    assert report.iloc[0]["status"] == "ok"
