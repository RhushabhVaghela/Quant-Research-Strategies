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