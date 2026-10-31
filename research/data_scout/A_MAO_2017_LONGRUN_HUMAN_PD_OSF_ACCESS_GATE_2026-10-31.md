# A public data scout: Mao et al. 2017 long-run human repeated Prisoner's Dilemma

Date: 2026-10-31 UTC. Target key: (A,Mao-Dworkin-Suri-Watts-2017,publication-and-OSF-64z8u-v1,independent-longitudinal-human-PD-access-and-R073-gate). No participant-level data was accessed, copied or scored.

## Primary English-language evidence
Andrew Mao, Lili Dworkin, Siddharth Suri, Duncan J. Watts (2017), "Resilient cooperators stabilize long-run cooperation in the finitely repeated Prisoner's Dilemma", Nature Communications 8:13800, DOI 10.1038/ncomms13800. Open full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC5241863/ . Published data statement links https://osf.io/64z8u/ . Author experiment code repository: https://github.com/TurkServer/long-run-cooperation .

The primary article states 113 initially recruited participants, 94 completing the retention criterion, 20 weekday sessions across August 2015, 20 randomly rematched games per session, each game exactly ten rounds, and 374,251 total individual decisions. Each round records cooperation/defection and feedback on the opponent's action. Participants could encounter the same population repeatedly; a game is an independent pairing episode only after checking the actual assignment structure, and within-player games are dependent longitudinal observations. Article reports average 375 ten-round games and 3,720 decisions per retained participant. These published aggregate figures are not independently recomputed from raw data.

## Access, schema and license checks
Official journal article accessed and study design/round unit checked. OSF public data URL was attempted on 2026-10-31; returned HTTP 403 from the available browser, so no actual raw behavior file was downloaded. Raw row count, CSV schema, anonymized subject keys, session/game/round fields, pair identity, missingness, checksum, privacy filtering and OSF file-level license remain **NOT_VERIFIED**. The journal article itself carries CC BY 4.0; that does not by itself prove that OSF participant-level data has the same license.

The linked author GitHub README was separately read from the public repository. It describes a Meteor/TurkServer implementation and experiment demonstration; the README does not establish raw study data access or the OSF file license. No paid account, private data or fee-based API used.

## Scientific suitability and blockers
This is a promising **human longitudinal repeated-game** dataset with a very long participant history and many independently rematched ten-round games. It is potentially suitable for separately frozen E2 learning-across-games or within-game dynamics analyses after source/permission/privacy validation and a genuinely independent holdout split by participant/session as appropriate.

R073 requires an independent dataset matching its frozen continuous human-human repeated-game trajectory and scoring conditions. The article explicitly describes ten-round individual games. Concatenating the many games into one hundred-round game would cross opponent rematching and game-reset boundaries. **R073_CONTIGUOUS_100_ROUND_SUPERGAME = NO** for the described design. The presence of >100 total decisions per participant does not change that. The raw data gate is also blocked by OSF HTTP 403. No R073 scoring, no new E2 evidence.

## Reproduction readiness
Status: PRIMARY_PUBLICATION_VERIFIED; HUMAN_HUMAN_DESIGN_VERIFIED_FROM_PAPER; OSF_RAW_DATA_ACCESS_BLOCKED_403; FILE_LICENSE_UNKNOWN; RAW_FIELDS_UNKNOWN; R073_FROZEN_ELIGIBILITY_NO_BY_TEN_ROUND_EPISODES. Next lawful action: retry the official OSF public file listing through a permitted no-cost route, then check individual file license, source hash, anonymized identities, game IDs and per-game round maxima. Do not concatenate game episodes or adapt R073 after inspecting outcomes. Preserve privacy review before storing or sharing any participant records.
