# R-track bounded handoff 2026-10-30T09:51:35Z
track: r
baseline_main_head: e97dce249dd11bed4b4fa65c2671679665c80f7f
observed_main_head_before_handoff: 74ac4e047ca1e5bd07e372afd7c0649e8af02dbf
target_keys:
  R: (r,R288,original-2026-10-23-freeze,S84-six-draw-sign-error)
  A: (A,Pereda2019,Zenodo-2590686-v1,public-CSV-schema-and-independence-gate)
  B: (B,R288,S84-v1,exact-six-draw-sign-error)
claim: NONE; no lease or atomic lock
state: BOUNDED_INCREMENT_ARCHIVED; R288_S84_SCIENTIFIC_ACCEPTANCE=PARTIAL
read_scope: main latest commits, 12 open Codex PR summaries, R288 original freeze/report/source/result/acceptance, R287 S83 prior handoff, original239 v7.8 crosswalk blob 36f24235901172642c46853298aebb421f1a3552, pending154 queue blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f, acceptance standard v1, project sync policy, other-track handoff names. Codex PR #1 and #3 remain unmerged; PR #2 protocol remains unmerged.
prescore_freeze_commit: 96a40fc1efe64aaa46c149b4c24d7f09294f5ec8
R_result_commit: 77ce5128e1defbc235380d8ec3d2fd02ab09bbd9
A_commit: 2ed1d98fc29c28f12716288d47a62ed9434e6147
B_script_commit: 1468c408e7d52d6d8a540c8c4a99747315dce83e
R_report_commit: 1885935a798b60677f4431cfcc8c7ad43390e864
B_report_commit: 74ac4e047ca1e5bd07e372afd7c0649e8af02dbf
outputs:
  R: research/validation/R288_S84_SIX_DRAW_SIGN_ERROR_PRESCORE_FREEZE_2026-10-30.md; research/validation/r288_s84_sign_error_20261030.js; research/validation/R288_S84_ALL_576_SIGN_RECEIPTS.csv; research/validation/R288_S84_EXACT_RESULTS.json; research/validation/R288_S84_SIX_DRAW_SIGN_ERROR_SCIENTIFIC_REPORT_2026-10-30.md
  A: research/data_scout/A_PEREDA_2019_ZENODO_PUBLIC_GOODS_ROUND_ID_AND_MISSINGNESS_GATE_2026-10-30.md
  B: research/evidence_audit/b_r288_s84_independent_binomial_20261030.py; research/evidence_audit/B_R288_S84_NONBLIND_BINOMIAL_AND_REMOTE_RECEIPT_AUDIT_2026-10-30.md
results_seen: 9 artificial worlds x 64 ordered sources = 576 rows. All nine P(correct)=42/64. Eight P(wrong)=22/64. r=0,L=3 has P(wrong)=7/64 and P(tie)=15/64, conditional wrong=1/7. Independent binomial 9/9 matches, 5 source mutants and 6 local Python summary mutants rejected. Archived R V8 replay matches remote 576-row CSV byte-for-byte; archived native Node and remote B Python CLI NOT_RUN. Local independently written Python 3 CLI PASS. A verified public Zenodo PGG CSV sampled rows and eight-field schema, observed blank separators and missing values; full file checksum and participant grouping OPEN. New E2 predictions 0, E3 0, external replication 0.
CI_at_pre_handoff_head: check_runs=0, statuses=0, PR_associated_runs=0; no Actions launched.
billing_checked: NO; no fee-bearing operation initiated.
R073: FROZEN
PESEN_v0_1: FROZEN
original_R288_acceptance: CLOSED_BOUNDED_E1 unchanged
R281_S77_frozen_assertion_failure: RETAINED
next: fresh main HEAD, review R289 for complementary prescore problem; B original archived native CLI if no billing risk; A verify public PGG license/session/group without publishing participant rows. Keep original239 and pending queue unchanged.
