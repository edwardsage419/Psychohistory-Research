# B-track nonblind independent audit: R333 S129 timed intervention

Date 2026-11-01 UTC. Key (b,R333,S129-v1,nonblind_complete_320_row_timing_audit). Status PASS_NONBLIND_INTERNAL_E1. Prior knowledge: R333 original protocol, code and published original results plus the S129 frozen design were read. No blind evaluation claim.

## Executed independent route
The standalone Python script `research/evidence_audit/b_r333_s129_independent_audit.py`, blob `0d1da176f9c9c858537892ae6fc4229c143af34f`, imports neither original R333 Python nor new R333 S129 JavaScript. It separately computes old-state synchronous XOR transitions and overwrites the intervention value at the selected time. Its complete reconstructed 320 CSV rows and 64 JSON worlds match the remote persisted blobs `ee36d676abe047c9fc1dbb0da4fa72baf115a8f5` and `e4381c6b8ea0b980214a94cad00ea586ccc24092`. Local Python normal and optimized (-O) executions both returned `PASS_NONBLIND_INTERNAL_E1: 64 worlds, 320 rows, 6 mutations rejected, legacy R333 byte identities PASS`.

The same independent script separately recreates the original R333 160-row CRLF CSV and 32-world pretty JSON with exact original Git blobs `8a202f773badb8833992ff0df25c3c90f60b3680` and `dd82e1f616528742622ebafc844ec66adadf18b5`. This verifies the tau=1 compatibility route at full byte identity, not only summary equality.

## Negative controls
Six real input corruptions were tested, checked non-no-op, and rejected: one missing CSV row, one duplicated CSV row, wrong intervention timing label, one Boolean state flip, a changed final-state world result, and false E2 identity. They cover both source and summary. This is one internal reviewer route with six mutations, not six independent scientific replications.

The exact remote archived primary JS source, blob `fa3cd41229c95a4230691d0de2a53d652806d4c0`, was executed under a V8 Node-module shim with actual remote CSV and JSON. It passed persisted byte replay; a deliberate CSV state mutation was rejected. Native Node CLI remains NOT_RUN.

## Scientific limits and open checks
All 320 rows are artificial E1, so participant leakage, group-held-out prediction, probability calibration, bootstrap uncertainty and empirical causal identification are NOT_APPLICABLE to this calculation. The two mechanism comparison and the do(B) intervention are fixed invented truth tables; human E2 and historical E3 are NOT_ESTABLISHED. Original R333 historical CI and acceptance unchanged. New CI and full regression NOT_RUN, external independent team NOT_RUN. GitHub free quota and billing NOT_VERIFIED. No paid API, runner or data source used. R073 and PESEN v0.1 remain frozen.
