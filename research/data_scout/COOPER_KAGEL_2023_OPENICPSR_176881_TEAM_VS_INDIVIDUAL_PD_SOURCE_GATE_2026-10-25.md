# A source gate: Cooper and Kagel (2023), human repeated PD, teams versus individuals
Date: 2026-10-25. Status: PUBLIC_REPLICATION_ARCHIVE_METADATA_VERIFIED; ROW_LEVEL_ACCESS_BLOCKED; R073_NOT_READY.

## Primary source actually inspected
American Economic Association / openICPSR public replication deposit: David J. Cooper and John H. Kagel, *Data and Code for: Using Team Discussions to Understand Behavior in Indefinitely Repeated Prisoner's Dilemma Games*, version V1, 2023-10-17, DOI https://doi.org/10.3886/E176881V1 ; listing https://www.openicpsr.org/openicpsr/project/176881/version/V1/view . Related journal article: Cooper and Kagel (2023), American Economic Journal: Microeconomics 15(4), 114–145, DOI https://doi.org/10.1257/mic.20210012 . Public indexed official archive listing was read. Direct archive open returned HTTP 403 in this run. No raw file bytes were obtained.

## Verified from public archive listing
The deposit describes an experiment with individuals and two-person teams playing an indefinitely repeated prisoner's dilemma with perfect monitoring. Its public file index lists a Stata .dta file named `all change to cooperative coding, final.dta` (17.8 KB), an `SFEM-estimation` directory, a PDF and DOCX README, and six separately named session chat DOCX files. The six chat filenames do not establish six independent data sessions or prove that each has distinct subjects. The published study compares team versus individual decisions and examines team dialogue. No row-level schema or exact subject/session/partner/round/action fields were verified.

## Cross-source deduplication
Searched the connected Psychohistory-Research GitHub code index for `Cooper Kagel`, `176881`, and `team discussions`: zero matching indexed files. This is a preliminary duplicate check only; it does not establish global uniqueness, since ZIP archives and unindexed source references may be missed. The experiment is not counted as a new independent E2 validation.

## R073 freeze compatibility and leakage gate
The source may contain binary dyadic repeated decisions, but the team unit differs from an individual actor. Treat team actions as team-level decisions unless a prespecified identity mapping justifies otherwise. Repeated supergames within a participant or team cannot automatically be treated as independent sessions. Need the raw .dta or equivalent official data, README, exact identity/round/session fields, licensing/redistribution terms, missingness and matching consistency, and a leakage-safe feature cutoff before applying the frozen R073 scoring. Chat transcripts were neither fetched nor processed, to avoid unnecessary collection of possible participant free text.

## Access, permission and cost
Direct openICPSR page access returned HTTP 403. File download and license terms not verified. No login, fee, paid API, private personal data, or download of chat text was attempted. A future free authorized retrieval route and field audit are required. New R073 independent scores: 0; new E2 human forecast evidence: 0; new E3 historical evidence: 0. Continue prioritizing the R queue.
