# R210 third method: post-assignment outcome-dependent selection, prescore freeze

Date: 2026-10-27 (Asia/Singapore). Status: FROZEN_BEFORE_NEW_SCORING. Evidence E1 artificial only. Existing R210 final acceptance remains unchanged.

## Fixed upstream identity
Use the seven R210 six-unit artificial worlds and their 20 equally probable balanced 3-treated/3-control assignments exactly as defined in `protocols/R210_RCT_7_WORLDS_140_RANDOM_ASSIGNMENTS_PRESCORE_FREEZE_2026-10-22.md`. No changes to potential outcomes, pair mapping, treatment probabilities, Fisher testing rules or existing R210 artifacts. Original 239 entry 09-001. R073 and PESEN v0.1 stay frozen.

## Prespecified target and outcome selection
For six SUTVA worlds, the target is the finite-population ATE = mean_i(Y_i(1)-Y_i(0)), not a conditional-on-retention estimand. In each of the 20 assignments, observe all six assignment-specific outcomes first. Compare three fixed selection procedures:

* FULL: retain all three observed outcomes in each arm.
* SYMMETRIC_TOP: remove exactly one largest observed outcome from each arm, retaining two per arm.
* ASYMMETRIC: remove the largest observed treated outcome and the smallest observed control outcome, retaining two per arm.

Tie-breaking uses smallest numeric unit ID. The estimand reported for each procedure is the exact randomization expectation of retained treated mean minus retained control mean; its deviation from the finite ATE is selection-induced design bias. Selection uses only post-assignment observed outcomes and arm labels. It never reads an unobserved counterfactual. All 20 assignments have 1/20 probability. Retention is 4/6 per assignment for the two selection rules, with no empty-arm exception.

For the PAIR_INTERFERENCE world, compute the same retained-group contrasts and their exact randomization means, but label comparison with the controlled direct effect 2 as descriptive only. A single-unit SUTVA ATE is undefined in that world.

## Prespecified checks
1. All six FULL expectations equal original R210 finite ATE, and all seven FULL expectations equal original R210 exact recorded expectations.
2. SYMMETRIC_TOP under RAMP_NULL, OUTLIER_NULL and RAMP_CONST_TWO has zero design bias by arm-swap or constant-shift symmetry.
3. ASYMMETRIC under the two sharp-null worlds yields negative selection bias even though all individual effects are zero. Never interpret as an observed human causal effect.
4. Report all 7 worlds x 3 selection rules, 20 assignment records per world, and exact Fraction expectations; provide min/max and exact mean squared error versus finite ATE for six SUTVA worlds. Record all 420 world-procedure-assignment rows, with full observed outcomes, selected IDs, retained outcomes, contrast, and probability.
5. Independent B audit must use a distinct analytical route for the six SUTVA worlds: population means and three-sample order-statistic expectations. For ascending sorted six outcomes x[0..5], E[max_3]=sum_{k=2..5} C(k,2)x[k]/20 and E[min_3]=sum_{k=0..3} C(5-k,2)x[k]/20. Expected retained-two mean is (3*population_mean - E[removed])/2. Compare all 18 SUTVA expected contrasts exactly. This route must not reuse R enumeration output as its input.
6. Negative controls: exchange treatment and control removal rules; replace selection by FULL; mutate one expected contrast; detect each departure when applicable. Record explicitly any degenerate control that cannot detect an error.
7. Verify output row counts, per-world probabilities, original six world values, provenance, SHA256 and rerun reproducibility. Keep scripts standard-library Python, no network, no billed services.

## Interpretation limits
This is a finite design exercise with intentionally outcome-dependent missingness. The selected-data contrast is a descriptive post-randomization statistic; original random assignment alone does not guarantee unbiasedness after outcome-dependent attrition. The analytical B route is internal procedural replication, not external independent replication. No E2/E3 evidence or R073 transfer claim. Any exploratory amendment must be documented separately and never retroactively described as prespecified.
