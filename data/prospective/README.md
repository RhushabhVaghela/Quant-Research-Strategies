# Prospective Data

This directory is reserved for local prospective Strategy 001I paper/shadow records.

## Strategy 001I

The live collector writes a run directory such as:

```text
strategy_001i/
├── run_manifest.json
├── bars.csv
├── signals.csv
└── outcomes.csv
```

These records are intentionally **not committed to Git** by default. They are point-in-time research evidence generated after the 001D strategy was frozen.

- `bars.csv` — completed 5-minute bars captured during the prospective run.
- `signals.csv` — append-only signal records created at the event-bar boundary.
- `outcomes.csv` — outcomes appended only after the frozen exit bar has completed.
- `run_manifest.json` — activation/protocol metadata.

Do not manually edit, backfill, delete, or overwrite prospective observations. If an operational problem occurs, record it as an exception rather than reconstructing the observation from later data.

The authoritative protocol is `research/journal/001I_prospective_oos_paper_shadow_protocol.md`.
