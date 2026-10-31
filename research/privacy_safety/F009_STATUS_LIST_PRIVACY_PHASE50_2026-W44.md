# F009 phase50 privacy-preserving revocation status and recovery
Date: 2026-11-01 Asia/Singapore, week 2026-W44. Track F. Baseline main 90fef6727b1d17662d82c10a3e924a1aff01ed98.
Target: (privacy_safety,F009,phase50,bitstring-revocation-group-privacy-freshness). Status COMPLETE_BOUNDED_STANDARDS_AND_SYNTHETIC_E1.

## Primary sources and versions
W3C Bitstring Status List v1.0 Recommendation 2025-05-15: https://www.w3.org/TR/vc-bitstring-status-list/
W3C v1.1 Working Draft 2026-10-21: https://www.w3.org/TR/vc-bitstring-status-list/all/ (draft is not a finalized Recommendation).
NIST SP 800-63B-4: https://pages.nist.gov/800-63-4/sp800-63b.html
The W3C Recommendation specifies at least 131072 status bits (16 KiB uncompressed) and discusses group privacy, cache, correlatable global identifiers, issuer tracking, stale status, and status-list authority. StatusListIndex links credential to status. The published bitstring can be holder-provided and cached; signature validity alone cannot establish current nonrevocation. The minimum list capacity does not imply 131072 actual issued credentials or anonymity for a single issued credential. A malicious issuer could create one list per credential. W3C privacy advice is a design input, not a legal-compliance certification.

## Executed artificial counterexamples
Script: research/privacy_safety/f009_phase50_status_list_privacy_20261101.js. V8 executed 11 assertions PASS. Eight deterministic candidate status cases: clean evidence -> REVIEW_ONLY, stale/unavailable status -> UNKNOWN_QUARANTINE, revoked/deletion-unsafe -> REJECT, untrusted issuer/wrong account -> UNKNOWN_QUARANTINE, no request -> NO_REQUEST. Three additional privacy checks use a 131072-slot list with only one actually issued credential; anonymity upper bound is one and a stable index shared with two verifiers remains linkable. These are artificial stipulated inputs and no real credential, digital signature, W3C bitstring parser, zero-knowledge proof or network system was tested.

## Candidate controls and limits
Prefer local cached, authenticated status list with bounded freshness; separate original credential issuer, status authority, account binding, status epoch and deletion ledger; unknown or stale status stays quarantined; never automatically restore sensitive data; allow manual review and appeal. Avoid one-person lists, persistent cross-verifier indexes and issuer request logs; use randomized allocation, limited retention and periodic reissuance only after evaluating traceability. Preserve only the minimum needed revocation evidence, with a documented expiry and erasure pathway. The 131072 bit count is a list capacity, not a guarantee of privacy. Recovery-status application is a future project analogy; W3C v1.0 governs verifiable credentials, not this unbuilt personal decision system.

Evidence: official W3C Recommendation and newer draft, official NIST standard, internally executed nonblind synthetic E1. No real cryptographic proof, external independent replication, real personal data, empirical E2/E3 or implementation. No new fees, paid services, CI or cloud compute. Next: examine the privacy versus freshness tradeoff for offline status verification and signed historical snapshots.
