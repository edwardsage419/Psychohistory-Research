# Public data scout: Jeongbin Kim repeated-game experiment, preliminary source registry

Date: 2026-10-24. Status: **PUBLIC_METADATA_ONLY / RAW_ROWS_NOT_LOADED / NOT_READY_FOR_R073_SCORING**.

Original project: Jeongbin Kim, *The Effects of Time Preferences on Cooperation: Experimental Evidence from Infinitely Repeated Games*, 2023. Public archival record: https://doi.org/10.3886/E152261V1 ; openICPSR project 152261, version V1.

Source listings verified from the English-language openICPSR public pages:
* `data_code/raw_data`: at least eight individually named 2016 session export files, including `160929_1539.xls`, `160929_1844.xls`, `160930_1436.xls`, `161003_1237.xls`, `161004_1544.xls`, `161004_1836.xls`, `161005_1827.xls`, `161006_1542.xls`. The dates/times embedded in filenames are **not verified independent session identifiers**.
* `data_code/temp`: named CSV and Stata files, e.g. `160929_1539_mod.csv` (660.3 KB), `160929_1844_mod.csv` (667.9 KB), `160930_1436_mod.csv` (663.3 KB) and `161003_1237_mod.csv` (411.6 KB).
* `data_code`: `readme.txt`, `time_coop.do`, `time_coop_data_generation.do` and text outputs are listed. Actual contents have not been loaded.

The public description identifies laboratory human repeated prisoner's dilemma play and manipulation of time preferences. Its original experiment is provisionally distinct from the already deduplicated FRD2012/R075, DF2011/R074 and Montero-Porras 2022/R096 sources; a complete comparison against every R073–R110 experiment remains open.

Required gates before any scoring: obtain openly accessible raw CSV/README without account creation; inspect actual participant ID, opponent/pair ID, round, game, treatment and action columns; determine independent session units, whether people recur across sessions, precise time alignment and lag-only predictor construction; establish dataset reuse and redistribution license; hash original files; match R073 frozen model inputs and scoring without re-tuning. No claim of record count, field identity, downloadable permissions, source license, or model compatibility has been established.

Risk: session filenames alone are inadequate for leakage-safe leave-one-session-out prediction. No private records accessed, no paid data purchased, no original data copied to the repository, no E2 score produced.
