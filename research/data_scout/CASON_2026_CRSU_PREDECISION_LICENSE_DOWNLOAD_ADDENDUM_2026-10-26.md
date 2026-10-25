# A Cason 2026 Dryad source gate addendum: access, predecision time, license scope

Date: 2026-10-26 Asia/Singapore. Track A. Additive followup to [earlier Cason source gate](CASON_RIEDL_SCHRAM_ULE_2026_CRSU_100_ROUND_INDIRECT_RECIPROCITY_SOURCE_GATE_2026-10-26.md). This is the SAME source and does not count as a fifth independent R073-compatible experiment or a new E2 score.

## Actually checked public English sources

1. Official Dryad dataset page, published 2026-01-20, DOI https://doi.org/10.5061/dryad.mcvdnckd6 , lists `CRSU_rawdata.csv` as a 2.75 MB raw data file, README.md 7.57 KB, Strategy_Class.csv 24.57 KB, and author Stata programs. No paid account required to inspect page metadata.
2. The embedded official README lists `ida`, `idb`, `round`, `adecision`, `session`, `cohort`, `indivIDa`, `indivIDb`, lagged donor/recipient help, snub and hurt counts, information-click indicators and treatment fields. The study documents 156 subjects, 100 rounds per session, 6-person cohorts and three donor-recipient pairs per round; each participant attended one session. The recipient has no decision in the same round. The donor's observed recipient history includes the latest three decisions. Outcomes are three categories (help, snub, hurt).
3. Dryad end-user terms (updated 2025-05-20), https://datadryad.org/terms , Section 1(a), state that dataset submitters grant public CC0 availability; Section 4(a) permits reuse of published datasets subject to usage restrictions. This supports **repository-level CC0 reuse policy**, but the dataset landing page does not expose a separate file-specific license identifier in its readable text. Mark `GENERAL_DRYAD_CC0_POLICY_VERIFIED`, `FILE_SPECIFIC_LICENSE_FIELD_NOT_OBSERVED`; no raw redistribution.
4. Attempted direct public file link via official Dryad page: https://datadryad.org/downloads/file_stream/4563239 returned **HTTP 403 Forbidden** in the available web retrieval environment. The raw 2.75 MB bytes were therefore NOT obtained, and no file hash, row count, participant consistency, actual missingness or per-session coverage was verified. The 156 participants and 100 rounds are documented design numbers, not a CSV count.

## Replication preparation and decision-time firewall

A later reproducibility script should read only permitted public raw bytes, record SHA256, check unique session/cohort/person identifiers, verify donor/recipient role assignment and the 100-round grid, and establish predecision event order. Candidate predictors: lagged own and recipient actions, lagged observed donor information, fixed treatment and elapsed round. Click fields are potentially choice-time information; verify click timestamps and experimental decision sequence before using them. `Strategy_Class.csv` contains ex post classifications and earnings and must never be treated as a predecision predictor.

Hold out complete independent sessions or cohorts, with session as conservative unit when competition across cohorts creates shared session effects. Recompute an unfitted baseline and score only after a new task-specific protocol is frozen. Preserve three-action outcomes, rather than forcing them into R073's two-player simultaneous binary game. R073 and PESEN v0.1 remain unchanged.

## Gate disposition

SOURCE_AND_SCHEMA_DOCUMENTED; GENERAL_DRYAD_CC0_POLICY_VERIFIED; FILE_SPECIFIC_LICENSE_FIELD_PENDING; RAW_DOWNLOAD_403_BLOCKED; RAW_HASH_AND_ROW_VALIDATION_PENDING; SESSION_COHORT_SPLIT_NOT_EXECUTED; R073_DIRECT_TRANSFER_INCOMPATIBLE; NEW_E2=0; NEW_E3=0. No purchases, account registration, Chinese-language sources or paid compute. This candidate remains valuable for R135 indirect reciprocity and a separately frozen three-action E2 evaluation.