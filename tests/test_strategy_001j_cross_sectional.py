import numpy as np
import pandas as pd

from src.research.strategy_001j_cross_sectional import (
    Strategy001JConfig,
    build_symbol_signals,
    run_universe,
    summarize_cross_section,
)


def make_frame(n: int = 80) -> pd.DataFrame:
    idx = pd.date_range("2026-01-05 09:15", periods=n, freq="5min", tz="Asia/Kolkata")
    close = np.linspace(100, 105, n)
    frame = pd.DataFrame(
        {
            "open": close,
            "high": close + 0.1,
            "low": close - 0.1,
            "close": close,
            "volume": 1000,
        },
        index=idx,
    )
    return frame


def test_features_use_prior_bars_only() -> None:
    frame = make_frame()
    signals = build_symbol_signals(frame, Strategy001JConfig())
    assert pd.isna(signals.iloc[29]["prior_mean"])
    assert not pd.isna(signals.iloc[30]["prior_mean"])


def test_universe_keeps_symbol_dimension() -> None:
    frames = {"AAA": make_frame(), "BBB": make_frame()}
    trades = run_universe(frames)
    if not trades.empty:
        assert set(trades["symbol"]) <= {"AAA", "BBB"}


def test_summary_reports_breadth() -> None:
    trades = pd.DataFrame(
        {
            "symbol": ["AAA", "BBB"],
            "signal_timestamp": pd.to_datetime(
                ["2026-01-05 10:00", "2026-01-05 10:00"], utc=True
            ),
            "gross_return": [0.01, -0.005],
        }
    )
    summary = summarize_cross_section(trades).iloc[0]
    assert summary["trades"] == 2
    assert summary["symbols"] == 2
    assert summary["max_concurrent_entries_same_timestamp"] == 2
