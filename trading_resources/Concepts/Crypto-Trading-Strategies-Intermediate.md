# Crypto Trading Strategies (Intermediate) — Concept Inventory
**Source:** `others\_extracted\CryptoTradingStrategiesIntermediate`
**Output file:** `_concept_lists\Crypto-Trading-Strategies-Intermediate.md`
**Goal:** Teach intermediate crypto strategy construction, backtesting hygiene, trade-level + performance analytics, and realistic cost modelling on crypto (mostly BTC/ETH) data. Eight notebooks spanning data acquisition, three live strategies (divergence, Ichimoku, day-of-week), and analytics/costs.
## Assets & Files
- **Notebooks (8):**
 1. `Getting Cryptocurrency Data\Cryptocurrency Data.ipynb`
 2. `Divergence Strategy\Divergence Strategy.ipynb`
 3. `Ichimoku Cloud\Calculate and Plot the Ichimoku Cloud.ipynb`
 4. `Ichimoku Cloud\Ichimoku Cloud Based Strategy.ipynb`
 5. `Performance Analysis\Performance Metrics.ipynb`
 6. `Performance Analysis\Trade Level Analytics.ipynb`
 7. `Trading Using Calendar Anomalies\The Day of the Week Strategy.ipynb`
 8. `Transaction Cost and Slippage\Transaction Costs and Slippage.ipynb`
- **Data modules:** hourly BTC `btc_feb_2019_feb_2024_hourly_data.csv`; daily BTC `btc_sep_2014_feb_2024.csv`; minute-level BTC `btc_usd_minute_data_*.csv` (3 windows, incl. slippage window); `ETHBTC.csv` (minute ETH/BTC); `BTCUSD.csv`; ether/sol/tether series; precomputed `ichimoku_feb_2019_feb_2024_close_signal.csv` and `trades_ichimoku.csv`.
- **Docs:** `Folder Structure ...html`, `ReadMe.html`.
- `plot_ichimoku_cloud(df)` — computes conversion_line (9p), base_line (26p), leading_span_A (shift 52), leading_span_B (shift 30), lagging_span (close shift −30) and fills/plots the cloud.
- `performance_analysis(df)` — prints cumulative multiple, CAGR, annualised Sharpe (sqrt(365·24), risk-free=0), max drawdown; plots equity curve vs buy-and-hold and the drawdown series.
- `ichimoku_improved_strategy(df)` — reproduces the full Ichimoku entry/exit **+ SMA(5)/SMA(20) drawdown filter** (below) and returns strategy returns.
## Notebook Concepts (grouped by theme)
### 1. Getting Cryptocurrency Data.ipynb
- **`cryptocompare` package** for free crypto data; requires a CryptoCompare **API key** (set via `cryptocompare.cryptocompare._set_api_key_parameter(...)`).
- **Fetch all tickers:** `get_coin_list()` → `pd.DataFrame.from_dict(...).T` lists every coin's metadata (Id, Url, CoinName, Taxonomy, Rating, …).
- **Historical OHLCV at daily / hourly / minute frequencies:**
 - `get_historical_price_day/hour/minute(ticker, currency, limit, exchange, toTs)`.
 - `limit` up to **2000 bars**; **minute data available only for the last ~7 days** (API internal limit).
 - Returned dict → DataFrame, `set_index("time")`, `pd.to_datetime(index, unit='s')`.
- Plot `close` for visualisation; tweak ticker/frequency/exchange (e.g. BTC/USDT on BINANCE before 20-Feb-2024).
### 2. Divergence Strategy.ipynb — RSI divergence via Aroon
- **RSI (Relative Strength Index)** via TA-Lib `ta.RSI(close, timeperiod=14)`.
- **Aroon indicator** via `ta.AROON(High, Low, timeperiod)` → AroonUp / AroonDown (0–100) measure how recent the period's highest high / lowest low occurred → trend direction & strength.
- Apply Aroon to the **price series** and again to the **RSI series itself** (`ta.AROON(RSI, RSI, ...)`); compare how market highs/lows behave vs the RSI's highs/lows (divergence detection).
- **UpSpread = AroonUp(price) − AroonUp(RSI)**; **DownSpread = AroonDown(price) − AroonDown(RSI)** — the momentum-oscillator divergence signal.
- **Threshold trading** (threshold `t = 75`; **higher `t` ⇒ fewer trades**)
 - `UpSpread > t` → buy (+1); `DownSpread > t` → sell (−1). Combined `Signal = Buysignal + Sellsignal`.
- **Signal lifecycle / bar mechanics (no look-ahead):** Candle 1 closes → indicators computed & signal generated; **Candle 2 opens → previous signal enters the trade**; Candle 2 closes → new signal; Candle 3 opens → returns for the Candle-2 position realised, etc. Implementation: `TradeSignal = Signal.shift(1)`.
- **Returns:** open-to-open `Return = (Open.shift(-1) − Open)/Open`; `StrRet = TradeSignal * Return`.
- Cumulative strategy returns plotted (cumsum).
### 3. Ichimoku Cloud — Calculate and Plot.ipynb
- **Ichimoku Kinko Hyo** components & default parameters **(9, 26, 52, 26)** — Conversion Line period, Base Line period, Leading Span period, displacement
 - **Tenkan-sen (Conversion Line):** `(9-period high + 9-period low) / 2` — short-term trend/signal (midpoint of recent range).
 - **Kijun-sen (Base Line):** `(26-period high + 26-period low) / 2` — medium-term trend / equilibrium, support & resistance.
 - **Senkou Span A (Leading Span A):** `(Conversion + Base) / 2`, plotted **shifted forward** (`.shift(52)`) — forward top edge / future support-resistance.
 - **Senkou Span B (Leading Span B):** `(26-period high + 26-period low) / 2`, `.shift(30)` — forward bottom edge.
 - **Chikou Span (Lagging Span):** close price plotted **backwards** (`.shift(-30)`).
 - **The Cloud = the area between Span A and Span B** (filled with `fill_between`); **price above ⇒ up-trend, below ⇒ down-trend, inside ⇒ flat/range**.
- Manual pandas computation: `rolling(max/min)`, `.mean()`, arithmetic, `.shift`, then plot with matplotlib.
### 4. Ichimoku Cloud Based Strategy.ipynb
- **Entry (buy, signal=1)** when all three hold: (1) close **above** the cloud (`close > SpanA & close > SpanB`), (2) **Span A above Span B**, (3) **Conversion (Tenkan) above Base (Kijun)**.
- **Exit (flat, 0)** when mirrors hold: close below cloud, Span A below Span B, Tenkan below Kijun, then `ffill` the signal. Note: **no shorting** — most exchanges disallow shorting crypto, so we just exit the long.
- Uses `plot_ichimoku_cloud` from the utility module.
- **Strategy returns:** `strategy_returns = close.pct_change() * signal.shift(1)` (prev hour's signal × this hour's return).
- **Performance (`performance_analysis`):** cumulative ≈ **13.88×**, CAGR ≈ **71.5%**, Sharpe ≈ **1.38**, MDD ≈ **−55%** (vs buy & hold).
- **Drawdown improvement via technical filter:** SMA(5) vs SMA(20) crossover — when short MA < long MA, force exit (signal → 0). Result: cumulative drops to **13.17×** / CAGR 69.6%, but **MDD improves from −55% to −40%** and **Sharpe rises to 1.54**.
### 5. Performance Metrics.ipynb (within-trade/continuously-varying metrics)
- Precomputed signal + trade files: `ichimoku_..._close_signal.csv`, `trades_ichimoku.csv`.
- **Equity curve:** `cumprod(1 + strategy_returns)`; positive slope = profitable, negative = losing; also visualises drawdowns.
- **CAGR:** `((EV/BV)^(1/n) − 1) × 100` (n in years; hourly data → n = days using 252·24).
- **Histogram of returns:** return distribution (bins).
- **Annualised volatility:** `std × sqrt(252×24)` (≈ 39.42% here).
- **Sharpe ratio:** `(mean return − risk_free) / volatility × sqrt(252·24)`; example 0.72 → "0.72 return per 1.0 of risk".
- **Maximum drawdown:** `(Peak − Trough)/Peak`, i.e. `min((CumRet − cummax)/cummax)`; example ≈ **−69.95%**.
### 6. Trade Level Analytics.ipynb (post-trade metrics)
- **Total PnL:** `sum(Exit Price − Entry Price)` ≈ **$16,661**.
- **Win / Loss %:** fraction of trades with PnL>0 / PnL≤0 (36.8% / 63.2%). *Key nuance:* **a win rate below 50% can still be profitable** if winners are much larger than losers.
- **Average profit per winning / average loss per losing trade** (`np.abs` on losers); want avg win high, avg loss low (e.g. $2,333 vs $1,148).
- **Average trade duration / holding period:** mean of `(Exit Date − Entry Date)` ≈ 7d 17h; too-long → news/surprise risk & capital lock-in, too-short → high transaction costs.
- **Profit factor:** `(Win% × avg win) / (Loss% × avg loss)` ≈ **1.18**; grading table — <1 unprofitable, =1 breakeven, 1.1–1.4 average, 1.4–2.0 decent, ≥2 excellent.
### 7. The Day of the Week Strategy.ipynb — calendar anomalies
- Exploit a **day-of-week anomaly** on Bitcoin (returns on a particular weekday are structurally higher; full-sample day-wise Sharpe peaks on **Monday**).
- Compute daily `pct_change`; **day-wise Sharpe** via `groupby(day)` (mean/std × sqrt(252)).
- **Dynamic rolling selection:** every 2-week window (i % 14 == 0), compute past-60-day day-wise Sharpe, pick the best day (`idxmax`); for the next two weeks, **long that day** (enter at previous day's close, exit at that day's close): signal=1 on that weekday else 0.
- Returns = signal × pct; **CAGR ≈ 9.19%, Sharpe ≈ 0.49, MDD ≈ −52.8%** → motivates stop-loss discussion; lookback (60 days) is tunable.
### 8. Transaction Cost and Slippage.ipynb
- **Brokerage/taxes:** broker fee `0.0001%` + tax `0.01%` of traded value → total **0.0101%** (`0.000101`).
- **Slippage modelling (worst-execution estimator, on 1-minute data):**
 - Take the **last 5 minute-candles per day** (high end-of-day liquidity) via `groupby(date).tail(5)`.
 - Buy slippage = `(High − Close)/Close`; sell = `(Close − Low)/Close`; daily means → take **max** → ≈ **0.09%**.
- **Total charges ≈ transaction cost (0.00001) + slippage + brokerage ≈ 0.1%** per trade (0.001).
- Apply cost **on position changes** (when `signal − signal.shift(1) == 1`, i.e. buys; many exchanges don't charge on sell), shift by 1 to align, subtract from strategy returns; compare cumulative equity with vs without costs.
- Note: use realistic broker/exchange rules.
## Prerequisites (Domain)
- **Python/pandas:** `read_csv`, datetime indexing, `groupby` (+`.tail`), `rolling`, `shift`, `pct_change`, `fillna`, `ffill`, `np.where`.
- **TA-Lib** for RSI / Aroon / SMA; **matplotlib** plotting.
- **Ichimoku Cloud** indicator logic; **momentum/trend** concepts; **calendar-anomaly** awareness; performance metrics (**Sharpe, CAGR, volatility, maximum drawdown, profit factor**); **trade-level analytics** (PnL, win rate, Avg holding, profit factor); **transaction-cost / slippage** realism; basic **backtest hygiene** (no look-ahead: signal applied on next-bar open, `.shift(1)`).