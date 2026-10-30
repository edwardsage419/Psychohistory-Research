# MKT159: ActivityWatch owner-originated edits, cursor and deletion boundary
Date UTC: 2026-10-30T20:19:45.924Z. Track market. Baseline main 17205cdf71c4d78cc2a5d077c47f19d6a4c0f3e6.
Target (market,ActivityWatch,aw-server-rust-fe353a66,owner-reconciliation-identity-lookback-and-full-deletion).
Status COMPLETE_BOUNDED_UPSTREAM_SOURCE_AND_SYNTHETIC_E1.

## Primary English evidence and actual read scope
1. ActivityWatch official 2026-10-06 sync article: https://activitywatch.net/blog/syncing-your-activitywatch-devices/
2. Official syncing documentation: https://docs.activitywatch.net/en/latest/syncing.html
3. ActivityWatch/aw-server-rust commit fe353a66ca3859231ce306a0f4faf15f732d8b41, aw-sync/src/sync.rs Git blob 1daffa82dec2efe877923f4789bc8c4c897b5c95. Directly read lines 770 to 1250, especially reconcile_updated_events at 942 to 1064 and sync_one 1066 onward.
4. Same upstream commit aw-sync/tests/historical_edit.rs Git blob 59e03794395d7d78cded8c70b8c9531b5398439c. Directly inspected test names and lines 398 to 462.
Official article and Rust source are upstream developer evidence, not an independently executed native Rust test.

## Verified implementation mechanism
Input: per-bucket activity events (timestamp, duration, JSON data) and device-origin buckets. State: source owner datastore, destination replica, destination newest-event-end resume cursor, event identity (timestamp, duration). Algorithm: reconcile_updated_events scans source and destination over [resume minus 7 days, resume), grouping by identity; matching payloads are kept, changed payloads are inserted before stale destination IDs are deleted. The separate incremental sync_one path copies newer events. Seven days is anchored to the destination resume cursor, not simply wall-clock age. Full deletion of an identity produces no source group, so the reconciliation loop has no corresponding deletion instruction. When one of several same-identity siblings remains, the group reconciliation can prune unmatched siblings. This limited side effect is not a general deletion propagation contract. The upstream historical_edit.rs test explicitly covers older-than-lookback edits and fresh destination rebuild.
Feedback and goals: tracked activity/category visualization, no demonstrated improvement of personal decisions. Privacy: local-first, optional sync folder copies, provider-cloud transport possible, deletion propagation absent. Explainability: source code and status command, no verified user-facing appeal system. Cost: free core MPL-2.0; optional paid support and provider services excluded. No registration, purchase or data sharing performed.

## Bounded executable model
Script research/market/mkt159_aw_sync_reconcile_synthetic_20261031.js executed in JavaScript V8 with 9/9 explicit assertions PASS. Cases: recent edit, older-than-lookback edit, complete identity deletion, partial same-identity sibling removal, source-only identity, duration identity, destination-cursor anchor, idempotence, cursor boundary. The script models only the final multiset of the reconciliation branch. It omits Rust database semantics, query clipping, pagination, failures, actual device transport and cryptographic verification. Native Rust tests NOT_RUN. No claim of a newly discovered production exploit.

## Candidate future design controls and evidence boundary
Preserve owner/source provenance and versioned correction events; separate correction from deletion; inventory replicas; bind erasure to request scope and monotonic version; protect restore against stale copies; retain uncertainty for unknown replicas. These are candidate methods for later research, not product implementation. MARKET source code evidence plus synthetic nonblind E1; new human E2=0, historical E3=0.
Next: inspect upstream v2 segment manifest and versioned deletion proposals at pinned source, compare explicit tombstone semantics; avoid repeating MKT158.
