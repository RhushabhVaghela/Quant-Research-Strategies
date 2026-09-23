# Strategy 003 — Protected Validation Protocol

**Status:** 🟢 Executed once; protected prediction gate passed. Economic execution test now frozen.

## 1. Purpose

Strategy 003 has completed its authorized development-stage discovery, characterization, mechanism decomposition, common-support control, component attribution, lineage separation, and economic-form decomposition.

The remaining predictive evidence question is whether the **frozen 003H additive two-variable form** survives the protected chronological validation period without retuning.

The protected test is now authorized. Its results must be generated once from the frozen specification before any decision is made.

## 2. Frozen candidate

The candidate is frozen **before reading protected-validation results**:

- universe: the same 15 eligible equities used in development;
- target: next 5-minute cross-sectional excess return;
- signal information: close_location_1bar and intraday_position_60bar only;
- model: additive OLS with training-only standardization;
- training data: all eligible observations through **2026-06-09**;
- validation data: **2026-06-10 through 2026-08-19**;
- no interaction term;
- no close-location-only substitution;
- no thresholds;
- no holding-period search;
- no nonlinear model;
- no cost-based parameter changes;
- no universe changes.

The close-location-only development finding remains explanatory evidence only and is **not** substituted into validation.

## 3. Protected boundary

- development evidence ends: **2026-06-09**
- protected validation begins: **2026-06-10**
- final holdout begins: **2026-08-20**
- final holdout: **untouched**

The validation runner must not read, score, optimize against, or otherwise inspect observations from 2026-08-20 onward.

## 4. Frozen evaluation

The runner reports:

- mean IC;
- mean rank IC;
- timestamp-level IC distribution;
- Q1–Q5 realized next-bar excess returns;
- Q1–Q5 spread;
- stock breadth;
- timestamp coverage;
- observations per timestamp;
- comparison with the frozen development reference;
- overlap/dependence diagnostics.

The diagnostic IC IR is descriptive only. Intraday observations are not assumed independent.

## 5. No post-validation tuning

Once the protected result is visible, do not:

- change the feature set;
- replace additive OLS with the interaction;
- substitute close-location-only;
- change the universe;
- change the horizon;
- change the holding period;
- tune thresholds;
- alter the cost basis to improve the result;
- inspect the final holdout;
- reopen Strategies 001 or 002.

## 6. Decision gate

### Prediction survives

If the frozen relationship preserves direction and a materially meaningful fraction of its development magnitude without rescue rules, proceed to the separately registered economic-execution test.

### Prediction fails

If the relationship substantially weakens, reverses, or becomes economically negligible, close Strategy 003 for the current research line. Do not inspect the final holdout to rescue the result.

### Ambiguous

Record the ambiguity and stop. Do not tune until a new research line is explicitly registered.

## 7. Execution-economics gate

If prediction survives, the next test is **not another alpha search**. It is a frozen executable implementation with:

1. explicit portfolio construction;
2. actual position sizing/turnover definition;
3. current statutory/broker charges;
4. separate spread/slippage assumptions;
5. separate market-impact assumptions;
6. pre-registered low/base/stress scenarios.

The current cost basis is documented in research/journal/003_execution_cost_basis_research_20260923.md.

## 8. Evidence boundary

This protocol authorizes one protected predictive test. It does **not** claim that the validation has been run. The final holdout remains protected until a later, separately justified decision.
## 9. Protected-validation result — 23 September 2026

| Metric | Development reference | Protected validation |
|---|---:|---:|
| Mean IC | +0.0696 | **+0.08136** |
| Mean rank IC | +0.0826 | **+0.10082** |
| Q1–Q5 spread | +2.2168 bps | **+1.6870 bps** |
| Positive timestamp IC fraction | — | **60.76%** |
| Usable timestamps | — | **711** |
| Observations | — | **10,665** |
| Stocks | 15 | **15** |

Protected Q1–Q5 mean next-bar excess returns were **−0.8952, −0.3388, −0.1837, +0.6259, +0.7918 bps**. The ordering is directionally coherent.

The protected Q1–Q5 spread retains approximately **76%** of the development-test magnitude while preserving direction. Mean IC and rank IC are higher than the development reference.

**Decision:** the frozen predictive relationship passes the preregistered prediction gate. Strategy 003 advances to the separately registered economic-execution test.

### Coverage caveat

The 711 protected timestamps occur only from approximately **14:10 through 15:20 IST** because of the frozen 60-bar within-session warm-up. The sample covers **50 trading dates**, but it does not establish all-day stability. This limitation is recorded rather than repaired after seeing the result.

The final holdout beginning **2026-08-20 remains untouched**.