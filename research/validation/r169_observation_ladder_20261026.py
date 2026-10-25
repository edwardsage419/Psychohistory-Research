"""R169 bounded observation ladder; exact rational finite-network calculations.
Uses only Python stdlib. Frozen design: protocols/R169_OBSERVATION_LADDER_72_WORLD_THIRD_METHOD_FREEZE_2026-10-26.md.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
import json, hashlib

GRAPHS = {
    'path':((0,1),(1,2),(2,3)),
    'star':((0,1),(0,2),(0,3)),
    'cycle':((0,1),(0,3),(1,2),(2,3)),
    'chord':((0,1),(0,2),(1,2),(2,3)),
}
OPINIONS={'block':(0,0,1,1),'alternate':(0,1,0,1),'singleton':(0,0,0,1)}
ALPHAS=(F(0),F(1,2),F(1)); MODES=('same','any')

def step(state,alpha,mode):
    edges,op=state
    active=[e for e in edges if op[e[0]]!=op[e[1]]]
    if not active: return {state:F(1)}
    out=defaultdict(F)
    for u,v in active:
        for anchor,other in ((u,v),(v,u)):
            weight=F(1,2*len(active))
            if alpha<1:
                next_op=list(op);next_op[anchor]=op[other]
                out[(edges,tuple(next_op))]+=weight*(1-alpha)
            if alpha>0:
                neighbors={b if a==anchor else a for a,b in edges if anchor in (a,b)}
                eligible=[k for k in range(4) if k!=anchor and k!=other and k not in neighbors and (mode=='any' or op[k]==op[anchor])]
                if eligible:
                    for k in eligible:
                        new_edges=tuple(sorted((set(edges)-{tuple(sorted((anchor,other)))})|{tuple(sorted((anchor,k)))}))
                        out[(new_edges,op)]+=weight*alpha/len(eligible)
                else:out[state]+=weight*alpha
    assert sum(out.values(),F(0))==1
    return dict(out)

def trajectory(state,alpha,mode):
    dist={state:F(1)};res=[dist]
    for _ in range(3):
        nxt=defaultdict(F)
        for s,mass in dist.items():
            for s2,p in step(s,alpha,mode).items():nxt[s2]+=mass*p
        assert sum(nxt.values(),F(0))==1
        dist=dict(nxt);res.append(dist)
    return res

def components(edges):
    parent=list(range(4))
    def find(i):
        while parent[i]!=i:i=parent[i]
        return i
    for a,b in edges:parent[find(a)]=find(b)
    return len({find(i) for i in range(4)})

def observable(s,level):
    edges,op=s
    a=sum(op)
    d=sum(op[i]!=op[j] for i,j in edges)
    if level==1:return (a,)
    if level==2:return (a,d)
    if level==3:return (a,d,components(edges))
    return (edges,op)

def marginal(dist,level):
    out=defaultdict(F)
    for s,p in dist.items():out[observable(s,level)]+=p
    return dict(out)

def signature(dist):return tuple(sorted((repr(k),str(v)) for k,v in dist.items()))

def tv(p,q):return sum((abs(p.get(k,F(0))-q.get(k,F(0))) for k in set(p)|set(q)),F(0))/2

def run():
    strata=[]; total={str(t):{str(k):{'classes':0,'uniques':0,'ambiguous':0,'distinguished_pairs':0} for k in range(1,5)} for t in range(1,4)}
    controls=[(a,m) for a in ALPHAS for m in MODES]
    witnesses=[]; full_paths=[]; path_state_checks=0
    for graph_name,edges in GRAPHS.items():
        for opinion_name,op in OPINIONS.items():
            start=(edges,op)
            trajectories={str(a)+'_'+m:trajectory(start,a,m) for a,m in controls}
            ids=list(trajectories)
            assert len(ids)==6
            for id_,path in trajectories.items():
                for t,dist in enumerate(path):
                    assert sum(dist.values(),F(0))==1
                    assert all(len(s[0])==len(edges) for s in dist)
                    path_state_checks+=len(dist)
                    full_paths.append([graph_name,opinion_name,id_,t,signature(dist)])
            row={'graph':graph_name,'opinion':opinion_name,'time':{}}
            for t in range(1,4):
                levels={k:{i:marginal(trajectories[i][t],k) for i in ids} for k in range(1,5)}
                for k in range(1,5):
                    groups=defaultdict(list)
                    for id_ in ids:groups[signature(levels[k][id_])].append(id_)
                    sizes=sorted(len(g) for g in groups.values())
                    uniques=sum(n==1 for n in sizes)
                    distinguish=sum(levels[k][i]!=levels[k][j] for i,j in combinations(ids,2))
                    val={'classes':len(groups),'uniques':uniques,'ambiguous':6-uniques,'distinguished_pairs':distinguish,'class_sizes':sizes}
                    row['time'].setdefault(str(t),{})['O'+str(k)]=val
                    for fld in ('classes','uniques','ambiguous','distinguished_pairs'):total[str(t)][str(k)][fld]+=val[fld]
                for i,j in combinations(ids,2):
                    for k in range(1,4):
                        if levels[k][i]!=levels[k][j] and levels[k+1][i]==levels[k+1][j]:
                            raise AssertionError('observation ladder refinement failed')
                    if levels[1][i]==levels[1][j] and levels[4][i]!=levels[4][j]:
                        witnesses.append({'graph':graph_name,'opinion':opinion_name,'t':t,'pair':[i,j],
                            'tv_O1':str(tv(levels[1][i],levels[1][j])),
                            'tv_O4':str(tv(levels[4][i],levels[4][j]))})
                assert all(levels[k]['0_same']==levels[k]['0_any'] for k in range(1,5))
                assert levels[1]['1_same']==levels[1]['1_any']
            strata.append(row)
    state=(GRAPHS['path'],OPINIONS['block'])
    original=step(state,F(1,2),'same'); mutant=step(state,F(1,3),'same')
    mutation_tv=tv(original,mutant)
    assert mutation_tv>0
    p=trajectory(state,F(1),'same')[2];q=trajectory(state,F(1),'any')[2]
    assert tv(p,q)==F(1,2), (tv(p,q),)
    digest=hashlib.sha256(json.dumps(full_paths,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    return {'research_id':'R169','evidence':'E1_INTERNAL_EXACT','worlds':72,'strata':12,'horizon':3,
        'levels':{'O1':'A count','O2':'A count + discordant edges','O3':'A count + discordant edges + components','O4':'full labeled graph and opinions'},
        'aggregate':total,'by_stratum':strata,'witness_count':len(witnesses),'witness_first':witnesses[0] if witnesses else None,
        'known_original_R169_TV2':'1/2','mutation_alpha_half_to_third_TV1':str(mutation_tv),
        'path_distribution_sha256':digest,'total_nonzero_state_snapshots':path_state_checks,
        'E2_new':0,'E3_new':0,'external_independent_replications':0}

if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True))
