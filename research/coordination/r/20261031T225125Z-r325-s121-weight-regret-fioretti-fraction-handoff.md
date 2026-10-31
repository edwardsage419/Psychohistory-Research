# R track handoff: R325 S121

utc: 2026-10-31T22:51:25Z
track: r
baseline_main: 58f129a38b7857f6ac0501d8259036251c9f10ce
target_keys:
  R: (r,R325,original_20261024_cubic_v1,S121_state_weight_sensitivity)
  A: (a,Fioretti_2022_openICPSR_130441_V1,source_raw_field_license_gate)
  B: (b,R325,S121_fff93b2a,nonblind_fraction_row_and_mutations)
status: PARTIAL_E1_EXTENSION_WITH_INTERNAL_NONBLIND_REPLAY_PASS
claim: NONE
claim_expiry: N/A
freeze_commit: fff93b2a837d63be4047e932b1c6f66bfff9a0a7
r_result_commit: 1b48a5e37ba01495125c8dbc234fb3fe3eb6fc72
reports_audit_commit: e9a8450fec090ec83cfcd5defdbbf32748d7db92
outputs:
  R: research/validation/R325_S121_ALL_4116_WEIGHTED_STATES.csv; research/validation/R325_S121_EXACT_WEIGHT_RESULTS.json; research/validation/r325_s121_weight_sensitivity.js; research/validation/R325_S121_WEIGHT_SENSITIVITY_SCIENTIFIC_REPORT_2026-11-01.md
  A: research/data_scout/A_FIORETTI_2022_DYNAMIC_REGRET_OPENICPSR_V1_SOURCE_GATE_2026-11-01.md
  B: research/evidence_audit/b_r325_s121_row_checker.py; research/evidence_audit/B_R325_S121_FRACTION_AND_LIVE_MUTATION_AUDIT_2026-11-01.md; research/evidence_audit/B_R325_S121_AUDIT_RECEIPT_2026-11-01.json
results_seen: Four weight profiles x three fixed kappa worlds x 343 ordered artificial triples = 4116 exact rows. Uniform reproduces original 0,6,6 reversals. EARLY/LATE kappa 1/4 reversals=14, kappa 1 reversals=16; CENTER reversals=16 in both nonlinear worlds. EARLY/LATE equal aggregate but individual choices differ 110/82/82 for kappa 0/1/4/1. Independent Python Fraction full CSV/JSON bytes match remote Git blobs 8df84f30ad1d680758aa526d3f8f05a911523bd0 and b1c4bf4d07f0479fdefb1dc22aa202b8e6526531. Compact archived checker source blob 5276cdf1176f8c75cb6ef0764369ba2b68acf134 matches executed local code. Normal and optimized checker both PASS; four live mutations rejected each. Local full oracle six additional live controls each, overlapping classes.
A_seen: openICPSR 130441 V1 2022-01-25, dynamic regret asset sale study; newchoicedata.csv 551.1KB, newlongdata_withhlcrt.txt 40.6MB and code metadata observed. Root access 403; row data, field names, identity keys, time units, license and checksums NOT_VERIFIED. R073 HARD_NO_BY_TASK_TYPE.
B_scope: internal nonblind E1 only. Native Node CLI NOT_RUN; external team NOT_RUN; human E2=0, historical E3=0. Existing market E154 confirms separate R324 S120 native --selftest defect; no duplicate R324 work.
source_identity: parent R325 original CSV b4964ef88aded2c9bd2a70280c067176fedcd597. original239 v7.8 36f24235901172642c46853298aebb421f1a3552 and pending154 3b96d46b3d88ccafd779a08509c3cfd0e435772f unchanged.
coordination: PR #1 and PR #3 open/unmerged, R257 S53 still not adopted into main. All nine new artifacts added, no prior file modified.
ci: S121 final evidence commit check_runs=0, statuses=0, PR_workflow_runs=0, NOT_RUN. Free billing allowance NOT_VERIFIED; no Actions initiated.
cost: no paid APIs, data, compute, runner or new subscription.
next: R326 hierarchical Bayesian model after fresh HEAD/other-track check; B native R325 S121 Node CLI and parent source 1029-row independent replay; A official openICPSR raw access/rights or another independent R073-compatible human dyad source. R073 and PESEN v0.1 frozen, no classification/fusion/personal product.
