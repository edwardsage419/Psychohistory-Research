# E127: R297 S93 persisted-source and receipt read-only governance
UTC 2026-10-30. Track operations. Baseline main f65da166a2e6b7118d92d36910d3c8ce6316f895. Target (operations,R297,S93-v1,nonblind-direct-persisted-field-reconciliation). Status COMPLETE_BOUNDED_READONLY; not scientific acceptance.

## Repository and coordination scope
Read main HEAD and recent commits, latest market MKT157/E126/F009 phase21 and market handoff, R297 S93 freeze, result, machine receipt, original source, original R script and B report, R-track handoff, A Grujic/Lenaerts data scout, theory TH162 handoff, owner workflow v2 and owner research sequence. Twelve Codex PRs are OPEN, including #1 R257 S53 counterexamples, #3 candidate strict gate, and #2 sync protocol. All are UNMERGED and do not change main acceptance. The sync protocol path on main returns 404, so user-supplied short coordination rules apply. No duplicate PR issue filed.

Verified Git compare: freeze 5ad31ab649e11f7c2147614105661548edf79ca7 is direct ancestor of result d16540648a47d687ccfe6a78de63d51634c38038 (ahead_by=1). R297 S93 status remains PARTIAL, original R297 bounded result unchanged. A Grujic 2020 paper covers 9 sessions, 16 people/session, 50 rounds, 4 neighbors, so fails frozen R073 100-round dyadic eligibility; original Dryad CSV/README HTTP403 and file checksum unverified. No new E2.

## New direct persisted comparison
Using the GitHub connector, directly read:
* original source CSV: Git blob b2309d463dbb80881ba484e0a67bd2fa3ac13bc5, 120 data rows
* S93 output CSV: blob 36420d77da6473d6c04da43d3870c1a38159d686, 120 rows
* S93 results JSON: blob 51b50571021b86190b7eca3d86b669081d42b077
* S93 machine receipt: blob 16e28b3a70d7acda4e381ca2de96369e3283c78f

Executed separate in-tool JavaScript BigInt rational cross-file audit without importing R or B code: 24 distinct worlds, 120 unique world-epoch keys, 1560 direct field comparisons/checks, zero mismatches. Original/source and output matched on world, gamma, alpha, coverage, backup_rule, epoch, both Q values, chosen action and oracle label; exact rational Q_gap, oracle regret and error were independently recomputed from source fields. Error counts per epoch 16,13,13,12,12; exact summed regret 81, epochs 1..4 total 61. Receipt Git blob links to original source, CSV and JSON all match remote blobs. An initial local audit diagnostic used JS number 0 rather than BigInt 0n and produced false error flags; the audit implementation was corrected and rerun, final checks PASS. This was a bug in the new audit diagnostic, not evidence of a defect in R297 data.

Limitations: this check uses pre-existing persisted R and B-visible outputs, so NONBLIND_INTERNAL and no external replication; it did not execute the archived native Python CLI in a fresh checkout, rederive the original Q recurrence from scratch, verify source SHA256 independently from raw bytes, or check all JSON world summaries. The prior B report separately records 8 negative mutations, which were read, not rerun here. Code execution and exact comparison do not imply scientific E2/E3 acceptance. R297 S93 remains PARTIAL. Commit combined statuses and commit-filtered workflow runs for result commit were empty; CI not run by this task, account billing/quota not independently checked. Previous checker issues R286/R290/R291/R293/R294 remain OPEN absent verified repair; R281 blind failure retained.

Open: E127-01 native clean-checkout S93 CLI and independent source recurrence; E127-02 historical metadata checker coverage; E127-03 R073 independent dyadic dataset still missing. No frozen protocol, other-track report, crosswalk or index changed. Next E128 inspect latest R stage, run native source replay only with confirmed zero cost and available bytes.
