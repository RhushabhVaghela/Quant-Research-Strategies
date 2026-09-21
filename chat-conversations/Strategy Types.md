# Strategy Types

# 1. Mean reversion

We have:

```
mean_reversion_strategy.py
mean_reversion_strategy_2.ipynb
```

And our own Strategy 001 originally began here.

### Basic idea

If something moves unusually far from its normal level:

```
Price too high
     ↓
short

Price too low
     ↓
long
```

Expected:

```
extreme → normal
```

### Variations available

Mean reversion can be:

### Time-series

One stock versus its own history.

Example:

```
GOLDBEES is 3 standard deviations above its recent mean
→ short
```

### Cross-sectional

One stock versus peers.

This is closer to Strategy 002.

### Pairs/statistical arbitrage

Two related instruments diverge:

```
A ↑↑
B ↑
```

Then:

```
short A
long B
```

expecting convergence.

We also have:

```
pairs_trading_strategy.py
pairs_trading_strategy_2.py
```

### Useful?

**Very useful**, but only when:

- the relationship is real
- the deviation is meaningful
- transaction costs aren't larger than the expected convergence

Strategy 002 demonstrated exactly why the third condition matters.

------

# 2. Momentum / continuation

We have many resources:

```
intraday_momentum_strategy.py
long_short_momentum_trading_strategy.py
time_series_momentum_strategy.py
moving_average_crossover_momentum_strategy.py
technical_indicators_based_momentum_strategy.py
creating_momentum_based_portfolio_strategy.py
```

And Strategy 001 itself evolved into this category.

### Basic idea

Instead of:

```
up → down
```

you hypothesize:

```
up → continue up
down → continue down
```

Momentum can operate at:

- intraday horizon
- daily horizon
- cross-sectional horizon
- trend-following horizon

This is a completely different mechanism from Strategy 002.

### Very useful?

Yes.

Momentum is one of the most important strategy families to test.

------

# 3. Pairs trading / statistical arbitrage

Resources:

```
pairs_trading_strategy.py
pairs_trading_strategy_2.py
```

Plus WQU material on:

- correlation
- cointegration
- error correction
- PCA
- dependence
- time series

The actual mechanism:

```
Find related assets
       ↓
Estimate normal relationship
       ↓
Relationship deviates
       ↓
Trade the spread
       ↓
Expect convergence
```

Example:

```
Stock A and Stock B normally move together.

A suddenly becomes expensive relative to B.

Short A
Long B
```

### Very useful?

Potentially very useful.

But it has serious research requirements:

- stable relationship
- cointegration or appropriate dependence
- hedge ratio
- structural-break detection
- borrow/short constraints
- transaction costs
- simultaneous execution

This is a major candidate family for us.

------

# 4. Volatility strategies

This repository has **a lot** here.

Examples:

```
GARCH.py
forward_volatility_strategy.py
volatility_targeting_method.py
volatility_skew_strategy.ipynb
volatility_smile_strategy.ipynb
```

And WQU has:

- ARCH
- GARCH
- stochastic volatility
- Heston
- volatility smiles
- local volatility
- implied volatility
- option pricing
- jump diffusion

### Basic idea

Instead of predicting:

> "Will price go up?"

we predict:

> **"How much will price move?"**

This opens an entirely different strategy universe.

For example:

```
Implied volatility
       ↓
Realized volatility
```

If options imply more volatility than subsequently occurs, there may be volatility-selling opportunities.

Or:

```
forecast volatility
       ↓
position sizing
```

rather than directional trading.

### Very useful?

**Extremely useful for derivatives**, but much more complicated.

------

# 5. Options strategies

The repository has:

```
short straddle
short butterfly
butterfly
volatility skew
volatility smile
option expiration effects
option ML
option decision trees
```

Plus extensive WQU derivative-pricing resources.

So we have the theoretical foundation for:

- straddles
- butterflies
- volatility trades
- skew trades
- smile trades
- expiry effects
- implied volatility
- stochastic volatility
- Greeks
- option pricing

This is probably the largest unused strategy family in our project.

### But there's a major problem

Options introduce:

```
strike
expiry
Greeks
implied volatility
bid/ask
lot size
margin
theta
gamma
vega
liquidity
rollover
```

With a small account, execution feasibility becomes critical.

So options are potentially valuable, but they should probably initially be **research/paper strategies**, not automatically live strategies.

------

# 6. FX value strategies

We have:

```
fx_value_strategy.ipynb
value_forex_strategy.py
```

This is a different mechanism.

Instead of short-term price patterns:

> Is a currency fundamentally or statistically cheap/expensive relative to some economic valuation measure?

This opens:

- carry
- value
- momentum
- mean reversion

within FX.

This would also give us a genuinely different asset class.

------

# 7. Volume / order-flow strategies

We have:

```
volume_reversal_strategy.py
backtesting_order_flow_strategy.ipynb
```

This is particularly interesting.

Instead of using only:

```
price
```

we examine:

```
volume
order flow
buy/sell pressure
```

The idea could be:

```
unusual volume / imbalance
        ↓
information about future price
```

This can potentially lead to:

- volume reversal
- volume momentum
- order-flow imbalance
- liquidity shock strategies

These are especially interesting for intraday research.

------

# 8. Technical indicator strategies

The repo has:

```
RSI
moving averages
Ichimoku
candlestick patterns
support levels
divergence
```

Examples:

```
relative_strength_index_strategy.py
moving_average_strategy.py
ichimoku_cloud_strategy.py
candlestick_pattern_strategy.py
support_level_strategy.py
divergence_strategy.py
```

These are useful as **baseline ideas**.

But I would be careful.

A technical indicator itself is not an economic mechanism.

For example:

> RSI < 30

doesn't automatically mean:

> buy.

We would need to discover whether the indicator captures:

- momentum
- exhaustion
- volatility
- liquidity
- behavioral bias
- trend regime

So these resources are useful, but we should not blindly backtest dozens of indicators.

That would create massive multiple-testing problems.

------

# 9. Fundamental / value strategies

We have explicit:

```
FX value
```

and various portfolio/value resources, but the repository currently does **not** contain a mature end-to-end equity fundamental alpha engine comparable to the intraday infrastructure.

This is an important gap.

A proper fundamental strategy would require:

```
Financial statements
        ↓
Point-in-time fundamentals
        ↓
Quality/value/profitability factors
        ↓
Portfolio construction
        ↓
Long/short or long-only
        ↓
Rebalance
```

The biggest challenge is **point-in-time fundamentals**.

If we use today's financial statement values to backtest ten years ago, we create look-ahead bias.

So fundamental strategies are possible, but we need the data layer first.

------

# 10. Machine-learning strategies

We have an enormous amount of ML material.

Examples include:

- decision trees
- random forests
- XGBoost
- SVM
- MLP
- classification
- regression
- clustering
- hierarchical clustering
- PCA
- ensemble learning
- boosting
- neural networks
- deep learning
- hyperparameter tuning

We even have:

```
Bitcoin trading strategy
```

and various ML trading examples.

### ML strategy architecture

Conceptually:

```
Market data
    ↓
Features
    ↓
ML model
    ↓
Probability / forecast
    ↓
Trading decision
```

For example:

```
momentum
volatility
volume
market return
RSI
cross-sectional rank
      ↓
XGBoost
      ↓
P(up next 30 min)
      ↓
trade if probability > threshold
```

### Is this useful?

Yes—but **later**.

Our methodology explicitly says:

> Establish a simple baseline before ML.

That is exactly what we did in Strategy 002.

ML should not be:

> "Let's throw XGBoost at the data and see what happens."

It should be:

```
economic pattern
      ↓
simple baseline
      ↓
ML potentially improves conditional prediction
```

Otherwise overfitting becomes enormous.

------

# 11. Clustering / regime strategies

We have:

```
k_means_strategy.py
k-means_clustering_strategy.ipynb
```

and WQU resources on:

- k-means
- hierarchical clustering
- PCA
- unsupervised learning
- networks

This can be used to identify:

### Similar stocks

```
Cluster A:
Banks

Cluster B:
IT

Cluster C:
Energy
```

or behavioral regimes:

```
High-volatility regime
Low-volatility regime
Trending regime
Mean-reverting regime
```

Then the strategy changes behavior according to the regime.

This is potentially very useful for improving strategies without simply adding arbitrary filters.

------

# 12. Time-series statistical models

The WQU resources are very strong here.

We have:

### AR

```
future return depends on past returns
```

### ARIMA

```
time-series forecasting
```

### GARCH

```
volatility forecasting
```

### VAR

```
multiple time series influence each other
```

### VECM / cointegration

```
multiple related non-stationary series
with stable long-run relationship
```

### Granger causality

```
Does information in A help predict B?
```

These are particularly relevant to:

- momentum
- mean reversion
- pairs trading
- macro
- cross-asset prediction
- volatility strategies

------

# Part 4 — Portfolio construction resources

This is another strong section.

We have:

```
Modern Portfolio Theory
Kelly Criterion
Hierarchical Risk Parity
Constant Proportion Portfolio Insurance
Volatility Targeting
```

These answer a different question.

A strategy tells us:

> **What should we trade?**

Portfolio construction asks:

> **How much should we trade?**

For example:

Suppose we have:

```
Strategy A
Strategy B
Strategy C
Strategy D
```

We don't necessarily put:

```
₹25k each
```

into them.

We could use:

### Volatility targeting

Give each strategy similar risk.

### HRP

Group correlated strategies and allocate according to hierarchical risk structure.

### Kelly

Use estimated expected return and risk to determine theoretically optimal sizing.

But Kelly is especially sensitive to estimation error, so we should be conservative.

------

# Part 5 — Risk-management resources

We have:

- volatility targeting
- stop-loss
- position management
- portfolio insurance
- drawdown analysis
- MFE/MAE
- trade distributions
- execution sensitivity

This is good because we don't want:

```
signal → trade
```

to be the entire system.

A real strategy needs:

```
Signal
 ↓
Position sizing
 ↓
Execution
 ↓
Risk controls
 ↓
Monitoring
 ↓
Kill switch
```

------

# Part 6 — Stochastic modeling

The WQU material gives us another entire toolbox:

### Heston

Stochastic volatility.

### Merton

Jump diffusion.

### Bates

Stochastic volatility + jumps.

### Interest-rate models

Useful for fixed-income/macro strategies.

### Markov models

Regime modeling.

### Hidden Markov Models

Latent market regimes.

### Reinforcement learning

Sequential decision-making.

### Network theory

Relationships between assets.

These are more advanced methods.

They aren't necessarily the first tools we should use, but they're available.

------

# Part 7 — Reinforcement learning

We have resources for:

- Q-learning
- portfolio rotation
- asset allocation
- RL on real-world price data
- live RL templates

Conceptually:

```
State
 ↓
Action
 ↓
Reward
 ↓
New state
 ↓
learn
```

For trading:

```
market state
    ↓
buy / sell / hold
    ↓
profit/loss
    ↓
learn policy
```

This is interesting, but I would put it **far later** in our research pipeline.

Why?

Because RL can easily learn:

> "the quirks of this historical dataset"

rather than a genuine market mechanism.

------

# Part 8 — Zerodha execution infrastructure

This is actually one of the most practically valuable parts of the repository.

We have resources for:

- authentication
- access tokens
- instrument lists
- live quotes
- historical data
- futures
- open interest
- WebSockets
- order placement
- order monitoring
- positions
- holdings
- stop-loss orders
- GTT/AMO
- iceberg orders
- cover orders
- automated trading system
- low-frequency trading

This is why we were able to perform Strategy 001I prospective shadow testing and Strategy 001J/002 data acquisition using actual broker infrastructure.

So the repo isn't just theoretical.

It has a path from:

```
research
→ data
→ signal
→ paper
→ broker
```

although the final live-execution layer still requires the safety/compliance gates documented in Phase 0.

------

# Part 9 — The most important research methods we have

If I simplify the entire repository into a toolbox, I would organize it like this:

| Method                   | Simple meaning                               | Best use                     |
| ------------------------ | -------------------------------------------- | ---------------------------- |
| Event study              | What happens after X?                        | Pattern discovery            |
| Autocorrelation          | Does the past predict the future?            | Momentum/reversal            |
| Cross-sectional residual | Who unusually outperformed peers?            | Stat arb                     |
| Leave-one-out residual   | Peer comparison without self-contamination   | Relative value               |
| Correlation              | Do assets move together?                     | Pairs/portfolio              |
| Cointegration            | Do assets maintain a long-run relationship?  | Pairs                        |
| PCA                      | What common factors drive assets?            | Factor/relative value        |
| Clustering               | Which assets behave similarly?               | Universe/regime              |
| Hurst exponent           | Trend-like or mean-reverting behavior?       | Time-series characterization |
| AR/ARIMA                 | Forecast time series                         | Forecast strategies          |
| GARCH                    | Forecast volatility                          | Volatility strategies        |
| Granger causality        | Does A contain predictive information for B? | Lead-lag                     |
| GARCH/Heston             | Model volatility dynamics                    | Options                      |
| Implied volatility       | What volatility is priced into options?      | Volatility trading           |
| ML classification        | Predict direction/class                      | ML alpha                     |
| ML regression            | Predict return/magnitude                     | ML alpha                     |
| XGBoost                  | Powerful nonlinear prediction                | ML                           |
| Random forest            | Ensemble nonlinear prediction                | ML                           |
| PCA                      | Compress correlated variables                | Factor/ML                    |
| HMM                      | Identify hidden regimes                      | Regime strategies            |
| RL                       | Learn sequential actions                     | Portfolio/trading policy     |
| HRP                      | Allocate across correlated assets            | Portfolio construction       |
| Kelly                    | Risk-sensitive sizing                        | Position sizing              |
| Volatility targeting     | Keep portfolio risk stable                   | Risk management              |
| MFE/MAE                  | What happened during a trade?                | Exit/risk design             |
| Cost sensitivity         | Does the edge survive costs?                 | Economic validation          |
| PIT replay               | What information was actually known?         | Anti-lookahead               |
| Chronological holdout    | Test on unseen future                        | Validation                   |
| Shadow trading           | Test live data without capital               | Operational validation       |

------

# Part 10 — Which resources are most useful for us?

This is where I want to make an important distinction.

Not every method deserves equal priority.

## Tier 1 — Extremely useful

These should be part of almost every future strategy:

### 1. Data audit

Essential.

### 2. Event studies

Extremely useful for pattern discovery.

### 3. Point-in-time controls

Essential.

### 4. Chronological validation

Essential.

### 5. Cost/slippage analysis

Essential.

### 6. Cross-sectional analysis

Very useful.

### 7. Correlation/covariance

Very useful.

### 8. PCA

Very useful for cross-sectional strategies.

### 9. Cointegration

Very useful for pairs/stat-arb.

### 10. Volatility analysis

Useful across almost everything.

### 11. Trade-level decomposition

Extremely useful.

### 12. Portfolio construction

Essential once we have multiple strategies.

------

# Part 11 — Tier 2: highly useful for specific strategies

These are excellent, but not universal.

### GARCH

For volatility forecasting.

### ARIMA

For certain time-series forecasting problems.

### Hurst

For diagnosing trend vs mean reversion.

### Clustering

For universe construction and regime identification.

### HMM

For regime strategies.

### Granger causality

For lead-lag relationships.

### Options volatility surface

For options strategies.

### Open interest

For derivatives strategies.

------

# Part 12 — Tier 3: use later

These aren't bad methods.

They are simply more dangerous/complex.

### Deep learning

### Reinforcement learning

### Large ML ensembles

### Huge feature sets

### Massive hyperparameter searches

These can produce very impressive backtests.

They can also produce extremely convincing nonsense.

That's why our methodology deliberately says:

```
Pattern
 ↓
Simple hypothesis
 ↓
Simple strategy
 ↓
Validation
 ↓
Only then consider ML
```

------

# Part 13 — What genuinely different strategies can we build from this repository?

Now we can connect this to your original portfolio objective.

We wanted strategies that are **economically different**, not just:

> same strategy with different parameters.

The repository supports something like:

### Strategy A — Time-series momentum

```
Asset moves strongly
↓
continue in same direction
```

### Strategy B — Cross-sectional mean reversion

```
Stock unusually underperforms peers
↓
revert
```

That's essentially what Strategy 002 investigated.

### Strategy C — Pairs/statistical arbitrage

```
A/B relationship deviates
↓
spread converges
```

Different from Strategy 002.

### Strategy D — Volatility forecasting

```
forecast future volatility
↓
trade volatility / adjust exposure
```

Different mechanism.

### Strategy E — Options volatility/skew

```
implied volatility surface mispricing
↓
options position
```

Different mechanism and asset class.

### Strategy F — Volume/order flow

```
unusual trading pressure
↓
future price response
```

Different information source.

### Strategy G — Fundamental/value

```
fundamentally cheap/expensive
↓
long/short
```

Very different horizon and information source.

### Strategy H — Regime-switching strategy

```
identify market regime
↓
apply appropriate strategy
```

Different architecture.

### Strategy I — FX value/carry

Different asset class.

### Strategy J — Crypto momentum / regime

Different asset class and market structure.

------

# Part 14 — What I think we have learned from Strategy 001 + 002

This is actually more valuable than simply having two strategies.

## Strategy 001 taught us:

A backtest can show:

```
gross edge
```

while:

```
costs
frequency
capacity
```

make it unsuitable.

And a strategy can have an interesting economic phenomenon without being useful for the current capital/time constraints.

------

## Strategy 002 taught us something different

Even when:

```
pattern
      ↓
mechanism
      ↓
temporal stability
      ↓
frozen baseline
```

all look promising, the final question remains:

> **Can we actually extract enough money from the signal after execution costs?**

The answer for the current Strategy 002 implementation is currently:

**not demonstrated.**

That is a very useful research result.

------

# Part 15 — One repository issue I noticed

There is one documentation inconsistency we should be aware of.

Some older README text still describes Strategy 002 as:

> "active research — no hypothesis selected"

and says that the leave-one-out/temporal work was still pending.

That text is now **behind the actual research state**.

The current state is further along:

```
hypothesis established
↓
baseline frozen
↓
validation completed
↓
cost-resilience gate failed
```

We already updated the Strategy 002 registry and added:

```
research/journal/002_validation_findings.md
```

but the top-level README/research README contain older narrative sections that should eventually be synchronized.

I would **not modify them blindly right now**, because we're doing the repository review first. We should make a deliberate documentation cleanup after we finish deciding Strategy 002's next research action.

------

# Part 16 — The big picture

If I reduce our entire project to one diagram, it now looks like this:

```
                    QUANT RESEARCH REPOSITORY
                              │
          ┌───────────────────┴───────────────────┐
          │                                       │
    RESEARCH ENGINE                         RESOURCE LIBRARY
          │                                       │
   ┌──────┼──────┐                     ┌──────────┼──────────┐
   │      │      │                     │          │          │
 Data  Statistics Strategy          Quantra     WQU      Zerodha
   │      │      │
   │      │      ├── Momentum
   │      │      ├── Mean reversion
   │      │      ├── Stat arb
   │      │      ├── Volatility
   │      │      ├── Options
   │      │      ├── ML
   │      │      └── etc.
   │      │
   └──────┴───────────────┐
                          ↓
                  Pattern discovery
                          ↓
                   Economic mechanism
                          ↓
                     Hypothesis
                          ↓
                    Simple baseline
                          ↓
                    Development
                          ↓
                     Validation
                          ↓
                       Holdout
                          ↓
                  Paper / Shadow
                          ↓
                  Controlled Live
```

