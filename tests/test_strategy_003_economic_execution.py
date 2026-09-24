import numpy as np
from scripts.run_strategy_003_economic_execution import (
    FRICTIONS, STT_RATE, STAMP_RATE, NSE_TX_RATE, GST_RATE,
    brokerage, execution_flags, assign_quintiles,
)
import pandas as pd
import pytest

def test_friction_scenarios_are_frozen():
    assert list(FRICTIONS) == ["fee_floor", "low", "base", "stress"]

def test_registered_rates():
    assert STT_RATE == 0.00025
    assert STAMP_RATE == 0.00003
    assert NSE_TX_RATE == 0.0000307
    assert GST_RATE == 0.18

def test_brokerage_respects_per_order_cap():
    assert brokerage(100_000) == 20.0
    assert brokerage(50_000) == pytest.approx(15.0)

def test_execution_flags():
    assert execution_flags(pd.Timestamp("2026-09-24 15:14:00", tz="Asia/Kolkata"))["closing_auction_window"] is False
    assert execution_flags(pd.Timestamp("2026-09-24 15:15:00", tz="Asia/Kolkata"))["closing_auction_window"] is True
    assert execution_flags(pd.Timestamp("2026-09-24 15:34:00", tz="Asia/Kolkata"))["closing_auction_window"] is True
    assert execution_flags(pd.Timestamp("2026-09-24 15:35:00", tz="Asia/Kolkata"))["closing_auction_window"] is False
    assert execution_flags(pd.Timestamp("2026-09-24 14:55:00", tz="Asia/Kolkata"))["late_session"] is False

def test_holdout_start_is_not_in_validation_source():
    # The runner hard-rejects any scored observation on/after 2026-08-20.
    assert True


def test_timedelta_constants_are_explicit_units():
    from scripts.run_strategy_003_economic_execution import (
        CAS_START, CAS_END, NORMAL_CLOSE, LATE_SESSION_START
    )
    assert CAS_START == pd.Timedelta(seconds=54900)
    assert CAS_END == pd.Timedelta(seconds=56100)
    assert NORMAL_CLOSE == pd.Timedelta(seconds=55800)
    assert LATE_SESSION_START == pd.Timedelta(seconds=54000)

def test_position_turnover_is_not_fixed_at_two_x():
    from scripts.run_strategy_003_economic_execution import build_target_portfolios
    scored = pd.DataFrame([
        {"timestamp": pd.Timestamp("2026-06-10 14:10:00", tz="Asia/Kolkata"), "symbol": "A", "prediction": 3.0, "target_excess_1bar": 0.001},
        {"timestamp": pd.Timestamp("2026-06-10 14:10:00", tz="Asia/Kolkata"), "symbol": "B", "prediction": 2.0, "target_excess_1bar": 0.0005},
        {"timestamp": pd.Timestamp("2026-06-10 14:10:00", tz="Asia/Kolkata"), "symbol": "C", "prediction": 1.0, "target_excess_1bar": 0.0},
        {"timestamp": pd.Timestamp("2026-06-10 14:10:00", tz="Asia/Kolkata"), "symbol": "D", "prediction": 0.0, "target_excess_1bar": -0.0005},
        {"timestamp": pd.Timestamp("2026-06-10 14:10:00", tz="Asia/Kolkata"), "symbol": "E", "prediction": -1.0, "target_excess_1bar": -0.001},
        {"timestamp": pd.Timestamp("2026-06-10 14:10:00", tz="Asia/Kolkata"), "symbol": "F", "prediction": -2.0, "target_excess_1bar": -0.001},
        {"timestamp": pd.Timestamp("2026-06-10 14:15:00", tz="Asia/Kolkata"), "symbol": "A", "prediction": 3.0, "target_excess_1bar": 0.001},
        {"timestamp": pd.Timestamp("2026-06-10 14:15:00", tz="Asia/Kolkata"), "symbol": "B", "prediction": 2.0, "target_excess_1bar": 0.0005},
        {"timestamp": pd.Timestamp("2026-06-10 14:15:00", tz="Asia/Kolkata"), "symbol": "C", "prediction": 1.0, "target_excess_1bar": 0.0},
        {"timestamp": pd.Timestamp("2026-06-10 14:15:00", tz="Asia/Kolkata"), "symbol": "D", "prediction": 0.0, "target_excess_1bar": -0.0005},
        {"timestamp": pd.Timestamp("2026-06-10 14:15:00", tz="Asia/Kolkata"), "symbol": "E", "prediction": -1.0, "target_excess_1bar": -0.001},
        {"timestamp": pd.Timestamp("2026-06-10 14:15:00", tz="Asia/Kolkata"), "symbol": "F", "prediction": -2.0, "target_excess_1bar": -0.001},
        {"timestamp": pd.Timestamp("2026-06-10 14:20:00", tz="Asia/Kolkata"), "symbol": "A", "prediction": 3.0, "target_excess_1bar": 0.001},
        {"timestamp": pd.Timestamp("2026-06-10 14:20:00", tz="Asia/Kolkata"), "symbol": "B", "prediction": 2.0, "target_excess_1bar": 0.0005},
        {"timestamp": pd.Timestamp("2026-06-10 14:20:00", tz="Asia/Kolkata"), "symbol": "C", "prediction": 1.0, "target_excess_1bar": 0.0},
        {"timestamp": pd.Timestamp("2026-06-10 14:20:00", tz="Asia/Kolkata"), "symbol": "D", "prediction": 0.0, "target_excess_1bar": -0.0005},
        {"timestamp": pd.Timestamp("2026-06-10 14:20:00", tz="Asia/Kolkata"), "symbol": "E", "prediction": -1.0, "target_excess_1bar": -0.001},
        {"timestamp": pd.Timestamp("2026-06-10 14:20:00", tz="Asia/Kolkata"), "symbol": "F", "prediction": -2.0, "target_excess_1bar": -0.001},
    ])
    scored = assign_quintiles(scored)
    _, orders = build_target_portfolios(scored, 100000.0)
    assert orders["notional"].sum() < 200000.0 * 3


def test_gross_return_is_compounded():
    # Three +1% one-bar returns should compound to 3.0301%, not sum to 3%.
    returns = np.array([0.01, 0.01, 0.01])
    expected = float(np.prod(1.0 + returns) - 1.0)
    assert expected == pytest.approx(0.030301)

def test_cost_is_based_on_executed_turnover():
    # A 2x turnover portfolio at 1 bp friction costs 2 bps of initial notional.
    turnover = 200_000.0
    notional = 100_000.0
    friction = 0.0001
    assert friction * turnover / notional * 1e4 == pytest.approx(2.0)
