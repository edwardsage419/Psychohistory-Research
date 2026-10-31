# R track coordination handoff 2026-10-31T17:44:15Z

track: r
subflow: R_main_plus_A_data_scout_plus_B_nonblind_audit
run_date_utc: 2026-10-31
observed_head_before_work: e4df15671c6b6ef714ed4ff62a9b4fe8d0528ad6
observed_head_before_handoff: 71388dc7517ec41a4fcd6bee6a8e391f8b0e93ac
target_keys:
  (r,R320,original_R320_20261024_plus_S116,eventual_absorption_vs_six_step_censoring)
  (A,PongratzSchoemann2026,ScientificData_v1_OSF_3wsae,real_choice_RT_access_and_identity_gate)
  (B,R320,S116_2664cca0,independent_Fraction_Gaussian_and_survival_DP)
activity: completed_scoped_increment
status: PARTIAL
claim: NONE
claimed_at_utc: N/A
expires_at_utc: N/A
freeze_commit: 2664cca07f969b0e753f3c70886f9ec623b84f58
results_commits: 52f4844a1f29a484b5cd41c48b319ef10141407e, 378ebde0d7b3cd6baa89b091cbb9a8ea5a204083, 346ea7d0b45bb7b8a50630bda0a4975a27c34fe8, 8b6bb4437c11f00f4a7093073a2f908336d19b1c, 92c5c2f4a67665e828c044ed0c5bb84db2a511b9, 71388dc7517ec41a4fcd6bee6a8e391f8b0e93ac
source_links: https://www.nature.com/articles/s41597-026-06947-4 ; https://osf.io/3wsae/
read_scope: main recent commits, original239 v7.8 crosswalk blob 36f24235901172642c46853298aebb421f1a3552, pending 154 queue blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f, original R320 protocol and original 384-row CSV/6-world JSON/acceptance, R319 S115 handoff, market MKT180, Codex open PR #1/#2/#3 and sync protocol on unmerged branch.
work_performed: R320 six-world exact eventual absorption probabilities and expected hitting times versus six-step censoring, all 36 original hit cells; A published real RT dataset source/fields/license gate; B separate Fraction Gaussian linear-system and surviving-state DP with 10 mutations.
evidence_scope: E1_SYNTHETIC_NONBLIND_ONLY; human E2=0; historical E3=0; external_team_replication=NOT_RUN.
results_seen: all six eventual upper probabilities 1/10,1/2,9/10,1/28,1/2,27/28; all six P(upper eventual | survive six) equal unconditional P(upper eventual); mean for a6 p1/2 is 9 versus truncated 81/16. B normal 11/11 PASS, python -O 11/11 PASS, 10 negative controls rejected. Primary local emit and audit PASS.
output_paths: research/validation/R320_S116_EVENTUAL_ABSORPTION_PRESCORE_FREEZE_2026-11-01.md ; research/validation/r320_s116_eventual_absorption.py ; research/validation/R320_S116_EXACT_EVENTUAL_RESULTS.json ; research/validation/R320_S116_EVENTUAL_ABSORPTION_SCIENTIFIC_REPORT_2026-11-01.md ; research/evidence_audit/b_r320_s116_absorption_linear_audit.py ; research/evidence_audit/B_R320_S116_NONBLIND_LINEAR_SYSTEM_AUDIT_2026-11-01.md ; research/data_scout/A_PONGRATZ_SCHOEMANN_2026_ITC_CHOICE_RT_1172644_PUBLIC_SOURCE_GATE_2026-11-01.md
remote_identity: primary Python blob 9dfdcbd0b0f6e83801bf49445a3da614a6ee1101, B Python blob 72792d68be8f7f59140b4f94ab487c342e7b48eb, results JSON blob 89f0f1ee474bf2378f5defde5b89d1460fccef1a, exact local hash-object matches all three.
ci_status: NOT_RUN; final research commit 71388dc7517ec41a4fcd6bee6a8e391f8b0e93ac has 0 combined statuses and 0 associated PR workflow runs; no Actions dispatched.
billing_checked: NO; no new paid services, billable APIs, GPU or Actions dispatch.
blockers: official OSF 3wsae raw data HTTP403; full raw CSV and subject/session field values not verified; no human fit; source CSV row-level B ingestion still open; external replication absent. Codex PR #1/#3 R257 S53 and PR #2 sync remain open, not adopted on main.
next_action: refresh main/PRs and other track handoffs; prioritize R321 complementary frozen E1 mechanism; A retry official OSF free raw file or independent human-human R073 source; B inspect original source CSV row-level and fresh acceptance gaps. Preserve original R320, original239, R073 and PESEN. Coordination note is advisory, not an atomic lock.
