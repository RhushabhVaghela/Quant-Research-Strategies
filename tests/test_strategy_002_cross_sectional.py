import numpy as np
import pandas as pd

from src.research.strategy_002_cross_sectional import (
    Strategy002Config,
    build_symbol_signals,
    run_universe,
    summarize_cross_section,
)


def _frame(seed: float = 100.0, n: int = 45) -> pd.DataFrame:
    idx = pd.date_range("2026-01-02 09:15", periods=n, freq="5min")
    close = np.linspace(seed, seed + 1.0, n)
    return pd.DataFrame(
        {
            "open": close,
            "high": close + 0.1,
            "low": close - 0.1,
            "close": close,
        },
        index=idx,
    )


def test_symbol_features_use_only_prior_bars():
    frame = _frame()
    out = build_symbol_signals(frame, Strategy002Config())
    assert out.loc[out.index[30], "prior_mean"] != out.loc[out.index[30], "close"]
    assert pd.isna(out.loc[out.index[29], "prior_mean"])
    assert pd.isna(out.loc[out.index[30], "prior_return"]) is False


def test_universe_keeps_symbol_dimension():
    trades = run_universe({"AAA": _frame(100), "BBB": _frame(200)})
    assert set(trades.columns) >= {"symbol", "signal_timestamp", "gross_return"}
    if not trades.empty:
        assert set(trades["symbol"]).issubset({"AAA", "BBB"})


def test_summary_reports_breadth_and_clustering():
    trades = pd.DataFrame(
        {
            "symbol": ["AAA", "BBB", "AAA"],
            "signal_timestamp": pd.to_datetime([
                "2026-01-02 12:00",
                "2026-01-02 12:00",
                "2026-01-02 13:00",
            ]),
            "gross_return": [0.001, -0.0005, 0.0002],
        }
    )
    summary = summarize_cross_section(trades).iloc[0]
    assert summary["trades"] == 3
    assert summary["symbols"] == 2
    assert summary["max_concurrent_entries_same_timestamp"] == 2
