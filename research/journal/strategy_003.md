# Strategy 003 — Intraday Prediction and Economic Execution

## 1. Why Strategy 003 was different

Strategies 001 and 002 were both built around explicit short-horizon price-pattern hypotheses.

The third research program changed the question:

> **Can observable, point-in-time market information predict cross-sectional differences in very short-horizon future returns, without assuming a particular trading rule in advance?**

This made Strategy 003 a **prediction-discovery program first**.

The methodological principle was:

> **ML is an extraction tool, not the economic hypothesis.**

The goal was to identify predictive information, understand what that information represented, and only then test whether it could support a trading strategy.

## 2. The original 1-day / 5-day experiment and why it was superseded

The initial Strategy 003 draft used **1-day and 5-day targets**.

That work was not abandoned because of the observed result. It was superseded because the broader research objective was specifically **intraday strategy research**.

A five-trading-day close-to-close target is a medium-horizon stock-selection problem. It answers a different question from the one Strategy 003 ultimately needed to answer.

The daily experiment therefore remains historical research evidence, while the active Strategy 003 definition was re-registered at the native intraday decision horizon.

This was an **objective-alignment decision**, not result-driven rewriting.

## 3. Why the revised target was the next 5-minute return

The available equity data was sampled at five-minute intervals, and Strategies 001 and 002 had already established five-minute bars as the research's native intraday resolution.

The revised target was:

`Close(t+1 bar) / Close(t) - 1`

converted into a **cross-sectional excess return** by subtracting the equal-weight mean next-bar return across the eligible equities.

Why not start with 15 minutes?

Because a 15-minute target would aggregate two intermediate five-minute observations before we knew whether the information disappeared after one bar or persisted.

Five minutes was therefore the **discovery horizon**, not a permanent commitment to a five-minute holding period.

## 4. Why the Strategy 002 data layer was reused

The revised Strategy 003 experiment reused the existing Indian-equity five-minute OHLCV data layer.

This was intentional:

- the data had already passed structural quality checks;
- the cross-sectional universe was already available;
- the five-minute sampling preserved comparability with earlier research;
- reusing the data layer reduced the risk that a new result was simply caused by a completely different acquisition process.

The active discovery set contained **15 eligible Indian equities**.

The universe still had a known broker-native survivorship / point-in-time limitation, so it was suitable for discovery-stage research but was not silently treated as perfect historical membership.

## 5. Why the four initial feature families were chosen

The first feature registration was designed around broad observable market state rather than a predetermined trading rule.

### Liquidity / activity

Examples included current log volume and rolling volume changes.

Reason: changes in participation and activity can affect short-horizon price formation.

### Volatility / state

Examples included short and longer realized volatility and current range information.

Reason: the same price move can have different meaning in a quiet market versus a rapidly changing one.

### Bar shape / intraday state

Examples included:

- `close_location_1bar`;
- `intraday_position_60bar`;
- session-clock information.

Reason: the current bar shows where trading finished within the observed range and where the asset sits within its recent intraday path.

### Market context

Examples included the contemporaneous NIFTYBEES return and market volatility.

Reason: cross-sectional stock predictions may depend partly on the state of the broader market.

Cross-sectional ranks and z-scores were included as registered transforms.

### Why continuation and reversal variables were explicitly excluded

The new research could not simply disguise Strategies 001 and 002 as a machine-learning strategy.

So the initial registration excluded:

- Strategy 001-style z-score continuation events;
- signed-return direction rules;
- Strategy 002-style residual reversal;
- direct encodings of the two closed mechanisms.

This became the Strategy 003 **lineage guardrail**.

## 6. Why the model ladder started with OLS and Ridge

The initial model ladder was fixed:

```text
zero baseline
      ↓
OLS
      ↓
fixed Ridge
```

**OLS (ordinary least squares)** provided an interpretable baseline.

**Ridge regression** added a fixed regularization penalty to reduce unstable coefficients when features are correlated.

The reason for starting here was diagnostic.

The research first needed to answer:

> **Is there predictive information at all, and can a simple model expose it?**

There was no reason to escalate to tree models or neural networks before establishing that a simpler model contained useful information.

## 7. First discovery result — a measurable prediction ordering appeared

The controlled discovery run used:

- **15 eligible Indian equities**;
- **39 registered model features** including registered transforms;
- next-5-minute cross-sectional excess return;
- development data through **2026-06-09**;
- one-decision-timestamp chronological purging;
- zero baseline, OLS and fixed Ridge α=1.

The frozen OLS model produced:

- **mean IC: +0.0696**;
- **mean rank IC: +0.0826**;
- **Q1–Q5 spread: +2.2168 bps**.

The prediction quintiles were:

| Prediction quintile | Mean next-bar excess return |
|---|---:|
| Q1 | −1.1230 bps |
| Q2 | −0.1004 bps |
| Q3 | −0.1497 bps |
| Q4 | +0.2794 bps |
| Q5 | +1.0937 bps |

The endpoints formed a clear low-to-high ordering, although the middle buckets were not perfectly monotonic.

### Why this changed the research question

This was more informative than a single average model statistic.

The predictions were separating the cross-section in the direction expected by the model score.

So the next question became:

> **What information was actually creating that separation?**

The correct next step was characterization, not immediate P&L optimization.

## 8. Tail sensitivity and model comparison

The OLS spread showed:

- raw mean spread **+2.2168 bps**;
- median spread **+2.6083 bps**;
- raw standard deviation **10.8615 bps**;
- winsorized mean **+2.2947 bps**;
- positive-spread fraction **61.31%**.

The similarity between the raw and winsorized means suggested that the average separation was not created entirely by a handful of extreme timestamps.

The result was still noisy because the spread's standard deviation was much larger than its mean.

OLS and fixed Ridge score predictions were almost identical:

**correlation ≈ 0.9999999**

### Why this changed the next step

There was no evidence that model complexity was creating a materially different ordering.

The research therefore moved toward **economic interpretation** rather than model escalation.

## 9. Feature-family decomposition

Development-test Q1–Q5 spreads were:

| Feature family | Mean spread |
|---|---:|
| Activity | +0.2125 bps |
| Volatility | +0.9845 bps |
| Bar shape / intraday state | +1.7537 bps |
| Market context | −0.0952 bps |

Bar shape / intraday state produced the largest descriptive contribution.

This did not mean that the family was automatically the final model. It changed the research question:

> **Can an interpretable intraday-state mechanism explain a meaningful portion of the prediction ordering?**

That led to 003H.

## 10. 003H — mechanism decomposition

The registered 003H mechanism used exactly:

- `close_location_1bar`;
- `intraday_position_60bar`;
- `bars_since_session_open`.

The experiment stayed within the development sample.

The purpose was **explanation**, not feature selection.

The mechanism-only model retained:

- development mean IC **+0.0585**;
- development rank IC **+0.0727**;
- development Q1–Q5 spread **+1.784 bps**.

Its development quintiles were:

| Quintile | Mean next-bar excess return |
|---|---:|
| Q1 | −0.6272 bps |
| Q2 | −0.6268 bps |
| Q3 | −0.2214 bps |
| Q4 | +0.3182 bps |
| Q5 | +1.1572 bps |

The model therefore retained the broad low-to-high ordering.

However, the frozen full model still had a larger development spread of **+2.2168 bps**.

### Interpretation

The three intraday-state variables explained a substantial part of the observed predictive structure, but not all of it.

So the next question became:

> **Where is the remaining information, and is it genuinely different from the mechanisms already tested in Strategies 001 and 002?**

## 11. Common-support control — make feature-family comparisons comparable

Different feature blocks did not always have exactly the same usable timestamps.

Comparing their metrics directly could therefore mix **model differences with sample differences**.

A common-support nested comparison was introduced.

The development-test incremental results were:

- activity: **−0.00270 mean IC**, **−0.00106 rank IC**, **−0.155 bps Q1–Q5**;
- volatility: **−0.01602 mean IC**, **−0.01294 rank IC**, **−0.349 bps**;
- market context: **+0.00047 mean IC**, **+0.00125 rank IC**, **−0.001 bps**.

The earlier apparent market-context contribution did not survive common-support comparison.

### Why the research moved on

The residual feature-family branches did not provide a convincing additional explanatory component under the registered specification.

The focus returned to the smaller 003H core.

## 12. Component attribution — which 003H variables carried the information?

The next controlled experiment compared the three 003H variables individually and in fixed combinations.

The results were:

| Specification | Mean IC | Rank IC | Q1–Q5 spread |
|---|---:|---:|---:|
| `close_location_1bar` | +0.04107 | +0.04799 | +0.930 bps |
| `intraday_position_60bar` | +0.00265 | +0.02668 | +0.184 bps |
| `bars_since_session_open` | not scored | not scored | not scored |
| close location + intraday position | +0.05849 | +0.07274 | +1.787 bps |
| all three | +0.05849 | +0.07272 | +1.784 bps |

The close-location + intraday-position pair reproduced the all-three model essentially exactly on common support.

### Why this led to lineage separation

The experiment had explained the representation, but one question remained:

> **Could these variables simply be proxies for the old Strategy 001 or Strategy 002 mechanisms?**

That was more important than immediately deciding that the pair was the final model.

## 13. Lineage separation — test for direct duplication of Strategies 001 and 002

A fixed development-only comparison used:

1. 003H core;
2. Strategy 001 event proxy;
3. Strategy 002 leave-one-out residual proxy;
4. both old mechanisms together;
5. 003H + both old mechanisms.

Results:

| Model | Mean IC | Rank IC | Q1–Q5 spread |
|---|---:|---:|---:|
| 003H core | +0.05849 | +0.07274 | +1.787 bps |
| 001 lineage | +0.00991 | +0.01842 | +0.013 bps |
| 002 lineage | +0.02801 | +0.04038 | +0.644 bps |
| 001 + 002 | +0.02815 | +0.04059 | +0.638 bps |
| 003H + 001 + 002 | +0.05577 | +0.06774 | +1.848 bps |

Adding the two older mechanisms did not remove the 003H cross-sectional ordering.

### Interpretation

Under the registered feature definitions, the research did not find direct representational duplication of Strategies 001 and 002.

This is not proof of causal independence.

It did justify keeping the 003H information source as a distinct research line.

The next question was therefore:

> **What is the simplest economically interpretable form of the 003H core?**

## 14. Economic-form decomposition

The final development-stage representation test compared:

| Specification | Mean IC | Rank IC | Q1–Q5 spread |
|---|---:|---:|---:|
| close-location only | +0.08419 | +0.09205 | +2.358 bps |
| intraday-position only | +0.00309 | +0.02768 | +0.219 bps |
| additive core | +0.05928 | +0.07355 | +1.780 bps |
| joint interaction | +0.06070 | +0.07258 | +1.871 bps |

The interaction increased mean IC by only **+0.00142** and Q1–Q5 spread by about **+0.090 bps**, while rank IC decreased slightly.

### Interpretation

There was no compelling evidence for a distinct interaction mechanism under the registered representation.

The explanatory evidence was therefore most consistent with a **close-location-dominant additive interpretation**.

This remained explanatory evidence; it was not permission to replace a frozen model after seeing the result.

## 15. Why protected validation came next

The exploratory/development research had now answered:

- whether predictive ordering existed;
- which feature family carried much of it;
- whether the main representation was distinct from Strategies 001/002;
- whether a more complex interaction materially changed the structure.

The candidate was frozen as:

- `close_location_1bar + intraday_position_60bar`;
- additive OLS;
- training-only standardization;
- 15-stock universe;
- next 5-minute cross-sectional excess return.

The protected period **2026-06-10 through 2026-08-19** was now used for the predictive validation test.

The final holdout beginning **2026-08-20** remained untouched.

## 16. Protected prediction result

The frozen candidate produced:

| Metric | Development | Protected validation |
|---|---:|---:|
| Mean IC | +0.0696 | **+0.08136** |
| Mean rank IC | +0.0826 | **+0.10082** |
| Q1–Q5 spread | +2.2168 bps | **+1.6870 bps** |

Additional protected results:

- **60.76% positive IC fraction**;
- **711 timestamps**;
- **10,665 observations**;
- **15 equities**.

The protected spread retained approximately 76% of the development magnitude and preserved direction.

### Coverage limitation

The frozen 60-bar within-session features meant the scored observations were concentrated roughly between **14:10 and 15:20 IST**.

This is a feature-availability limitation.

It was not turned into a new afternoon filter after seeing the result.

### Why economic execution became the next gate

The prediction had survived protected chronological validation.

But prediction quality is not the same thing as portfolio economics.

The next question became:

> **What happens when the frozen predictions are translated into actual positions and actual rupee execution costs?**

## 17. The first economic execution output was invalidated

The first execution prototype produced a very large cumulative turnover and fee figure.

Before treating that as economic evidence, the implementation was audited.

The prototype had:

- normalized unit notionals for brokerage;
- simplified full-refresh turnover accounting;
- incomplete operational treatment of the late-session auction regime.

So the economic output was **invalidated**, rather than used to close or promote the strategy.

The runner was corrected before the final economic decision.

## 18. Corrected economic execution test

The corrected implementation used:

- **₹1,00,000** gross portfolio notional;
- Q5 long / Q1 short;
- 50% / 50% gross split;
- equal notional within each side;
- one 5-minute holding bar;
- actual executed order turnover;
- brokerage and statutory charges;
- separately frozen low/base/stress execution scenarios;
- late-session / possible closing-auction diagnostics.

The final holdout was not used.

The corrected run produced:

- **711 portfolio timestamps**;
- **5,720 executed orders**;
- **₹106,033,333.33 cumulative executed turnover**;
- **1,060.333×** initial gross notional turnover;
- **+6.1708% gross compounded return**.

The large cumulative turnover is an execution-intensity measure: the same ₹1,00,000 notional can be redeployed repeatedly over 711 sequential observations.

### Cost results

| Scenario | Gross cumulative | Total cost | Net cumulative |
|---|---:|---:|---:|
| Fee floor | +6.1708% | ₹53,091.53 | **−46.9207%** |
| Low | +6.1708% | ₹63,694.86 | **−57.5241%** |
| Base | +6.1708% | ₹68,996.53 | **−62.8257%** |
| Stress | +6.1708% | ₹84,901.53 | **−78.7307%** |

Fee breakdown:

| Charge | Amount |
|---|---:|
| Brokerage | ₹31,810.00 |
| STT | ₹13,254.17 |
| Stamp duty | ₹1,590.50 |
| SEBI | ₹106.03 |
| GST | ₹6,330.83 |
| **Total** | **₹53,091.53** |

The fee-floor case alone produced a strongly negative net result.

## 19. Final interpretation

Strategy 003 answered two separate questions.

### Prediction gate

The frozen prediction relationship **passed** protected chronological validation.

### Economic execution gate

The frozen Q5-long / Q1-short one-bar portfolio **failed** the economic execution test because turnover and execution costs overwhelmed the gross return.

The research chain was:

```text
broad prediction question
        ↓
native 5-minute target
        ↓
feature-family discovery
        ↓
OLS / Ridge baseline
        ↓
Q1–Q5 predictive ordering
        ↓
tail and model checks
        ↓
mechanism-family decomposition
        ↓
003H intraday-state mechanism
        ↓
common-support control
        ↓
component attribution
        ↓
001/002 lineage separation
        ↓
economic-form decomposition
        ↓
frozen additive candidate
        ↓
protected prediction gate — passed
        ↓
economic execution gate — failed
        ↓
Strategy 003 closed
```

The main lesson is:

> **Prediction quality and trading economics are separate research questions.**

A model can contain useful predictive information and still fail as a trading strategy once the portfolio implementation and execution costs are included.

No post-result threshold, holding-period, time-of-day, symbol, universe, nonlinear-model or cost-rescue search was opened after the economic result. The final holdout remained untouched.

## Key terms

**Cross-sectional prediction:** predicting which assets should outperform or underperform relative to their peers.

**IC:** correlation between predicted scores and later returns.

**Rank IC:** the same relationship using rank order.

**Quintile spread:** the average future return of the highest-score group minus the lowest-score group.

**OLS:** ordinary least squares regression.

**Ridge:** linear regression with an L2 regularization penalty.

**Feature engineering:** converting raw market data into variables a model can use.

**Common support:** compare model specifications using the same observations.

**Lineage separation:** testing whether a new result is merely re-encoding an older strategy mechanism.

**Protected validation:** a chronological period kept out of candidate selection.

**Turnover:** the amount of portfolio notional bought and sold.

**Economic execution gate:** the stage where predictive information is translated into positions and tested against actual cost assumptions.

## Status

**Closed — protected prediction passed, but the frozen executable implementation failed the economic execution gate.**