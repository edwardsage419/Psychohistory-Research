"""R156 exact initial capital flow and curvature audit."""
from fractions import Fraction as Q
from collections import defaultdict
import json
A=(Q(1),Q(1,2))
K=(1,4,9)
S=(Q(1,10),Q(1,5),Q(2,5),Q(3,5))
D=(Q(0),Q(1,10),Q(1,5),Q(2,5))
def fmt(x):
    return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'
def run():
    rows=[]; one=defaultdict(list); two=defaultdict(list)
    for ai,alpha in enumerate(A):
        for ki,k in enumerate(K):
            sqrt=Q((1,2,3)[ki]); power=Q(k) if alpha==1 else sqrt
            for si,s in enumerate(S):
                for di,delta in enumerate(D):
                    v=s*power-delta*k
                    g=s*(Q(1) if alpha==1 else Q(1,2)/sqrt)-delta
                    a=g*v
                    key=f'a{ai}_k{ki}_s{si}_d{di}'
                    one[(ai,ki,v)].append(key)
                    two[(ai,ki,v,a)].append(key)
                    if alpha==Q(1,2) and v:
                        rec_s=2*sqrt*(v/k-a/v)
                        rec_delta=rec_s/sqrt-v/k
                        assert (rec_s,rec_delta)==(s,delta)
                    rows.append({'id':key,'alpha':fmt(alpha),'k0':k,'s':fmt(s),'delta':fmt(delta),'v':fmt(v),'a':fmt(a),'stationary':v==0})
    assert len(rows)==96
    by_alpha={}
    for ai in range(2):
        sub=[r for r in rows if r['alpha']==fmt(A[ai])]
        classes1=[v for k,v in one.items() if k[0]==ai]
        classes2=[v for k,v in two.items() if k[0]==ai]
        by_alpha[fmt(A[ai])]={'worlds':len(sub),'stationary_worlds':sum(r['stationary'] for r in sub),'one_jet_classes':len(classes1),'two_jet_classes':len(classes2),'two_jet_ambiguous_worlds':sum(len(v) for v in classes2 if len(v)>1),'two_jet_collision_sizes':sorted([len(v) for v in classes2 if len(v)>1]),'nonstationary_worlds':sum(not r['stationary'] for r in sub)}
    assert all(r['v']=='0' and r['a']=='0' for r in rows if r['stationary'])
    return {'research_id':'R156','evidence':'E1_SYNTHETIC_ONLY','source_blob':'96ecbc18053cd2f3fcea59a68a753975a471ef66','worlds':len(rows),'by_alpha':by_alpha,'rows':rows}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
