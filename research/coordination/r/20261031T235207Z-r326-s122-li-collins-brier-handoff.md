# R track coordination handoff: R326 S122
utc: 2026-10-31T23:52:07Z
track: r
baseline_main: b2fe953eb3bebf214fd747b9b2bd283a6e2e5192
target_keys:
  R: (r,R326,original_20261024_shared_Z_three_group_v1,S122_prior_predictive_brier_H_vs_I)
  A: (a,Li_Collins_2025_Cognition_254_105967,public_row_identity_license_R326_gate)
  B: (b,R326,S122_f2e4798f,nonblind_full_768_atom_factorized_audit)
status: PARTIAL_E1_EXTENSION_WITH_INTERNAL_NONBLIND_AUDIT_PASS
claim: NONE
claim_expiry: N/A
freeze_commit: f2e4798fc97697c642cc1fa20fd70cdd987b1c50
r_result_commit: d92f1f4ff47a2ee546094c2f4df4ba7f3d36ceca
a_b_report_commit: 9a0f9e0e288bc86ce6cf453992e075f3f59ea5cf
output_paths:
  R: research/validation/r326_s122_exact_predictive_brier.js; research/validation/R326_S122_ALL_768_PREDICTIVE_ATOMS.csv; research/validation/R326_S122_EXACT_BRIER_RESULTS.json; research/validation/R326_S122_PREDICTIVE_BRIER_SCIENTIFIC_REPORT_2026-11-01.md
  A: research/data_scout/A_LI_COLLINS_2025_HIERARCHICAL_POLICY_445280_ROW_SOURCE_GATE_2026-11-01.md
  B: research/evidence_audit/b_r326_s122_independent_factorized_audit.py; research/evidence_audit/B_R326_S122_NONBLIND_FACTORIZED_768_ATOM_AUDIT_2026-11-01.md
results_seen: 64 histories x 3 groups x 2 outcomes x 2 artificial laws = 768 exact atoms. H expected Brier hierarchical 2150517/9614080, independent 9/40, constant 1/4. I expected Brier hierarchical 16336700817/72211354880, independent 9/40, constant 1/4. H pooling gain 12651/9614080; I pooling penalty 89145969/72211354880. Parent original 64-row CSV independently rebuilt to same 3679-byte Git blob 3d2481365160c33fabbba7f8be6c3a9ff78e5121. Persisted new R CSV blob 27f50f1bbb10bb78c43f41acf29af58268957708 and JSON blob 30e88f65e1b15b5d6010f647750a9526898b88eb match independently generated local bytes.
A_seen: Li and Collins 2025 Cognition, DOI 10.1016/j.cognition.2024.105967, author repo jl3676/learning_hierarchy HEAD 85e637a07cdb0a28d0c0777b22c337e73fcf25fd. Actual full public CSV 23,441,134 bytes parsed: 445,280 rows, 1,012 anonymous ids, each 440 rows, 14 fields, zero duplicate id/block/trial keys; 20,581 empty stage-action cells per stage. Article reports 1,026 completed, discrepancy unresolved. Public data license unconfirmed. R073 HARD_NO_BY_TASK_TYPE.
B_seen: Python 3.13.5 standard-library no-import factorized exact oracle; all 768 rows and six risks compared, 8 mutations rejected in normal and -O. Local first source flag failure retained, resolved by exact parent CSV reconstruction. Internal nonblind E1 only. New primary archived Node native CLI NOT_RUN; external team NOT_RUN; E2 human scoring=0, E3 history=0.
original239: v7.8 Git blob 36f24235901172642c46853298aebb421f1a3552; pending154 Git blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f; unchanged.
codex: PR #1 OPEN_UNMERGED at final check; no main adoption of R257 S53 checker coverage. Other codex PRs read at run start, unmerged claims excluded.
ci: result commit check_runs=0, statuses=0, PR_workflow_runs=0; NOT_RUN. Historical parent R326 CI success separate.
cost: no Actions launched, no paid data/API/compute. Account billing and free allowance NOT_VERIFIED.
next: R327 original frozen POMDP source/queue check then bounded extension; A confirm Li/Collins data rights, reconcile 1012 vs 1026 and design a separate preregistered E2 mapping if lawful; B native archived Node S122 replay, then inspect R325 S121 native CLI. Preserve R073/PESEN v0.1 frozen, no taxonomy/fusion/personal product.
coordination: advisory handoff only, not an atomic lock.
