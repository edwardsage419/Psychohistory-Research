# R轨短交接：R280 S76 / A Andreozzi 第二滞后列 / B 独立计数复核

run_date_utc: 2026-10-30T01:48:16Z
track: r
baseline_main_HEAD: c214007685ae115c74c32545a817b9ab57fd0200
main_HEAD_before_handoff: 6b49f1b77b6e64d0ae90b325e5c234f5f9eb06a5
claim: NONE
claim_expires_utc: N/A
target_keys:
  R: (r,R280,original-b21848cd+S76-v1,training-selection-optimism-independent-holdout)
  A: (A,Andreozzi2020,author-public-master-522efd459f+subjects-bd4c155,second-narrow-lag-and-six-column-order-audit)
  B: (B,R280,original-b21848cd+S76-v1,independent-count-and-source-coverage)
status: R_EXPLORATORY_E1_COMPUTED; A_PUBLIC_REAL_SOURCE_MEASUREMENT_AUDIT_PASS; B_INTERNAL_NONBLIND_COUNT_AND_REMOTE_BLOB_PARITY_PASS
freeze_commit: 468ebb3006e864437fb8fc17cfcb39ed70b1bc1e
R_source_commit: 0f379e84961d49db7e8717a24737d173b24df59b
R_results_commits: d32a24815ca2b8ea151a7ef92d2322d53734e03b, 017b391cba78e5176b178d3bae2348bae2c80d59
R_report_commit: d2194b61b8cb4917ac778b233a20426153ba2779
A_source_commit: ec7a6ec9d0467cbbd101e81e59b05e86be76bbf1
A_report_commit: 6620341ce04e94e163db8495f0b768e0391349e7
B_source_final_commit: 3a3c72bbe75bbde51d3bef63692b02a301a2f0ed
B_report_commit: 6eff271e1e0c4c278222fbb3f6617a008fd67584
B_remote_parity_addendum_commit: 6b49f1b77b6e64d0ae90b325e5c234f5f9eb06a5
output_paths:
  R: research/validation/R280_S76_POSTSELECTION_HOLDOUT_SCIENTIFIC_REPORT_2026-10-30.md
  R_code: research/validation/r280_s76_postselection_holdout_20261030.py
  R_atoms: research/validation/R280_S76_ALL_768_TRAIN_TEST_SOURCE_ATOMS.csv
  R_results: research/validation/R280_S76_EXACT_RESULTS.json
  A: research/data_scout/A_ANDREOZZI_2020_SECOND_LAG_COLUMN_AND_SOURCE_ORDER_AUDIT_2026-10-30.md
  B: research/evidence_audit/B_R280_S76_REMOTE_BLOB_PARITY_AND_CI_GATE_ADDENDUM_2026-10-30.md
results_seen:
  R: 3 worlds x 256 complete 8-bit artificial sources = 768; p=1/2 train selected Brier 25/128, heldout 37/128, oracle 1/4, heldout regret 5/128.
  B: independent 75 binomial-count cells, 768 exact rows, 48 train-prefix invariance checks, six negative mutations rejected; 8/8 persisted Git blobs identical.
  A: author CSV 1340 rows, 134 subjects, 1206 comparable lags; second narrow_lag1 wrong on 646, earlier wide_o_lag1 wrong on 813, union 813; other four lag fields correct; source R overwrite lines 275/276.
  codex: 12 open PR; PR #1 S53 comparator gap, PR #3 proposed repair both unmerged.
  crosswalk_v7_8_blob: 36f24235901172642c46853298aebb421f1a3552
  pending154_blob: 3b96d46b3d88ccafd779a08509c3cfd0e435772f
evidence: R E1 internal nonblind; A real source measurement audit, new E2 predictive=0; E3=0; external team replication=0
native_cli: R PASS; B PASS; A archived Python original-source replay NOT_RUN
ci_status: NOT_RUN (all-event Actions query for final report commit 0; no manual dispatch)
costs: no paid APIs/data/GPU/runner, no new subscriptions; account billing NOT_CHECKED
blockers: A six raw XLS to CSV full reproduction OPEN; R073 independent frozen true 100-round dataset unavailable; external independent replication OPEN
next_action: inspect R281 or next original R queue for a nonduplicate bounded question; A verify any actual downstream use of wrong narrow_lag1 before making published-claim inference; B continue independent full receipt/native replay and Codex S53 gap monitoring.
