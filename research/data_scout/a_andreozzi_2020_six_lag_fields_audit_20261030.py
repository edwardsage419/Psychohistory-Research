#!/usr/bin/env python3
"""Read-only Andreozzi 2020 six-lag-column audit of the public subjects.csv.

Usage: python a_andreozzi_2020_six_lag_fields_audit_20261030.py path/to/subjects.csv
Requires original public file bytes; no download, no private data, no dependencies.
This archive program is provided for replay. The automation's direct remote
source audit used the GitHub connector and a separate JavaScript CSV parser.
"""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

EXPECTED_BLOB = 'bd4c1550002621bee7dfb50e0d15d317764d1ea9'
PAIRS = (
    ('opp_action', 'opp_action_lag1'),
    ('opp_cond_type', 'opp_cond_type_lag1'),
    ('opp_cond_class_wide', 'opp_cond_class_wide_lag1'),
    ('opp_cond_class_wide_o', 'opp_cond_class_wide_o_lag1'),
    ('opp_cond_class_narrow', 'opp_cond_class_narrow_lag1'),
    ('first_player', 'first_player_lag1'),
)


def audit(raw):
    sha = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if sha != EXPECTED_BLOB:
        raise ValueError('source blob mismatch: ' + sha)
    import io
    rows = list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
    if len(rows) != 1340 or len(rows[0]) != 67:
        raise ValueError('source dimensions mismatch')
    groups = defaultdict(list)
    for row in rows:
        groups[row['subject_unq']].append(row)
    if len(groups) != 134:
        raise ValueError('subject count mismatch')
    counts = {target: {'match': 0, 'mismatch': 0, 'first_na': 0, 'current_equal': 0}
              for _, target in PAIRS}
    overlap = both = 0
    treatments = defaultdict(lambda: {'comparisons': 0, 'wide_mismatch': 0, 'narrow_mismatch': 0})
    for subject, ordered in groups.items():
        if len(ordered) != 10 or [int(r['period']) for r in ordered] != list(range(1, 11)):
            raise ValueError('row order or period sequence differs: ' + subject)
        for i, row in enumerate(ordered):
            mismatched = set()
            for source, target in PAIRS:
                observed = row[target]
                expected = 'NA' if i == 0 else ordered[i - 1][source]
                if i == 0:
                    if observed != 'NA':
                        raise ValueError('period one lag not missing')
                    counts[target]['first_na'] += 1
                elif observed == expected:
                    counts[target]['match'] += 1
                else:
                    counts[target]['mismatch'] += 1
                    mismatched.add(target)
                if i > 0 and observed == row[source]:
                    counts[target]['current_equal'] += 1
            if i > 0:
                t = treatments[row['treatment']]
                t['comparisons'] += 1
                w = 'opp_cond_class_wide_o_lag1' in mismatched
                n = 'opp_cond_class_narrow_lag1' in mismatched
                t['wide_mismatch'] += int(w)
                t['narrow_mismatch'] += int(n)
                overlap += int(w or n)
                both += int(w and n)
    return {'source_git_blob': sha, 'rows': len(rows), 'subjects': len(groups),
            'comparisons': 1206, 'lag_fields': counts, 'union_mismatches': overlap,
            'both_mismatches': both, 'by_treatment': dict(treatments)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('public_subjects_csv')
    args = parser.parse_args()
    print(json.dumps(audit(Path(args.public_subjects_csv).read_bytes()), indent=2))
