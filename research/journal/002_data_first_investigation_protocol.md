# Strategy 002 — Data-First Investigation Protocol

**Status:** Active research investigation — no trading hypothesis selected  
**Restart rationale:** Apply the pattern-first methodology learned from Strategy 001 rather than committing to a strategy mechanism before understanding the data.

## 1. Research objective

Strategy 002 begins with an intentionally open question:

> What does the available market/data environment contain that could plausibly support a robust, executable trading strategy?

The answer must come from evidence. We do not begin by assuming mean reversion, momentum, pairs trading, fundamentals, volatility, arbitrage, or any other mechanism.

The output of this phase is **not a backtest return**. The output is a defensible description of the data, market structure, relevant economic context, and statistically interesting patterns that may justify one or more falsifiable hypotheses.

## 2. What was intentionally removed

The earlier Strategy 002 pair-mean-reversion path has been abandoned and removed from the active repository tree.

Removed active artifacts included:

- pair-mean-reversion specification;
- pair-selection implementation;
- pair-trading engine;
- development runner and tests;
- formation pair outputs and metadata;
- pair-specific development configuration/results.

This deletion does not erase history. Git history preserves the abandoned research path and its removal. The old pair result must not be reused as current Strategy 002 evidence.

## 3. Research universe

The universe must be selected for research reasons that are independent of future strategy P&L.

At the start of the investigation, record:

- asset class and instruments;
- data provider/source;
- instrument identifiers;
- available history;
- bar/tick frequency;
- session calendar;
- corporate-action treatment;
- survivorship limitations;
- liquidity/turnover fields;
- fundamental/economic fields, if any;
- point-in-time availability of every field that may later be used.

If the existing U1 universe is reused, its known construction and limitations must be carried forward explicitly rather than silently treating it as a perfect historical universe.

## 4. Data audit — first gate

Before looking for trading patterns, verify:

- schema and data types;
- timestamp timezone and ordering;
- duplicate timestamps;
- missing bars and interior gaps;
- terminal session truncation;
- OHLC consistency;
- non-positive prices;
- negative volume;
- session boundaries;
- corporate-action anomalies where detectable;
- symbol continuity;
- historical coverage;
- cross-sectional coverage;
- liquidity/volume coverage;
- availability of any fundamental/economic fields;
- point-in-time availability where applicable.

A data-quality problem must be repaired or documented before pattern interpretation. Do not relax a validation gate merely to obtain more observations.

## 5. Market and fundamental context

Before interpreting statistical patterns, understand what the instruments represent.

Where reliable data exists and is applicable, document:

- business/sector/industry classification;
- major economic drivers;
- market microstructure;
- trading-session mechanics;
- corporate-action characteristics;
- earnings/dividend/event structure;
- macro variables;
- rates, FX, commodities, or other relevant drivers;
- fundamental valuation/profitability/growth variables;
- whether those variables were actually knowable at the relevant historical timestamp.

Fundamental information is optional when it is not economically relevant or reliable for the chosen universe. Do not manufacture a fundamental narrative for a purely market-microstructure phenomenon.

## 6. Descriptive data understanding

Characterize the raw market behavior without constructing a trading rule.

At minimum investigate:

### Returns
- one-bar and multi-bar return distributions;
- mean, median, standard deviation;
- skewness and tails;
- extreme observations;
- autocorrelation.

### Volatility
- intraday volatility;
- rolling volatility;
- volatility clustering;
- volatility persistence;
- relation between volatility and volume.

### Volume and liquidity
- volume distribution;
- turnover where available;
- volume concentration by time of day;
- price/volume relationships;
- liquidity differences across instruments.

### Intraday structure
- returns by time of day;
- volatility by time of day;
- volume by time of day;
- opening and closing behavior;
- day-of-week effects where economically meaningful.

### Cross-sectional structure
- return correlations;
- rank correlations;
- covariance;
- clustering/PCA where justified;
- common-factor behavior;
- dispersion across securities.

These are descriptive investigations, not trading signals.

## 7. Pattern discovery

After the basic data structure is understood, investigate candidate patterns using methods already available in the repository.

Possible pattern families include:

- continuation/momentum;
- reversal/mean reversion;
- cross-sectional relative strength;
- lead-lag relationships;
- volatility behavior;
- volume/flow relationships;
- seasonality;
- factor/fundamental relationships;
- relative-value relationships;
- event-driven behavior;
- regime-dependent behavior.

These are **categories to investigate, not hypotheses to assume**.

The investigation must record which families were examined, which were not, and how many alternative definitions/horizons/transformations were tried.

## 8. Pattern characterization

A pattern is worth considering only if it can be characterized beyond a single attractive statistic.

For each promising pattern record:

- exact definition;
- information timestamp;
- prediction horizon;
- population;
- number of observations;
- cross-sectional breadth;
- temporal breadth;
- effect size;
- median and distribution;
- tails;
- dependence between observations;
- regime sensitivity;
- sensitivity to reasonable nearby definitions;
- liquidity/execution context;
- economic interpretation;
- limitations.

A single-stock or single-period effect is not automatically a broad market pattern.

## 9. Economic interpretation

Before writing a formal hypothesis, ask:

1. What could cause this pattern?
2. Who would be taking the other side?
3. Why would the opportunity remain available?
4. What risk is being compensated?
5. Could the effect simply be a data artifact?
6. Would transaction costs plausibly consume it?
7. Does the mechanism imply conditions where the effect should strengthen or weaken?

The interpretation must remain distinguishable from the statistical observation.

## 10. Hypothesis gate

Only after pattern characterization may a Strategy 002 hypothesis be proposed.

A valid hypothesis must state:

- economic mechanism;
- universe;
- signal/information;
- expected direction of the effect;
- prediction horizon;
- conditions under which it should operate;
- conditions under which it should fail;
- why it could survive costs;
- falsification criteria.

At this point, and not earlier, the research registry should be updated with the proposed mechanism.

## 11. Multiple-testing and data-snooping control

Exploration is necessarily broader than confirmatory testing, so the research process must make its breadth visible.

Maintain an investigation log containing:

- pattern family;
- variable definitions;
- transformations;
- horizons;
- universes;
- filters;
- statistical tests;
- number of variants examined;
- date of investigation;
- conclusion.

Do not hide unsuccessful investigations.

Repeated searches of the same sample increase the effective research space even when no explicit parameter optimization is performed.

The eventual hypothesis should therefore be evaluated with evidence that is appropriately separated from the exploratory search.

## 12. Holdout protection

The untouched chronological holdout is not used during this phase to:

- discover patterns;
- select variables;
- choose a hypothesis;
- choose thresholds;
- choose a universe;
- choose exits;
- compare candidate strategies.

The holdout is opened only after a complete candidate has been frozen.

## 13. Repository-resource requirement

Before implementing a new analysis, inspect the repository for relevant existing resources.

Particularly review:

- Quantra statistical/strategy notebooks;
- WQU Financial Data material;
- correlation/covariance;
- PCA;
- clustering and DBSCAN;
- stationarity;
- autocorrelation;
- pairs/relative-value methods;
- event studies;
- portfolio construction;
- broker data acquisition;
- point-in-time validation;
- execution and cost utilities.

Reuse, adapt, refactor, or combine existing methods where appropriate. Existing educational material is a building block, not validated alpha.

## 14. Required investigation deliverables

Before Strategy 002 receives a hypothesis, create:

1. data audit report;
2. market/universe description;
3. fundamental/economic context report where applicable;
4. descriptive statistics report;
5. pattern-discovery experiment log;
6. pattern-characterization reports for promising findings;
7. repository-resource review record;
8. hypothesis candidates with explicit evidence and limitations;
9. decision record explaining why a hypothesis was selected or why no hypothesis was justified.

## 15. Definition of success for this phase

Success is **not** finding a profitable backtest.

Success is reaching one of two defensible conclusions:

### Outcome A — hypothesis justified

The investigation identifies a sufficiently broad, stable, economically interpretable pattern that justifies a formal falsifiable hypothesis.

### Outcome B — no sufficiently strong hypothesis

The investigation does not identify a sufficiently robust pattern. The result is preserved as a negative/inconclusive research outcome, and another research direction may be opened without pretending that a weak pattern is an alpha.

Both outcomes are valid.

## 16. Immediate next step

Do not build a Strategy 002 trading engine yet.

First:

1. inspect the existing repository resources relevant to Indian-equity data investigation;
2. verify the current reusable universe/data inputs and their known limitations;
3. run the existing data-integrity gates over the intended investigation window;
4. inventory available market and fundamental fields;
5. produce the first descriptive data-understanding report;
6. only then begin the preregistered pattern-discovery experiments.

No holdout access is required for these first steps.
