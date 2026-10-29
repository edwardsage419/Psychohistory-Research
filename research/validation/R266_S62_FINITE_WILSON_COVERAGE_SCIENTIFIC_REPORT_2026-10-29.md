# R266 S62: exact finite Wilson score coverage under antithetic dependence

Date: 2026-10-29 UTC. Evidence grade: E1, exhaustive artificial probability space only. Target key: (r,R266,S62,finite-score-coverage-and-naive-independence).

## Protocol and original source identity

New protocol was frozen first in commit `6cdc35c36bdf6d2f06761dff5b04a8af8aa1bd8b`. Original R266 had already been read; this is a prespecified *new* score-coverage metric, not a blind replication. Original nine worlds, IID/ANTITHETIC designs, 5,328 source atoms and R266 acceptance are unchanged. The input source Git blob observed is `53a808994300f85826a18723146fdb2fea7c6db2`, original result Git blob `ec307a45a361d202cae074a45cea5406b2a8e28e`.

The independent offline Python source regeneration produced exactly 5,328 rows, 419,791 bytes and SHA256 `5e0aac41c960ee21b54d3266064793a7e9a2454dbb4493ae8e4451591d48587a`, identical to the historical R266 machine receipt. The archived new R JavaScript parser was evaluated in a V8 environment against the full GitHub-fetched CSV and original result JSON. Native Node CLI invocation of the archived program remains NOT_RUN.

## Exact frozen score metric

The two-sided Wilson score interval is tested at z=2 via the exact inclusion inequality `n*(p_hat-p)^2 <= 4*p*(1-p)`. For each of 18 design combinations, the complete source space is enumerated and its true probability mass aggregated. This evaluates coverage of an interval calculated under an IID assumption, while the actual antithetic design has dependent pairs. The normal-reference nominal level is approximately 95.45%; finite actual coverage is calculated exactly rather than assumed.

Selected results:

| Frozen world | IID exact coverage | Antithetic exact coverage | IID E[naive variance] / actual variance | Antithetic ratio |
| --- | ---: | ---: | ---: | ---: |
| THRESHOLD_Q1_N2 | 15/16 | 1 | 1/2 | 1 |
| THRESHOLD_Q1_N4 | 243/256 | 1 | 3/4 | 5/4 |
| THRESHOLD_HALF_N2 | 1 | 1 | 1/2 | undefined, actual variance 0 |
| THRESHOLD_HALF_N4 | 1 | 1 | 3/4 | undefined, actual variance 0 |
| THRESHOLD_Q3_N2 | 15/16 | 1 | 1/2 | 1 |
| THRESHOLD_Q3_N4 | 243/256 | 1 | 3/4 | 5/4 |
| SYMMETRIC_EXTREMES_N2 | 1 | 1 | 1/2 | 0 |
| SYMMETRIC_EXTREMES_N4 | 1 | 1 | 3/4 | 1/4 |
| SYMMETRIC_EXTREMES_N6 | 31/32 | 3/4 | 5/6 | 1/3 |

The key frozen counterexample is SYMMETRIC_EXTREMES_N6: with six equal-cost function evaluations, treating antithetic outputs as six independent Bernoulli observations yields exact Wilson score coverage of 3/4. The IID design achieves 31/32. The antithetic design's expected naive plug-in variance is 1/36, while its true estimator variance is 1/12, a factor of three difference. This is a precise conditional failure of the independence assumption, not an observed real-world calibration result.

The antithetic THRESHOLD_HALF estimator has exactly zero true variance but positive IID plug-in variance. Its ratio is deliberately null rather than infinity or zero. The two Q1/Q3 designs have improved score coverage under antithetic pairing in the frozen finite worlds; no universal ranking is claimed.

## Execution, B verification, and limits

R source: `research/validation/r266_s62_score_coverage.js`.
Machine result: `research/validation/R266_S62_EXACT_SCORE_COVERAGE_RECEIPT_2026-10-29.json`.
B independent four-point success-count convolution: `research/evidence_audit/r266_s62_independent_convolution_gate.js`.
Independent original-source regeneration: `research/evidence_audit/r266_s62_original_source_sha_rebuild.py`.

The independent B route never calls the R source-row parser; it reconstructs the complete count PMF by convolution of primitive four-state outcomes. All 18 combinations and 180 receipt fields matched, with zero differences. Five mutations (wrong coverage, missing row, duplicate row, evidence upgrade, boolean in numeric field) were rejected. The B reviewer had read R266 and the new R output, so this is NONBLIND INTERNAL method checking, not external independent replication.

Scope limitations: no empirical random-number draws, no confidence calibration on held-out human observations, no data leakage or independent-session test applicable to this artificial enumeration. A source hash match and 180 equal fields establish bounded mathematical and archive evidence, not empirical validity. Original R266 formal acceptance is unchanged. New E2=0, E3=0; R073 and PESEN v0.1 remain frozen. New GitHub Actions were not triggered. Node native CLI and independent external review remain open.
