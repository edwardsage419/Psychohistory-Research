# R127 / original239 05-003 Coordination Game: bounded independent itemwise audit

track: R+B
subflow: original239 P0 itemwise primary source and independent finite mathematics
run_date_utc: 2026-11-02
local_date: 2026-11-03 Asia/Singapore
starting_main: bce678be65257ecf8dd7c3445bce15efdfe22cc2
status: COMPLETE_BOUNDED_INTERNAL_EXACT / ORIGINAL239_FORMAL_QUEUE_PARTIAL
evidence: INTERNAL_NONBLIND_ARTIFICIAL_E1_AND_PUBLISHED_AGGREGATE_TRANSCRIPTION
CI: NOT_RUN
billing_checked: NO; no new paid services or workflow dispatch
target_key: (R+B,05-003/R127,2026-10-20-freeze,independent-exact-itemwise)

## Question and fixed scope

Can a standard-library calculation importing none of the original R127 code independently reproduce the frozen minimum-effort payoff universe, seven reported 1990 experiment margins, and finite symmetric 2x2 risk-dominance counts? This is a limited mathematical and transcription audit, not a new human behavioral prediction or a new transcription of the original article.

Source boundaries:
* Frozen protocol: `protocols/R127_VAN_HUYCK_1990_MINIMUM_EFFORT_ORIGINAL_TABLE2_AND_2X2_RISK_SELECTION_FREEZE_2026-10-20.md`, Git blob `4734ede5133701d622acfda76c4f9474bf660b21`.
* Archived R127 source `research/R127/r127_van_huyck_1990_min_effort_coordination_selection_exact.py`, Git blob `6964fa57e291e719e8cc071cc3a70d73836363e4`. Its implementation was inspected only to establish prior scope; the new calculation does not import it.
* Historical R127 acceptance `research/R127/R127_FINAL_ACCEPTANCE_STATUS.json`, blob `3aa5ed67f4d38f91474352627451e46500cde210`.
* Original article previously identified: Van Huyck, Battalio & Beil, AER 80(1), 1990, 234–248. Original scan at https://econweb.ucsd.edu/~jandreoni/Econ264/papers/Van%20Huyck%20et%20al%20AER%201990.pdf . This run did **not** freshly inspect the scan; published counts were transcribed from the already frozen protocol. Therefore the source transcription is not independently verified against paper images this run.
* original239 crosswalk v7.8 blob `36f24235901172642c46853298aebb421f1a3552`; pending154 CSV blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`. The current CSV row for 05-003 remains P0, PROVISIONAL_PRIMARY_README_LINK, ITEMWISE_PRIMARY_SOURCE_AND_SCIENTIFIC_EVIDENCE_AUDIT_REQUIRED.

## Executed independent calculations

The new standard-library program `research/validation/r127_original239_05_003_independent_exact_gate_20261103.py` has Git blob `18278991e122bc24347395ab8ff043092940b151`. Its exact Git blob was reconstructed locally and tested in CPython 3.13.5 normal, -O, and -OO modes. Each mode ran seven unit tests: three actual rejection controls (bad group margin, negative category count, missing session), three mathematical boundary controls (cash offset, risk tie, strict conflict), and one complete positive receipt. All 21 executions passed. No randomness was used.

The exact rational-number oracle independently computes all 2,793 effort profiles for group sizes 2,3,4, and 75,117 individual candidate payoff comparisons. Both the direct full-profile formula and the separate minimum-of-other-players formula agree. Every group size has exactly seven strict all-equal Nash profiles. The 1990 published aggregate transcription yields seven sessions totaling 107 participants, 33 choosing effort 7 in period 1, 2 choosing effort 1 in period 1, and 77 choosing effort 1 in period 10. This only checks the frozen transcription's internal margins.

The independent symmetric 2x2 enumeration of integer row payoffs a,b,c,d in 0..5 covers all 1,296 matrices. It finds 225 with two strict diagonal Nash equilibria, 30 with strict payoff versus risk dominance conflict, and 55 with tied risk products. The indifference belief is checked directly from the two expected payoff expressions for each qualifying game. All counts agree with archived R127 bounded E1 claims.

Machine receipt: `research/validation/R127_05_003_INDEPENDENT_FINITE_ORACLE_RECEIPT_20261102T1940Z.json`. The new checker itself is an independent algorithm within the same project, with historical model/protocol knowledge available to the reviewer. It is not blind or external-team reproduction.

## Scientific limits and queue disposition

No source-level numerical discrepancy was found in this fixed finite domain. This supports bounded mathematical reproducibility. It does not independently authenticate the 1990 scan transcription, reproduce individual decisions, estimate a longitudinal learning rule, establish causal equilibrium selection, or test transfer to unseen real sessions. The synthetic 2x2 matrices are project-created and distinct from the published multi-person minimum-effort experiment.

R127 historical finite E1 closure remains preserved. original239 05-003 gains a new independent exact-math audit artifact, but the crosswalk and formal pending CSV are unchanged pending independent governance/source review. Pending queue net reduction: 0. New E2=0, new E3=0, external team replication=0.

## Concurrent project, data scout, and next action

At entry main was `bce678be65257ecf8dd7c3445bce15efdfe22cc2`; twelve Codex PRs remained open, including #1/#3 for R257 S53. No open Codex PR was scoped to R127 05-003. R272 production enforcement P0 remains open; this itemwise audit does not affect it. R073 and PESEN v0.1 remain frozen.

A-scout briefly checked English-language public datasets for long repeated prisoner's dilemma. The 2022 Montero-Porras Zenodo record and 2020 Grujić Dryad data were already within project source scouting; computer-only Axelrod tournament records are ineligible as new human E2. No new eligible independent data were downloaded or scored this run.

Next highest-value action is to execute R272's pinned single entrypoint against a complete trusted checkout and perform the missing production enforcement review. For 05-003, an independent reinspection of the primary article's actual Table 2 cells and source identity is the remaining source-verification gate before considering formal queue reduction. No production workflows or branch rules were changed; Actions costs and account billing were not independently checked.
