"""Reusable cross-sectional engine for Strategy 001J.

001J keeps the Strategy 001 economic hypothesis while separating symbol-local
feature construction, signal selection, trade construction, and cross-sectional
aggregation. Parameter selection belongs to a separately registered experiment
and must never inspect the chronological holdout before the candidate is frozen.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Strategy001JConfig:
    """Signal/execution configuration for one frozen 001J experiment."""

    lookback_bars: int = 30
    z_threshold: float = 2.0
    trend_bars: int = 6
    holding_bars: int = 6
    cooldown_bars: int = 12


def _session_key(index: pd.DatetimeIndex) -> pd.Series:
    return pd.Series(index.normalize(), index=index)


def _prior_rolling(series: pd.Series, session: pd.Series, window: int, func: str) -> pd.Series:
    shifted = series.groupby(session, sort=False).shift(1)
    if func == "mean":
        return shifted.groupby(session, sort=False).transform(
            lambda s: s.rolling(window, min_periods=window).mean()
        )
    if func == "std":
        return shifted.groupby(session, sort=False).transform(
            lambda s: s.rolling(window, min_periods=window).std(ddof=1)
        )
    raise ValueError(f"Unsupported rolling function: {func}")


def build_symbol_signals(df: pd.DataFrame, config: Strategy001JConfig = Strategy001JConfig()) -> pd.DataFrame:
    """Build point-in-time continuation events for one symbol."""
    required = {"open", "high", "low", "close"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("DataFrame index must be a DatetimeIndex")
    if not df.index.is_monotonic_increasing:
        raise ValueError("Data must be chronologically ordered")
    if df.index.has_duplicates:
        raise ValueError("Data contains duplicate timestamps")
    if config.lookback_bars <= 0 or config.trend_bars <= 0:
        raise ValueError("lookback_bars and trend_bars must be positive")
    if config.holding_bars <= 0 or config.cooldown_bars < 0:
        raise ValueError("holding_bars must be positive and cooldown non-negative")

    out = df.copy()
    session = _session_key(out.index)
    out["prior_mean"] = _prior_rolling(out["close"], session, config.lookback_bars, "mean")
    out["prior_std"] = _prior_rolling(out["close"], session, config.lookback_bars, "std")
    out["z_score"] = (out["close"] - out["prior_mean"]) / out["prior_std"].replace(0, np.nan)

    prior_1 = out["close"].groupby(session, sort=False).shift(1)
    prior_n = out["close"].groupby(session, sort=False).shift(config.trend_bars + 1)
    out["prior_return"] = prior_1 / prior_n - 1.0
    out["event"] = (out["z_score"] >= config.z_threshold) & (out["prior_return"] > 0)

    selected = np.zeros(len(out), dtype=bool)
    last_selected = -10**9
    session_values = session.to_numpy()
    event_values = out["event"].fillna(False).to_numpy()
    for i, is_event in enumerate(event_values):
        if i and session_values[i] != session_values[i - 1]:
            last_selected = -10**9
        if is_event and i - last_selected > config.cooldown_bars:
            selected[i] = True
            last_selected = i
    out["selected_event"] = selected
    return out


def generate_symbol_trades(symbol: str, signals: pd.DataFrame, config: Strategy001JConfig = Strategy001JConfig()) -> pd.DataFrame:
    """Convert selected events into next-open to t+holding-close trades."""
    idx = signals.index
    session = _session_key(idx).to_numpy()
    selected_positions = np.flatnonzero(signals["selected_event"].to_numpy())
    rows: list[dict] = []
    for pos in selected_positions:
        entry_pos = pos + 1
        exit_pos = pos + config.holding_bars
        if entry_pos >= len(signals) or exit_pos >= len(signals):
            continue
        if session[entry_pos] != session[pos] or session[exit_pos] != session[pos]:
            continue
        entry = float(signals.iloc[entry_pos]["open"])
        exit_ = float(signals.iloc[exit_pos]["close"])
        if not np.isfinite(entry) or not np.isfinite(exit_) or entry <= 0:
            continue
        rows.append({
            "symbol": symbol,
            "signal_timestamp": idx[pos],
            "entry_timestamp": idx[entry_pos],
            "exit_timestamp": idx[exit_pos],
            "z_score": float(signals.iloc[pos]["z_score"]),
            "prior_return": float(signals.iloc[pos]["prior_return"]),
            "entry_price": entry,
            "exit_price": exit_,
            "gross_return": exit_ / entry - 1.0,
        })
    return pd.DataFrame(rows)


def run_universe(symbol_frames: Mapping[str, pd.DataFrame], config: Strategy001JConfig = Strategy001JConfig()) -> pd.DataFrame:
    """Run the configuration independently for every symbol."""
    tables: list[pd.DataFrame] = []
    for symbol, frame in sorted(symbol_frames.items()):
        signals = build_symbol_signals(frame, config=config)
        trades = generate_symbol_trades(symbol, signals, config=config)
        if not trades.empty:
            tables.append(trades)
    if not tables:
        return pd.DataFrame(columns=[
            "symbol", "signal_timestamp", "entry_timestamp", "exit_timestamp",
            "z_score", "prior_return", "entry_price", "exit_price", "gross_return",
        ])
    return pd.concat(tables, ignore_index=True).sort_values(
        ["signal_timestamp", "symbol"], kind="stable"
    ).reset_index(drop=True)


def summarize_cross_section(trades: pd.DataFrame) -> pd.DataFrame:
    """Report breadth and signal-clustering diagnostics."""
    if trades.empty:
        return pd.DataFrame([{
            "trades": 0, "symbols": 0, "mean_gross_return": np.nan,
            "median_gross_return": np.nan, "win_rate": np.nan,
            "profit_factor": np.nan, "max_concurrent_entries_same_timestamp": 0,
        }])
    returns = trades["gross_return"].astype(float)
    wins = returns[returns > 0].sum()
    losses = -returns[returns < 0].sum()
    grouped = trades.groupby("signal_timestamp").size()
    return pd.DataFrame([{
        "trades": int(len(trades)),
        "symbols": int(trades["symbol"].nunique()),
        "mean_gross_return": float(returns.mean()),
        "median_gross_return": float(returns.median()),
        "win_rate": float((returns > 0).mean()),
        "profit_factor": float(wins / losses) if losses > 0 else np.inf,
        "max_concurrent_entries_same_timestamp": int(grouped.max()),
    }])
