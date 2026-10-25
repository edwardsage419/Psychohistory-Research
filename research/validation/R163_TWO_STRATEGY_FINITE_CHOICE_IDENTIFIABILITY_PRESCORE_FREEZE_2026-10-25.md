# R163 finite choice identification: prescore freeze
Date: 2026-10-25. Additive R mainline third method. Input: research/R163/R163_EXACT_RESULTS.json Git blob 1f1dba0e64d8540695544bcde50e3df5ebcbf5e6. No changes to frozen R163, R073, PESEN v0.1 or original239 queue.

## Frozen design
Group all 72 source worlds by the six original artificial payoff profiles and three original displayed-payoff transforms (18 contexts). Each context must contain exactly two strategy types (best, means) and two artificial correct tokens each. Verify that copying probability does not depend on artificial correct token and validate both original probabilities from the JSON. No new strategy or model parameters.

For each of the 18 contexts, report exact P(A) under each strategy, exact one-choice total variation distance |p_best-p_means|, and equal-prior optimal binary mechanism-classification error E_n = (1/2) sum_{k=0}^n min[binom(n,k)p_best^k(1-p_best)^(n-k),binom(n,k)p_means^k(1-p_means)^(n-k)] for n in (1,2,4,8). Here n represents hypothetical independent draws under a fixed artificial context. Report number of identical and distinguishable contexts, error monotonicity, and number with zero error at n=1,8. Never treat repeated choices from a human as independent without evidence.

## Predeclared controls
When p_best=p_means, all n yield E_n=1/2, so strategy cannot be identified by copying alone even with infinitely many ideal independent draws. When p_best=1,p_means=0, E_n=0 for n>=1. All E_n must lie in [0,1/2] and be nonincreasing in n. Negative control: substitute p_means=p_best, must raise any distinguishable context's E_1 to 1/2. Explicitly count these detected mutants.

Scientific status at most bounded synthetic E1. No real human E2, history E3, calibration, true prestige or real-payoff inference. This is distinct from R162 cue partition; do not pool R162 and R163 worlds. Run locally; no paid CI.