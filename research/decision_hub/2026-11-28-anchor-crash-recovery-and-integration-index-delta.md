# Two-store anchor crash recovery and integration index delta
2026-11-28. Baseline 31aa732d2676e9a439ddd0bde1aca875d2648b5d; open PRs #63/#62/#61/#60/#59. Governing v3.2 and sync workflow blobs 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85 and 26c4d946e48f01858fb8e8c2cb06e4f7ba91bf05 inspected at baseline. Earlier fixed index exists: 2026-11-28-manual-research-integration-index.md blob 812cd70402cb74d9554ee7385fc1107da1d3ca54. Do not replace historical index.

## Actual execution
Container Python: anchor_protocol.py => {'ready': 800, 'abort': 400, 'finalize': 400, 'blocked': 1200} total 2800; policy_rollback_probe.py => 504 504 504 504; anchor_crash_replay.py => SQLite 3.46.1 SIGKILL 48 frontiers 48 rollback_rejections 48.
Four selected inputs (0,1,2,0,0),(4,1,2,1,1),(2,2,1,3,0),(6,3,2,0,1); two SQLite stores each in actual verified DELETE or WAL mode, synchronous=FULL, six real subprocess SIGKILL boundaries. At each case check negative SIGKILL return code, expected recovery classification and sequence, idempotent second recovery, resume one record per advance, complete certificate and analytical frontier, integrity_check on both databases, restore old authenticated row and reject.
Protocol: anchor holds current MAC and pending MAC; data row holds canonical JSON with identity, seq, cursor, rows, and HMAC. Recover verifies data HMAC: if MAC equals current clear pending (abort or ready), else if equals pending finalize, otherwise blocked. Advance first recover, compute one new record with existing step, persist pending MAC, commit data, finalize anchor. Kill before intent => ready seq0; after intent or before data commit => abort seq0; after data commit or before anchor commit => finalize seq1; after anchor commit => ready seq1. No output may be published before anchor finalization.
This is an actual two-store recovery demonstration under single writer and anchor not rolled back assumptions. Two ordinary SQLite databases are not trusted hardware. Both-store rollback, concurrent writers, malicious anchor changes, backup recovery, power loss, actual result publication/client invalidation, and device resource costs are not validated. Data authentication uses fixed synthetic key. Frontier code shared with earlier verifier. No independent research or user outcome. Four inputs chosen by researcher and overlap existing cases. Earlier reports without directly observed execution must not be treated as independently verified by commit; only two previous scripts above actually rerun this round.

## Reproduction assets
Exact sources packaged in conversation anchor_recovery_research.zip; SHA256:
- anchor_crash_replay.py 67a19193a31cd9ad2023c8b22b5d6691582decb6a4407e477abb46290b327170
- anchor_protocol.py 56c7a3e709b36e9f941d3977c68fa3e072878c1434813a626bdf8593dabc5ef1
- policy_incremental.py 52506764718c7146b710ea902d4b403fcabc05e661c78d65c194422c21b6190a
- policy_integrated.py c70e172048c179e6275817c54f175a575c72b34dac4f83ca9e3e62e27b4cc895
- policy_pruning.py adb58805158c6531dcd7cd46c02ad7f2c68fa4d06f6639b8d60792eed1059ef4
Run python anchor_crash_replay.py on POSIX with Python standard library. Source bundle not uploaded to repository in this round; this report is the archive record, not source synchronization.

## Incremental research inventory
GitHub compare f2febd55946432f739112c70dcbb4aff4cba18bd -> 31aa732d2676e9a439ddd0bde1aca875d2648b5d: 18 commits, 18 decision_hub file paths returned. Path inventory, not per-file reread or proof of execution:
- 2026-11-28-authenticated-resource-frontier-persistence.md
- 2026-11-28-authenticated-sqlite-solver-replay.md
- 2026-11-28-certificate-transaction-publication.md
- 2026-11-28-information-policy-persistence-replay.md
- 2026-11-28-manual-research-integration-index.md
- 2026-11-28-persistence-execution-evidence-correction.md
- 2026-11-28-policy-atomic-incremental-advance.md
- 2026-11-28-policy-certificate-negative-controls.md
- 2026-11-28-policy-concurrent-revocation.md
- 2026-11-28-policy-guarded-incremental-advance.md
- 2026-11-28-policy-incremental-search-replay.md
- 2026-11-28-policy-pruning-coverage-replay.md
- 2026-11-28-policy-publication-identity-binding.md
- 2026-11-28-policy-publication-process-crash.md
- 2026-11-28-policy-rollback-probe.md
- 2026-11-28-sqlite-checkpoint-transaction-recovery.md
- 2026-11-28-sqlite-conditional-publication.md
- 2026-11-28-sqlite-sigkill-recovery.md
Integration grouping: resource/condition/frontier -> decision_resources and decision_composition; pruning/certificate/incremental -> bounded mathematical engine; identity/guarded advance/revocation/rollback/anchor -> host storage and transaction lifecycle; actual independent acceptance must verify raw natural language, qualified evidence, scope, full native route, real devices, cross-revision publication and privacy. No separate production protocol introduced. Unique product handoff and full repository dedup still unverified. No major development, training, PR merge, deployment or additional cost.
