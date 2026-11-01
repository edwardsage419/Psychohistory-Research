# R333 through R340 P0: pinned eight-model acceptance dependency

Date: 2026-11-01 UTC. Track: R/B. Status: PARTIAL, production adoption pending.

## Problem and frozen boundary

Eight frozen original finite-E1 generators/checkers R333 through R340 were previously shown by native negative controls to accept corrupted or absent receipts under CPython -O. Their original source files, receipts, frozen protocols and historical failure evidence remain unchanged. This work introduces one additive, fail-closed **candidate acceptance entrypoint**. Its existence in main does not make it mandatory for older callers, CI, or historical scientific acceptance.

Baseline main observed before write: 6278989bf7c957a3ecac54d458127c60bf5cbd6c.
Original239 v7.8 crosswalk blob: 36f24235901172642c46853298aebb421f1a3552.
Pending itemwise queue blob: 3b96d46b3d88ccafd779a08509c3cfd0e435772f.
Directly counted queue: 154 rows (P0 27, P1 82, P2 45). Net queue closure: 0.

## Acceptance contract and trust boundary

Entrypoint: research/evidence_audit/r333_r340_acceptance_entry_20261101.py

Run on a trusted checkout, with Python standard library:

    python research/evidence_audit/r333_r340_acceptance_entry_20261101.py
    python -O research/evidence_audit/r333_r340_acceptance_entry_20261101.py

The CLI fixes the full eight-model universe. It authenticates the four underlying strict validator script blobs against constants, then invokes each model in both normal and optimized isolated Python modes, 16 subprocesses in total. It requires a zero exit status, no stderr, and an exact success receipt. Any missing model directory, validator mismatch, missing/corrupt original source or receipt, finite-E1 arithmetic mismatch, nonzero subprocess, timeout, spoofed stdout or incomplete universe must fail closed. The underlying authenticated strict validators independently pin each original source, CSV and JSON and recompute bounded mathematical results. A caller must authenticate the entrypoint itself from a trusted main commit or a separately pinned Git blob. This entrypoint cannot authenticate its own bytes.

At initial archive:
  entrypoint Git blob: 9822418253c6a2888119c2a823ffee62dd945d7c
  pinned R333/R337/R338/R339 validator blob: fce37d846c96598f491a155be684c3b009f7d7a0
  pinned R334 validator blob: bc025931c6bfaf3489ba3dcf91054a1e32fdaa29
  pinned R335 validator blob: 8c42c0e7f53a6ac855d295d0ee72c5618dc664d9
  pinned R336/R340 validator blob: bdd44dbc0422b1e4bd33b6bc5281e00227cce865

No assert is used to enforce acceptance checks. The entrypoint never invokes an original optimized-mode generator as its source of truth. All returned success grades are explicitly E1_ARTIFICIAL_ONLY. It does not evaluate empirical fit, out-of-sample prediction, E2, E3, external independent reproduction, or R073.

## Actual tests and limitations

Environment: local CPython 3.13.5 standard library; no RNG, no network, no third-party dependencies. The local entrypoint bytes were verified to match the remote Git blob 9822418253c6a2888119c2a823ffee62dd945d7c.

Synthetic fixture suite: 12 tests in ordinary mode, all PASS (executed in 4-test and 8-test batches); 12 tests in -O mode, all PASS. Positive fixture exercises all eight models in both child interpreter modes. Negative controls cover missing/corrupt receipt, missing model, missing or altered validator, validator symlink, shrinkage of mandatory universe, inconsistent shared validator pin, spoofed PASS stdout, and invalid JSON evidence grade. These tests use deliberately small mock validators with injected expected blobs. They verify orchestration and failure behavior only.

An initial all-in-one local unittest invocation exceeded its wall-clock limit; the suite was subsequently rerun in two ordinary-mode batches and one complete optimized-mode run, all passing. The local script was synchronized to the exact remote entrypoint blob before the final successful runs.

Real repository checkout with all eight original source/receipt directories and the archived four validators: native 16-subprocess end-to-end execution NOT_RUN in this environment. The GitHub connector was used to read the validator sources and Git blobs. A separate full native checkout replay is required before acceptance dependency can be adopted.

CI: NOT_RUN. No GitHub Actions triggered. Actual GitHub billing and free quota NOT_VERIFIED.

## A public data check

Rechecked upstream fdvorak/stratEst v1.1.8 DESCRIPTION and man/DF2011.Rd from English GitHub source. The manual explicitly defines "game" as supergame and "period" as period within that supergame; 7,358 rows and fields treatment, id, game, period, choice, other.choice. Package DESCRIPTION says GPL-3 and directs copyright details to a COPYRIGHTS file; the latter was not located in the inspected repository root. Dataset-specific reuse permission therefore remains UNRESOLVED. The binary DF2011.rda was not parsed. Prior NV_games source overlap and R073 frozen cohort eligibility remain UNKNOWN. No new E2 scoring, source promotion, or duplicate dataset registration.

## Coordination and next acceptance gates

The Codex R257 S53 PR #1 and PR #3 were directly checked and remain open draft/unmerged; their mathematical receipt and source authentication issues are separate. E165 operations handoff was read; E only monitors the P0 and does not own this R/B validator.

Next actions:
1. Obtain a complete read-only checkout at a verified main SHA and run this exact entrypoint in both parent modes; independently retain stdout, exit codes, validator source identities and original receipt identities.
2. Review adoption into an actual acceptance invocation with a trusted entrypoint pin and a mandatory failure dependency. Confirm this dependency cannot be bypassed by an older original checker PASS. Do not claim production remediation until a real caller enforces it.
3. Audit Codex PR #3 source authentication and historical blind-order status separately.
4. Resume original239 itemwise P0/P1 source evidence and frozen R073 external-data eligibility.

Scientific acceptance: PARTIAL. Original historical E1 claims and original scripts remain frozen. P0 optimized-mode false-accept risk remains open in unmodified production entrypoints.
