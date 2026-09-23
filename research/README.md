# Quant Research Workspace

This directory records the research process behind the strategy portfolio.

## Research lifecycle

The project follows a pattern-first workflow: data → pattern discovery → pattern characterization → economic interpretation → hypothesis → strategy definition → controlled development/optimization → candidate freeze → untouched chronological holdout → prospective paper/shadow → controlled live validation.

A pattern is not automatically a strategy, and exploratory discovery is not confirmatory evidence.

## Research principles

- Start with relevant data and discover/characterize patterns before committing to a strategy.
- Treat Quantra/WQU notebooks and the broader repository as reference material and building blocks, not automatically validated strategies.
- Establish a simple baseline before adding ML/DL.
- Use time-ordered validation and walk-forward testing where appropriate.
- Prevent look-ahead bias, leakage, survivorship bias, data snooping, and uncontrolled multiple testing.
- Use optimization only inside a pre-designated development sample.
- Protect the holdout from candidate selection and sequential tuning.
- Include explicit execution, cost, and slippage assumptions.
- Record negative and inconclusive results.
- Keep research-universe selection independent from strategy performance where possible.

Detailed policy: `journal/research_methodology.md`.

## Repository resource reminder

Before implementing a new analysis, feature, statistical test, strategy component, or data workflow, inspect the repository for relevant existing resources. Reuse, adapt, refactor, or combine them when appropriate. This includes Quantra, WQU, prior project notebooks, statistical methods, correlation/covariance, PCA, clustering, DBSCAN, stationarity, autocorrelation, pairs trading, portfolio construction, and broker/data-validation code.

Existing resources must still be validated in the current research context.

## Reference material

The repository contains WorldQuant University learning material and code under `trading_resources/WQU_resources/`. These resources can be used for study, implementation patterns, candidate strategy ideas, feature engineering, and later ML/model development. Code from those resources is not treated as automatically validated trading logic.

## Phase 0 controls

- `phase_00_india_retail_trading_spec.md`
- `phase_00_capital_and_execution_spec.md`
- `phase_00_research_universe_spec.md`

These documents define the project's research and execution controls.

## Phase 1 universe work

- `phase_01_universe_audit.md` — candidate resolution, common historical-data collection, audit gates, liquidity/capital checks, and universe-bias controls.
- `universe_candidates.csv` — reproducible initial candidate manifest.

The candidate manifest is defined independently of strategy performance.

## Strategy 003 — Intraday prediction-driven alpha discovery

Strategy 003 has completed its authorized exploratory/development research gates and has now passed the protected predictive gate; it is at the economic execution viability gate. It remains explicitly intraday.

The original draft used daily 1-day and 5-day targets. That draft is superseded because a 5-day close-to-close target is a multi-day prediction, not the project's intraday research objective.

The revised experiment stays on the existing 5-minute OHLCV data and predicts the next 5-minute cross-sectional excess return. The first feature families are liquidity/activity, volatility/state, bar shape/intraday state, and market context. The long within-session feature window is 60 bars because an Indian cash-equity session has about 75 five-minute bars; a 78-bar within-session window would never warm up.

The horizon decision is documented in `journal/003_horizon_decision_record.md`.

The first pass excludes signed-return direction and explicit continuation/reversal rules so Strategy 003 does not silently reproduce Strategy 001 or Strategy 002.

The first model ladder remains deliberately controlled:

```
zero baseline
    ↓
OLS
    ↓
fixed Ridge
```

Chronological model-development boundaries are purged by one decision timestamp. No large hyperparameter search, strategy PnL, or protected-period evaluation is allowed in discovery.

Protocol: `journal/003_prediction_discovery_protocol.md`.

Runner: `../scripts/run_strategy_003_prediction_discovery.py`.

## Strategy 002 — CLOSED

Strategy 002 was the Indian-equity cross-sectional residual-reversal research family.

The pattern-first sequence reached chronological validation for the fixed one-bar executable baseline. The baseline produced a small positive zero-cost gross validation result (+0.0896 bps mean return per portfolio observation), but the predefined 5 bps sensitivity overwhelmed the effect, so the implementation was not promotable.

A separate, pre-registered development experiment then tested H2, H3, and H6 holding lengths using **only 2025-09-18 through 2026-06-09**. H2 and H3 retained only +0.1921 and +0.2121 bps mean gross return per trade and were negative under the first 2 bps cost sensitivity. H6 was negative gross. No candidate satisfied the selection gate, so none was frozen and the protected validation period was not reopened for these variants.

The final holdout (**2026-08-20 through 2026-09-17**) remained untouched throughout this turnover-reduction selection process.

The turnover experiment also clarified the accounting: each completed trade has 2.0 normalized units of executed round-trip notional turnover (1.0 entry + 1.0 exit). Longer holding reduces trade frequency, but does not reduce turnover per completed round trip.

**Decision:** Strategy 002 is closed for the current capital-pursuit/candidate-selection program. This is not a statistical rejection of every possible residual-reversal phenomenon; it is closure of the tested executable research line under the project's cost and research-discipline gates.

Detailed findings: `journal/002_turnover_reduction_development_findings.md`.

## Strategy 001 research path — CLOSED

### 001 — GOLDBEES mean reversion

**Decision: 🔴 Rejected.**

The initial hypothesis was that unusually large deviations from a recent intraday mean would reverse. The event study did not support that relationship; positive deviations were followed by positive rather than negative returns.

### 001A — event structure & conditioning

**Decision: ✅ Complete — continuation lead identified.**

A fixed 12-bar non-overlap diagnostic reduced event clustering while preserving the positive-deviation continuation pattern. Prior six-bar trend was the clearest conditioning variable. No parameters were optimized.

### 001B — continuation attribution

**Decision: 🟡 Promising research lead.**

The strongest subgroup was positive deviation during a prior uptrend. Event returns exceeded matched non-event baselines across the tested horizons. Detailed results are in `journal/001B_continuation_attribution_results.md`.

### 001C — point-in-time continuation validation

**Decision: 🟡 Promising — continuation lead survives the point-in-time benchmark.**

The implementation produced 1,668 frozen events and 401 selected non-overlapping events under the fixed 12-bar cooldown.

For positive deviation + prior uptrend:

| Horizon | Event return | PIT baseline | Incremental return |
|---|---:|---:|---:|
| 5 min | +0.0148% | +0.0032% | **+0.0115%** |
| 15 min | +0.0205% | +0.0099% | **+0.0106%** |
| 30 min | +0.0443% | +0.0194% | **+0.0249%** |
| 60 min | +0.0527% | +0.0279% | **+0.0247%** |

The 30-minute primary horizon therefore showed approximately +2.49 basis points of incremental gross return relative to the point-in-time matched benchmark. This remains a research result, not a deployment decision.

Detailed results are in `journal/001C_continuation_hypothesis_results.md`.

### 001D — formal trading backtest

**Decision: 🟡 Candidate — gross backtest positive; cost sensitivity unresolved.**

The frozen implementation uses 5-minute GOLDBEES data, previous 30 completed same-session closes, sample standard deviation, z-score ≥ +2.0, prior six-bar return > 0, long-only, next-bar-open entry, close-of-t+6 exit, fixed 12-bar cooldown, no overnight feature construction, one position at a time, and no leverage or optimized sizing.

The completed baseline contains 310 trades. Gross performance was +15.85% cumulative with a +4.77 bps mean trade return, 55.81% win rate, and 2.269 profit factor. The predefined cost grid showed that modest friction can eliminate the gross edge, so this is not paper/live ready.

### 001E — trade distribution & execution audit

**Decision: 🟡 Complete — gross edge remains interesting, execution economics unresolved.**

001E found a +2.41 bps median and +4.77 bps mean gross trade return; the top 10% of winners contributed about 53.7% of positive profit; gross performance remained positive in each chronological period examined; mean trades per active day were about 1.30; median holding duration was 25 minutes; and the predefined friction grid rapidly consumed the small per-trade edge.

Detailed results are in `journal/001E_trade_distribution_execution_audit_results.md`.

### 001F — trade-level edge & execution decomposition

**Decision: 🟡 Promising for further research — not paper/live ready.**

After removing the top 10% of winning trades, the remaining 292 trades still had a +1.41 bps mean gross return, +1.32 bps median, 53.08% win rate, and 1.354 profit factor. Tail winners remain important, but the gross result is not solely produced by a few extremes. Later-session buckets were descriptively stronger, while z-score buckets showed no clean monotonic relationship. These are not selected filters.

The compact 001D trade export lacked the complete signal-time feature set and intermediate forward returns, motivating 001G.

Detailed results: `journal/001F_trade_edge_execution_decomposition_results.md`.

### 001G — point-in-time feature & forward-path replay

**Decision: 🟡 Complete — replay reconciled; forward-path diagnostics informative; not paper/live ready.**

The frozen 001D strategy was reconstructed directly from validated GOLDBEES OHLCV. All 310 replayed trades matched the 310-trade 001D reference within tolerance, with zero discrepancies.

The forward path was already positive before the frozen exit: mean return was +1.36 bps at 5 minutes, +2.44 bps at 10 minutes, +3.40 bps at 20 minutes, +4.51 bps at 25 minutes, and +4.77 bps at 30 minutes. Median return was +2.41 bps at 30 minutes. The 45- and 60-minute samples are smaller because paths cannot cross the session boundary.

MFE averaged +15.35 bps with a +9.48 bps median, while MAE averaged -9.63 bps with a -6.88 bps median. These are path diagnostics, not proof that intrabar highs/lows could be captured in execution.

Descriptive signal-time slices showed stronger gross outcomes in the 13–15 session buckets, but this is not being converted into an afternoon-only filter. Z-score buckets showed no clean monotonic relationship, and simple correlations of gross return with z-score, prior six-bar return, and volume ratio were small.

Detailed results: `journal/001G_point_in_time_feature_replay_results.md`.

### 001H — predefined robustness & chronological holdout

**Decision: 🟡 Complete — historical robustness encouraging; execution economics still unresolved.**

The frozen 001D strategy remained positive across all four chronological periods. 2025 contained 197 trades with +4.53 bps mean gross return, 57.87% win rate, 2.406 profit factor, and +9.31% cumulative gross return. The 2026 chronological holdout contained 113 trades with +5.18 bps mean gross return, 52.21% win rate, 2.105 profit factor, and +5.98% cumulative gross return.

The historical split provides evidence of persistence rather than a collapse in the later sample. However, it is explicitly **OOS-style**, not pristine untouched OOS, because the full January 2025–August 2026 sample has already been examined during research.

The cost ladder remains the central economic concern: 4 bps round-trip leaves +0.77 bps mean net trade return and +2.34% cumulative net return, while 6 bps round-trip produces -1.23 bps mean net return and -3.81% cumulative net return. At 14 bps round-trip, mean net return is -9.23 bps and cumulative net return is -24.95%. These are scenario assumptions, not observed live costs.

The local run completed successfully with 59 tests passing before the 001H robustness analysis. The plotting script initially exposed an implementation issue because the exported trade table does not carry the derived period label; that script has now been fixed to reconstruct the period from `signal_timestamp`.

Detailed results: `journal/001H_predefined_robustness_chronological_holdout_results.md`.

### 001I — prospective OOS / paper-shadow validation

**Decision: 🔵 Closed for current capital-pursuit program — not statistically rejected.**

Because the historical dataset has been examined through August 2026, we will **not** relabel August 2026 or any September data inspected before the prospective start as OOS. The first genuinely prospective OOS period begins after the immutable activation timestamp, with signals recorded before their outcomes are known.

The frozen 001D strategy remains unchanged during this window. Each signal is logged point-in-time, then its outcome and execution-friction information are appended only after the fixed exit completes. No threshold, holding period, time-of-day filter, stop, target, or other strategy rule may be changed based on observed prospective outcomes.

The first phase is paper/shadow rather than live capital. The implementation now has an append-only prospective ledger, an immutable run manifest, a collector that can restart across sessions without moving the OOS boundary, and a dedicated integrity validator.

Run validator: `scripts/validate_strategy_001i_run.py`.

Protocol: `journal/001I_prospective_oos_paper_shadow_protocol.md`.

Results journal: `journal/001I_prospective_oos_paper_shadow_results.md`.

## Strategy 001 historical research path — CLOSED

The historical sequence from 001C through 001I is preserved as evidence. 001I is no longer current work. The final decision was to close the Strategy 001 family for the current capital-pursuit program because the tested implementations did not establish sufficiently strong cost-resilient economics.

001I's two prospective observations were too few to statistically reject the underlying continuation phenomenon. 001J's broader-universe development searches remained in the few-basis-point gross range, and the strongest secondary search remained negative under the predefined 5-bps sensitivity. Further optimization on the same development sample was stopped to control sequential search and data-snooping risk.

```text
001C point-in-time validation                       🟡 exploratory lead
        ↓
001D formal baseline backtest                       🟡 historical candidate
        ↓
001E distribution + execution audit                 🟡 complete
        ↓
001F trade decomposition                            🟡 complete
        ↓
001G PIT feature + forward-path replay              🟢 complete
        ↓
001H robustness + chronological analysis            🟡 complete
        ↓
001I prospective OOS / paper-shadow                 🔵 closed
        ↓
001J cross-sectional development                    🔵 closed / no candidate
        ↓
Strategy 001 closure                                🔵 no promoted implementation
```

A failure at any gate is recorded rather than repaired by post-hoc parameter tuning.

**No Strategy 001 implementation was approved for deployment.**


### Strategy 003 characterization

The first intraday discovery run is complete. The frozen model relationship is now being characterized before any economic hypothesis, strategy construction, nonlinear model escalation, or protected validation.

Runner: `../scripts/run_strategy_003_prediction_characterization.py`.

Protocol: `journal/003_prediction_discovery_characterization_protocol.md`.


## Learning curriculum

A separate learning layer now maps the actual research history of Strategies 001–003 into reusable quant-research lessons. Start with `journal/research_learning_path.md`, then use `journal/research_learning_modules.md` as the detailed curriculum.

The active Strategy 003 work is currently at the final authorized development gate: economic-form decomposition of the locked 003H two-variable core. See `journal/003h_economic_form_decomposition_protocol.md`.


## Strategy 003 current gate

The final economic-form decomposition is complete. The interaction branch is closed, and the current development evidence is most consistent with a close-location-dominant additive interpretation. No protected validation or final holdout has been used.

Before deciding whether to continue, the project completed a current NSE cash-equity execution-cost basis review in `journal/003_execution_cost_basis_research_20260923.md`. The review concludes that the historical 5-bps round-trip sensitivity should be treated as a lower-bound/stress sensitivity, not a universal all-in retail execution-cost estimate.

The next permitted action is either to freeze the registered additive 003H form and execute the protected-validation protocol (`journal/003_protected_validation_protocol.md`) or close Strategy 003. No further exploratory feature search is authorized.


## Current Strategy 003 gate — 23 September 2026

The exploratory/development program is complete. The frozen candidate is now authorized for protected chronological validation:

- next 5-minute cross-sectional excess return;
- same 15 eligible equities;
- close_location_1bar + intraday_position_60bar;
- additive OLS with training-only standardization;
- no interaction, thresholds, holding-period search, feature search, universe changes or cost tuning.

Protected validation covers 2026-06-10 through 2026-08-19. The final holdout begins 2026-08-20 and remains untouched.

If prediction survives, use the preregistered economic execution viability protocol rather than opening another alpha-discovery cycle.

## Current published NSE/broker economics

The research cost basis has been updated using current official NSE/broker schedules. Intraday cash-equity costs include STT 2.5 bps on the sell side, NSE transaction charges about 0.307 bps per side, stamp duty 0.3 bps on the buy side, SEBI turnover fees, and 18% GST on applicable brokerage/exchange/SEBI charges. Zerodha publishes ₹20 or 0.03% per executed intraday order; Upstox and Angel One publish ₹20-or-percentage structures; Groww publishes ₹20/percentage-based intraday brokerage.

The current fee-only reference is approximately:

| Round-trip notional | Approx. broker + statutory cost |
|---:|---:|
| ₹50k | **10.6 bps** |
| ₹1 lakh | **8.3 bps** |
| ₹2.5 lakh | **5.4 bps** |
| ₹5 lakh | **4.5 bps** |
| ₹10 lakh | **4.0 bps** |
| ₹50 lakh | **3.6 bps** |

These figures are **before spread, slippage and market impact**. The historical 5-bps sensitivity is therefore retained only as a historical stress threshold, not as a universal all-in current cost estimate.

See `research/journal/003_execution_cost_basis_research_20260923.md`.

## Strategy 003 — protected validation result

The frozen additive 003H candidate passed the protected predictive gate on **2026-06-10 through 2026-08-19**:

- mean IC **+0.08136**
- mean rank IC **+0.10082**
- Q1–Q5 spread **+1.6870 bps**
- 711 timestamps / 10,665 observations / 15 equities

The development references were +0.0696 IC, +0.0826 rank IC and +2.2168 bps spread. The protected spread retains about 76% of development magnitude.

The scored protected timestamps are late-session (approximately 14:10–15:20) because of the frozen 60-bar warm-up. This is a coverage limitation, not a post-validation filter.

**Current decision:** Strategy 003 advances to economic execution viability testing. The final holdout remains untouched. Economic protocol: research/journal/003_economic_execution_viability_protocol.md.