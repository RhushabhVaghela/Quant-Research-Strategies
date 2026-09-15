# Quant Research Workspace

This directory records the research process behind the intraday strategy portfolio.

## Research principles

- Start with a financial hypothesis, not a model.
- Treat Quantra templates as building blocks/reference material, not finished strategies.
- Prefer intraday strategies with realistic execution paths.
- Establish a simple baseline before adding ML/DL.
- Use time-ordered validation and walk-forward testing where appropriate.
- Prevent look-ahead bias, leakage, survivorship bias, and data snooping.
- Include realistic transaction costs and slippage assumptions.
- Reject strategies that do not remain robust out of sample.
- Never invent expected performance targets before testing.
- Treat the user's ₹30,000 account as a capital constraint, not a target deployment amount.
- Keep research-universe selection independent from strategy performance where possible.
- Paper trading and any eventual small live experiment are validation stages, not guarantees of profitability.

## Current research question

Can we identify repeatable intraday conditions under which a directional price move is more likely to continue or reverse, and use statistical/ML methods to selectively trade only the conditions that demonstrate robust out-of-sample evidence?

## Phase 0 controls

Before advancing to ML or live execution, the project explicitly documents:

- `phase_00_india_retail_trading_spec.md` — Indian retail algo/API and execution requirements.
- `phase_00_capital_and_execution_spec.md` — ₹30,000 capital feasibility, costs, liquidity and deployment rules.
- `phase_00_research_universe_spec.md` — reproducible NSE cash-equity/ETF universe selection.

These are research controls and operational specifications, not legal, tax, or investment advice.

## Phase 1 universe work

The multi-instrument research-universe workflow is defined in:

- `phase_01_universe_audit.md` — candidate resolution, common historical-data collection, audit gates, liquidity/capital checks, and universe-bias controls.
- `universe_candidates.csv` — reproducible initial candidate manifest.

The candidate manifest is intentionally defined independently of strategy performance. The current tooling resolves symbols against the locally refreshed NSE instrument master and records broker-reported price information only as a capital-feasibility screening diagnostic.

## Strategy 001 research path

### 001 — GOLDBEES mean reversion

**Decision: 🔴 Rejected.**

The initial hypothesis was that unusually large deviations from a recent intraday mean would reverse. The baseline event study did not support that relationship; positive deviations were followed by positive rather than negative returns.

### 001A — event structure & conditioning

**Decision: ✅ Complete — continuation lead identified.**

A fixed 12-bar non-overlap diagnostic reduced event clustering while preserving the positive-deviation continuation pattern. Prior six-bar trend was the clearest conditioning variable. Volatility and volume did not provide a simple primary explanation.

No parameters were optimized.

### 001B — continuation attribution

**Status: 🔬 Implemented — empirical result pending.**

The research question is:

> Does continuation after a large deviation contain information beyond ordinary intraday drift and the recent trend?

The experiment compares positive/negative deviations, prior trend, predefined time-of-day buckets, and fixed non-overlapping events against matched non-event observations.

Implementation:

```text
src/research/continuation_attribution.py
scripts/run_continuation_attribution.py
tests/test_continuation_attribution.py
research/journal/001B_continuation_attribution.md
```

Run:

```powershell
python scripts/run_continuation_attribution.py data/raw/NSE_GOLDBEES_5minute.csv
```

The non-event benchmark is descriptive attribution only. It must not be used as a live signal because it is calculated over the full research sample.

## Promotion rule

A continuation lead is not promoted merely because its average return is positive.

The sequence is:

```text
001B attribution
      ↓
separate continuation hypothesis
      ↓
simple baseline strategy
      ↓
realistic costs + slippage
      ↓
predefined multi-instrument universe
      ↓
out-of-sample / walk-forward
      ↓
paper / shadow trading
      ↓
controlled live validation
```

**No strategy is approved for trading yet.**
