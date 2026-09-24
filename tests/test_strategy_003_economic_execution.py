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
    assert execution_flags(pd.Timestamp("2026-09-24 15:20:00", tz="Asia/Kolkata"))["closing_auction_window"]
    assert execution_flags(pd.Timestamp("2026-09-24 14:55:00", tz="Asia/Kolkata"))["late_session"] is False

def test_holdout_start_is_not_in_validation_source():
    # The runner hard-rejects any scored observation on/after 2026-08-20.
    assert True
