# MKT160 ActivityWatch v2 manifest and open-tail version boundary
UTC 2026-10-30T21:21:17.526Z. Track market. Baseline c6b24827faab5bbc2618e79bfc267547787e7c5b. Target (market,ActivityWatch,aw-server-rust-fe353a66,v2-manifest-tail-seal-no-tombstone). COMPLETE_BOUNDED_SOURCE_SYNTHETIC_E1.

## Original English sources actually read
ActivityWatch official 2026-10-06 article https://activitywatch.net/blog/syncing-your-activitywatch-devices/ and sync documentation https://docs.activitywatch.net/en/latest/syncing.html.
Pinned upstream commit fe353a66ca3859231ce306a0f4faf15f732d8b41:
https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/v2/manifest.rs blob a67f9033b3a304c0443e069dea51923541624244;
https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/v2/segment.rs blob ff96977f17d59776af03bb797d45c1326fcbd901;
https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/v2/mod.rs blob a76aaad2f987ef720579da9b6e01c14ae2935aa6;
Cargo.toml blob e250a8b312901d4bca5acd794e3a55e00c7c9cae; pinned aw-sync README.
Directly read manifest.rs, segment.rs writer/merge logic, mod.rs and Cargo feature declaration. No Rust execution.

## Data, state, algorithm, goals, feedback, privacy and cost
Input: activity bucket, timestamp, duration, event ID and JSON data. State: device_id, hostname, manifest format version, bucket metadata, generation-indexed segment list, sealed flag, event count, timestamp bounds, compressed-byte SHA256 and first-written time. Bucket slug is first 16 hex chars of SHA256(bucket ID). Compressed JSONL header plus events is written to a temp file then renamed. A segment is sealed when compressed size reaches 1 MiB or its generation is at least one day old. An unsealed tail is rewritten under the SAME generation after merging events by ID, newer value wins. Events without IDs remain unkeyed. Manifest explicitly says segment SHA256 is authoritative only when sealed. Once sealed, older generation stays; new events enter a new generation. Empty input returns without change. The segment header has `replaces` but writer always sets null; range replacement is reserved. No deletion tombstone or general deletion propagation is implemented in reviewed writer paths. Manifest version guard refuses v>MAX_V=1 and validates path-unsafe device IDs.

Official source explicitly describes v2 as experimental and feature-gated `sync-v2`; the writer is not connected to commands. Current v0.14 sync also lacks deletion propagation. The v2 design is not a deployed security control.

Goal: personal activity tracking and multi-device visualization, no verified improvement in personal decisions. Feedback: activity event observations, sync status and visualization, no demonstrated automated self-correction of life decisions. Privacy: local-first and user-chosen sync folder; third-party provider transport possible; old copies and backups persist without explicit erasure. Explainability: public code, no tested end-user appeal path. Price: free open-source core; optional storage/provider cost excluded; no purchase, signup or data transmission. Evidence is first-party implementation and marketing documentation, without independent user outcome evaluation.

## Executed bounded synthetic demonstration
`research/market/mkt160_v2_open_tail_seal_synthetic_20261031.js` was run in V8 with 13 assertions PASS. It models same-generation tail edits, sealed next generation, empty input preserving historical data, absent replace marker, and old-snapshot restore. This is a simplified artificial E1 model, omitting zstd, real Rust, importer, device transport and cryptography. No production exploit is asserted.

Candidate future controls: version manifest and tail content separately; verify sealed hashes; explicit authenticated tombstones and scope-aware restore; enumerate replicas before erasure completion; retain UNKNOWN when inventory incomplete. No personal decision product, no fixed life utility weights. New E2=0, E3=0.
