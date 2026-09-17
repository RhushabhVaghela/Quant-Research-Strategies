# Strategy 001J — Frozen September 2026 Experiment Window

**Status:** Frozen before Strategy 001J performance evaluation  
**Timezone:** Asia/Kolkata  
**Universe:** U1 — locked Kite-native liquid NSE EQ top 50  
**Frequency:** 5-minute OHLCV

## Frozen 90-session window

The accelerated experiment is frozen to **90 observed NSE trading sessions ending 2026-09-17**:

| Phase | Sessions | Inclusive dates |
|---|---:|---|
| Formation | 20 | 2026-05-12 through 2026-06-09 |
| Development | 50 | 2026-06-10 through 2026-08-19 |
| Holdout | 20 | 2026-08-20 through 2026-09-17 |

These are calendar-date boundaries. NSE holidays inside the interval are not counted as sessions. The phase boundaries were selected from the exchange-session calendar before examining 001J performance and are now immutable for this experiment.

The current U1 membership interval begins in 2025, so the frozen 2026 window is fully inside the registered U1 membership period. The formation phase above is **experiment formation for 001J**, not the earlier U1 liquidity-formation process that created the membership file.

## Why 90 sessions rather than 90 calendar days

The 001J specification calls for approximately 20 formation, 50 development, and 20 chronological holdout sessions. A literal 90-calendar-day window ending 2026-09-17 cannot contain 90 market sessions and therefore cannot satisfy that split. The experiment consequently freezes 90 **trading sessions**, while Kite request-size limits remain an acquisition/chunking concern rather than a reason to shorten the research sample.

## Phase discipline

- **Formation:** no Strategy 001J performance is used for U1 construction or candidate selection.
- **Development:** the preregistered 162-configuration grid may be evaluated here only.
- **Holdout:** opened only after a development candidate is frozen; no retuning from holdout observations.
- **Prospective:** begins only after holdout review and candidate freeze.

The frozen 001D parameters remain the first transfer baseline. The baseline is not an optimizer.

## Data gate contract

The data gate evaluates the actual intraday structure used by the engine rather than comparing file timestamps with midnight boundaries.

For each selected U1 symbol and observed session:

1. first bar must be 09:15 IST;
2. timestamps must advance exactly in 5-minute increments with no interior gaps;
3. OHLC must be positive and volume non-negative;
4. at least 37 bars must be present to permit one complete frozen-baseline trade path (30 completed lookback bars, signal bar, next-bar entry, and six-bar exit);
5. the final observed bar may be earlier than 15:25 IST if the session is otherwise contiguous — this is recorded as terminal truncation rather than treated as an automatic failure;
6. a missing interior bar, missing session, invalid session boundary, or short session fails the gate.

This explicitly allows clean 72-bar sessions ending at 15:10 while rejecting a session with an interior missing 5-minute bar.

## Evidence already collected

The targeted 2026-09-17 broker re-download covered all 50 U1 symbols and passed the raw audit. The observed 72-versus-75-bar session lengths therefore remain a data-integrity item to validate structurally, not a reason to impose an artificial universal 15:30 requirement.

## No result inspection before the freeze

This window file is a methodological lock. No Strategy 001J P&L, trade count, win rate, parameter-grid result, holdout result, or prospective observation is used to choose these dates.
