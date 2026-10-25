# A: Montero et al. 2022 long iterated human PD, independent session candidate

Audit date: 2026-10-25. Status: HIGH_PRIORITY_SOURCE_VERIFIED_ROW_ACCESS_BLOCKED. No R073 scoring performed.

## Directly checked non-Chinese primary sources
* Author deposited dataset: https://datadryad.org/dataset/doi:10.5061/dryad.37pvmcvmk (published 2022-05-25).
* Author-linked journal paper DOI: https://doi.org/10.1038/s41598-022-11654-2.
* Secondary metadata mirror: https://zenodo.org/records/5822760 (contains an HTML pointer, not raw CSV).
* Dryad lists fix.csv (742.09 kB), rand.csv (796.02 kB), README.txt (1.52 kB), UserInformation.csv (6.83 kB) and experimental instructions.

The Dryad methods explicitly describe 12 separate laboratory sessions, 188 human participants, two repeated two-player Prisoner's Dilemma treatments, and payoff R=3,T=4,S=0,P=1. Six fixed-partner sessions involve 92 participants. Six shuffled-partner sessions involve the remaining 96 participants. This makes the fixed-partner subset potentially suitable for a strict independent-session, binary-action R073 transfer test. Shuffled-partner observations require explicit opponent-ID checks.

## Actual access attempts and limitations
Web fetch of the official Dryad README file_stream/1514376 and fix.csv file_stream/1514373 returned HTTP 403. A separate environment request could not resolve datadryad.org. The Zenodo mirror exposes a small HTML pointer only. No CSV bytes were retrieved; no row count, schema, missingness, round number, unique session key, partner matching, or exact individual behavioral records were inspected. The Dryad record describes open public data, but dataset-specific redistribution/license terms were not independently retrieved; license gate remains UNVERIFIED. Do not infer that every participant has a unique ID across sessions from the article description.

GitHub code search for Montero and the Dryad DOI within Psychohistory-Research returned zero results at this check. Code search is not a complete content deduplication proof. Before use, compare R073/R074/R075 and other research source registries and fixed hashes.

## Frozen transfer eligibility gate
1. Obtain the exact original README and fixed-treatment CSV without payment, accounts or private access. Verify publisher dataset license and immutable file identity/hash.
2. Confirm binary own and partner actions, round and participant keys, true session identity, fixed partner, chronology and completeness.
3. Construct predictor features only from prior rounds. Never include current partner action, current payoff, end-of-game questionnaire or session outcome.
4. Preserve the R073 frozen model, feature rules, train/test partition logic and scoring. Require leave-one-true-session-out; no post hoc retuning or recoding.
5. Compare prespecified baseline and calibration; use session-cluster uncertainty, explicitly count 6 fixed sessions, and disclose power limitations. Evaluate shuffled condition separately only if the frozen protocol applies without modifications.
6. Preserve E2 status as ZERO until raw records, source independence and out-of-session scoring are all verified.

Decision: SOURCE_AND_DESIGN_HIGH_VALUE; RAW_BYTES_BLOCKED_403; REPRODUCTION_NOT_READY; R073_FROZEN.
