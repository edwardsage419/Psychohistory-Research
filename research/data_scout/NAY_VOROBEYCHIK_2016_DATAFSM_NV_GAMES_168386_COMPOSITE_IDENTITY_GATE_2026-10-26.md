# A data scout: Nay and Vorobeychik NV_games composite human IPD source gate

Date: 2026-10-26. Repo HEAD checked before write: 84b247886a3eea9443c0e0e7d47de91f2d433e43. Scientific status: SOURCE_DOCUMENTATION_AND_GIT_BLOB_VERIFIED; ORIGINAL_RDA_BINARY_NOT_DECODED; INDEPENDENT_R073_SOURCE_NOT_ESTABLISHED.

## Verified upstream sources
* Nay and Vorobeychik (2016), *Predicting Human Cooperation*, PLOS ONE 11(5), e0155656, DOI https://doi.org/10.1371/journal.pone.0155656.
* Upstream public GitHub repository: https://github.com/JohnNay/datafsm, branch master, Git tree `c2e55eab12f1a24d3a5b09a9b42aeefff8bc5be4` at inspection.
* Upstream source documentation: https://github.com/JohnNay/datafsm/blob/master/man/NV_games.Rd, Git blob `be625b217505dd05781f5bd9c12925df673a7ac0`, 4,245 bytes, actually read in UTF-8.
* Upstream binary `data/NV_games.rda`, Git blob `36a961908385a7fe33ba688479b5dfc7b0a6b609`, 761,556 bytes, existence and identity verified from the upstream Git tree. Binary contents could not be read through the GitHub UTF-8 text connector, so 168,386 is a **published documentation count**, not a first-hand row count.
* Package LICENSE.md, Git blob `c3cb9e0116916537880c87633bb506051d53d4ae`, MIT license for package software and documentation. Separate original human-study redistribution permissions are not established by this software license.

## Published schema and unit of observation
The `NV_games` man page describes **168,386 rows, 51 columns, 30 game variations** and per-turn decision `my.decision`, `period`, lagged own and opponent actions `my.decision1..9` and `other.decision1..9`, lagged payoffs, treatment/game parameters, source code `data`, and `group` as a game version. It attributes eight underlying studies: AM (Andreoni and Miller), BR (Bereby-Meyer and Roth), DB (Dal Bo), DF (Dal Bo and Frechette), DO (Duffy and Ochs), FO (Friedman and Oprea), FR (Fudenberg, Rand and Dreber), KS (Kunreuther et al.).

The documented 51 columns **do not list a participant ID, opponent ID, dyad ID or independent experimental session ID**. `group` is documented as game version, so it cannot be assumed to be a session identifier. Consequently leave-one-session-out splitting and leakage-safe identity separation cannot be certified from this derived object. Lagged columns may encode prior actions, but reconstruction of exact game boundaries and whether decisions are intended or realized remains unresolved.

## Source independence and R073 eligibility
This is a composite derivative of eight historical experiments. It is not a ninth independent human experiment. DF overlaps the already indexed Dal Bo and Frechette 2011 R074 source; FR-related data may overlap earlier project studies and requires original experiment identity matching. Any additional source must be checked study by study against R073, R074, R075, R077 and other E2 archives. A model trained or tuned on this composite could leak into a supposedly independent held-out source.

Status: `PUBLIC_DOCUMENTATION_VERIFIED / ORIGINAL_BINARY_UNREAD / SESSION_AND_PAIR_IDENTIFIERS_UNPROVEN / R073_FROZEN_NOT_SCORED`. Next action: locate primary-study row-level original files with stable subject, opponent and session IDs, verify licenses, reconstruct original row counts, freeze data mapping and only then consider locked R073 scoring. No purchase, registration or access-control bypass was attempted. E2=0, E3=0.