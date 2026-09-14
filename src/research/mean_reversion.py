"""Leakage-safe baseline mean-reversion event definition for intraday research."""
from __future__ import annotations

import numpy as np
import pandas as pd


def _validate(df: pd.DataFrame) -> None:
    if "close" not in df.columns:
        raise ValueError("Missing required columns: ['close']")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("DataFrame index must be a pandas DatetimeIndex")
    if not df.index.is_monotonic_increasing or df.index.has_duplicates:
        raise ValueError("DataFrame index must be increasing and unique")
    if df["close"].isna().any():
        raise ValueError("close contains missing values")


def add_mean_reversion_features(df: pd.DataFrame, lookback_bars: int = 30) -> pd.DataFrame:
    """Add prior-window mean, dispersion and current deviation z-score."""
    _validate(df)
    if lookback_bars < 2:
        raise ValueError("lookback_bars must be at least 2")
    out = df.copy()
    session = pd.Series(out.index.date, index=out.index)
    grouped = out["close"].groupby(session)
    out["prior_mean"] = grouped.transform(
        lambda s: s.shift(1).rolling(lookback_bars, min_periods=lookback_bars).mean()
    )
    out["prior_std"] = grouped.transform(
        lambda s: s.shift(1).rolling(lookback_bars, min_periods=lookback_bars).std(ddof=1)
    )
    out["deviation"] = out["close"] - out["prior_mean"]
    out["z_score"] = out["deviation"].div(out["prior_std"].replace(0.0, np.nan))
    return out


def make_mean_reversion_events(
    df: pd.DataFrame, lookback_bars: int = 30, z_threshold: float = 2.0
) -> pd.DataFrame:
    """Create positive, negative and combined mean-reversion event masks."""
    if z_threshold <= 0:
        raise ValueError("z_threshold must be positive")
    out = add_mean_reversion_features(df, lookback_bars)
    out["positive_event"] = out["z_score"].ge(z_threshold)
    out["negative_event"] = out["z_score"].le(-z_threshold)
    out["event"] = out["positive_event"] | out["negative_event"]
    out["event_direction"] = np.select(
        [out["positive_event"], out["negative_event"]], [1, -1], default=0
    ).astype(int)
    return out
