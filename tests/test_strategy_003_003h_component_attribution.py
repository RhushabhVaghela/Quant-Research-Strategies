"""Unit tests for Strategy 003H component attribution."""
from __future__ import annotations
from scripts.run_strategy_003_003h_component_attribution import BASE, COMPONENTS

def test_locked_components_exactly_match_003h():
    assert BASE == ["close_location_1bar","intraday_position_60bar","bars_since_session_open"]

def test_component_specs_are_singletons_pairs_and_reference():
    lengths=sorted(len(v) for k,v in COMPONENTS.items() if k!="all_three")
    assert lengths == [1,1,1,2,2,2]
    assert COMPONENTS["all_three"] == BASE

def test_no_new_variables_or_transforms():
    assert set(sum(COMPONENTS.values(), [])) == set(BASE)
