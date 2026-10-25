# A public data scout: SocioPatterns 2013 high school temporal contacts and friendship survey

Date: 2026-10-26 Asia/Singapore. Status: `OFFICIAL_SOURCE_SCHEMA_LICENSE_VERIFIED / RAW_COMPRESSED_BYTES_PENDING / R169_OPINION_OUTCOME_ABSENT`. Newly registered candidate, not a new R073 repeated-game experiment and not an R169 human-model prediction validation.

## Official provenance and published measurements

Official source: https://sociopatterns.org/datasets/high-school-contact-and-friendship-networks/ (published 2015-07-15). Source-maintained public English-language dataset description: https://github.com/SocioPatterns/sociopatterns.github.io/blob/main/_datasets/high-school-contact-and-friendship-networks.md . Original peer-reviewed paper: Mastrandrea, Fournet, Barrat (2015), PLOS ONE 10(9): e0136497, https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0136497 . The dataset is from a Marseille high school in December 2013, nine classes, five days of sensor contacts.

The source's temporal-contact record format is `t i j Ci Cj`: timestamp t in UNIX seconds, two anonymous person identifiers i,j, and class identifiers Ci,Cj. A row records an active face-to-face proximity edge in a 20-second interval. Multiple edges may share a timestamp. The same site publishes directed contact diaries `i j w` (duration category 1..4), directed friendship survey `i j`, known Facebook-link pairs `i j w` (w=0/1), and metadata `i Ci Gi` (class and gender).

The original site provides public links for compressed `HighSchool2013_proximity_net.csv.gz` (approximately 653 KB), `HighSchool2013_contactdiaries_network.csv.gz`, `HighSchool2013_friendship_network.csv.gz`, `HighSchool2013_facebook_known_pairs.csv.gz`, and `HighSchool2013_metadata.txt`. Official download paths are published in the dataset-maintainer's source repository. Terms: Creative Commons Attribution-NonCommercial-ShareAlike, specifically the official source HTML points to BY-NC-SA 3.0. The data license is noncommercial with attribution and share-alike obligations. No raw personal names were sought.

## Actual checks and limitations

Verified this round: live official dataset page, publication link, source-maintained file names, documented column meanings, 20-second temporal resolution, anonymous stable IDs within the study, multiple measurement channels, five-day window, and license text. No prior matching SocioPatterns high-school source gate was found in the current repository path tree before registering this candidate.

Blocked this round: raw .gz bytes could not be downloaded into the local calculation environment due to network DNS restrictions, and the GitHub text connector cannot parse compressed binary downloads. Therefore actual row count, unique person count, timestamp ordering, missingness, checksums, and cross-file identifier consistency are **UNVERIFIED**. No data rows are redistributed. The separately curated Zenodo hypergraph derived from this source is not an independent experiment and must not be counted as one.

## Model compatibility and independent units

R169 needs each person's evolving binary opinion and explicit rewiring versus adoption transitions, with known event clock. The observed data record temporal physical contacts and separate static reported friendships. Neither a binary opinion trajectory nor explicit choice between opinion adoption and rewiring is supplied. A disappearing sensor contact cannot be equated to deliberate social-tie rewiring. Thus no valid R169 parameter fit or out-of-sample opinion prediction can currently be scored. It may support future **network-only descriptive E2 measurement checks** after a separately frozen observation mapping, not a direct replication of R169's artificial E1 mechanism.

This is one school over five days. The nine classes, students and daily contact windows are dependent; counting days, edges or 20-second rows as independent studies would be pseudoreplication. Potential future blocked design: group by full student/community and time; define nonoverlapping train/test time windows without leakage of future contacts; retain full node identities only as anonymized codes; report block bootstrap uncertainty at an appropriate cluster level. No such score was computed.

R073 frozen repeated-prisoner's-dilemma scoring is inapplicable because this dataset contains no paired C/D game actions or independent repeated-game sessions. R073 model and scoring remain untouched. E2 newly scored = 0; E3 history = 0; external replication = 0.

## Next access gate

Only after lawful no-cost download: verify compressed file SHA256, count lines, inspect separators and timestamp range, validate anonymity and per-file join coverage, and document a network-only independent prediction question before scoring. If binary opinions and rewiring choices cannot be obtained, preserve `R169_DIRECT_E2_BLOCKED_BY_OUTCOME_MISMATCH`. No new cost or private data is permitted.
