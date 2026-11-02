# R272 P0 direct preimage path and mutation-sensitive regression

track: R+B
subflow: original239 12-002 scientific integrity
run_date_utc: 2026-11-02T08:44Z
starting_main_head: 8baa8d3b1f7818f17c3d72b28fdf230f2e3e2c83
target_key: (R+B,R272,2026-10-23 frozen 12-002,actual verify_preimage mutation-sensitive regression)
status: COMPLETE_LOCAL_DIRECT_REGRESSION / PARTIAL_PRODUCTION_ACCEPTANCE / P0_OPEN

## Question and inputs

The previous audit showed that deleting any one of three mandatory source, prescore-freeze or archived-machine-receipt identity guards left the candidate wrapper's existing --self-test green. This audit tests the actual verify_preimage entrypoint across all five required inputs and checks whether the regression suite fails when each of the three guards is deleted.

Read main, the original239 v7.8 crosswalk (Git blob 36f24235901172642c46853298aebb421f1a3552), actual pending queue (blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f), frozen R272 protocol (blob 9fbdb0078a58c4a9c0a548643227e30da5731119), R272 acceptance record, existing read-only wrapper, previous mutation audit, and production workflow (blob 3132b08cf4ee64b55f5112d2249894ea0ec9d42d). All 12 Codex PRs were open at the initial check; PR #1 and #3 concern R257 S53. No competing R272 PR was found. Later unrelated commits were not assumed to change the R272 science.

Code: research/validation/r272_preimage_actual_path_regression_20261102.py
Local code SHA256: 093d2683cab2547a41053277ffb653d6190e3967b05bc044301267021e6a43a4
Local and remote code Git blob: 678d9e8092e03e175eb748e019548d39920dc5ca
Baseline wrapper Git blob: 8722fd4388421e3b1f77c6648b4ed1b38088c4b0
Independent checker SHA256: f7109f8f815d166128ca3429fb42ff3e7cac780d03fb78f8243aeabbd6fbb786

## Executed controls

Environment: local CPython 3.13.5, Python standard library, temporary directories, no random seed. The pinned checker reconstructed the exact archived CSV and results SHA256 and the archived receipt Git blob. The original generator and prescore freeze files in the test checkout are explicitly SYNTHETIC_STAND_INS, and their expected blobs are patched in memory. This is a direct path test of the candidate wrapper, not a full authentic checkout replay.

The unchanged wrapper ran in normal Python, -O and -OO. Each mode: one intact positive accepted; appending one newline to each of source, freeze, CSV, results and receipt rejected 5/5; replacing each of those five inputs by a symlink to identical bytes rejected 5/5. Totals: 3 positive controls, 15 corrupted-byte rejections, 15 symlink rejections.

Next, each of the source, freeze and receipt mandatory require guards was separately deleted in a disposable copy of the wrapper. The same direct regression was executed under normal, -O and -OO for each mutant. All nine mutant regressions failed as required, each identifying its removed guard's corrupted input as falsely accepted. This closes the previously identified **test sensitivity gap for these three guards**, conditional on running this separate test suite. It does not repair the wrapper's own --self-test or production workflow.

Local command:

    python research/validation/r272_preimage_actual_path_regression_20261102.py \
      --wrapper research/validation/r272_preimage_first_readonly_gate_20261102.py \
      --gate /path/to/verified/r272_failclosed_independent_receipt_gate_20261102.py

Observed final JSON: status PASS; baseline_modes 3; baseline_positive 3; baseline_byte_rejections 15; baseline_symlink_rejections 15; removed_guard_regression_failures 9; native_full_checkout NOT_RUN; original_generator NOT_RUN; github_actions NOT_RUN. The pinned checker is distributed inside research/validation/R272_P0_FAILCLOSED_CANDIDATE_20261102.zip and must be extracted and SHA256 checked before use.

## Scientific interpretation and open acceptance conditions

This is internal nonblind finite artificial E1 program assurance. No new human E2, historical E3, real-world predictive evaluation, or external independent team replication. The current wrapper correctly rejects the tested five corrupted-byte and five linked-input cases. The new separate regression detects deletion of the three identity guards. No historical archived result, frozen protocol, generator, original workflow or other track was changed.

R272 production P0 remains OPEN: obtain an authentic complete checkout; run --root and --regenerate in ordinary and optimized modes; verify archive preimages before any emit, compare isolated regeneration, and make the independent gate mandatory in the actual workflow with appropriate path triggers. The current workflow still runs --emit before archive checking and uses assert; this run did not edit or execute it. The original historical CI success remains historical evidence only.

original239 queue: 154 pending, P0=27, P1=82, P2=45; formal net closure 0. R127's bounded acceptance recommendation is not silently adopted. R257 S53 historical blind-order failure and R333–R340 composite caller gaps remain open.

## A data, coordination, cost and next

Reviewed research/data_scout/A_DF2011_R074_PRIOR_DECODE_AND_SOURCE_DUPLICATE_STATUS_RECONCILIATION_2026-11-01.md. DF2011's 7,358 rows were already decoded in an earlier fixed-blob audit; it belongs to the same Dal Bó and Fréchette 2011 original experiment as R074. It is ineligible as a newly independent R073 experiment. No new dataset was downloaded, qualified or scored; R073 and PESEN v0.1 stay frozen.

No paid paper, API, compute, service or GitHub Actions run was initiated. Actual account billing and free quota: NOT_VERIFIED. CI: NOT_RUN. The code was uploaded to main and its Git blob independently read back; this report is an incremental audit record. Next action: native full-checkout R272 preimage-first acceptance and production mandatory caller review, then P0 R333–R340 composite acceptance.
