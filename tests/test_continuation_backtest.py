import numpy as np
import pandas as pd
import pytest

from src.research.continuation_backtest import (
    CostScenario,
    build_signals,
    generate_trades,
    summarize_trades,
)


def make_session(n=50):
    idx = pd.date_range("2026-01-01 09:15", periods=n, freq="5min", tz="Asia/Kolkata")
    # Keep the first 30 completed bars non-constant so the 30-bar sample
    # standard deviation is defined at bar 30. The test is checking timing,
    # not a zero-volatility edge case.
    close = 100.0 + 0.01 * np.arange(n)
    close[30:42] = np.linspace(100.0, 104.0, 12)
    close[42:] = np.linspace(110.0, 111.0, n - 42)
    return pd.DataFrame(
        {"open": close, "high": close, "low": close, "close": close, "volume": 1000},
        index=idx,
    )


def test_signal_uses_only_prior_completed_bars():
    df = make_session()
    signals = build_signals(df)
    assert pd.isna(signals.iloc[0]["z_score"])
    assert pd.isna(signals.iloc[29]["z_score"])
    assert pd.notna(signals.iloc[30]["z_score"])
    assert "selected_event" in signals


def test_trade_enters_next_bar_and_exits_six_bars_later():
    df = make_session()
    signals = build_signals(df, z_threshold=1.0)
    event_pos = 31
    signals["selected_event"] = False
    signals.iloc[event_pos, signals.columns.get_loc("selected_event")] = True
    trades = generate_trades(signals, CostScenario("gross"))
    assert len(trades) == 1
    assert trades.iloc[0]["entry_timestamp"] == df.index[event_pos + 1]
    assert trades.iloc[0]["exit_timestamp"] == df.index[event_pos + 6]


def test_costs_reduce_net_return():
    df = make_session()
    signals = build_signals(df, z_threshold=1.0)
    event_pos = 31
    signals["selected_event"] = False
    signals.iloc[event_pos, signals.columns.get_loc("selected_event")] = True
    gross = generate_trades(signals, CostScenario("gross"))
    costly = generate_trades(signals, CostScenario("costly", 5.0, 2.0))
    assert costly.iloc[0]["net_return"] < gross.iloc[0]["net_return"]


def test_summary_handles_wins_losses_and_drawdown():
    trades = pd.DataFrame({"net_return": [0.01, -0.005, 0.02, -0.01]})
    trades["equity"] = (1 + trades["net_return"]).cumprod()
    trades["running_peak"] = trades["equity"].cummax()
    trades["drawdown"] = trades["equity"] / trades["running_peak"] - 1
    summary = summarize_trades(trades)
    row = summary.iloc[0]
    assert row["trades"] == 4
    assert row["win_rate"] == pytest.approx(0.5)
    assert row["profit_factor"] > 1
    assert row["max_drawdown"] < 0
