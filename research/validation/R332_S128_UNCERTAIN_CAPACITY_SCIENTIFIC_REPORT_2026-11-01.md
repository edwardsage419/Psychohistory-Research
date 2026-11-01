# R332 S128: uncertain capacity, precommitment and the value of capacity information

Date: 2026-11-01 UTC. Research key: (r,R332,S128-v1,uncertain_capacity_precommit_vs_observed_adaptive). Scientific grade: PARTIAL_E1_EXTENSION. The original R332 bounded acceptance remains unchanged.

## Preregistered question and sources
Freeze protocol: `protocols/R332_S128_UNCERTAIN_CAPACITY_PRECOMMIT_VS_ADAPTIVE_PRESCORE_FREEZE_2026-11-01.md`, committed BEFORE any S128 numerical result in commit `b203dc38183c1cdbabf8082d8c4927217b7b05e8`. Original R332 fixed source `protocols/R332_THREE_TASK_COGNITIVE_RESOURCE_112_ATOMS_PRESCORE_FREEZE_2026-10-24.md`, blob `17d2022bece9d78a011796e61b581bf172b0c04a`, original CSV blob `d311966233bc608ba78eadcd696ae6c369c0674a`. Primary conceptual context: Miller (1956), DOI 10.1037/h0043158, with no claimed empirical capacity replication.

The original three-task utilities (1,3,4), baseline costs (1,2,3), recoded costs (1,1,3), lexicographic tie breaking and 8 candidate subsets remain fixed. In S128 the resource capacity is either L or L+1, with high-capacity probability k/4. An infeasible precommitted task set earns zero in that capacity outcome. Compare robust choice feasible at L, best fixed expected-payoff choice, and an oracle that learns capacity before selecting the task set. No real humans or fitted parameters.

## Exact enumerated universe
Two recoding flags, six lower capacities L=0..5, five probabilities k=0..4, eight subsets. Full 480 source rows and 60 world summaries, canonical order r,L,k,bits. All values are integer quarter-utility numerators, with no floating point. Artifact Git blobs:
* `research/validation/R332_S128_ALL_480_CAPACITY_SUBSETS.csv`: `6f60aeb788a81f935caaec470a80e1ce3bbb87e1`, 22,703 bytes.
* `research/validation/R332_S128_EXACT_60_CAPACITY_WORLDS.json`: `a94076add723eaf85eb50bb5955049dce1f4a6d5`, 16,816 bytes.
* `research/validation/r332_s128_uncertain_capacity.js`: `b3c82120fb80975f426259adab6a8ce04f27afa1`.

## Results
The capacity-aware oracle exceeds the optimal precommitted expected utility in 24 of 60 worlds. The remaining 36 have zero information value. Maximum information value is 6 quarter-units, or 1.5 utility units. Sum across all 60 constructed worlds is 59 quarter-units; this is an enumeration summary, not an expected population effect. In 20 worlds, optimal risky precommitment exceeds the always-feasible robust baseline. Oracle >= precommit >= robust holds in all 60 worlds. At k=0 or k=4, the oracle and optimal precommitment coincide in all 24 endpoint worlds.

Largest gap example: recoded r=1, L=3, k=2. The low capacity 3 selects subset 001 (C), utility 4. High capacity 4 selects 011 (B+C), utility 7. Oracle expected utility = (4+7)/2 = 5.5. Best precommitted subset 001 yields 4, and robust also yields 4. The value of observing capacity is 1.5. A fixed 011 subset has utility 0 if capacity is 3, utility 7 if capacity is 4, expected 3.5; its risk of noncompletion prevents it from beating 001.

Without recoding, the 30-world sum of information-value quarter-units is 34. With recoding it is 25. Recoding never decreases any of the three optimal utility values at identical L,k. It can decrease the value of additional information by changing which feasible subsets are optimal. No general claim about cognitive resource savings follows from these assigned costs.

## Reproduction and negative evidence
R source is a deterministic no-dependency Node script; V8-adapted execution of the exact remote archived source against the exact remote CSV/JSON returned PASS. Deliberate remote JSON world-count corruption was rejected. Separate Python 3 standard-library implementation, with no R source import, independently generated the same complete CSV and JSON Git blob SHA1 identities. Python auditor on the independently reconstructed complete receipts returned `PASS_NONBLIND_INTERNAL_E1: 60 worlds, 480 rows, 8 live mutations rejected` in normal and `python -O` modes. The exact Python auditor source is archived at `research/evidence_audit/b_r332_s128_independent_audit.py`.

The original R332 112-row/14-world source and historical CI were read as frozen context; no R332 original file was modified. New native Node CLI and GitHub Actions were NOT_RUN. No empirical out-of-sample prediction, human calibration, clustered resampling, historical validation, external team or causal inference. A01 scope PASS; A02 source PASS for original Git blobs; A03 V8 and independent Python PASS with native Node OPEN; A04 eight mutations PASS and all negative results retained; A05 E1 boundary PASS; A06 bounded extension report/remote receipts PASS with CI OPEN. This extension does not upgrade original R332 or R073/PESEN.

## Next
Continue original239 R-series with R333 after fresh HEAD and duplicate-target check. Separate empirical measurement would require precommitted real capacity operationalization, repeated participants, and independent validation; none is established here. Keep R073 and PESEN v0.1 frozen, E1/E2/E3 separate, classification/fusion and personal product paused.
