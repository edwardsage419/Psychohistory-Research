#!/usr/bin/env python3
"""Independent exact 4-state Gauss-Jordan replay of R136 tree-method CSV.

Does not import the third-method tree algorithm.
"""
import argparse
import csv
import hashlib
from fractions import Fraction
from pathlib import Path

F = Fraction
EXPECTED_SHA256 = 'c1e5c7680314e8734d6388662aef322b1e03befd7111dd5e5596b2c9c40ee856'


def matrix(p, q, swap=True):
    ys = (q[0], q[2], q[1], q[3]) if swap else q
    return [[a*b, a*(1-b), (1-a)*b, (1-a)*(1-b)] for a,b in zip(p, ys)]


def solve(P):
    A = [[P[j][i] - (1 if i == j else 0) for j in range(4)] for i in range(3)]
    A += [[F(1)]*4]
    rhs = [F(0), F(0), F(0), F(1)]
    for col in range(4):
        pivot = next((r for r in range(col,4) if A[r][col]), None)
        if pivot is None:
            return None
        A[col], A[pivot] = A[pivot], A[col]
        rhs[col], rhs[pivot] = rhs[pivot], rhs[col]
        factor = A[col][col]
        A[col] = [v/factor for v in A[col]]
        rhs[col] /= factor
        for r in range(4):
            if r != col:
                factor = A[r][col]
                A[r] = [A[r][j]-factor*A[col][j] for j in range(4)]
                rhs[r] -= factor*rhs[col]
    assert all(sum(rhs[i]*P[i][j] for i in range(4)) == rhs[j] for j in range(4))
    return tuple(rhs)


def pay(v):
    return (sum(a*b for a,b in zip(v,(3,0,5,1))),
            sum(a*b for a,b in zip(v,(3,5,0,1))))


def p_ext(chi, phi):
    return (1-2*phi*(chi-1), 1-phi*(4*chi+1), phi*(chi+4), F(0))


def main(path):
    raw=Path(path).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==EXPECTED_SHA256
    rows=list(csv.DictReader(raw.decode('utf8').splitlines()))
    assert len(rows)==1215
    count={'extortion':0,'equalizer':0,'singular':0,'row_mismatch':0}
    for row in rows:
        q=tuple(F(row[f'q{i}']) for i in range(1,5))
        if row['class']=='extortion':
            chi=int(row['chi']);p=p_ext(chi,F(row['phi']))
        else:
            p=(F(9,10),F(3,4),F(1,8),F(1,20))
        v=solve(matrix(p,q))
        assert v is not None
        x,y=pay(v)
        assert tuple(F(row[k]) for k in ('v_CC','v_CD','v_DC','v_DD'))==v
        assert (F(row['pay_X']),F(row['pay_Y']))==(x,y)
        if row['class']=='extortion':
            assert x-1-chi*(y-1)==F(row['identity_residual'])==0
        else:
            assert y==F(5,3)
        count[row['class']]+=1
    assert count['extortion']==1134 and count['equalizer']==81
    p=p_ext(3,F(1,20))
    for q in ((F(1),F(1),F(0),F(0)),(F(1),F(1),F(1),F(0))):
        assert solve(matrix(p,q)) is None
        count['singular']+=1
    q=(F(1,4),F(1,2),F(3,4),F(1,4))
    x1,y1=pay(solve(matrix(p,q,True)))
    x2,y2=pay(solve(matrix(p,q,False)))
    assert (x1,y1)==(F(721,328),F(459,328))
    assert (x2,y2)==(F(3413,1448),F(2103,1448))
    assert (x1,y1)!=(x2,y2)
    assert x1-1-3*(y1-1)==x2-1-3*(y2-1)==0
    print('GAUSS_JORDAN_PASS',count,'q_order_negative_control=INVALID_BY_INVARIANCE',
          'witness_correct=',(str(x1),str(y1)),'witness_wrong=',(str(x2),str(y2)))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('csv_path')
    main(parser.parse_args().csv_path)
