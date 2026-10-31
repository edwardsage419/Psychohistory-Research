#!/usr/bin/env python3
"""Independent exact Fraction oracle for R308 S104. No imports from R script."""
import csv
import json
import sys
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

PATTERNS = {
    'NONE': (0, 0, 0),
    'LOW_UNIFORM': (1, 1, 1),
    'HIGH_UNIFORM': (2, 2, 2),
    'ONE_STRONG_TWO_ZERO': (2, 0, 0),
    'ONE_WEAK_LINK': (2, 2, 0),
    'SAME_MEAN_NO_ZERO': (2, 1, 1),
    'HETEROGENEOUS': (2, 1, 0),
    'HALF_HALF_ZERO': (1, 1, 0),
}
COLS = ('pattern', 'aggregation', 'B_num6', 'c_half', 'w_half', 'r_half',
        'S0_A_num48', 'S1_Ac_num48', 'S1_Aw_num48', 'S1_Ar_num48',
        'S2_Acw_num48', 'S2_Acr_num48', 'S2_Awr_num48')
LEVELS = (Q(0), Q(1, 2), Q(1))


def oracle():
    rows = []
    groups = []
    for name, halves in PATTERNS.items():
        beliefs = [Q(x, 2) for x in halves]
        for rule in ('MEAN', 'BOTTLENECK_MIN'):
            b = sum(beliefs) / 3 if rule == 'MEAN' else min(beliefs)
            partitions = [defaultdict(list) for _ in range(4)]
            for c, w, r in product(LEVELS, repeat=3):
                a = b*c*w*r
                ac, aw, ar = b*w*r, b*c*r, b*c*w
                acw, acr, awr = b*r, b*w, b*c
                signatures = ((a,), (a, ac, aw, ar), (a, acw, acr, awr),
                              (a, ac, aw, ar, acw, acr, awr))
                for i, sig in enumerate(signatures):
                    partitions[i][sig].append((c, w, r))
                scaled = [b*6, c*2, w*2, r*2, a*48, ac*48, aw*48, ar*48,
                          acw*48, acr*48, awr*48]
                if any(x.denominator != 1 for x in scaled):
                    raise ValueError('noninteger scaled field')
                rows.append(dict(zip(COLS, (name, rule, *map(int, scaled)))))
            groups.append({'pattern': name, 'aggregation': rule, 'B_num6': int(b*6),
                           'classes': [len(p) for p in partitions],
                           'singleton_worlds': [sum(len(v)==1 for v in p.values()) for p in partitions],
                           'largest_class': [max(map(len, p.values())) for p in partitions]})
    return rows, groups


def verify(rows, groups):
    expected_rows, expected_groups = oracle()
    if len(rows) != 432 or len(groups) != 16:
        raise ValueError('universe count mismatch')
    keys = [(r['pattern'], r['aggregation'], r['c_half'], r['w_half'], r['r_half']) for r in rows]
    if len(set(keys)) != 432:
        raise ValueError('duplicate/missing world identity')
    if rows != expected_rows:
        raise ValueError('source or derived field mismatch')
    if groups != expected_groups:
        raise ValueError('partition summary mismatch')
    if [sum(g['classes'][i] for g in groups) for i in range(4)] != [56, 186, 276, 276]:
        raise ValueError('total class mismatch')
    if [sum(g['singleton_worlds'][i] for g in groups) for i in range(4)] != [20, 140, 270, 270]:
        raise ValueError('singleton mismatch')
    return True


def mutation_tests():
    rows, groups = oracle()
    import copy
    cases = []
    def case(label, mutator):
        r, g = copy.deepcopy(rows), copy.deepcopy(groups)
        mutator(r, g)
        try:
            verify(r, g)
        except ValueError:
            cases.append((label, 'REJECT'))
            return
        raise RuntimeError('mutation accepted: ' + label)
    case('drop_world', lambda r,g: r.pop())
    case('duplicate_world', lambda r,g: r.__setitem__(1, dict(r[0])))
    case('alter_belief', lambda r,g: r[100].__setitem__('B_num6', 6))
    case('alter_action', lambda r,g: r[100].__setitem__('S0_A_num48', -1))
    case('alter_single_gate', lambda r,g: r[100].__setitem__('S1_Ac_num48', -1))
    case('alter_double_gate', lambda r,g: r[100].__setitem__('S2_Acw_num48', -1))
    case('alter_group_classes', lambda r,g: g[4]['classes'].__setitem__(1, 19))
    case('alter_singletons', lambda r,g: g[4]['singleton_worlds'].__setitem__(2, 26))
    return cases


def main(argv):
    rows, groups = oracle()
    verify(rows, groups)
    if len(argv) == 3:
        with Path(argv[1]).open(newline='', encoding='utf-8') as fh:
            parsed = list(csv.DictReader(fh))
        if list(parsed[0]) != list(COLS):
            raise ValueError('CSV schema mismatch')
        parsed = [{k: (v if k in ('pattern','aggregation') else int(v)) for k,v in row.items()} for row in parsed]
        data = json.loads(Path(argv[2]).read_text(encoding='utf-8'))
        verify(parsed, data['groups'])
        if data['rows'] != parsed:
            raise ValueError('JSON CSV disagreement')
    elif len(argv) != 1:
        raise SystemExit('usage: python b_r308_s104_fraction_audit.py [CSV JSON]')
    cases = mutation_tests()
    print(json.dumps({'worlds':len(rows), 'groups':len(groups),
                      'classes':[sum(g['classes'][i] for g in groups) for i in range(4)],
                      'singletons':[sum(g['singleton_worlds'][i] for g in groups) for i in range(4)],
                      'mutations':cases, 'mode':'independent_nonblind_E1_fraction'},ensure_ascii=False))

if __name__ == '__main__':
    main(sys.argv)
