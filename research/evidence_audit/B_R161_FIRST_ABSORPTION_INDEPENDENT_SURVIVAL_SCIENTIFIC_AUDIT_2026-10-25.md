# B scientific audit: R161 first absorption time, independent enumeration and survival summation

Date: 2026-10-25. Frozen before computation: `research/validation/R161_FIRST_ABSORPTION_TIME_THIRD_METHOD_PRESCORE_FREEZE_2026-10-25.md`, commit `4761f0e87f97d9975d0d80bb012047cafa383c23`. This is internal independent algorithmic verification, E1 only.

## Audit object and independent algorithm

R161 original model: N=5 or 7; h in {0,1/4,1/2,1}; binomial next-generation A count conditional on current count; states 0 and N absorbing. Main supplementary computation uses exact rational Gaussian elimination of (I-Q)t=1. Independent B code does not call the main solver or transition builder. It enumerates each of 2^N binary learner configurations and groups probabilities by the number of A learners. It then iterates the survival function `P(T>t)` and sums it to estimate `E[T]`.

For each transient row, let `rho=max_i sum_j Q_ij`. The omitted tail after L survival terms is bounded by `rho^L/(1-rho)`. Predeclared tail requirement <1e-12; numerical comparison to exact main expectation <1e-10. Floating-point arithmetic is used in the independent Node implementation; its theoretical tail bound does not bound accumulated floating-point rounding. Numerical differences were separately checked against the exact Fraction results.

## Executed results

Eight kernels were independently enumerated and compared with the original immutable R161 transition matrices, maximum per-cell absolute discrepancy <=3.34e-16. All 48 frozen initial states matched the main exact expectations with maximum absolute discrepancy <=1.51e-14. Each of the eight survival tails met the predeclared theoretical bound. The L values were:

| N | h=0 | h=1/4 | h=1/2 | h=1 |
|---|---:|---:|---:|---:|
| 5 | 327 | 302 | 278 | 234 |
| 7 | 1378 | 1268 | 1162 | 968 |

Both predeclared negative controls were detected: an initially absorbing state must have first-absorption time zero, and omitting the first survival term for a transient start produces an error of one time unit. The frozen original source and exact JSON remain unchanged.

Program: `research/evidence_audit/r161_b_independent_survival.js`. Full numerical receipt: `research/evidence_audit/R161_B_INDEPENDENT_SURVIVAL_8_KERNEL_RECEIPT_2026-10-25.json`. Exact source: `research/validation/r161_first_absorption_exact.js`. Exact receipt: `research/validation/R161_FIRST_ABSORPTION_8_KERNEL_48_WORLD_EXACT_RECEIPT_2026-10-25.json`.

## Scientific validity and acceptance

A01 PASS for fixed finite Markov absorption-time question. A02 PASS for original R161 fixed blob and fixed model. A03 PASS for local executed two-method arithmetic and archived receipts; new remote CI NOT_RUN. A04 PASS for the two detected negative controls; future structural changes remain OPEN. A05 PASS only for synthetic mathematical scope. A06 PASS for incremental report and immutable append-only paths once commit readback is confirmed.

No data leakage, train/test partition, probability calibration, external independent sample, or bootstrap confidence interval is applicable to the exact synthetic Markov identity. This does not satisfy empirical prediction criteria. E2=0, E3=0. The same research operator authored both implementations; no external team independent replication occurred. R073 and PESEN v0.1 remain frozen. No original R161 acceptance status is altered.
