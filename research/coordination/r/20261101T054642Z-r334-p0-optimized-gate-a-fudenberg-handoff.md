# R track handoff: R334 P0 optimized receipt false acceptance

utc: 2026-11-01T05:46:42Z
track: r
baseline_main: 7944f045e6d6927bc7f7f53aba9b74aab5366139
verified_main_before_handoff: 5b3daaabc48fef14d5236ddee94c34e55c5ab9e9
status: PARTIAL_P0_ADDITIVE_GUARD_COMPLETE
claim: NONE
claim_expires_at_utc: N/A

target_keys:
  R: (r,R334,2026-10-24-prescore-frozen,optimized_assert_receipt_fail_open)
  A: (a,Fudenberg_Karreskog_Rehbinder_2024,openICPSR_182668_V1,session_supergame_R073_eligibility)
  B: (b,R334,original-pinned-blobs,nonblind_optimized_negative_controls)

work:
  P0: Exact original source Git blob 7d232a07d9d2979c2fcc8a407dd8bda18cd8ab93. Original render recreated archived CSV 6e3bdcc5ca07d1321a651c29b899798a32f7fb72 and JSON 02883b6b9cfc22b3b855d8a7cbaa5e5ddf6bd86c. In local CPython 3.13.5, original --test --audit with -O returned exit 0 and five unit tests OK for corrupted CSV, corrupted JSON and both missing files; normal mode rejected each. Original source-only alteration accepted in both modes. New independent no-import strict gate rejected all four negative controls in normal and -O. All tests local, nonblind E1; source, protocol, receipts and historical CI unchanged.
  A: Read author MIT preprint Section III and openICPSR V1 directory. Author reports 17 studies, 28 treatments, 161 sessions, 2612 participants, 232298 choices, median mean supergame length 6.7. Raw bytes, file license and dyad maximum not obtained; R073 frozen test eligibility UNKNOWN.
  B: Added no-import strict receipt checker, regression script, local result JSON, B report and R scientific-scope report. No Python 3.11/3.12 native replay or external team replication.

outputs:
  research/validation/R334_P0_OPTIMIZED_RECEIPT_SCIENTIFIC_SCOPE_2026-11-01.md
  research/evidence_audit/B_R334_P0_OPTIMIZED_ASSERT_NONBLIND_STRICT_GATE_2026-11-01.md
  research/evidence_audit/B_R334_P0_OPTIMIZED_GATE_LOCAL_EXECUTION_2026-11-01.json
  research/evidence_audit/r334_strict_receipt_gate_20261101.py
  research/evidence_audit/test_r334_optimized_gate_20261101.py
  research/data_scout/A_FUDENBERG_REHBINDER_2024_SAMPLE_UNIT_GATE_2026-11-01.md

commits: 5adbec013f3d174ac7c8941e153fa972ed550e09, fbfd09e63e5f8b139e7bf557bc4ae8f26e677004, 103251ba1c9fcd1cf4af8accfd318b5d22ad85e1, 3c29cf14fcb390fdc1f8ef2509f0014aefa73212, a1dd2482f9f916a01a09e4f47923fb9835123a00, 5b3daaabc48fef14d5236ddee94c34e55c5ab9e9
remote_verify: six new paths present, original paths changed 0; compare ahead_by=6.
index: original239 v7.8 blob 36f24235901172642c46853298aebb421f1a3552; pending154 blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f; unchanged.
codex: 12 open PR; PR #1 and #3 R257 S53 OPEN_UNMERGED; no main adoption.
ci: new head check_runs=0, combined statuses=0; NOT_RUN. Historic R334 CI run 40051279908 completed/success.
billing_checked: NO; quota UNKNOWN; no Actions dispatched or paid resource used.
next_action: Independent review and CPython 3.11/3.12 replay of strict R334 gate, then owner-reviewed integration without changing frozen source history; prioritize PR #1/#3 R257 P0 decision. A: obtain free licensed 17-study raw fields and test per-match identity/length, no R073 retuning.
