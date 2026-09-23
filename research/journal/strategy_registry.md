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

Protocol: `research/journal/003_residual_mechanism_decomposition_protocol.md`.

Runner: `scripts/run_strategy_003_residual_mechanism_decomposition.py`.


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


### Strategy 003H component attribution — result and closure (2026-09-23)

The preregistered seven-specification attribution experiment was completed on the development-only sample. All specifications used the same next-5-minute cross-sectional excess-return target, one-decision-timestamp purge, and raw registered 003H variables. The protected validation period and final holdout were untouched.

The key development-test results were:

| Specification | Mean IC | Rank IC | Q1–Q5 spread |
|---|---:|---:|---:|
| close_location_1bar | +0.04107 | +0.04799 | +0.930 bps |
| intraday_position_60bar | +0.00265 | +0.02668 | +0.184 bps |
| bars_since_session_open | not scored | not scored | not scored |
| close_location + intraday_position | +0.05849 | +0.07274 | +1.787 bps |
| close_location + session_clock | +0.04107 | +0.04799 | +0.930 bps |
| intraday_position + session_clock | +0.00265 | +0.02668 | +0.184 bps |
| all three | +0.05849 | +0.07272 | +1.784 bps |

The important result is that the **close_location + intraday_position pair reproduces the all-three 003H reference almost exactly** on the shared 540-timestamp support. Relative to all-three, its development-test mean-IC difference is about **−0.0000035**, rank-IC difference about **+0.0000198**, and Q1–Q5 spread difference about **+0.003 bps**. The session-clock variable adds no measurable incremental contribution in this controlled attribution; moreover, the singleton session-clock specification has zero scored timestamps under the frozen data-availability design and therefore cannot be interpreted as evidence about a general time-of-day effect.

The close-location singleton itself retains a positive and economically nontrivial portion of the ordering (**+0.93 bps** spread), while intraday-position alone is much weaker on the development-test sample (**+0.18 bps**). The pair's recovery of the full reference indicates that the predictive ordering in 003H is primarily attributable to the combination of current-bar price location and 60-bar intraday position, with no observed need for the registered session-clock variable.

This is an **attribution result, not permission to select the pair as a final feature set**. The pair should not be re-labelled as a newly optimized strategy. The experiment has answered the explanatory question well enough to simplify the economic interpretation, but it has not established tradability, cost resilience, causal mechanism, or protected out-of-sample persistence.

**Current decision:** keep Strategy 003 active, close the session-clock branch under the current specification, and treat `close_location_1bar + intraday_position_60bar` as the **provisional explanatory core of 003H**. Do not yet use protected validation, final holdout, threshold/holding-period search, nonlinear model escalation, transaction-cost optimization, or portfolio construction.

The next registered question should therefore move from component attribution to **mechanism falsification and lineage separation of the two-variable core**, while preserving the development-only evidence boundary. In particular, test whether the two-variable core is merely an alternate representation of already-closed Strategy 001 continuation or Strategy 002 residual reversal, and whether its relationship survives a pre-registered decomposition that separates the current-bar state from prior-return information without opening a general feature search.

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


### Strategy 003 common-support control

The residual-family decomposition showed different usable timestamp counts across blocks. A common-support nested control is therefore preregistered before any interpretation of incremental family information. It evaluates the locked 003H mechanism and each one-family extension on identical complete-case observations. Protocol: `research/journal/003_common_support_nested_mechanism_protocol.md`; runner: `scripts/run_strategy_003_common_support.py`. This remains development-only with validation and holdout protected.

### Strategy 003 component-attribution control

The common-support residual-family control is complete. Activity, volatility and market context did not demonstrate incremental information beyond 003H on identical support; the earlier apparent market-context increment is treated as support-composition artifact. The corresponding family branches are closed under the current specification.

The next registered experiment is finite attribution within the locked 003H variables only. Protocol: `research/journal/003_003h_component_attribution_protocol.md`; runner: `scripts/run_strategy_003_003h_component_attribution.py`.

This experiment compares the three singletons, three pairwise combinations, and all-three 003H reference for interpretation only. It does not authorize performance-based feature selection or any protected validation/holdout use.


### Strategy 003H lineage separation — preregistered next gate (2026-09-23)

The component attribution experiment identified `close_location_1bar + intraday_position_60bar` as the provisional explanatory core of 003H. Before any protected validation or strategy construction, the next controlled experiment is a development-only lineage-separation test against the two closed mechanisms.

The preregistered comparison uses exactly five fixed specifications: 003H core; Strategy 001 event proxy; Strategy 002 leave-one-out prior residual; 001+002 lineage proxies; and 003H core + both lineage proxies. Strategy 001 is represented by its frozen event definition `z_score >= 2.0 and prior_return_6bar > 0`. Strategy 002 is represented by the point-in-time leave-one-out prior close-to-close residual. No thresholds, horizons, features, transforms, universes, costs, or nonlinear models may be searched.

The experiment asks whether 003H retains predictive information conditional on the old mechanisms. It is a falsification/lineage test, not feature selection. Validation and final holdout remain protected.

Implementation: `scripts/run_strategy_003h_lineage_separation.py`; protocol: `research/journal/003h_lineage_separation_protocol.md`; tests: `tests/test_strategy_003h_lineage_separation.py`.


### Strategy 003H lineage separation — result and closure (2026-09-23)

The lineage-separation experiment was completed with five fixed specifications, no parameter/feature search, 155 local tests passing, and 15 eligible equities. The generated outputs were uploaded to the repository.

On the common 003H support, the standalone core produced **+0.05849 mean IC / +0.07274 rank IC / +1.787 bps spread**, while the combined 003H+001+002 model produced **+0.05577 / +0.06774 / +1.848 bps**. The frozen 001 and 002 lineage proxies therefore did not remove the 003H ordering.

**Decision:** Strategy 003 remains active as a distinct but unvalidated intraday prediction hypothesis. The current 001/002-overlap branch is closed under the frozen definitions; Strategies 001 and 002 remain closed and no 003H candidate is frozen.

The next controlled experiment is **economic-form decomposition of the two-variable 003H core**, using a finite preregistered representation set with common-support control. No unrestricted feature search, holding-period search, cost optimization, nonlinear escalation, portfolio construction, protected validation, or holdout use is authorized by the lineage result.

Protocol: `research/journal/003h_lineage_separation_protocol.md`.
Runner: `scripts/run_strategy_003h_lineage_separation.py`.
Outputs: `data/reports/strategy_003h_lineage_separation/`.


## Learning curriculum

The repository now has a separate educational layer that turns the cumulative Strategy 001–003 research process into reusable quant-research lessons rather than treating each experiment as an isolated backtest.

See:

- research/journal/research_learning_path.md — module index and strategy-to-module map.
- research/journal/research_learning_modules.md — detailed lessons covering hypothesis formation, leakage, chronological validation, holdout protection, cross-sectional prediction, IC/rank IC/quintiles, attribution, common support, mechanism decomposition, transaction costs, lineage testing, negative results, branch closure, strategy construction, and research decision-making.

These modules are educational summaries derived from the actual project record; they do not override any experiment's original protocol or evidence boundary.

## Strategy 003 final exploratory gate

The lineage-separation result left the 003H two-variable core distinct from the frozen 001/002 representations within the registered comparison. The final authorized development-stage question is now economic-form decomposition of the same two variables.

Registered experiment: research/journal/003h_economic_form_decomposition_protocol.md.
Implementation: scripts/run_strategy_003h_economic_form_decomposition.py.
Tests: tests/test_strategy_003h_economic_form_decomposition.py.

The experiment evaluates exactly four fixed specifications on common support: close-location only, intraday-position only, the additive two-variable core, and one pre-registered close-location × intraday-position interaction. It is development-only; protected validation and final holdout remain untouched.

After this gate, no new exploratory feature family, transform, threshold, holding-period search, cost optimization, nonlinear escalation, or portfolio work is authorized. The next decision must be either to close Strategy 003 or to freeze one clearly defined explanatory form for a separately controlled protected-validation experiment.

### Strategy 003H economic-form decomposition — result and closure (2026-09-23)

The final preregistered development decomposition was completed on common support. Close-location-only produced the strongest descriptive relationship (**+0.08419 mean IC, +0.09205 rank IC, +2.358 bps Q1–Q5 spread** in the development-test sample). The additive two-variable core produced **+0.05928 / +0.07355 / +1.780 bps**, while the fixed interaction produced **+0.06070 / +0.07258 / +1.871 bps**. Intraday-position-only was weak in development test (**+0.00309 / +0.02768 / +0.219 bps**).

The fixed interaction changed the additive result only marginally and was qualitatively similar across the internal validation split. The interaction branch is therefore closed. Close-location dominance is retained as explanatory evidence only; it is not post-hoc feature selection and does not replace the preregistered 003H core as a validated model.

**Decision:** the authorized exploratory decomposition is complete. Strategy 003 remains an unvalidated research hypothesis pending a hard promotion/closure decision. No further exploratory search is authorized under the current lineage. The next permitted action is either to freeze a narrowly specified explanatory form and preregister protected validation, or close Strategy 003 as insufficient for further work. Protected validation and the final holdout remain untouched.

Protocol: `research/journal/003h_economic_form_decomposition_protocol.md`.
Results: `research/journal/003_prediction_discovery_results.md`.
Runner: `scripts/run_strategy_003h_economic_form_decomposition.py`.