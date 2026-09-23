# Strategy 003H — Lineage Separation / Mechanism Falsification Protocol

**Status:** 🟡 Preregistered development-only experiment — no protected validation, no holdout, no strategy promotion.

## 1. Research question

The component attribution experiment established a provisional 003H explanatory core:

- `close_location_1bar`
- `intraday_position_60bar`

The next question is whether this predictive information is economically distinct from the two previously closed intraday research mechanisms:

- **Strategy 001:** short-horizon continuation after unusually strong intraday moves, represented by the frozen event ingredients `z_score >= 2` and `prior_return_6bar > 0`;
- **Strategy 002:** short-horizon cross-sectional residual reversal, represented by the point-in-time leave-one-out prior-bar residual return.

The purpose is **falsification/lineage separation**, not feature selection. The test asks whether the 003H core still explains next-bar cross-sectional excess returns after the old mechanisms are explicitly represented.

## 2. Fixed lineage representations

### Strategy 001 lineage proxy

Use exactly the frozen 001 event definition:

`001_event = (z_score >= 2.0) AND (prior_return_6bar > 0)`

where:

- `z_score` uses the current close relative to the mean/std of the prior 30 session bars;
- `prior_return_6bar = close[t-1] / close[t-7] - 1`;
- all inputs are point-in-time and session-local.

The fixed event proxy is used as a lineage marker, not as a new Strategy 001 search.

### Strategy 002 lineage proxy

Use the prior-bar leave-one-out cross-sectional residual:

`residual_1bar[t] = return_i[t] - mean(return_j[t] for j != i)`

where the mean is computed only from the other eligible equities at timestamp (t). This reproduces the economic information source used in the Strategy 002 leave-one-out residual work without importing Strategy 002's trading rule or thresholds.

## 3. Fixed model specifications

Evaluate exactly these five specifications:

1. **003H core:** close location + intraday position.
2. **001 lineage only:** 001 event proxy.
3. **002 lineage only:** leave-one-out prior residual.
4. **001 + 002 lineage:** both old-mechanism proxies.
5. **003H core + 001 + 002:** all registered lineage variables together.

No other features are permitted.

The purpose is to compare whether the 003H core retains predictive information conditional on the old mechanisms. The all-variable model is not an optimized model and must not be selected for performance.

## 4. Data and target

- Same 15 eligible equities used by 003H.
- Same NIFTYBEES market reference only for the inherited 003 panel construction.
- Same next-5-minute target:
  `close[t+1] / close[t] - 1`, less the equal-weight cross-sectional mean at (t+1).
- Same exploratory/development window: 2025-09-18 through 2026-06-09.
- Same chronological internal split and one-decision-timestamp purge.
- No validation-period observations and no final-holdout observations.

The 003H core requires the existing 60-bar warm-up, so all five specifications are evaluated on the common complete-case support created by the full registered variable set. This avoids attributing support changes to mechanism differences.

## 5. Evaluation

For each specification report:

- mean timestamp-level IC;
- mean rank IC;
- descriptive IC IR;
- positive IC fraction;
- Q1–Q5 realized next-bar excess returns;
- Q1–Q5 spread;
- usable timestamps and observations;
- development-test versus validation comparison.

The primary lineage question is whether adding the 003H core to the old-mechanism-only model produces meaningful incremental predictive information, and whether the 003H core remains predictive when the old mechanisms are included.

## 6. Decision rules

### Distinct 003 information

If the 003H core remains materially predictive in the combined model and the combined model does not eliminate the core's ordering, the evidence supports treating 003H as **not directly explained by the registered 001/002 mechanisms**.

This still does not establish a causal mechanism or tradable alpha.

### Old-mechanism explanation

If the combined model removes most of the 003H core's predictive contribution and the old-mechanism-only model reproduces the relevant ordering, the 003H signal should be treated as likely overlapping with an existing research lineage rather than promoted as a distinct Strategy 003 mechanism.

### Inconclusive

If results are unstable, support is insufficient, or the representations cannot cleanly distinguish the mechanisms, retain 003H as unresolved and do not promote it.

No outcome authorizes protected validation automatically.

## 7. Prohibited activities

This experiment must not:

- search thresholds;
- change the 001 event threshold of 2.0;
- change the 6-bar continuation window;
- change the 002 leave-one-out construction;
- add new return features;
- add feature transforms or interactions;
- search holding periods;
- optimize costs;
- select a universe;
- run nonlinear models;
- access protected validation or final holdout data;
- construct a portfolio.

## 8. Repository lineage references

Relevant frozen implementations are:

- `src/research/continuation_backtest.py` for Strategy 001's point-in-time `z_score` and `prior_return_6bar` construction;
- `scripts/run_strategy_002_leave_one_out_residual.py` for Strategy 002's leave-one-out residual construction;
- `scripts/run_strategy_003_prediction_discovery.py` for the frozen 003 target and panel construction.

These are reused as methodological references, not as strategy candidates.

## 9. Evidence boundary

The experiment is development-only. The project validation period beginning 2026-06-10 and final holdout beginning 2026-08-20 remain protected.
