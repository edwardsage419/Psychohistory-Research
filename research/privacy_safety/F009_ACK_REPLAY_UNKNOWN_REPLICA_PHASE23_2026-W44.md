# F009 phase23: replayed erasure acknowledgements and unknown replicas
Date UTC 2026-10-30T20:19:45.924Z. Track privacy_safety. Baseline main 17205cdf71c4d78cc2a5d077c47f19d6a4c0f3e6.
Target (privacy_safety,F009,phase23,stale-acknowledgement-and-incomplete-replica-inventory).
Status COMPLETE_BOUNDED_STANDARD_REVIEW_AND_SYNTHETIC_E1.

## Public English standards and boundaries
NIST SP 800-63B-4 (final July 2025) replay resistance: https://pages.nist.gov/800-63-4/sp800-63b/authenticators/ . Authentication nonces and freshness prevent reuse of old authenticator outputs. This standard governs authentication, and does not itself prescribe erasure receipts; the proposed application to deletion acknowledgements is a research analogy.
OWASP Webhook Security Cheat Sheet replay section: https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html . Signed timestamps and authenticated event IDs can help prevent duplicate/replayed processing; implementation choices depend on threat model.
ActivityWatch official sync article 2026-10-06 https://activitywatch.net/blog/syncing-your-activitywatch-devices/ documents replicas and missing deletion propagation. UK ICO right to erasure guidance https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/ is under review; legal applicability remains case-specific.

## Finite synthetic evaluation
Script research/privacy_safety/f009_phase23_ack_replay_unknown_replica_20261031.js executed in V8. Grid: two fictional device acknowledgements each FRESH/STALE/MISSING, replica inventory COMPLETE/UNKNOWN, backups CLEARED/PENDING, authentication assumed TRUE/FALSE, restore PENDING/FALSE. 144 artificial states, 152 assertions PASS. Naive rule accepting any nonmissing device ACK accepted 64; strict candidate requiring both fresh and complete inventory, backup cleared, authenticated ACK and no restore accepted 1. 63 naive-accepted states failed the stricter candidate. These grid counts are not attack probabilities, legal findings or production security test results.
A previously valid revision-1 ACK replayed for a revision-2 request can be accepted by a presence-only rule. The candidate strict policy requires ACK binding to request ID, subject scope, device identity, monotonic revision and fresh challenge; completeness requires explicit inventory confidence. Missing devices or stale offline acknowledgements remain UNKNOWN/PENDING. No real signatures, devices, backup erasure, network calls or personal data used.

## Candidate controls
F23-01 version-bound acknowledgements with replay detection and revocation.
F23-02 distinguish verified known replicas from undiscovered/unregistered devices; do not claim universal deletion when inventory incomplete.
F23-03 preserve a minimal appeal/exception path without retaining sensitive content indefinitely.
F23-04 replay deletion instructions after authorized restore and confirm new epoch acknowledgements.
F23-05 require human review before any high-impact irreversible action, retain provenance and uncertainty.
No personal decision product implementation. E1 synthetic only; new E2/E3=0. Next phase24 evaluate delayed device re-enrollment and restore-time scope mismatch with a separate candidate policy.
