from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.research.strategy_001h_robustness import (
    COST_LADDER_ROUND_TRIP_BPS,
    add_period,
    cost_sensitivity,
    development_vs_holdout,
    period_label,
    performance_summary,
    trading_activity_by_period,
)


def make_trades() -> pd.DataFrame:
    ts = pd.to_datetime(
        [
            "2025-01-15 12:00",
            "2025-07-15 13:00",
            "2026-02-15 13:00",
            "2026-07-15 14:00",
        ]
    ).tz_localize("Asia/Kolkata")
    return pd.DataFrame(
        {
            "signal_timestamp": ts,
            "entry_timestamp": ts + pd.to_timedelta(5, unit="min"),
            "exit_timestamp": ts + pd.to_timedelta(30, unit="min"),
            "gross_return": [0.01, -0.005, 0.02, -0.002],
        }
    )


def test_period_label_is_fixed_and_chronological() -> None:
    assert period_label(pd.Timestamp("2025-06-30", tz="Asia/Kolkata")) == "2025_H1"
    assert period_label(pd.Timestamp("2025-07-01", tz="Asia/Kolkata")) == "2025_H2"
    assert period_label(pd.Timestamp("2026-06-30", tz="Asia/Kolkata")) == "2026_H1"
    assert period_label(pd.Timestamp("2026-07-01", tz="Asia/Kolkata")) == "2026_H2"
    assert period_label(pd.Timestamp("2024-12-31", tz="Asia/Kolkata")) is None


def test_performance_summary_uses_compounded_return_and_distribution_metrics() -> None:
    out = performance_summary(make_trades(), "test").iloc[0]
    r = np.array([0.01, -0.005, 0.02, -0.002])
    assert out["period"] == "test"
    assert out["trades"] == 4
    assert out["cumulative_gross_return"] == pytest.approx(np.prod(1 + r) - 1)
    assert out["median_gross_return"] == pytest.approx(np.median(r))
    assert out["win_rate"] == pytest.approx(0.5)
    assert out["profit_factor"] == pytest.approx(0.03 / 0.007)


def test_cost_sensitivity_applies_fixed_round_trip_friction() -> None:
    out = cost_sensitivity(make_trades())
    assert out["round_trip_friction_bps"].tolist() == list(COST_LADDER_ROUND_TRIP_BPS)
    row = out.loc[out["round_trip_friction_bps"] == 14].iloc[0]
    assert row["mean_net_return"] == pytest.approx(make_trades()["gross_return"].mean() - 0.0014)


def test_development_vs_holdout_keeps_2025_and_2026_separate() -> None:
    out = development_vs_holdout(make_trades())
    assert out["period"].tolist() == [
        "development_reference_2025",
        "chronological_holdout_2026",
    ]
    assert out["trades"].tolist() == [2, 2]


def test_activity_reports_fixed_holding_duration() -> None:
    out = trading_activity_by_period(
        make_trades(),
        {
            "2025_H1": 10,
            "2025_H2": 10,
            "2026_H1": 10,
            "2026_H2": 10,
        },
    )
    assert out.loc[out["period"] == "2025_H1", "active_days"].iloc[0] == 1
    assert out.loc[out["period"] == "2025_H1", "median_holding_minutes"].iloc[0] == 25.0
    assert out.loc[out["period"] == "2025_H1", "pct_sessions_with_trade"].iloc[0] == pytest.approx(0.1)


def test_add_period_does_not_change_trade_count() -> None:
    trades = make_trades()
    out = add_period(trades)
    assert len(out) == len(trades)
    assert out["period"].tolist() == ["2025_H1", "2025_H2", "2026_H1", "2026_H2"]
