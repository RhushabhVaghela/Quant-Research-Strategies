# Strategy 003 — Horizon Decision Record

**Status:** Historical methodological record; active horizon is intraday.

## Decision

Strategy 003 currently uses the **next 5-minute bar** as its discovery target:

`Close(t+1) / Close(t) - 1`

expressed as cross-sectional excess return.

## Why did the first draft use 1-day and 5-day targets?

The first draft was designed as a broader **prediction-discovery experiment**. Before deciding that the active research program should operate at a specific intraday horizon, it was reasonable to ask whether observable market information contained predictive content at a smoother medium-horizon scale.

A 5-day close-to-close target is a legitimate research question for stock selection. It is not inherently invalid or inconsistent with quantitative research. The problem is that it answers a **different question** from the project's primary objective: intraday strategy discovery.

## Why did we pivot back?

After reviewing the project's stated objective and execution environment, continuing to optimize the 5-day target would have created scope drift. It could have turned Strategy 003 into a medium-horizon/swing prediction program while the project was explicitly trying to discover intraday mechanisms.

The pivot was therefore **objective alignment, not result shopping**. The five-day experiment remains historical evidence. It was not erased, relabeled, or selectively discarded because of performance.

If medium-horizon research is resumed later, it should receive a separate registered research line with its own hypothesis, feature set, validation boundaries and economic interpretation.

## Why 5 minutes instead of 15 minutes?

The source equity data are 5-minute bars, and the existing intraday research uses that native decision resolution. Starting at one bar preserves the most temporal information and avoids assuming that a 15-minute aggregation is the correct economic horizon before the signal's time scale is known.

The prediction horizon is **not the same thing as the eventual holding period**. A signal may predict the next bar while its economically useful effect persists for several bars. If a genuine signal survives the first discovery gate, a small pre-registered characterization set such as 5/10/15 minutes can test persistence and execution economics.

## Interview-ready answer

> “We initially tested one-day and five-day targets because Strategy 003 was conceived as a broad prediction-discovery experiment. A five-day target is a valid medium-horizon stock-selection question and let us test whether the information set contained predictive content before narrowing the research program. But the project's actual objective is intraday strategy discovery. We recognized that continuing to optimize a five-day target would answer a different question and create scope drift, so we preserved that experiment as historical research and re-registered the active experiment at the native five-minute resolution. That was an objective-alignment decision, not a reaction to a weak result. The five-minute target is a discovery horizon, not a commitment to hold for exactly five minutes; if the signal survives, we can preregister a small set of adjacent horizons such as 5, 10 and 15 minutes to study persistence and execution economics.”

## Guardrail

Do not use this decision record to justify changing horizons after seeing which horizon has the best historical performance. Any new horizon must be registered before confirmatory comparison.
