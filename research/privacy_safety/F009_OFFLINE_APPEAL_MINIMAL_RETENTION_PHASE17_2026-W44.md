# F009 phase17 offline appeal, review availability and minimal retention

UTC 2026-10-30; ISO week W44. Track privacy_safety. Target (privacy_safety,F009,phase17,offline-appeal-review-channel-retention). Status COMPLETE_BOUNDED_STANDARD_PLUS_ARTIFICIAL_E1. Previous phase16 focused on key epoch and revocation freshness; this phase addresses the separate human review and data-retention tension.

## Original public sources and limits

NIST SP 800-63B-4, published 2025-08-01: https://pages.nist.gov/800-63-4/sp800-63b.html ; account recovery notifications, authenticator invalidation and privacy requirements. Privacy considerations: https://pages.nist.gov/800-63-4/sp800-63b/privacy/ ; records retention should be evaluated against privacy risks, with notice, redress and use limitation.
OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet ; access tokens, passwords, session IDs and sensitive personal data should normally be excluded or masked, sanitized, hashed or encrypted as appropriate. This is guidance, not an assurance that a hash renders personal data anonymous.

Neither source specifies the artificial decision tree, the 128-state distribution or a universal retention duration used here. Offline credential revocation freshness is treated as an uncertain input, not a verified cryptographic fact.

## Executed synthetic state-space and minimal receipt

File `research/privacy_safety/f009_phase17_offline_appeal_retention_20261030.js` executed in local Node 22.16.0: 128 Boolean combinations, 242 assertions PASS. Seven assumed flags: signatureValid, accountBound, retentionExpired, legalHold, revocationFresh, appealOpen and reviewChannel. Deterministic candidate policy counts:
* REJECT_SOURCE: 96
* PURGE_LIMITED: 8
* DEFER_REFRESH: 12
* DEFER_REVIEW: 3
* HUMAN_REVIEW: 3
* REVIEWABLE_ONLY: 6

These are counts of equally enumerated artificial configurations, not empirical probabilities or regulatory compliance rates. REJECT_SOURCE represents failed source/account checks. PURGE_LIMITED is the synthetic no-hold expiration path. DEFER_REFRESH requires fresh independent status. DEFER_REVIEW preserves appeal without silently authorizing high-impact action. HUMAN_REVIEW requires a review channel and fresh verified status. REVIEWABLE_ONLY never authorizes autonomous life decisions.

A purpose-limited receipt is restricted in the synthetic program to event_ref, status, purpose_code, review_due_day and retention_basis_code. Injected email, access_token and health fields are excluded by construction. A pseudonymous event_ref may still be personal information when linkable, so actual retention and deletion policy needs jurisdictional review. No real PII, passwords, keys, accounts, emails or devices were accessed.

## Risks and candidate safeguards

Key risk: a legitimate offline appeal can outlast revocation-status freshness or a retention deadline. Immediate erasure may destroy necessary dispute evidence, while indefinite retention can expose personal information. Candidate control: short purpose-limited review hold with a documented legal basis and review deadline, explicit UNKNOWN status, accessible human challenge channel, no automatic high-impact action while unresolved, and prompt deletion of unnecessary fields when hold ends. A legalHold Boolean is only a fictional input; it cannot establish lawful retention.

Future validation: actual user appeal usability, independent authentication and revocation evidence, data subject access/erasure behavior, retention law by jurisdiction, and realistic offline denial-of-service risks. No software product developed, no paid service used. Evidence: STANDARD_PRIMARY and INTERNAL_NONBLIND_ARTIFICIAL_E1. New E2=0; E3=0. Next F phase18: bounded review hold expiry and adversarial attempts to keep stale appeals open indefinitely.
