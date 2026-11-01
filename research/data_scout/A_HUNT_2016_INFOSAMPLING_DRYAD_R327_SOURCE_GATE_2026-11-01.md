# A track public data gate: Hunt et al. 2016 information sampling
Date accessed: 2026-11-01 UTC. Track: a. Baseline main HEAD: 7b1c37b49ae5a9592b9f999074f621e377dc30a6.
Status: SOURCE_DESIGN_LICENSE_VERIFIED; RAW_FIELDS_BLOCKED; E2_REPRO_NOT_READY.

## Primary sources and identity
Original peer-reviewed English paper: Hunt, Rutledge, Malalasekera, Kennerley and Dolan (2016), Approach-Induced Biases in Human Information Sampling, PLOS Biology 14(11):e2000638. DOI https://doi.org/10.1371/journal.pbio.2000638 (published 2016-11-10; correction noted 2017-11-30).
Original public Dryad deposit: https://datadryad.org/dataset/doi:10.5061/dryad.nb41c (published 2017-01-05). The official landing page lists Hunt_infotask.zip, 44.46 MB, and README_for_Hunt_infotask.pdf, 517.71 KB, total 44.98 MB. The deposit describes raw .mat files and MATLAB analysis/model code.
Dryad's official reuse policy https://datadryad.org/help/guides/reuse states published datasets are CC0. This is a platform policy check; per-file legal exceptions and any embedded third-party content have not been inspected.

## Study design actually verified from the English article
The authors report 32,445 human participants and more than 3 million information-sampling decisions. In a card-gambling task, a participant can guess or pay to reveal more cards, choosing among six objectives (biggest/smallest under sum/product/single-card rules). Three successive optional sampling stages have nominal costs of 10, 15 and 20 points. Terminal choice pays 60 points if correct and loses 50 if incorrect, minus sampling costs. The article describes two short blocks of 11 trials per gameplay, and records choices to sample or guess at each stage. The paper compares these decisions to a dynamic-programming benchmark and reports multiple sampling biases.

Temporal unit verified: within-gameplay stage and trial sequence; actual timestamp fields and chronological granularity are UNKNOWN until raw .mat files are parsed. Human decision outcomes and within-gameplay repeated observations exist by study design. Stable anonymous person ID, session ID, missingness, full individual sequences, exact record count and experimental independence cannot yet be verified from the raw data.

## Access attempt, field gate and reproducibility
The Dryad landing page and the PLOS article were actually read. An attempt to open the official README_for_Hunt_infotask.pdf file stream returned HTTP 403. The raw ZIP was not obtained. Consequently no .mat header or data dictionary was inspected, no actual field names or individual-level keys were verified, and no checksum/record count was calculated. No participant-level data were copied or processed.

For a future R327-related E2 study, the existing R327 binary fixed-state one-sense mathematical rule cannot be treated as a fitted or calibrated predictor of this richer three-stage card task. A separate pre-score measurement bridge, loss function, participant/session split and held-out test are required. The raw source should be obtained only through a free lawful route, inspected for age/education or other sensitive covariates and minimized before analysis. Estimated effort: medium to high because raw data are MATLAB .mat inside a 44.46 MB archive and the original model has a different state/action/reward structure.

R073 frozen cross-experiment qualification: HARD_NO_BY_TASK_TYPE. The study is an individual information-sampling gambling task, not a continuous 100-round human dyadic prisoner's dilemma with own and opponent actions. No R073 parameters or scoring were touched. E2 human score: 0; E3 historical score: 0.

## Follow-up
1. Retry free public access to official README and ZIP; do not register or purchase anything.
2. Verify exact file version/hash, schema, participant/game/session keys, trial and stage time units, response fields, exclusions and consent/privacy constraints.
3. Pre-register a separate human task mapping before any E2 prediction; preserve frozen R327 E1 and R073.
4. Continue separate scouting for genuinely independent R073-qualified repeated dyadic human games.
