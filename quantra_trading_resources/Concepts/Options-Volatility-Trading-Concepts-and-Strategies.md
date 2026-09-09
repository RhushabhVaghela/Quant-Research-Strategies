# Options & Volatility Trading: Concepts and Strategies — Concept Inventory
## Notebooks & Modules Enumerated
**Notebooks (12 unique):**
| Module | Notebook |
|---|---|
| Sourcing Options Data | `Options Data Storing.ipynb` |
| Close-to-Close Estimator | `Close-to-Close Estimator of Volatility.ipynb` |
| Parkinson Estimator | `Parkinson Estimator of Volatility.ipynb` |
| Garman-Klass Estimator | `Garman-Klass Estimator of Volatility.ipynb` |
| Volatility Estimators | `Comparing Volatility Estimators.ipynb` |
| PnL Distribution of Options Strategies | `Geometric Brownian Motion.ipynb` |
| Monte Carlo Simulation | `Monte Carlo Simulator with GBM.ipynb`, `Monte Carlo Simulator for Long Strangles.ipynb`, `PL Distributions of Multiple Strategies.ipynb` |
| Options Valuation | `Analysis of the Options' Intrinsic and Extrinsic Values.ipynb` |
| How to Trade Variance Premium | `Backtest Short Straddle Strategy.ipynb`, `Backtest Short Straddle Strategy with VIX.ipynb` |
| Volatility Forecasting | `GARCH Parameters Estimation and Volatility Forecast.ipynb`, `Trading with GARCH Forecast.ipynb`, `Backtest and Trade Level Analytics of GARCH Forecast.ipynb` |
| Capstone Project | `Capstone Project Model Solution.ipynb` (also `Capstone Project Solution Template.ipynb`) |
**Python modules:** `data_modules/options_volatility_utils.py`, `data_modules/capstone_options_volatility_utils.py`, `Paper and Live Trading/GARCH.py`
---
## Sourcing Options Data
### `Options Data Storing.ipynb`
- Options data arrives as a zip containing comma-separated `.txt` files, one file per expiry month.
- **Prerequisite: implied vol** — raw options data carries strike, last-traded price, and option deltas that feed later IV (implied volatility) computation.
- `py7zr.SevenZipFile(...).extractall()` decompresses `.7z` archives in a loop over `os.listdir()`.
- Each `.txt` file is read with `pd.read_csv(file, sep=',')`, necessary columns retained into a per-month `monthly_data` frame, appended to a master `options_data` frame, then extracted files deleted with `os.remove()`.
- Notebook contains **raw cells** that do NOT run in the browser — must be downloaded and converted to Code cells manually (local-run only).
## Volatility: Close-to-Close Estimator
### V2 `Close-to-Close Estimator of Volatility.ipynb`
- **Concept: close-to-close volatility estimator.** A simple estimator using only close prices of an asset; starting block for choosing an optimal estimator.
- **Prereq: parkinson, garman-klass** — this is the baseline estimator the later Parkinson and Garman-Klass estimators are compared against.
- Computes daily log returns: `r_i = ln(S_i / S_{i-1})` using `np.log(close/close.shift(1))`.
- Volatility = rolling standard deviation of log returns over window N=20, scaled ×100: `spy['log_returns'].rolling(window=20).std()*100`.
- Window choice (N=20): "neither too low (noisy) nor too high (less relevant)".
- **Annualization**: multiply daily vol by sqrt(252) (assumed trading days/year).
- Extends to **overnight returns** (uses open-close gap) and **intra-day returns** — the estimator omits intra-day range (coverage gap that Parkinson/Garman-Klass address).
## Volatility Estimators: Parkinson
### V3 V3 `Parkinson Estimator of Volatility.ipynb`
- **Concept: parkinson volatility estimator.** Uses high & low prices (two data points/day) instead of close-only (one point/day) → uses twice the data of close-to-close.
- Formula: `σ_park = sqrt( (1/(4·N·ln2)) · Σ ln(High/Low)² )`, window N=20, ×100 for percent.
- Log range term `ln(High/Low)` computed with `np.log(spy['high']/spy['low'])`.
- **Known bias:** Parkinson estimator is biased **low** — evidenced by lower volatility values than close-to-close in comparison.
- **Annualised:** multiply daily by sqrt(252).
## Volatility Estimators: Garman-Klass
### V4 `Garman-Klass Estimator of Volatility.ipynb`
- **Concept:** garman-klass estimator. Combines closing prices AND intra-day high/low extremes to address shortcomings of both close-to-close and parkinson estimators.
- **Prereq:** parkinson & close-to-close — GK requires understanding of what each omits.
- Formula: `σ_GK = sqrt( (1/(2N))·Σ ln(High/Low)² − (1/N)·(2 ln2 − 1)·Σ ln(Close_t/Close_{t−1})² )`.
- Uses daily `high`, `low`, `close`; two log components (`high_low`, `curr_prev`).
- 20-observation rolling window; ×100 to percent; annualise ×sqrt(252).
- March 2020 COVID spike visible in the volatility series.
## Volatility Estimators: Comparison
### V5 `Comparing Volatility Estimators.ipynb`
- **Concept:** compare close-to-close, Parkinson, and Garman-Klass estimators on SPY (large-cap) and IWM (Russell 2000) data.
- Computes annualized vol for each estimator, plots them, compares distributions (skewness, kurtosis), produces summary statistics.
- **Compute the IWM–SPY volatility spread** (cross-variable spread between two index vol series).
- **Prereq application:** used to assess which estimator best feeds downstream strategies (variance premium, IV/forecast vol comparison).
- Uses `scipy.stats` for distribution stats; `tabulate` for tables.
---
## PnL Modelling: Geometric Brownian
### V6 `Geometric Brownian Motion.ipynb`
- **Concept:** geometric brownian motion (GBM) — the stochastic process model for stock price paths underlying Monte Carlo.
- **Prereq:** monte carlo (simulation is built on GBM paths).
- Terminal stock price formula: `S_T = S_0 · exp((r − 0.5σ²)t + σ·sqrt(t)·N(0,1))`, where r = risk-free rate, σ = price volatility, N(0,1) = standard normal draw.
- Steps: compute terminal price, then generate a full stock path over T by repeated draws (dt = T/N).
- Random draws from `np.random.normal(0,1)`, reproducibility via `np.random.seed(0)`.
## Monte Carlo Simulation
### V7 `Monte Carlo Simulator with GBM.ipynb`
- **Concept:** monte carlo simulation — model/analyze complex financial scenarios with multiple uncertain variables.
- **Prereq:** garman-klass? No — prereq is GBM (Geometric Brownian Motion) path generation.
- Simulates multiple stock paths using GBM but with **dynamic (random) risk-free rate r and volatility σ** sampled per simulation (e.g. r uniform in [0.01,0.1], σ uniform in [0.1,0.3]).
- Loops `num_simulations` paths, appends each to `stock_paths`; uses `random.uniform` for r and σ.
### V8 `Monte Carlo Simulator for Long Strangles.ipynb`
- **Concept:** Monte Carlo simulation of P/L distribution for **long strangle** options strategies under varying market conditions.
- **Prereq:** long strangle structure, BSM pricing, GBM terminal price.
- Pipeline: calculate terminal stock price (GBM) → compute long strangle payoff (long call + long put) → run N Monte Carlo simulations → summary statistics of P/L distribution (mean, std, skew, kurtosis).
- Uses `long_strangle()` and `terminal_stock_price()` from `options_volatility_utils`.
### V9 `PL Distributions of Multiple Strategies.ipynb`
- **Concept:** strategy selection under variance premium: when beginning-of-month implied vol > forecast vol, compare P/L distributions of multiple short-delta strangles and short straddle; select the best strategy.
- **Prereqs:** implied vol (IV at month start), forecasted volatility, delta hedging (strangle deltas), monte carlo.
- Reads `spx_eom_expiry_options_2015_2022_ov.bz2` (pine-encoded EOM-expiry options ew).
- Simulates terminal prices of the underlying expiring in one month, generates P/L distributions per strategy (10Δ short strangle, short straddle), plots and compares via summary statistics (mean, std, skew, kurtosis) to decide best.
- Imports `terminal_stock_price` from the utils module.
---
## Options Valuation (BSM Intrinsic/Extrinsic Analysis)
### V10 `Analysis of the Options' Intrinsic and Extrinsic Values.ipynb`
- **Concept:** solve the Black-Scholes-Merton (BSM) equation in Python; decompose option value into **intrinsic value** (payoff / time-variance) and **extrinsic value** (time value / volatility value).
- **Prereq:** BSM formula, d1/d2 probabilities.
- Computes lognormal returns and rolling std (window 60) annualized by sqrt(252) for historical underlying vol.
- Computes **d1 and d2** probabilities that the call expires in-the-money, then plots intrinsic (payoff) and extrinsic (BSM) values vs underlying price.
## Trading the Variance Premium — Short Straddle Backtest
### V13 `Backtest Short Straddle Strategy.ipynb`
- **Concept:** harvest the **variance premium** (implied vol > forecast vol) via a short straddle strategy.
- **Prereq:** implied vs forecast vol, straddle payoff, monte carlo simulation result.
- Open short straddle every Friday (next working day if Friday holiday), rebalance weekly.
- **Delta-hedging-adjacent risk mgmt:** stop-loss (SL) 30% and take-profit (TP) 60% of net entry premium; TP gives a 1:2 risk-to-reward ratio; SL too close → hit too frequently, too far → never hit.
- At-the-money strike selection: pick strike closest to underlying close price (strike in multiples of 25).
- Imports `trade_level_analytics()` from `options_volatility_utils` for performance analytics.
### V14 `Backtest Short Straddle Strategy with VIX.ipynb`
- **Concept:** adds a **VIX index filter**/signal on top of the short straddle strategy.
- **Prereq:** VIX, moving average, implied vol comparisons.
- Compute 5-day moving average of VIX; generate buy signal if `VIX_mv_avg > VIX` (mean-reversion of the VIX-lagged vs current), merged into `options_data` on QUOTE_DATE.
- Enter short straddle when filter conditions met; backtest & trade-level analytics.
## Volatility Forecasting — GARCH
### V15 `GARCH Parameters Estimation and Volatility Forecast.ipynb`
- **Concept:** estimate GARCH(1,1) parameters and forecastic forecast the next month's volatility of S&P 500.
- Pipeline: estimate Parkinson vol (monthly) → estimate GARCH(1,1) params by maximizing log-likelihood → forecast next-month vol with GARCH(1,1).
- **Prereq:** parkinson estimator output, log-likelihood optimization.
- Resample daily OHLCV to monthly (first/max/min/last via `agg` dictionary).
- GARCH(1,1) equation: `σ²_t = γ·V + α·r²_{t−1} + β·σ²_{t−1}` where V = long-term variance (Parkinson vol), γ/α/β weights.
- Log-likelihood function `garch_likelihood`; maximize by minimizing negative log-likelihood via `scipy.optimize.minimize` (methods: TNC/SLSQP/Powell/BFGS/Nelder-Mead); parameter bounds (0,1) for each of [γ,α,β].
- **Pitfall:** TNC minimize can produce NaN parameter estimates (convergence failure) — switch to SLSQP/Powell.
- Forecast uses the estimated γ,α,β in the GARCH(1,1) equation to predict next-month vol.
### V16 V7 `Trading with GARCH Forecast.ipynb`
- **Concept:** build a straddle trading strategy and generate signals from GARCH volatility forecasts.
- **Prereq:** GARCH forecast, implied volatility (C_IV/P_IV), straddle payoff.
- Merges options data (`options_daily_sp500_2018_2022.csv`) with underlying S&P500 OHLCV data.
- Signal generation (per trading day over last year of data)
 1) select 4y rolling daily options data, 2) resample to monthly, 3) Parkinson vol estimate, 4) estimate GARCH(1,1) params, 5) forecast next-month vol,
 6) if forecast vol > ATM call & put implied vol → **buy** straddle; if forecast vol < ATM implied vol → **sell** straddle,
 7) close the position after a week, 8) re-estimate rolling 4y & repeat.
- Signal encoding: `signal=1` long straddle, `-1` short straddle.
### V17 V8 `Backtest and Trade Level Analytics of GARCH Forecast.ipynb`
- **Concept:** backtest & trade-level analytics on the signals generated from GARCH forecasts.
- **Prereq:** GARCH forecast, round-trip/backtest mechanics, position P/L.
- Loop over dates; set up straddle when signal = 1 or −1; exit when signal=0.
- Backtest functions: `add_to_mtm` (daily mark-to-market), `get_premium` (both straddle legs CE+PE), `setup_straddle`, tracks `round_trips_details`, `trades`, `mark_to_market`.
- Runs trade-level analytics (import `trade_level_analytics` from module).
## Capstone Project
### V18 `Capstone Project Model Solution.ipynb`
- **Concept:** synthesizes the full course: variance premium + volatility forecast + straddle backtesting.
- **Prereqs:** monte carlo, garman-klass, parkinson, garch-forecast, implied vol, straddle strategies.
- Builds rolling 4-year GARCH signal generator: *Step-1* select 4y daily options data before selected date, *Step-2* resample to monthly (OHLC dict), *Step-3* Parkinson vol, *Step-4* estimate GARCH(1,1) params, *Step-5* forecast next-month vol, *Step-6* signal (buy straddle if forecast vol > ATM C_IV/P_IV, sell if lower), *Step-7* exit after a week, *Step-8* re-estimate on rolling 4y window & repeat.
- Imports GARCH likelihood/forecast + `trade_level_analytics` from capstone utils; backtests & analytics.
---
## Python Modules
### `options_volatility_utils.py`
- `terminal_stock_price(S0, r, sigma, t, N)` — GBM terminal stock price.
- `long_strangle(So, r, sigma, t)` — long strangle: BSM call+put pricing (d1/d2), terminal price, BSM value, and payoff.
- `garch_likelihood(parameters, returns, parkinson)` — GARCH(1,1) negative log-likelihood.
- `forecast_volatility(parameters, returns, parkinson)` — next-period vol forecast.
- `trade_level_analytics(round_trips, lot_size)` — per-trade P&L / trade-level metrics.
### `capstone_options_volatility_utils.py`
- Same GARCH/likelihood forecasting + `trade_level_analytics` functions for the capstone.
### `Paper and Live Trading/GARCH.py`
- Live-trading (paper) port of GARCH signal: uses NSE NIFTY50 index & options contracts via a trading context API (`superSymbol`, `order`, `schedule_function`).
- GARCH(1) likelihood/forecast adapted to context state; `rebalance` scheduled weekly after market open; stop/exit via `close_out`.
---
**Concept graph of key terms:** close-to-close → Parkinson → Garman-Klass → vol spread; GBM → Monte Carlo → P/L distributions; IV-vs-forecast (variance premium) → short straddle/short strangles → GARCH forecast → live trading strategy; BSM intrinsic/extrinsic value.