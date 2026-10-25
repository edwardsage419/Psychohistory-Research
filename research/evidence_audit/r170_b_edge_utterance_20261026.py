"""Independent R170 third-method B route: explicit undirected edge, utterance and flip.
Uses Python standard library only. Frozen 2026-10-26 protocol.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
import json

GRAPHS = {
 'path': ((0,1),(1,2),(2,3)),
 'star': ((0,1),(0,2),(0,3)),
 'cycle': ((0,1),(0,3),(1,2),(2,3)),
 'complete': ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3)),
}
INITIALS = {'split': (1,1,2,2), 'alternate': (1,2,1,2), 'bilingual': (1,3,2,3)}
NU = (F(0),F(1,4),F(1,2))
MODES = ('both_confirm','listener_only')

def direct_step(edges, inventory, nu, mode):
    result=defaultdict(F)
    for u,v in edges:
        for speaker,hearer in ((u,v),(v,u)):
            utterable=[w for w in (1,2) if inventory[speaker]&w]
            for uttered in utterable:
                for heard,noise_mass in ((uttered,1-nu),(3-uttered,nu)):
                    if not noise_mass: continue
                    nxt=list(inventory)
                    if nxt[hearer]&heard:
                        nxt[hearer]=heard
                        if mode=='both_confirm': nxt[speaker]=heard
                    else:
                        nxt[hearer]|=heard
                    result[tuple(nxt)]+=F(1,2*len(edges)*len(utterable))*noise_mass
    assert sum(result.values(),F())==1
    return dict(result)

def full_path(edges,initial,nu,mode):
    dist={initial:F(1)}
    snapshots=[dist]
    for t in range(3):
        nxt=defaultdict(F)
        for inv,p in dist.items():
            for inv2,q in direct_step(edges,inv,nu,mode).items():nxt[inv2]+=p*q
        dist=dict(nxt)
        assert sum(dist.values(),F())==1
        assert all(len(inv)==4 and all(mask in (1,2,3) for mask in inv) for inv in dist)
        snapshots.append(dist)
    return snapshots

def observe(inv,edges,level):
    if level=='O4':return inv
    hist=(inv.count(1),inv.count(2),inv.count(3))
    if level=='O1':return (hist[2],)
    if level=='O2':return hist
    return hist+(sum(inv[u]&inv[v]==0 for u,v in edges),)

def coarsen(dist,edges,level):
    law=defaultdict(F)
    for inv,p in dist.items():law[observe(inv,edges,level)]+=p
    assert sum(law.values(),F())==1
    return dict(law)

def sig(law):return tuple(sorted(law.items()))
def tv(a,b):return sum((abs(a.get(k,F())-b.get(k,F())) for k in set(a)|set(b)),F())/2

def main():
    levels=('O1','O2','O3','O4')
    aggregates={(t,l):dict(classes=0,unique=0,ambiguous=0,distinguishable_pairs=0) for t in (1,2,3) for l in levels}
    strata=[]; full={};laws={}; first_witness=None; normalization=0; state_snapshots=0
    for graph,edges in GRAPHS.items():
        for initial,inv in INITIALS.items():
            group=(graph,initial)
            six=[(nu,mode) for nu in NU for mode in MODES]
            for nu,mode in six:
                path=full_path(edges,inv,nu,mode)
                full[(graph,initial,nu,mode)]=path
                state_snapshots+=len(path)
                for t in range(4):
                    normalization+=1
                    for level in levels:
                        laws[(graph,initial,nu,mode,t,level)]=coarsen(path[t],edges,level)
            for t in (1,2,3):
                record={'graph':graph,'initial':initial,'t':t}
                for level in levels:
                    classes=defaultdict(list)
                    for nu,mode in six:
                        classes[sig(laws[(graph,initial,nu,mode,t,level)])].append((str(nu),mode))
                    unique=sum(len(c)==1 for c in classes.values())
                    amb=6-unique
                    distinct=15-sum(len(c)*(len(c)-1)//2 for c in classes.values())
                    assert unique+amb==6
                    record[level]={'classes':len(classes),'unique':unique,'ambiguous':amb,'distinguishable_pairs':distinct}
                    for k,v in zip(('classes','unique','ambiguous','distinguishable_pairs'),(len(classes),unique,amb,distinct)):
                        aggregates[(t,level)][k]+=v
                assert all(record[levels[i]]['classes']<=record[levels[i+1]]['classes'] for i in range(3))
                strata.append(record)
                if first_witness is None:
                    for a,b in combinations(six,2):
                        x=(graph,initial,*a,t)
                        y=(graph,initial,*b,t)
                        d1=tv(laws[x+('O1',)],laws[y+('O1',)])
                        d4=tv(laws[x+('O4',)],laws[y+('O4',)])
                        if d1==0 and d4>0:
                            first_witness={'graph':graph,'initial':initial,'t':t,'control_a':[str(a[0]),a[1]],'control_b':[str(b[0]),b[1]],'tv_O1':str(d1),'tv_O4':str(d4)}
                            break
    assert len(strata)==36 and normalization==288 and state_snapshots==288
    mono_equal=0
    for graph in GRAPHS:
        for initial in ('split','alternate'):
            a=full[(graph,initial,F(0),'both_confirm')][1]
            b=full[(graph,initial,F(0),'listener_only')][1]
            assert a==b
            mono_equal+=1
    edges=GRAPHS['path'];init=INITIALS['bilingual']
    perturb=full_path(edges,init,F(1,3),'both_confirm')[1]
    base=full[('path','bilingual',F(1,4),'both_confirm')][1]
    delta=tv(base,perturb)
    assert delta>0
    out={'schema':'r170_observation_ladder_B_v1','route':'independent_undirected_edge_speaker_utterance_flip',
      'worlds':72,'state_snapshots':state_snapshots,'normalized_snapshots':normalization,
      'strata':strata,'aggregate':{f't{t}_{level}':aggregates[(t,level)] for t in (1,2,3) for level in levels},
      'monolingual_nu0_first_step_equal':mono_equal,'mutation_t1_full_TV':str(delta),'first_witness':first_witness,
      'E1_only':True,'E2':0,'E3':0}
    print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))
if __name__=='__main__':main()
