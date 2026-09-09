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