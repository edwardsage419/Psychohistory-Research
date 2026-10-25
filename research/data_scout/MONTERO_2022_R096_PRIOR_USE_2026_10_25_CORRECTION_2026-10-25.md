# A source deduplication correction: Montero-Porras 2022 was already used by R096
Date: 2026-10-25. Classification: source provenance and duplication audit; no new E2.

## Trigger and source identity
The newly added `research/data_scout/MONTERO_2022_12_SESSION_FIXED_SHUFFLED_PD_SOURCE_GATE_2026-10-25.md` called the 2022 12-session repeated PD experiment an independent candidate and said code search for Montero within the project returned zero results. This negative code-search result was incomplete.

The same DOI `10.1038/s41598-022-11654-2` and Dryad `10.5061/dryad.37pvmcvmk` had ALREADY been matched on 2026-10-24 in `research/data_scout/MONTERO_PORRAS_2022_R096_PRIOR_E2_DEDUP_2026-10-24.md`. The 2026-10-25 source gate must be read together with this earlier deduplication; it cannot override the known earlier source use.

## Actual prior R096 experiment
`research/R096/README.md` and the formal R096 scientific report identify exactly the same Montero-Porras, Grujić, Fernández Domingos and Lenaerts 2022 experiment: 12 original sessions, 188 humans, six fixed-partner sessions with 92 people and six shuffled-partner sessions with 96 people, each 100 rounds. R096 actually read the author's Git repository `eladiomontero/PairwiseStrategies` fixed `submission` commit `4743f74d8a03a031b8f70aff64956f8ad5155182`; fixed Git source files `fix.csv` blob `3bf78bf85f6642afee18d6f1965dca7272582f40` and `rand.csv` blob `f5a86cd033b739da45d3fc7c5019068f612146a2`. R096 scored 18,612 person-round next-action targets with its own M0/M1/M2 complete-session held-out protocol. The official Dryad file bytes were never acquired, and no claim of byte identity between Dryad and author Git files is supported.

R096 used a separately frozen M0/M1/M2 protocol. It does NOT constitute a new exact external run of the R073 frozen contract. Its existing E2 evidence must be counted only once.

## Corrected gate
`SAME_ORIGINAL_EXPERIMENT_AS_R096 = YES`.
`NEW_INDEPENDENT_EXPERIMENT = NO`.
`NEW_R073_FROZEN_TRANSFER = NOT_RUN`.
`NEW_E2 = 0`.
`DRYAD_RAW_BYTES = BLOCKED_403`.
`R096_PRIOR_E2 = PRESERVED`.

No original archived source-gate or frozen R096 files are overwritten. The correction is append-only. Before future candidate announcements, search repository tree and read R073 through R110 source documentation, including author and DOI identity, rather than relying on code search alone. No personal data or paid sources used.
