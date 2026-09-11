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