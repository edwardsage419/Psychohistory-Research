# R160 selection and cultural mixing covariance identity: frozen E1 protocol

Date 2026-10-25. Source archive `research/R160/R160_EXACT_RESULTS.json` Git blob `684b0852cb606e713f3cf128fefff95a5325952a`. Source program `research/R160/r160_joint_gene_culture_exact.py` Git blob `591f3c96a143e98806f174c53de6f0dec3b1ffc2`. No original source modification.

## Predeclared mathematical target
For a 2x2 artificial joint table `(p00,p01,p10,p11)`, let `G=p10+p11`, `C=p01+p11`, `D=p11-G*C`, `Z=1+s*p11`. R160 selection weights only cell 11 by `1+s`, then horizontal culture mixing with rate u to a culture target q computed from a three-demonstrator majority rule with weight h. Derive and test exact identity:
`D_next=(1-u)*(D+s*p00*p11)/Z^2`.
This predicts one-step gene-culture association independent of the specific target q and hence independent of h when the starting joint table, s and u are held fixed. Test the associated selected G marginal identity `G_next=(G+s*p11)/Z`.

## Frozen checks
Read all 60 frozen original worlds with five archived joint-state observations each. Verify 240 next-step D identities and 240 G marginal identities using independent exact BigInt fractions; check 300 archived joint tables have total mass one, nonnegative cells, and correct archived D. Compare first-step D across the three h values at common initial distribution/s/u, including the neutral, positive and negative association cases. Predeclare negative controls (i) omit one factor Z from the denominator and (ii) ignore selection term `s*p00*p11`; record detected and undetected eligible cases rather than changing tests after observing results. No fitting, calibration or parameter modification.

## Evidence boundaries
This is synthetic E1 for the project-authored joint frequency model only. No real genetic or cultural population data, no causal human genetics, no E2 or E3. Preserve R073 and PESEN v0.1. CI not launched unless confirmed free. Use unique validation paths and expected-HEAD branch lease.
