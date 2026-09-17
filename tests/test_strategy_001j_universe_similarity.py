import numpy as np
import pandas as pd

from scripts.analyze_strategy_001j_universe_similarity import analyze


def _bars(path, values, start="2026-01-01 09:15"):
    idx = pd.date_range(start, periods=len(values), freq="5min", tz="Asia/Kolkata")
    df = pd.DataFrame(
        {
            "timestamp": idx,
            "open": values,
            "high": np.asarray(values) + 0.1,
            "low": np.asarray(values) - 0.1,
            "close": values,
            "volume": 1000,
        }
    )
    df.to_csv(path, index=False)


def test_similarity_respects_end_boundary(tmp_path):
    ref = tmp_path / "GOLDBEES.csv"
    universe = tmp_path / "universe"
    universe.mkdir()
    candidate = universe / "AAA.csv"

    _bars(ref, [100, 101, 102, 103, 104, 105])
    _bars(candidate, [50, 50.5, 51, 51.5, 52, 52.5])
    # A second day contains deliberately different data that must be excluded.
    _bars(ref, [100, 101, 102, 103, 104, 105], start="2026-01-02 09:15")
    _bars(candidate, [80, 70, 60, 50, 40, 30], start="2026-01-02 09:15")

    report = analyze(ref, universe, "2026-01-01T15:30:00+05:30")
    assert list(report["symbol"]) == ["AAA"]
    assert int(report.iloc[0]["observations_5m"]) == 5


def test_similarity_output_has_no_strategy_selection_flag(tmp_path):
    ref = tmp_path / "GOLDBEES.csv"
    universe = tmp_path / "universe"
    universe.mkdir()
    _bars(ref, [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121])
    _bars(universe / "AAA.csv", [50, 50.1, 50.2, 50.3, 50.4, 50.5, 50.6, 50.7, 50.8, 50.9, 51, 51.1, 51.2, 51.3, 51.4, 51.5, 51.6, 51.7, 51.8, 51.9, 52, 52.1])

    report = analyze(ref, universe, "2026-01-01T15:30:00+05:30")
    assert "selected" not in report.columns
    assert "strategy_return" not in report.columns
    assert "descriptive_rank" in report.columns
