#!/usr/bin/env python3
"""R317 independent temporal reachability via explicit path-subsequence enumeration."""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"R317"
SRC=D/"R317_ALL_81_ORIGINAL_TEMPORAL_CONTACT_SOURCE_ROWS.csv"
OUT=D/"R317_ALL_81_ORIGIN_TEMPORAL_REACHABILITY_OUTCOMES.json"
EDGE=((0,1),(0,2),(1,2))
HEAD=("schedule_id","schedule_code","time","contact_index","node_u","node_v")

def independent_earliest(schedule,origin):
    best=[None]*3
    best[origin]=0
    def rec(i,place):
        if i==3:return
        rec(i+1,place)  # Wait and optionally choose a later contact.
        u,v=EDGE[schedule[i]]
        if place in (u,v):
            nxt=v if place==u else u
            if best[nxt] is None or i+1<best[nxt]: best[nxt]=i+1
            rec(i+1,nxt)
    rec(0,origin)
    return best

def independent_static(schedule,origin):
    links=set(EDGE[j] for j in schedule)
    seen={origin}
    again=True
    while again:
        again=False
        for a,b in links:
            if a in seen and b not in seen:seen.add(b);again=True
            if b in seen and a not in seen:seen.add(a);again=True
    return sorted(seen)

def audit():
    with SRC.open(encoding="utf-8",newline="") as f:rows=list(csv.DictReader(f))
    data=json.loads(OUT.read_text(encoding="utf-8"))
    assert len(rows)==81 and data["source_rows"]==81
    assert data["schedule_count"]==27
    assert data["origin_evaluations"]==len(data["outcomes"])==81
    assert tuple(rows[0])==HEAD
    assert len({(x["schedule_id"],x["time"]) for x in rows})==81
    assert Counter(x["schedule_id"] for x in rows)=={str(i):3 for i in range(27)}
    deficits=0
    for sid in range(27):
        order=(sid//9,(sid//3)%3,sid%3)
        code="".join(str(x) for x in order)
        for t,k in enumerate(order,1):
            r=rows[3*sid+t-1]
            assert tuple(r.values())==tuple(map(str,(sid,code,t,k,*EDGE[k])))
        for origin in range(3):
            arrival=independent_earliest(order,origin)
            temporal=[i for i,x in enumerate(arrival) if x is not None]
            stat=independent_static(order,origin)
            missing=sorted(set(stat)-set(temporal))
            assert origin not in missing
            assert set(temporal).issubset(stat)
            want={"schedule_id":sid,"schedule_code":code,"origin":origin,
                  "earliest_arrival":arrival,"temporal_reachable":temporal,
                  "static_reachable":stat,"static_overstatement_targets":missing}
            actual=data["outcomes"][3*sid+origin]
            assert actual==want,(sid,origin,actual,want)
            deficits+=len(missing)
    assert deficits==data["ordered_static_overstatement_pairs"]==12
    witness0=data["outcomes"][3*18]
    witness2=data["outcomes"][3*18+2]
    assert witness0["earliest_arrival"]==[0,2,None]
    assert witness2["earliest_arrival"]==[2,1,0]
    assert witness0["static_reachable"]==[0,1,2]
    return {"status":"PASS","original_source_rows":81,"schedule_origin_outcomes":81,
            "static_overstatement_ordered_pairs":deficits,"human_E2":0,"history_E3":0}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true");p.add_argument("--audit",action="store_true")
    p.parse_args()
    print(json.dumps(audit(),sort_keys=True))
