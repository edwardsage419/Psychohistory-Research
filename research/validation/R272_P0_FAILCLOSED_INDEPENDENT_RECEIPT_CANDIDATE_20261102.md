# R272 P0 independent fail-closed archived receipt candidate

Date: 2026-11-02 Asia/Singapore. Track: R main, B independent scientific validation. Original239: 12-002. Initial observed main: f31835745437f4aa42a5c3c05c66c7cd9fbbfcfc. Status: COMPLETE for bounded native candidate and mutation tests; PARTIAL for actual production adoption; original P0 OPEN.

## Target and frozen evidence

The original R272 generator uses mandatory scientific Python assert guards. Prior archived-source injection proved ordinary Python rejects three corruptions while optimized Python accepts and emits affirmative claims. This candidate is a separate fail-closed verification program. It imports none of the archived R272 implementation, preserves the historical failure evidence, and does not edit frozen sources, original receipts, or workflows.

Pinned original source Git blob: 13843eecf2f9f05c19ee5545bdb224f58313f367.
Pinned prescore protocol Git blob: 9fbdb0078a58c4a9c0a548643227e30da5731119.
Freeze commit: 52f84dbfbe8563cf5c9a491e67d5e320223e0a56.
Pinned archived CSV SHA256: dc40ed773491817caf242ba6416e1bdf98ef2f1a2cd05e1956bdf5aec5801663.
Pinned archived JSON SHA256: f891df1c4640c2f49a457c436bc043f6bc08b768ac92594050e7e08061495a40.

## Actual executed work

A new standard-library-only Python independent checker was written and run under CPython 3.13.5 in normal and optimized mode. It uses unconditional ValueError checks, independent six-bit source enumeration, Fraction arithmetic, analytical Binomial(4,p) training expectations, future Brier expectations, exact log-loss infinity event probabilities, complete row identity and 15-column validation, nine world result checks, receipt identity, duplicate JSON-key rejection, strict JSON number and Boolean type comparison, archived byte SHA256 pins, and original source/protocol Git blob pins. The checker does not call or import the original generator.

The independent synthetic construction produced a CSV of 576 source rows and 61,489 bytes whose SHA256 exactly equals the archived CSV SHA256. Re-serializing the independently constructed nine-world JSON with the archived generator's documented JSON formatting produced the exact archived JSON SHA256. An independently reconstructed receipt referencing these byte-identical payloads passed the checker with archive pins enabled: 576 rows, nine worlds, 8,640 field values and two receipt hashes. This is byte-equivalent reconstruction, not a direct read of the complete repository files through the local Python runtime.

Native self-tests were run twice:
* python r272_failclosed_independent_receipt_gate_20261102.py --self-test: 1 positive, 11 mutations rejected, PASS.
* python -O r272_failclosed_independent_receipt_gate_20261102.py --self-test: 1 positive, 11 mutations rejected, PASS.

Mutation controls update receipt hashes where appropriate to avoid hash-only rejection. They cover probability mass, duplicate six-bit source, training/test identity corruption, test Brier corruption, false E2 claim, Boolean substitution for integer E2, false analytical verification flag, removed world results, receipt identity corruption, duplicate JSON key, and float substitution for integer receipt count. No random seed was used.

## Artifact and usage

The source file is archived inside research/validation/R272_P0_FAILCLOSED_CANDIDATE_20261102.zip as r272_failclosed_independent_receipt_gate_20261102.py. The ZIP was created with deterministic zip -X metadata stripping and has SHA256 f23b04706b60ac70bdbee6f051a74551779fb9d9a9b9af08c96cda345b055151 and Git blob 0da0436968db92056f08d14682e55f3f878f4314.

To run after extracting in the repository validation directory:
```
python research/validation/r272_failclosed_independent_receipt_gate_20261102.py --self-test
python -O research/validation/r272_failclosed_independent_receipt_gate_20261102.py --self-test
python research/validation/r272_failclosed_independent_receipt_gate_20261102.py --root .
python -O research/validation/r272_failclosed_independent_receipt_gate_20261102.py --root .
```
The final two complete-checkout commands have not been executed. The script's default root is inferred as two parents above its extracted location. The ZIP is an archival transport format; extraction is necessary for invocation.

## Scientific scope and remaining P0 closure

Internal nonblind finite artificial E1 independent program audit only. No new E2 human experiment, E3 history, external-team independent replication, or new model scoring. The original optimized-mode false-acceptance defect remains present in the original generator. The candidate is not wired into any production caller or CI workflow, and it does not prove the original generator actually executed its claimed oracle at historical runtime. A separate independent checker can establish the mathematical truth of archived claims but cannot retroactively prove an internal execution trace.

Before P0 closure: extract and execute the gate against the actual complete checkout with both interpreter modes; preserve stdout/stderr and exit codes; run native corrupted archived CSV/JSON/receipt cases; obtain separate authorized fail-closed production caller adoption and review workflow path triggers; preserve original failed tests and frozen history. Do not alter original generator or claim historical CI falsification without evidence.

The latest original239 v7.8 crosswalk and pending-154 file were re-read from main at initial head; the itemwise queue was not changed, so net reduction is zero. Codex PR #1 and #3 remain open and address R257 S53; no overlap with this candidate. R073 and PESEN v0.1 remain frozen. A public-data scout directory was inspected without obtaining a newly qualified frozen R073 dataset. No GitHub Actions or paid API was triggered; actual account billing and free allowance were not independently verified.
