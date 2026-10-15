# R065 Phase D: Retrospective diagnostic-trial prediction comparison

Date: 2026-10-16. This is a retrospective follow-up to already observed Phase A to C results. It is not independent prospective validation.

Source: Levy et al., `arielevy8/obs-learning-fishing` processed CSV Git blob `01bf211468abe093618dfa5e5c39e883230c9c03`.

Eligibility: apply original paper's all-trial exclusion rule before selecting `critical == 1`. Require exactly eight critical trials per included person and four per stakes condition, days 4,21,38,55,72,89,106,123. Outcomes are the author-computed binary `copied`.

Compare four fixed smoothing-based Bernoulli models using leave-one-entire-participant-out training:

* M0: a single pooled copying probability.
* M1: separate probabilities by high/low stakes.
* M2: separate probabilities by critical block (eight categories, across both stakes).
* M3: separate probabilities by block and stake (16 categories, with each subject only contributing one observed stakes level per block).

Each trained cell uses Beta(4,4) pseudocount smoothing, `p=(k+4)/(n+8)`; do not tune based on results. Empty training cells default to 0.5. On held-out persons compute per-person average log loss and Brier, then average per person. Compare M1 minus M0, M2 minus M0, M3 minus M2, M3 minus M1. Smaller score is better. Report M2 vs M1 as a secondary contrast. Use 20,000 participant-level paired bootstrap draws with xorshift32, seed 20261016, percentile CI indices floor(.025*(draws-1)) and ceil(.975*(draws-1)). All models evaluate exactly the same held-out 8 trials per person; no test label enters training probabilities.

This comparison cannot identify imitation versus goal emulation: it only tests whether descriptive copying frequencies vary usefully with time or stakes. Block and stakes effects may be confounded with counterbalanced sequence, and normal predictors from history have been discarded. In-sample discovery of a time trend motivates M2, so its apparent gain must not be called new independent generalization. The source code and author CSV were not materialized as private local raw files in the previous stage; if the present environment cannot download them, mark local Python real-source replay OPEN and distinguish GitHub connector execution.
