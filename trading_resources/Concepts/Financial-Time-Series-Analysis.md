# Financial Time Series Analysis for Trading — Concept Inventory
## COURSE: Financial Time Series Analysis for Trading
A () course on time-series modeling and forecasting for trading. Covers returns (simple, cumulative, log), correlation and covariance, linear/multivariate regression, error metrics, stationarity and the ADF test, volatility, ACF/PACF, AR/MA models, ARIMA model building and selection (via AIC), ARCH and GARCH volatility forecasting, trading-strategy construction from time-series predictions, and a capstone project combining model selection, forecasting, and performance analysis.
Notebooks enumerated (24): `Calculating Returns and Cumulative Returns`, `Log Returns`, `Portfolio Returns Calculations`, `Are Numerical Calculations Exact_` (Anscombe's Quartet), `Implementation of Correlation Coefficient`, `Types of Errors`, `R-Squared`, `Linear Regression Model`, `Multivariate Linear Regression Model`, `ADF Test`, `Calculate Volatility`, `ACF and PACF Plotting in Python`, `Simple AR Model`, `AR Model of Order p`, `Simple MA Model`, `MA Model of order q`, `Getting Started with ARIMA Model`, `ARIMA Model of Order (p, d, q)`, `Best ARIMA Model Selection`, `Implementation of the ARCH Model`, `Implementation of the GARCH Model`, `Trading Strategy using the GARCH Model`, `Working With Pickle File`, `Model Solution_ TSA Capstone Project`.
---
## MODULE: Simple and Cumulative Returns
### LESSON: Calculating Returns and Cumulative Returns
- **One-day return** — `(Today - Yesterday)/Yesterday = Today/Yesterday - 1`. prereqs: none.
- **Total return** — `(Last period price - First period price)/First period price`. prereqs: one-day return.
- **`pct_change()`** — pandas method computing daily returns. prereqs: pandas.
- **`dataframe.column[-1]`** — accesses the last row/first (`[0]`) of a dataframe. prereqs: dataframe.
- **Bar chart of daily returns** — `plot.bar()` with green (positive) / red (negative) via `np.where(condition, if_true, if_false)`. prereqs: matplotlib, numpy.
- **Daily returns are NOT time-additive** — `sum()` of daily returns ≠ total return. prereqs: daily returns.
- **Cumulative returns are multiplicative** — add 1 to each daily return then `prod()` (or `cumprod()`) to match total returns. prereqs: daily returns.
- **`cumsum()` vs `cumprod()`** — cumulative sum vs cumulative product; product is correct for compounding and matters over long backtests. prereqs: cumulative returns.
## MODULE: Log Returns
### LESSON: Log Returns
- **Log price** — natural log of price via `np.log()`; slope differences in log space correctly reflect percentage moves. prereqs: numpy.
- **Log price difference** — `diff()` of log prices; visually equals returns via bar plot. prereqs: log price.
- **Log returns formula** — `log(Today's price / Yesterday's price)`. prereqs: log price.
- **Log returns are time-additive** — sum of daily log returns = total log return `log(last/first)`. prereqs: log returns.
- **`np.exp()` conversion** — exponent of log returns gives normal (arithmetic) returns. prereqs: log returns.
- **Log vs simple returns for small moves** — approximately equal when prices barely move; used in volatility (normal-distribution assumption). prereqs: log returns.
- **`add_subplot()`** — matplotlib method to plot side-by-side graphs (e.g. price vs log price). prereqs: matplotlib.
### LESSON: Portfolio Returns Calculations
- **Asset returns (SPY equity + TLT bond)** — read price data and compute individual total returns. prereqs: total returns.
- **Portfolio weights** — 60% stocks / 40% bonds standard balanced portfolio. prereqs: total returns.
- **Portfolio return** — weighted combination of asset returns (cannot simply add different-weight returns). prereqs: asset returns, weights.
- **Daily portfolio returns** — multiply each asset's daily `pct_change()` by its weight and combine. prereqs: daily returns, weights.
- **Diversification benefit** — bonds may drag returns but add stability per risk appetite. prereqs: portfolio return.
## MODULE: Correlation Analysis
### LESSON: Are Numerical Calculations Exact_ (Anscombe's Quartet)
- **Anscombe's Quartet** — four datasets (Francis Anscombe, 1973) with identical summary statistics but very different plots. prereqs: none.
- **Misleading summary statistics** — same regression line, correlation (~0.82) and R² (~0.67) across datasets hides very different relationships. prereqs: linear regression, correlation.
- **Importance of visualisation** — visualize data before analysis; outliers and non-linearity can distort summary statistics. prereqs: scatter plot.
- **Outlier effect on correlation** — a single outlier can change the fitted line and the correlation coefficient substantially. prereqs: correlation.
### LESSON: Implementation of Correlation Coefficient
- **Correlation** — statistical measure of how two variables move together; measures linear association, not causation. prereqs: none.
- **Correlation formula** — `r = Σ(xi - x̄)(yi - ȳ) / sqrt(Σ(xi-x̄)² Σ(yi-ȳ)²)`. prereqs: none.
- **Correlation range / strength** — |r|>0.7 strong, 0.4–0.7 moderate, <0.4 weak; positive/negative/near-zero sign indicates direction. prereqs: formula.
- **Covariance vs correlation** — covariance is scale-dependent and unbounded (units = product of units); correlation is dimensionless, bounded [-1,1], easier to interpret. prereqs: formula.
- **`Series.corr()`** — pandas method for pairwise correlation of two columns. prereqs: pandas.
- **Correlation heatmap** — `sns.heatmap(data.corr())` from seaborn visualizes pairwise correlation. prereqs: pandas, seaborn.
- **Rolling correlation** — `col1.rolling(window).corr(col2)` shows how correlation varies over time. prereqs: Series.corr.
- **Limitations** — correlation fails to capture non-linear relationships and gives no insight about the future (correlation varies over periods). prereqs: correlation.
## MODULE: Types of Errors
### LESSON: Types of Errors
- **Residual / error** — `εᵢ = yᵢ - ŷᵢ`, the difference between observed and predicted values; explains the lack of an ideal model. prereqs: linear regression.
- **Mean Absolute Error (MAE)** — mean of absolute errors; `Series.abs().mean()` or `sklearn mean_absolute_error`. prereqs: residuals.
- **Mean Squared Error (MSE)** — mean of squared errors; `(error**2).mean()` or `sklearn mean_squared_error`. prereqs: residuals.
- **Root Mean Squared Error (RMSE)** — sqrt of MSE (`math.sqrt(...)` / `sqrt(mean_squared_error)`); grows with distance from actual. prereqs: MSE.
- **Mean Absolute Percentage Error (MAPE)** — mean of absolute percentage errors; always non-negative, scale-independent; no built-in Python function. prereqs: residuals.
- **Error-metric comparison** — residual plots and metric tables (via `tabulate`) show that same-sector predictors (BAC) give lower errors than different-sector ones (Nestle). prereqs: errors, linear regression.
## MODULE: Goodness of Fit
### LESSON: R-Squared
- **R-squared / Coefficient of Determination** — share of variance in the dependent variable explained by the independent variable(s). prereqs: linear regression.
- **R-squared formula** — `1 - Σ(yi-ŷi)² / Σ(yi-ȳ)²`. prereqs: residuals.
- **R-squared range** — between 0 and 1; 1 = perfect prediction, 0 = no relationship. prereqs: formula.
- **`r2_score(y_true, y_predicted)`** — sklearn function computing R²; interpretable across models (e.g. BAC ≈ 0.82 vs Nestle ≈ 0.35 for JPM). prereqs: sklearn.
- **Limitation of R-squared** — cannot detect bias; residual-plot analysis is required. prereqs: residuals.
## MODULE: Linear Regression
### LESSON: Linear Regression Model
- **Linear regression** — modeling a dependent variable (y) from an independent variable (X) with a fitted line. prereqs: scatter plot.
- **Independent vs dependent variable** — BAC price (X, x-coordinate) predicting JPM price (y, y-coordinate). prereqs: linear relationship.
- **`OLS(y, X).fit()`** — statsmodels ordinary-least-squares fit; `add_constant()` for intercept. prereqs: statsmodels.
- **`summary()`** — model summary with coefficient, slope, standard error, t-statistic, p-values, R², F-statistic. prereqs: OLS.
- **F-statistic** — compares model to one with all independent variables zero; high F + low `Prob (f-statistic)` means the model is better than no-predictors. prereqs: OLS.
- **t-statistic / p-value (`P>|t|`)** — coefficient / standard error; low p-value means the coefficient is significant and should be retained. prereqs: OLS summary.
- **`sns.regplot(x, y)`** — seaborn plot of the fitted line through the scatter. prereqs: seaborn, linear regression.
### LESSON: Multivariate Linear Regression Model
- **Multivariate linear regression** — regression with multiple independent variables (BAC and Citigroup) predicting JPM. prereqs: linear regression.
- **Model equation** — `JPM = -18.11 + 1.55*BAC + 1.26*C`. prereqs: multivariate OLS.
- **Adjusted R-squared** — penalizes extra independent variables; guards against redundant predictors inflating R². prereqs: R-squared.
- **Variable significance** — adjusted R² close to R² indicates the added independent variables are meaningful. prereqs: adjusted R-squared.
## MODULE: Stationarity
### LESSON: ADF Test
- **Stationary series** — a time series whose mean, variance, and autocorrelation are constant over time (values independent of when observed); easier to model. prereqs: time series.
- **Non-stationary series** — time series with trend or seasonality (e.g. declining Wheat ETF). prereqs: stationary series.
- **Stationarity check methods** — visual inspection, comparing section statistics, and statistical tests. prereqs: non-stationary series.
- **Augmented Dickey-Fuller (ADF) Test** — H0: series is not stationary; H1: stationary. Reject H0 if p-value ≤ 0.05. prereqs: hypothesis testing.
- **`adfuller(X)`** — statsmodels method returning (test stat, p-value, lags used, n obs, critical values, info criterion). prereqs: statsmodels.
- **Interpreting ADF output** — compare p-value to 0.05 or ADF statistic to critical values to conclude stationarity. prereqs: ADF test.
- **Differencing** — `y't = yt - y(t-1)` converts a non-stationary series into a stationary one (prerequisite to time-series modeling). prereqs: non-stationary series.
## MODULE: Introduction to Volatility
### LESSON: Calculate Volatility
- **Volatility** — statistical dispersion of returns; how much price fluctuates around the mean; directionless. prereqs: returns.
- **Daily volatility** — rolling standard deviation of returns over a lookback (e.g. 14 days). prereqs: returns, standard deviation.
- **Annualised volatility** — daily volatility × sqrt(252); 252 trading days/year; sqrt because variance ∝ time. prereqs: daily volatility.
- **Annual ↔ daily conversion** — divide/multiply by sqrt(252). prereqs: daily volatility.
- **Incorrect way to calculate volatility** — never over raw prices; volatility must be from log returns under the normal-distribution assumption. prereqs: log returns.
- **Importance of volatility** — a risk indicator; higher volatility = riskier asset. prereqs: volatility.
## MODULE: Autocorrelation and Partial Autocorrelation
### LESSON: ACF and PACF Plotting in Python
- **Autocorrelation (ACF)** — complete correlation between a series and its past/lagged values (direct + indirect effects). prereqs: correlation.
- **Partial autocorrelation (PACF)** — correlation of a series with a specific lag controlling for/removing the intervening lags (direct effect only). prereqs: ACF.
- **`plot_acf(data, lags)`** — statsmodels ACF plot; lag 0 ignored; values outside the 95% confidence band (blue region) are statistically significant. prereqs: statsmodels.
- **`plot_pacf(data, lags)`** — statsmodels PACF plot; significant spikes indicate direct lag dependence. prereqs: statsmodels.
- **`pct_change(lookback_period)`** — computed percentage returns for ACF/PACF of the return series. prereqs: pandas.
- **Return-series autocorrelation** — return series are generally random with little/no autocorrelation; PACF may still show lags usable for forecasting. prereqs: ACF/PACF.
- **Use in model selection** — ACF/PACF spikes determine the order of AR/MA/ARIMA terms (later lessons). prereqs: ACF/PACF.
## MODULE: Implement Autoregressive Model
### LESSON: Simple AR Model
- **Autoregressive model AR(1)** — `y_t = c + Φ1*y(t-1)`; output linearly related to its own previous value. prereqs: regression.
- **`ARIMA(data, (p, d, q))`** — statsmodels method; an AR model sets d=0, q=0 → `ARIMA(data, (p, 0, 0))`. prereqs: statsmodels.
- **Fitted AR(1) parameters** — e.g. `y_t = 14.27 + 0.99*y(t-1)`. prereqs: ARIMA.
- **Rolling-window forecasting** — train on a rolling window of past data (e.g. 70%) and predict the next point; predictions are shifted to align with the next timestamp. prereqs: AR model.
- **Residual analysis** — random residuals, sign bias (e.g. mostly negative = higher predictions), and residual autocorrelation via PACF. prereqs: residuals, PACF.
- **Trading strategy from AR predictions** — buy if the predicted price > previous predicted price (or predicted > observed). prereqs: AR forecast.
### LESSON: AR Model of Order p
- **AR(p) model** — autoregressive model with p lagged terms: `y_t = c + Φ1*y(t-1) + ... + Φp*y(t-p)`. prereqs: AR(1).
- **Order selection from PACF** — a significant spike at lag k (e.g. lag 1 and 11) suggests AR order k. prereqs: PACF.
- **Train AR(11)** — `ARIMA(data, (11, 0, 0))`; fitted as `y_t = 13.89 + 1.13*y(t-1) - ... - 0.15*y(t-11)`. prereqs: ARIMA.
- **Overfitting risk** — adding higher orders increases error (low signal-to-noise in markets) and execution time. prereqs: AR(p).
- **Compare AR(1) vs AR(11)** — table of MAE/MSE/RMSE/MAPE, cumulative returns, Sharpe, max DD; both predict poorly here. prereqs: error metrics, strategy performance.
## MODULE: Moving Average Model
### LESSON: Simple MA Model
- **Moving average model MA(1)** — `y_t = μ + ε_t + θ1*ε(t-1)`; output is a linear relationship of current & past error terms. prereqs: regression, errors.
- **MA parameter estimation** — μ and θ can't use standard regression (unknown error terms); found by iteration. prereqs: MA(1).
- **`ARIMA(data, (0, 1, q))`** — an MA model sets p=0, d=1, q=order. prereqs: ARIMA.
- **Fitted MA(1)** — e.g. `y_t = -0.21 + ε_t + 0.04*ε(t-1)`. prereqs: ARIMA.
- **MA rolling-window forecasting** — rolling window prediction via `predict_price_MA()`. prereqs: rolling forecast.
- **Residual analysis** — random residuals, sign bias (e.g. more positive = lower predictions), residual autocorrelation. prereqs: residuals, model_performance.
### LESSON: MA Model of Order q
- **MA(q) model** — `y_t = μ + ε_t + θ1*ε(t-1) + ... + θq*ε(t-q)`; q = order (lag count). prereqs: MA(1).
- **Order selection from ACF** — statistically significant ACF lags (e.g. up to 10) suggest MA order q. prereqs: ACF.
- **Train MA(10)** — `ARIMA(data, (0, 1, 10))`. prereqs: ARIMA.
- **Compare MA(1) vs MA(10)** — higher order raises error metrics but can raise cumulative returns (may be chance). prereqs: error metrics, strategy performance.
## MODULE: ARIMA Model
### LESSON: Getting Started with ARIMA Model
- **ARIMA model (general)** — autoregressive integrated moving average; predicts via lagged observations and error terms. prereqs: AR model, MA model.
- **ARIMA equation** — `y't = C + Σ Φi*y'(t-i) + Σ θj*ε(t-j) + ε_t`. prereqs: AR, MA.
- **ARIMA parameters (p, d, q)** — p = AR order (lag count), d = difference order (`I`, number of differencing passes to achieve stationarity), q = MA order. prereqs: stationarity, AR, MA.
- **`ARIMA(data, (p, d, q))`** — statsmodels constructor. prereqs: statsmodels.
- **Converting to stationary** — ADF test shows non-stationarity; one differencing pass yields d=1. prereqs: ADF test, differencing.
- **When NOT to use ARIMA** — if ACF of the differenced series shows no statistically significant spikes, the data isn't suited. prereqs: ACF.
### LESSON: ARIMA Model of Order (p, d, q)
- **Picking (p, d, q) from ACF/PACF** — PACF spikes → AR order (e.g. p=2); ACF spikes → MA order (e.g. q=2); higher orders overfit. prereqs: ACF, PACF.
- **Resampling to a lower frequency** — `data.resample(freq, label='right', closed='right').agg(ohlcv_dict)` (open first, high max, low min, close last, volume sum). prereqs: pandas resample.
- **Train ARIMA(2,1,2)** — fit on stationary differenced series. prereqs: ARIMA.
- **Forecast** — predict the differenced time series. prereqs: ARIMA fit.
- **Residual diagnostics** (model_performance) — small random residuals; autocorrelation in residuals if a lag falls outside the band. prereqs: model_performance.
- **ARIMA trading strategy** — buy/sell from predictions, then `analyse_strategy`. prereqs: strategy performance.
### LESSON: Best ARIMA Model Selection
- **Model selection via AIC** — Akaike Information Criterion; the model with the lowest AIC across (p, d, q) combos is the best fit. prereqs: ARIMA.
- **Rolling-window (sliding) selection** — re-select and re-fit the best ARIMA model on each rolling window of recent data. prereqs: rolling forecast.
- **Signal generation** — buy when predicted price > close, vice versa. prereqs: ARIMA forecast.
- **Strategy performance analysis** — apply `analyse_strategy`. prereqs: strategy performance.
- **Overfitting warning** — using a larger range of p/q may overfit. prereqs: ARIMA selection.
## MODULE: ARCH
### LESSON: Implementation of the ARCH Model
- **ARCH model equation** — `σ²(t+1) = α0 + α1 * r_t²`; predicts volatility from squared current returns. prereqs: volatility, returns.
- **ARCH purpose** — predicts volatility (conditional variance). prereqs: volatility.
- **Sliding-window fit** — fit ARCH constantly/coefficients each day on the latest fixed number of periods. prereqs: ARCH.
- **`arch_model(data, vol='ARCH', p=order, dist='skewt')`** — ARCH package function; skewed Student-t (`skewt`) is empirical for financial data. prereqs: arch package.
- **Annualised historical volatility** — rolling daily volatility (e.g. 14-day) then annualised; lookback choice affects results. prereqs: volatility.
- **Order p from PACF of squared returns** — optimal lag order. prereqs: PACF.
- **Analysing volatility forecasts** — compare ARCH-predicted volatility against historical volatility in normal vs adverse scenarios. prereqs: ARCH forecast, historical volatility.
## MODULE: GARCH
### LESSON: Implementation of the GARCH Model
- **GARCH model equation** — `σ²(t+1) = α0 + α1*r_t² + β1*σ_t²`; generalises ARCH by adding lagged-variance (conditional regression) term. prereqs: ARCH.
- **`arch_model(data, vol='GARCH', p=AR_order, q=MA_order, dist='skewt')`** — GARCH(p,q); p AR-order, q MA-order (from PACF of squared returns). prereqs: arch package.
- **Compare ARCH vs GARCH forecasts** — overlay predicted-volatility series. prereqs: ARCH, GARCH.
### LESSON: Trading Strategy using the GARCH Model
- **Volatility prediction vs historical volatility** — trade on the sign of the gap between GARCH-predicted and current historical volatility. prereqs: GARCH, historical volatility.
- **Signal rule (VXX ETN)** — buy VXX if GARCH-predicted volatility > historical volatility; sell when < . prereqs: GARCH forecast.
- **Strategy analysis** — via `analyse_strategy`; large drawdowns noted because VXX tracks volatile VIX futures. prereqs: strategy performance.
---
## MODULE: Capstone Project
### LESSON: Working With Pickle File
- **Pickle files (.bz2)** — Python serialisation format; retains column datatypes & DatetimeIndex on re-import. prereqs: pandas.
- **`to_pickle("filename.bz2")`** — saves a dataframe in bz2-compressed pickle. prereqs: pandas.
- **`read_pickle("filename.bz2")`** — loads the pickle preserving prior transformations. prereqs: pandas.
- **Pickle version compatibility** — pickle is Python/pandas-version-specific (backward compatible); errors like `AttributeError: Can't get attribute '_unpickle_block'` or `ValueError: unsupported pickle protocol`. prereqs: pickle.
### LESSON: Model Solution — TSA Capstone Project
- **Capstone workflow** — read minute-frequency price data (FX pairs) → resample to 4-hour bars → sanity-check → select model → forecast → trade → analyse. prereqs: all prior modules.
- **Resampling minute data to OHLCV** — 24-hr FX gives 6 four-hour points/day. prereqs: resampling.
- **Data sanity checks** — check for missing values (NaN) and outliers. prereqs: pandas.
- **Model selection logic** — stationary → ARMA; non-stationary but differenced-stationary → ARIMA. prereqs: ADF test.
- **Best-fit selection by AIC** — compare models across p, q, d. prereqs: AIC, ARIMA.
- **Sliding-window model selection & prediction** — wrap selection+prediction in a function for rolling application. prereqs: rolling forecast.
- **Trading rule** — buy asset if predicted price > current price. prereqs: ARIMA forecast.
- **Performance analysis via pyfolio** — analyse strategy results. prereqs: strategy performance.
---
## COURSE-LEVEL PREREQUISITE GRAPH
- Returns (simple → cumulative → log) → volatility (log-return std dev), stationarity (needs returns), correlation.
- Correlation & visualisation → linear regression → multivariate regression → error metrics (MAE/MSE/RMSE/MAPE) and R².
- Stationarity (ADF, differencing) → ACF/PACF → AR models → MA models → ARIMA(p,d,q) → ARIMA selection by AIC.
- Volatility (returns, log returns) → ARCH → GARCH → GARCH trading strategy.
- Everything feeds the capstone: resample → sanity → ADF → ARIMA/AIC → forecast → strategy → pyfolio.
- Prerequisites aliased into the ML course: this course does NOT assume machine learning; ML classification/backtesting (train-test split, classifier metrics, equity-curve/Sharpe) is covered in the companion *Python for Machine Learning* course.
---
## Financial-Time-Series-Analysis — Section-based course structure (full lesson-by-lesson view)
# Concept Inventory — Financial Time Series Analysis for Trading
## COURSE: Financial Time Series Analysis for Trading
### Section: Section 1 - Introduction
- **Course introduction / structure:** roadmap from returns, regression and correlation (Part I) → AR/MA/ARMA/ARIMA/SARIMA (Part II) → volatility/ARCH/GARCH (Part III). prereqs: none.
### Section: Section 2 - Introduction to Time Series
- **Introduction to time series:** ordered sequence of observations over time. prereqs: none.
- **Why time series analysis is required:** forecasting, trend/seasonality detection, volatility prediction. prereqs: time series.
- **When time series analysis is not required:** when the variable is stable/irrelevant to forecast. prereqs: time series.
### Section: Section 3 - Simple and Cumulative Returns
- **Introduction to returns:** simple return = (P_t − P_{t−1})/P_{t−1}. prereqs: none.
- **Cumulative returns:** compounded product of (1+r) over a period. prereqs: simple returns.
### Section: Section 4 - Log Returns
- **Log prices:** natural log of price series. prereqs: returns.
- **Log returns:** ln(P_t/P_{t−1}); properties/advantages (closer to normal, time-additive) and when not to use. prereqs: returns; log prices.
### Section: Section 5 - Components of Time Series
- **Components of time series:** trend, seasonality, cyclical, residual/noise. prereqs: time series.
- **Trending time series:** long-run upward/downward drift. prereqs: components.
- **Seasonal time series:** repeated fixed-interval patterns. prereqs: components.
- **Mean reverting time series:** reverts to a long-run mean. prereqs: components.
- **Cyclical time series:** multi-year/economic cycles. prereqs: components.
### Section: Section 6 - Linear Regression
- **Linear regression fundamentals:** modelling y = mx + c on a single predictor. prereqs: none.
### Section: Section 7 - Types of Errors
- **Types of error calculations:** measuring forecast errors (MAE, MSE, RMSE, etc.). prereqs: linear regression.
### Section: Section 8 - Goodness of Fit
- **Introduction to goodness of fit:** how well the model fits data (R², residual analysis). prereqs: linear regression; errors.
- **Assumptions for linear regression:** linearity, no autocorrelation, normality, homoscedasticity. prereqs: linear regression; goodness of fit.
### Section: Section 9 - Multivariate Linear Regression
- **Multivariate linear regression:** more than one independent variable. prereqs: linear regression.
- **Limitations and advantages of linear regression:** simplicity vs strict assumptions. prereqs: linear regression.
- **Interpreting OLS summary statistics.** prereqs: multivariate regression.
### Section: Section 10 - Correlation Analysis
- **Correlation and covariance:** measuring how two variables move together. prereqs: statistics.
- **Calculation of covariance & correlation:** population/sample covariance formulas, correlation = scaled covariance. prereqs: correlation.
### Section: Section 11 - Autocorrelation and Partial Autocorrelation
- **What is autocorrelation (ACF):** correlation of a series with its own lags. prereqs: correlation.
- **What is partial autocorrelation (PACF):** correlation of a series with a lag removing the effect of intervening lags. prereqs: autocorrelation.
- **ACF/PACF confidence intervals:** significance cutoffs for detecting autocorrelation. prereqs: autocorrelation.
### Section: Section 12 - Noise
- **Noise:** random, unpredictable component; white noise model (zero mean, constant variance, independent). prereqs: components of time series.
- **White noise vs random walk:** relation between the models. prereqs: noise.
### Section: Section 13 - Autoregressive Model
- **Overview of Part II:** forecasting models intro (AR, MA, ARMA). prereqs: Part I (regression, correlation).
- **Autoregressive model I & II:** AR(p) — regresses series on its own lagged values. prereqs: autocorrelation; linear regression.
### Section: Section 14 - Implement Autoregressive Model
- **Autoregressive processes:** definition; stationary vs non-stationary processes. prereqs: AR model.
- **Dynamic vs static AR models:** re-estimating orders/coefficients (DAR) vs constant (SAR); DAR outperforms slightly. prereqs: AR model.
### Section: Section 15 - Moving Average Model
- **Moving average model:** MA(q) — regresses on past forecast errors (innovation). prereqs: errors; AR model.
- **ACF to detect MA(q):** autocorrelation function used to determine appropriateness of an MA(q) model. prereqs: MA model; autocorrelation.
### Section: Section 16 - ARMA
- **ARMA model (AR+MA):** combination of AR and MA terms. prereqs: AR model; MA model.
- **Caveats of AR, MA and ARMA:** all require stationarity; a trending series must be made stationary first. prereqs: ARMA; stationarity concept.
### Section: Section 17 - Stationarity
- **Stationarity:** constant mean, variance, autocorrelation over time. prereqs: time series.
- **Detecting stationarity:** visual checks, ACF plots, Dickey-Fuller test, KPSS test. prereqs: stationarity concept.
### Section: Section 18 - ARIMA Model
- **ARIMA (Autoregressive Integrated Moving Average):** adds differencing (I, order d) to ARMA. prereqs: ARMA; stationarity.
- **Equation of ARIMA:** components AR (φ terms) + I (differencing) + MA (θ terms); ARIMA(p,d,q). prereqs: ARMA.
- **AIC and BIC:** information criteria for model selection balancing fit vs complexity. prereqs: ARIMA; model selection.
### Section: Section 21 - SARIMA Model
- **SARIMA (Seasonal ARIMA):** ARIMA extended with seasonal components — captures trend + seasonality. prereqs: ARIMA; seasonality.
### Section: Section 22 - Introduction to Volatility
- **Fundamentals of volatility:** dispersion of returns; measured by std dev / variance. prereqs: returns.
- **Importance of volatility:** risk, option pricing, position sizing. prereqs: volatility.
### Section: Section 23 - Stylised Facts and Importance of Volatility
- **Stylised facts of volatility:** volatility clustering, fat tails, leverage effect. prereqs: volatility.
- **Applications of volatility:** risk models, derivatives pricing, forex management. prereqs: stylised facts.
### Section: Section 24 - ARCH
- **Need for ARCH/GARCH:** volatility clustering requires time-varying conditional variance; ordinal models fail. prereqs: stylised facts.
- **Introduction to the ARCH model:** Autoregressive Conditional Heteroskedasticity — variance varies with time conditioned on past. prereqs: needs for ARCH.
- **Equation of the ARCH model:** conditional variance. prereqs: derivation.
- **Derivation of ARCH:** log returns → conditional variance → returns series = mean + variance component. prereqs: volatility; log returns.
- **Performance analysis of ARCH.** prereqs: ARCH.
### Section: Section 25 - GARCH
- **Implementation of the GARCH model:** Generalised ARCH adds past variance terms (volatility clustering persistence). prereqs: ARCH.
- **Performance analysis of GARCH / comparison vs ARCH.** prereqs: GARCH.
### Section: Section 26 - Capstone Project
- **Capstone — build an advanced time series model:** resample data, sanity check (missing/outliers), select ARMA/ARIMA/SARIMA, trade on predicted price, pyfolio performance analysis. prereqs: all prior sections.
### Section: Section 27 - Limitations
- **Limitations of time series analysis:** data gaps, changed behaviour, assuming linearity/trend. prereqs: time series models.
### Section: Section 28 - Future Enhancements
- **Future enhancements:** exponential smoothing, Kalman filter, SARIMAX, EGARCH, rolling GARCH as extensions. prereqs: GARCH; ARIMA.
### Section: Section 29 - Automate Trading Strategy Using IBridgePy
- **Automated trading via IBridgePy:** live/benefit backtesting & trading on Interactive Brokers, TD Ameritrade, Robinhood. prereqs: strategy implementation.
### Section: Section 31 - Course Summary
- **Course summary:** recap of returns → regression → correlation → ARIMA family → volatility/ARCH/GARCH. prereqs: all sections.
## Course Prerequisite Map
- Part I mechanics: *Returns → Cumulative/Log Returns; → Components of Time Series.*
- Regression path: *Linear Regression → Errors → Goodness of Fit → Multivariate Regression.* Correlation path: *Covariance → Correlation → ACF/PACF.*
- Part II models: *ACF/PACF + Regression → AR & MA → ARMA → Stationarity → ARIMA → SARIMA.* (Each model needs the earlier one; stationarity is a hard prerequisite for AR/MA/ARMA/ARIMA.)
- Part III: *Returns + Volatility → Stylised Facts → Need → ARCH → GARCH.*
- Capstone needs all: model selection (ARIMA/SARIMA/GARCH) + performance analysis.
- Enhancements build on ARIMA & GARCH.
- Course flow: **Intro → Returns/Log Returns → Components → Linear Regression/Errors/Goodness/Correlation → AR/MA/ARMA → Stationarity → ARIMA → SARIMA → Volatility → ARCH → GARCH → Capstone → Limitations → Enhancements → Automation → Summary.**
- FunPath basics feeding this course: Python for trading, pandas resampling, statistics (mean, variance, std), regression intuition.