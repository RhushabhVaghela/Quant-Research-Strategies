# Strategy 002 — Turnover and Execution Decomposition Protocol

**Status:** Development diagnostic in progress after the fixed baseline failed the initial cost-resilience gate.

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

The one-bar holding convention means prior positions are exited and the new target portfolio is entered. The diagnostic must distinguish these flows and must not double-count them in cost interpretation.

## Interpretation

High turnover does not itself invalidate the signal. Low turnover does not itself prove profitability. Exact live costs require real execution/spread/slippage evidence.

## Decision rule

If turnover is so high that the observed gross edge remains far below plausible execution costs, document closure for the current capital-pursuit program.

If a specific economically motivated lower-turnover expression is identified without using holdout information, define it as a new Strategy 002 development experiment. It must be specified before testing and remain within the permitted development data.

The final holdout remains locked.
