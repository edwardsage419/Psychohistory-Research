# R track bounded handoff: R282 S78, Akata A, independent B
run_date_utc: 2026-10-30T03:44:04.738Z
track: r
observed_head: 57db53bcb8df2e544607ce57d973d0f7ba496909
baseline_main_head: 2b543b4a0593dacfff9c7f8078676f45678ec088
claim: NONE
target_keys:
  R: (r,R282,original-5447354b+S78-v1,schedule-identification-from-observations)
  A: (A,Akata2024,author-Rmd-ca9991b6+CSV-2dd67c6,PD-cooperation-label-group-direction)
  B: (B,R282,S78-v1,inverse-transition-full-receipt-mutation)
statuses: R COMPLETE bounded exploratory E1 calculation, scientific acceptance PARTIAL; A PARTIAL; B COMPLETE internal nonblind V8 and persisted byte replay, native CLI NOT_RUN.
freeze_commit: def580607b81df0873fd54cd73ceff991f19e863
prior_results_seen: original R282 192-source, paired schedule disagreements; previous Akata PD score5 vs score8 warning; R281 S77 frozen tie FAIL preserved; Codex PR #1 and #3 unmerged.
results: R 192 complete artificial cases, 4 regimes Bayes accuracy 1/3,1/3,2/3,5/6, full trace alone TV zero; B inverse 192 state triples, 36 TV cells, seven mutations rejected, remote archived V8 CSV/JSON exact byte replay; A Akata Base 362/970 vs Prompted 421/980 score5, corrected score8 Base 362/970 vs Prompted 356/980, descriptive contrast reverses, one anomalous PD record preserved.
source_links:
  R: https://github.com/edwardsage419/Psychohistory-Research/tree/main/research/R282
  A: https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repgames.csv
  A_Rmd: https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repeated_games.Rmd
output_paths:
  R: research/validation/R282_S78_SCHEDULE_OBSERVABILITY_SCIENTIFIC_REPORT_2026-10-30.md
  A: research/data_scout/A_AKATA_2024_PD_LABEL_GROUP_CONTRAST_DIRECTION_2026-10-30.md
  A_license: research/data_scout/A_AKATA_2024_PUBLIC_DATA_LICENSE_SCOPE_GATE_2026-10-30.md
  B: research/evidence_audit/B_R282_S78_ARCHIVED_SOURCE_V8_BYTE_REPLAY_ADDENDUM_2026-10-30.md
commit_sha: 57db53bcb8df2e544607ce57d973d0f7ba496909 (pre-handoff HEAD; final handoff SHA must be verified separately)
ci_status: NOT_RUN; no workflow dispatch, billing quota NOT_VERIFIED
billing_checked: NO; no paid API, GPU, dataset, runner or cloud used
crosswalk_blob: 36f24235901172642c46853298aebb421f1a3552
pending154_blob: 3b96d46b3d88ccafd779a08509c3cfd0e435772f
blockers: native Node CLI not run; author Rmd full regression not rerun; human data redistribution rights unclear; R073 independent 100-round human-human data not obtained; external replication none.
next_action: inspect R283 for complementary S79 question or close S78 native CLI gap; independently run original Akata Rmd in free environment with participant-level clustering and published-output tracing, without changing original files; preserve R281 frozen failure. R073 and PESEN v0.1 FROZEN; E2 new prediction=0 E3=0.
