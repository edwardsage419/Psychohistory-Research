"""R149-A third method: exact stationary distribution and first boundary hit.
Reconstructs the frozen finite mechanism without importing original R149 code.
"""
from fractions import Fraction as F
import json

S=range(5)
Z=F(0)
O=F(1)

def transition(fixed=False):
    rows=[]
    for s in S:
        p=F(1,2) if fixed else F(s+1,6)
        row=[Z for _ in S]
        row[min(4,s+1)] += p*p
        row[max(0,s-1)] += (1-p)*(1-p)
        row[s] += 2*p*(1-p)
        assert sum(row)==1
        rows.append(row)
    return rows

def stationary(P):
    weights=[O]
    for s in range(4):
        weights.append(weights[-1]*P[s][s+1]/P[s+1][s])
    pi=[w/sum(weights) for w in weights]
    assert sum(pi)==1
    assert all(sum(pi[i]*P[i][j] for i in S)==pi[j] for j in S)
    return pi

def forward(P,horizons=(1,2,4,8,16,32)):
    a=[Z,Z,O,Z,Z]
    out={}
    for t in range(1,max(horizons)+1):
        a=[sum(a[i]*P[i][j] for i in S) for j in S]
        assert sum(a)==1
        if t in horizons:
            out[str(t)]={"distribution":[str(x) for x in a],
                         "endpoint":str(a[0]+a[4]),
                         "mean":str(sum(i*a[i] for i in S))}
    return out

def first_hit(P):
    # E_i[T]=1+sum_{j in {1,2,3}}P_ij E_j[T], E_0=E_4=0.
    a=[[F(int(i==j))-P[i][j] for j in (1,2,3)]+[O]
       for i in (1,2,3)]
    for k in range(3):
        assert a[k][k]
        factor=a[k][k]
        a[k]=[v/factor for v in a[k]]
        for i in range(3):
            if i!=k:
                factor=a[i][k]
                a[i]=[a[i][j]-factor*a[k][j] for j in range(4)]
    return [a[i][-1] for i in range(3)]

P=transition()
Q=transition(True)
pi=stationary(P)
pi_fixed=stationary(Q)
assert pi==[F(72,155),F(9,310),F(2,155),F(9,310),F(72,155)]
assert pi_fixed==[F(1,5)]*5
assert sum(i*pi[i] for i in S)==2
h=forward(P)
assert F(h['8']['endpoint'])==F(16624456774,19591041024)
assert all(x['mean']=='2' for x in h.values())
hit=first_hit(P)
assert hit==[F(11,4),F(19,4),F(11,4)]
assert P[0][1]==F(1,36) and P[4][3]==F(1,36)
assert F(1,6)*F(5,6)!=P[0][1]
assert pi[0]+pi[4]==F(144,155)
assert pi_fixed[0]+pi_fixed[4]==F(2,5)
print(json.dumps({"model":"R149-A","evidence":"E1_synthetic", "method":"exact detailed balance, 5-state forward, 3-state first-step elimination", "stationary_feedback":[str(x) for x in pi], "stationary_fixed_action":[str(x) for x in pi_fixed], "stationary_endpoint_feedback":"144/155","stationary_endpoint_fixed_action":"2/5","first_hit_interior":[str(x) for x in hit],"forward":h,"negative_controls_passed":2,"E2":0,"E3":0},indent=2))
