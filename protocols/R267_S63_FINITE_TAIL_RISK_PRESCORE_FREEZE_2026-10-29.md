# R267 S63: finite-sample absolute-error tail risk, prescore protocol

Date: 2026-10-29 UTC. Research family: R267, original catalogue 11-027. Baseline main HEAD before freeze: `ec92f2b08a7c9b6349c87dbc365a044f002d1244`. Scope: supplementary E1 mathematical experiment only. Original R267 acceptance, nine functions, sample design and source identities remain unchanged.

## Fixed input and evaluation

Read `research/R267/R267_EXACT_RESULTS.json` and its nine frozen world PMFs. Both designs use exactly three evaluations. IID has 729 equiprobable primitive triples per world, LHS has 36 equiprobable paired permutations per world. True mean is the nine-cell uniform grid mean. All probabilities and calculations use exact rational arithmetic.

For each of 18 world/design pairs, compute `P(|estimate - true_mean| > 1/3)`, `P(|estimate - true_mean| > 2/3)`, `E|estimate - true_mean|`, and `max |estimate - true_mean|`. Strict greater-than is mandatory. Save all 18 rows, their 36 tail-event probabilities, and the complete comparison of LHS vs IID for each tolerance. For the 9 paired worlds, report how ranking of tail risk depends on tolerance. Do not select new thresholds after reading results. Preserve all ties and fractions. Original R267 variance remains an external frozen baseline and is not re-estimated as a new scientific finding.

## Two routes and checks

R route: use the archived R267 full PMFs, recompute probability mass, exact means, and frozen variances, then calculate the new metrics.

B route: write an independent implementation of the nine frozen integrands and reconstruct all 18 estimator PMFs from primitive IID triples and paired permutations without importing R route PMF or code. Compare every new field with R route persisted receipt. Reject duplicate/missing world/design rows, type substitutions (bool for integer), altered probabilities, evidence-level upgrades, and wrong thresholds. State any non-blind knowledge of original R267 report.

Report only what is actually executed. A successful script is internal programmatic agreement, not external independent replication. No E2 or E3 data, no new historical acceptance, no modification of R073 or PESEN v0.1. Avoid CI unless confirmed free. Do not overwrite existing files or edit original R267 artifacts.