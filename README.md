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
Refinement
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
| Strategy 001 — GOLDBEES mean reversion | 🔬 Experiment 001 |
| Robust backtesting | ⏳ Not started |
| Out-of-sample validation | ⏳ Not started |
| Paper trading | ⏳ Not started |
| Live trading | ⛔ Not started |

**No live strategy has been approved.**

---

# Research Journal

## Strategy 001 — GOLDBEES Intraday Mean Reversion

**Status:** 🔬 Experiment 001 pending local execution

### Research question

> Does an unusually large short-term deviation of GOLDBEES from its recent intraday equilibrium tend to be followed by a statistically meaningful move back toward that equilibrium?

### Why GOLDBEES?

GOLDBEES is our first research instrument because it is suitable for investigating an intraday mean-reversion hypothesis and is accessible for eventual small-account validation.

Its lower nominal unit price is useful for later capital-feasibility analysis, but **price alone does not create an edge**. Eventual trading decisions must account for liquidity, spread, slippage, transaction costs, position sizing, and the ₹30,000 maximum-account-capital constraint.

### Experiment 001 — Baseline deviation event study

We deliberately begin with an **event study rather than a full trading strategy**.

The initial hypothesis is:

> If GOLDBEES closes unusually far from its recent intraday mean, the subsequent return should tend to have the opposite sign if short-term mean reversion exists.

Initial research defaults:

- 5-minute bars
- 30-bar prior lookback
- absolute deviation z-score ≥ 2.0
- forward horizons: 1, 3, 6, and 12 bars
- same-session forward returns only
- positive and negative deviations analysed separately

These are **predefined research defaults, not optimized parameters**.

### What we will measure

- event count;
- mean and median forward return;
- return dispersion;
- win rate;
- reversion-aligned return;
- exploratory t-statistic and 95% confidence interval;
- consistency across horizons;
- positive vs negative deviation behavior;
- event distribution and cumulative event outcomes.

### Decision framework

- 🔴 **REJECTED** — evidence does not justify continuing this hypothesis.
- 🟡 **INCONCLUSIVE** — potentially interesting, but evidence is insufficient or unstable.
- 🟢 **PROMISING** — justifies a robustness experiment.
- 🔵 **ROBUST** — survives predefined out-of-sample and robustness testing.
- 🟣 **PAPER READY** — survives research and execution checks and can enter paper/shadow trading.
- ⚫ **LIVE CANDIDATE** — only after paper/shadow validation and execution controls.

A promising event study is **not** a live-trading recommendation.

### Experiment 001 result

**Pending local execution.**

Run:

```powershell
python scripts/run_mean_reversion_event_study.py data/raw/NSE_GOLDBEES_5minute.csv
python scripts/plot_mean_reversion_results.py
```

The generated outputs will be placed under:

```text
data/reports/goldbees_mean_reversion/
├── summary.csv
├── events.csv
└── charts/
    ├── mean_reversion_by_horizon.png
    ├── deviation_vs_reversion_30m.png
    └── cumulative_event_aligned_return_30m.png
```

After execution, the observed metrics and charts will be added to this journal **without changing the original hypothesis after seeing the results**.

### Research record

Detailed Strategy 001 notes are kept in `research/journal/001_strategy_001_goldbees_mean_reversion.md`.

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
Strategy 001 — GOLDBEES mean reversion                🔬 current
Experiment 001 — Baseline event study                  🔬 pending
Strategy refinement / additional experiments            ⏳
Robust backtesting + realistic costs                     ⏳
Out-of-sample / walk-forward validation                  ⏳
Paper / shadow trading                                   ⏳
Broker execution validation                              ⏳
Controlled live validation                               ⏳
Additional asset-class strategies                         ⏳
Portfolio construction                                   ⏳
```

**The project is intentionally incomplete. The research journey is the deliverable.**
