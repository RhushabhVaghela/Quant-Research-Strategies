# Strategy 003 — Superseded Daily-Target Draft

**Status:** Superseded; not a strategy candidate.

The first implementation of Strategy 003 explored 1-day and 5-day cross-sectional excess-return prediction using daily observations derived from the existing 5-minute equity data.

This was a deliberate exploratory prediction-discovery attempt, not an accidental change of the project's objective. The intent was to test whether the feature space contained predictive information at a smoother medium-horizon scale before narrowing the active research program to the execution-relevant intraday horizon.

The 5-day target represented a close-to-close outcome five trading days after the decision date. That is a multi-day prediction horizon and does not match the project's stated objective of developing intraday strategies.

The pivot back to intraday was therefore an objective-alignment decision, not a response to an unfavorable 5-day result. Continuing to optimize the daily target would have created a separate medium-horizon/swing research program. The daily experiment is retained as historical evidence and as a methodological lesson; it is not silently discarded.

The daily draft also exposed methodological issues around forward-label overlap across chronological model-development boundaries and serial dependence in overlapping multi-day returns. Those issues are retained as lessons learned rather than carried into the revised primary experiment.

The daily draft did not use the protected validation or final holdout to select a strategy. It is preserved as historical research context and is superseded by the intraday next-5-minute discovery program.

The primary 003 protocol is now `research/journal/003_prediction_discovery_protocol.md`.


## Interview rationale

If asked why a five-day target was used when the project ultimately targets intraday strategies, the answer is:

> “The first 003 draft was a broader prediction-discovery experiment. A five-day target is a legitimate medium-horizon stock-selection question and gave us a way to test whether the available information contained predictive content before committing to an intraday horizon. Once we checked that against the project's actual objective, we recognized that optimizing five-day prediction would answer a different question and create scope drift. We therefore preserved the daily work as historical research and re-registered the active experiment at the native five-minute resolution. The change was about objective alignment, not about changing direction because the result was weak.”

This distinction is important: **historical exploratory work can be valid without becoming part of the active research objective.**
