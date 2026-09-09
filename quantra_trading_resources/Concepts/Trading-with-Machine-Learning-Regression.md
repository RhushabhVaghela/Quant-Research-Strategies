# Trading with Machine Learning: Regression — Concept Inventory
> Scope: end-to-end linear-regression pipeline to predict GLD (Gold ETF) price highs/lows and build a trading strategy.
> Modules/notebooks enumerated: **11** | Data: `data_modules/*.csv` | Module files: `ReadMe.html`, `Folder Structure and How to Run Code Files.html`
> Core workflow: create input/output parameters → preprocess → pipeline → cross-validated linear regression → predict high/low → generate signals → strategy analytics.
---
## Module: Introduction to Data Generation
### 1. `Import Data and Drop Missing Values.ipynb`
Foundational data-loading and missing-value handling.
**Concepts (with prerequisites):**
- **Data import with pandas** — `pd.read_csv(filename, parse_dates, index_col)` reads tabular CSV files; `parse_dates` parses a column as datetime; `index_col` sets a column as the row index.
 - *Prereq:* what a CSV file is, tabular data, date types.
- **Date indexing** — setting and correctly parsing the `Date` column as a datetime index for time-series data.
 - *Prereq:* datetime data type.
- **Missing-value detection** — `df.isna().sum()` returns a boolean mask of NA cells; `sum()` counts True values (missing entries) per column.
 - *Prereq:* boolean logic, column-wise aggregation.
- **Dropping missing values** — `df.dropna(axis, how, inplace)` removes rows/columns with missing values; `inplace=True` modifies the dataframe directly.
 - *Prereq:* functions returning new vs mutating objects.
### 2. `Create Input and Output Parameters.ipynb`
Builds the regression target (output) and raw feature (input) columns for the model.
**Concepts (with prerequisites):**
- **Target / output parameters** — the quantities the model must predict. Here `Std_U` (upward deviation) and `Std_D` (downward deviation) are computed from OHLC data as the future/predicted values.
 - *Prereq:* dependent vs independent variable.
- **Output formulas** — `Std_U = High − Open` and `Std_D = Open − Low` (upward/downward deviation from the open).
 - *Prereq:* OHLC price bars.
- **Input parameters (features)** — custom indicators engineered from raw prices used as predictors
 - `S_3`, `S_15`, `S_60` — 3/15/60-day moving averages of Close.
 - `Corr` — rolling correlation between Close and S_3.
 - `OD` — change from previous open (`Open − Open.shift(1)`).
 - `OL` — overnight change (`Close.shift(1) − Open`).
 - *Prereq:* moving average, correlation, feature engineering.
- **Rolling/windowed operations** — `Series.rolling(window).mean()` computes a moving window average; `shift(1)` excludes the current value (prevents look-ahead).
 - *Prereq:* window functions, lagging, look-ahead bias.
- **Rolling correlation** — `rolling(window=10).corr()` computes a trailing correlation between two series.
 - *Prereq:* correlation, windowed statistics.
- **Column creation** — computing new columns from existing DataFrame columns with vectorized pandas/numpy operations.
---
## Module: Data Preprocessing
### 3. `Data Preprocessing.ipynb`
Scaling and construction of feature/target matrices.
**Concepts (with prerequisites):**
- **Feature scaling rationale** — features with very different magnitudes cause larger-magnitude features to dominate the model; scaling fixes this.
 - *Prereq:* why scale features (sensitivity of distance/optimisation).
- **Standardization (StandardScaler)** — `StandardScaler().fit_transform(df)` centers data (mean 0) and scales to unit variance (std 1).
 - *Prereq:* mean, standard deviation, z-score.
- **Scaling method** — `fit_transform` on training; fit on train then transform validation/test to avoid data leakage.
 - *Prereq:* train/test discipline, data leakage.
- **Independent vs dependent split** — X holds the features (inputs), Y holds the outcome(s); here y can be the residual/Std columns predicted from X.
 - *Prereq:* features, target, X/y conventions.
- **Missing-value handling (recap)** — `isna().sum()` then `dropna(inplace=True)` to drop rows containing NaN.
 - *Prereq:* NaN handling.
### 4. `Concept of Pipeline.ipynb`
Encapsulating data transforms + estimator into a single object.
**Concepts (with prerequisites):**
- **Pipeline** — chains a sequence of steps executed in order; each step may be a transformer (data processing) or a final estimator (ML model).
 - *Prereq:* what transformers vs estimators are.
- **Pipeline syntax** — list of `(name, transform)` tuples passed to `Pipeline(steps)`, e.g. `[('scaler', StandardScaler()), ('linear', LinearRegression())]`.
 - *Prereq:* Python lists/tuples, scikit-learn API.
- **Reshaping for sklearn** — ML methods expect input shape `(n_samples, n_features)`; `np.reshape(x, (-1, 1))` converts a 1-D array to a 2-D column.
 - *Prereq:* array shapes/dimensions.
- **Train–test split** — 80/20 split splitting the data into training and test portions.
 - *Prereq:* train/test concept.
- **Pipeline `fit`/`predict`** — fitting the pipeline sequentially applies transforms then fits the estimator; `predict` runs the full chain.
 - *Prereq:* fit/predict API.
### 5. `Cross Validation, Test and Train.ipynb`
Hyperparameter tuning with grid search and time-series cross-validation.
**Concepts (with prerequisites):**
- **Hyperparameters** — parameters set before training (the model cannot learn them); e.g. `fit_intercept` for linear regression.
 - *Prereq:* parameters vs hyperparameters.
- **Independent/dependent variables** — X (inputs) and yU/yD (outputs: upward/downward deviation).
 - *Prereq:* features, target.
- **Feature scaling** — using `StandardScaler` inside a pipeline.
 - *Prereq:* scaling.
- **Time-series train–test split** — splitting into train (first 80%) and test (last 20%) preserving chronological order.
 - *Prereq:* why not to shuffle time series, look-ahead bias.
- **Cross-validation** — divide data into training/validation/test to reduce overfitting; model learns on train, tunes on validation, tests on unseen data.
 - *Prereq:* overfitting, validation set.
- **TimeSeriesSplit** — `TimeSeriesSplit(n_splits=5)` splits time-ordered data into 5 expanding training segments; appropriate for temporal data.
 - *Prereq:* cross-validation, time series.
- **GridSearchCV** — exhaustive search over a hyperparameter grid; here `{'linear__fit_intercept': [False, True]}`; uses cross-validation to pick the best.
 - *Prereq:* hyperparameter grid, k-fold CV.
- **Scoring / metric** — `neg_mean_squared_error` (negative MSE, so higher = better; equivalent to minimising MSE).
 - *Prereq:* MSE, sign of loss.
- **Best parameter extraction** — `GridSearchCV.best_params_` retrieves the optimal hyperparameter combination.
 - *Prereq:* optimisation.
---
## Module: Regression
### 6. `Linear Regression and Predicting GLD Movement.ipynb`
Trains linear regression on GLD data and evaluates with MSE.
**Concepts (with prerequisites):**
- **Multiple linear regression** — predicts a continuous output from multiple input features via a linear equation.
 - *Prereq:* linear equation, slope/intercept.
- **Pipeline with scaling + estimator** — `[('scaler', StandardScaler()), ('linear', LinearRegression())]`.
 - *Prereq:* pipeline concept.
- **Feature matrix `X`** — independent variables `['Open', 'S_3', 'S_15', 'S_60', 'OD', 'OL', 'Corr']`.
 - *Prereq:* features.
- **Two targets `yU`, `yD`** — predict upward and downward deviation separately.
 - *Prereq:* target variable, multi-output regression.
- **Hyperparameter tuning** — `fit_intercept` via `GridSearchCV` and `TimeSeriesSplit`; `best_params_` yields `fit_intercept=True`.
 - *Prereq:* hyperparameters, grid search.
- **Model training and prediction** — `reg.fit(X_train, y_train)`, `reg.predict(X_test)` for both targets.
 - *Prereq:* fit/predict.
- **Regression metric — Mean Squared Error (MSE)** — average of squared errors; lower is better; here MSE ≈ 0.10–0.12 interpreted as good performance.
 - *Prereq:* error, squaring, averaging.
---
## Module: Creating the Algorithm
### 7. `Data Preparation.ipynb`
Reproduces feature/target engineering in the strategy-building workflow and inspects data.
**Concepts (with prerequisites):**
- **Data loading and inspection** — reading GLD OHLC data; visual inspection (plotting Close) and `isna().sum()` to check for outliers/missing values.
 - *Prereq:* data inspection, visual checks.
- **Custom indicator creation** — `S_3/S_15/S_60` moving averages, `Corr` rolling correlation, `Std_U`/`Std_D` deviations, `OD`/`OL` differences.
 - *Prereq:* moving average, correlation, feature engineering.
- **Independent/dependent split** — `X = gold_prices[['Open','S_3','S_15','S_60','OD','OL','Corr']]`; `yU = Std_U`; `yD = Std_D`.
 - *Prereq:* features, target, X/y.
- **Saving processed data** — `df.to_csv('input_parameters.csv')` persists prepared features for later notebooks.
 - *Prereq:* CSV I/O.
### 8. `Data Preprocessing and Prediction.ipynb`
Scaling, cross-validated regression, and predicting next-period high/low deviations.
**Concepts (with prerequisites):**
- **Data cleaning** — checking and dropping NaN rows with `dropna(inplace=True)`.
 - *Prereq:* missing-value handling.
- **Feature scaling** — why large-variance features can dominate; `StandardScaler` standardises features.
 - *Prereq:* feature scaling rationale.
- **Pipeline** — `[('scaler', StandardScaler()), ('linear', LinearRegression())]`.
 - *Prereq:* pipeline.
- **Hyperparameters** — `fit_intercept` as a tunable hyperparameter.
 - *Prereq:* hyperparameters.
- **GridSearchCV + TimeSeriesSplit** — cross-validated tuning to avoid overfitting while respecting time order.
 - *Prereq:* grid search, time-series CV.
- **Train-test split** — 70% train / 30% test (chronological).
 - *Prereq:* train/test split.
- **Prediction** — `reg.predict(X_test)` for upward and downward deviations; recovering valid predictions by clipping negatives to 0 (deviations cannot be negative).
 - *Prereq:* domain constraints, inverse transformation.
- **Reconstructing price predictions** — `P_H = Open + yU_predict.shift(1)` and `P_L = Open − yD_predict.shift(1)` to get predicted High/Low; the `shift(1)` on predicted deviations avoids look-ahead when using prior close.
 - *Prereq:* transforming model outputs into price space, look-ahead bias.
- **Model saving** — persisting test predictions with `to_csv('test_dataset_pred_high_low.csv')`.
### 9. `Strategy Analytics.ipynb`
Turns predicted high/low into trading signals, computes returns, and analyzes strategy performance.
**Concepts (with prerequisites):**
- **Signal generation from predictions** — a sell signal (−1) when the actual High > predicted High AND Low > predicted Low (market likely to fall); a buy signal (+1) when actual High < predicted High AND Low < predicted Low (market likely to rise); otherwise 0 (no position).
 - *Prereq:* trading signals, buy/sell/flat states.
- **Position sizing / signal logic** — translating model predictions into discrete positions {−1, 0, +1}.
 - *Prereq:* long/short/flat positioning.
- **Return calculation** — `gld_returns = Close.pct_change()`; `strategy_returns = gld_returns * Signal.shift(1)` (using previous day's signal).
 - *Prereq:* percentage returns, `shift`/lag, look-ahead bias.
- **Cumulative (compound) returns** — `(1 + returns).cumprod()` to compare strategy vs benchmark (GLD) growth.
 - *Prereq:* compounding returns, benchmarking.
- **Strategy vs benchmark comparison** — plotting cumulative strategy returns against GLD buy-and-hold.
### 10. `Performance Analysis.ipynb`
Computes trade-level analytics, Sharpe ratio, and professional performance metrics.
**Concepts (with prerequisites):**
- **Sharpe ratio** — risk-adjusted return; excess return over risk-free rate per unit of volatility; annualised as `sqrt(252) * mean(excess_return)/std dev`.
 - *Prereq:* mean, standard deviation, risk-free rate, annualisation.
- **Long/short position tracking** — identifying entries/exits where the signal changes and recording position, entry/exit dates and prices.
 - *Prereq:* position/state tracking, loops over data.
- **Trade details** — building a `trades` DataFrame with `Position`, `Entry Date`, `Entry Price`, `Exit Date`, `Exit Price`.
 - *Prereq:* DataFrames, iteration.
- **Per-trade PnL** — `PnL = (Exit − Entry) × Position` (sign flips for shorts).
 - *Prereq:* long/short PnL.
- **Strategy analytics** — number of longs/shorts, total trades, gross profit/loss, net profit, winners/losers, win % / loss %, per-trade PnL for winners and losers.
 - *Prereq:* summary statistics, filtering.
- **Benchmarking** — computing GLD returns and strategy returns from the previous day's signal.
 - *Prereq:* returns, lagged signals.
- **Pyfolio tear sheet** — `pf.create_simple_tear_sheet()` generates cumulative returns, drawdowns, volatility, and beta analytics.
 - *Prereq:* performance/risk metrics (cumulative return, drawdown, beta).
- **Interpreting results** — drawdown (decline from a peak), beta (volatility vs benchmark), comparing strategy vs benchmark performance.
 - *Prereq:* risk-adjusted performance concepts.
---
## Module: Applying the Prediction
### 11. `Predict the Next Day's High and Low.ipynb`
Applies the whole workflow to predict and plot the next day's high/low vs actuals.
**Concepts (with prerequisites):**
- **Predictive setup** — using Open and other indicators available at close to predict the next day's High and Low (via deviations).
 - *Prereq:* features, target, prediction framing.
- **Recovering price predictions** — `P_H = Open + yU_predict.shift(1)`, `P_L = Open − yD_predict.shift(1)`; clipping negative deviations to 0 since deviations can't be negative.
 - *Prereq:* output post-processing, domain constraints.
- **Actual vs predicted** — computing actual High/Low from `yU_test`/`yD_test` (`A_H = Open + Std_U`) to compare against predictions.
 - *Prereq:* ground truth vs prediction.
- **Visual comparison** — plotting predicted vs actual High and Low over time to visually assess model fit.
 - *Prereq:* time-series line plots, residual/visual evaluation.
- **Full strategy loop** — linking data generation → scaling → regression → high/low prediction → signal generation → performance analysis.
 - *Prereq:* integration of all preceding concepts.