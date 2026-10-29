# A track: Akata et al. human-versus-LLM repeated games raw CSV field audit

Date 2026-10-29 UTC. Key `(A,eliaka/repeatedgames@224a605a21127cac69763f990e077f7b05abd422,human_experiment/repgames.csv,identity-round-payoff-license)`. New candidate, distinct from Montero 2022 and the existing R073 12-session cohort.

## Primary English-language sources actually read

* Author repository: https://github.com/eliaka/repeatedgames , fixed main HEAD `224a605a21127cac69763f990e077f7b05abd422`; paper preprint https://arxiv.org/abs/2305.16867 .
* Raw cleaned human experiment file: `human_experiment/analysis/repgames.csv`, Git blob `2dd67c6ff80f2d7aa07a70b470e26fe3592c6d95`, 97,945 UTF-8 bytes. Directly read all rows via the GitHub connector and checked schema and groups. https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repgames.csv
* Original experiment instructions: `human_experiment/experiment/README.md`, Git blob `77115c8edb43dbc7ef8bc46e596f67d58f2c8f81`. The instructions specify two games, each 10 rounds, and the prisoner's dilemma payoff matrix 8/8, 0/10, 10/0, 5/5.
* Analysis script `human_experiment/analysis/repeated_games.Rmd`, blob `ca9991b6d0917156672e1e2fea923548562d945e`, explicitly says this is cleaned Prolific human data. Experiment JS `human_experiment/experiment/js/script.js` shows game-block order is randomized. Root `LICENSE.md` blob `108cffb7c9fcd38dadc419f4c18e4e3e0afb4407` contains the MIT license for software and associated documentation; separate raw participant-data redistribution authorization has not been identified.

## Raw file audit

CSV header: `id,game,action,score,opponent,guess,coordination`. Exactly 3900 rows, seven columns, no empty cells. There are 195 distinct numeric anonymous `id` values (1 through 195), with 20 rows per id. Each id has exactly ten `PD` and ten `BoS` rows: 1950 prisoner-dilemma and 1950 Battle-of-the-Sexes actions. Each id/game's ten records form one contiguous block. For 98 of 195 participants BoS appears first, so assuming PD is always the first block would misorder data. No explicit round-index column exists; within-block row order can be treated only as an inferred round index, with original collection/export ordering still requiring verification.

The `opponent` condition is `Base` (1940 rows) or `Prompted` (1960 rows); `guess` is `LLM` (1990) or `Human` (1910). These two columns are constant **within each participant-game block**, and may differ between the two games for the same person. Thus `opponent` labels the LLM prompt treatment, not the opponent's per-round cooperation action. The `guess` column is a participant's human/LLM guess, not a true partner-identity key. Each participant interacts with an LLM, so these 195 human subjects cannot be treated as 195 independent human-human dyads.

For the 1950 PD rows, observed `action|score` pairs are `0|10` (235), `1|0` (213), `0|5` (783), `1|8` (718), and **`0|0` (1)**. The first four combinations are compatible with a binary action mapping (0 defection, 1 cooperation) and the published PD payoff matrix; `0|0` is incompatible under that mapping and the stated deterministic matrix. It occurs at anonymous id 153, CSV line 3061. This is a concrete negative data-quality observation. Do not silently recode, drop or impute it. The analysis Rmd also uses `score==5` as a `cooperated` proxy, which does not match the published matrix's mutual-defection payoff under this action mapping. That discrepancy needs author-code reconciliation before deriving an opponent action history from payoffs.

## Suitability and legal gate

Human behavioral records and anonymous participant IDs: `VERIFIED_RAW_CSV`. Two ten-round repeated game blocks per participant: `VERIFIED_FILE_STRUCTURE`. Exact chronology of rows within each block: `INFERRED_NOT_SOURCE_CONFIRMED`. Opponent identity and per-round opponent actions: `NOT_EXPLICITLY_PRESENT`; payoff reconstruction has one known inconsistency. File-level data license: `OPEN`; MIT root software license is visible, but data-specific reuse and redistribution scope remains to be checked. Source was accessed through a public repository without login or payment; no sensitive demographics were read.

R073 frozen direct 100-round human-human protocol eligibility: `NO` (only ten PD rounds and human-versus-LLM pairing, without an explicit independent human opponent history). Potential future **separate** E2 study of human-versus-LLM conditional choices: `CANDIDATE_WITH_DATA_QUALITY_AND_ROUND_ORDER_GATES`. No model fit, scoring, or new E2 result in this cycle. Do not redistribute the raw participant-level file pending license clarification.

Next: inspect author JS and R analysis mapping for `action` and `score`, establish whether row 3061 is an export/recording error, verify order preservation, and seek data-specific reuse permission. R073 and PESEN v0.1 remain frozen. No added costs.
