# R127 CI log verification and frozen-protocol row-level supplement

Date: 2026-10-24. Original239 item 05-003. Research evidence: bounded constructed E1.

## Preflight and independent verification

Main HEAD before write: `32ad06825f2dccebd1d39f55c70dfb69fd44c32d`. Repository public and push permission confirmed. Frozen R127 protocol and original CSV were read unchanged. Original source Git blob `6964fa57e291e719e8cc071cc3a70d73836363e4`. Original CSV Git blob `2a6706dcb047a5bf64f91651a8217d1d8009aa2c`, SHA256 `821f785bf21a96eae5b65d1200389a5a2baa45ad63e5a115e48505051a2e9df4`.

GitHub Actions **run 40099180033**, event push, head commit `d58f71bceacc08fba2ae8b0ce478dc51e54900e3`, completed / success. Jobs **120887604350** (Python 3.11) and **120887604624** (Python 3.12) both completed / success. Their actual logs independently confirm 2793 effort profiles, 10731 person-payoff comparisons against unchanged R127 source, 399 opponent profiles, 2793 candidate deviations, two tamper controls, four positive controls, original source blob and original raw SHA256. Each job reran **60 unchanged original tests: OK**.

## Frozen protocol archive discrepancy and supplement

The frozen protocol requires each archived profile row to include an exact comparison flag. The original 2793-row CSV has no such column. This is retained as a documented historical archive discrepancy. A **new** supplementary CSV now contains the four original fields plus `exact_comparison_flag` for every original row. Original CSV and protocol are preserved byte-for-byte.

The supplementary CSV was generated after inspecting the successful CI logs and independently re-enumerating all 2793 finite profiles in JavaScript, comparing every original raw row and 10731 integer payoff numerators. Every supplementary flag is `PASS`, inferred from the **earlier CI verifier's exhaustive original-source comparisons** together with this independent raw replay. The supplementary receipt was **not itself executed as a new CI job**. The accompanying Python `verify_r127_row_flags_supplement.py` is a future reproducibility tool that rechecks the unchanged original source, source blob, original CSV hash, every profile and the supplemental receipt; its execution in GitHub CI is still unverified.

The two provenance levels must remain separate: (1) previous original-source comparisons are CI verified; (2) new row-level archive is a post hoc derived receipt, not prospectively frozen primary raw output. This repairs inspectability of row-level flags without retroactively claiming that the original archived CSV met its frozen schema.

## Scientific decision and scope

The mathematical conclusion for the frozen finite n=2,3,4 and effort grid 1..7 is supported: original source agrees with independent integer payoff enumeration, and all 399 opponent configurations have unique best response at the opponents' minimum. The original paper's 107 participants remain published aggregate counts. No newly scored individual-level human data, calibration, holdout sessions, resampling CI, external-team replication or historical E3.

**Verdict: PASS_BOUNDED_INTERNAL_INTEGER_TENT_BEST_RESPONSE_E1, with an explicit retrospective archive supplement and no new CI for that supplement.** No claim of unqualified protocol conformity. Do not automatically decrement the catalogue queue.

## Catalogue concurrency caveat

Two distinct original239 tracking series coexist in main: the itemwise v7.6 queue of 157 provisional README links, and the separate v5.0 research-primary overlay recording 224 primary R, 3 shared math and 12 pending. Their `pending` numbers measure different gates and must not be subtracted or combined. Neither shared index nor either queue is modified in this commit. Any reconciliation requires a scoped crosswalk review before a new global count.

Frozen R073 and PESEN v0.1 remain unchanged. New E2=0, new E3=0. No paid resource was used; no new GitHub Actions run was requested.
