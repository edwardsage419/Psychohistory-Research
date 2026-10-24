"""Independent R134 matrix Fraction recomputation; synthetic E1 only."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json

S = ((0, 1), (1, 0))
T = ((2, 0), (0, 2))
GRID = (-1, 0, 1)
RESIDENT = (F(1, 4), F(1, 2), F(3, 4))
MUTANT = (F(0), F(1, 4), F(3, 4), F(1))
EPS = (F(0), F(1, 2), F(1))

def scale(M, z):
    return tuple(tuple(z * v for v in row) for row in M)

def mv(M, v):
    return tuple(sum(F(z) * w for z, w in zip(row, v)) for row in M)

def add(u, v):
    return tuple(x + y for x, y in zip(u, v))

def sub(u, v):
    return tuple(x - y for x, y in zip(u, v))

def dot(u, v):
    return sum(x * y for x, y in zip(u, v))

def mix(p, r, e):
    return add(tuple((1 - e) * z for z in p), tuple(e * z for z in r))

def payoff(a, b, c, d, p, q, r, s, e):
    pe, qe = mix(p, r, e), mix(q, s, e)
    f = add(mv(scale(S, a), pe), mv(scale(T, b), qe))
    g = add(mv(scale(T, c), pe), mv(scale(S, d), qe))
    return dot(sub(p, r), f) + dot(sub(q, s), g)

def field(a, b, c, d, x, y):
    p, q = (x, 1-x), (y, 1-y)
    f = add(mv(scale(S, a), p), mv(scale(T, b), q))
    g = add(mv(scale(T, c), p), mv(scale(S, d), q))
    return (x * (1-x) * (f[0]-f[1]), y * (1-y) * (g[0]-g[1]))

def four_point(a, b, c, d, component, axis):
    h = F(1, 8)
    def val(t):
        x, y = (t, F(1, 2)) if axis == 0 else (F(1, 2), t)
        return field(a, b, c, d, x, y)[component]
    mid = F(1, 2)
    return (-val(mid+2*h)+8*val(mid+h)-8*val(mid-h)+val(mid-2*h))/(12*h)

counts = Counter()
worlds = 0
triples = 0
joint_saddle = []
for a,b,c,d in product(GRID, repeat=4):
    j = ((four_point(a,b,c,d,0,0),four_point(a,b,c,d,0,1)),
         (four_point(a,b,c,d,1,0),four_point(a,b,c,d,1,1)))
    assert j == ((-F(a,2),F(b)),(F(c),-F(d,2)))
    tr = j[0][0]+j[1][1]
    det = j[0][0]*j[1][1]-j[0][1]*j[1][0]
    if det < 0: kind='saddle'
    elif det == 0: kind='nonhyperbolic'
    elif tr < 0: kind='asymptotically_stable_linear'
    elif tr > 0: kind='unstable_linear'
    else: kind='linear_center_inconclusive'
    counts[kind] += 1
    worlds += 1
    if a>0 and d>0 and det<0: joint_saddle.append((a,b,c,d))
    for x,y,r,s in product(RESIDENT, RESIDENT, MUTANT, MUTANT):
        p,q,rr,ss=(x,1-x),(y,1-y),(r,1-r),(s,1-s)
        f0,fh,f1 = (payoff(a,b,c,d,p,q,rr,ss,e) for e in EPS)
        assert fh*2 == f0+f1
        dp,dq = sub(rr,p),sub(ss,q)
        Q = dot(dp,add(mv(scale(S,a),dp),mv(scale(T,b),dq))) + dot(dq,add(mv(scale(T,c),dp),mv(scale(S,d),dq)))
        assert f1-f0 == -Q
        triples += 1
assert worlds == 81 and triples == 11664
assert len(joint_saddle) == 2
result={'method':'separate Python Fraction full matrix products and four-point finite difference',
        'worlds':worlds,'triples':triples,'payoff_evaluations':triples*3,
        'counts':dict(sorted(counts.items())),
        'joint_saddle_parameters':[list(z) for z in joint_saddle],
        'E1_only':True,'E2':0,'E3':0}
print(json.dumps(result,indent=2))
