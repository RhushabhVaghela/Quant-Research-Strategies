# Quant Research Learning Path

This is the index for the project's separate educational layer.

- **Strategy registry:** what was tested and its status.
- **Research journal:** what happened and why.
- **Learning modules:** what the research taught us as reusable quant-research skills.

## Module map

| Module | Skill | Strategy examples |
|---|---|---|
| 1 | Hypothesis formation | 001 mean reversion → continuation; 002 residual reversal; 003 prediction hypothesis |
| 2 | Leakage / point-in-time thinking | 001 timing; 002 leave-one-out; 003 train-only transforms |
| 3 | Chronological validation | 001 OOS/robustness; 002 locked splits; 003 purged next-bar validation |
| 4 | Holdout protection | 001/002 closure without rescue; 003 protected periods |
| 5 | Cross-sectional prediction | 002 residual framework; 003 excess-return target |
| 6 | IC / rank IC / quintiles | 003 discovery and characterization |
| 7 | Feature attribution | 003H component attribution |
| 8 | Common-support controls | 003 residual-family control |
| 9 | Mechanism decomposition | 003H simple mechanism |
| 10 | Transaction-cost effects | 001 execution friction; 002 cost gate |
| 11 | Lineage testing | 003H against frozen 001/002 mechanisms |
| 12 | Negative research results | 001 rejection; 002 closure; 003 target supersession |
| 13 | Closing research branches | stopping discipline across all three |
| 14 | From research to strategy | 001D frozen execution |
| 15 | Research decision making | integrated research checklist |

## Suggested study order

### Strategy 001
Modules 1–4, 10, 12–14.

### Strategy 002
Modules 1–5, 10, 12–14.

### Strategy 003
Modules 2–9, 11–15.

The modules are based on the project's actual research record. They are educational summaries and do not override any experiment's original protocol.

See `research/journal/research_learning_modules.md`.


## Completed research cycle — 24 September 2026

Strategies 001–003 now provide three distinct completed lessons.

| Strategy | Primary lesson | Outcome |
|---|---|---|
| 001 | A visually strong continuation pattern must still clear execution and prospective-frequency constraints | Closed; no promoted implementation |
| 002 | A weak but broad cross-sectional reversal can fail once its executable baseline is translated into costs | Closed; no frozen candidate |
| 003 | Stronger predictive metrics can still fail the economic gate when the portfolio turns over too rapidly | Protected prediction passed; frozen economic execution failed; executable line closed |

Strategy 003 is particularly useful as the complete example of why **prediction ≠ trading economics**. Its protected prediction relationship passed, but the fee-floor case already produced negative net economics, so no extra execution-friction assumption was needed to close the candidate.

The research repository therefore enters the next strategy-search stage with Strategies 001–003 preserved as historical evidence rather than active executable candidates. New work should begin from a genuinely different economic mechanism and should first inspect the repository's existing resources before registering a new Strategy ID.
