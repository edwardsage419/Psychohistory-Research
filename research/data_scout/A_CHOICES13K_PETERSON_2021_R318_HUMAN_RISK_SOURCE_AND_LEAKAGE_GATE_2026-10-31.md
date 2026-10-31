# A track: Choices13k public risky-choice source gate for R318
Date: 2026-10-31 UTC. Status: SOURCE_METADATA_AND_VISIBLE_RAW_ROWS_VERIFIED; FULL_BYTE_PARSE_AND_LICENSE_OPEN.
Target key: (A, Peterson2021-choices13k, GitHub main public blob 86b58f0, R318 human choice suitability and R073 negative gate).

## Source and actual reads
Authors Joshua C. Peterson, David D. Bourgin, Mayank Agrawal, Daniel Reichman, Thomas L. Griffiths (2021), *Using large-scale experiments and machine learning to discover theories of human decision-making*, Science 372:1209–1214, DOI 10.1126/science.abe2629.
Author-hosted repository: https://github.com/jcpeterson/choices13k ; README read via authenticated GitHub connector, blob b5ecab6dd7da53e21799ceb863cdab30463fd2bc (12,022 bytes). Public root enumerated.
- c13k_selections.csv: 1,179,986 bytes, Git blob SHA1 86b58f02476d38e267ff03426fb297acce90d15a. Public raw English CSV inspected via https://raw.githubusercontent.com/jcpeterson/choices13k/main/c13k_selections.csv ; first header, sample lines and final row visibly verified. Web text view has 14,569 lines including header, suggesting 14,568 data rows; full CSV parser count and cryptographic SHA256 NOT_RUN. The distinct problem count 13,006 is stated by authors; the row count differs because some problems have both feedback and no-feedback records.
- c13k_problems.json: 1,681,916 bytes, Git blob SHA1 b3d6a205ede6d95467108ff365b1f6823405201c. README documents keyed problem payoff distributions. Entire JSON was not parsed in this run.

## Unit, fields, access, license
README selection fields: Problem, Feedback, n, Block, Ha, pHa, La, Hb, pHb, Lb, LotShapeB, LotNumB, Amb, Corr, bRate, bRate_std (case as in actual CSV header). Problem identifies gamble pair; Feedback and Block describe condition; n is number of participants contributing to an aggregated problem/condition row; bRate is average selection rate across participant trials. The README states each participant completed five trials for a problem. No unique participant identifier, round-by-round opponent actions, independent game/session identifier, or UTC event timestamp appears in this public selection table. This is human aggregate choice evidence, not a human-human repeated game.
Source GitHub root shows README, example notebook, CSV and JSON, with no explicit LICENSE file. The data license and redistribution grant are therefore UNKNOWN from this source inspection; HURD-related third-party license statements do not substitute for author repository permission. Do not mirror raw files to this project until resolved.
Raw CSV is publicly readable through the browser, but GitHub connector file preview for this >1MB object returned no selected lines. Full local byte download, full parser, file SHA256, and subject identity verification remain OPEN.

## R318 and R073 gates
R318 S114 is 18 fixed synthetic lotteries with a noncanonical illustrative transform; Choices13k has 13,006 published risky-choice problems and aggregated choice rates, with differing payoff/feedback/ambiguity designs. No direct empirical R318 S114 accuracy claim can be made from the synthetic rankings. A later separate prescored study could compare probabilistic choice predictions and proper scores against baseline, using eligible unambiguous two-outcome problems and a grouped split by Problem to prevent feedback/no-feedback leakage. First verify the raw JSON payoff representation, source version, data rights, and participant overlap. Aggregated rates cannot be treated as independent individual decisions.
R073 eligibility = HARD_NO_BY_TASK_TYPE_AND_MISSING_DYAD_HISTORY. No frozen R073 model or scoring rule changed. New E2 scores = 0, E3 = 0.

## Follow-up
Confirm author data terms, retrieve and hash full files using no-cost access, validate 14,568 rows and 13,006 unique Problem IDs with a real CSV parser, inspect payoff JSON schema, and prefreeze any real scoring plan before looking at outcome-dependent performance. Do not spend money or access private subject data.
