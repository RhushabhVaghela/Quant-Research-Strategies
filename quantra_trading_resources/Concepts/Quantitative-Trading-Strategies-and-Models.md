# Quantitative Trading Strategies and Models — Concept Inventory
Course goal: quantitative time-series models (ARIMA for price, GARCH for volatility) plus technical trading strategies (Bollinger Bands, trend-based EMA/SAR/Stochastic, volume reversal) with signals, returns, and performance evaluation.
## Enumerated Notebooks (5) + Data
| # | Module folder | Notebook |
|---|---|---|
| 1 | Econometric Models | Implementation of ARIMA Model |
| 2 | Econometric Models | Implementation of GARCH Model |
| 3 | Technical Trading Strategies | Bollinger Bands Strategy |
| 4 | Technical Trading Strategies | Trend Based Strategy |
| 5 | Technical Trading Strategies | Volume Reversal Strategy |
Shared data: `data_modules/` CSV files (V_2010_2020.csv, Gold_data.csv, aaple_data_18_19.csv). No custom Python module.
---
## 1. Econometric Models / Implementation of ARIMA Model
**Concepts:**
- ARIMA (Autoregressive Integrated Moving Average) models future asset prices from past prices.
- **Stationarity** as a modelling prerequisite: non-stationary series have too many parameters to estimate.
- Testing stationarity: **Augmented Dickey-Fuller (ADF) test** (`statsmodels.tsa.stattools.adfuller`); null = non-stationary; p<0.05 means stationary. Also visual check via **ACF plot**.
- **Differencing** (first order) to stationarize the series; over-differencing detection via ACF going too far negative.
- Residuals should resemble **white noise**; clustered variance implies a modelable signal remains; a density plot with near-zero mean and finite variance confirms stationarity.
- Choosing AR/MA order: **PACF** significant lags → **p** (AR order); **ACF** significant lags → **q** (MA order).
- **Train/test split** before tuning.
- **Information Criterion (IC)** to penalise overfitting/complexity: AIC and BIC; lower is better; BIC penalises parameter additions more.
- **Rolling-window forecast** (updating train set and refitting after each step); `model_fit.forecast()`.
- **Error residuals** (predicted − actual) should look like white noise; density of good residuals ~ normal.
- Evaluate with **Mean Squared Error (MSE)**.
**Prereqs:** time-series basics; autocorrelation concepts; pandas; list-processing.
## 2. Econometric Models / Implementation of GARCH Model
**Concepts:**
- Volatility is unobservable and must be estimated from return fluctuations; **GARCH** forecasts volatility.
- Compute **daily returns** (`pct_change()`), rolling standard deviation (window 14), and **annualised volatility** (× √252).
- **Volatility clustering**: periods of high volatility follow low volatility; driven by market shocks that decay over time.
- Stationarity of returns again checked via ADF test.
- **GARCH hyperparameters**: p (lag returns), q (lag variance), plus distributional assumption for residuals and mean-return assumption (default often neglected).
- **Grid search** over p, q, dist to minimise AIC (commonly yields Normal/t/skew-t with certain p,q).
- **Standardised residuals** = residual / conditional volatility; should resemble white noise and normal density for a usable model.
- Forecast via **rolling window** using `arch_model(...).fit().forecast(horizon=1).variance` then annualise by √(variance)·√252.
- **EWMA** weighting: GARCH variance gives more weight to recent data; forecast is noisier but statistically correct.
- Improve volatility estimates via **EGARCH / GJR-GARCH** for asymmetric shocks (slow rise, sharp dip).
- Evaluate with residuals and MSE.
**Prereqs:** notebook 1 (ADF, rolling window, MSE); volatility definition; return arithmetic.
## 3. Technical Trading Strategies / Bollinger Bands Strategy
**Concepts:**
- Bollinger Bands technical indicator: **upper / middle / lower** bands around the price using a moving average and volatility.
- Choosing the window `n` (e.g., 60 trading days ≈ a quarter) for standard deviation and the Ta-Lib band function `BBANDS(close, timeperiod, *, matype)`.
- Compute daily returns and rolling standard deviation of returns.
- **Signal generation**: market crosses the upper band (breakout/up) vs lower band; require cross-bar classification.
- Strategy returns = previous-day signal × return (`Signal.shift(1) * Ret`).
- **Number of trades** counted via `np.count_nonzero(Signal)`; cumulative strategy returns plotted.
**Prereqs:** technical-indicator vocabulary; pandas `shift`; `.rolling().std()`; numpy.
## 4. Technical Trading Strategies / Trend Based Strategy
**Concepts:**
- Multi-indicator trend strategy: **Exponential Moving Average (EMA)** for trend direction, confirmed by **Parabolic SAR (PSAR)** and **Stochastic Oscillator (STOCH)**.
- Create indicators with the Ta-Lib moving averages (`t.EMA`, `t.SAR`, `t.STOCH`) after tuning timeperiod/acceleration/max step (`n=10`, `acc=0.04`, `max_step=0.2`).
- Build a **signal column** from overlapping indicator conditions (buy=+1, sell=−1, confirm with fast/slow oscillator bands).
- Market return (`Close.pct_change()`); strategy return = `Return * Signal.shift(1)`.
- Plot cumulative returns; then **drawdown** computation via running max and peak-to-trough.
- **Sharpe ratio** = (portfolio − risk-free)/volatility; calculate over annualisation.
**Prereqs:** indicators; `shift()`, `cumprod()`, `maximum.accumulate`; performance ratios.
## 5. Technical Trading Strategies / Volume Reversal Strategy
**Concepts:**
- **Volume reversal** strategy: identify price reversals backed by trading-volume evidence.
- Feature engineering from OHLCV: **5-day price change** via `Close.shift(1) − Close.shift(6)`.
- **100-day standard deviation** of price change (`rolling.window=100.std()`) to gauge volatility.
- **5-day average volume** with `shift`+`rolling.mean`; compare `5d_avg_vol` vs `past 5d_avg_vol` (shifted by 5).
- Generating **buy (1)** and **sell (−1)** signals from absolute price change > std and volume regime.
- **Continuous signals & exits**: iterate to track `c_signal` (position) and `exit` criterion; exit positions on 5th day or counter-trade.
- Market and strategy daily returns; **cumulative** returns across >200 days (post lookback).
- Performance: **Sharpe ratio**-style ratio of cumulative strategy vs market return over strategy std.
**Prereqs:** vectorised pandas; `shift` semantics; cumulative returns; loops over DataFrame rows.
---
## Quantitative-Trading-Strategies-and-Models — Section-based course structure
# Concept Inventory — Quantitative Trading Strategies and Models
## COURSE: Quantitative Trading Strategies and Models
### Section: Section 1 - Introduction to Quantitative Trading
- **Introduction to quantitative trading:** definition of quantitative trading. prereqs: none.
- **Definition of quantitative trading:** systematic, model/statistics-driven strategies. prereqs: none.
### Section: Section 2 - Technical Trading Strategies
- **Introduction to trend and volatility:** trend identification and volatility regimes as basis for strategies. prereqs: none.
- **Volume reversals & Fibonacci retracements:** technical entry signals. prereqs: trend & volatility.
- **Analysing price breakouts with Bollinger Band:** breakout detection using Bollinger Bands. prereqs: Bollinger bands; trend.
### Section: Section 2 PDF — Technical Primer I
- **Trading volume:** confirmation signal. prereqs: technical analysis.
- **Overbought / oversold:** extremes signalling possible reversal. prereqs: technical analysis.
- **Candlestick chart:** price-pattern visualisation. prereqs: technical analysis.
- **Support and resistance levels:** reversal/level references. prereqs: candlestick.
- **Absolute price change:** magnitude of move. prereqs: returns.
- **Fibonacci sequence, ratios, retracement:** golden-ratio levels for retracement zones. prereqs: support & resistance.
### Section: Section 2 PDF — Technical Primer II
- **Exponential Moving Average (EMA):** lag-reduced average. prereqs: moving averages.
- **Parabolic SAR (Stop and Reverse):** trend-following indicator (extreme point, acceleration factor). prereqs: trend.
- **Bollinger bands & breakout:** volatility bands; breakouts as signals. prereqs: EMA; volatility.
- **Keltner channels:** EMA-based bands. prereqs: Bollinger; EMA.
- **Momentum oscillator:** rate-of-change momentum measure. prereqs: technical indicators.
### Section: Section 5 - Econometric Models
- **Time series & autoregressive model:** AR — series regressed on its lags. prereqs: regression.
- **Introduction to heteroskedasticity & autocorrelation:** variance clustering and residual correlation — motivation for volatility/AR models. prereqs: time series.
- **Understanding the ARIMA model:** AR + I + MA for trend forecasting. prereqs: AR; stationarity.
- **Predicting volatility using GARCH model:** volatility forecasting via GARCH. prereqs: ARCH/GARCH; ARIMA.
### Section: Section 5 PDFs — Regression & Residuals
- **Linear regression forecasting equation:** yield line fit on scatter plot (S&P vs Stock ABC). prereqs: scatter; correlation.
- **Errors and residuals in linear regression:** residual = actual − forecast; Standard Error of Estimate (SEE) measures dispersion of actual about the regression line. prereqs: linear regression.
- **ACF and PACF:** autocorrelation (lag-k self-correlation) and partial autocorrelation (lag with intervening lags removed). prereqs: correlation.
### Section: Section 6 - Quantitative Trading Strategies for Options
- **Introduction to options Greeks:** delta, gamma, theta, vega sensitivity measures. prereqs: options basics.
- **Building a delta-neutral portfolio with gamma:** hedging directional exposure while managing curvature (gamma). prereqs: options Greeks.
- **Using gamma scalping to solve negative theta:** monetizing gamma while offsetting adverse long-dated time decay (theta). prereqs: delta-neutral; options Greeks.
### Section: Section 6 PDFs — Options Pricing
- **Introduction to options:** call/put contracts, strike, payoff and P&L of calls and puts. prereqs: none.
- **Moneyness:** in-the-money, at-the-money, out-of-the-money states. prereqs: options intro.
- **Option pricing / Black-Scholes-Merton model:** pricing using underlying price, strike, volatility, time to expiry; assumptions & Python implementation; merits/limitations. prereqs: options; moneyness; volatility.
### Section: Section 8 - Summary
- **Course recap:** technical → econometric → options quantitative strategies review. prereqs: all sections.
## Course Prerequisite Map
- Foundations: *Quantitative Trading Definition → trend/volatility → technical indicators (Primer I/II).*
- Technical strategies: *Primer concepts (volume, Fibonacci, candle, S&R, EMA, Bollinger, Parabolic SAR, Keltner, momentum) → Volume reversal / Bollinger breakout strategies.*
- Econometric models: *Regression + Correlation (→ACF/PACF) + AR → ARIMA; + Heteroskedasticity/volatility → GARCH.*
- Options path: *Options basics (call/put, payoff) → Moneyness → BSM pricing, then → Greeks → Delta-neutral/gamma → Gamma scalping/theta.*
- Course flow: **Intro → Technical Strategies → Econometric Models → Options Strategies → Summary.**
- FunPath basics feeding this course: Python for trading, options fundamentals, linear regression, time series (ARIMA/GARCH), technical indicators.