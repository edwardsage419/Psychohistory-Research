# A public human prisoner-dilemma data scout: OpenNeuro ds007822

Date: 2026-10-25. New candidate source: https://github.com/OpenNeuroDatasets/ds007822 at fixed main commit bba8cdf86f03c0e37c0740e9c788790e7cea2602. Source BIDS DOI declared in dataset_description.json: doi:10.18112/openneuro.ds007822.v1.0.0. Dataset title: Prisoner's Dilemma EEG Dataset. This is a distinct triadic experimental structure and is not an R073 dyadic external-scoring dataset.

## Actual source reads

Directly read the GitHub repository README, LICENSE, dataset_description.json, participants.tsv, and all 33 participant pddecision events.tsv text files at the pinned commit. The README declares 11 triads of three participants. participants.tsv independently enumerates 33 participant IDs with group G01..G11 and within-group slots S01..S03. Each of the 33 decision event files had 40 rows, for 1320 observed decision-event rows and 440 triad-round combinations. All files exposed the same eight fields: onset, duration, trial_type, trial, group, subject, choice, triad_outcome. Choice values 1 and 2 map to coop and def respectively, with 1024 coop rows and 296 def rows. For all 1320 rows, triad_outcome was exactly the subject's own choice label; zero choice-to-label mismatches. All checked decision onsets matched 4*(trial-1) seconds and duration was 4 seconds; zero onset/duration mismatches. All 11 groups contained three subject slots, 120 decision rows and 40 distinct trial numbers. No raw person-level rows were copied into this project repository.

Per-triad cooperative decision counts, each out of 120: G01 65, G02 117, G03 80, G04 103, G05 51, G06 115, G07 119, G08 84, G09 75, G10 115, G11 100. These are descriptive source checks, not inferential estimates. Group labels establish grouping in the released data; independence of participants across triads and external human authenticity were not independently validated.

## Critical field and duplication findings

The field name triad_outcome is misleading if interpreted as a group-level joint outcome. Example: G01 trial 11 has S01 choice 1 with triad_outcome coop while S02 choice 2 has triad_outcome def. Thus this column is a per-person choice label in the released event files. It must not be used as a collective group outcome or as a same-trial prediction feature. Reconstruct any group-level quantity from all three participants' choices with correct time alignment.

Additionally read pdfeedback events.tsv for three participants G01S01, G01S02 and G02S01. Each had 40 rows and identical trial-by-trial choice and outcome values to its pddecision file, with duration 2 seconds instead of 4. The two task files are repeated annotations of the same decisions in this checked subset. Do not double count decision and feedback rows. Full 33-person feedback duplication audit remains open.

## License and readiness

dataset_description.json declares License CC0, while repository LICENSE (Git blob 7cf9928dd50e0b154c7e5d09f91f16674dff64fc) explicitly says license information was not provided with the source files. Treat the discrepancy as unresolved until the source archive's license authority is checked. No source data redistributed.

The experiment is a three-person triad task, with 11 group identifiers and 40 trial numbers. R073 requires frozen dyadic history and scoring semantics, so this candidate is NOT_READY_FOR_R073_SCORING. Potential future use is a separate human triadic-cooperation E2 protocol after source authentication, session identity, participant independence, licensing, leakage-safe lag mapping, baselines and holdout groups are established. The released EEG .set files were not downloaded or processed. No paid API, data purchase, registration, or sensitive private records were used. New E2 scores 0; historical E3 0.
