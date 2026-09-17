# Strategy Registry

This registry defines the portfolio-level research map. A strategy ID represents a distinct economic hypothesis and its intended asset-class application. Versioned experiments under a strategy do not create a new strategy merely because the universe, parameters, or implementation changes.

## Non-duplication rule

No two promoted strategies should be materially the same hypothesis applied to the same asset class. A new strategy ID requires a genuinely different return mechanism, hypothesis, or asset-class application. Parameter variations and universe expansions remain experiments under the parent strategy unless the economic hypothesis itself changes.

## Current registry

| Strategy ID | Asset class | Economic hypothesis / mechanism | Status |
|---|---|---|---|
| 001 | Indian equities | Short-horizon continuation after unusually strong intraday moves, conditioned on recent positive direction | Active research |
| 002 | TBD | Reserved for a genuinely different hypothesis and/or asset-class combination | Planned |
| 003 | TBD | Reserved | Planned |
| 004 | TBD | Reserved | Planned |
| 005 | TBD | Reserved | Planned |

## Strategy 001 experiment lineage

| Experiment | Universe / instrument | Purpose | Status |
|---|---|---|---|
| 001D | GOLDBEES | Frozen single-instrument implementation | Frozen |
| 001I | GOLDBEES | Prospective OOS / paper-shadow test of 001D | Closed for capital-pursuit priority |
| 001J | U1: point-in-time Nifty 100 equities | Test whether the same economic continuation hypothesis generalizes across liquid equities, with separately pre-registered parameter selection | Active |

001D and 001I must remain immutable historical evidence. 001J is a new experiment under the same Strategy 001 hypothesis family; its parameters must not be back-filled into 001D.

## Asset-class planning principles

The portfolio may eventually include equities, derivatives, commodities, currencies, and crypto. Derivatives strategies may remain paper-only when reliable real-time data, contract economics, lot size, liquidity, or available capital make live deployment inappropriate. Paper-only status does not weaken the requirement for point-in-time data, OOS validation, cost analysis, and reproducibility.

## Promotion rule

A strategy is promoted only after it passes the project's methodology gates: reproducible data, point-in-time correctness, economic rationale, statistical evidence, chronological validation, realistic costs, execution feasibility, and explicit risk controls. A profitable backtest alone is not sufficient.
