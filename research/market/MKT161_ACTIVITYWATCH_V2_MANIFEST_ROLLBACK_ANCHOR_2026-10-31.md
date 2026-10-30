# MKT161 ActivityWatch v2 manifest rollback and external high water anchor

UTC 2026-10-30T22:24:50.922Z. Track market. Baseline main e5fbafa3c2bfd55ddd27323de2a8f1b4f690ba16. Target (market,ActivityWatch,aw-server-rust-fe353a66,v2-manifest-rollback-trust-anchor). Status COMPLETE_BOUNDED_SOURCE_AND_SYNTHETIC_E1.

## First party evidence actually inspected
Pinned upstream commit fe353a66ca3859231ce306a0f4faf15f732d8b41, manifest.rs blob a67f9033b3a304c0443e069dea51923541624244 and segment.rs blob ff96977f17d59776af03bb797d45c1326fcbd901:
https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/v2/manifest.rs
https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/v2/segment.rs
Official README: https://github.com/ActivityWatch/aw-server-rust/blob/master/aw-sync/README.md

The manifest holds format v, device identity, last written time, per bucket latest_generation, segment list and sealed segment compressed byte SHA256. load_or_default checks v <= MAX_V and validates the requested device path string, then deserializes the manifest. In the reviewed load path there is no external monotonic generation anchor, manifest signature or authenticated deletion epoch check. The writer reads latest_generation from the loaded manifest. A segment digest can detect a changed payload relative to a trusted digest; an older manifest together with its matching older segment can remain internally hash consistent. This is a structural rollback exposure of the reviewed format and trust assumptions, not a demonstrated production exploit. Atomic rename/fsync provide local write durability, not anti rollback authenticity.

## Product mechanism and boundaries
Inputs are local activity events with timestamps, durations, event IDs and JSON data. State is local bucket manifest plus compressed segment generations. Algorithm merges unsealed tail records by event ID and seals by age/size; no reviewed general deletion propagation. Goal is personal activity visualization and device synchronization. Feedback is observational dashboards; no verified decision quality or long horizon self correction. Public code provides implementation transparency, with no verified end user appeal process. Local first free/open source core; optional sync transport can depend on user chosen third party storage, which this run did not use or purchase. Data privacy depends on all copies and backups; a digest alone cannot prove deletion. V2 is experimental and not wired into a sync command in the reviewed README.

## Executed artificial test
research/market/mkt161_manifest_rollback_20261031.py executed with Python 3.13.5 standard library, 10 assertions PASS. SHA256 over two fictional event payloads demonstrates: current manifest plus current payload passes local digest and anchored check; stale manifest plus current payload fails local digest; stale manifest plus stale payload passes local digest; a separately retained trusted epoch 3 rejects the coordinated epoch 2 rollback. A stale trusted epoch 2 accepts it. Format version remains 1 in both cases. This is a deliberately simplified E1 model without zstd, actual Rust, signatures, storage compromise, device communication or real deletion.

Candidate future requirements: separately trusted high water epoch, signed/authenticated manifest provenance, explicit deletion epochs and tombstones, backup scope inventory, UNKNOWN when anchor or replica inventory is missing. These are design candidates, not verified ActivityWatch controls or a request to implement a personal decision product.

Evidence levels: upstream implementation code supports structural statements; official README supports experimental status; artificial E1 supports only the constructed examples. Independent security audit NOT_RUN, native Rust NOT_RUN, real user outcomes NOT_RUN. New E2=0, E3=0. No additional costs, paid API, CI or user data.
