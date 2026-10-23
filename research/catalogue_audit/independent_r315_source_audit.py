#!/usr/bin/env python3
"""Independent no-import R315 source/path replay; uses Floyd Warshall."""
from __future__ import annotations
import argparse
import csv
import json
from fractions import Fraction
from pathlib import Path
from collections import Counter

D=Path(__file__).resolve().parents[1]/"R315"
SRC=D/"R315_ALL_210_ORIGINAL_REWIRING_ATOMS.csv"
OUT=D/"R315_EXACT_180_TWO_EVENT_GRAPH_PATHS.json"

def label(e):
    return ";".join(f"{a}-{b}" for a,b in sorted(e))
def edge(a,b):
    assert a!=b
    return (min(a,b),max(a,b))
def seed(n):
    return set(edge(i,(i+d)%n) for i in range(n) for d in (1,2))
def adj(e,n):
    a=[set() for _ in range(n)]
    for x,y in e:
        a[x].add(y)
        a[y].add(x)
    return a
def independent_metrics(e,n):
    a=adj(e,n)
    cs=[]
    for v in range(n):
        b=sorted(a[v])
        links=sum(edge(x,y) in e for pos,x in enumerate(b) for y in b[pos+1:])
        cs.append(Fraction(links, len(b)*(len(b)-1)//2) if len(b)>=2 else Fraction(0))
    C=sum(cs,Fraction(0))/n
    inf=10**6
    dist=[[0 if i==j else (1 if j in a[i] else inf) for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j]=min(dist[i][j],dist[i][k]+dist[k][j])
    unseen=set(range(n));components=0
    while unseen:
        v=min(unseen)
        unseen.difference_update({j for j in range(n) if dist[v][j]<inf})
        components+=1
    L=None if components!=1 else Fraction(sum(dist[i][j] for i in range(n) for j in range(i+1,n)), n*(n-1)//2)
    return (str(C),str(L) if L is not None else None,components)

def independently_replay():
    with SRC.open(encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f))
    archive=json.loads(OUT.read_text(encoding="utf-8"))
    assert len(rows)==archive["source_atom_count"]==210
    assert archive["full_path_count"]==180
    seen_keys=set();offset=0;checked_paths=0
    for n in (8,10):
        base=seed(n);initial=label(base)
        assert len(base)==2*n
        for prob in (Fraction(0),Fraction(1,2),Fraction(1)):
            item=archive["parameter_worlds"][((n-8)//2)*3+(0 if prob==0 else (1 if prob==Fraction(1,2) else 2))]
            assert item["N"]==n and item["p"]==str(prob) and item["baseline_edges"]==initial
            C,L,comp=independent_metrics(base,n)
            assert (item["baseline_clustering"],item["baseline_mean_shortest_path"],item["baseline_components"])==(C,L,comp)
            expected_paths=[]
            first_options=[]
            for action,target in [("keep",-1)]+[("rewire",t) for t in range(n) if t!=0 and t not in adj(base,n)[0]]:
                first_options.append((action,target))
            first_rows=[]
            for a1,t1 in first_options:
                row=rows[offset];offset+=1
                w1=Fraction(1)-prob if a1=="keep" else prob/Fraction(len(first_options)-1)
                mid=set(base)
                if a1=="rewire":
                    mid.remove(edge(0,1));mid.add(edge(0,t1))
                assert row==dict(zip(row,[])) if False else True
                expected=[n,str(prob),1,"none",-1,0,1,a1,t1,initial,str(w1),label(mid)]
                if tuple(row.values())!=tuple(map(str,expected)):
                    raise AssertionError(f"invalid R315 stage 1 source {n=} {prob=} {a1=} {t1=}")
                key=(row["N"],row["p"],row["stage"],row["prior_action"],row["prior_target"],row["action"],row["new_target"])
                assert key not in seen_keys;seen_keys.add(key)
                second_targets=[t for t in range(n) if t!=1 and t not in adj(mid,n)[1]]
                options=[("keep",-1)]+[("rewire",t) for t in second_targets]
                for a2,t2 in options:
                    r2=rows[offset];offset+=1
                    w2=Fraction(1)-prob if a2=="keep" else prob/Fraction(len(options)-1)
                    end=set(mid)
                    if a2=="rewire":
                        end.remove(edge(1,2));end.add(edge(1,t2))
                    expected2=[n,str(prob),2,a1,t1,1,2,a2,t2,label(mid),str(w2),label(end)]
                    if tuple(r2.values())!=tuple(map(str,expected2)):
                        raise AssertionError(f"invalid R315 stage 2 source {n=} {prob=} {a1=} {a2=}")
                    k2=(r2["N"],r2["p"],r2["stage"],r2["prior_action"],r2["prior_target"],r2["action"],r2["new_target"])
                    assert k2 not in seen_keys;seen_keys.add(k2)
                    assert len(end)==len(base)==2*n and all(a<b for a,b in end)
                    metrics=independent_metrics(end,n)
                    expected_paths.append({
                        "first_action":a1,"first_target":t1,"second_action":a2,"second_target":t2,
                        "probability":str(w1*w2),"final_edges":label(end),
                        "clustering":metrics[0],"mean_shortest_path":metrics[1],"components":metrics[2]
                    })
            assert item["complete_paths"]==expected_paths
            assert len(expected_paths)==(19 if n==8 else 41)
            assert sum(Fraction(x["probability"]) for x in expected_paths)==1
            if prob==0:
                positive=[x for x in expected_paths if Fraction(x["probability"])>0]
                assert len(positive)==1 and positive[0]["final_edges"]==initial
            checked_paths+=len(expected_paths)
    assert offset==len(rows)==210 and len(seen_keys)==210 and checked_paths==180
    assert Counter(x["N"] for x in rows)=={"8":69,"10":141}
    return {"result":"PASS","independent_source_rows":210,"full_two_edge_paths":180,"graph_metric_method":"FLOYD_WARSHALL","real_human_E2":0,"historical_E3":0}

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--audit",action="store_true");parser.add_argument("--test",action="store_true")
    parser.parse_args()
    print(json.dumps(independently_replay(),sort_keys=True))
