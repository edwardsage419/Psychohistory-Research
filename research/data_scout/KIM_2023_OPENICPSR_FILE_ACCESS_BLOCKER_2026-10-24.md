# Kim 2023 openICPSR file-access and independent-session readiness addendum

Date: 2026-10-24. Independent A data-scout workflow. Study: Jeongbin Kim, *The Effects of Time Preferences on Cooperation: Experimental Evidence from Infinitely Repeated Games*, AEJ Microeconomics 15(1), 618–637, DOI 10.1257/mic.20200195. Public archive: https://doi.org/10.3886/E152261V1 (version V1, 2023-01-25).

## Source observations and actual retrieval

The official openICPSR project directory lists `raw_data`, `temp`, three `dfformatlab_strg_*.txt` text files of approximately 96.6, 97.2 and 107.2 KB, `readme.txt` (3.6 KB), `time_coop.do` (16.7 KB), `time_coop_data_generation.do` (3.8 KB), `time_coop_strategy.do` (3.1 KB), and `time_coop_dta.dta` (1.4 MB). These are file-list metadata only, not decoded records.

Source URL: https://www.openicpsr.org/openicpsr/project/152261/version/V1/view?path=%2Fopenicpsr%2F152261%2Ffcr%3Aversions%2FV1%2Fdata_code

Actual attempt to open `readme.txt` and `time_coop_data_generation.do` from the archive in this run returned HTTP **403 Forbidden**. No raw participant rows or variable names were acquired. No download, login, account creation or paid access was attempted.

Official study metadata states 3 treatment groups, 4 experimental sessions per treatment, 14 to 20 participants per session, Brown University undergraduate laboratory recruitment, and collection dates 2016-09-29 to 2016-10-19. These establish 12 source-reported sessions. The raw files and their session-to-file mapping remain unverified. A listed 1.4 MB Stata dataset is a promising later retrieval target.

## Frozen R073 compatibility gate

Status: **SOURCE_METADATA_VERIFIED / RAW_FIELDS_BLOCKED_HTTP_403 / NOT_READY_FOR_R073_SCORE**. Subject identifier, partner identifier, simultaneous decision timing, own action and partner action by round, supergame identifier, within-session repeated identity, leakage-safe lag mapping, and actual reuse versus R073/R074/R075/R096 source families are unverified. Study-level redistribution license was not confirmed from the accessible listing. Treat source access and license as separate unresolved gates.

No R073 model or score changes; no tuning on candidate data. No new E2 score or historical E3. Next permitted work: access publicly downloadable codebook/data via free official channels and establish a field-level identity and session map before any frozen-model scoring.
