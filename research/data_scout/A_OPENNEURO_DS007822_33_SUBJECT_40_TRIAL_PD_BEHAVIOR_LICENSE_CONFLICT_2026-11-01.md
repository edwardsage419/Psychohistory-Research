# A track public-data source gate: OpenNeuro ds007822

Date: 2026-11-01 UTC. Track r/A. Baseline main before report: 119877be1ca4893fb66b8685fe68404614a0c8d2.
Target key: (a, OpenNeuro ds007822 v1.0.0, public triadic PD events schema / R073 eligibility).
Source: https://github.com/OpenNeuroDatasets/ds007822
Persistent dataset ID: doi:10.18112/openneuro.ds007822.v1.0.0
No Chinese-language source used. No participant-level raw data copied into this research repository.

## Actual source and field verification
Read public source README, participants.tsv, participants.json, dataset_description.json, LICENSE, and all 33 participant-level `task-pddecision_events.tsv` files from the public GitHub repository. Participants file: 33 rows, 11 groups G01..G11, three slots S01..S03 per group. All 33 decision files contain 40 trial rows, trial indices 1..40, giving **1,320 observed decision-event rows**. Every file has these eight fields: onset, duration, trial_type, trial, group, subject, choice, triad_outcome. The first checked files contain choices encoded 1 and 2, and triad_outcome labels coop/def; choice-code semantic mapping is not independently verified. For each file checked, trial_type is decision; individual reaction-time measurement is not separately exposed in the event schema. Example G01S01 has 4.0-second event duration and onsets 0,4,8,...; BIDS time coordinates use seconds, and this is scheduled event timing, not demonstrated individual decision latency.

Verified public blob identities include:
participants.tsv `7555eca1349703e6b1683fce828756d703012eab`;
dataset_description.json `c6d51a07c3a5b3821b8ffabea51a502ea99835e4`;
LICENSE `7cf9928dd50e0b154c7e5d09f91f16674dff64fc`;
G01S01 decision events `594269370f3bb11ed54b5c02ff978fb762de5381`;
G11S03 decision events `bf602f89007953aec862b07855005e97e1a59771`.
The full 33-file content was read transiently through the public GitHub connector; no bulk data file was downloaded or archived. No missingness/choice consistency across the 1,320 rows was independently certified, beyond row counts, field structure and trial indices.

## Permission contradiction and reproducibility gates
`dataset_description.json` declares `"License": "CC0"`, while the repository `LICENSE` file says `License information was not provided with the source files.` The dataset-level metadata and the accompanying license file conflict in clarity. Record **DATA_REUSE_LICENSE_CONFLICT_UNRESOLVED** until the OpenNeuro release and source provenance are reconciled. Do not redistribute participant event data or assume that source authors separately licensed every EEG recording. EEG .set files are git-annex pointers in the GitHub tree; EEG binary payload was not obtained or inspected.

Independent observation units are triads, with three subjects sharing each triad and 40 indexed trials. Treating 1,320 event rows as independent people or independent dyadic games would be pseudoreplication. The 33 participants are identifiable only by public anonymous group/slot labels. No private identities were accessed.

## Eligibility and next steps
R073 FROZEN independent 100-round two-player repeated-game test: **HARD_NO**. The observed task has three-player groups and 40 trials. No R073 scoring, fitting, baseline comparison or tuning performed. This dataset can support a separately frozen E2 triadic cooperation/EEG task if license and outcome semantics are confirmed; its triad-clustered sample is 11, and split must be by triad rather than by row. Verify choice coding, session independence, all event-row validity, and original source license before any empirical model score.

Status: PUBLIC_SOURCE_AND_33_FILE_SCHEMA_VERIFIED; LICENSE_CONFLICT_OPEN; R073_INELIGIBLE; E2_NOT_RUN. Cost: free public metadata, no paid APIs, GPU, runner or downloads.
