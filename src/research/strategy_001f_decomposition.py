"""Diagnostic decomposition for frozen Strategy 001D trades.

This module deliberately does not optimize parameters. It decomposes an
already-generated trade set to understand tail dependence, timing, and
point-in-time signal characteristics.
"""
from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {"signal_timestamp", "entry_timestamp", "exit_timestamp", "gross_return"}


def _validate(trades: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS.difference(trades.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def winner_exclusion_summary(trades: pd.DataFrame) -> pd.DataFrame:
    _validate(trades)
    r = trades["gross_return"].astype(float).to_numpy()
    winners = np.sort(r[r > 0])[::-1]
    rows = []
    for label, fraction in [("none", 0.0), ("top_1pct", 0.01), ("top_5pct", 0.05), ("top_10pct", 0.10)]:
        k = int(np.ceil(len(winners) * fraction))
        excluded = set(winners[:k].tolist()) if k else set()
        # Rank-based exclusion is implemented on row indices to handle duplicate returns correctly.
        positive_idx = np.flatnonzero(r > 0)
        order = positive_idx[np.argsort(r[positive_idx])[::-1]] if len(positive_idx) else positive_idx
        excluded_idx = set(order[:k].tolist())
        kept = np.array([i for i in range(len(r)) if i not in excluded_idx])
        kr = r[kept]
        gross_profit = kr[kr > 0].sum()
        gross_loss = -kr[kr < 0].sum()
        rows.append({
            "exclusion": label,
            "excluded_winners": k,
            "remaining_trades": len(kr),
            "total_gross_return_sum": kr.sum(),
            "mean_gross_return": kr.mean() if len(kr) else np.nan,
            "median_gross_return": np.median(kr) if len(kr) else np.nan,
            "win_rate": (kr > 0).mean() if len(kr) else np.nan,
            "profit_factor": gross_profit / gross_loss if gross_loss else np.inf,
        })
    return pd.DataFrame(rows)


def distribution_by_bins(trades: pd.DataFrame, column: str, bins: list[float], labels: list[str]) -> pd.DataFrame:
    _validate(trades)
    if column not in trades.columns:
        raise ValueError(f"Column not available: {column}")
    frame = trades.copy()
    frame["bucket"] = pd.cut(frame[column].astype(float), bins=bins, labels=labels, include_lowest=True, right=False)
    out = frame.groupby("bucket", observed=False)["gross_return"].agg(
        trades="size", mean_gross_return="mean", median_gross_return="median", win_rate=lambda x: (x > 0).mean()
    ).reset_index()
    return out


def time_of_day_summary(trades: pd.DataFrame) -> pd.DataFrame:
    _validate(trades)
    frame = trades.copy()
    ts = pd.to_datetime(frame["signal_timestamp"])
    frame["hour_decimal"] = ts.dt.hour + ts.dt.minute / 60.0
    bins = [9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0]
    labels = ["09-10", "10-11", "11-12", "12-13", "13-14", "14-15", "15-16"]
    return distribution_by_bins(frame, "hour_decimal", bins, labels)


def holding_period_summary(trades: pd.DataFrame) -> pd.DataFrame:
    _validate(trades)
    frame = trades.copy()
    entry = pd.to_datetime(frame["entry_timestamp"])
    exit_ = pd.to_datetime(frame["exit_timestamp"])
    frame["holding_minutes"] = (exit_ - entry).dt.total_seconds() / 60.0
    return frame.groupby("holding_minutes", as_index=False)["gross_return"].agg(
        trades="size", mean_gross_return="mean", median_gross_return="median", win_rate=lambda x: (x > 0).mean()
    )


def feature_slice_summary(trades: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Return fixed diagnostic slices for available point-in-time features."""
    _validate(trades)
    out: Dict[str, pd.DataFrame] = {}
    if "z_score" in trades.columns:
        out["z_score"] = distribution_by_bins(
            trades, "z_score", [2.0, 2.25, 2.5, 3.0, np.inf], ["2.00-2.25", "2.25-2.50", "2.50-3.00", "3.00+"]
        )
    if "prior_6bar_return" in trades.columns:
        out["prior_6bar_return"] = distribution_by_bins(
            trades, "prior_6bar_return", [0.0, 0.001, 0.003, 0.005, np.inf], ["0-0.10%", "0.10-0.30%", "0.30-0.50%", "0.50%+"]
        )
    if "prior_volatility_30bar" in trades.columns:
        median = trades["prior_volatility_30bar"].median()
        frame = trades.copy()
        frame["volatility_regime"] = np.where(frame["prior_volatility_30bar"] <= median, "below_or_equal_median", "above_median")
        out["prior_volatility_30bar"] = frame.groupby("volatility_regime", as_index=False)["gross_return"].agg(
            trades="size", mean_gross_return="mean", median_gross_return="median", win_rate=lambda x: (x > 0).mean()
        )
    return out


def run_decomposition(trades: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    _validate(trades)
    report: Dict[str, pd.DataFrame] = {
        "winner_exclusion": winner_exclusion_summary(trades),
        "time_of_day": time_of_day_summary(trades),
        "holding_period": holding_period_summary(trades),
    }
    report.update(feature_slice_summary(trades))
    return report
