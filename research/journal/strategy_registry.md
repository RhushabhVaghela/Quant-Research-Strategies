# Strategy Registry

This registry defines the portfolio-level research map and prevents the project from creating multiple nominal strategies that are economically the same.

## Core rule

A **strategy ID** represents a materially different economic return hypothesis. A parameter variation, universe expansion, execution variant, or new experimental implementation of the same hypothesis remains an experiment/version under the parent strategy and does not receive a new strategy ID merely to create another backtest.

No two promoted strategies should be materially the same economic mechanism applied to the same asset class.

## Current registry

| Strategy ID | Asset class | Economic hypothesis / mechanism | Current experiment | Status |
|---|---|---|---|---|
| 001 | Indian equities | Short-horizon continuation after unusually strong intraday moves, conditioned on recent positive direction | 001J — Kite-native liquid NSE EQ cross-sectional experiment | Closed for current candidate selection; no candidate frozen |
| 002 | Indian equities | Intraday relative-value / statistical arbitrage: temporary pair-spread dislocation followed by normalization | 002 — initial pairs-mean-reversion experiment | Registered; research pending |
| 003 | — | Reserved for a genuinely different strategy/asset-class combination | — | Planned |
| 004 | — | Reserved | — | Planned |
| 005 | — | Reserved | — | Planned |

## Strategy 001 lineage

| Experiment | Universe / instrument | Purpose | Status |
|---|---|---|---|
| 001D | GOLDBEES | Frozen single-instrument implementation | Immutable historical candidate |
| 001I | GOLDBEES | Prospective OOS / paper-shadow test of 001D | Closed for capital-pursuit priority; not statistically rejected |
| 001J | U1: Kite-native liquid NSE EQ universe; PIT Nifty 100 deferred | Test whether the same continuation hypothesis generalizes cross-sectionally using the user's existing broker data infrastructure | Closed for current candidate selection; no candidate frozen |

001D and 001I are immutable historical evidence. 001J is a new experiment under the same Strategy 001 hypothesis family; its parameters must never be back-filled into 001D.

The tactical 001J U1 has an explicit current-instrument/survivorship limitation. A later PIT Nifty 100 implementation remains a separate universe experiment under Strategy 001 rather than being silently substituted into the tactical result.

## Strategy 002 initial experiment

Strategy 002 is deliberately different from Strategy 001. It studies relative-value mean reversion between two securities rather than directional continuation in one security.

The registered specification is:

`research/journal/002_intraday_pairs_mean_reversion_spec.md`

The initial experiment uses U1 only as a **predefined candidate universe**. Pair selection and hedge estimation must be formation-only and frozen before development selection.

## Portfolio asset classes

The research program may cover:

- equities;
- derivatives;
- commodities;
- currencies/FX;
- crypto.

The portfolio should deliberately contain different economic mechanisms. Candidate mechanisms include mean reversion, momentum/continuation, fundamentals/valuation, statistical arbitrage, volatility/derivatives relative value, carry, seasonality, and other hypotheses that can be stated before parameter optimization.

These categories are research directions, not claims that any particular strategy is profitable.

## Derivatives deployment policy

A derivatives strategy may remain paper-only when reliable real-time data, contract economics, lot size, liquidity, margin requirements, transaction costs, or available capital make live deployment inappropriate. Paper-only status still requires the same sequence: hypothesis → data audit → backtest → robustness → chronological validation → paper/shadow validation.

## Promotion discipline

A new strategy ID should be created only after its proposed hypothesis and asset-class combination has been checked against this registry. If the work is merely a continuation of an existing hypothesis, create a new experiment/version under that strategy instead.

Trade frequency is an operational constraint, not the economic objective. The project must never weaken thresholds solely to manufacture a target trade count.

## Promotion gates

A strategy is promoted only after the project's methodology gates are satisfied: reproducible data, point-in-time correctness or an explicitly disclosed alternative limitation, economic rationale, statistical evidence, chronological validation, realistic costs, execution feasibility, and explicit risk controls. A profitable backtest alone is not sufficient.
