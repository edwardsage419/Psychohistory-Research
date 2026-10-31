# R track verified handoff

handoff_utc: 2026-10-31T00:44:21Z
track: r
subflows: R-main; A-data-scout; B-internal-independent-method-audit
baseline_head: edcd96cbae6cac93a8777e5b771b214c6fcac833
freeze_commit: 47c82ad9419913b121ae64d655a806eccd071b55
research_commit: 12d210b7cca5808b0509a29c650514ca087c4ee5
status: PARTIAL
claim: NO
claim_expiry_utc: N/A
target_keys:
  R: (r,R303,S99-v1,observational-equivalence-and-latent-acquisition-identifiability)
  A: (A,Hertz-Bell-Raihani-2021,original-public-article-and-OSF,trial-access-and-time-order)
  B: (B,R303,S99-v1,independent-algebraic-partition-and-adversarial-coverage)
read_scope: latest main, recent commits, open Codex PRs, R303 original README/report/acceptance/protocol/script and original 486 CSV, original239 v7.8 crosswalk, pending154 queue, latest R302 handoff, relevant A prior Bang 2017 files, public Hertz article/OSF metadata. Internal nonblind.
R_outputs: research/validation/R303_S99_OBSERVATIONAL_IDENTIFIABILITY_PRESCORE_FREEZE_2026-10-31.md; research/validation/r303_s99_identifiability.py; research/validation/R303_S99_ALL_81_IDENTIFIABILITY_WORLDS.csv; research/validation/R303_S99_EXACT_EQUIVALENCE_CLASSES.json; research/validation/R303_S99_MACHINE_RECEIPT.json; research/validation/R303_S99_OBSERVATIONAL_IDENTIFIABILITY_SCIENTIFIC_REPORT_2026-10-31.md
A_output: research/data_scout/A_HERTZ_2021_OBSERVATION_ADVICE_OSF_ACCESS_GATE_2026-10-31.md
B_outputs: research/evidence_audit/b_r303_s99_independent_partition_audit.py; research/evidence_audit/B_R303_S99_NONBLIND_ALGEBRAIC_PARTITION_AND_EIGHT_MUTATIONS_2026-10-31.md
work_performed: 81 exact artificial tuples grouped into 13 observational classes, histogram 6 singleton + 6 triple + 1 class of 57; 75/81 worlds in 7 classes with nonunique latent acquisition; available response always identified by exact incentivized probability. Local R 3 tests PASS, B algebraic 81/13 PASS and eight mutated inputs REJECTED. Original R303 486/486 archived source phase rows independently checked for exact original equations.
archive: 8 additive research files in research commit; all five source/CSV/JSON/receipt blob SHAs match tested local files. Original R303 files untouched.
A_status: Hertz 2021 public paper n=1492, 3 blocks x 15 trials, OSF link HTTP403; raw fields/license unknown, no E2; R073 ineligible.
B_status: internal nonblind mathematical consistency PASS; external independent reproduction NOT_RUN; empirical calibration and holdout NOT_RUN.
original239_v7_8_blob: 36f24235901172642c46853298aebb421f1a3552 UNCHANGED
pending154_blob: 3b96d46b3d88ccafd779a08509c3cfd0e435772f UNCHANGED
codex: PR1 OPEN_UNMERGED; PR3 OPEN_UNMERGED, R257 S53 not adopted on main.
ci_status: NOT_RUN; final research commit check_runs=0, commit_statuses=0, PR-triggered workflow runs=0.
billing_checked: false
cost: no paid API/data/compute or GitHub Actions initiated; actual account billing/free quota not independently checked.
blockers: OSF 403, human E2/E3 not run, no external blind replication, runner budget not checked.
next_action: re-read main and coordination; R304 complementary question if still unclaimed; continue R073 data search, independent B audit, and original R303 archive parity without claiming human identification.
R073: FROZEN
PESEN_v0_1: FROZEN
