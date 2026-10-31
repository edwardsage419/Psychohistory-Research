#!/usr/bin/env python3
"""Illustrative two-period sequence-risk test; not ProjectionLab source code.
Uses fictional balances and exact fractions. No account or API access.
"""
from fractions import Fraction as F
from itertools import product
import json

START = F(100)
WITHDRAW = F(50)
RETURNS = (F(-1,5), F(1,5))

def path_balance(returns):
    balance = START
    history = []
    for r in returns:
        balance = balance * (1 + r) - WITHDRAW
        history.append(balance)
    return tuple(history)

def run():
    paths = {tuple(int(r*100) for r in p): path_balance(p) for p in product(RETURNS, repeat=2)}
    expected = {(-20,-20):(F(30),F(-26)),(-20,20):(F(30),F(-14)),
                (20,-20):(F(70),F(6)),(20,20):(F(70),F(34))}
    checks = 0
    for p,v in expected.items():
        checks += 1
        if paths[p] != v: raise AssertionError((p,paths[p],v))
    successes = sum(all(x>=0 for x in v) for v in paths.values())
    checks += 1
    if successes != 2: raise AssertionError('expected 2/4 synthetic successes')
    fixed = path_balance((F(0),F(0)))
    checks += 1
    if fixed != (F(50),F(0)): raise AssertionError('fixed path mismatch')
    checks += 1
    if paths[(20,-20)][1] - paths[(-20,20)][1] != F(20):
        raise AssertionError('sequence-order effect missing')
    print(json.dumps({'status':'PASS','checks':checks,'synthetic_paths':len(paths),
        'path_balances':{str(k):[str(z) for z in v] for k,v in paths.items()},
        'synthetic_success_count':successes,'synthetic_success_probability':'1/2',
        'fixed_zero_return_path':[str(x) for x in fixed],
        'scope':'fictional exact two-period model; no real forecast'},ensure_ascii=False))

if __name__ == '__main__': run()
