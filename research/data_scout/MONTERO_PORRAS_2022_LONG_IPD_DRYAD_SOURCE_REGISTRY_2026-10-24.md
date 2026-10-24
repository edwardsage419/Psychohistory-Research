# A: Montero-Porras et al. (2022) long iterated Prisoner's Dilemma source registry

Date: 2026-10-24. Status: **PUBLIC_METADATA_VERIFIED; RAW_ROWS_NOT_ACQUIRED; R073_EXTERNAL_SCORE_NOT_RUN**. Independent candidate screening only. This is not a new E2 result.

## Primary non-Chinese sources actually inspected

* Author's Dryad dataset landing page: https://datadryad.org/dataset/doi:10.5061/dryad.37pvmcvmk (published 2022-05-25), dataset DOI 10.5061/dryad.37pvmcvmk.
* Montero-Porras, Grujić, Fernández Domingos and Lenaerts (2022), *Inferring strategies from observations in long iterated Prisoner's dilemma experiments*, Scientific Reports 12:7589, DOI 10.1038/s41598-022-11654-2, https://www.nature.com/articles/s41598-022-11654-2 .
* Dryad's official reuse policy https://datadryad.org/help/guides/reuse states Dryad datasets use CC0. Licensing is confirmed at platform policy level; verify any embedded third-party file restrictions before redistributing.
* A related Zenodo deposit https://zenodo.org/records/5822760 was inspected. It lists a 29.2 kB HTML file, not the Dryad experiment CSVs; do not count as independent data or a substitute for the original CSV.

## Confirmed dataset design and available files

The Dryad dataset page lists `fix.csv` (742.09 kB), `rand.csv` (796.02 kB), `README.txt` (1.52 kB), `UserInformation.csv` (6.83 kB), and an experiment instructions DOCX (1.05 MB). The two treatments are fixed partners (FP) and shuffled partners (SP). Authors report **12 sessions, 188 human participants**. FP: 6 sessions, 92 participants; SP: 6 sessions, 96 participants by subtraction from total, pending direct row-level verification. In each treatment participants played iterated prisoner's dilemma with R=3, T=4, S=0, P=1. The author describes round-by-round behavior and anonymous partner matching, with fixed partners versus rematching every round.

These counts and conditions are **published metadata claims**, not independently recomputed from raw files. Raw field names, individual round counts, participant IDs, session identifiers, opponent pairing columns, treatment coding, uniqueness constraints, missingness, lag alignment and any user demographics have **not been verified**.

## Actual acquisition attempt and blocker

The official Dryad page displayed the five file names and download links. A direct retrieval attempt through the available web reader for `README.txt` (file_stream/1514376) and `fix.csv` (file_stream/1514373) returned **HTTP 403 Forbidden**. No CSV or README bytes were acquired. The linked Zenodo record does not supply the experiment CSVs. No purchased access, paid account, private participant records, API subscription or scraping circumvention was attempted.

## R073 frozen external reproduction gates

This appears to be a **distinct 2022 original experiment** from the prior R074 Dal Bó/Fréchette 2011 and R075 Fudenberg/Rand/Dreber 2012 sources. Before asserting independence, inspect any historical R-series reuse of this DOI and participant overlaps. Required gates before E2 scoring: download source bytes lawfully; pin DOI version and hashes; parse README and full CSV; establish exact session IDs and whether any subject crosses sessions; validate round, own action, opponent action and pairing; build strictly lagged predictors; preserve R073 model and scoring without tuning; freeze exclusion rules and held-out session splits; compare existing baselines, calibration and session-clustered uncertainty. Shuffled rematching each round may require a distinct compatibility determination under the original frozen R073 contract. If it cannot be mapped without changes, report `INCOMPATIBLE_WITH_FROZEN_R073` and do not score.

**Priority:** promising new independent human dataset, acquisition blocked in this run. No E2, no E3, no new expenditure, no raw personal information downloaded or archived.
