# R track handoff: R324 S120

utc: 2026-10-31T21:51:52Z
track: r
baseline_main_before_freeze: 50292a7e2e4d258d3a64c1387dceccda1e743414
target_keys:
  R: (r,R324,original_R324_20261024_frozen,ordinal_observation_S120)
  A: (a,Basel_Risk_Norms_2024,OSF_gu9df,public_metadata_and_raw_access_gate)
  B: (b,R324,S120_dc2bc2ad,nonblind_DU_multiplicity_oracle)
status: PARTIAL_E1_EXTENSION_REPLAY_PASS_NATIVE_CLI_OPEN
claim: NONE
claim_expiry: N/A

freeze_commit: dc2bc2ad22a0130984cf0ecb497c2c54f04803f8
r_code_commit: 7ab53cb623f07fadb1ea696c13f0a0cbd717db2b
r_csv_commit: 61a5fb830922eda9321cd5e3cdeec55a96d9a5da
r_json_commit: b5283949ffe5bae193c55bd4cadece6fe281f18e
b_code_commit: 27063499c52ec7bf763f03333875dfddea1cd1f4
r_report_commit: e0abfdff196ce5417d2694cca231df3d88347c6b
a_report_commit: ff358dc2028033d38221bac59d12013154f3c538
b_report_commit: f9226edd5a658d9e52ad8f4cb6659d961d6144c9
b_receipt_commit: 06e11d71ecce394f1bec80ce0452d7c5ecb10755

results_seen: 64 original R324 atoms reverified; P0..P5 accuracies 1/4,45/64,13/32,15/32,15/32,9/16; full 16-hazard ordinal profile 3/4, W2/W3 ordinal-equivalent, 15/16 cardinal scores different. V8 persisted R and B script replay PASS; independent local Python Fraction oracle matched. B actual persisted 64-row source and 64-row new CSV checks PASS; nine mutations rejected. Initial B aggregation failure and structuredClone runtime failure recorded and corrected. No native Node CLI or external team replay.
A_seen: Hussain et al 2024 1004 risks, 1506 risk-rating participants, 2360 psychometric-rating participants; 9 dimensions; OSF gu9df access HTTP 403, raw schema/rights unknown. Spence et al 2022 Dryad 727 participants, 11 diseases, 12 attributes, two raw file downloads HTTP 403. R073 both HARD_NO_BY_TASK.
source_identity: original R324 CSV blob 1b0062eeea020606a3d510d566da43db03ace8d9 unchanged. original239 v7.8 blob 36f24235901172642c46853298aebb421f1a3552 and pending154 blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f unchanged as read; no modifications.
coordination: 12 open Codex PRs seen initially; PR #1 and PR #3 verified open/unmerged after result. Other tracks' latest handoffs inspected. No collision on R324 S120.
ci: final evidence commit 06e11d71 check_runs=0, statuses=0, PR_workflow_runs=0. NOT_RUN. Free billing allowance NOT_VERIFIED. No Actions triggered.
cost: no paid API, no paid data, no paid compute. Existing ChatGPT and free GitHub connector only.
scope: E1_SYNTHETIC_ONLY; human E2=0, historical E3=0, R073 and PESEN v0.1 frozen; no classification, fusion or personal product.
next: R325 after fresh HEAD and cross-track check. B native Node CLI replay, independent method recheck, empirical validation gates remain open. A official OSF/Dryad raw access and dataset licence verification before any E2.
