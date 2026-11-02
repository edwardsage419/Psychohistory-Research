# R127 / original239 05-003: sharp transition bounds from published human aggregates

Date: 2026-11-02 (Asia/Singapore). Track: R and B scientific verification. Initial observed main: `ba5b6da56e6e5fec5e3f9b7adb839ebcda426be1`. Status: **COMPLETE_MARGINAL_BOUND_SCOPE / FORMAL_ITEMWISE_ACCEPTANCE_PARTIAL**.

## Frozen question and primary evidence

Can the seven published 1990 Treatment A period-1 and period-10 action marginals bound how many of the 107 participants must have changed action, even though no person-level identifiers or transitions are available? This is an incremental audit of original239 P0 `05-003 Coordination Game`, associated with R127. It does not alter the original R127 frozen protocol or historical receipts.

Original publication: Van Huyck, Battalio and Beil (1990), *Tacit Coordination Games, Strategic Uncertainty, and Coordination Failure*, AER 80(1):234–248. University-hosted scan: https://econweb.ucsd.edu/~jandreoni/Econ264/papers/Van%20Huyck%20et%20al%20AER%201990.pdf . This run inspected the actual printed Table 2 on pages 240 and 241, covering all seven sessions, and checked its period-1 and period-10 counts against the R127 archive. The R127 source snapshot is Git blob `6964fa57e291e719e8cc071cc3a70d73836363e4`. The table has session sizes 16,16,14,15,16,16,14, total 107, with 2 period-1 and 77 period-10 action-1 choices. The original study repeats the game ten times with the same experimental session cohort; bounds are conditional on stable participant identities within each session.

## Mathematical identification contract

For each session, let `a_i` and `b_j` be the published period-1 and period-10 marginal counts for efforts 7 through 1. A latent nonnegative integer 7×7 transition matrix `x_ij` must have row sums `a_i` and column sums `b_j`. Every feasible such matrix is compatible with the two observed marginals. The exact minimum and maximum of a target event over this transportation polytope are **sharp marginal bounds**, with integer solutions.

For the number whose effort changed, the lower bound is `n - sum_i min(a_i,b_i)`; the upper bound is `n - max(0, max_i(a_i+b_i-n))`. For effort 7 to effort 1, bounds are `max(0,a_7+b_1-n)` and `min(a_7,b_1)`. For new entrants into effort 1, bounds are `max(0,b_1-a_1)` and `min(b_1,n-a_1)`. These formulas are checked against an independent integer min-cost flow optimizer that constructs a valid 7×7 matrix attaining each extreme. Different extrema need not occur in the same latent transition matrix.

| Experiment | n | Any effort change, sharp range | 7 to 1, sharp range | New entrants to 1, sharp range |
| --- | ---: | ---: | ---: | ---: |
| 1 | 16 | 13 to 16 | 5 to 8 | 13 to 13 |
| 2 | 16 | 13 to 16 | 1 to 4 | 13 to 13 |
| 3 | 14 | 11 to 14 | 0 to 4 | 9 to 9 |
| 4 | 15 | 15 to 15 | 4 to 6 | 13 to 13 |
| 5 | 16 | 14 to 16 | 0 to 2 | 11 to 11 |
| 6 | 16 | 12 to 16 | 0 to 5 | 7 to 8 |
| 7 | 14 | 11 to 14 | 0 to 4 | 9 to 10 |
| **All seven, sessionwise** | **107** | **89 to 107** | **10 to 33** | **75 to 77** |

Consequently, at least **89/107 (83.18%)** participants must have changed their effort between periods 1 and 10 if the within-session roster is stable. At least 75 must have entered action 1 from a different initial effort. At least 10 and at most 33 could have moved specifically from 7 to 1. No exact person-specific transition count, causal learning mechanism, individual prediction, or independent sample generalization is identified.

## Independently executed computation and negative controls

Standalone program: `research/validation/r127_table2_sharp_transition_bounds_20261102.js`. The optimizer does not import the R127 implementation. It checks row/column conservation for every extreme and crosschecks all three bound families with separate closed-form identities. Independent brute-force enumeration of all feasible 3×3 transportation tables for each pair of margins with total n=1,2,3,4 validated **1110** objective/min-max cases. Seven deliberate marginal-count corruptions were rejected **7/7**. No randomness or external dependencies were used.

Execution performed in the connected JavaScript V8 runtime. Native Node.js CLI execution with the exact R127 repository checkout is **NOT_RUN**. The committed CLI separately authenticates the original R127 source Git blob before returning a source-bound PASS; `--selftest` reports only synthetic algorithm checks. This run's arithmetic was executed against the seven published marginals. GitHub CI was not triggered.

## Evidence limits and acceptance

This is **internal nonblind reanalysis of previously published human experimental aggregate counts**, plus exact mathematical partial identification. It is stronger than an invented person-level reconstruction and remains distinct from a new E2 individual holdout prediction. E1 synthetic model claims and published human aggregate evidence are reported separately. New E2 scores: 0. New E3 scores: 0. External team replication: NOT_RUN. Original239 P0 `05-003` remains in the actual pending itemwise queue pending formal source and acceptance adjudication. Queue reduction: 0.

Other known P0 risks, including R272 optimized Python false acceptance, R333–R340 composite mandatory-caller adoption, and R257 S53 historical blind-order failure, remain OPEN. This analysis neither repairs nor closes them. R073 and PESEN v0.1 remain frozen. No paid API, purchase, cloud runner, or Actions dispatch occurred; account billing is NOT_VERIFIED.

Next: obtain a trustworthy full checkout for R272 and R333–R340 native fail-closed controls, and independently adjudicate R127 original239 source coverage without claiming identified individual transitions.
