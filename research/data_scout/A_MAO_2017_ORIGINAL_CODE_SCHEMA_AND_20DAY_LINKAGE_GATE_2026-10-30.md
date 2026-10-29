# A source scout: Mao et al. 2017 original code schema and longitudinal linkage gate

Date 2026-10-30 Asia/Singapore. Target key (A,Mao2017,author-code-4d8ed83e,raw-behavior-identity-and-time-join). Complementary to prior A_MAO_2017_LONG_RUN_PD_OSF_ACCESS_GATE_2026-10-30.md. This report does not claim new raw human data.

## Verified primary sources
Paper: Mao, Dworkin, Suri and Watts (2017), Nature Communications 8:13800, DOI 10.1038/ncomms13800, https://www.nature.com/articles/ncomms13800. The paper reports 94 completing participants, 20 consecutive weekdays, up to 400 ten-round repeated PD games per person, and 374,251 decisions in total. Its data availability section points to https://osf.io/64z8u/.

Original author experiment code: https://github.com/TurkServer/long-run-cooperation pinned master commit 4d8ed83e7745e1ffe82ce9403064e3558fabfa6f (committer date 2022-01-09). Read actual files:
* models/models.js Git blob f55a61ee2533a6fdff8ce29b14cfcd69adee9764. Actions schema comment states roundIndex (1–10), userId, action (0/1), payoff. GameGroups store instances and counter. This is a code-level schema claim, not a verified raw-data header.
* library.py Git blob c331ba695c3846935c5e3e640e53569e78208c28. NUMROUNDS=10, NUMGAMES=20; get_instances joins gamegroups by batchId and counter, get_rounds queries actions by _groupId and orders by roundIndex; gen_worker_games_dict uses assignment workerId and batchId to recover experiment instance IDs; remove_abandoned filters experiment endReason == finished.
* server/server.js Git blob 3e135c7558c929d8a81f750694327b82ba7c5d82. chooseActionInternal records userId, roundIndex, timestamp and action with upsert; game/round identifiers must be reconciled with partitioned data before replay.

## Reproduction eligibility
Proposed row key requires (day batch, supergame counter, instance/group, roundIndex, pseudonymous player) and an opponent linkage within each instance. Per-person longitudinal units are repeated across days. The dyad is rematched across ten-round games. Treating each round or game as an independent participant would understate uncertainty. Missing or abandoned games require separate gates, including endReason and round count. Raw pseudonymous IDs must remain private; do not expose or upload identifying records.

Attempted public OSF node https://osf.io/64z8u/ and https://api.osf.io/v2/nodes/64z8u/files/ in this run: webpage HTTP 403, API access failed. Raw file list, actual field values, pseudonym stability, partner identity, license and complete row count **NOT_VERIFIED**. The author GitHub repository root contains no data directory and no visible LICENSE in the inspected root listing; article CC BY 4.0 does not by itself establish rights for a separate OSF raw dataset.

R073 frozen double-player 100-contiguous-round direct transfer eligibility: FAIL_APPLICABILITY on the known 10-round per-dyad design. A distinct 20-day longitudinal study might be possible after obtaining the raw records and verifying stable pseudonymous linkage and usage rights, with a separately frozen protocol. No R073 refitting, no human E2 prediction and no data purchase.

Status: CODE_SCHEMA_PARTIAL; RAW_SOURCE_BLOCKED; REPLICATION_NOT_READY. Next: retrieve official OSF file listing and rights if publicly accessible; otherwise retain access gate without treating paper-level counts as row verification.
