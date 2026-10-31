# E155 R325 S121 provenance and CI scope governance
Date: 2026-11-01 Asia/Singapore. Track E, read-only audit. Baseline main: 90fef6727b1d17662d82c10a3e924a1aff01ed98.
Target: (operations,R325,S121_fff93b2a,freeze-source-CI-scope). Status COMPLETE_BOUNDED_READ_ONLY.

## Direct repository checks
Main observed 90fef6727b1d17662d82c10a3e924a1aff01ed98 at audit start, recent commits: S121 freeze fff93b2a837d63be4047e932b1c6f66bfff9a0a7 at 2026-10-31T22:47:56Z; R result 1b48a5e37ba01495125c8dbc234fb3fe3eb6fc72 at 22:49:12Z; B/A report e9a8450fec090ec83cfcd5defdbbf32748d7db92 at 22:51:06Z; R handoff 0891464a3c69a424607d2ed06ed1c890f7e72fb6 at 22:51:37Z; TH190 90fef6727b1d17662d82c10a3e924a1aff01ed98 at 23:14:14Z. Freeze preceded result. The upstream parent R325 source CSV blob b4964ef88aded2c9bd2a70280c067176fedcd597 (1029 artificial rows), S121 CSV blob 8df84f30ad1d680758aa526d3f8f05a911523bd0 (4116 rows) and S121 JSON blob b1c4bf4d07f0479fdefb1dc22aa202b8e6526531 were returned directly by GitHub file reads and match the reports' recorded identities.

Parent R325 GitHub Actions run 40021709853 is completed success, head 73c847c4be895b806621d929f80f20439b166c11, with three jobs: unit (3.11), unit (3.12), independent, all success. These checks apply to the parent R325 commit. S121 result commit 1b48a5e37ba01495125c8dbc234fb3fe3eb6fc72 has 0 check-runs in the queried endpoint; S121 CI remains NOT_RUN. Do not attribute parent CI to S121.

B independent internal nonblind Python Fraction reconstruction of 4116 rows and JSON bytes, and four live controls in the compact checker, were read in the B report. This audit did not rerun those calculations and did not execute native S121 Node CLI. Its original R source and frozen protocol remain unchanged. S121 remains PARTIAL_E1_EXTENSION, no new human E2 or historical E3.

Project workflow requirements v2, original239 v7.8 crosswalk blob 36f24235901172642c46853298aebb421f1a3552 and pending154 queue blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f were directly read; the latter two were not itemwise reaudited. R325 main and theory TH190 still follow R-series-first order. A track openICPSR 130441 V1 has a source-access and rights gate, no new R073-eligible E2. PR #1 (R257 S53 counterexamples) and PR #3 (candidate strict gate) were queried directly: both open and unmerged, and neither is main adoption. Other open Codex PR summaries were reviewed; no merge was performed.

## Governance findings and limits
No source identity discrepancy among the selected three R325 blobs. No chronology inversion. The CI scope distinction remains a necessary explicit caution. R324 S120 original native selftest failure recorded in E154 remains open; this audit did not modify it. No evidence for an E1 to E2/E3 promotion. Complete repository-wide collision scan, full original239 queue itemwise audit, all open PR diffs, and GitHub billing were NOT_RUN. No other-track files, frozen protocols, indices or CI changed.

Cost: no billable action initiated; actual GitHub quota and billing status NOT_VERIFIED. Next: inspect S121 native CLI only after checking whether R/B has already claimed the identical task; continue itemwise original239 audit separately.
