# A source gate: stratEst DF2011 repeated Prisoner's Dilemma dataset

Date: 2026-11-01 UTC
Track: R / A public empirical data scout
Status: PUBLIC_METADATA_AND_UPSTREAM_FILE_IDENTITY_VERIFIED; RAW_ROWS_NOT_PARSED; R073_FROZEN_ELIGIBILITY_UNKNOWN

## Source verified

Upstream publisher repository: https://github.com/fdvorak/stratEst (public, default branch master).
Package: stratEst, DESCRIPTION reports version 1.1.8, date 2025-10-20, GPL-3 package license.
Upstream source file: https://github.com/fdvorak/stratEst/blob/master/data/DF2011.rda
Git blob: 52e216b02e1a7ab7fb1a6e335b5f7e2ef6b7f5a0, size 3,298 bytes.
A separate preprocessed variant `data.DF2011.rda` is also present, blob 4c2586af1a5465a9e690b41e6f839c33096a4903, size 5,082 bytes.

The upstream English CRAN package manual documents 7,358 individual decision rows and six fields: `treatment`, `id`, `game`, `period`, `choice`, `other.choice`. `game` is a supergame identifier, `period` a within-supergame round, and `other.choice` the opponent's contemporaneous action. The original cited experiment is Dal Bó and Fréchette (2011), American Economic Review, DOI 10.1257/aer.101.1.411.

Documentation: https://stat.ethz.ch/CRAN/web/packages/stratEst/refman/stratEst.html

## Eligibility and overlap gate

The data have apparent participant and opponent-action history fields. The actual binary .rda bytes were not fetched or parsed in this run. No participant counts, maximum uninterrupted dyad length, pair identity continuity, exclusions, missingness, checksum of decoded rows, or time-order completeness were independently verified.

Existing R-series scouting has already examined Nay and Vorobeychik `NV_games`, whose documented `data` origin labels include DF (Dal Bó and Fréchette). Therefore DF2011 may overlap existing sources. This is a **lineage risk**, not a proven row-level duplicate. Do not register DF2011 as a new independent R073 cohort before exact source and participant-level de-duplication.

The package's GPL-3 statement is confirmed. Permission to redistribute the original experimental records separately from package code is not established by this check. No third-party binary was committed.

R073 frozen model/scoring: UNCHANGED.
Raw data obtained: NO.
Frozen-test eligibility: UNKNOWN.
External R073 scoring: NOT_RUN.
E2 predictive evidence added: 0.

Next: retrieve only openly permitted data, parse the .rda locally using a free reader, verify participant/game/period/opponent continuity and max sequence length, compare against existing DF/NV provenance, then make an explicit eligibility decision without post-hoc model adjustment.
