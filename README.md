# Quant Research Strategies

This repository is a research journal and implementation workspace for developing, testing, and validating systematic trading strategies in Python.

The goal is not to collect a large number of backtests. The goal is to build a reproducible research process: relevant data → data audit → pattern discovery → pattern characterization → economic interpretation → hypothesis → strategy definition → controlled development/optimization → candidate freeze → untouched chronological holdout → prospective paper/shadow test → controlled live validation.

A pattern is not a hypothesis, a hypothesis is not a strategy, and a strategy is not validated alpha. The detailed policy is documented in `research/journal/research_methodology.md`.

Negative and inconclusive results are preserved as part of the research record.

---

## Strategy 001 — Intraday continuation research family — CLOSED

Strategy 001 began as a GOLDBEES mean-reversion hypothesis. The mean-reversion hypothesis was rejected during the original research. The observed continuation structure then became the active Strategy 001 economic hypothesis.

### Research status

| Stage | Status | Key result |
|---|---|---|
| 001 mean reversion | 🔴 Rejected | Large positive deviations did not reliably revert |
| 001A diagnostics | 🟢 Complete | Positive continuation and prior-trend conditioning identified |
| 001B attribution | 🟡 Promising | Continuation exceeded descriptive matched non-event baselines |
| 001C PIT baseline | 🟡 Promising | 30-min positive/up incremental result ≈ +2.49 bps |
| 001D frozen backtest | 🟡 Candidate | +4.77 bps mean gross trade, 310 trades; costs unresolved |
| 001E execution audit | 🟡 Complete | Small gross edge is highly friction-sensitive |
| 001F decomposition | 🟡 Complete | Edge not solely dependent on top tail winners |
| 001G replay | 🟡 Complete | 310/310 trades reconciled; forward path and MFE/MAE recovered |
| 001H robustness/chronological holdout | 🟡 Complete | Positive gross performance across examined periods; costs remain unresolved |
| 001I prospective OOS / paper-shadow | 🔵 Closed | Two genuine prospective trades on 2026-09-17; too low-frequency for current capital-pursuit sprint; not statistically rejected |
| **001J cross-sectional equity experiment** | **🔵 Closed** | Same economic hypothesis tested cross-sectionally using a broker-native liquid NSE EQ universe; no candidate frozen |

### Why Strategy 001 was closed

Strategy 001 was **not statistically rejected**. The two 001I prospective observations were far too few to reject the underlying continuation phenomenon.

The strategy family was instead closed because the tested implementations did not establish sufficiently strong, cost-resilient economics for the September 2026 capital-pursuit program. 001I was too low-frequency, while 001J's broader-universe development searches remained in the few-basis-point gross range. The strongest secondary development result was approximately 3.63 bps mean gross return per trade, with a negative median and negative mean under the predefined 5-bps sensitivity. Further repeated searches on the same development sample would have increased sequential-search, multiple-testing, and data-snooping risk without establishing a stronger economic basis.

Therefore the correct conclusion is: **the tested Strategy 001 implementations were not sufficient for promotion; the broader continuation phenomenon remains an unresolved research observation rather than a rejected hypothesis.** Existing 001D, 001I, U1, and historical journals remain immutable evidence.

### Why we stopped optimization

Optimization is appropriate after a pattern and economic hypothesis have been established, but only inside a pre-designated development sample. It should search for a robust parameter/model region, not an isolated historical maximum. Candidate selection must consider costs, breadth, drawdown, distribution, time stability, neighboring parameters, concentration, and execution feasibility.

Strategy 001 had already undergone extensive discovery, diagnostics, frozen implementation testing, primary development, and a separately registered secondary development search. Continuing to open more searches on the same development sample would increase the effective research degrees of freedom and make a later favorable result harder to interpret. The project therefore stopped optimization as a methodological control rather than trying to manufacture a deployable result.

See `research/journal/research_methodology.md` for the project's rules on optimization, multiple testing, data snooping, and holdout protection.

### Frozen 001D strategy

001D remains immutable evidence:

- 5-minute GOLDBEES OHLCV;
- previous 30 completed same-session closes;
- sample standard deviation;
- z-score ≥ +2.0;
- prior six-bar return > 0;
- long-only;
- signal at event-bar close;
- next-bar-open entry;
- close of `t+6` exit;
- fixed 12-bar session cooldown;
- no overnight feature construction;
- one position at a time;
- no leverage or optimized sizing.

### 001I status

001I was the prospective test of frozen 001D. It produced two selected trades on 2026-09-17. The prospective ledger passed validation, but the single-instrument opportunity rate was too low for the accelerated September 2026 capital-pursuit objective. The sample is too small to statistically reject the underlying continuation hypothesis. 001I is closed and must not be restarted or retuned.

### 001J — closed experiment

001J keeps the **Strategy 001 economic hypothesis** but changes the experimental universe and parameter-selection stage. This is not a modification of 001D.

**U1:** top 50 currently tradable NSE EQ instruments ranked by median daily traded value during a pre-strategy formation window, using 5-minute OHLCV acquired through the existing Zerodha Kite Connect infrastructure.

The tactical U1 is outcome-independent but carries current-instrument/survivorship bias because the broker's current instrument dump does not reconstruct historical index membership or delistings. The original PIT Nifty 100 U1 remains deferred and is not silently substituted.

A separate, outcome-independent GOLDBEES behavior report measures return correlation and other descriptive properties. It is diagnostic only and does not select symbols using Strategy 001J P&L. The first baseline then applies the exact 001D parameters cross-sectionally. Only after that baseline is recorded may the pre-registered 162-configuration development grid be evaluated.

See:

- `research/journal/001J_cross_sectional_equity_spec.md`
- `research/journal/001J_universe_u1_spec.md`
- `research/journal/001J_universe_discovery_protocol.md`
- `research/journal/001J_data_acquisition.md`
- `research/journal/001J_data_source_playbook.md`
- `config/strategy_001j_u1.json`
- `src/research/strategy_001j_cross_sectional.py`
- `scripts/fetch_strategy_001j_kite_data.py`
- `scripts/build_strategy_001j_broker_liquid_universe.py`
- `scripts/analyze_strategy_001j_universe_similarity.py`
- `scripts/validate_strategy_001j_data_gate.py`

---

## Strategy 002 — CLOSED

Strategy 002 developed from a pattern-first investigation of short-horizon cross-sectional residual reversal in Indian equities.

The research sequence reached chronological validation for the fixed one-bar executable baseline. The baseline produced only **+0.0896 bps mean gross return per five-minute portfolio observation**, and the predefined 5 bps sensitivity overwhelmed the effect. The fixed baseline therefore was not promotable.

A pre-registered turnover-reduction development experiment then tested H2, H3, and H6 using only the development period (**2025-09-18 through 2026-06-09**). H2 and H3 retained only +0.1921 and +0.2121 bps mean gross return per trade and were negative under the first 2 bps cost sensitivity. H6 was negative gross. No candidate satisfied the selection gate, so chronological validation was not reopened for these variants.

The final holdout (**2026-08-20 through 2026-09-17**) remained untouched. The turnover accounting was also clarified: each completed one-position round trip has 2.0 normalized units of executed notional turnover (1.0 entry + 1.0 exit); longer holding reduces trade frequency but not turnover per completed trade.

**Decision: Strategy 002 is closed for the current capital-pursuit/candidate-selection program.** This closes the tested executable research line; it is not a statistical rejection of every possible residual-reversal phenomenon.

Detailed findings: research/journal/002_turnover_reduction_development_findings.md.

## Strategy 003 — Intraday prediction-driven alpha discovery — ECONOMIC EXECUTION GATE

After Strategies 001 and 002, Strategy 003 changes the discovery layer rather than simply trying another narrow trading rule.

The original 003 draft used daily 1-day and 5-day targets as a broad prediction-discovery experiment. That draft is superseded because a 5-day close-to-close target is a multi-day prediction, not the project's intraday research objective. The pivot was an objective-alignment decision, not a reaction to the five-day result.

The revised 003 experiment stays on the existing 5-minute OHLCV data and predicts the next 5-minute cross-sectional excess return. The first long rolling feature window is 60 bars because a regular Indian cash-equity session has about 75 five-minute bars; a 78-bar within-session window would never become fully populated.

The first feature families are:

- liquidity/activity;
- volatility/state;
- bar shape/intraday state;
- market context.

The first pass explicitly excludes signed-return direction and continuation/reversal event rules so Strategy 003 cannot silently reproduce Strategy 001 continuation or Strategy 002 residual reversal.

The model ladder remains:

```
zero baseline → OLS → fixed Ridge
```

Chronological development boundaries are purged by one decision timestamp. No large hyperparameter search, strategy PnL, or protected-period evaluation is allowed in discovery.

See `research/journal/003_prediction_discovery_protocol.md` and `scripts/run_strategy_003_prediction_discovery.py`.

The Strategy 003 discovery, characterization, mechanism decomposition, common-support control, component attribution, lineage separation, and economic-form decomposition are now complete. No protected validation or final holdout data have been used.

The final economic-form decomposition found no material evidence for a separate interaction mechanism. Close-location-only was the strongest descriptive component, while the frozen additive 003H core remained the registered explanatory form. This is explanatory evidence, not post-hoc feature selection.

Final exploratory gate: `research/journal/003h_economic_form_decomposition_protocol.md`.

Protected-validation protocol: `research/journal/003_protected_validation_protocol.md`.

Current results record: `research/journal/003_prediction_discovery_results.md`.

Current execution-cost basis research: `research/journal/003_execution_cost_basis_research_20260923.md`.


## Strategy portfolio architecture

The project will eventually test genuinely different strategies across multiple asset classes, including equities, derivatives, commodities, currencies, and crypto. No two promoted strategies should be materially the same economic hypothesis applied to the same asset class.

A parameter variation or universe expansion of an existing hypothesis remains an experiment under the parent strategy. A genuinely different return mechanism receives a new strategy ID.

Derivatives strategies may remain paper-only when reliable realtime data, contract economics, lot size, liquidity, or available capital make live deployment inappropriate. Paper-only status still requires the same research discipline.

See `research/journal/strategy_registry.md` for the current strategy map and experiment lineage.

---

## Research standards

1. Start with relevant data and discover/characterize patterns before committing to a strategy definition.
2. Inspect the repository's existing research resources before reinventing equivalent methods or code.
3. Distinguish exploratory pattern discovery from confirmatory strategy validation.
4. Formulate an economic hypothesis only after the pattern has been characterized.
5. Use optimization only inside a pre-designated development sample.
6. Treat the total number of research decisions—not only model parameters—as an overfitting risk.
7. Protect the chronological holdout from candidate selection and sequential tuning.
8. Register additional development searches explicitly and record their overfitting implications.
9. Prefer parameter-neighborhood stability and economic robustness over isolated maxima.
10. Preserve negative and inconclusive results.
11. Use point-in-time information for prospective strategy construction.
12. Keep event definitions and forward outcomes strictly separated.
13. Establish a simple baseline before ML.
14. Test across time and market regimes.
15. Include transaction costs and slippage before judging economic value.
16. Treat backtests as evidence, not guarantees.
17. Require genuine prospective evidence before controlled live validation.
18. Never deploy simply because a backtest looks attractive.
19. Define universe membership before evaluating strategy performance.
20. Preserve every parameter-search result and never select holdout winners retrospectively.
21. Treat cross-sectional observations as potentially correlated rather than assuming every trade is independent.
22. Do not manufacture trade frequency by weakening thresholds solely to meet a target count.
23. Preserve strategy/experiment lineage so historical evidence cannot be rewritten by later research.
24. Keep descriptive universe discovery separate from strategy-outcome-based universe selection.
25. When a tactical non-PIT universe is used for schedule pressure, disclose the limitation explicitly rather than presenting it as PIT evidence.

<!-- legacy standards retained below for historical context -->

26. Start with an economic hypothesis, not a model.
2. Define the prediction target before choosing a model.
3. Use point-in-time information for prospective strategy construction.
4. Keep event definitions and forward outcomes strictly separated.
5. Establish a simple baseline before ML.
6. Record negative and inconclusive results.
7. Avoid parameter optimization before establishing evidence.
8. Test across time and market regimes.
9. Include transaction costs and slippage before judging economic value.
10. Treat backtests as evidence, not guarantees.
11. Require genuine prospective evidence before controlled live validation.
12. Never deploy simply because a backtest looks attractive.
13. Define universe membership before evaluating strategy performance.
14. Preserve every parameter-search result and never select holdout winners retrospectively.
15. Treat cross-sectional observations as potentially correlated rather than assuming every trade is independent.
16. Do not manufacture trade frequency by weakening thresholds solely to meet a target count.
17. Preserve strategy/experiment lineage so historical evidence cannot be rewritten by later research.
18. Keep descriptive universe discovery separate from strategy-outcome-based universe selection.
19. When a tactical non-PIT universe is used for schedule pressure, disclose the limitation explicitly rather than presenting it as PIT evidence.

---

## Repository resource reminder

Whenever a new GitHub research request is made, first remind ourselves to inspect the repository's existing resources. Relevant Quantra/WQU notebooks, statistical methods, pairs/correlation/PCA/clustering/stationarity material, data utilities, validation code, and prior research should be reused, adapted, or combined where appropriate rather than reinventing equivalent work. Existing resources are references/building blocks, not automatically validated alpha.

See `research/journal/repository_resource_policy.md` and `research/journal/research_methodology.md`.

## Reproducibility

Install dependencies from Windows CMD:

```cmd
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

Run the complete test suite:

```cmd
pytest -q
```

Strategy 002 is closed for the current capital-pursuit/candidate-selection program. Strategy 003 has completed its authorized exploratory development gates. The registered additive 003H form is now frozen and protected validation is authorized. No further exploratory feature search is authorized.

---

## Quant Research Learning Layer
The repository now includes a separate learning curriculum built from the actual Strategy 001–003 research path. It captures reusable skills such as hypothesis formation, leakage control, chronological validation, holdout protection, cross-sectional prediction, IC/rank IC, quintile analysis, attribution, common-support controls, mechanism decomposition, transaction-cost reasoning, lineage testing, negative results, and disciplined branch closure.

See `research/journal/research_learning_path.md` and `research/journal/research_learning_modules.md`.

### Strategy 003 current decision gate

The economic-form decomposition is complete. The interaction branch is closed. The current development evidence is most consistent with a simple close-location-dominant/additive interpretation, but no final trading model has been validated.

Current cost research also shows that the historical 5-bps round-trip sensitivity is not a defensible universal all-in NSE intraday cost basis: published brokerage/statutory charges alone can exceed 5 bps at ordinary retail notionals, before spread and market impact.

Cost research: `research/journal/003_execution_cost_basis_research_20260923.md`.

Protected validation protocol: `research/journal/003_protected_validation_protocol.md`.

The final holdout remains untouched.


## Current published NSE/broker economics — 23 September 2026

For NSE equity intraday, the current published cost schedule used by this research program is:

- STT = **2.5 bps**, sell side.
- NSE transaction charge = about **0.307 bps per side**.
- Stamp duty = **0.3 bps**, buy side.
- SEBI turnover fee = very small.
- GST = **18%** on applicable brokerage/exchange/SEBI charges.
- Zerodha brokerage = **₹20 or 0.03%, whichever is lower, per executed order**.
- Upstox and Angel One publish broadly similar **₹20-or-percentage** intraday structures.
- Groww also publishes a **₹20/percentage-based** intraday brokerage structure.

These rates are documented from current official NSE and broker schedules in `research/journal/003_execution_cost_basis_research_20260923.md`.

### Fee-only round-trip reference

| Round-trip notional | Approx. broker + statutory cost |
|---:|---:|
| ₹50k | **10.6 bps** |
| ₹1 lakh | **8.3 bps** |
| ₹2.5 lakh | **5.4 bps** |
| ₹5 lakh | **4.5 bps** |
| ₹10 lakh | **4.0 bps** |
| ₹50 lakh | **3.6 bps** |

These figures are **before spread, slippage and market impact**. They are a fee-only reference calculation, not a historical execution estimate. Exact costs vary with broker, order count, turnover and account-specific terms.

The historical **5-bps round-trip sensitivity remains a stress-test threshold, not a universal current all-in cost estimate**.

### Strategy 003 — current gate

The frozen candidate is:

- `close_location_1bar + intraday_position_60bar`;
- additive OLS;
- training-only standardization;
- next 5-minute cross-sectional excess return;
- same 15-stock eligible universe.

Protected validation is the next and final predictive gate. It must use 2026-06-10 through 2026-08-19 only. The final holdout beginning 2026-08-20 remains untouched.

If protected prediction survives, the next step is the preregistered economic execution viability test using current statutory/broker costs plus separately frozen spread/slippage/impact scenarios. If prediction fails, Strategy 003 closes without a rescue search.

Protocols:
- `research/journal/003_protected_validation_protocol.md`
- `research/journal/003_economic_execution_viability_protocol.md`
- `research/journal/003_execution_cost_basis_research_20260923.md`

## Strategy 003 — protected prediction gate passed

The frozen additive 003H candidate passed protected chronological validation for **2026-06-10 through 2026-08-19**:

| Metric | Protected result |
|---|---:|
| Mean IC | **+0.08136** |
| Mean rank IC | **+0.10082** |
| Q1–Q5 spread | **+1.6870 bps** |
| Positive IC fraction | **60.76%** |
| Timestamps | **711** |
| Observations | **10,665** |
| Equities | **15** |

The development references were +0.0696 mean IC, +0.0826 rank IC and +2.2168 bps spread. The protected spread retains approximately 76% of the development magnitude and preserves direction.

A coverage limitation is recorded: the frozen 60-bar feature warm-up means scored observations occur approximately 14:10–15:20 IST. This does not establish all-day stability and was not repaired after validation.

**Strategy 003 now advances to the frozen economic execution viability test.** No further alpha discovery or prediction tuning is authorized. The final holdout beginning 2026-08-20 remains untouched.

Economic runner: scripts/run_strategy_003_economic_execution.py.

Economic protocol: research/journal/003_economic_execution_viability_protocol.md.

## Strategy 003 — economic execution status (24 September 2026)

The first economic execution attempt is **invalidated** and is not used for the Strategy 003 decision gate. The run reported 1,060.333× cumulative turnover and ₹53,091.53 of fees on a ₹1,00,000 portfolio notional, exposing an implementation/accounting problem.

The runner has since been corrected to:
- compound the sequence of one-bar portfolio returns;
- distinguish cumulative portfolio P&L from cumulative executed turnover;
- apply per-order brokerage and statutory charges to actual rupee turnover;
- preserve the frozen Q5-long/Q1-short, equal-notional, one-bar portfolio rule;
- retain late-session/CAS diagnostics;
- keep the final holdout beginning 2026-08-20 untouched.

**Economic execution first run invalidated; corrected rerun required before any pass/fail decision.**
