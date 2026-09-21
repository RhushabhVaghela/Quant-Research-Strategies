import pandas as pd

from scripts.run_strategy_002_turnover_decomposition import (
    build_target_weights,
    calculate_turnover,
)


def test_target_weights_are_market_neutral():
    residual = pd.Series({"A": -0.02, "B": -0.01, "C": 0.01, "D": 0.02})
    weights = build_target_weights(residual)
    assert weights["A"] == 0.25
    assert weights["B"] == 0.25
    assert weights["C"] == -0.25
    assert weights["D"] == -0.25
    assert abs(weights.sum()) < 1e-12
    assert abs(weights.abs().sum() - 1.0) < 1e-12
    assert weights.dtype == "float64"


def test_turnover_between_rebalanced_target_portfolios():
    previous = pd.Series({"A": 0.5, "B": 0.5, "C": 0.0, "D": 0.0})
    current = pd.Series({"A": 0.0, "B": 0.0, "C": -0.5, "D": -0.5})
    result = calculate_turnover(previous, current)
    assert abs(result["one_way_turnover"] - 1.0) < 1e-12
    assert abs(result["absolute_weight_change"] - 2.0) < 1e-12
    assert abs(result["opened_notional"] - 1.0) < 1e-12
    assert abs(result["closed_notional"] - 1.0) < 1e-12
    assert abs(result["flipped_notional"]) < 1e-12
    assert abs(result["unchanged_notional"]) < 1e-12


def test_first_portfolio_has_no_prior_target_turnover():
    previous = pd.Series(dtype=float)
    current = pd.Series({"A": 0.5, "B": 0.5, "C": -0.5, "D": -0.5})
    result = calculate_turnover(previous, current)
    assert pd.isna(result["one_way_turnover"])
    assert pd.isna(result["opened_notional"])


def test_side_flip_counts_both_old_and_new_notional():
    previous = pd.Series({"A": 0.5, "B": -0.5})
    current = pd.Series({"A": -0.25, "B": 0.25})
    result = calculate_turnover(previous, current)
    assert abs(result["flipped_notional"] - 1.5) < 1e-12
