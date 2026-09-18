"""Strategy 002 intraday pairs mean-reversion engine.

Pair membership and hedge beta are frozen from formation. Signal statistics use
only completed bars before the signal bar. Both legs enter on the next bar open.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Strategy002Config:
    spread_lookback_bars: int = 120
    entry_z: float = 2.5
    exit_z: float = 0.5
    max_holding_bars: int = 6
    cooldown_bars: int = 12
    risk_stop_z: float = 4.0


def _session_key(index: pd.DatetimeIndex) -> np.ndarray:
    return index.normalize().to_numpy()


def run_pair(
    pair: Mapping[str, object],
    frames: Mapping[str, pd.DataFrame],
    config: Strategy002Config,
) -> pd.DataFrame:
    a_symbol = str(pair["symbol_a"])
    b_symbol = str(pair["symbol_b"])
    beta = float(pair["hedge_beta"])
    if config.spread_lookback_bars <= 0 or config.max_holding_bars <= 0:
        raise ValueError("lookback and max holding must be positive")
    if config.entry_z <= 0 or not (0 <= config.exit_z < config.entry_z):
        raise ValueError("z thresholds are invalid")
    if config.cooldown_bars < 0 or config.risk_stop_z <= config.entry_z:
        raise ValueError("cooldown/stop configuration is invalid")

    joined = pd.concat(
        [frames[a_symbol][["open", "close"]].add_suffix("_a"),
         frames[b_symbol][["open", "close"]].add_suffix("_b")],
        axis=1, join="inner"
    ).dropna()
    if joined.empty:
        return pd.DataFrame()

    log_spread = np.log(joined["close_a"].astype(float)) - beta * np.log(joined["close_b"].astype(float))
    prior_mean = log_spread.shift(1).rolling(
        config.spread_lookback_bars, min_periods=config.spread_lookback_bars
    ).mean()
    prior_std = log_spread.shift(1).rolling(
        config.spread_lookback_bars, min_periods=config.spread_lookback_bars
    ).std(ddof=1)
    z = (log_spread - prior_mean) / prior_std.replace(0, np.nan)

    idx = joined.index
    session = _session_key(idx)
    selected: list[dict] = []
    active_until = -1
    last_entry = -10**9

    for pos in range(len(joined)):
        if pos <= active_until or pos - last_entry <= config.cooldown_bars:
            continue
        z_now = z.iloc[pos]
        if not np.isfinite(z_now) or abs(z_now) < config.entry_z:
            continue

        entry_pos = pos + 1
        if entry_pos >= len(joined) or session[entry_pos] != session[pos]:
            continue

        direction = -1 if z_now > 0 else 1
        exit_pos = None
        exit_reason = None
        for p in range(entry_pos, min(len(joined), pos + config.max_holding_bars + 1)):
            if session[p] != session[pos]:
                break
            z_path = z.iloc[p]
            if np.isfinite(z_path) and abs(z_path) <= config.exit_z:
                exit_pos, exit_reason = p, "normalization"
                break
            if np.isfinite(z_path) and abs(z_path) >= config.risk_stop_z:
                exit_pos, exit_reason = p, "risk_stop"
                break
        if exit_pos is None:
            exit_pos = pos + config.max_holding_bars
            exit_reason = "max_holding"
        if exit_pos >= len(joined) or session[exit_pos] != session[pos]:
            continue

        a_ret = joined.iloc[exit_pos]["close_a"] / joined.iloc[entry_pos]["open_a"] - 1.0
        b_ret = joined.iloc[exit_pos]["close_b"] / joined.iloc[entry_pos]["open_b"] - 1.0
        pair_return = direction * (a_ret - b_ret)
        selected.append({
            "pair_id": str(pair["pair_id"]),
            "symbol_a": a_symbol,
            "symbol_b": b_symbol,
            "signal_timestamp": idx[pos],
            "entry_timestamp": idx[entry_pos],
            "exit_timestamp": idx[exit_pos],
            "entry_z": float(z_now),
            "exit_z": float(z.iloc[exit_pos]) if np.isfinite(z.iloc[exit_pos]) else np.nan,
            "direction": "long_a_short_b" if direction == 1 else "short_a_long_b",
            "entry_a": float(joined.iloc[entry_pos]["open_a"]),
            "entry_b": float(joined.iloc[entry_pos]["open_b"]),
            "exit_a": float(joined.iloc[exit_pos]["close_a"]),
            "exit_b": float(joined.iloc[exit_pos]["close_b"]),
            "gross_return": float(pair_return),
            "exit_reason": exit_reason,
            "holding_bars": int(exit_pos - entry_pos),
        })
        active_until = exit_pos
        last_entry = pos

    return pd.DataFrame(selected)


def run_pairs(
    pairs: pd.DataFrame,
    frames: Mapping[str, pd.DataFrame],
    config: Strategy002Config,
) -> pd.DataFrame:
    tables = []
    for pair in pairs.to_dict("records"):
        trades = run_pair(pair, frames, config)
        if not trades.empty:
            tables.append(trades)
    if not tables:
        return pd.DataFrame(columns=[
            "pair_id", "symbol_a", "symbol_b", "signal_timestamp",
            "entry_timestamp", "exit_timestamp", "entry_z", "exit_z",
            "direction", "entry_a", "entry_b", "exit_a", "exit_b",
            "gross_return", "exit_reason", "holding_bars",
        ])
    return pd.concat(tables, ignore_index=True).sort_values(
        ["signal_timestamp", "pair_id"], kind="stable"
    ).reset_index(drop=True)
