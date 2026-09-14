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
Refinement / diagnostics
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
| Initial exploratory event study | ✅ Complete — insufficient evidence |
| Strategy 001 — GOLDBEES mean reversion | 🔴 Rejected as symmetric mean reversion |
| Strategy 001A — event structure diagnostics | 🔬 Implemented — local execution pending |
| Robust backtesting | ⏳ Not started |
| Out-of-sample validation | ⏳ Not started |
| Paper trading | ⏳ Not started |
| Live trading | ⛔ Not started |

**No live strategy has been approved.**

---

# Research Journal

## Strategy 001 — GOLDBEES Intraday Mean Reversion

**Status:** 🔴 Rejected as a symmetric mean-reversion signal

### Research question

> Does an unusually large short-term deviation of GOLDBEES from its recent intraday equilibrium tend to be followed by a statistically meaningful move back toward that equilibrium?

### Experiment 001 — Baseline event study

We began with an event study rather than a full trading strategy. The predefined research defaults were 5-minute bars, a 30-bar prior lookback, absolute z-score ≥ 2.0, and same-session forward horizons of 1, 3, 6, and 12 bars.

The GOLDBEES dataset contained **30,912 five-minute bars** from January 2025 through August 2026. The baseline study produced **2,953 combined event observations**.

The symmetric mean-reversion hypothesis was rejected. Reversion-aligned mean returns were negative at every horizon:

| Horizon | Mean reversion-aligned return |
|---|---:|
| 5 min | -0.00365% |
| 15 min | -0.00901% |
| 30 min | -0.01703% |
| 60 min | -0.02105% |

Positive deviations were followed by positive average returns, increasing from approximately **+0.00764% at 5 minutes** to **+0.05577% at 60 minutes**. This is continuation-like behavior rather than mean reversion. Negative deviations were weaker and inconsistent.

These observations are **not yet a momentum strategy**. Event clustering, overlapping horizons, persistent price drift, the choice of raw-price rolling mean, and the absence of execution costs all require further investigation.

The failed hypothesis is intentionally preserved in `research/journal/001_strategy_001_goldbees_mean_reversion.md`.

---

## Strategy 001A — Event structure & conditioning diagnostics

The next research question is:

> Does the continuation-like behavior survive basic dependence controls, and is it concentrated in identifiable market conditions?

This stage deliberately avoids parameter optimization. The fixed diagnostics are:

- event clustering and a 12-bar non-overlap filter;
- time of day;
- six-bar prior trend;
- prior 30-bar volatility regime;
- event-bar volume relative to the prior 30-bar median;
- absolute z-score severity;
- positive vs negative deviations after non-overlap filtering.

The 12-bar cooldown equals the longest tested forward horizon. It is a **dependence diagnostic, not a tuned trading parameter**.

Implementation:

```text
src/research/mean_reversion_diagnostics.py
scripts/run_mean_reversion_diagnostics.py
research/journal/001A_diagnostics_plan.md
```

Run locally:

```powershell
python scripts/run_mean_reversion_diagnostics.py data/raw/NSE_GOLDBEES_5minute.csv
```

Outputs are written to:

```text
data/reports/goldbees_mean_reversion_diagnostics/
```

We will only create a separate continuation hypothesis if these diagnostics produce a stable and economically interpretable relationship. Any such hypothesis will get its own event study and will not inherit success merely because it descended from Strategy 001.

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

The first NIFTYBEES momentum/volume event study produced only 23 events and did not provide convincing continuation evidence. We therefore did not jump directly to ML or strategy optimization.

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
Phase 1 — Initial exploratory event study              ✅
Strategy 001 — GOLDBEES mean reversion                🔴 rejected
Strategy 001A — event structure diagnostics             🔬 current
Robust backtesting + realistic costs                     ⏳
Out-of-sample / walk-forward validation                  ⏳
Paper / shadow trading                                   ⏳
Broker execution validation                              ⏳
Controlled live validation                               ⏳
Additional asset-class strategies                         ⏳
Portfolio construction                                   ⏳
```

**The project is intentionally incomplete. The research journey is the deliverable.**
