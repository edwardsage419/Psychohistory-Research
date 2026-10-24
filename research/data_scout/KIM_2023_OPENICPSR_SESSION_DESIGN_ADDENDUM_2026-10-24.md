# Kim 2023 repeated PD: official archive session-design metadata addendum

Date: 2026-10-24. Track: A public empirical data scout. Status: **SOURCE_METADATA_VERIFIED / ROWS_NOT_RETRIEVED / NOT_READY_FOR_R073_SCORING**. Supplement to `KIM_2023_TIME_PREFERENCES_REPEATED_GAMES_PRELIMINARY_REGISTRY_2026-10-24.md`.

## Source directly inspected

English-language openICPSR official project V1, published 2023-01-25: https://doi.org/10.3886/E152261V1 (project 152261). Original study: Jeongbin Kim, *The Effects of Time Preferences on Cooperation: Experimental Evidence from Infinitely Repeated Games*, *American Economic Journal: Microeconomics* 15(1), 618-637 (2023), DOI 10.1257/mic.20200195. The official archive metadata reports collection dates 2016-09-29 to 2016-10-19 at Brown University Social Science Experimental Laboratory, USA.

The official methodology text says participants were randomly assigned to **three treatments, four sessions per treatment, with 14–20 subjects per session**. Thus the study reports **12 laboratory sessions in its design**. This is author/depositor metadata, not an independently validated row-level session count. The existing preliminary registry enumerated eight dated raw files from a public directory listing; eight filenames do not establish eight sessions and should not override the official twelve-session design. Exact mapping from files to the twelve sessions remains unverified.

The official source describes variation in weekly versus monthly stage-game payment intervals and initial payment delay, used to manipulate discount factors and present bias. These are payment-time treatments. The actual action-round time unit, subject pairing, continuation/stopping events and identifiers still require the raw files and codebook.

The public file listing includes `readme.txt`, `time_coop.do`, `time_coop_data_generation.do`, `dfformatlab_strg_1.txt`, `dfformatlab_strg_2.txt`, `dfformatlab_strg_3.txt`, and raw session exports. The listing alone does not prove field identities or successful download. This run did not retrieve file bytes or inspect the contents. No explicit reuse license was independently established from the inspected project metadata; do not assume public availability grants unrestricted redistribution.

## Replication gates

Before any frozen R073 score: (1) retrieve original files without payment or private credentials; (2) hash bytes and inspect English README and processing scripts; (3) map all 12 reported sessions to raw files, subject identities, opponents, games and rounds; (4) confirm participant uniqueness across sessions and lag-only action construction; (5) compare this experiment against existing R073–R110 sources for overlap; (6) document permission and feasible R073 input compatibility; (7) use unchanged frozen model and scoring protocol with an independent session holdout, and report calibration, baseline and uncertainty only if the data support them.

Current blockers: row access, precise fields, independent identity mapping, licensing and prior-source deduplication. New E2 predictions: 0. New E3: 0. No raw participant records were copied to the repository; no new costs or CI runs were initiated.
