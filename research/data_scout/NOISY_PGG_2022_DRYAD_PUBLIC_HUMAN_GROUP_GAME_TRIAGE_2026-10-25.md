# A workflow: 2022 noisy public-goods game public-data triage

Date: 2026-10-25. Status: OFFICIAL_DATASET_METADATA_VERIFIED / FILE_STREAM_HTTP_403 / ROW_FIELDS_UNVERIFIED / NOT_READY_FOR_REPLICATION.

## Original English-language sources and actual access
Dryad dataset DOI https://doi.org/10.5061/dryad.n02v6wx03, published 2022-01-26. Study: Salahshour, Oberhauser and Smerlak (2022), *The cost of noise: Stochastic punishment falls short of sustaining cooperation in social dilemma experiments*, PLOS ONE DOI https://doi.org/10.1371/journal.pone.0263028.

The official Dryad landing page directly lists `noisy-PGG.csv` (1.30 MB) and `README-noisy-PGG.pdf` (52.80 KB). The dataset reports experiments conducted March to July 2021 using oTree and Prolific, 384 recruited/completed people in 96 four-person groups. After stated group-level nonresponse exclusion, analysis retains 320 people in 80 groups, allocated 21 control, 20 low noise, 20 medium noise, 19 high noise groups. These are depositor-reported metadata, not independent participant-level counts.

Actual attempts to open both official Dryad file-stream links from the dataset landing page returned HTTP 403 Forbidden in this run. Thus **zero raw data rows and zero actual CSV column names were read**. No retry via paid accounts, private sources, or unauthorized access. Dryad's official licensing policy states published datasets use CC0, subject to checking the individual downloaded files for any contradictory notice. Dataset download remains blocked in this execution environment.

Primary source: https://datadryad.org/dataset/doi:10.5061/dryad.n02v6wx03
Dryad licensing: https://datadryad.org/mission
File access attempts: https://datadryad.org/downloads/file_stream/1283295 (CSV, 403), https://datadryad.org/downloads/file_stream/1283294 (README PDF, 403).

## Field and replication readiness matrix
* Human participants and repeated public-goods punishment experiment: supported by official depositor description.
* Group identities, participant identities, round index, timestamp and number of repeated rounds: **unknown at row level**.
* Contribution, punishment action, stochastic sanction realized, payoff and treatment columns: plausible study variables; **actual column names and missingness unverified**.
* Four-person group clusters and condition counts: metadata available, raw identity map unavailable.
* Independent experimental sessions: **not documented by accessible metadata**. 80 groups must not be called 80 independent sessions.
* License: repository-level CC0 policy confirmed, file-level contradictory terms not yet checked.
* Duplicate-source gate: source paper and DOI recorded for comparison against existing R047, R073 through R110, R126 and other archived human datasets; complete archive-wide deduplication still open.
* Expected reproduction difficulty: moderate to high until row fields, group/round identities and sanction timing are verified.
* R073 compatibility: **not eligible** under its frozen two-person repeated-game model and scoring rules. No adaptation, reparameterization, or scoring permitted.

## Next permitted work
Seek an accessible official or author-hosted mirror with exactly the same deposited dataset and README; verify file checksum/provenance, columns, action timing, participant/group/session structure, license and treatment assignment. If accessible, design a separately frozen group-game holdout study using existing R-series models where appropriate. Do not reuse the 320 analyzed participants as a newly independent experiment until source deduplication is complete.

New E2 prediction scores: 0. New historical E3: 0. No fee incurred. This A task remained secondary to R131 mainline and B audit.
