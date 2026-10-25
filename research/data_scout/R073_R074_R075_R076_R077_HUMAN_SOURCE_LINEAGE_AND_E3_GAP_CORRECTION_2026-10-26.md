# A data scout: R073 frozen-model external human study lineage and queue correction

Date: 2026-10-26 Asia/Singapore
Status: REPOSITORY_LINEAGE_VERIFIED / NO_NEW_DATASET_SCORED
Evidence: existing real-human E2 and cross-study E3 archives, no newly executed E2/E3.
Scope: append-only clarification of a cross-workflow research gap. No modification of R073, R074–R077 original files, frozen protocols, queue, crosswalk or operations E005.

## Why this check matters

The 2026-10-26 A file `MONTERO_2022_R073_ORIGINAL_SOURCE_IDENTITY_HARD_EXCLUSION_2026-10-26.md` correctly excludes Montero/Dryad as an independent replication of R073, because Montero is R073's own original experiment. However, operations E005-02 says a second independent human repeated-game dataset is still missing. That project-wide statement is contradicted by already archived R074, R075 and R077 results. The local `R073/README.md` label `E3=OPEN` refers to the original R073 closure scope, and must be interpreted alongside subsequent cross-study research, not as a statement that the entire repository has no external experiment.

## Source-identity and data-unit register

| Research | Original human study | Independent original participants/study | Fields and time units | Existing evaluation | Current availability |
| --- | --- | --- | --- | --- | --- |
| R073 | Montero-Porras et al. 2022, DOI 10.1038/s41598-022-11654-2; author submission Git CSV | Baseline original experiment, not independent of itself | 12 sessions, 188 humans, 100 rounds, own and past opponent C/D; 18424 eligible t>=3 decisions | Frozen M0–M6, whole-session LOSO, E2 internal | Original author Git CSV already scored; Dryad final-v8 byte equivalence unverified |
| R074 | Dal Bó & Fréchette 2011, DOI 10.1257/aer.101.1.411; original author TXT | Yes, different original study | 18 sessions, 37042 actions, 15338 t>=3 eligible targets, within-match own/opponent history | Same R073 seven formulas, per-treatment whole-session LOSO on new source, bounded E3 | Author TXT original SHA256 in R074 acceptance |
| R075 | Fudenberg, Rand & Dreber 2012, DOI 10.1257/aer.102.2.720; coauthor public ZIP | Yes, third original study | 18 sessions, 34446 intended action records, 26116 t>=3 targets; intention labels and noisy executed feedback differ | Same frozen formulas, whole-session LOSO on new source, bounded E3 | Coauthor ZIP original SHA256 in R075 acceptance |
| R077 | Drouvelis & Pearce 2025, DOI 10.1016/j.euroecorev.2025.105075; Zenodo 15462528 v1 | Yes, fourth original study | 15 sessions, 3620 person choices, 1040 fully eligible t>=3 targets; session, subject, game, own and other actions | R073 pooled-source parameters, zero target-label fitting, bounded external E3 | Zenodo v1 cleandata.dta MD5 4cce04ea68b7a0492c242b206efebe53; SHA256 in R077 acceptance |

R076 reuses the R074 and R075 originals for *retrospective* source-only numeric transfer. It does **not** constitute a fifth independent study. R096 and the Dryad Montero candidate reuse the R073 original study, likewise not new studies.

## Actual project evidence and negatives

Read original repository `research/R073/README.md`, `research/R074/README.md`, `research/R075/README.md`, `research/R076/README.md`, `research/R077/README.md`, and machine acceptance JSON for R074, R075 and R077 at main on this date.

R074: M3 minus M1 Brier = -0.022915328373344184 (16/18 sessions improve), while M4 minus M3 = +0.003170501040435799 (5/18 improve), an important negative cross-study result.

R075: M3 minus M1 = -0.029117355804310772 (18/18 improve), M4 minus M3 = -0.012416864447856633 (15/18 improve), but its no-execution-noise treatment worsens for M4.

R077: M3 minus M1 = -0.030210760470721517 (14/15 improve), M4 minus M3 = -0.001918699476466503 (8/15 improve). Rev-001 source eligibility failure and Rev-002 pre-first-target-score amendment are permanently retained. Its published experiment existed before this project; prospective applies to the internal target scoring freeze, not new recruitment.

R074 and R075 re-estimate conditional probabilities on training sessions of each *new* study. R076 performs numeric source-only transfer retrospectively after prior target results were visible. R077 performs zero target-label fitting on the fourth study with parameters trained on R073, with a documented pre-first-score protocol revision. These are different validation strengths and must never be pooled as identical prospective tests. Independent original participant samples do not constitute external independent research-team replication; all project evaluation code remains internally developed.

## New public source checks in this run

The English-language AEA publisher page for Dal Bó & Fréchette confirms the 2011 paper DOI and replication package: https://pubs.aeaweb.org/doi/10.1257/aer.101.1.411 .
Zenodo record https://zenodo.org/records/15462528 confirms 2025-05-19 v1, `cleandata.dta`, MD5 `4cce04ea68b7a0492c242b206efebe53` and publicly downloadable files. Its rendered License field is blank in this run, so the precise file-level license is **NOT VERIFIED**. The record says original study files may also be needed for the published paper's replication. No fresh binary bytes, person-level records, or license grant were downloaded or inferred in this run.

## Updated gaps and action gate

* `SECOND_INDEPENDENT_ORIGINAL_HUMAN_EXPERIMENT_ARCHIVED=YES` (R074); `THIRD=YES` (R075); `FOURTH=YES` (R077).
* `R073_OWN_CLOSURE_E3_LABEL=OPEN` remains unchanged; subsequent studies provide bounded external evidence elsewhere in the repository.
* `NEW_FIFTH_INDEPENDENT_EXPERIMENT=NOT_IDENTIFIED_THIS_RUN`.
* `EXTERNAL_INDEPENDENT_TEAM_REPLICATION=NOT_ESTABLISHED`.
* `HUMAN_CAUSAL_MEMORY_EFFECT=NOT_IDENTIFIED`.
* `R073_SOURCE_ONLY_TRUE_FUTURE_UNSEEN_NEW_EXPERIMENT=NOT_ESTABLISHED`.
* `NEW_E2=0`; `NEW_E3=0`; `COST=0`.

Next A task: screen a genuinely fifth original study or independently verify source/version and licensing gaps, with prespecified fields, complete session structure and target semantics. Avoid adding R074/R075/R077 as newly discovered datasets in future runs.
