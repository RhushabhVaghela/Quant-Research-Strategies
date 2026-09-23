"""Tests for the frozen Strategy 003 protected validation."""
from scripts.run_strategy_003_protected_validation import (
    FEATURES,
    HOLDOUT_START,
    VALIDATION_END,
    VALIDATION_START,
)


def test_frozen_features_are_exact():
    assert FEATURES == ["close_location_1bar", "intraday_position_60bar"]


def test_validation_boundary_is_before_holdout():
    assert VALIDATION_END < HOLDOUT_START
    assert VALIDATION_START < VALIDATION_END
