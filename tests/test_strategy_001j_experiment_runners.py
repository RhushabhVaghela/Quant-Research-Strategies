from scripts.run_strategy_001j_development_grid import GRID, _configs
from scripts.run_strategy_001j_holdout import HOLDOUT_END, HOLDOUT_START


def test_development_grid_is_preregistered_162_configs():
    assert len(_configs()) == 162
    assert GRID["lookback_bars"] == (20, 30, 40)
    assert GRID["z_threshold"] == (1.5, 2.0, 2.5)
    assert GRID["trend_bars"] == (3, 6, 9)
    assert GRID["holding_bars"] == (3, 6, 9)
    assert GRID["cooldown_bars"] == (6, 12)


def test_holdout_dates_are_frozen():
    assert HOLDOUT_START == "2026-08-20"
    assert HOLDOUT_END == "2026-09-17"
