"""R176 post-acceptance E1 observability audit. Python stdlib only.
Reproduces frozen four-agent transition rules without importing R176 source.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb
from collections import defaultdict, Counter
import json
from pathlib import Path

MUS=(Q(1,8),Q(1,4)); BETAS=(Q(0),Q(1,4)); GAMMAS=(Q(0),Q(1,2)); DS=(Q(0),Q(1,4)); KS=(1,2,3)
STATES=tuple(product(range(5),(0,1)))

def institution(rule,k,old):
    if rule=='threshold': return int(k>=3)
    return 1 if k>=3 else 0 if k<=1 else old

def row(k,j,mu,beta,gamma,d,rule):
    adopt=1-(1-mu)*(1-beta)**k*(1-gamma)**j
    stay=1-d/Q(1+j)
    z=defaultdict(Q)
    for survive in range(k+1):
        a=comb(k,survive)*stay**survive*(1-stay)**(k-survive)
        for gain in range(5-k):
            b=comb(4-k,gain)*adopt**gain*(1-adopt)**(4-k-gain)
            kk=survive+gain
            z[(kk,institution(rule,kk,j))]+=a*b
    assert sum(z.values())==1
    return {key:v for key,v in z.items() if v}

def propagate(dist,table):
    out=defaultdict(Q)
    for s,p in dist.items():
        for target,q in table[s].items(): out[target]+=p*q
    assert sum(out.values())==1
    return {s:p for s,p in out.items() if p}

def marginal(dist):
    o=defaultdict(Q)
    for (k,j),p in dist.items():o[k]+=p
    return dict(o)

def tv(a,b):
    return sum((abs(a.get(x,Q(0))-b.get(x,Q(0))) for x in set(a)|set(b)),Q(0))/2

def trajectory(mu,beta,gamma,d,k0,rule):
    table={s:row(*s,mu,beta,gamma,d,rule) for s in STATES}
    cur={(k0,0):Q(1)}; out=[]
    for t in range(13):
        out.append(cur)
        if t<12:cur=propagate(cur,table)
    return out

def micro_row(mask,j,mu,beta,gamma,d,rule):
    k=mask.bit_count(); out=defaultdict(Q)
    for target in range(16):
        p=Q(1)
        for i in range(4):
            before=(mask>>i)&1; after=(target>>i)&1
            p1=(1-d/Q(1+j)) if before else 1-(1-mu)*(1-beta)**k*(1-gamma)**j
            p*=p1 if after else 1-p1
        out[(target,institution(rule,target.bit_count(),j))]+=p
    assert sum(out.values())==1
    return {s:p for s,p in out.items() if p}

def micro_path(mu,beta,gamma,d,k0,rule):
    table={(mask,j):micro_row(mask,j,mu,beta,gamma,d,rule) for mask in range(16) for j in (0,1)}
    cur={((1<<k0)-1,0):Q(1)}; out=[]
    for t in range(4):
        agg=defaultdict(Q)
        for (mask,j),p in cur.items():agg[(mask.bit_count(),j)]+=p
        out.append(dict(agg))
        if t<3:cur=propagate(cur,table)
    return out

def run():
    rec=[]; cross=0; cross_cells=0; neg=0
    for mu,beta,gamma,d,k0 in product(MUS,BETAS,GAMMAS,DS,KS):
        a=trajectory(mu,beta,gamma,d,k0,'threshold')
        b=trajectory(mu,beta,gamma,d,k0,'hysteresis')
        jtv=[tv(x,y) for x,y in zip(a,b)]
        ktv=[tv(marginal(x),marginal(y)) for x,y in zip(a,b)]
        assert all(x<=y for x,y in zip(ktv,jtv))
        assert jtv[0]==jtv[1]==ktv[0]==ktv[1]==ktv[2]==0
        if d==0:
            assert all(x==0 for x in jtv+ktv); neg+=1
        else:
            assert jtv[2]>0 and ktv[3]>0
        am=micro_path(mu,beta,gamma,d,k0,'threshold')
        bm=micro_path(mu,beta,gamma,d,k0,'hysteresis')
        for t in range(4):
            for x,y in ((a[t],am[t]),(b[t],bm[t])):
                assert all(x.get(s,Q(0))==y.get(s,Q(0)) for s in STATES)
                cross+=1;cross_cells+=len(STATES)
        rec.append({'mu':str(mu),'beta':str(beta),'gamma':str(gamma),'dropout':str(d),'initial_k':k0,
                    'joint_tv':[str(v) for v in jtv], 'count_tv':[str(v) for v in ktv],
                    'first_joint':next((i for i,v in enumerate(jtv) if v),None),
                    'first_count':next((i for i,v in enumerate(ktv) if v),None)})
    assert len(rec)==48 and cross==384 and cross_cells==3840 and neg==24
    active=[r for r in rec if r['dropout']=='1/4']
    assert len(active)==24
    stats={'pairs':len(rec),'periods':13,'tv_values':len(rec)*13*2,'micro_trajectory_comparisons':cross,
           'micro_macro_probability_cells':cross_cells,'zero_dropout_exact_equivalence_pairs':neg,
           'positive_dropout_pairs':len(active),'first_joint_counts':dict(Counter(str(r['first_joint']) for r in rec)),
           'first_count_counts':dict(Counter(str(r['first_count']) for r in rec)),
           'active_t2_joint_tv_min':str(min(Q(r['joint_tv'][2]) for r in active)),
           'active_t2_joint_tv_max':str(max(Q(r['joint_tv'][2]) for r in active)),
           'active_t3_count_tv_min':str(min(Q(r['count_tv'][3]) for r in active)),
           'active_t3_count_tv_max':str(max(Q(r['count_tv'][3]) for r in active)),
           'active_t12_count_tv_min':str(min(Q(r['count_tv'][12]) for r in active)),
           'active_t12_count_tv_max':str(max(Q(r['count_tv'][12]) for r in active)),
           'active_t12_joint_tv_min':str(min(Q(r['joint_tv'][12]) for r in active)),
           'active_t12_joint_tv_max':str(max(Q(r['joint_tv'][12]) for r in active))}
    # Mutant: hysteresis mistakenly always resets when k=2.
    # It becomes the threshold rule; known reachable (k=2,J=1) must differ.
    mutant=institution('threshold',2,1)
    correct=institution('hysteresis',2,1)
    assert mutant==0 and correct==1
    assert any(Q(r['joint_tv'][2])>0 for r in active)
    stats['mutant_hysteresis_k2_reset_detected']=True
    out={'study':'R176_THIRD_METHOD_INSTITUTION_OBSERVABILITY_E1','stats':stats,'rows':rec,
         'evidence':'E1_SYNTHETIC','new_E2':0,'new_E3':0,'external_replication':False}
    with open(str(Path(__file__).resolve().with_name('r176_institution_observability_receipt_20261026.json')),'w') as f:
        json.dump(out,f,ensure_ascii=False,sort_keys=True,indent=2)
        f.write('\n')
    print(json.dumps(stats,ensure_ascii=False,indent=2))

if __name__=='__main__':run()
