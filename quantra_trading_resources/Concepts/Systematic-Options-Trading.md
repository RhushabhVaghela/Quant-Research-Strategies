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