# R332 S128 preregistration: uncertain capacity and contingent allocation

Date: 2026-11-01 UTC. Target: (r,R332,S128-v1,uncertain_capacity_precommit_vs_observed_adaptive). Evidence E1 only. This is a prospective complementary experiment; the original R332 protocol, source rows, results, and bounded acceptance remain frozen.

## Source and reuse boundary
R332 original239 02-015, source protocol `protocols/R332_THREE_TASK_COGNITIVE_RESOURCE_112_ATOMS_PRESCORE_FREEZE_2026-10-24.md` (Git blob 17d2022bece9d78a011796e61b581bf172b0c04a). Original costs A=1, B=2, C=3, utilities A=1, B=3, C=4. Recoding r=1 changes B cost to 1. Eight binary subsets in lexical order 000..111. Original solver uses maximum utility and lexical minimum among ties. R332 original code blob fd468b3177c98c59a4612ac9ce5b719ad11398d4, original CSV blob d311966233bc608ba78eadcd696ae6c369c0674a, original 14-world JSON blob 5d7c162c968171f0bb45320ffde835035ed46486.

## Question
When the available resource capacity is uncertain at the moment of committing to a task subset, how much does learning the realized capacity before allocation improve artificial payoff? Distinguish robust fixed subsets, expected-payoff optimal fixed subsets, and capacity-contingent oracle choices. This is a finite artificial decision problem with no empirical human assumptions.

## Frozen design before new results
For each recoding flag r in {0,1}, lower capacity L in {0,1,2,3,4,5}, and high-capacity probability q in {0,1/4,1/2,3/4,1}, capacity C equals L+1 with probability q and L otherwise. Capacity is sampled once per world. All 8 task subsets are available ex ante. If a fixed subset costs more than realized C, realized utility is 0 (all-or-nothing completion); otherwise realized utility is its original assigned sum. Thus fixed expected utility for subset s is ((4-k)*u(s)*1[cost<=L]+k*u(s)*1[cost<=L+1])/4 for q=k/4. Select precommitted subset maximizing expected utility, lexical minimum on ties. Robust baseline chooses original R332 winner at capacity L. Capacity-aware oracle chooses original R332 winner separately at L and L+1, with the same lexical tie rule; oracle expected utility is the probability-weighted sum of their utilities. There are 2*6*5=60 worlds, each with 8 candidate rows, total 480 rows.

Use integer numerators over common denominator 4 throughout. Store the complete 480-row universe as CSV with fields recoded,lower_capacity,high_probability_quarters,bits,cost,utility,low_realized,high_realized,expected_utility_quarters,precommit_bits,precommit_expected_quarters,robust_bits,robust_expected_quarters,oracle_low_bits,oracle_high_bits,oracle_expected_quarters,information_value_quarters. Store 60 world summaries as JSON with exact integer numerators. No floating point in acceptance gates. Use canonical order r, L, k, bits; CSV LF with fixed header and JSON compact one line LF. A separate Python implementation and an independent no-import alternative algorithm must agree on every world and row. Deliberate deletion, duplication, payoff mutation, choice mutation, evidence-tier mutation must be rejected.

## Predicted checks and falsifiers
1. Full 480 rows, 60 unique world keys, 8 unique subsets per world; exact original costs and utilities.
2. `oracle_expected_quarters >= precommit_expected_quarters >= robust_expected_quarters` for every world; negative gap is FAIL.
3. At k=0, precommit and oracle optimal utility equals original R332 utility at L. At k=4, equals original R332 utility at L+1. Tie-breaking at zero-probability endpoints is lexical among all expected-optimal subsets; original endpoint winners must be recovered.
4. The oracle gap is zero at k=0 and k=4. Positive interior gaps are allowed and must be counted rather than assumed.
5. Recoding cannot reduce any of the three optimal values when comparing identical (L,k) worlds, since lowering B cost enlarges feasibility.
6. Report zero and positive information values, strict preference differences, all-or-nothing sensitivity and tie cases. No after-the-fact exclusion, threshold changes or parameter tuning.

## Acceptance and boundaries
Only bounded E1 mathematical extension after full reproducible artifact, frozen source identity, negative controls and independent nonblind calculation. R332's historical CI and status are untouched. GitHub Actions not dispatched without verified zero-charge quota. No E2, E3, calibration, out-of-sample predictive validity, cognitive measurement or external-team replication. R073 and PESEN v0.1 remain frozen. All R models precede classification and fusion; personal decision product remains paused.
