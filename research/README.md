# Quant Research Workspace

This directory contains the research record for the strategy programs.

## Research story format

Each strategy document preserves the actual chain of decisions rather than presenting only a final result:

**starting question → why the dataset fits the question → first test → result → interpretation → next question → why the next experiment is justified → result → validation → execution economics → conclusion**

The purpose of the sequence is to make the research auditable. A later experiment should exist because an earlier result created a specific unanswered question, not because it happened to improve a historical number.

## Research principles

- A pattern is not automatically a hypothesis.
- A hypothesis is not automatically a strategy.
- A predictive result is not automatically economically tradable.
- Exploratory research, development validation, protected validation and final holdout evidence are kept distinct.
- Negative and inconclusive results remain part of the research record.
- New experiments should introduce a new question or resolve a known limitation rather than repeatedly search the same historical sample.

## Strategy documents

- `journal/strategy_001.md` — complete Strategy 001 story, from the original GOLDBEES mean-reversion question through continuation discovery, point-in-time validation, frozen execution, robustness, prospective testing, broader-universe research and closure.
- `journal/strategy_002.md` — complete Strategy 002 story, from universe/data audit through hypothesis-free cross-sectional discovery, residual mechanism testing, formal hypothesis, one-bar validation, turnover-reduction experiments and closure.
- `journal/strategy_003.md` — complete Strategy 003 story, from prediction discovery and the superseded daily-target experiment through feature decomposition, mechanism interpretation, lineage separation, protected prediction validation, corrected economic execution and closure.

## Methodology

`methodology.md` contains the common research controls used across the projects, including point-in-time construction, chronological validation, execution-cost treatment and holdout discipline.

The strategy documents should be read as the detailed application of those controls to the actual research history.