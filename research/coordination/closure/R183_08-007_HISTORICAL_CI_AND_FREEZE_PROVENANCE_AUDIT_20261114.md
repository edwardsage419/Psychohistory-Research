# R183 / 08-007: historical CI and prescore provenance read-only audit

Date: 2026-11-14. Track: closure. Observed main HEAD before audit: `a34343bcdf6812b305d064761ce1cf4baa50a511`.

## Direct GitHub API observations

* `GET /repos/edwardsage419/Psychohistory-Research/actions/runs/39561106676` returned `status=completed`, `conclusion=success`, `event=push`, `head_sha=265c0ef694ec534a12c862d5033f948e3e183d9c`, `created_at=2026-10-21T07:18:53Z`.
* `GET /actions/runs/39561106676/jobs` returned `total_count=3`; Python 3.11 and 3.12 logistic score/separation test jobs both `completed/success`; full-source-enumeration-and-permanent-archive job also `completed/success`. Their named verification, enumeration, artifact upload, and permanent publication steps all reported success. This confirms the historical GitHub CI metadata, not an independent execution of the tests or an examination of job logs.
* `GET /commits/28623c4e53834a4572a69e563c1eb05426b37e88` confirms that the prescore freeze commit changed only `protocols/R183_LOGISTIC_SEPARATION_45_WORLDS_PRESCORE_FREEZE_2026-10-21.md`. Current protocol blob is `e01003e1899739b42b2ed746f1837b8591e870b6`. Protocol declares R177 source code Git blob `2d032513ce84141214b6b3f84df9c0ed9976a02b` and R177 JSON SHA256 `57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535`.
* `GET /commits/977743d70ef674ec7e3bb3b77b9f908aab6d74bd` confirms parent `265c0ef694ec534a12c862d5033f948e3e183d9c` (the successful CI run's head SHA) and four added R183 artifacts: 4125-row CSV, exact results JSON, final machine acceptance JSON, and ZIP. Thus the archived result commit is directly descended from the CI-tested head; the artifacts themselves were added in the subsequent commit. The CI success cannot by itself attest to byte identity of those four newly committed artifacts.
* At observed main, the R177 Python blob is `2d032513ce84141214b6b3f84df9c0ed9976a02b`, matching the frozen Git blob reference. R177 JSON Git blob is `8a8819e4d85989b518b9152cfc98336457c76a9c`; its SHA256 has not been independently recomputed here. R183 Python source blob is `d3aba985f8f7c7de21ca12f318f73abaa7fb3b0d`. Static inspection finds an explicit SHA256 check of the R177 JSON and source blob verification, but this audit did not execute the script.
* Current `R183_FINAL_MACHINE_ACCEPTANCE.json` blob `145f71b55046985835ff92b53ad66ca799cb14cf` reports CSV SHA256 `1dcd2a85c2b241346e8fae8fe85727e2b8c0560fa2916c1e8ce01eb384acf285` and result JSON SHA256 `40927bae4616a9d9fc91ed964257a9d436372d9196abd8fabceb40740189a000`. These remain self-reported hashes pending independent byte verification.

## Scope and scientific disposition

**PARTIAL: independent historical CI metadata and Git ancestry verification.** This closes the specific uncertainty whether run 39561106676 actually existed and reported three successful jobs, and establishes the CI-head to publication-commit ancestry. It does not prove that the four subsequently committed artifacts are byte-identical to CI outputs. The prior independent 45-world arithmetic audit is a separate E1 evidence item; no repeated numeric work is claimed here.

Research status remains `CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_LOGISTIC`; catalogue 08-007 remains provisional/ACTIVE pending itemwise decision. New E2=0, E3=0, catalogue closures=0. No frozen protocol edit, R-core edit, PR merge, new CI invocation, or paid resource.

Next independent checks: recompute SHA256 over the raw R177 JSON, R183 CSV and results JSON; execute the frozen native R183 script and compare the resulting 4125 rows and numeric logloss against the committed artifacts. Check historical CI job logs or artifact manifest if available, then apply the existing itemwise closure standard. Do not infer E2/E3 or catalogue closure from CI success.
