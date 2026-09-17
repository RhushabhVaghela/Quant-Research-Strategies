# Universe Data

This directory is for local point-in-time universe membership tables used by Strategy 002.

Expected canonical file:

`u1_nifty100_membership.csv`

Required columns:

```text
symbol,effective_from,effective_to
```

Rules:

- dates are exchange-local calendar dates;
- membership intervals must not overlap for the same symbol;
- `effective_to` is inclusive only if the loader explicitly documents that convention;
- historical eligibility must use the membership interval containing the observation date;
- do not replace historical membership with today's constituent list;
- preserve the original source and retrieval date in a companion metadata file.

Raw source files are local and should remain ignored by Git where appropriate. Commit only the small, non-sensitive metadata/specification files needed for reproducibility.
