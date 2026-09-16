"""Diagnostics for the frozen Strategy 001D trade table.

No parameter search or strategy modification is performed here.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _profit_factor(r: pd.Series) -> float:
    wins = r[r > 0].sum()
    losses = -r[r < 0].sum()
    return float(wins / losses) if losses > 0 else np.inf


def distribution_summary(trades: pd.DataFrame) -> pd.DataFrame:
    r = trades["gross_return"].astype(float)
    q = r.quantile([0.10, 0.25, 0.50, 0.75, 0.90])
    top10 = r.nlargest(max(1, int(np.ceil(len(r) * 0.10)))).sum()
    total_positive = r[r > 0].sum()
    return pd.DataFrame([{
        "trades": len(r),
        "mean_gross_return": r.mean(),
        "median_gross_return": r.median(),
        "p10": q.loc[0.10],
        "p25": q.loc[0.25],
        "p75": q.loc[0.75],
        "p90": q.loc[0.90],
        "min": r.min(),
        "max": r.max(),
        "gross_win_rate": (r > 0).mean(),
        "gross_profit_factor": _profit_factor(r),
        "top_10pct_profit_share": (top10 / total_positive) if total_positive > 0 else np.nan,
    }])


def cost_grid(trades: pd.DataFrame) -> pd.DataFrame:
    """Predefined symmetric cost grid; no values are selected after testing."""
    rows = []
    for transaction_bps in [0, 1, 2, 3, 4, 5, 7.5, 10]:
        for slippage_bps in [0, 1, 2, 3, 5]:
            # Slippage is two-sided; transaction cost is explicitly two-sided.
            friction = 2 * (transaction_bps + slippage_bps) / 10_000.0
            net = trades["gross_return"].astype(float) - friction
            equity = (1.0 + net).cumprod()
            drawdown = equity / equity.cummax() - 1.0
            rows.append({
                "transaction_cost_bps_per_side": transaction_bps,
                "slippage_bps_per_side": slippage_bps,
                "round_trip_friction_bps": 2 * (transaction_bps + slippage_bps),
                "mean_net_return": net.mean(),
                "total_compounded_net_return": equity.iloc[-1] - 1.0,
                "win_rate": (net > 0).mean(),
                "profit_factor": _profit_factor(net),
                "max_drawdown": drawdown.min(),
            })
    return pd.DataFrame(rows)


def chronological_summary(trades: pd.DataFrame) -> pd.DataFrame:
    t = trades.copy()
    t["entry_timestamp"] = pd.to_datetime(t["entry_timestamp"])
    periods = pd.cut(
        t["entry_timestamp"],
        bins=[
            pd.Timestamp("2024-12-31 23:59:59", tz="Asia/Kolkata"),
            pd.Timestamp("2025-06-30 23:59:59", tz="Asia/Kolkata"),
            pd.Timestamp("2025-12-31 23:59:59", tz="Asia/Kolkata"),
            pd.Timestamp("2026-06-30 23:59:59", tz="Asia/Kolkata"),
            pd.Timestamp("2026-12-31 23:59:59", tz="Asia/Kolkata"),
        ],
        labels=["2025_H1", "2025_H2", "2026_H1", "2026_H2"],
    )
    t["period"] = periods
    rows = []
    for period, g in t.dropna(subset=["period"]).groupby("period", observed=True):
        r = g["gross_return"].astype(float)
        eq = (1 + r).cumprod()
        rows.append({
            "period": str(period),
            "trades": len(g),
            "total_compounded_gross_return": eq.iloc[-1] - 1.0,
            "mean_gross_return": r.mean(),
            "median_gross_return": r.median(),
            "win_rate": (r > 0).mean(),
            "profit_factor": _profit_factor(r),
            "max_drawdown": (eq / eq.cummax() - 1).min(),
        })
    return pd.DataFrame(rows)


def trading_activity(trades: pd.DataFrame) -> pd.DataFrame:
    t = trades.copy()
    for col in ["signal_timestamp", "entry_timestamp", "exit_timestamp"]:
        t[col] = pd.to_datetime(t[col])
    t["session_date"] = t["entry_timestamp"].dt.date
    holding_minutes = (t["exit_timestamp"] - t["entry_timestamp"]).dt.total_seconds() / 60.0
    gaps = t["signal_timestamp"].sort_values().diff().dt.total_seconds() / 60.0
    return pd.DataFrame([{
        "trading_days_with_trades": t["session_date"].nunique(),
        "mean_trades_per_active_day": t.groupby("session_date").size().mean(),
        "max_trades_in_day": t.groupby("session_date").size().max(),
        "mean_holding_minutes": holding_minutes.mean(),
        "median_holding_minutes": holding_minutes.median(),
        "median_signal_gap_minutes": gaps.median(),
        "p10_signal_gap_minutes": gaps.quantile(0.10),
    }])


def time_series_metrics(trades: pd.DataFrame) -> pd.DataFrame:
    """Create a daily mark-to-market proxy from completed trade returns.

    Days without a completed trade receive zero return. This is a simple
    constant-notional, non-overlapping representation, not a live portfolio
    accounting engine.
    """
    t = trades.copy()
    t["exit_timestamp"] = pd.to_datetime(t["exit_timestamp"])
    daily = t.groupby(t["exit_timestamp"].dt.normalize())["gross_return"].apply(
        lambda x: (1.0 + x).prod() - 1.0
    )
    if daily.empty:
        return pd.DataFrame([{"active_days": 0, "calendar_days": 0, "annualized_sharpe": np.nan, "annualized_volatility": np.nan}])
    full = daily.reindex(pd.date_range(daily.index.min(), daily.index.max(), freq="D", tz=daily.index.tz), fill_value=0.0)
    vol = full.std(ddof=1)
    sharpe = full.mean() / vol * np.sqrt(252) if vol > 0 else np.nan
    return pd.DataFrame([{
        "active_days": len(daily),
        "calendar_days": len(full),
        "annualized_sharpe": sharpe,
        "annualized_volatility": vol * np.sqrt(252),
    }])


def run_audit(trades: pd.DataFrame) -> dict[str, pd.DataFrame]:
    required = {"gross_return", "signal_timestamp", "entry_timestamp", "exit_timestamp"}
    missing = required - set(trades.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return {
        "summary": distribution_summary(trades),
        "cost_grid": cost_grid(trades),
        "chronological_summary": chronological_summary(trades),
        "trading_activity": trading_activity(trades),
        "time_series_metrics": time_series_metrics(trades),
    }
