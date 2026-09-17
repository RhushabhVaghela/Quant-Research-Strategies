# Quant Research Strategies

This repository is a research journal and implementation workspace for developing, testing, and validating systematic trading strategies in Python.

The goal is not to collect a large number of backtests. The goal is to demonstrate a reproducible research process: hypothesis → data audit → signal discovery → point-in-time validation → frozen strategy → trade-level backtest → execution/cost audit → robustness → chronological validation → prospective paper/shadow test → controlled live validation.

Negative and inconclusive results are preserved as part of the research record.

---

## Strategy 001 — GOLDBEES intraday continuation

Strategy 001 began as a mean-reversion hypothesis and was rejected. The research then investigated the observed continuation structure and produced a frozen long-only continuation strategy for GOLDBEES 5-minute data.

### Research status

| Stage | Status | Key result |
|---|---|---|
| 001 mean reversion | 🔴 Rejected | Large positive deviations did not reliably revert |
| 001A diagnostics | 🟢 Complete | Positive continuation and prior-trend conditioning identified |
| 001B attribution | 🟡 Promising | Continuation exceeded descriptive matched non-event baselines |
| 001C PIT baseline | 🟡 Promising | 30-min positive/up incremental result ≈ +2.49 bps |
| 001D frozen backtest | 🟡 Candidate | +4.77 bps mean gross trade, 310 trades; costs unresolved |
| 001E execution audit | 🟡 Complete | Small gross edge is highly friction-sensitive |
| 001F decomposition | 🟡 Complete | Edge not solely dependent on top tail winners |
| 001G replay | 🟡 Complete | 310/310 trades reconciled; forward path and MFE/MAE recovered |
| 001H robustness/chronological holdout | 🟡 Complete | Positive gross performance across all examined periods; costs remain unresolved |
| 001I prospective OOS / paper-shadow | 🔵 Closed | Two genuine prospective trades on 2026-09-17; too low-frequency for current capital-pursuit sprint; not statistically rejected |

### Frozen 001D strategy

- 5-minute GOLDBEES OHLCV;
- previous 30 completed same-session closes;
- sample standard deviation;
- z-score ≥ +2.0;
- prior six-bar return > 0;
- long-only;
- signal at event-bar close;
- next-bar-open entry;
- close of `t+6` exit;
- fixed 12-bar session cooldown;
- no overnight feature construction;
- one position at a time;
- no leverage or optimized sizing;
- no parameter optimization in the baseline.

### 001H result

001H kept the 001D strategy frozen and tested chronological periods, trading-frequency stability, return-distribution stability, and a predefined round-trip friction ladder. The frozen gross edge remained positive in all examined periods, but the historical cost grid showed that the small gross edge is highly friction-sensitive.

### 001I prospective OOS / paper-shadow — CLOSED

The 001I collector was deliberately kept unchanged while the prospective cohort was captured. On 2026-09-17 it generated two selected trades:

| Signal | z-score | Paper entry | Paper exit | Gross/net paper return |
|---|---:|---:|---:|---:|
| 12:00 | 2.2675 | 124.31 | 124.21 | -8.04 bps |
| 13:05 | 2.5350 | 124.87 | 124.71 | -12.81 bps |

The prospective ledger passed the repository validator. No live orders were placed. The sample is too small to statistically reject 001D, but the observed single-instrument frequency is too low for the September 2026 accelerated research/deployment objective.

001I is therefore **closed for capital-pursuit priority**. The frozen 001D rule will not be retuned from these observations. The broader continuation hypothesis may be investigated as a new experiment under Strategy 002.

See:

- `research/journal/001I_prospective_oos_paper_shadow_protocol.md`
- `research/journal/001I_prospective_oos_paper_shadow_results.md`

---

# Strategy 002 — Accelerated multi-asset research

Strategy 002 is now the active research program. It is designed to avoid the single-instrument frequency bottleneck while preserving the project's research discipline.

The first experiment will test whether the intraday continuation structure from Strategy 001 generalizes to a **predefined, point-in-time liquid Indian equity universe**.

### First universe: U1

U1 is specified as a point-in-time Nifty 100 constituent universe, subject to explicit data-coverage and liquidity eligibility rules. The current constituent list must not be applied blindly to the entire historical sample; historical membership must be represented by effective dates.

See `research/journal/002_universe_u1_spec.md`.

### First hypothesis

Reuse the economic hypothesis, not the frozen parameters:

> After an unusually strong positive intraday move, conditioned on recent positive direction, a short-horizon continuation may persist across liquid equities.

The first baseline will use the exact 001D parameters only as a **cross-sectional baseline**. It is not assumed to be optimal for U1.

A separate, narrow, pre-registered parameter-selection experiment may then be run on development data only. The selected configuration will be frozen before chronological holdout and prospective testing.

### Frequency objective

The objective is to obtain enough observations for rapid research decisions across the universe. An initial engineering target is roughly 20–50 candidate/selected opportunities per session across U1. Trade count is not a performance target, and parameters must not be weakened merely to manufacture 100+ trades/day.

### Research roadmap

```text
U1 point-in-time universe
        ↓
data/coverage/liquidity audit
        ↓
001D-parameter cross-sectional baseline
        ↓
continuation event study
        ↓
pre-registered parameter experiment on development data
        ↓
frozen Strategy 002 candidate
        ↓
chronological holdout
        ↓
one-session multi-symbol paper/shadow validation
        ↓
execution-cost audit
        ↓
controlled-live validation if all gates pass
```

Detailed schedule and gates: `research/journal/002_strategy_roadmap.md`.

---

# Strategy promotion principle

A strategy is not approved merely because a backtest is profitable or because it produces many trades. Promotion requires reproducibility, point-in-time correctness, chronological validation, realistic costs, adequate breadth of evidence, execution feasibility, and explicit risk controls.

---

# Research standards

1. Start with an economic hypothesis, not a model.
2. Define the prediction target before choosing a model.
3. Use point-in-time information for prospective strategy construction.
4. Keep event definitions and forward outcomes strictly separated.
5. Establish a simple baseline before ML.
6. Record negative and inconclusive results.
7. Avoid parameter optimization before establishing evidence.
8. Test across time and market regimes.
9. Include transaction costs and slippage before judging economic value.
10. Treat backtests as evidence, not guarantees.
11. Require genuine prospective evidence before controlled live validation.
12. Never deploy simply because a backtest looks attractive.
13. Define universe membership before evaluating strategy performance.
14. Preserve every parameter-search result and never select holdout winners retrospectively.
15. Treat cross-sectional observations as potentially correlated rather than assuming every trade is independent.

---

# Reproducibility

Install dependencies:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

Run the complete test suite:

```powershell
pytest
```

Strategy 001 historical scripts remain available for reproducibility. Strategy 001I is closed for capital-pursuit priority and should not be restarted as a new prospective cohort unless a separate research decision explicitly creates a new experiment.

Strategy 002 development begins with the U1 specification and reusable multi-symbol data/signal architecture.
