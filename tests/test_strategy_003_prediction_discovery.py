"""Unit tests for Strategy 003 discovery controls."""

from __future__ import annotations

import pandas as pd

from scripts.run_strategy_003_prediction_discovery import (
    EXPLORATORY_END,
    EXPLORATORY_START,
    HOLDOUT_START,
    VALIDATION_START,
    locked_exploratory_slice,
)


def test_locked_exploratory_slice_excludes_protected_periods() -> None:
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "2025-09-18",
                    "2026-06-09",
                    "2026-06-10",
                    "2026-08-20",
                ]
            ),
            "value": [1, 2, 3, 4],
        }
    )

    out = locked_exploratory_slice(frame)

    assert out["date"].min() >= EXPLORATORY_START
    assert out["date"].max() <= EXPLORATORY_END
    assert out["date"].max() < VALIDATION_START
    assert out["date"].max() < HOLDOUT_START
    assert len(out) == 2


def test_constants_are_chronological() -> None:
    assert EXPLORATORY_START < EXPLORATORY_END
    assert EXPLORATORY_END < VALIDATION_START
    assert VALIDATION_START < HOLDOUT_START


def test_trailing_features_market_beta_has_one_value_per_stock_day() -> None:
    from scripts.run_strategy_003_prediction_discovery import (
        daily_ohlcv,
        load_intraday,
        trailing_features,
    )
    from pathlib import Path

    data_dir = Path("data/raw/strategy_002_universe")
    stock = daily_ohlcv(
        load_intraday(data_dir / "NSE_RELIANCE_5minute.csv")
    )
    market = daily_ohlcv(
        load_intraday(data_dir / "NSE_NIFTYBEES_5minute.csv")
    )

    enriched = trailing_features(stock, market)

    assert len(enriched) == len(stock)
    assert enriched["market_beta_20d"].index.equals(enriched.index)
