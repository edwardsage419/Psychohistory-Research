# B R172 independent exact arithmetic and country-grouping audit

Date 2026-10-26 Asia/Singapore. Status PASS_BOUNDED_INTERNAL_ARITHMETIC_AUDIT; external independent replication=NO. B prescore method freeze [here](B_R172_COUNTRY_DELETION_EXACT_BRIER_PRESCORE_FREEZE_2026-10-26.md), commit b372d95b7d370c43298052ec9fd47bc182e8d0db, predates new R172 third-method numerical execution. This is implementation-path independence inside the same research project; the original 2026-10-21 R172 results and data were already visible.

B uses the same 319-row heldout CSV Git blob 00d0379d77ec8e776a00cbb9c6e9dd5a00958dce, separately parsed. Archived executable [B JS](r172_b_exact_country_deletion_20261026.js) uses BigInt numerator/denominator arithmetic with GCD reduction to compute each Bernoulli Brier squared error **exactly** from the original fraction strings. Main R uses floating arithmetic and direct per-country filtering. B derives country deletions by subtracting exact rational country sums from exact global sums, then separately verifies direct retained-row summation.

## Actual execution and evidence

* Recomputed 319 years, 35 regime episodes, 32 country IDs, 18 breakdown events; all event/ID/year checks passed.
* Exact full-sample Brier values converted to decimal: M0 **0.05440711323504093**, M1 **0.05466702789383365**, M2 **0.054105271592529286**. They match the original R172 published Brier values within 1e-10.
* All 32 country deletions times three model Brier sums, **96/96 exact BigInt equalities**, matched subtraction route to independently filtered direct route. For 32 countries times two model-minus-M0 contrasts, **64/64 cross-route comparisons** matched main floating code, maximum absolute difference **1.14e-17**.
* Nine fixed-bin membership and event-count cross-checks, **9/9 exact counts matched** main code. The observed 18 breakdowns exceed every model's 6.32 to 7.58 expected events; no recalibration was performed.
* Three countries, MRT, NER and SLB, each have two different heldout episodes. Their repeated country identities establish a dependence issue for the older episode-only bootstrap. The original training/test country overlap was disclosed by R172 but has not been independently reverified from full training source in this B run.
* Mutation negative control 1: reassign first row's country to new sentinel. The full-data Brier is invariant and country partition changes from 32 to 33. PASS.
* Mutation negative control 2: replace first row's M2 probability by 1/2; the exact squared-error total changes. PASS.
* Machine receipt [B_R172_EXACT_COUNTRY_DELETION_RECEIPT_2026-10-26.json](B_R172_EXACT_COUNTRY_DELETION_RECEIPT_2026-10-26.json) includes full 32-country Brier deletion table, fixed-bin counts, rational numerator/denominator modular signatures, code/input blob identities, all checks and negative controls.

## Scientific audit gates

**Data leakage**: no new fitted parameters, training refit, test-dependent cutoffs or feature engineering occurred in this third method. Original R172 cutoff and episode split were read from its existing frozen protocol. This audit does not establish true historical contemporaneous availability of libdem0, and it does not independently rerun the original raw-data training split.

**Baseline**: M0 retained, M1 retained despite worse predictive score, M2 advantage very small. No posthoc model elimination.

**Out-of-sample**: new R172 third-method analysis reuses the same 319 historically heldout years, 35 episodes and 32 countries. No new independent sample, and countries may overlap original training.

**Calibration**: all models substantially underpredict observed event counts in this retrospective test. Fixed bins contain zero predictions >=0.05. This is a source-specific descriptive warning, not a calibration-corrected forecast.

**Uncertainty**: country-cluster resampling in main R is more aligned with repeated country episodes than original episode bootstrap, yet common time shocks and cross-country dependence remain unmodeled. All four country-bootstrap loss-difference intervals include zero. No claim of statistical significance.

**Negative controls**: both independent B mutations actually executed, alongside main R's two mutations. Their expected direction was fixed before execution.

**Evidence classification**: original R172 is a bounded authentic historical retrospective test. New analysis is an internal audit on the same data. It adds no new prospective E3, no new E2 human behavioral experiment, no external team reproduction. R073 and PESEN v0.1 remain frozen. Original239 queue unchanged.

## Reproduction, CI and cost

`node research/evidence_audit/r172_b_exact_country_deletion_20261026.js research/R172/R172_REAL_HELDOUT_PREDICTIONS.csv`. Requires no paid packages. Actual execution was performed using the archived source through V8 against the GitHub-fetched CSV, and compared directly to the archived R source. GitHub Actions was **not** launched; remote CI for these new files is **NOT_RUN**. No new expense; billing and free runner allowance were not independently verified.