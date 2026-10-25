# B evidence taxonomy audit: legacy external-human E3 labels versus current E2/E3 meanings

Date: 2026-10-26 Asia/Singapore
Status: CLASSIFICATION_CONFLICT_IDENTIFIED_AND_SCOPED
Scope: append-only audit, no historical source files or frozen labels overwritten.

## Collision

The current project-owner requirement explicitly separates **E1 synthetic**, **E2 real human**, and **E3 historical** evidence. Existing 2026-10-17 R074, R075, R076 and R077 archive files used the string **E3** for a different axis: cross-study validation on an independent *human repeated-game experiment*. Those two definitions are incompatible if interpreted as a single mutually exclusive evidence grade.

Examples directly verified from GitHub:
* `research/R074/R074_FINAL_ACCEPTANCE_STATUS.json`: `study_type=INDEPENDENT_REAL_HUMAN_EXTERNAL_AUTHOR_EXPERIMENT_INTERNAL_SESSION_LOSO_E3`.
* `research/R075/R075_FINAL_ACCEPTANCE_STATUS.json`: `study_type=THIRD_INDEPENDENT_REAL_HUMAN_AUTHOR_EXPERIMENT_WITHIN_STUDY_FULL_SESSION_LOSO_E3`.
* `research/R077/R077_FINAL_ACCEPTANCE_STATUS.json`: `scientific_evidence_grade=E3_BOUNDED_DIFFERENT_AUTHOR_HUMAN_EXPERIMENT_PRE_TARGET_MODEL_SCORE_PROTOCOL_BUT_NOT_PRE_EXPERIMENT_PREREGISTRATION`.

These archives document genuine **real-human behavioral experiments**, with independent original study identities and some external transfer. They are not historical longitudinal civilization data, institutional history or historical event forecasts.

## Safe read-time mapping, without retroactive relabeling

Preserve the legacy literal status field as source provenance. For current reports, represent evidence along independent axes:

| Archive | Current source class | Independent experiment | Evaluation transfer | Current E3 historical claim |
| --- | --- | --- | --- | --- |
| R073 | E2 human | Baseline study | Within-study session LOSO | None |
| R074 | E2 human | Second study | Same model formulas, new-study within-treatment session training and LOSO | None |
| R075 | E2 human | Third study | Same model formulas, new-study within-treatment session training and LOSO | None |
| R076 | E2 human | Reuses studies 2 and 3 | Source-only numeric transfer, retrospective after prior study results | None |
| R077 | E2 human | Fourth study | R073 source-only numeric transfer with zero target-label fitting, pre-first-target-score freeze and retained Rev-001 failure | None |

Do not sum R076 as an independent fifth study. Do not infer independent research-team replication from different original experiment authors: all current project model evaluations were conducted internally. Do not count human experiments as E3 historical evidence merely because the older machine JSON contains the string E3.

## Interpretation of the parallel A correction

The same-run A register `research/data_scout/R073_R074_R075_R076_R077_HUMAN_SOURCE_LINEAGE_AND_E3_GAP_CORRECTION_2026-10-26.md` cites the original R074–R077 **legacy E3 labels**. Its statements that second, third and fourth independent human experiments already exist are supported by the archived original study records. For the current user-defined taxonomy, these are **E2 human external-study replications**, with their respective training and validation limitations. The new A record adds no fresh E2 scores.

## Future required reporting fields

Always report `source_class=E1_SYNTHETIC|E2_HUMAN|E3_HISTORICAL`, `original_study_id`, `study_independence`, `model_parameter_training_source`, `target_label_used_for_fit`, `holdout_unit`, `protocol_timing`, `research_team_independence`, `legacy_archive_grade` separately. Maintain both current mapping and exact archived label for traceability.

This is an evidence classification correction. It adds no new behavioral predictions, historical validation, paid resources or CI executions. R073 and PESEN v0.1 remain frozen.
