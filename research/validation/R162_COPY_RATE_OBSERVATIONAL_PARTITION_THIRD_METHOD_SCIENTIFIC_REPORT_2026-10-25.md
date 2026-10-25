# R162 third-method observational partition, 2026-10-25

Track R. Scientific status: PASS_BOUNDED_INTERNAL_E1. Pre-score freeze commit 0e8b464b79e0176f68d9832e4290a812e0152ce0; original 72-world source Git blob aa6fd210a803d0914b5d18692f9a49c86f9b3009; additive executed solver research/validation/r162_observational_partition_exact.js. No modification to the original R162 model or frozen protocols.

## Question and method
How many distinct artificial attention mechanisms remain observationally equivalent when the only available observation is the population probability of copying action A? The original R162 mechanism was previously validated by two exact routes. This study adds a complete, exact **observation-equivalence partition** of its 72 frozen worlds, without introducing parameters, fitting, or post-hoc world selection. For every world, the solver checked the five original probability and accuracy outputs by integer cross multiplication against the immutable JSON, then grouped worlds by four prespecified observation schemes.

## Executed exact results
| Observation scheme | Classes | Maximum class size | Worlds in nonsingleton classes | Classes with mixed artificial-accuracy advantage signs |
| --- | ---: | ---: | ---: | ---: |
| P0 copying probability only | 9 | 18 | 72 | 7 |
| P1 copying probability plus all three demonstrator actions | 12 | 18 | 72 | 8 |
| P2 P1 plus externally assigned correct action | 24 | 9 | 64 | 0 |
| P3 P2 plus attention bonus count | 32 | 3 | 64 | 0 |

All four partitions cover the same 72 source worlds. The complete class-size histograms are in the JSON receipt. The nonmonotonic number of mixed-sign classes across P0/P1 reflects finer partitioning; mixed-sign worlds decline from 36 to 24.

## Exact observational twins and identification boundary
World A: demonstrators (1,0,0), favored index 0, bonus 3, synthetic correct token 1: P(A)=2/3 and accuracy advantage +1/3.
World B: demonstrators (0,1,1), bonus 0, synthetic correct token 1: P(A)=2/3 and accuracy advantage 0.
World C: same as A with synthetic correct token 0: P(A)=2/3 and accuracy advantage -1/3.
Thus even infinitely many independent Bernoulli copying choices alone cannot distinguish these three artificial worlds because their likelihoods are identical for any observed sequence of copied actions. This is a statement about a fixed toy model, not a proof about real prestige, competence, causal effects or people.

For a fixed observed action triple y and externally known correct token c, the **artificial** success advantage is identified as (2c-1)[P(A)-sum(y)/3], even though the attention mechanism may remain unidentified. This is why P2 has no mixed-sign classes while 64 of 72 worlds remain in nonsingleton classes.

## Executed controls and limits
Weighted-copying-to-neutral mutant detected in 24 worlds. Correct-token-reversal mutant changes the nonzero advantage sign in 24 worlds. Both checks were computed rather than merely declared.
Independent B algorithm separately enumerated the physical tickets using Python Fraction and generated 72 worlds without importing the original R162 source or this JavaScript script. It matched all four partition counts, class-size histograms and both mutants. This is **internal methodological cross-check** by the same research operation, not external independent replication.

No real human observations, calibrated predictions, confidence intervals, sample-level bootstrap, real prestige measures, or out-of-sample tests are available here. No new E2 or E3 evidence. The original R162 bounded acceptance remains unchanged; the original239 v7.8 crosswalk and 154-item evidence queue are unchanged. R073 and PESEN v0.1 remain frozen. New CI NOT_RUN because free billing status was not established. No paid services used.
