# Crypto Trading Strategies (Advanced) — Concept Inventory
**Source:** `others\_extracted\CryptoTradingStrategiesAdvancedResources`
**Output file:** `_concept_lists\Crypto-Trading-Strategies-Advanced.md`
**Goal:** Advanced crypto strategies built on market-efficiency diagnostics (**Hurst exponent**), a systematic **cross-sectional momentum** framework, **statistical arbitrage (pairs trading)**, and unsupervised ML (**K-Means clustering**), plus slippage modelling and look-ahead control.
## Assets & Files
- **Notebooks (4):**
 1. `Hurst Exponent\Crypto Trading Using Hurst Exponent.ipynb`
 2. `Code the Long-Only Momentum Strategy\Long-Only Momentum Strategy.ipynb`
 3. `Code the Pairs Trading Strategy\Pairs Trading Strategy.ipynb`
 4. `Machine Learning in Cryptocurrency Trading\Clustering Strategy for Cryptocurrencies.ipynb`
- **Data modules (`data_modules\`):**
 - `1min_ETHUSDT.csv` — 1-minute ETH/USDT (used by Hurst + Clustering notebooks).
 - `cryptos_price.csv` — 10-coin daily close prices (BTC, XRP, EOS, XLM, LTC, ETH, XMR, DASH, NEO, ETC).
 - `Poloniex_BTCUSD.csv`, `Poloniex_XMRUSD.csv` — daily BTC/USD and XMR/USD for pairs trading.
- **Docs:** `Folder Structure ...html`, `ReadMe.html`.
- **Modules:** no standalone `.py`; logic lives in the notebooks (small `!pip install hurst` in notebook 1).
## Notebook Concepts
### 1. Crypto Trading Using Hurst Exponent.ipynb — Hurst + RSI regime strategy
- **Hurst exponent** via the **`hurst` library** (`from hurst import compute_Hc; compute_Hc(series, kind='price')[0]`). Characterises a time series' regime
 - **H ≈ 0.5** → **random walk** (no exploitable trend, momentum/mean-reversion both fail).
 - **H > 0.5** → **persistent / trending** market → momentum/trend-following strategies work.
 - **H < 0.5** → **anti-persistent / mean-reverting** market → mean-reversion strategies work.
- **Interpretation caveat:** H > 1 has no real theoretical meaning — usually indicates a **non-stationary input** (trend or seasonality) or **unsuccessful detrending** → reconsider/relook at the data series. (Stochastic trends, detrending concepts.)
- **Rolling Hurst** with a **240-minute (4-hour) lookback** (compute in a loop; ≈5–10 min for 100k points — drop to 1000 rows for speed).
- **Thresholds to avoid noise:** H > **0.65** ⇒ persistent (Signal +1); H < **0.35** ⇒ anti-persistent (Signal −1).
- **RSI** (TA-Lib, `timeperiod=14`) gauges overbought/oversold (computed on shifted close to avoid look-ahead).
- **Combined long/short rules:**
 - **Buy (long, +Return)** when: (RSI > 75 AND persist=+1) or (RSI < 25 AND persist=−1).
 - **Sell (short, −Return)** when: (RSI > 75 AND persist=−1) or (RSI < 25 AND persist=+1).
 - i.e. trade **with** the persistence direction in extreme RSI zones (contrarian flip when persistence opposes the RSI reading).
- **Returns & slippage:** returns from close `pct_change`; **average bid-ask spread 0.05** (from orderbook observations); total slippage = `nTrades × 0.05 / mean(Close)`.
- **Net profit after slippage ≈ +108%** on the test window.
### 2. Code the Long-Only Momentum Strategy.ipynb — systematic cross-sectional momentum
- **Quant-strategy framework** (alpha-strategy building blocks)
 1. **Universe selection** — static list of **10 coins** (BTC, XRP, EOS, XLM, LTC, ETH, XMR, DASH, NEO, ETC); selection criteria: **market cap + daily volume**.
 2. **Alpha generation** — per-asset scoring signals (each then **ranked daily across the universe** with `DataFrame.rank(axis=1)`)
 - **2-day returns** (`pct_change().rolling(2).sum()`) — rank **ascending** (higher returns → higher rank; momentum persists).
 - **7-day standard deviation** (`rolling(7).std()`) — rank **descending** (less volatile coins preferred).
 - **14-day RSI** (TA-Lib via `df.apply(calc_rsi, axis=0)`) — rank **ascending** (trend persistence).
 3. **Portfolio construction** — sum the per-parameter ranks into a **combined score**, re-rank, **go long the top 5** (equal weight); `signal_generator` maps `rank < 6 → 0`, `rank >= 6 → 1`; **number of positions varies (3–6)** due to ranking ties (acknowledged).
- **Alternative to simple rank-sum:** weighted average of the alpha ranks, weighted by each alpha's **historic predictive power** (e.g. over the past 100 days).
- **Rebalancing:** repeat alpha + portfolio construction **daily**.
- **Look-ahead control:** `signal.shift(1)` before multiplying by `df_pct` (momentum of day t drives position returned on t+1).
- **Portfolio returns:** equal-weighted mean by number of open positions: `daily_ret = strategy_returns.sum(axis=1)/signal.sum(axis=1)`; annualised **Sharpe ≈ 1.77** (excess over 5%/252 risk-free).
- **Extension note:** long-short (short the bottom 50%) is expected to be **more stable** than long-only, if the exchange allows shorting.
### 3. Code the Pairs Trading Strategy.ipynb — statistical arbitrage
- **Pairs trading (market-neutral stat-arb):** long one asset / short a related asset, betting the **spread converges to its mean** (BTC/USD vs XMR/USD).
- **Hedge ratio via OLS regression** `y = βX + ε` (`statsmodels.api.sm.OLS(df.BTC.iloc[:90], df.XMR.iloc[:90]).fit()`) → ratio ≈ **51.6**; scatter plot of the pair.
- **Spread = BTC − hedge_ratio × XMR** (a linear combination designed to be stationary).
- **Cointegration check with the ADF test** (`statsmodels.tsa.stattools.adfuller` on the first 90 days of spread): test statistic vs 1%/5%/10% critical values → **cointegrated at 90% confidence** (Sep 2017 – Oct 2018).
- **Bollinger bands on the spread:** 20-period MA (middle) ± **0.5 std** (upper/lower), i.e. `rolling(20).mean()` ± `0.5*rolling(20).std()`.
- **Signals:**
 - Spread **below lower band** → **buy the spread** (+1); exit when it returns to the **middle band**.
 - Spread **above upper band** → **short the spread** (−1); exit at the middle band.
 - Positions forward-filled (`ffill`) and combined: `position = long_position + short_position`.
- **Returns:** scale XMR by hedge ratio; `daily_returns = daily_returns_BTC − daily_returns_XMR(hedged)`; `strategy_returns = position.shift(1) × daily_returns`; cumulative plot.
### 4. Clustering Strategy for Cryptocurrencies.ipynb — K-Means + SMA regime filter
- **ML clustering for regime detection:** K-Means (`sklearn.cluster.KMeans(2)`) groups 1-minute bars by **|price movement|** (`abs(pct_change)` of shifted close).
 - Train on the **first 75%** of data (reshape single column with `np.reshape(..., (-1, 1))`), **predict on all**; the two cluster centres → **Cluster 0 = low-volatility** data (preferred to trade), **Cluster 1 = high-volatility**.
- **SMA(30):** `Close.shift(1).rolling(30).mean()` — shift avoids look-ahead.
- **Signals (trade only in the low-vol cluster, Cluster==0):**
 - `SMA < prior Close` → **long (+1)**; `SMA > prior Close` → **short (−1)**.
- **Returns & slippage:** returns = `Signal × Return`; slippage `abs(Signal) × 0.05 / Close` per trade subtracted; test on the **last 25%** (expanding cumulative sum).
- **Result: unprofitable (≈ −481%)** — learning point: a **single-factor clustering entry is insufficient**; entry points must be **optimized using the Hurst exponent** (cross-links to notebook 1 in this course).
## Prerequisites (Domain)
- **Python/data:** pandas (`pct_change`, `rolling().sum/std/mean`, `rank(axis=1)`, `shift`, `groupby`), numpy, matplotlib; **TA-Lib** (RSI, SMA); `pip install hurst`.
- **statsmodels** (OLS regression, `adfuller` ADF stationarity/cointegration test); **sklearn** (K-Means clustering).
- **Hurst exponent** interpretation (persistent vs anti-persistent vs random walk; trend vs mean-reversion regimes); **time-series stationarity & detrending** concepts.
- **Bollinger bands**; **momentum / trend-following** frameworks; **pairs trading** (long-short, spread, hedge ratio, cointegration); **unsupervised ML / K-Means**; **slippage modelling** and **look-ahead-avoidance** (shift 1).