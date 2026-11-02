# R257 S53: independent geometric face oracle, nonblind bounded reaudit

track: R/B
run_date_utc: 2026-11-02
report_local_date: 2026-11-03 Asia/Singapore
target_key: (R/B,R257_S53,2026-10-29 prescore freeze,mathematical receipt correctness)
baseline_main: 769e3fd87af5e5226e9c0942b3efac83031a6612
head_before_report_write: 5b976d64b4dab64ae1bdfd4f63377e4ef5d65e30
status: COMPLETE_BOUNDED_NONBLIND_GEOMETRIC_REAUDIT / PRODUCTION_P0_OPEN
evidence: INTERNAL_NONBLIND_ARTIFICIAL_E1
new_E2: 0
new_E3: 0
external_replication: NOT_RUN
historical_blind_order: FAIL_UNCHANGED
full_scientific_acceptance: PARTIAL
ci: NOT_RUN
billing_checked: NOT_VERIFIED
new_paid_operations: 0

## Target and source identities

Read the actual main branch, original239 crosswalk v7.8 and itemwise queue, R257 S53 frozen protocol, archived S53 JSON, the open Codex PR #1/#3 and their audit source. The original239 queue remains 154 rows (P0 27, P1 82, P2 45), unchanged. Codex PR #3 remains an unmerged candidate; this audit is a complementary algorithm, with no edits to Codex-owned files.

* Frozen protocol: `protocols/R257_S53_CAPACITY_SHADOW_PRICE_PRESCORE_FREEZE_2026-10-29.md`, Git blob `2060b7423fed97dcd62f7a53aebea5220b969d2b`.
* Historical receipt: `research/validation/R257_S53_EXACT_RECEIPT_2026-10-29.json`, Git blob `37f33083b45435e18c66641ef693c6f0c779a680`.
* Unmerged PR #3 comparator: `research/codex_audit/r257_s53_validator/validate_receipt.py`, Git blob `75c0870c49c26f175ab678a7600ae4d4b8a5c7f2` at PR head `97d5f74df5d84916917db943156120f08144f445`.
* New independent script: `research/validation/r257_s53_geometric_face_oracle_20261103.js`, Git blob `7a04a2df3b340aa3689efbfd786e561b37dd01df`.
* New machine receipt: `research/validation/R257_S53_GEOMETRIC_ORACLE_RECEIPT_20261103.json`.

## Independent method and executed scope

A new exact BigInt rational algorithm minimizes the squared distance to each of the three edges of the feasible triangle `x>=0, y>=0, x+y<=C`, and also considers the unconstrained target when feasible. For the slanted edge it uses `x=clip((a-b+C)/2,0,C)`, `y=C-x`; the two coordinate edges are projected separately. The smallest of these candidate objective values is the global minimum by convexity. This route neither imports the R257 optimizer nor uses Codex's KKT-certificate algorithm.

For all eight frozen strictly convex worlds, it independently solves five capacities each, then compares exact points, minima, capacities, baseline values, secants, and the derivative. The derivative is independently obtained from the exact symmetric quotient at `epsilon=1/4096`. The eight frozen baseline capacities lie in stable active-face neighborhoods. The ninth nonconvex control is excluded from convex sufficiency claims; only its archived label is checked.

Actual execution of the **exact remotely re-fetched new source** used isolated JavaScript V8 with a mocked read-only `node:fs.readFileSync` returning the authentic archived JSON. This avoids falsely claiming a native Node execution of the original receipt in a full checkout. An analogous geometric script's twelve closed-form controls were also executed under local Node 22.16.0. Random seed: N/A.

| Exact comparison category | PASS |
| --- | ---: |
| Eight unique world identities | 8 |
| Two optimal coordinates for each of 40 scenarios | 80 |
| Baseline and perturbed capacities | 48 |
| Forty minima plus eight baseline values | 48 |
| Eight local derivatives and eight multipliers | 16 |
| Thirty-two one-sided secants | 32 |
| **Total** | **232** |

All 232 exact comparisons agree with the historical receipt, zero discrepancies. Baseline derivatives by frozen world order: `0, -1/2, 0, 0, 0, -2, -2, 0`. The off-grid world's `C=3/4` optimum is `(23/40,7/40)`, objective `1/800`; its baseline at `C=1` is `(3/5,1/5)`, objective zero. These two points provide a direct check of the active-face transition.

The same exact remotely re-fetched source passed its twelve closed-form selftest controls. Seven modified copies of the real JSON were separately tested: duplicate worlds, altered minimum, altered coordinate, altered derivative, altered secant, changed E1 label, and corrupted delta identity. All seven were rejected with a nonzero exit and specific reason. A first attempt to execute the source in V8 without removing its Node hashbang failed at parsing; the harness was corrected to remove only the shebang, then the authentic positive, selftest and all seven negatives were rerun. The initial harness failure is not a scientific comparator failure.

## Limits and disposition

This independently supports the finite convex quadratic **numeric** claims. It does not restore the frozen requirement to compute B before viewing R. The historical blind-order failure remains explicitly FAIL. PR #3's source authentication remains NOT_RUN, its new validator remains unmerged, and the old B false-acceptance risk on main remains OPEN. The frozen protocol also asks for a nonconvex negative control; this increment checks only its receipt label and does not replay its original 225 candidate atoms. There are no human predictions, historical forecasts, external teams, or new scientific acceptance.

The Node CLI on an authentic full checkout, complete original source identity audit, original R/B replay and CI were NOT_RUN. Network-based `git clone` from the container failed DNS resolution of github.com; the connected GitHub read/write path remained available. No workflow dispatch, paid API, new subscription or paid compute was requested. Account billing and Actions free quota remain unverified.

## A data scout

Checked current English CRAN stratEst documentation and author tutorial for DF2011. The published package documentation reports 7,358 repeated-game observations, `treatment,id,game,period,choice,other.choice`; its transformed `data.DF2011` adds a previous-action `input` field. The author tutorial constructs that field with `input.lag=1`. These materials do not independently establish experimental session IDs, matching pairs, or original author licensing for R073's frozen session-level holdout. The previously known DF2011 candidate therefore remains unqualified for frozen R073 scoring. New qualified datasets=0; actual download/row-level scoring this run=NOT_RUN.

Sources:
* https://rdrr.io/cran/stratEst/man/data.DF2011.html
* https://fdvorak.com/stratEst/
* https://github.com/edwardsage419/Psychohistory-Research/pull/1
* https://github.com/edwardsage419/Psychohistory-Research/pull/3

## Next priority

1. On a trustworthy full checkout, run the existing R272 single-entrypoint preimage-first candidate with real archived files, all three Python modes and native negatives. Review frozen three-job compatibility before production adoption.
2. Independently assess the unmerged PR #3's strict receipt checker and input provenance; preserve the original R257 S53 blind-order FAIL.
3. Advance original239 itemwise closure only after source and governance adjudication; do not infer closure from this E1 mathematical consistency.

R073 and PESEN v0.1 remain frozen. No model classification, fusion, or personal decision product work.
