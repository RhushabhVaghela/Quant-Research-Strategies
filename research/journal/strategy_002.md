# Strategy 002 — Cross-Sectional Residual Reversal Research

## 1. Why Strategy 002 was started

Strategy 001 focused on a single-instrument continuation hypothesis.

The next strategy deliberately changed the economic question rather than making another variation of the same idea:

> **Can we separate movement specific to one asset from movement shared by the other assets, and does that asset-specific movement tend to reverse on the next intraday bar?**

This became a **cross-sectional residual reversal** research program.

A cross-sectional analysis compares several assets at the same timestamp. A residual is the part of an asset's return that remains after removing a common component.

The economic interpretation was that temporary stock-specific price pressure or a liquidity imbalance might push one asset away from its peers, after which some of that relative move could reverse.

## 2. Why an Indian equity universe and why 5-minute data

A single stock could not answer a question about relative behaviour across assets.

The research therefore used a predefined Indian equity/ETF universe with common **five-minute** observations.

The original manifest contained **20 NSE candidates** covering broad-market and sector ETFs, a commodity ETF, and liquid large-cap equities from several sectors.

The universe was defined independently of Strategy 002 performance.

A common historical window from **2025-09-18 through 2026-09-17** was acquired.

The audit found:

- **20/20** candidates downloaded successfully;
- **19/20** passed the structural data-quality gate;
- HINDUNILVR was excluded because of one unexpected interval and five zero-volume observations;
- the other 19 eligible instruments had zero duplicate timestamps, zero unexpected intervals and zero zero-volume observations in the audited sample.

The structural screen was a **data-quality gate**, not a profitability ranking.

## 3. Why the time split was fixed before pattern discovery

The available period was divided into:

| Phase | Dates | Allowed use |
|---|---|---|
| Exploratory development | 2025-09-18 → 2026-06-09 | pattern discovery, descriptive work, hypothesis formation, controlled development |
| Development validation | 2026-06-10 → 2026-08-19 | candidate validation / robustness |
| Final chronological holdout | 2026-08-20 → 2026-09-17 | final test of one frozen candidate only |

The holdout was already in the downloaded files, but discovery code was required to exclude it.

This prevented the research from repeatedly looking at future data and then calling the same observations out of sample.

## 4. First step — inspect what the cross-sectional dataset actually contains

The first Strategy 002 pattern pass was **hypothesis-free**.

Before deciding that residual reversal, momentum, or any other specific mechanism existed, the research examined:

- return autocorrelation;
- absolute-return autocorrelation;
- fixed forward-horizon returns;
- intraday/time-of-day structure;
- cross-sectional correlation and dispersion;
- PCA/common-factor structure.

The reason was methodological:

> **The dataset should determine which economic questions deserve a formal hypothesis.**

At this stage there was no trading P&L, no threshold grid and no holdout analysis.

## 5. The first pattern — broad next-bar cross-sectional reversal

The exploratory residual analysis initially defined each asset's five-minute residual relative to the contemporaneous cross-sectional mean.

A broad next-bar reversal pattern appeared:

- after a negative residual, median next-bar residual return was about **+3.71 bps**;
- **94.7%** of instruments had a positive next-bar response in that state;
- after a positive residual, median next-bar residual return was about **−4.25 bps**;
- none of the instruments had a positive mean response in the positive-residual state;
- by two bars, the effect weakened substantially;
- at longer horizons, the signs became small and unstable.

Magnitude buckets did not reveal a clean monotonic threshold.

### What the result meant

The data gave a useful descriptive observation:

> **Short-horizon relative moves appeared to reverse on the next bar.**

But the observation was not yet suitable for a strategy because two questions remained unresolved.

First, the residual benchmark included the asset's own return. That creates a mechanical self-contamination issue.

Second, earlier research had shown that some short-horizon reversal could concentrate around the **prior-close/next-open boundary**. The new residual effect might therefore be another representation of an already observed boundary phenomenon.

This determined the next experiment.

## 6. Mechanism decomposition — remove self-contamination and separate the bar boundary

The next question became:

> **Does residual reversal survive when each asset is removed from its own peer benchmark, and does the effect occur in the next bar itself or mainly around the close-to-open boundary?**

The controlled analysis therefore:

1. constructed leave-one-out residuals;
2. separated close-to-close, prior-close-to-next-open and next-open-to-next-close components;
3. measured sign-conditioned next-bar behaviour;
4. checked breadth and chronological stability.

The purpose was to determine whether the observed pattern represented an independent stock-specific effect.

## 7. The formal Strategy 002 hypothesis

Only after the pattern had been characterized was the economic hypothesis registered:

> **For an eligible Indian equity/ETF, when its five-minute close-to-close return is negative relative to the contemporaneous returns of the other eligible instruments, its next five-minute residual return should tend to be positive. Conversely, a positive residual should tend to be followed by a negative residual.**

The proposed mechanism was **temporary stock-specific price pressure / liquidity imbalance**.

Formally:

`r(i,t) = close(i,t)/close(i,t-1) - 1`

`m(-i,t) = mean(r(j,t)) for j != i`

`residual(i,t) = r(i,t) - m(-i,t)`

The signal was known at the close of bar `t`, so the baseline implementation used the next bar open and evaluated the next-bar residual outcome.

### Exploratory evidence behind the hypothesis

Within the locked development sample, the registered hypothesis recorded:

- negative residual → median next-bar residual **+3.9211 bps**; **94.7%** positive instruments;
- positive residual → median next-bar residual **−4.4816 bps**; **0%** positive instruments;
- negative residual → next close-to-open **+2.1336 bps** and next open-to-close **+2.1737 bps**;
- positive residual → next close-to-open **−2.4452 bps** and next open-to-close **−0.9523 bps**.

These were development observations, not validation or holdout results.

### Why the horizon was fixed at one bar

The exploratory evidence was strongest at the immediate next bar and weakened at longer horizons.

So the **next five-minute bar** became the primary confirmatory horizon.

This was a research translation of the observed time scale, not a post-hoc selection of the most profitable holding period.

## 8. Why a simple executable baseline came next

The next question was:

> **Does the registered residual-reversal hypothesis still exist when translated into an actual one-bar portfolio?**

The baseline deliberately avoided ML, threshold search and holding-period optimization.

It used the point-in-time residual sign to form the cross-sectional market-neutral position, entered at the next five-minute open, and exited at the next five-minute close.

This kept the implementation close to the economic hypothesis.

## 9. Chronological validation — quantify the size of the effect

Validation covered **2026-06-10 through 2026-08-19** across the **19 structurally eligible instruments**.

The final holdout beginning **2026-08-20** remained unused.

The fixed baseline produced:

| Round-trip cost | Mean return / portfolio observation | Median | Positive fraction | Compounded return | Daily Sharpe | Max drawdown |
|---:|---:|---:|---:|---:|---:|---:|
| 0 bps | +0.0896 bps | +0.1751 bps | 53.48% | +3.35% | 4.52 | -1.35% |
| 5 bps | -4.9104 bps | -4.8249 bps | 3.52% | -83.72% | -234.12 | -83.70% |
| 10 bps | -9.9104 bps | -9.8249 bps | 0.51% | -97.44% | -486.19 | -97.43% |
| 15 bps | -14.9104 bps | -14.8249 bps | 0.11% | -99.60% | -750.11 | -99.60% |

The gross effect was positive, but only **+0.0896 bps per five-minute portfolio observation**.

The baseline was also structurally high-turnover:

- mean one-way target-weight turnover: **57.98%**;
- median: **58.33%**;
- 95th percentile: **78.41%**;
- completed one-bar trades: **200% normalized round-trip turnover**;
- mean holding time: **5 minutes**;
- mean daily executed round-trip turnover: **147.96 normalized round trips**.

### Interpretation

The central problem was now clear.

The signal had a measurable statistical effect, but the effect was tiny compared with the amount of portfolio trading required to extract it.

The next question was therefore not which threshold increases the return.

It was:

> **Can the same residual-reversal idea be expressed at lower frequency so that a larger return per completed trade offsets the execution burden?**

## 10. H2 / H3 / H6 — registered lower-frequency development experiment

A separate pre-registered development experiment tested three longer holding variants:

- **H2**;
- **H3**;
- **H6**.

The variants used only the development period **2025-09-18 through 2026-06-09**.

The reason for testing them was to reduce the number of completed trades per unit of clock time.

The accounting was made explicit:

> A completed round trip still uses **2.0 normalized units of executed notional** — one entry plus one exit.

So longer holding reduces trade **frequency**, not turnover per completed round trip.

### Result

- H2: **+0.1921 bps mean gross return per trade**;
- H3: **+0.2121 bps mean gross return per trade**;
- H6: **negative gross**.

H2 and H3 were also negative under the first **2-bps** cost sensitivity.

No variant passed the economic selection gate.

## 11. Why the research stopped instead of opening more holding periods

The H2/H3/H6 experiment answered the intended question.

It did not find an economically large enough return per trade.

Opening H4/H5/H7 or repeatedly adjusting thresholds after observing these results would mostly add historical research decisions without introducing a new economic mechanism.

That would increase data-snooping risk.

The final holdout therefore remained untouched.

## 12. Final interpretation

Strategy 002 found evidence for a **short-horizon cross-sectional residual-reversal pattern**, but the tested executable implementation did not establish sufficient cost-resilient economics.

The research chain was:

```text
Universe/data audit
        ↓
hypothesis-free pattern discovery
        ↓
broad next-bar residual reversal observed
        ↓
leave-one-out + bar-boundary mechanism check
        ↓
formal residual-reversal hypothesis
        ↓
fixed one-bar executable baseline
        ↓
chronological validation
        ↓
small positive gross effect
        ↓
turnover decomposition
        ↓
H2/H3/H6 lower-frequency experiment
        ↓
no cost-resilient candidate
        ↓
Strategy 002 closed
```

The conclusion is deliberately narrow:

> **The tested executable Strategy 002 research line did not establish sufficient cost-resilient economics.**

This is not a claim that every possible residual-reversal phenomenon is false.

## Key terms

**Cross-sectional:** comparing multiple assets at the same point in time.

**Residual:** the part of an asset's return left after removing a common component.

**Leave-one-out:** exclude the asset itself when calculating its peer benchmark.

**Residual reversal:** an unusually negative relative move is followed by a positive relative move, or vice versa.

**Market neutral:** reduce exposure to broad market direction.

**Turnover:** how much portfolio notional is traded.

**Data snooping:** repeatedly making research choices using the same historical data.

## Status

**Closed — no Strategy 002 candidate was frozen for deployment.**