# R253 S49: four-action prefix forecasting of artificial hidden theta, pre-score freeze

Date: 2026-10-29 Asia/Singapore. EVIDENCE=E1 artificial only. Scope: incremental, original R253 formal acceptance unchanged. Repository HEAD inspected before this freeze: 474e00dae3ffdca05d3c17d478870dacf6b9856c. Original source blob 64920e410d5e6550f9a41d8b03f8300320a9a5bf, original nine-world mechanism, theta, private signal, public action, and 4608 nine-bit sources must remain unchanged. No R073 or PESEN v0.1 modification.

## Primary question and deterministic estimand
Predict the artificial binary latent state theta using only the public action prefix Y1..Yk for k=0,1,2,3,4, with the world identity known. For each world, derive the exact conditional posterior P(theta=1 | Y1..Yk) using the 512 equally weighted original source atoms. Score squared error (theta-p)^2, averaged over all 512 atoms, equivalent to exact population Brier risk. k=0 prior is 1/2 and risk 1/4. For zero-probability prefixes do not construct a posterior or count observations. Compare successive risks, and total risk reduction. Keep exact fractions in all primary outputs.

## Frozen design and checks
1. Nine worlds in the original R253 order. Five prefixes per world yield exactly 45 risk cells, 36 adjacent prefix improvements. No fitted parameters, holdout, or hyperparameter selection.
2. Source route: verify original source field names, per-world 512 rows, theta and Y1..Y4 binary, each mass 1/512, distinct nine-bit source keys; aggregate theta=1 and theta=0 counts for each observed prefix. Compute risk from group counts n0*n1/(512*(n0+n1)); sum over groups.
3. Independent theory route: enumerate theta in {0,1} and four private signals in {0,1}^4 with likelihood 1/2 product of q or 1-q, q fixed per original world. Independently implement original world-specific public action maps and compute conditional theta forecast risk from group masses. Compare all 45 exact risks and all 36 exact improvements.
4. Source integrity: verify original CSV blob identity and published SHA256 if executable supports it; reject missing/duplicate source keys, wrong weights, altered actions, malformed field names and unexpected world identities. Original data is immutable.
5. Negative controls: oracle leaked theta as extra predictor must give zero risk for all worlds; deliberately corrupt one exact risk and require comparator failure. These negative controls must be excluded from legitimate scores.
6. Check monotonic non-increasing risk with increasing prefixes; exact observational alias sets (Bayesian, hardcoded, fake report) and (imitation, common signal) must have identical prefix risks. Compare private-only and Bayesian outcomes without inferring human cognitive mechanisms.
7. Calibration here is exact in-sample oracle conditional probability under a fully known finite artificial world, so it is a mathematical identity, not empirical calibration. No resampling confidence intervals or independent real-world validation claims.
8. Scientific scope: E1 only; E2 new human 0, E3 historical 0; no external independent replication. Do not change R253 formal closure, R073 frozen model/scoring, or PESEN v0.1. Preserve owner order: complete R series before classification/fusion.
9. Submission: add only new S49 paths in research/validation and research/evidence_audit, with exact receipt and scripts; re-read main HEAD, file existence, concurrent writes and GitHub permissions before any write. Skip paid CI and expensive runners.

This protocol precedes S49 score calculation and is the sole freeze for S49.