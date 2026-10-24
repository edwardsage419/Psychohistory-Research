#!/usr/bin/env python3
"""R342 independent no-import three-actor choice enumerator."""
import csv
import io
import json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"R342"
EDGES=((0,1),(0,2),(1,0),(1,2),(2,0),(2,1))

def recreate():
    out=io.StringIO(newline="")
    writer=csv.writer(out,lineterminator="\n")
    writer.writerow(["r","network_bits","actor","choice","target","result_bits","reciprocity","weight","probability"])
    decisions=[]
    for r in (1,2):
        for mask in range(64):
            bits=f"{mask:06b}"
            adjacency=[[0]*3 for _ in range(3)]
            for i,(u,v) in enumerate(EDGES):
                adjacency[u][v]=int(bits[i])
            for actor in (0,1,2):
                other=sorted(set((0,1,2))-{actor})
                choices=(("stay",None),("toggle_first",other[0]),("toggle_second",other[1]))
                local=[]
                for label,target in choices:
                    arr=[row[:] for row in adjacency]
                    if target is not None:
                        arr[actor][target]=1-arr[actor][target]
                    result="".join(str(arr[u][v]) for u,v in EDGES)
                    u=sum(arr[actor][j]*arr[j][actor] for j in other)
                    w=r**u
                    local.append((label,"NONE" if target is None else str(target),result,u,w))
                z=sum(x[4] for x in local)
                ps=[]
                for label,target,result,u,w in local:
                    p=Fraction(w,z)
                    ps.append(p)
                    writer.writerow([str(r),bits,str(actor),label,target,result,str(u),str(Fraction(w)),str(p)])
                decisions.append({"r":str(r),"network_bits":bits,"actor":actor,"probabilities":[str(p) for p in ps]})
    obj={
        "schema":"R342_frozen_three_actor_local_choice_v1",
        "checks":{
            "worlds":2,"networks":64,"actors":3,"decisions":384,"source_rows":1152,
            "uniform_choice_decisions":192,"normalized_decisions":384,
        },
        "decisions":decisions,
    }
    return out.getvalue().encode(),(json.dumps(obj,indent=2,ensure_ascii=True)+"\n").encode()

def main():
    csv_expected,json_expected=recreate()
    csv_actual=(ROOT/"R342_ALL_1152_ARTIFICIAL_ACTOR_CHOICE_ATOMS.csv").read_bytes()
    json_actual=(ROOT/"R342_EXACT_384_LOCAL_DECISIONS.json").read_bytes()
    assert csv_actual==csv_expected,"independent CSV mismatch"
    assert json_actual==json_expected,"independent JSON mismatch"
    assert b'"source_rows": 1152' in json_expected
    assert b"1,000000,0,stay,NONE,000000,0,1,1/3" in csv_expected
    assert csv_actual!=csv_expected.replace(b"1,000000,0,stay,NONE,000000,0,1,1/3",b"1,000000,0,stay,NONE,000000,0,1,1/2")
    assert json_actual!=json_expected.replace(b'"source_rows": 1152',b'"source_rows": 1153')
    print("R342_INDEPENDENT_NO_IMPORT_AUDIT=PASS; NEGATIVE_TAMPER_TESTS=2")

if __name__=="__main__":
    main()
