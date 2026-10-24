# A public data scout: DF2011 actual original RDA row decoding

Date: 2026-10-24. Gate: **RAW_ROWS_DECODED_SCHEMA_CHECKED_SESSION_AND_IDENTITY_GATES_OPEN**. No new E2 prediction.

## Fixed original public source

Dal Bó and Fréchette (2011), *The Evolution of Cooperation in Infinitely Repeated Games: Experimental Evidence*, AER, DOI 10.1257/aer.101.1.411. Original binary is public CRAN mirror `cran/stratEst` at fixed commit `a6373b23d80dc816a63f18f973d372c9e8421914`, file `data/DF2011.rda`. Verified 3298-byte bzip2 RDA and Git blob SHA1 `52e216b02e1a7ab7fb1a6e335b5f7e2ef6b7f5a0`. Original data copyright and CC BY 4.0 were identified in upstream `inst/COPYRIGHT.txt`; no original rows were redistributed.

Protocol frozen at commit `84c855b44c8ec5450462ae4971b6d9caf2bf9892` before executable decoding. Audit script `research/data_scout/audit_df2011_fixed_blob_decode.py` downloads only the fixed public binary, checks identity, decodes with pinned free open-source `pyreadr==0.5.4`, and prints aggregated schema metadata without participant-level rows.

## Verified results from actual decoded rows

GitHub Actions run https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40083592838 finished `completed/success`. Job `120841917439` logged:

| Field | Verified value |
| --- | --- |
| RDA object | DF2011 |
| Original rows | 7358 |
| Original columns | treatment, id, game, period, choice, other.choice |
| Missing values in six fields | 0 each |
| Action categories | c, d in both choice fields |
| Treatment categories | D5R32, D5R40, D5R48, D75R32, D75R40, D75R48 |
| Distinct treatment plus participant ID combinations | 266 |
| Participant IDs reused across treatment labels | 0 |
| Distinct supergame number labels | 51 |
| Distinct period number labels | 23 |
| Maximum observed period | 23 |
| Duplicate (treatment,id,game,period) keys | 0 |
| Mutated binary and wrong SHA rejection controls | 2 passed |

These are direct checks of decoded original rows, stronger than the previous upstream-document-only 7358-row claim. Distinct `game` labels are labels rather than proof of 51 independent laboratory sessions. The six fields do not explicitly include a laboratory session ID, unique opponent pair ID or independent pairing roster. We have not verified whether `id` is a globally independent actor key across all supergames, nor whether there are repeated opponent matches.

## R073 external replication gate

This is a distinct human repeated prisoner's dilemma study candidate. It is still **BLOCKED_FOR_R073_HELDOUT_EVALUATION** pending a defensible session or actor-disjoint split, partner pairing identification, strict within-game lag construction and a frozen-feature compatibility check. Contemporaneous `other.choice` must never be used to predict the same round. The R073 model and scoring rules remain frozen; no tuning or scoring was executed. New real human E2 scores: 0; historical E3: 0. The A data decoding work does not itself certify an E2 scientific prediction result.

This run used a public repository standard GitHub-hosted Ubuntu runner and free open-source software, with no paid APIs, private participant data, large runner or original data redistribution.
