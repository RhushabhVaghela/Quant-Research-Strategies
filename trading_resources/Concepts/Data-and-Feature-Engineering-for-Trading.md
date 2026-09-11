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