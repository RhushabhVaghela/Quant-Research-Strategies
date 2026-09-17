from __future__ import annotations

import pandas as pd

from scripts.analyze_strategy_001j_development_stability import (
    DEVELOPMENT_END,
    DEVELOPMENT_END_EXCLUSIVE,
    DEVELOPMENT_START,
    _breadth,
    _metrics,
)


def test_development_metrics_use_trade_returns() -> None:
    trades = pd.DataFrame({"symbol": ["A", "A", "B"], "gross_return": [0.01, -0.005, 0.002]})
    metrics = _metrics(trades)
    assert metrics["trades"] == 3
    assert metrics["symbols"] == 2
    assert metrics["win_rate"] == 2 / 3
    assert metrics["profit_factor"] == (0.012 / 0.005)


def test_breadth_reports_symbol_distribution() -> None:
    trades = pd.DataFrame({"symbol": ["A", "A", "B", "C"], "gross_return": [0.01, -0.002, 0.003, -0.001]})
    breadth = _breadth(trades)
    assert breadth["symbol_count"] == 3
    assert breadth["positive_symbol_fraction"] == 2 / 3
    assert 0 < breadth["top5_share_abs"] <= 1


def test_development_metadata_end_dates_are_explicit() -> None:
    """Keep metadata date generation free of generic NumPy timedelta arithmetic."""
    assert DEVELOPMENT_START.date().isoformat() == "2026-06-10"
    assert DEVELOPMENT_END.date().isoformat() == "2026-08-19"
    assert DEVELOPMENT_END_EXCLUSIVE.date().isoformat() == "2026-08-20"
    assert DEVELOPMENT_END < DEVELOPMENT_END_EXCLUSIVE
