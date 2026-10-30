# B track: R283 S79 exact PMF and persisted-receipt audit
Date UTC: 2026-10-30. Status: COMPLETE internal nonblind mathematical and persisted-byte check; archived native CLI and external-team replication OPEN. Target: (B,R283,S79-v1,27-cell-independent-PMF-and-mutations).
Previously read: original R283 report, original Python source, original exact receipt and frozen design, plus S79 protocol and generated results. This is NOT blind replication.

## Distinct mathematical route
R route: full 64 six-bit treatment/control source enumeration per regime, 192 total. B route: only 27 triples of three-valued study risk differences per regime, with probabilities P(d=-1)=(1-pT)pC, P(d=0)=pTpC+(1-pT)(1-pC), P(d=1)=pT(1-pC). Independently computes Q using the fixed oracle weights and aggregates the complete rational PMF. No import of original R283 or S79 R implementation. All three full PMFs, expected Q, P(Q=0), P(Q>=6) agree exactly. Each 64-source universe checked, original six-bit source mass and Q recomputed, 192 unique rows checked.

## Negative controls executed locally
Six distinct mutation cases each rejected: duplicate source, missing source, changed original mass, changed Q, E1 falsely changed to E3, altered tail-probability receipt. Local command `python /mnt/data/r283_s79_b_audit.py /mnt/data/r283_s79_out` exited successfully with output `PASS: 192 original source rows; 3 independent 27-cell PMFs; 6/6 mutations rejected`. A functionally equivalent standalone audit script is archived at `research/evidence_audit/B_R283_S79_INDEPENDENT_27_CELL_AUDIT.py`; exact archived bytes have not been run as a native CLI.

## Persistence verification
Actual remote fetched CSV Git blob `9e087a230ab8085dfae28a12c9e0017f95062092` and JSON Git blob `94e615904aaafac1ad47127da26783c3e52fddf3`. Local six-bit Python regenerated CSV and JSON with the same Git blob identities, including complete byte serialization. Remote CSV contains 192 rows, 64 per regime. JSON carries the prescore freeze commit `d6a072305ed28a12d987cf148f5f53b3eaeb3262` and `E1_ARTIFICIAL_NONBLIND`. Exact results: homogeneous Q>=6 is 135/2048, balanced 41/256, reversal 455/2048. The fixed threshold is descriptive; no real statistical significance claim.

## Evidence boundary
Original R283 E1 closed-bounded status unchanged; S79 is a bounded nonblind internal E1 extension. This does not test real-world heterogeneity, real published study selection, external replicability or real E2/E3 predictive performance. No Actions dispatched; CI NOT_RUN and free billing quota NOT_VERIFIED. R073/PESEN v0.1 frozen.
Next: execute exact remote archived R and B scripts with native Python, then separately inspect R284 existing study-selection evidence and avoid duplicate work.
