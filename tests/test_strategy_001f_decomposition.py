import pandas as pd
import pytest

from src.research.strategy_001f_decomposition import holding_period_summary, run_decomposition, winner_exclusion_summary


def make_trades() -> pd.DataFrame:
    ts = pd.date_range("2025-01-01 09:20", periods=4, freq="30min", tz="Asia/Kolkata")
    return pd.DataFrame({
        "signal_timestamp": ts,
        "entry_timestamp": ts + pd.to_timedelta(5, unit="min"),
        "exit_timestamp": ts + pd.to_timedelta(35, unit="min"),
        "gross_return": [0.01, -0.005, 0.02, -0.002],
    })


def test_winner_exclusion_removes_ranked_positive_trades():
    out = winner_exclusion_summary(make_trades())
    assert out.loc[out.exclusion == "none", "remaining_trades"].iloc[0] == 4
    assert out.loc[out.exclusion == "top_10pct", "excluded_winners"].iloc[0] == 1
    # Remove the largest winner (0.02): (0.01 - 0.005 - 0.002) / 3 = 0.001.
    assert out.loc[out.exclusion == "top_10pct", "mean_gross_return"].iloc[0] == pytest.approx(0.001)


def test_holding_period_is_derived_from_entry_and_exit():
    out = holding_period_summary(make_trades())
    assert out["holding_minutes"].tolist() == [30.0]
    assert out["trades"].iloc[0] == 4


def test_run_decomposition_has_core_views():
    out = run_decomposition(make_trades())
    assert {"winner_exclusion", "time_of_day", "holding_period"}.issubset(out)
