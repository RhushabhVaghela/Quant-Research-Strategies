import numpy as np
import pandas as pd

from scripts.analyze_strategy_001j_universe_similarity import analyze


def _bars(path, values, start="2026-01-01 09:15"):
    idx = pd.date_range(start, periods=len(values), freq="5min", tz="Asia/Kolkata")
    pd.DataFrame({
        "timestamp": idx,
        "open": values,
        "high": np.asarray(values) + 0.1,
        "low": np.asarray(values) - 0.1,
        "close": values,
        "volume": 1000,
    }).to_csv(path, index=False)


def test_similarity_respects_end_boundary(tmp_path):
    ref = tmp_path / "GOLDBEES.csv"
    universe = tmp_path / "universe"
    universe.mkdir()
    candidate = universe / "AAA.csv"
    _bars(ref, [100, 101, 102, 103, 104, 105])
    _bars(candidate, [50, 50.5, 51, 51.5, 52, 52.5])
    report = analyze(ref, universe, "2026-01-01T09:35:00+05:30")
    assert list(report["symbol"]) == ["AAA"]
    # Five bars (09:15 through 09:35) produce four 5-minute returns.
    assert int(report.iloc[0]["observations_5m"]) == 4


def test_similarity_has_no_strategy_selection_flag(tmp_path):
    ref = tmp_path / "GOLDBEES.csv"
    universe = tmp_path / "universe"
    universe.mkdir()
    values = list(np.arange(100, 122))
    _bars(ref, values)
    _bars(universe / "AAA.csv", list(np.arange(50, 72) * 1.001))
    report = analyze(ref, universe, "2026-01-01T15:30:00+05:30")
    assert "selected" not in report.columns
    assert "strategy_return" not in report.columns
    assert "descriptive_rank" in report.columns
