"""Tests for Strategy 003H economic-form decomposition."""
from scripts.run_strategy_003h_economic_form_decomposition import FEATURES, SPECS


def test_locked_features_are_exact():
    assert FEATURES == ["close_location_1bar", "intraday_position_60bar"]


def test_exactly_four_preregistered_specs():
    assert list(SPECS) == [
        "close_location_only",
        "intraday_position_only",
        "additive_core",
        "joint_interaction",
    ]


def test_no_unregistered_raw_features():
    allowed = set(FEATURES + ["close_location_x_intraday_position"])
    assert set(sum(SPECS.values(), [])) == allowed


def test_interaction_is_only_joint_extension():
    assert SPECS["joint_interaction"][-1] == "close_location_x_intraday_position"
    assert SPECS["additive_core"] == FEATURES
