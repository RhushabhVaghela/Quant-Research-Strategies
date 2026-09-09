# Quantra Strategy Template Inventory

This inventory maps the supplied Quantra templates into research building blocks for the intraday strategy project.

## Intraday / execution-oriented

| Template | Potential research use | Initial assessment |
|---|---|---|
| `intraday_momentum_strategy.py` | Intraday momentum baseline/features | High relevance |
| `backtesting_order_flow_strategy.ipynb` | Order-flow concepts and event features | High relevance, data-dependent |
| `trading_in_milliseconds_MFT_strategies_alpaca_paper_trade.py` | Streaming/execution architecture reference | Useful architecture reference; not direct Zerodha implementation |
| `volume_reversal_strategy.py` | Price-volume reversal hypothesis | Useful feature/hypothesis source |
| `candlestick_pattern_strategy.py` | Candlestick/event features | Feature source, not final strategy |

## Momentum / trend building blocks

- `time_series_momentum_strategy.py`
- `long_short_momentum_trading_strategy.py`
- `moving_average_crossover_momentum_strategy.py`
- `creating_momentum_based_portfolio_strategy.py`
- `moving_average_strategy.py`
- `moving_averages.py`
- `technical_indicators_based_momentum_strategy.py`
- `ichimoku_cloud_strategy.py`
- `support_level_strategy.py`
- `divergence_strategy.py`

Use primarily as signal/feature references. Do not treat simple indicator rules as the final project objective.

## Mean reversion / statistical arbitrage

- `mean_reversion_strategy.py`
- `mean_reversion_strategy_2.ipynb`
- `pairs_trading_strategy.py`
- `pairs_trading_strategy_2.py`
- `hurst_exponent_strategy.py`

These are important for studying spread dynamics, stationarity, mean reversion and regime-dependent behavior.

## Machine learning

- `decision_tree_classifier_model.py`
- `support_vector_classifier_strategy.py`
- `random_forest_strategy.py`
- `machine_learning_classification_strategy.ipynb`
- `machine_learning_regression_trading_strategy.py`
- `mlp_classifier_trading_strategy.py`
- `bow_xgboost.py`
- `tfidf_xgboost.py`
- `xgboost_model.ipynb`
- `trading_rules_using_regression_tree_model.ipynb`

These provide candidate model implementations and patterns. Model choice must follow the research question and validation evidence.

## Clustering / regime detection

- `k_means_strategy.py`
- `k-means_clustering_strategy.ipynb`

Potentially useful for unsupervised market-regime features, provided regime construction does not leak future information.

## Volatility / risk

- `GARCH.py`
- `backtest_and_trade-level_analytics_of_GARCH_forecast.ipynb`
- `volatility_targeting_method.py`
- `forward_volatility_strategy.py`
- `volatility_skew_strategy.ipynb`
- `volatility_smile_strategy.ipynb`

Useful for volatility forecasting, regime features and position sizing. Options-specific material should be separated from the first equity research phase.

## Options

- `backtest_short_butterfly.ipynb`
- `backtest_short_straddle_strategy.ipynb`
- `butterfly_options_strategy.py`
- `decision_tree_option_strategy.py`
- `options_expiration_week_effect.ipynb`
- `forward_volatility_strategy.py`
- `volatility_skew_strategy.ipynb`
- `volatility_smile_strategy.ipynb`

Potential future strategy family after the core intraday framework is established.

## FX / macro-style relative value

- `fx_value_strategy.ipynb`
- `value_forex_strategy.py`
- `arima_model_prediction_strategy.py`

Potential future asset-class research. Some templates are not intraday by design, so their ideas must be adapted and revalidated rather than copied.

## Portfolio / position sizing / allocation

- `constant_proportion_portfolio_insurance.py`
- `portfolio_based_on_kelly_criterion.py`
- `weight_allocation_using_hrp.py`
- `modern_portfolio_theory.ipynb`
- `volatility_targeting_method.py`

These are mainly portfolio/risk components rather than standalone intraday signals.

## Reinforcement learning

- `quantra_reinforcement_learning.py`
- `reinforcement_learning_live_template.py`
- `reinforcement_learning_on_real_world_price_data.ipynb`

Interesting for later experimentation, but should not be the first strategy family. RL introduces additional modeling and evaluation complexity and should be justified by the problem.

## Other / reference material

- `buy_and_hold_strategy.py`
- `short_selling_in_trading.py`
- `turn_of_the_month_strategy.py`
- `selective_long_on_vix_strategy.py`
- `strategy_analytics.ipynb`

`strategy_analytics.ipynb` is especially useful as a reference for standardized trade-level and performance analysis.

## Key takeaway

The strongest immediate building blocks for our first intraday research program are:

1. Intraday momentum / price-event behavior.
2. Volume and volatility context.
3. Regime detection.
4. Classical statistical baselines.
5. Tree-based ML as a conditional signal/filter model.
6. Volatility-aware risk management.
7. Standardized trade-level and portfolio analytics.
8. Streaming/API architecture only after the research signal survives backtesting.

The templates are educational/reference material. They are not assumed to be profitable or production-ready.