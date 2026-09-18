"""Tests for Strategy 002 formation-only pair selection."""

from __future__ import annotations

import numpy as np
import pandas as pd

from scripts.build_strategy_002_pairs import (
    MAX_HALF_LIFE_BARS,
    MAX_PAIRS_PER_SYMBOL,
    MIN_HALF_LIFE_BARS,
    MIN_RETURN_CORRELATION,
    select_pairs,
    _window,
)


def _frame(values: np.ndarray) -> pd.DataFrame:
    idx = pd.date_range(
        "2026-05-12 09:15:00",
        periods=len(values),
        freq="5min",
        tz="Asia/Kolkata",
    )
    return pd.DataFrame({"close": values}, index=idx)


def test_pair_selection_is_bounded_and_unique() -> None:
    base = np.exp(np.cumsum(np.full(700, 0.0001)))
    frames = {
        "AAA": _frame(base),
        "BBB": _frame(base * np.exp(np.sin(np.arange(700) / 20) * 0.001)),
        "CCC": _frame(base * np.exp(np.sin(np.arange(700) / 23) * 0.001)),
        "DDD": _frame(base * np.exp(np.sin(np.arange(700) / 27) * 0.001)),
    }
    pairs = select_pairs(frames)
    assert len(pairs) <= 20
    assert pairs["pair_id"].is_unique
    counts = {}
    for row in pairs.itertuples(index=False):
        counts[row.symbol_a] = counts.get(row.symbol_a, 0) + 1
        counts[row.symbol_b] = counts.get(row.symbol_b, 0) + 1
    assert all(v <= MAX_PAIRS_PER_SYMBOL for v in counts.values())


def test_window_uses_explicit_python_timedelta():
    start = _window("2026-05-12")
    end = _window("2026-06-09", end_of_day=True)
    assert str(start) == "2026-05-12 00:00:00+05:30"
    assert str(end) == "2026-06-10 00:00:00+05:30"


def test_mean_reversion_sign_convention_accepts_negative_delta_coefficient() -> None:
    n = 900
    rng = np.random.default_rng(7)
    spread = np.zeros(n)
    for i in range(1, n):
        spread[i] = 0.92 * spread[i - 1] + rng.normal(0.0, 0.01)
    base = np.exp(np.cumsum(rng.normal(0.0001, 0.0002, n)))
    frames = {"AAA": _frame(base * np.exp(spread)), "BBB": _frame(base)}
    pairs = select_pairs(frames)
    assert not pairs.empty
    assert pairs.iloc[0]["half_life_bars"] >= MIN_HALF_LIFE_BARS
    assert pairs.iloc[0]["half_life_bars"] <= MAX_HALF_LIFE_BARS


def test_registered_thresholds_are_explicit() -> None:
    assert MIN_RETURN_CORRELATION == 0.75
    assert MIN_HALF_LIFE_BARS == 2.0
    assert MAX_HALF_LIFE_BARS == 120.0
    assert MAX_PAIRS_PER_SYMBOL == 2
