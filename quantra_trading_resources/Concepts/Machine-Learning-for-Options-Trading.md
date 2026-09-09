# Machine Learning for Options Trading — Concept Inventory
## Notebooks & Modules Enumerated
**Notebooks (24 unique):**
| Module | Notebook |
|---|---|
| Options Data: Sourcing and Storing | `Options Data Storing.ipynb`, `Working With Pickle File.ipynb` |
| Implied Volatility Concepts | `Implied Volatility Calculation.ipynb` |
| Features to Predict the Underlying | `Predictor and Target Variables.ipynb` |
| Forecasting Direction with Decision Tree Classifier | `Decision Tree Classifier to Forecast the Underlying.ipynb` |
| Metrics to Evaluate a Classifier | `Metrics to Evaluate a Classifier.ipynb` |
| Ensemble Classifiers | `Voting Classifier Model.ipynb` |
| Blending Models | `Blending of Machine Learning Models.ipynb` |
| Options Pricing: Feature Engineering | `Features for Options Pricing.ipynb` |
| ML for Options Pricing | `Predicting Options Prices.ipynb`, `Options Pricing with Multiple Models.ipynb` |
| Defining the Best Option Strategy to Trade | `Creating the Target Variable - Strategy Design.ipynb`, `Creating the Target Variable Using Strategy Returns.ipynb` |
| Input Features for Predicting the Best Option Strategy | `Creating the Input Features.ipynb` |
| Forecasting Implied Volatility | `Forecasting IV.ipynb` |
| Model Design and Backtesting the Performance | `Machine Learning Model Design.ipynb`, `Backtest the Predicted Strategies.ipynb`, `Strategy Analytics of Predicted Strategies.ipynb`, `Trade Level Analytics of Predicted Strategies.ipynb` |
| Options Trading with Decision Trees Classifier | `Set Up the Call Spread Strategy.ipynb`, `Backtesting Options Spread Strategy.ipynb` |
| Trade Level Analytics | `Trade Level Analytics of ML Based Spread Trading Strategy.ipynb` |
| Trading Options Using Forecasted IV Values | `Backtest Short Straddle Strategy.ipynb` |
| Probability Levels For Improving ML Model | `Implementation of Probability Level in ML Model.ipynb` |
| Challenges in Live Trading | `Save Train and Simulate ML Model.ipynb` |
| Capstone Project | `Capstone Project Model Solution.ipynb` |
---
## Data Sourcing & Storage
### `Options Data Storing.ipynb`
- Loads SPX EOM options & underlying market data; prepares raw options-chain datasets for feature/target engineering.
### `Working With Pickle File.ipynb`
- **Concept:** pickle/bz2 serialization for options data; retains column dtypes (DatetimeIndex preserved), compresses memory.
- **Pitfall:** pickle is Python-version-specific; backward compatible (lower-version pickles readable in higher versions, not vice versa).
- Step: read CSV → convert index to `DatetimeIndex` → `df.to_pickle("file.bz2")` → reload; `platform.python_version()`.
## Implied Volatility (IV)
### `Implied Volatility Calculation.ipynb`
- **Concept:** implied vol — expected volatility by market participants; useful for forecasting underlying price moves.
- **Prereq:** Black-Scholes, mibian library, option pricing inputs.
- Uses `mibian.BS(...).impliedVolatility` over (underlying close, strike, rate, DTE, call/put price) on `spx_eom_options_2022.csv`; datetime parsing of QUOTE_DATE/EXPIRE_DATE.
## Predicting the Underlying Direction — Feature Build
### `Features to Predict the Underlying/Predictor and Target Variables.ipynb`
- **Concept:** engineer underlying-price prediction features (f_* columns: lagged returns f_ret_1/5/10/22/44/88 etc.) & binary target (price up/down).
- **Prereq:** technical indicators (talib), time-series feature engineering, classifier target (binary up/down).
- Builds SPY feature/target frame saved as `spy_features_target_2009_2022.csv`.
## Decision Tree Classifier — Forecast the Underlying
### `Decision Tree Classifier to Forecast the Underlying.ipynb`
- **Concept:** learn decision rules from training data & apply tree to forecast SPY direction (1 up / 0 down) next day.
- **Prereqs:** decision tree classifier, feature importance, train/test split, classifier metrics (accuracy).
- Reads `spy_features_target_2009_2022.csv`; `X = spy.filter(like='f_')`, target binary; feature importance; evaluate strategy performance; saves `spy_predicted_2018_2022.csv` / `spy_expected_target_2018_2022.csv`.
## Classifier Evaluation Metrics
### `Metrics to Evaluate a Classifier.ipynb`
- **Concept:** classifier accuracy is sensitive to class distribution — biased under imbalance; use **precision, recall, F1-score** which are less distribution-sensitive.
- **Prereq:** classifier metrics, confusion matrix, classification report.
- Reads predicted vs expected target (`spy_predicted_2018_2022`, `spy_expected_target_2018_2022`); computes `confusion_matrix`, `ConfusionMatrixDisplay`, `classification_report` (precision/recall/F1).
## Ensemble Classifiers — Voting
### `Ensemble Classifiers/Voting Classifier Model.ipynb`
- **Concept:** ensembles — voting classifier aggregates outputs of multiple ML models into one final prediction.
- **Prereqs:** ensembles, XGBoost, Logistic Regression, SVM, ensemble aggregation / hard-soft voting.
- Reads `sp500_features_Jan_2009_June_2022.csv`; splits & scales (StandardScaler); fits `XGBClassifier`, `LogisticRegression`, `svm.SVC`, aggregates via `sklearn.ensemble.VotingClassifier`; accuracy_score.
## Blending Models
### `Blending of Machine Learning Models.ipynb`
- **Concept:** blending / stacked generalization — train a meta-model ("blender") on the base learners' outputs to intelligently weight them (e.g., down-weights a base model in trending markets).
- **Prereq:** ensembles, base learners output→meta-features, stacking.
- Base learners: `XGBClassifier`, `LogisticRegression`, `svm`, `DecisionTreeClassifier`, `ExtraTreesClassifier`, `AdaBoostClassifier`; train/predict each base model, feed predictions to a blender to classify SPY up/down; accuracy measures.
---
## Options Pricing with ML
### `Options Pricing_ Feature Engineering/Features for Options Pricing.ipynb`
- **Concept:** feature engineering for option price prediction: three data sets (options chain, interest rate as 1-year US Treasury yield risk-free rate, underlying S&P500 index).
- **Prereq:** options pricing, feature engineering, risk-free rate, underlying OHLCV.
- Features stored as `features_data_options_pricing.csv`; uses `1_year_treasury_rate_yield.csv`.
### `ML for Options Pricing/Predicting Options Prices.ipynb`
- **Concept:** predict option prices with **MLP Regressor** (4 hidden layers) using engineered features.
- Prereqs: neural-net regression, feature set, scaling, R² metric.
### `ML for Options Pricing/Options Pricing with Multiple Models.ipynb`
- **Concept:** compare multiple regression models for option price prediction — MLP Regressor, Lasso, Random Forest, Decision Tree Regressor.
- **Prereq:** regressor metrics (R²), StandardScaler, feature data.
- Imports `features_data_options_pricing.csv`; trains all → visually compares R² performance.
## Defining the Best Option Strategy to Trade
### `Creating the Target Variable - Strategy Design.ipynb`
- **Concept:** design a strategy universe — enumerate candidate options trading strategies (straddles/strangles/spreads across delta/moneyness), then find `atm_strike_price` (strike minimizing `[STRIKE_DISTANCE_PCT]`).
- **Prereq:** options strategy construction, strikes/moneyness, itertools combinations.
- Reads `spx_eom_options_2010_2022.bz2` + `sp500_index_2010_2022.csv`; builds strategy combination table `strategies_combinations_mlo.csv`.
### `Creating the Target Variable Using Strategy Returns.ipynb`
- **Concept:** compute 3-day returns of call/put/underlying each day, derive 3-day returns of all strategies, and set the **target variable = strategy with max returns** per day.
- **Prereq:** option margin/capital (premium×lot size), covariance/mark-to-market, target construction.
- Reads strategies + underlying `underlying_data_strategy_design_mlo.csv`; uses buy/sell capital: buying an option → premium × lot size (margin); returns → target column.
## Creating the Input Features (Strategy prediction)
### `Creating the Input Features.ipynb`
- **Concept:** build input features from three families for predicting the best strategy: (a) underlying-asset features, (b) **options Greeks** features, (c) options-contract features; plus the target.
- **Prereq:** option greeks (delta/gamma/vega/theta), underlying indicators, feature engineering.
- Reads `underlying_data_options_target_variable_2010_2022.csv`; `spx_eom_expiry_options_2010_2022.bz2`; builds feature+numerical target (strategy_* returns; `max_returns_strategy`).
## Forecasting Implied Volatility (ML Regressor)
### `Forecasting IV .ipynb`
- **Concept:** forecast the next day's iv via **Random Forest regressor** using technical indicators (MACD, RSI, NATR, OBV, ADX) + IV features.
- **Prereqs:** implied vol, RandomForestRegressor, technical indicators, TimeSeriesSplit, GridSearchCV.
- Cleans col names (strip brackets), filters to needed columns, quality checks, feature creation, prediction function, actual-vs-predicted results → short-straddle trading.
---
## Model Design (LSTM) & Backtesting the Predicted Strategy
### `Machine Learning Model Design.ipynb`
- **Concept:** design an **LSTM** classifier/regressor to pick the best strategy; include feature encoding & scaling, LSTM architecture (dropout, dense), accuracy/loss curves.
- **Prereq:** LSTM, to_categorical encoding, StandardScaler, classifier metrics (confusion, f1, accuracy).
- Reads SPX EOM options; builds sequence model to classify the best-strategy labels; plots accuracy/loss; accuracy analysis.
### `Backtest the Predicted Strategies.ipynb`, `Strategy Analytics of Predicted Strategies.ipynb`, `Trade Level Analytics of Predicted Strategies.ipynb`
- **Concept:** backtest the ML-predicted strategies: rule-signal validation, backtest across dates, and trade-level analytics.
- **Prereq:** backtesting, predicted labels (`predicted_labels_lstm_mlo.csv`), round-trips, trade-level P&L.
- Compute predicted-vs-actual, round-trips/mark-to-market (`round_trips_lstm_mlo.csv`, `mark_to_market_lstm_mlo.csv`, `trades_lstm_mlo.csv`); trade-level analytics.
## Options Trading with Decision Trees — Call Spread Strategy
### `Set Up the Call Spread Strategy.ipynb`, `Backtesting Options Spread Strategy.ipynb`
- **Concept:** construct & backtest a **call spread** options strategy driven by decision-tree forecast of the underlying.
- **Prereq:** decision tree, call spread (bull call spread), round trips, best-option selection, backtesting.
- Sets up call spread from SPX EOM data; backtests strategy performance (`trades_call_spread.csv`, `round_trips_call_spread.csv`, `mark_to_market_call_spread.csv`).
## Trade Level Analytics of ML Spread Strategy
### `Trade Level Analytics of ML Based Spread Trading Strategy.ipynb`
- **Concept:** per-trade analytics for the ML-based spread strategy.
- **Prereq:** trade-level analytics utilities, round-trips, P&L post-costs.
- Reads trades/round-trips/mtm for call-spread.
## Trading Options Using Forecasted IV
### `Trading Options Using Forecasted IV Values/Backtest Short Straddle Strategy.ipynb`
- **Concept:** use forecasted (below-current) implied vol to short straddle / trade strategy, backtest.
- **Prereq:** forecasted IV, short straddle, strategy return.
- Backtests short straddle for forecasted IV values; trade-level analytics.
## Probability Levels for Improving ML Model
### `Probability Levels For Improving ML Model/Implementation of Probability Level in ML Model.ipynb`
- **Concept:** improve a classifier/threshold via probability (class-probability threshold) instead of hard 0.5 cutoff to trade signal.
- **Prereq:** classifier metrics, predicted probabilities, threshold tuning.
- Plots/uses predicted probabilities to set a probability level → ML signals (`spy_signals_2018_2022.csv`, `spy_predicted_2018_2022.csv`).
## Challenges in Live Trading
### `Challenges in Live Trading/Save Train and Simulate ML Model.ipynb`
- **Concept:** persist a trained classifier (pickle `model_save.pkl`), re-load, and simulate/trade SPY likewise for early vessel anomaly.
- **Prereq:** pickle serialization, decision tree classifier, talib technical features, live/resimulation flow.
- Trains DecisionTreeClassifier on SPY OHLCV (`spy_daily_2009_2022.csv`), saves & reloads model, generates signals for simulated live run.
---
## Capstone Project
### `Capstone Project Model Solution.ipynb`
- **Concept:** end-to-end capstone: predict the best options strategy to deploy, using logistic regression classifier.
- **Prereqs:** feature engineering (underlying-asset, option greeks, contract features), strategy calculations, scaling, logistic regression, classifier metrics.
- Imports SPX options + underlying data; engineers features; computes strategies / target is best-strategy; StandardScaler; fits `LogisticRegression`; performance analysis (accuracy, confusion matrix, ROC/AUC, recall).
---
## Python Module
- Helper utilities (metrics, strategy returns, signal/backtesting helpers) reused across notebooks; `.pyc` cache present for cpython-311.
---
**Key concept graph:** data sourcing → IV calc → IV forecasting (Random Forest) & underlying forecast → decision tree → classifier metrics (precision/recall/F1) → ensembles (voting, blending) → options price ML (MLP/Lasso/RF/DT) → strategy design (best-option target via strategy returns) → input features (underlying + options greeks + contract) → LSTM strategy learner → backtest/analytics → call spread, short straddle, live save/simulate → capstone logistic-regression.