# Strategy 002 — Chronological Research Split

**Status:** Locked before pattern discovery.

## Purpose

The historical acquisition window contains more observations than may be used for exploratory research. This document prevents accidental use of the final OOS/holdout observations during pattern discovery or development.

## Locked dates

| Phase | Start | End | Primary use |
|---|---|---|---|
| Exploratory development | 2025-09-18 | 2026-06-09 | Descriptive analysis, pattern discovery, economic interpretation, hypothesis formation |
| Development validation | 2026-06-10 | 2026-08-19 | Controlled candidate comparison and robustness checks |
| Final holdout / OOS | 2026-08-20 | 2026-09-17 | One frozen candidate's final chronological evaluation |

All dates are inclusive.

## Information-control rules

### Exploratory development

May be searched repeatedly for pattern discovery, but every search and material decision should be recorded. Repeated searches increase the effective research degrees of freedom.

### Development validation

May be used only after a candidate mechanism/strategy definition is sufficiently specified to justify the test. It can support candidate selection and robustness assessment, but it is not the final untouched OOS test.

### Final holdout / OOS

The holdout is considered **locked and unseen** for all exploratory work.

Before candidate freeze, do not use holdout observations to:

- discover or confirm patterns;
- choose instruments;
- choose features or transformations;
- select thresholds;
- choose holding periods or exits;
- optimize model/strategy parameters;
- compare candidate strategies;
- decide whether a hypothesis survives;
- alter the universe;
- estimate costs for candidate selection when the estimate would influence the candidate.

After candidate freeze, evaluate only the frozen candidate on the holdout. Do not retune it after observing holdout results.

## Important implementation rule

The raw files contain all three periods because a single historical acquisition is operationally simpler. **Physical presence in the CSV is not permission to use the observation.**

Every research script that can influence a Strategy 002 decision must explicitly define its permitted date range. Pattern-discovery scripts should default to the exploratory-development range rather than the entire downloaded period.

A full-window audit remains useful for data-quality diagnostics, because structural integrity is not a strategy-selection result. However, performance statistics, event frequencies, correlations, feature relationships, or other decision-relevant analyses over the full window must not be used for candidate selection.

## Holdout opening condition

The final holdout may be opened only after:

1. a specific economic hypothesis exists;
2. a precise executable strategy definition exists;
3. development/validation analysis is complete;
4. the candidate is frozen with parameters and implementation recorded;
5. the holdout evaluation procedure is fixed.

The holdout result cannot be used to retroactively modify the frozen candidate.

## Current state

Strategy 002 has **no hypothesis and no candidate** yet. Therefore the final holdout remains completely untouched for research discovery.
