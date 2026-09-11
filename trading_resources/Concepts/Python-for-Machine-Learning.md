# Python for Machine Learning — Concept Inventory
## COURSE: Python for Machine Learning
A () beginner course that teaches Python fundamentals in the context of machine learning for trading, then walks through a complete ML classification workflow on intraday (15-min) J.P. Morgan data: feature/target engineering, train-test split, model training/forecasting with a RandomForestClassifier, classifier evaluation metrics, backtesting, and regression evaluation with R-squared.
Notebooks enumerated (11): `My First Jupyter Notebook`, `Operations and Functions in Python`, `DataFrame and Basic Functionality`, `Target and Features`, `Data Visualisation`, `Importing Time Series Data`, `Train-Test Split`, `Model Training and Forecasting`, `Metrics to Evaluate a Classifier`, `R-Squared`, `Strategy Backtesting`. Data modules (CSV only, no Python modules): `coca_cola_price.csv`, `JPM_2017_2019.csv`, `jpm_and_bac_price.csv`, `jpm_and_bac_price_2019.csv`, `JPM_features_2017_2019.csv`, `JPM_features_testing_2017_2019.csv`, `JPM_features_training_2017_2019.csv`, `JPM_predicted_2017_2019.csv`, `JPM_target_2017_2019.csv`, `JPM_target_testing_2017_2019.csv`, `JPM_target_training_2017_2019.csv`, `predicted_jpm_and_nestle_price_2019.csv`.
---
## MODULE: Introduction to Python
### LESSON: My First Jupyter Notebook
- **Programming** — the act of telling a machine what to do via code; also called developing or coding. prereqs: none.
- **Python** — a language favoring coding productivity, readability, and simplified English-like syntax. prereqs: none.
- **Jupyter notebook cell semantics** — run code cells with Shift + Enter; output appears below the cell. prereqs: none.
- **Code comments** — non-executed notes created with `#` (single-line/multi via `#`) or triple quotes `""" """` (multi-line). prereqs: none.
- **`print()` statement** — outputs text/variables to the console. prereqs: none.
- **Variables** — named storage for values, repeatable across code; the `=` sign means "is set to", not "equals". prereqs: none.
- **Data types** — integers (whole numbers), floats (real numbers, defined as decimal e.g. `5.0` or via `float(5)`), strings (text in `''` or `""`), booleans (True/False). prereqs: variables.
- **`type()` function** — returns the data type of a variable. prereqs: variables.
- **Case sensitivity** — Python is case-sensitive (`gold_price` vs `Gold_Price` are different). prereqs: variables.
- **Indentation** — Python enforces consistent white-space indentation within code blocks; incorrect indentation raises an error. prereqs: none.
- **Simple returns** — percentage change `(Final/Initial - 1) * 100` of a stock price. prereqs: variables, print.
- **Log returns (intro)** — natural log of final/initial price; the basis of later return analysis. prereqs: simple returns.
### LESSON: Operations and Functions in Python
- **Mathematical operators** — `+`, `-`, `*`, `/`, exponents `**`, remainder/modulo `%`. prereqs: variables.
- **Built-in math functions** — `abs()`, `round()`, `max()`, `min()`, `sum()`. prereqs: none.
- **`import`** — keyword to bring in a library (`import math`); exposing its functions to the program. prereqs: none.
- **Comparison (logical) operators** — `==`, `!=`, `<`, `>`, `<=`, `>=`; return boolean True/False. prereqs: booleans.
- **Logical operators** — `not`, `or`, `and` with their truth tables over assertions P and Q. prereqs: comparison operators.
- **Functions** — reusable blocks of code defined with `def name(params):` and indented body; promote clean, modular code. prereqs: none.
- **Variable scope** — a variable created inside a function is only usable inside it; values are exported via `return`. prereqs: functions.
- **Function parameters** — inputs passed into a function, separated by commas. prereqs: functions.
- **Return statement** — passes a computed value out of a function so it can be stored in a wider-scope variable. prereqs: functions, scope.
### LESSON: DataFrame and Basic Functionality
- **DataFrame** — pandas' spreadsheet-like structure storing data in named rows and columns; the core tabular data structure. prereqs: pandas.
- **`pd.DataFrame(data, index)`** — constructor creating a dataframe. prereqs: pandas import.
- **Index vs columns** — columns are named fields; index labels rows (default integer 0..n or a set column). prereqs: dataframe.
- **`set_index()`** — sets a column as the dataframe index for label-based access. prereqs: dataframe.
- **`pd.read_csv(filename, index_col)`** — reads a CSV into a dataframe; `index_col` chooses the index column (0-based). prereqs: pandas.
- **OHLCV price columns** — Open, High, Low, Close, Adj Close, Volume. prereqs: financial data.
- **`head(n)` / `tail(n)`** — show first/last n rows (default 5). prereqs: dataframe.
- **`loc[index]` (label-based access)** — selects rows by index label; slicing start:stop is inclusive of both ends. prereqs: dataframe.
- **`iloc[index]` (position-based access)** — selects rows by integer position; slicing start:stop excludes the stop. prereqs: dataframe.
- **Boolean indexing** — filtering a dataframe with a boolean condition, e.g. `df[quantity_owned > 5000]`. prereqs: logical operators.
- **Column access** — `df[col_name]` accesses a single column. prereqs: dataframe.
- **`drop()`** — removes rows or columns from a dataframe. prereqs: dataframe.
- **Adding columns** — assign a computed series (e.g. 10-period moving average `rolling().mean()`) as a new column. prereqs: dataframe.
- **Moving average (intro)** — rolling mean over a window via `rolling(10).mean()`. prereqs: dataframe.
---
## MODULE: Financial Market Data and Visualisation
### LESSON: Importing Time Series Data
- **Time series data import methods** — (a) Python package download, (b) reading a CSV; here the focus is CSV and `yfinance`. prereqs: none.
- **`pip install yfinance`** — installing the Yahoo Finance data package. prereqs: pip.
- **`yf.download(ticker, start, end)`** — downloads OHLCV from Yahoo Finance. prereqs: yfinance.
- **Adjusted vs raw price** — `auto_adjust=True` returns adjusted prices (corporate-action corrected). prereqs: yfinance.
- **CSV (Comma Separated Values)** — plain-text tabular format with comma separators. prereqs: none.
- **`pd.to_datetime(index)`** — converts a string index to a datetime index enabling time operations. prereqs: pandas.
### LESSON: Data Visualisation
- **Data visualisation** — graphical representation used to draw insights from data. prereqs: none.
- **`matplotlib.pyplot` import & style** — `import matplotlib.pyplot as plt`, `%matplotlib inline`, `plt.style.use()`. prereqs: none.
- **Line graph** — `dataframe.column.plot(figsize, color)` to plot a price series. prereqs: matplotlib.
- **Plot labels** — `plt.title`, `plt.xlabel`, `plt.ylabel` (with `fontsize`). prereqs: matplotlib.
- **Scatter plot** — `plt.scatter(col1, col2)` studies the relationship between two variables. prereqs: matplotlib.
- **Histogram** — `df[col].plot(kind='hist')` shows the distribution of a variable (e.g. daily returns). prereqs: pandas plot.
- **Interpretation of visual** — line range, co-moving assets from scatter, return distribution from histogram. prereqs: line/scatter/histogram.
---
## MODULE: Target Variable and Features
### LESSON: Target and Features
- **Problem statement** — decide whether to go long/buy JPM at a given time; frames the ML task. prereqs: none.
- **Target variable (y)** — what the model predicts to solve the problem; a binary `signal` column (1 = buy, 0 = do not buy). prereqs: none.
- **`pct_change()`** — computes percentage change of a price series. prereqs: pandas.
- **`shift(period)`** — shifts a series; combined as `pct_change().shift(-1)` to get *future* returns as the target. prereqs: pct_change.
- **Features (X)** — input variables with predictive power for the target. prereqs: none.
- **Prior percentage-change features** — prior 15-min, 30-min, 75-min returns as inputs. prereqs: pct_change, shift.
- **Technical-indicator features** — RSI and ADX computed via `talib` `ta.RSI(data, timeperiod)` / `ta.ADX(high, low, open, timeperiod)`. prereqs: talib.
- **Rolling features** — `rolling(window).mean()` (SMA) and `rolling(window).corr()` (rolling correlation) of close. prereqs: pandas.
- **Volatility feature** — rolling standard deviation of the `pct_change` column. prereqs: pct_change, rolling.
- **Create X and y** — drop rows with missing values, store `signal` in `y` and engineered columns in `X`, excluding raw OHLCV columns. prereqs: features, target.
- **Stationarity check** — `from statsmodels.tsa.stattools import adfuller`; if p-value ≤ 0.05 reject H0 (feature stationary), else drop. Most ML algorithms require stationary features. prereqs: ADF test.
- **Correlation check** — drop features with pairwise correlation above a threshold (e.g. 0.7) to remove redundancy. prereqs: correlation.
- **`to_csv()`** — exports X and y dataframes to disk for reuse in later notebooks. prereqs: pandas.
---
## MODULE: Train-Test Split
### LESSON: Train-Test Split
- **Train-test split** — splitting data into training and testing portions to evaluate generalization. prereqs: features, target.
- **Training vs testing data** — model is trained on `train_data` and evaluated on `test_data` (unseen). prereqs: train-test split.
- **Under-learning** — training on too little data, analogous to a student not preparing enough; pick a representative split (popular: 80/20, 90/10, 75/25). prereqs: train-test split.
- **`train_test_split(X, y, train_size, shuffle)`** — sklearn function returning `X_train, X_test, y_train, y_test`. prereqs: sklearn.
- **Shuffling trade-offs** — shuffling is fine for discrete independent observations but *wrong* for time series. prereqs: train-test split.
- **Why time series cannot be shuffled** — timestamps follow a sequence (no future data at train time); shuffling uses future to predict past. prereqs: time series.
- **Correct time-series split** — set `shuffle=False` so train precedes test chronologically. prereqs: train_test_split, time series.
---
## MODULE: Training & Forecasting
### LESSON: Model Training and Forecasting
- **Model fitting/training** — using `train_data` (X_train, y_train) to let the model learn patterns. prereqs: train-test split.
- **`RandomForestClassifier`** — ensemble classification model; chosen as an illustration (usable interchangeably with other classifiers). prereqs: classifier concept.
- **Hyperparameters** — `n_estimators` (trees), `max_features`, `max_depth`, `random_state` (seed for reproducibility). prereqs: random forest.
- **`model.fit(X_train, y_train)`** — trains the model object. prereqs: classifier.
- **`model.predict(X_test)`** — forecasts labels on unseen data, returning `y_pred` (0 = no position, 1 = long). prereqs: fit.
- **Forecast interpretation** — a predicted 1 means a long-position signal at that timestamp. prereqs: predict.
- **Need for evaluation metrics** — motivates the subsequent module on classifier metrics. prereqs: predict.
---
## MODULE: Metrics to Evaluate a Classifier
### LESSON: Metrics to Evaluate a Classifier
- **Accuracy** — total correct predictions / total predictions. prereqs: y_test, y_pred.
- **Confusion matrix** — table of model actions (columns/x-axis) vs expected actions (rows/y-axis). prereqs: none.
- **`confusion_matrix(y_test, y_pred)`** — sklearn function returning the matrix as a numpy array. prereqs: sklearn.
- **True/False Positive/Negative** — TP/FP/TN/FN interpretation for a long/no-position classification. prereqs: confusion matrix.
- **Precision** — correct predictions of a class / total predicted of that class. prereqs: confusion matrix.
- **Recall** — correct predictions of a class / total actual of that class. prereqs: confusion matrix.
- **F1-score** — harmonic mean of precision and recall: `2 * (precision*recall) / (precision + recall)`. prereqs: precision, recall.
- **`classification_report(y_test, y_pred)`** — sklearn returns precision, recall, f1-score, support per class. prereqs: sklearn.
- **Support** — number of actual occurrences of a class in the dataset; used as weight in averages. prereqs: classification report.
- **Macro vs weighted average** — macro = simple average of classes; weighted = weighted by support (handles imbalance). prereqs: classification report.
- **Backtesting motivation** — evaluation metrics inform whether signals are good enough to backtest/trade. prereqs: metrics.
---
## MODULE: Metrics to Evaluate a Regressor
### LESSON: R-Squared
- **R-squared / Coefficient of Determination** — percentage of variance in the dependent variable explained by the independent variable(s). prereqs: linear regression.
- **R-squared formula** — `1 - SSE/SST = 1 - Σ(yi-ŷi)² / Σ(yi-ȳ)²`. prereqs: residuals.
- **R-squared range** — always between 0 and 1; 1 = perfect prediction, 0 = no captured relationship. prereqs: formula.
- **`r2_score(y_true, y_predicted)`** — sklearn function computing R-squared. prereqs: sklearn.
- **Prediction direction** — R² is interpretable across two models (e.g. JPM predicted from BAC ≈ 0.82 vs from Nestle ≈ 0.35). prereqs: r2_score.
- **Limitation of R-squared** — does not detect bias; residual analysis required to spot structured error. prereqs: R-squared.
---
## MODULE: Introduction to Backtesting
### LESSON: Strategy Backtesting
- **Backtesting** — evaluating a strategy's returns and risk on historical data using model-generated signals. prereqs: model predictions.
- **Read signal + price data** — combine a predicted-signals CSV with matching close-price data, sliced to the signal period. prereqs: read_csv.
- **Strategy returns** — position-weighted returns from the signal and close prices. prereqs: returns, signals.
- **Equity curve** — cumulative strategy returns plotted over time, showing portfolio value change. prereqs: cumulative returns.
- **Annualised returns** — average annual return: `(CumReturns^(annual_trading_freq/n_days)) - 1`; here freq = 252*6.5*4 for 15-min data. prereqs: cumulative returns.
- **Annualised volatility** — `sqrt(Var(Returns)) * sqrt(annual_freq)`; the price variation over a year. prereqs: returns.
- **Maximum drawdown** — `(Trough - Peak)/Peak`; maximum portfolio loss from a peak. prereqs: equity curve.
- **Sharpe ratio** — `(Rp - Rf)/σp`, excess return over risk-free rate per unit of volatility; higher preferred. prereqs: returns, volatility.
- **Transaction costs / slippage (noted)** — omitted here for simplicity but acknowledged as a simplification. prereqs: backtesting.
- **Model performance interpretation** — annualised return, volatility, drawdown, and Sharpe quantify how the ML signals would have traded. prereqs: metrics, backtesting.
---
## COURSE-LEVEL PREREQUISITE GRAPH
- Python basics (variables, operators, functions) → DataFrame functionality → importing/visualising financial data.
- Features + target engineering (pct_change, shift, rolling, talib, stationarity/correlation checks) → Train-test split.
- Train-test split + RandomForest `fit`/`predict` → Classifier metrics (accuracy, confusion matrix, precision/recall/f1) → Backtesting (returns, equity curve, annualised return/volatility, max drawdown, Sharpe).
- The course does NOT cover ARIMA/ARCH/seasonality or statistical forecasting; those live in the companion *Financial Time Series Analysis for Trading* course. Websockets, streaming, and live order handling are out of scope (they appear in the Zerodha algo-trading course).
---
## Python-for-Machine-Learning — Section-based course structure (full lesson-by-lesson view)
# — Python for Machine Learning in Finance — Concept Inventory
**Track:** 4 — Machine Learning & Dсов Learning in Trading (Beginners)
**Media note:** PDFs only (no mp4s in folder).
**Overlap with D: notebooks:** partial — the D: side has notebook-based `Python-for-Machine-Learning` extraction covering the same import/EDA/data-visualisation → preprocessing → target/labelling → classifier/regressor → backtesting → performance pipeline. This course mirrors those steps with its own reading PDFs (metrics, backtesting, regression assumptions, summary).
## COURSE
An end-to-end Python roadmap for building a (classification-based) trading strategy: understanding what machine learning is, fetching/visualising financial data, constructing target variables and features, choosing an ML algorithm, training a model, evaluating classifiers and regressors, and finally backtesting + paper/live trading the strategy. Emphasis is on the *pipeline in Python*, not deep algorithm theory (algorithm detail is out of scope by design).
## Course Prerequisite Map
- **Section 1 Introduction:** none (orienting flow diagram).
- **Section 2 ML Overview ⚜ D:** required reading for Sections 4,6,7,10,14 (defines supervised/unsupervised/RL terminology used throughout).
- **Section 4 Financial Data & Visualisation requires:** Python data tools (pandas) + Section 2.
- **Section 6 Target Variable & Features requires:** Sections 2 & 4 (data collection), plus RSI/ADX/stationarity/correlation background (given as "pre-reading").
- **Section 7 ML Algorithms requires:** Section 2.
- **Section 10 Metrics (Classifier) requires:** a trained classifier + Section 2.
- **Section 11 Backtesting requires:** Sections 10 (metrics) & 4 (data); overlap with D: intro-backtesting notebook.
- **Section 14 Regressor Metrics requires:** linear-regression assumptions + Section 7.
- **Section 16 Summary** wraps the course.
---
### Section 1 — Introduction
- **CONCEPT:** Course structure / flow — the end-to-end ML-for-trading pipeline (data → target → algorithm → train → evaluate → backtest → paper/live). prereqs: none (course map).
### Section 2 — Machine Learning Overview
- **CONCEPT:** Machine learning definition & components — algorithms that learn patterns from data; components (hypothesis, loss/objective, optimisation) and relation of ML to deep learning. prereqs: basic statistics/programming.
- **CONCEPT:** Types of ML algorithms — supervised (labels), unsupervised (no labels; clustering), semi-supervised (mixed), reinforcement learning (agent, reward). prereqs: none; used to map which algorithm to apply.
### Section 4 — Financial Market Data and Visualisation
- **CONCEPT:** Retrieving stock/volume/fundamental data in Python — APIs (Yahoo, data providers) and the pandas data model (DataFrame/Series, datetimes, join/merge). prereqs: Python, pandas.
- **CONCEPT:** Data cleaning — handling incomplete/missing values, aligning dates, correct dtypes; essential before constructing features. prereqs: pandas, data retrieval.
- **CONCEPT:** Visualisation — plotting price/returns (matplotlib/seaborn) to inspect distribution and stationarity. prereqs: Section 4 data, plotting basics.
### Section 6 — Target Variable and Features
- **CONCEPT:** Target variable (y) — the value the model predicts; labelling data into categories is the standard way to define the target for a classification-based trading strategy. prereqs: Section 2, Section 4 data.
- **CONCEPT:** Features (X) — engineered inputs to predict the target; a price series can be transformed (returns, RSI, ADX, momentum) into feature columns. prereqs: pandas, data retrieval.
- **CONCEPT:** Stationarity & correlation checks — stationarity (constant mean/var) readiness for regression; correlated features add no new information and mislead. prereqs: statistics/indicators (pre-reading covers RSI, ADX, stationarity, correlation).
### Section 7 — Machine Learning Algorithms
- **CONCEPT:** Choosing an algorithm — no single algorithm dominates; one must know the broad classes (supervised / unsupervised / semi-supervised / RL) and match a regression or classification learner to the target type. prereqs: Section 2, Section 6 target/features.
- **CONCEPT:** Random Forest (illustration used in course) — a bagged ensemble of trees used as the example classifier in this course's implementation. prereqs: Section 2, decision-tree intuition.
### Section 10 — Metrics to Evaluate Classifier
- **CONCEPT:** Classification metrics — the top metrics for a classifier (confusion-matrix-derived: accuracy, precision, recall, F1, ROC/AUC). prereqs: Section 2 + a fitted classifier.
- **CONCEPT:** Metrics for imbalanced classification — choosing the right metric when classes are rare/imbalanced (F1, PR-AUC, cost-aware) — typical for trade-direction labels. prereqs: Section 10 metrics + rare-event awareness.
- **CONCEPT:** Interpreting a classifier's true/false positive vs negatives for a trading signal. prereqs: Section 10.
### Section 11 — Introduction to Backtesting
- **CONCEPT:** Backtesting — running the strategy on historical data to estimate performance; why, platforms, parameters. prereqs: Sections 4 + 10.
- **CONCEPT:** Backtesting biases & pitfalls — common mistakes, survivorship/snooping; divergences between backtest and live results. prereqs: Section 11.
- **CONCEPT:** Trading psychology — why most traders lose; emotional discipline is treated as a requirement for strategy usability. prereqs: none.
### Section 14 — Metrics to Evaluate a Regressor
- **CONCEPT:** Linear-regression assumptions — before interpreting/using OLS predictions you must check (1) linearity of relation, (2) no autocorrelation in residuals, (3) normality, (4) homoscedasticity; violating them ± predictions are unusable. prereqs: regression model, residuals.
- **CONCEPT:** Regressor metrics — because regression accompanies classification in the ML toolbox: MSE, MAE, R² etc. prereqs: Section 7 algorithm + the above assumptions.
### Section 16 — Course Summary
- **CONCEPT:** Course recap / next steps — you should be able to explain ML, list the ML task steps, implement an end-to-end ML task in Python, evaluate a model, backtest, and paper/live trade on Blueshift. Detection of what was out of scope: ML algorithm detail, data/feature engineering, and algorithm deep-dives (deferred to later courses). Resources `.zip` bundled plus blueshift/ABridgePy nexts.
- **CONCEPT:** Blueshift / live trading as the deployment context for the paper/live step. prereqs: full course.