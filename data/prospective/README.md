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
- `run_manifest.json` — immutable activation/protocol metadata for the cohort.

Do not manually edit, backfill, delete, or overwrite prospective observations. If an operational problem occurs, record it as an exception rather than reconstructing the observation from later data.

### Activation boundary

The first run creates an activation timestamp in `run_manifest.json`. Re-running the collector against the same directory must use the same activation timestamp; the implementation rejects attempts to move it. If a genuinely new prospective cohort is required, create a new run directory and register a new activation boundary.

If the collector starts after the session has begun, previously completed bars are not reconstructed as prospective observations. The first eligible bar is the first bar actually captured after activation. Because Strategy 001D uses same-session history, a mid-session start may therefore have an initial warm-up period before signals can be evaluated.

### Integrity validation

After a session, validate the run before interpreting any results:

```powershell
python scripts/validate_strategy_001i_run.py data/prospective/strategy_001i
```

The validator checks the activation boundary, bar ordering, duplicate identifiers, frozen signal timing, orphan outcomes, and outcome-finalization timing.

The authoritative protocol is `research/journal/001I_prospective_oos_paper_shadow_protocol.md`.
