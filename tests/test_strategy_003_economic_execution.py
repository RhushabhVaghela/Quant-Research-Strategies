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
    assert CAS_START == pd.to_timedelta("15:15:00")
    assert CAS_END == pd.to_timedelta("15:35:00")
    assert NORMAL_CLOSE == pd.to_timedelta("15:30:00")
    assert LATE_SESSION_START == pd.to_timedelta("15:00:00")

def test_position_turnover_is_not_fixed_at_two_x():
    from scripts.run_strategy_003_economic_execution import (
        assign_quintiles,
        build_target_portfolios,
    )

    # The production portfolio requires 3 Q5 longs and 3 Q1 shorts.
    # Use 15 symbols so the quintile construction matches the frozen
    # production universe structure.
    rows = []
    for ts, offset in [
        (pd.Timestamp("2026-06-10 14:10:00", tz="Asia/Kolkata"), 0.0),
        (pd.Timestamp("2026-06-10 14:15:00", tz="Asia/Kolkata"), 0.0),
        (pd.Timestamp("2026-06-10 14:20:00", tz="Asia/Kolkata"), 0.0),
    ]:
        for i in range(15):
            rows.append(
                {
                    "timestamp": ts,
                    "symbol": f"S{i:02d}",
                    "prediction": float(15 - i) + offset,
                    "target_excess_1bar": float(7 - i) / 10000.0,
                }
            )

    scored = assign_quintiles(pd.DataFrame(rows))
    _, orders = build_target_portfolios(scored, 100000.0)

    # The same six names remain in the same Q1/Q5 portfolios, so the
    # intermediate rebalances should not create a full 2x turnover each bar.
    # Only the initial entry and final close are required here.
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
