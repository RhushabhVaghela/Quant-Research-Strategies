# Strategy 002 — Turnover and Execution Decomposition Protocol

**Status:** Development diagnostic in progress after the fixed baseline failed the initial cost-resilience gate.

**Important accounting clarification:** target-weight turnover between consecutive hypothetical portfolios is reported separately from executed turnover. The frozen baseline does not carry positions from one signal to the next; it enters the next portfolio at the next-bar open and closes it at that same bar's close. Therefore a normalized 100%-gross one-bar round trip has 2.0 units of executed notional turnover: 1.0 entry + 1.0 exit.

## Purpose

Measure the actual trading activity implied by the frozen Strategy 002 baseline before deciding whether the underlying residual-reversal mechanism has any defensible lower-turnover expression.

This is a diagnostic only. It does not modify, optimize, or replace the frozen baseline.

## Data permission

- Use only the chronological validation window: **2026-06-10 through 2026-08-19**.
- Do not inspect, summarize, optimize against, or otherwise use the final holdout: **2026-08-20 through 2026-09-17**.
- No live/prospective data is used.

## Frozen baseline being measured

At each completed 5-minute bar: calculate close-to-close returns, calculate leave-one-out cross-sectional residuals, negative residual -> long, positive residual -> short, equal weight within each sleeve, 50% gross long and 50% gross short, enter next bar open, exit next bar close, no overnight positions.

The signal rules must remain unchanged.

## Measurements

Report where supported:
- portfolio timestamps;
- long/short counts;
- target signed weights;
- gross and net exposure;
- one-way turnover between consecutive target portfolios;
- opening, closing, replacement and side-flip activity;
- unchanged/opened/closed/flipped position fractions;
- effective holding behavior;
- daily turnover;
- turnover concentration by instrument;
- gross return per unit of turnover;
- explicit cost sensitivity;
- relationship between turnover and gross return.

## Definition

For signed target weights w_i,t normalized so total absolute exposure is 1:

**One-way turnover = 0.5 × sum of absolute(w_i,t − w_i,t−1).**

The first portfolio has no prior target and is reported separately.

The one-bar holding convention means every selected portfolio has 1.0 unit of gross entry notional and 1.0 unit of gross exit notional. The diagnostic reports this **executed round-trip turnover** separately from target-weight turnover so the same trading activity is not double-counted.

## Interpretation

High turnover does not itself invalidate the signal. Low turnover does not itself prove profitability. Exact live costs require real execution/spread/slippage evidence.

## Decision rule

If turnover is so high that the observed gross edge remains far below plausible execution costs, document closure for the current capital-pursuit program.

If a specific economically motivated lower-turnover expression is identified without using holdout information, define it as a new Strategy 002 development experiment. It must be specified before testing and remain within the permitted development data.

The final holdout remains locked.
