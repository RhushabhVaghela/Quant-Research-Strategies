"""Tests for the preregistered Strategy 003H lineage separation experiment."""
from scripts.run_strategy_003h_lineage_separation import CORE, LINEAGE, SPECS


def test_core_is_locked_two_variable_003h_attribution_result():
    assert CORE == ["close_location_1bar", "intraday_position_60bar"]


def test_lineage_representations_are_fixed():
    assert LINEAGE == ["strategy_001_event", "strategy_002_prior_loo_residual"]
    assert len(SPECS) == 5


def test_no_unregistered_features():
    allowed = set(CORE + LINEAGE)
    assert set(sum(SPECS.values(), [])) == allowed


def test_combined_spec_is_union_of_registered_sources():
    assert SPECS["003h_plus_001_plus_002"] == CORE + LINEAGE
