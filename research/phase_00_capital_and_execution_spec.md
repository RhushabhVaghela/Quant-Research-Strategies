# Phase 0 — ₹30,000 Capital & Execution Feasibility Specification

**Status:** Research specification.

## 1. Why this document exists

The project is being developed around a personal trading account with approximately **₹30,000** of available capital. The strategy therefore has to be economically executable at small size.

A strategy is not considered feasible merely because its backtest has a high Sharpe ratio. It must survive the constraints imposed by position size, spreads, turnover, transaction costs, liquidity and execution.

## 2. Capital is a constraint, not a target

We will not assume that the full ₹30,000 should be deployed.

Conceptually:

```text
Total account capital
        │
        ├── reserve / unallocated cash
        │
        └── strategy capital
                │
                ├── current position exposure
                └── available risk budget
```

The exact allocation will be determined after strategy research. Until then, **no live deployment amount is prescribed**.

## 3. Position-sizing feasibility

For every candidate instrument and strategy we will calculate:

- price per unit;
- quantity affordable with the strategy allocation;
- gross notional exposure;
- stop distance, if applicable;
- rupee loss at stop;
- percentage of account capital at risk;
- estimated entry cost;
- estimated exit cost;
- spread/slippage sensitivity;
- expected turnover.

A strategy that produces a statistically attractive signal but cannot express it economically with small capital will be rejected or redesigned.

## 4. Cost model

The research backtester must support configurable costs rather than silently assuming zero-cost execution.

For each round trip, model as applicable:

```text
Gross P&L
- brokerage
- STT
- exchange transaction charges
- GST
- SEBI charges
- stamp duty
- bid/ask spread
- slippage / market impact
= Net P&L
```

The exact rates must be maintained as dated assumptions and re-verified before live deployment. They must not be presented as timeless constants.

## 5. Liquidity policy

A candidate instrument should not enter the final universe solely because it has historical OHLCV data.

We need to examine, where data permits:

- traded volume;
- turnover;
- price level;
- frequency of zero/low-volume bars;
- spread or proxy for spread;
- frequency of large gaps;
- ability to enter and exit at the intended size;
- sensitivity of results to adverse execution.

If reliable bid/ask data is unavailable, backtests must use conservative slippage assumptions rather than pretending that the close price is an executable fill.

## 6. Strategy turnover policy

Small-capital strategies are especially sensitive to excessive turnover.

Therefore every strategy report must include:

- number of trades;
- average holding time;
- trades per day;
- turnover;
- gross P&L;
- estimated costs;
- net P&L;
- cost as a percentage of gross edge;
- worst-case/slippage sensitivity.

A strategy whose edge disappears under modestly worse execution assumptions should not proceed.

## 7. Capital-feasibility tiers

Candidate strategies will be classified as:

### Tier A — Directly feasible

Can be expressed with the ₹30,000 account without requiring leverage or unrealistic position sizing, and remains viable after conservative costs.

### Tier B — Research-feasible, live-capital constrained

The research idea is valid but the current account is too small for meaningful live deployment. It may remain useful as a portfolio/research project.

### Tier C — Not feasible for this account

Requires leverage, derivatives margin, excessive turnover, or execution conditions that are inappropriate for the current capital constraint.

## 8. Initial product preference

For the first strategy family, prioritize **NSE cash equities and ETFs**.

Reasons:

- simpler contract mechanics;
- no expiry/roll model for cash instruments;
- no futures margin requirement;
- no option-strike/expiry/Greeks complexity;
- easier explanation and reproducibility;
- suitable for testing whether an intraday statistical edge exists before adding derivatives complexity.

This is a research preference, not a claim that cash equities are always superior.

## 9. NIFTYBEES role

NIFTYBEES remains in the repository as the **first pipeline-validation instrument** because its historical data successfully exercised the Zerodha instrument-resolution, download, validation and audit layers.

It is not yet selected as the final strategy instrument.

The next universe study should compare multiple liquid NSE instruments before strategy selection.

## 10. Live-deployment rule

No real-money deployment occurs merely because:

- the backtest is profitable;
- the Sharpe ratio is high;
- an ML classifier has high accuracy;
- a paper-trading period is positive.

Live deployment requires the complete evidence chain:

```text
Economic hypothesis
→ clean data
→ event evidence
→ baseline
→ realistic costs
→ out-of-sample validation
→ walk-forward stability
→ paper/shadow trading
→ execution validation
→ controlled live test
```

## 11. Current decision

**Do not deploy the ₹30,000 account yet.**

The account is currently a future validation resource. The immediate task is to determine which strategy families and instruments are economically compatible with it.
