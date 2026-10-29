# A track: Grujić 2020 original CSV access gate and DF2011 deduplication

UTC date: 2026-10-29. New scope keys:
(A,doi:10.5061/dryad.7fq25s8,2020,exact-csv-endpoint-access);
(A,DF2011-stratEst,existing-R074,duplication-gate).
Prior read: `A_GRUJIC_2020_DRYAD_CC0_POLICY_AND_README_DOWNLOAD_GATE_2026-10-29.md`; this entry records only newly checked access and dedup evidence.

## First-party Dryad source and actual access

Official dataset: https://datadryad.org/dataset/doi:10.5061/dryad.7fq25s8 (Grujić and Lenaerts, published 2020-07-27). The official file roster lists `DataSet.csv` (215.22 KB), `README_for_DataSet.txt` (1.41 KB), and two English instruction PDFs. The official paper is https://doi.org/10.1098/rsos.200618 .

The exact CSV file link obtained by following the dataset's official `DataSet.csv` entry resolves to `https://datadryad.org/downloads/file_stream/296893`. The web fetch returned HTTP 403 Forbidden. The exact README file link `https://datadryad.org/downloads/file_stream/296894` also returned HTTP 403. The public dataset REST endpoint `https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.7fq25s8` was not accessible in this execution environment.

Confirmed from paper and official dataset listing: human spatial repeated Prisoner's Dilemma, nine experimental sessions, 144 participants, sixteen per session, fifty rounds. The maximum possible 144*50=7,200 person-round cells is a design calculation, not a verified CSV row count. Raw column names, round sorting, anonymized person/session keys, missingness, network edges, and exact reuse license field remain NOT_VERIFIED. Dryad platform CC0 policy was verified in the prior report; dataset-version-specific license metadata remains OPEN. R073 direct 100-round dyad frozen replay remains NO. Reproduction readiness: SOURCE_IDENTIFIED_RAW_ACCESS_BLOCKED_HTTP403. No data were purchased, privately accessed, or redistributed.

## Deduplication of another public human candidate

A fresh search surfaced Dal Bó and Fréchette 2011 human repeated-game data distributed as `DF2011` in the English-language `stratEst` package. Public documentation lists 7,358 rows and six fields `treatment,id,game,period,choice,other.choice`, with the original paper DOI https://doi.org/10.1257/aer.101.1.411 and package project https://github.com/fdvorak/stratEst . This is documentation-level metadata, not a new raw-file row audit. The package's code license/terms must not be treated as independent authorization to redistribute every underlying experimental record.

Project `research/R074/README.md` already documents Dal Bó's author-sourced second independent human experiment and actual source verification, including 18 sessions and 37,042 individual actions, with a different historical E3 terminology. Therefore this candidate is DUPLICATE_RESEARCH_FAMILY_PENDING_EXACT_DATASET_IDENTITY; no new R073 transfer experiment is initiated, and the historical E3 label is not counted as new E3 historical evidence under the current E1/E2/E3 convention. If a future comparison is needed, first establish whether the package's 7,358 rows are a strict subset, transform, or independent extraction of the R074 original author data.

A increment this round: exact official CSV download endpoint and its HTTP403 block, plus a documented dedup gate. New human E2 scoring=0; historical E3=0. No claims of full raw access or dataset-level license closure.
