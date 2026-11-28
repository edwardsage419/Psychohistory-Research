# Serialized anchor advancement and client receipt gating
2026-11-28. Research baseline 46512d7d48eb1d0bd329073cf146ea3e1b62ec16; open draft/candidate PR list #63/#62/#61/#60/#59 (open status checked; draft status not independently checked for each). Read prior actual source anchor_crash_replay.py, policy_incremental.py, policy_integrated.py and policy_pruning.py; reviewed V08_COMPOSITION.md at candidate 734686980b19da9291bdd08b67d4e2519c011acf, blob a602867cb0ff640f3c585d6bb46890a27a6567bc. No product modification. This extends existing research, not a second production protocol.

## Actual runs
Container command python anchor_serial_client.py:
SQLite 3.46.1 storage (24, 24, 24, 48) client (72, 48, 24, 2)
Storage tuple = 24 double-process update trials, 24 real SIGKILL trials, 24 final frontiers and 48 stale requests (24 duplicate sequence, 24 wrong caller identity). Two verified SQLite journal modes, four existing selected mathematical inputs, three repeats; POSIX advisory flock across both stores. Launch two independent processes against the same identity and expected sequence zero; exactly one advances, other stale. No barrier to guarantee simultaneous wait. After wrong caller rejected, kill worker at after_intent, after_data_commit or before_anchor_commit for each repeat. Subsequent process obtains lock and recovery yields expected sequence 1 or 2. Continue all remaining records and check certificate frontier against analytic reference; integrity_check both stores. Existing reference frontier implementation is shared. Prior anchor_crash_replay.py rerun: SQLite 3.46.1 SIGKILL 48 frontiers 48 rollback_rejections 48. Regression only.
Core wrapper:
```python
@contextmanager
def exclusive(root):
    with open(root/'writer.lock','a+b') as f:
        fcntl.flock(f,fcntl.LOCK_EX)
        try: yield
        finally: fcntl.flock(f,fcntl.LOCK_UN)

def guarded(root, identity, expected, crash='none'):
    with exclusive(root):
        if recover(root)=='blocked': return 'blocked'
        with connect(root/'data') as db: x=checked(get(db))
        if x['identity']!=identity or x['seq']!=expected: return 'stale'
        if not x['pending']: return 'done'
        assert advance(root,crash)
        return 'advanced'
```
Requires a stable lock inode and all paths, including publication/revoke/restore/initialization in a future product, to cooperate. Existing functions callable without wrapper, not a security boundary against hostile processes. Single local filesystem, not network/distributed locks; no proof of trusted storage, dual-store rollback resistance, arbitrary process schedules, power-loss behavior or revocation under lock. Ordinary SQLite anchor assumed protected from rollback. No actual result publication integrated with this wrapper. No claim of resource performance.

## Client receipt protocol
Initial model: six scope fields, 72 constrained permutations of authority change, old receipt, new receipt and stale authority notification. Reject 48 stale receipt deliveries; naive last-delivery display ends stale in 24 schedules; guarded model zero. Two trivial unknown-state checks are illustrative only.
Stronger actual executable run:
schedules 240 old_reject 150 early_reject 120 weak_final 60 negative_receipts 71
Script committed 55a33abc269a94a1c8f1789a47a441c5cf557e58, 2026-11-28-client-receipt-gate.py, Git blob 4fd0824fb387e0b6dd8f26863aa511790079e96f equal to local git hash-object and exact connector readback. Enumerates six fields x 40 orders of authority update, old receipt, new receipt, stale authority update and retry. Retry constrained after host update and first new receipt. All 240 guarded final displays correct; invariant current scope or empty after each event. Weak baseline accepts last delivered receipt and clears on host change, 60 final stale. Reject 150 old deliveries, 120 early new deliveries; 72 separate mode/epoch/generation/completeness combinations, 71 rejected and one legitimate accepted. Revocation, disconnect, conflicting same-generation notice clear display. New epoch/reconnect intentionally unsupported and requires fresh trusted handshake. Host updates assumed authenticated; complete flag in test is synthetic, real host must bind verified mathematical result, evidence, full dependencies, purpose, authorization and receipt authenticity. Client cannot detect unseen revocation or independently establish freshness while disconnected. Historical offline view needs separate explicit authority/status; no native UI, actual transport, cache or privacy deletion tested. Test scope six integer fields, developer-selected, not real user data or independent acceptance.

## Reproduction and archive
Conversation ZIP anchor_serial_client_research.zip SHA256 c8396cc7b8fa40b717e84de73c574441993743fd27dd4a591d138d4c6c6c618d; ZIP integrity tested. SHA256:
anchor_serial_client.py ef1692fc934d5bd09e3738cace21e82afcb5aa73b560b638d0ba7b5244ccea0c
client_receipt_gate.py df967164f64ff33414f6b796fd5a86c1def9f29a36cf9beb0c882bece3d0a8ae
anchor_crash_replay.py 67a19193a31cd9ad2023c8b22b5d6691582decb6a4407e477abb46290b327170
policy_incremental.py 52506764718c7146b710ea902d4b403fcabc05e661c78d65c194422c21b6190a
policy_integrated.py c70e172048c179e6275817c54f175a575c72b34dac4f83ca9e3e62e27b4cc895
policy_pruning.py adb58805158c6531dcd7cd46c02ad7f2c68fa4d06f6639b8d60792eed1059ef4
Only standalone client source and this report synchronized to GitHub, complete six-source bundle retained in conversation. Reuse existing manual integration index and prior delta at 46512d7; no cumulative independent counts. Unique recent handoff and repository-wide dedup not completed. No major development, training, merge, deployment or added cost.
