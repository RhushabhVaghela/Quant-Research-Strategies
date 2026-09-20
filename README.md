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

## Strategy 002 — Intraday pairs mean reversion

Strategy 002 is the project's relative-value/statistical-arbitrage research family for Indian equities. It is deliberately distinct from Strategy 001's directional continuation hypothesis.

### Current status

The formation-only screen has completed on the locked U1 universe and selected **1 pair**. The local test suite passed with **104 tests** at formation completion. No development or holdout P&L has been loaded or used in pair selection.

The next step is the preregistered **108-configuration development grid** using the frozen pair set. Development covers 2026-06-10 through 2026-08-19; the holdout (2026-08-20 through 2026-09-17) remains locked until a candidate freeze record is completed.

See `research/journal/002_intraday_pairs_mean_reversion_spec.md`, `src/research/strategy_002_pairs.py`, and `scripts/run_strategy_002_development.py`.

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

Install dependencies:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

Run the complete test suite:

```powershell
pytest
```

The immediate active work is Strategy 002 development: use the frozen formation pair set, run the preregistered 108 configurations on the development window, inspect breadth/stability and correctly defined two-leg cost sensitivity, then freeze or reject a candidate before opening the holdout.
