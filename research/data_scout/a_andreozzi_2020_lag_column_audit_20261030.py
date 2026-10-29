#!/usr/bin/env python3
"""Audit Andreozzi et al. 2020 published subjects.csv lag variable.

Read-only, stdlib only; requires an independently obtained CC BY 4.0 CSV.
Usage: python a_andreozzi_2020_lag_column_audit_20261030.py subjects.csv
No participant-level output or re-publication.
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

def audit(path):
    with Path(path).open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required = {"subject_unq", "period", "opp_cond_class_wide_o",
                    "opp_cond_class_wide_o_lag1", "opp_cond_type",
                    "opp_cond_type_lag1"}
        if not required.issubset(reader.fieldnames):
            raise ValueError("missing required columns")
        groups = defaultdict(list)
        total = 0
        for row in reader:
            groups[row["subject_unq"]].append(row)
            total += 1
    current_equal = previous_equal = mismatch = control_mismatch = 0
    first_nonmissing = 0
    comparisons = 0
    for subject, group in groups.items():
        group.sort(key=lambda x: int(x["period"]))
        periods = [int(r["period"]) for r in group]
        if periods != list(range(1, 11)):
            raise ValueError("unexpected period sequence")
        if group[0]["opp_cond_class_wide_o_lag1"] not in ("NA", ""):
            first_nonmissing += 1
        for prior, current in zip(group, group[1:]):
            comparisons += 1
            lag = current["opp_cond_class_wide_o_lag1"]
            if lag == current["opp_cond_class_wide_o"]:
                current_equal += 1
            if lag == prior["opp_cond_class_wide_o"]:
                previous_equal += 1
            else:
                mismatch += 1
            if current["opp_cond_type_lag1"] != prior["opp_cond_type"]:
                control_mismatch += 1
    result = {
        "rows": total, "subjects": len(groups), "lag_comparisons": comparisons,
        "lag_equal_current": current_equal,
        "lag_equal_true_previous": previous_equal,
        "lag_mismatch_true_previous": mismatch,
        "period1_nonmissing": first_nonmissing,
        "control_opp_cond_type_lag1_mismatch": control_mismatch,
        "scope": "SOURCE_PREPROCESSING_AUDIT_NO_PREDICTION"}
    if (total, len(groups), comparisons, current_equal, previous_equal, mismatch,
        first_nonmissing, control_mismatch) != (1340, 134, 1206, 1206, 393, 813, 0, 0):
        raise ValueError("published source counts changed: " + json.dumps(result))
    return result

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: audit.py path/to/subjects.csv")
    print(json.dumps(audit(sys.argv[1]), sort_keys=True))
