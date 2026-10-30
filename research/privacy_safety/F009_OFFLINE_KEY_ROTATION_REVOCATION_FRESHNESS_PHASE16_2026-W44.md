# F009 phase16 offline key rotation and revocation freshness uncertainty

UTC 2026-10-30, ISO week W44. Track privacy_safety. Target (privacy_safety,F009,phase16,offline-key-epoch-and-revocation-freshness). Status COMPLETE_BOUNDED_STANDARD_PLUS_ARTIFICIAL_E1.

## Primary standards and applicability

NIST SP 800-63B-4, published 2025-08-01, https://pages.nist.gov/800-63-4/sp800-63b.html covers authenticator invalidation, compromised keys and account binding. IETF RFC 6960, June 2013, https://www.rfc-editor.org/info/rfc6960/ defines OCSP certificate-status freshness with thisUpdate and nextUpdate; stale nextUpdate responses should be considered unreliable. OCSP specifically concerns X.509 certificate status. Applying its freshness logic to future personal-decision evidence issuer keys is a candidate analogy, not an RFC requirement for that application.

## Artificial executable test

research/privacy_safety/f009_phase16_revocation_freshness_20261030.js executed locally with Node: 144 artificial states, 250 assertions PASS. States cross key epoch CURRENT/REVOKED/UNKNOWN, revocation GOOD/REVOKED/UNKNOWN, status freshness FRESH/STALE, and three assumed Boolean oracles signatureVerified/accountBound/nonceUnused. Artificial policy yields 136 REJECT, 7 DEFER_UNKNOWN, 1 REVIEWABLE_SOURCE_CLAIM. A mathematically valid signature under a known revoked old key is rejected. A fresh signature with unknown key epoch is deferred. A formerly good but stale revocation receipt is deferred. REVIEWABLE_SOURCE_CLAIM only permits subsequent human review; it does not certify factual truth.

The state variables are pre-assumed truth values. Actual cryptographic signature checks, key ownership verification, online OCSP requests, nonce store, offline device tests, account data, and real revocation latency measurement are all NOT_RUN. The 144 counts are policy state-space counts, not attack probabilities or compliance measurements.

## Candidate safeguards and risks

Record issuer key reference, key epoch, trusted revocation authority and last verified status timestamp, signed event digest, nonce/sequence and account-binding reference with purpose-limited retention. When offline status is stale or unavailable, mark UNKNOWN and defer high-impact automatic actions; allow human appeal and explicit revalidation. When confirmed revoked, reject affected signatures even if their mathematical signature verifies. Avoid publishing private keys, raw identity tokens, email, health or financial records. Potential costs: offline false denials, delayed recovery and availability tradeoffs; need future jurisdictional review and usability evaluation. No universal risk utility weights or product implementation. Evidence STANDARD_PRIMARY and INTERNAL_NONBLIND_ARTIFICIAL_E1; E2/E3 new 0. Next F phase17: reconcile user challenge, safe offline review and data retention without keeping unnecessary sensitive identifiers.
