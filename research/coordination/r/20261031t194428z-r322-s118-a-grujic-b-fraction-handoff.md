# R track scoped handoff R322 S118

utc: 2026-10-31T19:44:28.894Z
track: r
baseline_head_before_new_freeze: 5437a44e9b03ecdd4aed43b2b9d5f7eba94af917
observed_head_before_handoff: 56f807a61e31863a9dd97a9070d302f430812dc4
target_keys: (R,R322,S118_fa68814b,behavior_vs_process_label_noise); (A,Grujic_Lenaerts_2020,Dryad_7fq25s8,50_round_source_gate); (B,R322,S118_fa68814b,nonblind_fraction_60_cells)
status: COMPLETE_SCOPED_INCREMENT; scientific grade PARTIAL_E1_EXTENSION
claim: NONE
claim_expiry: N/A

freeze_commit: fa68814b2a036e6430519c8058a815acfdb0fce2
r_code: research/validation/r322_s118_exact.js
r_result: research/validation/R322_S118_EXACT_OBSERVATION_LABEL_NOISE_RESULTS.json
r_report: research/validation/R322_S118_OBSERVATION_LABEL_NOISE_SCIENTIFIC_REPORT_2026-11-01.md
r_report_commit: 751e8b1ab8ec61b6ba3925809cd0a8bcf28fe528
a_report: research/data_scout/A_GRUJIC_LENAERTS_2020_SPATIAL_PD_DRYAD_50ROUND_SOURCE_GATE_2026-11-01.md
a_commit: ccce0331f79e275828351ddb2c3ff5306645a970
b_code: research/evidence_audit/b_r322_s118_independent_oracle.py
b_report: research/evidence_audit/B_R322_S118_NONBLIND_60_CELL_FRACTION_AUDIT_2026-11-01.md
b_report_commit: 56f807a61e31863a9dd97a9070d302f430812dc4

results_seen: original R322 256 CSV Git blob verified 0cd38ecc22adc5941832c2b00e6928d48be8d896; 60 exact cells cross-route agreement; six source mutation rejections; behavior-only TV=0; full noiseless intervention label TV=1/16, accuracy=17/32; flip=1/4 TV=1/32; r=0 TV=0; r=1 TV=1/8; all gates present TV=1/2. Independent Python run locally; archived Node CLI and exact archived Python bytes native replay NOT_RUN. A Dryad CSV/README access HTTP 403; original paper says 144 humans, 9 sessions, 50 rounds, four neighbors; R073 hard no.

source_identity: original239 v7.8 crosswalk blob 36f24235901172642c46853298aebb421f1a3552; 154 queue blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f; unchanged by this track. Open Codex PR #1 and #3 remain unmerged as of initial PR search; no adoption.
ci: NOT_RUN; no Actions dispatched; free billing balance NOT_VERIFIED
cost: no paid API, compute, data purchase or cloud resources
scope: E1 synthetic internal nonblind only; E2=0; E3=0; external team=NOT_RUN. R073/PESEN frozen.
next: R323 complementary model only after fresh HEAD/PR/coordination review; B exact archived native CLI replay and test asymmetric label noise only under new freeze; A retry public Dryad access, preserve raw 403 block.
