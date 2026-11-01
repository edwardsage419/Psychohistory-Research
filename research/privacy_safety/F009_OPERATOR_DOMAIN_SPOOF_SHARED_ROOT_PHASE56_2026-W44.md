# F009 phase56: claimed operator independence versus shared infrastructure roots
Date: 2026-11-01 UTC, W44. Track: privacy_safety. Key: (privacy_safety,F009,phase56,operator-label-spoof-and-common-root). Baseline main: f3c827a1a72af27b60f041d1f3e2f57a5a8b1537. Status: COMPLETE_BOUNDED.

## Original public sources
Sigstore official threat model https://docs.sigstore.dev/about/threat-model/ describes signer and identity provider compromise. RFC 9162 https://www.rfc-editor.org/rfc/rfc9162.html covers consistency across log views. W3C VC 2.0 https://www.w3.org/TR/vc-data-model/ discusses issuer validation, status and correlation risks. None proves that real witness operators have independent hardware, keys, cloud administration or software.

## New mechanism beyond phase55
Phase55 assumed three witness slots with two sharing one declared operator. Phase56 examines four distinct organizational labels with only three infrastructure roots, including two labels sharing CLOUD_X. Candidate policy additionally requires an authenticated current map of organization labels to root-control domains. Spoofed labels or stale trust mapping are insufficient evidence. Three independent roots for REVIEW_ONLY is an illustrative conservative candidate threshold, not a standard mandate or calibrated quorum.

## Synthetic exhaustive test
Script research/privacy_safety/f009_phase56_operator_shared_root_20261101.py enumerates all 3^4=81 ordered four-slot VALID/REVOKED/MISSING states. Python stdlib, 12 assertions PASS. REVIEW_ONLY=3, REJECT=15, CONFLICT_QUARANTINE=50, UNKNOWN_QUARANTINE=13. Naive two-valid vote rule accepts eight states rejected or isolated by the independent-root policy. ORG_A and ORG_B both VALID while others missing shares CLOUD_X and yields UNKNOWN. A/C/D VALID spans three assumed roots and allows human review. Any VALID/REVOKED split is quarantined. Unauthenticated operator metadata or stale map returns UNKNOWN even if labels appear diverse. Automatic high-impact restoration=0.

These 81 cases are an artificial universe, not attack frequencies. The script takes root labels as assumptions, performs no real identity proof, signatures, infrastructure discovery or compromise measurement. Distinct organizations can still share hidden administrators or dependencies.

## Candidate privacy/safety controls
Maintain a local versioned operator-to-root evidence register; separate organization name, signing key, hosting account, admin control and software dependency. Check current issuer authority, key validity and signature independently of witness count. Preserve UNKNOWN and appeal, refuse automatic high-impact restoration, minimize identifiers in witness queries, and specify retention/erasure. No personal data, accounts or product. NONBLIND synthetic E1 only; E2=0, E3=0. No new paid operations.
Next phase57: trust-map key rotation and delayed revocation under offline rollback.
