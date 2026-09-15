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
Retest
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
| Strategy 001B — continuation attribution | 🔬 Implemented — empirical result pending |
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

A continuation hypothesis is **PROMISING as an exploratory lead**, but it is not yet an approved trading hypothesis because we still need to determine whether the event adds information beyond ordinary intraday drift and the trend that was already present.

Details are recorded in `research/journal/001A_diagnostics_plan.md`.

---

## Strategy 001B — Continuation Attribution

### Current hypothesis

> A large positive deviation, especially during an existing short-term uptrend, may contain continuation information beyond ordinary intraday drift and the recent trend itself.

001B tests this rather than assuming it is true.

It compares:

- positive versus negative deviations;
- prior down/flat/up six-bar trend;
- the fixed non-overlapping event set;
- predefined time-of-day buckets;
- event returns versus matched non-event observations with the same time-of-day and prior-trend buckets.

The non-event comparison is explicitly a **descriptive attribution benchmark**, not a prospective trading signal. It is calculated over the research sample to answer the attribution question. If the result is promising, a separate point-in-time benchmark will be required before any trading rule is built.

Implementation:

```text
src/research/continuation_attribution.py
scripts/run_continuation_attribution.py
tests/test_continuation_attribution.py
research/journal/001B_continuation_attribution.md
```

Run locally:

```powershell
python scripts/run_continuation_attribution.py data/raw/NSE_GOLDBEES_5minute.csv
```

### 001B decision gate

- **REJECTED:** continuation disappears relative to matched normal behavior or is not sufficiently stable.
- **INCONCLUSIVE:** interesting direction, but evidence is insufficient.
- **PROMISING:** continuation survives non-overlap and remains incremental after trend/time-of-day attribution.

Only a promising result justifies creating a separate continuation trading specification.

---

# Why we do not jump directly to a stock universe

The project has a predefined multi-instrument universe framework, and the next research stage will eventually test hypotheses across that universe rather than cherry-picking instruments.

However, we do not want to move to broad universe testing **before finishing the attribution question for the current lead**. Otherwise we could accidentally select instruments because they happen to show the same attractive-looking pattern and increase data-snooping risk.

The intended sequence is:

```text
Discover relationship
        ↓
Check whether it is real or explained by simpler effects
        ↓
Define the strategy hypothesis
        ↓
Test the same hypothesis across the predefined universe
        ↓
Cost model + execution constraints
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
3. Use point-in-time information only.
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

The historical-data pipeline uses Zerodha Kite Connect. Credentials and access tokens must remain local and must never be committed.

---

# Roadmap

```text
Phase 0 — Research design / execution constraints      ✅
Phase 1 — Historical data validation                    ✅
Strategy 001 — GOLDBEES mean reversion                🔴 rejected
Strategy 001A — event structure diagnostics             ✅ continuation lead
Strategy 001B — continuation attribution                🔬 current
Continuation trading specification                        ⏳
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
