# R333/R337/R338/R339 native optimized receipt P0, bounded scientific scope

Date: 2026-11-01 UTC
Track: R main and B independent-method verification
Baseline main at start: `41dcdfcf9bf35cb619f9033cd7d731312d6559b9`
Status: **COMPLETE for native P0 reproduction and additive strict checker; PARTIAL for mandatory production remediation**.
Evidence: same-operator nonblind engineering and finite artificial E1. Human E2, historical E3, and external-team reproduction: NOT_RUN.

## 1. P0 question and fixed scope

Previous R/B handoff left R333, R337, R338, R339 as static-only risks. This run examined all four frozen original Python scripts and their exact archived CSV/JSON receipts. Original scripts, frozen model logic, and prior acceptance records were left unchanged.

Each source was retrieved through the connected GitHub repository at current main and reconstructed locally. All four source files matched their repository Git blob SHA. The original render routines were executed in CPython 3.13.5 to regenerate eight complete receipts, each matching the repository Git blob exactly. Thus the native test input identity is established at the source and receipt level, with no claim of independent real-world validity.

Source SHA:
* R333 `c28c82a6a18ababe8da14b0f48c846d940bf32b3`
* R337 `96e9e2be1b7d7ac0ac7b3cfcf05c7c81e938090d`
* R338 `1ee4cff348278f208628358b626174fd5fcb5524`
* R339 `ed769df49658f345e78859f2be733b5b43322791`

## 2. Native negative controls

Four models times five input conditions times two Python modes times two checker programs = **80 native subprocess executions**. Each original was invoked with `--test --audit`. Each independent strict checker invocation was performed against the same isolated disposable directory. Conditions: valid receipts, single-byte CSV corruption, single-byte JSON corruption, both receipts missing, and source-only benign comment change. Every case ran in normal and `-O` optimized mode.

| Condition | Original normal | Original optimized | Strict gate normal and optimized |
| --- | --- | --- | --- |
| Valid source and receipts | PASS | PASS | PASS |
| Corrupted CSV | FAIL | FALSE PASS | FAIL |
| Corrupted JSON | FAIL | FALSE PASS | FAIL |
| Both receipts missing | FAIL | FALSE PASS | FAIL |
| Source comment only | PASS | PASS | FAIL |

The original optimized checker falsely accepted all three receipt failures for each model, **12 observed false accepts**. The strict checker rejected **32 of 32** negative cases, including source identity mutations, in both modes. All 40 paired scenario records matched their predeclared expected statuses. Original tests were run together with audit, showing the tests themselves can report success even when optimized audit assertions are elided.

The failure mechanism is explicit: each original `audit()` uses bare `assert` for persisted receipt equality. Python optimization strips these assertions. A successful original optimized replay therefore cannot be used as the sole integrity acceptance gate.

## 3. Additive fail-closed gate

`research/evidence_audit/r333_r337_r338_r339_strict_gate_20261101.py` checks fixed Git blob identity for source and both receipts, rejects missing/changed bytes and duplicate JSON keys, and independently enumerates the finite constructed mathematics and complete CSV/JSON semantics for all four models. It does not import any audited implementation. Explicit exceptions remain active under Python optimization.

The test harness is `research/evidence_audit/test_r333_r337_r338_r339_native_20261101.py`. It resolves original sources from `research/R333`, `research/R337`, `research/R338`, and `research/R339`, and creates only disposable copies for mutation. A full local execution log exists separately. The repository machine matrix contains the 40 observed paired status records and counts.

Independent formula implementation is **same-operator, nonblind method-level replication**. Pinned source identity also means a future legitimate source change requires a new explicit review and a new gate version; the old gate must not silently accept changed inputs.

## 4. Scientific interpretation and remaining gates

The eight-model static-risk cluster from R333 through R340 has now been tested for the four previously pending candidates, following earlier native confirmation for R334/R335/R336/R340. All eight original optimized receipt entry points are confirmed affected in the bounded conditions. No actual historical tampering was detected. Frozen artificial results remain distinguishable from the ability of an original checker to validate persisted receipts.

Production remediation remains **PARTIAL** because the frozen original entry points are preserved and the additive gate has not been adopted as a mandatory acceptance dependency. Any E1 grade upgrade must require fail-closed source/receipt identity and independent mathematical checks. Python 3.11/3.12 native replay, a unified mandatory gate, external-team replication, human E2 prediction, and historical E3 prediction remain **NOT_RUN**.

The original239 v7.8 crosswalk and the 154-row pending triage file were read at this baseline; neither was edited. No itemwise scientific completion was claimed. Codex R257 S53 PR #1/#3 remains separate draft evidence until merged and independently accepted. R073 and PESEN v0.1 remain frozen.

## 5. A source scout and resource boundary

A reviewed the existing DF2011 stratEst source gate and its documented `treatment/id/game/period/choice/other.choice` fields. Original binary row decoding, participant continuity, licensing and NV_games overlap checks remain open. No new independently qualified R073 cohort or E2 score was created. Existing A registry was retained without duplicate write.

Environment: CPython 3.13.5 standard library. No random sampling. No GitHub Actions triggered. GitHub account billing and remaining free quota were not independently checked. No paid services or private data used.

Next: make the strict checker a mandatory, versioned scientific acceptance dependency without rewriting frozen sources, and address the existing itemwise P0 queue and Codex PR #3 merge gates after review.