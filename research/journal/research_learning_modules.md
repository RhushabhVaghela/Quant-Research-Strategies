# Quant Research Learning Modules

## Purpose

This is the project's reusable learning layer. It records what the research process has taught us, not just which trading ideas were tested.

The central lesson is:

> The durable skill is not discovering one profitable rule. It is learning how to turn a market observation into a falsifiable research question, test it without leaking future information, understand what the evidence actually says, and know when to stop.

This module is linked to the historical Strategy 001, Strategy 002, and Strategy 003 research records. It does not rewrite their original findings.

---

## Module 1 — Hypothesis Formation

### Core idea

A quant researcher starts with a **testable claim**, not a backtest.

A good hypothesis specifies the economic mechanism, population/instruments, information available at decision time, prediction target, expected relationship, and conditions under which the effect should weaken or disappear.

### Strategy 001 lesson

Strategy 001 began with an explicit mean-reversion hypothesis. The data contradicted it. Rather than force the intended result, the research recorded the rejection and investigated the continuation structure that was actually observed.

### Strategy 002 lesson

Strategy 002 began from a cross-sectional residual-reversal observation and converted that observation into a precise leave-one-out residual formulation before executable testing.

### Strategy 003 lesson

Strategy 003 changed the research question to next-5-minute cross-sectional prediction. The model was not treated as the hypothesis; the economic mechanism had to be interpreted after predictive information was established.

### What to remember

**Observation → hypothesis → test. Not backtest → story.**

---

## Module 2 — Leakage and Point-in-Time Thinking

Leakage occurs when future or unavailable information influences a feature, target, model fit, universe, or trading decision.

For every feature ask:

> **Could I have known this value at the exact moment I claim the decision was made?**

### Project lessons

- Strategy 001 separated signal time, next-bar entry, and later exit; signal construction stayed session-local.
- Strategy 002 used a point-in-time leave-one-out cross-sectional residual.
- Strategy 003 fit standardization on training data and used chronological purging; protected periods were excluded from candidate selection.

---

## Module 3 — Chronological Validation

Financial observations are time ordered. Random train/test splits can mix future market states into training.

The project's progression is **development → validation → holdout → prospective**. When the target looks forward, split boundaries are purged by the relevant future horizon.

### Project lessons

Strategy 001 progressed from event study to fixed backtest, chronological robustness/OOS diagnostics, and prospective paper/shadow testing.

Strategy 002 fixed development/validation/holdout boundaries and did not use the protected holdout to rescue a failed cost gate.

Strategy 003 uses a one-decision-timestamp purge for its next-5-minute target.

---

## Module 4 — Holdout Protection

A holdout is valuable only while it is genuinely unseen.

Using holdout results to choose thresholds, features, models, universes, or rescue rules turns the holdout into another development set.

### What the project teaches

Strategy 001 preserved frozen implementations and did not back-fill later prospective observations into the historical rule.

Strategy 002 closed the tested executable research line without using its protected final holdout to search for a rescue configuration.

Strategy 003 has kept its project validation and final holdout outside current discovery/characterization.

**Once a protected sample influences a research decision, its original protection is gone.**

---

## Module 5 — Cross-Sectional Prediction

Cross-sectional research asks whether observable information can rank assets by their future relative returns at the same timestamp.

Strategy 003 defines the target as next-5-minute return minus the equal-weight cross-sectional mean at that future timestamp.

The question becomes:

> Can information available now distinguish which eligible assets will have relatively higher or lower next-bar returns?

This differs from forecasting broad market direction.

---

## Module 6 — IC, Rank IC, and Quintile Analysis

### IC

Information Coefficient measures the cross-sectional association between predicted scores and subsequent realized returns.

### Rank IC

Rank IC measures the association after converting both sides to ranks. It focuses on ordering rather than score scale.

### Quintiles

Quintile analysis sorts assets into five score groups and measures subsequent returns in Q1 through Q5. A positive Q5-minus-Q1 spread means the high-score group had higher average subsequent relative returns.

### Strategy 003 lesson

The first 003 development-test diagnostic showed broad directional ordering with a small non-monotonic middle: Q1 averaged negative next-bar excess return, Q5 positive, with about +2.22 bps Q1-to-Q5 separation for the frozen OLS diagnostic.

That was predictive evidence, **not strategy P&L**.

---

## Module 7 — Feature Attribution

Attribution asks which registered inputs explain a model's predictive relationship. It must not silently become a feature-selection contest.

### Strategy 003 lesson

003H compared single features, all pairs, and the fixed three-feature reference.

The main result was that `close_location_1bar` carried substantial standalone signal; `intraday_position_60bar` was weak alone; the pair reproduced the all-three diagnostic essentially exactly; and `bars_since_session_open` added no measurable contribution under the frozen availability design.

**Attribution asks 'what explains the model?' Feature selection asks 'what should I trade?'**

---

## Module 8 — Common-Support Controls

Two models can appear different simply because they were evaluated on different observations.

Common-support control forces nested comparisons onto the same complete-case observations.

### Strategy 003 lesson

An initial residual-family comparison appeared to show a small positive market-context contribution. After common-support control, that apparent increment disappeared.

### What to remember

Before comparing models, check the same rows, timestamps, universe, target, split, and information boundary.

---

## Module 9 — Mechanism Decomposition

Once a predictive relationship is found, do not immediately turn every feature into a strategy.

Mechanism decomposition asks:

> Can a small, interpretable set of variables explain a meaningful portion of the predictive relationship?

### Strategy 003 lesson

The frozen full model's development-test spread was about +2.22 bps. The locked 003H mechanism retained about +1.78 bps, showing that the bar-shape/intraday-state family explained a substantial component but not all of the observed structure.

The later attribution narrowed the provisional core to current-bar close location plus recent intraday position.

---

## Module 10 — Transaction-Cost Effects

Gross return is not the same as tradable economics. Spread, slippage, fees, market impact, turnover, and execution constraints can erase a small intraday effect.

### Strategy 001 lesson

Positive gross performance remained highly sensitive to realistic friction, which became a central reason not to promote the implementation.

### Strategy 002 lesson

The fixed executable baseline produced only about +0.0896 bps mean gross return per portfolio observation, and the predefined cost sensitivity overwhelmed it. Turnover-reduction variants did not establish sufficient cost-resilient economics.

### Strategy 003 lesson

The current +~1.8 to +2.2 bps diagnostic separation is predictive evidence only. Cost and execution testing come later, after the explanatory hypothesis is frozen.

**A small gross edge is not 'almost profitable.' It may be economically zero after implementation costs.**

---

## Module 11 — Lineage Testing

A new strategy ID should represent a genuinely different return mechanism, not a renamed version of an old one.

### Strategy 003 lesson

The 003H core was tested against explicit frozen representations of Strategy 001 continuation and Strategy 002 leave-one-out residual reversal.

The combined model still retained the 003H relationship, providing evidence against direct representational duplication of those registered mechanisms.

This is not proof of causal independence and does not test every possible return-based mechanism.

### What to remember

> **Is this genuinely new information, or did I teach the model an old idea using different words?**

---

## Module 12 — Negative Research Results

A rejected hypothesis is a successful research outcome when the experiment was designed correctly.

### Strategy 001 lesson

The original mean-reversion hypothesis was rejected and preserved as historical evidence.

### Strategy 002 lesson

The tested executable residual-reversal line was closed after failing its economic/cost gate. That did not establish that every residual-reversal idea is impossible.

### Strategy 003 lesson

The original daily 1-day/5-day prediction work was superseded when the project objective was aligned explicitly with intraday research. The earlier analysis was preserved rather than erased.

**'Failed' and 'learned nothing' are not synonyms.**

---

## Module 13 — Closing a Research Branch

Continuing to search after repeated weak results creates sequential-search and data-snooping risk.

### Strategy 001 lesson

After extensive discovery, fixed implementation testing, execution analysis, chronological robustness work, prospective paper/shadow observations, and a secondary cross-sectional development search, the tested family was closed for the current capital-pursuit program.

### Strategy 002 lesson

The fixed baseline and preregistered turnover-reduction variants failed the cost-resilience gate, so the tested executable line was closed without reopening protected data.

### Strategy 003 lesson

The program has an explicit gate structure:

**current development evidence → final economic-form decomposition → hard decision gate → close OR freeze → protected validation**

Knowing when **not** to run another backtest is itself a quantitative research skill.

---

## Module 14 — From Research to Strategy

The project separates:

**pattern → predictive information → economic mechanism → hypothesis → strategy → validation → prospective evidence**

A model score is not automatically a signal. A signal is not automatically a portfolio. A positive backtest is not automatically validated alpha.

Strategy construction must define universe, signal timing, execution, holding period, position sizing, costs, risk controls, and overlap rules before the relevant validation stage.

Strategy 001D is the clearest project example of the bridge from an interpreted continuation hypothesis to a frozen executable rule.

---

## Module 15 — Research Decision Making

Before advancing an idea, ask:

1. What exactly did we observe?
2. What hypothesis explains it?
3. What information was available at decision time?
4. Could the result be leakage or support mismatch?
5. Was the split chronological and protected?
6. Is the effect broad across timestamps and stocks?
7. Does the economic mechanism make sense?
8. Is it materially distinct from existing strategy lineage?
9. Is the gross magnitude large enough to justify execution testing?
10. What is the predefined stopping rule?
11. What evidence would falsify the idea?
12. What data remain genuinely untouched?

## The real output of the project

The output is not only a collection of strategy files. It is a reusable research process:

**design → test → falsify → characterize → control → freeze → validate → stop when warranted.**

## Project linkage

Read this module alongside the individual strategy records:

- Strategy 001: hypothesis rejection, continuation attribution, frozen execution, cost sensitivity, chronological/OOS discipline, prospective testing, closure.
- Strategy 002: residual-reversal discovery, leave-one-out construction, fixed executable baseline, turnover/cost gate, closure.
- Strategy 003: predictive-information discovery, IC/rank IC/quintiles, attribution, common support, mechanism decomposition, lineage testing, final economic-form gate.