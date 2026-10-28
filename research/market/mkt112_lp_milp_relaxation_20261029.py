#!/usr/bin/env python3
"""MKT112: local, synthetic SciPy LP/MILP feasibility and slack audit.
Requires existing SciPy and NumPy. No API, network, or user data.
"""
import json
import numpy as np
from scipy.optimize import linprog, milp, Bounds, LinearConstraint

checks = 0

def check(test, message):
    global checks
    checks += 1
    if not test:
        raise AssertionError(message)

# Case 1: a continuous feasible point that is forbidden by integrality.
lp = linprog([0.0], bounds=[(0.5, 0.5)], method='highs')
integer = milp(c=[0.0], integrality=[1], bounds=Bounds([0.5], [0.5]))
check(lp.status == 0, 'LP should be feasible')
check(abs(lp.x[0] - 0.5) < 1e-9, 'LP point')
check(integer.status == 2, 'MILP should be proven infeasible')

# Case 2: incompatible bounds x>=7 and x<=5.
conflict = linprog([0.0], A_ub=[[-1.0], [1.0]], b_ub=[-7.0, 5.0], bounds=[(0, 10)], method='highs')
check(conflict.status == 2, 'LP infeasible')

# Relax both constraints using nonnegative slacks a and b.
# x + a >= 7, x - b <= 5; objective a+b.
A = [[-1.0, -1.0, 0.0], [1.0, 0.0, -1.0]]
b = [-7.0, 5.0]
slack = linprog([0.0, 1.0, 1.0], A_ub=A, b_ub=b,
                bounds=[(0, 10), (0, None), (0, None)], method='highs')
check(slack.status == 0, 'slack LP feasible')
check(abs(slack.fun - 2.0) < 1e-9, 'minimum L1 slack 2')
for x, a, c in [(5, 2, 0), (6, 1, 1), (7, 0, 2)]:
    check(x + a >= 7 and x - c <= 5, 'slack feasibility')
    check(a + c == 2, 'equal optimum')

# Weight choices select different compromises; weights are not universal utilities.
prefer_upper = linprog([0.0, 1.0, 3.0], A_ub=A, b_ub=b,
                       bounds=[(0, 10), (0, None), (0, None)], method='highs')
prefer_lower = linprog([0.0, 3.0, 1.0], A_ub=A, b_ub=b,
                       bounds=[(0, 10), (0, None), (0, None)], method='highs')
check(prefer_upper.status == 0 and prefer_lower.status == 0, 'weighted solvers')
check(abs(prefer_upper.x[0] - 5) < 1e-9, 'higher penalty upper violation chooses x=5')
check(abs(prefer_lower.x[0] - 7) < 1e-9, 'higher penalty lower violation chooses x=7')

# Enumerate minimal unsatisfiable subsets of original A: x>=7, B: x<=5, C: x<=9, D: x>=0.
constraints = [lambda x: x >= 7, lambda x: x <= 5,
               lambda x: x <= 9, lambda x: x >= 0]
unsat = []
for mask in range(16):
    feasible = any(all(fn(x) for i, fn in enumerate(constraints) if mask & (1 << i))
                   for x in range(11))
    if not feasible:
        unsat.append(mask)
    check(feasible == (not (mask & 3 == 3)), f'conflict mask {mask}')
check(unsat == [3, 7, 11, 15], 'all unsat masks')
minimal = [m for m in unsat if not any(n != m and n & m == n for n in unsat)]
check(minimal == [3], 'minimal conflict AB')

print(json.dumps({
    'status':'PASS', 'checks':checks, 'failures':0,
    'scipy_version':__import__('scipy').__version__,
    'integrality_case':{'LP_status':int(lp.status),'LP_x':float(lp.x[0]),'MILP_status':int(integer.status)},
    'conflict_case':{'LP_status':int(conflict.status),'L1_slack':float(slack.fun),
                     'optimal_slack_examples':[[5,2,0],[6,1,1],[7,0,2]],
                     'weighted_x':[float(prefer_upper.x[0]),float(prefer_lower.x[0])],
                     'minimal_unsat_masks':minimal}
},ensure_ascii=False))
