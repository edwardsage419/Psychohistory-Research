# R296 S92 scientific report: unequal cue salience and oscillatory prediction error
Date: 2026-10-30 UTC. Original catalogue 02-001. Frozen protocol: research/validation/R296_S92_UNEQUAL_CUE_SALIENCE_PRESCORE_FREEZE_2026-10-31.md, commit 4338d098ba7677fbbfca1845ff427bd6fe8c0171. Parent R296 formal bounded E1 acceptance is unchanged.

## Question and original mechanism
Under Rescorla Wagner shared compound error, can unequal cue-specific learning rates produce overshoot and alternating prediction error within the same frozen artificial training schedule? The original 1972 account and the R296 source protocol supply the equation. A relevant English scientific discussion is https://pmc.ncbi.nlm.nih.gov/articles/PMC9614022/ . The new 36-world rate grid is a researcher-designed sensitivity extension, not original empirical data.

## Exact finite method
alpha_A and alpha_B independently take 1/4, 1/2, 3/4. A-only pretraining length is 0 or 8, compound reward 1 or 2, compound stages 0 through 4. Each of 36 worlds yields five deterministic source rows, total 180. Simultaneous updates use e=lambda-A-B, delta_A=alpha_A*e and delta_B=alpha_B*e. Independent-error B is the negative control.

For p=1-(1-alpha_A)^npre, s=alpha_A+alpha_B and q=1-s, the independently derived exact solution is B_m=(alpha_B/s)*(lambda-p)*(1-q^m), A_m=p+(alpha_A/s)*(lambda-p)*(1-q^m), e_m=(lambda-p)*q^m. These are associative strengths, not event probabilities.

## Results
All 180 exact rational rows match the recurrence and closed form. For 12/36 worlds s>1 and the first compound trial overshoots the reward target: e_1<0. In all 12, nonzero e_1 through e_4 alternates in sign. The other 24 worlds have no first-trial negative error; s=1 gives exact convergence after the first trial, and s<1 yields monotone residual decay. All 18 paired pretraining comparisons at fixed rates and target show lower B_4 after eight A pretraining trials. All 9 rate pairs at npre=8 show higher B_4 under lambda=2 than lambda=1.

Representative npre=0, lambda=1, alpha_A=alpha_B=3/4: B_1=3/4, B_2=3/8, B_3=9/16, B_4=15/32. First-trial total A+B=3/2 exceeds target 1, producing error -1/2 and a negative subsequent update. The original R296 alpha_A=alpha_B=1/2, npre=8, lambda=1 result B_4=1/512 is reproduced exactly. Independent-error B remains invariant to A pretraining at fixed alpha_B, target and stage.

## Reproduction and scientific limits
The self-contained Python generator was executed locally, generated 180 CSV rows and 36 JSON summaries, and its persisted-file native check passed. A separate nonblind formula auditor read the persisted artifacts, verified all 180 rows and 36 worlds, and rejected 8/8 deliberately altered cases. Python standard library Fraction was used. This is an internal methodological cross-check, not external-team independent replication. GitHub Actions NOT_RUN because zero billing could not be verified. No stochastic holdout, calibration, human E2, animal E2, or historical E3 inference exists. No R073 or PESEN v0.1 changes.

A01 PASS bounded question; A02 PASS original R296 source and freeze; A03 PASS local native scripts and persisted artifact checks, remote native execution to be verified after commit; A04 PASS eight negative mutations, empirical counterexamples OPEN; A05 PASS E1 scope; A06 PARTIAL pending final remote SHA and CI status check. New S92 scientific status PARTIAL; original R296 CLOSED_BOUNDED_E1 unchanged.
