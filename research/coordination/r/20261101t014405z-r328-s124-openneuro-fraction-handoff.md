# R track handoff: R328 S124
utc: 2026-11-01T01:44:05.867Z
track: r
baseline_main: ecf4c3c51a07caddd2b99c795b92898dd0f37e84
pre_handoff_main: 24076266db5f3ca8c03441c58a2c3a565f7ed668
target_keys:
  R: (r,R328, S124-v1, finite_gradient_step_size_stability)
  A: (a,OpenNeuro_ds007822_v1.0.0,triadic_PD_33_subject_40_trial_source_license_gate)
  B: (b,R328,S124-v1,nonblind_fraction_closed_form_480_and_five_mutations)
status: PARTIAL_E1_EXTENSION_NONBLIND_INTERNAL_AUDIT_PASS
claim: NONE
claim_expiry: N/A
freeze_commit: b9838d4052c9632d950cffd2e22a9fa3e1ae47b5
primary_js_commit: 16293a8c6d20acfc48a28b9ae2e0d7a05356b709
csv_commit: 798d43ec37aa491af133d4816afd0506630a288f
json_commit: 1003a8dd5109094200b2881398e5d43c55ea599e
b_python_commit: 119877be1ca4893fb66b8685fe68404614a0c8d2
a_report_commit: e295f5ba5fdeda21a9b6634df2f8e019a04934c2
r_report_commit: 796983a93d130a00a939488666d47e7c0c9be3fb
b_report_commit: 24076266db5f3ca8c03441c58a2c3a565f7ed668
outputs:
  R: protocols/R328_S124_GRADIENT_STEP_SIZE_STABILITY_PRESCORE_FREEZE_2026-11-01.md; research/validation/r328_s124_step_size.js; research/validation/R328_S124_ALL_480_STEP_SIZE_STATES.csv; research/validation/R328_S124_EXACT_96_STABILITY_WORLDS.json; research/validation/R328_S124_STEP_SIZE_STABILITY_SCIENTIFIC_REPORT_2026-11-01.md
  A: research/data_scout/A_OPENNEURO_DS007822_33_SUBJECT_40_TRIAL_PD_BEHAVIOR_LICENSE_CONFLICT_2026-11-01.md
  B: research/evidence_audit/b_r328_s124_independent_fraction.py; research/evidence_audit/B_R328_S124_NONBLIND_FRACTION_480_ROW_FIVE_MUTATIONS_2026-11-01.md
results_seen: 96 exact artificial worlds; 480 unique rows; 120 original R328 rows match alpha=1/4. Flat32 contractive32 neutral8 expansive24; 24 worlds show energy increases. Exact archived JS V8 re-execution matches full remote CSV/JSON bytes; independently executed Python Fraction source SHA equals remote committed auditor; Python normal and -O pass; 5 mutations rejected; independently reconstructed full CSV/JSON Git blob matches remote SHA (c2343a241f5389071eb1c8cdaf8c9e955f7daca2,9e06c249036ebe09316e9952017b043afe96df73). Native Node CLI NOT_RUN; external replication NOT_RUN.
A_seen: OpenNeuro ds007822 DOI 10.18112/openneuro.ds007822.v1.0.0. 33 public anonymized subjects in 11 triads, all 33 event TSV files read, 40 trials each = 1320 decision event rows, 8 fields; 3-player 40-trial design HARD_NO for R073 frozen 100-round dyad. dataset_description declares CC0 while LICENSE states source license absent; conflict OPEN. No raw participant data archived.
B_seen: E1 only, no real human E2/historical E3. R073 and PESEN v0.1 frozen.
index: original239 v7.8 blob 36f24235901172642c46853298aebb421f1a3552; pending154 blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f; unchanged.
codex: PR #1 and #3 OPEN_UNMERGED; no R257 S53 main adoption.
ci: S124 commit check_runs=0, statuses=0, PR workflow_runs=0; NOT_RUN, no Actions triggered. Actual GitHub billing/free runner quota NOT_VERIFIED.
cost: no paid APIs, data purchases, runners, GPU or cloud. All local Fraction and public GitHub reads.
next: R329 original protocol/source/queue then select bounded nonoverlapping mechanism extension; A find eligible independent 100-round human dyadic PD and resolve ds007822 license before E2; B native Node replay of archived S124 and R327 S123; maintain distinct E1/E2/E3.
coordination: advisory only, no atomic lock, no active claim.
