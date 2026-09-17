# Quant Research Strategies

This repository is a research journal and implementation workspace for developing, testing, and validating systematic trading strategies in Python.

The goal is not to collect a large number of backtests. The goal is to demonstrate a reproducible research process: hypothesis → data audit → signal discovery → point-in-time validation → frozen strategy → trade-level backtest → execution/cost audit → robustness → chronological validation → prospective paper/shadow test → controlled live validation.

Negative and inconclusive results are preserved as part of the research record.

---

## Strategy 001 — Intraday continuation research family

Strategy 001 began as a GOLDBEES mean-reversion hypothesis. The mean-reversion hypothesis was rejected during the original research. The observed continuation structure then became the active Strategy 001 economic hypothesis.

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
| 001H robustness/chronological holdout | 🟡 Complete | Positive gross performance across examined periods; costs remain unresolved |
| 001I prospective OOS / paper-shadow | 🔵 Closed | Two genuine prospective trades on 2026-09-17; too low-frequency for current capital-pursuit sprint; not statistically rejected |
| **001J cross-sectional equity experiment** | **🟡 Active** | Same economic hypothesis tested across a point-in-time Nifty 100 universe with a separately registered parameter process |

### Frozen 001D strategy

001D remains immutable evidence:

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
- no leverage or optimized sizing.

### 001I status

001I was the prospective test of frozen 001D. It produced two selected trades on 2026-09-17. The prospective ledger passed validation, but the single-instrument opportunity rate was too low for the accelerated September 2026 capital-pursuit objective. The sample is too small to statistically reject the underlying continuation hypothesis. 001I is closed and must not be restarted or retuned.

### 001J — active experiment

001J keeps the **Strategy 001 economic hypothesis** but changes the experimental universe and parameter-selection stage. This is not a modification of 001D.

**U1:** point-in-time Nifty 100 constituents, with historical membership represented by effective dates and explicit data/liquidity eligibility rules.

A separate, outcome-independent GOLDBEES behavior report measures return correlation and other descriptive properties. It is diagnostic only and does not replace U1 or select symbols using Strategy 001J P&L. The first baseline then applies the exact 001D parameters cross-sectionally. Only after that baseline is recorded may the pre-registered 162-configuration development grid be evaluated. A candidate must be frozen before chronological holdout and prospective paper/shadow testing.

See:

- `research/journal/001J_cross_sectional_equity_spec.md`
- `research/journal/001J_universe_u1_spec.md`
- `research/journal/001J_universe_discovery_protocol.md`
- `research/journal/001J_data_acquisition.md`
- `config/strategy_001j_u1.json`
- `src/research/strategy_001j_cross_sectional.py`
- `scripts/analyze_strategy_001j_universe_similarity.py`
- `scripts/validate_strategy_001j_data_gate.py`

---

## Strategy portfolio architecture

The project will eventually test genuinely different strategies across multiple asset classes, including equities, derivatives, commodities, currencies, and crypto. No two promoted strategies should be materially the same economic hypothesis applied to the same asset class.

A parameter variation or universe expansion of an existing hypothesis remains an experiment under the parent strategy. A genuinely different return mechanism receives a new strategy ID.

Derivatives strategies may remain paper-only when reliable realtime data, contract economics, lot size, liquidity, or available capital make live deployment inappropriate. Paper-only status still requires the same research discipline.

See `research/journal/strategy_registry.md` for the current strategy map and experiment lineage.

---

## Research standards

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
16. Do not manufacture trade frequency by weakening thresholds solely to meet a target count.
17. Preserve strategy/experiment lineage so historical evidence cannot be rewritten by later research.
18. Keep descriptive universe discovery separate from strategy-outcome-based universe selection.

---

## Reproducibility

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

The immediate active work is the 001J external data gate: acquire defensible PIT Nifty 100 membership and 5-minute equity data, audit coverage, then run the similarity diagnostics and frozen 001D-parameter cross-sectional baseline.
