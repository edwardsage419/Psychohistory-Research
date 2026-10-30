# R track bounded handoff 2026-10-30T12:44:23Z

track: r
subflows: R primary, A public data, B independent method audit
baseline_main_head: 97d34de93a788cee16c3c5e31ab7d618824bf0ec
observed_main_head_before_handoff: 2fbbfc31e7427f3e53fcafa6faa44bcfd8d41684
activity: completed_bounded_increment
status: PARTIAL (S87 native CLI and full scientific acceptance open)
claimed: NO
target_keys:
  R: (r,R291,S87-prescore-4f51f811,misclassified-intention-proxy-and-norm-omission-Brier)
  A: (A,UCDP-GED,26.1,official-codebook-temporal-leakage-and-identity)
  B: (B,R291,S87-prescore-4f51f811,independent-conditional-variance-768-source-audit)
read_scope: main HEAD, 12 open Codex PR titles/abstracts including PR1 R257 S53 and PR3, unmerged Codex sync protocol, original239 v7.8 and pending154 blob IDs, R291 original freeze/code/results/report/acceptance, R290 S86 handoff, official UCDP GED 26.1 codebook/download/API.
original239_crosswalk_blob: 36f24235901172642c46853298aebb421f1a3552
pending154_blob: 3b96d46b3d88ccafd779a08509c3cfd0e435772f
prescore_commit: 4f51f8119ab5faba95fcf4b7b44b63eb6bb3621b
R_code_commit: cdb3722a2674982a7b5e4083f73ebfe0604aa668
R_source_commit: 96d2251f8a8d1008a7036bc8fd6cd7318505bf79
R_results_commit: 0f399655b2ffab19ee4e2125acc68c913dc1c4d8
A_commit: 36d203074453b59dd8ada7b6200d63ec6ae7f22d
B_code_commit: afde9553f6853e2269a9c6c20c0ddc443b3362b8
R_report_commit: 6028e669e1a1ac61c41ab16ce5a23f65a6331bac
B_report_commit: 2fbbfc31e7427f3e53fcafa6faa44bcfd8d41684
output_paths:
  R: research/validation/R291_S87_NOISY_INTENTION_PROXY_PRESCORE_FREEZE_2026-10-30.md; research/validation/r291_s87_noisy_intention_20261030.js; research/validation/R291_S87_ALL_768_PROXY_SOURCE_CELLS.csv; research/validation/R291_S87_EXACT_RESULTS.json; research/validation/R291_S87_NOISY_INTENTION_PROXY_SCIENTIFIC_REPORT_2026-10-30.md
  A: research/data_scout/A_UCDP_GED_26_1_OFFICIAL_CODEBOOK_TEMPORAL_LEAKAGE_GATE_2026-10-30.md
  B: research/evidence_audit/b_r291_s87_independent_conditional_variance_20261030.js; research/evidence_audit/B_R291_S87_NONBLIND_CONDITIONAL_VARIANCE_AND_SOURCE_AUDIT_2026-10-30.md
results_seen: 8 R291 synthetic DGPs times 3 proxy error rates, 768 full cells including 128 zero cells, 24 exact four-predictor Brier risks; BALANCED mediated norm gap 0, 11/4480, 1/256 at error rates 0,1/4,1/2. NORM_NULL mediated gap 0 always. B independent conditional-variance aggregation exact match 24 worlds, 768 sources, 5 malformed controls rejected. Separate local Python Fraction oracle matched 24 gaps. R generator four source mutations rejected.
source_links: https://people.umass.edu/aizen/f%26a1975.html ; https://ucdp.uu.se/downloads/ ; https://ucdp.uu.se/downloads/ged/ged261.pdf ; https://ucdp.uu.se/apidocs/
A_result: official UCDP GED 26.1 codebook extraction 2026-03-30, persistent event id vs mutable relid, source_date 1753-01-01 missing sentinel, date interval/precision, post-event revision leakage; free CSV ZIP linked, raw bytes not downloaded.
evidence_scope: internal nonblind E1 exact artificial; original R291 CLOSED_BOUNDED_E1 unchanged; S87 PARTIAL; E2=0; E3=0; external independent replication=0.
CI: final prehandoff commit check_runs=0; statuses=0; PR workflow runs=0; NOT_RUN
billing_checked: NO; no fee-bearing operations, Actions not triggered.
codex_PR1_R257_checker_gap: OPEN_UNMERGED; codex_PR3_candidate_fix: OPEN_UNMERGED
R281_S77_frozen_failure: RETAINED
R073: FROZEN
PESEN_v0_1: FROZEN
blockers: archived native Node --test/--check and B CLI NOT_RUN; full CI fee allowance unknown; UCDP ZIP binary not downloaded or parsed; no new human or historical predictive evidence.
next_action: refresh main and Codex PRs; run archived original R/B native Node CLI and exact receipt replay when local file bytes are available; then advance R292 complementary control-feasibility mechanism if no overlapping active work; A seek truly independent 100-round human dyads; keep E1/E2/E3 distinct.
