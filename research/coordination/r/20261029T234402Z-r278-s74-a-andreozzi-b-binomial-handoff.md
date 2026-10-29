# R轨短交接：R278 S74、A Andreozzi 与 B 完整收据
run_date_utc: 2026-10-29T23:44:02Z
track: r
subflows: R-main, A-data-scout, B-evidence-audit
observed_main_HEAD_initial: a01d4f68c932669efe155220b1b022a4208726ef
observed_main_HEAD_before_handoff: 474fb0908459ad9fa4d53b288b24198590b75fdd
target_keys:
  R: (r,R278,original-eb1c8df3+S74-v1,two-step-joint-Brier-mixture-versus-product)
  A: (A,Andreozzi2020,author-979abf87,wrong-wide-o-lag-actual-analysis-references)
  B: (B,R278,S74-v1,independent-binomial-and-persisted-960-receipt)
activity: completed_bounded
status: COMPLETE (R exploratory E1 exact computation; A static main.R source usage audit; B internal analytic and 960 source audit), PARTIAL (native Node and full remote-to-native Python CLI; original-to-cleaned real data replay)
claim: NONE
claimed_at_utc: null
expires_at_utc: null
freeze_commit: 56b00cf6d016242e4d35c800c9b4a3162d01ea1e
R_artifact_commit: 97f02c11ba30e778e4725fd0cd55477985a4899c
R_A_B_report_commit: 474fb0908459ad9fa4d53b288b24198590b75fdd
output_paths:
  R_protocol: research/validation/R278_S74_TWO_STEP_JOINT_PREDICTIVE_PROTOCOL_FREEZE_2026-10-30.md
  R_source: research/validation/r278_s74_joint_20261030.js
  R_csv: research/validation/R278_S74_ALL_960_ARTIFICIAL_SOURCES_2026-10-30.csv
  R_json: research/validation/R278_S74_EXACT_RESULTS_2026-10-30.json
  R_report: research/validation/R278_S74_TWO_STEP_JOINT_PREDICTIVE_SCIENTIFIC_REPORT_2026-10-30.md
  A: research/data_scout/A_ANDREOZZI_2020_WRONG_LAG_FIELD_MAIN_ANALYSIS_USAGE_GATE_2026-10-30.md
  B: research/evidence_audit/B_R278_S74_NONBLIND_BINOMIAL_AND_PERSISTED_RECEIPT_AUDIT_2026-10-30.md
  B_source: research/evidence_audit/b_r278_s74_receipt_check_20261030.py
results_seen:
  R: 960 policy-labelled artificial sources, 15 exact joint Brier worlds; BMA joint minus product p1/4,p3/4=-2347029/551368000; p1/2=+1204403217/113030440000. Coherent BMA predicted future dependence even though true fixed-p future independent.
  B: two independent exact methods 15/15, source CSV Git blob 494c688596cda6186fb6f0e1c588584009659934 matches local Python CSV byte for byte; native Python compact checker PASS 960 rows/15 worlds; 6+6 injected failures rejected.
  A: author main.R 459 lines no reference to wrong opp_cond_class_wide_o_lag1; author Table 3 uses narrow lag; previous 813/1206 wide_o lag errors remain, static code path limits immediate impact claim.
  PR: 12 open Codex PRs including #1 R257 S53 gap and #3 strict checker candidate, both unmerged.
original239_v7_8_blob: 36f24235901172642c46853298aebb421f1a3552
original239_pending154_blob: 3b96d46b3d88ccafd779a08509c3cfd0e435772f
source_links:
  R_original: https://github.com/edwardsage419/Psychohistory-Research/tree/main/research/R278
  A_author: https://github.com/seyhunsaral/stabilitycondcoop/tree/979abf87b5d3cfb7aa8be13b81ef233076c3bb75
ci_status: NOT_TRIGGERED_THIS_RUN (full GitHub Actions list not yet verified)
billing_checked: NO
cost: no paid API, paid data, GPU rental, or manually triggered Actions
evidence_scope: E1 exploratory internal nonblind; E2 new predictions=0; E3=0; external team replication=0; R073/PESEN v0.1 frozen
blockers: native Node CLI NOT_RUN; remote persisted receipt full Python CLI NOT_RUN; author raw-to-CSV and paper numeric reproduction NOT_RUN; R278 original formal acceptance unchanged
next_action: inspect R279 forecast calibration for distinct complementary problem; A reconstruct author raw data pipeline by session; B close R278 S74 native CLI receipt and then revisit R277 S73 Node gap if still open
