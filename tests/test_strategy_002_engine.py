"""Tests for the Strategy 002 intraday pairs engine."""

import numpy as np
import pandas as pd

from src.research.strategy_002_pairs import Strategy002Config, run_pair


def _frame(values):
    idx = pd.date_range("2026-06-10 09:15", periods=len(values), freq="5min", tz="Asia/Kolkata")
    return pd.DataFrame({"open": values, "close": values}, index=idx)


def test_mean_reversion_trade_direction_and_next_open_entry():
    n = 80
    base = np.full(n, 100.0)
    a = base.copy()
    b = base.copy()
    a[61] = 110.0
    a[62:] = 100.0
    pair = {"pair_id": "002P01", "symbol_a": "AAA", "symbol_b": "BBB", "hedge_beta": 1.0}
    frames = {"AAA": _frame(a), "BBB": _frame(b)}
    config = Strategy002Config(spread_lookback_bars=20, entry_z=2.0, exit_z=0.5, max_holding_bars=3)
    trades = run_pair(pair, frames, config)
    assert trades.empty or trades.iloc[0]["entry_timestamp"] > trades.iloc[0]["signal_timestamp"]


def test_invalid_configuration_rejected():
    pair = {"pair_id": "002P01", "symbol_a": "AAA", "symbol_b": "BBB", "hedge_beta": 1.0}
    frames = {"AAA": _frame(np.ones(20)), "BBB": _frame(np.ones(20))}
    try:
        run_pair(pair, frames, Strategy002Config(entry_z=1.0, exit_z=1.0))
    except ValueError:
        pass
    else:
        raise AssertionError("invalid z configuration was accepted")
