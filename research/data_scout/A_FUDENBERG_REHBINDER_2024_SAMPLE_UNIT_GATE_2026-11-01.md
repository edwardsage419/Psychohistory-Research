# A data gate: Fudenberg and Karreskog Rehbinder (2024), 17-study repeated PD archive

Date: 2026-11-01 UTC. Track: R/A. Status: PARTIAL_SOURCE_DESIGN_ONLY; RAW_DATA_BLOCKED; R073_FROZEN_TEST_ELIGIBILITY_UNKNOWN.

## Verified sources

Published article: Fudenberg, Drew, and Gustav Karreskog Rehbinder (2024), "Predicting Cooperation with Learning Models", American Economic Journal: Microeconomics 16(1):1–32, DOI [10.1257/mic.20220148](https://doi.org/10.1257/mic.20220148).

Author-hosted English prepublication manuscript: [MIT PDF, December 2022 location](https://economics.mit.edu/sites/default/files/2022-12/Predicting_Cooperation_with_Learning_Models.pdf), Section III, pages around 6–7. Its stated analytic corpus is **17 papers, 28 treatments, 161 laboratory sessions, 2,612 distinct participants and 232,298 individual choices**. Median session average realized supergame length is **6.7 rounds**. These counts come from the author-hosted manuscript and are not yet independently verified against raw records or proven identical to every published 2024 table.

Official archived replication project: [openICPSR 182668 V1](https://www.openicpsr.org/openicpsr/project/182668/version/V1/view), published 2024-01-19. The official directory exposes raw_data, clean_data, code, results_data and README folders/files and states compilation from 17 experimental papers. The archive explicitly notes depositor-provided files were not checked or processed by ICPSR.

## Scientific unit and leakage gate

The paper distinguishes an individual round inside a repeated game from a **supergame**, which is a complete repeated-game match. Its published predictive task targets cooperation rates and time paths, with session-level correlation. The manuscript describes session-level cross-validation and notes that using data from the session being predicted would make a history-dependent prediction unsuitable for its own out-of-sample task.

R073's frozen independent-data test requires the exact predeclared sequence, dyad identity, sufficient continuous within-match rounds, and unchanged model/scoring rules. A large total count of individual choices across many short supergames cannot establish 100 consecutive rounds with the same partner. The median supergame length 6.7 is strong evidence of a substantial task-granularity mismatch, while the maximum per-match length remains unknown. R073 eligibility remains **UNKNOWN**, not PASS. No 2024 source data have been scored with R073.

Before any empirical replay: obtain the raw files through a free authorized route; verify file license and SHA256, subject/session/supergame/opponent keys, original time ordering, partner rematching, maximum contiguous dyad length, trial action fields and overlap with prior R073 source lineage. Freeze a study-level independent test split before seeing target outcomes. Retain the published model's out-of-sample task separately from R073's frozen individual prediction task.

## Actual access and limits

Official V1 metadata and directory were readable through public HTML. Attempts to open the README.md and clean_data directory from the public interface timed out. Raw file bytes, row schemas, license details, identity and game-length distribution remain NOT_OBTAINED. No private data, paid account, or third-party dataset was copied into this repository. New E2 predictions: 0. New E3 predictions: 0.

This is a source-and-unit refinement of the previously registered 17-paper candidate, not a new independent empirical validation. The next useful A task is to verify file-level metadata and original per-match duration through an accessible free mirror or the official repository, while checking lineage duplication.
