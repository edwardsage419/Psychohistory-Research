# R333 to R340 P0: eight-workflow caller reachability audit

track: R+B
run_date_utc: 2026-11-01
observed_main: 6c4a1d5913b21dc85ed8aa1e8c5e37a6a0efa7d8
target_key: (R+B,R333-R340,2026-10-24-frozen-originals,mandatory-acceptance-caller-reachability)
status: COMPLETE_STATIC_SCOPE / PRODUCTION_P0_OPEN
native_full_checkout: NOT_RUN
CI: NOT_RUN
billing_checked: NOT_VERIFIED

## Question and source scope

Determine whether the eight existing original-model E1 GitHub Actions workflows actually call the newly archived composite acceptance entry `research/evidence_audit/r333_r340_composite_acceptance_20261101.py`, and whether edits to that entry are included in the workflows' push path filters. This is a read-only source-path audit, not a native execution, workflow run, or proof about every possible external caller.

Read the current main ref, the composite entry (Git blob `104beae6d60e4df8e879841567ca08c4088438a4`), its two pinned children (`9822418253c6a2888119c2a823ffee62dd945d7c` and `add869ed3c8dc3f9eb39d91fb836ac9df5eb307f`), the workflow directory, and all eight model E1 workflow files. Also checked open PR metadata; PR #1 and #3 remain open and concern R257 S53, not this target.

## Direct workflow evidence

| Model | Existing workflow under .github/workflows/ | Workflow Git blob |
| --- | --- | --- |
| R333 | r333-triadic-feedback-160-states-e1.yml | d53cbb4ec4aa881fe1f48317cc67c5058719f41f |
| R334 | r334-dissonance-48-atoms-e1.yml | 3282ceb368ccc3e1a270efd52d9c3c49ffcd8313 |
| R335 | r335-groupthink-384-atoms-e1.yml | 83eecdb05245142c25659714d40759fbc47cac35 |
| R336 | r336-inoculation-96-atoms-e1.yml | 3fe8d09ba1a5e9b88c91f6c16226b7fcd27a302e |
| R337 | r337-elm-64-atoms-e1.yml | 304166d968aab8d4b24ada8b34c637e2dc4ac2c1 |
| R338 | r338-relative-deprivation-128-atoms-e1.yml | 2157013cd1f755d191c46e346fb49544b9defcc8 |
| R339 | r339-social-comparison-100-atoms-e1.yml | 37ccef7b74a52c40d3623c870fba7be6752f1c1c |
| R340 | r340-sis-two-node-48-atoms-e1.yml | 231c454f017baf6925f6c61b0ecda1e139937f46 |

All eight declare three jobs: Python 3.11 original-model `--test --audit`, Python 3.12 original-model `--test --audit`, and an existing `research/catalogue_audit/independent_rXXX_*.py` audit. Their run commands contain no invocation of the composite entry, the new mathematical acceptance entry, or the new historical-claims gate. All eight `push.paths` filters include their model directory, their pre-existing catalogue independent audit file, and their own workflow YAML. None includes `research/evidence_audit/**` or the composite entry. All eight also declare `workflow_dispatch`, whose current commands remain the same.

Static counts for the inspected eight-workflow universe:
* Composite mandatory caller: 0/8.
* Composite entry in push path filter: 0/8.
* Original-model ordinary-mode commands: 16/16.
* Existing independent catalogue audit jobs: 8/8.
* Native composite invocations actually executed in this run: 0.

## Scientific consequence

The composite gate may pass its own synthetic unit tests while the eight existing workflows continue to report success without calling it. A change confined to the new gate files does not satisfy any of these eight workflows' declared push path filters. This is a **confirmed mandatory-caller adoption gap in these eight workflow definitions**. It does not prove that their historical CI results are mathematically false, that the independent catalogue audits are ineffective, or that every possible downstream caller is unprotected. Previous native mutation evidence for the original Python optimized-mode acceptance remains a separate finding. The new composite's full authentic checkout run and production binding remain unestablished.

The eight workflows currently use normal Python mode; the optimized-mode false-accept counterexample does not itself show an actual CI false acceptance in these jobs. E1 artificial evidence cannot be promoted to E2 or E3 from this review.

## Conditions before P0 closure

1. Obtain a trustworthy complete checkout at a fixed main commit and execute the pinned composite against real archived source, CSV, JSON, and 16 historical claim files. Retain stdout, stderr, exit codes, interpreter versions and source blob IDs.
2. Run separate native mutation controls against a mathematical CSV/JSON and a historical claim file; both must fail under ordinary and optimized Python modes.
3. Review and explicitly adopt a mandatory fail-closed caller with externally pinned composite entry identity, full eight-model universe, and required failure propagation. For a GitHub Actions path, audit every relevant trigger filter and dependency so edits to the composite and its children are included. A CI success must be impossible when the mandatory gate fails.
4. Preserve the old workflows and frozen evidence history. Any future workflow change requires a separate authorized review and confirmation of zero additional GitHub Actions charges before execution.
5. Independently review R257 S53 PR #3 source authentication and its distinct blind-order limitation. Do not merge this issue with R333 to R340.

## Limits and operational state

This run read the eight exact workflow source files via the connected GitHub repository, with their returned blob identities. No full local checkout, native composite execution, error injection, Actions dispatch, or external team replication occurred. Other possible external callers and organization-level branch rules were not exhaustively inspected. original239 crosswalk blob `36f24235901172642c46853298aebb421f1a3552`, pending queue blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`; queue change = 0, pending formal itemwise adjudication. R073 and PESEN v0.1 remain frozen. New E2/E3 = 0. No new paid operation requested; actual GitHub billing and remaining free quota not independently verified.
