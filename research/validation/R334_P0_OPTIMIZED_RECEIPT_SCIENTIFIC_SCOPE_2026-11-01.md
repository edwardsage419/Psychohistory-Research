# R334 P0 audit: optimized Python suppresses archived receipt checks

Date: 2026-11-01 UTC. Track: R. Scientific state: PARTIAL_P0_REMEDIATION. Scope: frozen R334 finite constructed E1 induced-compliance experiment, original239 03-011. This is a post-hoc nonblind execution integrity review, with no new S number, no model refit, no empirical E2/E3 evidence and no revision of the 2026-10-24 prescore freeze.

## Provenance and reproducible observation

Pinned original source: `research/R334/r334_dissonance.py`, Git blob `7d232a07d9d2979c2fcc8a407dd8bda18cd8ab93`. Pinned archived CSV blob `6e3bdcc5ca07d1321a651c29b899798a32f7fb72`; JSON blob `02883b6b9cfc22b3b855d8a7cbaa5e5ddf6bd86c`. All three identities were independently checked against the current main file metadata, and the pinned original source reproduced both archived receipt blobs exactly.

The original `audit()` function uses Python `assert` for every archived CSV/JSON byte identity test and all finite falsifier checks. Under `python -O`, those statements are removed by the interpreter. The CLI still prints `R334 PRODUCTION_REPLAY_PASS`. Its `unittest` suite also reports five passing tests because the receipt-specific `test_byte_replay` invokes that same disabled `audit()`. The other four tests operate on internally generated states and do not inspect persisted receipt files.

On local CPython 3.13.5, the exact pinned source was run in isolated temporary directories. Original CLI with `--test --audit` returned exit 0 and reported five passing tests in optimized mode when the archived CSV was corrupted, when the JSON was corrupted, and when both files were deleted. Normal interpreter mode rejected all three. The original CLI also lacks source-file identity authentication: appending one newline to the source leaves its computations intact and both original CLI modes accept it. These are execution-gate counterexamples, not claims that the original scientific data were corrupted.

## Independent bounded gate

Added a no-import strict gate at `research/evidence_audit/r334_strict_receipt_gate_20261101.py`. It checks three pinned Git blobs, complete 48-row CSV order and arithmetic, all 16 JSON conditions, frozen falsifier counts and duplicate JSON keys using explicit exceptions. The original source and receipts remain unchanged. It is an additive reviewer tool; the existing R334 production entrypoint has not been replaced.

The companion regression `research/evidence_audit/test_r334_optimized_gate_20261101.py` verifies the clean case and four negative controls under normal and optimized interpreter modes. Both new gate modes reject all four negative controls. This test suite uses the original pinned source to create baseline bytes, so it is nonblind; the strict gate itself independently reconstructs the mathematical content without importing that source. The result is a program-integrity check for this finite E1 receipt, not an external replication.

## Acceptance impact and remaining work

Historical [R334 CI run 40051279908](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40051279908) is confirmed completed/success on 2026-10-24. Its documented Python 3.11/3.12 jobs used normal execution. This new conditional optimized-mode flaw does not retrospectively prove that archived E1 calculations are wrong. It shows that optimized execution of the original receipt verifier can produce a false acceptance and should not be used as a scientific evidence gate.

P0 remediation status: **PARTIAL**. A separate strict verifier and regression are archived; a formal decision to integrate the guard into the original CLI, plus cross-version native replay in Python 3.11/3.12 and independent review, remains OPEN. Keep the original frozen protocol, source, receipts, historical CI and any failure evidence unchanged. Do not upgrade R334 beyond its bounded constructed E1 scope.

R073 and PESEN v0.1 remain frozen. original239 v7.8 and its 154-item provisional itemwise queue are unchanged. Codex PR #1/#3 R257 S53 remains an independent OPEN_UNMERGED P0 topic, not addressed by this R334 gate. No paid resources or Actions were triggered.
