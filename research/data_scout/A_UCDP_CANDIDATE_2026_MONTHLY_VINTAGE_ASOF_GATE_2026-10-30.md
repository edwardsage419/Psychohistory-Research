# A track: UCDP Candidate historical vintages as-of source gate

Date: 2026-10-30 UTC. Track A. Source class: public historical organized-violence events, potential E3 preparation only. No human individual-level behavioral records. This is an independent source access and temporal leakage assessment, not an E3 forecast.

## First-party sources actually checked

Official current download page: https://ucdp.uu.se/downloads/
Official historical versions page: https://ucdp.uu.se/downloads/olddw.html
Official API access policy: https://ucdp.uu.se/apidocs/

The official download page lists the UCDP Candidate Events monthly release September 2026 version 26.0.9 and January–September 2026 aggregate 26.01.26.09, each with direct CSV and a codebook. The official historical page lists archived monthly candidate versions including 26.0.8 and 25.0.9 and multiple 2024, 2023 and 2022 monthly vintages. This is a material addition to the earlier GED 26.1 single-vintage codebook review: archived monthly releases may permit a limited as-of historical prediction design.

Actual direct CSV links discovered from first-party page:
* https://ucdp.uu.se/downloads/candidateged/GEDEvent_v26_0_9.csv
* https://ucdp.uu.se/downloads/candidateged/GEDEvent_v26_0_8.csv
* https://ucdp.uu.se/downloads/candidateged/GEDEvent_v25_01_25_09.csv

The web fetch rejected these endpoints because the response content type was CSV, and a separate container download attempt failed. No raw CSV bytes were obtained; row count, headers, event ID consistency, date fields, duplicate keys, and dataset SHA256 are NOT_VERIFIED. The official site states current datasets are free of charge under CC BY 4.0 with citation. The API is free but requires a requested token, and this project did not request one.

## Planned independent E3 gate

Define a prediction cutoff by *verified publication availability time* of each monthly snapshot. Freeze a particular archived vintage and exact file SHA256 before fitting or scoring. Use event start/end date and source publication date only if present and known at the cutoff. Exclude future revisions and future labels. Cross-version ID matching requires actual raw-file inspection, because stable identifiers and changes cannot be inferred from filenames alone. Treat GED 26.1 retrospectively curated records as an evaluation reference only after verifying a separate ground-truth and revision policy. Train/test splits must separate time, countries/conflict clusters where appropriate; use a predeclared baseline, Brier/log loss, calibration, bootstrap at a defensible clustered unit, and uncertainty. Do not mix candidate preliminary events with finalized GED records without explicit versioned reconciliation.

## Result and blockers

SOURCE_METADATA_AND_VINTAGE_DISCOVERY=PASS. RAW_FILE_PARSE=BLOCKED. SCHEMA=NOT_VERIFIED. INDEPENDENT_EVENT_ID=NOT_VERIFIED. ASOF_PUBLICATION_TIMESTAMP=NOT_VERIFIED. LICENSE=OFFICIAL_CC_BY_4_0. COST=ZERO_NEW_SPEND. R073_RELEVANCE=NO: historical conflict events cannot be used as an independent hundred-round human dyadic PD experiment. E3_PREDICTION=0. Next: obtain official CSV bytes via a permitted free download route, hash and parse at least two vintages, verify release timestamps and stable identity before any as-of scoring.
