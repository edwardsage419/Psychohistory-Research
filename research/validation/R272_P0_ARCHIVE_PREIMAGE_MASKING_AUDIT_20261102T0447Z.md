# R272 P0: archived-input trigger bypass and regeneration-before-verification audit

Date UTC: 2026-11-02T04:47Z. Track: R main and B independent scientific verification.
Target key: (R+B,R272,2026-10-23 frozen 12-002,archived-input preimage trigger and destructive regeneration).
Initial main HEAD: 27480453997f01b0a4737a67fa36bcf9b7aa1980.
Main immediately before this report: c79c019a5cc99549b0d7722e903bb8e6d051d1be.
Status: COMPLETE_STATIC_SCOPE_AND_SYNTHETIC_NEGATIVE / PRODUCTION_P0_OPEN.
No original R272 code, freeze, workflow, historical receipts, or original239 queue modified.

## New risk and exact remote evidence

Read the actual GitHub main workflow at .github/workflows/r272-exact-train-test-oos-e1.yml, Git blob 3132b08cf4ee64b55f5112d2249894ea0ec9d42d, and original generator research/R272/r272_exact_train_test_prediction.py, Git blob 13843eecf2f9f05c19ee5545bdb224f58313f367. The current push.paths list contains exactly two paths: the generator and its own workflow YAML. Direct exact-path comparison against these two paths gives:

| Changed path on its own | R272 push workflow eligible by path filter |
| --- | --- |
| Original source CSV | NO |
| Original result JSON | NO |
| Original machine receipt JSON | NO |
| Archived independent candidate ZIP in research/validation | NO |
| Original generator Python | YES |
| R272 workflow YAML | YES |

This is a separate archived-input trigger coverage defect, in addition to the previously recorded absence of a mandatory independent checker call.

The archive job first runs `python research/R272/r272_exact_train_test_prediction.py --emit`. The subsequent inline auditor reads CSV/JSON/receipt from disk. Source inspection confirms emit() writes all three archive files: src.open("w"), jp.write_text(...), and R272_MACHINE_RECEIPT.json.write_text(...). The workflow has contents: write permission and can git add/commit/push the regenerated files. The inline audit also uses Python assert. Thus, when a workflow does run, its scientific audit observes freshly generated artifacts after a potentially destructive write. It does not separately authenticate the three files that were present in the checked-out commit before regeneration. An archive-only change does not match this workflow's push path filter. Manual dispatch has the same regeneration-before-read order.

This is a source-level reachability and temporal-order finding. No real historical CI false acceptance, malicious Git commit, or historical data corruption was observed. Regeneration can yield correct mathematical results while masking an already-corrupt preimage.

## Actual local negative controls

Execution environment: container CPython 3, standard library only, deterministic inputs; random seed N/A. A local uploaded R272 fail-closed candidate was run with --self-test under normal Python, -O and -OO. Each returned 1 positive control and 11 correctly rejected mutations, total 33 mutation rejections across modes. This is re-execution of existing tests, not 33 independent scientific claims.

New read-only diagnostic: research/validation/r272_archive_preimage_gate_audit_20261102.py. Seven unittest controls passed in ordinary mode and seven under -O. Tests cover archive-only push exclusion, source/workflow positive triggers, emit-before-read order, missing mandatory candidate call, a proposed widened path filter, read-before-emit order, and missing YAML structure. The seven unit tests use a small constructed workflow fixture, while the actual main workflow and source were separately read and checked directly through the GitHub connector. Native --root execution of this diagnostic against a complete checkout is NOT_RUN.

A separate disposable synthetic R272 fixture was corrupted by duplicating a six-bit source identity and updating its receipt SHA256. The existing independent candidate rejected the corrupted preimage with 'source identity or field-level mathematics differs'. Replacing the three files with regenerated correct fixture bytes then produced PASS. Corrupt CSV SHA256: 6a6e0b5374ccbea883dce908b367a667166947bbafbbb73999ed21b4897f6785. Regenerated CSV SHA256: dc40ed773491817caf242ba6416e1bdf98ef2f1a2cd05e1956bdf5aec5801663. This is a synthetic order-of-operations demonstration, not execution of the actual archived generator or GitHub Actions.

## P0 acceptance conditions

1. Verify the checked-out archived CSV, result JSON, and receipt as read-only preimages before any --emit or other mutation; use fixed identity pins and the independent fail-closed checker in both normal and optimized Python.
2. In a separate disposable directory regenerate artifacts, verify those separately, then compare exact bytes and identities against the checked-out preimages. Preserve both on failure. No automatic overwrite of frozen historical evidence.
3. Include archive, candidate checker, source, protocol and caller paths in a reviewed mandatory verification trigger policy. Check actual path matching and failure propagation; account for manual dispatch.
4. Keep the archived original generator, historical CI, optimized-mode false-acceptance counterexamples, and frozen protocol unchanged. Production workflow modifications require separate review and confirmed no-extra-fee Actions policy. Do not trigger Actions before that confirmation.

## original239, A data, evidence, and coordination

Read original239 v7.8 crosswalk blob 36f24235901172642c46853298aebb421f1a3552 and current 154-row queue blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f. Counts P0=27, P1=82, P2=45; R272 12-002 remains P0 and PROVISIONAL_PRIMARY_README_LINK. Net closed items 0. Twelve open Codex PRs checked; #1/#3 concern R257 S53 and remain unmerged. Recent theory and market main commits inspected. Existing R333 to R340 composite caller gap is already separately audited; no duplicate checker developed here.

A data: read the 2023 Romero and Rosokha Econometrica primary paper (DOI 10.3982/ECTA17482) and the author's official research page. Publisher lists 197 MB data-and-programs supplement, not downloaded. The author's 'Code for this experiment' GitHub link currently returns 404, while the coauthor's SFEM GitHub repository is publicly accessible and describes an example notebook. No participant-level file, data dictionary, licence, or R073 frozen eligibility verified. Candidate only, no new qualified R073 dataset or E2 score.

Evidence: INTERNAL_NONBLIND_FINITE_ARTIFICIAL_E1_PROGRAM_AUDIT only. New R E2=0; E3=0; external-team replication=0. R073 and PESEN v0.1 unchanged. No classification, fusion, or personal decision product work. No paid data/API/compute; no Actions triggered; account billing/free quota NOT_VERIFIED. CI NOT_RUN.

Next: native complete-checkout verification of the candidate --root path and archived preimage mutations, followed by independently reviewed mandatory preimage-first caller design. P0 remains OPEN.
