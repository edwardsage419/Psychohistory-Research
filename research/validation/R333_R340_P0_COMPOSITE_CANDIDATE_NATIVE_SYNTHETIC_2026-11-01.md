# R333 to R340 composite E1 acceptance dependency: candidate implementation and native synthetic controls

UTC date: 2026-11-01. Track: R with B scientific audit. Initial observed main: `c0f5a2253de1416476276770c9270d5e71913ffc`. Status: **PARTIAL_P0_OPEN**.

## Frozen problem and inputs

Eight historical R333 to R340 finite artificial E1 studies have verified conditional Python `-O` false acceptance in their original receipt checkers. The already archived mathematical entry `research/evidence_audit/r333_r340_acceptance_entry_20261101.py` has Git blob `9822418253c6a2888119c2a823ffee62dd945d7c`. The separately archived historical claim gate `research/evidence_audit/r333_r340_claim_receipt_gate_20261101.js` has Git blob `add869ed3c8dc3f9eb39d91fb836ac9df5eb307f`. Their source and archived evidence remain unchanged.

This stage adds a candidate caller `research/evidence_audit/r333_r340_composite_acceptance_20261101.py`. It authenticates both exact gate source blobs before execution, requires all eight model identities, executes the Node historical claim gate, then runs the Python mathematical entry in ordinary and `-O` isolated interpreter modes. It requires successful exit, no stderr, a single duplicate-key-free JSON object, correct E1-only status, eight-model coverage and claimed child check counts. The ordinary and optimized mathematical receipts must agree. Failure of any component prevents the composite PASS.

The caller deliberately reports `PASS_COMPOSITE_CANDIDATE_E1_ONLY` and `production_adoption=NOT_ESTABLISHED`. This program is not yet a mandatory trusted entrypoint for all production or historical acceptance paths. Its CLI uses the fixed two-source pins. Its `verify(..., pins=...)` injection exists solely for synthetic tests; production callers must use the pinned CLI or separately authenticate this composite source.

## Actually executed work

Local environment: CPython 3.13.5 and Node.js v22.16.0. Standard libraries only; no randomness. `python test_r333_r340_composite_acceptance_20261101.py` passed **14/14** tests. `python -O test_r333_r340_composite_acceptance_20261101.py` passed **14/14** tests. Two tests launched actual local Node/Python child processes against generated synthetic scripts. The other twelve exercised source pins, symlink rejection, duplicate JSON keys, bad statuses, missing models, evidence grade promotion, ordinary/optimized disagreement, child stderr and optimized-only failure. A separate CLI negative control with an incomplete local checkout returned exit 1, `COMPOSITE_ACCEPTANCE_FAIL: unsafe audit directory`.

These tests use synthetic gate scripts and receipts. The **authentic full repository native run remains NOT_RUN** because the local execution container cannot resolve github.com and a complete original checkout was unavailable. No authentic eight-model 16-child mathematical run or original claim-gate native run occurred in this stage. No actual historical receipt was changed. Historical CI and previous E1 finite results are unchanged. No external team reproduction, independent human E2 prediction or historical E3 validation occurred.

Source identity of locally tested code and the remote uploaded files:
* Composite: `104beae6d60e4df8e879841567ca08c4088438a4`.
* Tests: `82a91d28966fede09808456571d35096e5d16222`.

## Coordination and queue

Main crosswalk: `docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.8_2026-10-25.json`, blob `36f24235901172642c46853298aebb421f1a3552`. Pending itemwise queue: `docs/ORIGINAL_239_PENDING_154_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-25.csv`, blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`. Recount: 154 pending, P0 27, P1 82, P2 45. Net closed: 0. Twelve Codex PRs were open at initial read; PR #1 and #3 for R257 S53 remained unmerged. No Codex PR content was adopted or overwritten.

A-track brief scan considered publicly indexed repeated Prisoner's Dilemma sources. The Montero 2022 Dryad study and DF2011 already have prior lineage records; no new dataset was obtained, scored or qualified for the frozen R073 test. R073 and PESEN v0.1 stay frozen.

## Remaining P0 conditions

1. Obtain a complete trusted read-only checkout and execute this exact pinned composite CLI against all authentic archived files. Preserve full stdout/stderr, interpreter versions, exit status and source/receipt blob identities.
2. On isolated copies, mutate one of the 16 historical claim files and one mathematical receipt separately, and prove the composite rejects both while the old optimized checker can still falsely pass its documented counterexample.
3. Independently review and authorize the mandatory production caller binding, including authentication of this composite script itself. Until then the original optimized false-accept P0 remains OPEN.
4. Continue the R127 original239 itemwise protocol adjudication and review R257 S53 PR #3 source identity and coverage before scientific closure.

GitHub Actions were not triggered. New CI: NOT_RUN. No paid API, runner, cloud, GPU, data purchase or subscription used. GitHub account billing and remaining free quota: NOT_VERIFIED. This stage makes no E2, E3 or MARKET evidence claim.
