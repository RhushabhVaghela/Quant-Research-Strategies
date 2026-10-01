# Strategy 001 — Intraday Continuation Research

## 1. Where the research started

The first question was deliberately simple:

> **When GOLDBEES moves unusually far from its recent intraday level, does that move tend to reverse?**

This was a mean-reversion hypothesis. The reasoning was that a large short-term deviation from a recent mean might reflect temporary pressure, so price could move back toward its recent level.

The first test was therefore an **event study**, not an immediate trading backtest. The purpose was to determine whether the underlying relationship existed before adding execution rules.

## 2. Why GOLDBEES and why 5-minute data

The first instrument was **GOLDBEES** and the data was five-minute OHLCV.

Five-minute data was chosen because the research question was intraday. A daily dataset would hide much of the short-horizon movement being studied.

GOLDBEES was chosen as a practical single-instrument starting point. It allowed the initial price-behaviour question to be studied without immediately introducing the additional contract, expiry, and liquidity complications of derivatives.

The initial dataset contained **30,912 five-minute bars from January 2025 through August 2026**.

This choice was about creating a suitable starting experiment, not selecting an instrument because it had already shown a profitable result.

## 3. Experiment 001 — test the original mean-reversion hypothesis

For each completed five-minute bar, the research measured the distance between the current close and its recent intraday mean.

The initial implementation used:

- 30 completed five-minute bars;
- an absolute z-score threshold of 2.0;
- same-session forward returns;
- 5-, 15-, 30- and 60-minute horizons.

A **z-score** measures how far an observation is from its mean in standard-deviation units.

The original hypothesis predicted:

- large positive deviation → subsequent negative return;
- large negative deviation → subsequent positive return.

### Result

The event study produced **2,953 combined directional event observations**.

The reversion-aligned mean returns were negative at every tested horizon:

| Horizon | Reversion-aligned mean return |
|---|---:|
| 5 min | -0.00365% |
| 15 min | -0.00901% |
| 30 min | -0.01703% |
| 60 min | -0.02105% |

Positive deviations instead showed positive average forward returns, rising from about **+0.00764% at 5 minutes to +0.05577% at 60 minutes**.

### Interpretation

The first economic story did not match the data.

The large positive deviations were not followed by the reversal expected under mean reversion. They were more consistent with **continuation**.

The research therefore did not search for a better mean-reversion threshold. The evidence changed the question itself:

> **Could an unusually large positive move contain short-horizon continuation information?**

## 4. Experiment 001A — characterize the new continuation observation

The next question was:

> **If large positive deviations are followed by positive returns, under what conditions is that behaviour strongest?**

This was a characterization step, not yet a strategy.

A fixed **12-bar non-overlap filter** was introduced to reduce the dependence caused by clustered events. The original 30-bar lookback and 2.0 z-score threshold were retained.

The events were then separated by predefined conditions such as:

- prior six-bar direction;
- positive versus negative deviation;
- time-of-day buckets;
- event versus non-event behaviour.

### Result

The continuation-like pattern survived the non-overlap control.

The clearest concentration was:

> **large positive deviation + positive prior six-bar trend**

Negative deviations remained weaker and inconsistent.

Volume and volatility did not provide a simple primary explanation. Late-session and severity concentrations were treated as exploratory observations rather than optimized filters.

### Why this led to the next experiment

The research now had a narrower mechanism candidate:

**an unusually large positive move may contain additional continuation information when the asset was already moving upward before the event.**

But the result was still descriptive. The comparison had not yet been made strictly point-in-time.

That led to 001B.

## 5. Experiment 001B — separate continuation from ordinary drift and prior trend

The next question was:

> **Does the continuation after a large deviation contain information beyond normal intraday drift and the trend that already existed before the event?**

The strongest subgroup was again positive deviation plus prior uptrend.

| Horizon | Events | Event mean | Matched baseline | Incremental return |
|---|---:|---:|---:|---:|
| 5 min | 363 | +0.0156% | +0.0025% | **+0.0128%** |
| 15 min | 343 | +0.0202% | +0.0084% | **+0.0113%** |
| 30 min | 299 | +0.0443% | +0.0177% | **+0.0255%** |
| 60 min | 246 | +0.0532% | +0.0270% | **+0.0243%** |

The event remained above the matched non-event baseline at all four horizons.

### Interpretation

This strengthened the continuation case.

However, the benchmark was still a full-sample descriptive attribution benchmark. It was not yet a point-in-time validation and had not addressed execution, costs, turnover or chronological out-of-sample stability.

So the next question became:

> **Does the same relationship survive when the benchmark is constructed only from information that would have been available at the signal time?**

## 6. Experiment 001C — point-in-time continuation validation

The continuation hypothesis was frozen before moving forward:

> **When a five-minute bar closes at least 2.0 standard deviations above the previous 30 completed closes and the prior six-bar return is positive, the subsequent return should be positive and stronger than the historical point-in-time return of comparable non-event observations.**

The execution convention was also fixed:

- signal known at event-bar close;
- enter at next-bar open;
- exit at close of t+6.

A **point-in-time (PIT)** test means that only information available at the decision time can influence the signal or benchmark.

### Result

The implementation produced **1,668 frozen events** and **401 selected non-overlapping events** under the fixed 12-bar cooldown.

| Horizon | Event return | PIT baseline | Incremental return |
|---|---:|---:|---:|
| 5 min | +0.0148% | +0.0032% | **+0.0115%** |
| 15 min | +0.0205% | +0.0099% | **+0.0106%** |
| 30 min | +0.0443% | +0.0194% | **+0.0249%** |
| 60 min | +0.0527% | +0.0279% | **+0.0247%** |

The pre-specified 30-minute horizon showed about **+2.49 bps** of incremental gross return.

### Why this justified a trading backtest

The continuation relationship survived a stricter information-timing control.

The remaining questions were no longer mainly about whether the pattern existed:

- How much return does an actual trade earn?
- How stable is the trade distribution?
- How much turnover is produced?
- Does the result survive costs?
- Does it persist across chronological periods?
- Is there enough opportunity to matter operationally?

That justified freezing the rule and moving to 001D.

## 7. Experiment 001D — turn the frozen hypothesis into a trading rule

The frozen strategy used:

- five-minute GOLDBEES OHLCV;
- previous 30 completed same-session closes;
- sample standard deviation;
- z-score ≥ +2.0;
- prior six-bar return > 0;
- long-only;
- next-bar-open entry;
- close-of-t+6 exit;
- fixed 12-bar session cooldown;
- no overnight feature construction;
- one position at a time;
- constant-notional accounting;
- no leverage or optimized position sizing.

The purpose was to test the existing hypothesis as written, not find better parameters.

### Result

The backtest produced:

- **310 trades**
- **+15.85% cumulative gross return**
- **+4.77 bps mean gross trade return**
- **55.81% win rate**
- **2.269 profit factor**

The gross result was positive.

But +4.77 bps per trade is small enough that execution economics could easily dominate it.

The next question therefore became:

> **Is the gross edge broad enough and large enough to survive trading friction?**

## 8. Experiment 001E — inspect the trade distribution before changing the rule

The strategy was not changed.

Instead, the trades were examined in more detail.

The audit found:

- **+2.41 bps median** gross trade return;
- **+4.77 bps mean** gross trade return;
- the top 10% of winners contributed about **53.7%** of positive profit;
- about **1.30 trades per active day** on average;
- **25 minutes** median holding duration.

### Interpretation

The result was not solely produced by one or two extreme winners, although the largest winners mattered.

The per-trade edge was still small.

That made it useful to ask whether the result was still present after removing tail winners, and whether the trade path supported the fixed holding period.

## 9. Experiment 001F — decompose the trade-level edge

The top 10% of winning trades were removed as a diagnostic.

The remaining **292 trades** still showed:

- **+1.41 bps mean gross return**
- **+1.32 bps median**
- **53.08% win rate**
- **1.354 profit factor**

So the gross effect was not solely a tail-winner artifact.

Other observations were recorded without turning them into filters:

- later-session buckets looked descriptively stronger;
- z-score buckets did not show a clean monotonic relationship.

### Why the next step was a replay

The compact 001D trade export did not contain the complete signal-time variables and intermediate forward path needed for a full execution/edge decomposition.

The safest next step was therefore not to invent additional features, but to reconstruct the frozen strategy directly from the validated OHLCV data.

## 10. Experiment 001G — replay the frozen strategy and inspect the forward path

The frozen 001D strategy was reconstructed directly from the validated GOLDBEES data.

All **310 trades matched the original reference with zero discrepancies**.

The mean forward path was:

| Forward point | Mean return |
|---|---:|
| 5 min | +1.36 bps |
| 10 min | +2.44 bps |
| 20 min | +3.40 bps |
| 25 min | +4.51 bps |
| 30 min | +4.77 bps |

The 30-minute median was **+2.41 bps**.

MFE/MAE diagnostics were:

- **MFE mean +15.35 bps; median +9.48 bps**
- **MAE mean -9.63 bps; median -6.88 bps**

**MFE** is the best favourable price movement experienced during an open trade. **MAE** is the worst adverse movement.

### Interpretation

The average trade had already accumulated much of its gross return before the frozen exit.

However, MFE and MAE are path diagnostics, not executable profit. They do not mean the strategy can automatically capture the intrabar high or avoid the intrabar low.

Later-session and z-score observations remained descriptive only.

The unresolved issue was still whether the edge was economically large enough.

## 11. Experiment 001H — predefined chronological robustness

The frozen 001D strategy was then evaluated across predefined chronological periods without changing the rule.

The result remained positive in the examined periods.

| Period | Trades | Mean gross/trade | Win rate | Profit factor | Cumulative gross |
|---|---:|---:|---:|---:|---:|
| 2025 | 197 | +4.53 bps | 57.87% | 2.406 | +9.31% |
| 2026 chronological period | 113 | +5.18 bps | 52.21% | 2.105 | +5.98% |

This gave evidence that the gross result did not simply collapse in the later sample.

But this was explicitly **OOS-style, not pristine untouched OOS**, because the broader January 2025–August 2026 sample had already been inspected during research.

### The cost sensitivity

| Round-trip cost | Mean net/trade | Cumulative net |
|---:|---:|---:|
| 4 bps | +0.77 bps | +2.34% |
| 6 bps | -1.23 bps | -3.81% |
| 14 bps | -9.23 bps | -24.95% |

These were scenario assumptions, not measured historical execution costs.

### Why the next step became prospective

The historical evidence suggested that the gross continuation relationship had some persistence, but the economic margin was thin.

The research therefore needed a genuinely prospective test:

> **What happens when the rules are frozen and signals are recorded before outcomes are known?**

## 12. Experiment 001I — prospective paper/shadow test

The historical data had already been examined through August 2026.

The frozen 001D implementation was therefore used in a prospective paper/shadow process with an immutable activation boundary.

The controls included:

- signals recorded before outcomes were known;
- append-only prospective records;
- fixed strategy rules;
- no threshold, holding-period or filter changes after seeing prospective outcomes;
- dedicated run-integrity validation.

The first prospective run produced **two selected trades on 2026-09-17**.

### Interpretation

Two observations are far too few to statistically reject the continuation phenomenon.

They are also far too few to establish strong evidence for a live strategy.

The practical issue was therefore opportunity rate: the single-instrument implementation was producing too few observations for the research objective.

That led to 001J.

## 13. Experiment 001J — test the same economic hypothesis across a broader universe

The next question was:

> **If the continuation mechanism is real, can the same economic hypothesis be observed across a broader liquid NSE equity universe?**

The economic hypothesis was kept unchanged. The experiment changed the universe and the pre-registered development stage rather than silently modifying 001D.

The tactical universe used the top 50 currently tradable NSE EQ instruments ranked by median daily traded value during a pre-strategy formation window.

This universe has an important limitation: the current broker instrument dump does not reconstruct historical index membership or delistings. It was therefore treated as a tactical broker-native universe, not perfect point-in-time historical membership.

The exact 001D parameters were first applied cross-sectionally before the registered development search.

### Result

The broader search did not produce a sufficiently strong candidate after considering the required stability and execution constraints.

The strongest secondary development result remained in the few-basis-point range, around **3.63 bps mean gross return per trade**, and became negative in both mean and median terms under the predefined **5-bps** sensitivity.

### Why the research stopped

The research had already moved through:

**mean-reversion hypothesis → rejection → continuation characterization → attribution → point-in-time validation → frozen trade rule → execution audit → trade decomposition → replay → chronological robustness → prospective testing → broader-universe search**

Opening additional searches on the same development sample would add research degrees of freedom without introducing a new economic question.

That would increase data-snooping and multiple-testing risk.

## 14. Final interpretation

Strategy 001 was **not statistically rejected as a phenomenon**.

The research found a continuation-like relationship after unusually large positive intraday deviations, particularly when prior short-term direction was positive. The frozen implementation also produced positive gross historical performance.

The failure occurred at the transition from a gross statistical relationship to a sufficiently robust and cost-resilient **executable implementation**.

The prospective sample was too small to reject the phenomenon or validate it strongly.

The broader-universe experiment did not produce a sufficiently strong candidate.

Therefore the tested Strategy 001 line was closed without promoting an implementation for deployment.

### Research chain

```text
Initial mean-reversion question
        ↓
large positive deviations did not revert
        ↓
001A: continuation + prior-uptrend structure
        ↓
001B: stronger than matched descriptive baseline
        ↓
001C: continuation survives point-in-time benchmark
        ↓
001D: frozen executable strategy
        ↓
001E: trade distribution / friction sensitivity
        ↓
001F: tail and trade-level decomposition
        ↓
001G: replay and forward-path diagnostics
        ↓
001H: chronological robustness
        ↓
001I: prospective test — two observations
        ↓
001J: broader-universe development — no promotable candidate
        ↓
Strategy 001 closed
```

The key distinction is:

> **A statistical edge is not automatically a tradable edge.**

## Key terms

**Mean reversion:** expectation that an unusually high or low value moves back toward a recent level.

**Continuation / momentum:** an existing move continues for some period.

**Z-score:** distance from the mean measured in standard deviations.

**Point-in-time:** only information available at the decision time is used.

**MFE / MAE:** best favourable and worst adverse movement during an open trade.

**Transaction cost:** brokerage, taxes, exchange fees and other direct trading costs.

**Slippage:** difference between intended and actual execution price.

**Data snooping / overfitting:** repeatedly adapting research to the same historical data until noise can look like a signal.

## Status

**Closed — no Strategy 001 implementation was promoted for deployment.**