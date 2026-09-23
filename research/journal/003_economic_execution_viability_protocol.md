# Strategy 003 — Economic Execution Viability Protocol

**Status:** 🟢 Preregistered next gate — execute only after protected prediction validation is reviewed.

## Purpose

If the frozen 003H prediction relationship survives protected validation, the next question is economic rather than predictive:

> Can a fixed executable portfolio implementation convert the protected next-5-minute cross-sectional information into gross return that survives current NSE cash-equity implementation costs?

This is not another alpha-discovery experiment.

## Frozen prediction input

Use only the protected-validation candidate: close_location_1bar, intraday_position_60bar, additive OLS, training-only standardization, the same 15-stock eligible universe, and the next 5-minute cross-sectional excess-return target.

No post-validation feature replacement is allowed.

## Portfolio construction

Before reading economic results, pre-register signal timestamp, ranking/portfolio formation, long/short selection, gross and net exposure, position sizing, rebalance frequency, turnover definition, entry/exit prices, treatment of unavailable or short-sale-ineligible names, overnight treatment, and partial fills.

## Current published NSE/broker economics

- STT = **2.5 bps**, sell side.
- NSE equity transaction charge = about **0.307 bps per side**.
- Stamp duty = **0.3 bps**, buy side.
- SEBI turnover fee = very small: ₹10/crore.
- GST = **18%** on applicable brokerage/exchange/SEBI charges.
- Zerodha equity intraday brokerage = **₹20 or 0.03%, whichever is lower, per executed order**.
- Upstox equity intraday brokerage = **₹20 or 0.1%, whichever is lower, per executed order**.
- Angel One equity intraday brokerage = **₹20 or 0.1%, whichever is lower, per executed order**, with a published minimum of ₹5.
- Groww equity intraday brokerage = **₹20 or 0.1%, whichever is lower**, subject to its published minimum-brokerage rules.

Primary sources are recorded in research/journal/003_execution_cost_basis_research_20260923.md.

## Fee-only reference table

| Round-trip notional | Approx. broker + statutory cost |
|---:|---:|
| ₹50,000 | **10.6 bps** |
| ₹1 lakh | **8.3 bps** |
| ₹2.5 lakh | **5.4 bps** |
| ₹5 lakh | **4.5 bps** |
| ₹10 lakh | **4.0 bps** |
| ₹50 lakh | **3.6 bps** |

These are **before spread, slippage and market impact**.

This is a reference calculation, not a historical execution estimate. Exact charges can vary with broker, order count, turnover, and account-specific terms.

## Execution-cost scenarios

Report at least:

1. **Fee floor:** statutory/broker charges only.
2. **Low-friction:** fee floor + pre-registered modest spread/slippage.
3. **Base:** fee floor + pre-registered spread/slippage + order-size-linked impact.
4. **Stress:** base + additional adverse execution friction.

Spread/slippage and impact parameters must be frozen before reading protected economic results and must not be tuned to make the strategy pass.

## Economic decision gate

- **Fails prediction:** close Strategy 003 for the current line; do not run an economic rescue search.
- **Passes prediction, fails economics:** close the current executable form. This is an economically informative negative result, not evidence that the predictive relationship never existed.
- **Passes prediction and economics:** only then proceed to prospective paper/shadow testing.

## Prohibited actions

Do not change features after protected validation, switch to close-location-only, add the interaction, search holding periods, search thresholds, change universe, change costs to rescue a result, inspect the final holdout to rescue economics, or reopen Strategies 001/002.

## Evidence boundary

This protocol is registered before protected economic testing. It does not claim that the economic test has been run.
