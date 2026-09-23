# Strategy Registry

This registry defines the portfolio-level research map and prevents the project from creating multiple nominal strategies that are economically the same.

## Research lifecycle

The portfolio uses a pattern-first lifecycle: data → pattern/predictive-information discovery → characterization → economic interpretation → hypothesis → strategy definition → development/controlled optimization → candidate freeze → holdout → prospective → live.

A pattern discovery result is not automatically a strategy. A strategy candidate requires an explicit economic interpretation and precise executable definition.

## Repository resource reminder

Before starting a new investigation, inspect the repository's existing resources and reuse, adapt, or combine relevant methods and code where appropriate. See research/journal/repository_resource_policy.md.

## Core rule

A **strategy ID** represents a materially different economic return hypothesis. A parameter variation, universe expansion, execution variant, or new experimental implementation of the same hypothesis remains an experiment/version under the parent strategy and does not receive a new strategy ID merely to create another backtest.

No two promoted strategies should be materially the same economic mechanism applied to the same asset class.

## Current registry

| Strategy ID | Asset class | Economic hypothesis / mechanism | Current experiment | Status |
|---|---|---|---|---|
| 001 | Indian equities | Short-horizon continuation after unusually strong intraday moves, conditioned on recent positive direction | 001J — Kite-native liquid NSE EQ cross-sectional experiment | **Closed; no candidate frozen** |
| 002 | Indian equities | Short-horizon cross-sectional residual reversal: unusually negative peer-relative returns are followed by positive relative returns, and vice versa | Initial audit → locked split → pattern discovery → pattern characterization → reversal mechanism decomposition → cross-sectional residual investigation → leave-one-out residual mechanism decomposition → temporal stability characterization → fixed-baseline validation → cost-resilience gate failed → turnover/execution decomposition → H2/H3/H6 turnover-reduction development | **Closed; no candidate frozen** |
| 003 | Indian equities | Intraday prediction-driven discovery using liquidity/activity, volatility/state, bar-shape/intraday-state and market context; first pass excludes 001/002 signed-return mechanisms | Next-5-minute discovery → frozen-model characterization → provisional mechanism test 003H | **Active hypothesis test; no candidate frozen** |
## Strategy 003 — intraday prediction-driven alpha discovery

### Strategy 003H mechanism decomposition — result

003H tested the preregistered bar-shape/intraday-state mechanism using exactly three locked raw features: `close_location_1bar`, `intraday_position_60bar`, and `bars_since_session_open`. The development-test result retained positive cross-sectional ordering (mean IC **+0.0585**, mean rank IC **+0.0727**, mean top-bottom spread **+1.78 bps**) but did not explain the entire frozen full-model separation (**+2.22 bps**). The simple mechanism is therefore treated as a meaningful component, not a complete explanation and not a promoted strategy.

The lineage audit found no direct encoding of Strategy 001 signed-return events or Strategy 002 peer-residual returns in the locked feature definitions. However, the mechanism models have zero scored observations before 14:00 because of the frozen 60-bar warm-up, so time-of-day generality remains unresolved.

**Current decision:** keep Strategy 003 active as an unresolved intraday prediction hypothesis. Do not construct a portfolio, optimize thresholds/holding periods, escalate to nonlinear ML, or use protected validation yet. The next registered step is a finite residual-mechanism decomposition: test the existing locked mechanism with one additional pre-existing feature-family block at a time (activity, volatility, market context), without parameter tuning or selecting the best family from development performance.


Strategy 003 is a **research program**, not a frozen trading strategy. The original draft used 1-day and 5-day daily targets as a broad prediction-discovery experiment. It is now superseded because the project objective is intraday strategy research. A 5-trading-day target is a multi-day close-to-close prediction, not an intraday prediction target.

The initial daily experiment is preserved rather than rewritten. It was a legitimate medium-horizon prediction question, but continuing to optimize it would have created scope drift. The pivot to intraday was an objective-alignment decision, not a reaction to an unfavorable result.

The revised program uses the existing 5-minute equity data, predicts the next 5-minute cross-sectional excess return, and begins with liquidity/activity, volatility/state, bar-shape/intraday-state and market-context features. Its longer rolling feature window is 60 bars, because an Indian cash-equity session contains about 75 five-minute bars; a 78-bar within-session window would never warm up. It explicitly excludes signed-return mechanisms already owned by Strategy 001 continuation and Strategy 002 residual reversal, so ML cannot silently relabel an old mechanism as new alpha.

The model ladder remains zero baseline → OLS → fixed Ridge. Chronological development is purged by one decision timestamp because the target is the next 5-minute bar. Protected validation and final holdout remain untouched.

The first discovery run established a stable-looking development-test predictive relationship: OLS mean IC was +0.0696 with mean rank IC +0.0826 and mean top-bottom quintile spread +2.22 bps; fixed Ridge was essentially identical. This is discovery evidence, not validated alpha or strategy P&L.

The characterization pass is complete enough to move to a provisional economic-mechanism test. Q1→Q5 endpoint separation is about +2.22 bps, winsorized spread remains about +2.29 bps, bar-shape/intraday-state is the largest registered family in the descriptive ablation, and OLS/Ridge scores are effectively identical. The middle quintiles are not strictly monotonic, so the result is described as broad directional ordering rather than strict monotonicity. Early-session model coverage remains structurally limited by the frozen 60-bar features. The next registered experiment is 003H mechanism decomposition; protected validation and final holdout remain untouched.

Protocol: `research/journal/003_prediction_discovery_protocol.md`.

Discovery results: `research/journal/003_prediction_discovery_results.md`.

Characterization protocol: `research/journal/003_prediction_discovery_characterization_protocol.md`.

Provisional hypothesis protocol: `research/journal/003_prediction_hypothesis_protocol.md`.

Discovery runner: `scripts/run_strategy_003_prediction_discovery.py`.

Characterization runner: `scripts/run_strategy_003_prediction_characterization.py`.

003H mechanism runner: `scripts/run_strategy_003_hypothesis_003h_mechanism.py`.

| 004 | — | Reserved | — | Planned |
| 005 | — | Reserved | — | Planned |

## Strategy 001 closure

Strategy 001 is closed for the current capital-pursuit/candidate-selection program. The tested implementations did not establish sufficiently strong cost-resilient economics. This is **not** a statistical rejection of the broader continuation phenomenon. 001I was too sparse for rejection, while 001J's development results remained only a few basis points gross and did not satisfy the project's economic/cost requirements.

Further optimization was stopped because the same development sample had already been searched through a primary grid and a separately registered secondary grid. Repeatedly reopening it would increase research degrees of freedom, data-snooping risk, and the effective multiple-testing burden.

Existing 001D, 001I, 001J, universe files, and journals remain historical evidence and must not be silently retuned.

## Strategy 001 lineage

| Experiment | Universe / instrument | Purpose | Status |
|---|---|---|---|
| 001D | GOLDBEES | Frozen single-instrument implementation | Immutable historical candidate |
| 001I | GOLDBEES | Prospective OOS / paper-shadow test of 001D | Closed for capital-pursuit priority; not statistically rejected |
| 001J | U1: Kite-native liquid NSE EQ universe; PIT Nifty 100 deferred | Test whether the same continuation hypothesis generalizes cross-sectionally using the user's existing broker data infrastructure | Closed for current candidate selection; no candidate frozen |

001D and 001I are immutable historical evidence. 001J is a new experiment under the same Strategy 001 hypothesis family; its parameters must never be back-filled into 001D.

The tactical 001J U1 has an explicit current-instrument/survivorship limitation. A later PIT Nifty 100 implementation remains a separate universe experiment under Strategy 001 rather than being silently substituted into the tactical result.

## Strategy 002 closure

Strategy 002 is closed for the current capital-pursuit/candidate-selection program. The fixed one-bar implementation produced only +0.0896 bps mean gross return per validation observation and failed the predefined cost-resilience gate. The subsequent pre-registered H2/H3/H6 development experiment was confined to 2025-09-18 through 2026-06-09; H2 and H3 retained only about +0.19/+0.21 bps gross per trade and became negative under the 2 bps sensitivity, while H6 was negative gross. No candidate was frozen, chronological validation was not reopened for these variants, and the final holdout remained untouched.

This closes the tested Strategy 002 research line rather than claiming that every residual-reversal phenomenon is false. Further searches under the same mechanism should not be added after the observed results. A new strategy ID should use a materially different economic mechanism and/or asset class.

Detailed findings: `research/journal/002_turnover_reduction_development_findings.md`.

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

## Strategy-lineage guardrail

Strategy 003 may use Strategies 001 and 002 only as historical evidence and exclusion references. Continuation-like signed-return prediction remains 001 lineage; cross-sectional residual reversal remains 002 lineage. A 003 model must demonstrate a distinct information source and economic interpretation before candidate promotion.

## Promotion discipline

A new strategy ID should be created only after its proposed hypothesis and asset-class combination has been checked against this registry. If the work is merely a continuation of an existing hypothesis, create a new experiment/version under that strategy instead.

Trade frequency is an operational constraint, not the economic objective. The project must never weaken thresholds solely to manufacture a target trade count.

## Promotion gates

A strategy is promoted only after the project's methodology gates are satisfied: reproducible data, point-in-time correctness or an explicitly disclosed alternative limitation, economic rationale, statistical evidence, chronological validation, realistic costs, execution feasibility, and explicit risk controls. A profitable backtest alone is not sufficient.
