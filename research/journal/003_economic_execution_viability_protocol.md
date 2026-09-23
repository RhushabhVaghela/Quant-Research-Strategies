# Strategy 003 — Economic Execution Viability Protocol

**Status:** 🟢 Protected prediction gate passed; economic test frozen for execution.

## 1. Protected-validation decision

Protected validation used the frozen additive 003H model on 2026-06-10 through 2026-08-19 without feature/model/threshold/holding-period/cost tuning.

- mean IC: **+0.08136**
- mean rank IC: **+0.10082**
- Q1–Q5 spread: **+1.6870 bps**
- positive timestamp IC fraction: **60.76%**
- 711 usable timestamps / 10,665 stock-timestamp observations / 15 equities

Development references were +0.0696 mean IC, +0.0826 rank IC and +2.2168 bps Q1–Q5 spread. The protected spread retains about 76% of development magnitude and preserves direction. The Q1–Q5 ordering is also present.

**Decision: the predictive relationship passes the preregistered protected-prediction gate. Strategy 003 advances to economic execution testing.** This is not a profitability claim.

## 2. Coverage limitation

The protected scored observations occur only from approximately 14:10 through 15:20 IST because the frozen 60-bar within-session feature requires a warm-up. There are 50 trading dates and 711 timestamps. This does not establish all-day stability. The economic test must use the complete frozen protected sample rather than selecting a more convenient time window.

## 3. Frozen executable baseline

- rank the 15 eligible equities by the frozen prediction at each eligible timestamp;
- long Q5: top 20% = 3 stocks;
- short Q1: bottom 20% = 3 stocks;
- equal notional within each side;
- 50% gross notional long and 50% gross notional short;
- net exposure = 0%;
- hold exactly one 5-minute bar;
- exit at the next bar close;
- rebalance every eligible signal timestamp;
- no leverage, thresholds, volatility scaling, stop-loss/take-profit, symbol selection or time-of-day filtering;
- no overnight positions.

This is a close-to-close execution proxy because the validated target is close(t) to close(t+1). It is not a claim that fills occur exactly at recorded closing prices.

## 4. Turnover

For a fully refreshed one-bar dollar-neutral portfolio, entry gross turnover is 1.0x and exit gross turnover is 1.0x, giving 2.0x round-trip gross turnover. The implementation must calculate actual order-level turnover from position changes rather than assume a fixed turnover when rankings change.

## 5. Current fee model

Use the current published Zerodha NSE equity intraday schedule: brokerage ₹20 or 0.03%, whichever is lower, per executed order; STT 0.025% on sell turnover; NSE transaction charge 0.00307% on buy and sell turnover; stamp duty 0.003% on buy turnover; SEBI ₹10/crore; GST 18% on brokerage + transaction charges + SEBI charges.

Exact brokerage is calculated per executed order because the ₹20 cap makes the effective percentage depend on order notional.

## 6. Frozen friction scenarios

| Scenario | Additional execution friction |
|---|---:|
| Fee floor | 0 bps/side |
| Low | 0.5 bps/side |
| Base | 1.0 bps spread/slippage + 0.5 bps impact per side |
| Stress | 2.0 bps spread/slippage + 1.0 bps impact per side |

These assumptions are frozen before economic results and are not to be calibrated to make the strategy pass. They are scenario assumptions, not claims about the historical spread of every constituent.

## 7. Late-session execution regime

The validated signal is late-session. NSE introduced a 2026 closing-auction framework, so the economic runner must flag bars potentially affected by that regime rather than silently treating every late-session observation as ordinary continuous trading. Those observations must not be removed after seeing profitability.

## 8. Short-side feasibility

The baseline is dollar-neutral and therefore includes short exposure. Indian securities-market rules permit short selling subject to the applicable framework, while naked short selling is not permitted. The economic test therefore treats short-side execution as an explicit feasibility constraint rather than assuming every theoretical short is automatically executable.

## 9. Decision gate

- If the fee floor and predefined base scenario preserve positive economics, advance to prospective paper/shadow testing.
- If prediction survives but fee floor/base economics eliminate the executable edge, close the current Strategy 003 line.
- If ambiguous, record ambiguity and stop. No rescue optimization.

## 10. Prohibited actions

Do not change Q1/Q5, long/short weights, holding period, time window, closing-auction treatment, universe, cost assumptions, feature set, model, or threshold after economic results are observed. Do not inspect the final holdout or reopen Strategies 001/002.

## 11. Evidence boundary

The final holdout beginning 2026-08-20 remains untouched. The economic test uses only the frozen protected-validation period.