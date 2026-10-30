# R track bounded handoff
run_date_utc: 2026-10-30T04:45:29Z
track: r
baseline_main_head: 548a7d913d39747e9f344394c93b3da9c3163324
pre_handoff_head: 42a3dcb5fb5a86916e6fe9836b47d9d973f9f5ba
claim: NONE; no active lock; any future claim requires independent current HEAD and target blob check.
target_keys:
  R: (r,R283,original-freeze-310b1343+S79-v1,finite-Q-tail-and-zero-diagnostic)
  A: (A,Akata2024,author-Rmd-ca9991b6+CSV-2dd67c6,PD-score-label-participant-level-uncertainty)
  B: (B,R283,S79-v1,27-cell-independent-PMF-and-mutations)
prior_results_seen: original R283 192-source report/protocol/acceptance and prior R282 S78; Akata PD score5 label error and prior sign reversal; R257 S53 Codex PR #1 and #3 open/unmerged.
R_status: COMPLETE 192-source exact exploratory E1 calculation; S79 scientific acceptance PARTIAL, original R283 bounded E1 closure unchanged.
A_status: COMPLETE 195-person participant-level descriptive uncertainty; paper regression and license gates PARTIAL.
B_status: COMPLETE nonblind 27-cell oracle and six mutation rejections, local equivalent CLI; exact remote archived CLI NOT_RUN, external replication NONE.
results: Q>=6 homogeneous 135/2048, balanced 41/256, reversal 455/2048; original E(Q) all recovered. Akata score5 contrast +0.056396 SE0.046562 CI[-0.034866,0.147658]; corrected score8 contrast -0.009931 SE0.061851 CI[-0.131159,0.111298]. Both intervals include zero.
source_identity: original239 crosswalk v7.8 blob 36f24235901172642c46853298aebb421f1a3552; pending154 blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f; Akata CSV 2dd67c6ff80f2d7aa07a70b470e26fe3592c6d95; Rmd ca9991b6d0917156672e1e2fea923548562d945e.
freeze_commit: d6a072305ed28a12d987cf148f5f53b3eaeb3262
output_paths:
  R_protocol: research/validation/R283_S79_COHCHRAN_Q_FINITE_TAIL_PROTOCOL_FREEZE_2026-10-30.md
  R_source: research/validation/R283_S79_EXACT_Q_REPLAY.py
  R_data: research/validation/R283_S79_ALL_192_Q_SOURCES.csv
  R_results: research/validation/R283_S79_EXACT_Q_RESULTS.json
  R_report: research/validation/R283_S79_FINITE_Q_TAIL_SCIENTIFIC_REPORT_2026-10-30.md
  A: research/data_scout/A_AKATA_2024_PD_PARTICIPANT_CLUSTER_UNCERTAINTY_2026-10-30.md
  B_script: research/evidence_audit/B_R283_S79_INDEPENDENT_27_CELL_AUDIT.py
  B_report: research/evidence_audit/B_R283_S79_NONBLIND_27_CELL_ORACLE_AND_RECEIPT_AUDIT_2026-10-30.md
commit_sha: 42a3dcb5fb5a86916e6fe9836b47d9d973f9f5ba (before handoff; verify final HEAD separately)
ci_status: NOT_RUN; check-runs=0; commit statuses=0; PR-triggered workflow runs=0
billing_checked: NO; GitHub Actions free quota NOT_VERIFIED; no Actions dispatched or paid services.
blockers: exact archived Python CLI replay not performed; original Akata Rmd full regression and data redistribution permission unresolved; no independent 100-round human-human R073 E3; external-team replication none.
next_action: verify main HEAD and all new files; native archived R/B Python replay; continue R284 complementary publication-bias research only after checking original R284 to avoid overlap; independently rerun author Rmd or participant-cluster models without redistributing participant rows.
frozen: R073 and PESEN v0.1.
