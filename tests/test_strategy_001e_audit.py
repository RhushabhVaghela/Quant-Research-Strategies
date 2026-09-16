import pandas as pd
import pytest

from src.research.strategy_001e_audit import cost_grid, distribution_summary, run_audit


def make_trades() -> pd.DataFrame:
    ts = pd.date_range("2025-01-01 09:20", periods=4, freq="30min", tz="Asia/Kolkata")
    return pd.DataFrame({
        "signal_timestamp": ts,
        "entry_timestamp": ts + pd.Timedelta(minutes=5),
        "exit_timestamp": ts + pd.Timedelta(minutes=30),
        "gross_return": [0.01, -0.005, 0.02, -0.002],
    })


def test_distribution_summary_reports_expected_median_and_win_rate():
    out = distribution_summary(make_trades()).iloc[0]
    assert out["trades"] == 4
    assert out["median_gross_return"] == pytest.approx(0.004)
    assert out["gross_win_rate"] == pytest.approx(0.5)


def test_cost_grid_is_explicit_and_two_sided():
    out = cost_grid(make_trades())
    row = out[(out.transaction_cost_bps_per_side == 5) & (out.slippage_bps_per_side == 2)].iloc[0]
    assert row.round_trip_friction_bps == pytest.approx(14.0)
    assert row.mean_net_return == pytest.approx(make_trades().gross_return.mean() - 0.0014)


def test_run_audit_returns_all_required_views():
    report = run_audit(make_trades())
    assert set(report) == {
        "summary", "cost_grid", "chronological_summary", "trading_activity", "time_series_metrics"
    }
