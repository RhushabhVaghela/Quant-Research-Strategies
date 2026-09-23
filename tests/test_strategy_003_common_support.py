"""Tests for common-support nested mechanism comparison."""

from scripts.run_strategy_003_common_support import BASE, BLOCKS

def test_base_is_locked():
    assert BASE == ["close_location_1bar", "intraday_position_60bar", "bars_since_session_open"]

def test_blocks_are_fixed():
    assert set(BLOCKS) == {"activity","volatility","market_context"}
