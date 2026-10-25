# R160 exact selection and horizontal mixing covariance identity: scientific report

Date: 2026-10-25. Prescore freeze: `research/validation/R160_COVARIANCE_SELECTION_MIXING_IDENTITY_PRESCORE_FREEZE_2026-10-25.md`. Source archive blob `684b0852cb606e713f3cf128fefff95a5325952a`. Original project-authored R160 source and frozen 60-world results were not modified.

## Mathematical derivation
Write `G=p10+p11`, `C=p01+p11`, `D=p11-G*C`, and `Z=1+s*p11`. The R160 artificial selection rule multiplies only the 11 cell by `1+s`. After normalization, the selected association is
`D_sel=(D+s*p00*p11)/Z^2`.
The horizontal cultural mixing step replaces a fraction u of each gene-tag row with the same population cultural target q. The gene marginal is unchanged by this step. Thus
`D_next=(1-u)*(D+s*p00*p11)/(1+s*p11)^2`,
`G_next=(G+s*p11)/(1+s*p11)`.
The target q and conformity parameter h cancel from the same-step D identity. Subsequent D can depend on previous h through changed future joint tables. This is a one-step conditional invariance.

If s=0, the exact identity simplifies to `D_next=(1-u)D` for any current joint table, even with nonzero h. If initial D=0, positive selection s>0 can generate positive D when both p00 and p11 are positive. For the uniform initial table with s=1/2,u=1/4, `D_next=1/54`, regardless of h. These are synthetic algebraic statements only.

## Executed archived source checks
A new standalone Node.js BigInt rational evaluator read the original R160 JSON and checked all 300 archived joint tables for mass, nonnegative cells, gene/culture marginals and association. Verified all 240 consecutive transitions for the D identity and all 240 for G identity. For 20 fixed initial-table/s/u groups, the three distinct h settings gave 40 exact pairwise D equalities. The cultural marginal itself varied with h in 3 of those groups, demonstrating that the D invariance is a genuine cancellation rather than identical entire trajectories.

Predeclared wrong-denominator mutant detected 72 deviations; omitted-selection mutant detected 72 deviations. The count is a count of differing transitions in the frozen grid, not a population error rate. No tolerance, estimation or post-hoc parameter selection.

Executable: `research/validation/r160_covariance_identity_exact.js`. Exact receipt: `research/validation/R160_COVARIANCE_IDENTITY_60_WORLD_EXACT_RECEIPT_2026-10-25.json`. Replay with `node research/validation/r160_covariance_identity_exact.js research/R160/R160_EXACT_RESULTS.json`.

## Scientific boundary
The artificial G/C labels do not represent real people, genetic variants or observed cultures. This calculation is an E1 formal property of a toy selection and mixing map. No original author's full gene-culture coevolution equations were reconstructed. No E2 human predictive or E3 historical evidence was created, no calibration or out-of-sample evaluation occurred, and no external independent replication is claimed. Original R160 CLOSED_BOUNDED_E1 and R073/PESEN v0.1 freeze remain unchanged. Remote CI NOT_RUN.
