# R117 original239 03-009 bounded independent method re-audit

Date 2026-10-24. Frozen protocol commit `772c2185dca3e57726f0fee5b7e0abba3bd3105d`. Existing R117 source blob `023d8302853e0256f08e362b36a16a808004e999` and test blob `3e35f31c80323ee328bf2cbbb10d5ee420f69e38` were reused without modification.

Primary published sources: Cialdini, Reno and Kallgren 1990 DOI 10.1037/0022-3514.58.6.1015; Schultz et al. 2007 DOI 10.1111/j.1467-9280.2007.01917.x. The source numbers were transcribed in the existing R117 archive from the published Figure 1 and household group means; this audit independently recomputes their arithmetic, not a new reading of raw subjects or household time series.

1990 Figure 1 group sizes (31,50,24,34) sum to 139. Printed whole percentages (6,14,54,32) each admit exactly one integer success count under half-up rounding: (2,7,13,11). Rounded percentage contrasts are -8 and +22 percentage points; rounded difference in differences is +30 pp. Exact count-derived contrast is `92843/316200`, approximately 29.3621 pp. Treating +30 pp as an exact individual-level contrast would introduce rounding error. Original statistical significance was not re-estimated.

2007 four published group sizes (64,79,63,81) sum to 287, consistent with 290 initial households minus three withdrawals. Published mean short-term differences in daily kWh are -1.22, +0.89, -1.72, +0.24. These are differences of published rounded group means, with no paired variance or original meter time series. The +0.24 value was reported by authors as not significant; the independent audit cannot estimate its uncertainty.

Separate project-created focus toy with D=1/5 and I=9/10 yielded four exact probabilities 1/2, 7/20, 7/10, 11/20; equal cues D=I=4/5 yield 13/20 under either single focus. Both deliberate corruptions were detected.

GitHub Actions run `40075340202`, Python 3.11 and 3.12 jobs `120817361102` and `120817360876`, completed success. Original source/test SHA256 checked in both jobs. Independent audit and original 39 tests passed on each Python version. CI receipt: `research/validation/R117_INDEPENDENT_AGGREGATES_FOCUS_CI_RECEIPT_2026-10-24.json`.

**Acceptance: PASS_BOUNDED_INTERNAL_AGGREGATE_AND_SYNTHETIC_E1**. Published human aggregates are genuine external source summaries, but this project did not score original individual humans, estimate causal effects, compute held-out predictions, calibrate a model, bootstrap clusters, or independently replicate either field experiment. New E2=0, E3=0, external independent replication=false. Early ZIP strict reuse remains open. R073 and PESEN v0.1 remain frozen. Catalogue association is evidence provenance, not validation of the complete social norms theory family.
