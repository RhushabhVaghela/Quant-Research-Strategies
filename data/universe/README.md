# Universe Data

This directory contains compact point-in-time universe specifications and membership tables used by systematic research experiments.

## Strategy 001J U1

Canonical membership file:

`u1_nifty100_membership.csv`

Required columns:

```text
symbol,effective_from,effective_to
```

Rules:

- dates are exchange-local calendar dates;
- membership intervals must not overlap for the same symbol;
- the loader must document whether `effective_to` is inclusive;
- historical eligibility uses the membership interval containing the observation date;
- today's constituent list must never be substituted for historical membership;
- preserve source name, source URL/document identifier, publication/effective date where available, retrieval date, and transformation notes in companion metadata;
- raw licensed/source files should remain local and ignored by Git where appropriate.

The final Strategy 001J backtest may proceed only after the point-in-time membership table and its metadata pass validation.
