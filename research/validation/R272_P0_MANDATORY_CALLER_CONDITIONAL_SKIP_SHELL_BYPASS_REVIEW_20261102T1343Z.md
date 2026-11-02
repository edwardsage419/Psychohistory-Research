# R272 P0 candidate mandatory caller conditional skip and shell bypass review

Date: 2026-11-02 UTC. Track: R/B scientific verification. Status: PARTIAL. Acceptance: OPEN.

## Read scope and fixed identities

* Starting main HEAD: `fc8153cd97eba1e5133e831b868c77114de728eb`.
* Proposal `research/validation/r272_mandatory_acceptance_proposal_20261102.yml`, Git blob `fe7165cf0dfe1de12664ddfbcf4360b73c29a518`.
* Existing structural checker `research/validation/r272_proposed_caller_structural_gate_20261102.py`, Git blob `9121d9d873b364446e41e2dea5c765a9f1a2e827`.
* Active workflow `.github/workflows/r272-exact-train-test-oos-e1.yml`, Git blob `3132b08cf4ee64b55f5112d2249894ea0ec9d42d`.
* Freeze `protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md`, Git blob `9fbdb0078a58c4a9c0a548643227e30da5731119`.
* Original239 v7.8 crosswalk Git blob `36f24235901172642c46853298aebb421f1a3552`; current 154-row queue Git blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`. Reparsed 154 rows: P0=27, P1=82, P2=45. This is an administrative queue, not 154 scientifically unstudied models.
* Open PR #1 and #3 still concern R257 S53. They are unmerged and do not implement the R272 mandatory caller.

## New structural risk

The candidate workflow was previously reported as passing 10 structural mutations. The existing structural checker examines job dependencies, watched paths, permissions, literal command strings, ZIP hash, and `continue-on-error`. It does not inspect job-level or step-level `if` keys, nor custom step `shell` templates.

Six additive adversarial variants were constructed from the exact remote candidate YAML without deleting any required literal command:

1. Insert `if: ${{ false }}` on `preimage-first` job.
2. Insert the same conditional on its mandatory preimage audit step.
3. Insert it on the original 83-test step.
4. Insert it on the final archive verification job.
5. Insert it on all three jobs.
6. Insert `shell: bash {0}` on the multiline preimage audit step, removing default shell `-e` fail-fast behavior.

Connector-side JavaScript mutation inspection confirmed six nonempty modifications, preservation of existing required command literals, and absence of `if` / `shell` checks in the archived Python checker. The original checker CLI against the complete authentic checkout was NOT_RUN, so an observed count of original-checker false accepts is not claimed here. The source-level omissions establish a review gap. GitHub documentation specifies conditional job/step skipping and the difference between default `bash -e {0}` and a custom shell template.

## Independent control and bounded tests

Added `research/validation/r272_caller_skip_and_shell_mutation_review_20261102.py`. It loads the archived checker for comparison and independently rejects conditional jobs, conditional steps, ignored failures, and custom shell templates. It is a read-only candidate, not an adopted workflow or replacement of the original checker.

Local CPython + PyYAML 6.0.3: Python compile PASS; synthetic three-job fixture PASS; six mutations each correctly rejected by the new independent control (6/6). No random seed. Exact real proposal execution of the new Python review: NOT_RUN, because the complete checkout was unavailable in the local runtime. No Actions dispatch, no production CI result, no real human E2 or historical E3 prediction, and no external-team replication.

The previous 10 structural controls remain valid for the conditions they exercised. Their scope is incomplete for mandatory execution semantics. This is an unadopted proposal risk, not evidence of historical data falsification or an observed false-green production run.

## Required closure

Before adopting the candidate, require a full-checkout run of the new review and the original structural checker; confirm all six mutants fail the mandatory adoption gate. Review every job/step `if`, `shell`, `defaults.run.shell`, and error-suppression option. Preserve a red-to-green test receipt, exact source hashes, and actual command outputs. Independently verify preimage-first native replay, negative controls, and non-overwrite semantics. Only then consider installing a read-only workflow, subject to owner permissions and verified zero-cost CI eligibility. A passing static checker or successful GitHub workflow alone cannot upgrade the scientific E1/E2/E3 level.

## A public data check

Read the original English ICPSR registration for Kim (2023), DOI `10.3886/E152261V1`, version V1 published 2023-01-25. It describes three experimental treatments and four sessions per treatment, each with 14 to 20 participants. The present round did not download session files, establish independent participant/session identities, confirm reuse rights, or run frozen R073 scoring. New R073-qualified dataset: 0. Source: https://doi.org/10.3886/E152261V1 .

## State and costs

R272 P0 OPEN. R257 S53 historical blind failure retained. R333 to R340 production caller gaps remain open. R073 and PESEN v0.1 unchanged. Original239 queue net reduction 0. Existing active R272 workflow unchanged. No CI dispatched, no paid API, no purchase, no additional resource provisioning. Account billing and Actions free quota NOT_VERIFIED. No restricted data or personal information archived.

Next action: run this six-case review on a full authentic checkout and close the conditional skip/shell bypass before workflow adoption. After that, return to the higher-value original239 P1 itemwise and external R073 data qualification.
