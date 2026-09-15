# Quant Research Strategies — Research Journal

This repository documents a **hypothesis-driven quantitative research journey** rather than a collection of pre-selected profitable strategies.

The main README is intentionally the interview-facing journal. An interviewer should be able to understand what we thought, what we tested, what happened, what we learned, and what we did next without navigating through many files.

---

## Research lifecycle

```text
Economic hypothesis
        ↓
Prediction target
        ↓
Data validation
        ↓
Simple baseline
        ↓
Statistical experiment
        ↓
Decision: reject / inconclusive / promising
        ↓
Refinement / attribution
        ↓
Freeze hypothesis
        ↓
Point-in-time validation
        ↓
Multi-instrument validation
        ↓
Out-of-sample / walk-forward validation
        ↓
Costs + slippage + execution analysis
        ↓
Paper / shadow trading
        ↓
Controlled live validation
```

**Failures are part of the portfolio.** We do not delete unsuccessful hypotheses or optimize until a backtest looks attractive.

---

# Current research status

| Stage | Status |
|---|---|
| Research design / regulatory constraints | ✅ Complete |
| ₹30,000 capital feasibility framework | ✅ Complete |
| Research-universe framework | ✅ Complete |
| Historical data validation | ✅ Complete |
| Strategy 001 — GOLDBEES mean reversion | 🔴 Rejected |
| Strategy 001A — event structure diagnostics | ✅ Complete — continuation lead identified |
| Strategy 001B — continuation attribution | 🟡 Promising research lead |
| Strategy 001C — frozen continuation specification | 🟡 Frozen — validation pending |
| Point-in-time benchmark audit | ⏳ Next |
| Multi-instrument hypothesis validation | ⏳ Not started |
| Robust trading backtest | ⏳ Not started |
| Out-of-sample / walk-forward validation | ⏳ Not started |
| Paper trading | ⏳ Not started |
| Live trading | ⛔ Not started |

**No strategy is approved for trading.**

---

# Research Journal

## Strategy 001 — GOLDBEES Intraday Mean Reversion

### Original hypothesis

> When GOLDBEES closes unusually far from its recent intraday mean, the subsequent return should tend to have the opposite sign and move back toward the mean.

The first experiment used 5-minute bars, a 30-bar prior lookback, an absolute z-score threshold of 2.0, and same-session forward horizons of 1, 3, 6, and 12 bars.

The GOLDBEES dataset contained **30,912 five-minute bars** from January 2025 through August 2026. The baseline study produced **2,953 combined event observations**.

### What Experiment 001 taught us

The symmetric mean-reversion hypothesis was **rejected**. Reversion-aligned mean returns were negative at every tested horizon:

| Horizon | Mean reversion-aligned return |
|---|---:|
| 5 min | -0.00365% |
| 15 min | -0.00901% |
| 30 min | -0.01703% |
| 60 min | -0.02105% |

Positive deviations were followed by positive average returns, increasing from approximately **+0.00764% at 5 minutes** to **+0.05577% at 60 minutes**. That is continuation-like behavior, not mean reversion. Negative deviations were weaker and inconsistent.

This did **not** immediately become a momentum strategy because the events were clustered, forward horizons overlapped, and ordinary intraday drift or prior trend could explain part of the result.

The failed hypothesis remains permanently recorded in `research/journal/001_strategy_001_goldbees_mean_reversion.md`.

---

## Strategy 001A — Event Structure & Conditioning Diagnostics

001A asked:

> Does the continuation-like behavior survive basic dependence controls, and is it concentrated in identifiable market conditions?

We deliberately did **not** optimize parameters. The diagnostics used a fixed 12-bar non-overlap filter, predefined time-of-day buckets, six-bar prior trend, prior volatility, volume relative to its prior median, and predefined z-score severity bands.

### What we learned

1. **Event clustering was substantial.** The raw event stream contained many events within 12 bars of each other. The fixed cooldown reduced this dependence.
2. **Positive-deviation continuation survived non-overlap.** Therefore the observed direction was not solely an artifact of counting every nearby event.
3. **Prior trend mattered.** Positive deviations occurring during an existing upward six-bar trend showed the clearest continuation behavior.
4. **Negative deviations were weaker and inconsistent.** The effect is therefore not obviously symmetric.
5. **Volume and volatility did not provide a simple primary explanation.**
6. Some late-session and high-severity concentrations were interesting, but we explicitly did not optimize around them.

### Decision

The mean-reversion hypothesis remains **REJECTED**.

A continuation hypothesis became a **PROMISING exploratory lead**, but we needed to determine whether the event added information beyond ordinary intraday drift and the trend already present.

Details are recorded in `research/journal/001A_diagnostics_plan.md`.

---

## Strategy 001B — Continuation Attribution

### Research question

> Does the continuation-like return after a large deviation contain information beyond ordinary intraday drift and the recent six-bar trend?

001B compared positive/negative deviations, prior down/flat/up six-bar trend, predefined time-of-day buckets, fixed non-overlapping events, and matched non-event observations.

### What 001B taught us

The strongest subgroup was **positive deviation + prior uptrend**. In the fixed 12-bar non-overlapping event set, event returns exceeded the matched non-event baseline at every tested horizon:

| Horizon | Events | Event mean | Matched baseline | Incremental return |
|---|---:|---:|---:|---:|
| 5 min | 363 | +0.0156% | +0.0025% | **+0.0128%** |
| 15 min | 343 | +0.0202% | +0.0084% | **+0.0113%** |
| 30 min | 299 | +0.0443% | +0.0177% | **+0.0255%** |
| 60 min | 246 | +0.0532% | +0.0270% | **+0.0243%** |

Positive deviations also remained above the matched baseline when trend regimes were pooled. Negative deviations did not show the symmetric reversal pattern expected from mean reversion.

In simple terms:

> When GOLDBEES was already moving upward and then made an unusually large positive move, subsequent returns were historically stronger than comparable non-event periods.

### Decision

**🟡 PROMISING RESEARCH LEAD.**

The evidence is strong enough to stop trying to rescue the original symmetric mean-reversion hypothesis and to formalize a continuation hypothesis for broader validation.

However, 001B is **not a validated trading strategy**. The event-vs-non-event comparison is a full-sample descriptive attribution benchmark. It is useful for diagnosis but must not be turned directly into a live signal. A strictly point-in-time benchmark, costs/slippage, and chronological out-of-sample validation are still required.

Detailed results are recorded in `research/journal/001B_continuation_attribution_results.md`.

---

## Strategy 001C — Frozen Continuation Hypothesis

001C is the methodological lock between discovery and validation. We freeze the hypothesis **before** looking for the best-performing instrument or parameter combination.

### Frozen hypothesis

> When a 5-minute bar closes at least 2.0 standard deviations above the previous 30 completed closes and the prior six-bar return is positive, the subsequent 30-minute return should be positive and stronger than the historical point-in-time return of comparable non-event observations.

### Frozen baseline

- 5-minute bars
- 30 completed-bar deviation lookback
- z-score ≥ +2.0
- prior six-bar return > 0
- 30-minute (6-bar) primary horizon
- signal decision after the event-bar close
- entry at next-bar open
- exit at the close of bar t+6
- 12-bar session cooldown
- no overnight feature construction
- minimum 30 completed historical benchmark observations
- no parameter search during this validation stage

The 30-minute horizon is a fixed middle-horizon baseline, not a choice made because it had the best historical return.

### Point-in-time benchmark rule

At event time `t`, a historical non-event observation is eligible for the benchmark only if its forward outcome has **fully completed strictly before `t`**, and it belongs to the same predefined time-of-day and prior-trend bucket.

This matters because merely having a historical starting timestamp before the event is not sufficient: its outcome must already have been observable. The new implementation enforces this rule.

### Decision

**🟡 Specification frozen — validation pending.**

This is the point where the project stops changing the hypothesis and starts testing whether it generalizes.

Implementation is recorded in:

```text
research/journal/001C_continuation_hypothesis_spec.md
src/research/point_in_time_baseline.py
scripts/run_point_in_time_baseline.py
tests/test_point_in_time_baseline.py
```

---

# Why we do not cherry-pick the universe

The project has a predefined multi-instrument universe framework. The continuation hypothesis is now frozen, so the next validation can move across that universe without selecting instruments based on post-discovery performance.

The intended sequence is:

```text
Discovery on GOLDBEES
        ↓
Attribution / falsification
        ↓
Freeze continuation hypothesis
        ↓
Point-in-time benchmark audit
        ↓
Apply unchanged hypothesis to predefined universe
        ↓
Cost + execution analysis
        ↓
Out-of-sample / walk-forward
        ↓
Paper / shadow trading
```

GOLDBEES is therefore a **discovery/prototype instrument**, not a claim that GOLDBEES is the best instrument to trade.

---

# Earlier research milestones

### Phase 0 — Research controls

Completed:

- India retail algo/API research specification
- ₹30,000 capital and execution feasibility specification
- research-universe specification
- Zerodha integration and execution constraints

These are research controls, not legal, tax, or investment advice. Current requirements must be re-verified before any live deployment.

### Phase 1 — Data

Completed:

- historical 5-minute data pipeline;
- OHLCV validation;
- session/gap audit;
- multi-instrument universe audit tooling.

### NIFTYBEES checkpoint

The first pipeline checkpoint contained 1,575 five-minute rows across 21 sessions with 75 bars per session and no detected duplicate timestamps, unexpected intraday gaps, or zero-volume rows.

This was a **data-quality checkpoint, not evidence of a trading edge**.

### Initial exploratory event study

The first NIFTYBEES event study produced only 23 events and did not provide convincing continuation evidence. We therefore did not jump directly to ML or strategy optimization.

That result remains part of the research history because rejecting weak evidence is itself part of the methodology.

---

# Project structure

```text
Quant-Research-Strategies/
├── README.md                         # Interview-facing research journal
├── research/
│   ├── journal/                      # Chronological research decisions
│   ├── phase_*.md                    # Research specifications and methodology
│   ├── strategies/                   # Strategy-specific research material
│   └── universe_candidates.csv       # Predefined research universe
├── src/
│   ├── data/                         # Authentication, historical data, validation, audit
│   └── research/                     # Event studies and research utilities
├── scripts/                          # Reproducible command-line experiments
├── tests/                            # Research and data-quality tests
├── data/
│   ├── raw/                          # Local historical datasets; not all data is committed
│   └── reports/                      # Generated experiment outputs
└── trading_resources/                # Reference learning material
```

---

# Research standards

1. Start with an economic hypothesis, not a model.
2. Define the prediction target before choosing a model.
3. Use point-in-time information only for prospective strategy construction.
4. Keep event definitions and forward outcomes strictly separated.
5. Establish a simple baseline before ML.
6. Record negative and inconclusive results.
7. Avoid threshold/parameter optimization before establishing evidence.
8. Test across time and market regimes.
9. Include transaction costs and slippage before judging economic value.
10. Treat backtests as evidence, not guarantees.
11. Require out-of-sample / walk-forward evidence before paper trading.
12. Treat paper trading as a validation stage, not proof of future profitability.
13. Never deploy the ₹30,000 account merely because a backtest looks attractive.

---

# Reproducibility

Install dependencies:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

Run tests:

```powershell
pytest
```

Run the frozen 001C point-in-time audit on the current GOLDBEES dataset:

```powershell
python scripts/run_point_in_time_baseline.py data/raw/NSE_GOLDBEES_5minute.csv
```

The historical-data pipeline uses Zerodha Kite Connect. Credentials and access tokens must remain local and must never be committed.

---

# Roadmap

```text
Phase 0 — Research design / execution constraints      ✅
Phase 1 — Historical data validation                    ✅
Strategy 001 — GOLDBEES mean reversion                🔴 rejected
Strategy 001A — event structure diagnostics             ✅ continuation lead
Strategy 001B — continuation attribution                🟡 promising lead
Strategy 001C — frozen continuation specification      🟡 validation pending
Point-in-time benchmark audit                             ⏳ NEXT
Multi-instrument hypothesis test                          ⏳
Robust backtesting + realistic costs                      ⏳
Out-of-sample / walk-forward validation                   ⏳
Paper / shadow trading                                    ⏳
Broker execution validation                               ⏳
Controlled live validation                                ⏳
Additional asset-class strategies                          ⏳
Portfolio construction                                    ⏳
```

**The project is intentionally incomplete. The research journey is the deliverable.**
