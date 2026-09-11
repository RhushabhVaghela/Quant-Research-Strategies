# Statistical Arbitrage — Exhaustive Concept Inventory
## MODULE: Statistical Concepts Overview
### LESSON: Cointegration vs. Correlation (`Cointegration vs. Correlation.ipynb`)
- **CONCEPT:** Cointegration — a relationship between two non-stationary price series where their combined spread is stationary, so the series share a common long-run drift and the spread mean-reverts over time. prereqs: none
- **CONCEPT:** Price series — a time-ordered sequence of asset prices (here synthetic, generated series) used to study cointegration and correlation. prereqs: none
- **CONCEPT:** Spread of two series — the difference (or ratio) between two price series; when the spread is stationary and oscillates around a mean line, the pair is said to be cointegrated. prereqs: mean, series difference
- **CONCEPT:** Stationary series — a price series that stays near its mean rather than trending; a stationary spread is the defining property of a cointegrated pair. prereqs: mean, trend, variance
- **CONCEPT:** Correlation — a statistic ranging from −1 to +1 that measures the strength and direction of the linear relationship between two variables; +1 perfect positive, −1 perfect negative, 0 none. prereqs: covariance, scatter
- **CONCEPT:** Cointegration without correlation — two series can be cointegrated (stationary spread) yet have near-zero correlation (e.g. a normal-noise series versus an independent square wave). prereqs: cointegration, correlation
- **CONCEPT:** Correlation without cointegration — two series can be near-perfectly correlated yet their spread widens over time (is non-stationary), so high correlation does NOT imply cointegration. prereqs: cointegration, correlation
- **CONCEPT:** Augmented Dickey-Fuller (ADF) test — a statistical stationarity test applied to the regression residual (spread) to determine whether a pair is cointegrated; the pair is cointegrated if the ADF statistic meets a critical-level (e.g. 10%) threshold. prereqs: hypothesis tests, p-value
- **CONCEPT:** Ordinary Least Squares (OLS) regression — a linear-regression fit used to compute the residual (spread) between two series that is then tested for stationarity. prereqs: linear regression, residuals
- **CONCEPT:** Synthetic series generation — generating artificial price series (normal distribution, square wave, daily trend drift plus noise) to isolate and demonstrate the difference between cointegration and correlation. prereqs: random variable, normal distribution
## MODULE: Pairs Trading Strategy in Python
### LESSON: Pairs Trading Strategy (`Pairs Trading in Python.ipynb`)
- **CONCEPT:** Pairs trading / statistical arbitrage — a market-neutral strategy that trades the price spread between two cointegrated assets, going long one leg and short the other, expecting the spread to revert to its mean. prereqs: cointegration, mean reversion
- **CONCEPT:** Cointegration test as a strategy gate — positions are taken only while the asset pair passes a rolling cointegration test; a cointegration break (CB) closes trades to avoid trading a broken pair. prereqs: cointegration, ADF test, rolling window
- **CONCEPT:** Log-price spread — computing the log of the ratio of two close-price series to linearise percentage changes, so equal relative moves correspond to equal vertical distances and estimation is improved. prereqs: logarithms, price ratios
- **CONCEPT:** Moving average of the spread / standard deviation of the spread — rolling mean and standard deviation of the log-ratio spread computed over a look-back window up to the current day, used to standardise the current spread. prereqs: mean, standard deviation, window
- **CONCEPT:** Z-score — standardised distance of the current spread from its rolling mean: (current_spread − mean) / std, measuring how stretched the spread has become relative to its history. prereqs: mean, standard deviation
- **CONCEPT:** Z-score-based trading signal — SELL the spread when z-score > threshold and SELL when the spread is expected to fall to mean; BUY when z-score < −threshold and the spread is expected to rise; otherwise no position. prereqs: z-score, thresholds
- **CONCEPT:** Threshold parameter — the number of standard deviations (e.g. 1.75) above/below the mean beyond which a buy/sell signal fires; a configurable strategy knob. prereqs: z-score, standard deviation
- **CONCEPT:** Look-back window — a trailing set of days (e.g. 90) used to (1) test cointegration and (2) compute the rolling mean/std of the spread on each trading day. prereqs: rolling statistics
- **CONCEPT:** Mark-to-market (MTM) — the fair value of open positions at current market prices, tracked daily and used to compute unrealised PnL; equals signed price moves times lot sizes. prereqs: market price, position sizing
- **CONCEPT:** Stop loss (SL) — an MTM threshold below which an open trade is closed to limit further loss. prereqs: MTM, risk management
- **CONCEPT:** Take profit (TP) — an MTM threshold above which an open trade is closed to bank profit. prereqs: MTM, PnL
- **CONCEPT:** Cointegration break (CB) — a position-closing status triggered when the pair's cointegration test fails (adftest = No) while a trade is open. prereqs: cointegration test, status flags
- **CONCEPT:** Entry / buy price vs sell price for long and short legs — in a pairs trade, a BUY spread on one leg is offset by a SELL spread on the other; buy/sell reference prices are assigned to the appropriate contract depending on long or short exposure. prereqs: long/short position, pairs
- **CONCEPT:** Lot sizes per leg — contract quantities (e.g. N = 5000, M = 5000) per instrument used to scale raw price differences into position PnL. prereqs: position sizing, MTM
- **CONCEPT:** Cumulative PnL — the running sum of realised PnL as the strategy trades over time, plotted to assess overall profitability. prereqs: PnL, cumsum arithmetic
- **CONCEPT:** Event-driven day-by-day backtest — iterating each trading day (with a 90-day lead-in) to recompute cointegration, z-score, signal, position, MTM, status, and PnL over historical data. prereqs: none
- **CONCEPT:** Strategy performance / profitability check — observing the plotted PnL to conclude a strategy is profitable, then suggesting improvements (multiple indicators, optimised threshold, leverage) to enhance entry-point quality and PnL. prereqs: PnL curve, parameter tuning
---
## Statistical-Arbitrage — Section-based course structure (full lesson-by-lesson view)
# Concept Inventory — Statistical Arbitrage Trading
## COURSE: Statistical Arbitrage Trading
### Section: Section 1 - Definition and Background
- **Introduction of the course:** overview of statistical arbitrage / pairs trading. prereqs: none.
- **Arbitrage strategies in commodities:** relative-value trading applied to commodities. prereqs: none (illustrative).
- **What is statistical arbitrage:** trading one instrument (or basket) against another, capitalising on a statistical relationship reverting to its mean; also called convergence trading / pairs trading. prereqs: none.
- **Types of statistical arbitrage strategies:** directional trading, pairs/triplets/co-integrated portfolios, index arbitrage, long-short portfolios. prereqs: what is stat arb.
### Section: Section 2 - Statistical Concepts in Pairs Trading
- **Mean reversion and Z-Score overview:** prices/spreads revert to a mean; Z-score standardises deviation from mean. prereqs: statistics (mean, std).
- **What is Cointegration:** two non-stationary series whose regression residuals are stationary; Y − βX − β0 stationary ⇒ cointegrated. prereqs: linear regression; stationarity.
- **How to select pairs:** qualitative grouping (sector, market cap, liquidity) → correlation filter → cointegration test. prereqs: cointegration; correlation.
- **ADF test:** Augmented Dickey-Fuller test checks stationarity; more negative t-stat ⇒ stronger rejection of non-stationarity null; critical-value comparison. prereqs: hypothesis testing; stationarity.
### Section: Section 3 - Pairs Trading Strategy in Excel
- **Check for cointegration of pairs:** running ADF on regression residuals to confirm the pair. prereqs: cointegration; ADF test.
- **Generating buy or sell signals [I] & [II]:** enter when spread/Z-score deviates from mean (e.g. >+k short spread, <−k long spread); exit on reversion. prereqs: Z-score; cointegration.
### Section: Section 4 - Pairs Trading Strategy in Python
- **Import libraries and initialise variables:** Python setup for the strategy. prereqs: Python; pairs strategy.
- **Define functions:** encode cointegration check and signal generation. prereqs: pairs strategy.
- **Execute pairs trading strategy:** run the backtest and produce trades. prereqs: defined functions.
### Section: Section 7 - Managing Risks in Stat Arb
- **Risks in statistical arbitrage:** breakdown of cointegration (regime change to trending), model/parameter risk, market shocks. prereqs: cointegration.
- **Identify pairs and stop loss:** filtering 500+ stocks into groups → correlation → cointegration; stop-loss to exit a pair when PnL threshold breached and when to re-enter after mean reversion; or removing the pair from the universe. prereqs: pairs selection; risk management.
- **Loss minimisation via cointegration / minimum profit bounds:** embedding loss protection inside the statistical model. prereqs: pairs strategy; risk.
- **Course summary.** prereqs: all sections.
### Section: Section 9 - Downloadable Resources
- **Downloadable resources:** supporting data/notebook references. prereqs: none.
## Course Prerequisite Map
- Foundations: *What is Stat Arb → Types (pairs, index arb, long-short, directional).*
- Statistics: *Mean/Std → Z-Score; + Regression → Cointegration → ADF test; + Correlation → Pairs selection.*
- Implementation: *Cointegration check → Signal generation (Excel) → Python implementation (imports → functions → execution).*
- Risk: *Cointegration + Risk Management → pair stop-loss and universe prunin; + model robustness.*
- Course flow: **Definition/Background → Statistical Concepts (Z-score, Cointegration, ADF, Pairs Selection) → Excel Strategy → Python Strategy → Risk Management → Resources.**
- FunPath basics feeding this course: Python for trading, linear regression, correlation, stationarity/ADF (from time series), pandas.