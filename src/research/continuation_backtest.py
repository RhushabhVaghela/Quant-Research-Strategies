"""Backtest the frozen Strategy 001D continuation rule.

This module intentionally keeps signal generation, execution timing, and
cost/slippage accounting explicit. It is not an optimizer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class CostScenario:
    """Per-side execution assumptions in basis points."""

    name: str
    transaction_cost_bps: float = 0.0
    slippage_bps: float = 0.0


def _session_key(index: pd.DatetimeIndex) -> pd.Series:
    return pd.Series(index.normalize(), index=index)


def build_signals(
    df: pd.DataFrame,
    lookback_bars: int = 30,
    z_threshold: float = 2.0,
    trend_bars: int = 6,
    cooldown_bars: int = 12,
) -> pd.DataFrame:
    """Build the frozen Strategy 001D event and selected-trade signals."""
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

    out = df.copy()
    session = _session_key(out.index)
    grouped = out.groupby(session)["close"]

    # Shift first: the event bar itself cannot enter its feature window.
    prior = grouped.shift(1)
    out["prior_mean_30"] = prior.groupby(session).rolling(lookback_bars).mean().reset_index(level=0, drop=True)
    out["prior_std_30"] = prior.groupby(session).rolling(lookback_bars).std(ddof=1).reset_index(level=0, drop=True)
    out["z_score"] = (out["close"] - out["prior_mean_30"]) / out["prior_std_30"].replace(0, np.nan)

    prior_6 = grouped.shift(1)
    prior_7 = grouped.shift(trend_bars + 1)
    out["prior_return_6bar"] = prior_6 / prior_7 - 1.0
    out["event"] = (out["z_score"] >= z_threshold) & (out["prior_return_6bar"] > 0)

    # Select the first valid event, then ignore subsequent events for the
    # fixed cooldown. The loop is intentionally explicit for auditability.
    selected = np.zeros(len(out), dtype=bool)
    last_selected = -10**9
    session_values = session.to_numpy()
    for i, is_event in enumerate(out["event"].fillna(False).to_numpy()):
        if session_values[i] != (session_values[i - 1] if i else session_values[i]):
            last_selected = -10**9
        if is_event and i - last_selected > cooldown_bars:
            selected[i] = True
            last_selected = i

    out["selected_event"] = selected
    return out


def _apply_execution_prices(entry_open: float, exit_close: float, scenario: CostScenario) -> tuple[float, float]:
    """Apply conservative symmetric per-side bps adjustments."""
    entry = entry_open * (1.0 + scenario.slippage_bps / 10_000.0)
    exit = exit_close * (1.0 - scenario.slippage_bps / 10_000.0)
    return entry, exit


def generate_trades(
    signals: pd.DataFrame,
    scenario: CostScenario = CostScenario("gross", 0.0, 0.0),
    holding_bars: int = 6,
) -> pd.DataFrame:
    """Convert selected signals into next-open to t+6-close trades."""
    rows: list[dict] = []
    idx = signals.index
    session = _session_key(idx).to_numpy()
    selected_positions = np.flatnonzero(signals["selected_event"].to_numpy())

    for pos in selected_positions:
        entry_pos = pos + 1
        exit_pos = pos + holding_bars
        if entry_pos >= len(signals) or exit_pos >= len(signals):
            continue
        if session[entry_pos] != session[pos] or session[exit_pos] != session[pos]:
            continue

        entry_raw = float(signals.iloc[entry_pos]["open"])
        exit_raw = float(signals.iloc[exit_pos]["close"])
        if not np.isfinite(entry_raw) or not np.isfinite(exit_raw) or entry_raw <= 0:
            continue

        entry, exit_ = _apply_execution_prices(entry_raw, exit_raw, scenario)
        gross_return = exit_raw / entry_raw - 1.0
        net_price_return = exit_ / entry - 1.0
        transaction_cost = 2.0 * scenario.transaction_cost_bps / 10_000.0
        net_return = net_price_return - transaction_cost

        rows.append(
            {
                "signal_timestamp": idx[pos],
                "entry_timestamp": idx[entry_pos],
                "exit_timestamp": idx[exit_pos],
                "z_score": float(signals.iloc[pos]["z_score"]),
                "prior_return_6bar": float(signals.iloc[pos]["prior_return_6bar"]),
                "entry_price_raw": entry_raw,
                "exit_price_raw": exit_raw,
                "gross_return": gross_return,
                "transaction_cost": transaction_cost,
                "slippage_return": net_price_return - gross_return,
                "net_return": net_return,
            }
        )

    trades = pd.DataFrame(rows)
    if trades.empty:
        return pd.DataFrame(
            columns=[
                "signal_timestamp", "entry_timestamp", "exit_timestamp", "z_score",
                "prior_return_6bar", "entry_price_raw", "exit_price_raw",
                "gross_return", "transaction_cost", "slippage_return", "net_return",
            ]
        )
    trades["equity"] = (1.0 + trades["net_return"]).cumprod()
    trades["running_peak"] = trades["equity"].cummax()
    trades["drawdown"] = trades["equity"] / trades["running_peak"] - 1.0
    return trades


def summarize_trades(trades: pd.DataFrame, periods_per_year: float | None = None) -> pd.DataFrame:
    """Return a one-row portfolio summary from a trade table."""
    n = len(trades)
    if n == 0:
        return pd.DataFrame([{
            "trades": 0, "total_net_return": 0.0, "mean_net_return": np.nan,
            "win_rate": np.nan, "average_win": np.nan, "average_loss": np.nan,
            "profit_factor": np.nan, "max_drawdown": 0.0, "sharpe": np.nan,
        }])

    r = trades["net_return"].astype(float)
    wins = r[r > 0]
    losses = r[r < 0]
    total = float(trades["equity"].iloc[-1] - 1.0)
    sharpe = np.nan
    if r.std(ddof=1) > 0:
        sharpe = float(r.mean() / r.std(ddof=1))
        if periods_per_year is not None:
            sharpe *= np.sqrt(periods_per_year / n)

    gross_profit = wins.sum()
    gross_loss = -losses.sum()
    profit_factor = float(gross_profit / gross_loss) if gross_loss > 0 else np.inf

    return pd.DataFrame([{
        "trades": n,
        "total_net_return": total,
        "mean_net_return": float(r.mean()),
        "win_rate": float((r > 0).mean()),
        "average_win": float(wins.mean()) if len(wins) else np.nan,
        "average_loss": float(losses.mean()) if len(losses) else np.nan,
        "profit_factor": profit_factor,
        "max_drawdown": float(trades["drawdown"].min()),
        "sharpe": sharpe,
    }])


def run_scenarios(
    df: pd.DataFrame,
    scenarios: Iterable[CostScenario],
) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    """Run the frozen strategy under explicit cost scenarios."""
    signals = build_signals(df)
    summaries: list[pd.DataFrame] = []
    trade_tables: dict[str, pd.DataFrame] = {}
    for scenario in scenarios:
        trades = generate_trades(signals, scenario=scenario)
        summary = summarize_trades(trades)
        summary.insert(0, "scenario", scenario.name)
        summary.insert(1, "transaction_cost_bps_per_side", scenario.transaction_cost_bps)
        summary.insert(2, "slippage_bps_per_side", scenario.slippage_bps)
        summaries.append(summary)
        trade_tables[scenario.name] = trades
    return pd.concat(summaries, ignore_index=True), trade_tables
