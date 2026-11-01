# A data scout: OpenNeuro ds004917, human ambiguity choices
Date: 2026-11-01 UTC. Status: PUBLIC_BEHAVIORAL_SAMPLE_READ_SCHEMA_CONFLICT_FOUND; E2_REPRO_NOT_READY.

## Verified public source
OpenNeuro dataset "Probability Decision-making Task with ambiguity", version 1.0.1, DOI 10.18112/openneuro.ds004917.v1.0.1, https://openneuro.org/datasets/ds004917/versions/1.0.1 . Fixed public GitHub source https://github.com/OpenNeuroDatasets/ds004917 at commit e66291e48b57243d6d24211ba2f7a52bcaa2b760 (2024-05-23). Paper: Valdebenito-Oyarzo et al. (2024), PLOS Biology, DOI 10.1371/journal.pbio.3002452. English-language sources only.

Read and checked actual source files via GitHub:
* dataset_description.json Git blob d5838a819c9d4e2ff38b48e30f55c439688820ae: BIDS 1.9.0, license field CC0, dataset DOI.
* participants.tsv blob d722e7fd2d815a2f48212808947a9125f6d2665e: 53 anonymized subject IDs, modalities include fMRI and EEG.
* task-pdm_events.json blob d6fdc5be2ce284d9369afe58e8250a5e0382bea6: onset seconds, duration and rt milliseconds, probability p, visible probability pv, ambiguity fraction a, stimulus event value, response, trial label ronda.
* sub-01/func/sub-01_task-pdm_events.tsv blob bbf4b713bc05b5d28a2dec7655a5bb7c130fb9ad: 180 event rows, 11 columns, 40 event-code-10 decision presentations, all 40 response entries encoded 1 or 2, 40 numeric rt values. Four distinct nonempty ronda labels repeat within participant; ronda alone is not a globally unique trial ID.
* sub-02/eeg/sub-02_task-pdm_events.tsv blob 86be47774c1149d9a3f564c991e14d76bf33e7ab: 1320 event rows, 16 columns, 240 event-code-10 presentations, 240 numeric rt entries. For all 240 code-10 rows, response exactly equals rt, and zero response entries are encoded 1 or 2. Thus the documented response coding is inconsistent with this EEG event file. Do not treat EEG response as a choice label until an author codebook or a validated independent source resolves the discrepancy.

The two files are public anonymized event records. Only aggregate structural counts and file identities are archived here; no individual-level participant values, neuroimaging files, or identifying attributes are copied. Other subjects' event files have not been enumerated, so these sample counts cannot be extrapolated to the whole dataset.

## Eligibility and measurement gates
The experiment records human risky/ambiguous choices, probability and visibility attributes, event times, and anonymized participant IDs. It does not experimentally offer a PRECISE versus NOISY information-acquisition policy as defined in R329 S125. There is no legitimate direct mapping from this dataset's ambiguity manipulation to the constructed EFE sensor choice without a new prespecified measurement model. EEG choice coding discrepancy requires resolution. Participant-level train/test separation, task-block identity, missingness, repeated-trial dependence, license scope for any derived release, and exact data-file version must be checked before empirical scoring.

R073 frozen 100-round dyadic repeated prisoner's dilemma: HARD_NO_BY_TASK_TYPE. No R073 frozen model or scoring rule modified. No new E2 result. Data and code are public under the dataset's CC0 declaration; the full imaging dataset is large and was not downloaded. No paid access, registration or API use.

## Candidate search and deduplication
Rechecked the human 100-round dyadic PD need. Existing local A registers already cover Mao et al. 2017 (400 separate 10-round games, not a single 100-round dyad), DF2011 (existing R074 experiment), Montero-Porras (existing R073-source identity conflict), and Nay/Vorobeychik pooled data (dyad/session identity unresolved). Machine-generated Axelrod tournament datasets do not qualify as new human E2. No new independently eligible R073 dataset verified in this pass.

Next: resolve EEG response semantics from author scripts or codebook; verify a second sample participant and full task/block identity; require a frozen measurement and participant-grouped holdout before any E2 claim.
