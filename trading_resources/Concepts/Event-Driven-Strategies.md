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