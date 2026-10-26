# R178 third method: Wilson score coverage under artificial within group dependence

Date 2026-10-26. Protocol frozen in commit `8712c87d8af4800f19be7acc9ccc6b7985a74043` before this calculation. Frozen source `research/R178/R178_EXACT_RESULTS.json` Git blob `3b4a5abeaa14b5be32fb258a15aa6bf502b2756c`.

## Research design

For each of the original 30 artificial finite count worlds, compute exact coverage for the conventional two sided Wilson score interval at fixed z=1.96. Wilson inclusion condition is `n*(k/n-p)^2 <= (49/25)^2*p*(1-p)`. The existing Wald interval inclusion condition is `(k/n-p)^2 <= (49/25)^2*(k/n)*(1-k/n)/n`. All 270 source probability cells and original 30 Wald coverage values are checked using exact rational arithmetic. The original model, generating parameters, MLE and R178 acceptance are unchanged.

## Actual results

Wilson coverage strictly improves in **19** worlds, ties in **10**, and worsens in **1**. Wilson coverage is below the nominal 95% level in **27** of 30 worlds; Wald is below in **30** of 30. These 30 related artificial worlds do not represent independent empirical replications.

For fixed n=8 and p=1/4:

| Generating mechanism | Wald actual coverage | Wilson actual coverage | Wilson minus Wald |
| :--- | ---: | ---: | ---: |
| IID_BIN | 87.26% | 97.27% | 10.01 pp |
| CLUSTERED_BB_C2 | 46.55% | 83.65% | 37.09 pp |
| CLUSTERED_BB_C8 | 71.61% | 91.61% | 20.00 pp |
| INACTIVE_ZIB_Z1_8 | 77.41% | 95.84% | 18.43 pp |
| INACTIVE_ZIB_Z1_4 | 65.48% | 93.40% | 27.93 pp |

Wilson score inversion can include boundary counts that Wald excludes. This increases exact coverage in some finite samples. Both intervals use the IID working assumption; correlated or structurally zero inflated worlds can still have substantial undercoverage. These calculations do not establish a uniformly valid confidence interval under unknown dependence.

## Independent verification and limitations

The B audit separately uses integer cross multiplication and complementary excluded probability mass. It checks 540 interval membership decisions, 60 world level exact coverages, and reproduces all original Wald coverages, with 0 mismatches. The predeclared z=1 negative control changes 60 Wilson cell decisions. The second method is internal procedural verification on the same archived E1 source.

Artifacts: `research/validation/r178_wilson_exact_20261026.js`, `research/validation/R178_WILSON_SCORE_COVERAGE_EXACT_RECEIPT_2026-10-26.json`, `research/evidence_audit/r178_b_score_integer_20261026.js`, `research/evidence_audit/B_R178_WILSON_SCORE_INDEPENDENT_RECEIPT_2026-10-26.json`. No additional real human E2 score, historical E3 forecast or external replication. R073 and PESEN v0.1 remain frozen. This is a bounded post acceptance E1 diagnostic; the R178 formal original E1 acceptance remains unchanged.
