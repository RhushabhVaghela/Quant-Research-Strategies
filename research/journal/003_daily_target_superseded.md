# Strategy 003 — Superseded Daily-Target Draft

**Status:** Superseded; not a strategy candidate.

The first implementation of Strategy 003 explored 1-day and 5-day cross-sectional excess-return prediction using daily observations derived from the existing 5-minute equity data.

The 5-day target represented a close-to-close outcome five trading days after the decision date. That is a multi-day prediction horizon and does not match the project's stated objective of developing intraday strategies.

The daily draft also exposed methodological issues around forward-label overlap across chronological model-development boundaries and serial dependence in overlapping multi-day returns. Those issues are retained as lessons learned rather than carried into the revised primary experiment.

The daily draft did not use the protected validation or final holdout to select a strategy. It is preserved as historical research context and is superseded by the intraday next-5-minute discovery program.

The primary 003 protocol is now `research/journal/003_prediction_discovery_protocol.md`.
