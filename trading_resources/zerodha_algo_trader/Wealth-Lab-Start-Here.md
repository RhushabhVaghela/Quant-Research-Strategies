# Wealth Lab — Start Here

## The rule that protects the experiment

The ₹30,000 is **not trading capital yet**. It is reserved experiment capital.

No live order, options/futures trade, leverage, or automated execution until a written strategy has passed the gates below. API credentials are never placed in notebooks, commits, screenshots, or shared files.

## What we are building

A repeatable research loop:

`question → hypothesis → data → rules → backtest → costs/risk → out-of-sample check → paper trade → tiny live test`

The first objective is not to double capital. It is to learn whether a specific rule has a plausible, repeatable edge after realistic frictions.

## Learning order (ignore everything else for now)

| Phase | Why it comes now | Resource to use | Output |
|---|---|---|---|
| 1. Foundations | Learn the minimum Python, market-data, signal, and backtest vocabulary. | `Getting-Started-with-Algorithmic-Trading-20250416T104101Z-001.zip`: *My First Jupyter Notebook*, *DataFrame and Basic Functionality*, *Data Visualisation*, *Moving Average Crossover Strategy* | Explain one rule in plain English. |
| 2. Honest testing | Learn why a pretty chart is not evidence. | `Backtesting-Trading-Strategies.zip`: data quality, signals, backtest/trade sheet, transaction costs/slippage, performance metrics, risk management | A backtest with declared assumptions. |
| 3. Data plumbing | Get historical data safely and reproducibly; read-only only. | `D:\Zerodha AlgoTrader\6 - Fetching and Resampling Historical Data.ipynb` | Saved, documented dataset. |
| 4. Risk | Decide loss limits before testing more ideas. | `Position-Sizing-Resources.zip`: fixed sum, fixed percentage, volatility targeting | A sizing rule. |
| 5. Strategy variations | Test one modification at a time. | Technical Indicators / Price Action / Event Driven resources | Research log with rejected and surviving ideas. |
| Later, only if justified | ML, neural nets, LLMs, RL, options, shorting, stat-arb. | The corresponding course archives | Never use these to skip the earlier validation gates. |

## Strategy 0: our learning baseline

**Name:** Daily trend-following moving-average crossover.

| Question | Answer for this first experiment |
|---|---|
| What? | Hold one liquid, non-leveraged Indian equity ETF when its short moving average is above its long moving average; otherwise hold cash. |
| Why this? | The calculation and rule are visible. It teaches the entire research cycle without pretending a complex model is an edge. |
| When does it act? | Once per day, after the daily candle is complete. The earliest assumed fill is the next session's open (or a clearly declared alternative). |
| How is the signal made? | Begin with 20-day and 50-day simple moving averages. Buy/hold when SMA20 > SMA50; exit to cash when SMA20 ≤ SMA50. |
| What is deliberately excluded? | Intraday trading, derivatives, short selling, leverage, discretionary overrides, optimization across many parameters, and live execution. |
| What must be modelled? | Brokerage/fees/taxes assumptions, bid–ask/slippage estimate, one-day signal-to-fill delay, missing data, and cash periods. |
| What would count as failure? | No robust out-of-sample advantage after costs, intolerable drawdown, or results that disappear with small sensible changes to dates/parameters. |

This is a **baseline, not a recommendation to buy an ETF or a claim of profitability**.

## Validation gates

1. **Specification first:** record the instrument, dates, data source, entry, exit, execution timing, costs, sizing, and metrics before running it.
2. **In-sample research:** use an earlier period only to understand the rule—do not keep adjusting until it looks good.
3. **Out-of-sample check:** freeze the rules and test on a later untouched period.
4. **Sanity checks:** inspect trades, include costs, compare to buy-and-hold/cash, and test small parameter/date changes.
5. **Paper-trading log:** run the unchanged strategy forward for a meaningful pre-declared period.
6. **Only then consider live:** separate approval, a capped loss budget, and manual confirmation. No automated order placement at this stage.

## Today: a 15-minute win

Your only job is to open the first four notebooks in Phase 1 **in order**. Do not take notes beyond these three answers in a plain text file or chat:

1. What is a DataFrame?
2. What are the two moving averages in the rule?
3. Why can a signal based on today's close not be filled at today's close in an honest backtest?

Stop after 15 minutes even if you feel momentum. Completion is opening the material and answering imperfectly—not understanding every line.

## Anti-boredom operating rule

- Use a 15-minute timer; phone goes outside reach and YouTube stays closed until the timer ends.
- There is one next action only—the "Today" action above. Do not browse course folders.
- At the end, leave a one-sentence log: `date — opened X — learned Y — next action Z`.
- If you skip a day, restart with 15 minutes; no catching up and no self-lecture.

## Questions to ask before every action

1. What exact decision or claim will this action help us make?
2. Why is this the smallest useful next step?
3. What data and assumptions does it require?
4. Could it leak future information, omit costs, or overfit?
5. What result would make us stop or reject the idea?
6. Does it create any possibility of a live order? If yes, stop unless it has passed the validation gates.

## What not to do today

Do not open notebooks 7–10 in the Zerodha folder. Those concern futures, placing/modifying orders, and positions; they are useful much later but are distractions and create avoidable execution risk right now.
