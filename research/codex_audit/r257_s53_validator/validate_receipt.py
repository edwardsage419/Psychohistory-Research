#!/usr/bin/env python3
"""Nonblind R257 S53 mathematical receipt gate; no scientific acceptance upgrade.

Checks sufficient exact KKT certificates for strictly convex quadratic objectives.
No archived R/B optimizer is imported. This does not authenticate input provenance.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import re
import sys

PARAMS = {
    'INTERIOR_OFF_GRID': ('1', '3/5', '1/5'),
    'BINDING_SUM_BOTH': ('1', '3/4', '3/4'),
    'LOWER_X_ACTIVE': ('1', '-1/2', '1/2'),
    'LOWER_Y_ACTIVE': ('1', '1/2', '-1/2'),
    'VERTEX_ORIGIN': ('1', '-1/2', '-1/2'),
    'VERTEX_RIGHT': ('1', '2', '1/4'),
    'VERTEX_UPPER': ('1', '1/4', '2'),
    'CAPACITY_TWO_SLACK': ('2', '3/4', '3/4'),
}
DELTAS = {F(-1, 4), F(-1, 16), F(0), F(1, 16), F(1, 4)}
STEPS = {F(1, 4), F(1, 16)}
CONTROL = 'KKT_stationary_0_vs_feasible_-1/4'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def keys(obj, expected, context):
    require(type(obj) is dict, context + ': object required')
    require(set(obj) == set(expected.split()), context + ': field set mismatch')


def rational(value):
    require(type(value) is str and re.fullmatch(r'-?[0-9]+(?:/[1-9][0-9]*)?', value) is not None,
            'exact integer/fraction string required')
    return F(value)


def unique(rows, field, expected, numeric=False):
    require(type(rows) is list and len(rows) == len(expected), field + ': coverage count')
    found = {}
    for row in rows:
        require(type(row) is dict and field in row, field + ': missing identity')
        identity = rational(row[field]) if numeric else row[field]
        require(type(identity) is str if not numeric else isinstance(identity, F),
                field + ': invalid identity type')
        require(identity in expected and identity not in found, field + ': duplicate/unknown identity')
        found[identity] = row
    require(set(found) == set(expected), field + ': coverage mismatch')
    return found


def certificate(row, a, b):
    """Return value and capacity multiplier after exact primal/dual checks."""
    C = rational(row['capacity'])
    require(type(row['point']) is list and len(row['point']) == 2, 'point: two coordinates required')
    x, y = map(rational, row['point'])
    v = rational(row['minimum'])
    require(C > 0 and x >= 0 and y >= 0 and x+y <= C, 'primal feasibility')
    require(v == (x-a)**2 + (y-b)**2, 'objective mismatch')
    # L=f+lambda*(x+y-C)-mu_x*x-mu_y*y. At C>0 a binding
    # capacity has a positive coordinate, fixing lambda by complementarity.
    lam = F(0) if x+y < C else 2*(a-x) if x > 0 else 2*(b-y)
    mux, muy = 2*(x-a)+lam, 2*(y-b)+lam
    require(lam >= 0 and mux >= 0 and muy >= 0, 'dual feasibility')
    require(mux*x == 0 and muy*y == 0 and lam*(x+y-C) == 0, 'KKT complementarity')
    return v, lam


def validate(data):
    keys(data, 'research_id evidence capacity_evaluations one_sided_secants baseline_lambdas assertions_passed nonconvex_negative_control worlds new_human_E2 new_history_E3', 'receipt')
    require(data['research_id'] == 'R257_S53' and data['evidence'] == 'E1', 'research/evidence identity')
    for name, expected in {'capacity_evaluations': 40, 'one_sided_secants': 32,
                           'baseline_lambdas': 8, 'assertions_passed': 127,
                           'new_human_E2': 0, 'new_history_E3': 0}.items():
        require(type(data[name]) is int and data[name] == expected, name + ': identity/count mismatch')
    require(data['nonconvex_negative_control'] == CONTROL, 'nonconvex control label')
    worlds = unique(data['worlds'], 'world', PARAMS)
    for name, w in worlds.items():
        keys(w, 'world baseline_capacity baseline_minimum baseline_lambda local_derivative perturbations secants', name)
        C0, a, b = map(F, PARAMS[name])
        require(rational(w['baseline_capacity']) == C0, name + ': baseline capacity')
        rows = unique(w['perturbations'], 'delta', DELTAS, numeric=True)
        values = {}
        lambdas = {}
        for delta, row in rows.items():
            keys(row, 'delta capacity minimum point', name + ': perturbation')
            require(rational(row['capacity']) == C0+delta, name + ': delta/capacity identity')
            values[delta], lambdas[delta] = certificate(row, a, b)
        v0, lam = values[F(0)], lambdas[F(0)]
        require(rational(w['baseline_minimum']) == v0, name + ': baseline value')
        require(rational(w['baseline_lambda']) == lam, name + ': multiplier mismatch')
        require(rational(w['local_derivative']) == -lam, name + ': derivative mismatch')
        for delta, v in values.items():
            require(v >= v0-lam*delta, name + ': supporting bound')
        for h, sec in unique(w['secants'], 'step', STEPS, numeric=True).items():
            keys(sec, 'step left_secant right_secant', name + ': secant')
            left, right = rational(sec['left_secant']), rational(sec['right_secant'])
            require(left == (v0-values[-h])/h and right == (values[h]-v0)/h, name + ': secant mismatch')
            require(left <= -lam <= right <= 0, name + ': convex slope bounds')
    return {'status': 'COMPLETE', 'scope': 'NONBLIND_E1_MATHEMATICAL_RECEIPT_CHECK',
            'capacity_certificates': 40, 'secants_checked': 32, 'baseline_multipliers_checked': 8,
            'blinded_prescore_order': 'FAIL', 'full_scientific_acceptance': 'PARTIAL',
            'source_authentication': 'NOT_RUN', 'external_team_replications': 0,
            'new_human_E2': 0, 'new_history_E3': 0}


def no_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, 'duplicate JSON key: ' + key)
        obj[key] = value
    return obj


def main():
    try:
        require(len(sys.argv) == 2, 'usage: validate_receipt.py RECEIPT.json')
        data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'), object_pairs_hook=no_duplicate_keys)
        result = validate(data)
    except (ValueError, OSError) as exc:
        print(json.dumps({'status': 'BLOCKED', 'reason': str(exc)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
