from scripts.run_strategy_001j_secondary_development import (
    COST_BPS,
    DEVELOPMENT_END,
    DEVELOPMENT_START,
    GRID,
    _configs,
)


def test_secondary_grid_has_exactly_108_configs() -> None:
    assert len(_configs()) == 108


def test_secondary_development_dates_are_frozen() -> None:
    assert DEVELOPMENT_START == "2026-06-10"
    assert DEVELOPMENT_END == "2026-08-19"


def test_secondary_cost_grid_is_frozen() -> None:
    assert COST_BPS == (0, 5, 10, 15, 20)


def test_secondary_grid_contains_registered_values() -> None:
    configs = _configs()
    assert {c.z_threshold for c in configs} == set(GRID["z_threshold"])
    assert {c.holding_bars for c in configs} == set(GRID["holding_bars"])
    assert {c.cooldown_bars for c in configs} == set(GRID["cooldown_bars"])
