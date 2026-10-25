# A source gate: SSA national baby-name frequencies for R165 multi-variant historical replication

Date: 2026-10-25 Asia/Singapore. Track A. No paid access, account, private individual records, or redistributed raw bytes.

## Original source and provenance

Publisher: United States Social Security Administration (SSA). Official source and public download listing:
* https://www.ssa.gov/oact/babynames/limits.html
* https://www.ssa.gov/oact/babynames/names.zip
* https://www.ssa.gov/oact/babynames/background.html
* https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-data

The official SSA page visibly lists a roughly 7 MB national ZIP, state and territory archives, and annual frequency coverage. The government catalog marks access public, annual accrual and data last updated 2026-05-08. SSA's 2026 pages include birth year 2025.

Actual access attempt: the ZIP link was followed on 2026-10-25; the available browser fetch returned `Unsupported content-type: application/zip`. **No original ZIP bytes were downloaded, parsed, hashed, or row counted in this run.** The linked HTML metadata and source caveats were read. A secondary English-language format description at https://github.com/hackerb9/ssa-baby-names reports annual `yobYYYY.txt` records `name,sex,number`, with birth year encoded in the file name. The secondary description remains to be reconciled with the current official archive's internal readme after acquisition.

## Eligibility and gaps

| Gate | Observed status |
| --- | --- |
| Authentic publisher and download landing page | VERIFIED official SSA |
| Time unit | Birth year, annual; 1880 onward; official current tables include 2025 |
| Proposed columns | Name, sex, count, year from file name; exact current ZIP readme pending |
| Behavioural unit | Aggregated birth-name frequencies; no individual imitation or parent identity |
| Repeated observation | Annual panels by name and sex, but not independent experimental sessions |
| Population denominator | SSA card application coverage, not necessarily all births; compare published year/sex totals |
| Suppression | Names with fewer than 5 occurrences omitted; unobserved category mass cannot be treated as zero |
| Provenance identity | Official ZIP hash and per-year raw-file hashes PENDING |
| License | Public federal government data, publicly accessible catalog; exact ZIP-specific reuse notice PENDING |
| Acquisition | ZIP metadata available; raw byte retrieval blocked by tool's binary support |
| R073 frozen model fit | INELIGIBLE; lacks per-round paired repeated-game actions |
| R165 original multi-variant neutral drift | HIGH-VALUE CANDIDATE for a **separate pre-frozen** historical E3 study, after acquisition |
| Existing R165 two-token E1 result | UNCHANGED; no original historical reproduction |

## Measurement and model mismatch

The historical dataset has potentially thousands of named categories. The R165 frozen E1 mechanism has exactly two anonymous symbols and symmetric replacement, so it cannot be scored as an unchanged historical multi-category model. A future multi-category model must be declared as a **new, separately frozen study**, with an explicit training/holdout period, sample-size scaling, names threshold treatment, spelling and sex handling, missing mass, calibration, likelihood or distributional distances, and competitive popularity/fitness models. Do not use 2025 to tune a model later presented as a 2025 holdout.

The SSA data are aggregate historical observations. They do not identify copying links, causal imitation or individual innovations. The observation years are dependent and a year/name cell is not an independent experiment. SSA cautions that pre-1937 births are incompletely represented by card applicants; names with missing birth state or sex are excluded. SSA does not combine spelling variants, and removes spaces/hyphens.

## Decision

`OFFICIAL_SOURCE_AND_AGGREGATE_SCHEMA_VERIFIED / RAW_BYTES_AND_FILE_LICENSE_PENDING / E3_NOT_SCORED`

Priority: moderate-high for a future original neutral-drift multi-variant E3 comparison, after current R-series obligations. Next: obtain the official free ZIP through a permitted binary-capable route, hash archive and readme, inspect at least two separated birth-year files, count rows and suppressed mass limitations, then freeze independent historical scoring before any evaluation. Do not treat this as an additional independent R073 E2 experiment.

Cost risk: none incurred. Source licensing and external transfer restrictions to be checked before any redistribution. No CI triggered.
