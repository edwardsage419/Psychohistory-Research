# A data scout: Andreozzi et al. 2020 published opponent lag misalignment

Date: 2026-10-30 Asia/Singapore. Target key (A,Andreozzi2020,source-979abf87,opponent-wide-o-lag-column-validation). This complements the previous 1340-row partner-pair audit. No predictive model was fitted.

## Fixed source and license

Author repository: https://github.com/seyhunsaral/stabilitycondcoop
Paper: https://doi.org/10.1038/s41598-020-70681-z
Source commit: 979abf87b5d3cfb7aa8be13b81ef233076c3bb75.
Published cleaned file: data/csv/subjects.csv, Git blob bd4c1550002621bee7dfb50e0d15d317764d1ea9, 425701 bytes, 1340 rows, 67 fields, 134 people, six sessions, 10 post-practice periods.
Cleaning program: code/process_raw_data.R, Git blob 522efd459f574ccaef3d9ce1dd2b086ffb70370e.
Source LICENSE blob a7d26c9987564e97e270547d50707d7093ada753. Author README licenses data CC BY 4.0 and code MIT. No participant rows redistributed.

## Actual source-code and released-CSV check

The cleaning script first creates a within-person lag:
`mutate(opp_cond_class_wide_o_lag1 = dplyr::lag(opp_cond_class_wide_o, n=1, default=NA, order_by=subject_unq))`.

Later in the same pipeline, the script applies:
`mutate(opp_cond_class_wide_o_lag1 = replace(opp_cond_class_wide_o, period==1, NA))`.

The second expression reads the *current* `opp_cond_class_wide_o` and overwrites the earlier lag for periods 2..10. It does not read the lagged variable. This is a concrete preprocessing logic error for a variable whose name asserts one-period lag.

We actually read the complete published 425701-byte CSV and parsed it with a quote-aware CSV parser. For every subject we sorted periods 1..10 and compared the released lag field against current and prior period values. Results:

| Check | Count |
| --- | ---: |
| Published rows | 1340 |
| Unique subjects | 134 |
| Periods 2..10 compared | 1206 |
| Released `opp_cond_class_wide_o_lag1` equals **current** value | 1206 / 1206 |
| Released field equals **actual previous-period** value | 393 / 1206 |
| Released field differs from actual previous-period value | **813 / 1206** |
| Period 1 lag field nonmissing | 0 |
| Negative control `opp_cond_type_lag1` differs from actual previous period | 0 / 1206 |

Thus 813 of 1206 post-first-period rows have a provably incorrect value for the column labeled as lagged opponent wide-o class. The 393 matching rows are coincidental equal categories and do not demonstrate correct lag generation. The independent opponent type lag control matches actual prior periods in all 1206 rows, supporting the chronological comparison used here.

## Reproduction and limitations

Archived standalone Python audit: `research/data_scout/a_andreozzi_2020_lag_column_audit_20261030.py`. The actual published full CSV was checked in V8 against the source blob, with counts above. The archived Python script has not been executed natively against the full original CSV in this round. The source-code error was read directly; the original R/zTree raw-to-cleaned pipeline was NOT_RUN. These findings concern the published cleaned file and one lag variable, not all columns and not the study's reported scientific claims. Any downstream use of the named lag field should rebuild it from prior-period observations within each subject, after checking temporal ordering and group dependence, and compare results before/after. Avoid modifying or silently replacing the author's original CSV.

R073 frozen 100-round two-human PD replication eligibility remains NO for this ten-round different-task dataset. This is E2 data provenance/measurement auditing only. New E2 prediction tests=0; E3=0. No private data, no paid access, no extra fees.
