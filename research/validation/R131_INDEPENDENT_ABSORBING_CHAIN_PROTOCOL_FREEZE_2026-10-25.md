# R131 independent absorbing Markov chain audit: prescore freeze

Date: 2026-10-25. Scope: original239 05-007, existing R131 only. Research level: finite synthetic E1. No new model number.

## Provenance and immutable scope
Main HEAD checked before this freeze: `192ecb7df5918903152d604cc2115f91cfc5021f`. Existing R131 primary code blob: `3c61e0c3c0fe7a6d4458eccd8fc18e9714e7152f`. Existing final acceptance blob: `3fa4bc6657ae38ee306e106dbd98f21edd48451b`. Taylor and Jonker (1978), DOI 10.1016/0025-5564(78)90077-9, provides the separate three-strategy ESS and continuous/discrete dynamics examples. The five-person Moran birth-death illustration is a project-created extension, not a result of that 1978 paper.

## Frozen independent computation
For each population size N=2,...,8 and each ordered fitness pair (resident A, mutant B) in {(3,2),(1,1),(2,3)}, independently construct the full (N+1) by (N+1) transition matrix from a birth draw weighted by fitness followed by a uniformly random death draw. States are the number i of mutant B individuals. Boundary states 0 and N are absorbing. Use exact rational arithmetic and independently solve the interior Dirichlet system (I-Q)h=b by pivoted Gauss-Jordan elimination, where h_0=0 and h_N=1. Do not use the original R131 forward-difference fixation routine or import its source to construct the independent result.

Predeclared checks: 7 population sizes times 3 fitness scenarios times all N-1 interior starting states = 84 independent fixation probabilities. All 84 transition rows sum exactly to one, all 84 solved Dirichlet residuals are zero, all h_i are in [0,1], and h_i strictly increases with i. Compare h_1 with the existing R131 forward-difference implementation only after independent construction, giving 21 checks. Fixed anchors at N=5: disadvantaged mutant h_1=16/211, neutral h_1=1/5, advantaged mutant h_1=81/211. Two negative controls must reject a forced neutral h_1=1/5 under disadvantage and a modified absorbing boundary h_N=0. Do not count code assertions as external team replication.

## Interpretation and acceptance gate
Exact agreement supports only this finite, artificial Moran process. It does not estimate real human or animal population fitness, mutation, sampling, probability calibration, historical change, or the original 1978 authors' empirical findings. Original R131 research and its CI remain separate. New CI is optional and must not run if GitHub Actions cost status is uncertain. This audit cannot change R073, PESEN v0.1, the original239 global crosswalk, or any existing research file. No E2/E3 or new original239 completion is claimed by the freeze.
