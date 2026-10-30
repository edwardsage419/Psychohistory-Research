# F009 phase20: repeated appeal, retention extension and fair review

UTC 2026-10-30. Track privacy_safety. Target (privacy_safety,F009,phase20,repeated-appeal-retention-reset-and-individual-review). Status COMPLETE_BOUNDED_PRIMARY_REGULATOR_GUIDANCE_AND_SYNTHETIC_E1.

## Original English guidance and scope
UK Information Commissioner's Office right-of-access guidance, updated 2025-12-08, https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/right-of-access/when-can-we-consider-a-sar-to-be-manifestly-unfounded-or-excessive/ states that repeat requests are not automatically excessive, and each case requires contextual assessment and supporting evidence. This source concerns UK subject access requests, not a general global legal rule for private account appeals. The ICO right-to-restrict-processing page https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-restrict-processing/ reinforces individual review and contextual assessment. OWASP logging https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html and ICO retention guidance provide general background for minimising sensitive event records. No private account data, emails, real complainants or real retention records accessed.

## Actual finite test
Python 3 standard-library script research/privacy_safety/f009_phase20_repeat_appeal_retention_20261031.py executed locally. Enumerated all 4^4=256 artificial event sequences at relative days 5,12,20,29. Event types NONE, REPEAT, NEW_EVIDENCE, APPROVED_HOLD. Base illustrative retention deadline day30; explicit illustrative human-approved hold deadline day45. These are arbitrary model parameters, not a statutory or NIST retention requirement.

A naive rule extends deadline to t+30 whenever any appeal event arrives. It extends retention in 255/256 sequences and yields deadline day59 after four repeated appeals. The candidate rule preserves day30 unless an explicit APPROVED_HOLD event exists, in which case it sets day45. Under the 256 fixed artificial sequences, 175 have such approval. New evidence and repeat events both enter contextual review; neither automatically extends the deadline or triggers automatic denial. 1285 assertions PASS. This is a finite synthetic control comparison, not an estimate of actual malicious appeal frequency or compliance certification.

## Candidate controls and risk register
1. Separate case identity, evidence identity, and approved retention authority. Duplicate evidence may be deduplicated for storage while the new request is still assessed on its own merits.
2. Maintain bounded, reviewable hold authorisation with purpose, approver, expiry, and ability to contest. An unresolved legally justified restriction may require separate legal analysis before deletion.
3. Preserve appeal access and human review. No blanket refusal, no automated finding of abuse based on repeat count, and no predetermined fixed legal retention duration.
4. Retain minimal structured reason and provenance, isolate personal identifiers, and review backup copies. Reject sensitive tokens or unrelated user information in audit fields.
5. Unknown legal basis, jurisdiction, or conflicting deletion obligation requires human legal review and UNKNOWN status; do not auto-delete necessary legal evidence or hold indefinitely.

Evidence level PRIMARY_REGULATOR_GUIDANCE + INTERNAL_NONBLIND_SYNTHETIC_E1. Real identity, encryption, abuse detection, actual deletion, and legal compliance NOT_TESTED. No new E2 or E3. No paid service or CI. Weekly F009 research remains active. Next phase21: appeal escalation and conflicting erasure/restriction requests with bounded unknown states.