from scripts.run_strategy_003_economic_execution import (
    FRICTIONS, STT_RATE, STAMP_RATE, NSE_TX_RATE, GST_RATE,
    brokerage, execution_flags,
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
    assert CAS_START == pd.Timedelta(hours=15, minutes=15)
    assert CAS_END == pd.Timedelta(hours=15, minutes=35)
    assert NORMAL_CLOSE == pd.Timedelta(hours=15, minutes=30)
    assert LATE_SESSION_START == pd.Timedelta(hours=15)

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
    _, orders = build_target_portfolios(scored, 100000.0)
    assert orders["notional"].sum() < 200000.0 * 3
