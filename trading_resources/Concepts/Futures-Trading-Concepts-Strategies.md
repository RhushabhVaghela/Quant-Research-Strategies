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