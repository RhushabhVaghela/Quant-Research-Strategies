# Quant Research Strategies

This repository contains the research record and implementation workspace for three quantitative strategy research programs.

The strategy documents are written as research stories. They preserve not only the final outcome, but also the reason each experiment was chosen, what the previous result meant, and why that result caused the next step.

## Strategy map

| Strategy | Research question | Final result |
|---|---|---|
| [001 — Intraday Continuation Research](research/journal/strategy_001.md) | Do unusually large positive intraday moves continue when prior short-term direction is positive? | Continuation evidence persisted, but no sufficiently cost-resilient implementation was promoted |
| [002 — Cross-Sectional Residual Reversal Research](research/journal/strategy_002.md) | Do asset-specific relative moves reverse on the next intraday bar? | A measurable reversal relationship existed, but the executable effect was too small relative to turnover and costs |
| [003 — Intraday Prediction and Economic Execution](research/journal/strategy_003.md) | Can short-horizon cross-sectional returns be predicted from observable market state? | Protected prediction passed, but the frozen portfolio failed the economic execution gate |

## How the research is organized

Each strategy follows the actual decision chain:

**Starting question → why this dataset → first observation → interpretation → next question → controlled experiment → result → why the next experiment was chosen → validation → execution economics → conclusion**

This distinction is important:

**Pattern ≠ hypothesis ≠ strategy ≠ validated alpha ≠ economically viable implementation**

A pattern can be real but too small to trade. A model can predict returns but still produce a portfolio that is uneconomic after turnover and execution costs.

## Research standards

The research record emphasizes:

- point-in-time information;
- chronological validation;
- protected holdouts;
- common-support comparisons;
- simple statistical baselines before model escalation;
- explicit transaction-cost and slippage assumptions;
- strategy and experiment lineage;
- preservation of failed and inconclusive branches;
- stopping rules that limit repeated searches of the same historical data.

The purpose of keeping failed branches is not to make the repository larger. It is to preserve why the research moved in one direction instead of another.

## Key terms

**Point-in-time:** use only information available when the decision is made.

**Out-of-sample:** evaluate a frozen idea on data not used to choose it.

**Overfitting:** fitting historical noise so closely that the result does not generalise.

**Turnover:** the amount of portfolio value traded.

**Transaction costs:** brokerage, taxes, exchange fees and other direct trading costs.

**Slippage:** difference between intended and actual execution price.

More specific terms are defined inside each strategy document.
