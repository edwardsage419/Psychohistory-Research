# F009 phase22: cross-device erasure acknowledgements and backup restoration
UTC 2026-10-30. Track privacy_safety. Baseline main f65da166a2e6b7118d92d36910d3c8ce6316f895. Target (privacy_safety,F009,phase22,cross-device-ack-backup-inventory-and-restore-guard). Status COMPLETE_BOUNDED_REGULATOR_DOC_AND_SYNTHETIC_E1.

## Primary English sources
UK ICO Right to erasure https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/ read 2026-10-30 UTC. Valid requests without exemptions require steps regarding live and backup data, with clear explanation to the individual. Some backup data can remain until scheduled overwrite if placed beyond use; jurisdiction and facts matter. ICO guidance is under review following UK Data (Use and Access) Act.
ActivityWatch official 2026-10-06 https://activitywatch.net/blog/syncing-your-activitywatch-devices/ and pinned upstream aw-sync README Git blob 755b5e9ae11e11e96c43d88d75e1a3d4bde9d921 document replica copies and lack of deletion propagation. These are software-design examples, not proof of compliance or real-world deletion.

## Executed finite model
Native Python standard library research/privacy_safety/f009_phase22_cross_device_backup_ack_20261031.py, SHA256 97176463d29db0b26ccfcaab5edcdc8324046aa040d81fcd4cf6bfd1b339e95b, executed 1944 fictional states and 1960 assertions PASS. State grid: three devices each ACK/PENDING/UNREACHABLE (27), two backups each ERASED/QUARANTINED/LIVE (9), restore request boolean (2), legal hold boolean (2), acknowledgement authentication boolean (2).
Outcomes: REVIEW_LEGAL_BASIS 972; VERIFY_ACK_AUTHENTICITY 486; PENDING_DEVICE_ACK 468; PENDING_BACKUP_ERASURE 10; RESTRICTED_BACKUP_WAIT 6; RESTORE_BLOCKED 1; ALL_SCOPED_ACK_CANDIDATE 1. These counts are properties of an arbitrary uniform Cartesian test grid, not probabilities, legal categories or estimates of user risk. The candidate ALL_SCOPED_ACK state requires all three device ACK, both backups ERASED, authenticated acknowledgements, no restore request, no hold. Acknowledgement variables are assumed synthetic inputs; no cryptographic proof, true device inventory or actual deletion is verified. RESTORE_BLOCKED is a candidate workflow state, not evidence of physically blocked restore.

## Candidate control register
F22-01 inventory all known device and backup replicas, track source and scope of deletion.
F22-02 authenticate acknowledgement origin and bind it to request, subject scope and monotonically increasing revision.
F22-03 place pending backups beyond use and prevent unreviewed restore; replay scoped deletion/tombstone instructions after any authorized recovery.
F22-04 distinguish legal hold, processing restriction, pending deletion, backup expiry and verified actual erasure; permit appeal and human review.
F22-05 never infer universal deletion from a single device ACK or expired timer; account for offline and unregistered replicas.
No real user data, emails, cloud sync, cryptographic operations, actual legal assessment or product deployment. E1 synthetic only; new human E2=0, historical E3=0. No paid APIs, CI or purchases. Next F009 phase23: authenticated acknowledgement replay and missing replica discovery, still using fictional data.
