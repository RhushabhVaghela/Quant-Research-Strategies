# Strategy 001 — GOLDBEES Intraday Mean Reversion

**Status:** 🔴 Original mean-reversion hypothesis rejected; 🟡 continuation hypothesis promoted to Strategy 001D candidate backtest

## Research question

Does an unusually large short-term deviation of GOLDBEES from its recent intraday equilibrium tend to be followed by a statistically meaningful move back toward that equilibrium?

## Why GOLDBEES?

GOLDBEES is the first instrument selected for this strategy research because it is accessible for eventual small-account validation and allows us to study an intraday hypothesis without starting with derivatives. Its lower nominal unit price is useful for later capital-feasibility analysis, but **price alone is not evidence of profitability**. The strategy must first demonstrate an edge after realistic costs and execution assumptions.

## Research discipline

This experiment was deliberately an **event study before a trading backtest**. We did not optimize a trading rule until we had evidence about the underlying relationship.

The sequence is:

1. Define the hypothesis before examining the result.
2. Measure the deviation using only information available at the event bar.
3. Measure future returns only after the event.
4. Keep forward returns within the same trading session.
5. Separate positive and negative deviations.
6. Report sample size and distribution, not only average return.
7. Record negative and inconclusive results rather than deleting them.
8. Only promote a hypothesis after statistical and economic evidence justifies doing so.

## Experiment 001 — Baseline deviation event study

### Hypothesis

When GOLDBEES closes unusually far from its recent intraday mean, the subsequent return should tend to have the opposite sign if a short-term mean-reversion effect exists.

The initial implementation used a configurable default lookback of **30 five-minute bars** and an absolute z-score threshold of **2.0**. These were research defaults, not optimized parameters.

### Prediction target

For each event, calculate same-session forward close-to-close returns over 1, 3, 6, and 12 bars (5, 15, 30, and 60 minutes). For mean reversion, positive deviation should be followed by negative return and negative deviation by positive return.

### Result

The GOLDBEES dataset contained **30,912 five-minute bars** from January 2025 through August 2026. The baseline event study produced **2,953 combined directional event observations**.

The symmetric mean-reversion hypothesis was **rejected**. Reversion-aligned mean returns were negative at every tested horizon:

| Horizon | Mean reversion-aligned return |
|---|---:|
| 5 min | -0.00365% |
| 15 min | -0.00901% |
| 30 min | -0.01703% |
| 60 min | -0.02105% |

Positive deviations instead showed positive average forward returns, increasing from approximately **+0.00764% at 5 minutes** to **+0.05577% at 60 minutes**. Negative deviations were weaker and inconsistent.

### Decision

**REJECTED as a symmetric mean-reversion signal.**

We did not convert this into a trading rule merely because another parameterization might produce a better backtest.

## Experiment 001A — Event Structure & Conditioning Diagnostics

001A tested whether the continuation-like behavior survived dependence controls and whether it was concentrated in predefined conditions. It retained the fixed 30-bar / 2.0-z-score baseline and used a fixed 12-bar non-overlap diagnostic.

### Main findings

- Raw events were highly clustered; the fixed 12-bar non-overlap filter reduced this dependence.
- Positive-deviation continuation remained visible after non-overlap filtering.
- The clearest concentration was positive deviation combined with an existing **upward six-bar prior trend**.
- Negative-deviation behavior was weaker and inconsistent.
- Volume and volatility did not provide a simple primary explanation.
- Late-session and severity concentrations were treated as exploratory only; no parameters were optimized around them.

### Decision

**Symmetric mean reversion remained rejected. Continuation became a promising exploratory lead.**

The unresolved question was whether continuation contained information beyond ordinary intraday drift and the trend already present before the event.

## Experiment 001B — Continuation Attribution

001B asked:

> **Does the continuation-like return after a large deviation contain information beyond ordinary intraday drift and the recent six-bar trend?**

It compared positive and negative deviations, prior-trend regimes, predefined time-of-day buckets, and fixed non-overlapping events against matched non-event observations.

### Result

The strongest subgroup was **positive deviation + prior uptrend**. Event returns exceeded the matched non-event baseline at every tested horizon:

| Horizon | Events | Event mean | Matched baseline | Incremental return |
|---|---:|---:|---:|---:|
| 5 min | 363 | +0.0156% | +0.0025% | **+0.0128%** |
| 15 min | 343 | +0.0202% | +0.0084% | **+0.0113%** |
| 30 min | 299 | +0.0443% | +0.0177% | **+0.0255%** |
| 60 min | 246 | +0.0532% | +0.0270% | **+0.0243%** |

Positive deviations also remained above the matched baseline when trend regimes were pooled. Negative deviations did not show the symmetric reversal pattern expected under mean reversion.

### Decision

**PROMISING RESEARCH LEAD.**

The evidence was sufficient to stop investigating whether the original symmetric mean-reversion relationship should become a strategy. It should not.

The evidence was also sufficient to formalize a continuation hypothesis. However, 001B was not a validated trading strategy because the non-event comparison was a full-sample descriptive attribution benchmark and costs, execution, and chronological out-of-sample stability had not been tested.

Detailed results are recorded in `research/journal/001B_continuation_attribution_results.md`.

## Experiment 001C — Point-in-Time Continuation Validation

001C froze the continuation hypothesis before parameter or instrument selection and replaced the descriptive full-sample benchmark with a strictly point-in-time benchmark.

### Frozen rule

> **When a 5-minute bar closes at least 2.0 standard deviations above the previous 30 completed closes and the prior six-bar return is positive, the subsequent 30-minute return should be positive and stronger than the historical point-in-time return of comparable non-event observations.**

The trading convention associated with this frozen hypothesis is next-bar-open entry and close-of-`t+6` exit.

### Result

The GOLDBEES implementation produced **1,668 frozen events** and **401 selected non-overlapping events** under the fixed 12-bar cooldown.

For the positive/uptrend continuation condition:

| Horizon | Event return | Point-in-time baseline | Incremental return | Positive incremental rate |
|---|---:|---:|---:|---:|
| 5 min | +0.0148% | +0.0032% | **+0.0115%** | 51.2% |
| 15 min | +0.0205% | +0.0099% | **+0.0106%** | 47.8% |
| 30 min | +0.0443% | +0.0194% | **+0.0249%** | 51.0% |
| 60 min | +0.0527% | +0.0279% | **+0.0247%** | 49.0% |

The pre-specified 30-minute primary horizon therefore showed approximately **+2.49 basis points of incremental gross return** relative to the point-in-time matched benchmark.

### Interpretation

The continuation lead **survived the point-in-time benchmark restriction**. This is stronger evidence than the full-sample descriptive attribution in 001B.

It is not yet sufficient to call the effect a tradable alpha. The incremental hit rate is close to 50%, so the positive mean may depend on outcome magnitude. Costs, slippage, drawdown, turnover, execution timing, and chronological out-of-sample stability remain unresolved.

### Decision

**PROMISING — promote the frozen continuation hypothesis to the formal Strategy 001D candidate backtest.**

The original symmetric mean-reversion hypothesis remains permanently **REJECTED**.

Detailed results are recorded in `research/journal/001C_continuation_hypothesis_results.md`.

## Experiment 001D — Formal Trading Backtest

001D converts the frozen 001C hypothesis into an executable baseline without changing the signal rule.

### Frozen execution specification

- 5-minute bars;
- previous 30 completed same-session closes;
- sample standard deviation;
- z-score ≥ +2.0;
- prior six-bar return > 0;
- long-only;
- signal after event-bar close;
- entry at next-bar open;
- exit at close of `t+6`;
- 12-bar session cooldown;
- no overnight trades;
- one position at a time;
- constant-notional normalized accounting;
- no leverage or optimized position sizing;
- no parameter optimization.

The backtest must separately report gross performance and explicit cost/slippage sensitivity. OHLCV data alone cannot reveal exact historical spread and execution quality, so cost assumptions will be transparent scenarios rather than presented as measured historical costs.

### Required outputs

Trade-level:

- signal, entry, and exit timestamps;
- entry and exit prices;
- z-score and prior trend;
- gross return;
- transaction cost;
- slippage;
- net return;
- cumulative equity;
- drawdown.

Portfolio-level:

- trade count;
- total return;
- mean return;
- win rate;
- average win/loss;
- profit factor;
- maximum drawdown;
- Sharpe where a defensible annualization convention exists;
- turnover/exposure proxies.

### Implementation

- `research/journal/001D_formal_strategy_spec.md`
- `src/research/continuation_backtest.py`
- `tests/test_continuation_backtest.py`
- `scripts/run_strategy_001_backtest.py`

### Decision status

**CANDIDATE — implementation committed; historical backtest result pending.**

The first 001D backtest is not a deployment test. It is the next evidence gate before OOS/walk-forward validation and paper trading.

## Research direction

We are no longer asking:

> "Can we make mean reversion work on GOLDBEES?"

We are asking:

> **"Does an unusually large positive move, when combined with an already-positive short-term trend, provide repeatable and executable continuation information?"**

Strategy 001 will remain the active project until it either reaches the paper/live gates or is rejected. Strategy 002 will not begin before Strategy 001 has completed its validation path.

## Next phase

1. Run the 001D baseline backtest on the full GOLDBEES history.
2. Inspect and validate the generated trades against the frozen execution convention.
3. Compare gross results with explicit cost/slippage scenarios.
4. Diagnose return distribution, drawdown, turnover, and concentration.
5. Run predefined robustness tests without changing the baseline rule.
6. Perform chronological out-of-sample / walk-forward validation.
7. If robust, begin paper/shadow trading using the same frozen implementation.
8. If paper evidence is satisfactory, assess controlled live validation with explicit risk limits.

## Current limitations

- No cost-aware Strategy 001D historical result has yet been recorded.
- No out-of-sample or walk-forward test has been performed.
- No paper trading has started.
- No live deployment is justified by the current evidence.
- The original mean-reversion hypothesis remains permanently rejected.
