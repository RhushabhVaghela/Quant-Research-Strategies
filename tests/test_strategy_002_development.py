"""Tests for the Strategy 002 development runner registration."""

from scripts.run_strategy_002_development import (
    LOOKBACKS, ENTRY_ZS, EXIT_ZS, HOLDINGS, COOLDOWNS,
    DEV_START, DEV_END, DEV_END_EXCLUSIVE, COST_BPS, PAIR_COST_LEG_MULTIPLIER,
)


def test_registered_grid_has_108_configurations():
    assert len(LOOKBACKS) * len(ENTRY_ZS) * len(EXIT_ZS) * len(HOLDINGS) * len(COOLDOWNS) == 108


def test_development_window_is_frozen():
    assert DEV_START == "2026-06-10"
    assert DEV_END == "2026-08-19"
    assert DEV_END_EXCLUSIVE == "2026-08-20"


def test_pair_cost_sensitivity_is_two_leg_round_trip():
    assert COST_BPS == (0, 5, 10, 15, 20)
    assert PAIR_COST_LEG_MULTIPLIER == 2
