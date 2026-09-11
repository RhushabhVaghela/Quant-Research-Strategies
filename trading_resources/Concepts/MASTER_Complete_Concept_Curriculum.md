# 📚 COMPLETE CONCEPT CURRICULUM (ALL COURSES)

> The full learning library — every course concept and its prerequisites, organized for study.
>
> **📖 START HERE: `CORE_CONCEPTS_LIBRARY.md`** defines every foundational concept the courses assume but do not teach (put-call parity, Black-Scholes, greeks, covariance, stationarity, ADF, cointegration, train-test, metrics, etc.).
> **🗺️ STUDY PLAN: `STUDY_ORDER_ROADMAP.md`** — the ordered Beginner→Master learning path.

**Total courses: 41**

---

## 📑 Course Index

| # | Course | Section view included |
|---|--------|----------------------|
| 1 | Advanced-Options-Volatility-Strategies-and-Risk-Management | yes |
| 2 | Algo-Trading-Zerodha | yes |
| 3 | Backtesting-Trading-Strategies | yes |
| 4 | Candlestick-Patterns | yes |
| 5 | Crypto-Trading-Strategies-Advanced | yes |
| 6 | Crypto-Trading-Strategies-Intermediate | yes |
| 7 | Data-and-Feature-Engineering-for-Trading | yes |
| 8 | Decision-Trees-in-Trading | yes |
| 9 | Deep-Reinforcement-Learning-in-Trading | yes |
| 10 | Event-Driven-Strategies | yes |
| 11 | Financial-Time-Series-Analysis | yes |
| 12 | Forex-Trading-with-Python-Basics | yes |
| 13 | Futures-Trading-Concepts-Strategies | yes |
| 14 | Getting-Market-Data-Stocks-Crypto-News | yes |
| 15 | Getting-Started-with-Algorithmic-Trading | yes |
| 16 | Introduction-to-Machine-Learning-for-Trading | yes |
| 17 | Machine-Learning-for-Options-Trading | yes |
| 18 | Natural-Language-Processing-in-Trading | yes |
| 19 | Neural-Networks-in-Trading | yes |
| 20 | Options-Trading-Strategies-Advanced | yes |
| 21 | Options-Trading-Strategies-Basic | yes |
| 22 | Options-Trading-Strategies-Intermediate | yes |
| 23 | Options-Volatility-Trading-Concepts-and-Strategies | yes |
| 24 | Position-Sizing | yes |
| 25 | Price-Action-Trading-Strategies | yes |
| 26 | Python-for-Machine-Learning | yes |
| 27 | Python-for-Trading-Basic | yes |
| 28 | Quantitative-Portfolio-Management | yes |
| 29 | Quantitative-Trading-Strategies-and-Models | yes |
| 30 | Short-Selling-in-Trading | yes |
| 31 | Statistical-Arbitrage | yes |
| 32 | Swing-Trading-Strategies | yes |
| 33 | Systematic-Options-Trading | yes |
| 34 | Technical-Indicators-Strategies-Using-Python | yes |
| 35 | Trading-Using-LLM | yes |
| 36 | Trading-Using-Options-Sentiment-Indicators | yes |
| 37 | Trading-with-ML-Classification-and-SVM | yes |
| 38 | Trading-with-Machine-Learning-Regression | yes |
| 39 | Unsupervised-Learning-in-Trading | yes |
| 40 | Value-Strategy-in-Forex | yes |
| 41 | Volatility-Trading-Beginners | yes |

---



====================
Advanced-Options-Volatility-Strategies-and-Risk-Management
====================

# Advanced Options & Volatility Trading: Strategies and Risk Management — Concept Inventory
## Notebooks & Modules Enumerated
**Notebooks (23 unique, under `Advanced Options Volatility Trading_ Strategies and Risk Management/`):**
| Module | Notebook |
|---|---|
| Sourcing Data | `Options Data Storing.ipynb`, `Other Assets Data.ipynb`, `Pre-Processing Data.ipynb`, `Working With Pickle File.ipynb` |
| Options Pricing | `IV Calculation.ipynb` |
| Volatility Skew | `Plotting IV Surface.ipynb` |
| Calculation of Volatility Skew | `Calculating Volatility Skew.ipynb` |
| Trading Volatility Skew | `Trading Volatility Skew.ipynb` |
| Delta Neutral Skew Analysis | `Trading Volatility Skew - Delta based Approach.ipynb` |
| IV Rank | `IV Rank Calculation.ipynb` |
| Skew Rank | `Skew Rank Calculation.ipynb` |
| IV Rank in Trading | `IV Rank Based Short Straddle Strategy.ipynb` |
| Skew Rank in Trading | `Short Straddle Strategy - IV Rank and Skew Rank.ipynb` |
| Implementation of Delta Hedging | `Delta Hedging.ipynb` |
| Managing Risk of a Volatility Position | `Dollar-Based Risk Management.ipynb` |
| Trading Based on a Relative View | `Calendar Spread Strategy.ipynb` |
| Volatility Around Events | `Trade Volatility Around Events.ipynb` |
| Trading Strategy on VIXY Using VIX | `VIX - Mean Reversion Strategy.ipynb` |
| Forecasting IV Using Machine Learning / LSTM_s Role in Forecasting IV | `Forecasting IV Using LSTM - Features and Target Variable.ipynb`, `Forecasting IV Using LSTM - Predictions.ipynb`, `Short Straddle-Forecasted IV.ipynb` |
| Capstone Project on Strangle | `Capstone Project Model Solution.ipynb` |
| Capstone Project on Risk Management | `Risk Management Capstone Solution.ipynb` |
**Python modules:** `data_modules/adv_options_volatility_utils.py`, `adv_opt_vol_strangle_capstone_utils.py`, `capstone_risk_management_utils.py`
---
## Sourcing Data
### `Options Data Storing.ipynb`, `Other Assets Data.ipynb`
- Extract raw options data from compressed archives; store/append per-month OHLCV & options fixture data.
- **Prereq:** raw market-data retrieval (Yahoo Finance / exchange APIs); pandas.DataFrame append/stack assembly into a master table (date, strike, last price, delta, IV).
### `Pre-Processing Data.ipynb`
- Preprocess options data: datetime index parsing, resampling/aggregation (OHLC first/max/min/last), cleaning, joining underlying price series.
- **Prereq:** implied vol concepts for cleaning IV columns; pandas merge/join.
### `Working With Pickle File.ipynb`
- Read/write pickle/bz2-encoded options datasets (`pd.read_pickle`, `to_pickle`); bz2 compression.
---
## Options Pricing — Implied Volatility (IV)
### `IV Calculation.ipynb`
- **Concept:** implied vol — the volatility in the underlying expected by market participants, recovered from option market prices.
- **Prereq:** Black-Scholes pricing (mibian library), option Greeks, moneyness.
- Uses `mibian.BS(...).impliedVolatility` over (close of underlying, strike, interest rate from U.S. Treasury yield curve, days-till-expiry, call/put price) for SPX EOM options (`spx_eom_expiry_options_18Dec2023.csv`).
- Interest rate ~2% (U.S. Treasury yield curve rates), single illustration date.
## Volatility Surface & Skew
### `Plotting IV Surface.ipynb`
- **Concept:** IV surface — market expectation of future volatility across strike prices & expiry.
- **Prereq:** implied vol, OTM strikes, volatility skew.
- Reads `spx_eom_expiry_options_2015_2023.bz2`; drops to strike/IV columns; computes ATM strike (SPX strikes in multiples of 5), selects OTM option IVs (call side / put side) for a given date, plots a 3D IV surface across strike & DTE.
### `Calculating Volatility Skew.ipynb`
- **Concept:** volatility skew — difference between implied volatilities of OTM puts and OTM calls at the same distance from ATM.
- **Prereq:** implied vol, IV surface, ATM strike selection, delta.
- `calculate_skew` function: 1) determine ATM strike (nearest multiple of 5 to underlying last), 2) select equidistant OTM call & put strikes, 3) skew = (OTM Put IV − OTM Call IV) / ATM IV.
- Produces a daily skew series (fixed strike percentage basis).
## Volatility Skew Trading
### `Trading Volatility Skew.ipynb`
- **Concept:** volatility-skew-based trading strategy exploiting skew extremes (fixed-strike-percentage skew).
- **Prereq:** volatility skew, IV skew series, entry/exit signal generation.
- Reads `IV_Skew_fixed_strike_percentage_2015_2023.csv`; generates entry/exit signals; computes strategy returns & performance analysis (round trips, profit factor).
### `Trading Volatility Skew - Delta based Approach.ipynb`
- **Concept:** delta-neutral skew — a dynamic approach to measure skew based on option **Delta** values rather than fixed strike distance (delta-based approach).
- **Prereq:** delta hedging (option delta), volatility skew, moneyness, delta-neutral positions.
- Calculates skew from Delta values (dynamic skewing), compares to fixed-strike strategy performance; creates delta-based skew trading strategy; backtests & analysis.
## IV Rank and Skew Rank
### `IV Rank Calculation.ipynb`
- **Concept:** IV rank — where current IV stands relative to recent trading history: `IV_Rank = (Current IV − Min IV)/(Max IV − Min IV)`.
- **Prereq:** implied vol, ATM strike selection, rolling windows.
- Focuses on ATM strikes (most liquid, reflect market sentiment). Rolling 252-day min/max IV; express rank ×100. Saves `IV_Rank_spx_*.csv`.
### `Skew Rank Calculation.ipynb`
- **Concept:** skew rank — current IV skew relative to its historical distribution: `Skew_Rank = (Current Skew − Min Skew)/(Max Skew − Min Skew)`.
- **Prereq:** volatility skew (delta neutral skew), rolling windows.
- Reads delta-neutral skew CSV (`IV_Skew_2015_2023.csv`, from delta-based notebook); rolling 252-day min/max; saves `IV_Skew_Rank_spx_*.csv`.
## Ranking-Based Trading
### `IV Rank Based Short Straddle Strategy.ipynb`
- **Concept:** short straddle deployed when **high IV rank** indicates rich volatility (variance-harvesting).
- **Prereq:** IV rank, short straddle, ATM strike, entry/exit condition, backtesting.
- Read options + IV rank; drop unnecessary columns; join IV rank; entry if rank above threshold; exit conditions; backtest + trade-level analytics (`trade_level_analytics`).
### `Short Straddle Strategy - IV Rank and Skew Rank.ipynb`
- **Concept:** combine **IV rank for entry** (high IV rank ⇒ short straddle) and **skew rank for exit** (exit when IV rank falls OR skew rank extreme ⇒ higher probability directional move).
- **Prereq:** IV rank, skew rank, delta, straddle premium (get_delta/get_premium), short straddle.
- Entry high IV rank; exit when IV rank below threshold or skew rank extreme; backtest + analytics; uses `setup_straddle`, `get_delta`, `get_premium`, `add_to_mtm`.
---
## Implementation of Delta Hedging
### `Delta Hedging.ipynb`
- **Concept:** delta hedging of a volatility position (short straddle) — delta-trading & hedge of positional P/L against underlying moves; analysis of PnL sensitivity to delta threshold values.
- **Prereq:** delta hedging, option Greek of strikes & straddle, IV/skew rank filters.
- Reads options + IV rank + skew rank; compute ATM strike; entry condition; exit conditions; backtest; **sensitivity analysis** of PnL vs delta thresholds (`sensitivity_analysis` from module).
## Managing Risk of a Volatility Position
### `Dollar-Based Risk Management.ipynb`
- **Concept:** dollar-based stop-loss (SL) and take-profit (TP) applied to a short straddle (manage losses/rewards in dollar terms rather than only premium %).
- **Prereq:** risk management, dollar risk-derived thresholds, squeeze-n-leverage.
- Reads `spx_eom_expiry_options_2015_2023.bz2` + IV rank + skew rank; drop non-needed columns; rename; entry/exit; backtest; trade-level analytics (dollar-based SL/TP on round-trip PnL).
---
## Relative View & Event-Driven Trading
### `Calendar Spread Strategy.ipynb` (Relative view on volatility)
- **Concept:** long **calendar spread** (buy far-term IV, sell near-term / vertical calendar) to capture the volatility spike before FOMC events.
- **Prereq:** calendar spread structure, FOMC event calendar, ATM strike, volatility crush risk.
- Parameters `days_to_enter_before_fomc=14`, `days_to_exit_before_fomc=1` — enter ~2 weeks before FOMC, exit before the meeting to avoid the post-event volatility crush.
- Pipeline: read options, ATM strike, FOMC dates (`FOMC_meeting_dates_2019_2023.csv`), unique expiries, near-term vs far-term expiries (closest_expiry), merge options+FOMC, generate signal, backtest + trade-level analytics.
- ⚠️ Notebook won't run on portal — download in `Relative View on Volatility` folder (local only).
### `Trade Volatility Around Events.ipynb` (`Volatility Around Events`)
- **Concept:** long straddle strategy to capture volatility rise before FOMC (8 scheduled meetings/yr), exiting before meeting to avoid crush.
- **Prereq:** FOMC event calendar, long straddle, ATM strike, volatility mean-reversion around announcements.
- Parameters `days_to_enter_before_fomc=14`, `days_to_exit_before_fomc=1`; read options, calculate ATM, FOMC dates, nearest expiries, merge, signal, backtest, trade-level analytics/trade analysis.
- ⚠️ Local-run only (folder `Volatility Around Events`).
## Trading Strategy on VIXY Using VIX — Mean Reversion
### `VIX - Mean Reversion Strategy.ipynb`
- **Concept:** VIX is mean-reverting; construct a mean-reversion *trading* strategy on VIXY (volume index / VIX direction ETF) using the VIX level against its moving average.
- **Prereq:** mean reversion, technical indicators (talib), signal generation, strategy performance evaluation.
- Reads `vix_data_2014_2024.csv` + `vixy_data_2014_2024.csv`; computes indicator (e.g. moving average / VIX ratio), generates buy/sell signals; performance analysis.
---
## Forecasting IV Using LSTM
### `Forecasting IV Using Machine Learning — Features and Target Variable.ipynb` (`LSTM_s Role in Forecasting IV/...`)
- **Concept:** forecast implied volatility with an LSTM; engineer features & target for a regressive time-series forecasting task.
- **Prereq:** implied vol, LSTM, feature engineering, technical indicators.
- Reads SPX options + S&P500 data; filters to retained IV columns; computes indicators (MACD, RSI, NATR, OBV, ADX) as features; builds `X_final` features + target (next-day ATM IV); saves/LSTM features/target CSVs.
- Stationarity check via ADF (`adfuller`).
### `Forecasting IV Using LSTM - Predictions.ipynb`
- **Concept:** build/train/evaluate an LSTM regression model to predict next-day ATM IV; split train/test, scale (MinMaxScaler), actual-vs-predicted.
- **Prereq:** LSTM, feature/target build, scaling, time-series.
- Loads `lstm_features_iv_forecast_2015_2023.csv`, `lstm_target_iv_forecast_2015_2023.csv`; TensorFlow/Keras `Sequential`, `LSTM`, `Dense`; saves `forecasted_iv_lstm_2021_2023.bz2`.
### `Short Straddle-Forecasted IV.ipynb`
- **Concept:** use LSTM-forecasted IV to trade a short straddle: enter when predicted IV < current IV (expect vol contraction → variance premium harvesting).
- **Prereq:** LSTM forecast (C_IV/P_IV from forecast), short straddle, ATM strike.
- Reads `forecasted_iv_lstm_2021_2023.bz2` (`PREDICTED_NEXT_DAY_ATM_IV`, `ATM`, `ATM_IV`); entry when predicted below current IV; exit conditions; backtest; trade-level analytics.
---
## Capstone Projects
### Strangle Capstone — `Capstone Project Model Solution.ipynb`
- **Concept:** model solution for the **short strangle** capstone; ties IV rank, skew rank, short strangle, and trading.
- **Prereqs:** IV rank, skew rank, short strangle strategy, entry/exit, backtesting, trade-level analytics.
- Reads options + IV rank + skew rank (joining); drop delta/IV/volume columns; entry high-IV rank; exit on rank/skew extremes; module `adv_opt_vol_strangle_capstone_utils`.
### Risk Mgmt Capstone — `Risk Management Capstone Solution.ipynb`
- **Concept:** model solution for the **risk management of a short straddle** capstone; risk gating & trade analytics.
- **Prereqs:** delta hedging, IV rank, skew rank, short straddle, dollar-based SL/TP, sensitivity analysis.
- Module `capstone_risk_management_utils` provides `trade_level_analytics`, `sensitivity_analysis`.
---
## Python Modules
### `adv_options_volatility_utils.py`
- `trade_level_analytics(round_trips, lot_size)` — win % / loss %, per-trade winners/losers PnL, profit factor, post-cost PnL.
- `add_to_mtm(mark_to_market, option_strategy, trading_date)` — daily mark-to-market accumulation.
- `get_premium(options_strategy, options_data)` — CE (`[C_LAST]`) / PE (`[P_LAST]`) premium.
- `get_delta(options_strategy, options_data)` — CE (`[C_DELTA]`) / PE (`[P_DELTA]`).
- `setup_straddle(options_data, direction='short')` — construct `long`/'short' straddle with Position +1/−1, Premium, Delta.
- `sensitivity_analysis(...)` — per-strategy sensitivity of PnL to parameter thresholds (delta, rank).
### `adv_opt_vol_strangle_capstone_utils.py`
- Strangle-specific variants of premium/mtm/trade analytics for the strangle capstone.
### `capstone_risk_management_utils.py`
- Capstone-specific `trade_level_analytics`, `sensitivity_analysis` (risk-focused).
---
**Key concept graph:** IV → IV surface → volatility skew → delta-neutral skew → IV rank & skew rank → ranking-driven short straddle / short strangle → delta hedging & dollar-based SL/TP risk management → event-driven (FOMC straddles & calendar spreads) → LSTM IV forecasting → forecast-driven & strangle capstones.


====================
Algo-Trading-Zerodha
====================

# Algo Trading with Zerodha (Kite Connect) — Concept Inventory
## COURSE: AlgoTradingZerodhaResources
A () course on building automated trading systems in Python against the Zerodha Kite Connect API (and KiteTicker WebSocket). Covers authentication/session management, instrument lists, market quotes (LTP/OHLC/full quote), API rate limiting & batching, historical data & resampling, derivatives/Open Interest, order types (regular, stop-loss SL/SL-M, cover CO, GTT, AMO, Iceberg), order management, positions & holdings, WebSocket live streaming, SMA/crossover trading signals, a low-frequency polling system, and a full end-to-end automated trading system.
Notebooks enumerated (20): `KiteConnect Authentication`, `Storing and Reusing the Access Token`, `Fetching Full Instrument Lists`, `Fetching Live Quotes with Kite Connect`, `API Rate Limiting and Optimization Strategies`, `Fetching and Resampling Historical Data`, `Access Historical Derivatives Data and Analysing Open Interest`, `Streaming Live Market Data`, `Calculation of SMA Using Websockets`, `Trading Signal`, `Placing Your First Trade with Kite Connect`, `Monitoring and Managing Orders`, `Stop-Loss Orders`, `Cover Orders`, `GTT and AMO`, `Iceberg Orders`, `Managing Trading Positions with KiteConnect`, `Managing Portfolio Holdings with KiteConnect`, `Low Frequency Trading System`, `A Complete Automated Trading System`.
No local Python modules — relies on the external `kiteconnect` package (`KiteConnect`, `KiteTicker`) plus `pandas`, `matplotlib`.
---
## MODULE: API Login and Session Management
### LESSON: KiteConnect Authentication
- **KiteConnect API** — Zerodha's REST-like API giving programmatic access to a trading account (historical data, portfolio/funds, live order placement). prereqs: none.
- **`kiteconnect` Python package** — abstraction over HTTP calls; JSON responses returned as native Python structures. prereqs: none.
- **Installation** — `pip install kiteconnect`. prereqs: pip.
- **API key & API secret** — credentials from a developer-account app; treat like passwords (environment variables / config, never hardcoded). prereqs: none.
- **`login_url()`** — generates the manual-login URL. prereqs: KiteConnect init.
- **`request_token`** — one-time token captured from the redirect URL query string after browser login (User ID + Password + TOTP). prereqs: login_url.
- **`kite.generate_session(request_token)`** — exchanges `request_token` for the `access_token` used for all subsequent API calls. prereqs: request_token.
- **Authentication flow** — API key → login URL → request_token → session → access_token. prereqs: all above.
### LESSON: Storing and Reusing the Access Token
- **`access_token` lifetime** — valid for the full trading day; reusing avoids repeated manual logins. prereqs: access_token.
- **Storing the access token** — save `access_token` to a local file (e.g. `access_token.txt`) in the notebook folder for reuse. prereqs: access_token.
- **Reuse with fallback** — on run, load the saved token; on failure/expiry fall back to full manual login. prereqs: access_token.
- **`kite.profile()`** — fetches account profile details using the stored token. prereqs: authenticated kite object.
- **`kite.margins('equity')`** — fetches funds and margins data for a segment. prereqs: authenticated kite object.
- **`kite.logout()`** — invalidates the current access_token and ends the programmatic session; subsequent calls fail with auth errors. prereqs: access_token.
## MODULE: Fetching Market Quotes
### LESSON: Fetching Full Instrument Lists
- **Instrument master** — the full list of all tradable instruments (stocks, indices, commodities, derivatives) via a single API call. prereqs: none.
- **`kite.instruments()`** — downloads the complete instrument list (list of dicts). prereqs: authenticated kite object.
- **Instruments to DataFrame** — load the list into a pandas DataFrame for querying. prereqs: pandas.
- **`instrument_token`** — unique numeric id needed for orders, historical data, and live subscriptions (found from the instrument list). prereqs: instrument master.
- **Filtering by exchange** — filter the `exchange` column for NSE (equities), NFO (futures & options), MCX (commodities). prereqs: instrument DataFrame.
- **KiteAuth helper class** — reusable class wrapping the manual login (URL → request_token → access_token). prereqs: authentication.
### LESSON: Fetching Live Quotes with Kite Connect
- **Instrument symbol format** — `EXCHANGE:TRADINGSYMBOL` (e.g. `NSE:INFY`). prereqs: instrument master.
- **LTP (Last Traded Price)** — quickest price call; `kite.ltp()` returns dict of `instrument_token` + `last_price`. prereqs: authenticated kite object.
- **OHLC quotes** — day's open, high, low, and previous close; `kite.ohlc()`. prereqs: LTP.
- **Full quote** — comprehensive packet (OHLC, LTP, volume, average traded price, market depth of top-5 bids/asks); `kite.quote()`. prereqs: OHLC.
- **Market depth** — top-5 pending bids/asks used for limit-vs-market order decisions and liquidity assessment. prereqs: full quote.
- **When to use each format** — LTP for dashboards/watchlists; OHLC for daily/candlestick analysis; full quote for order-placement logic. prereqs: quote formats.
- **Polling vs streaming** — quote functions are polling-based; tick-by-tick needs the WebSocket API. prereqs: quote formats.
### LESSON: API Rate Limiting and Optimization Strategies
- **API rate limits** — servers cap requests/second for stability & fair use; Kite limits ~10 requests/second, exceeding triggers errors (HTTP 429 / `TokenException`). prereqs: none.
- **Consequences of ignoring limits** — requests get blocked and the application breaks. prereqs: rate limits.
- **Batch processing** — request multiple instruments in one call (`ltp`, `ohlc`, `quote` all support it); the single most effective optimization. prereqs: quote functions.
- **Throttling** — introduce `time.sleep()` delays between polling calls to stay within the rate limit. prereqs: polling.
- **Prefer WebSockets for high frequency** — streams push data instead of repeated polls. prereqs: streaming.
## MODULE: Historical Data Analysis
### LESSON: Fetching and Resampling Historical Data
- **Historical OHLCV data** — foundation for backtesting, analysis, and signal generation; per-instrument across timeframes. prereqs: none.
- **`kite.historical_data(instrument_token, from, to, interval)`** — fetches historical data, requires token not symbol. prereqs: instrument_token.
- **Interval data limits** — e.g. 1-min 60 days, 3/5/10-min 100 days, 15/30-min 200 days, 60-min 400 days, day 2000 days. prereqs: historical_data.
- **Resampling** — converting a time series from one frequency to another. prereqs: pandas.
- **`.resample(freq).agg()`** — aggregate OHLCV when converting to a lower frequency. prereqs: pandas.
- **Setting index for resampling** — set the `date` column as the DataFrame index first. prereqs: resampling.
- **Verifying resampled data** — plot close prices of multiple frequencies to confirm logic. prereqs: matplotlib.
### LESSON: Access Historical Derivatives Data and Analysing Open Interest
- **Open Interest (OI)** — total outstanding (unsettled) derivative contracts; one buyer pairs with one seller. prereqs: derivatives.
- **Expired futures via continuous data** — use the `instrument_token` of a live contract + `continuous=True` to get stitched historical futures data. prereqs: historical_data.
- **Expired options data unavailable** — historical candlestick data for specific expired options not offered by Kite Connect. prereqs: historical_data.
- **`oi=True`** — include Open Interest in the historical response. prereqs: historical_data.
- **OI + price sentiment signals** — Price↑ / OI↑ = long buildup (bullish); Price↓ / OI↑ = short buildup (bearish); Price↑ / OI↓ = short covering; Price↓ / OI↓ = long unwinding. prereqs: Open Interest.
- **Dual-axis price vs OI plot** — visualise trend conviction & exhaustion. prereqs: matplotlib.
## MODULE: Streaming Data
### LESSON: Streaming Live Market Data
- **WebSocket / KiteTicker** — persistent connection for streaming every price tick (push, vs polling pull). prereqs: none.
- **`KiteTicker(api_key, access_token)`** — the WebSocket streaming class. prereqs: kiteconnect.
- **Callback functions** — event-driven handlers: `on_ticks` (every tick), `on_connect` (connection established), `on_close` (disconnected). prereqs: KiteTicker.
- **Assigning callbacks** — set handler functions on the `kws` `on_` attributes. prereqs: callbacks.
- **Subscribing instruments** — subscribe to instrument tokens (e.g. Reliance) to receive their updates. prereqs: instrument_token.
- **`kws.connect()`** — blocking call that listens forever until closed. prereqs: KiteTicker.
- **Streaming modes** — `ws.MODE_LTP`, `ws.MODE_QUOTE` change the data payload size (data-use optimization). prereqs: KiteTicker.
- **Reconnect logic** — call `connect()` again from `on_close` to make the script robust. prereqs: on_close.
### LESSON: Calculation of SMA Using Websockets
- **Parsing live ticks** — extract Last Traded Price (LTP) from each incoming tick. prereqs: on_ticks.
- **Stateful price history** — a `ltp_history` list stores recent prices. prereqs: streaming.
- **Fixed-size history** — trim the list to the SMA period (e.g. 10) by dropping the oldest price. prereqs: price history.
- **Live Simple Moving Average (SMA)** — recompute SMA of the window on every new tick when enough data has accumulated. prereqs: SMA, streaming.
- **Real-time indicator bridge** — going from receiving data to processing it into an indicator. prereqs: history, SMA.
### LESSON: Trading Signal
- **Crossover strategy** — classic SMA-crossover buys on bullish, sells on bearish crossover. prereqs: SMA.
- **State (memory) variable** — `position_status` remembers whether price was previously above (`BULL`) or below (`BEAR`) the SMA. prereqs: live SMA.
- **Why state is needed** — checking price-vs-SMA alone would signal every tick; only the *moment of crossing* matters. prereqs: crossover.
- **Bullish crossover signal** — price > SMA AND previous state was BEAR → BUY. prereqs: state, crossover.
- **Bearish crossover signal** — price < SMA AND previous state was BULL → SELL. prereqs: state, crossover.
- **Preventing repeated signals** — update `position_status` immediately after generating a signal. prereqs: state.
- **Signal→execution gap** — completes Data Feed → Analysis → Signals; execution comes next. prereqs: signals.
## MODULE: Order Execution
### LESSON: Placing Your First Trade with Kite Connect
- **`kite.place_order()`** — sends an order; parameters map to web-platform fields. prereqs: authenticated kite object.
- **Order parameters** — `variety`, `exchange`, `tradingsymbol`, `transaction_type`, `quantity`, `product`, `order_type`, `price`. prereqs: none.
- **Varieties** — `VARIETY_REGULAR`, `VARIETY_AMO` (after-market), `VARIETY_CO` (cover), plus GTT/Iceberg later. prereqs: place_order.
- **Transaction types** — `TRANSACTION_TYPE_BUY` / `TRANSACTION_TYPE_SELL`. prereqs: place_order.
- **Product types** — `PRODUCT_CNC` (delivery equity), `PRODUCT_MIS` (intraday), `PRODUCT_NRML` (overnight F&O). prereqs: place_order.
- **Order types (basic)** — `ORDER_TYPE_MARKET` (best available price) vs `ORDER_TYPE_LIMIT` (specific price or better; `price` param required). prereqs: place_order.
- **BUY vs SELL orders** — sell order identical except `transaction_type`. prereqs: place_order.
- **Other order types preview** — stop-loss limit/market, AMO, CO, GTT, Iceberg covered in later sections. prereqs: order types.
### LESSON: Monitoring and Managing Orders
- **`kite.orders()`** — fetches all of the day's orders; format into a pandas table. prereqs: authenticated kite object.
- **Order statuses** — OPEN, TRIGGER PENDING, COMPLETE, CANCELLED, REJECTED etc. (see Kite docs). prereqs: orders.
- **`kite.modify_order(order_id, ...)`** — change parameters of a pending order (e.g. price). prereqs: orders, order_id.
- **`kite.cancel_order(order_id)`** — cancel a pending order. prereqs: order_id.
- **`kite.order_history(order_id)`** — full lifecycle of a specific order (status changes). prereqs: order_id.
- **`kite.trades()`** — the trade book: only orders actually filled. prereqs: orders.
- **Postback / webhooks** — public-URL notifications for reliable order updates irrespective of timing. prereqs: order management.
## MODULE: Order Placement and Stop Loss Orders
### LESSON: Stop-Loss Orders
- **Stop-loss order** — risk-management instruction to auto-exit a trade at a predetermined level. prereqs: order placement.
- **Stop-Loss Market (SL-M)** — single trigger price; on hit, exit at next available market price; guaranteed execution but slippage-prone; API: `ORDER_TYPE_SLM`, `price=0`. prereqs: order types.
- **Stop-Loss Limit (SL)** — trigger price + limit price (worst acceptable); `ORDER_TYPE_SL`, limit `price` set; price control but execution not guaranteed if market gaps past limit. prereqs: order types.
- **Trigger price** — the price that activates the exit order. prereqs: stop-loss.
- **Exiting an existing buy position** — the protective exit order is a SELL with quantity matching the open position. prereqs: transaction type, stop-loss.
- **Slippage vs fill certainty trade-off** — SL-M guarantees close, SL caps price. prereqs: SL, SL-M.
### LESSON: Cover Orders
- **Cover Order (CO)** — special intraday order type (`product='MIS'`) combining entry + compulsory stop-loss into one automated command. prereqs: stop-loss, mas.
- **`variety=kite.VARIETY_CO`** — marks the order as a Cover Order. prereqs: place_order.
- **Two-legged structure** — initial Market/Limit entry + compulsory SL-M leg. prereqs: CO, order types.
- **Mandatory risk definition** — cannot place CO without defining maximum risk (trigger) upfront; enforces discipline. prereqs: CO.
- **`trigger_price`** — the stop-loss trigger of the CO entry. prereqs: CO.
- **`try...except` error handling** — wraps order placement so failures (insufficient margin, bad trigger) are reported, not crashed. prereqs: python exceptions.
### LESSON: GTT and AMO
- **Good Till Triggered (GTT)** — a standing instruction active up to one year; when the trigger price is met, Zerodha places a Limit order. prereqs: order types.
- **`place_gtt()`** — special method (not `place_order`) for placing GTTs. prereqs: GTT.
- **Single-leg GTT** — one trigger for one action (e.g. buy 5 TCS if price ≤ ₹3000). prereqs: GTT.
- **One-Cancels-Other (OCO) GTT** — two triggers on a holding (target above, stop-loss below); if one fires, the other auto-cancels; like a long-term bracket order. prereqs: GTT.
- **After Market Order (AMO)** — place orders after market close; broker sends to exchange at next open; `variety='amo'` in `place_order`. prereqs: order types.
### LESSON: Iceberg Orders
- **Iceberg order** — a large parent order split into several smaller child legs shown to the market; only one leg active at a time. prereqs: order types.
- **Purpose** — discreetly execute large quantities, minimizing market impact and hiding true size. prereqs: Iceberg.
- **`variety=kite.VARIETY_ICEBERG`** — marks the order as Iceberg. prereqs: place_order.
- **`iceberg_legs` & `iceberg_quantity`** — `iceberg_quantity = total_quantity / iceberg_legs`. prereqs: Iceberg.
- **Typical parameters** — limit `price`, `ORDER_TYPE_LIMIT`, `PRODUCT_CNC` for delivery, quantity = grand total. prereqs: place_order, product types.
- **Order placement & confirmation** — `place_order` returns parent `order_id`. prereqs: Iceberg.
## MODULE: Trading Positions
### LESSON: Managing Trading Positions with KiteConnect
- **`kite.positions()`** — returns current positions, split into Net (actual current) and Day (taken during the day). prereqs: authenticated kite object.
- **Position data fields** — `quantity` (positive long / negative short), `average_price`, `pnl`, `m2m` (mark-to-market unrealized P&L). prereqs: positions.
- **Mark-to-Market P&L** — unrealized P&L for current-day trades. prereqs: positions.
- **`kite.convert_position()`** — convert an intraday (MIS) position to overnight (CNC/NRML) or vice versa. prereqs: positions, margins.
- **Margin constraint on conversion** — conversion requires sufficient margin, else rejected. prereqs: convert_position.
- **Exiting a position** — place a counter order. prereqs: positions, order placement.
## MODULE: Portfolio Holdings
### LESSON: Managing Portfolio Holdings with KiteConnect
- **Holdings vs positions** — holdings are long-term delivery (CNC) investments in demat; positions are active day/net trades. prereqs: positions.
- **`kite.holdings()`** — fetches the list of all delivery instruments in the account. prereqs: authenticated kite object.
- **Holdings fields** — `tradingsymbol`, `quantity`, `t1_quantity` (T+1 not-yet-delivered), `average_price`, `last_price`, `pnl`. prereqs: holdings.
- **Settlement concepts** — T+1 shares, final (T+2 settled) quantity, realised/used/opening quantity. prereqs: holdings.
- **Pledge / collateral & e-authorisation** — collateral_quantity/type, authorised_quantity/date (eDIS) for selling. prereqs: holdings.
- **MTF (Margin Trading Facility)** — mtf.quantity, used, average_price, value, initial_margin. prereqs: holdings.
- **`kite.mf_holdings()`** — fetch mutual fund holdings (fund name, folio, quantity, average/last price, P&L). prereqs: holdings.
- **Portfolio-level totals** — compute invested value, current market value, and overall P&L. prereqs: holdings.
## MODULE: Low Frequency Trading System
### LESSON: Low Frequency Trading System
- **Polling architecture** — periodic pull (wake → fetch → calculate → sleep → repeat) instead of WebSocket push. prereqs: none.
- **Polling vs WebSocket fit** — polling for low-frequency swing/positional (hourly/daily) strategies; WebSockets for intraday reaction strategies. prereqs: streaming.
- **`fetch_data_and_calculate_sma`** — function fetching latest historical data and computing e.g. 200-day SMA. prereqs: historical_data, SMA.
- **`main_trading_loop`** — infinite `while True` that calls the data/analysis function, runs a trading-logic placeholder, then `time.sleep()`s to set frequency. prereqs: polling.
- **`if __name__ == "__main__":`** — guard so the loop only runs on direct script execution. prereqs: python.
- **Efficiency** — saves bandwidth/compute vs tick-reactive systems. prereqs: polling.
## MODULE: A Complete Automated Trading System
### LESSON: A Complete Automated Trading System
- **End-to-end system** — integrates KiteTicker (live data + signals) with KiteConnect (order execution) into one autonomous loop. prereqs: streaming, order placement.
- **`place_market_order` function** — dedicated, reusable order-placement function with error handling. prereqs: place_order.
- **Position state variable (`current_position`)** — `None` / `'LONG'` prevents duplicate orders. prereqs: state, signals.
- **Crossover + state gating in `on_ticks`** — calls `place_market_order` only on crossover when no open position. prereqs: crossover, positions.
- **`on_order_update` callback** — executed on every order update; prints order id, symbol, status, filled qty, average price, timestamp for real-time monitoring. prereqs: callbacks, orders.
- **Margin check** — `kite.order_margins()` computes requirement (span, exposure, option premium, additional, bo, cash, var, pnl) for large/spread orders before placing. prereqs: margins.
- **Postback (webhook) updates** — reliable arbitrary order updates (COMPLETE, CANCEL, REJECTED, UPDATE, partial fills) anytime. prereqs: order management.
- **Going live & risk disclaimer** — the script can place real trades; sequence: listen → analyze → signal → execute automatically. prereqs: all modules.
- **Extensions** — stop-loss/take-profit, position sizing by risk, RSI/MACD combo, reconnect logic, backtesting before live. prereqs: system.
---
## COURSE-LEVEL PREREQUISITE GRAPH
- Authentication (access_token) is the gateway for every subsequent notebook.
- Instrument master (token lookup) → quotes (LTP/OHLC/full) → historical data & derivatives/OI; rate-limit + batching applies to all polling calls.
- WebSockets (KiteTicker, callbacks) → live SMA → crossover trading signals → order execution integration.
- Order placement basics → stop-loss (SL/SL-M) → Cover Orders / GTT / AMO / Iceberg; order management after placement.
- Positions & holdings follow order execution.
- Two architecture patterns for the final system: WebSocket push (intraday) and polling (low-frequency).
- Out of scope (covered elsewhere): machine-learning signal generation (see *Python for Machine Learning*) and ARIMA/ARCH/GARCH statistical forecasting (see *Financial Time Series Analysis for Trading*).


====================
Backtesting-Trading-Strategies
====================

## COURSE: Backtesting Trading Strategies
### MODULE: Financial Data
#### NOTEBOOK: Daily Stock Price Data
- **Backtesting** — Simulating a trading strategy on historical data to evaluate its viability before going live. prereqs: none
- **yfinance** — Python package to download historical financial data from Yahoo Finance. prereqs: Python, pip
- **yf.download(ticker, start, end)** — Downloads OHLCV data for an asset across a date range into a DataFrame. prereqs: yfinance
- **OHLCV columns** — The open, high, low, close, adjusted close, and volume columns common to price data. prereqs: yfinance
- **Tickers for different geographies** — Suffixes denote exchange, e.g. HSBA.L (London), RELIANCE.NS (NSE India). prereqs: tickers
- **Plotting close price** — Using matplotlib `.plot()` to visualise a full year of price movement. prereqs: matplotlib
- **Adjusted vs unadjusted prices** — Raw closing prices vs prices adjusted for corporate actions. prereqs: price data
- **Corporate actions** — Stock splits, dividends, and rights offerings that alter historical prices. prereqs: adjusted prices
- **auto_adjust=True** — yfinance option returning all OHLCV columns already split/dividend-adjusted. prereqs: yf.download
- **warnings.filterwarnings('ignore')** — Suppresses warnings for a cleaner notebook. prereqs: Python
### MODULE: Data Pre-Processing
#### NOTEBOOK: Data Quality Checks and Data Cleaning
- **Data quality** — Ensuring input data is clean and reliable before analysis for trustworthy results. prereqs: none
- **pd.read_csv(parse_dates, index_col)** — Loading a CSV while parsing a date column and setting an index column. prereqs: pandas
- **parse_dates** — read_csv argument converting a named column to datetime (date columns default to strings). prereqs: read_csv
- **head() / tail()** — Previewing the first/last five rows of a DataFrame. prereqs: pandas
- **dataframe.info()** — Concise summary of columns, non-null counts, and dtypes. prereqs: pandas
- **isna()** — Returns a boolean Series marking missing (NA) values per element. prereqs: pandas
- **isna().sum()** — Counts missing values in each column. prereqs: isna
- **Missing / null values** — Gaps in the dataset that may skew analysis if not handled. prereqs: isna
- **dropna()** — Removes rows (axis=0/'index') or columns (axis=1/'columns') containing nulls. prereqs: pandas
- **dropna parameters (axis, how, inplace)** — `how='any'/'all'` choose when to drop; `inplace=True` mutates the DataFrame. prereqs: dropna
- **DataFrame.shape** — Tuple of (rows, columns); `shape[0]` gives the row count. prereqs: pandas
- **Duplicate values** — Repeated rows arising from human error or merging multiple sources. prereqs: data cleaning
- **duplicated().value_counts()** — Counts duplicated (True) vs unique (False) observations. prereqs: pandas
- **Proportion of duplicates** — Ratio of duplicate rows to total; small fractions may be ignored. prereqs: duplicated
- **Consecutive duplicate removal** — Using `.diff() != 0` across columns to drop only immediately repeated rows. prereqs: pandas diff
- **Outliers** — Values unusually large/small vs the rest of the data, detectable via large percentage changes. prereqs: data cleaning
- **pct_change() for outlier detection** — Plotting daily percentage change to spot extreme (anomalous) moves. prereqs: pct_change
### MODULE: Trading Rules
#### NOTEBOOK: Generate Entry and Exit Signals
- **Trading hypothesis** — The stated rule/sentiment basis driving when to enter and exit positions. prereqs: backtest concepts
- **Backtest flowchart** — A diagram of the full backtesting pipeline (import → signals → trade sheet → analytics). prereqs: none
- **Short-term & long-term lookback** — Window periods (9-day, 21-day) for the two moving averages. prereqs: moving averages
- **Short/long moving averages** — Simple moving averages of Close via `.rolling().mean()` stored as `ma_short`, `ma_long`. prereqs: pandas rolling
- **Signal definition** — `np.where(ma_short > ma_long, 1, 0)`: 1 when short MA is above long MA, else 0. prereqs: numpy
- **Entry condition** — Open a long position when the short-term MA crosses above the long-term MA from below. prereqs: signal
- **Exit condition** — Close the long position when the short-term MA crosses below the long-term MA from above. prereqs: signal
- **Holding period** — The date range during which a long position is active. prereqs: signal
- **Visualising holding periods** — Plotting price with `secondary_y` and `plt.fill_between(where=signal>0)` to shade in-position periods. prereqs: matplotlib
- **Strategy returns** — `signal.shift(1) * Close.pct_change()`; multiply prior-day signal by daily price change. prereqs: pct_change, shift
- **Lookahead avoidance (shift)** — Applying the signal a day later to prevent using same-day data for trades. prereqs: shift
- **Total cumulative strategy return** — `(strategy_returns+1).prod()-1` gives compounded return over the period. prereqs: prod, strategy returns
#### NOTEBOOK: Backtest and Generate Trade Sheet
- **Trade sheet** — A table of all backtested trades with positions, entry/exit dates, and entry/exit prices. prereqs: trading signals
- **Long crossover column** — Boolean marking entry days: previous day short<long and today short≥long. prereqs: moving averages
- **Exit/squared crossover column** — Boolean marking exit days: previous day short>long and today short≤long. prereqs: moving averages
- **np.where with shifted conditions** — Change-of-state detection using `.shift(1)` on the moving averages. prereqs: np.where
- **Trade record fields** — Position, Entry Date, Entry Price, Exit Date, Exit Price per completed trade. prereqs: trade sheet
- **current_position state variable** — Tracks '1' (holding long) or '0' (flat) during the backtest loop. prereqs: backtesting
- **Iterating over dates** — Looping `for current_date in data.index` to process each day's entry/exit logic. prereqs: pandas
- **pd.concat() to append trades** — Accumulating completed trades into a growing trade_sheet DataFrame. prereqs: pandas
- **backtest_trade_sheet() function** — A reusable wrapper producing the trade sheet from data and crossover columns. prereqs: trading rules
- **Trade PnL** — `(Exit Price - Entry Price) * Position` computes profit/loss per trade. prereqs: trade sheet
- **Total PnL** — Sum of all per-trade PnL, indicating overall strategy profit/loss. prereqs: trade PnL
### MODULE: Trade Level Analytics
#### NOTEBOOK: Trade Level Analytics
- **Trade level analytics** — Metrics describing performance across completed trades (not within them). prereqs: backtesting outputs
- **Total PnL** — `trades.PnL.sum()` gives the sum of all gains and losses across trades. prereqs: trade analytics
- **Number of trades** — Counting trades via indexing a Position/PnL subset (long trades only). prereqs: pandas filtering
- **Win rate (Win %)** — % of profitable trades: `(winners / total) * 100`; above 50% is favourable. prereqs: trade PnL
- **Loss rate** — % of losing trades: `(losers / total) * 100`. prereqs: total trades
- **Average profit per winning trade** — Sum of winner PnL divided by winner count. prereqs: win rate
- **Average loss per losing trade** — Mean absolute value of losing trades' PnL. prereqs: loss rate
- **Average trade duration (holding period)** — Mean of `(Exit Date - Entry Date)`; capital is locked during a trade. prereqs: trade sheet
- **pd.to_datetime() on entry/exit dates** — Casting to datetime so holding periods can be subtracted. prereqs: pandas
- **Profit Factor** — Ratio of (Win% × avg win PnL) to (Loss% × avg loss PnL); a graded strategy-quality metric. prereqs: win/loss rate, averages
- **Profit-factor interpretation** — Grades: <1 unprofitable, 1 breakeven, 1.1–1.4 average, 1.4–2.0 decent, ≥2 excellent. prereqs: profit factor
### MODULE: Performance Metrics
#### NOTEBOOK: Performance Metrics
- **Performance metrics** — Measures evaluating a strategy's behaviour between trade entry and exit. prereqs: trade analytics
- **Strategy returns** — `signal.shift(1) * Close.pct_change()` gives per-day strategy return. prereqs: pct_change
- **Equity curve** — Plot of cumulative strategy returns over time; positive slope indicates profitability. prereqs: returns
- **Cumulative returns** — `(returns+1).cumprod()` running product compounding daily returns. prereqs: strategy returns
- **CAGR** — Compound Annual Growth Rate: `((EV/BV)^(1/n)-1)*100` annualising growth with compounding. prereqs: equity curve, returns
- **Histogram of returns** — `Strategy_Returns.hist(bins=50)` shows the distribution of daily returns. prereqs: matplotlib
- **Annualised volatility** — `std() * sqrt(252)` converts daily volatility to a yearly figure. prereqs: std, annualisation
- **Standard deviation (volatility)** — Average dispersion/fluctuation of the strategy returns. prereqs: statistics
- **Sharpe ratio (with risk-free)** — `(mean_return - daily_risk_free)/std * sqrt(252)`; ratio of excess return to volatility. prereqs: mean, std, risk-free
- **Risk-free rate** — A baseline (e.g. 2%/year) subtracted from returns before Sharpe; converted to daily. prereqs: Sharpe ratio
- **Maximum drawdown** — Max loss from a running peak to a trough of the equity curve: `(Cum-Ret - Peak)/Peak`. prereqs: equity curve
- **Cumulative maximum (Peak)** — `Cumulative_Returns.cummax()` tracks the running peak of the curve. prereqs: pandas
- **Drawdown series** — Per-day percentage decline of returns from the running peak. prereqs: cumulative max
- **Plotting drawdowns** — `plt.plot` + `plt.fill_between(where=drawdown)` to show frequency/severity of losses. prereqs: matplotlib
### MODULE: Risk Management
#### NOTEBOOK: Backtesting With Stop-Loss and Take-Profit
- **Stop-loss** — A predefined price level that caps a trade's loss; exiting when price falls to it. prereqs: risk management
- **Take-profit** — A predefined price level that locks in profit; exiting when price rises to it. prereqs: risk management
- **Exit conditions (with stop-loss/take-profit)** — Exit on low≤stop-loss, high≥take-profit, or a crossover exit. prereqs: risk rules
- **Stop-loss / take-profit price** — `entry_price * (1 ± percentage)` for SL and TP levels at entry. prereqs: position sizing
- **Stop-loss & take-profit percentages** — Levels set as a fraction of the long entry price (e.g. 3% SL, 15% TP). prereqs: risk parameters
- **Exit Type column** — Labels each closed trade as 'Stop-Loss', 'Take-Profit', or 'Exit_crossover/Squareoff'. prereqs: trade sheet
- **backtest_trade_sheet_sl_tp()** — Function to generate trades adding SL/TP breach checks to the backtest loop. prereqs: backtest function
- **PnL with stop-loss/take-profit** — Same `(Exit - Entry)*Position` PnL; adding SL/TP can raise total PnL (e.g. +19%). prereqs: trade PnL
- **close-column breach testing** — Using the day's close/price value to decide if a stop-loss/take-profit was hit. prereqs: stop-loss
### MODULE: Transaction Costs and Slippage
#### Notebook: Implementation of Transaction Cost and Slippage
- **Transaction costs** — Commissions/fees, slippage, and taxes paid to execute trades; must be modelled pre-live. prereqs: backtesting
- **Brokerage fee** — The commission a broker charges to execute a transaction (e.g. 0.03% of traded value). prereqs: trading costs
- **Tax on trades** — Government tax imposed on financial transactions (e.g. 0.02%). prereqs: trading costs
- **Total brokerage cost** — Sum of brokerage + tax percentages (e.g. 0.05% combined). prereqs: brokerage, tax
- **Slippage** — Difference between expected trade price and actual execution price; estimated from market data. prereqs: transaction costs
- **Last 5-minute candles** — Using the final five one-minute price candles of each day to estimate end-of-day slippage. prereqs: slippage modelling
- **groupby(date).tail(5)** — Keeping the last N rows per day to isolate closing-minute bars. prereqs: groupby
- **Slippage for buy orders** — `(High - Close)/Close`: worst buy execution is at the bar high. prereqs: slippage modelling
- **Slippage for sell orders** — `(Close - Low)/Close`: worst sell execution at the bar low. prereqs: slippage modelling
- **Mean & maximum slippage** — Averaging daily slippage then taking the maximum buy/sell cost as the estimate (e.g. 0.09%). prereqs: slippage modelling
- **Transaction cost** — A fixed per-dollar cost on shares purchased/sold (e.g. 0.001). prereqs: costs
- **Total charges** — Sum of transaction cost + slippage cost + brokerage cost. prereqs: costs & slippage
- **Trading cost on position change** — `total_charges * |signal - signal.shift(1)|` applies cost only when position changes. prereqs: signal, shift
- **Net strategy returns** — Subtract the trading cost from raw strategy returns to get realistic returns. prereqs: strategy returns
- **Cumulative returns after costs** — `(net_returns+1).cumprod()` plots growth after all charges. prereqs: cumprod
- **Comparing costed vs uncosted results** — Showing how costs degrade headline strategy performance before going live. prereqs: cumulative returns
### MODULE: Capstone Project
#### NOTEBOOK: Capstone Project Solution Template
- **Multi-stock backtest** — Backtesting the moving-average crossover strategy on Apple, Facebook, Microsoft, and Tesla. prereqs: backtesting
- **Capital-reading multiple prices** — Reading a CSV with four price series and parsing the date index to datetime. prereqs: read_csv
- **Computing moving averages for many stocks** — `.rolling(window).mean()` applied across an entire multi-column DataFrame. prereqs: rolling
- **Signals for the portfolio** — Comparing short/long moving averages across all stocks at once. prereqs: moving averages
- **Equal-weighted portfolio** — Averaging strategy returns across stocks (`.mean(axis=1)`) as a simple portfolio. prereqs: equity curves
- **Equity curves per stock & portfolio** — Plotting `(returns+1).cumprod()` for each stock and the equal-weighted average. prereqs: cumulative returns
- **CAGR for a portfolio** — Annualising portfolio compounded returns via `((cumprod.iloc[-1] ** (252/days)) - 1) * 100`. prereqs: CAGR
- **Portfolio Sharpe ratio** — Applying the annualised Sharpe formula to mean portfolio returns vs a 2% risk-free rate. prereqs: Sharpe ratio
#### NOTEBOOK: Capstone Project Model Solution
- **Data ingestion & datetime index** — `pd.read_csv` + `data.index = pd.to_datetime(...)` normalises index across assets. prereqs: pandas
- **Multiple rolling means** — `data.rolling(9).mean()` / `data.rolling(21).mean()` over all stock columns. prereqs: rolling
- **Signal with boolean→int** — `ma_short > ma_long` yields a boolean DataFrame; `.astype(int)` converts to 1/0. prereqs: signals
- **Strategy returns (element-wise)** — `signal.shift(1) * data.pct_change()` lets pandas broadcast across all assets. prereqs: pct_change, shift
- **Equity curve plotting** — `plt.plot((strategy_returns+1).cumprod())` draws cumulative returns per stock. prereqs: matplotlib, cumprod
- **Plot legend & tick_params** — `plt.legend(...)` and `plt.tick_params(labelsize=15)` polish the equity plot. prereqs: matplotlib
- **Equal-weighted portfolio curve** — `(strategy_returns.mean(axis=1)+1).cumprod()` averages across the four stocks. prereqs: equity curves
- **Portfolio CAGR** — Compounding portfolio returns then annualising with the 252-day exponent. prereqs: CAGR
- **Daily risk-free rate for Sharpe** — Setting `risk_free_rate = 0.02/252` before computing the pool Sharpe. prereqs: Sharpe ratio
- **drawdown_cal() function** — A custom function returning (max drawdown, drawdown series) from a cumulative-returns series. prereqs: drawdown
- **running_max via np.maximum.accumulate()** — Cumulative running peak of the pooled portfolio returns, floored at 1. prereqs: numpy
- **Maximum drawdown of portfolio** — Deepest % peak-to-trough loss (e.g. −22.04%) via the min drawdown. prereqs: drawdown_cal
- **Plotting portfolio drawdown** — `plt.plot(drawdown)` plus `plt.fill_between(..., red)` to visualise loss periods. prereqs: matplotlib
---
## Backtesting-Trading-Strategies — Section-based course structure
# Concept Inventory — Backtesting Trading Strategies
## COURSE: Backtesting Trading Strategies
### Section: Section 1 - Introduction
- **Course structure & roadmap:** how the course is organized into backtesting steps (data → rules → analytics → metrics → risk). prereqs: none.
- **What you will learn in the course:** the end-to-end backtesting workflow. prereqs: none.
### Section: Section 2 - Backtesting
- **What is Backtesting:** evaluating a trading strategy on historical data to estimate its performance without risking capital. prereqs: none.
- **Backtesting vs Simulation:** backtesting runs on *historical* data; simulation can use synthetic/future hypothetical scenarios. prereqs: what is backtesting.
- **Backtesting Process:** the step-by-step pipeline (get data, pre-process, define rules, execute, measure). prereqs: what is backtesting; financial data.
- **Key decisions & parameters for backtesting:** period selection, dataset scope, bias avoidance. prereqs: what is backtesting.
- **Backtesting platforms:** tools used to construct and run backtests. prereqs: what is backtesting.
### Section: Section 3 - Financial Data
- **Financial data:** price (OHLCV), fundamental, sentiment and news data used as inputs to a strategy. prereqs: none.
- **Financial data storage:** organization/persistence of price & volume data for analysis. prereqs: financial data.
- **Limitations of financial data:** data is not always available, may be missing/erroneous, survivorship-ed; affects result reliability. prereqs: financial data.
- **Getting market data via APIs / Python packages:** retrieving data programmatically (pandas, yfinance-style tools). prereqs: financial data; Python basics.
- **Fundamental & sentiment data sources:** alternate data feeds beyond prices. prereqs: financial data.
### Section: Section 4 - Data Pre-Processing
- **Data pre-processing / cleaning:** handling incorrect and missing values so analysis is statistically valid. prereqs: financial data.
- **Data cleaning importance:** erroneous values produce disastrous/misleading backtest results. prereqs: data pre-processing.
- **Survivorship bias:** using only currently-listed stocks inflates performance because delisted (failed) stocks are excluded. prereqs: data pre-processing; financial data.
- **Look-ahead bias:** using information not yet available at the trade time; avoided with point-in-time databases. prereqs: survivorship bias.
### Section: Section 5 - Trading Rules
- **Developing trading rules:** encoding a strategy's entry/exit logic explicitly and consistently. prereqs: backtesting.
- **Entry and Exit rules:** the specific conditions that open and close positions. prereqs: trading rules.
### Section: Section 6 - Trade Level Analytics
- **Trade level analytics I:** per-trade measures used to inspect individual trades. prereqs: trading rules.
- **Trade level analytics II:** win ratio, average P&L of winning trade, profit factor, average trade duration. prereqs: trade level analytics I.
- **Average Profitability Per Trade (APPT):** P/L ratio alone is insufficient; APPT combines win rate and payoff. prereqs: trade level analytics.
- **17 common trading metrics:** suite of metrics to interpret a strategy's generated trades. prereqs: trade level analytics.
### Section: Section 7 - Performance Metrics
- **Equity Curve:** cumulative value/growth of a strategy over time. prereqs: cumulative returns.
- **CAGR (Compound Annual Growth Rate):** annualized return of the equity curve. prereqs: equity curve; cumulative returns.
- **Sharpe Ratio:** excess return per unit of total risk (volatility). prereqs: returns; standard deviation.
- **Sortino Ratio:** Sharpe-type measure using only downside volatility. prereqs: Sharpe ratio.
- **Maximum Drawdown:** largest peak-to-trough decline in the equity curve — a core risk measure. prereqs: equity curve.
- **Cumulative Returns (computation):** product of successive (1+r) terms; can be expressed as growth multiplier or as percentage (−1). prereqs: returns.
- **Performance/risk metrics & strategy optimisation:** metrics used not just to measure but to tune strategies. prereqs: performance metrics.
### Section: Section 8 - Risk Management
- **Stop-Loss and Take-Profit:** predefined exit levels limiting loss and locking profit. prereqs: entry/exit rules; performance metrics.
- **Guidelines for setting Stop-Loss / Take-Profit:** how to choose levels (e.g., via MAE). prereqs: stop-loss & take-profit.
- **Maximum Adverse Excursion (MAE):** worst adverse price move during a trade; used to set optimum stop-loss. prereqs: stop-loss; risk management.
- **Maximum Favorable Excursion (MFE):** best favorable move; used to size positions relative to risk. prereqs: MAE; risk management.
- **Fixed vs trailing stop-loss:** trade-off between cost and protection. prereqs: stop-loss.
- **Algorithmic trading risks & checks:** operational/compliance risks of running strategies live. prereqs: risk management.
### Section: Section 9 - Transaction Costs and Slippage
- **Transaction costs:** commissions and other fees that erode strategy returns. prereqs: performance metrics.
- **Slippage:** difference between expected and actual fill price. prereqs: transaction costs.
- **Slippage decomposition:** spread, market impact, and volatility costs. prereqs: slippage.
- **Estimating and minimising slippage:** accounting for costs so backtests reflect reality. prereqs: slippage; transaction costs.
### Section: Section 10 - Paper Trading
- **Introduction to Paper Trading:** running a strategy on live/streaming data without real capital. prereqs: backtesting.
- **Advantages/disadvantages of paper trading:** validation before risking capital; psychological and data-bookkeeping caveats. prereqs: paper trading.
- **Things to keep in mind while paper trading:** how long to paper trade, realistic fills, discipline. prereqs: paper trading; slippage.
### Section: Section 13 - Common Pitfalls in Backtesting
- **Biases to avoid:** general category of systematic errors in backtests. prereqs: data pre-processing.
- **Survivorship & look-ahead bias via point-in-time data:** using point-in-time databases to avoid biases. prereqs: survivorship bias; look-ahead bias.
- **Data Snooping:** testing many parameter combinations until one 'works' by chance (multiple-testing problem). prereqs: biases; statistics basics.
- **Common mistakes with trading volume:** assuming you can trade more than available volume/liquidity. prereqs: financial data; slippage.
- **Over-reliance on backtesting:** backtests are no guarantee of future live performance. prereqs: backtesting.
- **LTCM case study:** importance of risk management (Long Term Capital Management collapse). prereqs: risk management.
### Section: Section 14 - FAQs
- **Ideal time period for backtesting:** choosing a representative sample window. prereqs: backtesting.
- **Number of assets to backtest on:** diversification vs overfitting trade-off. prereqs: backtesting.
- **Risk metrics and Sharpe ratio questions:** interpretation of common metrics. prereqs: Sharpe ratio; risk management.
- **Paper vs live trading differences:** why live results differ from backtest. prereqs: paper trading.
### Section: Section 15 - Capstone Project
- **Capstone project — moving-average crossover backtest:** build & backtest a long-only 9/21-day MA crossover on 4 stocks; equal-weighted portfolio; compute CAGR, Sharpe, MaxDD. prereqs: all prior sections.
### Section: Section 17 - Course Summary
- **Course recap and next steps:** entire backtesting process; follow-on Python-for-trading courses. prereqs: all prior sections.
## Course Prerequisite Map
- Backtesting itself is foundational (needs only market basics): *Backtesting → Simulation, Process, Platforms, FAQs, Capstone.*
- Financial data builds on none; *Financial Data → Storage → Pre-Processing → Survivorship/Look-ahead bias.*
- Trading Rules needs backtesting; *Trading Rules → Entry/Exit → Trade Level Analytics.*
- Performance Metrics needs returns: *Returns → Cumulative Returns → Equity Curve → CAGR/Drawdown; + Sharp/Sortino.*
- Risk Management builds on Entry/Exit + Performance Metrics; *MAE/MFE → stop-loss guidelines.*
- Transaction Costs/Slippage builds on metrics; *Transaction Costs → Slippage (spread/impact/vol).*
- Paper Trading and Common Pitfalls build on backtesting + data + statistics fundamentals.
- Course flow: **Introduction → Backtesting → Financial Data → Pre-Processing → Trading Rules → Trade Analytics → Performance Metrics → Risk Mgmt → Costs/Slippage → Paper Trading → Pitfalls → FAQs → Capstone.**
- FunPath basics feeding this course (from Track ladder): Python basics for trading, returns math (simple/cumulative/log), basic statistics (mean, std, correlation).


====================
Candlestick-Patterns
====================

# Candlestick Patterns — Concept Inventory
## COURSE: Candlestick Patterns
A () course on identifying Japanese candlestick patterns (bullish marubozu, hammer, hanging man, shooting star) with TA-Lib, visualising them on candlestick charts with mplfinance, and backtesting long/short strategies with stop-loss/take-profit levels. Covers trade sheets, trade-level analytics, performance metrics, data resampling, and a multi-asset capstone. Repeated concepts (strategy returns, trade analytics, performance metrics) are defined once and reused across patterns.
---
## MODULE: Bullish Marubozu Pattern
### LESSON: Visualise Bullish Marubozu
- **Candlestick chart** — visualises OHLC as candles with bodies and wicks, showing open/close/high/low. prereqs: none.
- **Bullish Marubozu** — a long-bodied candle with no (or very small) shadow, signifying extreme bullishness. prereqs: candlestick chart.
- **Bearish Marubozu** — the bearish counterpart of the bullish marubozu. prereqs: bullish marubozu.
- **`ta.CDLMARUBOZU(open, high, low, close)`** — TA-Lib returns +100 for bullish, −100 for bearish, 0 if no pattern. prereqs: talib.
- **`mplfinance` (`mpf`)** — a library for plotting candlestick charts. prereqs: none.
- **`mpf.plot(...)`** — plots a candlestick chart with `type='candle'`, style, and volume options. prereqs: mplfinance.
- **`mpf.make_addplot()`** — adds overlay markers (e.g. pattern flags) to the candlestick chart. prereqs: mplfinance.
- **Pattern marker** — place a scatter marker slightly above the high (e.g. `1.01 × High`) to flag a pattern. prereqs: addplot.
- **`np.where(pattern_signal == 100, high×1.01, np.nan)`** — builds marker positions only where the pattern occurs. prereqs: numpy.
---
## MODULE: Backtesting Bullish Marubozu
### LESSON: Backtesting Bullish Marubozu
- **Candlestick backtesting** — simulate trading on pattern signals over historical price data. prereqs: pattern identification.
- **Entry condition** — enter long at the current candle's Open if the previous candle is a bullish marubozu. prereqs: bullish marubozu.
- **Entry signal** — `np.where(pattern_signal == 100, 1, 0)`; 1 marks a long entry. prereqs: numpy.
- **Stop-loss (bullish)** — set at the minimum Low of the previous n candles. prereqs: risk/regime.
- **Take-profit (bullish)** — set at entry + (entry − SL), a risk-reward multiple of the stop. prereqs: stop-loss.
- **`exit_values()`** — helper computing stop-loss and take-profit from entry price and the last n lows/highs. prereqs: backtesting.
- **Iterative backtest loop** — walk over rows, open on entry, close when SL/TP hit, and record each trade. prereqs: loops.
- **Trade sheet** — table of Entry Date/Price, Exit Date/Price, Exit Type, PnL. prereqs: backtesting.
- **Trade signal column** — mark 1 on entry dates and 0 on exit dates, then forward-fill. prereqs: signals.
- **`isin()`** — pandas membership test used to locate entry/exit dates in the price index. prereqs: pandas.
### LESSON: Trade Level Analytics (Marubozu backtest)
- **Trade-level statistics** — metrics evaluating the strategy after each trade is executed. prereqs: trade sheet.
- **Total PnL** — the sum of gains and losses across all trades. prereqs: trade sheet.
- **Win rate/percentage** — number of winning trades / total trades × 100. prereqs: trade sheet.
- **Loss percentage** — losing trades / total trades × 100. prereqs: trade sheet.
- **Average PnL per trade** — mean profit per winning and mean loss per losing trade (absolute value). prereqs: trade sheet.
- **Average trade duration** — average holding period; capital is locked while a trade is open. prereqs: trade sheet.
- **Profit factor** — (Win% × avg win) / (Loss% × avg loss); gained dollars per lost dollar. prereqs: win rate.
- **Profit-factor interpretation** — <1 unprofitable, =1 breakeven, >1 desired. prereqs: profit factor.
### LESSON: Performance Metrics (Marubozu backtest)
- **Performance metrics** — analyse returns between a trade's entry and exit. prereqs: trade analytics.
- **Open-to-close / close-to-close returns** — `(Close/Open − 1)` and `pct_change()`. prereqs: returns.
- **Strategy returns with open-to-close handling** — apply open-to-close returns on the day a new trade enters. prereqs: strategy returns.
- **Equity curve** — plot of cumulative strategy returns; consistently positive slope implies profit. prereqs: cumulative returns.
- **Cumulative returns** — `(strategy_returns + 1).cumprod()`. prereqs: strategy returns.
- **CAGR** — compound annual growth rate; `(final^(252/days) − 1) × 100`. prereqs: cumulative returns.
- **Histogram of returns** — the distribution of the strategy returns. prereqs: strategy returns.
- **Annualised volatility** — `std(strategy_returns) × sqrt(252)` for daily data. prereqs: returns.
- **Sharpe ratio** — `(R_x − R_f)/σ_x`; excess return per unit of risk; >1 preferred. prereqs: returns, volatility.
- **Risk-free rate** — return of a risk-free asset used in the Sharpe ratio. prereqs: Sharpe ratio.
- **Maximum drawdown** — `(Peak − Trough)/Peak` of cumulative equity; the largest peak-to-trough loss. prereqs: equity curve.
- **`cummax()`** — pandas rolling maximum tracking the equity peak. prereqs: pandas.
- **Drawdown series** — `(Cumulative − Peak)/Peak`. prereqs: maximum drawdown.
---
## MODULE: Hammer Candlestick Pattern
### LESSON: Backtesting and Analysing Hammer Patterns
- **Hammer candlestick** — formed during a downtrend; signals a possible reversal of the existing downtrend (bullish). prereqs: candlestick.
- **`ta.CDLHAMMER(open, high, low, close)`** — TA-Lib returns `100` for a hammer, otherwise `0`. prereqs: talib.
- **Downtrend check** — confirm the three prior close prices are in ascending order before entering. prereqs: close series.
- **Hammer entry** — enter a long at the next candle's Open after a hammer forms, given a downtrend. prereqs: hammer pattern.
- **Hammer stop-loss** — set at the Low of the hammer candle. prereqs: risk exits.
- **Hammer take-profit** — set at entry + (rr × (entry − SL)) using a reward-to-risk ratio. prereqs: hammer stop-loss.
- **Reward-to-risk ratio (rr)** — scales take-profit relative to risk; often rr=3 for hammers. prereqs: take-profit.
- **`backtesting(data, direction, rr)`** — packaged backtest helper producing trades and signals. prereqs: backtesting.
- **`trade_level_analytics(trades)`** — packaged helper computing trade-level statistics. prereqs: trade analytics.
- **`performance_metrics(data, direction)`** — packaged helper computing strategy metrics. prereqs: performance metrics.
---
## MODULE: Hanging Man Candlestick Pattern
### LESSON: Hanging Man Notebook
- **Hanging man candlestick** — formed during an uptrend; signals a possible reversal of the existing uptrend (bearish). prereqs: candlestick.
- **`ta.CDLHANGINGMAN(open, high, low, close)`** — TA-Lib returns `−100` for a hanging man, otherwise `0`. prereqs: talib.
- **Short entry** — enter a short at the next candle's Open if the previous candle is a hanging man and an uptrend exists. prereqs: hanging man pattern.
- **Uptrend condition** — confirm the prior three close prices are in descending order. prereqs: close series.
- **Hanging man stop-loss** — set at the High of the hanging man candle. prereqs: risk exits.
- **Hanging man take-profit** — set at entry − (SL − entry), the short-side risk/reward target. prereqs: hanging man stop-loss.
- **`backtesting(data, 'short', rr=1)`** — backtest the hanging man short strategy. prereqs: backtesting.
---
## MODULE: Shooting Star Candlestick Pattern
### LESSON: Resample Data (Shooting Star preparation)
- **High-to-low resampling** — resampling is only valid from higher frequency to lower frequency. prereqs: none.
- **Price mapping** — dict mapping open→first, high→max, low→min, close→last. prereqs: resampling.
- **`resample(interval).agg(mapping)`** — converts 1-minute candles to a coarser frequency (e.g. 5min). prereqs: pandas.
- **Resample interval values** — minute `m`, hour `H`, daily `D`, weekly `W`, monthly `M`. prereqs: resampling.
- **`dropna()` on resampled data** — removes off-market (weekend/holiday) NaNs. prereqs: resampling.
- **`closed` parameter** — which side (left/right) of an interval is included in aggregation. prereqs: resample.
- **`label` parameter** — how the output bucket is labeled (left vs right edge). prereqs: resample.
### LESSON: Shooting Star Notebook
- **Shooting star candlestick** — formed during an uptrend; signals a possible reversal to bearish. prereqs: candlestick.
- **`ta.CDLSHOOTINGSTAR(open, high, low, close)`** — TA-Lib returns `−100` for a shooting star, otherwise `0`. prereqs: talib.
- **Short entry for shooting star** — enter short on the next candle when the previous candle is a shooting star and an uptrend exists. prereqs: shooting star pattern.
- **Shooting star stop-loss** — set at the High of the shooting star candle. prereqs: risk exits.
- **Shooting star take-profit** — target at entry − (SL − entry), the rr-scaled short target. prereqs: shooting star stop-loss.
- **`backtesting(data, 'short', rr=1)`** — backtest the shooting star short strategy. prereqs: backtesting.
---
## MODULE: Capstone Project
### LESSON: Capstone Project Model Solution
- **Candlestick capstone** — build and backtest a candlestick-pattern strategy on multiple assets. prereqs: all modules.
- **Multi-asset price data** — daily OHLC data for two tickers (AAPL, TSLA) read from CSV. prereqs: read_csv.
- **Pattern identification** — detect marubozu and shooting star patterns with TA-Lib in one function. prereqs: talib.
- **Entry type conversion** — map 'Buy'/'Sell' labels to numeric +1/−1 positions for signal computation. prereqs: signals.
- **Strategy returns** — `trade_signal.shift(1) × Close.pct_change()`, cumulative-plotted. prereqs: strategy returns.
- **Portfolio returns** — combine each asset's strategy returns; equal-weight average; plot cumulative. prereqs: cumulative returns.


====================
Crypto-Trading-Strategies-Advanced
====================

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


====================
Crypto-Trading-Strategies-Intermediate
====================

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


====================
Data-and-Feature-Engineering-for-Trading
====================

# Data & Feature Engineering for Trading — Concept Inventory
**Totals:** 12 modules, 18 notebooks
Data-centric preparation for financial machine learning: bar/feature extraction from tick data (time, tick, volume, dollar, information/imbalance bars), stationarity & fractional differentiation, outlier identification, dataset hygiene (survivorship bias, delisted/redundant/multi-class stocks), news feature engineering (numerical + categorical), data labelling (fixed-time horizon, triple-barrier), and correct merging of fundamental data.
---
## Module: Exploratory Data Analysis in Finance
**Notebooks:** `Examining the OHLCV Data.ipynb`, `Working With Pickle File.ipynb`
### Prerequisites
- pandas dataframes; OHLCV structure; datatypes
### Concepts (Examining the OHLCV Data.ipynb)
- **EDA on multi-stock OHLCV pickle data:** ~700k rows, 8 columns (Date, Open, High, Low, Close, Adj Close, Volume, Symbol), ~203 unique symbols from Yahoo finance.
- **Data checks:** `.info()` for dtypes/memory, `.isnull().sum()` for nulls, `.describe()` for statistics, `.Date.min()/.max()` for range.
- **Read pickle:** `pd.read_pickle` on the `.bz2`-compressed dataset.
- **Profile report:** `ydata_profiling` `.profile_report()` for a quick automated data-quality overview.
### Concepts (Working With Pickle File.ipynb)
- **Pickle benefits:** retains datatypes (e.g., a `DatetimeIndex`) across save/load, unlike CSV; supports `.bz2` compression for compact storage.
- **Save/load:** `df.to_pickle("file.bz2")` and `pd.read_pickle("file.bz2")`.
- **Version caveats:** pickle is Python/pandas-version-specific (backward compatible); errors like `AttributeError: Can't get attribute '_unpickle_block'...` (newer pandas read by older) and `ValueError: unsupported pickle protocol: 4` (needs Python ≥3.4).
---
## Module: Types of Bars — Features Extraction
**Notebooks:** `Creating Time Bars.ipynb`, `Creating Tick Bars.ipynb`, `Creating Volume Bars.ipynb`, `Creating Dollar Bars.ipynb`
### Prerequisites
- Tick/transaction data (time, price, volume)
- Resampling / aggregation to OHLCV
### Concepts
- **Bars** = sampled OHLCV buckets from raw tick data; bar type decides the **sampling criterion** (fixed time, fixed transactions, fixed volume, fixed dollar value).
- **Time bars** (`Creating Time Bars.ipynb`): resample ticks into fixed intervals (e.g., 5-min) using pandas `.resample('5T')`; Open=first, High=max, Low=min, Close=last, Volume=sum; drop empty slots (no transactions).
- **Tick bars** (`Creating Tick Bars.ipynb`): group a fixed number of ticks (`data.index // frequency`); aggregate open/high/low/close/volume per group; bar timestamp = last tick's time.
- **Volume bars** (`Creating Volume Bars.ipynb`): group ticks until cumulative volume crosses a threshold; `volume_grouper()` assigns a new group id whenever cumulative volume ≥ threshold; better statistical sampling (includes volume information).
- **Dollar bars** (`Creating Dollar Bars.ipynb`): group ticks until cumulative **dollar value** (`volume × price`) crosses a threshold; `dollar_value_grouper()`; according to academic literature, dollar bars surpass the standard bars in statistical properties (more i.i.d.-like sampling).
- All bar types plot cumulative returns to compare behavior.
---
## Module: Information Bars — Market Order Imbalances
**Notebook:** `Imbalance Bars.ipynb`
### Prerequisites
- Tick sampling; the **tick rule** (trade direction); EWMA
### Concepts
- **Information bars:** sample on "information" rather than fixed time/volume/dollar; **imbalance bars** are one kind, capturing the contrast between buy and sell orders (a sign of informed trading).
- **Tick rule:** sign of consecutive-tick price change (`signed_tick`); carried forward on zero change — proxy for trade direction.
- **Cumulative tick imbalance θ:** accumulated signed ticks up to time T.
- **Bar-sampling condition:** sample a new bar when `|θ_t| ≥ E₀[T]·(P[b=1] − P[b=−1])` (expected ticks × expected imbalance per tick).
- **Estimators:** expected number of ticks via **EWMA** (`pandas .ewm()`), and expected tick imbalance; `expected_num_ticks_init` hyperparameter seeds the first bar.
- Implementation walks ticks, accumulates imbalance, and emits OHLCV bars when imbalance becomes anomalous.
---
## Module: Why Stationary Features?
**Notebook:** `Fractional Differentiation.ipynb`
### Prerequisites
- **Stationarity** (mean, variance, autocorrelation invariant in time); ADF test
- The **memory vs stationarity dilemma**
- **Fractional differentiation** (Lopez de Prado)
### Concepts
- **The dilemma:** differenced series (returns) are stationary but **memory-less**; price levels have memory but are **non-stationary**. Predictors need both.
- **Fractional differentiation:** partially differentiate so the result is stationary AND retains memory — a series between returns and prices.
- **Backshift operator (B)** and its binomial-series expansion; the differentiation order **d** is real (not necessarily 1).
- **Weights:** binomial/palindromic weights per lag `w_k = −w_{k−1}/k·(d−k+1)`, starting w₀=1; **weights become 0 for k > d** (memory beyond that point is cut off). Weights alternate sign and peak mid-lag.
- **Weight threshold:** stop generating weights when |w| < threshold (a better memory proxy than a fixed count).
- **`fracDiff(series, d, thres)`:** apply weights to shifted series to build the fractionally differentiated series (uses log prices).
- **Finding optimal d (`findMinD`):** the smallest d whose fractionally-differentiated series passes the **ADF** test at the 1% level (returns d=0.2 for MSFT) — maximum memory while stationary.
- **Compare:** ADF statistics of log price (−3.27), returns (−15.89), and fractionally differenced (−3.75) — fractionally differenced is closer to the (memory-preserving) original yet stationary.
---
## Module: Outliers — How to Identify and Deal With Them
**Notebook:** `Dealing With Outliers.ipynb`
### Prerequisites
- Returns calculation; candlestick/volume plotting (`mplfinance`)
### Concepts
- **Outliers:** data points significantly different from the rest; must be identified and handled.
- **Zero-volume / inactive days:** check `describe()` and count rows with Volume==0 — remove illiquid/uninteresting days.
- **Returns on Adj Close:** compute daily returns per symbol via `groupby('Symbol').apply(pct_change)` (adjusted prices avoid split artifacts).
- **Infinite returns from zero Adjusted Close:** stocks with Adj Close==0 (penny/bankrupt symbols) cause ±inf; drop those symbols.
- **Abnormal return screening:** sort daily returns ascending/descending to find extreme single-day moves (e.g., UPL +3809%, WETF +3175%, YRCW −77%); use `describe()` (max 38.1) and **candlestick plots** (`mplfinance`/`candlestick_ohlc` with volume) to inspect `slice` windows around the anomaly date for structural context (splits, delistings, collapses).
---
## Module: Survivorship Bias for Stock Data
**Notebook:** `Delisted Stocks.ipynb`
### Prerequisites
- Index universes; **survivorship bias** concept
### Concepts
- **Survivorship bias:** analyzing only currently-listed stocks biases results upward; must include **delisted** stocks.
- **Finding delisted symbols:** compute the dataset's overall `max_date`; any symbol whose own `groupby('Symbol').Date.max()` is before that is flagged **delisted** (93 of 203 in the example).
- **Caveat:** assume missing data = delisting, but verify with other vendors (data could be unavailable for other reasons).
---
## Module: Redundant Stocks Data
**Notebook:** `Handling Duplicate Stock Data.ipynb`
### Prerequisites
- Close-price panel data; **redundant/duplicate** securities
### Concepts
- **Duplicate detection via identical closes:** many equal unadjusted close values between two symbols ⇒ closely-related/redundant data.
- **Stock pairs:** `itertools.combinations(columns, 2)` → N·(N−1)/2 pairs (20,503 here).
- **Identical-value screening:** count days where close prices are equal; flag pairs with ≥20 identical values (e.g., CBG/CBRE, CPRI/KORS, WLB/WLBAQ).
- **Runs analysis:** count consecutive runs of identical values (`groupby` + `Counter`) to confirm redundancy.
- **Investigation & cleanup:** plot pairs and research corporate events (e.g., KORS renamed to CPRI → keep CPRI; "Q" suffix = bankruptcy, WLB vs WLBAQ → keep WLBAQ) then discard the redundant symbol to avoid double-counting the same security.
---
## Module: Multiple Stock Classes — One or All?
**Notebook:** `Multiple Stock Classes.ipynb`
### Prerequisites
- Ticker conventions (hyphen = stock class, e.g., BF-A/BF-B, BRK-A/BRK-B, GOOG/GOOGL)
### Concepts
- **Multiple stock classes:** a company may issue A/B/C classes; typically include only **one** class in your universe.
- **Identify classed tickers:** `Symbol.str.contains("-")`, then strip the class suffix (`split('-')[0]`) to group classes by base ticker.
- **Selecting one class:** compare pairs via helper functions `plot_pair` (close & volume) and `check_range` (start/end date differences)
 - BF-A vs BF-B: same range, similar close, but BF-B much higher volume → keep BF-B.
 - LEN-A vs LEN-B: longer history + higher volume → keep LEN-A, drop LEN-B.
 - HEI-A vs HEI-B: volume mean/median higher for HEI-A → keep HEI-A.
---
## Module: News Data — Numerical Features
**Notebook:** `Numerical Features.ipynb`
### Prerequisites
- News data fields: sentiment_score, sentiment_class, relevance, novelty; market open/close logic
### Concepts
- **News feature set (numerical):** `time`, `headline`, `asset_name`, `sentiment_score` (VADER), `sentiment_class` (1/−1/0), `category`, `relevance` (1 if asset named), `novelty` (repeat count).
- **Combine scores:** `feature_score = (sentiment_class × relevance) / (1 + novelty)` — penalizes repeated (low novelty) news.
- **Time-of-day alignment (`get_trade_open`):** assign each headline to the market open when it would be tradeable — headlines between prev close and today open → today's open; between today close and tomorrow open → next open; **headlines during market hours are ignored** (`BDay` offsets handle weekend/business-day boundaries).
- **Daily aggregation:** `groupby('date').feature_score.mean()` produces a single daily numeric feature per asset.
---
## Module: News Data — Categorical Features
**Notebook:** `Aggregating Categorical Features.ipynb`
### Prerequisites
- **Categorical attributes** (no inherent order, e.g., news category); one-hot encoding
### Concepts
- **One-hot encoding:** `pd.get_dummies(category)` creates one binary column per category (business, health, sports, technology); exactly one is "hot" (1) per row; join with original, drop the category column.
- **Why one-hot:** numeric values are needed for ML without imposing an order on unordered labels.
- **Daily aggregation of binary features:**
 - **Mean:** average of binary columns per `(asset_name, date)` — but repeated news gets undue weight.
 - **Logical OR:** `groupby().sum()` then clip ≥1 → 1; a day with at least one item of a category gets 1 — preferred to avoid overweight from repeated news.
---
## Module: Data Labelling for Better Outcomes
**Notebooks:** `The Fixed-Time Horizon Method.ipynb`, `The Triple Barrier Method.ipynb`
### Prerequisites
- **Labeling** — mapping feature windows to positional labels for supervised learning
- Feature window (N bars) vs label window/horizon (M bars); look-ahead avoidance
### Concepts (Fixed-Time Horizon)
- **FDV**; **Fixed-time-horizon labeling:** label by the return at the end of the label window (M bars after the feature window).
- **Static threshold:** `fut_returns = Adj Close.pct_change(M).shift(-M)`; label 1 if > threshold, −1 if < −threshold, else 0.
- **Dynamic threshold:** threshold = `0.125·sqrt(feature_window)·rolling(feature_window).std()` of daily returns — produces a **balanced** label distribution (avoids class imbalance).
- **Limitation:** ignores the path price takes inside the label window — a crash-then-recover could wrongly label +1 (fixed horizon would mislabel what a stop-loss hit).
- **Multi-stock extension:** loop over a list of price dataframes.
### Concepts (Triple Barrier)
- **Path-aware labeling:** real traders care about what happens *during* the period (profit goals, stop losses), not just the end — the path matters.
- **Three barriers:** upper horizontal (profit-taking), lower horizontal (stop-loss), vertical (end of period). Label = which barrier is touched **first**
 - upper barrier first → +1 (buy); lower barrier first → −1 (sell); only the vertical barrier within M → 0 (no position).
- **`triple_barrier_target_class`:** iterate over cumulative returns of the label window vs `±threshold`; set label by first breach.
- **Barriers may be asymmetric/dynamic (volatility-scaled)** — fixed/symmetric used for illustration.
---
## Module: Fundamental Data — Merge Them Correctly
**Notebooks:** `Sharadar Data.ipynb`, `Wall Street Horizon Data.ipynb`
### Prerequisites
- **Fundamental data** (SEC filings: 10-K/10-Q/8-K); event-date semantics; look-ahead bias
### Concepts (Sharadar Data)
- **Sharadar SF1 data (from Quandl/SEC EDGAR):**
 - **Indicators:** field dictionary (317 indicators, e.g., revenue, cor, sgna, rnd, opex).
 - **Tickers:** company info (ticker, name, exchange, sector, location, `isdelisted`, first/last price dates).
 - **Earnings data:** EPS, revenue, net income, EBIT per report.
- **Dimension views:** `ARQ/MRQ` quarterly, `ARY/MRY` annual, `ART/MRT` trailing-12-mo; AR = excluding restatements, MR = including restatements.
- **Look-ahead bias avoidance:** use **AR** (as-reported, excluding restatements) — the `datekey` is the SEC filing date, the first moment the data was knowable; avoid MR restatements in backtests.
### Concepts (Wall Street Horizon Data)
- **Why WSH:** Sharadar provides filing dates, but the actual **earnings announcement date** (press release) comes earlier; WSH supplies upcoming announcement dates (available via Interactive Brokers ~$30/mo, XML feed).
- **WSH XML structure:** per company: Name, Ticker, ISIN, Exchange, EarningsList entries (TimeStamp, Period, Etype e.g. Confirmed/Unconfirmed, Time Before/After Market, quarter dates).
- **Extracted dataframe (`earnings_announcement_wsh.bz2`):** `file_date`, `company_names`, `next_ed` (next earnings date), `next_ed_quarter`, `stock_exchange`, `stock_symbol`, `time_of_day`, `timestamp`.
- Combining Sharadar earnings + WSH announcement dates lets you merge fundamental data to the correct event (announcement) date without look-ahead bias.
---
## Cross-cutting prerequisite lenses
- **Bar construction chain:** tick data → time/tick/volume/dollar bars → information/imbalance bars → feature extraction.
- **Feature/statistics prerequisites:** stationarity & ADF → fractional differentiation (Why Stationary Features).
- **Dataset-quality hygiene:** EDA (OHLCV/pickle) → outliers → survivorship/delisted → redundant duplicates → multiple stock classes.
- **Alt-data feature engineering:** news numerical → news categorical/one-hot.
- **Supervised target setup:** fixed-time-horizon labeling → triple-barrier (path-aware) labeling.
- **Fundamental merge:** Sharadar indicators/tickers/earnings → Wall Street Horizon announcement dates → merge without look-ahead bias.
---
## Data-and-Feature-Engineering-for-Trading — Section-based course structure
# — Data & Feature Engineering for Trading — Concept Inventory
**Track:** 4 — Machine Learning & Deep Learning in Trading (Beginners)
**Media note:** This course ships only PDFs + a resources zip (no mp4 video files present); sub-topics derived from PDF prerequisites and section titles.
**Overlap with D: notebooks:** Yes — the D: side carries an expanded notebook-based version (`Data-Feature-Engineering-for-Trading` extraction) covering OHLCV EDA, time/tick/volume/dollar bars, imbalance bars, and triple-barrier labelling in `.ipynb` form. The PDFs here cover the prerequisite/threshold concepts (futures roll mechanics, calendar spreads, run bars) rather than the notebook implementations.
## COURSE
Data-centric preparation for applying machine learning to financial data: recognising and avoiding look-ahead / deceptive-return bias, the futures and roll-return machinery behind minutely or tick-derived signals, and information/imbalance bars that sample on informational content rather than price/volume/dollar buckets.
## Course Prerequisite Map
- **Section 12 requires:** futures contract / roll-return mechanics (supplied as its own prerequisite PDF) + calendar-spread (market-neutral) basics.
- **Section 14 requires:** bar construction concepts (time/tick/volume/dollar), trade-direction/tick-rule ideas, EWMA estimators. The accompanying reading assumes familiarity with Lopez de Prado's run-bar/imbalance-bar definitions.
- **Section 18 (Summary)** is a resources wrap-up; no new prereqs.
---
### Section 12 — Look-ahead Bias: Deceptive Returns
- **CONCEPT:** Look-ahead bias — using future information (e.g., future returns, final settle values, or index membership) that would not have been known at decision time, inflating/obscuring true strategy performance. "Deceptive returns" result when such leakage is unnoticed. prereqs: data hygiene, backtesting awareness.
- **CONCEPT:** Futures contract — legal agreement to buy/sell a specific asset at a set price on a future date; standardized, exchange-traded, default risk removed by clearing house; traded on initial margin (10–20% of contract value) plus maintenance margin as a volatility/Value-at-Risk cushion. prereqs: trading basics, margin/leverage.
- **CONCEPT:** Spot vs Settlement vs Last Traded price — intraday data conventions: spot = current/negotiated price, settlement = price used for final cash transfer, last traded price (LTP) = most recent executed price; matters for correctly aligning price series to signal time. prereqs: futures contract.
- **CONCEPT:** Roll returns — the return earned when a futures position is rolled into the next-scheduled contract as the current one approaches expiry; introduces price discontinuities and a data second bias if not handled correctly. prereqs: futures contract, contract expiry calendar.
- **CONCEPT:** Calendar spread strategy (prereq reading) — a market-neutral strategy: simultaneously long one future and short another of the same underlying but different expiry (near-vs-long legs), insulated from market direction; useful in volatile, direction-uncertain regimes. prereqs: futures contract, option/long-short legs.
### Section 14 — Information Bars: Market Order Imbalances
- **CONCEPT:** Information bars — bars sampled by informational content rather than fixed time/volume/dollar buckets. "Run bars" / **imbalance bars** trigger on the cumulated **buy-vs-sell order imbalance** (effects the signed balance of informed orders) rather than price movement. prereqs: bar construction, trade-direction inference.
- **CONCEPT:** A run-bar balance — anomaly of trade-direction imbalance accumulation; imbalance is a proxy for informed/accelerated trading activity. prereqs: tick-rule / order clustering.
- **CONCEPT:** Additional reading points to Marcos Lopez de Prado, *Advances in Financial Machine Learning*, ch. 2 for run/associated bars. prereqs: bar-taxonomy, statistical sampling.
### Section 18 — Summary
- **CONCEPT:** Course resources — downloadable data + notebooks (`Data-Feature-Engineering-for-Trading-Resources.zip`) consolidating the bar/feature workflow. prereqs: all sections.


====================
Decision-Trees-in-Trading
====================

# Decision Trees in Trading — Concept Inventory
**Totals:** 6 modules, 12 notebooks
Supervised learning applied to trading: building tree-based models (regression and classification trees) that extract trading rules from price data, then layering in ensemble methods (bagging, random subspace, random forest, boosting) to control overfitting, followed by model evaluation (cross-validation, hyperparameter tuning) and a live-trading simulation with model retraining.
---
## Module: Regression Trees
**Notebooks:** `Regression Tree Model.ipynb`, `Strategy Analytics.ipynb`
### Prerequisites to this module
- OHLV / adjusted close price data (Open, High, Low, Close, Volume, adjusted prices)
- One-day / multi-day returns (percent change) and rolling standard deviation as features
- Concept of a target variable forecast one day ahead (shifted future return)
- Train/test split of time-series data
- **Regression trees** — a supervised model that auto-selects important predictors and splits data into leaves, each leaf predicting a value (expected return) used to define trading rules
- Strategy performance metrics: **Sharpe ratio** and **CAGR** (compounded annual growth rate)
### Concepts
- **Predictor engineering from OHLCV:** rolling returns (ret1, ret5, ret10, ret20, ret40 via `pct_change()` + `rolling().sum()`) and rolling standard deviations (std5, std10, std20, std40) as input features; volume as an additional predictor.
- **Target: one-day future return** — `retFut1 = ret1.shift(-1)` forecasts the next day's return.
- **Train/test split:** first 80% train, last 20% test to validate on unseen data while preserving temporal order.
- **Regression tree model (`DecisionTreeRegressor`):** `min_samples_leaf=400` to avoid overfitting (leaf should not be too small); `fit()` on train.
- **Tree visualization:** `sklearn.tree.export_graphviz` + graphviz to inspect splits, feature importance, and leaf expected values.
- **Trading rule from single leaf:** pick the leaf with the highest expected return and map its split conditions (e.g., `ret5 > 0.0014 AND std5 > 0.0155` ⇒ buy/1 else hold/0).
- **Trading rule from full tree:** use **all** leaves — predict expected return for every point (`dtr.predict(X) > 0` ⇒ +1 buy, else −1 sell) and multiply future returns by signal for strategy returns.
- **Performance evaluation:** annualized Sharpe ratio (`sqrt(252) * mean/std` of excess returns over risk-free ~5% p.a. / 252) and CAGR (`(cumprod)^(252/days) − 1`).
- **Comparison:** single-leaf vs full-tree rules on train and test; cumulative return plots.
### Pre-requisite concepts
Decision trees; returns and rolling statistics; supervised regression; Sharpe ratio; CAGR; train/test split.
---
## Module 2: Classification Model
**Notebooks:** `Classification Decision Tree Model.ipynb`, `Class Weights In Decision Trees.ipynb`
### Prerequisites to include classification
- **Classification trees** — predict a discrete label (direction of next-day return) instead of a continuous value
- **Technical indicators** via TA-Lib: **ADX** (Average Directional Index), **RSI** (Relative Strength Index), **SMA** (Simple Moving Average)
- **Labeling returns** into classes (binary 0/1, or multi-class buckets)
- **Gini impurity** as the split criterion
- **Class imbalance** and re-weighting
### Concepts (Classification Decision Tree Model.ipynb)
- **Classification tree setup:** `DecisionTreeClassifier(criterion='gini', max_depth=3, min_samples_leaf=5)` predicting binary next-day direction.
- **Feature set:** ADX, RSI, SMA (14- and 20-period windows) from TA-Lib.
- **Binary target labeling:** `np.where(Return > 0, 1, 0)` — 1 for positive next-day return, 0 otherwise.
- **Split & train/test:** 80/20 split; fit on train.
- **Visualizing the tree:** each node shows split feature, gini value, `samples`, and per-class `value` counts; a leaf path (e.g., RSI ≤ 55.868, SMA bands) yields a pure node usable as a long (buy) rule.
- **Predictions:** `clf.predict(X_test)`.
- **Classification metrics:** precision, recall, F1-score, support from `classification_report`; F1 is harmonic mean of precision & recall; values above ~0.5 considered good.
- **Backtest strategy:** multiply lagged signal by close `pct_change()` for strategy returns; plot cumulative product for out-of-sample performance.
### Concepts (Class Weights In Decision Trees.ipynb)
- **Class imbalance problem:** when one class dominates, the tree maximizes accuracy on common labels and ignores rare/important classes.
- **Multi-class labeling:** `returns_to_class()` buckets returns by range (≤0 → 0; 0–0.02 → 1; 0.02–0.03 → 2; else 3) creating a skewed distribution.
- **Unweighted model baseline:** `classification_report` shows near-zero precision/recall on underrepresented classes (2, 3).
- **Class weight rebalancing:** `class_weight='balanced'` re-weights so classes appear with equal frequency, trading overall accuracy for better coverage of rare classes; note the tradeoff (a previously good model may look worse overall).
### Prebuiltin concepts
Decision trees; classification; technical indicators (RSI, SMA, ADX); labeling; class imbalance / imbalanced data; precision/recall/F1.
---
## Module: Cross Validation and Hyperparameter Tuning
**Notebooks:** `K-Fold Cross Validation.ipynb`, `Hyperparameter Tuning.ipynb`
### Prerequisites
- **Random forest** model
- **Cross-validation** — estimate performance from multiple train-validation splits
- **Hyperparameters** — model settings set before training (cannot be learned)
- **Grid / random search** over hyperparameter space
### Concepts (K-Fold Cross Validation.ipynb)
- **Cross-validation rationale:** evaluate model on multiple train/validation splits for a more reliable performance estimate than a single split.
- **KFold** (`sklearn.model_selection`): `n_splits` (number of folds, ≥2) and `shuffle` (pre-shuffle ordering); splits data into k consecutive train/test sets.
- **cross_val_score:** accepts estimator, X, y, cv; returns an array of per-fold scores (e.g., 5 accuracy scores for a random forest classifier).
- **Summarizing:** mean ± standard deviation of fold scores as the model's robustness measure (e.g., "Accuracy: 53.14% ± 1.95%").
### Concepts (Hyperparameter Tuning.ipynb)
- **Hyperparameters of a random forest:** `n_estimators`, `max_features`, `max_depth`, `min_samples_leaf`, `bootstrap`.
- **Parameter grid:** dictionary of hyperparameter names → value ranges (n_estimators 10–20; max_features 0.3–1.0; max_depth 2–10; min_samples_leaf 300–600; bootstrap True/False).
- **RandomizedSearchCV:** samples `n_iter` parameter combinations at random, tuned with CV; `.best_params_`, `.best_estimator_`.
- **GridSearchCV:** exhaustively tries all combinations (more thorough but slower); `.best_params_`.
- **Bias/variance tradeoff:** smaller `max_features` reduces variance (overfit) but increases bias (underfit); larger `n_estimators` improves until a critical point.
### Prebuiltins
Ensembles (random forest); cross-validation; hyperparameter optimization; bias-variance tradeoff.
---
## Module: Parallel Ensemble Methods
**Notebooks:** `Bagging Model.ipynb`, `Random Subspace Model.ipynb`, `Random Forest Model.ipynb`
### Prerequisites
- **Ensembles** — combine multiple models to reduce variance/overfitting
- **Regression trees** as the base estimator
- **Bootstrap sampling** (with replacement)
### Concepts
- **Bagging (Bootstrap Aggregating):** create 'N' random subsets **with replacement** from training data, fit one model per subset, and combine by averaging (regression) or majority voting (classification); reduce variance/overfit of a single tree. Implemented with `BaggingRegressor(estimator=DecisionTreeRegressor, n_estimators, random_state=)return`.
- **Random Subspace (attribute/feature bagging):** sample the **predictors** (with replacement) instead of the data rows; via `BaggingRegressor(bootstrap=False, bootstrap_features=True, max_features=0.7)` — offers diversity across feature subsets.
- **Random Forest:** hybrid of bagging + random subspace — bootstrap-sample rows **and** randomly select a predictor subset at each split; average or majority-vote all trees. `RandomForestRegressor(n_estimators=20, bootstrap=True, max_features=0.6, min_samples_leaf=400, random_state=42)`.
- **Parameter intuition:** `n_estimators` (higher = better up to a critical point), `max_features` (smaller reduces variance but risks bias), `min_samples_leaf` guards against tiny leaves/overfit.
### Prebuiltins
Ensembles; bagging; random subspace; random forests; bias–variance.
---
## Sequential Ensemble Modules (Boosting)
**Notebooks:** `AdaBoosting Model.ipynb`, `Gradient Boosting Model.ipynb`
### Prerequisites (Boosting)
- **Boosting** / sequential ensembles — models added sequentially that each correct the previous model's mistakes
- **Adaptive Boosting** (AdaBoost, Freund & Schapire 1996)
- **Gradient boosting** (Friedman) — additive models following gradient descent on loss
### Concepts
- **AdaBoost naming & idea:** adaptive; builds a sequence where each model improves its predecessor; add models until all train data are correct or a max model count is reached.
- **AdaBoostRegressor** implementation: `AdaBoostRegressor(estimator=DecisionTreeRegressor(min_samples_leaf=400), n_estimators=4, random_state=42)`.
- **Gradient Boosting:** extension of AdaBoost by Friedman; each added model reduces the loss, following gradient descent on the residual.
- **GradientBoostingRegressor:** `GradientBoostingRegressor(n_estimators=4, random_state=42)`.
- **Comparison practice:** import data, define features/target, train/test split, compute strategy returns, compare across all models.
### Covered outcome
Boosting sequential ensembles reduce overfit so that **all leaves** can be used for prediction (contrast with single-tree full-leaves fear of overfit).
---
## Module: Challenges in Live Trading
**Notebook:** `Trading Simulation Using Decision Trees.ipynb`
### Prerequisites
- **Random forest classifier** (balanced class weights)
- **Feature generation** from OHLCV returns/rolling stats
- **Model persistence:** pickle save/load
- **Simulation / walk-forward trading** — point-by-point, rolling re-fit of the model, monitoring performance
- **Data leakage avoidance** — never let future data leak into features
### Concepts
- **Data & libraries:** BAC.csv daily data; pandas, sklearn RandomForestClassifier, pickle, accuracy_score, matplotlib.
- **Feature generation as a function:** `create_features(data)` builds return (ret1/3/5/10/20) and rolling std (std3/5/10/20) features, drops NaNs, constructs future returns `retFut1`, and returns predictor matrix X and target y (class 1/−1 for up/down).
- **Simulation parameters:** `simulation_length` (trading horizon), `minimum_feature_length` (rows needed to form a full feature row), `performance_length` (rows over which past performance is checked).
- **Train/simulation split:** reserve enough prior rows so features and performance checks are free of data leakage.
- **Train, save, load, retrain functions:** `train_model(X,y)` returns an `RandomForestClassifier(n_estimators=200, class_weight='balanced')`; `save_model` / `load_model` via pickle (model_save.pkl); `create_new_model` reuses feature + trainTransform + save.
- **Walk-forward simulation loop:** for each iteration, load past window; compute features; load model; predict; check rolling accuracy over `performance_length` (threshold ~0.55), then
 - good performance → use today's "Buy"/"Sell" signal;
 - poor performance → do NOT trade (append 0), roll the train set forward and **retrain** (create_new_model).
- **Simulated performance:** multiply signals by future returns; plot cumulative product (`np.nancumprod`) to view P&L.
### Prebuiltins
Random forests; classification; feature engineering; cross-validation; simulation; model persistence.
---
## Cross-cutting prerequisite links (recommendations)
- Before **Regression Trees**: OHLCV data, returns/rolling std, Sharpe/CAGR.
- Before **Classification**: regression-trees module; technical indicators; labeling of direction.
- Before **Class Weights**: classification, unbalanced data, classification metrics.
- Before **Cross Validation / Tuning**: random forest.
- Before **Ensiebles**: regression trees, overfitting.
- Before **Boosting**: ensembles, overfitting via all-leaves rule.
- Before **Live Trading**: all tree + ensemble + tuning concepts and pickle persistence.
---
## Decision-Trees-in-Trading — Section-based course structure
# — Decision Trees in Trading — Concept Inventory
**Track:** 4 — Machine Learning & Deep Learning in Trading (Beginners)
**Media note:** PDFs + a downloadable code zip only (no mp4s in this course folder).
**Overlap with D: notebooks:** The D: side has notebook-based decision-tree content (splitting criteria, tree visualisation, hyperparameter search in `.ipynb`); here the PDFs supply the underlying loss functions, ensemble math, and installation/verification steps.
## COURSE
Building decision-tree models for trading: how trees partition feature space via splitting, stopping and pruning; training classification trees; combining trees sequentially into ensembles (boosting, specifically AdaBoost); and tuning/generalising trees via cross-validation and hyperparameter selection.
## Course Prerequisite Map
- **Section 2 requires:** basics of supervised classification/regression, overfitting bias-variance intuition.
- **Section 3 requires:** slicing/decision-tree logic + a Python environment for tree visualisation.
- **Section 8 requires:** Section 2 (weighted splitting) + idea that a tree can be fit on a weighted random subsample (bootstrapping/boosting intuition).
- **Section 9 requires:** Sections 2 & 3 (a trained tree + a labelled dataset to fold/split). Prereqs for Section 9 also intersect with metrics (gini/entropy, confusion matrix) used to score CV folds.
---
### Section 2 — Splitting, Stopping and Pruning Methods
- **CONCEPT:** Loss function — a metric evaluating how well a trained ML algorithm generalises to unseen data; small loss = viable model, and it drives fine-tuning of model. prereqs: ML train/test split, supervised learning.
- **CONCEPT:** Tree splitting loss for classification — **gini impurity** and **entropy** (both distribution-purity measures) chosen as split criteria for classification trees. prereqs: probability/distribution basics, tree structure.
- **CONCEPT:** Tree-splitting loss for regression — **mean squared error (MSE)** and **mean absolute error (MAE)** as node-impurity/cost criteria for regression trees; custom loss functions also possible. prereqs: regression error metrics, node prediction.
- **CONCEPT:** Splitting — recursively choosing the feature split that most reduces impurity/loss at each node. prereqs: loss functions above.
- **CONCEPT:** Stopping/pruning — early depth/leaf thresholds or post-hoc pruning to prevent overfitting (too-deep trees memorising noise). prereqs: bias-variance trade-off, overfitting.
### Section 3 — Classification Model
- **CONCEPT:** Classification decision-tree model — recursively partitioned data into pure classes; predictions produced by following splits to a leaf (majority/class confidence). Built on the gini/entropy criteria from Section 2. prereqs: Section 2, classification labels.
- **CONCEPT:** Visualising the tree in Python — `pip install graphviz` (fallback `pip install python-graphviz`) and `pydot` to render the trained tree; alternative planners packages (Box3d, Gephi). Gives sharers introspective clarity on the final tree structure. prereqs: a trained model, Python env.
### Section 8 — Sequential Ensemble Methods
- **CONCEPT:** Sequential/boosting ensembles — combine sheaves of weak tree learners sequentially, each new tree corrects the mistakes of previous ones; AdaBoost is the canonical example. prereqs: decision tree, weighted-sample sampling.
- **CONCEPT:** AdaBoost math — (1) initialise all n training items with equal weight W_i = 1/n; (2) draw a random subsets with replacement (sample weights = selection probabilities); (3) fit a weak tree on that subset; (4) re-raise weights of misclassified items (formula doubles down on errors) so the next learner focuses on them, improving the ensemble over iterations. prereqs: sampling with replacement, weighted loss, sequential fitting.
- **CONCEPT:** Ensemble learning is a foundation concept progressively feeding into gradient boosting models used in gradient-boosting/DNN trading strategies later. prereqs: Section 2 splitting/entropy + Section 3 classification.
### Section 9 — Cross Validation and Hyperparameter Tuning
- **CONCEPT:** Cross-validation (k-fold) — splitting the dataset into k folds, training k times (each fold held out once) and averaging performance → robust generalisation estimates of a trading model. prereqs: evaluation metrics, data partitioning, confusion matrix (to threshold misclassification).
- **CONCEPT:** x-tables/hyperparameter tuning — selecting tree depth, min-split, max-features, etc. using CV score as the selection signal rather than a single train/test split. prereqs: Section 8 (ensemble) + Section 2 loss.
- **CONCEPT:** Confusion matrix helps judge a CV-selected classifier beyond accuracy (TPR/FPR, precision for trading). prereqs: Section 2, prediction outputs.
### Section 12 — Downloadable Code
- **CONCEPT:** Course code/resources (`DTResources.zip`) — the decision-tree notebook(s) and data for reproducing the splitting/ensemble/CV workflow locally. prereqs: all prior sections.


====================
Deep-Reinforcement-Learning-in-Trading
====================

# Deep Reinforcement Learning in Trading — Concept Inventory
## COURSE: Deep Reinforcement Learning in Trading
---
## MODULE: Initialise Game Class
### LESSON: Initialise Game Class
- **Gamification of trading:** Treating each individual trade as a game with a start, play period, and end; the RL agent plays these games. prereqs: reinforcement learning, trading.
- **Game class:** The environment the agent explores; generates input features, assembles states, updates positions, and computes rewards. prereqs: RL environment, OOP.
- **OHLCV data:** Open, High, Low, Close, Volume price bars; here 5-minute data from a compressed pickle file. prereqs: market data.
- **read_pickle():** pandas method to read a (compressed) pickle file, e.g. `PriceData5m.bz2`. prereqs: pandas, serialization.
- **Resample / agg():** Converting high-frequency data to lower frequency (5m → 1h → 1d) using `resample(freq, label, closed).agg(ohlcv_dict)`. prereqs: pandas, time series.
- **ohlcv_dict aggregation:** Mapping open→first, high→max, low→min, close→last, volume→sum when resampling. prereqs: resampling, OHLCV.
- **label / closed parameters:** `label` chooses which side labels the interval; `closed` sets interval inequality (left=(start,end], right=[start,end)). prereqs: resampling.
- **reset():** Resets all state values to defaults when a trade game is over, before starting a new game. prereqs: Game class, RL episode.
### LESSON: Working With Pickle File
- **Pickle file (.bz2):** Python serialization format; retains column datatypes (e.g. DatetimeIndex) unlike CSV. prereqs: serialization, pandas.
- **bz2 compression:** Compressed pickle format for smaller file sizes. prereqs: serialization.
- **to_pickle() / read_pickle():** pandas methods to save/load dataframes as pickle files. prereqs: pandas, serialization.
- **Python-version compatibility:** Pickle files are Python-version-specific and backward compatible; version mismatches cause errors. prereqs: serialization.
- **Common pickle errors:** `AttributeError: Can't get attribute '_unpickle_block'` (pandas version mismatch) and `ValueError: unsupported pickle protocol: 4` (older Python). prereqs: serialization, debugging.
---
## MODULE: Construct and Assemble State
### LESSON: Minute Price Data and Resampling Techniques
- **Minute-level data:** Higher-granularity price data (1m, 5m) used to test strategies; you can resample high→low frequency but not the reverse. prereqs: market data, time series.
- **yfinance download():** Downloads minute data (e.g. `period="5d", interval="1m"`); minute data limited to ~7 days. prereqs: data acquisition.
- **Resample to custom frequency:** Using `resample('15T'/'1H'/'4H').agg(ohlcv_dict)` to build 15-min, 1-hour, 4-hour candles from minute data. prereqs: resampling, OHLCV.
### LESSON: Get Last N Time Bars
- **Lookback period (lkbk):** Number of past bars (N) used to build input features; a hyperparameter. prereqs: time series, hyperparameters.
- **get_last_N_timebars():** Function returning the last N bars for 5m, 1h, and 1d resolutions before the current time. prereqs: time series, pandas slicing.
- **Window width (wdw):** Time interval (in days) pulled before the current time to ensure enough bars; e.g. wdw5m=9, wdw1h=ceil(lkbk*15/24), wdw1d=ceil(lkbk*15). prereqs: time series.
- **assert keyword:** Tests a condition (e.g. bar length == lookback) and raises an exception if false. prereqs: Python, debugging.
- **np.ceil():** Returns the smallest integer not less than x; used to widen time windows. prereqs: numpy.
### LESSON: Assemble States
- **State (RL):** The input feature vector the agent observes; passed to the neural network to predict an action. prereqs: RL, feature engineering.
- **State construction:** Building the state from (1) stationary candlestick bars, (2) technical indicators, (3) time signature, (4) position. prereqs: RL, feature engineering.
- **Flatten():** Converting a dataframe to a 1-D array (neural networks prefer array input). prereqs: numpy.
- **Stationary candlestick bars:** Candlesticks are non-stationary; z-scoring them (bar - mean)/std makes them stationary, which NNs prefer. prereqs: stationarity, normalization.
- **Z-score:** (value - mean)/standard deviation; used to normalize candlestick bars. prereqs: statistics, normalization.
- **Technical indicators (TA-Lib):** Features computed from price bars; here relative difference of two SMAs, RSI, Momentum, Balance of Power (BOP), and Aroon Oscillator. prereqs: technical analysis.
- **Relative Strength Index (RSI):** Momentum oscillator measuring speed/change of price moves. prereqs: technical indicators.
- **Momentum (MOM):** Rate of change of price. prereqs: technical indicators.
- **Balance of Power (BOP):** Indicator measuring the strength of buyers vs sellers. prereqs: technical indicators.
- **Aroon Oscillator:** Indicator measuring trend strength/direction. prereqs: technical indicators.
- **Time signature:** Time-of-day (hours*60+minutes)/(24*60) and day-of-week (weekday()/6), normalized, added to the state. prereqs: feature engineering.
- **Position feature:** Current position (long/short/flat) appended to the state. prereqs: RL, trading.
- **State size:** 120 (normalized candlesticks) + 15 (5 indicators × 3 granularities) + 3 (time, day, position) = 138 features. prereqs: feature engineering.
---
## MODULE: Positions and Rewards
### LESSON: Update the Positions
- **update_position():** Updates the trading position in response to the action suggested by the neural network. prereqs: RL, trading.
- **Actions (buy/sell/hold):** Action 0 = hold/do nothing, action 2 = buy (enter long / exit short), action 1 = sell (enter short / exit long). prereqs: RL, trading.
- **Position update rules:** Do nothing if action matches current position or is hold; open a new position if flat; close the position (game over) if action is opposite to current position. prereqs: RL, trading.
- **Game over:** When a position is closed by an opposite action, the trade game ends. prereqs: RL episode.
### LESSON: Reward System
- **Reward function:** Defines the scalar reward the agent receives; design significantly impacts algorithm performance. prereqs: RL, reward design.
- **get_pnl():** Percentage PnL = (curr*(1-tc) - entry*(1+tc))/entry*(1+tc)*position, incorporating transaction cost/commissions (tc=0.001). prereqs: trading, PnL.
- **Transaction cost / commissions:** Costs deducted from PnL; configurable to match local markets/brokers. prereqs: trading costs.
- **Slippage:** Difference between expected and executed price; noted but not included to avoid complexity. prereqs: trading costs.
- **reward_pure_pnl:** Returns the raw percentage PnL. prereqs: reward design.
- **reward_positive_pnl:** Returns PnL only when positive, else 0 (positive reinforcement only). prereqs: reward design.
- **reward_pos_log_pnl:** For positive PnL returns ceil(log(pnl*100+1)), else 0; compresses large gains. prereqs: reward design, log transform.
- **np.ceil():** Smallest integer not less than x. prereqs: numpy.
- **reward_categorical_pnl:** Returns sign of PnL (+1 win, -1 loss). prereqs: reward design.
- **reward_positive_categorical_pnl:** Returns 1 for win, 0 for loss; suited to long-only strategies. prereqs: reward design.
- **reward_exponential_pnl:** Returns exp(PnL); penalizes small PnL changes and rewards large gains exponentially (used in the algorithm). prereqs: reward design, exponential.
- **get_reward():** Computes reward only when the game is over; no reward mid-game. prereqs: reward design, RL.
- **Custom reward systems:** Reward can be based on Sharpe ratio, max drawdown, average return, etc., not just PnL. prereqs: reward design, performance metrics.
---
## MODULE: Game Class
### LESSON: Game Class
- **Game class (full):** Combines position updates, reward design, feature creation, and state assembly into the environment. prereqs: RL environment, OOP.
- **get_state():** Returns the assembled state (candlesticks, indicators, day of week, time of day, position). prereqs: RL, state.
- **act():** Takes an action from the neural network, updates the game, and returns (reward, game_over flag). prereqs: RL, environment.
- **Game over on opposite action:** Passing an action opposite to the current position ends the game and yields the reward. prereqs: RL, trading.
- **Agent as action source:** The neural network (agent) suggests actions; the Game class executes them. prereqs: RL, ANN.
---
## MODULE: Experience Replay
### LESSON: Experience Replay Implementation
- **Experience replay:** Mechanism where the agent stores past experiences and samples them to train the network, breaking correlation and stabilizing learning. prereqs: RL, DQN.
- **Memory / replay buffer:** A list storing experiences (state, action, reward, next state) up to a maximum size. prereqs: RL, DQN.
- **ExperienceReplay class:** Implements `init()` (buffer + max size), `remember()` (add experience, truncate oldest), and `process()` (build input states and target Q-values). prereqs: RL, DQN.
- **remember():** Appends [state_t, action, reward, state_tp1, game_over] to memory; deletes oldest when over max_memory. prereqs: RL, memory buffer.
- **process():** Randomly samples experiences (S.A.R.S: state, action, reward, next state) and computes target Q-values for training. prereqs: RL, DQN.
- **Target Q-value (Bellman update):** Q_new(s,a) = reward_t + discount * max_a' Q(s',a'); for terminal states target = reward_t. prereqs: RL, Bellman equation.
- **Discount rate (gamma):** Tradeoff between immediate reward and future Q-value of the next state (e.g. 0.99). prereqs: RL, Bellman equation.
- **Model R vs Model Q:** Model R provides current Q-values per action (target vector); Model Q provides the max Q-value of the next state. prereqs: DDQN.
- **train_on_batch():** Trains the Q-network on a batch of (inputs, targets) to reduce loss. prereqs: Keras, DQN.
---
## MODULE: Artificial Neural Network Implementation
### LESSON: ANN in Keras
- **Agent (RL):** The learner/decision-maker; in deep RL it is modeled with an Artificial Neural Network (ANN). prereqs: RL, ANN.
- **Double Deep Q-Learning (DDQN):** Uses two identical ANN agents (two Q-tables) trained on different samples to avoid value overestimation, stabilizing and speeding learning. prereqs: DQN, Q-learning.
- **Multi-layer perceptron (MLP):** Feedforward network; data passes once forward, error propagates backward (backpropagation). prereqs: neural network.
- **init_net():** Function defining two identical MLPs (modelR, modelQ) for DDQN. prereqs: Keras, DDQN.
- **ANN input/output dimensions:** Input = state dimension; output = number of actions (buy, sell, hold = 3). prereqs: ANN, RL.
- **Sequential + Dense layers:** Three dense layers (input, hidden, output) in a sequential model. prereqs: Keras, MLP.
- **Softmax output activation:** Converts action scores to a probability distribution over actions. prereqs: activation functions, classification.
- **SGD optimizer (stochastic gradient descent):** Optimizer used to update weights; learning rate controls step size. prereqs: gradient descent, optimization.
- **Learning rate:** Multiplier for gradient steps; how fast the optimizer reaches an optimum. prereqs: optimization, hyperparameters.
- **Loss function (mse):** Quantifies how far predictions are from ground truth. prereqs: loss functions.
- **Activation function (relu):** Adds non-linearity for fitting complex curves. prereqs: activation functions.
- **HIDDEN_MULT:** Multiplier determining hidden layer size relative to input size. prereqs: ANN architecture, hyperparameters.
- **NUM_ACTIONS:** Number of actions the agent can take (buy, sell, hold). prereqs: RL, actions.
- **BATCH_SIZE:** Number of samples trained on at a time. prereqs: training, hyperparameters.
- **Resampling to 1h/1d:** Building hourly and daily bars from 5m data for the multi-granularity state. prereqs: resampling.
- **LKBK (lookback):** Number of bars used as lookback for training. prereqs: time series, hyperparameters.
- **START_IDX:** Initial index of the dataset where the agent starts learning. prereqs: RL, training.
---
## MODULE: Backtesting Implementation
### LESSON: Backtesting Implementation
- **Episode:** Each iteration of exploring the environment (one trade game). prereqs: RL.
- **Epsilon (exploration vs exploitation):** Probability of taking a random action vs the optimal (max Q-value) action; decays over episodes. prereqs: RL, exploration.
- **Epsilon decay (exponential):** epsilon = EPSILON^(log10(episode)) + EPS_MIN, decreasing exploration over time. prereqs: RL, exploration.
- **EPSILON / EPS_MIN:** Initial and minimum epsilon values. prereqs: RL, hyperparameters.
- **MAX_MEM:** Maximum length of the experience replay buffer. prereqs: RL, memory buffer.
- **DISCOUNT_RATE:** Tradeoff between reward and next-state Q-value. prereqs: RL, Bellman equation.
- **run() function:** Trains the agent in the Game environment: initializes env + ANNs + replay buffer, loops over episodes/states, selects actions via epsilon, stores experiences, computes target Q-values, and trains the Q-network. prereqs: RL, DQN, backtesting.
- **Action selection:** If random <= epsilon, pick a random action; else argmax of Q-network prediction. prereqs: RL, exploration.
- **Experience storage:** Adding [state_t, action, reward, state_tp1] to the replay buffer each step. prereqs: RL, memory buffer.
- **Target Q-value computation:** Using modelR and modelQ to compute targets for sampled experiences. prereqs: DDQN, Bellman equation.
- **r_network.set_weights(q_network.get_weights()):** Syncing the R-network weights to the Q-network when a game ends (UPDATE_QR). prereqs: DDQN.
- **Trade logs:** Recording current time, position, and episode for each step. prereqs: backtesting, logging.
- **Saving weights / trade logs / replay buffer:** Periodically persisting model weights, trade logs, and memory to disk. prereqs: serialization, checkpointing.
- **TEST_MODE:** Flag to stop training after a few trades for resource constraints; set False for full runs. prereqs: RL, training.
- **PRELOAD:** Flag to load pre-trained weights and replay memory from disk. prereqs: RL, checkpointing.
---
## MODULE: Performance Analysis_ Synthetic Data
### LESSON: Synthetic Time Series Patterns
- **Synthetic OHLCV:** Simulated price data based on a base signal plus random noise, used to test the RL model. prereqs: simulation, market data.
- **create_synth_ohlc():** Builds synthetic open/high/low/close/volume from a wave `y` plus noise (mult * randn); high/low ~1 unit away; volume fixed at 1000. prereqs: simulation, numpy.
- **Mean-reverting (sine) time series:** Base signal y = 10*sin(0.005*x)+100; tests the model on a mean-reverting pattern. prereqs: mean reversion, simulation.
- **Trending time series:** Base signal y = 0.01*x+100; tests the model on a trending pattern. prereqs: trend, simulation.
- **Mixed time series:** First half sine wave, second half trending; tests regime-shift behavior. prereqs: simulation, regime change.
- **Noise multiplier (mult):** Controls the amount of random noise added to the synthetic signal. prereqs: simulation.
### LESSON: Apply RL on Synthetic Mixed Wave Pattern
- **Running RL on synthetic data:** Applying the run() function to the mixed wave pattern to train the agent and observe strategy performance. prereqs: RL, backtesting.
- **trade_analytics():** Function that joins trade logs with price data, computes strategy returns, cumulative returns, drawdown, and Sharpe ratio. prereqs: performance analysis.
- **Strategy returns:** percent_change * position.shift(1). prereqs: returns, trading.
- **Cumulative strategy returns:** (1 + strategy_returns).cumprod(). prereqs: returns.
- **RL learns sine better than trend:** The model learns the mean-reverting (sine) regime remarkably well but crashes when the regime shifts to trending. prereqs: RL, regime change.
- **Synthetic performance caveat:** Huge synthetic returns (e.g. 2.5×10^5%) are unlikely on real price data. prereqs: backtesting, realism.
---
## MODULE: Performance Analysis_ Real World Price Data
### LESSON: RL Model on Real World Price Data
- **Applying RL to real price data:** Running the RL model on actual 5-minute price data and analyzing strategy performance. prereqs: RL, backtesting.
- **rl_config hyperparameters:** LEARNING_RATE, LOSS_FUNCTION, ACTIVATION_FUN, NUM_ACTIONS, HIDDEN_MULT, DISCOUNT_RATE, LKBK, BATCH_SIZE, MAX_MEM, EPSILON, EPS_MIN, START_IDX. prereqs: RL, hyperparameters.
- **Performance analysis:** Plotting returns and drawdown and computing metrics via trade_analytics(). prereqs: performance analysis.
- **Drawdown metrics:** Percentage decline from running maximum of cumulative returns; max drawdown reported. prereqs: performance metrics.
- **Sharpe ratio (5-min bars):** mean/std * sqrt(252*78) since 5-minute time steps. prereqs: Sharpe ratio, risk.
- **Portfolio return:** Final cumulative strategy return minus 1. prereqs: returns.
- **Model robustness to crashes:** The RL model handles market crashes (2019 flat, 2020 drawdown recovery) reasonably well. prereqs: RL, risk.
---
## MODULE: Capstone Project
### LESSON: Model Solution Template_ Building the RL Model
- **Capstone RL model template:** A structured template to build a reinforcement learning model for the capstone project; must be calibrated per underlying asset. prereqs: RL, project workflow.
- **Data sanity check:** Checking for missing values and outliers; fixing data or obtaining good-quality data. prereqs: data quality.
- **Input features (extendable):** Statistical (beta of high/low), overlap studies (EMA instead of SMA), volatility (ATR), and other-asset data (On Balance Volume). prereqs: feature engineering, technical analysis.
- **Average True Range (ATR):** Volatility indicator measuring average true range of price. prereqs: technical indicators.
- **On Balance Volume (OBV):** Volume-based indicator. prereqs: technical indicators.
- **Reward function selection:** Choosing/creating a reward function based on the desired outcome. prereqs: reward design.
- **Recency sampling vs uniform random sampling:** Sampling the N most recent experiences from the buffer (recency) as a baseline vs uniform random sampling; used to assess the impact of experience replay. prereqs: experience replay, sampling.
- **Backtesting function (run):** The run() function trains the RL agent on historical data. prereqs: RL, backtesting.
### LESSON: Model Solution_ Combining the Agents
- **Combining RL agents:** Running the RL algorithm multiple times to obtain several agents, then building a strategy by allocating portfolio weights based on recent performance. prereqs: RL, portfolio construction.
- **Loading trained agents:** Reading each agent's trade logs and computing its strategy returns. prereqs: backtesting, serialization.
- **Agent selection:** Selecting agents on performance parameters (Sharpe, drawdown) or by return correlation (least correlated). prereqs: portfolio construction.
- **Rolling performance:** Computing positive rolling returns (window e.g. 30000 bars); negative returns set to 0 to avoid incorrect weight allocation. prereqs: performance analysis.
- **Weight allocation:** Portfolio weight = agent rolling return / sum of all agents' rolling returns; updated every N bars (e.g. 1500). prereqs: portfolio construction.
- **Strategy returns:** Sum over agents of (agent returns * weight.shift(1)). prereqs: portfolio construction.
- **pyfolio tear sheet:** Generating performance metrics with `pf.create_simple_tear_sheet()`. prereqs: performance analysis.
- **Combination benefit:** A combination of agents performs better overall than selecting a single best agent. prereqs: portfolio construction, diversification.
---
## MODULE: data_modules (supporting module)
- **Reward functions:** get_pnl, reward_pos_log_pnl, reward_pure_pnl, reward_positive_pnl, reward_categorical_pnl, reward_positive_categorical_pnl, reward_exponential_pnl. prereqs: reward design.
- **Game class (module):** Full environment with _update_position, _assemble_state, _get_last_N_timebars, _get_reward, get_state, act, reset. prereqs: RL environment, OOP.
- **_assemble_state():** Builds the state from normalized candlesticks (5m/1h/1d), technical indicators (SMA diff, RSI, MOM, BOP, Aroon), time signature, and position. prereqs: feature engineering, RL.
- **_get_last_N_timebars():** Gets last N bars for 5m/1h/1d resolutions based on lookback. prereqs: time series.
- **_get_reward():** Computes reward via the reward function only when the game is over. prereqs: reward design.
- **act():** Updates position, computes unrealized/realized PnL, and returns (reward, game_over). prereqs: RL, trading.
- **reset():** Resets game state and resamples bars for a new trade. prereqs: RL episode.
- **init_net():** Creates two identical MLPs (modelQ, modelR) for DDQN. prereqs: Keras, DDQN.
- **ExperienceReplay class:** remember() + process() implementing the replay buffer and Bellman target computation. prereqs: RL, DQN.
- **run():** Full training/backtesting loop over episodes with epsilon-greedy action selection and Q-network updates. prereqs: RL, DQN.
- **drawdown_metrics():** Computes and plots drawdown; returns max drawdown. prereqs: performance metrics.
- **trade_analytics():** Computes strategy returns, cumulative returns, drawdown, portfolio return, and Sharpe ratio from trade logs. prereqs: performance analysis.
---
## Deep-Reinforcement-Learning-in-Trading — Section-based course structure
# — Deep Reinforcement Learning in Trading — Concept Inventory
**Track:** 5 — Artificial Intelligence in Trading (Advanced)
**Media note:** PDFs + resource/template zips only (no mp4s in folder).
**Overlap with D: notebooks:** the D: side carries a notebook-based treatment of the same RL trading pipeline (agent scaffolding via ANN, replay buffer, backtesting, capstone); this course is organised as an narrative walkthrough (RL foundations → ANN → backtest → automate → paper/live → capstone).
## COURSE
Build an end-to-end deep-Q reinforcement-learning trading agent: model a trading problem as an MDP-like (state → action → reward) Q-learning loop, construct and assemble a state from price/indicator data, define trade positions and reward, replay experiences to stabilise learning, express the value function as an **artificial neural network (deep Q network)**, define backtesting logic (price, transaction cost, execution), then move to paper/live trading and a capstone that swaps in your own asset/minute data.
## Course Prerequisite Map
- **Section 1 Introduction:** none (course map). Strongly consume prior ML/classification & Python-of-ML track courses.
- **Section 4 Q Learning :** (no prereqs) — foundation for all subsequent RL sections.
- **Section 5 State construction requires:** Section 4 (state concept) + feature/indicator engineering.
- **Section 6 Policies requires:** Section 4; π(state)→action mapping, exploration vs exploitation.
- **Section 9 Positions & Rewards requires:** Sections 5–6 (how the agent acts) + PnL.
- **Section 11 Construct/Assemble State requires:** Sections 5 & 9 + `talib` (installed). Deepens the state vector with indicators and returns.
- **Section 13 Experience Replay requires:** Section 4/5 (transition tuples) + replay-buffer concept.
- **Section 14 ANN Concepts requires:** Section 13 (DQN needs a learning target) + neural-network basics (gradient descent).
- **Section 15 ANN Implementation requires:** Section 14 + Keras/TensorFlow env.
- **Section 16 Backtesting Logic requires:** Sections 9–15 (a trained policy + reward to replay) + trade-level the logic needed to be modelled.
- **Section 17 Backtesting Implementation requires:** Section 16 + the ANN agent/model files.
- **Section 19 Performance Analysis requires:** Sections 11–17 (real price data + model rollout).
- **Section 20 Automated Trading requires:** Section 19 (minute data) + IBridgePy/broker connect.
- **Section 21 Paper & Live Trading requires:** Section 20 + template.
- **Section 22 Capstone requires:** all of the above (project on your own asset/minute data).
- **Section 23 Future Enhancements & 25 Summary:** no new prereqs.
---
### Section 1 — Introduction
- **CONCEPT:** Course structure — the RL-agent pipeline from Q-learning foundations through ANN-based DQN, backtesting, automation, and live deployment. prereqs: none.
### Section 4 — Q Learning
- **CONCEPT:** Q-learning — model-free RL where an agent learns an action-value `Q(s,a)` (expected future return of taking action a in state s) and updates it toward the best next-state value; the backbone for DQN/A3C-style algorithms and DeepMind breakthroughs. prereqs: RL MDP vocabulary, state/action/reward.
- **CONCEPT:** Bellman update / temporal difference — the Q-value update target relating current estimate to reward + discounted next-state maximum. prereqs: Section 4 Q-table.
### Section 5 — State Construction
- **CONCEPT:** State — data the agent uses to decide action; must contain all info needed for prediction, simplified from the raw market stream. prereqs: Section 4 + features.
- **CONCEPT:** Why state quality matters — the behavioural-IRL cautionary frame (individual investors underperform; sell winners/hold losers) motivating engineered features. prereqs: trading behaviour awareness, Section 5.
### Section 6 — Policies in Reinforcement Learning
- **CONCEPT:** Policy π — the mapping from state to action the agent follows; RL balances **exploration** (trying new actions) vs **exploitation** (using the current best policy) — the core RL trade-off. prereqs: Section 4/5.
### Section 9 — Positions and Rewards
- **CONCEPT:** Reward design — the scalar feedback the agent optimises; for trading often a PnL/aware-shape; reward should align with profitable behaviour. prereqs: Section 5–6, PnL.
- **CONCEPT:** Volatility-scaled rewards — position scaled by market volatility to make reward more stable for continuous futures/FX. prereqs: Section 9 + volatility.
### Section 11 — Construct and Assemble State
- **CONCEPT:** Assembling the state vector — gather price/indicator (ta-lib: technical indicator library) features into the state fed to the agent. **pip install TA-Lib** (/windows/mac) prerequisite reading. prereqs: Section 5 state + indicator definitions.
### Section 13 — Experience Replay
- **CONCEPT:** Experience replay — store (state, action, reward, next-state) transitions in a replay buffer and sample batches uniformly for training, decoupling data correlation. prereqs: Q-learning/transition tuples.
- **CONCEPT:** Replay capacity/pro-portions — the replay ratio (learning updates vs experience collected) and buffer size must be tuned; too large a buffer can hurt DQN performance. prereqs: Section 13 + batch training.
### Section 14 — Artificial Neural Network Concepts
- **CONCEPT:** The ANN as a value function — represents the Q/mode value approximated across states; training via **gradient descent** on a loss between predicted and target Q. prereqs: neural net basics + gradients.
- **CONCEPT:** Gradient descent — the algorithm that minimises the network loss by stepping against gradients; why GD is central to training a DQN. prereqs: calculus (derivative, chain rule), forward/backprop.
### Section 15 — Artificial Neural Network Implementation
- **CONCEPT:** ANN agent implementation — build the Q-network in Keras/TensorFlow (versions 2.2.4 / 1.12.0 pinned); setup requires Visual Studio on Windows; two Q-tables/Double DQN of moving targets & maximisation bias mitigation. prereqs: Section 14 + TF/Keras env.
- **CONCEPT:** DQN vs Double-DQN boundary — using two Q-value tables (target/online) to reduce maximisation bias. prereqs: Section 15.
### Section 16 — Backtesting Logic
- **CONCEPT:** Backtesting logic — the model-priced simulation step: iterate bars sequentially, decide position via the agent (get prediction from ANN), apply costs, and carry the PnL. (PDF `Backtesting Logic.pdf` describes this loop.) prereqs: trained policy + state + reward.
### Section 17 — Backtesting Implementation
- **CONCEPT:** Backtest the trained agent on historical data — replay historical price bars, let the agent make position decisions, with sanity checks; produces `indicator_model.h5` (ANN weights) + `replay_buffer.bz2`. prereqs: Section 16 logic + Section 15 model.
### Section 19 — Performance Analysis (Real-World Price Data)
- **CONCEPT:** Model rollout on live/real price data — evaluate the trained DQN on minutely/real data; compare equity/CAGR vs buy-and-hold; discusses asset-appropriate and data-source FAQ. prereqs: Section 17 + minute data.
### Section 20 — Automated Trading Strategy
- **CONCEPT:** Automated execution of trades — connect to a broker (Trader Workstation for IBKR, IBroute Py), load the algorithm, stream live data, generate signals, place orders — the live execution flow. prereqs: trained model + broker account/IBridgePy.
- **CONCEPT:** IBridgePy / automated paper account practice — placing orders in a demo/paper/live Interactive Brokers (or TD Ameritrade/Robinhood) account. prereqs: broker setup.
### Section 21 — Paper and Live Trading
### Section 22 — Capstone Project
- **CONCEPT:** Capstone problem statement — build an advanced DRL model for your own asset (minute data; FX pair sample given); data sanity checks, add input features in `assemble_state`, train, download template/capstone solution `.zip`. prereqs: all prior.
### Section 23 — Future Enhancements
- **CONCEPT:** Future directions — deep RL for asset allocation; RL survey; reward-free exploration paving ways beyond this course. prereqs: capstone.
### Section 25 — Course Summary
- **CONCEPT:** Resources recap — the full `Deep-Reinforcement-Learning-in-Trading-Resources.zip` (RL env, time, template) bringing the pipeline together. prereqs: entire course.


====================
Event-Driven-Strategies
====================

# Event-Driven Strategies — Exhaustive Concept Inventory
## COURSE: Event-Driven Strategies (Calendar & Seasonal Trading)
## MODULE: Auction Trading Effect in Fixed Income
### LESSON: Treasury Auction Strategy (`Auction Trading Effect Code.ipynb`)
- **CONCEPT:** Calendar / seasonal trading strategy — a strategy that systematically holds a position only around recurring, publicly-known calendar events; often low risk because it stays in the market for only a short part of the year. prereqs: none
- **CONCEPT:** Treasury auction — periodic (roughly monthly) US government debt auctions, announced far in advance; despite being foreseeable, surrounding auctions influence secondary-market Treasury prices. prereqs: treasury market basics
- **CONCEPT:** Auction effect on prices — Treasury security prices tend to decline in pre-auction days and recover shortly after the auction, creating a mean-reverting opportunity around the event. prereqs: auction dates, price behaviour
- **CONCEPT:** TLT ETF — an exchange-traded fund tracking long-term US Treasuries, used here as the trading instrument. prereqs: ETF concept
- **CONCEPT:** Reading price data with pandas `read_csv` — loading a CSV of OHLC / adjusted-close data into a DataFrame and parsing the Date column into datetime. prereqs: pandas basics
- **CONCEPT:** Daily returns via `pct_change` — computing each day's fractional price change (Close.pct_change()) as the per-day strategy return. prereqs: percentage change
- **CONCEPT:** Business-day offset (`BDay`) — the pandas tseries business-day offset used to shift dates by a fixed number of business days; here to test whether yesterday or the day before was an auction date. prereqs: business-day calendar
- **CONCEPT:** Trading-signal generation (`np.where`) — conditionally assigning a signal value (1 = hold/long, 0 = no position) by checking date matches against known event dates. prereqs: numpy where, boolean masks
- **CONCEPT:** Strategy returns by signal weighting — multiplying each day's return by the signal so returns only accrue on active trading dates. prereqs: element-wise multiply, signals
- **CONCEPT:** Cumulative strategy returns (`cumprod`) — compounding daily strategy returns into a cumulative equity curve via (1 + r).cumprod(). prereqs: compounding
- **CONCEPT:** CAGR (Compound Annual Growth Rate) — annualised growth rate computed from cumulative returns over 252 trading days per year: (final)^(252/days) − 1. prereqs: growth rate, annualisation
- **CONCEPT:** Maximum drawdown — the largest peak-to-valley decline of the cumulative return curve, computed by dividing the curve by its running maximum and subtracting 1. prereqs: running maximum, cumulative returns
- **CONCEPT:** Plotting strategy returns & drawdown — visualising cumulative returns (matplotlib `plot`) and filling the drawdown area under the curve to inspect strategy health. prereqs: matplotlib basics
- **CONCEPT:** Performance summary — summarising strategy returns, CAGR, maximum drawdown, and CAGR/max-drawdown via a formatted table (tabulate) to compare strategy efficiency. prereqs: metrics, tabulate
## MODULE: Calendar Effect in Volatility Market
### LESSON: VIX Futures Expiration Strategy (`VIX Futures Expiration Strategy.ipynb`)
- **CONCEPT:** VIX futures expiration effect — a calendar anomaly in the volatility market: VIX futures expire monthly on well-known dates, and there is a pattern around those expirations that supports a simple strategy. prereqs: calendar anomaly
- **CONCEPT:** VIXY ETF — an exchange-traded fund tracking VIX short-term (1-month average maturity) futures contracts, with daily resets of exposure. prereqs: ETF concept, VIX futures
- **CONCEPT:** Short position on VIXY before expiry — taking a short position on VIXY for two trading days leading up to the VIX futures expiration date to profit from the expected price pattern. prereqs: short selling, calendar signal
- **CONCEPT:** Short signal encoding with `np.where` — assigning a −1 (short) signal value for the two days before expiration, and 0 otherwise. prereqs: numpy where
- **CONCEPT:** Date-shift signal matching — using `shift(-1)` and `shift(-2)` to flag dates that fall one/two days before a known expiration date. prereq: pandas shift
- **CONCEPT:** Daily returns & strategy returns — computing `pct_change()` daily returns, multiplying by the short signal (−1 flips the sign), and compounding the curve. prereqs: returns, signal multiplication
- **CONCEPT:** Maximum drawdown of a short strategy — measuring drawdown; a very high drawdown (e.g. −61%) is driven by panic-crash positions such as during the 2020 pandemic, motivating a filter. prereqs: drawdown, market stress
- **CONCEPT:** Performance measures table — reporting strategy returns, CAGR, max drawdown, and CAGR/max drawdown for comparison with the enhanced variant. prereqs: metrics
### LESSON: Enhanced VIX Futures Expiration Strategy (`VIX Futures Expiration Enhanced Strategy.ipynb`)
- **CONCEPT:** Strategy enhancement via a vol-level filter — the same VIX expiration short strategy but taking exit/entry only when a market-volatility condition holds, to reduce drawdown. prereqs: VIX futures expiration strategy
- **CONCEPT:** VIX1M (CBOE 1-month Volatility Index) — a real-time market index of the market's expected 30-day forward-looking volatility (VIX). prereqs: implied volatility, S&P 500 options
- **CONCEPT:** VIX3M (CBOE 3-Month Volatility Index) — a constant measure of the expected 3-month forward-looking volatility. prereqs: implied volatility
- **CONCEPT:** Filter condition VIX3M > VIX1M — short VIXY only when longer-month volatility exceeds the 1-month level (a regime/term-structure filter), avoiding high-volatility panic periods. prereqs: VIX1M, VIX3M
- **CONCEPT:** Data availability constraint — VIX3M data begins later (e.g. 2011-10-06), so the backtest and usable-signal window start from the later common date. prereqs: data spans, merges
- **CONCEPT:** Merging price panels — inner/outer joins of VIXY, VIX1M, and VIX3M price data on Date to align all signals. prereqs: pandas merge, datetime index
- **CONCEPT:** Combined condition signal — triggering a short only when both (near-expiry) and (VIX3M above VIX1M) hold; improving CAGR strongly and cutting maximum drawdown. prereqs: boolean logic, signals
- **CONCEPT:** Comparative strategy evaluation — comparing normalized vs. enhanced metrics (returns, CAGR, max drawdown, CAGR/DD) to quantify improvement from the filter. prereqs: metrics tables
## MODULE: December Effect in Volatility Market
### LESSON: December Seasonality Effect (`December Seasonality Effect.ipynb`)
- **CONCEPT:** Pre-holiday / December seasonality effect — a well-known volatility-market anomaly: returns tend to drop between December's VIX futures expiration and Christmas, with lower volatility and heightened sentiment as Christmas approaches. prereqs: calendar anomaly
- **CONCEPT:** VIXY December short position — shorting VIXY from two days before December's VIX futures expiration until (exit) the first business day after Christmas. prereqs: short selling, VIXY
- **CONCEPT:** Entry-signal definition — flagging dates two days before the December VIX futures expiration (December-month condition) as short-position entry. prereqs: event dates, datetime month
- **CONCEPT:** Exit-signal definition — flagging the first (and security second) business day after Christmas as the exit day, using `BDay` offsets to survive holiday windows. prereqs: BDay offset, date arithmetic
- **CONCEPT:** Forward-fill of positions (`ffill`) — after entry/exit flags, filling NaN signal values forward so positions (short = −1) and flat (0) are continuous across the held window. prereqs: pandas fillna, signal continuity
- **CONCEPT:** Daily returns & cumulative strategy returns — `pct_change()` returns multiplied by the short signal, then `cumprod` for the equity curve. prereqs: returns, compounding
- **CONCEPT:** Drawdown calculation — computing maximum drawdown from cumulative returns vs. running maximum to judge risk of the seasonal short. prereqs: drawdown definition
- **CONCEPT:** VIX1M / VIX3M use & enhancement filter — shorting VIXY only when VIX3M > VIX1M in the entry conditions, to avoid trading during extreme volatility regimes (crises, pandemics); enhances CAGR and lowers max drawdown. prereqs: VIX1M, VIX3M, filtering
- **CONCEPT:** Enhanced vs unenhanced comparison — tabulating returns, CAGR, max drawdown, and CAGR/max-drawdown for the December strategy with and without the VIX futures filter. prereqs: metrics, comparison
## MODULE: End of the Month Effect in Fixed Income
### LESSON: End of the Month Effect (`End of the Month.ipynb`)
- **CONCEPT:** End-of-month effect — an anomaly in coupon Treasury securities: average returns are positive and statistically significant in the last few days of the month but not different from zero at other times. prereqs: calendar anomaly
- **CONCEPT:** TLT ETF as trading vehicle — holding the long-term Treasury ETF for the last two days before month-end. prereqs: TLT, position holding
- **CONCEPT:** EOM signal generation — inserting 1 on the last two trading days of each month by comparing the current month number against the previous days' month values (month-change detection). prereqs: datetime month, boolean masks
- **CONCEPT:** Strategy returns and cumulative curve — daily returns × eom_signal then `cumprod` for the equity curve. prereqs: returns, cumprod
- **CONCEPT:** CAGR performance — annualised growth over the trading-day count. prereqs: CAGR arithmetic
- **CONCEPT:** Maximum drawdown & performance summary — measuring peak-to-valley decline and compiling strategy returns, CAGR, max drawdown, CAGR/DD in a tabulate table. prereqs: drawdown, metrics
## MODULE: FED Day Effect in Equities
### LESSON: Federal Open Market Committee (FOMC) Day Effect (`FED Day Effect Code.ipynb`)
- **CONCEPT:** FOMC (FED) meeting effect — the S&P 500's average daily returns on FOMC meeting dates have historically been outstanding (five-plus times average-day returns); with meeting dates public, one can long the SPY ETF around them. prereqs: calendar anomaly, central-bank events
- **CONCEPT:** SPY ETF — an ETF designed to track the S&P 500 index (later also used in the composite strategy). prereqs: equity ETF
- **CONCEPT:** FED-day signal matching — assigning a signal of 1 on SPY trading dates that coincide with announced FED meeting days (via `isin`). prereqs: event calendar, isin
- **CONCEPT:** Trend factor / moving-average filter — a filter that trades only when SPY's price sits above its 200-period simple moving average (SMA), a regime filter to avoid downtrends and cut drawdown. prereqs: SMA, rolling mean, trend following
- **CONCEPT:** SMA computation (`rolling(window).mean()`) — computing the 200-day rolling simple moving average of close prices. prereqs: rolling window, mean
- **CONCEPT:** SMA signal with shift — comparing previous close > previous SMA (shift(1)) so positions are decided on information available at the prior close, avoiding lookahead. prereqs: shift, comparison
- **CONCEPT:** Strategy returns with and without trend factor — multiplying daily changes by the FED signal, and additionally by the SMA signal in the trend-filtered variant. prereqs: signal multiplication
- **CONCEPT:** Effect of the trend filter on risk-adjusted returns — the trend factor lowers CAGR but drastically improves maximum drawdown (e.g. −8.5% → −4.9%). prereqs: drawdown vs CAGR trade-offs
## MODULE: Options Expiration Effect in Equities
### LESSON: Options Expiration Week Effect (`Options Expiration Effect Code.ipynb`)
- **CONCEPT:** Options-expiration week effect — a calendar anomaly where large-cap stocks with actively-traded options have substantially higher average weekly returns in the options-expiration week (week before the third Friday / before each 3rd Saturday per US market convention). prereqs: options expiry, calendar anomaly
- **CONCEPT:** Strategy implementation — buy SPY ETF at close of the Friday before the 2nd Saturday and sell at close the following Thursday, capturing the expiration-week return premium. prereqs: position timing
- **CONCEPT:** Finding the expiration day — a utility function `get_expiration_day` using `relativedelta(weekday=FR(3))` to find the third Friday of each month for the whole backtest range. prereqs: date arithmetic, relativedelta
- **CONCEPT:** Expiration-week signal — flagging all trading dates that lie one to four days ahead of an options expiration day using `timedelta` date shifts and OR logic. prereqs: boolean OR, date shift
- **CONCEPT:** Strategy returns / CAGR / drawdown — multiplying daily changes by the week-signal, compounding, and computing CAGR and maximum drawdown. prereqs: returns, CAGR, drawdown
- **CONCEPT:** Trend-factor enhancement — overlaying the 200-day SMA filter to trade only in up-trends, increasing CAGR and sharply improving max drawdown. prereqs: SMA trend filter
## MODULE: Payday Effect in Equities
### LESSON: The Payday Effect (`Payday Effect Code.ipynb`)
- **CONCEPT:** Payday effect — the abnormal-return anomaly in equities linked to paydays (many companies pay twice a month, the 15th and month end), so a mid-month pattern analogous to the turn-of-month effect exists. prereqs: calendar anomaly, payroll cycles
- **CONCEPT:** Strategy rule — buying the SPY ETF at close on the 15th day of each month and selling at close the next day to capture the payday return. prereqs: payday anomaly
- **CONCEPT:** Weekend-aware payday signal — placing 1 on the day with day-of-month 16, and (if the 16th falls on a weekend) also checking day 17 and 18 while guarding against double-counting with a shift-difference guard. prereqs: day-of-month, weekend calendar
- **CONCEPT:** Payday signal generation with `np.where` — conditional flagging using successive `np.where` steps and `shift` guards for weekend-pushed paydays. prereqs: numpy where, shift
- **CONCEPT:** Strategy returns / CAGR / drawdown — daily returns weighted by the payday signal, compounded, and measured for CAGR and maximum drawdown. prereqs: returns, CAGR, drawdown
- **CONCEPT:** Trend-filter overlay — adding the 200-day SMA trend condition to reduce drawdown (CAGR drops but max drawdown improves). prereqs: SMA filter
## MODULE: Turn of Month Effect in Equities
### LESSON: Turn of the Month Effect (`Turn of the Month Code.ipynb`)
- **CONCEPT:** Turn-of-the-month (ToM) effect — a well-documented equity-index anomaly via which prices tend to rise over the last four and the first three days of each month (DJIA / S&P 500). prereqs: calendar anomaly
- **CONCEPT:** Strategy rule — buying SPY at the end of the month and selling at the close of the first day of the following month. prereqs: ToM calendar pattern
- **CONCEPT:** ToM signal generation — placing 1 when the current date's month differs from the previous date's month (first day of each month). prereqs: datetime month, np.where
- **CONCEPT:** Strategy returns / CAGR / drawdown — daily returns weighted by the ToM signal × daily change, then compounded; evaluate CAGR and maximum drawdown. prereqs: returns, CAGR, drawdown
- **CONCEPT:** Trend-filter overlay — trading only when close > 200-day SMA to improve both CAGR and max drawdown with the trend factor. prereqs: SMA trend filter
## MODULE: Composite Strategy
### LESSON: Composite Seasonal Strategy — Volatility Weighted (`Composite Strategy.ipynb`)
- **CONCEPT:** Composite seasonal strategy — combining the separate calendar/seasonal strategies from equities, fixed income, and volatility into one portfolio, to improve return and risk-adjusted performance versus running each sub-strategy alone. prereqs: calendar strategies, portfolio construction
- **CONCEPT:** Sub-strategy per asset class — the composite uses 4 equity signals (Turn of the Month, Payday, FED day, Option Expiration Week) OR'd into one SPY signal; 2 fixed-income signals (End of Month, Treasury Auction) OR'd for TLT; and 2 volatility signals (VIX futures expiration, December expiration) minimised for VIXY. prereqs: each seasonal strategy individually
- **CONCEPT:** Signal fusion with OR logic — combining several 0/1 signal vectors by logical OR; implemented numerically as the elementwise `max` for long signals (equities, fixed income) and `min` for the short VIXY signals (since shorts are −1). prereqs: boolean OR, max/min reduction
- **CONCEPT:** Asset-class instruments — SPY (equities/S&P 500), TLT (government fixed income), and VIXY (volatility) ETFs traded by the composite strategy. prereqs: instruments per class
- **CONCEPT:** Trimming asset histories — restricting each asset's price history to the shortest one (VIXY, from 2011) so all panels align at the backtest start date. prereqs: data alignment, tails
- **CONCEPT:** Calendar data import — loading FED days, VIX futures expiration dates, and Treasury auction dates as the event calendars powering the sub-signals. prereqs: event calendars
- **CONCEPT:** Equal weighting vs volatility weighting — evenly splitting capital (eight equal 12.5% pieces) versus weighting assets inversely to their volatility (risk parity) so riskier assets contribute less risk. prereqs: portfolio weights, risk
- **CONCEPT:** Inverse-volatility / risk-parity weighting — a weight selection methodology where assets/strategies with higher volatility get lower portfolio weight, used here to size SPY/TLT/VIXY (e.g. 37.68% / 51.11% / 11.21%). prereqs: volatility, weighting
- **CONCEPT:** Weighted daily portfolio returns — combining each asset's signal-weighted daily returns scaled by its portfolio weight, summing, and compounding the resulting combined return path. prereqs: weighted sum, cumprod
- **CONCEPT:** Risk/return of the composite — evaluating the combined strategy's CAGR, maximum drawdown, and CAGR/drawdown ratio against individual strategies. prereqs: metrics, money-weighted series
- **CONCEPT:** Composite drawdown measure — computing maximum drawdown of the combined equity curve to verify the diversification benefit of combining sub-strategies. prereqs: drawdown, diversification
## Full-Module Concepts Shared Across all Calendar Strategies
- **CONCEPT:** pandas `read_csv` + datetime parsing — loading OHLC/close data files and converting the Date column (or index) to datetime for date-based signal logic. prereqs: pandas basics
- **CONCEPT:** `pct_change()` daily returns — daily fractional asset returns from each day's close price; the raw ingredient for strategy returns. prereqs: percentage change
- **CONCEPT:** Signal-weighted strategy returns — multiplying each day's return by a 0/1 (or +1/−1) signal vector so returns accrue only on active signal days. prereqs: signals, elementwise multiply
- **CONCEPT:** Compound equity curve (`cumprod`) — compounding (1 + daily_return) to build the cumulative strategy performance. prereqs: compounding
- **CONCEPT:** CAGR from cumulative curve — annualising the final equity ratio over the universe of 252 trading days. prereqs: CAGR, annualise
- **CONCEPT:** Running maximum & drawdown — `np.maximum.accumulate` to find the running peak and define drawdown = curve/running_max − 1; minimum is the maximum drawdown. prereqs: cumulative returns, running statistics
- **CONCEPT:** Performance table — tabulate reporting of returns, CAGR, maximum drawdown, and the CAGR/max-drawdown efficiency ratio. prereqs: metrics, table formatting
---
## Event-Driven-Strategies — Section-based course structure (full lesson-by-lesson view)
# Concept Inventory — Event Driven Trading Strategies
## COURSE: Event Driven Trading Strategies
### Section: Section 1 - Introduction to the Course
- **Prologue / course structure:** overview of seasonal & calendar event-driven strategies across equities, fixed income, and volatility markets. prereqs: none.
### Section: Section 2 - Introduction to Event Trading Strategies
- **Seasonal event-driven trading strategies:** strategies that exploit recurring calendar/seasonal patterns. prereqs: none.
- **Theory behind event-driven trading strategies:** why predictable events create exploitable return patterns (behavioral, institutional flows). prereqs: seasonal strategies.
### Section: Section 3 - Turn of Month Effect in Equities
- **Precap of calendar anomalies in equities:** review of known calendar effects (Halloween, January, weekend, holiday). prereqs: event trading intro.
- **Turn of the Month effect:** abnormal positive returns around the last/first days of the month. prereqs: calendar anomalies.
- **Exchange-Traded Fund (ETF):** basket of securities tracking a benchmark (SPY→S&P500, TLT→Treasuries, VIXY→VIX); types (market, sector, dividend, style, commodity, currency, bond). prereqs: equities basics.
### Section: Section 4 - Turn of Month Effect in Equities Code
- **Turn of the Month effect evidence:** documented on DJIA 1897–2005; persists across financial crises. prereqs: turn of month effect.
- **Anatomy of calendar effects:** interaction of Halloween, January, turn-of-month, weekend, holiday effects. prereqs: calendar anomalies.
### Section: Section 7 - Payday Effect in Equities
- **Payday effect:** abnormal returns near the 16th of the month (payday anomaly). prereqs: calendar anomalies.
### Section: Section 8 - FED Day Effect in Equities
- **FED day effect:** positive significant calendar effect around FOMC meeting dates on S&P 500. prereqs: calendar anomalies.
- **Pre-FOMC drift:** return drift before FOMC announcements; its disappearance post-2015. prereqs: FED day effect.
### Section: Section 9 - Options Expiration Effect in Equities
- **Options expiration effect:** return/activity patterns over option-expiration week (S&P 100). prereqs: options basics.
- **Causes of expiration effect:** delta-hedge rebalancing by market makers; declining risk perceptions (implied vol). prereqs: options expiration effect; options Greeks.
### Section: Section 10 - Auction Trading Effect in Fixed Income
- **Fixed income / government bonds:** debt securities with coupon payments; bondholders paid before shareholders; low-risk. prereqs: none.
- **Auction trading effect:** Treasury prices fall in days before auctions and recover after, despite announced schedule. prereqs: government bonds.
- **Trading ahead of Treasury auctions:** model of gradual price decrease before anticipated asset sales. prereqs: auction effect.
### Section: Section 11 - End of the Month Effect in Fixed Income
- **End of the month effect (fixed income):** positive excess returns on coupon Treasuries in last days of month; high annualized Sharpe (~1). prereqs: fixed income; turn of month effect.
### Section: Section 12 - Calendar Effect in Volatility Market
- **Volatility concepts:** statistical dispersion of returns; implied vs historical volatility. prereqs: none.
- **VIX / VIX3M indices:** CBOE Volatility Index measuring expected S&P 500 volatility. prereqs: volatility.
- **Volatility trading & markets:** trading volatility as an asset class. prereqs: VIX.
- **Futures, forward curve, VIX futures, spot price:** derivatives basics for volatility products. prereqs: volatility.
- **Contango and backwardation:** futures term-structure states. prereqs: futures.
- **Volatility ETF:** ETF tracking volatility (e.g., VIXY). prereqs: ETF; VIX.
- **VIX futures expiration effect:** calendar pattern around VIX futures expiration; enhancement of the effect. prereqs: VIX futures; calendar effects.
### Section: Section 13 - December Effect in Volatility Market
- **December seasonality effect:** holiday calendar effects on returns/volatility (DJIA, Eurozone). prereqs: calendar effects.
- **Holiday effect explanation:** investors avoid selling around holidays → abnormal pre/post-holiday returns. prereqs: December effect.
### Section: Section 14 - Composite Strategy
- **Introduction to composite seasonal strategy:** combining multiple seasonal effects into one strategy. prereqs: all seasonal effects.
- **Composite strategy — equal weighted:** averaging signals/returns of component effects equally. prereqs: composite strategy.
- **Composite strategy — volatility weighted:** weighting components by inverse volatility. prereqs: composite strategy; volatility.
- **Composite strategy — enhanced volatility:** refined volatility weighting to improve risk-adjusted returns. prereqs: volatility-weighted composite.
### Section: Section 15 - Composite Strategy Enhancement
- **Effect of trading cost:** how transaction costs erode composite strategy returns. prereqs: composite strategy; transaction costs.
- **Composite strategy improvement:** tuning/refining the composite for better performance. prereqs: composite strategy.
### Section: Section 16 - Effect of COVID-19
- **Effect of COVID-19:** how the pandemic disrupted seasonal/calendar patterns and strategy performance. prereqs: composite strategy.
### Section: Section 17 - Automate Trading Strategies
- **Automation of strategy / live trading steps:** connect to broker, load algorithm, stream live data, generate signals, send orders. prereqs: strategy implementation.
- **Algorithmic execution example (IBridgePy/TWS):** deploying a strategy via Interactive Brokers TWS + IBridgePy. prereqs: automation steps.
### Section: Section 19 - Course Summary
- **Course summary:** recap of all event-driven effects and composite construction. prereqs: all prior sections.
## Course Prerequisite Map
- Foundations: *ETF, government bonds, volatility/VIX, futures, options basics* (each standalone).
- Calendar anomalies in equities: *Turn of Month → Payday → FED Day → Options Expiration* (all build on calendar-anomaly concept).
- Fixed income effects: *Government bonds → Auction effect; + Turn of Month → End of Month effect.*
- Volatility effects: *Volatility/VIX → VIX futures → VIX expiration effect; + calendar → December effect.*
- Composite Strategy requires all seasonal effects; *Equal-weighted → Volatility-weighted → Enhanced.*
- Enhancement needs transaction costs; COVID-19 effect modifies composite.
- Automation builds on any implemented strategy.
- Course flow: **Intro → Event Trading Theory → Equities effects (TOM, Payday, FED, Options Exp) → Fixed income (Auction, EOM) → Volatility (VIX exp, December) → Composite → Enhancement → COVID → Automation → Summary.**
- FunPath basics feeding this course: returns math, basic statistics (mean, std, Sharpe), Python for trading, options & futures fundamentals.


====================
Financial-Time-Series-Analysis
====================

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


====================
Forex-Trading-with-Python-Basics
====================

# Concept Inventory: Forex Trading using Python - Basics
> Inventory source: 1 PDF (` Blueshift Utility Functions.pdf`), 1 Python strategy (`forex_basic_code.py`). No section subfolders exist in this course folder — course content is flat (single unit).
## COURSE
Introductory course on building & backtesting a simple algorithmic forex trading (currency-pair rebalancing) strategy on the Blueshift platform, which is built on **Zipline**. Focus is on the Blueshift API function set (initialize / scheduling / data fetching / order placement) and a working momentum-style multi-currency-pair rebalance strategy. The content corresponds to roughly the first unit of a larger forex algorithmic-trading stream.
### Section: (Course unit) — Blueshift Utility Functions (platform API)
Source: ` Blueshift Utility Functions.pdf` • Course code: `forex_core.py`
- Blueshift is built on Zipline (Pythonic algorithmic trading/backtesting library).
- `zipline.api` basic functions underpin every strategy on the platform.
- **Initialize function**
 - `initialize(context)` called once before strategy start; passed a `context` object.
 - `context` is a persistent namespace for storing variables accessible from anywhere in the algorithm (lookback, currency list, etc.).
- **Optional functions**
 - `before_trading_start(context, data)` — called before the market opens (pre-market setup).
 - `handle_data(context, data)` — called **every minute**; receives current trading bar OHLC + volume for all currency pairs.
 - `schedule_function(...)` — schedule a named function to run on chosen days/times.
 - `date_rules`: `every_day`, `week_start`, `week_end`, `month_start`, `month_end`; supports `days_offset`.
 - `time_rules`: `market_open`, `market_close`; supports `hours` / `minutes` offsets.
 - `set_account_currency('USD')` — set base/PnL currency.
 - `get_datetime()` — current strategy datetime.
- **Data fetching — `data.history(...)`**
 - `assets` = currency-pair symbol or iterable of symbols (string notational).
 - `fields` = 'price', 'open', 'high', 'low', 'close', 'volume'.
 - `bar_count` = integer number of bars/sub-sample.
 - `frequency` = '1m' (minute) or '1d' (daily); for other frequencies use pandas `resample`.
 - Returns a pandas Series / DataFrame / Panel indexed by date.
 - 'price' field is forward-filled (last known price, else NaN).
- **Order placement**
 - `order_target_percent(symbol, target_pct)` — rebalance a currency pair to a target portfolio weight (supports long/short via +/- percentages; 0 = flat entry).
- **Strategy logic (from `forex_cross.py`)**
 - Currency pairs list: AUD/USD, EUR/USD, GBP/USD, NZD/USD, USD/CHF, USD/CAD, USD/JPY.
 - `context.lookback = 50` days; fetch daily 'close' bars.
 - Compute returns over lookback = `iloc[-1]/iloc[0] - 1`; sort descending by return.
 - **Long** the top-3 pairs (weight 1/6 each), **Short** the bottom-3 pairs (weight -1/6 each), flat (0) the middle (4th) pair — a simple momentum/reversal rebalance.
 - Rebalance weekly at `week_start`, market_open +15min.
### Prerequisites (for this unit)
- Basic familiarity with Zipline OR willingness to learn its API surface.
- Working knowledge of pandas DataFrame indexing/slicing (`iloc`), pandas resample.
- Understanding of currency-pair symbols (FX convention AUD/USD etc.).
- Basic Python function definitions and module imports.
## Course Prerequisite Map
- **Python fundamentals** → pandas data structures (Series/DataFrame) → `data.history` return shapes.
- **Zipline/event-loop model** → initialize/before_trading_start/handle_data lifecycle.
- **Portfolio/weight math incl. MPT & position sizing concepts (Track 7 / Track 1 level)** → `order_target_percent` rebalancing weights per pair.
- **Forex market basics** → currency pair ticks, bid/ask/OHLC, '1d' vs '1m' frequency, pricing marks.
- No formal folder-level prerequisite chain exists in this course (single unit).
---
*Notes on D (duplicate/overlap) with other tracks*: Blueshift/Zipline API concepts overlap with Track 1 (Algorithmic Trading for Beginners) strategy skeleton material; momentum/reversal pair rebalancing overlaps Track 3 and Track 6 (Value Strategy in Forex) weight-selection logic.


====================
Futures-Trading-Concepts-Strategies
====================

## COURSE: Futures Trading: Concepts & Strategies
Course folder: `Futures-Trading-Concepts-Strategies-20250429T093046Z-001`
Notebooks: 17
---
## MODULE: Trend Following Introduction
- Notebook: `Trend Following Introduction/Expected PnL Calculation.ipynb`
### LESSON: Expected PnL Calculation
- **Expected PnL** — profit/loss expectation over repeated trades. − prereqs: PnL, returns
- **Dice-rolling game analogy** — a small edge pays off given enough trials. − prereqs: probability, expected value
- **High loss-rate trend model** — most trend trades fail (60–70%), but winners are large. − prereqs: win rate, gain expectancy
- **Law of large numbers** — many trades converge toward the expected value. − prereqs: probability, random sampling
- **Small edge compounding** — a slight positive edge becomes decisive over many trades. − prereqs: expected value, cumulative returns
- **Random simulation in Python** — using `randint` to simulate repeated outcomes. − prereqs: randomness, simulation
- **Total vs net PnL** — costs reduce gross gain to the net result. − prereqs: PnL, trading costs
## MODULE: Trend Following Entries
- Notebook: `Trend Following Entries/Code Trend Following Entries.ipynb`
### LESSON: Code Trend Following Entries
- **Trend filter** — direction of the dominant trend via moving averages. − prereqs: trend, moving averages
- **40/80-day exponential moving average** — fast vs slow EMA crossover defines trend. − prereqs: EMA, moving averages
- **Bullish vs bearish trend** — fast EMA above (bull) or below (bear) slow EMA. − prereqs: trend filter, moving averages
- **Breakout window** — lookback period for highs/lows (50 days). − prereqs: rolling functions, window
- **Rolling high / low** — trailing maximum/minimum of close price. − prereqs: pandas rolling, window
- **Long entry signal** — bullish trend AND price breaks 50-day high. − prereqs: trend filter, breakout
- **Short entry signal** — bearish trend AND price breaks 50-day low. − prereqs: trend filter, breakout
## MODULE: Trend Following Exits
- Notebook: `Trend Following Exits/Trend Following Exits_ Single Asset.ipynb`
### LESSON: Trend Following Exits — Single Asset
- **Pullback** — volatility-normalised decline from the recent high/low. − prereqs: trend, volatility
- **Pullback formula** — (close − rolling highest) / volatility. − prereqs: rolling high, volatility
- **Pullback threshold exit** — exit long when pullback < −3 units. − prereqs: pullback, threshold
- **Breakout** — max/min close over the breakout window. − prereqs: rolling window, breakout
- **Long position rules** — enter on uptrend + breakout, exit on pullback. − prereqs: entries, exits
- **Short position rules** — enter on downtrend + breakout, exit on pullback. − prereqs: long rules, inverse
- **Forward-fill positions** — `ffill()` holds the last position until the next action. − prereqs: fillna, positions
## MODULE: Trend Following Analysis on Single Markets
- Notebook: `Trend Following Analysis on Single Markets/Strategy Returns for Trend Following.ipynb`
### LESSON: Strategy Returns for Trend Following
- **Trend strategy function** — encapsulating entry/exit logic as a reusable function. − prereqs: trend following, functions
- **Total position** — sum of long and short positions. − prereqs: long position, short position
- **Strategy returns** — daily percentage change × previous-day position. − prereqs: returns, daily change
- **Cumulative returns** — cumulative product of (return + 1). − prereqs: returns, compounding
- **Single-asset instability** — trend following on one asset gives uneven returns. − prereqs: cumulative returns, drawdown
- **Interpreting drawdowns** — sharp dips signal a weak single-asset trend strategy. − prereqs: equity curve, drawdown
## MODULE: Diversification in Trend Following
📂 Notebook: `Diversification in Trend Following/Trend Following Strategy on Multiple Assets.ipynb`
### LESSON: Trend Following Strategy on Multiple Assets
- **Diversification** — holding many assets to stabilise portfolio returns. − prereqs: portfolio, risk
- **Inverse volatility weights** — a larger weight to the less volatile asset. − prereqs: volatility, weights
- **Inverse volatility formula** — weight = (1/vol) normalised by the sum of inverse vols. − prereqs: volatility, weights
- **Volatility-driven position allocation** — using volatility to allocate position sizes. − prereqs: volatility, position sizing
- **Portfolio returns** — sum of volatile-weighted strategy returns. − prereqs: weights, strategy returns
- **Reduced drawdowns** — diversification lowers drawdown vs a single asset. − prereqs: drawdown, portfolio returns
- **Comparable return dispersion** — weighting makes asset contributions comparable. − prereqs: drawdown, volatility
## MODULE: Pushing Diversification Further
### 📝 Notebook: `Pushing Diversification Further/Pushing Diversification Further.ipynb`
### LESSON: Pushing Diversification Further
- **Portfolio of strategies** — combine multiple (core trend, counter trend, term structure). − prereqs: portfolio, strategy
- **Monthly rebalancing** — periodically resetting portfolio weights. − prereqs: rebalancing, weights
- **Rebalancing class** — a Python class encapsulating monthly rebalancing. − prereqs: classes, rebalancing
- **Weighted combined returns** — rebalanced cumulative returns dotted with weights. − prereqs: weights, returns
- **Benchmark comparison** — combined strategy vs S&P 500 Total Return index. − prereqs: benchmark, returns
- **Annualised return** — backtest returns raised to inverse years. − prereqs: returns, annualisation
- **Annualised volatility** — daily vol scaled by sqrt(252). − prereqs: volatility, annualisation
- **Sharpe ratio** — annualised return divided by annualised vol. − prereqs: return, volatility
- **Maximum drawdown** — worst peak-to-trough portfolio loss. − prereqs: cumulative returns, drawdown
## MODULE: Counter Trend Strategy
- Notebook: `Counter Trend Entries/Entry Signal.ipynb`, `Counter Trend Exits/Counter Trend Exits.ipynb`
### LESSON: Counter Trend Entry Signal
- **Counter-trend entry** — entering in opposition to the pullback direction. − prereqs: trend, pullback
- **Volatility-normalised pullback** — standardising dips from the recent high. − prereqs: pullback, volatility
- **Rip-entry signal (long)** — enter on a pullback below −3 in an uptrend. − prereqs: entry, pullback
- **EMA trend filter reuse** — the same 40/80-day EMA trend definition. − prereqs: EMA, trend filter
### LESSON: Counter Trend Exits
- **Counter-trend exit** — exit on a trend flip or after a one-month hold. − prereqs: countertrend entry, exits
- **Trend flip as exit trigger** — exit a long when the uptrend turns to a downtrend. − prereqs: trend filter, trend
- **One-month time stop** — close positions held for 30 days. − prereqs: holding, exits
- **Iterating over dates** — a `for` loop to apply entry/exit logic each day. − prereqs: loops, positions
- **Strategy returns** — daily change × previous-day position. − prereqs: positions, returns
## MODULE: Futures Continuation
### 📗 Notebook: `Futures Continuations/Additive Adjustment.ipynb`, `Futures Continuations/Proportional Adjustment.ipynb`
### LESSON: Additive Adjustment
- **Futures continuation** — stitching consecutive futures contracts into one series. − prereqs: futures, contracts
- **Rollover date** — the expiry date when switching to the next contract. − prereqs: contracts, futures
- **Rollover gap** — an artificial price jump unless adjusted. − prereqs: continuation, expiry
- **Adjustment factor (additive)** — second contract price − first contract price on expiry. − prereqs: prices
- **Backwards Panama canal roll** — add/subtract a fixed amount to the earlier contract. − prereqs: addition, continuation
- **End-to-end roll** — rolling the contract on the first contract's expiry date. − prereqs: rollover, contracts
- **Continuous price series** — a series with no artificial jumps. − prereqs: continuation, price
### LESSON: Proportional adjustment
- **Drawbacks of additive adjustment** — long series can go negative, breaking returns. − prereqs: additive adjustment, returns
- **Proportional (ratio) factor** — second contract price ÷ first contract price. − prereqs: prices, division
- **Backwards ratio roll** — multiply the previous contract by a ratio. − prereqs: proportional adjustment, continuation
- **Multiple-contract roll** — joining more than two contracts in sequence. − prereqs: proportional adjustment, contracts
- **Expiry vs roll date** — last trading date vs next-contract switch date. − prereqs: rollover, futures
## MODULE: Futures Profit and Loss
### 📘 Notebook: `Futures Profit and Loss/Calculate Futures PnL in Python.ipynb`
### LESSON: Calculate Futures PnL in Python
- **Futures PnL** — profit/loss on a futures position. − prereqs: futures, profit & loss
- **Point value / contract size** — fixed per-market multiplier (e.g. gold = 100 oz). − prereqs: futures, contract
- **Market metadata lookup** — point value stored in a dictionary/table. − prereqs: point value, lookup
- **Daily PnL** — daily price change × position × point value. − prereqs: PnL, price change
- **Cumulative PnL** — cumulative sum of daily PnL. − prereqs: daily PnL, cumsum
- **Percentage returns** — `pct_change()` to compute daily returns. − prereqs: returns, percentage
- **Daily long trades** — buying at close, selling at close later. − prereqs: positions, futures
## MODULE: Term Structure
## 📙 Notebook: `Term Structure/Annualised Implied Yield Calculation.ipynb`, `Term Structure/Quantification of Term Structure.ipynb`
### LESSON: Annualised Implied Yield (and Quantification of Term Structure)
(The two notebooks cover the same standalone content.)
- **Term structure / yield curve** — relationship between near and far futures contracts. − prereqs: futures, yield
- **Contango** — futures price higher than spot. − prereqs: spot, futures
- **Backwardation** — futures price lower than spot. − prereqs: spot, futures
- **Annualised implied yield** — annualised rate enabling cross-market comparison. − prereqs: term structure, annualisation
- **Days difference** — days between a futures expiry and the current date. − prereqs: dates, maturity
- **Percentage difference** — (futures / spot) − 1. − prereqs: prices, ratio
- **Open interest** — number of outstanding contracts (spot has none). − prereqs: contracts, futures
- **Shorting an overpriced contract** — shorting when annualised implied yield is favourable. − prereqs: yield, short
## MODULE: Risk Management — Position Sizing
### 📚 Notebook: `Risk Management/Position Allocation Using Python.ipynb`
### LESSON: Position Allocation Using Python
- **Position allocation** — giving every position a similar contribution to portfolio PnL. − prereqs: portfolio, risk
- **Annualised volatility** — std of % changes scaled by sqrt(252). − prereqs: volatility, annualisation
- **Daily variation per contract** — price standard deviation × contract size. − prereqs: contract size, volatility
- **Inverse-volatility allocation** — fewer contracts for volatile, more for calm assets. − prereqs: volatility, position size
- **Target daily variation** — portfolio value × risk factor. − prereqs: portfolio, risk
- **Notional exposure** — contracts × latest price × contract size. − prereqs: contracts, position size
## MODULE: Strategy backtesting
### 📚 Notebook: `Strategy Analysis/Strategy Analysis.ipynb`
### LESSON: Strategy Analysis
- **Backtest analysis** — analysing a strategy's historical results. − prereqs: returns, backtest
- **Benchmark comparison** — comparing strategy returns vs an index. − prereqs: benchmark, returns
- **Equity curve** — plotting cumulative returns over time. − prereqs: plotting, cumulative returns
- **Log-scale equity curves** — a semi-log y-axis aids long series comparison. − prereqs: plots, log scale
- **Annualised metrics (return, vol, Sharpe, max drawdown)** — performance statistics. − prereqs: returns, vol, Sharpe, drawdown
- **Rolling 6-month Sharpe & returns** — time-varying risk-adjusted performance. − prereqs: Sharpe, rolling window
## MODULE: Capstone Project (Trend Following)
### 📒 Notebook: `Futures-Trading-Capstone-.../Model Solution & Solution Template.ipynb`
### LESSON: Model Solution — Futures Trading Capstone
- **Complete trend-following pipeline** — building, weighting and analysing a trend strategy. − prereqs: trend, portfolio
- **Reading expiry futures data** — loading futures contracts from CSV with `Contracts.csv`. − prereqs: futures, CSV
- **Data sanity check** — detecting and dropping missing/outlier values. − prereqs: data cleaning, NaN
- **Continuous contract chain** — proportional adjustment across multiple assets. − prereqs: continuation, adjustment
- **Trend strategy function** — reusable trend-following entries/exits & returns. − prereqs: trend following, functions
- **Inverse-volatility weights** — allocate weight inversely to rolling vol. − prereqs: volatility, weights
- **Weighted strategy returns** — strategy returns × weights per asset. − prereqs: strategy, weights
- **Pyfolio performance analysis** — creating a tear sheet for the portfolio. − prereqs: performance metrics
### LESSON: Solution Template (same capstone)
- **Blank-capstone template** — a scaffold with placeholders for the learner to fill. — prereqs: all capstone concepts
---
## Cross-cutting / Thematic Concepts
Artificial across several notebooks in this course
- **Pandas dataframes & time series** — `read_csv`, `diff`, `pct_change`, `rolling`, `ffill` throughout. − prereqs: none
- **Charting** — matplotlib & seaborn plotting of prices, signals and returns. − prereqs: none
---
## Futures-Trading-Concepts-Strategies — Section-based course structure
# Concept Inventory — Futures Trading : Concepts & Strategies
> **26 sections on disk** (numbering gaps: sections 24–25 absent).
## COURSE — Futures Trading : Concepts & Strategies
**Purpose:** Master futures contracts as tradable instruments (mechanics, standardisation, margins, P&L, markets, datasets), then design, backtest, and automate systematic futures trading strategies — trend following, counter-trend, and term-structure (calendar spread) models — with risk management and diversification.
### Section: Section 1 - Introduction
- **CONCEPT:** Futures trading introduction — what futures are and how the course builds from contract mechanics to strategies to automation. prereqs: none.
- **CONCEPT:** Course structure flow — roadmap linking contract basics → market → data → term structure → systematic strategies. prereqs: none.
### Section: Section 2 - Futures Contract
- **CONCEPT:** What makes futures unique — a standardized, exchange-traded, legally binding contract to transact an underlying at a future date and price; futures ≠ spot. prereqs: none.
### Section: Section 3 - Standardisation & Clearing
- **CONCEPT:** Standardisation — contract specification (lot size, delivery month, tick value) makes futures fungible and liquid. prereqs: futures contract.
- **CONCEPT:** Clearing — central clearing house novates contracts, guarantees performance, manages margin. prereqs: futures contract, standardisation.
### Section: Section 4 - Futures Specific Properties
- **CONCEPT:** Futures specific properties I — expiration/delivery, leverage, tradableity of the contract vs the underlying. prereqs: futures contract.
- **CONCEPT:** Futures specific properties II — continuous vs spot relationship, basis risk, and why futures ≠ underlying. prereqs: futures specific properties I.
### Section: Section 5 - Futures Profit and Loss
- **CONCEPT:** Futures P&L calculation — P&L from price change × contract lot size × contract multiplier; marking to market. prereqs: futures contract.
- **CONCEPT:** Futures and currency exposure — non-USD-denominated futures introduce FX risk into P&L. prereqs: futures P&L.
### Section: Section 6 - Futures Market
- **CONCEPT:** Futures sectors — overview of futures across commodities, interest rates, FX, energy, equities. prereqs: futures contract.
- **CONCEPT:** Futures in the commodity sector — physical commodity futures behavior and drivers. prereqs: futures sectors overview.
### Section: Section 7 - Futures Dataset
- **CONCEPT:** Futures data — structure of historical futures price records (multiple contract months per asset). prereqs: futures market.
- **CONCEPT:** The issue of limited life span — each futures contract expires; no single continuous price series for an asset. prereqs: futures data.
- **CONCEPT:** Price difference in futures contracts — contracts of different delivery months trade at different prices. prereqs: futures data.
### Section: Section 8 - Futures Continuations
- **CONCEPT:** Default futures continuations — the standard method to stitch expired contracts into a continuous series (adjustment to front/spot contract). prereqs: futures dataset, limited life span.
- **CONCEPT:** Other methods of futures continuation — alternative adjustment schemes (e.g., proportional, price ratio) beyond the default. prereqs: default continuation.
- **CONCEPT:** Sources for futures data — where to obtain historical futures contract data. prereqs: futures dataset.
### Section: Section 9 - Analysing Tradable Assets
- **CONCEPT:** Trade what you analyse — analyse the actual futures contract traded, not the underlying; the underlying is rarely directly tradable. prereqs: price difference in contracts.
- **CONCEPT:** Futures trading concept — consolidate contract, dataset, and continuation into a single tradable asset series. prereqs: futures continuation, tradable assets.
### Section: Section 10 - Trend Following Introduction
- **CONCEPT:** Trend following background — systematic rule-based capture of sustained market trends. prereqs: systematic trading basics.
- **CONCEPT:** Principles of trend following — ride trends, cut losers, let winners run, defined by clear entry/exit rules. prereqs: trend following background.
### Section: Section 11 - Trend Following Entries
- **CONCEPT:** Trend following entries — rule-based signals (e.g., moving averages / price-break thresholds) to open long/short futures positions. prereqs: trend following principles, technical indicators.
### Section: Section 12 - Risk Management
- **CONCEPT:** Financial risk primer — risk sources in futures (market, leverage, tail risk) and why sizing and stops matter. prereqs: futures P&L.
- **CONCEPT:** Measuring financial risk using volatility — quantify per-asset volatility as a risk input. prereqs: risk primer, statistics.
- **CONCEPT:** Position allocation — size positions (often inverse-volatility weighted) so a multi-asset futures book is risk-balanced. prereqs: volatility risk measure.
### Section: Section 13 - Trend Following Exits
- **CONCEPT:** Trend following exits — rule-based exit signals (stop-loss/take-profit, trend reversals) to close positions. prereqs: trend following entries, risk management.
- **CONCEPT:** Setting the stop distance — calibrating stop-loss distance (e.g., to volatility) so exits are neither too tight nor too loose. prereqs: trend following exits, volatility.
### Section: Section 14 - Trend Following Analysis on Single Markets
- **CONCEPT:** Trend following rules — a formal logic flow (signal → entry → stop → exit) per market, captured in a flowchart. prereqs: entries, exits, stops.
- **CONCEPT:** Trend following on single markets — running the rules on one futures asset in analysis. prereqs: trend folowing rules, futures continuation.
### Section: Section 15 - Diversification in Trend Following
- **CONCEPT:** The power of diversification — spreading trend-following capital across many uncorrelated futures assets smooths equity & improves risk-adjusted returns. prereqs: trend following analysis, risk management.
### Section: Section 16 - Strategy Analysis
- **CONCEPT:** Strategy analysis — evaluating trend-following performance (returns, drawdown, Sharpe/Calmar) on a portfolio. prereqs: trend following on single markets, diversification.
- **CONCEPT:** Trend following trades — anatomy of individual trades: win/loss distribution, fee drag, and expectancy.
- **CONCEPT:** Limitations of trend following trades — whipsaws, rising interest, regime shifts; realistic expectation setting. prereqs: trend following trades.
### Section: Section 17 - Counter Trend Models
- **CONCEPT:** Counter trend models — systematic short-term reversals against a prevailing trend, mean-reversion assumption of ownership. prereqs: trend following exits, mean reversion.
### Section: Section 18 - Counter Trend Entries
- **CONCEPT:** Counter trend entries — entry signals for mean-reversion trades (overextended moves, indicator extremes). prereqs: counter trend models, indicators.
### Section: Section 19 - Counter Trend Exits
- **CONCEPT:** Counter trend exits — profit-taking / re-entry rules; rapid reversal targets and conservative stops. prereqs: counter trend entries.
### Section: Section 20 - Counter Trend Strategy Analysis
- **CONCEPT:** Counter trend strategy analysis — performance review of counter-trend against trend-following (frequency, win-rate, expectancy). prereqs: counter trend exits, strategy analysis.
### Section: Section 21 - Term Structure
- **CONCEPT:** Introduction to term structure — the pattern of futures prices across delivery months (the futures "curve"). prereqs: futures dataset.
- **CONCEPT:** Futures price and delivery dates — per-contract expiry & delivery creates the term dimension. prereqs: term structure introduction.
- **CONCEPT:** Term structure concept (contango / backwardation) — contango = far months > front; backwardation = far < front; implies directional bias. prereqs: futures price/delivery.
- **CONCEPT:** Quantifying term structure — implied yield (IY) as a normalized/directional measure to compare contract months. prereqs: term structure concept.
### Section: Section 22 - Term Structure Trading
- **CONCEPT:** Contract selection — using term structure to pick which delivery-month contracts to trade. prereqs: quantifying term structure.
- **CONCEPT:** Trading term structure — rotate long/short positions across the curve based on implied yield ranking. prereqs: contract selection.
- **CONCEPT:** Term structure strategy analysis — evaluating curve-based strategies (e.g., balanced fixed-distance long/short portfolio). prereqs: trading term structure.
- **CONCEPT:** Calendar spread strategy — concurrently hold offsetting legs across near/far months (futures analogue of options calendar spread) to exploit curve moves. prereqs: term structure trading.
### Section: Section 23 - Pushing Diversification Further
- **CONCEPT:** Pushing diversification further — broadening the multi-asset futures portfolio for even smoother risk-adjusted returns. prereqs: term trading, diversification.
### Section: Section 26 - Automate Trading Strategy Using IBridgePy
- **CONCEPT:** IBridgePy automation — using the IBridgePy framework to run futures strategies (trend, counter-trend) live every day before close. prereqs: full tested strategy.
- **CONCEPT:** Live trading template — `ft_functions_live_trading.py` + `ticker_information.csv` + per-strategy files configure symbols, lots, exchange, expiry. prereqs: IBridgePy automation.
### Section: Section 27 - Capstone Project
- **CONCEPT:** Capstone: futures strategy build — pick ≥3 uncorrelated expired futures; sanity-check data; build continuous series via continuation; design trend strategy; allocate inverse-vol weights; evaluate with Sharpe/Calmar & pyfolio. application of all course blocks. prereqs: term structure, trend following, risk management, diversification.
### Section: Section 28 - Course Summary
- **CONCEPT:** Conclusion & resources — full-syllabus recap and packaged code/data resources. prereqs: all course.
## Course Prerequisite Map
- Contract → Standardisation/Clearing → Specific Properties → P&L → Markets → Dataset → Continuation → Tradut Asset → [Term Structure | Trend Following]
- Term path: Intro → Delivery → Contango/Backward → Quantify (Implied Yield) → Contract Selection → Trading Curve → Calendar Spread → Diversify further
- Trend path: Background → Principles → Entries → Risk Mgmt → Exits/Stops → Single-Market Rules → Diversification → Analysis → Limitations; Counter-Trend branches off Exits for reversals.
- Strategy Analysis and Diversification feed forward into Counter-Trend, Term, and Capstone.
- Live automation (IBridgePy) and the Capstone integrate all blocks.


====================
Getting-Market-Data-Stocks-Crypto-News
====================

# Getting Market Data: Stocks, Crypto, News & Fundamental — Concept Inventory
Course goal: how to programmatically download the full range of market data (equity, index, minute-level, FX, futures, macro, news, options, and fundamental statements) into pandas DataFrames for backtesting and analysis, plus the basics of data-quality checks/cleaning.
## Enumerated Notebooks (15) + Module (1)
| # | Module folder | Notebook |
|---|---|---|
| 1 | Equity Price Data | Stock Daily Price Data |
| 2 | Equity Price Data | Stock Index Data |
| 3 | Equity Price Data | Data from Different Geographies |
| 4 | Equity Price Data | Minute Price Data and Resampling Techniques |
| 5 | Forex Price Data | Forex Price Data |
| 6 | Futures Data | Futures Data |
| 7 | Futures Data | Futures Continuations |
| 8 | Macro Data | Macro Data |
| 9 | Crypto Data | Cryptocurrency Data |
| 10 | News Data | Fetch News Headlines |
| 11 | Options Data | Options Chain Data from Yahoo! Finance |
| 12 | Stock Fundamental Data | Fundamental Data |
| 13 | Stock Fundamental Data | Ratios from Fundamental Data |
| 14 | Stock Fundamental Data | Other Company Data |
| 15 | Data Quality Checks and Data Cleaning | Basic Data Quality Checks and Data Cleaning |
---
## 1. Equity Price Data / Stock Daily Price Data
**Concepts:**
- Accessing historical OHLCV (Open-High-Low-Close-Volume) price data is a prerequisite for creating/backtesting any strategy.
- Using the `yfinance` package to download daily stock price data from Yahoo! Finance (`yf.download(ticker, start, end)`).
- Yahoo! Finance as a free data source covering stocks, currencies, crypto, futures, bonds, and fundamentals.
- Distinguish **Close** vs **Adjusted Close**: adjusted prices account for corporate actions (stock splits, dividends, rights offerings).
- Fetching fully adjusted OHLCV using the `auto_adjust=True` parameter of `download()`.
- Plotting the close-price series with `matplotlib`.
**Prereqs:** pandas DataFrame basics; date handling; basic plotting.
---
## 2. Equity Price Data / Stock Index Data
**Concepts:**
- Downloading price data for **multiple assets at once** by passing a list of tickers to `yf.download(ticker_list, start, end)[column]`.
- Reading web tables into DataFrames using pandas `read_html(url)` (e.g., S&P 500 constituents from Wikipedia).
- Converting a DataFrame column to a list via `DataFrame[column].tolist()` to build the ticker list.
- Normalizing comparative price charts by dividing each price series by its first value so assets at different magnitudes can be compared on the same scale.
- Extracting a single OHLCV column (e.g., Close) from a multi-asset download.
**Prereqs:** single-asset `yfinance` download (notebook 1); pandas Series/DataFrame methods; matplotlib.
## 3. Equity Price Data / Data from Different Geographies
**Concepts:**
- Fetching stock data for assets outside the standard US/S&P 500 universe (local-market tickers).
- Using the Yahoo! Finance symbol lookup to find ticker suffixes per exchange (e.g., `INFY` NYQ, `INFY.NS` NSE, `INFY.BO` BSE).
- Understanding exchange/provider suffix codes on Yahoo! Finance.
- Reusing `yf.download()` for geo-varied tickers; parameterising start/end dates.
**PreReqs:** notebook 1 daily download; website symbol-search workflow.
## 4. Equity Price Data / Minute Price Data and Resampling Techniques
**Concepts:**
- Downloading **minute-frequency** data via `yf.download(tickers, period, interval, auto_adjust)`.
- Valid `period` and `interval` enums for Yahoo! Finance minute data.
- Constraint: minute data is available only for ~7 days from Yahoo! Finance.
- **Resampling** high→low frequency using pandas `DataFrame.resample(interval).agg(aggregate)` ('15T', 'H', 'D', 'M').
- Resampling rule that OHLCV cannot be resampled back up (high-frequency info is lost).
- Defining an aggregation dictionary (Open=first, High=max, Low=min, Close=last, Volume=sum) with column names matching the DataFrame.
**Prereqs:** OHLCV semantics; pandas datetime index; basic `.agg`.
## 5. Forex Price Data
**Concepts:**
- Forex (foreign exchange / FX) price data download using `yfinance`.
- FX ticker convention `EURUSD=X` (base/quote currency pair).
- Downloading daily and minute FX data with the same `download()` parameters as equities.
- Looking up currency pair ticks on Yahoo! Finance.
**Prereqs:** notebooks 1 and 4 (day/minute download and resample).
## 6. Futures Data / Futures Data
**Concepts:**
- Futures contracts for an asset have successive expiry dates; most trading activity is in the earliest-expiring contract.
- **Continuous futures series** are built by joining successively-expiring contracts to enable analysis/backtesting.
- Downloading continuous futures data with `yf.download(ticker_symbol, start, end)` (e.g., `HE=F` lean hogs).
- Symbol lookups on Yahoo! Finance for futures tickers.
**PreReqs:** yfinance download workflow; basic time series concept.
## 7. Futures Data / Futures Continuations
**Concepts:**
- The limitation of vendor-built continuous futures series: at contract expiry a price difference (gap) exists between contracts.
- Adjusting earlier contracts backward to remove artificial price jumps when rolling over.
- **Additive adjustment**: shift by a constant so last value of first contract matches first value of second; drawback — long series can drift negative, and percentage moves are not preserved.
- **Proportional adjustment (backwards-ratio / end-to-end roll)**: right-shift the first contract by a *ratio* at rollover; preserves percentage moves.
- Stepwise procedure: get prices on rollover date → compute factor = second_price/first_price → multiply first-contract data by factor → append second contract.
- Terminology: end-to-end roll (roll on expiry date) and backwards ratio (keep current contract, adjust prior contracts).
**Prereqs:** notebook 6; basic returns/percent-change reasoning.
## 8. Macro Data
**Concepts:**
- Macroeconomic data (GDP, CPI, interest rates, unemployment, commodity/Gold ETF prices) as a big-picture view of an economy, relevant to markets.
- FRED (Federal Reserve Economic Database) via the `fredapi` wrapper: API key setup, `fred.get_series(series_ID)`.
- Knowing series IDs (GDP, `CPIAUCSL` CPI, `DGS3MO`/`DGS1`/`DGS10` treasuries, `UNRATE`, `POILBREUSDM` brent crude).
- World Bank data via `wbgapi` (`wb.data.DataFrame(code, mrv, labels=True)`, `wb.series.info()`).
- GDP-by-country retrieval, `dropna()` and `sort_values()` ordering.
- Gold ETF prices (`GLD` ticker) via `yfinance`.
- Visualising time series as percentage change from previous year.
**Prereqs:** pandas cleaning ops; time series; API-key usage.
## 9. Crypto / Cryptocurrency Data
**Concepts:**
- Fetching historical cryptocurrency data for backtesting with the `cryptocompare` package.
- Fetching all crypto tickers via `get_coin_list()`; converting dict → DataFrame.
- Fetching daily/hourly/minute history with `get_historical_price_day/hour/minute(ticker, currency, limit, exchange, toTs)`.
- `limit_value` max = 2000 bars; `toTs` = data-before timestamp.
**Prereqs:** API-key pattern; pandas `from_dict.csv`; OHLC plotting.
## 10. News Data / Fetch News Headlines
**Concepts:**
- Aggregating news headlines for sentiment/fundamental context via news APIs (NewsAPI, Webhose, GoogleNews, News Fetch).
- Common pipeline: install/import → obtain API key → apply filters (keywords, language, timeframe) → fetch articles.
- NewsAPIClient usage; building a DataFrame of date, time, title/headline, description, source.
- Filter by keywords (e.g., `AAPL`).
**Prereqs:** API key workflow; DataFrame construction.
## 11. Options Data / Options Chain Data from Yahoo! Finance
**Concepts:**
- Yahoo! Finance offers US-equity **options chain** data (calls and puts).
- Creating a `Ticker` object and reading available expiration dates via `.options` (call/pattern).
- Downloading the option chain with `ticker_object.option_chain(expiration_date)`.
- Interpreting chain fields: bid, ask, last traded price, volume, open interest per strike.
- Reading call price vs strike relationship (in-the-money > out-of-the-money); inverse for puts.
**Prereqs:** yfinance `Ticker` object; calls/puts basics; asset expiry.
## 12. Stock Fundamental Data / Fundamental Data
**Concepts:**
- Fetching stock fundamental statements (income statement, balance sheet, cash flow) via `simfin` and `yfinance`.
- SimFin API key setup; US/Germany market coverage; loading quarterly statements (`sf.load_income`, `sf.load_balance`, `sf.load_cashflow`).
- Pulling quarterly statements from yfinance (`Ticker.quarterly_income_stmt` etc.) and merging heterogeneous sources.
- Using a mapping dictionary to rename columns and union the merged DataFrame.
**Prereqs:** financial statements; DataFrame merge/rename (append join); API keys.
## 13. Stock Fundamental Data / Ratios from Fundamental Data
**Concepts:**
- Fundamental **ratios** summarise company performance/financial health from statements.
- **Current ratio** = Total Current Assets / Total Current Liabilities (liquidity measure; very high or <1 are warning signs).
- **Return on Equity (ROE)** = Net Income / Total Equity × 100 (profitability-to-equity).
- **Debt-to-Equity (D/E)** = Long Term Debt / Total Equity (leverage/risk measure).
- Reusing the `get_fundamental_data()` helper to compute ratios.
**Prereqs:** notebook 12; ratio arithmetic; interpreting statements.
## 14. Stock Fundamental Data / Other Company Data
**Concepts:**
- Fetching company calendar/action events from `yfinance`.
- **Earnings calendar** dates: schedule when companies announce period earnings.
- **Corporate actions** (dividends, stock splits): dividend = distribution of earnings to shareholders; split = shares increased by a multiple while price decreases by same factor.
- Observation: dividends occur more frequently than splits (quarterly vs requiring board approval).
- Interpreting these as fundamental/qualitative market signals.
**Prereqs:** notebook 12; corporate-filings vocabulary.
## 15. Data Quality Checks and Data Cleaning / Basic Data Quality Checks and Data Cleaning
**Concepts:**
- Cleaning data quality is a prerequisite for reliable analysis/model output.
- **Explore** data first: `head()`/`tail()`, `info()` (column names, types, non-null count), and rows count.
- Detect **null values** directly with `.isna().sum()`.
- Handle missing values: `dropna(inplace=True)`; dropping feasible only when the missing fraction is small (otherwise biases/shortens). `shape` to confirm before/after.
- Detect **duplicates** with `duplicated().value_counts()`; rule-of-thumb tolerance (~0.5%); examine and drop consecutive duplicates.
- Detect **outliers** by plotting percentage change of price; spikes betray erroneous values.
**Prereqs:** pandas cleaning; bias/mean intuition.
Build outputs: This course is a data-fetching survey. Each subsequent notebook also carries recurring concepts of reading CSV via `pd.read_csv()`, plotting, and reusing the shared data/utils module. Results were extracted from the Jupyter notebook sources' markdown cells.


====================
Getting-Started-with-Algorithmic-Trading
====================

## COURSE: Getting Started with Algorithmic Trading
### MODULE: Introduction to Python
#### NOTEBOOK: My First Jupyter Notebook
- **Programming** — The task of telling a machine (computer/phone) what to do by writing software; synonymous with coding/developing. prereqs: none
- **Jupyter Notebook** — An interactive document combining markdown text and runnable code cells for learning/analysis. prereqs: none
- **Code cells & Markdown cells** — Two cell types in a notebook; markdown holds explanatory text, code holds executable Python. prereqs: Jupyter Notebook
- **Shift+Enter to run a cell** — The keyboard shortcut that executes the current notebook cell. prereqs: Jupyter Notebook
- **Simple Python syntax** — Python reads like English, prioritising coding productivity and readability; portable across platforms. prereqs: none
- **Code comments (#)** — Non-executable notes prefixed with `#` that explain code and are ignored when run; anything after `#` is commented out. prereqs: Python syntax
- **Multi-line comments (triple quotes)** — Text wrapped in `"""..."""` is not executed and serves as a multi-line comment. prereqs: Python syntax
- **Print statement** — `print("...")` outputs text/values to the console. prereqs: Python syntax
- **Variables** — Named storage of values that can be reused; Python variables can hold different data types. prereqs: Programming
- **Assignment `=` semantics** — The `=` sign means "is set to", not "equal to". prereqs: Variables
- **Integer (int)** — A whole number data type, positive or negative; `type()` returns `int`. prereqs: Variables
- **Float** — A real-number (decimal) data type; defined as `5.0` or via `float(5)`. prereqs: Variables
- **String** — A data type for text (alphabets, numbers, special chars) wrapped in single or double quotes. prereqs: Variables
- **Case sensitivity** — Python distinguishes variable names differing only by case (e.g. `gold_price` vs `Gold_Price`). prereqs: Variables
- **type() function** — Built-in that returns the data type of a value/object. prereqs: Variables
- **Indentation** — Python requires consistent indentation (spaces) for block structure; inconsistent indents raise `IndentationError`. prereqs: Python syntax
- **Exponentiation operator `**`** — Raises a number to a power (e.g. `3**2 == 9`). prereqs: Python basics
- **Simple returns** — Percentage change in price over a period: `(Final/Initial - 1) * 100`. prereqs: Variables, arithmetic
- **Log returns** — Natural log of `final/initial`, computed with `math.log(price_2/price_1)`. prereqs: Simple returns, math import
- **import math** — Bringing in the standard `math` library to use functions like `log()`. prereqs: Functions, libraries
#### NOTEBOOK: Operations and Functions in Python
- **Arithmetic operators** — Basic operations `+ - * /` performed on numbers/variables. prereqs: Python basics
- **Exponentiation operator `**`** — Computes a number raised to a power. prereqs: Arithmetic
- **Modulo operator `%`** — Returns the remainder of a division (e.g. `15 % 4 == 3`). prereqs: Arithmetic
- **Built-in math functions** — `abs()`, `round()`, `max()`, `min()`, `sum()` operated on numbers. prereqs: Python basics
- **import keyword** — Loads a library (`import math`) so its functions become available. prereqs: Python basics
- **math package constants/functions** — `math.pi` (π), `math.e` (Euler's constant), `math.cos()`. prereqs: import math
- **Comparison (relational) operators** — `==`, `!=`, `<`, `>`, `<=`, `>=` return booleans `True`/`False`. prereqs: Python basics
- **Boolean results** — Logical/comparison operations evaluate to `True` or `False`. prereqs: Comparison operators
- **Logical operators** — `not` (negation), `and` (both true), `or` (either true); combined per a truth table. prereqs: Booleans
- **Equality `==`** — Compares two values, returning `True` if equal, `False` otherwise. prereqs: Comparison operators
- **Functions** — Reusable blocks of code defined with `def` that can be called repeatedly for clean, modular code. prereqs: Python syntax
- **Function definition & call** — `def name():` begins a function; calling `name()` executes its body. prereqs: Functions
- **Function parameters** — Input values placed inside parentheses in the definition, separated by commas, used by the function body. prereqs: Functions
- **return statement** — Exits a function and hands a value back to the caller for storage in an outer variable. prereqs: Functions
- **Variable scope** — The region of code where a variable is accessible; variables defined inside a function are local to it. prereqs: Functions
- **Scope error (NameError)** — Referencing a function-local variable outside raises `NameError: name not defined`. prereqs: Variable scope
#### NOTEBOOK: DataFrame and Basic Functionality
- **DataFrame** — pandas' tabular/spreadsheet-like structure storing data in named rows and columns. prereqs: Pandas
- **import pandas as pd** — Importing the pandas library under the alias `pd`. prereqs: Python
- **pd.DataFrame() constructor** — Creates a DataFrame from data (e.g. a dict of lists), optionally with index. prereqs: pandas
- **Columns & index** — Columns are named fields; the index is the row-label sequence (default 0..n). prereqs: DataFrame
- **set_index()** — Assigns a column's values as the DataFrame's index for label-based access. prereqs: DataFrame
- **pd.read_csv()** — Loads a CSV file into a DataFrame; `index_col` sets an index column. prereqs: pandas
- **head() / tail()** — Display the first/last n rows (default 5) to preview data. prereqs: DataFrame
- **loc[]** — Label-based row/index access; both start and stop labels are included. prereqs: pandas indexing
- **iloc[]** — Position-based row access by integer position (0-indexed); the stop index is excluded. prereqs: pandas indexing
- **Boolean indexing** — Filtering a DataFrame with a boolean condition (e.g. `df[df.quantity > 5000]`). prereqs: DataFrame
- **Accessing columns** — Reference a column by its name via `df["colname"]`. prereqs: DataFrame
- **drop()** — Removes rows (by index position) or columns (`axis=1`), optionally saving in place. prereqs: DataFrame
- **axis parameter** — Specifies whether to operate along rows (0/"index") or columns (1/"columns"). prereqs: pandas
- **Adding a column** — `df["new_col"] = expression` creates a computed field, e.g. a moving average. prereqs: DataFrame
- **rolling() + mean()** — The `.rolling(window=N).mean()` construct computes an N-period simple moving average. prereqs: pandas, DataFrame columns
- **Simple Moving Average (SMA)** — The mean of the last N observations at each point in a time series. prereqs: rolling()
### MODULE: Financial Market Data and Visualisation
#### NOTEBOOK: Importing Time Series Data
- **yfinance** — A Python package for fetching financial data from Yahoo Finance. prereqs: pip, Python
- **pip install** — The tool/command that installs and manages Python packages. prereqs: none
- **yf.download(ticker, start, end)** — Downloads OHLCV data for a ticker between given dates into a DataFrame. prereqs: yfinance
- **Ticker** — The exchange symbol identifying a stock/asset (e.g. 'KO' for Coca Cola). prereqs: yfinance
- **auto_adjust parameter** — When `True`, yfinance returns split/dividend-adjusted price data (default `False`). prereqs: yf.download
- **Adjusted close price** — Closing price restated for corporate actions (splits/dividends). prereqs: adjusted data
- **CSV file** — A Comma-Separated-Value text file storing tabular data; readable via `pd.read_csv()`. prereqs: pandas
- **Financial time series data** — Ordered daily price data (open/high/low/close/volume) indexed by date. prereqs: CSV
- **pd.to_datetime()** — Converts a date column/index to datetime type for easier date operations. prereqs: pandas
- **Datetime index** — Using a parsed datetime column as the DataFrame index enables time-series operations. prereqs: pd.to_datetime
#### NOTEBOOK: Data Visualisation
- **Data visualisation** — Graphical representation (charts/graphs) of data to draw insights. prereqs: none
- **matplotlib** — The Python plotting library; commonly imported as `matplotlib.pyplot as plt`. prereqs: Python
- **%matplotlib inline** — Magic command rendering graphs inline within a notebook. prereqs: matplotlib
- **plt.style.use()** — Sets a global plotting style (e.g. 'seaborn-v0_8-darkgrid'); options in `plt.style.available`. prereqs: matplotlib
- **Line graph** — A plot of a continuous series; in pandas via `dataframe.column.plot(figsize, color)`. prereqs: matplotlib
- **Plot decorators** — `plt.title()`, `plt.xlabel()`, `plt.ylabel()`, and `plt.show()` label and display a chart. prereqs: matplotlib
- **figsize & color params** — Control plot dimensions (x,y) and line colour. prereqs: line graph
- **Scatter plot** — `plt.scatter(x, y)` plots two variables against each other to study relationships. prereqs: matplotlib
- **Histogram** — `data["col"].plot(kind='hist')` shows the frequency distribution of a numeric column. prereqs: pandas plot
- **Insights from charts** — Reading ranges, co-movement, and distribution shape from plotted data. prereqs: line/scatter/hist
### MODULE: Moving Average Crossover Strategy
#### NOTEBOOK: Moving Average Crossover Strategy
- **Momentum** — Persistence of a trend/returns in a particular direction in an asset's price. prereqs: none
- **numpy (np) & pandas (pd)** — Core numerical and dataframe libraries used in strategy work. prereqs: Python
- **warnings.filterwarnings('ignore')** — Suppresses warning messages during analysis. prereqs: Python
- **Slicing data columns** — Retaining only desired columns (e.g. `data[['Adj Close']]`). prereqs: DataFrame
- **rolling()/mean() for SMA** — Computes short- and long-term moving averages with window sizes. prereqs: pandas rolling
- **Short-term vs long-term window** — Window sizes (40 and 70 days) defining fast vs slow averages. prereqs: rolling()
- **Moving-average crossover logic** — Buy when the short-term average rises above the long-term average; sell when it falls back. prereqs: moving averages
- **np.where(condition, if_true, if_false)** — Element-wise array selection assigning signal values (1 buy / −1 sell). prereqs: numpy
- **shift() to lag signals** — Shifting the signal forward one day so the trade executes the next day, avoiding lookahead. prereqs: pandas
- **Replace NaN with 0** — `series.replace(np.nan, 0)` cleans the first-day missing signal value. prereqs: pandas
- **pct_change()** — Computes the daily percentage change `(today - yesterday)/yesterday`. prereqs: pandas
- **Strategy returns** — Daily strategy return = signal (previous day) × daily price change. prereqs: pct_change
- **Trading cost / commission** — Charging a fixed commission on position changes: `0.001*|signal - shifted-signal|`. prereqs: strategy returns
- **Buy & hold strategy** — Simply purchasing and holding the asset; used as a comparison baseline. prereqs: none
- **Cumulative returns** — Running product of `(1+return)` via `.cumprod()`, showing total growth over time. prereqs: strategy returns
- **prod()** — Multiplicative product of all elements, giving the final cumulative growth factor. prereqs: cumprod
- **Yearly annualisation (252)** — Multiplying daily stats by `sqrt(252)` to annualise to ≈ number of trading days/year. prereqs: Sharpe ratio
- **Standard deviation (risk)** — Measures average dispersion/movement of prices; proxies uncertainty/risk. prereqs: statistics
- **Sharpe ratio** — Average excess return per unit of risk: `(mean / std) * sqrt(252)`. prereqs: mean, std, annualisation
- **Drawdown** — Decline of cumulative returns from a previous running peak, quoted as a percentage drop. prereqs: cumulative returns
- **Cumulative maximum** — `np.maximum.accumulate()` tracks the running maximum of a series (peak). prereqs: numpy
- **Maximum drawdown** — The deepest peak-to-trough percentage loss of the equity curve. prereqs: drawdown
- **plt.fill_between()** — Shading the area under a drawdown curve to visualise loss regions. prereqs: matplotlib
---
## Getting-Started-with-Algorithmic-Trading — Section-based course structure
# Concept Inventory — Getting Started with Algorithmic Trading
## COURSE: Getting Started with Algorithmic Trading
### Section: Section 1 - Introduction
- **Introduction / course structure:** overview of what algorithmic trading is and how the course is organised. prereqs: none.
### Section: Section 2 - What is Algorithmic Trading
- **What is algorithmic trading:** using automated programs executing trades based on predefined rules. prereqs: none.
- **Direct Market Access (DMA):** connecting directly to an exchange to place orders with reduced latency. prereqs: algo trading.
- **What is high-frequency trading (HFT):** ultra-fast automated trading exploiting small latency advantages. prereqs: algo trading; DMA.
### Section: Section 3 - Why Algorithmic Trading
- **Why go algo (parts 1–3):** benefits — speed, discipline, backtestability, removal of human emotion. prereqs: what is algo.
- **How to start algorithmic trading:** practical first steps (learning, platforms, small strategies). prereqs: why algo.
### Section: Section 4 - Available Platforms & Languages
- **Available platforms & languages:** Python, C++, R, broker APIs, backtesting libraries. prereqs: what is algo.
### Section: Section 5 - Strategy Paradigms
- **Types of algorithmic trading strategies:** broad taxonomy. prereqs: what is algo.
- **Market making strategy:** posting bids/asks to profit from the spread. prereqs: strategy types.
- **Momentum based strategies:** trading on trend/momentum signals. prereqs: strategy types.
- **Statistical arbitrage:** exploiting statistical mispricings between related instruments. prereqs: strategy types.
- **Machine-readable news & ML:** using news & machine learning in strategies. prereqs: strategy types.
### Section: Section 6 - Algorithmic Trading Platform
- **Algorithmic Trading Platform (ATP):** three core functions — receive data, analyse/decide, place orders. prereqs: what is algo.
- **Server:** core hardware/software infra of an ATP. prereqs: ATP.
- **Market Data Adapter (MDA):** handles incoming exchange data feeds. prereqs: ATP; server.
- **Complex Event Processing (CEP) Engine:** real-time analysis/decision engine. prereqs: ATP.
- **Order Routing/Management System (OMS):** routes and manages orders to exchange. prereqs: ATP; server.
### Section: Section 8 - Financial Market Data and Visualisation
- **Importing data:** fetching price/volume/fundamental data via Python APIs. (Financial Market Data) prereqs: Python basics.
- **Market data & analysis in Python:** working with price, volume, fundamental data. prereqs: importing data.
- **Data cleaning basics:** handling incomplete/erroneous data. prereqs: importing data.
- **Data sources:** free vs paid market data APIs; fundamental & sentiment feeds. prereqs: importing data.
### Section: Section 9 - Moving Average Crossover Strategy
- **Moving average crossover strategy:** long/short on short-period MA crossing long-period MA. prereqs: market data; strategy paradigms.
### Section: Section 12 - Regulations & Compliance (Optional Section)
- **Regulations & compliance (SEBI, India):** audit requirements, order limits (>20/s penalised), India-routed orders, approved IDs. prereqs: algo trading foundations.
- **Global regulation snapshots:** EU, US algo/commodity (CFTC/CME) regulations. prereqs: regulations.
### Section: Section 14 - Summary
- **Summary / course recap:** recap of all concepts, trading desk FAQ. prereqs: all sections.
- **Setting up a trading desk (FAQs):** capital, licensing, infrastructure, human-resource skills (stats, programming, markets, compliance). prereqs: summary.
- **Handbook:** × MCX intro reference. prereqs: none (annexure).
## Course Prerequisite Map
- Foundations: *What is Algo → DMA → HFT; Why Algo → How to start.*
- Platforms: *Available Platforms → Strategy Paradigms → Moving Average Crossover (needs returns + MA).*
- Infrastructure: *What is Algo → ATP (Server → MDA/CEP/OMS).*
- Data: *Python basics → Importing Data → Market Analysis → Visualisation.*
- Compliance is optional and standalone (after fundamentals).
- Course flow: **Intro → What is Algo/DMA/HFT → Why → Platforms → Strategy Paradigms → Platform Architecture → Market Data → MA Crossover → [Regulations] → Summary/Handbook.**
- FunPath basics feeding this course: Python for trading, return calculation, moving averages, basic market structure.


====================
Introduction-to-Machine-Learning-for-Trading
====================

# Introduction to Machine Learning for Trading — Concept Inventory
> Scope: supervised machine-learning classifiers/regressors for price-direction and return prediction on S&P 500 (SPY) data.
> Modules/notebooks enumerated: **7** | Data: `data/SPY.csv`, `data/BAC_2010_2021.csv` | Module files: `ReadMe.html`, `Folder Structure and How to Run Code Files.html`
---
## Module: Supervised Learning
### 1. `Linear Regression.ipynb`
Statistical/ML baseline for predicting a real-valued target from inputs.
**Concepts (with prerequisites):**
- **Linear regression model equation** — y = β₀ + β₁x₁ + β₂x₂ + … + ε; output is a weighted sum of inputs.
 - *Prereq:* basic algebra, equation of a line, what a coefficient/slope means.
- **Supervised learning framing** — model learns a mapping from inputs X to output y using labelled examples (X, y pairs).
 - *Prereq:* none.
- **Features (independent variables)** — input columns used to predict; here `prev_day_returns` (previous day's return) built via `pct_change()` and `shift()`.
 - *Prereq:* what a feature/predictor is; pandas column math.
- **Target (dependent variable)** — the outcome being predicted; here today's `return`.
 - *Prereq:* none.
- **Feature engineering from prices** — computing daily returns as `Close.pct_change()` and shifting to lag returns (prevents look-ahead bias).
 - *Prereq:* understanding of prices vs returns, time lags.
- **Train–test split (time-ordered)** — keeping chronological order and holding out the last 20% as test; no shuffling because of temporal data.
 - *Prereq:* why we need held-out data for honest evaluation.
- **Fitting a model** — `LinearRegression().fit(X_train, y_train)` learns coefficients; `predict(X_test)` gets predictions.
 - *Prereq:* what training/fitting means.
- **Regression metrics — Mean Squared Error (MSE)** — average of squared errors; larger = worse fit.
 - *Prereq:* concept of prediction error/residuals.
- **R² score (coefficient of determination)** — proportion of variance explained; 1.0 = perfect fit, ≤0 = worse than the mean. Here ~0.05, interpreted as underfitting.
 - *Prereq:* variance, correlation intuition.
- **Regression line visualisation** — plotting fitted line over data points.
 - *Prereq:* scatter plot reading.
### 2. `Random Forest.ipynb`
Ensemble of decision trees for classification (also regression).
**Concepts (with prerequisites):**
- **Random Forest (Random Decision Forest)** — ensemble method combining many decision trees; for classification each tree "votes" and majority wins; for regression outputs are averaged.
 - *Prereq:* what a decision tree is, majority voting, averaging.
- **Decision trees / CART model** — trees of decisions; single tree aggregated into the forest.
 - *Prereq:* none.
- **Bagging (bootstrap sampling)** — each tree trained on a random sample with replacement of N cases.
 - *Prereq:* random sampling, "with replacement".
- **Random feature subsampling** — at each split, only m of M total input variables considered; m held constant while trees grow.
 - *Prereq:* none.
- **Classification vs regression usage of Random Forest** — classifier predicts class labels; regression averages outputs.
 - *Prereq:* classification vs regression distinction.
- **Features (independent variables)** — here 4: `Open/Close`, `High/Low` ratios, 1-day lag returns, 2-day lag returns.
 - *Prereq:* ratio/indicator construction from OHLC data.
- **Target (dependent variable)** — binary signal: +1 if tomorrow's close > today's close, else −1 (via `np.where`).
 - *Prereq:* classification labels, forward-looking signal.
- **Train–test split (75/25, time-ordered)** — first 75% train, last 25% test.
 - *Prereq:* train/test split rationale.
- **Model fitting** — `RandomForestClassifier(random_state=5).fit(X_train, y_train)`; `random_state` for reproducibility.
 - *Prereq:* what fitting does, seed/reproducibility.
- **Classification metric — accuracy score** — fraction of correct predictions out of total.
 - *Prereq:* none.
- **Out-of-bag (OOB) error advantage** — reduces need for a separate validation split.
 - *Prereq:* validation set concept (advanced).
- **Advantages** (error balancing, missing-data robustness, feature-importance/outlier use) and **disadvantages** (poor continuous extrapolation, limited range beyond training data).
 - *Prereq:* none.
### 3. `KNN_Classification.ipynb`
K-Nearest Neighbours — a lazy, distance-based classifier.
**Concepts (with prerequisites):**
- **K-Nearest Neighbours (KNN) classifier** — classifies a point by the majority class of its k closest training neighbours; decision based on local distance.
 - *Prereq:* Euclidean distance intuition, majority voting.
- **Features (lagged returns)** — `1_day_lag_returns` and `2_day_lag_returns` from `Close.pct_change().shift()`.
 - *Prereq:* feature engineering, lags, look-ahead avoidance.
- **Target variable** — binary: 1 if today's return > 0 else 0.
 - *Prereq:* binary classification.
- **Time-ordered train/test split** — last 20% test, respecting chronological order.
 - *Prereq:* why we don't shuffle time series.
- **Model instantiation & fit** — `KNeighborsClassifier()` with default k=5; `fit(X_train, y_train)`.
 - *Prereq:* k hyperparameter concept.
- **Prediction & evaluation** — `predict(X_test)`, `accuracy_score`, `confusion_matrix`.
 - *Prereq:* accuracy, confusion matrix (TP/FP/TN/FN).
- **Decision-region plot** — shaded regions where model predicts class 0 vs 1; "island-like" non-linear boundaries typical of KNN.
 - *Prereq:* scatter plots, decision boundary intuition.
- **Confidence interpretation** — points far from boundary more confident; near boundary uncertain.
 - *Prereq:* probability/confidence intuition.
### 4. `SVM_Trading.ipynb`
Support Vector Machine — max-margin linear classifier.
**Concepts (with prerequisites):**
- **Support Vector Machine (SVM)** — finds a hyperplane separating classes that **maximises the margin** to the closest points (support vectors).
 - *Prereq:* 2D geometry of a line, distance to a line, maximisation.
- **Hyperplane / decision boundary** — the separating line (2D) or plane (3D) where the SVM score = 0.
 - *Prereq:* none.
- **Margins and support vectors** — dashed lines at score = ±1; support vectors lie on/inside margins and determine boundary.
 - *Prereq:* none.
- **Kernel (here linear)** — `SVC(kernel='linear')` draws a straight-line boundary; other kernels extend to non-linear data.
 - *Prereq:* what linear vs non-linear means.
- **Regularization parameter C** — `C=1.0`; lower C → wider margin/more regularisation; higher C → tighter fit to training data.
 - *Prereq:* bias–variance / overfitting idea.
- **Features** — two lagged returns; **target** — binary direction (1 if return > 0).
 - *Prereq:* features, target, labels.
- **Train–test split (time-aware, last 20% test)**.
 - *Prereq:* train/test split.
- **Model coefficients** — `coef_` and `intercept_` define the boundary for linear kernel.
 - *Prereq:* equation of a line from weights.
- **Evaluation** — test accuracy (0.625) and confusion matrix; note class-imbalance pitfall (all predictions one class while still ~62%).
 - *Prereq:* accuracy, confusion matrix, class imbalance.
- **`decision_function`** — signed distance from boundary; sign gives class, magnitude gives confidence.
 - *Prereq:* distance to a hyperplane.
### 5. `Logistic Regression.ipynb`
Linear model for **binary classification** via the sigmoid function.
**Concepts (with prerequisites):**
- **Logistic (sigmoid) function** — y = 1/(1 + e^(−x)); S-shaped curve squashing any input to (0,1), the probability of the positive class.
 - *Prereq:* exponential function, graphing a curve.
- **Classification vs regression** — despite the name, logistic regression is a **classifier** for a categorical/binary dependent variable (0/1, −1/1, True/False).
 - *Prereq:* classification vs regression distinction.
- **From linear to logistic regression** — computes a weighted sum of inputs (like linear regression) then passes it through the sigmoid to get a probability.
 - *Prereq:* linear regression, weighted sum.
- **Decision boundary** — the straight line where P(up) = 0.5; axis of the two lagged-return features.
 - *Prereq:* linear boundary, probability = 0.5 threshold.
- **Features** — `1_day_lag_returns`, `2_day_lag_returns` (prior days' returns to prevent look-ahead).
 - *Prereq:* feature engineering, lags.
- **Target** — binary `(return > 0).astype(int)`.
 - *Prereq:* binary labels.
- **Train–test split** — last 20% kept chronological as test.
 - *Prereq:* train/test split.
- **Regularization parameter C** — `LogisticRegression(C=1e5)`; high C gives training data more weight than the complexity penalty.
 - *Prereq:* regularization intent.
- **`predict` vs `predict_proba`** — class labels vs `P(up)` for each day.
 - *Prereq:* class vs probability output.
- **Metrics — accuracy and confusion matrix** — overall hit rate; rows=true class, columns=predicted class (TN/FP/FN/TP).
 - *Prereq:* accuracy, confusion matrix.
- **Decision-region visualisation** — shaded class regions, test points, straight separating line.
 - *Prereq:* scatter/contour plots.
- **Limitations** — accuracy inflated by class imbalance; teaching demo only.
 - *Prereq:* class imbalance.
### 6. `Artificial Neural Network.ipynb`
Multi-Layer Perceptron (MLP) classifier.
**Concepts (with prerequisites):**
- **Artificial Neural Network (ANN)** — supervised learning loosely inspired by the brain; nodes (neurons) connected by links pass and transform data.
 - *Prereq:* none.
- **Architecture — input/hidden/output layers** — input layer, one or more hidden layers, output layer; each layer has nodes; fully connected between adjacent layers.
 - *Prereq:* none.
- **Multi-Layer Perceptron (MLP)** — a neural network with multiple fully-connected layers of nodes.
 - *Prereq:* what a layer is.
- **Weights and bias** — each link has a weight; algorithm adjusts weights during training based on errors.
 - *Prereq:* what a weight does (analogous to β coefficients in linear regression).
- **Backpropagation and gradient descent** — gradients computed by backpropagation; weights updated via gradient descent to minimise loss.
 - *Prereq:* partial derivatives, gradient (introductory).
- **Loss: Cross-Entropy** — default loss for classification; produces per-sample class probability vectors via `predict_proba`.
 - *Prereq:* probability, what a loss function is.
- **Model parameters (coefs_)** — weight matrices; shapes show layer connectivity, e.g. `[(2,5),(5,2),(2,1)]`.
 - *Prereq:* matrix shape/size.
- **Hyperparameters** — `hidden_layer_sizes=(5,2)`, `solver='lbfgs'`, `alpha` (regularization), `random_state`.
 - *Prereq:* what a hyperparameter is.
- **`fit` / `predict` / `predict_proba`** — train, label new samples, output class probabilities.
 - *Prereq:* model lifecycle API.
- **Feature/label arrays** — X shape `(n_samples, n_features)`, y shape `(n_samples)`.
 - *Prereq:* matrix/array dimensions.
---
## Module: Predict Trend Using Classification
### 7. `Support Vector Classifier Strategy.ipynb`
End-to-end SVC trading-signal pipeline (S&P 500 / SPY).
**Concepts (with prerequisites):**
- **Support Vector Classifier (SVC)** — SVM used for classification; finds a hyperplane separating classes (max-margin).
 - *Prereq:* SVM, hyperplane, margin (see notebook 4).
- **Hyperplane dimensionality** — hyperplane dimension = number of features − 1 (line in 2D, plane in 3D).
 - *Prereq:* coordinate geometry.
- **Features (explanatory variables)** — `Open/Close` and `High/Low` ratios as indicator-like predictors; choice described as somewhat arbitrary (can extend).
 - *Prereq:* OHLC data, ratio indicators.
- **Target (dependent variable / signal)** — +1 buy signal if tomorrow's close > today's close, −1 otherwise; built with `np.where(condition, if_true, if_false)`.
 - *Prereq:* numpy `np.where`, forward-looking labels.
- **Train–test split** — first 80% train, last 20% test (chronological).
 - *Prereq:* train/test split, no look-ahead.
- **Model training** — `SVC().fit(X_train, y_train)`; `predict(X_test)` for signals.
 - *Prereq:* fit/predict API.
- **Classifier accuracy** — `accuracy_score(y_true, y_pred)` on both train and test; ~58% test accuracy interpreted as above chance (effective classifer).
 - *Prereq:* accuracy metric.
- **Strategy implementation & backtest-style returns** — generate `Predicted_Signal` on full data, compute daily `Returns = Close.pct_change()`, strategy returns = `Returns * signal.shift(1)`, geometric cumulative returns via `.cumprod()`.
 - *Prereq:* log/simple returns, `shift()` to avoid look-ahead, cumulative product.
- **Signal shifting** — `shift(1)` applies today's signal from the previous bar's close (avoids look-ahead).
 - *Prereq:* time lags, look-ahead bias.
- **Cumulative-returns visualisation** — plot of strategy equity/returns over test period (~10% return).
 - *Prereq:* line plots, compounding returns.
- **Model iteration / tweaking** — trying different datasets and engineered indicators to improve accuracy.
 - *Prereq:* none.


====================
Machine-Learning-for-Options-Trading
====================

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


====================
Natural-Language-Processing-in-Trading
====================

# Natural Language Processing in Trading — Concept Inventory
## COURSE: Natural Language Processing in Trading
Scope: convert financial news headlines into numeric features (BoW, TF-IDF, Word2Vec, BERT), predict sentiment class with XGBoost, aggregate per-day sentiment scores, and build sentiment-based trading strategies on AAPL stocks and bonds. Includes a live-data capstone and news-data collection APIs.
---
## MODULE: Sources of News Headline Data
### LESSON: Sources of News Headline Data.ipynb
- **News headline sentiment dataset:** CSV (`news_headline_sentiments.csv`) containing `news_headline`, `time_stamp`, `URL`, `source_id`, `sentiment_class`, and `sentiment_scores` columns — the raw input for the whole course. prereqs: CSV, pandas DataFrame
- **Chunked CSV reading:** `pd.read_csv(..., chunksize=...)` reads a huge dataset in manageable pieces iterated with a for loop. prereqs: CSV, iterables
- **Data cleaning / drop missing values:** `df.dropna()` removes rows with nulls before filtering. prereqs: DataFrame
- **Lowercasing text:** `df.news_headline.str.lower()` normalizes casing so keyword matching works regardless of case. prereqs: string casing, text preprocessing
- **Keyword filtering by substring:** `df.loc[df.news_headline.str.contains('apple')]` selects only headlines mentioning a target ticker/company. prereqs: boolean masks, regular substring match
- **Data concatenation:** `pd.concat([...])` combines filtered per-chunk dataframes into one full frame. prereqs: two dataframes
- **Word/headline frequency counting:** counting rows per ticker (e.g. aapl/amzn/msft) to gauge data availability. prereqs: `len()` on DataFrame, dict
- **CSV export:** `df.to_csv(...)` persists filtered data (e.g. `news_headline_sentiments_aapl.csv`) for downstream use. prereqs: CSV writing, pandas
---
## MODULE: Bag of Words
### LESSON: Bag of Words Calculation.ipynb
- **Bag of Words (BoW):** the simplest way to convert text into a numeric vector by counting word frequency per document — ignores word order. prereqs: corpus, words
- **Corpus:** a collection of text documents (here a list of sentences) used as input. prereqs: Python list, text
- **Tokenization:** splitting a document into its constituent tokens/words — CountVectorizer does this internally. prereqs: words, text
- **CountVectorizer (sklearn):** `from sklearn.feature_extraction.text import CountVectorizer`; fits a vocabulary and counts occurrences to build a document-term frequency matrix. prereqs: BoW concept
- **fit_transform:** fits the vectorizer on the corpus and transforms it into the count matrix in one call. prereqs: CountVectorizer, fit/transform
- **Feature / vocabulary extraction:** `cv.get_feature_names_out()` returns the learned word features (unique terms). prereqs: CountVectorizer
- **Document-term matrix:** counts laid out as a DataFrame (rows=documents, columns=terms); note `toarray()` converts the sparse output to a dense array. prereqs: sparse matrix, DataFrame
- **Default CountVectorizer preprocessing:** by default everything is lowercased, words < 2 letters are dropped, punctuation is removed, and duplicate tokens are collapsed. prereqs: CountVectorizer, text preprocessing
---
## MODULE: TF-IDF
### LESSON: TF-IDF Calculation.ipynb
- **Term Frequency (TF):** how many times a word appears in a document — same as the BoW count. prereqs: BoW
- **Inverse Document Frequency (IDF):** measures a word's significance; the more documents a word appears in, the less significant it is. prereqs: term frequency, document frequency
- **IDF formula:** `IDF = log(N / df(t))` where N is the number of documents and df(t) the count of documents containing term t. prereqs: logarithms, document frequency
- **Smoothed IDF:** sklearn uses `1 + log(N/df(t))` so terms appearing in every document (IDF=0) are still given weight. prereqs: IDF formula, log
- **TfidfTransformer:** sklearn component that takes a count matrix and re-weights it into TF-IDF values via `fit`/`transform`. prereqs: CountVectorizer output, TF-IDF
- **TfidfVectorizer (direct):** computes TF-IDF from raw text directly (`fit_transform`) instead of counting first. prereqs: TF-IDF, vectorizer
- **TF-IDF product rule:** TF-IDF score = TF × IDF per term. prereqs: TF, IDF
- **stop_words removal:** `stop_words='english'` strips common words (the, and, of...) that carry little meaning. prereqs: tokenization, BoW
- **L1 / L2 normalization:** `norm='l2'` (default) scales each row to unit length; `norm='l1'` scales absolute values to sum to 1 — prevents long documents dominating. prereqs: norm, vector math
- **smooth_idf & use_idf flags:** `smooth_idf=False` uses the unsmoothed IDF; `use_idf=True` enables IDF re-weighting. prereqs: IDF
### LESSON: TF-IDF to XGBoost.ipynb
- **TF-IDF → XGBoost pipeline:** feed TF-IDF vectors into XGBClassifier to predict sentiment, mirroring the BoW workflow. prereqs: TF-IDF, XGBClassifier
- **Sentiment target mapping:** map sentiment labels `{-1,0,1}` → `{0,1,2}` so they fit classifier conventions. prereqs: label encoding, sentiment class
- **Predictor / target variables:** `X` = news headlines, `y` = sentiment_class (dependent variable predicted from independent features). prereqs: ML features/labels
- **train/test split:** split data (80% train / 20% test); use `fit_transform` on train and only `transform` on test (never refit on test). prereqs: overfitting, fit/transform
- **XGBClassifier fit & predict:** `XGBClassifier(max_depth=6, n_estimators=100, eval_metric='mlogloss')` then `.fit()` on train and `.predict()` on test. prereqs: gradient boosting, classification
- **accuracy_score:** fraction of correct predictions on the test set (≈0.709 here). prereqs: classification metrics
---
## MODULE: Predicting Sentiment Score Using XGBoost
### LESSON: BoW to XGBoost.ipynb
- **Sentiment classification task:** predict the sentiment class of a news headline (positive/neutral/negative) — a 3-class supervised classification problem. prereqs: classification, sentiment
- **Target variable y:** `sentiment_class` remapped from `{-1,0,1}` to `{0,1,2}`. prereqs: label encoding
- **Predictor variable X:** the raw `news_headline` strings, coerced to `str`. prereqs: ML feature columns
- **train/test split:** 80/20 ratio; recommended to keep ≥ 60% for training. prereqs: overfitting, holdout
- **Bag-of-Words vectorization with stopwords:** `CountVectorizer(stop_words='english', lowercase=True)`, fit on train, transform on test. prereqs: BoW, stop words
- **XGBClassifier hyperparameters:** `max_depth` (limits tree/node depth) and `n_estimators` (number of boosted trees), `eval_metric='mlogloss'` for multi-class. prereqs: XGBoost, decision trees
- **Model fitting & prediction:** `xg.fit(X_new_train, y_train)` then `xg_model.predict(X_new_test)`. prereqs: XGBClassifier
- **Confusion matrix:** `sklearn.metrics.confusion_matrix` shows true-vs-predicted counts per class for a classification model. prereqs: classification metrics
- **Classification report:** `classification_report` summarizes precision, recall, and F1-score per class. prereqs: precision/recall/F1
- **Prediction accuracy:** `accuracy_score(y_test, prediction)` — ≈0.725 here. prereqs: accuracy metric
---
## MODULE: WordVec
### LESSON: Basic Implementation.ipynb
- **Word embeddings:** dense vector representations of words learned from corpora, where similar words map near each other. prereqs: vectors, text
- **Word2Vec (gensim):** `gensim.models.Word2Vec` learns word vectors from tokenized text (a neural embedding model). prereqs: word embeddings, gensim
- **NLTK tokenization:** `nltk.download('punkt')` + `word_tokenize` split each headline into a list of word tokens. prereqs: tokenization, nltk
- **Tokenized corpus input:** Word2Vec takes a list of lists of words (tokenized sentences) as training input. prereqs: tokenization, Word2Vec
- **min_count parameter:** `Word2Vec(tokens, min_count=2)` keeps only words appearing at least twice in the corpus. prereqs: Word2Vec, corpus frequency
- **Vector dimensionality:** `size=300` sets 300-dimensional word vectors. prereqs: vector dimensions
- **Word similarity:** `word2vec.wv.similarity('United','States')` returns cosine-style similarity between word vectors. prereqs: word vectors, similarity
- **most_similar:** `word2vec.wv.most_similar('Stock')` returns nearest-neighbor words ranked by similarity. prereqs: word vectors, similarity
- **Word vector retrieval:** `word2vec.wv['states']` gives the 300-dim vector for a word. prereqs: word vectors, numpy array
- **Sentence vector:** `word2vec.wv[sentence]` stacks each word's vector into a sentence matrix. prereqs: word vectors, matrices
- **Average sentence vector:** `np.average(np.vstack(sentence_vector), axis=0)` collapses word vectors to one mean vector per sentence. prereqs: numpy, averaging, matrices
- **Data pre-processing for Word2Vec:** sort by timestamp, keep headline+sentiment columns, drop duplicates and missing values. prereqs: pandas, data cleaning
- **Chunked data ingestion:** read the large CSV in 50k-row chunks. prereqs: CSV, pandas chunks
### LESSON: Word2Vec Using Google Model.ipynb
- **Pre-trained Google News Word2Vec:** load Google's large pre-trained model via `gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300-SLIM.bin', binary=True)`. prereqs: Word2Vec, model files
- **KeyedVectors:** gensim class for loading/inspecting pre-trained word vectors without the training model. prereqs: gensim, pre-trained embeddings
- **Pre-trained similarity lookup:** `word2vec.most_similar('Stock')` and `word2vec.similarity('Cat','Australia')` on the Google vocabulary. prereqs: word vectors, similarity
- **Pre-trained word vector:** `word2vec['states']` retrieves the 300-dim vector. prereqs: KeyedVectors
- **Pre-trained sentence vector:** `[word2vec[x] for x in sentence_token]` then average over dimensions (results in a 300-dim vector). prereqs: word vectors, averaging, numpy
### LESSON: Word2Vec to XGBoost.ipynb
- **Embedding averaging function:** `create_vector(words, model, num_features)` sums word vectors present in the model and divides by count to get a headline vector. prereqs: word embeddings, numpy
- **Sentence-to-vector helper:** `create_vector_from_news_headline` builds a matrix of averaged vectors for a whole set of headlines. prereqs: create_vector, matrices
- **Feature/target extraction:** `get_feature_and_target_variable` tokenizes lowercased headlines keeping only in-vocabulary words, then produces X (vectors) and y (class). prereqs: tokenization, word vectors
- **Incremental model training:** feed chunks sequentially, using `xg.fit(X, y, xgb_model=xg.get_booster())` to continue boosting from the previous model — enables training on data larger than memory. prereqs: XGBoost, boosting, chunks
- **XGBClassifier on embeddings:** `XGBClassifier(max_depth=5, n_estimators=20, learning_rate=0.50, eval_metric='mlogloss')`. prereqs: gradient boosting, hyperparameters
- **Class remapping function:** `remap()` converts predicted/actual labels back from `{0,1,2}` to `{-1,0,1}`. prereqs: label encoding
- **Confusion matrix / classification report:** evaluate Word2Vec-based predictions; the model here predicts only the neutral class, showing Word2Vec works poorly on sentences. prereqs: classification metrics
- **Word2Vec limitation:** works well on individual words but not on whole sentences (no context handling) → motivates context-aware BERT. prereqs: Word2Vec, sentence embeddings
---
## MODULE: BERT
### LESSON: Implementation of BERT Model.ipynb
- **BERT (Bidirectional Encoder Representations from Transformers):** a Google NLP model trained bidirectionally so it understands word context (e.g. differentiates "bucket list" from "bucket of water"). prereqs: word embeddings (Word2Vec), transformers
- **BERT training data:** pretrained on Wikipedia (≈2.5B words) + BookCorpus (≈800M words). prereqs: BERT, language models
- **BERT model sizes:** Base (12-layer, 768-hidden, 12-heads, 110M params) vs Large (24-layer, 1024-hidden, 16-heads, 340M params); case-preserved and uncased variants. prereqs: transformer architecture, parameters
- **BERT as a Service:** `from bert_serving.client import BertClient` exposes a running BERT server over a client; `encode()` converts sentences to fixed-length vectors with little code. prereqs: client-server, BERT
- **BERT word embeddings:** `bc.encode(news_headline)` returns a 768-dim vector per sentence (here shape (2, 768)). prereqs: BertClient, embeddings
- **Uncased BERT + context awareness:** encoding news headlines to feed a downstream classifier. prereqs: BERT embeddings, XGBoost
### LESSON: BERT to XGBoost.ipynb
- **BERT-embedding features:** use `BertClient.encode` to produce the feature matrix `X` from the headline column. prereqs: BERT embeddings, feature engineering
- **BERT + XGBoost classifier:** `XGBClassifier(max_depth=5, n_estimators=20, learning_rate=0.50, eval_metric='mlogloss')` trained on BERT vectors. prereqs: XGBClassifier, BERT
- **Incremental training with embeddings:** same `xgb_model=xg.get_booster()` chunked-boosting pattern on BERT vectors. prereqs: incremental training, XGBoost
- **Target remapping:** `y = df[sentiment_column].replace(-1, 2)`. prereqs: label encoding
- **Confusion matrix / classification report:** evaluate the BERT-featured model on the test set. prereqs: classification metrics
---
## MODULE: Sentiment Score and Strategy Logic
### LESSON: Calculate Daily Sentiment Score in Python.ipynb
- **Daily sentiment score:** the mean of `sentiment_class` for all headlines mapped to one trading day — the signal that drives strategies. prereqs: mean, sentiment class
- **Trading time assignment (`get_trade_open`):** maps each headline timestamp to the market-open time when it should be used for trading. prereqs: datetime, market hours
- **Market open/close times:** US session 09:30 open / 16:00 close, used as boundaries for headline bucketing. prereqs: market hours, datetime
- **Business-day offset (BDay):** `from pandas.tseries.offsets import BDay` computes previous/next business/trading days (skipping weekends). prereqs: pandas offsets, trading calendar
- **Previous-day close / next-day open:** computed to decide which day's session a headline belongs to. prereqs: BDay, datetime arithmetic
- **Headline bucketing rule:** headlines made after previous close and before today's open → today's open; after today's close and before next open → next day's open; headlines during market hours are ignored. prereqs: conditional logic, trading sessions
- **Grouped mean aggregation:** `data.groupby('trading_time').sentiment_class.agg('mean')` yields one score per session — "one approach"; more refined scores can ignore weak headlines. prereqs: groupby, aggregation
- **Date normalization:** floor timestamps to day, strip timezone, set Date as index for clean visualization. prereqs: pandas datetime, tz handling
- **Persist score:** `to_csv('apple_daily_sentiment.csv')` for reuse in strategies. prereqs: CSV writing
---
## MODULE: Sentiment Strategy on Stocks
### LESSON: Sentiment Strategy on Stocks.ipynb
- **Sentiment-based trading signals:** a `signal` column where score ≥ 0.25 → buy (1), score ≤ −0.25 → sell (−1), else neutral (0); thresholds are arbitrary/tunable. prereqs: sentiment score, thresholding
- **Data merging:** `aapl_stock_data.merge(sentiment_df, on='Date')` joins daily prices with daily sentiment on matching dates. prereqs: DataFrame merge, key column
- **Open-to-open returns:** `prices['Open'].pct_change()` computes daily returns between consecutive opens. prereqs: returns, prices
- **Signal lagging (avoid lookahead):** `strategy_return = signal.shift(1) * return` trades on yesterday's signal, holding through today's return. prereqs: pandas shift, lookahead bias
- **Cumulative strategy returns:** `(strategy_return + 1).cumprod()` compounds returns to an equity curve. prereqs: compounding, cumulative product
- **Sharpe ratio:** annualized `(mean excess return / std) × sqrt(252)`, using a 2% risk-free rate and 252 trading days → ≈0.88 here. prereqs: risk-free rate, standard deviation, annualization
---
## MODULE: Sentiment Strategy on Bonds
### LESSON: How to Calculate Bond Returns_.ipynb
- **Bond data fields:** bid/ask/mid OAS, bid/ask/mid price and yield, coupon, maturity, duration from an AAPL bond CSV. prereqs: bonds, market data
- **Option-Adjusted Spread (OAS):** measure of the bond's spread over a risk-free benchmark after adjusting for embedded options; `bid_oas`/`ask_oas`/`mid_oas`. prereqs: bond spreads, options
- **Daily OAS change:** `mid_oas.diff()` = today's OAS minus previous day's, used as the driver of bond returns. prereqs: pandas diff, spreads
- **Bond duration:** weighted average time until a bond's cash flows are received; measures price sensitivity to yield changes. prereqs: bond pricing, cash flows
- **Bond return formula:** `bond_returns = (−duration × daily_change_oas) / 100`. prereqs: duration, OAS change
- **Cumulative bond P&L:** `(bond_returns/100 + 1).cumprod()` plotted as daily profit & loss; persist returns to `bond_returns_aapl.csv`. prereqs: compounding, CSV export
### LESSON: Sentiment Strategy on Bonds.ipynb
- **Bond sentiment strategy:** identical logic to the stock strategy but applied to bond returns (long when score > 0.25, short when < −0.25). prereqs: sentiment signals, bond returns
- **Bond return + sentiment merge:** join `bond_returns_aapl.csv` with daily sentiment on Date. prereqs: DataFrame merge
- **Strategy return on bonds:** `strategy_return = signal.shift(1) * bond_returns`. prereqs: pandas shift, returns
- **Cumulative bond strategy plot:** `(strategy_return/100 + 1).cumprod()` visualized as cumulative percentage returns. prereqs: cumulative product, plotting
---
## MODULE: Paper and Live Trading
### LESSON: Recent News Headline Data.ipynb
- **News data APIs:** Webhose, NewsAPI, News Fetch, GoogleNews aggregate headlines; pick one, read its docs. prereqs: APIs, networking
- **API key & client init:** `from newsapi import NewsApiClient; newsapi = NewsApiClient(api_key=...)`; keys from registration. prereqs: API keys, client objects
- **Fetching articles with filters:** `newsapi.get_everything(q=keyword, language='en', sort_by='publishedAt', page_size=...)` filters by keyword, language, recency. prereqs: NewsAPI, query params
- **Article information extraction:** pull Title, description, URL, publication date per article into a DataFrame for downstream sentiment. prereqs: loops, pandas
- **Live-data workflow:** the fetched recent headlines feed into sentiment prediction and strategies in the capstone. prereqs: sentiment prediction, strategy
---
## MODULE: Capstone Project
### LESSON: Model Solution.ipynb
- **End-to-end sentiment pipeline:** read data → choose target/predictor → 80/20 split → Bag of Words → XGBoost train → accuracy. prereqs: BoW, XGBoost, train/test
- **max_features constraint:** `CountVectorizer(..., max_features=200)` limits vocabulary size to 200 terms. prereqs: CountVectorizer, feature dimension
- **XGBoost training & accuracy:** `XGBClassifier(max_depth=6, n_estimators=100)` fit and `accuracy_score` (≈0.5499 on full data). prereqs: XGBClassifier, accuracy
- **Fetching recent news (NewsAPI):** loop keywords/date ranges, `newsapi.get_everything`, dedupe into `article_info`. prereqs: NewsAPI, pandas
- **Predict sentiment on new headlines:** convert to str, `count_vectorizer.transform(...)`, `xg_model.predict(...)`, attach class column. prereqs: vectorizer transform, predict
- **Trading-time assignment for live data:** reuse `get_trade_open` to bucket recent headlines into sessions. prereqs: trading time logic
- **Live daily sentiment score:** groupby trading_time → mean sentiment as before. prereqs: groupby mean
- **Yahoo Finance price fetch:** `yfinance.download('AAPL', start, end)` retrieves daily OHLC. prereqs: yfinance, OHLC
- **Live sentiment trading strategy:** buy when score > 0, sell when score < 0; `returns = Open.pct_change()`, `strategy_returns = signal.shift(1) * returns`, plot cumulative. prereqs: signals, returns, shift
---
## MODULE: data_modules (Supporting Code)
- **BERT server IP helper:** `get_ip_address()` returns the host of the BERT server used by `BertClient`. prereqs: BERT as a Service
- **Tweepy/Twitter API access:** `tweepy.AppAuthHandler` builds a Twitter API client; `tweepy.Cursor(api.search, q=...)` streams tweets by query. prereqs: Twitter API, OAuth
- **Tweet metadata extraction:** `full_text`, `id_str`, `retweet_count`, `created_at`, `user.screen_name` from tweet objects. prereqs: tweepy, data extraction
- **VADER sentiment:** `from vaderSentiment ... SentimentIntensityAnalyzer`; `analyzer.polarity_scores(text)['compound']` produces a compound sentiment score for arbitrary text. prereqs: sentiment analysis, lexicon
- **Date-window querying:** `since`/`until` date strings (today ± 1 day) bound the tweet search window. prereqs: datetime, search queries
- **Reusable extraction functions:** helper functions to fetch tweets by query or by ID list and return a tidy DataFrame. prereqs: functions, pandas
---
## Natural-Language-Processing-in-Trading — Section-based course structure
# — Natural Language Processing in Trading — Concept Inventory
**Track:** 5 — Artificial Intelligence in Trading (Advanced)
**Media note:** PDFs only (no mp4s present).
**Overlap with D: notebooks:** partial — the D: side holds notebook-based NLP-in-trading extraction (news sentiment → strategy). This package mirrors it but deepens the word-embedding method theory (BoW → TF-IDF → Word2Vec → BERT) plus BERT fine-tune/adaptation.
## COURSE
Use news headlines to drive sentiment-based trading strategies: tokenising headlines, converting text to numeric vectors via word-embedding methods (Bag of Words, TF-IDF, Word2Vec, BERT), training an XGBoost/BERT classifier over a labelled sentiment dataset, calculating sentiment class of unseen headlines, fine-tuning/adapting BERT to financial spread-change prediction, comparing embedding methods, and finally paper/live trading (IBridgePy) the model.
## Course Prerequisite Map
- **Section 10 Sentiment Class becomes requires:** pandas / CSV handling, a way to compute features for a classifier.
- **Section 12 WordVec requires:** Section 10 setup + vectorisation concepts (BoW dim+ordering problems, TF-IDF weighting).
- **Section 13 BERT requires:** Sections 10 + 12 (embedding progression) + transformer/attention intuition.
- **Section 14 BERT Adaptation requires:** Section 13 (a pre-trained BERT fine-tuned workflow).
- **Section 15 Result Analysis requires:** Sections 12–14 (all four embedding methods) + comparison / evaluation metrics.
- **Section 18 Paper & Live Trading requires:** Section 15 (a working sentiment model) + news data sources.
- **Section 19 Capstone requires:** all prior + ML classifier construction.
- **Section 20 Summary** requires all.
---
### Section 10 — Sentiment Class of News Headlines
- **CONCEPT:** Sentiment-class label — training set of headlines tagged with a sentiment class (used to train a classifier that labels any new headline). **Train/Test breakout (80/20).** prereqs: pandas, text features.
- **CONCEPT:** Vectorise and classify — tokenise headline, convert to numeric via a word-embedding method, pass vector + class to XGBoost, then test accuracy. prereqs: tokenizer + bag-of-words + a gradient-boosting classifier.
- **CONCEPT:** Build a trading strategy per the sentiment class — once classed, the label drives the strategy (e.g., trade Apple stock on daily-headline sentiment). prereqs: Section 10 classifier + data.
### Section 12 — WordVec
- **CONCEPT:** Limitations of Bag-of-Words (BoW) & TF-IDF — **dimension blow-up** (one dimension per unique word across all documents) and **ordering loss** (BoW loses word order/meaning — "This is Good" vs "Is this Good" same vector); TF-IDF adds word-weighting within a document (frequent + signature words get weight) but still limited. prereqs: vectorisation, text data.
- **CONCEPT:** Word2Vec — overcome BoW/TF-IDF limits by learning **distributed dense vectors** through **two-layer neural networks** with two training tactics: **CBOW** and **Skip-Gram**. The vectors are low-dim and wear meaning (similar words placed nearby in embedding space). prereqs: BoW/TF-IDF limitations + neural net basics.
### Section 13 — BERT
- **CONCEPT:** BERT (Google, 2018) — **Bidirectional Encoder Representations from Transformers**: a transformer trained bidirectionally to learn contextual relation (probability over word/sub-word sequences) — vs sequential left-to-right/right-to-left models. prereqs: word embeddings + encoder/attention.
- **CONCEPT:** Two training strategies — pre-training with masked language modelling + next-sentence prediction, then fine-tuning on a downstream task (e.g. sentiment). prereqs: transformer, fine-tuning.
- **CONCEPT:** BERT setup / deployment — install/use `transformers`, run in Google Colab; pre-trained model weights from Google available. prereqs: programming + tokenizer.
### Section 14 — BERT Model Adaptation
- **CONCEPT:** Fine-tuned BERT baseline — pre-trained BERT fine-tuned on single-firm (Apple) headlines to predict **daily spread changes**; the naive model predicts one-sided (all positive, 51%–52% range) → it captured no real signal, only dataset imbalance. prereqs: Section 13.
- **CONCEPT:** Adapting the last layer — because pre-trained BERT is general-language (on sentiment 3-class it did well → 66%), and re-pre-training is impossible (huge finance corpus/gPU/time), instead **modify the last layers** of BERT and add a flexible task-specific downstream model, using Google's embeddings as a feature extractor. prereqs: Section 13 + transfer learning.
### Section 15 — Result Analysis
- **CONCEPT:** Comparing the four embedding methods — **BoW**: simplest; counts word frequency per doc (loses order). **TF-IDF** better at relevance. **Word2Vec** less polys not ordered, meaning-bearing dense vectors. **BERT** contextual/bidirectional — best of context but heavy. Choose by task/data size and interpretability priorities. prereqs: Sections 12–14.
### Section 18 — Paper and Live Trading
- **CONCEPT:** Sources of news-headline data — `news-fetch` python crawler; **News API** (REST); Google News fetch via Python. prereqs: web data + Section 15.
- **CONCEPT:** Paper/live template — IBridgePy NLP template (`IBridgePyNLP.zip`) to paper/live trade the sentiment model on a broker. prereqs: Section 15 worked model + broker connection.
### Section 19 — Capstone Project
- **CONCEPT:** Capstone — build an end-to-end NLP trading strategy: train embedding + classifier on the headline sentiment data (BoW → XGBoost, template + data files supplied), fetch/apply to your own headlines, define the strategy, backtest/paper/Live. prereqs: all prior.
### Section 20 — Course Summary
- **CONCEPT:** Recap + resources (`Natural-Language-Processing-in-Trading-Resources.zip`) — wraps the full pipeline (headlines → embeddings → classifier → strategy → live). prereqs: entire course.


====================
Neural-Networks-in-Trading
====================

# Neural Networks in Trading — Concept Inventory
## COURSE: Neural Networks in Trading
Course on building neural-network trading strategies with sklearn MLPClassifier, Keras DNNs, RNNs and LSTMs, hyperparameter tuning via cross-validation, and live-trading simulation. 7 notebooks + 1 supporting module (`data_modules/Keras_CV.py`).
---
## MODULE: Neural Networks
### LESSON: MLPClassifier Hands-on
- **Neural Network (MLP):** A multi-layer perceptron is a feedforward network of neurons in layers; data flows once forward, error propagates backward (backpropagation). prereqs: linear algebra, supervised learning.
- **MLPClassifier (sklearn):** sklearn's neural-network classifier used to build a trading strategy; configured via `activation`, `hidden_layer_sizes`, `random_state`, `solver`. prereqs: neural network, classification.
- **Predictor variables (features):** Inputs to the model; here one-day returns (`ret1`), five-day returns (`ret5`), five-day std (`std5`), volume/ADV20, and price differences (H-L, O-C). prereqs: pandas, feature engineering.
- **Target variable (labels):** The output to predict; here 1 if future one-day return is positive, else 0 (binary classification). prereqs: classification, returns.
- **pct_change():** pandas method computing percentage change from the previous row. prereqs: pandas.
- **rolling(window).sum() / .std():** Rolling-window aggregation computing sum/std over the previous N rows. prereqs: pandas, time series.
- **shift(periods):** Shifts values forward/backward in time; used to create future returns (`retFut1`). prereqs: pandas, time series.
- **dropna():** Removes rows with missing values (e.g. the last day whose future return is unknown). prereqs: pandas.
- **Train/test split:** Splitting data into a training set (80%) to build the model and a test set (20%) to verify it. prereqs: model validation.
- **Regime change / non-stationarity:** Time-series statistics change over time; a model trained on earlier data is more realistic than random sampling, and ML strategies must be robust to non-stationary regimes. prereqs: time series, stationarity.
- **StandardScaler:** Standardizes features by removing the mean and scaling to unit variance; prevents unexpected model behavior from unscaled predictors. prereqs: feature scaling.
- **Activation function:** Non-linear function defining neuron output (e.g. logistic/sigmoid); adds non-linearity so the network can fit complex patterns. prereqs: neural network.
- **hidden_layer_sizes:** Tuple specifying number of hidden layers and neurons per layer, e.g. `(5)` = one hidden layer of 5 neurons. prereqs: MLP architecture.
- **random_state / seed:** Sets the random seed for weight/bias initialization so results are reproducible. prereqs: reproducibility.
- **solver (sgd):** Optimization function (stochastic gradient descent) used to update weights during backpropagation. prereqs: gradient descent.
- **fit():** Trains the model on the predictor/target training data. prereqs: MLP, training.
- **predict():** Uses the trained model to output class predictions for new input data. prereqs: MLP, inference.
- **Trading signal / strategy returns:** Signal (+1 buy, 0 no-buy) from predictions multiplied by future returns to generate strategy returns. prereqs: trading strategy, returns.
- **Sharpe Ratio:** Risk-adjusted return = sqrt(N) * mean(excess return)/std(excess return); higher is better, >1.5 preferred. prereqs: returns, risk metrics.
- **Excess return:** Strategy return minus the risk-free rate (assumed 5% p.a., daily = 0.05/252). prereqs: Sharpe ratio.
- **CAGR (Compound Annual Growth Rate):** Annualized compounded return = (cumulative returns)^(252/days) - 1. prereqs: compounding, returns.
- **Cumulative returns:** Product of (1+returns) over time; plotted to visualize strategy growth. prereqs: returns.
- **classification_report (sklearn.metrics):** Reports precision, recall, F1-score, and support per class. prereqs: classification metrics.
- **Precision:** tp/(tp+fp); ability of the classifier not to label a negative sample as positive. prereqs: classification metrics.
- **Recall:** tp/(tp+fn); ability of the classifier to find all positive samples. prereqs: classification metrics.
- **F1-score:** Weighted harmonic mean of precision and recall; best at 1, worst at 0. prereqs: precision, recall.
- **Support:** Number of occurrences of each class in the true labels. prereqs: classification metrics.
---
## MODULE: Deep Learning in Trading
### LESSON: DNN Trading Strategy Code
- **Deep Neural Network (DNN):** A neural network with many hidden layers; deeper models create more complex features but risk overfitting. prereqs: neural network, MLP.
- **MinMaxScaler:** sklearn scaler that maps values to [0,1]; used for the Volume column. prereqs: feature scaling.
- **Manual OHLC scaling:** Scaling Open/High/Low/Close together using global min/max to preserve the relationship High >= Close >= Low (MinMaxScaler scales columns independently and would break it). prereqs: feature scaling, OHLC data.
- **Look-ahead bias avoidance:** Scaling using only train-data min/max so test data is not leaked into the scaler. prereqs: data leakage, train/test split.
- **Feature/target datasets:** X = OHLCV features; y = 1 if close 5 days ahead is higher, else 0 (weekly trend prediction). prereqs: feature engineering, classification.
- **Class imbalance / class weights:** When one class dominates, the model over-learns it; class weights rebalance so both classes get equal learning weightage. prereqs: classification, imbalanced data.
- **Sequential model (Keras):** Linear stack of layers built with `model.add()`. prereqs: Keras, DNN.
- **Dense layer:** Fully connected layer; each neuron connects to all neurons of the previous layer. prereqs: neural network, Keras.
- **Activation layer (Keras):** Applies an activation function (e.g. tanh) to layer outputs. prereqs: activation functions, Keras.
- **Dropout layer:** Randomly switches off a fraction of neurons during training to reduce overfitting. prereqs: regularization, overfitting.
- **BatchNormalization:** Normalizes layer inputs to stabilize and speed up training. prereqs: DNN, normalization.
- **kernel_initializer (he_normal):** Initializes weights from He-normal distribution at first run. prereqs: weight initialization.
- **bias_initializer (zeros):** Initializes bias terms to zero. prereqs: weight initialization.
- **input_shape:** Defines the number of input features (columns) for the first layer. prereqs: Keras, DNN.
- **Hyperparameters:** Configuration values set before training (neurons, dropout ratio, activation, epochs, batch size, momentum); tweaked to improve the model. prereqs: model training.
- **ModelCheckpoint callback:** Saves the best model weights during training by monitoring a metric (e.g. val_loss); `save_best_only=True`, `mode='auto'`. prereqs: Keras callbacks, validation.
- **model.summary():** Prints layer-by-layer architecture with output shapes and parameter counts. prereqs: Keras.
- **compile():** Configures the model with loss function, optimizer, and metrics. prereqs: Keras.
- **Loss function (binary_crossentropy):** Quantifies how far predictions are from ground truth for binary classification. prereqs: loss functions, classification.
- **Optimizer (adam):** Algorithm that updates weights to minimize loss. prereqs: gradient descent, optimization.
- **Metrics (accuracy):** Metric reported during training to evaluate model performance. prereqs: classification metrics.
- **epochs:** Number of full passes over the training data. prereqs: training.
- **batch_size:** Number of training samples processed before updating weights. prereqs: training.
- **validation_split:** Fraction of training data held out to evaluate the model on unseen data each epoch. prereqs: validation.
- **training.history:** Dict of per-epoch metrics (loss, val_loss, accuracy, val_accuracy) used to plot convergence. prereqs: training, validation.
- **Overfitting / underfitting:** Diagnosed by comparing train vs validation loss curves; overfit = train loss low, val loss high. prereqs: validation, bias-variance.
- **load_weights():** Loads the best saved weights back into the model before prediction. prereqs: model checkpointing.
- **predict() probability threshold:** Keras predict returns a probability; >0.5 maps to class 1 (buy), <=0.5 to class 0. prereqs: classification, inference.
- **accuracy_score:** Fraction of correct predictions on the test set. prereqs: classification metrics.
- **Buy and hold benchmark:** Comparing strategy cumulative returns against simply holding the market. prereqs: trading strategy, returns.
- **Risk-free rate adjustment:** Subtracting daily risk-free rate (e.g. 5%/252) from strategy returns to compute excess returns. prereqs: Sharpe ratio.
---
## MODULE: Cross Validation in Keras
### LESSON: Trading Strategy using Cross Validation
- **Cross-validation:** Technique to evaluate a model on multiple train/validation splits to find the best hyperparameters. prereqs: model validation, train/test split.
- **GridSearchCV (sklearn):** Exhaustively searches a grid of hyperparameter combinations using k-fold cross-validation to find the best set. prereqs: cross-validation, hyperparameters.
- **KerasModelWrapper (BaseEstimator, ClassifierMixin):** Custom wrapper class making a Keras model compatible with sklearn's GridSearchCV (implements fit/predict/score). prereqs: sklearn API, Keras.
- **Pipeline (sklearn):** Chains steps (e.g. classifier) so they can be cross-validated together; parameters set via `step__param` naming. prereqs: sklearn, cross-validation.
- **param_grid:** Dictionary of hyperparameter values to search (neurons, activation, dropout ratio). prereqs: GridSearchCV.
- **n_jobs / verbose:** Parallelism and logging controls for GridSearchCV. prereqs: GridSearchCV.
- **best_params_:** The best hyperparameter combination found by GridSearchCV. prereqs: GridSearchCV.
- **pickle save/load:** Serializing the best parameters to a `.sav` file for reuse. prereqs: serialization.
- **create_new_model() (data_modules/Keras_CV.py):** Reusable function building a 5-hidden-layer DNN (Dense+Activation+Dropout) with configurable neurons/activation/dropout, compiled with binary_crossentropy + adam. prereqs: Keras, DNN.
- **ModelCheckpoint on best model:** Saving best weights of the tuned model during training. prereqs: callbacks, validation.
- **Predicting trend with best model:** Using the tuned model to predict buy/sell signals on test data and computing accuracy. prereqs: inference, classification.
- **Strategy vs market returns comparison:** Multiplying signals by future returns and comparing cumulative strategy vs market returns. prereqs: trading strategy, returns.
- **Conclusion — time cost of CV:** Cross-validation is time-consuming but saves manual hyperparameter tuning effort. prereqs: cross-validation.
---
## MODULE: Long Short Term Memory Unit (LSTMs)
### LESSON: LSTM Based Strategy
- **LSTM (Long Short-Term Memory):** A recurrent neural network variant with gated memory cells that captures long-term dependencies in sequences; used to predict future close prices. prereqs: RNN, sequence modeling.
- **Timestep / lookback window:** Number of past days (e.g. 20) fed to the model at each step to predict the next value. prereqs: sequence modeling, time series.
- **3D input shape (samples, timesteps, features):** LSTM input is (batch, timesteps, features); here (n, 20, 5) for 20 days of OHLCV. prereqs: LSTM, tensor shapes.
- **return_sequences=True:** LSTM returns output for every timestep (keeps sequence dimension) rather than only the last. prereqs: LSTM.
- **StandardScaler for LSTM:** Standardizing train and test sets separately before building sequences. prereqs: feature scaling.
- **Deep LSTM + Dense stack:** LSTM layer followed by several Dense+Dropout layers; depth increases feature complexity but risks overfitting. prereqs: LSTM, DNN.
- **mean_squared_error (MSE) loss:** Regression loss used because the LSTM predicts continuous close prices. prereqs: loss functions, regression.
- **mse metric:** Mean squared error reported during training. prereqs: regression metrics.
- **ModelCheckpoint (val_loss):** Saves best weights whenever validation loss improves. prereqs: callbacks, validation.
- **load_weights:** Loading best weights before predicting test close prices. prereqs: checkpointing.
- **Predicted vs actual close:** Building a performance dataframe comparing predicted and actual close prices. prereqs: regression evaluation.
- **Spread (Actual - Predicted):** Difference between actual and predicted prices; if mean-reverting, it can generate entry/exit signals. prereqs: mean reversion, pairs trading.
- **Bollinger-style bands on spread:** Plotting expanding mean ± s*std of the spread; buy when spread below lower band, sell when above upper band. prereqs: mean reversion, standard deviation.
- **Mean-reverting strategy caveat:** Such a strategy is for paper trading only; not for real trading without extensive backtesting. prereqs: backtesting, risk.
---
## MODULE: Recurrent Neural Networks
### LESSON: Predicting Prices using RNN
- **RNN (Recurrent Neural Network):** A network with recurrent connections that processes sequences step by step, carrying hidden state across time; used to predict future close prices. prereqs: neural network, sequence modeling.
- **SimpleRNN (Keras):** Basic recurrent layer; here with `timestep` units and input shape (timesteps, features). prereqs: RNN, Keras.
- **Timestep of 20 days:** Feeding the past 20 days of OHLCV at each step; can be changed to predict a sequence of 5 days. prereqs: sequence modeling.
- **Dropout ratio 0.5:** Half the neurons in the preceding layer are switched off during training to reduce overfitting. prereqs: dropout, overfitting.
- **Deep RNN + Dense stack:** SimpleRNN followed by progressively wider Dense+Dropout layers (32→2048). prereqs: RNN, DNN.
- **mean_squared_error loss:** Regression loss for predicting continuous prices. prereqs: loss functions, regression.
- **ModelCheckpoint (val_loss):** Saves best weights on validation loss improvement. prereqs: callbacks.
- **load_weights:** Loading best weights before prediction. prereqs: checkpointing.
- **Reshape predictions:** Reshaping model output to a single column vector to match y_test for the performance dataframe. prereqs: numpy, tensor shapes.
- **Lagging predictions:** RNN predictions look lagging; accuracy improves by tuning hyperparameters (e.g. via GridSearch). prereqs: RNN, hyperparameters.
### LESSON: Strategy Analytics for RNN
- **Trade-wise analytics:** Per-trade list with entry time, entry price, exit time, exit price, and PnL for each trade. prereqs: backtesting, trading.
- **Signal generation:** Signal = 1 if predicted price > previous day's actual price, else -1. prereqs: trading signals.
- **get_trades() function:** Iterates over signals, records position changes (long/short/neutral) and builds a trade log with entry/exit and PnL. prereqs: backtesting, pandas.
- **PnL per trade:** (Exit price - Entry price) * Position; position is +1 long, -1 short. prereqs: trading, PnL.
- **Strategy analytics (get_analytics()):** Computes number of long/short trades, total trades, gross profit/loss, net profit, winners/losers, win/loss percentage, and average profit/loss per trade. prereqs: trade statistics.
- **Win percentage:** 100 * winners / total trades. prereqs: trade statistics.
- **Equity curve:** Cumulative product of (1 + strategy returns) plotted against benchmark cumulative returns. prereqs: returns, performance.
- **Strategy returns:** Daily returns * signal shifted by one day (position applied next day). prereqs: returns, trading.
- **Drawdown:** Percentage decline from the running maximum of cumulative returns. prereqs: performance metrics.
- **Maximum drawdown:** The largest peak-to-trough decline in the equity curve. prereqs: drawdown, risk.
---
## MODULE: Challenges in Live Trading
### LESSON: Trading Simulation using Deep Learning
- **Live-trading simulation:** Using a trained ML model in a rolling simulation, retraining it whenever performance drops. prereqs: DNN, backtesting.
- **create_features() function:** Reusable function generating features and target from raw data at every data point. prereqs: feature engineering.
- **Simulation parameters:** `simulation_length` (number of simulation points), `performance_length` (past window to check model performance), `minimum_feature_length` (min data needed for one feature point). prereqs: simulation design.
- **Train/simulation split:** Splitting raw data into a training set (to build the initial model) and a simulation set (to walk forward). prereqs: train/test split.
- **train_model() function:** Builds and fits a DNN (via create_new_model) with a ModelCheckpoint, returning the trained model. prereqs: Keras, DNN.
- **save_model() function:** Saves model architecture as JSON and weights as HDF5. prereqs: model serialization.
- **load_model() function:** Reconstructs the model from JSON and loads weights. prereqs: model serialization.
- **model_from_json / to_json:** Keras methods to serialize/deserialize model architecture. prereqs: Keras, serialization.
- **train_new_model() function:** Retrains a model by creating features, training, and saving — used when performance degrades. prereqs: retraining, simulation.
- **Performance-based trading decision:** If past accuracy > threshold (0.55), trade on the latest prediction; otherwise retrain and skip trading that day. prereqs: model monitoring, simulation.
- **Rolling retraining:** Rolling the training window forward and retraining as new data becomes available. prereqs: online learning, simulation.
- **Cumulative strategy returns in simulation:** Multiplying signals by future returns and cumulating to measure simulation performance. prereqs: returns, simulation.
---
## MODULE: data_modules (supporting module)
### LESSON: Keras_CV.py
- **create_new_model(neurons, act_1, dropout_ratio):** Reusable Keras function building a 5-hidden-layer DNN (Dense+Activation+Dropout, neurons doubling per layer) with a sigmoid output, compiled with binary_crossentropy + adam + accuracy. prereqs: Keras, DNN.
- **he_normal kernel initializer:** Weight initialization suited to ReLU/tanh activations. prereqs: weight initialization.
---
## Neural-Networks-in-Trading — Section-based course structure (full lesson-by-lesson view)
# — Neural Networks — Concept Inventory
**Track:** 5 — Artificial Intelligence in Trading (Advanced)
**Media note:** PDFs only (no mp4s present).
**Overlap with D: notebooks:** light — D: holds notebook-based DL/neural-network extraction; this course is the maths + Keras-hyperparameter companion (forward propagation, backprop, activation functions, normalisation, cross-entropy, early stopping).
## COURSE
Handling of neural networks for trading strategies built on the math: forward propagation (moving input through a 3-layer net), backward propagation (gradient-based weight updates), and their mathematical machinery (function derivatives + chain rule); then building/regularising deep models in Keras — activation functions (ReLU, sigmoid/softmax), data normalization/batch, cross-entropy loss; concludes with cross-validation and hyperparameter tuning, paper/live deployment via IBridgePy.
## Course Prerequisite Map
- **Section 1 (Neural Networks complete history):** requires calculus (derivative, chain rule) — serves upward as core for the rest of course.
- **Section 4 (Deep Learning in Trading):** requires Section 1 math + install Keras/TensorFlow; activation functions, normalisation, cross-entropy.
- **Section 7 (Cross Validation in Keras):** requires Section 4 (a K sequence model) + every slight hyperparameter concept.
- **Section 10 Paper & Live:** requires Section 7 model + IB bridge.
- **Section 11 Downloadable Resources** wraps.
---
### Section 1 — Neural Networks
- **CONCEPT:** Derivative and chain rule — student prerequisite for "Math behind backprop": the derivative measures change/slope, and the chain rule composes derivatives across layers (∂L/∂w via backprop). prereqs: calculus/analysis prerequisite.
- **CONCEPT:** Forward propagation — compute the network output by multiplying input vector × weights across layers, through activation, layer by layer (the 3-layer example: input → hidden = 2 units → output = 2 units). prereqs: network architecture, matrix multiply.
- **CONCEPT:** Backpropagation — after forward pass, compute the loss and propagate error gradients backward via the chain rule, updating each weight to reduce loss — the training algorithm. prereqs: forward pass + chain rule + loss.
### Section 4 — Deep Learning in Trading
- **CONCEPT:** Activation functions — **ReLU**, **ELU**, **sigmoid**, **tanh**, **softmax**. They introduce nonlinearity; softmax used for classification output, ReLU most common hidden. prereqs: forward propagation, binary/multiclass features.
- **CONCEPT:** Normalization / Standardization and batch norm — scaler/standardization brings values to comparable scale; **batch normalization** stabilises and accelerates training within dense blocks. prereqs: data range divergence, deep layering.
- **CONCEPT:** Cross-entropy loss — measures the error for classification prediction: from **entropy** (uncertainty) it links predicted-class probabilities to ground truth. prereqs: entropy, probability distribution, loss.
- **CONCEPT:** Keras/TensorFlow installation — version-guided install on Windows (VS), Mac, Ubuntu; Keras backend on TensorFlow. prereqs: Python + a DL env.
### Section 7 — Cross Validation in Keras
- **CONCEPT:** Keras layer/hyperparameter building blocks — Dense layer, constraints, activation, **Dropout**, ModelCheckpoint. **Early stopping** (monitor-val loss, restore best, patience) avoids overfitting. prereqs: Section 4 model + tuning concepts.
- **CONCEPT:** Important hyperparameters — hyperparameters of RNNs incl. recurrent initializer, entropy, recurrent_regularizer, recurrent_constraint, recurrent_dropout, stateful semantics for sequence data. prereqs: Keras + recurrent/region intuition.
- **CONCEPT:** Cross-validation of the Keras model — using validation-fold(s) and early stopping to pick epoch count/architecture robustly. prereqs: Sections 4 + 7.
### Section 10 — Paper and Live Trading
- **CONCEPT:** IBridgePy / paper-live — deploy the Keras NN strategy through IBridgePy (template `IBridgePyNN.zip`) into a broker/paper account. prereqs: trained model + broker interface.
### Section 11 — Downloadable Resources
- **CONCEPT:** Class resources (`Neural-Networks-in-Trading-Resources.zip`) — notebooks/data + templates for the whole NN-in-trading workflow. prereqs: entire course.


====================
Options-Trading-Strategies-Advanced
====================

# Options Trading Strategies in Python — Advanced (Concept Inventory)
Data modules (`data_modules/`): `AAPL_new.csv`, `closeprice.csv` (7-stock portfolio), `BankNifty_Futures_Data.csv`, `BankNifty_Options_Data.csv`, `BankNifty_Preprocessed_Options_Data.csv`, `NIFTY_GS_data.csv`, `Nifty_ML_data.csv`, `spx_options_raw_data/*.7z`.
Key conventions: `mibian.BS` for implied volatility and Greeks; futures price as the underlying with `interest_rate = 0`; lot sizes (Nifty 75, BankNifty 40) applied when aggregating Greeks.
---
## MODULE: Sourcing Options Data
### LESSON: Options Data Storing.ipynb
- **Bulk options data sourcing** — extract SPX `.7z` bundles with `py7zr`, concatenate monthly CSVs into a master frame. prereqs: pandas I/O, 7z/ZIP handling
- **File housekeeping** — `os.listdir`/`os.remove` plumbing. prereqs: Python os
- **Raw option-quote schema** — quote unix/readtime/date/hour, underlying last, expire date, DTE, strike distance, per-leg Δ Γ V Θ ρ, IV, volume. prereqs: options data
## MODULE: Dispersion Trading
### LESSON: Dispersion Trading Strategy.ipynb
- **Dispersion trading** — profit from mean-reversion in the implied correlation between an index and its constituents. prereqs: implied volatility, straddle payoff
- **Data required** — ATM strikes/IV for the index (BankNifty) and top constituents, weighted-constituent IV, "dirty" implied correlation, lot sizes and index weights. prereqs: dispersion trading
- **Pipeline** — read per-instrument options CSV → time-to-expiry → ATM strike (min |future − strike|) → daily straddle PnL → IV via `mibian.BS.impliedVolatility` → straddle delta per leg. prereqs: Black-Scholes IV, pandas
- **Straddle construction** — ATM call + ATM put; straddle delta near zero → Delta hedging with futures skipped (kept ~neutral). prereqs: straddle payoff, delta
- **Dirty implied correlation** — `(index IV / weighted-average constituents IV)²`, i.e. squared vol ratio. prereqs: implied volatility, correlation
- **Trading rule** — long index-straddle + short-constituent-straddles when correlation is low (below mean − ½·std); reverse when high; exit on reversion (signal +1/−1/0). prereqs: mean-reversion signal construction
- **Constituent leg PnL** — opposite sign of index signal; aggregate with weighted × lot-size PnL → cumulative strategy PnL. prereqs: dispersion trading
- **Expiry-day caveat** — correlation spike (≈5) ignored; no positions on expiry. prereqs: dispersion trading
## MODULE: Exotic Options (Value at Risk)
### LESSON: VaR (Historical Method).ipynb
- **Value at Risk (VaR)** — maximum portfolio loss not exceeded over a horizon at a given confidence level; three components: confidence level, time horizon, expected loss. prereqs: daily returns, percentiles/quantiles
- **Historical (non-parametric) method** — compute daily returns → sort worst-to-best → VaR at 90/95/99% = 10th/5th/1st percentile. prereqs: VaR, percentiles
- **Motivating histogram** — few days lose more than −4%. prereqs: returns distribution
- **Application** — single stock (Apple) and equally-weighted 7-stock portfolio; daily VaR in %. prereqs: portfolio maths
- **Diversification effect** — portfolio VaR lower than single-stock VaR → diversification cuts stock-specific risk. prereqs: portfolio maths
### LESSON: VaR (Monte Carlo Simulation).ipynb
- **Monte Carlo VaR** — simulate stock returns by geometric Brownian motion `ST = S0·exp((μ − ½σ²)T + σ√T·ε)` with normal random shocks. prereqs: GBM, normal RNG
- **Parameters** — `S0`, drift μ, vol σ, horizon T, number of simulations I (e.g., 500). prereqs: Monte Carlo VaR
- **VaR from simulations** — sort simulated terminal returns worst→best, take percentiles for 90/95/99% VaR. prereqs: Monte Carlo VaR, percentiles
- **Simulation dispersion** — each simulation yields slightly different results; supports confidence-interval intuition. prereqs: Monte Carlo VaR
### LESSON: VaR (Variance-Covariance Method).ipynb
- **Parametric VaR** — assumes normally distributed returns; estimate mean/σ from history, overlay normal pdf, read VaR off quantiles. prereqs: normal distribution, VaR
- **Closed-form** — at 95% → mean − 1.65·σ; at 99% → mean − 2.33·σ (via `scipy.stats.norm.ppf`). prereqs: parametric VaR, scipy
- **Application** — single stock (Apple) and equally-weighted portfolio; smoother/gaussian-model-based values. prereqs: parametric VaR
- **Three VaR styles** — contrast historical (empirical), Monte Carlo, and parametric approaches. prereqs: VaR methods
## MODULE: Machine Learning
### LESSON: Options Price Prediction Using Decision Tree.ipynb
- **Supervised classifier** — learns decision rules from predictor variables (IV, Delta, Gamma, Theta, Vega) to predict whether tomorrow's option price moves up (+1) or down (−1). prereqs: option Greeks, basic supervised classification
- **Target definition** — `+1` if next-day LTP > today's LTP, else `−1` (`np.where(LTP.shift(-1) > LTP, 1, -1)`). prereqs: numpy, pandas
- **Train/test split** — e.g., first 70 days train, remainder test; hyper-params `max_depth=6, min_samples_split=2, max_leaf_nodes=8`. prereqs: train/test splitting
- **Model fit & accuracy** — `DecisionTreeClassifier.fit(...)` then `accuracy_score` on train (80%) and test (55.7%). prereqs: decision tree, accuracy
- **Strategy returns** — predicted signal × next-day return; plot cumulative strategy returns in test period. prereqs: strategy returns
## MODULE: Risk Management
### LESSON: Delta Hedging Strategy.ipynb
- **Delta hedging** — removes the portfolio's sensitivity to the underlying move; Delta = change in option price per unit change in underlying. prereqs: delta, implied volatility
- **Compute IV then Delta** — IV from observed option price → Delta via `mibian.BS(...).callDelta`. prereqs: mibian, implied volatility
- **Contract-delta scaling** — multiply Delta by option lot size (Nifty 75) to get total delta. prereqs: lot sizing, delta
- **Delta neutrality** — sell futures to offset a long call's positive delta (round futures to a tradable multiple). prereqs: futures mechanics, delta
- **PnL decomposition** — futures PnL + call PnL = portfolio PnL; residual loss (≈ ₹600) because higher-order Greeks (Gamma, Theta) are unhedged. prereqs: delta hedging
- **Bridge to gamma scalping** — full Delta-neutrality with Gamma/theta effects feeds into Gamma scalping. prereqs: delta hedging, gamma
### LESSON: Gamma Scalping Strategy.ipynb
- **Gamma scalping** — repeatedly re-hedging a long-Gamma (long-vega) position to monetise convexity earned from committed vs re-hedged moves, offsetting daily time decay (theta). prereqs: delta/gamma, straddle payoff
- **Structure** — buy an ATM straddle (ATM call + ATM put) on Nifty; track the straddle's aggregate Delta. prereqs: straddle payoff, delta
- **Rebalancing rule** — underlying rises → straddle delta-positive → sell Nifty futures; underlying falls → straddle delta-negative → buy futures; keep futures book-neutral in lot-size multiples. prereqs: delta hedging, futures mechanics
- **PnL** — straddle PnL (call + put daily delta×lot) + Nifty futures PnL → cumulative strategy PnL. prereqs: gamma scalping
- **Demonstration** — profitability (≈ ₹1000) purely from delta re-hedging momentum. prereqs: gamma scalping
## Course-level prerequisite map
- Sourcing (1) is a prerequisite; IV/Delta/sigma helpers employed throughout.
- Risk notebooks (7–8) consume the Greeks/hedging from Intermediate, forming the "delta-neutral" theme.
- VaR notebooks (3–5) cover risk estimation (historical / Monte-Carlo / parametric).
- Dispersion (2) pulls together straddles, implied vol, correlation, delta-neutral hedging, and lot-size aggregation.
- ML notebook (6) applies classifier modelling to option-price direction.


====================
Options-Trading-Strategies-Basic
====================

# Options Trading Strategies in Python — Basic (Concept Inventory)
Data module(s): `data_modules/apple_stock_data.csv` (Apple adjusted close prices). No standalone Python modules; all code is embedded in the notebooks.
Key libraries used across the course: `numpy`, `pandas`, `matplotlib.pyplot` (payoff plotting and rolling volatility).
---
## MODULE: Know Your Options!
### LESSON: Call Option Payoff.ipynb
- **Call option (long)** — buying a call gives the right, not the obligation, to buy the underlying at the strike; payoff depends on where spot sits relative to strike at expiry. prereqs: none (entry-level)
- **Call payoff formula** — via `np.where`: profit = `spot - strike` when spot > strike, else `0`, then minus premium. prereqs: numpy.where
- **Call buyer risk/reward** — loss capped at premium paid; profit rises linearly and is unlimited above the strike; must first recover premium (break-even region). prereqs: call payoff
- **Call seller payoff** — exact mirror (multiply buyer payoff by −1); max profit = premium; loss is open-ended as spot rises. prereqs: call payoff
- **Selling a call** — appropriate only when the view is that the underlying will not rally beyond the strike. prereqs: call payoff
- **Payoff plotting** — matplotlib plotting with a zero-moved spine to show profit/loss regions. prereqs: matplotlib
### LESSON: Put Option Payoff.ipynb
- **Put option (long)** — buying a put gives the right to sell the underlying at the strike; payoff depends on spot vs strike at expiry. prereqs: none
- **Put payoff formula** — profit = `strike - spot` when spot < strike, else `0`, then debit the premium. prereqs: numpy.where
- **Put buyer risk/reward** — limited risk (premium), potentially large (near-linear, capped at strike) profit as underlying falls. prereqs: put payoff
- **Put seller payoff** — mirror image: max profit = premium received; losses accrue as the underlying falls below the break-even. prereqs: put payoff
- **Selling a put** — appropriate only when the view is that the underlying will not fall below the strike. prereqs: put payoff
## MODULE: Options Trading Strategies
### LESSON: Bull Call Spread Payoff.ipynb
- **Bull call spread** — long a lower-strike call + simultaneous short of a higher-strike call on the same underlying/expiry. prereqs: call option payoff, premium/debit concept
- **Strategy objective** — profit from small positive (moderately bullish) moves; ceiling placed on both profit and loss. prereqs: bull call spread
- **Payoff assembly** — add long-leg payoff and −1× short-leg call payoff; `max()`/`min()` give capped max profit (strike width − net debit) and max loss (net debit). prereqs: call payoff, numpy
- **Worked example** — long 920C / short 940C on Infosys → max profit ₹15, max loss ₹5. prereqs: bull call spread
- **numpy.arange** — used to build the stock-price-at-expiry range. prereqs: numpy
### LESSON: Bear Put Spread Payoff.ipynb
- **Bear put spread** — long a higher-strike put + simultaneous short of a lower-strike put. prereqs: put option payoff, spread mechanics
- **Strategy objective** — benefit from small negative (moderately bearish) price moves. prereqs: bear put spread
- **Combined payoff** — long put payoff + short put payoff, giving capped max profit (strike width − net debit) and bounded max loss (net debit). prereqs: put payoff
- **Worked example** — long 880P / short 860P on Infosys → max profit ₹15, max loss ₹5. prereqs: bear put spread
- **max()/min() on combined array** — reading off max profit/min loss. prereqs: numpy
### LESSON: Covered Call Payoff.ipynb
- **Covered call** — long (own) stock + simultaneous short call on that stock → a "neutral" view strategy. prereqs: long stock payoff, call payoff
- **Capped upside** — profit ceiling ≈ call premium received; unlimited downside exposure scaled by the long stock position. prereqs: covered call
- **Payoff** — stock payoff (`spot - purchase price`) + short-call payoff. prereqs: stock payoff, call payoff
- **Worked example** — Wipro at ₹300, short 300C → max profit capped at ₹10, max loss proportional to the fall below ₹300. prereqs: covered call
### LESSON: Protective Put Payoff.ipynb
- **Protective put** — long stock + long put on the same underlying ("insurance" against adverse moves). prereqs: stock payoff, put payoff
- **Downside capped** — max loss ≈ put premium; upside remains unlimited. prereqs: protective put
- **Payoff** — long stock payoff + long put payoff. prereqs: stock payoff, put payoff
- **Worked example** — Auro Pharma 700P strike premium ₹20 → max loss bounded to ₹20. prereqs: protective put
## MODULE: Types of Volatility
### LESSON: Historical Volatility Calculation.ipynb
- **Historical (realized) volatility** — gauges past price fluctuations of the underlying over a fixed look-back period. prereqs: volatility concept
- **Daily log returns** — `np.log(Adj_Close / Adj_Close.shift(1))`. prereqs: pandas, log-return math
- **20-day historical volatility** — rolling standard deviation of log returns, annualized-scaled (× `sqrt(window)`), expressed as a percentage. prereqs: standard deviation, annualization scaling
- **Volatility time-series plot** — visualization with matplotlib. prereqs: matplotlib
## Prerequisite chain across the course
- Payoff fundamentals (Call/Put) → every spread strategy (Bull Call, Bear Put, Covered Call, Protective Put).
- Historical volatility lays groundwork for the Intermediate course's volatility skew / smile / forward-volatility modules.
---
## Options-Trading-Strategies-Basic — Section-based course structure (full lesson-by-lesson view)
# Concept Inventory — Options Trading Strategies In Python : Basic
> **5 sections on disk** (Sections 1–4, 6; no Section 5).
## COURSE — Options Trading Strategies In Python : Basic
**Purpose:** Foundational options skill course — understand call/put options, terminology, nomenclature, moneyness, put-call parity, open interest & volume, volatility (realized/historical, implied, forward), pricing inputs, and build simple directional, hedging and neutral option strategies with payoff diagrams in Python.
### Section: Section 1 - Know Your Options!
- **CONCEPT:** Introduction — why options; rights vs obligations, asymmetrical payoff. prereqs: none.
- **CONCEPT:** Options terminology — underlying, premium, strike price, expiration date, style (European/American/Bermudan), ITM/ATM/OTM, intrinsic vs time value. prereqs: none.
- **CONCEPT:** Call options — the right (not obligation) to BUY the underlying at strike; bullish; payoff diagram. prereqs: terminology.
- **CONCEPT:** Put options — the right (not obligation) to SELL the underlying at strike; bearish; payoff diagram. prereqs: terminology.
### Section: Section 2 - Options Nomenclature
- **CONCEPT:** Types of options — classification by exercisability (European/American/Bermudan), tradability (exchange-traded vs OTC), underlying (equity/index/commodity/futures/currency); plain-vanilla vs exotic (Asian average, Binary, Barrier). prereqs: calls & puts.
- **CONCEPT:** Moneyness — ITM/ATM/OTM for calls and puts; drives intrinsic and time value. prereqs: nomenclature.
- **CONCEPT:** Open interest and volume — OI = number of open contracts; Volume = number traded; joint interpretation for market activity. prereqs: payment.
- **CONCEPT:** Put-call parity (PCP) — relationship C + K·e^(-rt) = P + S linking call/put prices; deviation implies arbitrage; used to price/screen. prereqs: calls, puts, moneyness, arbitrage.
- **CONCEPT:** Arbitrage & risk-free profit — exploit mispricing across markets/contracts to lock near-riskless gain (PCP enforcement). prereqs: PCP.
### Section: Section 3 - Types of Volatility
- **CONCEPT:** Normal probability distribution — bell curve, mean (expected value, drift), standard deviation (risk/volatility); assumption that asset returns are normally distributed. prereqs: basic statistics.
- **CONCEPT:** Historical (realized) volatility — annualized σ computed from observed daily returns; measure of realized price dispersion. prereqs: normal distribution, standard deviation.
- **CONCEPT:** Implied volatility (IV) — expected future volatility back-solved from an option's market price (Black-Scholes-Merton); market's consensus forecast. prereqs: normal distribution, option pricing input.
- **CONCEPT:** Forward volatility — future expected volatility over an upcoming horizon implied from term of IVs. prereqs: implied volatility.
### Section: Section 4 - Options Trading Strategies
- **CONCEPT:** Delta trading strategies — directional sensitivity; using delta to express/protect directional (bull/bear) bias. prereqs: moneyness, options pricing.
- **CONCEPT:** Hedging with options — protective put, covered call to reduce downside / enhance yield, insurance-style payoffs. prereqs: call & put payoffs.
- **CONCEPT:** Bull call spread — buy low-strike call, sell higher-strike call (same expiry); limited-risk bullish bet. prereqs: call payoff, spread mechanics.
- **CONCEPT:** Bear put spread — buy high-strike put, sell lower-strike put; limited-risk bearish bet. prereqs: put payoff, spread mechanics.
- **CONCEPT:** Iron Condor (neutral) — short strangle + outer long wings = bull put spread + bear call spread; high-prob small profit when price stays range-bound, limited loss. prereqs: bull put, bear call spread.
### Section: Section 6 - Wrapping Up!
- **CONCEPT:** Course summary — recaps payoff/PCP, historical volatility, bull-call, bear-put, covered call, protective put, iron condor; ability to compute payoffs in Python. prereqs: all course.
- **CONCEPT:** Backtesting & live trading next steps — beyond course scope; resources for data fetching, backtesting tools, broker APIs (IBridgePy/Blueshift). prereqs: all course.
## Course Prerequisite Map
- Terminology → Calls & Puts → Nomenclature (Types, Moneyness, OI/Volume, PCP)
- Normal Distribution → Historical Volatility; IV needed for pricing-based strategies.
- Calls/Puts + Moneyness → Bull Call Spread / Bear Put Spread → Iron Condor (combines spreads).
- Hedging (Protective Put, Covered Call) is built directly from call & put payoff foundations.
- PCP + OI/Volume + Payoffs feed all strategy construction; Wrapping Up consolidates and points to the Intermediate / Python resources.


====================
Options-Trading-Strategies-Intermediate
====================

# Options Trading Strategies in Python — Intermediate (Concept Inventory)
Data modules (`data_modules/`): `Nifty.csv`, `nifty_futures_data_2022.csv`, `nifty_options_data_2022.csv`, `Option_data_NIFTY.csv`, `spx_options_raw_data/*.7z` (SPX option quotes; 481,630 rows × 33 cols).
Key conventions: `mibian` (open-source Black–Scholes pricing + Greeks library) is the central tool; the futures price is used as the underlying with `interest_rate = 0`.
---
## MODULE: Option Greeks: Delta
### LESSON: Greeks Calculator.ipynb
- **Option Greeks set** — Delta, Gamma, Vega, Theta, Rho for both calls and puts via `mibian.BS`. prereqs: call/put payoff
- **mibian BS signature** — `BS([underlying, strike, rate, days_to_expiry], volatility=iv, ...)` returning call/put price, deltas, thetas, rhos, vega, gamma. prereqs: implied volatility
- **Numeric interpretation** — (S=340.3, K=350, 29d, IV=30%): call Δ +0.386, put Δ −0.614, gamma +0.013, vega +0.367, theta −0.19/day, rho call (+) vs put (−). prereqs: Greeks
- **BS theoretical vs market** — theoretical prices should approximate observed market prices. prereqs: Black–Scholes
## MODULE: Option Greeks: Gamma
### LESSON: Option Price Using Delta and Gamma.ipynb
- **Delta-gamma approximation** — first-order (Delta) + second-order (Gamma) Taylor-series: `Price ≈ Initial + Δ·(ΔS) + ½·Γ·(ΔS)²`. prereqs: Greeks calculator, calculus (Taylor series)
- **Approximation accuracy** — approximated call price 5.5680 vs BS true 5.5679; residual from higher-order Greeks. prereqs: delta-gamma approximation
- **Gamma as curvature** — the linear Delta term alone is insufficient; quadratic (Gamma) correction matters for larger moves. prereqs: gamma
## MODULE: Option Greeks: Vega
### LESSON: Option Price Using Vega.ipynb
- **Vega sensitivity** — sensitivity of option price to a 1-point (1%) change in implied volatility: `Price ≈ Initial + Vega × (ΔIV×100)`. prereqs: implied volatility, pricing models
- **Vega approximation accuracy** — approximated price at IV 31% ≈ 4.0923 vs BS true 4.0923. prereqs: vega
- **Vega links price to volatility** — core tool for volatility trading. prereqs: vega, implied volatility
## MODULE: Options Pricing Models
### LESSON: Theoretical Price of Option.ipynb
- **Black–Scholes in mibian** — build the model and compute theoretical call/put prices. prereqs: option pricing fundamentals
- **BS inputs** — underlying price, strike, risk-free rate (0 when futures used), days-to-expiry, implied volatility. prereqs: Black–Scholes
- **Reading outputs** — via `callPrice`/`putPrice` attributes. prereqs: mibian
- **Parameter sensitivity** — vary parameters and observe how option prices change. prereqs: Black–Scholes
## MODULE: Options Trading Strategies
### LESSON: Calculate Calendar Spread Payoff.ipynb
- **Calendar (time/horizontal) spread** — same underlying, same strike, different expiries; sell front-month (short-dated), buy back-month (long-dated). prereqs: call payoff, Black-Scholes
- **Payoff estimation** — one month guesstimated with Black–Scholes for both legs at front-month expiry, holding IV and rates constant. prereqs: calendar spread
- **Profit sources** — time decay (theta) and/or rise in implied volatility; each leg's IV recovered with `impliedVolatility`. prereqs: theta, implied volatility
- **Max profit/loss** — max profit when underlying is at strike at front-month expiry; loss grows deep ITM/OTM. prereqs: calendar spread
- **Worked example** — Nifty: short Nov-28 call ₹50.50, long Dec-30 call ₹148.50. prereqs: calendar spread
## MODULE: Sourcing Options Data
### LESSON: Options Data Storing.ipynb
- **Bulk options data sourcing** — unpackaging tick-rate options (SPX, 2010–2014). prereqs: pandas I/O, ZIP/7z handling
- **py7zr.extractall** — extraction of `.7z` bundles. prereqs: py7zr
- **File plumbing** — `os.listdir`/`os.remove`; concatenating monthly CSV blocks into one master `options_data` frame with `pd.concat`. prereqs: pandas
- **Raw quote schema** — UNIX timestamps, DTE, strike distance, per-leg Δ Γ V Θ ρ, IV, volume. prereqs: options data
## MODULE: Volatility Skew
### LESSON: Strategy Using Volatility Skew.ipynb
- **Volatility skew** — difference between implied volatilities of OTM puts and OTM calls at equal distance from ATM. prereqs: implied volatility, ATM/OTM
- **ATM strike computation** — `strike_difference × round(underlying/strike_difference)`; OTM call = ATM + 2·diff, OTM put = ATM − 2·diff. prereqs: skew, numpy
- **Per-contract IV** — via `mibian.BS(...).impliedVolatility` with call/put branch and guards for `days_to_expiry == 0` / `LTP == 0`. prereqs: mibian, implied volatility
- **Normalized skew** — `(OTM Put IV − OTM Call IV) / ATM IV`. prereqs: skew
- **Skew interpretation** — positive skew ⇒ put IV > call IV ⇒ market expects a fall; negative skew ⇒ call IV > put IV ⇒ rally expected. prereqs: skew
- **Rule-based strategy** — long entry when skew < −5% threshold; short entry when skew > +10%; exit on reversal. prereqs: skew, signal construction
- **Performance metrics** — compounded returns (≈1.12×), Sharpe ≈ 2.37, max drawdown ≈ −3.39% (rolling cummax). prereqs: Sharpe, max-drawdown math
## MODULE: Volatility Trading Strategies
### LESSON: Strategy Using Forward Volatility.ipynb
- **Forward (term) volatility** — future value of an option's implied volatility extrapolated from near- and far-month contracts. prereqs: implied volatility, options data
- **Time-scaled variance** — `IV² · (tau/365)`; take far−near variance, divide by forward (gap) days, then square root → forward-vol estimate. prereqs: variance vs volatility math
- **Signal rule** — forward-vol > near-month IV (far-month "expensive") → short (signal −1); else far-month "cheap" → long (signal +1). prereqs: forward volatility
- **PnL computation** — day-over-day far-month vs near-month LTP differences, scaled by prior-day signal. prereqs: pandas
- **Worked example** — Nifty 2017 (near expiry 2017-09-28, far 2017-10-26); profitable off option mispricing. prereqs: forward volatility
### LESSON: Strategy Using Volatility Smile.ipynb
- **Volatility smile** — U-shaped curve of IV across strikes for same-expiry options; anomalies ("bumps") are exploitable. prereqs: implied-option IV
- **Bump detection** — identify a single-strike bump where IV exceeds neighbour by 1.5, respecting moneyness (ITM/OTM, same-day). prereqs: smile, pandas data manipulation
- **Butterfly to trade the bump** — long two outer money calls, sell 2× middle(at-bump) calls to capture overpriced IV. prereqs: butterfly construction
- **Signals & PnL** — open (buy) when smile has a bump (signal=1), accumulate cost ≈ `2×LTP − neighbouring LTPs`; exit when bump recedes; track PNL/MTM and cumulative PNL. prereqs: butterfly, signal construction
- **Worked example** — Nifty Dec-29 2017 expiry — cumulative PnL ≈ ₹5.8. prereqs: volatility smile
## Course-level prerequisite map
- Greeks + pricing notebooks (1–4) build the quantitative toolkit.
- Sourcing notebook (6) supplies options data/plumbing for strategy notebooks (5, 7–9).
- Strategies in notebooks 5, 7–9 rely on Black-Scholes for IV and payoff computation.
- Volatility modules (skew, smile, forward) form the Intermediate "volatility trading" theme.
- This course feeds into the Advanced course (dispersion, risk management, exotic options, ML).
---
## Options-Trading-Strategies-Intermediate — Section-based course structure (full lesson-by-lesson view)
# Concept Inventory — Options Trading Strategies In Python : Intermediate
> **12 sections on disk** (numbering gaps: sections 9 and 12 absent).
## COURSE — Options Trading Strategies In Python : Intermediate
**Purpose:** Intermediate options engineering — price options with the Black-Scholes & Merton models (and evolved Derman-Kani / Heston models), master the Greeks (first, second, third order) and their sensitivities, and build intermediate multi-leg strategies (arbitrage/box, calendar spread, earnings IV trades) with volatility trading (smile, skew, forward volatility) and paper/live trading via IBridgePy.
### Section: Section 1 - Options Pricing Models
- **CONCEPT:** Course introduction & structure — roadmap onto pricing models, Greeks, and strategies. prereqs: none.
- **CONCEPT:** Analogy to pricing a call option (dice game) — intuition for expected-payoff valuation and how option price derives from underlying uncertainty. prereqs: call options, expected value.
- **CONCEPT:** Intuitive explanation of the Black-Scholes-Merton (BSM) model — continuous-time closed-form formula pricing European options using S, K, r, σ, T. prereqs: pricing analogy, normal distribution, risk-free rate.
- **CONCEPT:** Black-Scholes inputs & assumptions — underlying, strike, interest rate, days to expiry, volatility; lognormal underlying, no early exercise. prereqs: BSM model.
- **CONCEPT:** Mibian Python package — implementing BSM (and Garman-Kohlhagen, Merton) to compute call/put price, Greeks, implied volatility, and put-call-parity. prereqs: BSM, Python.
### Section: Section 2 - Option Type and Applicability
- **CONCEPT:** Option type & applicability — course methods apply to European-style options (US index options SPX/RUT/DJX, NSE India equities/index); NOT American single-stock options (early-assignment risk). prereqs: European/American options.
- **CONCEPT:** Sourcing US options data — retrieving/laying-out options chain data (OptionsDX) for pricing and Greek analysis. prereqs: option type, data structure.
- **CONCEPT:** Data vendors for options — reliable sources of historical options & IV data. prereqs: data sourcing.
### Section: Section 3 - Evolved Options Pricing Model
- **CONCEPT:** Derman-Kani model — implied binomial tree calibrated to observed option prices to price other options consistent with the market. prereqs: BSM, implied volatility.
- **CONCEPT:** Heston model — stochastic-volatility model with mean-reverting volatility to better fit implied-volatility surface. prereqs: Derman-Kani, advanced stochastics.
- **CONCEPT:** Other options pricing models — Lattice models (Binomial Cox-Ross-Rubinstein, Trinomial), Monte Carlo option pricing, Finite Difference method (for American-style options and complex payoffs). prereqs: BSM, lattice/Monte Carlo concepts.
### Section: Section 4 - Options Greeks - Delta
- **CONCEPT:** Greeks primer — Δ,Γ,Θ,ν as first-order sensitivities of option price to underlying, time, and volatility. prereqs: BSM pricing.
- **CONCEPT:** Delta (Δ) — change in option price per unit change in underlying; call Δ ∈ [0,1], put Δ ∈ [-1,0]; also approx. prob. of ITM at expiry. prereqs: Greeks primer.
- **CONCEPT:** Delta with respect to underlying price — how Δ varies across ITM/ATM/OTM (S-curve). prereqs: delta.
- **CONCEPT:** Delta with respect to time to expiry — how Δ changes toward 0/1 as expiry approaches. prereqs: delta.
- **CONCEPT:** Delta with respect to volatility — Δ flattens toward 0.5 with high IV (less directional certainty). prereqs: delta, volatility.
### Section: Section 5 - Option Greeks - Gamma
- **CONCEPT:** Gamma (Γ) — rate of change of Δ per unit underlying move; "acceleration"; largest for ATM, smallest for ITM/OTM; with respect to time to expiry and volatility. prereqs: delta, BSM.
- **CONCEPT:** Gamma sensitivity — rebalancing frequency, delta-hedged portfolio convexity/risk. prereqs: gamma, delta hedging.
### Section: Section 6 - Option Greeks - Vega
- **CONCEPT:** Vega (ν) — change in option price per 1% change in implied volatility; positive for long options. prereqs: implied volatility, BSM.
- **CONCEPT:** Vega with respect to time to expiry and volatility — vega peaks for longer-dated & ATM options; vol-sensitivity dynamics. prereqs: vega.
### Section: Section 7 - Option Greeks - Theta and Rho
- **CONCEPT:** Theta (Θ) — time decay; negative for long options, positive for short options; with respect to time & moneyness. prereqs: BSM, time value.
- **CONCEPT:** Rho (ρ) — interest-rate sensitivity; call ρ positive, put ρ negative; sensitive to time to expiry and moneyness. prereqs: theta, interest rates.
- **CONCEPT:** Advanced Greeks (2nd/3rd order) — Vanna, Charm, Veta, Vomma/Volga, Vera, and third-order Color, Speed, Zomma, Ultima; refine risk measurement. prereqs: first-order Greeks.
### Section: Section 8 - Options Trading Strategies
- **CONCEPT:** Arbitrage strategy — exploit mispricing / violation of no-arbitrage relationships to lock riskless profit; Box spread as synthetic risk-free. prereqs: PCP, moneyness.
- **CONCEPT:** Box trading — combining a bull call spread + bear put spread → synthetic forward / box arbitrage. prereqs: arbitrage strategy.
- **CONCEPT:** Calendar spread — same strike, different expirations (sell near, buy far); monetizes time decay and IV term structure. prereqs: theta, implied volatility.
- **CONCEPT:** Implied volatility in earnings strategy — buy a strangle before an earnings announcement to sell the post-announcement IV collapse. prereqs: strangle, IV crush.
- **CONCEPT:** Stock price movement in earnings strategy — ATM bull-call (bullish) or bear-put (bearish) spreads to profit from the post-earnings price move while limiting IV-crush damage. prereqs: bull call / bear put spread, IV.
- **CONCEPT:** Multi-leg strategy mechanics — payoff and risk profile construction from component legs. prereqs: spread mechanics, Greeks.
### Section: Section 10 - Volatility Trading Strategies
- **CONCEPT:** Forward volatility — expected future volatility over a target forward horizon (derived from the IV term structure) used for forward-start/calendar vol trades. prereqs: implied volatility, volatility term structure.
- **CONCEPT:** Volatility smile — IV varies by strike (not constant as BSM assumes); observed smile shape. prereqs: implied volatility, moneyness.
### Section: Section 11 - Volatility Skew
- **CONCEPT:** Predicting market movement via volatility skew — higher OTM put IV (reverse skew) signals fear/negative-return expectations; skew as a sentiment/hedging signal. prereqs: volatility smile.
- **CONCEPT:** Volatility skew strategy logic — building trades from the skew curve (reverse & forward skew). prereqs: volatility skew concept.
- **CONCEPT:** Reverse vs forward skew & market implication — additional reading on skew behavior and jump-risk interpretation. prereqs: volatility skew strategy.
### Section: Section 13 - Paper and Live Trading
- **CONCEPT:** IBridgePy options automation — template and IBridgePyOPTIONSINT resources for paper/live options trading. prereqs: full tested strategy, broker integration.
- **CONCEPT:** Broker/gateway setup and order flow — connecting broker API, placing multi-leg options orders. prereqs: IBridgePy automation.
### Section: Section 14 - Wrapping Up!
- **CONCEPT:** Summary & resources — recap of pricing models, Greeks, strategies, volatility trading; OTSIResources package. prereqs: all course.
## Course Prerequisite Map
- Options pricing (BSM) ← Dice-game intuition + normal distribution; Mibian implements BSM for Greeks.
- Pricing models (BSM) → Evolved Models (Derman-Kani, Heston, lattice/Monte Carlo/Finite-Difference).
- Greeks build on pricing: Delta → Gamma (rate of change of delta) → Vega (vol sensitivity) → Theta/Rho (time/rates) → Advanced 2nd/3rd order Greeks.
- Strategies combine Greeks + volatility: Arbitrage/Box (PCP enforcement) ← PCP; Calendar spread ← Theta & IV term; Earnings trades ← IV crush & underlying move.
- Volatility path: Implied Vol → Forward Volatility → Volatility Smile → Volatility Skew → Skew strategies.
- Paper/Live (IBridgePy) depends on a complete, back-tested strategy; Wrapping Up consolidates all blocks.


====================
Options-Volatility-Trading-Concepts-and-Strategies
====================

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


====================
Position-Sizing
====================

## COURSE: Position Sizing
Course folder: `Position-Sizing-Resources/Position-Sizing-Resources`
Notebooks: 14
---
## MODULE: Position Sizing Terms
- Notebook: `Position Sizing Terms/Calculate Volatility & Drawdown in Python.ipynb`
### LESSON: Calculate Volatility &amp; Drawdown in Python
- **Volatility** — standard deviation of an asset's returns. − prereqs: returns, statistics
- **Daily returns** — computed with `pct_change()`. − prereqs: returns, percentage change
- **Rolling volatility** — rolling standard deviation over a window (e.g. 252 days). − prereqs: rolling, standard deviation
- **Drawdown** — loss of value from its running peak. − prereqs: cumulative returns
- **Running maximum** — `np.maximum.accumulate()` for the peak series. − prereqs: numpy, cumulative maximum
- **Maximum drawdown** — the largest peak-to-trough decline. − prereqs: drawdown
- **Volatility spikes** — periods of uncertainty (e.g. crisis, pandemic) raise volatility. − prereqs: volatility
## MODULE: Basic Position Sizing — Fixed Units and Fixed Sum
- Notebooks: `Basic Position Sizing_ Fixed Units and Fixed Sum/Fixed Units Implementation.ipynb`, `Basic Position Sizing_ Fixed Units and Fixed Sum/Fixed Sum Implementation.ipynb`
### LESSON: Fixed Units Implementation
- **Fixed units sizing** — always trade the same number of units. − prereqs: position sizing
- **Fixed units formula** — units = floor(initial capital / first-trade price). − prereqs: division, capital
- **Portfolio value (fixed units)** — cumulative pnl + initial capital. − prereqs: pnl, cumsum
- **Profit-and-loss per unit** — close-price `diff()`. − prereqs: prices, pnl
- **Portion of capital** — units × price × signal (wealth committed per trade). − prereqs: position, capital
- **Leverage ratio** — portion of capital used / available portfolio value. − prereqs: capital, ratio
### LESSON: Fixed Sum Implementation
- **Fixed sum sizing** — spend a fixed capital amount per trade. − prereqs: position sizing
- **Number of units (fixed sum)** — fixed capital / current close price. − prereqs: division, price
- **Portfolio value (fixed sum)** — cumulative sum + initial capital (additive, not multiplicative). − prereqs: cumsum, pnl
- **Reducing leverage over time** — profits are not reinvested, so leverage falls as the account grows. − prereqs: leverage, reinvestment
## MODULE: Basic Position Sizing — Fixed Percentage and Fixed Fraction
- Notebook: `Basic Position Sizing_ Fixed Percentage and Fixed Fraction/Fixed Percentage Implementation.ipynb`
### LESSON: Fixed Percentage Implementation
- **Fixed percentage sizing** — spend only a fixed portion of capital per trade. − prereqs: position sizing, capital
- **Portfolio value (fixed percentage)** — (cumulative returns × capital × pct) + (capital × (1−pct)). − prereqs: returns, capital
- **Portion of capital used** — fixed percentage of the current portfolio value. − prereqs: capital, portfolio value
- **Constant leverage** — a fixed percentage keeps the leverage ratio constant. − prereqs: leverage, ratio
## MODULE: Volatility Models
- Notebook: `Volatility Targeting/Volatility Models.ipynb`
### LESSON: Volatility Models
- **Simple volatility** — equal weight across all returns in the window. − prereqs: volatility, rolling
- **EWMA volatility** — exponentially weighted moving-average volatility (more weight on recent). − prereqs: EWMA, weighting
- **Average True Range (ATR)** — mean of the true range indicator. − prereqs: volatility, OHLC
- **True range formula** — `max(high−low, |high−prev close|, |low−prev close|)`. − prereqs: OHLC, max
- **GARCH model** — advanced volatility estimate capturing volatility clustering. − prereqs: volatility, time series
- **GARCH(p,q) with `arch_model`** — fitting a GARCH model and forecasting 1-day volatility. − prereqs: GARCH, arch library
## MODULE: Application of Volatility Targeting
- Notebook: `Application of Volatility Targeting/Application of Volatility Targeting.ipynb`
### LESSON: Application of Volatility Targeting
- **Volatility targeting** — sizing positions to keep portfolio vol near a target. − prereqs: volatility, position sizing
- **Target volatility parameter** — the volatility level to target. − prereqs: volatility target
- **Leverage cap** — maximum allowed leverage (e.g. 2). − prereqs: leverage, cap
- **Leverage formula** — target volatility / asset volatility. − prereqs: volatility, leverage
- **Leverage applied to returns** — strategy returns × calculated leverage. − prereqs: leverage, returns
- **Derived portfolio value** — cumulative returns × initial capital. − prereqs: returns, capital
## MODULE: Constant Proportion Portfolio Insurance
- Notebook: `Constant Proportion Portfolio Insurance/Implementation of CPPI.ipynb`
### LESSON: Implementation of CPPI
- **CPPI** — a position-sizing strategy pursuing upside while hedging downside. − prereqs: portfolio, risk
- **Risky asset + floor value** — balance portfolio as the minimum account value. − prereqs: portfolio, floor value
- **Multiplier** — multiple `m` levering the risky asset returns (`1/drawdown`). − prereqs: multiplier, drawdown
- **Cushion percentage/value** — the portion above the floor. − prereqs: floor value, portfolio value
- **Levered return** — multiplier × risky-asset return. − prereqs: leverage, returns
- **Account value update** — floor + cushion × (1 + levered return). − prereqs: cushion, floor
- **Cushion recalculation** — cushion = account value − floor. − prereqs: cushion, account
- **Leverage in CPPI** — leverage = m × (cushion / account value). − prereqs: leverage, cushion
- **Leverage financing cost** — leverage has a cost that reduces total returns. − prereqs: leverage, cost
## MODULE: Time Invariant Portfolio Protection
- Notebook: `Time Invariant Portfolio Protection/Implementing Time Invariant Portfolio Protection.ipynb`
### LESSON: Implementing Time Invariant Portfolio Protection (TIPP)
- **CPPI floor problem** — once the portfolio rises far above the floor, it holds the risky asset entirely. − prereqs: CPPI, floor
- **TIPP** — updates the floor relative to the previous portfolio peak. − prereqs: CPPI, floor value
- **New floor update** — when account exceeds its max, floor = floor_percent × new high. − prereqs: floor, high
- **Floor updates / capped leverage** — TIPP keeps leverage in check by raising the floor at new highs. − prereqs: leverage, floor
## MODULE: Conservative Framework (TIPP + Volatility Targeting)
- Notebook: `Conservative Framework for Position Sizing/Implementing TIPP with Volatility Targeting.ipynb`
### LESSON: Implementing TIPP with Volatility Targeting
- **Volatility-adjusted multiplier** — multiplier becomes a function of current vs target vol. − prereqs: TIPP, volatility target
- **Adjusted multiplier** — `new multiplier = multiplier × leverage`. − prereqs: multiplier, leverage
- **Volatility-linked capital use** — use less capital when vol is high, more when calm. − prereqs: volatility, capital
- **Improved Return-to-MDD** — volatility targeting raises the return-to-max-drawdown ratio. − prereqs: drawdown, return-to-MDD
## MODULE: Kelly Criterion
- Notebook: `Kelly Formula/Implementation of Kelly Criterion.ipynb`
### LESSON: Implementation of Kelly Criterion
- **Kelly criterion (K%)** — formula for optimal trade size. − prereqs: trade size
- **Winning probability (W)** — share of positive trades. − prereqs: statistics, win rate
- **Win/loss ratio (R)** — average win / average loss magnitude. − prereqs: returns, ratio
- **Number of trades** — for daily rebalanced strategies, count of non-zero returns. − prereqs: returns, trades
- **Kelly formula** — K% = W − (1−W)/R. − prereqs: win probability, win/loss ratio
## MODULE: Optimal F
- Notebook: `Optimal F/Implementation of Optimal F.ipynb`
### LESSON: Implementation of Optimal F
- **Kelly limitations** — returns reduced to binary values; volatility ignored. − prereqs: Kelly criterion
- **Optimal f** — maximizing cumulative holding-period return over different trade sizes. − prereqs: cumulative returns, optimisation
- **Cumulative return calculation** — product of (1 + each return). − prereqs: compounding, returns
- **Leverage grid** — linspace of candidate leverages (0..40). − prereqs: iteration, leverage
- **Optimal leverage** — the leverage achieving the maximum cumulative return. − prereqs: optimisation, leverage
## MODULE: Numerical Methods — Bootstrapping
- Notebook: `Numerical Methods/Bootstrap Simulation.ipynb`
### LESSON: Bootstrap Simulation
- **Bootstrap sampling** — random sampling with replacement. − prereqs: statistics, sampling
- **Bootstrap samples** — alternative realities made from the original sample. − prereqs: bootstrapping
- **Bootstrap drawdown distribution** — distribution of drawdown across resampled datasets. − prereqs: drawdown, distribution
- **Benchmark percentile** — where the benchmark's drawdown sits among the simulations. − prereqs: percentile, bootstrapping
---
## MODULE: Implementation of the Trading Strategy
- Notebook: `Implementation of the Trading Strategy/Index Reversal Strategy Implementation.ipynb`
### LESSON: Index Reversal Strategy Implementation
- **Index reversal strategy** — exploits local-minimum-day price anomaly of an index. − prereqs: index, behaviour
- **Local minimum day** — day the 2-min-before-close price equals the 10-day minimum. − prereqs: minimum, window
- **Signals for long positions** — buy when close == trailing minimum, else close. − prereqs: signal, position
- **Strategy returns** — close percentage change × shifted signal. − prereqs: returns, signal
- **Cumulative returns** — product of (1 + returns). − prereqs: returns, compounding
- **Performance analysis function** — reusable utility for total/CAGR/max-drawdown. − prereqs: metrics
## MODULE: Capstone Project (Position Sizing)
- Notebook: `Capstone Project/Model Solution_ Position Sizing Capstone Project.ipynb`
### LESSON: Model Solution — Position Sizing Capstone
- **Position sizing capstone** — compare position-sizing techniques on a ticker. — prereqs: position sizing
- **Train/test split** — data split for parameter selection (2000–2010) and backtest (2011–2021). — prereqs: hold-out, backtest
- **Multiplier estimation** — multiplier = 1 / max drawdown from benchmark. — prereqs: multiplier, drawdown
- **Volatility target estimation** — average rolling volatility of benchmark returns. — prereqs: volatility
- **Volatility targeting, CPPI, TIPP, TIPP+vol** — four presizing techniques implemented & compared. — prereqs: the four methods
- **Return-to-MDD model selection** — choose the technique with the highest return per unit of risk. — prereqs: Return-to-MDD
---
## Cross-cutting / Thematic Concepts
- **SPY ETF minute/daily price data** — price data one/two minutes before the close is used across the course. − prereqs: none
- **Position sizing taxonomy** — fixed units, fixed sum, fixed percentage, volatility target, CPPI, TIPP, Kelly, Optimal F, bootstrap. − prereqs: portfolio, risk


====================
Price-Action-Trading-Strategies
====================

# Price Action Trading Strategies Using Python — Concept Inventory
Course goal: detect and backtest price-action chart patterns (head and shoulders, inverse head and shoulders, double/triple tops & bottoms, support/resistance), pivot-point systems (traditional, Woodie's, Camarilla) and Fibonacci retracements — with entry/exit risk management, backtesting, trade-level analytics, performance metrics, and transaction-cost/slippage accounting.
## Enumerated Notebooks (24) + Module (1)
| # | Module folder | Notebook |
|---|---|---|
| 1 | Detecting Head and Shoulders Pattern | Identify Local Minima and Maxima |
| 2 | Detecting Head and Shoulders Pattern | Detecting Head and Shoulders |
| 3 | Backtesting Head and Shoulders Pattern | Head and Shoulders: Entry and Exits |
| 4 | Backtesting Head and Shoulders Pattern | Backtesting Head and Shoulders Pattern |
| 5 | Inverse Head and Shoulders Pattern | Detect the Inverse Head and Shoulders Pattern |
| 6 | Inverse Head and Shoulders Pattern | Backtest the Inverse Head and Shoulders Pattern |
| 7 | Double Top Pattern | Detect the Double Top Pattern |
| 8 | Double-Bottom Pattern | Detect the Double Bottom Pattern |
| 9 | Triple and n-Top Patterns | Detect the Triple Top Pattern |
| 10 | Triple-Bottom Pattern | Detect the Triple Bottom Pattern |
| 11 | Strategy Using Support and Resistance | Detecting Support and Resistance Levels |
| 12 | Strategy Using Support and Resistance | Backtesting Support Level |
| 13 | Pivot Points | Compute and Visualise Pivot Points |
| 14 | Types of Pivot Points | Visualise Woodie's Pivots |
| 15 | Types of Pivot Points | Visualise Camarilla Pivots |
| 16 | Woodie's Trend Trading | Woodie's Trend Based Strategy |
| 17 | Woodie's Range Trading | Woodie's Range Trading Strategy |
| 18 | Camarilla Trend Trading | Camarilla Trend Based Strategy |
| 19 | Fibonacci Ratios | Calculation of Fibonacci Ratios |
| 20 | Fibonacci Retracement Strategy | Fibonacci Retracement Strategy |
| 21 | Performance Analysis | Trade Level Analytics |
| 22 | Performance Analysis | Performance Metrics |
| 23 | Transaction Costs and Slippage | Implementation of Transaction Cost and Slippage |
| 24 | Capstone Project | Capstone Project Solution |
Recurring module functions (used across most strategy notebooks)
- **`get_min_max(data, argrel_window)`** — local minima/maxima detection (via scipy `argrelextrema`).
- **`backtester(data)` / `intraday_backtester(data, intraday_exit)`** — produce a `round_trips_details` trade log (entry/exit dates & prices, position, `exit_type`, PnL).
- **`trade_level_analytics(trades)`** — win%, avg PnL, holding period, profit factor.
- **`get_performance_metrics(data, col_names)`** — CAGR, Sharpe, annualised vol, max drawdown, equity curve.
---
## 1. Identify Local Minima and Maxima
**Concepts:**
- Detecting local minima/maxima is the foundational first step for any chart-pattern detection.
- **scipy `argrelextrema`** to find swing lows/highs: pass the `Low` series with `np.less` comparator, or the `High` series with `np.greater`; `order=argrel_window` sets the comparison window.
- Mapping integer indices back to dates/prices.
- Candlestick visualisation with `mplfinance` (`plot`, `style` param).
- Build reusable `get_min_max()` function in the shared module.
**Prereqs:** pandas; numpy; min/max reasoning on a series; plotting.
## 2. Detecting Head and Shoulders
**Concepts:**
- A **head and shoulders (HS)** pattern = 5 sequential local extremes: shoulders A, E (maxima), head C (maxima above both), neckline points B, D (minima).
- Define pattern-detection conditions: A, C, E ∈ maxima; B, D ∈ minima; C above A & E; A & E above B & D; shoulders within 1.5% of their mean (tolerance).
- Build an **HS scanner** over consecutive sequences of 5 min/max points; reports indices of valid patterns.
- **Store pattern details** (dates/prices of head, shoulders, neckline) for later analysis.
- Visualise detected patterns with `mplfinance`.
**Prereqs:** notebook 1; structural reasoning about chart shapes.
## 3. Head and Shoulders: Entry and Exits
**Concepts:**
- HS pattern is completed only after the right shoulder breaks **below the neckline** — the confirmation event.
- Filter patterns to avoid look-ahead bias: `time_for_confirmation > 5 bars` (pattern fully formed) **and** within 30 bars (not overextended).
- Visualise the breakdown candle with `mplfinance`.
- **Risk management / exit levels** for short entry: stop-loss just above the second shoulder; target at a multiple of (head − neck2) below entry.
- Plot confirmation point, stop-loss (red) and target (green) levels.
**Prereqs:** notebook 2; understanding of look-ahead bias; risk-level thinking.
## 4. Backtesting Head and Shoulders
**Concepts:**
- Merge price data (`spy_daily_1993_2018.csv`) with stored pattern details into one strategy DataFrame.
- **Backtester** logic: initial settings (capital, position sizing, entry/exit flags); positions check; entry-position update when `entry_flag=True`; exit-position update when `exit_flag=True`.
- Record trade log (`round_trips_details`) with entry/exit dates & prices, position, exit-type (stop/target/time), and PnL.
- Interpreting a **trade log** print.
**Prereqs:** notebooks 2–3; event-driven loop reasoning; merges.
## 5. Detect the Inverse Head and Shoulders (IHS)
**Concepts:**
- IHS is the mirror of HS: 5 sequential points with A, C, E ∈ minima (troughs), B, D ∈ maxima (neckline), head C below the neckline, shoulders above it, shoulders within 1.5% of their mean.
- **IHS scanner** analogous to the HS scanner with mirrored conditions.
- Store pattern details; find the long-entry confirmation date.
- Filter for validity (confirmation > 5 bars, within 30 bars).
- **Risk management** for long entry: stop-loss 1% below the right shoulder; target at `head_length` above entry.
**Prereqs:** notebook 2 (HS detection pattern); notebook 3 (risk levels).
## 6. Backtest the Inverse Head and Shoulders
**Concepts:**
- Merge `apple_daily_1980_2022.csv` with `ihs_pattern_details.csv`; generate a `signal` column.
- Generate a trade sheet with `backtester()`.
- **Trade-level analytics** via `trade_level_analytics()` (win count, **profit factor ≈ 2.7** = excellent).
- **Strategy performance** via `get_performance_metrics()` (CAGR, Sharpe, max drawdown); forward-fill `signal` across entry→exit range.
**Prereqs:** notebooks 4–5; backtesting & analytics functions.
## 7. Detect the Double Top Pattern
**Concepts:**
- **Double top** = 3 sequential points: A, C ∈ maxima (two tops), B ∈ minima (neckline); A & C above B; tops within 1.5% tolerance.
- **Double top scanner** (similar pattern to HS/IHS scanners with the stated conditions).
- Store pattern details; find short-entry confirmation date; filter validity (5-bar look-ahead guard, within 30 bars).
- **Trade**: confirmation of breakdown below neckline → short the second top.
- **Risk management**: stop-loss 1% above the second top; target at `top_length` below short entry.
**Prereqs:** notebook 1; notebook 3 (risk) and 5 (scanner pattern-conditions).
## 8. Detect the Double Bottom Pattern
**Concepts:**
- **Double bottom** mirror of double top: A, C ∈ minima (two bottoms), B ∈ maxima (neckline); A & C below B; bottoms within 1.5% tolerance.
- **Double bottom scanner** with conditions inverted from double top.
- Store details; find long-entry confirmation date; validity filters.
- **Risk management**: stop-loss 1% below the second bottom; target at `bottom_length` above long entry.
**Prereqs:** notebooks 1 and 7 (mirror logic).
## 9. Detect the Triple Top Pattern
**Concepts:**
- **Triple top** = 5 sequential points: A, C, E ∈ maxima (three tops) above neckline points B, D ∈ minima; first two tops within 1.5% tolerance (rule from Advanced Trading Rules).
- **Triple top scanner** (analogous to other scanners).
- Store pattern details; short entry confirmation; validity filters.
- **Risk management**: stop-loss 1% above the third top; target at `top_length` below short entry.
**Prereqs:** notebook 7 (double top); scanner-condition pattern logic.
## 10. Detect the Triple Bottom Pattern
**Concepts:**
- **Triple bottom** mirror of triple top: A, C, E ∈ minima below B, D ∈ maxima (neckline); first two bottoms within 1.5% tolerance.
- **Triple bottom scanner**; store details; long entry confirmation; validity filters.
- **Risk management**: stop-loss 1% below the third bottom; target at `bottom_length` above long entry.
**Prereqs:** notebook 9 (mirror, like double-bottom from double-top).
## 11. Detecting Support and Resistance Levels
**Concepts:**
- Support = level from which price has bounced at least once; resistance = level capped by price.
- Resample minute data to daily (`resample`), use a `90-day` lookback window.
- Identify levels via `get_min_max()` from the shared module (minima= support, maxima = resistance).
- **Nearest support/resistance**: a level is support if `ltp` > support and vice versa; pick the most recent for higher re-test probability.
- Build `get_support(price_data, argrel_window=15)` and `get_resistance(...)` helpers.
**Prereqs:** notebooks 1 (min/max) and 4 (resampling); level-trading intuition.
## 12. Backtesting Support Level
**Concepts:**
- Multi-timeframe strategy: find daily support, trade on 15-minute closes.
- Map daily support into the 15-min merged DataFrame; merge daily + 15-min frames.
- **Entry**: go long at current Close when previous Close dropped below the support level with no open position.
- **Exit**: stop-loss 10% below and take-profit 15% above entry Close.
- Backtest (long at next candle close), then apply `trade_level_analytics()` and `get_performance_metrics()`.
**Prereqs:** notebooks 11 and 4; multi-timeframe merge; risk levels.
## 13. Compute and Visualise Pivot Points
**Concepts:**
- **Pivot point (P)** = (High + Low + Close)/3 of the preceding day; better reference than prior close (captures range).
- Support/resistance formula set for traditional pivots (R1..R3, S1..S3 from P and (High−Low) range).
- `shift(1)` to compute on preceding candle's OHLC.
- Resample minute→daily to compute daily pivots, visualise over a recent minute window as horizontal lines.
**Prereqs:** OHLCV candle semantics; resampling; plotting.
## 14. Visualise Woodie's Pivots
**Concepts:**
- **Woodie's pivots** suit longer (positional) timeframes; computed on weekly data.
- **W-Pivot WP = (High + Low + 2×Close)/4** (weekly).
- Support/resistance formulas (R1..R3, S1..S3) based on WP and weekly range.
- Resample minute→daily + weekly; visualise levels over daily close series.
**Prereqs:** notebook 13 (pivot formula concept); resampling.
## 15. Visualise Camarilla Pivots
**Concepts:**
- **Camarilla pivots** yield 6 support + 6 resistance levels, closer together (especially S1–S3 / H1–H3); best on shorter timeframes.
- Pivot P = (High+Low+Close)/3 computed on daily data.
- Resistance H1..H6 & support L1..L6 formulas driven by `Range = High − Low` (e.g., H1 = Close + Range×(1.1/12), H3, H4; H5=Close×(High/Low), H6 derived; matching L-side levels).
- Visualise levels over minute closes.
**Prereqs:** notebook 13 (traditional pivots); understanding of ranges.
## 16. Woodie's Trend Based Strategy
**Concepts:**
- **Trend (breakout)** regime signal on weekly Woodie's: `Day's Open > Week's R2` and `Day's Open < Week's R3`.
- **Entry** on 15-min close above **R3**; final signal = trend_signal AND entry_signal.
- Multi-frequency workflow: resample minute→weekly/daily/15-min, compute weekly Woodie's, freeze levels for the week, merge.
- **Risk management**: stop-loss at R2; target set at a distance relative to (R3−R2) above R3 (tuned to avoid negative PnL).
- Backtest with `backtester()`; analytics + performance metrics (CAGR, Sharpe, max drawdown); parameter sensitivity (target distance change flips PnL).
**Prereqs:** notebooks 14; 4 (backtest) and 21 (analytics).
## 17. Woodie's Range Trading Strategy
**Concepts:**
- **Range** regime signal on weekly Woodie's: `Day's Open < Week's R2` and `Day's Open > Week's S2`.
- **Entry** on 15-min close **below S2**; final signal = range_signal AND entry_signal.
- Multi-frequency merge (weekly pivots → daily/15-min), freeze weekly pivot levels for the week.
- **Risk management**: stop-loss at average of S2 & S3; target = W-Pivot level.
- Backtest; trade-level analytics; strategy performance.
**Prereqs:** notebook 16 (workflow mirror, inverted regime) + 14.
## 18. Camarilla Trend Based Strategy
**Concepts:**
- **Camarilla trend (breakout)** conditions from daily Camarilla levels: `Day's Open < H3` and `Day's Open > H4`.
- **Entry** on 5-min close **above H4**; final = trend_signal AND entry_signal.
- Higher trade frequency than Woodie's (frequent, closely-spaced Camarilla levels → more trades).
- **Risk management** (long): stop-loss at H3, target at H6.
- Backtest with `intraday_backtester()`; forward-fill for equity curve; `trade_level_analytics()` + `get_performance_metrics()` (e.g., 394 trades, profit factor 1.58; CAGR 3.95%, Sharpe 0.31, MDD −14.98%).
**Prereqs:** notebooks 15 and 16/17 (regime+entry pattern), 4/21 (backtest/analytics).
## 19. Calculation of Fibonacci Ratios
**Concepts:**
- Fibonacci retracement ratios: 23.6%, 38.2%, 50%, 61.8%, 78.6% of the price range (Max − Min).
- Identify max/min price from the `High`/`Low` (candlestick) or `Close` (line) series.
- Plot the price series with the Fibonacci ratio lines; observe price reacting near levels (e.g., reversal at 50%).
**Prereqs:** price-range arithmetic; plotting.
## 20. Fibonacci Retracement Strategy
**Concepts:**
- Two-timeframe design: monthly (or daily) to compute Fibonacci levels; 30-min (intraday) for entry timing.
- Preconditions for a tradable segment: price in **uptrend** and max price > min price + 25% (strong trend).
- Compute per-year Fibonacci ratios (rolling min/max).
- **Buy zone** = Close between 38.6% and 50% level; **SMA signal** = 21-period SMA above the 50% level; buy when both hold.
- **Exit/sell** when conditions break; **stop-loss** at 61.8% level; **take-profit** at 23% level.
- Drop unused OHLC columns, rename `Close` to distinguish monthly vs 30-min, merge dataframes.
- Filter to valid uptrend periods; backtest with `backtester()`; `trade_level_analytics()` + `get_performance_metrics()` (win% > loss%, positive profit factor; CAGR, Sharpe, max drawdown).
**Prereqs:** notebook 19; multi-timeframe resample/merge; backtest & analytics functions.
## 21. Trade Level Analytics
**Concepts:**
- Metrics evaluating a strategy **per trade** (beyond aggregate PnL).
- **Profit & Loss** (sum of trade gains/losses).
- **Win Percentage / Win Rate** = winning trades / total × 100 (a <50% win rate can still be profitable if winners >> losers).
- **Average PnL per trade** (average profit per winning trade vs average loss per losing trade).
- **Average Trade Duration / holding period** (exit − entry) and its capital/turnover implications.
- **Profit Factor** = win% × avg-win / (lose% × avg-loss); grading scale (<1 unprofitable, ~1 breakeven, 1.1–1.4 average, 1.4–2 decent, ≥2 excellent).
- Wrap into reusable `trade_level_analytics()`.
**Prereqs:** trading results data; ratio arithmetic.
## 22. Performance Metrics
**Concepts:**
- Metrics evaluating strategy performance **within trades** (entry→exit).
- **Equity curve** (cumulative strategy returns) for profit trajectory & visibility of drawdowns.
- **CAGR** (Compound Annual Growth Rate) = ((EV/BV)^(1/n) − 1)×100.
- **Annualised Volatility** = std(strategy_returns) × √(252 × candles/day).
- **Sharpe Ratio** = (mean return − risk-free) / volatility; higher preferred (Sharpe > 1 preferable).
- **Maximum Drawdown** = (peak − trough)/peak; lower magnitude preferred.
- Histogram of returns (distribution).
- Wrap into reusable `get_performance_metrics()`.
**Prereqs:** cumulative-returns; standard deviation; CAGR formula.
## 23. Implementation of Transaction Cost and Slippage
**Concepts:**
- Account for **brokerage/commission + taxes** before going live (e.g., 0.03% + 0.02% of traded value; broker-dependent).
- **Slippage modelling** = difference between expected and executed price; estimate from minute data using last-5-minute candles per day (`groupby("date")`, high end-of-day liquidity).
- Buy slippage = worst execution price (High) − last traded (Close); sell slippage = last traded (Close) − worst execution (Low); express as % of close; use a conservative max.
- Adjust strategy returns: detect position change (`signal.diff`) and deduct `change × total cost` from daily returns.
- Compare gross vs net (post-cost) cumulative returns (e.g., 1.126× → 1.004×), and total PnL vs total cost to judge viability.
**Prereqs:** notebooks 21–22; position change/turnover reasoning.
## 24. Capstone Project Solution
**Concepts:**
- End-to-end integration of the pattern-detection and analytics toolkit on `spy_daily_1993_2018.csv`.
- Sections: Min–Max (locate extremes) → Head and Shoulders → Inverse Head and Shoulders → **Box Plot** (visualising trade/return distributions).
- Consolidates `get_min_max`, scanners, backtester, and analytics into a single analysis.
**Prereqs:** every preceding notebook, particularly 1–2, 5, 21–22.
---
## Price-Action-Trading-Strategies — Section-based course structure (full lesson-by-lesson view)
# Concept Inventory — Price Action Trading Strategies Using Python
## COURSE: Price Action Trading Strategies Using Python
### Section: Section 1 - Introduction
- **Introduction:** course overview. prereqs: none.
- **Course structure:** pattern identification (reversal/continuation) → support/resistance → pivots → Fibonacci → backtesting. prereqs: none.
### Section: Section 2 - Basics of Price Action Trading
- **Price action trading:** studying basic price behaviour across time to make trading decisions without relying solely on lagging indicators. prereqs: none.
- **Benefits & drawbacks of price action trading:** clean signals, widespread timeframe applicability; but noise on short timeframes. prereqs: price action.
- **Asset & dataset applicability (FAQs):** concepts apply to any listed stock; minute-level data resampled to 15-min/hourly/daily. prereqs: price action.
### Section: Section 3 - Supply and Demand Analysis
- **Supply and demand analysis:** supply zone (sellers dominant) and demand zone (buyers dominant); price reverses after entering the zone. prereqs: price action.
- **Supply/demand zones & patterns:** zones defined by price patterns (Rally-Base-Rally, Drop-Base-Drop); Wykoff market phases. prereqs: supply & demand analysis.
### Section: Section 4 - Head and Shoulders Pattern
- **Head and shoulders pattern:** bearish reversal pattern (two shoulders + higher head + neckline); forms at the end of an uptrend. prereqs: price action basics.
- **Trading head and shoulders pattern:** entry on neckline break; targets and stop placement. prereqs: head & shoulders.
### Section: Section 5 - FAQs on Head and Shoulders Pattern
- **Variations in shoulders:** asymmetric/unequal shoulder variants tolerated. prereqs: head & shoulders.
- **Timeframe reliability:** patterns more reliable on longer timeframes; noise increases false signals short-term. prereqs: head & shoulders.
### Section: Section 6 - Detecting Head and Shoulders Pattern
- **Local minima and maxima:** programmatic detection of extremes within a window (shoulders/head at maxima, neck at minima); used to find swing points. prereqs: head & shoulders; Python.
### Section: Section 8 - Performance Analysis
- **Performance analysis:** backtested pattern trades with trade metrics (profit factor, win rate). prereqs: backtesting basics.
- **APPT & 17 trading metrics:** deeper per-trade analytics beyond P/L ratio. prereqs: performance analysis.
### Section: Section 9 - Transaction Costs and Slippage
- **Transaction costs & slippage:** costs eroding pattern-strategy returns; slippage splits into spread, market impact, volatility costs; minimising slippage. prereqs: performance analysis.
### Section: Section 10 - Inverse Head and Shoulders Pattern
- **Inverse head and shoulders pattern:** bullish reversal mirror of head & shoulders (forms at end of downtrend). prereqs: head & shoulders.
### Section: Section 11 - Double Top Pattern
- **Double top pattern:** bearish reversal forming two near-equal tops ("M") at end of an uptrend. prereqs: price action.
### Section: Section 12 - Double-Bottom Pattern
- **Double-bottom pattern:** bullish reversal, two lows near a support level ("W"); neckline between the two lows; confirms support. prereqs: double top.
### Section: Section 13 - Triple and n-Top Pattern
- **Triple and n-Top pattern:** bearish reversal after three (or n) near-equal tops; failure to make a higher high due to buyer/seller imbalance. prereqs: double top.
- **Reversal patterns additional reading:** harmonic patterns, triple-top trading, candlestick reversals. prereqs: reversal patterns.
### Section: Section 14 - Triple-Bottom Pattern
- **Triple-bottom pattern:** bullish reversal, three lows at a strong support zone, seller exhaustion; neckline at the highest interim point. prereqs: double-bottom; triple-top.
### Section: Section 15 - Continuation Patterns
- **Continuation patterns:** patterns that suggest the existing trend will resume (triangles, rectangles, flags, pennants). prereqs: price action.
- **Cup and handle (continuation):** bullish continuation pattern with buy targets. prereqs: continuation patterns.
### Section: Section 16 - Triangle Pattern
- **Triangle pattern:** consolidation/pennant-like continuation pattern formed by converging trendlines. prereqs: continuation patterns.
### Section: Section 17 - Flag Pattern
- **Flag pattern:** short-term consolidation after a sharp move, flagpole + flag; continuation signal. prereqs: continuation patterns.
### Section: Section 18 - Pennant Pattern
- **Pennant pattern:** small symmetrical triangle at the end of a flagpole; continuation signal. prereqs: continuation patterns.
### Section: Section 19 - Support and Resistance
- **Support and resistance:** price levels where buying (support) or selling (resistance) pressure reverses the move. prereqs: price action.
### Section: Section 20 - Strategy Using Support and Resistance
- **Strategy using support and resistance in action:** backtested support/resistance break-and-retest strategy logic. prereqs: support & resistance; backtesting.
### Section: Section 23 - Pivot Points
- **Pivot points:** derived levels from prior-period high/low/close used as intraday support/resistance references. prereqs: support & resistance.
- **Effectiveness of pivot-point strategies:** tested accuracy vs traditional & modified criteria. prereqs: pivot points.
### Section: Section 24 - Types of Pivot Points
- **Types of pivot points:** Standard, Fibonacci, Camarilla and Woodie's pivots (different formulas). prereqs: pivot points.
### Section: Section 25 - Woodie's Range Trading
- **Range trading using Woodie's pivots:** buying at Woodie support, selling at resistance s (mean-reversion around pivot). prereqs: Woodie pivots; range trading.
### Section: Section 26 - Woodie's Trend Trading
- **Woodie's trend trading:** trend-following uses of Woodie's pivots (breakout of pivot levels). prereqs: Woodie pivots; trend following.
### Section: Section 27 - Camarilla Trend Trading
- **Trend-based strategy using Camarilla pivots:** intraday support/resistance around Camarilla levels for trend entries. prereqs: Camarilla pivots; trend.
### Section: Section 28 - Fibonacci Ratios
- **Fibonacci ratios:** 23.6%, 38.2%, 50%, 61.8% retracement/extension levels. prereqs: none.
- **Fibonacci retracement & extension applications; limitations.** prereqs: Fibonacci ratios.
### Section: Section 29 - Fibonacci in Action
- **Fibonacci in action:** plotting retracement/extension levels on price data and their use. prereqs: Fibonacci ratios.
### Section: Section 30 - Fibonacci Retracement Strategy
- **Fibonacci retracement strategy:** entry at retracement support within an uptrend. prereqs: Fibonacci ratios.
- **FAQs on Fibonacci strategy:** placement, targets, validity. prereqs: Fibonacci strategy.
### Section: Section 31 - Short-Selling with Fibonacci Retracements
- **Short selling with Fibonacci:** short entry at a retracement resistance in a downtrend. prereqs: Fibonacci strategy; short selling basics.
### Section: Section 32 - Capstone Project
- **Capstone project:** backtest head & shoulders and inverse head & shoulders on SPY daily (2010–2022); pattern recognition functions; returns box plot. prereqs: all sections.
### Section: Section 34 - Summary
- **Summary of the course:** recap of supply/demand zones, reversal & continuation patterns, support/resistance, pivots, Fibonacci; next steps. prereqs: all sections.
## Course Prerequisite Map
- Foundations: *Price Action Basics → Supply & Demand.*
- Reversal patterns: *Supply/Demand + Support → Head & Shoulders → Inverse H&S; Double Top → Double Bottom → Triple/n-Top → Triple Bottom.* (Each pattern builds on prior reversal concepts.)
- Reversal-pattern detection: *Local Minima/Maxima (Python) → programmatic pattern detection.*
- Continuation patterns: *Continuation concepts → Triangle → Flag → Pennant.*
- Levels tools: *Support/Resistance → Strategy; → Pivot Points → Types (Woodie, Camarilla) → Range/Trend strategies; → Fibonacci Ratios → Retracement Strategy → Short-selling variant.*
- Backtesting/analytics: *Backtesting + Transaction Costs → Performance Analysis.* (Applies to all strategies.)
- Course flow: **Intro → Price Action Basics → Supply/Demand → H&S (+FAQs, Detection) → Inverse H&S → Double/Triple patterns → Continuation (Triangle/Flag/Pennant) → Support/Resistance → Strategy → Pivots (Types/Woodie/Camarilla) → Fibonacci (Ratios/Action/Retracement/Short) → Capstone → Summary.**
- FunPath basics feeding this course: Python for trading, pandas, local extrema (scipy argrelmax), basic backtesting and trade metrics.


====================
Python-for-Machine-Learning
====================

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


====================
Python-for-Trading-Basic
====================

## COURSE: Python for Trading (Basic)
### Hello Python
#### My First Python Code
- PROGRAMMING — telling a machine what to do; also called coding/developing. prereqs: none
- JUPYTER-NOTEBOOK-CELL — code/markdown cells run sequentially with Shift+Enter; a [*] shows a running cell. prereqs: none
- PRINT — built-in function that prints text or variable values to the console. prereqs: none
- STRING-LITERAL — text placed inside quotes ("..."), e.g. "Hello World!". prereqs: print
- PRINT-MULTIPLE-STRINGS — printing several distinct string messages. prereqs: print, string literal
- PYTHON-READABILITY — Python uses near-English syntax and emphasizes coding productivity and readability. prereqs: none
- VARIABLE — a named storage slot holding a value (e.g. x = 2). prereqs: none
- VARIABLE-ASSIGNMENT — the '=' sign means "is set to", not "equal to". prereqs: variable
- ARITHMETIC-OPERATORS — basic operations (+, -, *, /) applied to variables/numbers. prereqs: variables
- SIMPLE-PROGRAM — combining assignment, arithmetic, and print to compute (e.g. sum of two variables). prereqs: variables, print, arithmetic
- VARIABLE-INITIALIZATION — assigning a starting value to a new variable with a comment. prereqs: variables, comment
- ID — built-in id() returns the object's memory address (ID). prereqs: variables
- TYPE — built-in type() returns the data type of an object. prereqs: variables
- DATA-TYPE — the kind of value an object holds (int, float, string); dictates allowed operations. prereqs: variables
- DYNAMIC-TYPING — a variable's type can change automatically on reassignment (int→float→string). prereqs: type, variables
- INT-VS-FLOAT-VS-STRING — numeric types versus text; they live in different memory locations. prereqs: type, data type
- OBJECT-REFERENCE — two variables assigned the same value (b = a) point to the same object ID. prereqs: id, variables
- MULTI-LINE-STATEMENT — split a long statement across lines using backslash '\' line-continuation. prereqs: variables, arithmetic
- INDENTATION — Python requires consistent spaces per code block; wrong indent raises IndentationError. prereqs: comments, variables
- COMMENT — the '#' symbol marks inline explanatory text ignored by Python. prereqs: none
- EXPONENT — '**' raises a number to a power (num ** 2). prereqs: arithmetic
#### Install Packages in Python
- BUILT-IN-PACKAGES — Pandas, NumPy etc. available by default in Python. prereqs: none
- MODULENOTFOUNDERROR — error raised when importing a package not installed. prereqs: import
- PIP — the package installer that manages packages from PyPI (Python Package Index). prereqs: none
- PACKAGE-INSTALL-MAGIC — '!pip install package_name' installs a package from inside a Jupyter notebook. prereqs: pip, packages
- PIP-COMMAND-LINE — 'pip install package_name' run in Command Prompt/Spyder. prereqs: pip
- INSTALL-SPECIFIC-VERSION — 'pip install package==version' installs a particular package version. prereqs: pip, package install
- PERMISSION-DENIED — installing packages on the hosted server is forbidden (EnvironmentError); run notebooks locally. prereqs: pip
- PACKAGE-VERSION — checking an installed package version via package.__version__. prereqs: import, package install
#### Import Python Modules
- MODULE — any .py file holding objects, classes, attributes, functions to be imported. prereqs: none
- IMPORT — statement that loads a module (import math). prereqs: none
- WARNINGS-SUPPRESS — import warnings + warnings.filterwarnings('ignore') to hide warnings. prereqs: import
- DOT-NOTATION — accessing a module object via modulename.obj (math.pi, math.cos, math.sin). prereqs: import, math module
- DIR — built-in dir() lists the names (functions/objects) a module defines. prereqs: import
- FROM-IMPORT — 'from scipy import mean' imports only specific objects from a module. prereqs: import
- SCIPY-STATS — scipy.stats provides statistical functions like harmonic mean hmean. prereqs: from-import, scipy
- FROM-STAR-IMPORT — 'from numpy import *' imports all names (which is discouraged). prereqs: import
- IMPORT-AS-ALIAS — 'import numpy as np' imports a module under a shorter alias. prereqs: import
- NP-MEDIAN — np.median returns the median of a number set. prereqs: numpy, alias import
- NP-MIN-NP-MAX — np.min and np.max return the min/max of a number set. prereqs: numpy, alias import
- MATH-CONSTANTS — math.pi is the constant pi. prereqs: math module, dot notation
### Expressions
#### Use of Expressions
- EXPRESSION — a combination of numbers, variables, and operators that returns a value. prereqs: variables, arithmetic operators
- TVM — Time Value of Money concept: money has different value now vs later. prereqs: none
- FUTURE-VALUE — FV = PV * ((1 + r) ** n); value of an investment after n periods. prereqs: variables, exponent, present value
- PRESENT-VALUE — PV = FV / ((1 + r) ** n); discounting a future amount back. prereqs: variables, exponent
- COMPOUNDING — FV = PV * ((1 + r/n) ** (n*t)) when interest compounds n times per year over t years. prereqs: FV, exponent, variables
- ANNUITY-PAYMENT-FV — AP = (FV * r) / (((1 + r) ** n - 1) * (1 + r)) gives periodic savings to hit a lump sum. prereqs: FV, exponent, TVM
- PV-OF-ANNUITY — PV = (AP * (1 - ((1 + r) ** -n))) / r — present value given regular payments. prereqs: annuity, exponent
- EXPONENT-OPERATOR — '**' computes exponentiation inside financial formulas. prereqs: arithmetic
### Python Data Structures
#### Learn to Create Lists
- LIST — a mutable, ordered collection of heterogeneous elements inside square brackets. prereqs: none
- EMPTY-LIST — creating a list with no elements using []. prereqs: list
- NESTED-LIST — a list that contains other lists (e.g. [[10,20],[10.1,20.2]]). prereqs: list
- MUTABILITY — lists can change content without changing identity. prereqs: list, nested list
- LIST-APPEND — list.append(x) adds an item to the end of the list. prereqs: list
- LIST-EXTEND — list.extend(iterable) appends all items of an iterable to the list. prereqs: list, append
- LIST-INSERT — list.insert(i, x) inserts item x at position i (0 inserts at the start). prereqs: list, indexing
- LIST-REMOVE — list.remove(x) removes the first item equal to x (error if absent). prereqs: list
- LIST-POP — list.pop(i) removes and returns the item at index i; pop() removes the last item. prereqs: list, indexing
- LIST-INDEX — list.index(x) returns the zero-based index of the first matching item. prereqs: list, indexing
- LIST-COUNT — list.count(x) returns how many times x occurs in the list. prereqs: list
- LIST-REVERSE — list.reverse() reverses the order of items in place. prereqs: list, indexing
- LIST-SORT — list.sort() sorts the list items in ascending order. prereqs: list
- METHOD-VS-FUNCTION — methods (e.g. list.append) are functions attached to objects, executed on the object. prereqs: list, dot notation
#### Learn to Create and Print Dictionaries
- DICTIONARY — an unordered key→value mapping enclosed in curly braces { }. prereqs: none
- DICT-CREATION — creating a dict with 'key': value pairs separated by commas. prereqs: dictionary
- EMPTY-DICT — empty dictionary `{}`. prereqs: dictionary
- DICT-ACCESS-BY-KEY — retrieving a value using dict['key']. prereqs: dictionary, dict creation
- LEN-DICT — len(dict) returns the number of key-value pairs. prereqs: dictionary
- DICT-KEYS — dict.keys() returns all keys of the dictionary. prereqs: dictionary
- DICT-VALUES — dict.values() returns all values of the dictionary. prereqs: dictionary, keys
- DEL-DICT — del dict['key'] statement deletes a key from the dictionary. prereqs: dictionary, access by key
- DICT-POP — dict.pop(key) removes a key and returns its value. prereqs: dictionary, del dict
- SORTED-DICT — sorted(dict) returns the keys sorted by value. prereqs: dictionary, dict keys
- DICT-CLEAR — dict.clear() removes all key-value pairs. prereqs: dictionary
#### Learn to Create Tuples and Sets
- TUPLE — an immutable sequence enclosed in parentheses (). prereqs: list
- TUPLE-CREATION — tuple items separated by commas inside parentheses. prereqs: tuple
- NESTED-TUPLE — a tuple containing other tuples. prereqs: tuple
- TUPLE-IMMUTABLE — a tuple cannot be appended, edited, or item-reassigned after creation. prereqs: tuple, list mutability
- TUPLE-INDEXING — accessing an item at a given index with tuple[i] (read only). prereqs: tuple, indexing
- LEN-TUPLE — len(tuple) returns the number of elements. prereqs: tuple
- SET — an unordered collection of unique (no duplicate) elements, mutable. prereqs: none
- SET-CREATION — creating a set with curly braces or the set() function. prereqs: set
- SET-DEDUPLICATION — a set automatically keeps only unique values (duplicates vanish). prereqs: set, set creation
- SET-FROM-STRING — set('THEMATRIX') breaks a string into its unique characters. prereqs: set creation, string
- SET-UNION — x.union(y) or x | y returns all unique items of both sets. prereqs: set, set creation
- SET-INTERSECTION — x.intersection(y) or x & y returns items common to both sets. prereqs: set, union
- SET-DIFFERENCE — x.difference(y) or x - y returns items in set 1 not in set 2. prereqs: set, union, intersection
- SET-DIFFERENCE-UPDATE — x.difference_update(y) removes set 2's elements from set 1 in place. prereqs: set, difference
- SET-ISDISJOINT — x.isdisjoint(y) returns True if two sets have no common items. prereqs: set, intersection
- SET-ISSUBSET — y.issubset(x) (or y < x) is True if every element of y is in x. prereqs: set, difference, set operators
- SET-ISSUPERSET — x.issuperset(y) (or x > y) is True if x contains all elements of y. prereqs: set, subset
- SET-ADD — x.add(e) adds a single item to the set, updating it. prereqs: set
- SET-DISCARD — x.discard(e) removes a single item from the set. prereqs: set, add
- SET-POP — x.pop() pops and returns an arbitrary item from the set. prereqs: set, add, discard
- SET-COPY — x.copy() creates a (shallow) copy of the set. prereqs: set
- SET-CLEAR — x.clear() removes all items from the set. prereqs: set, copy
#### What Are Stacks, Queues, Graphs & Trees
- STACK — a LIFO (Last In, First Out) collection of objects. prereqs: list
- LIFO-PRINCIPLE — the last item added to a stack is removed first. prereqs: stack
- STACK-PUSH — adding to a stack using the append() method. prereqs: list, stack, LIFO
- STACK-POP — stack removal from the top using the pop() method. prereqs: list, stack, push
- QUEUE — a FIFO (First In, First Out) collection of objects. prereqs: list
- FIFO-PRINCIPLE — the first item arrived is removed first. prereqs: queue
- DEQUE — deque from the 'collections' module — a list-like container with fast appends/pops at both ends. prereqs: queue, import
- QUEUE-ENQUEUE — appending to a deque to add arriving items. prereqs: deque, queue
- DEQUE-POPLEFT — my_queue.popleft() removes the leftmost (first-arrived) item. prereqs: deque, queue append
- QUEUE-EFFICIENCY — lists as queues with insert/remove are inefficient (elements shift); deque is preferred. prereqs: queue, deque
- GRAPH — a network of nodes (vertices) connected by edges. prereqs: none
- GRAPH-TYPES — directed graphs (edges have direction) vs undirected graphs (no direction). prereqs: graph
- GRAPH-ADJACENCY-DICT — representing a graph as a dictionary of adjacency lists (node → neighbours). prereqs: dictionary, graph, list
- EDGE-ENUMERATION — functions with nested for loops to list all edges of a graph. prereqs: dictionary, function, for loop, graph
- TREE — a tree data structure with root node, branch nodes, and leaf nodes. prereqs: graph
- CLASS — user-defined blueprint grouping data + methods (e.g. Tree). prereqs: tree, object
- INIT-METHOD — class __init__( self, ...) sets up a new instance's attributes. prereqs: class, instance attributes
- INSTANCE-ATTRIBUTE — self.info, self.left, self.right store per-instance data. prereqs: class, __init__
- STR-METHOD — class __str__(self) defines how print() displays the object. prereqs: class, __init__
- OBJECT-INSTANTIATION — calling a class with args builds an instance (tree = Tree("Root", ...)). prereqs: class, __init__
### Conditional Statements and Loops
#### Introduction to Conditional Statements
- IF-STATEMENT — if (condition): executes a block only when the condition is True. prereqs: comparison operators, indentation, variables
- ELIF — if (cond1)... elif... chains for multiple mutually exclusive conditions. prereqs: if-statement, comparison
- IF-ELSE — 'if (cond): block' else ": block — executes the else block when the if is False. prereqs: if-statement, elif
- COMPARISON-OPERATORS — <, >, == evaluate relationship between two values to a Boolean. prereqs: variables, conditions
- TRADING-CONDITIONAL — using if/elif/else to decide buy/sell/hold share counts based on stock price thresholds. prereqs: if, elif, comparison
#### Introduction to Loops
- FOR-LOOP — for variable in sequence: repeats a block once per sequence element. prereqs: list, indentation, print
- SEQUENCE-ITERATION — the loop variable takes each element of a list/sequence in turn. prereqs: for-loop, list, if
- NESTED-IF-IN-LOOP — placing if statements inside a for loop to classify each element (Buy/No positions/Sell). prereqs: for-loop, if, list
- RANGE-LEN-LOOP — for i in range(len(df)) to iterate over integer row positions. prereqs: len, range, pandas, for loop
- ILOC-ROW-ACCESS — infy.iloc[i]['Close Price'] fetches a specific row/column value. prereqs: pandas, iloc row access, for loop
- WHILE-LOOP — while (condition): block — repeats while the condition is True. prereqs: comparison, variables, indentation
- WHILE-PRINT-COUNTER — a = a + 1 increments a counter inside the while loop until the condition turns False. prereqs: while-loop, variables, assignment
### Importing Data and Data Visualisation
#### Import Data from Web Sources
- WEB-DATA-IMPORT — fetching market data directly from a web source (Yahoo Finance). prereqs: pip, imports
- YFINANCE-INSTALL — pip install yfinance to access Yahoo Finance data. prereqs: pip install, package install
- YF-DOWNLOAD — yf.download('AAPL', start, end) returns price history as a DataFrame. prereqs: yfinance, pandas, datetime
- SECONDARY-REFERENCES — reading about alternative/parallel market data sources. prereqs: web import, yfinance
#### Read Data from CSV Files
- CSV-READ — pandas.read_csv() reads a Comma-Separated file into a DataFrame. prereqs: pandas
- LOCAL-DATA-FILE — pandas.read_csv('path/file.csv') loads a CSV stored on the local disk. prereqs: pandas, read_csv
- TRADING-CSV-READ — pandas.read_csv is the most frequently used data-loading function for trading strategies. prereqs: pandas, read_csv
- CSV-VS-WEB-STABILITY — CSV is stable local data; web sources need third-party access that may fail or forbid requests. prereqs: import data web, read_csv
- HEAD — DataFrame.head() shows the first 5 rows. prereqs: read_csv, dataframe
- TAIL — DataFrame.tail() shows the last 5 rows. prereqs: read_csv, dataframe, head
#### Data Visualization
- MATPLOTLIB — robust plotting library ('matplotlib.pyplot' sublibrary). prereqs: import
- IMPORT-PYPLOT — import matplotlib.pyplot as plt and %matplotlib inline to embed plots. prereqs: matplotlib, notebook cell
- PLT-PLOT — plt.plot(data) draws a line plot of the data. prereqs: matplotlib, dataframe column
- PLT-SHOW — plt.show() renders/displays the plot figure. prereqs: plt.plot, figure
- DATAFRAME-SET-INDEX — df.set_index('Date', inplace=True) sets a column as the row index. prereqs: pandas, dataframe, column selection
- DATAFRAME-COLUMN-SELECTION — infy[['Date', 'Close Price']] selects specific columns. prereqs: pandas, dataframe
- PLOT-CHARACTERIZATION — 'b' draws a blue line, 'g' a green line; 'ro' draws red circular markers. prereqs: plt.plot, figure
- FIGURE-SIZE — plt.figure(figsize=(14,5)) sets the plot width/height. prereqs: matplotlib, plt
- PLOT-COLOR-MARKERS — color strings 'b' line, 'ro' colored markers (r=red, o=circle). prereqs: plt.plot, figure
- PLT-GRID — plt.grid(True) adds a grid layout to the plot. prereqs: plt, figure
- PLT-TITLE — plt.title('...') sets the plot title. prereqs: plt, figure
- PLT-XLABEL-YLABEL — plt.xlabel('...') and plt.ylabel('...') label the axes. prereqs: plt, title, grid
- MULTI-SERIES-PLOT — plotting two series (Close, Open) on the same figure. prereqs: plt.plot, dataframes columns
- PLT-LEGEND — plt.legend(loc=0) displays a legend (loc=0 is best fit). prereqs: matplotlib, labels
- PLOT-LABEL — passing label='Close Price' to plt.plot names a series for the legend. prereqs: plt.plot, legend
- PLOT-LINE-WIDTH — the lw=1.5 linewidth argument in plt.plot controls line thickness. prereqs: plt.plot, figure
- PLT-AXIS-TIGHT — plt.axis('tight') reduces whitespace to data bounds. prereqs: plt, figure, legend
- SCATTER-PLOT — plt.scatter(x, y, marker='o') creates a scatter plot. prereqs: numpy, matplotlib
- RANDOM-STANDARD-NORMAL — np.random.standard_normal(shape) generates normal-distributed random values. prereqs: numpy arrays
- HISTOGRAM — plt.hist(data) creates a frequency histogram. prereqs: numpy, matplotlib
- NP-RANDOM-SEED — np.random.seed(n) makes random generation reproducible. (prereqs: numpy)
- RETURNS-HISTOGRAM-DIST — plotting returns distribution as a histogram with Frequency and Returns In Percentage axes. prereqs: numpy, histogram
#### 3D Plotting
- NP-LINSPACE — np.linspace(start, stop, n) creates n evenly spaced points. prereqs: numpy
- NP-MESHGRID — np.meshgrid(x, y) builds a rectangular grid from x and y 1D arrays. prereqs: numpy, linspace, arrays
- ARRAY-ARITHMETIC — scalar-array formulas (e.g. fake implied volatility) computed element-wise. prereqs: numpy arrays, operators
- IMPLIED-VOLATILITY — modelled as (strike−100)²/(100·strike·time) across a surface. prereqs: meshgrid, arrays
- 3D-AXES-IMPORT — from mpl_toolkits.mplot3d import Axes3D enables 3D plotting axes. prereqs: matplotlib
- ADD-SUBPLOT-3D — fig.add_subplot(111, projection='3d') creates a 3D axes subplot. prereqs: matplotlib, figure
- PLOT-SURFACE — axis.plot_surface(x, y, z, cmap, rstride, cstride) draws a 3D surface. prereqs: 3D axes, meshgrid, arrays
- COLORMAP — cmap=plt.cm.coolwarm colours the surface by value. prereqs: plot_surface, colormap
- SETXLABEL-SETZ — axis.set_xlabel/set_ylabel/set_zlabel label the three axes. prereqs: 3D axes, plot_surface
- COLORBAR — fig.colorbar(surface) maps values to colors alongside the 3D figure. prereqs: matplotlib, plot_surface
#### Candlesticks (Optional Read)
- CANDLESTICK-CHART — candlestick chart shows OHLC price action of a day as a candle. prereqs: read csv, pandas
- READ-CSV-INDEX — pd.read_csv(file, index_col=0) uses the first column as the index. prereqs: pandas, read_csv
- PD-TO-DATETIME — pd.to_datetime(df.index) converts a string index to datetime. prereqs: pandas, index
- BOKEH-PLOTTING — bokeh.plotting figure/shows/output_file builds interactive web graphs. prereqs: bokeh, pandas
- BOKEH-FIGURE — figure(x_axis_type='datetime', tools=...) creates an interactive plot. prereqs: bokeh, datetime index
- BOOL-SERIES-COMPARISON — inc = df.Close > df.Open produces a Boolean mask of green days. prereqs: pandas, comparison
- CANDLE-COLOR-RULE — green candle when Open < Close; red candle when Open > Close. prereqs: Boolean mask
- BOKEH-SEGMENT — p.segment(x, high, y, low) draws high–low lines (wicks). prereqs: bokeh figure, Boolean masks
- BOKEH-VBAR — p.vbar(index, w, open, close, ...) draws candlestick bodies. prereqs: bokeh, segment, Boolean masks
- PIPELINE-COLOURS — vbar fill colours #1ED833 (green/increase) and #F258E (red/decrease). prereqs: vbar, Boolean masks
- BOKEH-INTERACTIVE-TOOLS — pan, wheel zoom, box zoom, reset, save tools for the figure. prereqs: bokeh figure
- BOKEH-OUTPUT-FILE — output_file('name.html') exports the graph to an HTML file. prereqs: bokeh, show
- BOKEH-SHOW — finally show(p) opens the interactive graph in the browser. prereqs: bokeh figure, output_file
- GRID-ALPHA — p.grid.grid_line_alpha = 0.3 sets gridline transparency. prereqs: bokeh figure
- XAXIS-ORIENTATION — p.xaxis.major_label_orientation = pi/4 rotates tick labels. prereqs: bokeh, math.pi
## Numpy
#### Introduction to Arrays
- NUMPY — 'NumPy' — the fundamental package for scientific computing with Python. prereqs: none
- IMPORT-NUMPY-AS-NP — importing the numpy library with alias np. prereqs: numpy
- NP-ARRAY — np.array(sequence) creates an N-dimensional array from a list or tuple. prereqs: numpy, list
- NDARRAY-DTYPE — np.ndarray is the array data type object. prereqs: numpy, np.array
- ARRAY-ALTERED — np.array(stockvalues) makes an array from a tuple. prereqs: numpy, tuple, np.array
- NP-ARANGE — np.arange(start, stop, step, dtype) returns steps evenly spaced array. prereqs: numpy
- ARANGE-DEFAULTS — start defaults to 0, step defaults to 1, dtype inferred from arguments. prereqs: np.arange
- ARANGE-EXCLUSIVE-STOP — arange(1,15) includes 1 but excludes 15. prereqs: np.arange
- ARANGE-STEP — np.arange(0,21,2) spaces values every 2. prereqs: np.arange
- ARANGE-DTYPE — np.arange(1.3, 23.3, 2.1, int) forces float inputs to int output via dtype. prereqs: np.arange, dtype
- NP-LINSPACE — np.linspace(start, stop, num=50, endpoint=True, retstep=False) evenly spaced array given count. prereqs: numpy arrays
- LINSPACE-NUM — num sets the number of elements in the array (default 50). prereqs: np.linspace
- LINSPACE-ENDPOINT — endpoint=True includes stop; False excludes it. prereqs: np.linspace
- LINSPACE-RETSTEP — retstep=True also returns the spacing between adjacent values. prereqs: np.linspace
- ARRAY-DIMENSIONS — arrays can be 0-D (scalar), 1-D (vector), 2-D (rows/cols), N-D. prereqs: numpy arrays
- SCALAR-ARRAY — a zero-dimensional array with a single element. prereqs: np.array, arrays
- NP-NDIM — np.ndim(array) returns the number of dimensions of an array. prereqs: numpy arrays
- ARRAY-DTYPE-METHOD — .dtype attribute returns the datatype of the array. prereqs: np.ndim, arrays
- ONE-D-ARRAY — a 1-D array (vector) of at least two elements in one row. prereqs: arrays, np.array
- TWO-D-ARRAY — a 2-D array of multiple rows and columns, elements addressable as row/col. prereqs: arrays, np.array
- THREE-D-ARRAY — a 3-D array, i.e. an array of 2-D arrays. prereqs: 2D arrays, arrays
- STRING-COERCION — mixed numeric/string data in a 2D array is coerced to strings, blocking arithmetic. prereqs: 2D arrays, dtype
- ARRAY-SHAPE — array.shape or np.shape returns (rows, columns), axis 0 rows, axis 1 columns. prereqs: arrays, ndim
- RESHAPE-ASSIGNMENT — assigning a.shape = (r,c) reshapes the array (size must match). prereqs: ndim, array shape
- SHAPE-VS-DIM — shape expresses rows/columns (a.shape); dimensions expressed by np.ndim. prereqs: shape, ndim
- ARRAYS-VS-DATAFRAME — DataFrames handle mixed types and arithmetic that plain arrays cannot (demo with pd.DataFrame + np.mean). prereqs: np.array, pandas DataFrame
#### Indexing & Slicing Arrays
- ARRAY-INDEX-0-BASED — array elements are located by index starting at 0. prereqs: arrays
- NEGATIVE-INDEXING — index -1 = last element, -2 = second-last. prereqs: indexing 0-based, array
- 1D-INDEXING — access A[0], A[-1], A[i] in one-dimensional arrays. prereqs: arrays, indexing
- 2D-INDEXING-TWO-BRACKETS — A[row][col] accesses a 2D element via two bracket pairs. prereqs: 2D arrays, indexing
- INDEXING-COMMA — A[row, col] selects a 2-D element with a comma. prereqs: 2D arrays, indexing
- 2D-INDEXING — locating a 2-D element requires both row and column indices. prereqs: 2D arrays, indexing
- SLICING — extracting subscripted subarrays array[start:stop:step]. prereqs: indexing
- SLICE-STOP-EXCLUSIVE — slicing A[2:5]: stop index is excluded. prereqs: slicing
- DEFAULT-SLICE-BOUNDS — slicing uses default start/stop/step when omitted (A[:] whole, A[:4] first 4, A[6:] from 6, A[2:5] range). prereqs: slicing
- STEP-SLICING — A[::2] selects alternating elements by a step. prereqs: slicing, start/stop
- 2D-SLICING — slicing rows and columns with array[row_slice, col_slice]. prereqs: slicing, 2D arrays
- ROW-COL-MASK-SLICING — A[:, 1] selects a column, A[1, :] selects a row. prereqs: 2D slicing
- STEP-IN-2D — A[::2, :], A[:, 1:5:2] apply steps over rows/columns separately. prereqs: 2D slicing
- ARANGE-RESHAPE — np.arange(50).reshape(5,10) creates an array of 5 rows and 10 columns. prereqs: np.arange, reshape
- NP-ONES — np.ones((r,c)) array of element ones (default float dtype). prereqs: slicing, arrays
- ONES-DTYPE — np.ones((r,c), dtype=int) builds the array with integer values. prereqs: np.ones
- NP-ZEROS — np.zeros((r,c)) creates an array of zeros. prereqs: ones, arrays
- NP-IDENTITY — np.identity(n) square array with diagonal element ones. prereqs: np.ones, np.zeros, arrays
- RESHAPE-LINK — reshaping shares memory; assigning one element then affects both arrays (B = A.reshape shared view). prereqs: reshape, arrays
#### Vectorization & Broadcasting in Arrays
- VECTORIZATION — operating on an entire array at once instead of iterating element-by-element (faster, compact code). prereqs: numpy arrays
- SCALAR-ADD — each array element increased by a scalar using V + 2. prereqs: vectorization, arrays
- SCALAR-SUBTRACT — each element reduced by a scalar using V − 2.4. prereqs: vectorization, arrays
- SCALAR-MULTIPLY — each element multiplied by a scalar (V2 * 10). prereqs: vectorization, arrays
- ARRAY-POWER — element-wise exponentiation (V2 ** 2). prereqs: scalar multiply, arrays
- ELEMENT-WISE-ADD — 2 arrays of same shape are added element-by-element with a + B. prereqs: vectorization, arrays
- ELEMENT-WISE-SUBTRACT — A -B is element-wise. prereqs: elementwise add, same-shape arrays
- ELEMENT-WISE-MULTIPLY — A * B is element-wise (not matrix multiplication). prereqs: elementwise, add
- SHAPE-MISMATCH-ERROR — adding arrays of different shapes raises a ValueError (must use broadcasting). prereqs: elementwise add, same-shape arrays
- BROADCASTING — combining objects of different shapes in one operation, when a vector length equals one array dimension. prereqs: numpy arrays, vectorization
- BROADCAST-MULTIPLY — multiplying a 2-D array by a compatible 1-D vector via broadcasting. prereqs: broadcasting, arrays
- BROADCAST-ADD — adding a 1-D vector to a 2-D array via broadcasting. prereqs: broadcasting, multiply
- NP-NEWAXIS — B[:, np.newaxis] converts a row vector into a column vector(one missing dimension axis). prereqs: broadcasting, arrays
- BROADCAST-COLUMN — multiplying A * B[:, np.newaxis] broadcasts a column vector along rows. prereqs: np.newaxis, broadcasting
- BROADCAST-CROSS — using A[:, np.newaxis] and B to form an outer/product of array broadcasting. prereqs: np.newaxis, broadcasting, arrays
- ARRAY-COMPARISON — A == B compares two arrays element-wise and returns a Boolean array. prereqs: arrays, vectorization, comparison
- ARRAY-EQUAL — np.array_equal(A, B) returns True only if all elements and arrangement match. prereqs: array comparison
- LOGICAL-AND — np.logical_and(a, b) element-wise AND of Boolean arrays. prereqs: arrays, logical comparison
- LOGICAL-OR — np.logical_or(a, b) element-wise OR of Boolean arrays. prereqs: arrays, logical comparison
### Pandas
#### Introduction to Series
- SERIES — a one-dimensional labelled array-like object; a single data column with an index. prereqs: numpy arrays, index
- SERIES-FROM-LIST — pd.Series([...]) builds a Series from a list with automatic index. prereqs: pandas, list
- SERIES-CONSTRUCTOR — pd.Series(data=None, index=None, dtype=None, name=None) is the Series constructor. prereqs: pandas, series
- SERIES-DTYPES — a Series can hold int, float, or mixed types (mixed → object dtype). prereqs: series, dtype
- OBJECT-DTYPE — a Series holding string/heterogeneous values gets the object datatype. prereqs: series, mixed python objects
- SERIES-CUSTOM-INDEX — pd.Series(data, index=list) assigns explicit index labels. prereqs: series, list, construct
- SERIES-INDEX-ALIGNMENT — adding two Series aligns by index labels position-wise. prereqs: series, arithmetic
- SERIES-INDEX-MISMATCH — adding Series with differing indexes produces NaN for missing labels. prereqs: series alignment
- NAN — NaN (Not a Number) is the mark for missing/corrupt data. prereqs: series, alignment
- SERIES-INDEX — Series.index returns the index range of a Series. prereqs: series, index
- SERIES-VALUES — Series.values returns the raw values of the series. prereqs: series
- SERIES-ISNULL — Series.isnull() returns True for missing (NaN) values. prereqs: series, NaN
- SERIES-DROPNA — Series.dropna() filters out/drops missing data values. prereqs: series, NaN, isnull
- SERIES-FILLNA — Series.fillna(scalar) fills custom NaN values with a chosen scalar. prereqs: series, NaN
- SERIES-APPLY — Series.apply(func) applies any Python function to each value. prereqs: series, function, numpy
- APPLY-SIN-TAN — applying np.sin / np.tan to every element via apply(). prereqs: series-apply, numpy
#### DataFrame & Basic Functionality
- DATAFRAME — a 2-D spreadsheet-like structure with discrete rows and columns, each column named/indexed. prereqs: series, numpy
- DATAFRAME-CONSTRUCTOR — pd.DataFrame(data=None, index=None) builds a DataFrame (rows+ column index). prereqs: pandas
- DICT-TO-DATAFRAME — creating a DataFrame from a dict of column: list of entries. prereqs: dictionary, dataframe, series
- CUSTOM-DATAFRAME-INDEX — passing index=ordinals (default index) as list of row labels. prereqs: dataframe, index
- DATAFRAME-COLUMN-ORDER — defining column order with columns=[...] in the constructor. prereqs: dataframe, custom index
- DATAFRAME-SET-INDEX-COLUMN — passing index=SomeSeries (e.g. stock names) to use a column as index. prereqs: dataframe, columns, custom index
- DATAFRAME-ACCESS-CO-BLOCK — dataframe['col'] retrieves a single named column (Series). prereqs: dataframe, columns
- LOAD-FINANCIAL-DATA — loading stock data from a CSV with pd.read_csv and showing it. prereqs: pandas, read_csv
- HEAD-TAIL-ON-DATA — df.head() / df.tail() preview first/last rows of loaded market data. prereqs: read_csv, dataframe
- DROP-COLUMNS — DataFrame.drop(['col',...], axis=1) removes columns; axis=1 refers to columns. prereqs: dataframe, columns
- DROP-ROWS — df.drop(df.index[[3,4]]) removes specific rows by index position. prereqs: dataframe, index
- RENAME-COLUMNS — df.rename(columns={'Old':'New'}) renames columns. prereqs: dataframe, columns
- SORT-VALUES — df.sort_values(by='col', ascending=False) sorts the dataframe by a column value. prereqs: dataframe, columns
- RANDOM-INT — np.random.randint(50000, 120000, size=(12,5)) fills an array with random draw. prereqs: numpy, dataframe
- DATAFRAME-FROM-RANDOM — pd.DataFrame(data, columns=names, index=months) builds labeled frame from a random array. prereqs: np.random.randint, dataframe
#### Descriptive Statistical Function
- DATA-PREP — loading OHLC data into a dataframe; good habit to view head/tail. prereqs: pandas read_csv, pandas
- DATAFRAME-COUNT — df.count() returns non-null observation count for whole frame or a column. prereqs: dataframe, pandas
- DATAFRAME-MIN — df.min() returns minimum value of a column or all columns. prereqs: dataframe
- DATAFRAME-MAX — df.max() returns maximum value. prereqs: dataframe, min
- DATAFRAME-MEAN — df.mean() returns the arithmetic average. prereqs: dataframe, statistical
- DATAFRAME-MEDIAN — df.median() returns middle-value median of ascending dataset. prereqs: dataframe, mean
- DATAFRAME-MODE — df.mode() returns the most frequent value(s) in the data. prereqs: dataframe, median
- DATAFRAME-SUM — df.sum() returns total sum of requested observations. prereqs: dataframe, mean
- DATAFRAME-DIFF — df.diff() returns difference between current and previous observation. prereqs: dataframe
- DATAFRAME-PCT-CHANGE — df.pct_change() returns percentage change from prior observation (daily returns). prereqs: dataframe, diff
- RETURNS-PLOT — plotting pct_change() returns to observe daily price fluctuation. prereqs: matplotlib, pct_change, dataframe
- DATAFRAME-VAR — df.var() returns variance (spread) of the dataset. prereqs: dataframe, mean
- DATAFRAME-STD — df.std() returns standard deviation (dispersion relative to mean). prereqs: dataframe, variance
- ROLLING-MEAN — df.rolling(window=n).mean() computes moving/rolling average on technical indicator. prereqs: dataframe, mean, window
- MOVING-AVERAGE-SMOOTHING — rolling mean of close price smooths the noisy price series. prereqs: rolling, dataframe, matplotlib
- EXPANDING-MEAN — df.expanding(min_periods=n).mean() uses all data up to each point in time. prereqs: dataframe, rolling mean
- DATAFRAME-COV — df['A'].cov(df['B']) computes covariance between two assets' returns. prereqs: dataframe, statistics
- DATAFRAME-CORR — df['A'].corr(df['B']) computes correlation (linear relation) between two series. prereqs: dataframe, covariance
- KURTOSIS — df.kurt() returns Fisher kurtosis tail-heavy measure; + leptokurtic, − platykurtic. prereqs: corr, statistics
- SKEWNESS — df.skew() measures asymmetry of the distribution around the mean (positive skew). prereqs: kurtosis, statistics
- SEABORN-IMPORT — import seaborn as sns for statistical visualizations. prereqs: seaborn, matplotlib
- SNS-DISTPLOT — sns.distplot(series) plots a distribution of a numeric series. prereqs: seaborn, skewness/kurtosis
- SNS-SET — sns.set(color_codes=True) sets seaborn plotting configuration. prereqs: seaborn, distplot
#### Indexing & Missing Values
- DATAFRAME-SHAPE — df.shape returns number of rows & columns. prereqs: dataframe, pandas
- INDEXING-PANDAS — label-based/location-based data selection in dataframes. prereqs: dataframe, index
- LOC-INDEXER — df.loc[row, col] label-based location selection; includes stop when slicing. prereqs: indexing, dataframe
- LOC-COLUMN-ROW — infy.loc[:, 'Close'] selects all rows for a column by label. prereqs: loc
- LOC-MULTI-COLUMN — infy.loc[:, ['col1','col2']] selects multiple columns. prereqs: loc, dataframe
- LOC-SLICING-INCLUSIVE — df.loc[:4, cols] includes row index 4 (inclusive stop) unlike iloc. prereqs: loc, slicing
- LOC-ROWS-2-7 — df.loc[2:7] selects rows 2-7 all columns by label. prereqs: loc, slicing
- BOOLEAN-MASK — df.loc[[4], [...]] > 1130 compares rows and returns a boolean grid. prereqs: loc, comparison
- ILOC-INDEXER — df.iloc[r1:r2, c1:c2] integer-position selection; EXCLUDES stop in slicing. prereqs: indexing, numpy
- ILOC-ROWS-COLUMNS — infy.iloc[1:5, 2:4] integer-position rows and columns. prereqs: iloc, indexing
- ILOC-LIST-OF-ROWS-COLS — df.iloc[[1,3,5,7],[1,3,5,7,9]] pick specific positional rows/cols. prereqs: iloc, integer indexing
- MISSING-VALUES — actual data often contains missing values (NaN) needing handling. prereqs: dataframe, pandas
- ISNULL — df.isnull() returns True where a cell is NaN (boolean frame). prereqs: dataframe, NaN
- NOTNULL — df.notnull() returns True where a cell is not NaN. prereqs: isnull, NaN
- FILLNA-SCALAR — df.fillna(1000) or per-column fills every NaN with that scalar value. prereqs: isnull, NaN
- FILLNA-BACKFILL — fillna(method='backfill'|'bfill') fills NaN with the next-row value. prereqs: fillna, NaN
- FILLNA-FFILL — fillna(method='ffill'|'pad') fills NaN with the previous-row value. prereqs: fillna, NaN
- DROPNA — dropna() drops rows (axis=0) or with axis=1 columns having any NaN. prereqs: isnull, df
- REPLACE-VALUES — df.replace({old: new}) finds/replaces given values in the dataframe. prereqs: dataframe, fillna
- REINDEXING — reindex(index=[...], columns=[...]) conforms data to new labels and shape. prerequisites: label indexing, loc
#### Grouping & Reshaping
- PD-GROUPBY — split-apply-combine aggregation on a dataframe. prereqs: dataframe, pandas
- SPD-SPLIT-APPLY-COMBINE — grouping breaks data into groups, applies a function, and combines results. prereqs: groupby
- GROUPBY-APPLY-OPS — aggregation, transformation, or filtration in the apply step. prereqs: groupby
- GROUPBY-GROUPS — mp.groupby('MarketCap').groups shows index memberships per group. prereqs: groupby, dataframe
- GROUPBY-MULTI-COLUMN — groupby(['A','B']) groups by combination of multiple columns. prereqs: groupby, groups
- ITERATE-GROUPS — for name, group in grouped: iterates over each group. prereqs: for loop, groupby
- SELECT-GROUP — grouped.get_group('Mid Cap') selects only rows in that group. prereqs: groupby, iterate-groups
- GROUPBY-AGG — grouped['col'].agg(np.mean) computes mean per group; np.size gives group size. prereqs: groupby, aggregation
- MULTIPLE-AGGRE-AGG — grouped['col'].agg([np.sum, np.mean]) applies several aggregation functions at once. prereqs: grouping aggregation
- GROUPBY-TRANSFORM — grouped.transform(z_score) computes per-group transformation like z-score = (x-mean)/std. prereqs: groupby, function, agg
- Z-SCORE-FUNCTION — def z_score(x): return (x−x.mean()) / x.std() and then attributing numeric columns. prereqs: transform, function, dataframe
- GROUPBY-FILTER — grouped.filter(lambda x: len(x) >= 3) removes groups failing a condition. prereqs: groupby, transform, lambda
- MERGE-DATA — pd.merge(left, right, on='key') merges two dataframes on a common column. prereqs: dataframe, key column
- MERGE-MULTIKEYS — pd.merge(left, right, on=['Sector','Company']) merges on multiple keys. prereqs: merge, on
- MERGE-HOW — merge with how='left'| 'right' | 'outer' | 'inner' selects join type. prereqs: merge, on
- CONCATENATE — pd.concat([df1, df2]) stacks dataframes along rows. prereqs: dataframes
- CONCAT-KEYS — pd.concat([...], keys=['x','y']) adds hierarchical identifiers. prereqs: concat
- CONCAT-IGNORE-INDEX — pd.concat(..., ignore_index=True) resets the index. prereqs: concat, keys
- CONCAT-AXIS — pd.concat([...], axis=1) places dataframes side by side (columns). prereqs: concat
### Buy and Hold Strategy
#### Coding a Buy and Hold Strategy
- BUY-AND-HOLD-STRATEGY — investing idea: buy stocks and hold long-term, rebalancing monthly. prereqs: none/strategy background
- PORTFOLIO — of 8 US stocks, equally weighted, rebalanced each month. prereqs: equity, strategy
- PD-READ-CSV — pd.read_csv(filename, index_col=0) loads daily stock closes; index_col sets row labels. prereqs: pandas read_csv, index col
- DATETIME-INDEX — daily_stocks_data.index = pd.to_datetime(...) sets datetime index. prereqs: read_csv, pandas datetime
- ASFREQ — DataFrame.asfreq('M') converts daily series to monthly frequency. prereqs: pandas, datetime index
- RESAMPLE-DROPNA — dropna() drops NaN rows after resampling/returns calculation. prereqs: pandas, asfreq
- RETURNS-CALCULATION — monthly_percent_change = data.pct_change() computes monthly percentage returns. prereqs: asfreq, pandas, pct change
- PORTFOLIO-RETURNS — mean(axis=1) average monthly returns across stocks = equal-weight portfolio returns. prereqs: pct_change, pandas mean
- WEIGHTING-NOTE — portfolio returns use per-stock weights multiplied by returns and summed. prereqs: portfolio returns, numpy
- CUMPROD — (returns+1).cumprod() compounds to cumulative portfolio returns over time. prereqs: portfolio returns, pandas
- STYLE-USE — plt.style.use('seaborn-darkgrid') sets a plot style. prereqs: matplotlib.style, plot
- STRATEGY-PLOT — cum_portfolio_returns.plot(figsize=(10,7)) plots the cumulative strategy curve. prereqs: pandas plot, matplotlib, cumprod
- PLOT-LABELS-TITLE — plt.title/label-fontsize sets title and axis label font sizes. prereqs: plot, matplotlib
- STRATEGY-REPLICATION — strategy can be retested on other stocks with different rebalance frequencies. prereqs: buy&hold, pandas
# Prerequisite Map
- Python environment setup (install Python, run Jupyter/Spyder notebooks); running code cells
- Basic computer literacy (files/paths, running install commands)
- No prior programming is assumed — the course teaches programming from Hello World onward
- Basic math: arithmetic, exponents/exponentiation (needed for TVM and array operations), percentages
- Basic time-value-of-money familiarity (present/future value intuition) — TVM formulas are used to demonstrate expressions
- Foundational knowledge of the financial/market domain: stocks, shares, buying/selling, OHLC data, moving averages, technical indicators, portfolio, equal-capital/allocation, rebalancing, returns, extended indices (Nifty, S&P 500), market cap terminology
- Basic statistics intuition: mean, median, variance, standard deviation, correlation, kurtosis, skewness (used in descriptive-statistics section)
- Comfort reason editing/reviewing tabular (spreadsheet-like) data and plotting charts


====================
Quantitative-Portfolio-Management
====================

# Quantitative Portfolio Management — Concept Inventory
> 11 notebooks (no shared code module; data files in `data_modules/`).
Course flow: portfolio construction mathematics → Modern Portfolio Theory → risk-based weights (Risk Parity, Kelly) → single-asset risk (Beta) → factor models (Momentum, Short-Term Reversal, Fama-French) → performance measurement → capstone.
---
## Notebooks
### 1. Basics of Portfolio Construction — **Basics of Portfolio Construction_/Basics of Portfolio Construction.ipynb**
- **Annualized returns** of individual stocks (compound/geometric annualization of cumulative returns over trading days). *Prereq: daily returns, pct_change, trading days/year.
- **Annualized standard deviation (volatility)** of stock returns (daily σ × √trading days). *Prereq: standard deviation, sqrt rule.
- **Portfolio returns** — weighted sum of component expected returns. *Prereq: weights, expected returns.
- **Covariance** — measure of co-movement between two asset return series. *Prereq: return series, variance.
- **Portfolio standard deviation** — combining individual σ with covariance (two-asset covariance including weights). *Prereq: covariance, weights.
- Built on MSFT + GOOGL price CSV read via `.read_csv`. *Prereq: pandas, price data.
### 2. Modern Portfolio Theory — **Modern Portfolio Theory/Implement Modern Portfolio Theory in Python.ipynb**
- **Portfolio return & variance** — extends baseline to a three-asset portfolio (CVX, MSFT, GOOGL). *Prereq: portfolio construction.
- **Efficient frontier** — varying weight combinations (a,b) to trace the set of optimal risk/return portfolios. *Prereq: portfolio σ/return, optimization over weights.
- **Optimal weights / minimum-variance and max-return portfolios** — identifying best weight allocation on the frontier. *Prereq: efficient frontier, constraint formulation.
- **Experimental exploration** — changing stocks and the weight parameters to see effects on frontier shape. *Prereq: MPT math.
### 3. Risk Parity — **Risk Parity_/Risk Parity.ipynb**
- **Risk-parity capital allocation (2 stocks)** — weights inversely proportional to each security's risk (annualized σ), equalizing risk contribution. *Prereq: annualized returns/volatility, risk-based allocation.
### 4. Risk Parity for Multiple Stocks — **Risk Parity_/Risk Parity for Multiple Stocks.ipynb**
- **Risk parity for multiple stocks (CVX/IBM/JPM)** — generalize the two-stock allocation to N assets by equal risk contribution per stock. *Prereq: risk parity two-stock, covariance matrix, weights.
- **Portfolio returns of the risk-parity allocation** for evaluation. *Prereq: portfolio returns.
### 5. Kelly Criterion — **Kelly Criterion_/Create a Portfolio Based on Kelly Criterion.ipynb**
- **Kelly criterion** — optimal growth (fractional) betting/position-size rule maximizing long-run portfolio growth (f = edge/odds). *Prereq: portfolio returns, wealth growth, probability theory.
- **Kelly portfolio via cvxpy** — optimize the Kelly criterion to get best weight combination for Chevron (CVX) + IBM. *Prereq: cvxpy optimization, daily returns.
### 6. Beta of an Asset — **Beta/Beta of an Asset in Python.ipynb**
- **Beta via regression (OLS)** — regress asset daily returns vs market (S&P 500 SPY) returns over ~1yr; slope = β. *Prereq: returns, OLS, market benchmark.
- **Beta via variance-covariance method** — β = Cov(asset, market)/Var(market). *Prereq: covariance, variance.
- **Uses & caveats** — systematic-risk measure; needs ≥1 year data; AMZN vs SPY. *Prereq: correlation, market risk.
### 7. Multi-Factor Model — **Multi Factor Model/The Momentum Factor in Python.ipynb**
- **Momentum factor construction** — a factor = a cumulative or trailing price/return series representing momentum across the stock set. *Prereq: daily % change, factor definition.
- **From factor to a factor-based portfolio** — accumulate the momentum factor into a multi-factor model input. *Prereq: daily returns, portfolio construction.
### 8. Multi-Factor Model — **Multi Factor Model/The Short-Term Reversal Factor in Python.ipynb**
- **Short-term reversal factor** — capture mean-reversal of recent losers/winners as a factor. *Prereq: daily returns, reversal effect.
- **Combining momentum + reversal into a multi-factor portfolio** — weighted combination of factor signals into an aggregate factor-based strategy. *Prereq: momentum factor, reversal factor, portfolio weighting.
### 9. Fama-French Three-Factor Model — **Fama-French Three- Factor Model/Expected Returns using Fama-French Model.ipynb**
- **Fama-French three-factor regression** — expected return modeled on : market excess (Rm−Rf), size (SMB = Small minus Big), value (HML = High minus Low), plus Rf. *Prereq: excess returns, multiple linear regression, factor definitions.
- **Daily/excess returns of the stock**, then **coefficients of the Fama-French factors** via regression. *Prereq: returns computation, OLS.
- **Annualized factor returns + expected stock return** — using the fitted coefficients to compute expected return (AMZN, 2016–2019 dataset). *Prereq: coefficient application, annualization.
### 10. Portfolio Performance Analysis — **Portfolio Performance Analysis/Portfolio Performance Analysis.ipynb**
- Portfolio performance measures (all computed on a multi-factor/factor strategy returns series)
 - **Annualized returns** and **annualized volatility** (σ×√252). *Prereq: returns, std.
 - **Sharpe Ratio** (excess return / volatility). *Prereq: risk-free, std.
 - **Sortino Ratio** (return / downside deviation). *Prereq: downside semi-deviation.
 - **Beta** (market co-movement). *Prereq: regression/covariance.
 - **Treynor Ratio** (excess return / β). *Prereq: β.
 - **Information Ratio** (active return / tracking error). *Prereq: benchmark, tracking error.
 - **Skewness** and **Kurtosis** (distribution shape of returns). *Prereq: moments.
 - **Maximum drawdown** (peak-to-trough peak of the aggregate curve). *Prereq: drawdown/equity curve.
### 11. QPM Capstone Project — **Capstone Project/Model Solution_ QPM Capstone Project.ipynb**
- **MPT on multiple assets (capstone)** — import data, annualized returns, random-weight portfolios, compute portfolio metrics, locate minimum-risk / maximum-return / optimal-weight portfolio. *Prereq: MPT notebook, annualized returns/variance, random weights; all portfolio-module concepts.
## Data files (`data_modules/`)
- `AMZN_SPY_Prices_2018_to_2019_Beta.csv` — Beta notebook (AMZN + SPY).
- `Stock_Prices_2016_To_2017_MPT.csv` / `..._RP_3stocks.csv` / `..._RP.csv` — MPT & Risk Parity.
- `Capstone_data.csv` — capstone MPT multiple-asset input.
- `Data_2016_to_2019_FF.csv` — Fama-French factors (Rm−Rf, SMB, HML, Rf) + AMZN.
- `Stock_Prices_2012_To_2017_Factor.csv` — multi-factor (momentum / short-term reversal) stocks.
- `Returns_2012_To_2017_Portfolio_Analysis.csv` / `Momentum_Performance_2012_To_2017.csv` — performance-analysis returns series.
- `Stock_Prices_2011_To_2017_Kelly_Portfolio.csv` — Kelly criterion.
## Non-code support
- `Folder Structure and How to Run Code Files.html`, `ReadMe.html` — setup/run instructions.
## Concept prerequisite flow
portfolio-construction math → MPT → risk-based allocation (Risk Parity → Kelly) → Beta → factor models (Momentum → Short-Term Reversal → Fama-French) → performance measures → capstone MPT model solution.
---
## Quantitative-Portfolio-Management — Section-based course structure
# Concept Inventory: Quantitative Portfolio Management
> Inventoried Sections: 3, 4, 7, 10, 11, 16, 17 (as they appear on disk). PDFs read per section; code confirmed from `QPMResources.zip`.
## COURSE
Quantitative portfolio *construction*, *optimization*, and *position sizing* over a multi-asset equity portfolio. Comprises Modern Portfolio Theory (returns/risk/covariance matrices, efficient frontier), Kelly Criterion (log-optimal bet sizing), Risk Parity (equal risk-contribution weighting), and Fama-French multi-factor expected-return models (3-factor and 5-factor), culminating in a capstone applying MPT to a multi-asset portfolio.
### Section 3 — Modern Portfolio Theory (MPT)
Sources: `Section 3 - Modern Portfolio Theory/11 - Construct Multiple Stocks Portfolio using MPT.pdf` • notebooks: `Implement Modern Portfolio Theory in Python.ipynb`
- **Generalized portfolio returns equation**: `Portfolio returns = Σ(Wi·Xi)`; for two stocks `W1*X1 + W2*X2`.
- **Matrix form**: returns row-vector `X` (1×n annualized returns) × weights column-vector `W` (n×1) → `Portfolio returns = X·W`.
- **Generalized portfolio standard deviation**: `√(Wᵀ · Covariance Matrix · W)`.
- **Two-stock std dev**: `√(W1²σ11 + W2²σ22 + 2·W1·W2·σ12)`; notation σXY = covariance, σXX = variance.
- **Covariance Matrix**: diagonal = variances (self), off-diagonal = covariances (σij=σji); MPT: favor low covariance to maximize risk-return trade-off.
- **Optimization objective**: maximize returns/risk ratio subject to `ΣWi=1` (weights sum to 1).
- **Efficient frontier**: construct many random-weight portfolios, simulate, plot return-vs-risk frontier; **optimal weights** = max (returns/standard deviation) point (max Sharpe-type ratio in the two-asset → multi-asset generalization).
- Python: compute annualized returns & std dev, covariance, change stocks/weights, plot efficient frontier, output min-risk & max-return-risk portfolios.
**Prereqs**: matrix transpose & multiplication; covariance/variance statistics; expected-return concept; some Pandas (returns, cov/corr, portfolio simulation).
### Section 4 — Kelly Criterion
Files: `Section 4 - Kelly Criterion/5 - Kelly-Criterion.pdf` • notebook: `Create a Portfolio Based on Kelly Criterion.ipynb`
- **Formula origin**: J.L. Kelly, Jr., Bell Labs 1956; **Kelly bet size = argmax expected log wealth** (max expected geometric growth rate); used successfully by Warren Buffett / Berkshire Hathaway.
- **Portfolio return (daily)**: `Σ(AssetWeight_i × Asset RateOfReturn_i)`.
- **Portfolio value**: `1 + daily portfolio return` each day.
- **Final portfolio value**: product (compounding) of daily values `∏(1 + Σ W·r)` over j=1..days.
- **Kelly derivation**: maximize logarithm of final portfolio value; because `max(A·B) = max(log A + log B)`, the log transforms the multiplicative-compounding problem into an **additive summation** you can solve directly.
- **Kelly Criterion equation**: `E[ Σ_j log(1 + Σ_i AssetWeight_i · AssetRateOfReturn_i) ]` — maximize expected sum of log daily portfolio values.
- **Application in Python**: compute daily returns across candidate weights, formulate log-sum objective, optimize weights (via python solver); build the Kelly portfolio with those optimized weights; compare performance against a benchmark.
- Core intuition: **_growth-maximizing position sizing** — over/under-sizing reduces compounding growth.
**Prerequisites**: MPT returns formula (Section 3); logarithms / laws of logs; expectation notation; portfolio annualization & compounding; absolute basis for optimization.
### Section 7 — Risk Parity (RP)
Files: `Section 7 - Risk Parity/7 - Portfolio with Multiple Stocks.pdf` • notebook: `Risk Parity.ipynb`
- **Risk Parity principle**: each security's marginal risk contribution to the portfolio is made *equal* — balanced risk across constituents rather than cap-weighting.
- **Two-stock weight formula**: `W1 = (1/σ11) / (1/σ11 + 1/σ22)`, `W2 = (1/σ22) / (1/σ11 + 1/σ22)` generalizes to `wi ∝ 1/σii` normalized.
- **Derivation**: start from portfolio std dev; force equal per-stock variance contribution: `W1²·σ11 = W2²·σ22` (cancels cross-covariance term); yields inverse relationship `Wi·σi = Wj·σj` for each pair → weights inversely prop. to (own) std dev.
- **Multi-stock RP condition**: equate each stock's contribution `Wi·Σ(W·σ)`, i.e. `Σ_n contributions equal for every stock`, subject to `ΣWi=1`.
- **Multi-stock solution**: derivations require advanced math (solving nonlinear parity equations) — out of course scope; practical approach = solve statistically via **scipy / sklearn** library optimizers.
- Notebook: compute annualized returns and std dev, then calculate weights using risk parity.
**Prereqs**: covariance matrix, std dev/variance, weights-normalization, solver literacy (scipy/sklearn), same matrix prereq as MPT/SD.
### Section 10 — Fama-French Three-Factor Model
Files: `Section 10 - Fama-French Three- Factor Model/5 - Calculation of SMB and HML Factor.pdf` • notebook: `Expected Returns using Fama-French Model.ipynb`
- **Three factors**: market, size (SMB – Small minus Big), value (HML – High minus Low).
 - `R_i = Rf + βm(Rm−Rf) + βSMB·SMB + βHML·HML`.
- **Six buckets via two sort dimensions**
 - **Size axis**: rank by market cap; below median = *small*; above median = *big*.
 - **Value axis (B/M ratio)**: rank by Book/Market; >70th pct = *value* (cheap); <30th = *growth* (expensive); 30–70 = *neutral*.
 - Resulting 6 portfolios: Small Value, Small Neutral, Small Growth, Big Value, Big Neutral, Big Growth.
- **SMB factor** = «avg small minus avg big»: `SMB = ⅓(Small V+Neutral+G) − ⅓(Big V+Neutral+G)`.
- **HML factor** = «avg high − avg low»: `HML = ½(Small Value + Big Value) − ½(Small Growth + Big Growth)`.
- **Use**: compute expected returns of a stock (Amazon example) by regressing returns vs the three factors and plugging betas & factor premia into the return formula.
**Prereqs**: CAPM fundamentals (beta, market risk premium), factor regression fit, market-cap & B/M construction, arithmetic averaging.
### Section 11 — Fama-French Five-Factor Model
Files: `Section 11 - Fama-French Five-Factor Model/1 - Fama-French-Five-Factor-Model.pdf`
- Extends 3-factor (CAPM + size + value) with 2 more factors: **Profitability** and **Investment**.
- **Profitability factor (RMW, Robust minus Weak)**: high-profitable firms (gross-profits/assets) yield higher returns than low-profitability. RMW = avg returns of the two robust portfolios minus avg of the two weak.
- **Investment factor (CMA, Conservative minus Aggressive)**: low asset-growth firms outperform high-asset-growth; CMA analogous averaging.
- **Model equation**: `Ri = Rf + β1·(Rm−Rf) + β2·(SMB) + β3·(HML) + β4·(RMW) + β5·(CMA)`.
- **Factor construction** uses 6 portfolios on (each pair of) size-and-book-to-market, size-and-profitability, size-and-investment; SMB is computed by averaging per dimensions: `(SMB)_BM, (SMB)_OP, (SMB)_Inv` then `SMB = ⅓(...)`.
**Prereqs**: 3-factor model (above), factor-style regression, gross-profit margins, asset growth-accounting, portfolio construction.
### Section 16 — Capstone Project
Files: `Section 16 - Capstone Project/2 - Problem Statement.pdf` • templates `4 - QPMCapstoneTemplate.zip` • solution `6 - QPMCapstoneSolution.zip`
- **Goal**: apply Modern Portfolio Theory end-to-end to a **multi-asset** portfolio.
- **Steps**
 1. **Price data**: gather any number of assets; sample data = 3 assets.
 2. **Random portfolios w/ different weights**: generate random weight vectors for multi-asset portfolio; compute and store portfolio metrics.
 3. **Identify max-return/risk & min-risk**: pick portfolios with min risk and max Sharpe (returns/risk).
 4. **Plot the Efficient Frontier** and print optimal weights.
- Deliverable: template notebook with helper fx (data reading, plotting); solution notebook present.
**Prereqs**: all sections 3–11 (MPT, efficient frontier, basic portfolio metrics, data reading & plotting).
### Section 17 — Summary / Course Recap
Files: `Section 17 - Summary/2 - QPMResources.zip` (all course notebooks + data packed)
- Notebook recap across topics: **Basic Portfolio Construction**, **Beta of an Asset** (regression vs variance-covariance), **MPT**, **Kelly Criterion**, **Risk Parity**, **Fama-French (expected returns)**, **Multi-Factor Model** (Momentum factor, Short-Term Reversal factor), **Portfolio Performance & annualized measures** (Sharpe, Sortino, Treynor, Beta, Information ratio, skewness, kurtosis, max drawdown, monthly-returns heatmap, cumulative vs S&P500).
- Consolidates the entire course into reusable functions and summary analyses.
**Prereqs**: everything above; performance-measure calculus, time-series plotting metrics.
## Course Prerequisite Map
- **Statistical / matrix literacy** → covariance & variance → Σ (weighted) returns & portfolio std dev → **MPT efficient frontier**.
- **MPT** → returns formula reused in **Kelly portfolio** derivation → log-optimal sizing.
- **MPT / covariance** → each stock contributes to total risk → derive risk-parity weight → **Risk Parity** (library-based solution).
- **CAPM(beta, risk-free premium)** → **Fama-French 3-factor** (apply size/value) → **Fama-French 5-factor** (add profitability/investment factors).
- **All optimization & factor results** → **Capstone application** on multi-asset portfolios.
- D-overlap with sibling track topics: beta regression, factor modeling, Sharpe/Sortino analytics all recur in continuous courses (Track 1 Quant methods, Track 4 ML). Course-specific distinctness: REER/value weighting (Track 6), position sizing via Kelly/risk-parity (Track 7) — mechanisms unique to this track.


====================
Quantitative-Trading-Strategies-and-Models
====================

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


====================
Short-Selling-in-Trading
====================

## COURSE: Short Selling in Trading
Course folder: `Short-Selling-in-Trading/Short Selling in Trading`
Notebooks: 12
---
## MODULE: Returns
- Notebook: `Stock Return Calculation/Return Calculation.ipynb`
### LESSON: Return Calculation
- **Return** — profit or loss from trading, investing, or saving. − prereqs: PnL
- **Arithmetic returns** — percentage change: (current − previous)/previous. − prereqs: prices, percentage change
- **Logarithmic returns** — natural log of (current price / previous price). − prereqs: returns, logarithms
- **Cumulative arithmetic returns** — cumulative sum of daily arithmetic returns. − prereqs: returns, cumsum
- **Cumulative log returns** — cumulative sum of daily log returns. − prereqs: log returns, cumsum
- **Time-additivity of log returns** — multi-period log return = sum of period log returns. − prereqs: log returns
- **Return histogram** — plotting the returns distribution. − prereqs: plotting, returns
## MODULE: Relative Series
- Notebook: `Relative Series/Compute the Relative Series.ipynb`
### LESSON: Compute the Relative Series
- **Relative series** — a stock restated relative to a benchmark and currency. − prereqs: returns
- **Adjustment factor** — benchmark close × exchange rate. − prereqs: multiplication
- **Relative series formula** — OHLC price divided by the adjustment factor. − prereqs: division, adjustment factor
- **Rebased series** — relative series rebased to the first stock price. − prereqs: relative series
- **Currency / benchmark effect** — separating stock moves from market and FX moves. − prereqs: exchange rate, benchmark
- **Relative-series function** — a reusable Python function (`relative`). − prereqs: functions, series
## MODULE: Stock Classification (Screener)
- Notebook: `Stock Classification/Classification of Stocks.ipynb`
### LESSON: Classification of Stocks (screener)
- **Stock screener** — a screening tool to scan a universe of stocks. − prereqs: universe, screening
- **Relative series computation** — the screener builds a relative series first. − prereqs: relative series
- **Swing detection** — 20-period local highs and lows (`argrelextrema`). − prereqs: swings, extremum
- **Regime detection** — identifying the trading phase from swings and price moves. − prereqs: swings, regime
- **Regime change date** — extracting the most recent regime shift date. − prereqs: regime detection
- **Absolute vs relative cumulative returns** — unadjusted vs benchmark-adjusted returns. − prereqs: cumulative returns, relative series
- **Loop over multiple stocks** — screening all tickers in a universe. − prereqs: loops, screening
## MODULE: Regime Detection
- Notebooks: `Regime Change Detection/Regime Change- Breakout_Breakdown Model.ipynb`, `Regime Change Detection/Regime Change- Crossover Model.ipynb`, `Regime Methods/Compare the Regimes.ipynb`
### LESSON: Moving Average Crossover (Crossover Model)
- **Moving average crossover** — short-term MA crossing above/below long-term MA defines regime. − prereqs: moving averages, trend
- **Golden / death cross** — 50/200 crossover (bullish golden, bearish death). − prereqs: SMA, crossover
- **Simple moving average (SMA)** — equal-weight windowed average of prices. − prereqs: moving averages
- **Exponential moving average (EMA)** — weighted average favouring recent price data. − prereqs: SMA, weighting
- **Regime signal** — +1 when short MA >= long MA (bullish), -1 bearish. − prereqs: crossover
- **Whipsaw problem** — MA crossover fails in sideways markets. − prereqs: crossover, sideways market
### LESSON: Breakout / Breakdown Model
- **Breakout** — price printing a new high over a 252-day (52-week) window. − prereqs: highs, rolling window
- **Breakdown** — price printing a new low over the lookback window. − prereqs: lows, breakout
- **Regime breakout signal** — go long when rebased high >= rolling high. − prereqs: breakout
- **Regime breakdown signal** — go short when rebased low <= rolling low. − prereqs: breakdown
- **Breakout-breakdown model** — combined long/short regime from new highs/lows. − prereqs: breakout, breakdown
- **Lag drawback** — unavoidable 252-day lag gives back gains to the market. − prereqs: breakout, lag
- **Low win rate** — shortening the horizon produces false positives. − prereqs: win rate, horizon
### LESSON: Compare the Regime Methods
- **Regime change comparison** — comparing crossover, breakout, and floor/ceiling regimes. − prereqs: regime, detection
- **Hindsight bias in floor/ceiling** — swings are retroactively assigned, so a lag is needed. − prereqs: floorceiling, lag
- **Cumulative return comparison** — comparing compounded returns across methods. − prereqs: cumulative returns
- **Drawdown comparison** — comparing maximum drawdowns across methods. − prereqs: drawdown
- **Golden cross advantage** — captures regime change best but with high volatility. − prereqs: crossover, drawdown
- **Method blending** — combining methods to reduce drawdown. − prereqs: regime methods
## MODULE: Floor & Ceiling
- Notebooks: `Floor and Ceiling/Swings.ipynb`, `Floor and Ceiling/Floor and Ceiling.ipynb`
### LESSON: Swing Calculation
- **Swing high / low** — local price peaks and troughs. − prereqs: prices, local extrema
- **`argrelextrema`** — scipy function to find peaks/troughs over a window. − prereqs: scipy, extrema
- **Alternation** — requiring swings to alternate high/low and keeping extreme values. − prereqs: swings
- **Eliminating non-alternating swings** — rule-based while-loop filtering of repeats. − prereqs: alternation, loops
- **Last swing adjustment** — aligning the final swing with the most recent extreme. − prereqs: swings, extremum
- **Join and crossover avoidance** — dropping existing columns before a join to avoid overlap. − prereqs: join, pandas
### LESSON: Floor & Ceiling Method
- **Floor & ceiling** — quantify distance from a peak/bottom to later swings. − prereqs: swings
- **Classic vs floor/ceiling bull–bear definition** — traditional HH/HL definitions have low statistical validity. − prereqs: bull/bear, regime
- **Volatility-standardised distance** — measuring distance in units of rolling standard deviation (3-month). − prereqs: volatility, distance
- **1.5-stdev threshold** — marks the start of a regime change. − prereqs: distance test, threshold
- **Floor/ceiling stability** — does not flip in sideways markets (unlike crossing). − prereqs: switching, regime
- **Breakout/breakdown handling** — positive or negative breakthrough changes the regime. − prereqs: breakout, floor/ceiling
- **Regime state (−1 bearish / +1 bullish)** — binary regime indicator. − prereqs: regime
## MODULE: Stop Loss and Position Sizing — Metrics
- Notebooks: `Stop Loss and Position Sizing/Position Sizing - I.ipynb`, `Stop Loss and Position Sizing/Position Sizing - II.ipynb`
### LESSON: Position Sizing - I
- **Gain expectancy** — win% × avg win% − loss% × abs(avg loss%). − prereqs: PnL, probability
- **Signal module** — the win/loss side of gain expectancy. − prereqs: gain expectancy
- **Money management module** — position sizing / avg win–loss amplitudes. − prereqs: gain expectancy
- **Equal-weight position sizing** — fixed percentage per position; relies on signals, ignores vol. − prereqs: sizing, portfolio
- **Constant equity at risk** — position sized vs a constant stop-loss distance; penalises volatile stocks. − prereqs: stop loss, volatility
- **Hit rate / miss rate** — rolling ratio of winning vs losing days. − prereqs: returns, statistics
- **Arithmetic & geometric gain expectancy** — win/loss-density measures. − prereqs: expectancy, returns
- **Gain-to-pain ratio (profit factor)** — sum(profits)/sum(losses). − prereqs: returns, profit/loss
- **Tail ratio** — quantile-based left/right tail measure on cumulative returns. − prereqs: quantile, returns
- **Common sense ratio** — profit factor × tail ratio. − prereqs: profit factor, tail ratio
- **Kelly criterion (K%)** — W − (1−W)/R based trade-size. − prereqs: win rate, win/loss ratio
- **Robustness metrics (grit, ulcer, T-stat, Calmar)** — drawdown/loss-driven robustness. − prereqs: drawdown, loss
- **Cumulative returns (log-exp form)** — expanding sum then exponential. − prereqs: returns, exponential
### LESSON: Position Sizing - II
- **Stock universe loop** — iterate four bank stocks and a MA parameter grid. − prereqs: loops
- **Relative series, swings & regime per stock** — chaining reusable function steps. − prereqs: relative, swings, regime
- **MA-cross signal within regime** — `signal_fcstmt` for entry when regime & cross align. − prereqs: regime, crossover
- **Stop-loss function** — `stop_loss(...)` for risk-adjusted position. − prereqs: stop loss
- **Transaction costs** — `transaction_costs` deducted from daily returns. − prereqs: returns, transaction costs
- **Scoreboard optimisation** — sorting parameter combinations by robustness score. − prereqs: robustness, optimisation
- **Round-lot sizing** — `round_lot` rounding shares to lots. − prereqs: sizing, shares
- **Equity-at-risk vs equal weight** — comparing the two sizing curves. − prereqs: position sizing
- **Equity-curve simulation** — simulating daily account value. − prereqs: equity curve
## MODULE: Trading Strategy
- Notebooks: `Strategy Creation/Strategy Creation.ipynb`, `Strategy Creation/Strategy Optimization.ipynb`
### LESSON: Strategy Creation
- **Gain expectancy formula reuse** — the linkage between signal and money module. − prereqs: expectancy
- **Strategy definition** — blending the three regime methods into a long/short strategy. − prereqs: regime, strategy
- **Stable, low-lag, sideways-resilient regime** — selects floor/ceiling as the base. − prereqs: regime selection
- **Signal generation (MA cross)** — short- and mid-term MAs produce entries/exits. − prereqs: MA, signals
- **Stop loss for short trades** — essential because MA lag causes false positives. − prereqs: stop loss, short
- **Long entry/exit** — long when regime==1 and st>=mt; exit when st<mt. − prereqs: regime, crossover
- **Short entry/exit** — short when regime==-1 and st<=mt; exit when st>mt. − prereqs: short, crossover
- **Stop-loss breach handling** — exit a trade when stop loss is breached. − prereqs: stop loss, signal
- **Transaction-cost function** — detect entry/exit and deduct costs. − prereqs: transaction costs, returns
### LESSON: Strategy Optimization
- **Strategy optimisation** — search over short/mid-term MA combinations. − prereqs: moving averages, optimisation
- **Relative and absolute returns** — rebased-close and raw-close log returns. − prereqs: returns, log returns
- **ST/MT permutation grid** — `itertools.product` over short/mid-term windows. − prereqs: itertools, permutations
- **Hurdle criterion** — strategy must beat max(passive, regime) returns. − prereqs: hurdle, returns
- **Performance ranking** — sorting combinations by cumulative performance. − prereqs: performance, ranking
- **Top-combination chart** — plot top 10 st/mt strategy curves. − prereqs: plotting, ranking
---
## Cross-cutting / Thematic Concepts
Recurring across many notebooks (trivial, convenience).
- **pandas / numpy time-series basics** — read_csv, diff, rolling, expanding, cumsum. − prereqs: none
- **SciPy signal processing** — `argrelextrema` for local-extremum detection. − prereqs: none
- **Custom `short_selling` module** — reusable functions (`relative`, `swings`, `regime_fc`, `returns`, `cumulative_returns`). − prereqs: packaging
---
## Short-Selling-in-Trading — Section-based course structure
# Concept Inventory — Short Selling in Trading
## COURSE: Short Selling in Trading
### Section: Section 1 - Introduction
- **About the author / course:** credibility and scope. prereqs: none.
- **Introduction to short selling:** definition and motivation for shorting an asset. prereqs: none.
### Section: Section 2 - Short Selling
- **Short selling:** selling an asset you do not own (borrowed) and buying it back later, profiting from a price decline. prereqs: stock market basics.
- **Long-short strategy:** combining long positions in undervalued stocks with short positions in overvalued ones to capture relative performance. prereqs: short selling, long positions.
### Section: Section 3 - Relative Series
- **Factors affecting a stock (PDF):** company fundamentals, sector, market, currency, benchmark that drive a stock's own path. prereqs: equity analysis.
- **Relative series:** the price series of a stock normalized relative to a benchmark, showing outperformance vs underperformance independent of the market. prereqs: price series, benchmark.
- **Calculating relative series:** dividing the stock price by a benchmark index price across each date. prereqs: relative series, pandas.
### Section: Section 4 - Stock Return Calculation
- **Returns (Additional Reading):** simple vs log returns and why log returns are used in quantitative analysis (time-additive, symmetric). prereqs: price series, math.
- **Stock return calculation:** computing daily percentage change of the relative series. prereqs: returns.
### Section: Section 5 - Regime Definition
- **Regime definition:** classifying the market into distinct states (bull/bear/trending/range) over time. prereqs: time series, trend.
### Section: Section 6 - Regime Change Detection
- **Breakout / breakdown model:** detecting a regime change when price breaks above (breakout) or below (breakdown) a level. prereqs: regimes, support/resistance.
- **Crossover model:** detecting regime change via moving-average crossovers (short vs long MA). prereqs: moving averages, regime.
### Section: Section 7 - Floor and Ceiling
- **Floor and ceiling:** price bands (floor = lower support, ceiling = upper resistance) defining a trading range. prereqs: support/resistance.
- **Swings:** local highs and lows used to identify structural turning points. prereqs: price action.
- **Lagless swing detection (zip):** an indicator that marks swings with minimal lag. prereqs: swings.
### Section: Section 8 - Regime Methods
- **Compare regime methods:** evaluating breakout/breakdown vs crossover for regime classification quality. prereqs: regimes, crossover model, breakout model.
### Section: Section 9 - Stock Classification
- **Classify stocks to bulls or bears:** assigning each stock a bull or bear label based on its regime. prereqs: regimes.
- **Flow diagram for classification (PDF, image):** visual pipeline: relative series → returns → regime detection → classification. prereqs: stock classification.
### Section: Section 10 - Strategy Creation
- **Overview of strategy creation:** building a short/hold strategy from the regime classification. prereqs: stock classification.
- **Strategy logic:** go short when classified bearish, long/hold when bullish. prereqs: classification, short selling.
- **Strategy flow diagram (PDF, image):** entry/exit signal generation from regime. prereqs: strategy logic.
### Section: Section 13 - Stop Loss and Position Sizing
- **Performance metrics:** evaluating strategy with returns, Sharpe, drawdown. prereqs: backtesting metrics.
- **Optimisation:** tuning strategy parameters (thresholds/indicators) for better out-of-sample performance. prereqs: performance metrics.
- **Stop loss and position sizing:** setting risk per trade and sizing positions. prereqs: risk management, position sizing.
### Section: Section 14 - World Stock Screener Notebook
- **World stock screener notebook (zip):** applying the short-selling screening logic across many global stocks. prereqs: stock classification, screener.
### Section: Section 16 - Course Summary
- **Course summary:** recap of relative series → regime → classification → strategy. prereqs: all previous.
- **Short selling in current market:** relevance and application today. prereqs: short selling.
## Course Prerequisite Map
Before this course a learner needed: basics of equities and short selling; price/return series and percentage (log) returns; support/resistance and trend concepts; moving averages for crossover regimes; pandas for relative-series and return computation; and an understanding of backtesting performance metrics (returns, Sharpe, drawdown).


====================
Statistical-Arbitrage
====================

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


====================
Swing-Trading-Strategies
====================

# Swing Trading Strategies — Concept Inventory
## COURSE: Swing Trading Strategies
A () course on building and backtesting swing trading strategies in Python. Covers Python fundamentals, financial data handling, MACD and Williams Fractal indicators, stock screening, trade-book construction, and performance analysis.
---
## MODULE: Introduction to Python
### LESSON: My First Jupyter Notebook
- **Programming** — telling a machine what to do by writing code. prereqs: none.
- **Jupyter notebook** — an interactive document of code cells and markdown cells run with Shift+Enter. prereqs: none.
- **Code comments** — non-executable notes using `#` (single line) or triple quotes `"""..."""` (multi-line). prereqs: none.
- **Print statement** — `print("...")` outputs text/values to the console. prereqs: none.
- **Variables** — named storage for values, assigned with `=` (read as "is set to"). prereqs: none.
- **Integer** — a whole number data type (positive or negative). prereqs: variables.
- **Float** — a real/decimal number data type, e.g. `5.0` or `float(5)`. prereqs: variables.
- **String** — text data enclosed in single or double quotes. prereqs: variables.
- **Case sensitivity** — Python treats `gold_price` and `Gold_Price` as different variables. prereqs: variables.
- **Indentation** — Python requires consistent leading spaces within a code block; wrong indentation raises an error. prereqs: variables.
- **Simple returns** — percentage change in price: `(Final/Initial - 1) * 100`. prereqs: variables, arithmetic.
- **Log returns** — natural log of the price ratio: `math.log(price_2 / price_1)`. prereqs: simple returns, math module.
- **`type()` function** — returns the data type of a variable. prereqs: variables.
- **`math` module** — Python standard library for math functions; imported with `import math`. prereqs: none.
### LESSON: Operations and Functions in Python
- **Exponentiation operator** — `**` raises a number to a power, e.g. `3**2`. prereqs: arithmetic.
- **Modulo operator** — `%` returns the remainder of a division, e.g. `15 % 4`. prereqs: arithmetic.
- **Built-in math functions** — `abs()`, `round()`, `max()`, `min()`, `sum()`. prereqs: none.
- **`import` keyword** — loads a library so its functions become available. prereqs: none.
- **Comparison operators** — `==`, `!=`, `<`, `>`, `<=`, `>=`; return booleans. prereqs: none.
- **Boolean values** — `True` / `False` results of logical operations. prereqs: comparison operators.
- **Logical operators** — `not`, `or`, `and` combine boolean statements per a truth table. prereqs: booleans.
- **Functions** — reusable blocks of code defined with `def name(params):`. prereqs: none.
- **Function parameters** — inputs passed into a function, separated by commas. prereqs: functions.
- **Variable scope** — a variable defined inside a function is not accessible outside it. prereqs: functions.
- **`return` statement** — sends a value out of a function so it can be stored/used outside. prereqs: functions, scope.
### LESSON: DataFrame and Basic Functionality
- **DataFrame** — pandas' tabular data structure of rows and columns (spreadsheet-like). prereqs: none.
- **`pd.DataFrame()` constructor** — creates a dataframe from a dict of lists. prereqs: pandas import.
- **Index** — the row labels of a dataframe; can be set with `set_index()`. prereqs: DataFrame.
- **`set_index()`** — sets a column as the row index. prereqs: DataFrame.
- **`pd.read_csv()`** — reads a CSV file into a dataframe; `index_col` sets the index column. prereqs: pandas.
- **`head()` / `tail()`** — display the first/last n rows (default 5). prereqs: DataFrame.
- **`loc`** — label-based row/column access; end index is inclusive. prereqs: DataFrame.
- **`iloc`** — position-based row/column access; end index is exclusive. prereqs: DataFrame.
- **Boolean indexing** — filtering rows with a boolean condition, e.g. `df[df.col > 5000]`. prereqs: DataFrame, booleans.
- **Accessing columns** — select a column by name with `df[["col"]]`. prereqs: DataFrame.
- **`drop()`** — removes rows or columns; `axis=1` drops columns. prereqs: DataFrame.
- **Adding columns** — assign a new column, e.g. `df['SMA'] = df['Close'].rolling(10).mean()`. prereqs: DataFrame.
- **`rolling().mean()`** — computes a rolling (moving) average over a window. prereqs: DataFrame.
---
## MODULE: Financial Market Data and Visualisation
### LESSON: Importing Time Series Data
- **Time series data** — data indexed by time (e.g. daily OHLCV prices). prereqs: none.
- **`yfinance` package** — downloads financial data from Yahoo Finance; installed via `!pip install yfinance`. prereqs: none.
- **`yf.download()`** — fetches OHLCV data for a ticker between start/end dates. prereqs: yfinance.
- **Adjusted price** — price adjusted for corporate actions; `auto_adjust=True` in `yf.download`. prereqs: yfinance.
- **CSV file** — comma-separated values plain-text tabular file. prereqs: none.
- **`pd.to_datetime()`** — converts an index/column to datetime format for time-series operations. prereqs: pandas.
### LESSON: Data Visualisation
- **Data visualisation** — graphical representation of data to draw insights. prereqs: none.
- **`matplotlib` library** — Python plotting library; `import matplotlib.pyplot as plt`. prereqs: none.
- **`%matplotlib inline`** — magic command to render plots inside the notebook. prereqs: matplotlib.
- **`plt.style.use()`** — sets the plot style; `plt.style.available` lists options. prereqs: matplotlib.
- **Line graph** — `df['col'].plot()` plots a column over its index. prereqs: matplotlib, DataFrame.
- **`plt.title()` / `plt.xlabel()` / `plt.ylabel()`** — set plot title and axis labels. prereqs: matplotlib.
- **Scatter plot** — `plt.scatter(col1, col2)` shows the relationship between two variables. prereqs: matplotlib.
- **Histogram** — `df['col'].plot(kind='hist')` shows the frequency distribution of a column. prereqs: matplotlib.
- **`plt.show()`** — displays the current figure. prereqs: matplotlib.
---
## MODULE: MACD
### LESSON: MACD Entry Rules
- **MACD (Moving Average Convergence Divergence)** — momentum indicator from the difference of two EMAs. prereqs: EMA.
- **MACD line** — fast-period EMA minus slow-period EMA (default 12 and 26). prereqs: EMA.
- **Signal line** — EMA of the MACD line (default 9-period). prereqs: MACD line.
- **MACD histogram** — MACD line minus signal line. prereqs: MACD line, signal line.
- **TA-Lib (`talib`)** — technical analysis library; `ta.MACD(close)` returns line, signal, histogram. prereqs: none.
- **`pd.read_pickle()`** — reads a compressed pickle file (`.bz2`) into a dataframe. prereqs: pandas.
- **`dropna()`** — removes rows with missing (NaN) values. prereqs: DataFrame.
- **`np.where(condition, if_true, if_false)`** — vectorized conditional to build a signal column. prereqs: numpy.
- **Long entry signal** — buy when MACD line crosses above the signal line (`MACD line > Signal line`). prereqs: MACD components.
### LESSON: Minute Price Data Resampling Techniques
- **Minute data** — intraday data at 1-minute frequency. prereqs: none.
- **`yf.download(period=, interval=)`** — downloads data at a chosen frequency (e.g. `1m`). prereqs: yfinance.
- **Resampling** — converting high-frequency data to a lower frequency (not the reverse). prereqs: time series.
- **`DataFrame.resample(interval).agg(dict)`** — aggregates data to a new frequency. prereqs: pandas.
- **OHLCV aggregation dict** — maps Open→first, High→max, Low→min, Close→last, Volume→sum. prereqs: resampling.
- **Resample intervals** — `15T` (15 min), `1H` (1 hour), `4H` (4 hours). prereqs: resampling.
### LESSON: Working With Pickle File
- **Pickle file** — Python serialization format that retains column/index data types. prereqs: none.
- **`bz2` compression** — compressed pickle format for smaller file size. prereqs: pickle.
- **`to_pickle()`** — saves a dataframe to a pickle file. prereqs: pandas.
- **`read_pickle()`** — reads a pickle file back into a dataframe. prereqs: pandas.
- **DatetimeIndex** — index of datetime objects, preserved through pickle. prereqs: pickle, datetime.
- **Pickle version compatibility** — pickle files are Python-version-specific and backward compatible. prereqs: pickle.
- **Common pickle errors** — `AttributeError` (pandas version mismatch) and `ValueError: unsupported pickle protocol`. prereqs: pickle.
---
## MODULE: Stock Screener
### LESSON: Fetch Data for Multiple Stocks
- **Data vendor** — a service (e.g. Yahoo Finance) providing OHLCV data. prereqs: none.
- **Ticker** — the symbol identifying a stock. prereqs: none.
- **Loop over tickers** — `for t in tickers: stock_data[t] = yf.download(t, ...)` fetches data for many stocks. prereqs: yfinance, loops.
- **Dictionary of dataframes** — storing each stock's dataframe keyed by ticker. prereqs: dict, DataFrame.
- **`pickle.dump()` / `pickle.load()`** — write/read a Python object to/from a pickle file. prereqs: pickle.
- **Adjusted prices** — prices adjusted for stock splits, dividends, and rights offerings. prereqs: none.
### LESSON: Stock Screener
- **Stock screener** — filters a stock universe by criteria to find tradable assets. prereqs: none.
- **Penny stock filter** — exclude stocks with average price below a threshold (e.g. $5). prereqs: screener.
- **Liquidity filter** — require average dollar-volume above a threshold (e.g. $100M). prereqs: screener.
- **Dollar-volume** — price × volume, a liquidity measure. prereqs: liquidity.
- **Market capitalisation filter** — require market cap above a threshold (e.g. $200B). prereqs: screener.
- **Market capitalisation** — outstanding shares × average price. prereqs: none.
- **ADX filter** — require ADX > 25 to confirm a strong trend. prereqs: ADX indicator.
- **Hurst exponent** — measures trend persistence; `compute_Hc()` from the `hurst` package. prereqs: none.
- **Hurst filter** — require Hurst exponent > 0.5 to validate the trend. prereqs: Hurst exponent.
- **Distance from 52-week high** — `(52-week high - Close) / 52-week high`; small distance indicates an uptrend. prereqs: screener.
- **Uptrend filter** — select stocks within 10% of their 52-week high. prereqs: distance from high.
- **Forward bias avoidance** — in backtesting, split data so filters use past data only. prereqs: backtesting.
---
## MODULE: Williams Fractals
### LESSON: Williams Fractal
- **Williams Fractal** — a 5-candle reversal pattern indicator. prereqs: candlesticks.
- **Bullish fractal** — the middle of the latest 5 candles has the lowest low. prereqs: Williams Fractal.
- **Bearish fractal** — the middle of the latest 5 candles has the highest high. prereqs: Williams Fractal.
- **`rolling(5).apply(func)`** — applies a function over a rolling 5-bar window. prereqs: pandas.
- **`shift(1)`** — lags a signal by one bar to avoid forward bias (fractal confirmed only after candles form). prereqs: pandas.
- **Fractal signal** — combined bullish (+1) and bearish (−1) fractal signals, shifted. prereqs: bullish/bearish fractal.
- **Trade book** — a table of entry/exit times and prices from a strategy. prereqs: none.
- **`get_trade_book()`** — helper that builds a trade book from a signal column, take-profit, and stop-loss. prereqs: trade book.
- **Take-profit / stop-loss** — exit levels set as percentages of entry price (e.g. 4% / 2%). prereqs: trade book.
- **`analyse_performance()`** — helper that computes strategy performance metrics. prereqs: performance measures.
---
## MODULE: Swing Strategy Backtesting
### LESSON: MACD Swing Strategy
- **Entry signal** — buy when MACD line > signal line. prereqs: MACD.
- **Exit via technical indicator** — close a long when the MACD line crosses below the signal line. prereqs: MACD.
- **Stop-loss / profit-target exit** — close when stop-loss or profit target is hit. prereqs: risk management.
- **Risk-reward ratio** — e.g. 1:2 means 2% stop-loss and 4% profit target. prereqs: none.
- **Time exit** — close a position automatically after a holding period (e.g. one month). prereqs: none.
- **PnL calculation** — exit price minus entry price, minus trading costs. prereqs: none.
- **Transaction cost** — broker fee per trade (e.g. 0.0002). prereqs: PnL.
- **Slippage** — difference between expected and actual fill price (e.g. 0.0005). prereqs: PnL.
- **`timedelta`** — `datetime` object for date/time arithmetic (e.g. holding-period checks). prereqs: datetime.
---
## MODULE: Different Performance Measures
### LESSON: Performance Measures
- **Backtesting details** — number of trades, start/end dates, duration, holding time. prereqs: trade book.
- **Holding time** — duration of a trade (exit time − entry time); average/median/min/max. prereqs: trade book.
- **Annualised returns** — average annual return of a strategy, annualised from cumulative returns. prereqs: returns.
- **Profit factor** — sum of profits divided by sum of losses. prereqs: returns.
- **Win rate** — proportion of winning trades. prereqs: returns.
- **Heatmap of month vs year returns** — visualises returns by month and year. prereqs: returns.
- **Equity curve** — cumulative strategy returns over time. prereqs: returns.
- **Annualised volatility** — `sqrt(Var(returns)) * sqrt(252*6.5)` for hourly data. prereqs: returns.
- **Maximum drawdown** — `(Trough - Peak) / Peak`; the largest peak-to-trough loss. prereqs: equity curve.
- **Rolling volatility** — volatility over a rolling window (e.g. 60 days). prereqs: volatility.
- **Sharpe ratio** — `(R_p - R_f) / sigma_p`; excess return per unit of risk. prereqs: returns, volatility.
- **Sortino ratio** — risk-adjusted return using only downside volatility. prereqs: Sharpe ratio.
- **Calmar ratio** — annualised return divided by maximum drawdown. prereqs: returns, max drawdown.
- **Risk-adjusted return metrics** — returns adjusted for the risk taken, for comparing portfolios. prereqs: returns, risk metrics.
- **`analyse_performance()`** — combines backtesting details, return, risk, and risk-adjusted metrics. prereqs: all metrics.
---
## MODULE: Composite Swing Trading Strategy
### LESSON: Composite Swing Trading Strategy
- **Composite strategy** — combining two indicators (MACD + Williams Fractal) for entry signals. prereqs: MACD, Williams Fractal.
- **Composite entry signal** — buy when both MACD and Williams Fractal signal an entry. prereqs: MACD, fractal.
- **Signal quality** — combining indicators can improve signal quality and performance. prereqs: composite strategy.
- **Performance comparison** — composite strategy vs individual strategies (Sharpe, volatility). prereqs: performance measures.
---
## MODULE: Capstone Project
### LESSON: Capstone Project Model Solution
- **Capstone project** — build a swing trading strategy with a stock screener on multiple assets. prereqs: all modules.
- **Read price data** — load a pickle dict of minute data for multiple tickers. prereqs: pickle, dict.
- **Resample to hourly** — convert minute data to hourly candles with an OHLCV aggregation dict. prereqs: resampling.
- **Data sanity check** — check for missing data/outliers (e.g. 7 hourly points per day). prereqs: resampling.
- **Data split for backtesting** — use the first part for screening filters, the second for trading (avoid forward bias). prereqs: screener.
- **Williams Alligator** — 3 EMA lines (Jaw 13-shift8, Teeth 8-shift5, Lips 5-shift3) for momentum swings. prereqs: EMA.
- **Alligator bullish signal** — Lips above Teeth above Jaw. prereqs: Williams Alligator.
- **Combined buy signal** — buy when Williams Fractal is bullish AND Williams Alligator is bullish. prereqs: fractal, alligator.
- **Trade book per asset** — build a trade book for each filtered asset with take-profit/stop-loss. prereqs: trade book.
- **Portfolio returns** — combine per-asset strategy returns with equal weights. prereqs: returns.
- **`pyfolio` package** — generates performance tear sheets for a portfolio. prereqs: performance measures.
- **`create_simple_tear_sheet()`** — pyfolio function producing a full performance report. prereqs: pyfolio.
### LESSON: Capstone Project Solution Template
- **Solution template** — a scaffold notebook with placeholders to build the capstone solution. prereqs: capstone.
- **`sys.path.append()`** — adds a directory to the Python import path for custom modules. prereqs: python.
- **`compute_Hc()`** — computes the Hurst exponent for trend validation. prereqs: hurst package.
---
## Swing-Trading-Strategies — Section-based course structure
# Concept Inventory — Swing Trading Strategies
## COURSE: Swing Trading Strategies
### Section: Section 1 - Introduction
- **Course introduction & structure:** scope — Python/data, technical analysis, MACD strategy, backtesting, capstone. prereqs: none.
- **Course structure flow diagram (PNG):** overview of the learning path. prereqs: none.
### Section: Section 2 - Swing Trading Overview
- **What is swing trading:** holding positions for days-to-weeks to capture medium-term price swings. prereqs: trading basics.
- **Properties of swing trading:** timeframe, frequency, goals, distinctions from day trading / investing. prereqs: swing trading.
### Section: Section 3 - Swing Trading Style
- **Swing trading style:** risk/reward profile and the technical approach used throughout. prereqs: swing trading.
### Section: Section 5 - Financial Market Data and Visualisation
- **Importing data:** loading price data via yfinance/CSV (DataFrame). prereqs: pandas, finance.
- **Additional reading for financial market data:** data sources, data quality and cleaning. prereqs: data import.
- **FAQs on data:** common questions on OHLCV and frequency. prereqs: price data.
### Section: Section 6 - Strategic Plan
- **Strategic plan:** the step-by-step method for building and validating a swing strategy. prereqs: swing trading.
### Section: Section 7 - Technical Analysis in Trading
- **Technical analysis in trading:** using historical price/volume patterns for decisions. prereqs: none.
- **Types of technical indicators:** trend, momentum, volatility, volume indicator categories. prereqs: technical analysis.
### Section: Section 8 - Moving Average Primer
- **Moving average & EMA (PDF):** SMA vs EMA definitions and weighting. prereqs: price series.
- **Moving average crossovers:** golden/death cross signals and their interpretation. prereqs: moving averages.
### Section: Section 9 - MACD
- **MACD entry points:** using MACD for long/short entries. prereqs: MACD indicator.
- **MACD line & signal line:** MACD line (12-26 EMA diff) vs signal line (9 EMA), crossovers. prereqs: EMA.
- **MACD histogram:** difference between MACD and signal line, momentum representation. prereqs: MACD.
### Section: Section 10 - Exit Strategy
- **Need of exit rules:** why exits matter for locking profit and cutting losses. prereqs: risk management.
- **Exit rules:** predefined rules for closing positions (targets, stops, signal reversal). prereqs: entry signals.
- **Additional reading for exit rules:** exit strategy research. prereqs: exit rules.
### Section: Section 11 - Introduction to Backtesting
- **What is backtesting:** simulating strategy on historical data. prereqs: none.
- **How to do backtesting:** signal generation, position sizing, equity curve. prereqs: backtesting.
- **Additional reading for backtesting:** backtest methodology and pitfalls. prereqs: backtesting.
### Section: Section 13 - Different Performance Measures
- **Different performance measures:** CAGR, Sharpe, Sortino, Calmar, max drawdown, win rate. prereqs: returns.
- **Measuring risk:** drawdown, volatility as risk measures. prereqs: performance measures.
- **Additional reading for performance measures:** metric definitions and interpretation. prereqs: performance measures.
### Section: Section 16 - Optimum Number of Indicators
- **Optimum number of indicators:** how many indicators to combine for robust signals vs overfitting. prereqs: technical indicators.
### Section: Section 17 - Williams Fractals
- **Williams fractals:** Bill Williams' 5-bar fractal pattern marking swing highs/lows. prereqs: price action.
### Section: Section 19 - Stock Screener
- **Stock screener:** filtering stocks by criteria (liquidity, volatility, trend). prereqs: technical analysis.
- **Identify trending stocks:** ranking stocks by trend strength. prereqs: screener, trend.
- **Identifying direction of trend:** technical trend direction confirmation. prereqs: trend.
### Section: Section 20 - Risk Management
- **Risk management:** risk-reward, stop-loss, position risk. prereqs: none.
- **Position sizing:** fraction-of-capital sized by risk and stop distance. prereqs: risk management.
- **Additional reading for risk management:** risk control strategies. prereqs: risk management.
### Section: Section 21 - Automate Trading Strategy Using IBridgePy
- **IBridgePy automation (zip MACDSwingStrategy):** automating strategy execution via Interactive Brokers bridge. prereqs: IB API, strategy.
### Section: Section 23 - Capstone Project
- **Problem statement (PDF):** build a full swing-trading strategy. prereqs: all previous.
- **Solution template & model solution (zips):** provided code and data for capstone evaluation. prereqs: capstone.
### Section: Section 24 - Course Summary
- **Ten simple rules for swing trading (PDF):** good-practice checklist. prereqs: swing trading.
- **Ten deadly sins of swing trading (PDF):** common mistakes to avoid. prereqs: swing trading.
- **Course summary:** recap and downloadable ZIP. prereqs: all.
## Course Prerequisite Map
Before this course a learner needed: Python + pandas for data import/manipulation; financial data (OHLCV) and plotting with matplotlib; basic technical analysis (moving averages, trend); understanding of returns and compounding; and foundational backtesting + performance-metric concepts (Sharpe, Sortino, drawdown).


====================
Systematic-Options-Trading
====================

# Systematic Options Trading — Concept Inventory
> Companion live-trading template: `Live Trading Template/IBridgePy_SYSTEMATIC_OPTIONS_TRADING/butterfly_options_strategy.py`
Course flow: options data sourcing → data pre-processing → volatility & technical indicators → probability of profit → multi-leg strategy construction (butterfly, spreads, iron condor) → backtesting → risk management → analytics → screener → capstone.
---
Utility library powering all notebooks. Functions and the concepts they encode
- **`get_premium(options_strategy, options_data)`** — fetches the last traded premium for a given option type (CE/PE) and strike from the options dataset. *Prereq:* options table structure (strike, option type, Last price).
- **`setup_butterfly(futures_price, options_data, direction)`** — Builds a 4-leg butterfly: long 2 × ATM options (CE & PE), short 2 OTM options one deviation out; deviation chosen so legs are offset by premium ratio. Flip position for short butterfly. *Prereq: ATM strike, CE vs PE, premium, multi-leg structure.*
- **`setup_call_spread` / `setup_put_spread`** — Build bull call / bear put vertical spreads (ATM + one OTM leg, deviation = premium spread), with direction flip for bear call / bull put. *Prereq: spread concept, ATM strike, premium ratio.
- **`setup_iron_condor`** — 4-leg long/short iron condor: short leg at IVT±50, far OTM legs positioned from collected premium. *Prereq: condor structure, wings, net premium.
- **Payoff helpers** — `long_call_payoff`, `long_put_payoff`, `short_call_payoff`, `short_put_payoff`, `get_payoff` implement option payoff at expiry (long unprotected upside; short profit capped at premium, breakeven = strike ± premium). *Prereq: option payoff math, long vs short positions.
- **`get_pop_lognormal`** — Probability-of-profit from a lognormal distribution fitted to futures returns over the trading days to expiry; lognormal params (μ, σ) derived from ATM price and annualized historical vol. *Prereq: lognormal distribution, historical volatility, days-to-expiry.
- **`get_pop_empirical`** — Empirical POP via a 30-bin histogram over forecasted prices (previous N-trading-day % change applied to current price) and the CDF of that histogram. *Prereq: percent change, histograms, empirical CDF.
- **`get_expected_profit_empirical`** — Expected profit = Σ(probability × payoff) across the price range, combining the payoff function and empirical POP. *Prereq: probability-of-profit, payoff.
- **`calculate_IV` / `get_IV_percentile`** — Implied volatility per option via `mibian.BS` using futures price, strike, risk-free rate, days-to-expiry; then a rolling percentile rank of IV (IVP) over a window. *Prereq: Black-Scholes, implied volatility, percentile rank, days-to-expiry.
---
## Notebooks
### 1. Options Data — `Options Data/Storing US Options Data.ipynb`
- **Storing raw US options data** — Crawls monthly `.7z` archives of EOD options data; each zip holds comma-separated `.txt` files per strike/date set. Concepts: byte-size data storage, extracting archives, converting `.txt` → `.csv`, merging/looping months into one time-ordered frame. *Prereq: filesystem/pandas I/O, options dataset fields (underlying, strike, expiry, option type, Last).
- **Sourcing options data for strategy building** — Why raw options data must be normalized (strike grid, daily bars, expiry alignment) before a screener or backtest can use it. *Prereq: options quoting conventions.
### 2. Data Pre-Processing — **Data Pre-Processing/Data Quality Checks and Data Cleaning.ipynb**
- **Data quality checks on options data** — Detect missing, duplicate, and contradictory rows (e.g. mismatched strike/option-type, zero/negative Last, out-of-order dates) before any analysis. *Prereq: pandas dataframes, options dataset schema.
- **Data cleaning methods** — filling missing numeric fields with forward/backward fill into place, dropping or flagging duplicates, coerced dtype fixes and index hygiene. *Prereq: pandas missing-data idioms.
- Why cleaned daily options bars are a precondition for IVT/ADX/spreads downstream. *Prereq: course data pipeline.
### 3. Data Pre-Processing — **Data Pre-Processing/Working With Pickle File.ipynb**
- **Pickle (`.bz2`) vs CSV** — Pickle preserves dtypes and a datetime index on re-load, unlike CSV round-tripping. Concepts: compression, serialization, and index retention. *Prereq: pandas I/O, dataframes.
- **Reading compressed pickle options data** — `pd.read_pickle` on `.bz2`; perils: Python-version/Package-version specificity, memory footprint, pickling for archival. *Prereq: data cleanliness topics above.
### 4. Technical Indicator — **Technical Indicator/Average Directional Index.ipynb**
- **Average Directional Index (ADX)** — A 0–100 technical index of trend strength; ADX > 25–30 indicates a strong trend, < 25 an absence of trend. *Prereq: technical indicators, trend-following basics.
- **Computing ADX** on the underlying futures series for use as the entry filter of the short-butterfly strategy. *Prereq: rolling window/avg, time-series returns.
### 5. Implied Volatility — **Implied Volatility/Implied Volatility.ipynb**
- **Implied volatility (IV)** — the volatility the market expects in the underlying, backed out from traded option premiums; an absolute measure. *Prereq: option premiums, Black-Scholes, futures price.
- **Computing IV per option** with `mibian.BS` (inputs: underlying price, strike, risk-free, days-to-expiry, market premium). *Prereq: days-to-expiry, CE/PE option-type mapping.
- **Interpreting IV** (high IV = expected strong underlying move), relevant to a short-butterfly that profits from strong movement. *Prereq: strategy motivation.
### 6. Implied Volatility Percentile — **Implied Volatility Percentile/Implied Volatility Percentile.ipynb**
- **IV percentile (IVP)** — relative IV ranking: a rolling percentile of IV instance vs its own trailing window, overcoming the "is IV high or low?" ambiguity of the absolute measure. *Prereq: IV computation, percentileofscore.
- **IVP as a normalized signal** for entry (e.g. only short a butterfly when today's IV sits in a chosen historical percentile). *Prereq: percentile logic, short-butterfly setup.
### 7. Lognormal Distribution — **Lognormal Distribution/The Lognormal Distribution.ipynb**
- **Lognormal distribution of futures prices** — why futures/spot price series, which cannot go negative, fit a lognormal rather than normal distribution; forward step to probability-of-profit. *Prereq: normal distribution, volatility estimate.
- **Estimating lognormal parameters** from the daily historical volatility normalized to the trading days-to-expiry horizon. *Prereq: standard deviation of log-returns, days-to-expiry.
### 8. Probability of Profit Using Lognormal Distribution — **Probability of Profit Using Lognormal Distribution/Probability of Profit Using the Lognormal Distribution.ipynb**
- **POP (lognormal)** — probability that the underlying expire price lands in the payoff-favorable zone, computed from the lognormal CDF across a strike grid and the strategy payoff band. *Prereq: lognormal distribution, butterfly payoff, ATM grid.
### 9. Probability of Profit Using Empirical Distribution — **Probability of Profit Using the Empirical Distribution.ipynb**
- **POP (empirical)** — an alternative, non-parametric probability using a 30-bin histogram of forecast prices (current price × (1 + realized n-day % change)) and its empirical CDF. *Prereq: histograms, % change windows, payoff band.
### 10. Expected Profit — **Expected Profit/Expected Profit Notebook.ipynb**
- **Expected profit vs raw probability** — probability alone can mislead (rare but profitable trades vs frequent small ones); expected profit = Σ(probability × payoff) over the price grid is the better decision statistic. *Prereq: probability of profit, payoff vector, integral-over-grid.
### 11. Butterfly Strategy Payoff — **Butterfly Strategy Payoff/Payoff Diagram of the Butterfly Strategy.ipynb**
- **Payoff diagram of a butterfly** — graphing the long and short butterfly payoff functions to see which market regimes profit (their geometry: max profit at the long/short ATM legs, bounded loss wings). *Prereq: payoff helpers, long vs short option exposure, ATM strikes.
### 12. Butterfly Strategy for Options Trading — **Butterfly Strategy for Options Trading/Setup the Butterfly Strategy.ipynb**
- **Setting up the butterfly** — long 2 ATM options & short 2 OTM options to profit from high underlying volatility; its ATM strike derived from the futures price (rounded to the ~ grid), legs offset by one strike. *Prereq: ATM strike, option legs, premium, multi-leg options, setup_butterfly.
### 13. Spread Trading — **Spread Trading/Backtesting Spreads.ipynb**
- **Backtesting bull call and bear put spreads** — vertical spread construction legs, entry/exit conditions (ADX + IVP + days-to-expiry) designed to profitability. *Prereq: call/put spreads, ADX, IVP, entry conditions.
### 14. Iron Condor — **Iron Condor/Backtesting Iron Condor.ipynb**
- **Backtesting a long iron condor** — 4-leg condor constructed from the underlying with net credit from collected premium, entered on ADX? IVP? days-to-expiry conditions and run to expiry. *Prereq: iron condor structure, setup_iron_condor, entry/exit conditions.
### 15. Butterfly Strategy Backtest — **Butterfly Strategy Backtest/Backtesting Short Butterfly.ipynb**
- **Backtesting the short butterfly** — entry driven by ADX/IVP/days-to-expiry, exit at expiry: assemble trades across the historical window, produce a trade log. *Prereq: ADX, IVP, short-butterfly set up, backtest loop, expiry.
- Trade leg/PnL accounting and holding the strategy to expiry as the baseline (contrast with risk-managed variant later). *Prereq: trade logs, expiry.
### 16. Risk Management — **Risk Management/Backtesting Short Butterfly with SL and TP.ipynb**
- **Stop-loss (SL) and take-profit (TP) as risk tools** — exit orders that cap downside and bank gains on short butterflies before expiry. *Prereq: short-butterfly backtest, position P&L sign.
- **Backtest with SL/TP** — event-driven exit at SL/TP vs expiry; the effect on return vs risk (drawdown) vs the expiry-only baseline. *Prereq: short-butterfly backtest, entry/exit events.
### 17. Trade Level Analytics — **Trade Level Analytics/Trade Level Analytics.ipynb**
- **Trade-level metrics** — average PnL per trade, win/loss percentages, average holding period, profit factor (gross win/loss), interpreting the quality of trades over the backtest. *Prereq: trade log from full backtest, per-position PnL.
### 18. Strategy Analysis — **Strategy Analysis/Strategy Analysis.ipynb**
- **Strategy returns** — aggregate the per-trade PnL into the strategy's time series of returns and cumulative returns vs the underlying. *Prereq: trade PnL, time series, cumulative return.
- **Performance metrics/plots** — plots and summary/risk-adjusted measures to judge strategy vs underlying. *Prereq: returns series, risk/return analytics.
### 19. Creation of an Options Screener — **Creation of an Options Screener/Options Liquidity Screener in Python.ipynb**
- **Options liquidity screener** — choose the correct strike, open interest (OI), and options expiry for a multi-leg strategy so the trade is liquid in live markets. *Prereq: strategy needs, open-interest/liquidity concept, options data.
### 20. Capstone Project — **Capstone Project/Capstone Project Model Solution.ipynb** (and `Code-Template-and-Data-Files/.../Capstone Project Solution Template.ipynb`, same analysis in template form)
- **End-to-end capstone model solution** — pick an options strategy, prep data, compute IVP/ADX, define entry/exit, backtest historically, apply SL/TP, compute trade-level + strategy analytics. *Prereq: all prior notebooks; answer bleeding problem statements across the full pipeline.
### 21. Live Trading Template — `Live Trading Template/IBridgePy (live) template/system`
 - **IBridgePy live wrapper (`ros`)** — strategy ported to IBridgePy `butterfly_options_strategy.py`: live entry/exit via exchange APIs, same IVP/ADX/flags, SL/TP handling. *Prereq: backtest logic, live order-execution basics.
## Non-code support files
- `Folder Structure and How to Run Code Files.html`, `ReadMe.html` — setup/execution guides.
- `data_modules/` — historical options & futures data (bzip2), `mtm.csv`, round-trip/trades CSV for analytics.
---
**Concept prerequisites summary (flow):** options data → clean/prep → IV & IVP & ADX → lognormal-POP / empirical-POP → expected profit → payoff diagram → butterfly/spread/iron-condor setup → backtesting → SL/TP risk → trade-level analytics → strategy analysis → screener → capstone.
---
## Systematic-Options-Trading — Section-based course structure (full lesson-by-lesson view)
# Concept Inventory — (Continue) Systematic Options Trading
> **8 sections on disk** (gaps in numbering exist: sections 5–8, 12–15 not present).
## COURSE — Systematic Options Trading
**Purpose:** Learn the end-to-end process of building, backtesting, and automating a systematic (rule-based) options trading strategy on European-style index options (SPX / Nifty 50), including risk management, probability of profit, technical trend filters, and live trading via IBridgePy.
### Section: Section 1 - Introduction
- **CONCEPT:** Course orientation — datasets, brokers, exchanges, and the backtesting-to-automation pipeline for systematic options trading. prereqs: none (foundational).
- **CONCEPT:** European vs American option exercise — learnings apply to European-style index options (SPX, Nifty); single-stock US options carry early-assignment risk. prereqs: options terminology.
- **CONCEPT:** Backtesting and automation overview — why strategies must be validated on historical data before live/paper trading. prereqs: none.
### Section: Section 2 - Systematic Trading Process
- **CONCEPT:** The systematic trading process — a repeatable, rule-driven loop (idea → data → signal → sizing → backtest → automation) replacing discretionary trading. prereqs: none.
- **CONCEPT:** From a strategy idea to tradable rules — every trade decision must be expressible as deterministic conditions on data. prereqs: systematic trading process.
### Section: Section 3 - Options Data
- **CONCEPT:** Options data structure and option chains — how strikes, expirations and contract chains are organized for a given underlying (open interest, volume, bid/ask, IV). prereqs: none.
- **CONCEPT:** Data storage — persistent, structured storage of recurring options records (daily EOD option chains). prereqs: options data structure.
- **CONCEPT:** Sourcing US options data — OptionsDX download workflow spanning many expirations (1 day to 3+ years) and loading into a single DataFrame. prereqs: data structure.
- **CONCEPT:** Recurrent calculations — computing streaming statistics (e.g. rolling standard deviation) from previous values to save store/time when storage is constrained. prereqs: basic stats.
- **CONCEPT:** Options data vendors — paid/free historical options data vendors and reliability/authorization considerations. prereqs: none.
### Section: Section 4 - Data Pre-Processing
- **CONCEPT:** Data pre-processing / cleaning — handling missing and erroneous options-chain values before modeling; clean data is a prerequisite to reliable strategy results. prereqs: options data structure.
### Section: Section 9 - Lognormal Distribution
- **CONCEPT:** Lognormal distribution — why asset prices (rather than returns) are modeled lognormal; linking lognormal to normal mean/median/mode/variance. prereqs: normal distribution, basic statistics.
- **CONCEPT:** Lognormal vs normal — prices are multiplicative (log-normal), returns are additive (normal). prereqs: lognormal distribution.
### Section: Section 10 - Probability of Profit Using Lognormal Distribution
- **CONCEPT:** Probability of Profit (PoP) via lognormal — using the lognormal CDF to compute the probability an options strategy ends profitable. prereqs: lognormal distribution, CDF.
### Section: Section 11 - Probability of Profit Using Empirical Distribution
- **CONCEPT:** Empirical distribution for PoP — when data does not fit standard models, build an empirical CDF in Python and compute probability values from it. prereqs: lognormal PoP, Python stats, CDF.
### Section: Section 16 - Technical Indicator
- **CONCEPT:** Average Directional Index (ADX) — quantifies trend STRENGTH (0–100; >25–30 signals strong trend), not directional; a rising/falling ADX line shows trend strengthening/weakening, not reversal. prereqs: trend concepts, technical indicators.
### Section: Section 3 → (supporting strategy concepts from notebooks/resources)
- **CONCEPT:** The recurring CDF-based option strategies (Lognormal PoP, empirical PoP) prereq the strategies because strategies score/select contracts using IV and PoP. prereqs: PoP concept.
- **CONCEPT:** Strategy families named in course — Butterfly, Iron Condor, Bull Call Spread, Bear Put Spread, plus Calendar, Diagonal, Box, Jelly Roll logic. prereqs: option payoff, spread mechanics.
## Course Prerequisite Map
- Foundations → Options Data → Data Pre-Processing → Lognormal Distribution → Probability of Profit (Lognormal) → Probability of Profit (Empirical) → Strategy + ADX filter → Backtesting / Automation
- Backtesting and Automation depends on a complete tested strategy (all prior blocks).
- ADX (Section 16) is an indicator layer applied downstream onto strategy signals; PoP (Sections 10–11) is fed by distribution knowledge (Section 9).
- Overlapping D: notebook workflow: Data → Screener (IP Percentile) → PoP → Payoff → Backtest → Capstone.


====================
Technical-Indicators-Strategies-Using-Python
====================

# Technical Indicators Strategies in Python — Concept Inventory
## COURSE: Technical Indicators Strategies in Python
A () course on building and backtesting technical-indicator trading strategies in Python. Covers moving averages (SMA/EMA/WMA), MACD, RSI, ROC, volume indicators (Chaikin), TRIN, market-breadth analysis, screeners, trade sheets, transaction costs/slippage, risk management, and performance metrics. Repetitive concepts (data import, signal→return computation) are defined once in their introducing lesson and cross-referenced.
---
## MODULE: Moving Average
### LESSON: Simple Moving Average
- **Moving average (rolling average)** — the mean of a data field over a set of consecutive periods; a trend-following indicator. prereqs: none.
- **Simple Moving Average (SMA)** — moving average that weighs all data points equally. prereqs: moving average.
- **`rolling(window).mean()`** — pandas method computing a rolling average over a lookback window. prereqs: pandas.
- **Bullish crossover** — SMA crosses above the close price (candle 1 SMA below close, candle 2 SMA above close); signals an uptrend. prereqs: SMA.
- **Bearish crossover** — SMA crosses below the close price; signals a downtrend. prereqs: SMA.
- **Crossover detection with `np.where`** — identifies crossovers using conditions on current and shifted values. prereqs: numpy, shift.
### LESSON: SMA and Price Crossover
- **SMA and Price Crossover Strategy** — a long-only strategy buying when close > SMA. prereqs: SMA.
- **Entry condition** — enter long when the SMA crosses the price line from above (go long when close > SMA). prereqs: crossover.
- **Exit condition** — exit when the SMA crosses the price line from below. prereqs: crossover.
- **Signal column** — `np.where(close > SMA, 1, 0)` stores 1 for buy, 0 otherwise. prereqs: numpy.
- **`pct_change()`** — computes percentage change (returns) of a price series. prereqs: pandas.
- **Strategy returns** — `returns * signal.shift(1)`; `shift(1)` avoids look-ahead bias by using the previous signal. prereqs: returns, shift.
- **`shift(1)`** — lags a series by one period so positions are known before returns accrue. prereqs: pandas.
- **Cumulative strategy returns** — `(strategy_returns + 1).cumprod()` visualises long-term performance. prereqs: strategy returns.
### LESSON: Exercise Notebook (Precomputed SMA Signals)
- **Precomputed signal data** — reading a CSV that already contains close, SMA, and signal columns. prereqs: read_csv.
- **Trade signals dataframe** — a prices/signals dataset used to build trade sheets and metrics. prereqs: signals.
---
## MODULE: Exponential Moving Average
### LESSON: Exponential Moving Average
- **Exponential Moving Average (EMA)** — moving average assigning exponentially increasing weights to more recent data. prereqs: WMA.
- **EMA vs WMA weighting** — WMA weights rise linearly; EMA weights rise exponentially. prereqs: EMA, WMA.
- **`ewm(span=).mean()`** — pandas method computing the EMA with a lookback span. prereqs: pandas.
- **EMA price-crossing strategy** — buy when close > EMA (signal 1), exit on bearish crossover. prereqs: EMA.
- **`get_strategy_returns()`** — utility function plotting signals, returns, cumulative returns, and drawdowns. prereqs: strategy returns.
---
## MODULE: Weighted Moving Average
### LESSON: Weighted Moving Average
- **Weighted Moving Average (WMA)** — a moving average that assigns higher weight to the most recent data point. prereqs: SMA.
- **WMA rationale** — responds faster than SMA without discarding older data. prereqs: SMA.
- **`ta.WMA(data, timeperiod)`** — TA-Lib function computing the weighted moving average. prereqs: talib.
- **WMA crossover** — buy when close price > WMA; exit on bearish crossover. prereqs: WMA, crossover.
- **Moving average choice** — SMA/WMA/EMA selection depends on holding period and response speed. prereqs: SMA, WMA, EMA.
---
## MODULE: Multiple Moving Averages
### LESSON: Moving Average Crossovers
- **Moving average crossover** — the point where one moving average cuts through another moving average. prereqs: moving average.
- **Short and long EMA** — two EMAs with different lookback periods (e.g. 100 and 500). prereqs: EMA.
- **Bullish MA crossover** — short EMA crosses above the long EMA; suggests an uptrend / long entry. prereqs: short/long EMA.
- **Bearish MA crossover** — short EMA crosses below the long EMA; suggests a downtrend / exit. prereqs: short/long EMA.
- **Crossover entry** — go long when the short EMA > long EMA. prereqs: crossover strategy.
- **Exponential Moving Average Crossover Strategy** — use two EMAs to generate buy/sell signals. prereqs: EMA, crossover.
### LESSON: Triple Crossover Strategy
- **Triple Crossover Strategy** — adds a medium EMA to the double crossover (short, medium, long EMAs). prereqs: double crossover.
- **Triple entry condition** — enter long when the short EMA crosses both the long and medium EMAs from below. prereqs: crossover.
- **Signal for triple crossover** — buy when short EMA > long EMA AND short EMA > medium EMA. prereqs: numpy.
- **Signal reduction** — more moving averages reduce false signals but can miss profitable opportunities. prereqs: triple crossover.
---
## MODULE: MACD
### LESSON: MACD
- **MACD (Moving Average Convergence Divergence)** — momentum indicator from two EMAs. prereqs: EMA.
- **MACD line** — fast-period EMA minus slow-period EMA (default 12 and 26). prereqs: EMA.
- **Signal line** — EMA of the MACD line (default 9-period). prereqs: MACD line.
- **MACD histogram** — MACD line minus signal line. prereqs: MACD line, signal line.
- **`ta.MACD(close)`** — TA-Lib returns MACD line, signal line, and histogram. prereqs: talib.
- **Buy signal** — buy when the MACD line crosses above the signal line (`MACD line > Signal line`). prereqs: MACD components.
- **Exit signal** — exit when the MACD line crosses below the signal line. prereqs: MACD components.
- **`np.where` for signals** — vectorized conditional to build a 1/0 signal column. prereqs: numpy.
---
## MODULE: Multiple Timeframes
### LESSON: Data Resampling
- **Multiple timeframe analysis** — studying price charts across more than one timeframe. prereqs: none.
- **Data resampling** — converting minute data into longer candles (e.g. 15min, 240min) with `resample()`. prereqs: pandas.
- **OHLCV resample dict** — open→first, high→max, low→min, close→last, volume→sum. prereqs: resampling.
- **`resample(freq, label, closed).agg(dict)`** — aggregates minute data to a chosen frequency. prereqs: pandas.
- **Short and long SMA per timeframe** — compute `sma_short`/`sma_long` (e.g. rolling 50 and 200) in both timeframes. prereqs: SMA, resampling.
- **`pd.merge`** — merges two dataframes on their datetime index with suffixes per timeframe. prereqs: pandas.
- **`fillna(method='ffill')`** — forward-fills missing values after merging frequencies. prereqs: merge.
- **Column selection** — filter the merged dataframe to the columns needed for the strategy. prereqs: dataframe.
### LESSON: Multiple Timeframe Strategy
- **Higher/lower timeframe** — e.g. 240min (higher, trend direction) and 15min (lower, entry/exit timing). prereqs: data resampling.
- **Timeframe selection** — higher timeframe under 1 day (240min); lower from a factor of 4 (240 / 4 / 4 = 15min). prereqs: resampling.
- **Crossover per timeframe** — bullish crossovers identified in both `crossover_15min` and `crossover_240min` columns. prereqs: crossover.
- **Multiple-timeframe entry** — enter long only when bullish crossover is confirmed in BOTH higher and lower timeframes. prereqs: multi-timeframe.
- **Multi-timeframe signal** — `np.where(crossover_240min, 1, 0) * crossover_15min`. prereqs: numpy.
- **Trend confirmation** — higher timeframe sets trend direction; lower timeframe confirms timing. prereqs: multi-timeframe.
- **Three-timeframe extension** — higher (major), medium (minor), and lower (signals) timeframes. prereqs: multiple timeframe.
---
## MODULE: ROC
### LESSON: Rate of Change
- **ROC (Rate of Change)** — percentage change in prices between current and price N periods ago. prereqs: none.
- **`pct_change(period)`** — pandas method computing ROC over a gap (default 1). prereqs: pandas.
- **Positive/negative momentum** — positive ROC implies rising prices; negative ROC implies falling prices. prereqs: ROC.
- **ROC semi-annual** — `pct_change(125)` compares price to ~6 months ago. prereqs: ROC.
- **ROC long-only strategy** — signal 1 when ROC_125 > 0 (buy), else 0 (no position). prereqs: ROC, signals.
---
## MODULE: Chaikin Oscillator
### LESSON: Volume Indicators
- **Volume indicators** — evaluate a security's buying vs selling pressure and which side controls price action. prereqs: none.
- **Chaikin A/D** — cumulative volume line built from price changes; measures buying/selling pressure. prereqs: volume indicators.
- **`ta.AD(high, low, close, volume)`** — computes the Chaikin accumulation/distribution line. prereqs: talib.
- **Chaikin Oscillator** — momentum of the Chaikin A/D line; the difference of slow and fast EMA of Chaikin AD. prereqs: Chaikin A/D.
- **`ta.ADOSC(high, low, close, volume, fastperiod, slowperiod)`** — computes the Chaikin oscillator. prereqs: talib.
- **Interpreting the oscillator** — >0 means buying pressure has momentum; ≤0 means selling pressure has momentum. prereqs: Chaikin oscillator.
### LESSON: Trading Hypothesis
- **Trading hypothesis** — a stated rule linking indicator behaviour to entry/exit decisions before implementation. prereqs: none.
---
## MODULE: Chaikin Oscillator Strategy
### LESSON: Chaikin Oscillator Strategy
- **Chaikin long-only strategy** — buy when Chaikin Oscillator > 0, hold while above 0. prereqs: Chaikin oscillator.
- **Entry condition** — open long when `chaikin_osc > 0`. prereqs: Chaikin oscillator.
- **Exit condition** — close long when Chaikin ≤ 0. prereqs: Chaikin oscillator.
- **Chaikin signal** — `np.where(chaikin_osc > 0, 1, 0)`. prereqs: numpy.
### LESSON: Chaikin Oscillator and Bollinger Bands Strategy
- **Bollinger Bands** — the bands of an SMA plus/minus a multiple of a moving standard deviation. prereqs: SMA.
- **`ta.BBANDS(series, period, nbdevup, nbdevdn)`** — returns upper, middle, and lower bands. prereqs: talib.
- **Upper/middle/lower band** — moving average middle band; upper/lower set by moving std ± dev. prereqs: Bollinger band.
- **Composite entry** — long entry when Chaikin crosses below the lower band (likely reversal up). prereqs: Bollinger band, oscillator.
- **Long exit** — exit when Chaikin crosses above the middle band. prereqs: oscillator, bands.
- **Short entry** — go short when Chaikin crosses above the upper band. prereqs: oscillator, bands.
- **Short exit** — exit short when Chaikin crosses below the middle band. prereqs: oscillator, bands.
- **Long/short signal combination** — sum long (+1) and short (−1) signals into one column. prereqs: signals.
---
## MODULE: Transaction Costs and Slippage
### LESSON: Implementation of Transaction Cost and Slippage
- **Transaction costs** — commissions, individual taxes, and exchange-mandated fees on executed trades. prereqs: none.
- **Brokerage cost** — a broker commission as % of traded value (e.g. 0.03%) plus taxes (e.g. 0.02%). prereqs: none.
- **Slippage** — the difference between the expected and actual execution price. prereqs: none.
- **Slippage modelling** — estimate from the last five-minute candles of each trading day using groupby. prereqs: groupby.
- **Buy-order slippage** — worst/buy execution at the high: `(high − close)/close`. prereqs: slippage.
- **Sell-order slippage** — worst/sell execution at the low: `(close − low)/close`. prereqs: slippage.
- **Total charges** — transaction cost + slippage + brokerage, applied on net position changes. prereqs: all costs.
- **Net strategy returns** — deduct trading cost (total charges × |signal − signal.shift(1)|) from gross returns. prereqs: strategy returns, costs.
- **Cost impact** — transaction costs can convert a profitable backtest (5x) into a marginal result (0.2x). prereqs: net returns.
---
## MODULE: Relative Strength Index
### LESSON: Relative Strength Index
- **RSI (Relative Strength Index)** — oscillator measuring trend strength, ranging 0–100, identifying overbought/oversold regions. prereqs: none.
- **`ta.RSI(close, timeperiod)`** — TA-Lib computes RSI with a lookback period (default 14). prereqs: talib.
- **Oversold region** — RSI < 30 implies the stock may reverse up, a possible buy. prereqs: RSI.
- **Overbought region** — RSI > 70 implies overbought, a possible sell/exit. prereqs: RSI.
- **RSI long-only strategy** — long entry when RSI < 30; exit when RSI > 70. prereqs: RSI.
- **Forward-filling signals** — `fillna(method='ffill')` keeps a position until an exit triggers. prereqs: signal.
---
## MODULE: Calculation of TRIN Indicator
### LESSON: Calculation of TRIN Indicator
- **TRIN indicator** — a market breadth tool using price and volume of an index's constituents. prereqs: none.
- **Market breadth** — a measure of how many market stocks are moving in a given direction. prereqs: none.
- **Advancing/declining stocks** — count of index constituents whose price rose vs. fell versus yesterday. prereqs: market breadth.
- **AD ratio** — number of advancing stocks divided by the number of declining stocks. prereqs: market breadth.
- **`AU` volume ratio** — traded volume of advancing stocks divided by volume of declining stocks. prereqs: market breadth.
- **TRIN formula** — TRIN = AD ratio / AD volume ratio. prereqs: AD ratio, AD volume ratio.
- **TRIN = 1 (neutral)** — a balanced market when advancing equals declining counts and volumes. prereqs: TRIN.
- **TRIN < 1 (bullish)** — more volume in advancing stocks, interpreted as an uptrend. prereqs: TRIN.
- **TRIN > 1 (bearish)** — more volume in declining stocks. prereqs: TRIN.
- **`diff()`** — pandas method computing the change from the previous row. prereqs: pandas.
---
## MODULE: TRIN Indicator Based Strategy
### LESSON: Implementation of TRIN Strategy
- **TRIN limitation** — TRIN fails in extreme scenarios, so decompose it into AUD and AUD-volume ratios. prereqs: TRIN.
- **Trinity This smoothing** — calculate a 9-day SMA of the AD ratio and AD volume ratio to reduce false signals. prereqs: SMA.
- **TRIN buy signal** — buy when both AD ratio and AD volume ratio are below their respective SMAs. prereqs: TRIN components.
- **TRIN exit signal** — exit when either the AD ratio or AD volume ratio rises above its SMA. prereqs: TRIN components.
- **Strategy vs index returns** — compare the strategy's cumulative returns against the S&P500 buy-and-hold. prereqs: cumulative returns.
---
## MODULE: Creation of a Screener Using Technical Indicators
### LESSON: Implementation of Screener Using Three Indicators
- **Technical-indicator screener** — filters stocks by conditions using indicator values. prereqs: indicators.
- **Screener indicators** — ADX (trend), Chaikin ROC oscillator, and SMA; plus volatility (order/rule step). prereqs: ADX, ROC, SMA.
- **Positive vs negative ADX** — drop stocks where the positive-direction ADX is below the negative-direction ADX. prereqs: screener.
- **Ranking indicator values** — use `rank()` on each indicator column when comparing stocks. prereqs: pandas.
- **Low-volatility filter** — sift out top N low-volatility stocks to reduce risk. prereqs: ranking.
- **Score and sort** — take the equal-weight average of indicator ranks, sort descending, keep the top 20. prereqs: ranking.
- **`pd.read_html`** (in capstone) — read tables directly from a Wikipedia page via pandas. prereqs: pandas.
### LESSON: Technical Analysis Dashboard
- **Technical Analysis Dashboard** — input a ticker and get indicator values plus trading signals. prereqs: none.
- **Dashboard data load** — `yf.download(stock, date, auto_adjust=True)` fetches the asset data. prereqs: yfinance.
- **Moving-average signals** — buy signal if the last price > the MA value over several periods, otherwise sell. prereqs: moving average.
- **Oscillator values** — record the last day's ADX (14), Money Flow Index, and modern. prereqs: talib.
- **Volume indicator section** — compute the Chaikin A/D oscillator (`ta.ADOSC`). prereqs: Chaikin.
- **Market breadth** — the percentage of S&P500 stocks above short/long SMAs; >60% implies an uptrend. prereqs: SMA, market breadth.
---
## MODULE: Putting It All Together
### LESSON: Multiple Indicator Strategy
- **Multiple indicator strategy** — combine indicators of different categories (trend + volume). prereqs: none.
- **Price ROC** — `close.pct_change(500)` for a long-horizon trend measurement. prereqs: ROC.
- **Chaikin Oscillator ROC** — `chaikin_osc.pct_change(500)` measures volume momentum. prereqs: Chaikin oscillator.
- **Entry condition** — enter when oscillator ROC > 0 AND price ROC > 0.05. prereqs: ROC.
- **Exit condition** — exit when oscillator ROC < 0 OR price ROC < 0. prereqs: ROC.
- **Signal reduction** — combining indicators reduces false signals and can miss opportunities. prereqs: multiple-indicator strategy.
---
## MODULE: Risk Management
### LESSON: ATR-Based Stop-Loss and Take-Profit
- **Fixed stop-loss/taking-profit limitation** — fixed levels ignore market volatility, causing early/late exits. prereqs: none.
- **ATR (Average True Range)** — a volatility gauge of how much an asset moves on average over a period. prereqs: none.
- **True range** — `max(High−Low, |High−Prev Close|, |Low−Prev Close|)`. prereqs: ATR.
- **ATR calculation** — the average of true range over n periods. prereqs: true range.
- **`ta.ATR(high, low, close, timeperiod)`** — computes the ATR. prereqs: talib.
- **ATR-based stop-loss** — the stop level set at a multiple of ATR away from entry price. prereqs: ATR.
- **ATR-based take-profit** — the take-profit at a multiple of ATR away from entry price. prereqs: ATR.
- **Trade book with ATR exits** — a trade sheet capturing entry/exit when the stop-loss or target hits. prereqs: trade book.
- **Volatility-aware improvement** — ATR-adjusted exits raised cumulative return and Sharpe ratio (crucial example). prereqs: ATR exits.
---
## MODULE: Trade Sheet
### LESSON: Generate Trade Sheet
- **Trade sheet** — records all trades with Position, Entry Date/Price, Exit Date/Price, PnL. prereqs: none.
- **Long crossover confirmation** — `close < SMA` on the previous candle and `close ≥ SMA` now. prereqs: crossover.
- **Exit crossover confirmation** — `close > SMA` on the previous and `close ≤ SMA` now. prereqs: crossover.
- **Iterative trade recording** — loop over dates, treat on entry confirmation and close on exit confirmation. prereqs: loops, signals.
- **Trade PnL** — `(Exit Price − Entry Price) × Position`. prereqs: trade sheet.
---
## MODULE: Performance Analysis
### LESSON: Trade Level Analytics
- **Trade-level analytics** — metrics evaluating a strategy after each trade executes. prereqs: trade sheet.
- **TradeTotal PnL** — the sum of gains and losses across all trades. prereqs: trade sheet.
- **Win rate/percentage** — winning trades / total trades × 100. prereqs: trade sheet.
- **Loss percentage** — losing trades / total trades × 100. prereqs: trade sheet.
- **Per-trade PnL winners/losers** — mean profit per winning and mean loss per losing trade (absolute value). prereqs: trade analytics.
- **Average trade duration** — average holding period; locked capital reduces simultaneous trades. prereqs: trade dates.
- **Profit given Factor** — (Win% × avg win) / (Loss% × avg loss); money made vs lost. prereqs: trade analytics.
- **Profit-factor interpretation** — <1 unprofitable, =1 breakeven, >1 desired. prereqs: profit factor.
- **Low win rate with profits** — a strategy can profit even below a 50% win rate if gains outsize losses. prereqs: win rate.
### LESSON: Performance Metrics
- **Performance metrics** — analyze returns between a trade's entry and exit. prereqs: trade-level analytics.
- **Equity curve** — plot of cumulative strategy returns; consistent positive slope implies profit. prereqs: strategy returns.
- **Cumulative return** — `(strategy_return + 1).cumprod()`. prereqs: strategy returns.
- **CAGR** — the compound annual growth rate of the strategy. prereqs: cumulative returns.
- **Histogram of returns** — distribution of the strategy returns. prereqs: strategy returns.
- **Annualised volatility** — `std(strategy_returns) × sqrt(252 × n)` for candles per day. prereqs: returns.
- **Sharpe ratio** — `(R_x − R_f)/σ_x`; mean excess return per unit of risk; >1 preferred. prereqs: returns, volatility.
- **Risk-free rate** — the return of a risk-free asset used in the Sharpe ratio. prereqs: Sharpe.
- **Maximum drawdown** — `(Peak − Trough)/Peak` of cumulative equity; the largest peak-to-trough loss. prereqs: equity curve.
- **`cummax()`** — pandas rolling maximum to track the peak for drawdown. prereqs: pandas.
- **Drawdown series** — `(Cumulative − Peak)/Peak`. prereqs: maximum drawdown.
- **`get_strategy_returns()`** — reusable helper computing and plotting returns + performance metrics. prereqs: all metrics.
---
## MODULE: Capstone Project
### LESSON: Capstone Project (Solution + Template)
- **Capstone project** — build and backtest a strategy combining market breadth, SMA, and Supertrend. prereqs: all modules.
- **Market breadth analysis** — the percentage of S&P500 stocks above their 50-SMA. prereqs: market breadth, SMA.
- **Long-term trend signal** — Apple's daily close > 50-period SMA. prereqs: SMA.
- **Multiple-frequency merge** — merge 15-min signals with the daily SMA using `pd.merge` + ffill. prereqs: merge, resample.
- **Supertrend indicator** — ATR-based bands indicating an uptrend. prereqs: ATR.
- **Supertrend parameters** — `atr_period = 27×14`, `atr_multiplier = 3`. prereqs: ATR.
- **`ta.ATR` in Supertrend** — uses `ta.ATR(high, low, close, timeperiod)` for the volatility bands. prereqs: ATR.
- **Combine strategy signals** — returns only when market breadth > condition, SMA crossover, and Supertrend all agree. prereqs: strategy signal.
- **Strategy returns** — `supertrend.shift(1) × close.pct_change() × sma_crossover.shift(1) × (breadth>50).shift(1)`. prereqs: multi-indicator.
- **Portfolio performance** — apply the strategy to multiple tickers and average the returns; plot cumulative. prereqs: portfolio, cumulative returns.
- **Model template vs solution** — a scaffold notebook with placeholders to build the capstone. prereqs: capstone.
---
## Technical-Indicators-Strategies-Using-Python — Section-based course structure (full lesson-by-lesson view)
# Concept Inventory — Technical Indicators Strategies in Python
## COURSE: Technical Indicators Strategies in Python
### Section: Section 1 - Introduction
- **Introduction to the course:** scope — indicators, strategies, backtesting, screener. prereqs: none.
- **Course structure (PDF, image):** learning path outline. prereqs: none.
- **FAQs (PDF):** common course questions. prereqs: none.
### Section: Section 2 - Principles of Technical Analysis
- **Principles of technical analysis:** price discounting, trends, history repeats; assumptions. prereqs: none.
- **Why technical analysis gets a bad reputation:** subjectivity and misuse critiques. prereqs: technical analysis.
- **Additional reading (PDF):** fundamental principles reading. prereqs: technical analysis.
### Section: Section 3 - Trend is your Friend
- **Trend is your friend:** trend analysis principle; trade with the prevailing trend. prereqs: technical analysis.
### Section: Section 4 - Moving Average
- **Simple Moving Average (SMA):** mean of last N prices via rolling window. prereqs: price series.
- **Classification of moving averages:** SMA/WMA/EMA families and applications. prereqs: moving average.
- **Strategy flow diagram (PDF):** building a SMA-based signal. prereqs: SMA.
- **Additional reading for data source (PDF):** fetching price data. prereqs: pandas, data.
### Section: Section 6 - Performance Analysis
- **Additional reading on performance metrics (PDF):** Sharpe, drawdown, CAGR evaluation. prereqs: returns.
- **Additional reading on trade level analytics (PDF):** per-trade win/loss analysis. prereqs: trade sheet.
### Section: Section 7 - Transaction Costs and Slippage
- **Transaction costs and slippage:** brokerage, spread, market impact; impact on net returns. prereqs: backtesting.
- **Additional reading (PDF):** cost modeling detail. prereqs: transaction costs.
### Section: Section 10 - Weighted Moving Average
- **Weighted Moving Average (WMA):** average with linearly increasing weights on recent prices. prereqs: moving average.
- **Anatomy of a candle (PDF):** OHLC anatomy. prereqs: price data.
- **Strategy flow diagram (PDF):** WMA-based signal. prereqs: WMA.
### Section: Section 11 - Exponential Moving Average
- **Exponential Moving Average (EMA):** weighted average with exponential decay favoring recent prices. prereqs: moving average.
- **EMA calculation (PDF):** recursive formula, smoothing factor. prereqs: EMA.
- **Types of moving averages (PDF):** SMA vs EMA vs WMA comparison. prereqs: moving average.
- **5 FAQs about moving averages (PDF):** lag, sensitivity. prereqs: moving average.
- **Strategy flow diagram (PDF):** EMA-based signals. prereqs: EMA.
### Section: Section 12 - Multiple Moving Averages
- **Moving average crossovers:** double and triple crossover strategies (e.g. MACD-like). prereqs: moving averages.
- **Strategy flow diagrams (PDF):** multi-MA signal pipelines. prereqs: crossovers.
- **Additional reading on moving average strategies (PDF):** applications. prereqs: crossovers.
### Section: Section 13 - MACD
- **MACD entry points:** MACD-based long/short entries. prereqs: MACD.
- **MACD line & signal line:** 12-26 EMA diff and 9 EMA signal, crossovers. prereqs: EMA.
- **MACD histogram:** (MACD line − signal line), momentum strength. prereqs: MACD.
- **Strategy flow diagram (PDF):** MACD strategy. prereqs: MACD.
### Section: Section 14 - ROC
- **ROC (Rate of Change):** momentum indicator = (P_t/P_{t-n} − 1). prereqs: price series.
- **ROC strategy logic (PDF):** trading on ROC sign/magnitude. prereqs: ROC.
### Section: Section 15 - Intuition and Interpretation of RSI
- **Intuition of RSI indicator:** measures speed/magnitude of price change, 0-100 oscillator. prereqs: momentum.
- **Interpret values of RSI:** overbought (>70) / oversold (<30) zones. prereqs: RSI.
### Section: Section 16 - Properties and Practical Application of RSI
- **Properties of RSI indicator:** bounded range, mean-reverting behavior. prereqs: RSI.
- **RSI in action:** divergences and practical signal use. prereqs: RSI.
- **RSI strategy logic (PDF):** RSI-based entry/exit. prereqs: RSI.
- **Additional reading on RSI (PDF):** detailed RSI reference. prereqs: RSI.
### Section: Section 17 - Volume
- **Spikes in volume:** identifying unusual volume surges as signals. prereqs: volume.
- **On-Balance Volume (OBV):** cumulative volume adding/subtracting by price direction. prereqs: volume, price.
### Section: Section 18 - Chaikin AD
- **Chaikin Accumulation/Distribution:** money-flow indicator from close location value vs HL range, times volume. prereqs: volume, price range.
- **Additional reading on Chaikin AD (PDF):** reference. prereqs: Chaikin AD.
### Section: Section 19 - Limitations of Chaikin AD and OBV
- **Limitations of OBV and Chaikin AD:** divergence does not always work; lag and noise. prereqs: Chaikin AD, OBV.
### Section: Section 20 - Chaikin Oscillator
- **Chaikin oscillator (PDF):** EMA(spread) of the Chaikin AD measures momentum of buying/selling pressure. prereqs: Chaikin AD, EMA.
### Section: Section 21 - Chaikin Oscillator Strategy
- **Chaikin oscillator strategy logic (PDF, image):** signal rules on oscillator. prereqs: Chaikin oscillator.
- **Bollinger Bands (PDF):** price bands at ±kσ around SMA. prereqs: SMA, std.
- **Chaikin oscillator + Bollinger strategy logic (PDF, image):** composite strategy. prereqs: Chaikin oscillator, Bollinger.
### Section: Section 22 - Putting It All Together
- **Combining indicators:** using multiple indicators for stronger confirmations. prereqs: indicators.
- **Chaikin oscillator with ROC:** composite momentum strategy. prereqs: Chaikin oscillator, ROC.
- **Strategy flow diagram (PDF):** integrated pipeline. prereqs: combining indicators.
### Section: Section 23 - Multiple Timeframes
- **Multiple timeframes:** combining e.g. 15-min + 240-min signals for context and entries. prereqs: time series.
### Section: Section 24 - ATR
- **ATR (Average True Range):** volatility measure from true range (max of high-low, high-prevClose, low-prevClose). prereqs: OHLC.
- **Additional reading for ATR (PDF):** reference and use. prereqs: ATR.
### Section: Section 25 - Risk Management
- **ATR-based SL & TP:** setting stop-loss/take-profit as multiples of ATR. prereqs: ATR.
- **Additional reading for SL & TP using ATR (PDF):** adaptive stops research. prereqs: ATR, SL/TP.
### Section: Section 26 - Market Breadth Analysis
- **Need of market breadth analysis:** assessing broad market participation beyond single index. prereqs: equity indices, technical analysis.
### Section: Section 27 - McClellan Indicator
- **McClellan indicator:** breadth indicator from exponentially smoothed advance/decline net change (AD line). prereqs: market breadth.
- **Additional reading (PDF):** reference. prereqs: McClellan.
### Section: Section 28 - Application of McClellan Indicator
- **Application of McClellan indicator:** overbought/oversold breadth signals. prereqs: McClellan.
- **Can McClellan predict a market crash:** historical crashes vs extreme breadth readings. prereqs: McClellan.
- **Additional reading (PDF):** application reference. prereqs: McClellan.
### Section: Section 29 - Calculation of TRIN Indicator
- **TRIN (Arms Index):** (advancing/declining ratio) / (adv/del volume ratio); volume-weighted breadth. prereqs: market breadth, volume.
### Section: Section 30 - TRIN Indicator Based Strategy
- **TRIN strategy:** trading on TRIN extremes (fear/greed breadth). prereqs: TRIN.
- **Flow chart of TRIN strategy (PDF, image):** signal logic. prereqs: TRIN.
- **Alternative methods for market breadth (PDF):** other breadth approaches. prereqs: market breadth.
- **Additional reading for TRIN (PDF):** reference. prereqs: TRIN.
### Section: Section 31 - Creation of a Screener Using Technical Indicators
- **Creation of a screener using technical indicators:** ranking stocks by indicator values and selecting top N. prereqs: indicators, ranking.
- **Alternative method for creating screener (PDF):** level-based vs rank-based screening. prereqs: screener.
### Section: Section 32 - Five Secrets of Successful Traders
- **Five secrets:** discipline, risk control, system, consistency, review. prereqs: none.
- **Technical analysis checklist (PDF):** pre-trade checklist. prereqs: technical analysis.
### Section: Section 33 - Capstone Project
- **Problem statement (PDF):** build an indicator-based strategy with backtesting. prereqs: all previous.
- **Code template & solution (zips):** provided code and data. prereqs: capstone.
### Section: Section 35 - Summary
- **Summary of the course:** recap and downloadable resources. prereqs: all.
- **Next steps (PDF):** what to do after the course. prereqs: all.
## Course Prerequisite Map
Before this course a learner needed: Python + pandas + NumPy for data handling and indicator math; financial OHLCV data and matplotlib plotting; moving averages and trend concepts; an understanding of returns, compounding, and basic statistics (mean, standard deviation); and foundational backtesting and performance-metric concepts (Sharpe, drawdown, transaction costs, slippage, trade-level analytics).


====================
Trading-Using-LLM
====================

# Trading Using LLM — Concept Inventory
Exhaustive per-module / per-lesson inventory of every concept taught in this "Trade FOMC meeting using LLM" course, extracted from all notebooks (markdown + code) and the supporting `finbert_sa.py` / `trade_fed_utils.py` modules.
## COURSE: Trading Using LLM
Scope: collect & preprocess FOMC (Fed) press-conference transcripts and SPY price data, score the text with FinBERT (a financial LLM), optionally transcribe earnings-call audio with OpenAI Whisper, then build and compare multiple FOMC sentiment-driven trading strategies via backtesting.
---
## MODULE: Data Collection and Preprocessing
### LESSON: Data Collection and Preprocessing.ipynb
- **FOMC press conference:** post-meeting press conference where the Fed Chair reads a statement — its speech text is the raw sentiment input. prereqs: Federal Reserve, monetary policy
- **FOMC transcripts (PDF):** 21 press-conference transcript PDFs (Jan 2022 – Jul 2024) downloaded from the Federal Reserve website. prereqs: PDFs, data collection
- **FOMC_Timestamp metadata:** CSV of Meeting Date, Start Time, End Time, and Duration of the Chairman's speech per meeting. prereqs: CSV, datetime
- **PDF text extraction (pypdf):** `from pypdf import PdfReader` + `reader.pages[i].extract_text()` to pull text out of each PDF page. prereqs: PDFs, Python
- **Header/footer filtering:** `is_header_or_footer` drops boilerplate lines ("Transcript of Chair Powell's FOMC Press Conference", "Page", "PRELIMINARY") so only speech content remains. prereqs: string matching, data cleaning
- **Speech boundary detection:** locate the start ("Good afternoon.") and end ("Thank you.") phrases to slice out just the Chair's prepared speech. prereqs: substring search, slicing
- **Text cleaning with regex:** `re.sub` fixes broken words/newlines (`\n(?!\s*[A-Z])`), collapses whitespace (`\s+`), and removes spaces before punctuation. prereqs: regular expressions, whitespace
- **Words-per-minute estimation:** total words ÷ speech duration (minutes) so text can be spread evenly across 1-minute bins. prereqs: division, durations
- **Minute-level segmentation:** assign `total_minutes` buckets of ~words_per_minute words each, each tagged with a 1-min timestamp and a `video_id`. prereqs: loops, slicing, datetime
- **Timezone conversion:** `tz_localize('America/New_York').tz_convert('UTC')` turns meeting time into coordinated UTC. prereqs: timezones, pandas
- **Alpaca API for live prices:** `StockHistoricalDataClient(api_key, secret_key)` provides minute-level market data. prereqs: API clients, market data
- **StockBarsRequest / TimeFrame.Minute:** Alpaca request object specifying symbol (SPY), 1-minute timeframe, and start/end for `get_stock_bars`. prereqs: Alpaca API, OHLC
- **OHLC data:** Open/High/Low/Close bars fetched per timestamp for the SPY ETF during the live meeting. prereqs: OHLC, ETFs
- **Data merging:** `pd.merge(result_df, ohlc_df, on='timestamp')` joins speech text with matching price bars. prereqs: DataFrame merge, key column
- **Persisting combined dataset:** save the merged text + OHLC frame to `fomc_text_spy_ohlc_jan22_to_jul24.csv` for sentiment work. prereqs: CSV export
---
## MODULE: Sentiment Analysis of FOMC Transcripts
### LESSON: Sentiment Score of FOMC Transcripts.ipynb
- **FinBERT:** a BERT variant fine-tuned on financial text (earnings calls, analyst reports, financial news) for domain sentiment analysis (positive/negative/neutral). prereqs: BERT, sentiment analysis
- **Load a pre-trained financial LLM:** `finbert_sa.load_model()` loads `ProsusAI/finbert` via `AutoModelForSequenceClassification`. prereqs: transformers, model loading
- **Per-text sentiment scoring:** `finbert_sa.predict_overall_sentiment(text, model)` tokenizes, runs the model, and returns an overall sentiment score. prereqs: FinBERT, inference
- **Batch sentence scoring:** `finbert_sa.process_sentences(model, sentences)` computes a score for each sentence in the FOMC transcript column. prereqs: FinBERT, loops
- **sentiment_score feature column:** store per-minute transcript sentiment scores in the DataFrame for strategy use. prereqs: DataFrame, feature engineering
- **Tokenization & attention features:** internally text is tokenized into `[CLS] ... [SEP]` sequences with `input_ids`, `attention_mask`, `token_type_ids`, zero-padded to fixed length. prereqs: tokenization, transformers
- **Model inference → logits → softmax:** feed tensors through the model under `torch.no_grad()` and convert logits to probabilities with softmax. prereqs: neural inference, softmax
- **Sentiment score from probabilities:** `sentiment_score = logits[:, 0] − logits[:, 1]` (positive-class minus negative-class probability) captures strength, not just label. prereqs: probabilities, arrays
- **Positive / negative / neutral labels:** `argmax` over the 3-class output maps each sentence to a sentiment label dictionary. prereqs: classification, argmax
- **Persisting scored data:** save the frame with scores to `fomc_sentiment_score_spy_ohlc_jan22_to_jul24.csv`. prereqs: CSV export
---
## MODULE: Sentiment Analysis Using Audio Data
### LESSON: Speech to Text.ipynb
- **Speech-to-text / transcription:** converting spoken audio into written text so it can be fed to sentiment models. prereqs: audio, text
- **OpenAI Whisper:** a powerful open speech-recognition model for transcribing audio. prereqs: ASR, audio files
- **Audio model sizes:** `tiny`, `base`, `small`, `medium`, `large` — bigger = more accurate but more compute; here `base` balances accuracy/performance. prereqs: model scale, compute
- **Loading a Whisper model:** `whisper.load_model("base")` downloads/loads the pretrained weights. prereqs: whisper, model loading
- **Transcribing a file:** `model.transcribe(audio_file_name)` (e.g. `amazon_earnings_call_q2_2024.wav`) returns a dict; `result['text']` holds the transcript. prereqs: whisper, .wav/audio
- **Supported audio formats:** m4a, mp3, webm, mp4, mpga, wav, mpeg — convert unsupported files first. prereqs: audio codecs
- **Transcript → sentiment workflow:** the generated earnings-call transcript feeds into FinBERT sentiment analysis. prereqs: transcription, FinBERT
---
## MODULE: Trade FOMC Meeting Using Sentiment Score
### LESSON: Trading Strategy Based on Sentiment Score Threshold.ipynb
- **Rolling / expanding sentiment score:** `video['sentiment_score'].expanding().mean()` accumulates the running mean of minute-level scores up to the current minute. prereqs: pandas expanding, mean
- **Sentiment score threshold:** use `sentiment_score_threshold = 0.1`; long when the rolling score exceeds +0.1, short when below −0.1. prereqs: thresholds, sentiment signals
- **Position state tracking:** `current_position` = 1 (long), −1 (short), 0 (flat) drives the event loop. prereqs: state variables
- **Entry rules:** open long/short when flat and the rolling score crosses the threshold; skip entry on the final minute. prereqs: conditional logic, trading
- **Exit rules:** close a held position when the opposite threshold is crossed or at the meeting's last minute. prereqs: exit logic, event handling
- **trade_sheet ledger:** records Position, Entry Datetime, Entry Price, Exit Datetime, Exit Price per trade. prereqs: tabular data, trade recording
- **Trade P&L:** `pnl = Position × (Exit Price − Entry Price)` yields per-trade profit/loss. prereqs: arithmetic, position sizing
- **Trade-level analytics (`trade_analytics`):** total PnL, number of trades, winners/losers, win & loss %, average PnL per winner/loser, average holding time. prereqs: statistics, trades
- **Signal column update (`update_signal_column`):** copies each trade's position onto the full minute-level SPY series between entry and exit timestamps. prereqs: datetime range slicing, signals
- **Strategy returns:** `strategy_returns = signal.shift(1) × close.pct_change()` (lagged signal × price returns). prereqs: pct_change, lag, returns
- **Equity curve / cumulative returns:** `(strategy_returns + 1).cumprod()` plotted. prereqs: compounding
- **CAGR:** compound annual growth rate annualized from cumulative returns and trading-candle count. prereqs: annualization, growth rate
- **Sharpe ratio:** annualized `(mean strategy return − daily risk-free) / std × sqrt(days)`, risk-free 2%. prereqs: Sharpe, risk-free rate
- **Maximum drawdown:** deepest peak-to-trough decline of the equity curve, plotted and reported. prereqs: equity curve, drawdown
- **Backtesting:** replaying historical sentiment vs price to evaluate a strategy's performance (here Sharpe ≈ 0.96, max DD ≈ 1.08%). prereqs: strategy, performance metrics
---
## MODULE: Strategy Variations to Trade the FOMC Meeting
### LESSON: Trading Strategy With Sentiment Score and Price Trend.ipynb
- **Price trend via moving averages:** `minute_data.close.rolling(window=9).mean()` → `mva9` (short) and window 21 → `mva21` (long). prereqs: moving average, pandas rolling
- **Trend condition:** `mva9 > mva21` signals an upward trend, `mva9 < mva21` a downward trend. prereqs: moving averages, trend
- **Combined sentiment + trend entry:** long only when rolling sentiment > 0.1 AND `mva9 > mva21`; short when rolling sentiment < −0.1 AND `mva9 < mva21`. prereqs: AND logic, sentiment signals, moving averages
- **Combined exit:** opposite thresholds with opposite trend, or last meeting minute. prereqs: exit logic, combined conditions
- **Backtest + analytics:** same `trade_analytics`, `update_signal_column`, `get_performance_metrics` flow (net PnL negative, Sharpe ≈ −2.33). prereqs: backtesting, performance metrics
### LESSON: Trading Strategy Post FOMC Meeting and Price Trend.ipynb
- **Post-report entry:** enter only after the entire FOMC report is released, not during the live meeting. prereqs: event timing
- **Daily FOMC sentiment score:** `daily_sentiment_score_FOMC_Transcript.csv` holds one sentiment score per full report. prereqs: sentiment score, daily aggregation
- **Sentiment + trend post-report strategy:** long when report sentiment > 0 AND `mva9 > mva21`; short when sentiment < 0 AND `mva9 < mva21`. prereqs: moving averages, sentiment threshold
- **End-of-day (EOD) exit:** positions held until the day's last minute bar (`minute_data.loc[str(i)[:10]][-2:-1]`). prereqs: intraday bars, EOD
- **Trade analytics & performance:** same functions; Sharpe ≈ −4.75, max DD ≈ 6.03% — no improvement over the live strategy. prereqs: trade analytics, performance metrics
### LESSON: Trading Strategy Entry Post Report.ipynb
- **Sentiment-only post-report entry:** long when the daily report sentiment > 0, short when < 0, regardless of price trend. prereqs: sentiment score, threshold
- **EOD holding:** enter immediately after the report, exit at the last candle of the day. prereqs: intraday bars, EOD
- **Total pnl / winners / losers:** trade analytics on the sentiment-only variant (Total pnl ≈ 5.08, Win 55.56%). prereqs: trade analytics
- **Performance metrics:** Sharpe ≈ 0.35, max DD ≈ 8.23% — still no improvement vs including the price trend. prereqs: backtesting metrics
### LESSON: Trading Strategy Based on Rolling Text.ipynb
- **Rolling text construction:** `fomc_data.groupby(by_date)['text'].apply(lambda x: x.apply(lambda y: y+' ').cumsum().str.strip())` accumulates all transcript text spoken up to each minute. prereqs: groupby, cumsum, string concat
- **Sentiment of rolling text:** run `finbert_sa.process_sentences` on the `text_rolling` column to get `rolling_sentiment_score` from the cumulative transcript. prereqs: FinBERT, rolling text
- **Rolling-text threshold strategy:** long when rolling text sentiment > 0.1, short when < −0.1; positions closed / not opened at the last minute. prereqs: thresholds, sentiment signals
- **Trade & performance analytics:** same helpers; Sharpe ≈ 0.32, max DD ≈ 1.11% — slightly worse than the rolling-score variant. prereqs: trade analytics, performance metrics
- **Comparison across variants:** rolling-score threshold (best), rolling-text, price-trend combos, and post-report EOD variants are contrasted to see what improves performance. prereqs: backtesting, comparative analysis
---
## MODULE: data_modules (Supporting Code)
### LESSON: finbert_sa.py
- **FinBERT loading helper:** `load_model()` returns `AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert', num_labels=3)`. prereqs: transformers, FinBERT
- **AutoTokenizer:** `AutoTokenizer.from_pretrained('bert-base-uncased')` encodes text to token IDs for the model. prereqs: tokenizers, BERT
- **Sentence tokenization (nltk):** `sent_tokenize` splits text into sentences, each scored independently. prereqs: nltk, sentence segmentation
- **Batching:** a `chunks(l, n)` generator processes sentences in small batches for efficient inference. prereqs: generators, batching
- **convert_examples_to_features:** tokenize → add `[CLS]`/`[SEP]` → `input_ids`, `attention_mask`, `token_type_ids` → zero-pad to `max_seq_length`. prereqs: tokenization, padding
- **softmax over logits:** converts the model's raw 3-class outputs into probabilities. prereqs: softmax, logits
- **Sentiment score = pos-minus-neg probability:** `logits[:,0] − logits[:,1]` gives a continuous score instead of a hard label. prereqs: probability arrays
- **predict_overall_sentiment:** mean of per-sentence scores = the text's overall sentiment score. prereqs: mean, sentence scores
- **process_sentences:** vectorized scoring of full series with a progress bar via tqdm. prereqs: loops, numpy, tqdm
### LESSON: trade_fed_utils.py
- **trade_analytics:** computes total PnL, trade count, winners/losers, win & loss %, average per-trade PnL, and average holding time from a `trade_sheet`. prereqs: statistics, trades
- **update_signal_column:** maps each trade's entry/exit window and position onto a minute-level signal column. prereqs: datetime slicing, signal mapping
- **get_performance_metrics:** returns equity curve, CAGR, Sharpe ratio, and maximum drawdown, with drawdown filling. prereqs: performance metrics, drawdown, Sharpe


====================
Trading-Using-Options-Sentiment-Indicators
====================

# Trading Using Options Sentiment Indicators — Concept Inventory
> This course has **no notebooks**. Content lives in an ebook (`TUOSI-ebook.pdf`) plus three standalone Python strategy modules (`.py`). The accompanying `.txt` files are readable copies of each `.py`.
Course flow (ebook TOC): sentiment trading intro → market sentiment → greed/fear & bubbles → breadth measures (TRIN) → TRIN strategy → option trading measures (volume/open interest/PCR) → PCR strategy → volatility measures (hist vol/implied vol/VIX) → VIX strategy → risks → conclusion.
---
## eBook — `TUOSI-ebook.pdf` (course theory)
### 1. Introduction to Sentiment Trading
- **Sentiment / fear–greed driven markets** — markets priced by intrinsic value + market sentiment; overvaluation from greed, undervaluation from fear; the 2008 real-estate bubble as the canonical greed→bubble→fear cycle. *Prereq: market mechanics.
- **Contrarian trading** — profit by taking positions against crowd behavior on exploitable mispricing. *Prereq: sentiment signals.
- **Algorithmic trading** — pre-defined rules place orders automatically (no per-trade discretion). *Prereq: Python, order logic.
### 2. Market Sentiment
- **Market sentiment definition** — investors' perception of current/future price; bullish (buying, prices rise) vs bearish (selling, prices fall).
- **Volume as sentiment strength gauge** — high volatility + high volume = strong sentiment; high vol + low volume = weak.
- **Mispricing & intrinsic value** — separating drift caused by fundamentals vs. sentiment; the target of sentiment trading.
### 3. Breadth Measures
- **Market breadth** — number/volume of advancing vs declining stocks in an index; breadth & volume gauge sentiment strength and direction.
- **Importance of volume** — volume spikes mark support/resistance and bull/bear strength.
- **High/Low measures** — today's/52-wk/all-time highs/lows; range = stock's spread; trades near highs = bullish, near lows = bearish.
- **New High/Low ratio** — (today's new highs)/(today's new lows); >2 strong new high, <0.5 strong new low; divergences flag unsustainable trends; derived % new highs/lows, % high-low, cumulative new high-low line.
- **Advance/Decline ratio & line** — # advancing / # declining; AD line = cumulative (adv−decl); AD ratio 1.25–2 = bullish band.
- **TRIN (Arms Index / Short-Term TRading INdex)** — `TRIN = (advancing stocks/declining stocks) / (advancing vol / declining vol)`; spikes = bearish/sell days, troughs = bullish/buy days; >1 bearish, <1 bullish, ~1 neutral.
- **Making TRIN trade-able** — log transform to de-lopside the ratio; Bollinger bands (moving avg ± k·σ, usually 2σ) to detect oversold/overbought; market thrust component to resolve volume contradictions.
- *Prereq:* stocks/index breadth data, moving averages, standard deviation, Bollinger bands.
### 4. TRIN Strategy
- **Log-TRIN + SMA(22)** normalization, then **Bollinger bands** (k=1.5σ) and stop-loss bands (additional l=2σ).
- **Contrarian entry** — TRIN crossing the **Upper Bollinger Band** = oversold → **BUY** S&P futures; crossing the **Lower Bollinger Band** = overbought → **SELL**.
- **Exit (take profit)** — TRIN reverts to the moving average → close the open position.
- **Two stop-loss exits** — (1) TRIN crosses the stop-loss band (further away than entry), (2) absolute S&P 500 move of 25 points → book loss.
- **Single-position discipline** — no new position while one is open; flag matrix for open/close tracking.
- *Prereq:* TRIN indicator, Bollinger bands, stop-loss/take-profit order types, futures contracts, flag state machine.
### 5. Option Trading Measures — Volume & Open Interest
- **Options basics** — call/put contracts, long (right to buy/sell) vs short (obligation), strike price, premium, exercise date; unbounded long payoff vs capped short premium.
- **Volume** — number of option contracts traded (not direction-specific); each option contract has a buyer and seller.
- **Open Interest (OI)** — contracts traded but not yet liquidated; OI increases / unchanged / decreases depending on new vs offsetting positions and delivery.
- *Prereq:* options contract mechanics, order execution.
### 6. Put Call Ratio (PCR)
- **PCR definition** — (traded volume of put options)/(traded volume of call options); >1 = bearish (more puts), <1 = bullish (more calls).
- **Three PCR types** — Equity PCR, Index PCR, Total PCR (equity + index put volume / equity + index call volume).
- **PCR interpretation as sentiment** — extreme high PCR = oversold (favor long), extreme low PCR = overbought (favor short); use short-term moving-average trends.
- *Prereq:* volume, open interest, calls/pures, sentiment interpretation.
### 7. PCR Strategy
- **SMA(20)** of PCR + **Bollinger bands** (k=1σ) and stop-loss bands (l=1σ more).
- **Contrarian entry** — PCR crossing the **Upper Band** = oversold → **BUY**; crossing **Lower Band** = overbought → **SELL**.
- **Exits** — reversion to moving average = mechanical take profit; stop-loss band or absolute S&P move (5 points) = exit at loss.
- Same single-position / flag discipline as TRIN.
- *Prereq:* PCR indicator, Bollinger bands, order types, futures.
### 8. Volatility Measures — Historical & Implied
- **Volatility as dispersion** — variance = avg squared deviation from mean; standard deviation = sqrt(variance); annualized historical vol = daily σ × √(trading days/yr ~254).
- **Historical volatility** — annualized std of past returns; an imperfect guide to future move.
- **Moneyness** — in / at / out-of-the-money for calls vs puts.
- **Option price = intrinsic + extrinsic value**; **Black-Scholes-Merton** 5 inputs (S, X, t, r, σ) price the option.
- **Implied volatility** — back out σ from market option premiums (all else fixed & the only unknown being vol); forward-looking, reflects demand/supply and time-to-expiry.
- *Prereq:* underlying option pricing, standard deviation, BSM.
### 9. VIX (Volatility Index)
- **VIX definition** — CBOE's implied-volatility estimate for S&P 500 index options over next ~30 days; from a kernel-smoothed variance of first two months' option premiums (outside money); σ × 100.
- **Reading VIX** — quoted in % (e.g. 20 = expected ±20% annualized at 1σ); high VIX = high uncertainty/fear/falls; low VIX = calm sure; >30 high-fear, <20 calm.
- **VIX variants & instruments** — VXN (NASD), VXD (DJIA), India VIX, etc.; VIX futures/options; "fear/index".
- *Prereq: implied volatility, options pricing, sqrt rule.
### 10. VIX Strategy
- **Threshold trigger** — VIX crosses threshold (e.g. **22**) → oversold/fear → **BUY** S&P futures.
- **Take-profit** — sell when futures rise **5%** above the buy price.
- **Stop-loss** — sell when futures fall **5%** below buy price (absolute value).
- **Recurring structure of the contrarian no-position-while-open logic, flag-based** (buy_flag/sell_flag 0/1).
- *Prereq:* VIX indicator, take-profit/stop-loss, futures.
### 11. Risks in Trading
- **Risk itself** — uncertainty of realized vs expected return; std of returns as measure; conservative vs aggressive investors.
- **Specific/unsystematic risk** — company/sector-specific (fire, strike, etc.); diversified away (MPT ~30 names).
- **Systematic/market risk** — affects entire market (2008 crisis); not diversifiable; measured by **Beta** (β=1 market risk).
- **Systemic risk** — failure of a "too-big/too-interconnected" firm triggers sector/market collapse (Lehman→AIG).
- **Price risk** — loss from price fall; reduced by **hedging** (futures price lock; natural long → sell futures).
- **Execution risk** — order fails to execute at desired price (slippage); market vs limit orders trade-off.
- **Model risk** — errors in your own trading model's inputs/complexity; mitigate via model averaging, sensitivity.
- *Prereq:* risk/return, diversification, hedging, order types.
### 12. Conclusion & extension
- Use **multiple sentiment indicators** with the fundamentals/rationality, not in isolation; combine TRIN + PCR + VIX + breadth signals; extend with more indicators (polling, margin debt, short interest, new equity issuance). *Prereq:* all indicator modules above.
---
## Python Strategy Modules
### 1. `Breadth Measures/TRIN.py` (also `TRIN.txt`)
- **TRIN computation from breadth data** — merges advancing/declining stock counts & volumes, forms [(adv/decl) / (adv_vol/decl_vol)], applies **log transform**, and joins S&P 500 futures 'Last' as the trade instrument.
- **Bollinger/stop-loss bands** — SMA(22) of TRIN; lower/upper Bollinger bands (k=1.5σ); stop-loss bands (l=2σ); custom `variance_calculator` (rolling squared-deviation with (n-1)).
- **Trade state machine** — UBB-crossover → **BUY**, LBB-crossover → **SELL**; take-profit on reversion to cleaned moving average (mAvg crossover); exit on stop-loss bands or absolute SL (25 S&P points).
- **Trade-report artifacts** — placed orders, cumulative PnL/cash, per-trade cause/stoploss columns; `.xlsx` output; plots TRIN with bands.
- *Prereq:* TRIN strategy theory, pandas rolling windows, flags.
### 2. `Option Trading Measures/PCR.py` (also `PCR.txt`)
- **PCR input & bands** — reads S&P PUT-CALL RATIO series + S&P futures; SMA(20); Bollinger bands (k=1σ), stop-loss bands (l=1σ); custom variance solver.
- **Trade machine** — UBB-crossover → **BUY**, LBB-crossover → **SELL**; close at moving-average reversion (TP) or on band/absolute SL (5 S&P points); single-active-position flag logic.
- **Account/analytics output** — placed orders, per-trade PnL, mark-to-market, cumulative account, `.xlsx` export, PCR/Band plot.
- *Prereq:* PCR strategy, Bollinger, pandas.
### 3. `Volatility Measures/VIX.py` (also `VIX.txt`)
- **VIX threshold entry** — reads VIX close series + S&P futures; when VIX ≥ threshold (22) → **BUY** (interpreted as fear/oversold). *Prereq:* VIX indicator, futures.
- **Take-profit / sticky-loss** — sell when futures rise **5%** (TP) or fall **5%** (SL) from buy price; c_1/c_2 multiplier by.
- **Position flags & accounting** — buy_flag/sell_flag state; mark-to-market, cumulative account, per-trade profit, `.xlsx` output, PnL plot. *Prereq:* VIX strategy, order types.
## Non-code support
- `ReadMe.html`, `Folder Structure...html` — setup/execution instructions.
- Breadth/option/volatility measure `.csv` input datasets (`advancing.csv`, `declining.csv`, `adv_vol.csv`, `dec_vol.csv`, `local_data.csv`, `local_future.csv`, `VIX_data.csv`, `Data1.csv`).
## Order of concept prerequisites (flow)
sentiment/market breadth → TRIN → TRIN strategy; then option-basics → volume/OI → PCR → PCR strategy; then volatility → historical/implied vol → VIX → VIX strategy; cap with risks; use multiple indicators in combination.


====================
Trading-with-ML-Classification-and-SVM
====================

# Trading with Machine Learning: Classification and SVM — Concept Inventory
> Scope: intraday classification trading strategy using a tuned Support Vector Machine (SVC) on 1-minute ICICI Bank futures OHLCV data.
> Modules/notebooks enumerated: **1** (`Trading Strategy Classification.ipynb`) | Data: `data_modules/ICICI Minute Data.csv` | Module files: `ReadMe.html`, `Folder Structure and How to Run Code Files.html`
> Core workflow: import data → create indicators → calculate returns → train/test split → build signal targets → hyperparameter tuning → SVM → predict signals → analyse performance → plot results.
---
## Module: Prediction and Strategy
### 1. `Trading Strategy Classification.ipynb`
Complete supervised-classification trading strategy built around an SVM classifier.
**Concepts (with prerequisites):**
- **Data loading & cleaning**
 - **Reading OHLCV data** — `pd.read_csv('...ICICI Minute Data.csv')`; 1-minute bars for two days of a futures instrument.
 - *Prereq:* CSV import, OHLCV bars.
 - **Liquidity filtering** — dropping rows with zero traded volume (avoids training on illiquid moves).
 - *Prereq:* volume/liquidity awareness.
 - **Datetime index** — converting `Time` to pandas datetime and setting as index; needed to detect market close (~15:29) for squaring-off positions.
 - *Prereq:* datetime parsing, index setting.
- **Feature engineering (indicators)**
 - **RSI (Relative Strength Indicator)** — computed via `talib` on shifted Close with `timeperiod=n`; uses prior n minutes' close prices (look-ahead avoidance).
 - *Prereq:* technical indicators, RSI definition, shifting/lagging.
 - **SMA (Simple Moving Average)** — `Close.shift(1).rolling(n).mean()` over a 10-minute window.
 - *Prereq:* moving average, rolling windows.
 - **Correlation coefficient** — rolling correlation between Close and SMA; trimmed to `[-1, 1]` because correlation is bounded.
 - *Prereq:* correlation bounds, rolling statistics.
 - **SAR (Stop and Reverse)** — computed on High/Low (sensitive to new highs/lows) with acceleration and max-step parameters (0.2, 0.2).
 - *Prereq:* Parabolic SAR indicator, support/resistance.
 - **ADX (Andrews/Directional Index)** — here computed on High/Low/Open (recent price information) rather than Close.
 - *Prereq:* ADX indicator mechanics.
 - **Previous-minute OHLC** — `Prev_High`, `Prev_Low`, `Prev_Close` via `shift(1)` to convey recent volatility.
 - *Prereq:* lags/look-ahead bias.
 - **Open-price differences** — `OO = Open − Open.shift(1)` (minute-over-minute open change) and `OC = Open − Prev_Close` (overnight/intraday gap).
 - *Prereq:* gap/change features.
 - **All indicators use past data** — `shift(1)` on the source series to avoid look-ahead leakage into the target.
 - *Prereq:* temporal causality, data leakage.
- **Returns and target**
 - **Future return target** — `Fut_Ret = (Open.shift(−1) − Open)/Open`; the one-period-ahead open-to-open return the model must predict.
 - *Prereq:* returns, forward-looking targets.
 - **Lag-return columns** — `return1 … returnN` via `Fut_Ret.shift(i)`, capturing the trend of past n periods.
 - *Prereq:* feature lags, rolling trend.
- **Output signal encoding (classification target)** — quantile-based binning of `Fut_Ret` into three classes: `1` (Buy, top tercile), `−1` (Sell, bottom tercile), `0` (hold, middle); thresholds from train data quantiles (0.66 / 0.34).
 - *Prereq:* classification, multiclass labels, quantiles.
- **Market-close squaring-off** — zeroing `Signal` and `Fut_Ret` at the 15: closing minute so the intraday strategy holds no positions overnight.
 - *Prereq:* intraday trading, position flattening.
- **Feature/target construction** — dropping raw columns (Close, Signal, High, Low, Volume, Fut_Ret) and setting `X` (features) and `y = Signal` (labels).
 - *Prereq:* features vs target, X/y.
- **Hyperparameter tuning**
 - **Pipeline** — `[('scaler', StandardScaler()), ('svc', SVC())]` chains scaling before model fitting to neutralize per-feature weight differences.
 - *Prereq:* pipelines, feature scaling.
 - **Hyperparameters of SVC** — `C` (regularization costs), `gamma` (kernel coefficient), and `kernel`; tuned over a tested grid (`rbf` kernel, several C and gamma values).
 - *Prereq:* SVM hyperparameters, kernel, regularization.
 - **RandomizedSearchCV + TimeSeriesSplit** — random hyperparameter search with time-ordered sequential CV splits (n_splits=2) to respect time order and avoid overfitting.
 - *Prereq:* hyperparameter search, time-series cross-validation.
- **Best-parameter selection** — `rcv.best_params_` yields optimal `C`, `gamma`, `kernel` for a newly instantiated `SVC(...)`.
 - *Prereq:* model selection.
- **Training & prediction**
 - **Standardisation before fit/predict** — `StandardScaler().fit_transform(train)` for training; `ss1.transform(test)` reuses the fit (no leakage) before prediction.
 - *Prereq:* scaling discipline.
 - **Prediction and saving** — `cls.predict(...)` on train and test; storing predictions into `Pred_Signal` column.
 - *Prereq:* model inference, prediction arrays.
 - **Strategy returns** — `Ret1 = Fut_Ret × Pred_Signal` (position-timed return).
 - *Prereq:* strategy/position sizing, returns.
- **Performance evaluation**
 - **Accuracy** — overall fraction of correct signal labels.
 - *Prereq:* classification accuracy.
 - **Confusion matrix** — table of true vs predicted classes; here 3×3 for classes {−1,0,1}, showing per-class true/false hits.
 - *Prereq:* classification, confusion matrix, class imbalance.
 - **Classification report — precision, recall, F-score, support** — per-class precision = tp/(tp+fp), recall = tp/(tp+fn), F-score (harmonic mean), support (class counts).
 - *Prereq:* precision, recall, F-measure.
 - **Drawdown** — cumulative returns, running max, and percentage drawdown (decline from peak); max drawdown reported.
 - *Prereq:* drawdown / peak-to-trough decline.
 - **Annualised Sharpe ratio** — risk-adjusted return scaled to annualised frequency using per-year minute count (`sqrt(252*6.25*60)`).
 - *Prereq:* Sharpe ratio, risk-free annualisation.
 - **Cumulative-return and benchmark comparison plot** — comparing strategy returns vs market returns over the test window.
 - *Prereq:* cumulative returns, buy-and-hold benchmark.
---
## Trading-with-ML-Classification-and-SVM — Section-based course structure
# — Trading with Machine Learning: Classification and SVM — Concept Inventory
**Track:** 4 — Machine Learning & Deep Learning in Trading (Beginners)
**Media note:** PDFs + resources zip only (no mp4s in folder).
**Overlaps with D: notebooks:** heavy — the D: side has notebook-based `Trading-with-ML-Classification-and-SVM` extraction (binary/multi-class classification, SVM, prediction/strategy notebooks, and paper/live templates). This course carries the corresponding maths/measurement PDFs (decision boundary, probability, performance measures, one-hot/softmax, SVM maths).
## COURSE
Using classification to build trading signals, from binary to multiclass: probability foundations; decision boundaries, cost functions, gradient descent; performance measures for classifiers; encoding categorical targets (one-hot, softmax) and class probability outputs; and **support vector machines** (SVM) from hard-margin objective to soft-margin and kernel-based nonlinear classifiers. Ends with a complete prediction-and-strategy pipeline plus live-trading (IBridgePy) template.
## Course Prerequisite Map
- **Section 1 Introduction requires:** Python + installing scikit-learn (SVC, StandardScaler, RandomizedSearchCV, pipeline). No ML prereq strictly.
- **Section 2 Binary Classification requires:** Section 1 env; core terms introduced in the decision-boundary PDF (decision boundary, cost, gradient descent).
- **Section 3 Multiclass requires:** Section 2 + Probability Concepts 1 & 2 (conditional/joint prob, total-probability rule, `.predict_proba`), plus performance-measure/confusion-matrix knowledge.
- **Section 4 Support Vector Machine requires:** Section 2 (boundary/margin/max-margin) + linear algebra/optimization basics (for the margin maximisation maths).
- **Section 5 Prediction & Strategy requires:** Section 3 (a trained classifier producing class probabilities → prediction) + features.
- **Section 9 Paper & Live Trading requires:** Section 5 (vectorised backtest) + Python env / IBridgePy; also kindred backtesting knowledge from the Python-for-ML course.
---
### Section 1 — Introduction
- **CONCEPT:** Technical references and environment setup — install scikit-learn in your Python IDE; the core sklearn APIs used: `SVC` (support-vector classifier), `StandardScaler` (feature scaling), `RandomizedSearchCV` (randomised hyperparameter search), `pipeline` + `pandas`/`numpy`/`Talib` (technical indicators). prereqs: Python env, package install.
### Section 2 — Binary Classification
- **CONCEPT:** Decision boundary — the n-dimensional plane (hyperplane) that splits feature space into two classes; binary classification aims for the boundary that best separates the two classes. prereqs: linear algebra, two-class label.
- **CONCEPT:** Cost function — the function minimised to get the boundary that minimizes classification prediction error. prereqs: decision boundary concept.
- **CONCEPT:** Gradient descent — iterative process used to minimise the cost function (partial derivatives, stepping along the gradient) to refine model parameters toward the optimal boundary. prereqs: calculus derivatives, cost function.
### Section 3 — Multiclass Classification
- **CONCEPT:** Probability fundamentals (Pt.1) — terms (experiment, event, sample space), calculating probability, two defining properties; unconditional/marginal vs conditional vs joint probability; addition and multiplication rules. prereqs: basic counting/probability.
- **CONCEPT:** Probability fused (Pt. 2) — **Total probability rule** (unconditional P(A) from conditional terms of mutually exclusive/exhaustive events), **expected value**, and `.predict_proba()` as the classifier-giving-per-class probabilities. prereqs: Pt.1 concepts + binary classifier output.
- **CONCEPT:** Performance measures in classification — **confusion matrix** (TP/FP/FN/TN), **accuracy**, **precision**, **recall**, **F-measure/F1** — quantifying a classifier's predictive capability. prereqs: Section 2 model + multiclass outputs.
- **CONCEPT:** Categorical feature encoding — one-hot encoding for categorical (non-numeric) features so a vector classifier can consume them. prereqs: feature extraction, categorical data.
- **CONCEPT:** Softmax regression — the multiclass generalisation of logistic regression; transforms a per-class logit/probabilities vector into ∝ probabilities over n classes. prereqs: one-hot encoding + Section 2 probability outputs.
### Section 4 — Support Vector Machine
- **CONCEPT:** Max-margin / hyperplane selection — the SVM picks the decision boundary by **maximising the distance between the two nearest support points of each class** (margin = max distance to nearest training points). prereqs: Section 2 boundary concepts + Euclidean geometry.
- **CONCEPT:** Maths behind SVM — maximise margin subject to constraints (hard-margin QP); then generalise to **soft-margin** (allow some misclassification via slack) and **nonlinear models** (kernel trick → transform feature space) for inseparable data. prereqs: linear algebra, convex optimisation, Section 2.
### Section 5 — Prediction and Strategy
- **CONCEPT:** Section flow — turns the fitted classifier's class-probability output into trading predictions, maps to a long/flat/short strategy, and backtests the resulting decision vector (vectorised backtesting). prereqs: Sections 3 & 4 predictions + returns data.
- **CONCEPT:** Strategy construction from predicted classes — execute long/short/flat based on the predicted direction class. prereqs: targeting from ML-for-Finance course.
### Section 9 — Paper and Live Trading
- **CONCEPT:** Template for live trading documentation — modifying the Jupyter-backtested SVM strategy for **IBridgePy** live trading on Interactive Brokers / TD Ameritrade / Robinhood (virtual env, packages installed per ReadMe, IBridgePy version binding). prereqs: Section 5 strategy + IBridgePy familiarity.
- **CONCEPT:** Live-trading determinism — a script run by IBridgePy on a cadence to place orders based on the trained SVM model. prereqs: backtesting (Python-for-ML course).
### Section 11 — Downloadable Resources
- **CONCEPT:** Full course resources (`...Classification-and-SVM-Resources.zip`) — notebooks + data for the classification/SVM pipeline. prereqs: all sections.


====================
Trading-with-Machine-Learning-Regression
====================

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


====================
Unsupervised-Learning-in-Trading
====================

# Unsupervised Learning in Trading — Concept Inventory
**Totals:** 14 modules, 17 notebooks + 2 support Python modules
End-to-end unsupervised learning workflow for trading: covariance/PCA fundamentals → feature selection (stationarity, correlation) → scaling (min-max vs standard) → k-means clustering + choosing cluster count → cluster analysis for signal generation (hit ratio, skewness) → DBSCAN (density-based, outlier-robust) → pairs trading (feature engineering, DBSCAN pairs, cointegration test) → compiled "putting it all together" + a capstone project.
---
## Module: Introduction to Principal Component Analysis
**Notebook:** `Variance and Covariance.ipynb`
### Prerequisites
- Basic statistics; mean, standard deviation
- **PCA** (conceptual) — finds the "best" line maximizing the spread of points
### Concepts
- **Variance (σ²):** how far values are from the mean: `Σ(xᵢ − x̄)² / (n−1)`; squaring gives equal weight to points above/below the mean and more weight to farther points.
- **Covariance:** direction of co-movement of two features; positive when they move together, negative otherwise: `Σ(xᵢ − x̄)(yᵢ − ȳ) / (n−1)`.
- **Covariance matrix (via pandas `.cov(ddof=1)`):** a square matrix where **diagonal = variances**, **off-diagonal = covariances**; shape n×n for n columns. This is the core object PCA is built on.
- Read RSI/ADX data to compute variance, covariance and the covariance matrix as a foundation for eigenvalues/eigenvectors.
---
## Module: Maths Behind Principal Component Analysis
**Notebooks:** `Maths Behind PCA.ipynb`, `PCA Example.ipynb`
### Prerequisites
- Variance and covariance
- **Eigenvalues and eigenvectors** — of the covariance matrix
- **PCA** — unsupervised dimensionality reduction
### Concepts (Maths Behind PCA.ipynb)
- **PCA as dimension reduction:** projects data onto directions (components) that maximize variance.
- **Eigen-decomposition:** `numpy.linalg.eig(cov_matrix)` returns eigenvalues and eigenvectors; the eigenvector of the **largest eigenvalue** is the **first principal component**.
- **Orthogonality:** principal components are perpendicular; spread is largest along PC1.
- **De-meaning:** subtract the mean so eigenvectors pass through the origin; project de-meaned data onto PC1 via dot product.
- **1D reduction:** `data_shifted.dot(pc1)` collapses data onto one axis.
- **sklearn implementation:** `PCA().fit(data)`, `.components_` (eigenvectors), `.explained_variance_` (eigenvalues), `.fit_transform(data)`; the sign of eigenvectors is arbitrary — magnitude (variance captured) is what matters.
- **3D→2D example** (PCA Example.ipynb): generate 100 3-D points with noise+rotation; `PCA(n_components=2)`; verify reduced shape (100,2) retains the data's structure (semi-circular distribution), showing PCA keeps information while lowering dimension.
---
## Module: Principal Component Analysis (choosing features)
**Notebook:** `Choosing the Number of Features in PCA.ipynb`
### Prerequisites
- PCA mechanics and eigenvalues/eigenvectors
- Explained variance ratio
### Concepts
- **Returns data for 473 stocks** (365 trading days), transposed to date×stock returns matrix.
- **explained_variance_ratio_:** proportion of total variance explained by each principal component (e.g., PC1 ≈ 0.443).
- **Selecting components by cumulative variance:** plot cumulative `explained_variance_ratio_` vs number of features; pick the number achieving a target (e.g., 90%) — here ~81 of 473 features.
- **n_components shortcut:** if `n_components` is between 0 and 1 it is read as proportion of variance; if an integer >1 it is the number of components — both routes give the same result (81).
- **Takeaway:** 473-dimensional data reduced to 81 dimensions at 90% explained variance.
---
## Module: Feature Selection (for k-means)
**Notebook:** `Feature Selection.ipynb`
### Prerequisites
- **Stationarity** of a time series
- **Correlation** between features
- **k-means** requirements for input features
### Concepts
- **Why feature selection for clustering:** k-means inputs must be **stationary** (value not dependent on time) and **not highly correlated** (correlated features overweight a common signal).
- **Features produced from 15-minute Apple data:** 3.75-hour return, 14-day return, 1-day SMA, 1-day & 14-day volatility, RSI, ADX, ATR.
- **Stationarity test:** **ADF test** (`statsmodels.tsa.stattools.adfuller`); p-value < 0.05 ⇒ stationary; non-stationary features (SMA, Volatility14) are dropped.
- **Correlation check:** absolute correlation matrix; drop any feature pair with |corr| > 0.7 (ATR correlative with Volatility) — remove ATR to keep the most features.
- **Outcome:** a clean stationary, low-correlation feature set (ret375_hours, ret14_days, Volatility, RSI, ADX) for k-means.
---
## Module: Scaling the Data
**Notebook:** `Scaling the Data.ipynb`
### Prerequisites
- k-means sensitivity to feature scale
- RSI/volatility features of different ranges
### Concepts
- **Why scaling:** with un-scaled features of different ranges (RSI 0–100 vs volatility 0–1.4) k-means effectively ignores the smaller-range feature; distance to centroid is dominated by scale.
- **Min-max scaling:** `x_scaled = (x − x_min)/(x_max − x_min)` → range 0–1, via `sklearn.preprocessing.MinMaxScaler`.
- **Standard scaling:** `x_scaled = (x − μ)/σ` → mean 0, std 1, via `StandardScaler`; assumes normality; range is not fixed.
- **Tradeoff:** StandardScaler can still overweight features with extreme tails; MinMaxScaler is preferred when the feature range is known (RSI) or estimable (volatility) — the course uses **MinMaxScaler** going forward.
---
## Module: K-Means for Financial Data
**Notebook:** `Applying K-Means to Create Clusters.ipynb`
### Prerequisites
- **k-means** algorithm (centroids, iterative reassignment)
- Technical indicators: **RSI**, **ADX**, **volatility**
### Concepts
- **Feature computation with TA-Lib:** RSI (`ta.RSI`), ADX (`ta.ADX`), and volatility from rolling std of returns; for 15-min data the 1-day period = 6.5×4 ≈ 26 periods.
- **k-means model:** `sklearn.cluster.KMeans(n_clusters, random_state)`; fit on features (RSI+ADX); access centroids via `model.cluster_centers_`.
- **Assigning points:** `model.predict(features)` gives cluster labels; scatter plot with centroids shows cluster structure.
- **Reusable function `plot_kmeans_clusters`:** fits k-means and plots clusters for 2 features (used across later modules).
- **Observation that motivates scaling:** RSI+volatility clusters look distorted because of scale mismatch — leads into the scaling module.
---
## Module: Selecting Clusters for K-Means
**Notebook:** `Choosing the Number of Clusters.ipynb`
### Prerequisites
- k-means (needs pre-chosen `n_clusters`)
- WCSS / inertia concept
- Min-max scaled features
### Concepts
- **WCSS / inertia:** within-cluster sum of squares; `KMeans.inertia_`.
- **Elbow curve:** plot WCSS vs number of clusters (1–30); WCSS declines monotonically.
- **Change in WCSS plot:** find where the reduction flattens/becomes ~constant (here ~10–12).
- **Percentage-change rule:** choose the number of clusters where % change in WCSS drops below a threshold (here 4.5%) → ~11 clusters; implementable in `get_number_of_clusters(features, threshold, max_range)` (takes WCSS and threshold).
---
## Module: Analysing Clusters (Hit Ratio & Skewness)
**Notebooks:** `Cluster Analysis with Hit Ratio.ipynb`, `Strategy Analytics for Hit Ratio.ipynb`, `Cluster Analysis with Skewness.ipynb`
### Prerequisites
- k-means clustering output (train/test cluster labels)
- Future-return labeling and train/test split
- **Hit ratio** and **skewness** metrics; backtesting metrics
### Concepts (Cluster Analysis with Hit Ratio.ipynb)
- Feature pipeline: `calculate_features()` (ret375_hours, ret14_days, Volatility, Volatility14, RSI, ADX, ATR) + 15-period future returns (`fut_ret`); drop SMA & ATR.
- 75/25 train/test split; fit MinMaxScaler on train, transform both.
- Fit k-means (11 clusters) on train; assign cluster labels to test via `predict`.
- **Hit-ratio signal rule:** per cluster, compute % positive and % negative future returns; long if positive ≥55%, short if negative ≥55%, else neutral; map direction to test rows.
- **Backtest:** strategy returns = `close.pct_change() × direction.shift(1)`; cumulative returns; metrics: total returns, annualized (CAGR), max drawdown (MDD), return-to-MDD ratio via `performance_analysis()`.
- **Result:** hit-ratio strategy on Apple underperforms buy-and-hold.
### Concepts (Strategy Analytics for Hit Ratio.ipynb)
- Trade-wise log generation: `get_trades(data, close_column, signal_column)` — columns Position, Entry Time, Entry Price, Exit Time, Exit Price, PnL (PnL = Δprice × position).
- **Strategy analytics:** `get_analytics(trades)` → #long/#short/total trades, gross profit/loss, net profit, winners/losers, win %/loss %, avg profit/loss per trade.
- **pyfolio tear sheet:** `pf.create_simple_tear_sheet(strategy_returns, benchmark_rets)` for detailed trade metrics.
### Concepts (Cluster Analysis with Skewness.ipynb)
- **Skewness** of future-return distributions: histogram per cluster; negative skew = left tail, positive skew = right tail (fat tails).
- **Interpretation scale:** symmetric −0.5…0.5; moderate ±(0.5–1); high <−1 or >1.
- **Skewness signal rule:** long clusters with skewness > 1, short clusters with skewness < −1, else neutral.
- **Result:** skewness-based strategy on Apple outperforms buy-and-hold (total ~77%, return-to-MDD ~6.2) — capturing tail events works well.
---
## Module: Putting It All Together (k-means strategy)
**Notebook:** `Putting It All Together.ipynb`
### Prerequisites
### Concepts
- Reuses the module helpers: `performance_analysis, calculate_features, stationary, get_number_of_clusters, hit_ratio_analysis, skewness_analysis, get_trades, get_analytics`.
- **Full pipeline from scratch on Apple:** read 15-min data → compute features → check stationarity (drop SMA) → correlation check (drop ATR) → 75/25 split → MinMax scaling → elbow/threshold cluster count → fit k-means → `hit_ratio_analysis` and `skewness_analysis` add `direction_hit_ratio` / `direction_skewness` columns → compute & plot cumulative returns.
- **Comparison:** hit-ratio strategy poor (negative returns); skewness strategy strong (total ~56%, return-to-MDD ~4.1) — template for creating trading signals from k-means on any asset.
---
## Module: DBSCAN
**Notebook:** `K-Means Vs DBSCAN.ipynb`
### Prerequisites
- k-means (spherical clusters, pre-set clusters count)
- **DBSCAN** (density-based clustering)
### Concepts
- **DBSCAN (Density-Based Spatial Clustering of Applications with Noise):** density-based; robust to noise/outliers; separates regions of high density from low density; doesn't need a pre-defined `n_clusters`.
- **Hyperparameters:** `eps` (max distance for neighborhood) and `min_samples` (min points to consider a cluster dense); noise points given label `-1`.
- **sklearn:** `sklearn.cluster.DBSCAN(eps, min_samples).fit(data)`; `.labels_`.
- **When DBSCAN beats k-means:** non-globular/irregular clusters; varying densities; outlier detection (outliers get −1); noisy data. Both have strengths; choice depends on the problem.
---
## Module: Application of Unsupervised Learning for Pairs Trading
**Notebook:** `Feature Engineering for Pairs Trading.ipynb`
### Prerequisites
- PCA & variance selection; StandardScaler; fundamentals data
### Concepts
- **Pairs selection goal:** use unsupervised clustering to find similar stocks (e.g., same-sector banks) for pairs trading.
- **Read 473 S&P 500 returns** (`SP_500_data.csv`), `.pct_change()`.
- **Standardize returns** with `StandardScaler` so stocks are comparable.
- **PCA reduction:** reduce to the components explaining 90% variance (→ 78 components).
- **Combine fundamentals:** append `profitMargins`, `revenueGrowth`, `returnOnEquity` from `fundamentals.csv` (→ 78 + 3 = 81 features).
- **Re-standardize the combined matrix** so PC features and fundamentals are comparable; export as `SP500_principal_components.csv`.
---
## Module: Pairs Trading using Clustering Algorithms
**Notebooks:** `Create Pairs using DBSCAN.ipynb`, `Cointegration Test.ipynb`
### Prerequisites
- DBSCAN; PCA-reduced + fundamental features; t-SNE visualization; **cointegration** and ADF test
### Concepts (Create Pairs using DBSCAN.ipynb)
- DBSCAN on the 81-feature matrix (`eps=5, min_samples=3`) → 9 clusters; stocks with label −1 are noise (excluded).
- **Clusters as similarity groups:** stocks in the same cluster are similar (e.g., cluster 5 = BAC, JPM, PNC, USB — banks) and likely to form good pairs.
- **t-SNE visualization:** `sklearn.manifold.TSNE(n_components=2, learning_rate, perplexity, random_state)` reduces 81-D to 2-D to visualize clusters; grey points = noise.
- **Pair creation:** within each cluster, `itertools.combinations(cluster_stocks, 2)` → nC2 pairs; cluster sizes determine pair counts.
### Concepts (Cointegration Test.ipynb)
- **Cointegration:** two non-stationary series whose linear portfolio is stationary (even if each alone wanders) — required for mean-reversion/pairs trading.
- **Hedge ratio via OLS:** `sm.OLS(stock1, stock2)` to build portfolio = stock1 − hedge×stock2.
- **ADF test** on the portfolio, null = not stationary; reject (test stat < critical value at 10%) ⇒ cointegrated.
- **`is_coint(pair)` function:** returns True/False per pair; applied across all DBSCAN pairs; at 90% confidence ~55 cointegrated pairs selected for pairs trading.
---
## Module: Capstone Project
**Notebook:** `Capstone Project Model Solution.ipynb`
### Prerequisites
- Everything in the course; `unsup_capstone_util.py` helpers (`check_stationarity, correlation_check, get_number_of_clusters, performance_analysis`)
### Concepts
- **Reference solution template** on daily GOOG (2011–2021): train 2011–2017, backtest 2018–2021.
- **Feature set:** 5-day returns, 20-day SMA, 14/50-day volatility, RSI, ADX, ATR, Williams %R (`TA-lib`).
- **Feature engineering checks:** stationarity (drop non-stationary SMA, ATR) → correlation (drop WILLR, correlated with returns/RSI) → MinMax scaling on train, transformed test.
- **Clustering:** `get_number_of_clusters` (elbow/threshold) → k-means fit on train; label train/test observations.
- **Cluster analysis:** 5-day future returns; histogram per cluster; observe skewness.
- **Trading strategy rules:** long if skewness > 0.5, mean return > 0, and trades ≥ 22; short if skewness < −0.5, mean return < 0, and trades ≥ 22; else neutral. Trade daily based on previous day's cluster prediction.
- **Performance:** `performance_analysis` vs buy-and-hold — total return, CAGR, max drawdown, return-to-MDD.
---
## Support Python Modules (data_modules)
- **`unsup_capstone_util.py`:** `check_stationarity`, `correlation_check`, `get_number_of_clusters`, `performance_analysis` — helpers for the capstone solution.
## Cross-cutting prerequisite lenses
- **PCA prerequisite chain:** variance/covariance → eigenvalues/eigenvectors/maths → PCA example → choosing number of features.
- **Clustering prerequisite chain:** feature selection (stationarity+correlation) → scaling → k-means → choosing clusters → cluster analysis (hit ratio/skewness).
- **Pairs prerequisite chain:** PCA+fundamentals feature engineering → DBSCAN clustering/pairs → cointegration test.
- **Supported by** custom utility modules (data_modules) used throughout.
---
## Unsupervised-Learning-in-Trading — Section-based course structure
# — Unsupervised Learning in Trading — Concept Inventory
**Track:** 5 — Artificial Intelligence in Trading (Advanced)
**Media note:** PDFs only (no mp4s).
**Overlap with D: notebooks:** significant — the D: side carries notebook-based `Unsupervised-Learning-in-Trading` extraction covering k-means on financial data, feature scaling/selection, hit-ratio/skewness cluster analysis, PCA and pairs trading in `.ipynb` form. This course mirrors it and adds the maths/parameter PDFs (k-means, PCA math, DBSCAN parameter selection, pairs-trading/clustering, capstone).
---
## COURSE
Unsupervised learning to discover structure in financial data and trade it: **k-means clustering** for grouping stocks into regimes (with data scaling, feature selection, and choosing the number of clusters via elbow/kurtosis), **evaluating** clusters by hit-ratio and skewness, **principal component analysis (PCA)** for dimensionality reduction (from curse-of-dimensionality rationale through to eigenvalue/eigenvector maths and application), **DBSCAN** (density-based clustering) as a non-k alternative, and pairs-trading / statistical-arbitrage built from mean-reverting cointegrated pairs identified via clustering — closing with an IBridgePy automated strategy and a capstone.
## Course Prerequisite Map
- **Section 4 K-Means requires:** distance/Euclidean measurements + centroid concepts.
- **Section 5 K-Means for financial data requires:** Section 4 + technical indicators (RSI, ADX from prerequisites).
- **Section 6 Scaling the Data requires:** Sections 4–5 (features differing in scale break clustering).
- **Section 7 Feature Selection requires:** Section 5/6 + stationarity (ADF test), correlation.
- **Section 8 Selecting Clusters requires:** Section 4 (inertia) + elbow-curve logic.
- **Section 9 Hit Ratio requires:** Section 8 (a labelled cluster mapping) + backtesting.
- **Section 10 Skewness requires:** Section 9 (cluster distributions) + moment stats (skew/kurtosis).
- **Section 11 Putting It All Together requires:** Sections 4–10 (parse the full k-means strategy).
- **Section 12 Curse of Dimensionality requires:** SQL / high-dimensional space intuition.
- **Section 13 PCA Intro requires:** Section 12 + dimensional reduction need.
- **Section 14 Maths Behind PCA requires:** Section 13 + matrix multiply + eigenvector/eigenvalue.
- **Section 15 PCA requires:** Section 14 + choosing principal components (variance explained).
- **Section 16 Pairs Trading App requires:** Sections 4–15 (clustering) + cointegration/mean-reversion.
- **Section 17 DBSCAN requires:** Section 4-16 clustering comparison + density logic.
- **Section 18 Pairs Trading using Clustering requires:** Sections 16 & 17 (identify cointegrated pairs via clustering) + Bollinger-bands pairs basier.
- **Section 20 Capstone requires:** all prior.
- **Section 21 Automate requires:** Section 18-capstone model + IBridgePy.
---
### Section 4 — K-Means Clustering
- **CONCEPT:** k-means algorithm — partition data into k clusters by iterative assignment to the nearest centroid; distances measured with **Euclidean distance** (plus standardised/weighted variants); centroid updates recomputed from cluster means; variations exist (efficiency vs computational strain). prereqs: distance geometry, averaging.
### Section 5 — K-Means for Financial Data
- **CONCEPT:** Apply k-means to stocks — cluster stocks on indicator features (RSI, ADX, etc.) to group similar behaviours; the DocRead also (review the RSI/ADX calculations) so clustering features are interpretable. prereqs: Section 4 + indicator/feature knowledge.
### Section 6 — Scaling the Data
- **CONCEPT:** Feature scaling — **min-max scaler** and **standard scaler** (and other techniques) so no single feature dominates the Euclidean distance used in clustering. prereqs: Sections 4–5.
### Section 7 — Feature Selection
- **CONCEPT:** Feature selection — select features that add signal: test **stationarity** (augmented Dickey-Fuller test), prune highly correlated/redundant features (similarity measure / max-information-compression index). prereqs: Sections 4–6 + statistics.
### Section 8 — Selecting Clusters for K-Means
- **CONCEPT:** Choosing the number of clusters k — **elbow curve** of inertia (within-cluster sum of squares): pick the k at the elbow; alternatives such as scaled-inertia heuristics. (1D data often needs kernel density estimators instead.) prereqs: Section 4 + inertia plot.
### Section 9 — Analysing Clusters: Hit Ratio
- **CONCEPT:** Hit ratio — fraction of instances in which the next-day return sign matches the cluster-implied direction; a backtester uses hit ratio to score cluster fidelity. prereqs: Section 8 + daily return/forward-return labels.
- **CONCEPT:** Backtesting the cluster-based strategy — walk-forward testing, performance metrics (Sharpe, Sortino), strategy validation in a notebook. prereqs: Section 9 + backtesting.
### Section 10 — Analysing Clusters: Skewness
- **CONCEPT:** Skewness & kurtosis of cluster-return distributions — skewness measures distribution symmetry; kurtosis measures tail risk (both applied to cluster-predicted returns vs benchmark S&P/Bitcoin tail-risk). prereqs: distribution moments, Section 9.
### Section 11 — Putting It All Together
- **CONCEPT:** The full k-means trading strategy — from OHLC data → indicator features → scale → reduce (PCA preview) → cluster → hit-ratio / skewness analysis → backtest a lower-timeframe strategy; papers applying k-means + regression / commodity cluster analysis inform this. prereqs: Sections 4–10.
### Section 12 — Curse of Dimensionality
- **CONCEPT:** Curse of dimensionality — as feature dimensions grow, data becomes sparse and distance measures break down; prefer fewer effective dimensions (same result with less). prereqs: high-dimensional geometry intuition.
### Section 13 — Introduction to Principal Component Analysis (PCA)
- **CONCEPT:** PCA — linear, unsupervised dimensionality reduction that projects data onto the directions of greatest variance using **variance and covariance** of features (mutual experience: two features, reduces to one while retaining variance). prereqs: Section 12 + feature covariance.
### Section 14 — Maths Behind Principal Component Analysis
- **CONCEPT:** Matrix multiply + eigenvalues/eigenvectors — PCA's principal components are the **eigenvectors of the covariance matrix** (with eigenvalue = variance explained) gained via linear algebra; you must be comfortable multiplying matrices and computing eigenvectors/eigenvalues. prereqs: Section 13 + matrix algebra.
### Section 15 — Principal Component Analysis (implementation)
- **CONCEPT:** Choose principal components — retain PCs by explained-variance ratio, cumulative variance, or other heuristics; uses log / linear returns as features; can build **eigen-portfolios** (weights from eigenvectors/eigenvalues). prereqs: Section 14 + covariance.
### Section 16 — Application of Unsupervised Learning for Pairs Trading
- **CONCEPT:** Pairs / statistical arbitrage trading — a **mean-reverting** time-series profile where you buy low/sell high; natural mean-reverting financial series a rare, so you **fabricate** one by combining two price series; clustering selects candidate pairs (cointegrated price series) — pairs spread from their combined mean-reverting. prereqs: Section 15 + cointegration.
### Section 17 — DBSCAN
- **CONCEPT:** DBSCAN — density-based clustering (clusters formed only where points are dense; noise tolerated) — vs k-means; **parameters**: **minPts** (≥2; rule of thumb ≥1 more than features, ~2× dimension for large sets) and **epsilon (eps) distance**. HDBSCAN = advanced variant. prereqs: clustering intuition + geometry.
### Section 18 — Pairs Trading using Clustering Algorithms
- **CONCEPT:** Select pairs via clustering — using the clusters (k-means/DBSCAN) to find cointegrated pairs for pairs trading; **correlation** and **cointegration** are the selection criterion; common trade approach via Bollinger bands on the spread. prereqs: Sections 16–17 + cointegration stats + Bollinger bands; TSNE visualisation for pre-cluster inspection.
### Section 20 — Capstone Project
- **CONCEPT:** Capstone: build an end-to-end unsupervised trading strategy — read your dataset (e.g. GOOG daily CSV), define/engineering features with sanity checks (correlation, stationarity), normalize, cluster select, evaluate, strategy; template/solutions zips. prereqs: entire course.
### Section 21 — Automate Trading Strategy Using IBridgePy
- **CONCEPT:** IBridgePy automation — deploy the k-means/live strategy through IBridgePy (`unsupkmeansliveibridgepy.zip`) into paper/live account flow. prereqs: Section 18 model + broker.
### Section 22 — Course Summary
- **CONCEPT:** Recap + resources (`UnsupervisedLearningResources.zip`). prereqs: entire course.


====================
Value-Strategy-in-Forex
====================

# Value Strategy in Forex — Concept Inventory
**Source course dir:** `others\_extracted\Value-Strategy-in-Forex`
**Output file:** `_concept_lists\Value-Strategy-in-Forex.md`
**Goal of course:** Build a currency **value strategy** that buys undervalued and sells overvalued currencies, using REER (Real Effective Exchange Rate) as the valuation yardstick. Apply it to 8 USD-based FX pairs and measure performance (Sharpe, CAGR, max drawdown).
---
## Assets & Structure
- **Notebooks (1):**
 - `Forex Value Strategy_ Implementation\FX Value Strategy in Python.ipynb`
- **Data modules (`data_modules\`):**
 - `REER_2023_Aug2021_Jul2023.csv` — BIS Real (CPI-based) Effective Exchange Rate, **Narrow** indices, **monthly averages** (Aug 2021 – Jul 2023), one column per country (Australia, Canada, Euro area, Japan, New Zealand, Singapore, Switzerland, UK).
 - `currency_data_2023.csv` — daily **close** prices for the 8 USD-based currency pairs (SGDUSD, AUDUSD, CADUSD, CHFUSD, GBPUSD, JPYUSD, NZDUSD, EURUSD).
- **Docs:** `Folder Structure and How to Run Code Files.html`, `ReadMe.html`.
- **Modules:** No standalone `.py` module — all logic lives inside the notebook.
## Per-Notebook Concepts
### FX Value Strategy in Python.ipynb
Pipeline: read REER → rolling mean → signal → import currency prices → compute strategy returns → analyse performance.
- **Value-investing premise applied to FX:** buy a currency when it is "cheap" (undervalued) and sell when "expensive" (overvalued), where valuation is measured by the **REER relative to its own recent history** (a mean-reversion/valuation view, not a trend view).
- **REER (Real Effective Exchange Rate):** trade-weighted *real* exchange-rate index (here BIS, Real CPI-based, Narrow indices, monthly averages). Interpretation: REER above its trend ⇒ currency **overvalued** ⇒ expect depreciation → **sell**; REER below its trend ⇒ **undervalued** ⇒ expect appreciation → **buy**.
- **Rolling-mean benchmark (6 months):** `reer.rolling(6).mean()` → the trailing 6-month average REER serves as the valuation yardstick per country. Rolling-mean syntax `dataframe.rolling(lookback).mean()` computes the mean along columns.
- **Signal generation (mean-reversion on valuation):**
 - `signal = reer < reer_mean` → True (1) when REER below its 6-month mean (undervalued → buy).
 - Replace `True → 1` and `False → NaN`, then `fillna(-1.0)` so **NaN → −1** (overvalued → sell). Final signal ∈ {+1 buy, −1 sell}.
 - Booleans bridge cleanly to ±1 trading signals via replace/fillna.
- **Bridge to daily data (publication lag & frequency):**
 - Signal exists only monthly; forward-fill (`ffill`) across all trading days: create a daily-indexed frame via `signal.join(pd.DataFrame(index=currency_returns.index), how='outer')` then `fillna(method='ffill')`.
 - **Look-ahead-avoidance:** BIS publishes REER around the **16th of each month** → signal shifted **11 trading days** (`signal.shift(11)`) so the trade uses only data that was actually available (no look-ahead bias).
- **Strategy returns:** `strategy_returns = currency_returns * signal.shift(11)` per pair, where `currency_returns = currency_price.pct_change()` (daily returns).
- **Portfolio combination:** equal-weighted mean of the 8 pairs × a leverage factor: `daily_ret = strategy_returns.sum(axis=1)/8.0 * leverage` (leverage = **5.0**).
- **Performance analysis (custom functions):**
 - **Annualised Sharpe:** `annualized_sharpe_ratio(returns, N=252) = sqrt(N)*mean/std`.
 - **CAGR:** `100*((cumsum+1)**(252/n_days) − 1)`.
 - **Maximum drawdown:** `min(cumulative_returns − cumulative_returns.cummax())` (peak-to-trough).
 - **Benchmark outputs:** Sharpe ≈ **0.58**, CAGR ≈ **10.23%**, max DD ≈ **−13.52%** for the combined leveraged portfolio.
- **Caveats:** backtest **ignores commission and rollover (swap) charges**; the notes explicitly advise including them for realistic results, and point forward to an interactive exercise.
## Prerequisites (concepts the learner is expected to know)
- **pandas:** `read_csv(index_col=0)`, `to_datetime` indexing, `rolling().mean()`, `pct_change`, `replace`, `fillna`, `ffill`, `join`/outer merge, `shift` for lag/lead; **matplotlib** plotting; **numpy**.
- FX quote conventions (USD-based pairs: e.g. 1.28 GBP per USD) and daily return computation.
- Meaning of **valuation / mean-reversion** (a currency's real value oscillates around a long-run norm), and the intuition that "cheap assets to buy, expensive assets to sell".
- (Conceptual links) **momentum / mean-reversion frameworks** from prior courses; **data-publication-lag handling** for macro/fundamental data (avoiding look-ahead bias).
---
## Value-Strategy-in-Forex — Section-based course structure
# Concept Inventory: Value Strategy in Forex
> Inventory source: 1 PDF (`REER.pdf`), 1 Python strategy (`value_forex.py` inside `IBridgePyValueForex.zip`), 1 resource notebook (`FX Value Strategy in Python.ipynb` in `VSIFResources.zip`), REER CSV data. No flat section folders — organized by resource archives instead.
## COURSE
Value (fundamental/valuation) strategy applied to the **Forex** asset class. The course teaches measuring whether a currency is over/undervalued relative to a weighted basket of trading-partner currencies using the **Real Effective Exchange Rate (REER)**, and turning that signal into a long-only, monthly-rebalanced multi-currency portfolio using Zipline/IBridgePy on Blueshift. Covers REER construction (weights, exchange-rate indices, inflation adjustment), currency basket selection, signal generation (REER vs its rolling mean), and strategy performance analysis.
### Section: REER — Real Effective Exchange Rate (theory)
Source: `REER.pdf`
- **Definition & purpose**: weighted average of a country's exchange rate relative to a basket of trading-partner currencies, inflation-adjusted per currency; measures *real* purchasing power / overall currency value vs. trading partners.
- Used to gauge whether a currency appreciated/depreciated *in real terms* across its trade network (e.g., 2015 RMB: ~8% vs USD but ~10% real appreciation once trade-weighted).
- REER is volatile over short windows; **not** a good standard-of-living comparator — that requires Purchasing Power Parity (PPP) measures.
- Released by IMF, central banks, BIS with ~3-month lag.
- **Construction**
 - Bilateral real exchange rate (RER) averaged across trading partners.
 - Weights = each partner's trade share (trade volume / total trade).
 - Adjusted by inflation (CPI) for each currency.
 - RBI uses a 36-country basket; course example uses 6 majors (US, Germany, UAE, Saudi Arabia, China, Hong Kong SAR).
- **Formula components** (RBI methodology)
 - n = number of basket countries; i = ith currency.
 - e / ei = indexed exchange rate of INR / foreign currency versus IMF Special Drawing Rights (SDR).
 - wi = trade weight of currency i.
 - Pi / P = CPI of foreign country i / India (India uses CPI to adjust REER).
 - **REER = product over i of [(e/ei) × (P/Pi)]^wi** (empowered geometric weighted combination).
- **Worked example (India, 6 currencies)**
 - Trade volumes (FY2017-18, US$bn) → weights (%): China 29.15, USA 25.66, UAE 17.17, Hong Kong 11.76, Saudi 9.23, Germany 7.02.
 - Exchange rates vs INR (Jul 2018, base Jan 2015) — e.g., China 102.59; Germany 114.07 (EUR/INR).
 - CPI values (Jul 2018) vs India 120.3 — e.g., China 102.1, USA 117.58.
 - Product of all REER components → total REER (e.g., 0.01008).
 - **Benchmarking**: REER benchmarked to 100 in a base year; subsequent years expressed relative (e.g., next year 0.01002 → 99.404).
### Section: Value Strategy — Implementation (code)
Sources: `value_forex.py` (IBridgePyValueForex.zip) • `FX Value Strategy in Python.ipynb` (VSIFResources.zip) • `REER_27.csv` / `REER_2023_Aug2021_Jul2023.csv`
- **Strategy style**: Systematic, Long-only, asset class *Forex*; input = Forex + REER data.
- **Symbol universe**: CASH, <CCY> / USD pairs — SGD, AUD, CAD, CHF, GBP, JPY, NZP, EUR.
- **Rebalancing schedule**: monthly, at `month_end` (offset), 5 minutes before market close.
- **REER data intake**
 - Read REER CSV (downloaded from **BIS** — Bank for International Settlements) into pandas; set index to datetime.
 - REER updated monthly by BIS; refresh the CSV each month.
- **Signal generation**: compute rolling mean of REER (e.g., rolling 6-month window), compare each currency's current REER to rolling mean.
 - Undervalued currency (REER < rolling mean) → overweight (order_target_percent ~0.1).
 - Overvalued currency → reduce/exit (order_target_percent 0).
- **Notebook pipeline (FX Value Strategy in Python)**
 1. Read REER data.
 2. Generate the trading signal.
 3. Import currency-pairs price data.
 4. Compute strategy returns.
 5. Analyze performance.
- **Conf** suspicion: code sample shows a conditional bug (`if reer < reer_mean ... elif reer < reer_mean`) — treat as reference logic to fix; intended rule = overweight undervalued, flat/underweight overvalued.
### Prerequisites
- Understanding of *value* vs *momentum* style factors (value = mean-reversion / undervalued-reflation).
- Exchange-rate quoting, currency pairs, SDR concept, CPI/inflation.
- pandas: read_csv with index, to_datetime, rolling window means.
- Zipline/IBridgePy API: initialize, schedule_function, date_rules.month_end/time_rules.market_close, data.history, order_target_percent.
- Case-study mental model from REER doc (weighted-geoetric index arithmetic).
- Basic statistics: rolling means, signal thresholding.
## Course Prerequisite Map
- **FX market basics** → currency pair symbols → unit-selected buffer.
- **REER** (this course) → value/investment signal → currency rebalance weights.
- **Data handling**: CSV ingest → pandas datetime index → rolling mean.
- Forward dependency: **momentum vs. value factor distinction** feeds later multi-factor and position-sizing units.
- Overlaps with `Forex Trading using Python - Basics` (same Blueshift/Zipline API for order/schedule/data.history) — that unit is effectively prerequisite here.


====================
Volatility-Trading-Beginners
====================

# Volatility Trading for Beginners — Exhaustive Concept Inventory
## COURSE: Volatility Trading for Beginners
## MODULE: Calculating Beta
### LESSON: Calculate Beta With Python (`Calculate Beta With Python.ipynb`)
- **CONCEPT:** Beta — a measure of a stock's volatility relative to the benchmark (e.g. S&P 500); beta > 1 means the stock overperforms/moves more than the benchmark, beta < 1 less. prereqs: none
- **CONCEPT:** Benchmark return — the reference index (S&P 500) return series against which a stock's returns are regressed to estimate beta. prereqs: index returns
- **CONCEPT:** Daily returns — computing each asset's day-to-day percentage change (`pct_change()`), the raw input to beta regression. prereqs: percentage change
- **CONCEPT:** Ordinary Least Squares (OLS) regression — linear regression via statsmodels `sm.OLS(y, x).fit()`; the slope of regressing stock returns on index returns is beta. prereqs: linear regression, slope
- **CONCEPT:** Independent vs dependent variable — index returns (x, independent) and stock returns (y, dependent) in the regression; beta is the coefficient of x. prereqs: regression roles
- **CONCEPT:** Constant/intercept term — `sm.add_constant` adds the intercept; omitting it forces the intercept to zero and estimates only the slope, avoiding overfitting. prereqs: intercept, model specification
- **CONCEPT:** y-intercept and slope from `.params` — reading the fitted intercept (`params[0]`) and beta/slope (`params[1]`) from the fitted model. prereqs: fitted parameters
- **CONCEPT:** Regression equation `y = a + bx` — using the intercept and beta in the line equation to reconstruct estimated stock returns from index returns. prereqs: linear equation
- **CONCEPT:** Scatter plot of returns — plotting index returns vs stock returns and overlaying the fitted regression line to visualise the slope and relationship. prereqs: scatter plot, matplotlib
- **CONCEPT:** Beta and the CAPM link — interpreting beta (estimated here) for use later in the Capital Asset Pricing Model (CAPM) expected-return framework. prereqs: beta, CAPM
## MODULE: Research on BAB (Betting Against Beta)
### LESSON: Research on the BAB Strategy — I (`Research on BAB - I.ipynb`)
- **CONCEPT:** Betting-Against-Beta (BAB) — Frazzini & Pedersen's (2014) strategy that argues against holding high-beta stocks; instead going long low-beta and short high-beta stocks to obtain positive risk-adjusted returns. prereqs: CAPM, beta
- **CONCEPT:** CAPM high-beta appeal — under the Capital Asset Pricing Model, high-beta stocks are expected to give higher expected returns, which attracts investors to them. prereqs: CAPM, expected return
- **CONCEPT:** Frazzini–Pedersen hypothesis — the empirical claim that betting against beta (long low beta, short high beta) produces superior risk-adjusted performance. prereqs: BAB idea, risk-adjusted return
- **CONCEPT:** Train/test split of data — dividing the price sample into a train year (to estimate betas) and a test year (to evaluate performance), so results are out-of-sample. prereqs: overfitting avoidance, train/test
- **CONCEPT:** `calc_beta` via OLS — function that regresses a stock's returns on market returns and returns the slope (beta). prereqs: OLS, beta
- **CONCEPT:** Computing stock returns (`pct_change`) — train-sample daily returns used to regress betas. prereqs: percentage change
- **CONCEPT:** Beta for all stocks via `apply` — applying `calc_beta` across every stock column (axis=0) to get a beta value per stock. prereqs: pandas apply, beta
- **CONCEPT:** Beta quantile buckets — using `pd.qcut(beta, q=20)` to split the ~487 stocks into 20 beta buckets, each with ~25 stocks, from lowest (bucket 1) to highest (bucket 20) beta. prereqs: quantiles, sorting
- **CONCEPT:** Bucket return performance — computing each stock's test-period return and averaging by beta bucket to examine the low-to-high beta return pattern. prereqs: grouping, means
- **CONCEPT:** Downward slope of returns vs beta — observing that returns decline from low-beta to high-beta buckets, supporting the hypothesis that shorting high beta would be profitable. prereqs: bucket returns, trend
### LESSON: Research on the BAB Strategy — II (`Research on BAB - II.ipynb`)
- **CONCEPT:** Multi-year validation — extending the BAB backtest from a 2-year window (2021–2022) to a longer 7-year span (2015–2022) to check whether the hypothesis holds more reliably. prereqs: BAB research design
- **CONCEPT:** Iterated yearly train/test loop — a `for` loop over years that treats each year as training data and the next year as test data, recomputing beta buckets and bucket-return plots each iteration. prereqs: loops, train/test split
- **CONCEPT:** `get_performance` helper — a function encapsulating beta calculation, quantile bucketing, and per-bucket return averaging/plotting for one train/test pair. prereqs: functions, beta buckets
- **CONCEPT:** try-except end-of-data guard — using a try-except block so that when the loop requests a nonexistent next-year test set (e.g. training on 2022 requiring 2023), execution stops gracefully. prereqs: error handling
- **CONCEPT:** Slope direction across years — summarising whether each year's bucket-return curve slopes upward or downward (only 2 of 7 years downward), used to test the generality of the BAB claim. prereqs: trend interpretation
- **CONCEPT:** Hypothesis not confirmed on recent data — concluding that betting against beta was not consistently profitable in the more recent sample, motivating a pivot to long-only high-beta backtests. prereqs: BAB hypothesis, empirical results
## MODULE: Backtesting BAB
### LESSON: Backtesting the BAB Strategy — I (`BAB Backtesting - I.ipynb`)
- **CONCEPT:** Long-only high-beta backtest — following the research conclusion that over most years going long high-beta stocks makes sense, backtesting a long-only portfolio of the highest-beta S&P 500 stocks for 2016. prereqs: high-beta stocks, research on BAB
- **CONCEPT:** Beta estimation on a training year — calculating betas on the prior year's (2015) returns using the calc_beta/OLS function, then applying them to trade the test year (2016). prereqs: beta, train/test
- **CONCEPT:** Rolling-year change detection — detecting a new calendar year via `data.index[i].year != data.index[i-1].year` to isolate train-year data. prereqs: looping, datetime year
- **CONCEPT:** Beta for a whole panel — `apply(calc_beta, args=(S&P500 returns,), axis=0)` computes each stock's beta against the S&P 500 for the train year. prereqs: pandas apply, OLS
- **CONCEPT:** Descending beta ranking — `beta_df.rank(ascending=False, axis=1)` ranks stocks from highest to lowest beta across each row (axis=1). prereqs: ranking, axis semantics
- **CONCEPT:** Top-bucket stock selection — selecting the first 20 ranked (high-beta) stocks as the long universe; assigning 1 to those chosen and 0 otherwise via `applymap`. prereqs: ranking, threshold selection
- **CONCEPT:** Equally-weighted portfolio returns — averaging the selected stocks' daily returns (`mean(axis=1)`) to compute an equal-weight portfolio backtest. prereqs: mean, pct_change
- **CONCEPT:** Strategy analytics (`qa.strategy_stats`) — a helper module reporting the top 5 largest drawdowns and summary metrics (Sharpe ratio, CAGR, MDD) for a returns series. prereqs: analytics module
- **CONCEPT:** Result interpretation — decent CAGR (e.g. 18.04%) but low risk-adjusted Sharpe (0.70) for the single-year backtest, motivating a longer validation. prereqs: Sharpe, CAGR, MDD
### LESSON: Backtesting the BAB Strategy — II (`BAB Backtesting - II.ipynb`)
- **CONCEPT:** Multi-year long-only BAB backtest — rebalancing the high-beta portfolio annually from 2015 to 2022 to validate the strategy over a longer window. prereqs: BAB backtesting I, annual rebalancing
- **CONCEPT:** Annual beta estimation loop — for each new year, estimating betas on the prior year and storing them, producing a beta_df indexed by each test year's start. prereqs: loops, beta
- **CONCEPT:** Signals spanning the whole period — creating a `signals` dataframe covering all trading days by concatenating yearly long-asset flags with the remaining data index, sorting, and forward-filling. prereqs: concat, ffill, index alignment
- **CONCEPT:** Position persistence via forward fill — filling the signals NaN gaps with the previous yearly selection (`fillna(method='ffill')`) so positions persist between rebalances. prereqs: ffill, rebalancing
- **CONCEPT:** Equally-weighted daily strategy returns — `(signals * data.pct_change()).mean(axis=1)`, combining stock returns with active-position flags into one strategy series. prereqs: signals, returns, mean
- **CONCEPT:** Strategy statistics over the broad sample — Sharpe 0.86, CAGR 25.1%, max drawdown 43.7% (2020 crash) using `qa.strategy_stats`. prereqs: Sharpe, CAGR, MDD
- **CONCEPT:** Survivorship caveat — noting the backtest ignores that some stocks entered and left the S&P 500 list between 2016–2022, a known limitation (adds survivorship bias). prereqs: survivorship bias, index constituents
## MODULE: Bollinger Bands
### LESSON: Oversold Trading Strategy (`Oversold Trading Strategy.ipynb`)
- **CONCEPT:** Bollinger Bands — a volatility envelope: middle band is a moving average, upper band = MA + (mult × moving std), lower band = MA − (mult × moving std); computed here with TA-Lib `ta.BBANDS`. prereqs: moving average, standard deviation
- **CONCEPT:** Moving average (middle band) — the rolling mean of the close over the look-back period (e.g. 20). prereqs: mean, rolling window
- **CONCEPT:** Upper/lower band multiples — `nbdevup`/`nbdevdn` multiples of the moving standard deviation added/subtracted from the moving average to form the bands. prereqs: standard deviation, bands
- **CONCEPT:** Oversold signal — a long entry when the close crosses below the lower band for the first time (today's Close < lowerband AND yesterday's Close > yesterday's lowerband). prereqs: bands, crossover detection
- **CONCEPT:** Crossover detection with `np.where` — flagging a signal when current close is below the lower band and the previous close was above it. prereqs: boolean conditions, shift
- **CONCEPT:** Average True Range (ATR) — a volatility indicator used to set dynamic stop-loss and take-profit multiples from the entry price. prereqs: true range, volatility indicator
- **CONCEPT:** Dynamic SL/TP targets — stop_loss = entry − ATR × stop_loss_multiple; take_profit = entry + ATR × take_profit_multiple; dynamically follow volatility while in a trade. prereqs: ATR, entry price
- **CONCEPT:** Event-driven backtesting loop — iterating each day, entering a long on the oversold signal and closing when the close breaches stop-loss or take-profit. prereqs: backtest loop, signals
- **CONCEPT:** Trade book / trading dataframe — a record of Position, Entry Time, Entry Price, Exit Time, Exit Price, and PnL for each trade. prereqs: dataframes, trade recording
- **CONCEPT:** PnL net of trading cost — subtracting a per-trade transaction cost (close × 0.0002 × 2 for entry+exit) from gross PnL. prereqs: transaction cost, PnL
- **CONCEPT:** Plotting positions — marking buy (green up-triangle) and sell (red down-triangle) points on the close-price chart to visualise trade timing. prereqs: scatter plotting
- **CONCEPT:** Strategy analytics & conclusion — computing Sharpe, CAGR, MDD; noting that an oversold (mean-reversion) band strategy works well for mean-reverting stocks but not for trend-following ones. prereqs: performance metrics, style fit
### LESSON: Breakout Strategy Implementation (`Breakout Strategy Implementation.ipynb`)
- **CONCEPT:** Breakout / trend-following strategy — a Bollinger-band-based trend strategy that buys when price transitions out of a squeeze into an expansion phase, for trending (non-mean-reverting) stocks. prereqs: Bollinger bands, trend following
- **CONCEPT:** Bandwidth — (upper − lower) / middle, a normalised measure of the band width that rises when volatility expands out of a squeeze. prereqs: bands, ratio
- **CONCEPT:** Rolling bandwidth — the rolling mean (e.g. 21-period) of bandwidth used as a reference to detect expansion. prereqs: rolling mean, bandwidth
- **CONCEPT:** Expansion-condition signal — entering a long when today's bandwidth > rolling bandwidth (transition to expansion) AND today's High rises above the upperband. prereqs: conditional logic, bands
- **CONCEPT:** Signal termination (0) and forward-fill — setting signal to 0 when Low falls back below the middle band (squeeze return), then forward-filling so position persists between those events. prereqs: ffill, exit condition
- **CONCEPT:** ATR-based dynamic exits — stop-loss and take-profit as multiples of ATR from the entry price (e.g. 2× and 3× for breakout strategy). prereqs: ATR, SL/TP
- **CONCEPT:** Event-driven backtesting loop & trade book — long entry on breakout signal, exit on SL/TP breach; PnL net of trading cost recorded in a trades frame. prereqs: backtest loop, PnL, trading cost
- **CONCEPT:** Strategy analytics & comparison — high Sharpe (1.29) and CAGR (85.94%) with large drawdown (51.41%), characteristic of a momentum/breakout profile; tuning suggestions include trying other stocks and a short variant. prereqs: Sharpe, CAGR, MDD
## MODULE: Entry Signals
### LESSON: Determine the Entry Points (`Determine the Entry Points.ipynb`)
- **CONCEPT:** Moving-average crossover strategy — a trend-detection method using a short and a long simple moving average; a long entry occurs when the short MA crosses above the long MA (bullish crossover). prereqs: moving averages, crossover
- **CONCEPT:** Bullish crossover — when the short-term SMA (e.g. 15-day) rises above the long-term SMA (e.g. 35-day), indicating bullishness and triggering a buy. prereqs: SMAs, comparison
- **CONCEPT:** Bearish crossover — when the short-term SMA falls below the long-term SMA, signalling bearishness (exit signal). prereqs: SMAs, comparison
- **CONCEPT:** Simple moving average (SMA) via TA-Lib — `ta.SMA(series, timeperiod)` computes a rolling average of close prices for a given span. prereqs: TA-Lib, rolling average
- **CONCEPT:** Crossover detection with two reference points — the signal fires when yesterday's SMA_15 below SMA_35 AND today's SMA_15 above SMA_35, found by shifting yesterday's values with `shift(1)`. prereqs: shift, boolean AND
- **CONCEPT:** `np.where` signal generation — conditionally assigning 1 when the crossover condition holds, else 0. prereqs: numpy where
- **CONCEPT:** Plotting entry signals — overlaying green triangles where the long-signal fires on the close-price chart. prereqs: scatter plotting
- **CONCEPT:** Saving signals to CSV (`to_csv`) — persisting the enriched dataframe (with SMA and signal columns) to `visa_signals.csv` for reuse by the exit-strategy notebooks. prereqs: pandas I/O
## MODULE: Fixed SL & TP
### LESSON: Exit Using Fixed Stop-Loss and Take Profit (`Exit Using Fixed Stop-Loss and Take Profit.ipynb`)
- **CONCEPT:** Fixed stop-loss and take-profit — pre-set percentage-based exit levels (e.g. stop 1%, take 3%) decided once at entry and unchanged regardless of market volatility. prereqs: exit rules, percentages
- **CONCEPT:** Stop-loss price — entry_price × (1 − stop_loss_percentage); a level at which a losing trade is closed. prereqs: entry price, percentages
- **CONCEPT:** Take-profit price — entry_price × (1 + take_profit_percentage); the level at which a profitable trade is banked. prereqs: entry price, percentages
- **CONCEPT:** Trade book — a tracking dataframe of Position, Entry Time, Entry Price, Exit Time, Exit Price, and PnL for all historical trades. prereqs: trade recording, dataframes
- **CONCEPT:** Position-state tracking — a binary flag (0 = flat, 1 = long) to track whether a long position is open during the backtest loop. prereqs: state machine, backtest loop
- **CONCEPT:** Backtest entry/exit loop — on a buy signal enter a long (record entry, set SL/TP levels), and while long exit whenever close breaches SL or TP, recording the closed trade. prereqs: signals, backtest loop
- **CONCEPT:** PnL net of transaction cost — exit close − entry price − (close × 0.0002 × 2) to reflect entry-plus-exit costs. prereqs: PnL, transaction costs
- **CONCEPT:** Limitation of fixed exits — fixed thresholds stay constant even in volatile conditions, causing early or inappropriate exits and losses (visible in 2019–2022 returns). prereqs: fixed levels, volatility sensitivity
## MODULE: SL & TP using ATR
### LESSON: Exit Using ATR (`Exit Using ATR.ipynb`)
- **CONCEPT:** Average True Range (ATR) — a volatility indicator measured as the average of the True Range over n periods (e.g. 14); indicates how much an asset moves on average. prereqs: true range, volatility
- **CONCEPT:** True Range (TR) — max of (High − Low), |High − prev Close|, |Low − prev Close|; the widest gap of a candle against the prior close. prereqs: OHLC, absolute values
- **CONCEPT:** ATR formula & TA-Lib computation — TR averaged over the window, computed here via `ta.ATR(high, low, close, timeperiod=14)`. prereqs: ATR formula, TA-Lib
- **CONCEPT:** Dynamic stop-loss / take-profit — SL = entry − ATR × stop_loss_multiple; TP = entry + ATR × take_profit_multiple; levels scale with current volatility instead of staying fixed. prereqs: ATR, exit levels
- **CONCEPT:** Volatility-adaptive exits motivation — fixed levels ignore volatility and exit too early or too late; ATR-based levels adjust to the asset's live volatility. prereqs: fixed-vs-dynamic contrast
- **CONCEPT:** Backtest loop and trade book — same event-driven long entry/exit loop as the fixed approach, but with ATR-computed SL/TP; higher PnL than fixed (e.g. ~$50 vs ~$35). prereqs: backtest loop, trade book
- **CONCEPT:** Comparison preview — noting returns are higher with dynamic exits, motivating a head-to-head comparison notebook. prereqs: metrics comparison
### LESSON: Comparison Between Fixed and Dynamic Approaches (`Comparison Between Fixed and Dynamic Approaches.ipynb`)
- **CONCEPT:** Trade analytics (`get_analytics`) — a summary of trading statistics for a trade book: number of longs, net profit, winners/losers counts, win/loss percentages, and average profit/loss per trade. prereqs: trade book, statistics
- **CONCEPT:** Win/loss percentage — percentage of profitable vs loss-making trades out of all long trades; dynamic approach shows a higher win percentage (e.g. 65.85% vs 62.79%). prereqs: winners/losers counts
- **CONCEPT:** Net profit comparison — dynamic ATR-based exits produced substantially higher net profit (e.g. $72.3 vs $17.1) than fixed exits. prereqs: PnL summing
- **CONCEPT:** Profit/loss per trade — average gain on winning trades and average loss on losing trades; dynamic exits may set wider stops (larger ATR) leading to larger per-trade losses but overall higher profit. prereqs: means, PnL distribution
- **CONCEPT:** Position column via `ffill` — adding a long-position indicator (1 at entry, 0 at exit) and forward-filling for the full history, to later compute strategy returns. prereqs: ffill, position tracking
- **CONCEPT:** Cumulative strategy returns — weighted daily returns (`pct_change() × shifted long_position`) compounded; the dynamic strategy's equity curve sits higher. prereqs: pct_change, cumprod, shift
- **CONCEPT:** Drawdown comparison — computing max drawdown of both equity curves; the dynamic approach's drawdown is higher (e.g. −13.52% vs −8.16%) because high-volatility ATR can set wide stops. prereqs: running maximum, drawdown
- **CONCEPT:** Sharpe ratio — (mean return / std return) × √252; a risk-adjusted performance measure where higher is better; the dynamic approach has a higher Sharpe (e.g. 0.75 vs 0.56). prereqs: mean, std, annualisation
- **CONCEPT:** Overall conclusion of the comparison — the dynamic approach performs better on net profit, win percentage, cumulative returns, and Sharpe despite occasionally larger drawdowns from volatility-scaled stops. prereqs: metric integration, trade-offs
## MODULE: Hedging Using VIX
### LESSON: Portfolio Hedging Using VIX (`Portfolio Hedging Using VIX.ipynb`)
- **CONCEPT:** Negative SPY–VIX correlation — SPY (S&P 500) and VIX (volatility) generally move inversely: portfolio falls and VIX rises during market panic; the basis for hedging. prereqs: correlation, VIX behaviour
- **CONCEPT:** VIXY as a short-term VIX ETF — an ETF tracking short-term VIX futures, used as the hedge leg versus the SPY long. prereqs: VIX, VIXY instrument
- **CONCEPT:** Hedge ratio — the quantity of VIXY per unit of SPY (e.g. 0.5); capital is allocated between legs in this ratio. prereqs: position sizing
- **CONCEPT:** Hedged daily returns — SPY daily return plus 0.5 × VIXY daily return (scaled by hedge ratio). prereqs: returns, weighting
- **CONCEPT:** Portfolio weighted return — dividing the summed returns by (1 + hedge_ratio) so the combined position normalises to one unit of capital. prereqs: weighting, normalisation
- **CONCEPT:** Cumulative portfolio return — compounding the hedged portfolio returns and comparing its equity curve to SPY alone to check hedging benefit. prereqs: cumprod, equity curve
- **CONCEPT:** VIXY monthly-return heatmap — a seaborn heatmap of VIXY returns by (year, month) showing that VIXY is negative most months—revealing that always-long hedging drags portfolio profitability. prereqs: resampling, heatmap
- **CONCEPT:** Selectivity motivation — because VIX only spikes rarely, going selectively long on VIXY (only when fear rises) improves the hedge strategy; addressed in the next section. prereqs: VIX regime behaviour
## MODULE: Selective Long on VIX
### LESSON: Going Selectively Long on VIX (`Going Selectively Long on VIX.ipynb`)
- **CONCEPT:** Selectively long VIX — holding VIXY (the hedge) only when volatility is rising, since VIX rises only during infrequent panic episodes; improves return vs always-long hedging. prereqs: VIX hedging, fear regime
- **CONCEPT:** Entry trigger with Bollinger upper band — going long VIXY when the 5-period SMA of VIXY close crosses above the upper Bollinger band (timeperiod 60, nbdevup 1.5). prereqs: SMA, Bollinger bands
- **CONCEPT:** Exit trigger on reversion — exiting the VIXY long when the 5-SMA falls back below the upper band. prereqs: bands, SMA crossover
- **CONCEPT:** Multi-period indicators — a short 5-period SMA versus a longer 60-period upper band set the hedge-timing regime. prereqs: indicator periods
- **CONCEPT:** Signal & capital margin — when no VIXY position is held, that allocated capital sits as cash; only the SPY long accrues returns. prereqs: positions, cash margin
- **CONCEPT:** Strategy returns — signal-gated VIXY returns (× hedge ratio) plus SPY returns, normalised by (1 + hedge ratio), then compounded. prereqs: hedging, weighted returns, cumprod
- **CONCEPT:** Conclusion — selectively-long VIXY outperforms always-long VIXY because VIX gains are rare; suggestions include futures data, dynamic hedge ratio, and shorting SPY when long VIXY. prereqs: comparison, enhancement ideas
## MODULE: VIX Spread
### LESSON: VIX Spread Strategy (`VIX Spread Strategy.ipynb`)
- **CONCEPT:** VIXM — an ETF tracking medium-term VIX futures, used as the long leg to hedge the short leg. prereqs: VIX futures ETFs
- **CONCEPT:** VIXY short bias — instead of always long VIX (which loses money), going short VIXY is more prudent, but a short exposes the portfolio to rising-VIX panic losses. prereqs: short positions, VIX behaviour
- **CONCEPT:** Long-short VIX spread — hedging the short VIXY exposure with a long VIXM position, forming a market-neutral-style VIX spread. prereqs: long/short, hedging
- **CONCEPT:** Hedge ratio for the spread — 3 contracts of VIXM per 1 contract of short VIXY (hedge_ratio = 3). prereqs: relative sizing, hedging
- **CONCEPT:** Leg returns — VIXM daily returns scaled by the hedge ratio and VIXY returns negated (−1 for the short leg). prereqs: returns, sign flipping
- **CONCEPT:** Portfolio weighted return — summed leg returns divided by (1 + hedge ratio) to normalise the combined spread position. prereqs: normalisation, weighting
- **CONCEPT:** Cumulative spread return — compounding the long-short portfolio returns and plotting to evaluate the VIX-spread strategy's performance vs VIXY alone. prereqs: cumprod, equity curve
## MODULE: Capstone Project
### LESSON: Capstone Project (`Capstone_Project_Model_Solution.ipynb`)
- **CONCEPT:** Capstone study — a full-cross-section backtest applying the Bollinger breakout strategy to the entire S&P 500 stock universe to identify the best performers. prereqs: breakout strategy, backtesting
- **CONCEPT:** Multi-stock panel data — reading S&P 500 constituent prices over 2010–2022 with a multi-level (ticker, field) column header via `header=[0, 1]`. prereqs: multiindex columns
- **CONCEPT:** `str_perf` strategy function — a reusable function that, for one stock, builds Bollinger bands, computes bandwidth + rolling width, generates the breakout signal and an ATR/exits-free long-only run with middle-band take-profit, then returns the Sharpe, CAGR, and MDD via the `qa` helper. prereqs: breakout signal, band take-profit
- **CONCEPT:** Band-width break-out entry — entering a long when bandwidth exceeds its rolling mean AND High breaches the upper band, consistent with the breakout strategy. prereqs: bandwidth, breakout
- **CONCEPT:** Middle-band take-profit exit — exiting the long when Close exceeds the middle band (a tighter mean-reversion-style objective for the capstone variant). prereqs: Bollinger middle band, exit rules
- **CONCEPT:** Trading-cost-adjusted PnL — per-trade PnL minus trading cost (close × 0.0002 × 2). prereqs: PnL, transaction costs
- **CONCEPT:** Cross-sectional backtest loop — iterating every ticker, running `str_perf`, and storing each stock's Sharpe/CAGR/MDD in a results dataframe; a try-except skips stocks that fail to generate trades. prereqs: loops, error handling, results collection
- **CONCEPT:** Selecting the best five stocks — ranking stocks by Sharpe ratio and choosing the top five performers for the portfolio recommendation. prereqs: sorting, ranking, Sharpe


====================
APPENDIX — CORE CONCEPTS LIBRARY (prerequisite definitions)
====================

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