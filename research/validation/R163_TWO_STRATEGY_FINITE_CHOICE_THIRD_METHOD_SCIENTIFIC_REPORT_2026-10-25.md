# R163 finite-choice identification third method, 2026-10-25
Track R. Protocol frozen before scoring in commit 9ea466577063eb8d331ec1e46c0d6d933104fec9. Original source: research/R163/R163_EXACT_RESULTS.json blob 1f1dba0e64d8540695544bcde50e3df5ebcbf5e6. Original R163 remains CLOSED_BOUNDED_E1; this is additive synthetic evidence only.

## Research question
When do the two frozen artificial success-copying strategies, Imitate the Best and Compare Means, generate different observable choices? How does the theoretically optimal equal-prior classification error change after 1, 2, 4 or 8 **hypothetical independent choices** under the same frozen payoff table?

## Exact results
The 72 original source worlds correspond to 18 distinct payoff profile × display transformation contexts, with two strategies and two correctness tokens each. Directly re-evaluated the original copying probabilities from the archived action and displayed payoff fields. Correctness token had no effect on copying probability, as required.

Of 18 contexts, **7 have exactly identical copying distributions** for the two strategies. Under the stipulated observation channel, any number of copying observations has Bayes classification error 1/2 with equal strategy priors. **11 contexts are distinguishable**. In two raw outlier contexts the rules predict opposite deterministic actions, so one observation has zero theoretical classification error. In three tie-related contexts the single-choice error is 1/4 and eight-choice error is 1/512. In the six flat-payoff contexts, the one-choice error is 5/12 and eight-choice error is 1044605/3359232, approximately 0.311. All 18 contexts passed exact nonincreasing-error and probability bounds. Replacing the means rule with the best rule was detected as a mutant in all 11 distinguishable contexts.

The source JSON receipt contains all 18 probability pairs, total variation distances, and exact errors for n=1,2,4,8. Independent Python Fraction and binomial enumeration rederived the aggregate counts and selected exact values without importing the JavaScript solver.

## Scientific boundary
This is a finite mathematical identifiability calculation with hypothetical iid Bernoulli draws. Real participants may adapt, share histories, use different strategies over time, or be affected by payoff uncertainty. Neither a real participant's mental strategy nor real success can be identified from these artificial calculations. No human E2, historical E3, external independent replication, calibration or true out-of-sample predictive evidence was added. R162 and R163 universes remain separate. The original239 crosswalk v7.8 and 154-item scientific queue remain unchanged. R073 and PESEN v0.1 remain frozen.

Status PASS_BOUNDED_INTERNAL_E1. New CI NOT_RUN because free billing eligibility was not established. No paid resources used.
