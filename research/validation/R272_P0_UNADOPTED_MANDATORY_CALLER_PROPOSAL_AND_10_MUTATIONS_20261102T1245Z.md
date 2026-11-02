# R272 P0 mandatory caller adoption candidate and structural mutation audit

track: R+B
subflow: original239 12-002 / production scientific integrity
run_date_utc: 2026-11-02T12:45Z
starting_main: 91c604702ae49d842bda584c8a2429d78d1ae53c
frozen_protocol_blob: 9fbdb0078a58c4a9c0a548643227e30da5731119
original_workflow_blob: 3132b08cf4ee64b55f5112d2249894ea0ec9d42d
original239_crosswalk_blob: 36f24235901172642c46853298aebb421f1a3552
pending_queue_blob: 3b96d46b3d88ccafd779a08509c3cfd0e435772f
status: COMPLETE_STATIC_PROPOSAL / PRODUCTION_P0_OPEN
evidence: INTERNAL_NONBLIND_FINITE_ARTIFICIAL_E1_METHOD_AUDIT
ci: NOT_RUN
billing_checked: NOT_VERIFIED

## Current caller, actual evidence and scope

Read the current main, the original239 v7.8 and pending queue, R272 prescore freeze, original R272 workflow, pinned independent checker and wrapper, previous native replay, latest cross-track commits and all twelve open Codex PRs. PR #1 and #3 remain open for R257 S53, with no competing R272 adoption PR. The latest theory/market commits do not change R272.

The original production workflow remains unchanged and still (1) watches the original generator and workflow paths only; (2) has `permissions: contents: write`; (3) runs the generator's `--emit` before validating archived inputs; (4) uses `assert` inside its scientific audit; (5) never invokes the independent R272 checker or preimage-first wrapper; (6) can commit and push regenerated archives to main. The last three properties are observable in the workflow text. The known preimage masking and optimized-mode acceptance counterexamples remain relevant. Historical CI falsification is NOT established.

## New candidate, outside the executable Actions directory

File: `research/validation/r272_mandatory_acceptance_proposal_20261102.yml`

This is an intentionally unadopted proposal. It is outside `.github/workflows/`, so the proposal is not a registered GitHub Actions workflow. It preserves three named job roles, adds a mandatory preimage-first dependency, validates the historical ZIP SHA256 and member identity, invokes the pinned read-only wrapper in ordinary, -O and -OO modes, runs isolated regeneration and the existing native mutation regression, covers the source/protocol/archive/checker/wrapper/workflow input paths, removes automatic archive overwrites and repository writes, and makes the final job depend on both prerequisites. All positive claims are prospective until independently reviewed and adopted.

Candidate YAML Git blob: `fe7165cf0dfe1de12664ddfbcf4360b73c29a518`.
Candidate ZIP expected SHA256: `f23b04706b60ac70bdbee6f051a74551779fb9d9a9b9af08c96cda345b055151`.

## B independent structural tests actually executed

File: `research/validation/r272_proposed_caller_structural_gate_20261102.py`.
Script Git blob: `9121d9d873b364446e41e2dea5c765a9f1a2e827`.
Environment: local CPython 3.13.5, PyYAML 6.0.3. No random seed.

Command:

```sh
python research/validation/r272_proposed_caller_structural_gate_20261102.py research/validation/r272_mandatory_acceptance_proposal_20261102.yml --self-test
```

Actual result: PASS for the candidate and **10/10 deliberately altered candidates correctly rejected**. Mutations: remove source path trigger, grant repository write permission, remove each of the two job dependencies, remove -O, remove -OO, mark a step continue-on-error, reintroduce original --emit before validation, corrupt the ZIP identity constant, and remove mandatory native negative regression.

This is a bounded **static YAML structural guard**. It does not execute the candidate on GitHub Actions, does not prove shell semantics in every environment, does not prove the full historical repository preimage is authentic, and cannot independently attest branch protections or actions/checkout supply-chain identity. It also uses PyYAML for offline review only; the proposed workflow itself uses Python standard library.

## A data qualification delta

Read the original English openICPSR/AEA V1 deposit for Jeongbin Kim (2023), DOI 10.3886/E152261V1, including its `data_code/temp` file listing. The deposit exposes **12 session-named CSV files and 12 corresponding Stata files**, with individual CSV sizes about 316 to 668 KB; published V1 date 2023-01-25. Three treatments with four sessions each, 14 to 20 participants per session are described. This is a materially stronger file-availability observation than merely identifying a deposit page. Actual CSV bytes, variable names, participant/session keys, matching, repeated-game time semantics, reuse with existing R records, and license rights were not verified. No file was downloaded or scored. Candidate status only; new R073-qualified independent data = 0; new E2/E3 = 0.

Primary record: https://doi.org/10.3886/E152261V1
Session files: https://www.openicpsr.org/openicpsr/project/152261/version/V1/view?path=%2Fopenicpsr%2F152261%2Ffcr%3Aversions%2FV1%2Fdata_code%2Ftemp

## Production closure conditions

The candidate must receive independent review and be installed by an authorized workflow maintainer, preserving historical frozen results and failure evidence. Verify that the actual checkout's original archives are checked before any write, that every required gate failure blocks all scientific success claims, and that all relevant path changes trigger the gate. Recheck the exact ZIP membership and run on an authenticated full checkout in the intended Python 3.11/3.12 environments. Confirm GitHub Actions execution will incur no additional charges before enabling any trigger or dispatch. Review branch protection and independent caller identity. Only then consider closing R272 P0.

No current original239 row changed: queue remains 154 (P0 27, P1 82, P2 45); net formal closure 0. R257 S53 historical blind FAIL and R333–R340 caller risks are preserved. R073 and PESEN v0.1 remain frozen. No model classification, fusion or personal-decision implementation.
