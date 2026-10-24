#!/usr/bin/env python3
"""R136 post-failure corrective audit, independently reconstructing Markov rows.

Python standard library only. Does not import R136 tree or Gauss-Jordan solvers.
A separate, precommitted corrective protocol governs this computation.
"""
import argparse
import csv
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

EXPECTED_SHA256 = 'c1e5c7680314e8734d6388662aef322b1e03befd7111dd5e5596b2c9c40ee856'
STATES = ('CC', 'CD', 'DC', 'DD')
PERMS = tuple((perm, (-1 if sum(perm[i] > perm[j] for i in range(4) for j in range(i+1,4)) % 2 else 1))
              for perm in itertools.permutations(range(4)))


def determinant(matrix):
    return sum((sign * matrix[0][p[0]] * matrix[1][p[1]] *
                matrix[2][p[2]] * matrix[3][p[3]] for p, sign in PERMS), F(0))


def stationary_cramer(P):
    A = [[P[j][i] - (i == j) for j in range(4)] for i in range(3)]
    A.append([F(1)] * 4)
    rhs = (F(0), F(0), F(0), F(1))
    denom = determinant(A)
    if denom == 0:
        return None
    result = []
    for k in range(4):
        M = [[rhs[i] if j == k else A[i][j] for j in range(4)] for i in range(4)]
        result.append(determinant(M) / denom)
    assert sum(result) == 1
    assert all(sum(result[i] * P[i][j] for i in range(4)) == result[j] for j in range(4))
    return tuple(result)


def build_matrix(p, q, swap):
    y = (q[0], q[2], q[1], q[3]) if swap else q
    rows = []
    for a, b in zip(p, y):
        rows.append((a*b, a*(1-b), (1-a)*b, (1-a)*(1-b)))
    return tuple(rows)


def extortion_p(chi, phi):
    return (1-2*phi*(chi-1), 1-phi*(4*chi+1), phi*(chi+4), F(0))


def payoff(v):
    return (sum(v[i]*F((3,0,5,1)[i]) for i in range(4)),
            sum(v[i]*F((3,5,0,1)[i]) for i in range(4)))


def audit(path):
    raw = Path(path).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256, 'CSV SHA256 mismatch'
    rows = list(csv.DictReader(raw.decode('utf-8').splitlines()))
    assert len(rows) == 1215, 'CSV row count mismatch'
    assert tuple(rows[0]) == ('class','chi','phi','q1','q2','q3','q4','tau_sum',
                             'v_CC','v_CD','v_DC','v_DD','pay_X','pay_Y','identity_residual')
    counts = Counter()
    seen = set()
    q_grid = set(itertools.product((F(1,4),F(1,2),F(3,4)),repeat=4))
    allowed_chis = (2,3,5,7)
    allowed_phis = (F(1,100),F(1,50),F(1,25),F(1,20),F(1,10))
    valid_ext = {(chi,phi) for chi in allowed_chis for phi in allowed_phis
                 if all(0 <= a <= 1 for a in extortion_p(chi,phi))}
    assert len(valid_ext) == 14
    for row in rows:
        q = tuple(F(row['q'+str(i)]) for i in range(1,5))
        assert q in q_grid
        cls = row['class']
        if cls == 'extortion':
            chi,phi = int(row['chi']),F(row['phi'])
            assert (chi,phi) in valid_ext
            p = extortion_p(chi,phi)
            key = (cls,chi,phi,q)
        elif cls == 'equalizer':
            assert row['chi'] == row['phi'] == ''
            p = (F(9,10),F(3,4),F(1,8),F(1,20))
            key = (cls,q)
        else:
            raise AssertionError('Unknown class: '+cls)
        assert key not in seen, 'Duplicate input grid row'
        seen.add(key)
        P = build_matrix(p,q,True)
        correct_y = (q[0],q[2],q[1],q[3])
        for i in range(4):
            assert sum(P[i]) == 1
            assert P[i][0]+P[i][1] == p[i], 'X marginal incorrect'
            assert P[i][0]+P[i][2] == correct_y[i], 'Y marginal incorrect'
            counts['correct_marginal_checks'] += 1
        v = stationary_cramer(P)
        assert v is not None
        assert tuple(F(row['v_'+s]) for s in STATES) == v
        x,y = payoff(v)
        assert (F(row['pay_X']),F(row['pay_Y'])) == (x,y)
        if cls == 'extortion':
            assert x-1-chi*(y-1) == F(row['identity_residual']) == 0
        else:
            assert y == F(5,3)
            assert F(row['identity_residual']) == 0
        counts['cramer_replayed_rows'] += 1
        counts[cls] += 1
        if q[1] != q[2]:
            wrong = build_matrix(p,q,False)
            failed_states = sum(wrong[i][0]+wrong[i][2] != correct_y[i] for i in range(4))
            assert failed_states == 2
            counts['negative_control_detected_rows'] += 1
            counts['negative_control_failed_state_marginals'] += failed_states
        else:
            counts['negative_control_unidentifiable_rows'] += 1
    assert counts['extortion'] == 1134 and counts['equalizer'] == 81
    assert counts['correct_marginal_checks'] == 4860
    assert counts['negative_control_detected_rows'] == 810
    assert counts['negative_control_failed_state_marginals'] == 1620
    assert counts['negative_control_unidentifiable_rows'] == 405
    assert len(seen) == len(valid_ext)*len(q_grid)+len(q_grid)
    witness_p = extortion_p(3,F(1,20))
    witness_q = (F(1,4),F(1,2),F(3,4),F(1,4))
    correct_pay = payoff(stationary_cramer(build_matrix(witness_p,witness_q,True)))
    wrong_pay = payoff(stationary_cramer(build_matrix(witness_p,witness_q,False)))
    assert correct_pay == (F(721,328),F(459,328))
    assert wrong_pay == (F(3413,1448),F(2103,1448))
    assert correct_pay != wrong_pay
    assert all(x-1-3*(y-1) == 0 for x,y in (correct_pay,wrong_pay))
    return {'status':'PASS_CORRECTIVE_CONTROL_ONLY', 'historical_frozen_control':'FAILED_NONDISCRIMINATING_UNCHANGED',
            'method':'independent_four_by_four_cramer_determinant_and_direct_y_marginal',
            'input_sha256':EXPECTED_SHA256, 'input_bytes':len(raw), 'input_rows':len(rows),
            'counts':dict(sorted(counts.items())),
            'witness_correct_payoffs':[str(z) for z in correct_pay],
            'witness_wrong_payoffs':[str(z) for z in wrong_pay],
            'evidence':'E1_INTERNAL_ONLY', 'E2':0, 'E3':0, 'external_replication':0,
            'new_ci':'NOT_RUN'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('csv_path')
    parser.add_argument('--receipt',help='Write JSON receipt to this path')
    args=parser.parse_args()
    result=audit(args.csv_path)
    s=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.receipt:
        Path(args.receipt).write_text(s,encoding='utf-8')
    print(s)


if __name__=='__main__':
    main()
