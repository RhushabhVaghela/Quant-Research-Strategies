# Strategy 002 — Turnover-Reduction Development Findings

**Status:** Closed — no candidate frozen.

## Scope

- Development period: **2025-09-18 through 2026-06-09**
- Variants registered before results: H2, H3, H6
- Validation period: **2026-06-10 through 2026-08-19** — not used for selection
- Final holdout: **2026-08-20 through 2026-09-17** — untouched
- Signal: frozen leave-one-out cross-sectional residual sign
- Construction: 50% gross long / 50% gross short, equal-weighted within sleeves
- Entry: next 5-minute bar open
- Exit: close of the final holding bar
- No overlapping positions and no overnight positions

## Development results

| Variant | Mean gross return/trade | Median gross return/trade | Gross win rate | Compounded gross return | Max drawdown | Mean net return at 2 bps cost |
|---|---:|---:|---:|---:|---:|---:|
| H2 (10 min) | +0.1921 bps | +0.2139 bps | 52.76% | +8.79% | -1.43% | -1.8079 bps |
| H3 (15 min) | +0.2121 bps | +0.2556 bps | 53.20% | +6.90% | -1.49% | -1.7879 bps |
| H6 (30 min) | -0.1564 bps | +0.0358 bps | 50.48% | -2.78% | -6.79% | -2.1564 bps |

The reported cost rows are sensitivity scenarios, not measured live transaction costs.

## Interpretation

H2 and H3 preserve a small positive gross effect, but the magnitude is substantially below even the experiment's first 2 bps round-trip sensitivity. H6 does not preserve positive gross economics. Therefore none of the three pre-registered variants satisfies the requirement to improve economics under the low-cost sensitivity.

An important accounting point is that **executed turnover per completed trade remains 2.0 normalized gross-notional units for H2, H3, and H6**: one unit of entry notional plus one unit of exit notional. Longer holding reduces the number of completed trades per unit of clock time, but it does not reduce the turnover of an individual round trip. Thus the economic benefit sought from H2/H3/H6 would have had to come from larger gross return per trade relative to the same round-trip execution burden. The development results do not establish that benefit.

## Gate decision

**No candidate is frozen. Strategy 002's current executable research line is closed for the present capital-pursuit program.**

This is not a statistical rejection of every possible residual-reversal phenomenon. It is a decision that the tested executable expressions did not establish adequate cost-resilient economics under the pre-registered development process.

The chronological validation result for the one-bar baseline remains historical evidence and is not retroactively changed. The validation period was not used to choose H2/H3/H6, and the final holdout was not inspected for this decision.

## Next research step

Do not reopen Strategy 002 with additional holding-period searches or post-hoc filters. The next research effort should use a genuinely different economic mechanism/asset-class combination under a new strategy ID, after reviewing the repository's existing research resources and registering a fresh data-first investigation. Strategy 003 remains reserved for that new mechanism.
