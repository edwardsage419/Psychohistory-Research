# A data scout: Kim 2023 time preferences and repeated prisoner's dilemma

Date 2026-10-30 UTC. Key (A,Kim_2023_openICPSR_E152261V1,repository-v1,source design and R073 eligibility). Independent from the R298 S94 artificial experiment.

## Actual inspected English sources

Primary project: https://www.openicpsr.org/openicpsr/project/152261/version/V1/view (DOI https://doi.org/10.3886/E152261V1; V1 published 2023-01-25). Official data_code directory: https://www.openicpsr.org/openicpsr/project/152261/version/V1/view?path=/openicpsr/152261/fcr:versions/V1/data_code . Official temp directory: https://www.openicpsr.org/openicpsr/project/152261/version/V1/view?path=/openicpsr/152261/fcr:versions/V1/data_code/temp . Publication DOI https://doi.org/10.1257/mic.20200195 .

Project explicitly describes real human laboratory repeated prisoner's dilemma, with decisions made all at once and stage-game payoffs paid over weeks or months. Three randomized treatments, four experimental sessions per treatment, 14 to 20 people per session, collection 2016-09-29 through 2016-10-19. Project file listing exposes `time_coop.dta` 1.4 MB, `time_coop.do`, `time_coop_data_generation.do`, `time_coop_strategy.do`, `readme.txt`, and three `dfformatlab_strg_*.txt` files. The temp directory displays **12 paired session CSV and Stata files** (24 listed records), with examples `160929_1539_mod.csv` 660.3 KB, `160929_1844_mod.csv` 667.9 KB and `161019_1537_mod.csv` 316.4 KB. The raw_data directory lists session XLS files. These are repository **metadata observations**, not locally parsed source records.

## Eligibility and barriers

Verified metadata: publication, study, treatment count, session count, session-level filenames, human participants, stage-game decisions and payoff-delay manipulation. Field names, action encoding, opponent identity, stable participant ID, actual dyad IDs, exact number of rounds per supergame, row count, missingness, per-file SHA256, file-level redistribution license and independence from previous R073 experiment remain **UNVERIFIED**. Attempt to read the official readme through public browser returned HTTP 403; full CSV content was not obtained. No account registration, private data access or payment attempted. Public landing-page visibility alone is not a data-use license.

**R073 frozen 100-round independent dyadic replay eligibility = NOT_ESTABLISHED.** All-at-once choice design may prevent the adaptive previous-opponent-history test even if a subject makes many decisions across games. Never treat 12 sessions or repeated choice as automatically satisfying 100 consecutive within-dyad rounds. No R073 model refit or scoring rule change.

Next: obtain free official readme/CSV if permitted without login, verify session and participant/dyad keys, round order, action fields, source license and genuine experiment independence. If no access, keep BLOCKED_SOURCE_BYTES. Candidate may still be useful for other bounded E2 time preference and cooperation research. No E2 evaluation executed this round.
