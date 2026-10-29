# R轨交接：R277 S73 时间下采样与A/B验证
run_date_utc: 2026-10-29T22:44:49Z
track: r
subflows: R-main, A-data-scout, B-evidence-audit
observed_main_HEAD_before: fd35be5c4c30f90f27e944028c80ea4a3d39777a
verified_main_HEAD_before_handoff: ca6c08c4dcc57590b3e559bbea14df1e566a12be
target_keys:
  R: (r,R277,53e3b18b28d46c0c5e26194dd8e85bc408450af6,three-observation-temporal-subsampling-aliasing)
  A: (A,Andreozzi2020,author-979abf87,session-heldout-vs-row-split-leakage)
  B: (B,R277,S73-freeze-53e3b18b,independent-kernel-and-receipt-check)
activity: completed_bounded
status: COMPLETE (R exact E1 exploratory; A source structure gate), PARTIAL (B native Node and external replication)
claim: NONE
claimed_at_utc: null
expires_at_utc: null
freeze_commit: 53e3b18b28d46c0c5e26194dd8e85bc408450af6
result_commit: af9e01a411cdf98cc683fb3c90518f698c7fdd37
B_script_commit: af63730cfcad2ee32cafd7cecce5528e5ce80c50
A_report_commit: 59ff89b53a8c529ae77a995174a542044e06f30f
B_report_commit: 00531cc724d352bf14860d94688c66442fa929b0
R_report_commit: ca6c08c4dcc57590b3e559bbea14df1e566a12be
output_paths:
  R: research/validation/R277_S73_TEMPORAL_SUBSAMPLING_IDENTIFIABILITY_SCIENTIFIC_REPORT_2026-10-30.md
  R_source: research/validation/r277_s73_temporal_subsampling_20261030.js
  R_CSV: research/validation/R277_S73_OBSERVED_TRIPLETS_72_ROWS_2026-10-30.csv
  R_JSON: research/validation/R277_S73_EXACT_RESULTS_2026-10-30.json
  A: research/data_scout/A_ANDREOZZI_2020_SESSION_SPLIT_AND_SUBJECT_LEAKAGE_GATE_2026-10-30.md
  B: research/evidence_audit/B_R277_S73_NONBLIND_TRANSITION_KERNEL_AND_RECEIPT_AUDIT_2026-10-30.md
  B_script: research/evidence_audit/b_r277_s73_transition_kernel_receipt_audit_20261030.js
results_seen:
  R: 192 original artificial sixbit configurations, 72 observed probabilities; adjacent macro 13/24 and anti/persistent TV1/2; alternate macro 73/192 and TV0.
  A: 134 people in 6 sessions (3 each treatment), 1340 rows; deterministic row-level split 1072/268 shares all 134 people, unsuitable temporal holdout.
  B: remote V8 R source reproduces complete CSV/JSON; independent analytic 72 probabilities, 27 confusion, 9 TV, 72 CSV; 8 mutations rejected.
  PR: 12 open Codex PRs, PR1 R257 S53 comparator gap and PR3 strict candidate remain unmerged.
original239_v7_8_blob: 36f24235901172642c46853298aebb421f1a3552
original239_pending154_blob: 3b96d46b3d88ccafd779a08509c3cfd0e435772f
CI: NOT_TRIGGERED (latest commit combined statuses 0, PR-filtered workflow runs 0; full Actions enumeration unavailable)
billing_checked: NO, free Actions quota unknown
cost: no new paid operations
evidence_scope: exploratory E1 nonblind internal; A E2 data provenance only, new E2 predictions 0, E3 0, external team replication 0
blockers: native Node CLI against persisted artifacts NOT_RUN; full original raw-to-cleaned Andreozzi pipeline NOT_RUN; source-specific statistical independence NOT_ESTABLISHED
next_action: check latest HEAD, open Codex PRs and coordination; prioritize complementary R278 joint model averaging predictive dependence; B native Node CLI, A independent session-level E2 protocol preparation if eligible; preserve R073 and PESEN v0.1 frozen.
