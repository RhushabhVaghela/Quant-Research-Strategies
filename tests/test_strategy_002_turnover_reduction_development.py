import pandas as pd

from scripts.run_strategy_002_turnover_reduction_development import build_weights


def test_build_weights_is_market_neutral():
    residual = pd.Series({"A": -0.03, "B": -0.01, "C": 0.02, "D": 0.04})
    weights = build_weights(residual)
    assert abs(weights.sum()) < 1e-12
    assert abs(weights.abs().sum() - 1.0) < 1e-12
    assert weights["A"] == 0.25
    assert weights["C"] == -0.25


def test_build_weights_requires_both_sides():
    residual = pd.Series({"A": -0.03, "B": -0.01, "C": -0.02, "D": -0.04})
    assert build_weights(residual).empty
