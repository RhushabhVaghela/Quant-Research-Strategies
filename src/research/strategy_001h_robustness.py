"""Robustness and chronological holdout diagnostics for frozen Strategy 001D.

001H is a validation layer, not an optimizer. It reuses the frozen 001D
signal/execution implementation, evaluates predefined chronological periods,
and applies a fixed round-trip friction ladder to the same gross trade set.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

from src.research.continuation_backtest import build_signals, generate_trades


PERIOD_ORDER = ("2025_H1", "2025_H2", "2026_H1", "2026_H2")
COST_LADDER_ROUND_TRIP_BPS = (0, 2, 4, 6, 8, 10, 14)


def _profit_factor(values: pd.Series) -> float:
    wins = values[values > 0].sum()
    losses = -values[values < 0].sum()
    return float(wins / losses) if losses > 0 else np.inf


def period_label(timestamp: pd.Timestamp) -> str | None:
    """Map a timestamp to the pre-registered chronological period."""
    if timestamp.year == 2025:
        return "2025_H1" if timestamp.month <= 6 else "2025_H2"
    if timestamp.year == 2026:
        return "2026_H1" if timestamp.month <= 6 else "2026_H2"
    return None


def add_period(trades: pd.DataFrame, timestamp_column: str = "signal_timestamp") -> pd.DataFrame:
    """Attach fixed chronological period labels without changing observations."""
    required = {timestamp_column}
    missing = required - set(trades.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    out = trades.copy()
    ts = pd.to_datetime(out[timestamp_column])
    out["period"] = ts.map(period_label)
    return out


def _daily_series(trades: pd.DataFrame, return_column: str) -> pd.Series:
    if trades.empty:
        return pd.Series(dtype=float)
    ts = pd.to_datetime(trades["exit_timestamp"])
    return trades.assign(_day=ts.dt.normalize()).groupby("_day")[return_column].apply(
        lambda x: (1.0 + x.astype(float)).prod() - 1.0
    )


def _daily_sharpe(trades: pd.DataFrame, return_column: str) -> float:
    daily = _daily_series(trades, return_column)
    if len(daily) < 2:
        return np.nan
    vol = float(daily.std(ddof=1))
    if vol == 0:
        return np.nan
    # Diagnostic annualization over calendar daily observations. This is not
    # presented as a live portfolio Sharpe or a risk-adjusted guarantee.
    full = daily.reindex(
        pd.date_range(daily.index.min(), daily.index.max(), freq="D", tz=daily.index.tz),
        fill_value=0.0,
    )
    full_vol = float(full.std(ddof=1))
    return float(full.mean() / full_vol * np.sqrt(252)) if full_vol > 0 else np.nan


def _max_drawdown(values: pd.Series) -> float:
    if values.empty:
        return 0.0
    equity = (1.0 + values.astype(float)).cumprod()
    return float((equity / equity.cummax() - 1.0).min())


def performance_summary(trades: pd.DataFrame, label: str | None = None) -> pd.DataFrame:
    """Summarize one fixed period or the complete frozen trade set."""
    if "gross_return" not in trades.columns:
        raise ValueError("Missing required columns: ['gross_return']")
    r = trades["gross_return"].astype(float)
    if r.empty:
        return pd.DataFrame([{
            "period": label, "trades": 0, "mean_gross_return": np.nan,
            "median_gross_return": np.nan, "win_rate": np.nan,
            "profit_factor": np.nan, "cumulative_gross_return": 0.0,
            "max_drawdown": 0.0, "p10": np.nan, "p25": np.nan,
            "p75": np.nan, "p90": np.nan, "largest_winner": np.nan,
            "largest_loser": np.nan, "top_10pct_profit_share": np.nan,
            "annualized_daily_sharpe": np.nan,
        }])
    q = r.quantile([0.10, 0.25, 0.75, 0.90])
    positive = r[r > 0]
    top_k = max(1, int(np.ceil(len(r) * 0.10)))
    top_profit = r.nlargest(top_k).sum()
    positive_profit = positive.sum()
    return pd.DataFrame([{
        "period": label,
        "trades": len(r),
        "mean_gross_return": float(r.mean()),
        "median_gross_return": float(r.median()),
        "win_rate": float((r > 0).mean()),
        "profit_factor": _profit_factor(r),
        "cumulative_gross_return": float((1.0 + r).prod() - 1.0),
        "max_drawdown": _max_drawdown(r),
        "p10": float(q.loc[0.10]),
        "p25": float(q.loc[0.25]),
        "p75": float(q.loc[0.75]),
        "p90": float(q.loc[0.90]),
        "largest_winner": float(r.max()),
        "largest_loser": float(r.min()),
        "top_10pct_profit_share": float(top_profit / positive_profit) if positive_profit > 0 else np.nan,
        "annualized_daily_sharpe": _daily_sharpe(trades, "gross_return"),
    }])


def chronological_performance(trades: pd.DataFrame) -> pd.DataFrame:
    """Return fixed H1/H2 performance slices in chronological order."""
    t = add_period(trades)
    rows = []
    for period in PERIOD_ORDER:
        rows.append(performance_summary(t[t["period"] == period], period).iloc[0].to_dict())
    return pd.DataFrame(rows)


def development_vs_holdout(trades: pd.DataFrame) -> pd.DataFrame:
    """Compare 2025 development/reference against 2026 chronological holdout."""
    t = add_period(trades)
    groups = {
        "development_reference_2025": ["2025_H1", "2025_H2"],
        "chronological_holdout_2026": ["2026_H1", "2026_H2"],
    }
    rows = []
    for label, periods in groups.items():
        subset = t[t["period"].isin(periods)]
        row = performance_summary(subset, label).iloc[0].to_dict()
        rows.append(row)
    return pd.DataFrame(rows)


def cost_sensitivity(trades: pd.DataFrame, round_trip_bps: Iterable[float] = COST_LADDER_ROUND_TRIP_BPS) -> pd.DataFrame:
    """Apply the pre-registered round-trip friction ladder to gross returns."""
    if "gross_return" not in trades.columns:
        raise ValueError("Missing required columns: ['gross_return']")
    rows = []
    gross = trades["gross_return"].astype(float)
    for cost_bps in round_trip_bps:
        net = gross - float(cost_bps) / 10_000.0
        equity = (1.0 + net).cumprod()
        rows.append({
            "round_trip_friction_bps": float(cost_bps),
            "trades": len(net),
            "mean_net_return": float(net.mean()) if len(net) else np.nan,
            "median_net_return": float(net.median()) if len(net) else np.nan,
            "win_rate": float((net > 0).mean()) if len(net) else np.nan,
            "profit_factor": _profit_factor(net),
            "cumulative_net_return": float(equity.iloc[-1] - 1.0) if len(net) else 0.0,
            "max_drawdown": float((equity / equity.cummax() - 1.0).min()) if len(net) else 0.0,
            "annualized_daily_sharpe": _daily_sharpe(
                trades.assign(_net_return=net), "_net_return"
            ),
        })
    return pd.DataFrame(rows)


def trading_activity_by_period(trades: pd.DataFrame, total_sessions_by_period: dict[str, int] | None = None) -> pd.DataFrame:
    """Measure signal frequency and holding duration by fixed period."""
    required = {"signal_timestamp", "entry_timestamp", "exit_timestamp"}
    missing = required - set(trades.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    t = add_period(trades)
    t["signal_timestamp"] = pd.to_datetime(t["signal_timestamp"])
    t["entry_timestamp"] = pd.to_datetime(t["entry_timestamp"])
    t["exit_timestamp"] = pd.to_datetime(t["exit_timestamp"])
    t["session_date"] = t["signal_timestamp"].dt.date
    t["holding_minutes"] = (t["exit_timestamp"] - t["entry_timestamp"]).dt.total_seconds() / 60.0
    rows = []
    for period in PERIOD_ORDER:
        g = t[t["period"] == period]
        active_days = int(g["session_date"].nunique())
        gaps = g["signal_timestamp"].sort_values().diff().dt.total_seconds() / 60.0
        total_sessions = None if total_sessions_by_period is None else total_sessions_by_period.get(period)
        rows.append({
            "period": period,
            "trades": len(g),
            "active_days": active_days,
            "total_sessions": total_sessions,
            "pct_sessions_with_trade": (active_days / total_sessions) if total_sessions else np.nan,
            "trades_per_active_day": (len(g) / active_days) if active_days else np.nan,
            "median_signal_gap_minutes": float(gaps.median()) if gaps.notna().any() else np.nan,
            "p10_signal_gap_minutes": float(gaps.quantile(0.10)) if gaps.notna().any() else np.nan,
            "median_holding_minutes": float(g["holding_minutes"].median()) if len(g) else np.nan,
        })
    return pd.DataFrame(rows)


def build_daily_equity(trades: pd.DataFrame, return_column: str = "gross_return") -> pd.DataFrame:
    """Build a daily completed-trade equity series for plotting."""
    daily = _daily_series(trades, return_column)
    if daily.empty:
        return pd.DataFrame(columns=["date", "daily_return", "equity", "drawdown"])
    frame = daily.rename("daily_return").to_frame()
    frame["equity"] = (1.0 + frame["daily_return"]).cumprod()
    frame["drawdown"] = frame["equity"] / frame["equity"].cummax() - 1.0
    frame.index.name = "date"
    return frame.reset_index()


def run_robustness(data: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Run all predefined 001H diagnostics on the frozen 001D implementation."""
    signals = build_signals(data)
    trades = generate_trades(signals)
    chronological = chronological_performance(trades)
    holdout = development_vs_holdout(trades)
    costs = cost_sensitivity(trades)
    total_sessions = (
        pd.Series(1, index=data.index.normalize())
        .groupby(level=0)
        .size()
    )
    session_counts = {}
    for date in total_sessions.index:
        label = period_label(pd.Timestamp(date))
        if label is not None:
            session_counts[label] = session_counts.get(label, 0) + 1
    activity = trading_activity_by_period(trades, session_counts)
    daily = build_daily_equity(trades)
    return {
        "trades": trades,
        "chronological_performance": chronological,
        "development_vs_holdout": holdout,
        "cost_sensitivity": costs,
        "trading_activity": activity,
        "daily_equity": daily,
    }
