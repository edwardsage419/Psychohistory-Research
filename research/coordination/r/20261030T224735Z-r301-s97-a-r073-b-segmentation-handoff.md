# R track coordination handoff
handoff_utc: 2026-10-30T22:47:35Z
track: r
status: PARTIAL_NONBLIND_INTERNAL_E1
claim: NO
claim_expiry_utc: N/A
baseline_main_HEAD: eb1e40292489d0637e456b72f361da815da19de3
freeze_commit: b18d1cd4e149a60ebfe3732f38f09f1cb6d94e7a
science_commit: f8d63599598caab1fbe4209724bbc3247ee410cd
head_before_handoff: f8d63599598caab1fbe4209724bbc3247ee410cd
target_keys:
  R: (r,R301,S97-v1,fifth_bit_heldout_hazard_misspecification_Brier)
  A: (A,R073_second_dataset,source_gate-v1,independent_hundred_round_human_dyad_access)
  B: (B,R301,S97-v1,independent_full_segmentation_oracle_and_mutations)
read_scope: main HEAD, recent commits, original239 v7.8 blob 36f24235901172642c46853298aebb421f1a3552, pending154 blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f, original R301 protocol/script/report/acceptance, R300 S96 handoff, 12 open Codex PRs including #1/#3, primary Figshare/Mao/OSF and machine simulation candidate pages. Nonblind.
R_outputs: research/validation/r301_s97_hazard_heldout.py; research/validation/R301_S97_ALL_288_HELDOUT_ATOMS.csv; research/validation/R301_S97_EXACT_HELDOUT_RESULTS.json; research/validation/R301_S97_RECEIPT.json; research/validation/R301_S97_SCIENTIFIC_REPORT_2026-10-31.md
A_output: research/data_scout/A_R073_CANDIDATE_RECHECK_2026-10-31.md
B_outputs: research/evidence_audit/b_r301_s97_independent_segmentation.py; research/evidence_audit/B_R301_S97_NONBLIND_SEGMENTATION_AUDIT_2026-10-31.md
R_result: 288 full artificial atoms, 9 exact Brier risks. True hazard 1/2 with assumed 0 yields risk 113/432 > constant 1/4. R 8 local tests pass.
A_result: Figshare ZIP unsupported and rights unresolved, Mao 400 independent 10-round games and OSF 403, machine tournament excluded; no new eligible R073 second independent dataset.
B_result: independent exhaustive segmentation 288 rows and nine risk/excess pairs exact; 9 tests pass including seven mutations rejected.
original239_v7_8: UNCHANGED
pending154: UNCHANGED
codex: 12 PRs open; PR1/3 unmerged, R257 S53 not marked fixed on main.
CI: NOT_RUN; science commit statuses=0, check-runs=0, associated PR workflow runs=0.
cost: no paid services or Actions dispatched; billing and free quota NOT_VERIFIED.
evidence: E1 artificial only; new E2=0, E3=0, external team replication=0.
R073: FROZEN
PESEN_v0_1: FROZEN
original_R301_formal_acceptance: UNCHANGED
next: re-read main HEAD/PRs and coordination, choose complementary R302 S98 or unresolved R301 audit gap; A continue legal raw access and independent dyad search; B preserve R281 S77 frozen failure and check native replay when feasible. No taxonomy/fusion/product.
