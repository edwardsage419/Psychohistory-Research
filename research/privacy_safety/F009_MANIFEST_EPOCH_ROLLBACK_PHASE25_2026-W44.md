# F009 phase25 deletion epoch persistence across restored manifests

UTC 2026-10-30T22:24:50.922Z. Track privacy_safety. Baseline main e5fbafa3c2bfd55ddd27323de2a8f1b4f690ba16. Target (privacy_safety,F009,phase25,coordinated-epoch-rollback-and-trusted-anchor). COMPLETE_BOUNDED_STANDARDS_SYNTHETIC_E1.

## English primary standards and implementation references
NIST SP 800-88 Rev. 2 final, September 26 2025: https://csrc.nist.gov/pubs/sp/800/88/r2/final . This covers media sanitization program and assurance, not a mandated manifest epoch protocol.
OWASP Cryptographic Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html . It warns that encryption by itself supplies limited replay protection and that a separate unique message identity check may be required.
ActivityWatch pinned v2 manifest.rs and segment.rs at fe353a66ca3859231ce306a0f4faf15f732d8b41, first party implementation for the scenario. MKT161 audits code structure; this phase focuses on a hypothetical future personal data deletion approval policy.

## Distinct policy question and actual E1 execution
Can all device acknowledgements, a tombstone, backup version and a manifest agree with one another while all are stale? A 5 field artificial binary grid uses epochs 2 and 3 for manifest, tombstone, two device acknowledgements and backup restoration, 32 combinations. A consistency only policy accepts two states: all 2 and all 3. A candidate rule additionally requiring independently retained trusted high water epoch 3 accepts only all 3. The fully rolled back bundle (2,2,2,2,2) is internally consistent but rejected by the anchored rule. The test runs research/privacy_safety/f009_phase25_epoch_rollback_20261031.py, Python 3.13.5 stdlib, 71 assertions PASS.

The counts are artificial enumeration counts, not attack frequencies. The independent anchor is assumed trustworthy in this exercise; key management, tamper resistance, backup erasure and user revocation are not demonstrated. Missing or compromised anchor must yield UNKNOWN and defer high impact completion claims.

## Candidate privacy and safety controls
Require explicit request scoped deletion epoch, authenticated replica and backup acknowledgements, independent monotonic high water evidence, restore time revalidation and narrowly retained audit fields. Keep an appeal channel and preserve legitimate processing restriction or legal hold review where applicable. Do not declare deletion complete from internally consistent stale receipts. Minimize identifiers and keep the anchor separate from sensitive event content.

No personal sensitive data, real devices, real cryptography, legal compliance testing, paid services or personal decision product. E1 synthetic only, new E2=0 and E3=0. Next: compare deletion epoch recovery after lost anchor and distinguish UNKNOWN from permanent rejection.
