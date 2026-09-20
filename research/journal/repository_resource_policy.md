# Repository Resource Policy

## Standing rule

Whenever a new GitHub research request is made, first remind ourselves:

> **The repository already contains substantial research resources. Before inventing an analysis, statistical method, feature, strategy component, or implementation from scratch, inspect the repository for relevant existing material.**

The goal is to use the project's accumulated knowledge rather than repeatedly reinventing the same work.

## What counts as a resource

Relevant resources may include:

- Quantra quantitative trading, backtesting, strategy, trade analytics, momentum, volume, volatility, and execution material;
- WorldQuant University material under `trading_resources/WQU_resources/`;
- prior project notebooks and scripts;
- statistical methods and implementations;
- correlation/covariance, PCA, clustering, DBSCAN, similar-stock identification;
- stationarity, autocorrelation, pairs trading, portfolio construction;
- data acquisition and point-in-time validation;
- execution, cost, slippage, and risk-control implementations;
- prior strategy experiments, including failed approaches.

## How to use resources

We have freedom to:

1. reuse code that fits the current problem;
2. adapt or refactor existing code;
3. combine methods from multiple resources;
4. use the mathematical/statistical understanding from educational material;
5. simplify an existing method when the research question does not require its full complexity;
6. replace an existing approach when the current problem requires something different.

The project should prefer **reuse + adaptation + independent validation** over unnecessary reinvention.

## What this policy does not mean

Existing notebooks, code, or claimed strategies are not automatically correct or profitable.

Every reused method must still be evaluated for:

- point-in-time correctness;
- lookahead/leakage;
- data quality;
- suitability to the current asset/universe;
- execution realism;
- statistical validity;
- costs and capacity;
- overfitting/data-snooping risk.

A reference strategy can provide an idea or implementation building block without becoming validated alpha.

## Pattern-first integration

Repository resources should be considered especially during:

1. pattern discovery;
2. statistical characterization;
3. economic hypothesis formulation;
4. strategy construction;
5. backtesting;
6. execution/cost modeling;
7. validation and robustness.

The project is allowed to combine several resources into a new research implementation when that combination is better suited to the current evidence and hypothesis.

## Research-log requirement

When a repository resource materially influences a strategy or investigation, record the relevant resource(s) in the experiment journal or implementation documentation. Explain whether the resource was reused directly, adapted, or used only for conceptual reference.

This makes the accumulated research knowledge discoverable for future work.
