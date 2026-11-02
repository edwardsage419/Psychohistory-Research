# R272 P0: archived triplet reconstruction, additional adversarial controls and mandatory caller audit

Date UTC: 2026-11-02T03:42Z. Track: R main and B scientific verification.
Original239: 12-002 Out of Sample Prediction. Target: R272 archived finite artificial E1.
Starting main: 49af07fcb2408c5b83f027955a727441ab582261.
After adversarial script submission, main: 618f0537fcaf0a7b59f77facc954fb02da9d19eb.
Status: COMPLETE_BOUNDED_RECONSTRUCTION_AND_STATIC_CALLER_AUDIT / PRODUCTION_P0_OPEN.
No change to frozen original program, protocol, receipts or workflows.

## Pinned original evidence and queue

Read the live main ref, latest two commits, original239 v7.8 crosswalk and 154-item queue, R272 freeze protocol, three archived R272 payload identities, candidate report, original workflow and open Codex PR metadata. Queue blob: 3b96d46b3d88ccafd779a08509c3cfd0e435772f; counts independently parsed from all 154 CSV rows: P0=27, P1=82, P2=45. Crosswalk blob: 36f24235901172642c46853298aebb421f1a3552; 239 original items. R272 original program blob: 13843eecf2f9f05c19ee5545bdb224f58313f367. Freeze protocol blob: 9fbdb0078a58c4a9c0a548643227e30da5731119. Candidate ZIP SHA256 pin: f23b04706b60ac70bdbee6f051a74551779fb9d9a9b9af08c96cda345b055151.

Open Codex PR count from live search: 12. PR #1 and #3 both open and target R257 S53, so no competing R272 candidate work was identified in those two PRs. No merge or PR mutation.

## Native local bounded reconstruction

Execution: CPython 3.13.5 standard library, local uploaded candidate source. No random seed. A clean full Git checkout was unavailable because git remote access failed DNS resolution. Reconstructed source CSV, results JSON and receipt using the archived candidate's synthetic fixture and the original documented two-space JSON indentation plus trailing newline. Verified the following independently against the live GitHub directory metadata:

* CSV: 61,489 bytes, Git blob 8fbbc73d239765f5c66395af1bcf9cf7a8df1f41, SHA256 dc40ed773491817caf242ba6416e1bdf98ef2f1a2cd05e1956bdf5aec5801663.
* Results JSON: 4,402 bytes, Git blob db3ca11ae224af52c2caf385c898e24aaa0cc54b, SHA256 f891df1c4640c2f49a457c436bc043f6bc08b768ac92594050e7e08061495a40.
* Receipt JSON: 413 bytes, Git blob 85d36858911a7eb79c73c607cddf45ea88852a60.

All three reconstructed byte streams match the recorded original Git blob identities. The candidate verify(csv, results, receipt, pins=True) returned PASS for 576 sources, nine artificial worlds, 8,640 CSV field values and two receipt hashes. This is exact byte-equivalent synthetic reconstruction with independent remote identity comparison; it is not a direct complete-checkout invocation of --root, nor external team replication.

Existing candidate --self-test was run under python, python -O and python -OO: each mode reported one positive control and 11 rejected mutations. Additional locally executed adversarial controls tested duplicate CSV header, extra CSV field, missing source, false per-world analytical flag, nested duplicate JSON key, unearned external replication claim, nonstandard NaN receipt number and extra E2 receipt claim. All eight were rejected in each of the three Python modes. Total additional rejected controls: 24 executions. Where appropriate the receipt hashes were recalculated after corruption, so the checks exercised scientific content and schema beyond hash equality.

The portable supplementary script was archived at research/validation/r272_candidate_additional_adversarial_controls_20261102.py, Git blob f176bcc50fa641507d2655e6bf662270c4bba787. The local tested script used an extracted sibling candidate; the repository script's ZIP-loading branch has not been run against the actual remote binary ZIP. Treat that execution path as NOT_RUN until native checkout testing.

## Confirmed production adoption gap

Read .github/workflows/r272-exact-train-test-oos-e1.yml, Git blob 3132b08cf4ee64b55f5112d2249894ea0ec9d42d. Its two Python-version test jobs run the original R272 program --test. The archive job runs the original program --emit and a large inline third-party audit implemented with Python assert. The workflow contains no invocation of the newly archived fail-closed candidate. Its push.paths list contains only the original generator path and the workflow YAML; it excludes research/validation/** and the candidate ZIP. The candidate exists on main as an archived ZIP, requiring extraction before command-line invocation.

Observed mandatory candidate caller count in this workflow: 0/1. Candidate edits that touch only research/validation/ do not match this workflow's declared push.paths filter. This is a static workflow source finding. Historical CI ran ordinary Python mode; no claim is made that historical CI accepted a falsified result. The original optimized-mode false acceptance remains separately proven in earlier R272 native mutation work. The candidate cannot close P0 without fail-closed mandatory caller adoption, a native --root execution against a complete pinned checkout, separate mutated archived files, and review of production trigger paths and failure propagation.

## A data scout and evidence grade

Briefly checked existing OpenNeuro ds007822 public three-player Prisoner's Dilemma EEG dataset candidate. The published description has 11 triads, 33 participants and 40 task trials per participant; this is not evidence of eligibility for R073's unchanged frozen 100-round two-player and session-heldout scoring. No new original data file was acquired or scored this run. R073 and PESEN v0.1 remain frozen. New E2=0, E3=0, external-team replication=0. The R272 result remains internal nonblind finite artificial E1.

## Next acceptance work and limitations

Priority 1: obtain trustworthy complete checkout at pinned main, verify candidate ZIP member and invoke the archived candidate --root in ordinary and optimized modes against original source/protocol/CSV/JSON/receipt, preserving exit codes and stderr. Priority 2: add a separately reviewed mandatory fail-closed caller and trigger coverage only after confirming GitHub Actions cost and owner scope. Priority 3: revisit R333 to R340 composite gate caller adoption. No frozen evidence, prior failures, or acceptance status has been overwritten.

This run did not trigger Actions, purchase data, call a billed API or request paid computing. Actual account billing/free quota NOT_VERIFIED. CI NOT_RUN. The newly submitted file is a test artifact; its existence or test PASS alone does not close any original239 item. Queue net change: zero.
