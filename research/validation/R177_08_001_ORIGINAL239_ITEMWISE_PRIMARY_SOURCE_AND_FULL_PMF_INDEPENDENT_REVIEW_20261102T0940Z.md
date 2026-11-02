# R177 / original239 08-001: itemwise source and exact finite PMF audit

run_utc: 2026-11-02T09:40Z
track: R + B, with brief A qualification
target_key: (R+B,R177,2026-10-21 prescore freeze,original239 08-001 itemwise source and finite E1 scientific evidence)
starting_main: 7a4db2d169fd3a2ff935240332d8619781fec081
status: COMPLETE_BOUNDED_ITEMWISE_REVIEW / FORMAL_CROSSWALK_ADOPTION_PENDING
new_E2: 0
new_E3: 0
external_independent_replication: NOT_RUN

## Scope and exact inputs

The original239 v7.8 crosswalk Git blob `36f24235901172642c46853298aebb421f1a3552` lists 08-001 Probability Distribution Families as P0, proposed primary R177, status PROVISIONAL_PRIMARY_README_LINK. Its machine status is explicitly undetermined by README and filenames. The pending queue Git blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f` has 154 items (27 P0, 82 P1, 45 P2). This review does not edit those shared files.

R177 prescore protocol: `protocols/R177_FOUR_FINITE_COUNT_DISTRIBUTION_FAMILIES_108_WORLDS_PRESCORE_FREEZE_2026-10-21.md`, Git blob `fdf3afb48c0ad7bd8783ec5bbfda3b43f14332b3`. Its freeze commit `c8feb4fbf4cb0933705c0e10524f5bc0d3eaf368` precedes the archived result commit `127ff6c087e64694ded7d2eb7ede4becf3668d9e` on the same ancestry path: GitHub compare returned ahead_by=3, behind_by=0.

Archived full PMF: `research/R177/R177_EXACT_RESULTS.json`, Git blob `8a8819e4d85989b518b9152cfc98336457c76a9c`, recorded SHA256 `57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535`. Machine acceptance Git blob `6131e62d673e289ee6e5f3d769c8e5dd46595acc`. The archived report Git blob is `f6279472616fa87f07ae56684c107d04ea9c2dd2`.

Primary English-language statistical references checked: NIST binomial distribution (https://itl.nist.gov/div898/handbook/eda/section3/eda366i.htm); NIST beta-binomial/Polya urn (https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/bbnpdf.htm); He et al. (2015) zero-inflated binomial longitudinal counts, DOI https://doi.org/10.1080/02664763.2015.1023270, free author manuscript https://pmc.ncbi.nlm.nih.gov/articles/PMC4589204/. These are definitions and methodological background. No original empirical participant records from He et al. were obtained or analyzed in R177.

## Independent method and actual execution

A new, independent JavaScript BigInt rational-number implementation was run against the entire remote archived JSON content in the tool V8 environment. It did not import the R177 Python implementation or call the archived generator. The source is `research/validation/r177_original239_itemwise_independent_108_pmf_gate_20261102.js`, remote Git blob `cd1119472009b0cf539986a25942df88e9bca6b2`. The file also includes a Node.js standard-library CLI with a pinned archived JSON SHA256, but the native Node.js CLI itself was NOT_RUN in this cycle.

For each fixed family, n, p and regime, the oracle reconstructed all exact PMF support probabilities from elementary combinatorial formulas and rational rising factorials. It checked all 108 world identities, 972 cells, exact mass 1, mean np, archived variance and P(X=0). It checked 27 matched-parameter groups for the fixed HG < BIN < BB/ZIB variance and zero-probability ordering, verified 90 unique parameter configurations, and independently reconstructed the frozen n=2 BB versus ZIB full-PMF alias (1/3,1/3,1/3). All checks passed.

Five independent fault injections were actually run in the V8 environment with a fresh JSON copy per mutation. A PMF cell corruption, a variance corruption, a duplicate world identity, a false alias probability and an E2 grade promotion were each rejected: 5/5. No random seed was needed; exact deterministic integer arithmetic was used. This is same-team nonblind mathematical reimplementation, not independent external-team replication or a new data-based prediction.

Historical Actions run 39553799453 was separately read from the GitHub API. It completed with conclusion success on 2026-10-21; its three jobs (Python 3.11 tests, Python 3.12 tests, full evaluation/archive) each report success. The workflow run HEAD is `ee940f3d377eba4ea2355b4253f5a28172324ba4`. This is historical CI evidence. No Actions run was started this cycle, and the historical CI status alone does not establish new real-data science.

## Itemwise scientific disposition

The evidence supports `ELIGIBLE_FOR_BOUNDED_E1_ITEMWISE_PRIMARY_R177` for original239 08-001: explicit primary ID linkage, a prescore frozen original finite-model scope, independently reconstructed complete archived PMFs, five negative controls, source documentation and a historical three-job CI record. The precise claim is finite artificial probability distribution mechanism mathematics and an observation-equivalent count-model counterexample.

There is no observed human or historical population used for model fit or predictive testing, no E2/E3, no source-specific empirical replication of He et al., and no external-team replication. Do not promote this record to empirical validation or general real-world identifiability. The original239 shared crosswalk and pending queue remain unchanged; formal owner/governance adoption is pending. **Formal queue net reduction in this cycle: 0.**

## A data, coordination and zero-cost boundaries

The Akata human-versus-LLM `repgames.csv` Git blob `2dd67c6ff80f2d7aa07a70b470e26fe3592c6d95` was briefly re-read, then checked against existing `research/data_scout/A_AKATA_2024_REPEATEDGAMES_HUMAN_LLM_CSV_AND_PAYOFF_GATE_2026-10-29.md` and the prior sign-reversal and timeout audits. The 3900-row, 195-participant data and its payoff discrepancy were already recorded. No new independent R073 dataset or qualification resulted. DF2011 also remains the same original experiment as R074. R073 and PESEN v0.1 are frozen.

All 12 open Codex PRs were checked; PR #1 and #3 concern R257 S53, not this target. No PR was merged or modified. R272 production P0, R333 to R340 mandatory caller and R257 S53 blind-order failures remain open, with no claim of closure here.

No paid API, paper, data, service, cloud compute or new subscription was used. No GitHub Actions were triggered. Actual account billing and remaining free quota are NOT_VERIFIED. Only the two R/B validation-directory files from this cycle were added; historical evidence, frozen protocols and shared indexes were preserved.

Next high-value task: execute R272 preimage-first checker and isolated regeneration against an authentic checkout in ordinary and optimized Python modes, then require the independent checker in the production caller. Separately submit R177's bounded itemwise disposition for governance review without silently changing the 154-item queue.
