#!/usr/bin/env python3
"""R314 independent degree-sum verifier, never imports the model generator."""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

DIR=Path(__file__).resolve().parents[1]/"R314"
BASE={
    "P3":{(0,1),(1,2)},
    "K3":{(0,1),(0,2),(1,2)},
    "S4":{(0,1),(0,2),(0,3)}
}
HEAD=["seed","stage","prefix","edges_before","old_node_count","target","target_degree","degree_sum","choice_probability","edges_after"]
def token(edges):
    return ";".join(f"{i}-{j}" for i,j in sorted(edges))
def identity(edges):
    assert edges
    allnodes={v for e in edges for v in e}
    assert allnodes==set(range(len(allnodes)))
    return len(allnodes)
def degree(edges):
    n=identity(edges)
    return [sum(i in edge for edge in edges) for i in range(n)]
def new_edges(edges,dst):
    n=identity(edges)
    assert 0<=dst<n
    return edges|{(dst,n)}

def audit():
    with (DIR/"R314_ALL_54_ORIGINAL_TARGET_SOURCE_ATOMS.csv").open(newline="",encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    o=json.loads((DIR/"R314_EXACT_44_TWO_ARRIVAL_PATH_RESULTS.json").read_text(encoding="utf-8"))
    assert len(rows)==54 and list(rows[0])==HEAD
    assert len(o["seed_results"])==3
    assert o["source_atoms"]==54 and o["two_arrival_paths"]==44
    expected_rows=[]
    expected_paths={}
    for seed,base in BASE.items():
        n=identity(base)
        first=degree(base)
        firstsum=sum(first)
        assert firstsum==2*len(base)
        paths=[]
        for chosen in range(n):
            p=Fraction(first[chosen],firstsum)
            expected_rows.append((seed,1,"none",token(base),n,chosen,first[chosen],
                                  firstsum,str(p),token(new_edges(base,chosen))))
        for chosen in range(n):
            intermediate=new_edges(base,chosen)
            second=degree(intermediate)
            secondsum=sum(second)
            assert secondsum==firstsum+2
            for j in range(n+1):
                p=Fraction(second[j],secondsum)
                after=new_edges(intermediate,j)
                expected_rows.append((seed,2,chosen,token(intermediate),n+1,j,second[j],
                                      secondsum,str(p),token(after)))
                paths.append({"first_target":chosen,"second_target":j,
                              "path_probability":str(Fraction(first[chosen],firstsum)*p),
                              "final_edges":token(after)})
        assert sum(Fraction(x["path_probability"]) for x in paths)==1
        expected_paths[seed]={"seed":seed,"initial_edges":token(base),
                              "first_choices":n,"second_choice_atoms":n*(n+1),
                              "paths":paths}
    for actual,expected in zip(rows,expected_rows):
        if tuple(actual.values())!=tuple(str(x) for x in expected):
            raise AssertionError(f"source mismatch: {actual} expected {expected}")
    assert len(expected_rows)==54
    assert [x["seed"] for x in o["seed_results"]]==list(BASE)
    for item in o["seed_results"]:
        assert item==expected_paths[item["seed"]]
    assert Counter(row["seed"] for row in rows)=={"P3":15,"K3":15,"S4":24}
    assert Counter(row["stage"] for row in rows)=={"1":10,"2":44}
    assert len({(x["seed"],x["stage"],x["prefix"],x["target"]) for x in rows})==54
    assert [x["path_probability"] for x in expected_paths["P3"]["paths"]][:1]==["1/12"]
    return {"status":"PASS","seeds":3,"conditional_source_atoms":54,"two_step_paths":44,
            "new_human_E2":0,"new_history_E3":0}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true");p.add_argument("--audit",action="store_true")
    p.parse_args()
    print(json.dumps(audit(),sort_keys=True))
