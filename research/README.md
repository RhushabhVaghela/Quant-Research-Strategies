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
- Paper trading and any eventual small live experiment are validation stages, not guarantees of profitability.

## Current research question

Can we identify repeatable intraday conditions under which a directional price move is more likely to continue or reverse, and use statistical/ML methods to selectively trade only the conditions that demonstrate robust out-of-sample evidence?

## Current status

Phase 0 — Research universe and strategy ideation.

No strategy is approved for trading yet.
