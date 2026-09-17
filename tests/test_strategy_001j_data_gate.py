import pandas as pd
import pytest

from scripts.validate_strategy_001j_data_gate import validate


def _write_membership(path):
    pd.DataFrame([{
        "symbol": "AAA",
        "effective_from": "2026-01-01",
        "effective_to": "2026-02-01",
    }]).to_csv(path, index=False)


def _write_bars(path, start="2026-01-01 09:15", periods=75):
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
        validate(membership, data, "2026-01-01", "2026-01-01")


def test_regular_full_session_passes(tmp_path):
    membership = tmp_path / "membership.csv"
    data = tmp_path / "data"
    data.mkdir()
    _write_membership(membership)
    _write_bars(data / "AAA.csv", periods=75)
    report = validate(membership, data, "2026-01-01", "2026-01-01")
    assert report.iloc[0]["status"] == "ok"
    assert report.iloc[0]["terminal_truncation_sessions"] == 0


def test_terminal_truncation_is_allowed_when_contiguous(tmp_path):
    membership = tmp_path / "membership.csv"
    data = tmp_path / "data"
    data.mkdir()
    _write_membership(membership)
    _write_bars(data / "AAA.csv", periods=72)
    report = validate(membership, data, "2026-01-01", "2026-01-01")
    assert report.iloc[0]["status"] == "ok"
    assert report.iloc[0]["terminal_truncation_sessions"] == 1


def test_interior_gap_is_rejected(tmp_path):
    membership = tmp_path / "membership.csv"
    data = tmp_path / "data"
    data.mkdir()
    _write_membership(membership)
    idx = pd.date_range("2026-01-01 09:15", periods=75, freq="5min", tz="Asia/Kolkata")
    idx = idx.delete(40)
    pd.DataFrame({
        "timestamp": idx,
        "open": 100.0,
        "high": 101.0,
        "low": 99.0,
        "close": 100.5,
        "volume": 1000,
    }).to_csv(data / "AAA.csv", index=False)
    with pytest.raises(SystemExit, match="FAILED"):
        validate(membership, data, "2026-01-01", "2026-01-01")


def test_short_session_is_rejected(tmp_path):
    membership = tmp_path / "membership.csv"
    data = tmp_path / "data"
    data.mkdir()
    _write_membership(membership)
    _write_bars(data / "AAA.csv", periods=36)
    with pytest.raises(SystemExit, match="FAILED"):
        validate(membership, data, "2026-01-01", "2026-01-01")
