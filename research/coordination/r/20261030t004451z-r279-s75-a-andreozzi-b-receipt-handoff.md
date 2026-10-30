# R轨短交接：R279 S75 有限样本校准与 A/B 复核
run_date_utc: 2026-10-30T00:44:51.682Z
track: r
baseline_main_HEAD: d237bb443382f07d77e57a95330ead5f142a0189
observed_main_HEAD_before_handoff: f4dd67b7add8b4b17319b5413cb2cefa2b7e88fa
target_keys:
  R: (r,R279,original-prescore+S75-v1,finite-four-bit-empirical-Murphy-bias)
  A: (A,Andreozzi2020,author-public-raw-six-session,raw-XLS-to-clean-CSV-provenance-gate)
  B: (B,R279,S75-v1,independent-count-and-persisted-receipt)
claim: NONE
claim_expires_utc: N/A
status: R_EXPLORATORY_E1_COMPUTED; A_PARTIAL_RAW_PIPELINE; B_INTERNAL_NONBLIND_V8_PASS; NATIVE_CLI_OPEN
artifact_commits:
  freeze: fb5fbd79c2589842d4b4ae27d59fe95f087cade4
  R_results: 48f589f6d86ee8d103f8e5b0b889bc0abc9e0e2e
  B_script: a876772c093c83752bf862bdedafcda38d525990
  R_report: fa49f51b50eabf2fedd7381e958c64a48dd296e7
  A_report_corrected: f4dd67b7add8b4b17319b5413cb2cefa2b7e88fa
  B_report: cc1581ad4fbfaec18b5af056673d05ea4ef8e7fc
output_paths:
  R: research/validation/R279_S75_FINITE_SAMPLE_CALIBRATION_BIAS_SCIENTIFIC_REPORT_2026-10-30.md
  R_source: research/validation/r279_s75_finite_sample_calibration_20261030.py
  R_data: research/validation/R279_S75_ALL_144_EMPIRICAL_SOURCE_ATOMS.csv
  R_receipt: research/validation/R279_S75_EXACT_RESULTS.json
  A: research/data_scout/A_ANDREOZZI_2020_SIX_RAW_SESSION_PIPELINE_AND_LICENSE_GATE_2026-10-30.md
  B: research/evidence_audit/B_R279_S75_NONBLIND_COUNT_ORACLE_AND_PERSISTED_RECEIPT_AUDIT_2026-10-30.md
  B_source: research/evidence_audit/b_r279_s75_strict_receipt_20261030.js
results_seen:
  R: 9 worlds x 16 source atoms=144; 99 positive; population-calibrated ORIGINAL_BUCKETS empirical REL expectation=3/32, P(empirical REL=0)=0; FLAT_HALF expectation=3/64, Pzero=59/128.
  B: independent Python Fraction count-route calculations for 9 REL expectations and Pzero; V8 strict persisted 144-source/9-world audit PASS, 7 mutations rejected.
  A: original six public XLS files and exact source metadata, zTree raw pipeline and CC BY 4.0/MIT license checked; raw XLS parsing and full reconstruction NOT_RUN.
  original_R279: CLOSED_BOUNDED_E1 remains unchanged.
  original239_v7_8_blob: 36f24235901172642c46853298aebb421f1a3552
  original239_pending154_blob: 3b96d46b3d88ccafd779a08509c3cfd0e435772f
  codex: 12 open PR including #1 S53 gap and #3 candidate; neither merged.
ci_status: NOT_RUN (commit statuses empty, PR-filtered associated workflow runs empty; all event runs not exhaustively enumerated)
billing_checked: NO; no paid API, no new services, no manually dispatched GitHub Actions
evidence_scope: E1 internal nonblind artificial only; new E2=0, E3=0, external independent team=0
blockers: archived R Python native CLI NOT_RUN; B Node native CLI NOT_RUN; original raw XLS->CSV reproduction NOT_RUN; no new scientific confirmation upgrade
next_action: run original archived R279 S75 Python --selftest and --emit, compare full persisted CSV/JSON; run B Node CLI; examine R280 next complementary problem. A seek raw XLS source replay in free open-source environment.
