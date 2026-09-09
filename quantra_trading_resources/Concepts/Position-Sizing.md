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