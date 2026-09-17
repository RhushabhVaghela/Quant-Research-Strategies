# Strategy 001J — Candidate Freeze Record

**Status:** Template; do not mark frozen until development review is complete.

## Experiment lock

- Formation: 2026-05-12 through 2026-06-09
- Development: 2026-06-10 through 2026-08-19
- Holdout: 2026-08-20 through 2026-09-17
- Universe: U1 — locked Kite-native liquid NSE EQ top 50
- Frequency: 5-minute OHLCV

## Candidate

| Parameter | Frozen value |
|---|---:|
| lookback_bars | |
| z_threshold | |
| trend_bars | |
| holding_bars | |
| cooldown_bars | |

## Development evidence reviewed

The candidate must be reviewed against the full 162-row development grid. The decision must not be based only on cumulative return.

Required evidence:

1. Trade breadth and number of participating symbols.
2. Mean and median trade return.
3. Win rate and profit factor.
4. Loss/gain tails and drawdown.
5. Stability across chronological development subperiods.
6. Stability across neighboring parameter configurations.
7. Signal concentration by timestamp, symbol, and sector where classification is available.
8. Holding time and turnover implications.
9. Conservative transaction-cost and slippage sensitivity.
10. Whether the effect remains economically interpretable as the registered continuation hypothesis.

## Selection discipline

A candidate is not frozen merely because it is the highest-returning configuration. Avoid selecting an isolated parameter spike, a low-breadth result, or a configuration whose apparent edge disappears under modest costs or chronological subdivision.

The development grid is the only place where parameter selection is permitted. The holdout must remain unopened until this record is completed.

## Holdout authorization

- [ ] Development grid reviewed.
- [ ] One configuration frozen before holdout evaluation.
- [ ] No holdout result has been inspected during selection.
- [ ] Candidate parameters above are the exact parameters passed to the holdout runner.

**Freeze timestamp:**  
**Reviewer:**  
**Rationale:**  

## Holdout result

Complete only after the candidate has been frozen and the holdout runner has executed.

- Holdout trades:
- Participating symbols:
- Mean trade return:
- Median trade return:
- Win rate:
- Profit factor:
- Max daily equal-weight drawdown:
- Max concurrent entries:
- Cost sensitivity:
- Interpretation:

## Promotion decision

Do not promote to live capital from holdout performance alone. A later prospective paper/shadow phase is required, followed by explicit execution, capacity, cost, and risk review. If evidence is weak or unstable, rejection or another experiment under Strategy 001 is valid.
