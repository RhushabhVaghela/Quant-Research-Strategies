# 📖 CORE CONCEPTS LIBRARY — Every Foundation the Courses Assume (But Don't Teach)
> **Why this exists:** Every concept file in `_concept_lists/` lists *prerequisite* concepts in shorthand (`prereq: put-call parity`, `prereq: covariance`), but the courses themselves assume you already know them. This library **defines and explains** those foundational concepts so you can understand every course without a separate textbook.
>
> **How to use it:** Each section is a domain. Look up the concept by name before/during studying a course. A concept marked `→ used in:` lists the course files that reference it.
---
## PART 1 — PYTHON & PANDAS PROGRAMMING FOUNDATIONS
> `→ used in:` every course (Python-for-Trading, Backtesting, all ML, all options)
| Concept | What it is |
|---|---|
| **Variable** | A named container holding a value (`price = 150.0`). |
| **Data type** | The kind of value: `int`, `float`, `str`, `bool`. |
| **List** | Ordered, mutable sequence `[1, 2, 3]`; indexable. |
| **Tuple** | Ordered, immutable sequence `(1, 2, 3)`. |
| **Dictionary** | Key→value map `{'open': 150}`; fast lookup by key. |
| **Set** | Unordered collection of unique elements. |
| **Control flow** | `if/elif/else` — branch code on a condition. |
| **Loop** | `for` (iterate sequence) / `while` (repeat while condition). |
| **Function** | Reusable block `def f(x): return x*2`; improves DRY. |
| **Lambda** | Anonymous single-expression function. |
| **Scope** | Which names a function can see (local vs global). |
| **Exception handling** | `try/except/finally` — handle errors gracefully. |
| **Import** | Load a library: `import pandas as pd`. |
| **pip / package install** | Install libraries: `pip install pandas`. |
| **NumPy array** | N-dimensional homogeneous array; vectorized math. |
| **Vectorization** | Operating on whole arrays without Python loops (100× faster). |
| **Broadcasting** | NumPy applies an operation across arrays of compatible shapes. |
| **Pandas Series** | 1D labeled array, like a column. |
| **Pandas DataFrame** | 2D labeled table (rows × columns), like an Excel sheet. |
| **Index** | Row labels (often dates in finance). |
| **`.loc` / `.iloc`** | Label-based / position-based row selection. |
| **Boolean indexing** | Filter rows by a condition: `df[df['Close'] > 100]`. |
| **`.rolling(window)`** | Moving/rolling calculation over a fixed look-back window. |
| **`.shift(n)`** | Shift values down/up by n rows (to avoid look-ahead in signals). |
| **`pct_change()`** | Fractional change between consecutive rows = returns. |
| **`cumprod()`** | Cumulative product — compounds returns into equity curve. |
| **`resample()`** | Change frequency (daily→monthly). |
| **`groupby()`** | Split-apply-combine aggregation by a key. |
| **`merge/concat`** | Combine DataFrames (join on key / stack vertically). |
| **`NaN` / missing values** | Gaps; handle with `dropna()` / `fillna()` |
| **`datetime`** | Date handling; `pd.to_datetime()`, business-day offsets. |
| **`matplotlib` (plt)** | Plotting library: `plt.plot`, `plt.scatter`, `plt.hist`. |
| **JSON / pickle / CSV** | file serialization formats for saving data/models. |
---
## PART 2 — STATISTICS & PROBABILITY
> `→ used in:` Financial Time Series, Statistical Arbitrage, ML, Options, Volatility
| Concept | What it is |
|---|---|
| **Mean (average)** | Sum of values ÷ count; central tendency. |
| **Median** | Middle value when sorted; robust to outliers. |
| **Standard deviation (σ)** | Spread of values around the mean = √variance. |
| **Variance** | Average squared deviation from the mean. |
| **Quantile / percentile** | Value below which a given % of data falls (median = 50th). |
| **Normal distribution** | Bell-shaped distribution; fully described by mean & σ; 68/95/99.7 rule. |
| **Standard normal / z-score** | (value − mean)/σ; N(0,1). |
| **Skewness** | Asymmetry of a distribution (left/right tail). |
| **Kurtosis** | Tailedness — how fat the tails are (fat tails = more extreme events). |
| **Correlation** | Degree two variables move together, range −1 to +1 (Pearson). |
| **Covariance** | Unscaled measure of joint variability; correlation = covariance/(σ_x σ_y). |
| **Regression** | Model Y = a + bX; OLS finds best-fit line by minimizing squared errors. |
| **OLS** | Ordinary Least Squares; the slope of regressing Y on X is the beta. |
| **R²** | Proportion of variance in Y explained by the model. |
| **Residuals** | Y − predicted-Y; the unexplained part. |
| **Histogram** | Bar chart of how often values fall in each bin. |
| **Probability distribution** | Function describing likelihood of each outcome. |
| **Lognormal distribution** | Distribution of a variable whose log is normal; used for stock prices (>0 always). |
| **Hypothesis testing** | Rule for deciding if an effect is statistically significant. |
| **p-value** | Probability of the result under the null hypothesis. |
| **Expected value** | Probability-weighted average of outcomes. |
| **Bootstrap** | Resample data with replacement to estimate uncertainty. |
---
## PART 3 — FINANCIAL MATHEMATICS
> `→ used in:` Backtesting, Financial Time Series, Options, Portfolio, Position Sizing
| Concept | What it is |
|---|---|
| **Simple return (R_t)** | (P_t − P_{t−1})/P_{t−1}; daily change. |
| **Log return (r_t)** | ln(P_t / P_{t−1}); time-additive, symmetric, more normal. |
| **Compounding** | Returns multiply over time: (1+R1)(1+R2)… |
| **Cumulative return** | Total compounded return over a period: Π(1+r) − 1. |
| **Annualization** | Scaling a monthly/daily figure to one year; returns ×12, volatility ×√252 (daily). |
| **Time value of money (TVM)** | Money today is worth more than the same amount later. |
| **Future value (FV)** | PV × (1+r)^n. |
| **Present value (PV)** | FV / (1+r)^n. |
| **Risk-free rate** | Theoretical return of a riskless asset (e.g., T-bill); used in Sharpe & BS. |
| **Arithmetic vs geometric return** | Simple average vs compounded average of returns. |
| **Equity curve** | Cumulative value of a strategy over time. |
| **Sharpe ratio** | (Return − risk-free) / volatility; reward per unit of risk. |
| **Sortino ratio** | Like Sharpe but uses only downside volatility. |
| **Calmar ratio** | Annualized return / max drawdown. |
| **Treynor ratio** | Excess return per unit of beta. |
| **Information ratio** | Active return / tracking error vs a benchmark. |
| **Max drawdown** | Largest peak-to-trough decline of the equity curve. |
| **CAGR** | Compound Annual Growth Rate over a period. |
| **Win rate** | Fraction of winning trades. |
| **Profit factor** | Gross profit / gross loss. |
| **Recovery factor** | Total profit / max drawdown. |
| **Expected PnL** | Probability-weighted net profit of a strategy/trade. |
---
## PART 4 — TIME SERIES & ECONOMETRICS
> `→ used in:` Financial Time Series, Statistical Arbitrage, Crypto Advanced, Unsupervised
| Concept | What it is |
|---|---|
| **Stationarity** | A series whose mean & variance are constant over time (no trend/seasonality). Required for many models. |
| **Unit root / ADF test** | Augmented Dickey-Fuller test for stationarity; low p-value = stationary. |
| **Autocorrelation (ACF)** | Correlation of a series with its own past lags. |
| **Partial autocorrelation (PACF)** | Autocorrelation of lag k after removing intermediate lags. |
| **White noise** | Random series with zero autocorrelation; uncorrelated unpredictable. |
| **AR model** | Autoregressive: Y_t = c + φY_{t−1} + ε — depends on its own past. |
| **MA model** | Moving-average: Y_t depends on past forecast errors ε. |
| **ARIMA(p,d,q)** | AutoRegressive Integrated Moving Average: combines AR, differencing (I), MA; AIC used for order selection. |
| **ARCH / GARCH** | Models for time-varying volatility (variance clustering); GARCH: σ_t² = ω + αε²_{t−1} + βσ²_{t−1}. |
| **Volatility clustering** | Periods of high volatility tend to cluster. |
| **Cointegration** | Two non-stationary series that share a stable long-run relationship; their spread is stationary → pairs trading. |
| **Hedge ratio** | Units of one asset to offset one unit of another in a spread. |
| **Mean reversion** | The tendency of a series/spread to return to its long-run average. |
| **Hurst exponent** | H>0.5 persistent/trending, H<0.5 mean-reverting, H=0.5 random walk. |
| **Correlation matrix** | Table of pairwise correlations among variables. |
| **Signal-to-noise ratio** | Amount of real signal vs random noise. |
| **Kalman filter** | Recursive estimator of an unobserved state from noisy observations. |
---
## PART 5 — OPTIONS THEORY (The Ones the Courses Assume)
> `→ used in:` Options Basic/Intermediate/Advanced, Options Volatility, Systematic Options, ML for Options, Options Sentiment
| Concept | What it is |
|---|---|
| **Call option** | Right (not obligation) to **buy** the underlying at strike before/at expiry. |
| **Put option** | Right (not obligation) to **sell** the underlying at strike before/at expiry. |
| **Strike price (K)** | Fixed price at which the option can be exercised. |
| **Underlying price (S)** | The asset the option is on. |
| **Premium** | Price paid/received for the option. |
| **Expiry / maturity (T)** | Last date the option can be exercised. |
| **Time to expiry ($\tau$ or DTE)** | Days until expiry, often /365 in formulas. |
| **Moneyness** | Position of S vs K: ITM/ATM/OTM. |
| **In-the-money (ITM)** | Call: S>K; Put: S<K. |
| **At-the-money (ATM)** | S ≈ K; strike closest to spot. |
| **Out-of-the-money (OTM)** | Call: S<K; Put: S>K. |
| **Intrinsic value** | Immediate exercise value: max(S−K, 0) call, max(K−S, 0) put. |
| **Time value** | Premium − intrinsic value; decays as expiry nears. |
| **Payoff diagram** | Profit/loss at expiry vs underlying price. |
| **Break-even point** | Spot where profit = 0 (call: K+premium; put: K−premium). |
| **PUT-CALL PARITY** | Relationship linking call & put prices on same underlying/strike/expiry: **C + K·e^(−rT) = P + S**. If violated → arbitrage. Used to derive one price from the other and to check market consistency. |
| **Black-Scholes Model (BSM)** | Closed-form option pricing formula: price = N(d₁)·S − N(d₂)·K·e^(−rT), where d₁ = [ln(S/K)+(r+σ²/2)T]/σ√T, d₂ = d₁−σ√T. Assumes: lognormal S, constant σ & r, no dividends, European options. |
| **Implied volatility (IV)** | The σ that, plugged into BS, reproduces the market price. Market's forecast of future vol. |
| **Historical / realized volatility** | Actual past volatility, computed from log returns (std ×√ann). |
| **Volatility skew** | IV differs across strikes: OTM puts usually demand higher IV (crash protection). |
| **Volatility smile** | U-shaped plot of IV across strikes (OTM on both sides have higher IV). |
| **IV rank / IV percentile** | Current IV relative to its historical range. |
| **Volatility term structure / forward vol** | IV across different expiries; forward vol from near/far contracts. |
| **Greeks — Delta (Δ)** | ∂price/∂S; sensitivity to a $1 underlying move. Call: 0→1; Put: −1→0. |
| **Greeks — Gamma (Γ)** | ∂Δ/∂S; rate of change of delta; curvature. |
| **Greeks — Theta (Θ)** | ∂price/∂time; time decay per day (usually negative for long options). |
| **Greeks — Vega (ν)** | ∂price/∂IV; sensitivity to a 1-point change in volatility. |
| **Greeks — Rho (ρ)** | ∂price/∂r; sensitivity to the risk-free rate (often minor). |
| **Payoff of a spread** | Sum of individual legs' payoffs (long lower-strike call + short higher-strike). |
| **Bull call spread** | Long K1 call + short K2 call (K2>K1); capped bull strategy. |
| **Bear put spread** | Long K2 put + short K1 put (K1<K2); capped bear strategy. |
| **Covered call** | Long stock + short call; neutral-to-dull bullish income. |
| **Protective put** | Long stock + long put; insurance (capped downside). |
| **Straddle** | Long both ATM call + ATM put; profits from big moves either direction. |
| **Strangle** | Long OTM call + OTM put; cheaper than straddle, needs bigger move. |
| **Butterfly spread** | Long 2 outer calls, short 2 inner (at-strike) calls; profits from low vol around strike. |
| **Iron condor** | Short OTM call + short OTM put + protective outer legs; profits from range-bound market. |
| **Calendar (horizontal) spread** | Same strike, different expiries; profits from time decay/term structure. |
| **Dispersion** | Trading index vol vs the weighted vol of constituents (implied correlation). |
| **Delta hedging** | Neutralizing Δ by trading the underlying/futures to offset option delta. |
| **Gamma scalping** | Repeatedly re-hedging a long-gamma position to monetize convexity. |
| **Option pricing via Taylor** | Price ≈ Price₀ + Δ·ΔS + ½Γ·(ΔS)² + ν·ΔIV (greeks as derivatives). |
| **Value at Risk (VaR)** | Max loss at a confidence level over a horizon; historical/Monte-Carlo/parametric methods. |
---
## PART 6 — VOLATILITY & TRADING
> `→ used in:` Volatility Beg, Options Volatility, Volatility Trading, Crypto Inter
| Concept | What it is |
|---|---|
| **Volatility (σ)** | Magnitude of price fluctuation; annualized std of returns. |
| **ATR (Average True Range)** | Indicator = rolling mean of True Range = max(High−Low, |High−prevClose|, |Low−prevClose|). |
| **EWMA volatility** | Exponentially weighted volatility — recent data weighted more. |
| **GARCH volatility forecast** | Model-based forecast of tomorrow's volatility. |
| **Bollinger Bands** | SMA ± k·σ bands; mean-reversion & breakout signals. |
| **VIX** | CBOE's implied-volatility index of S&P 500. |
| **Bettng-Against-Beta (BAB)** | Long low-beta, short high-beta; Frazzini-Pedersen. |
| **Beta (β)** | Stock's sensitivity to the market; slope of regressing stock on index. |
| **CAPM** | E[r] = r_f + β(E[rm]−r_f); links beta to expected return. |
| **Efficient frontier** | Set of optimal portfolios (max return for given risk); MPT. |
| **Risk parity** | Allocating so each asset contributes equal risk. |
| **Position sizing** | Determining number of shares/contracts. |
| **Fixed-fractional sizing** | Risk = capital × risk% / stop-distance. |
| **Kelly criterion** | Optimal bet fraction = edge/odds; maximizes long-run growth. |
| **Volatility targeting** | Sizing inverse to volatility to hit a target portfolio vol. |
| **CPPI** | Constant Proportion Portfolio Insurance; floor + multiplier on risky asset. |
| **Margin / leverage** | Trading with borrowed capital magnifying returns & risk. |
---
## PART 7 — MACHINE LEARNING, DEEP LEARNING & NLP
> `→ used in:` Intro ML, Regression, Classification-SVM, Decision Trees, Unsupervised, Feature Engineering, Neural Networks, Deep RL, NLP, LLM, ML for Options
| Concept | What it is |
|---|---|
| **Features (X)** | Input variables the model learns from. |
| **Target (y)** | The output the model predicts. |
| **Train / test split** | Hold out data to evaluate out-of-sample performance. |
| **Cross-validation** | Repeated train/validate splits (KFold) for robust evaluation. |
| **Overfitting** | Model learns noise/train data, fails on new data. |
| **Underfitting** | Model too simple, misses the pattern. |
| **Bias-variance tradeoff** | Balancing error from simplifying assumptions vs over-sensitivity to data. |
| **Hyperparameter** | Model setting chosen before training (max_depth, learning_rate). |
| **Hyperparameter tuning** | GridSearch/RandomizedSearch to find best hyperparameters. |
| **Classification** | Predicting a category/label (up/down). |
| **Regression** | Predicting a continuous number (price, return). |
| **Logistic regression** | Linear model with sigmoid for binary classification. |
| **SVM (Support Vector Machine)** | Finds max-margin separating hyperplane; can use kernels. |
| **KNN** | Predicts by majority of k nearest neighbors. |
| **Decision tree** | Tree of if-then rules splitting on features (gini for classification). |
| **Random Forest** | Ensemble of many decision trees (bagging). |
| **Bagging** | Train models on random samples, average predictions (reduces variance). |
| **Boosting (AdaBoost, Gradient)** | Train models sequentially, each correcting prior errors (reduces bias). |
| **XGBoost** | Fast, regularized gradient boosting. |
| **Confusion matrix** | TP/FP/TN/FN table for classifier evaluation. |
| **Accuracy** | Correct predictions / total. |
| **Precision** | TP / (TP+FP); of predicted positives, how many right. |
| **Recall / sensitivity** | TP / (TP+FN); of actual positives, how many caught. |
| **F1-score** | Harmonic mean of precision & recall. |
| **ROC / AUC** | Tradeoff of true-positive vs false-positive rate. |
| **Feature scaling (MinMax/Standard)** | Normalize features to comparable ranges. |
| **PCA (Principal Component Analysis)** | Dimensionality reduction; projects data onto directions of max variance. |
| **K-means clustering** | Unsupervised; partitions data into k clusters by centroid distance; WCSS/elbow picks k. |
| **DBSCAN** | Density-based clustering; finds arbitrary shapes; marks outliers as noise. |
| **t-SNE** | Non-linear dimensionality reduction for visualization. |
| **Feature engineering** | Creating informative features from raw data. |
| **Labeling** | Defining the target (fixed-time horizon, triple-barrier). |
| **Fractional differentiation** | Transform preserving memory while making series stationary. |
| **Neural network (MLP)** | Layers of neurons; learns complex nonlinear functions. |
| **Activation function** | ReLU, sigmoid, tanh — introduce nonlinearity. |
| **Loss function** | Measure of prediction error (MSE, cross-entropy). |
| **Optimizer** | Algorithm updating weights (SGD, Adam). |
| **Epoch / batch size** | One pass over data / samples per weight update. |
| **RNN** | Recurrent net — processes sequences with hidden state. |
| **LSTM** | Long Short-Term Memory; gates control long-range memory; for time series. |
| **Gradient descent** | Iteratively reduce loss by moving down the gradient. |
| **Reinforcement learning / DQN** | Agent learns by rewards; DQN uses a deep net to approximate Q-values. |
| **DDQN** | Double DQN; reduces overestimation of Q-values. |
| **Experience replay** | Store past transitions; sample random batch to break correlation. |
| **Reward design** | Designing what the agent is rewarded for (PnL, Sharpe). |
| **Tokenization** | Splitting text into words/subwords. |
| **Stopwords** | Common words removed pre-analysis (the, and). |
| **Bag of words / TF-IDF** | Text as word-frequency vectors; TF-IDF weights by rarity. |
| **Word embeddings** | Dense vector representations of words capturing meaning. |
| **BERT / FinBERT** | Transformer language models; FinBERT fine-tuned for finance sentiment. |
| **Sentiment score** | Numerical polarity of text (positive/negative). |
| **XGBoost on text** | Applying gradient-boosted trees to NLP features. |
---
## PART 8 — TRADING STRATEGY, EXECUTION & RISK
> `→ used in:` Backtesting, all strategy courses, Algo Trading, Event-Driven
| Concept | What it is |
|---|---|
| **Backtesting** | Simulating a strategy on historical data to estimate viability. |
| **Vectorized backtest** | Signal applied to whole series at once (fast, idealized). |
| **Event-driven backtest** | Bar-by-bar simulation of orders (realistic, slower). |
| **Look-ahead bias** | Using future data in a signal (must avoid; use `.shift()`). |
| **Survivorship bias** | Only testing stocks still listed (delisted ones removed). |
| **Out-of-sample** | Data not used in design/training; true test. |
| **Walk-forward analysis** | Rolling train/test windows — the gold standard. |
| **Transaction costs** | Commissions, spread, fees per trade. |
| **Slippage** | Difference between expected & actual fill price. |
| **Market impact** | Large orders move price against you. |
| **Signal** | Rule indicating trade direction (1 long, −1 short, 0 flat). |
| **Position** | Current holding (long/short/flat). |
| **Trade sheet / trade book** | Table of all trades with entry/exit, prices, PnL. |
| **Entry / exit rules** | Conditions for opening and closing a position. |
| **Stop-loss (SL)** | Pre-set exit to cap a loss. |
| **Take-profit (TP)** | Pre-set exit to lock profit. |
| **Trailing stop** | Stop that follows price favorably. |
| **Risk-reward ratio** | Potential profit / potential loss (target ≥ 2:1). |
| **Stop-loss hit / OCO / cover orders** | Order types that auto-exit (broker-dependent). |
| **Order types** | Market, Limit, SL, SL-M(arket), CO(ver), GTT, AMO, Iceberg, bracket. |
| **Margin / leverage** | Borrowed capital amplifying exposure & risk. |
| **Regime detection** | Classifying market into bull/bear/range states. |
| **Relative series** | Stock price / benchmark; isolates stock-specific vs market move. |
| **Calendar / seasonal anomalies** | Recurring date patterns (turn-of-month, payday, FED day, expiry) exploited by event strategies. |
---
*End of Core Concepts Library.* Add to `MASTER_Complete_Concept_Curriculum.md` by running the assembler after including this file, or reference standalone.