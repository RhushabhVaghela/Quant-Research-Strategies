"""Leakage-safe event-study utilities for intraday OHLCV research.

The event study deliberately measures what happens *after* an event. It does
not place trades, estimate a strategy's Sharpe ratio, or claim profitability.
All event definitions are evaluated using information available at the event
bar, while forward returns use future bars only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class EventStudyConfig:
    """Configuration for forward-return measurement."""

    horizons: tuple[int, ...] = (1, 3, 6, 12)
    min_events: int = 1

    def __post_init__(self) -> None:
        if not self.horizons or any(h <= 0 for h in self.horizons):
            raise ValueError("horizons must contain positive bar counts")
        if tuple(sorted(set(self.horizons))) != self.horizons:
            raise ValueError("horizons must be strictly increasing and unique")
        if self.min_events < 1:
            raise ValueError("min_events must be at least 1")


def add_forward_returns(
    df: pd.DataFrame,
    horizons: Iterable[int],
    price_column: str = "close",
) -> pd.DataFrame:
    """Add future close-to-close returns for each requested bar horizon.

    For an event at bar ``t``, horizon ``h`` is calculated as
    ``close[t+h] / close[t] - 1``. No backward-looking value is used to form
    the forward return, and rows without enough future bars remain NaN.
    """
    if price_column not in df.columns:
        raise ValueError(f"Missing price column: {price_column}")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("DataFrame index must be a pandas DatetimeIndex")

    horizons = tuple(horizons)
    if not horizons or any(h <= 0 for h in horizons):
        raise ValueError("horizons must contain positive bar counts")

    out = df.copy()
    session = pd.Series(out.index.date, index=out.index)
    for horizon in horizons:
        future_price = out[price_column].shift(-horizon)
        future_session = session.shift(-horizon)
        same_session = session.eq(future_session)
        values = future_price.div(out[price_column]).sub(1.0)
        out[f"forward_return_{horizon}bar"] = values.where(same_session)
    return out


def make_momentum_volume_events(
    df: pd.DataFrame,
    lookback_bars: int = 6,
    return_threshold: float = 0.002,
    volume_lookback_bars: int = 20,
    volume_multiplier: float = 1.5,
) -> pd.Series:
    """Create an exploratory directional momentum + volume event mask.

    The event fires when the current close is sufficiently far from the close
    ``lookback_bars`` ago and current volume is unusually high versus the
    preceding volume window. The current bar is included in the event
    decision, but no future data is used.

    This is a research hypothesis, not a recommended trading strategy.
    """
    required = {"close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if lookback_bars < 1 or volume_lookback_bars < 1:
        raise ValueError("lookback bars must be positive")
    if return_threshold <= 0 or volume_multiplier <= 0:
        raise ValueError("thresholds must be positive")

    session = pd.Series(df.index.date, index=df.index)
    past_close = df["close"].shift(lookback_bars)
    past_session = session.shift(lookback_bars)
    same_session = session.eq(past_session)
    momentum = df["close"].div(past_close).sub(1.0).where(same_session)

    # Shift the volume baseline so the current bar cannot influence its own
    # comparison. This also makes the event definition easier to defend.
    prior_volume_mean = (
        df["volume"]
        .groupby(session)
        .transform(lambda s: s.shift(1).rolling(volume_lookback_bars, min_periods=volume_lookback_bars).mean())
    )
    volume_ratio = df["volume"].div(prior_volume_mean)

    event = momentum.abs().ge(return_threshold) & volume_ratio.ge(volume_multiplier)
    return event.fillna(False).astype(bool)


def run_event_study(
    df: pd.DataFrame,
    events: pd.Series,
    config: EventStudyConfig | None = None,
    price_column: str = "close",
) -> pd.DataFrame:
    """Measure forward returns at event bars and summarize each horizon.

    Returns one row per horizon with event count, mean/median forward return,
    standard deviation, win rate, and selected quantiles. Events are aligned
    to ``df`` and are restricted to boolean observations. A ValueError is
    raised when the event series has fewer observations than ``min_events``.
    """
    config = config or EventStudyConfig()
    if not events.index.equals(df.index):
        raise ValueError("events index must exactly match the OHLCV index")
    if events.dtype != bool:
        raise TypeError("events must be a boolean pandas Series")

    work = add_forward_returns(df, config.horizons, price_column=price_column)
    rows: list[dict[str, float | int]] = []
    total_events = int(events.sum())
    if total_events < config.min_events:
        raise ValueError(
            f"Only {total_events} events found; minimum required is {config.min_events}"
        )

    for horizon in config.horizons:
        values = work.loc[events, f"forward_return_{horizon}bar"].dropna()
        if values.empty:
            rows.append(
                {
                    "horizon_bars": horizon,
                    "events": 0,
                    "mean_forward_return": np.nan,
                    "median_forward_return": np.nan,
                    "std_forward_return": np.nan,
                    "win_rate": np.nan,
                    "p10_forward_return": np.nan,
                    "p90_forward_return": np.nan,
                }
            )
            continue

        rows.append(
            {
                "horizon_bars": horizon,
                "events": int(values.size),
                "mean_forward_return": float(values.mean()),
                "median_forward_return": float(values.median()),
                "std_forward_return": float(values.std(ddof=1)) if len(values) > 1 else np.nan,
                "win_rate": float((values > 0).mean()),
                "p10_forward_return": float(values.quantile(0.10)),
                "p90_forward_return": float(values.quantile(0.90)),
            }
        )

    return pd.DataFrame(rows).set_index("horizon_bars")
