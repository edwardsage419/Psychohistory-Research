# R333 S129: intervention timing and delayed reciprocal feedback

Date 2026-11-01 UTC. Scientific grade PARTIAL_E1_EXTENSION. Original R333 bounded E1 acceptance unchanged.

## Frozen protocol and original source
The S129 protocol was committed first, before new numerical results, at `01a0852d2c3e9ebe7bb84f427368a383dea3d943`: `protocols/R333_S129_INTERVENTION_TIMING_PERSISTENCE_PRESCORE_FREEZE_2026-11-01.md`. Original R333 protocol blob f66b8437f63bce079a7f10a0b8b82311dbdc64a4; original Python solver blob c28c82a6a18ababe8da14b0f48c846d940bf32b3. Bandura (1989), DOI 10.1037/0003-066X.44.9.1175, and Bandura (2001), DOI 10.1146/annurev.psych.52.1.1, motivate the general research question but do not specify these artificial equations.

Two invented mechanisms share P'=P XOR E, B'=P XOR B. Cyclic has E'=B XOR E; feedforward has E'=E. The intervention overwrites B at t=1 or t=2 after the synchronous update for that time. All eight initial P,B,E states, two do values, two times and two mechanisms are fully enumerated through t=4.

## Full results
64 worlds and 320 time-indexed artificial rows. For each fixed mechanism, initial triple and intervention time, compare d=0 versus d=1. All counts below are out of eight initial triples.

| Mechanism | Intervention time | E at t+1 differs | P at t+2 differs | P4 differs | B4 differs | E4 differs |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| cyclic | 1 | 8 | 8 | 8 | 0 | 8 |
| cyclic | 2 | 8 | 8 | 8 | 8 | 0 |
| feedforward | 1 | 0 | 0 | 0 | 8 | 0 |
| feedforward | 2 | 0 | 0 | 0 | 8 | 0 |

This is a precise finite counterexample to treating an endpoint-only observation as a time-invariant test of feedback. At t=4, cyclic E is sensitive to the t=1 behavior intervention but insensitive to the t=2 intervention; cyclic B shows the opposite pattern. The delayed P4 contrast is present for both timings in cyclic and absent in feedforward. At fixed intervention d, changing timing changes P4,B4,E4 in eight of sixteen cyclic world comparisons each, and only B4 in eight of sixteen feedforward comparisons. These are structural properties of the invented XOR transition rules.

## Original compatibility and complete receipts
Independent Python reconstruction of original tau=1 R333 source recovered its original full CSV Git blob `8a202f773badb8833992ff0df25c3c90f60b3680` (4,298 bytes, 160 rows) and original complete JSON blob `dd82e1f616528742622ebafc844ec66adadf18b5` (6,193 bytes, 32 worlds). Thus the new tau=1 case preserves all original source bytes and exact world results under the original serializer.

New S129 artifacts:
* `research/validation/r333_s129_timed_intervention.js`, blob `fa3cd41229c95a4230691d0de2a53d652806d4c0`.
* `research/validation/R333_S129_ALL_320_TIMED_TRIADIC_STATES.csv`, blob `ee36d676abe047c9fc1dbb0da4fa72baf115a8f5`, 8,874 bytes.
* `research/validation/R333_S129_EXACT_64_TIMED_TRIADIC_WORLDS.json`, blob `e4381c6b8ea0b980214a94cad00ea586ccc24092`, 8,703 bytes.

Remote exact JavaScript source executed in a V8 Node-compatible shim against the remote persisted CSV/JSON: PASS. An altered CSV state cell was rejected. Independent Python standard-library auditor reconstructed all 320 rows and 64 worlds, with identical complete Git blob identities. Six live mutations were rejected in both ordinary and optimized Python modes. See `research/evidence_audit/b_r333_s129_independent_audit.py` and B addendum.

## Scientific and execution boundaries
These are exhaustive E1 artificial Boolean worlds. The imposed intervention is a software operation, not a randomized human treatment. No human E2, historical E3, real-world agency identification, out-of-sample prediction, calibration, resampling, or external independent team. Native Node CLI, new GitHub Actions and full repository regression are NOT_RUN. Historical R333 CI is separate. The result changes no original R333, R073 or PESEN v0.1 files or scientific statuses. Continue R series next with R334 after live HEAD check. Classification, fusion and personal decision system remain paused.
