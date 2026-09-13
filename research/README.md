# Quant Research Workspace

This directory records the research process behind the intraday strategy portfolio.

## Research principles

- Start with a financial hypothesis, not a model.
- Treat Quantra templates as building blocks/reference material, not finished strategies.
- Prefer intraday strategies with realistic execution paths.
- Establish a simple baseline before adding ML/DL.
- Use time-ordered validation and walk-forward testing where appropriate.
- Prevent look-ahead bias, leakage, survivorship bias, and data snooping.
- Include realistic transaction costs and slippage assumptions.
- Reject strategies that do not remain robust out of sample.
- Never invent expected performance targets before testing.
- Treat the user's ₹30,000 account as a capital constraint, not a target deployment amount.
- Keep research-universe selection independent from strategy performance where possible.
- Paper trading and any eventual small live experiment are validation stages, not guarantees of profitability.

## Current research question

Can we identify repeatable intraday conditions under which a directional price move is more likely to continue or reverse, and use statistical/ML methods to selectively trade only the conditions that demonstrate robust out-of-sample evidence?

## Phase 0 controls

Before advancing to ML or live execution, the project now explicitly documents:

- `phase_00_india_retail_trading_spec.md` — Indian retail algo/API and execution requirements.
- `phase_00_capital_and_execution_spec.md` — ₹30,000 capital feasibility, costs, liquidity and deployment rules.
- `phase_00_research_universe_spec.md` — reproducible NSE cash-equity/ETF universe selection.

These are research controls and operational specifications, not legal, tax, or investment advice.

## Phase 1 universe work

The multi-instrument research-universe workflow is now defined in:

- `phase_01_universe_audit.md` — candidate resolution, common historical-data collection, audit gates, liquidity/capital checks, and universe-bias controls.
- `universe_candidates.csv` — reproducible initial candidate manifest.

The candidate manifest is intentionally defined independently of strategy performance. The current tooling resolves symbols against the locally refreshed NSE instrument master and records broker-reported price information only as a capital-feasibility screening diagnostic.

## Current status

- Phase 0 — Regulatory/execution specification: **complete**.
- Phase 0 — Capital feasibility specification: **complete**.
- Phase 0 — Research universe specification: **complete**.
- Phase 1 — NIFTYBEES data validation/audit: **complete as a pipeline checkpoint**.
- Phase 1 — Initial NIFTYBEES event study: **exploratory; insufficient evidence for strategy approval**.
- Phase 1 — Multi-instrument universe audit tooling: **implemented**.
- Phase 1 — Initial candidate manifest and broker-master resolution workflow: **implemented; local execution pending**.

**No strategy is approved for trading yet.**
