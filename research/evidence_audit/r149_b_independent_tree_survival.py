"""Independent R149-A birth-death spanning-tree and survival audit.
Only Python standard library; original R149 code is not imported.
"""
from fractions import Fraction as F
from functools import reduce
from operator import mul
import json

S = range(5)
p = [F(i+1,6) for i in S]
u = [x*x for x in p]
d = [(1-x)**2 for x in p]
# Directed tree weight rooted at i: lower edges point up, higher edges down.
w = [reduce(mul, u[:i], F(1)) * reduce(mul, d[i+1:], F(1)) for i in S]
pi = [x/sum(w) for x in w]
assert pi == [F(72,155),F(9,310),F(2,155),F(9,310),F(72,155)]
assert sum(i*pi[i] for i in S) == 2
assert pi[0]+pi[4] == F(144,155)
# Independent first-hit audit via absorption-survival tail, no matrix inverse.
state = [F(0),F(0),F(1),F(0),F(0)]
partial = F(0)
traces={}
for t in range(256):
    partial += sum(state)
    nxt = [F(0) for _ in S]
    for i in (1,2,3):
        nxt[i] += state[i] * (1-u[i]-d[i])
        if i>1: nxt[i-1] += state[i]*d[i]
        if i<3: nxt[i+1] += state[i]*u[i]
    state = nxt
    if t+1 in (8,16,32,64,128,256):
        traces[str(t+1)] = {"partial":str(partial),"survival":str(sum(state))}
# Every interior state absorbs within two steps with probability >=2/9.
# Hence remaining expected time after 256 steps <=9*(7/9)^128.
error_bound = 9*F(7,9)**128
assert partial < F(19,4) < partial + error_bound
assert error_bound < F(1,10**12)
assert u[0] == F(1,36) and d[4] == F(1,36)
assert p[0]*(1-p[0]) != u[0]
out = {"model":"R149-A","method":"independent directed spanning tree and 256-step survival series", "stationary":[str(x) for x in pi],"first_hit_expected_exact_comparator":"19/4","survival_partial_256":str(partial),"survival_error_bound":str(error_bound),"error_less_than_1e_minus_12":True,"traces":traces,"negative_controls_passed":2,"new_E2":0,"new_E3":0}
print(json.dumps(out,ensure_ascii=False,indent=2))
