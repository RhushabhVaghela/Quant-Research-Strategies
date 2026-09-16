from __future__ import annotations

import pandas as pd
import pytest

from scripts.run_strategy_001i_paper_shadow import _build_bar, _session_boundaries


def _tick(ts: str, price: float, volume: int, bid: float = 99.9, ask: float = 100.1):
    return {
        "exchange_timestamp": pd.Timestamp(ts, tz="Asia/Kolkata").to_pydatetime(),
        "last_price": price,
        "volume_traded": volume,
        "depth": {
            "buy": [{"price": bid, "quantity": 100, "orders": 1}],
            "sell": [{"price": ask, "quantity": 100, "orders": 1}],
        },
    }


def test_build_bar_uses_tick_ohlc_and_volume_delta():
    bucket = pd.Timestamp("2026-09-18 09:15:00", tz="Asia/Kolkata")
    ticks = [
        _tick("2026-09-18 09:15:01", 100.0, 1000),
        _tick("2026-09-18 09:17:00", 100.5, 1010),
        _tick("2026-09-18 09:19:59", 100.2, 1030, bid=100.1, ask=100.3),
    ]
    bar = _build_bar(bucket, ticks)
    assert bar["timestamp"].startswith("2026-09-18T09:15")
    assert bar["open"] == pytest.approx(100.0)
    assert bar["high"] == pytest.approx(100.5)
    assert bar["low"] == pytest.approx(100.0)
    assert bar["close"] == pytest.approx(100.2)
    assert bar["volume"] == pytest.approx(30.0)
    assert bar["best_bid_last"] == pytest.approx(100.1)
    assert bar["best_ask_last"] == pytest.approx(100.3)


def test_session_boundaries_are_five_minute_exchange_aligned():
    boundaries = _session_boundaries(pd.Timestamp("2026-09-18", tz="Asia/Kolkata").date())
    assert boundaries[0] == pd.Timestamp("2026-09-18 09:20", tz="Asia/Kolkata")
    assert boundaries[-1] == pd.Timestamp("2026-09-18 15:30", tz="Asia/Kolkata")
    assert len(boundaries) == 75
