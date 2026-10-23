#!/usr/bin/env python3
"""R332 independent no-import audit of exact artificial resource allocation."""
import csv
import io
import json
from itertools import product
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"R332"
CSV=ROOT/"R332_ALL_112_ARTIFICIAL_RESOURCE_SUBSETS.csv"
JSON=ROOT/"R332_EXACT_14_RESOURCE_WORLDS.json"

def audit(csv_text,json_text):
    rows=list(csv.DictReader(io.StringIO(csv_text)))
    data=json.loads(json_text)
    assert len(rows)==112 and data["source_row_count"]==112
    assert len(data["worlds"])==data["world_count"]==14
    assert data["model"]=="R332_CONSTRUCTED_THREE_TASK_RESOURCE_E1"
    cursor=0
    observed=[[],[]]
    for r in (0,1):
        for cap in range(7):
            local=[]
            for flags in product((0,1),repeat=3):
                bits="".join(str(x) for x in flags)
                cost=flags[0]+flags[1]*(1 if r else 2)+flags[2]*3
                util=flags[0]+flags[1]*3+flags[2]*4
                local.append((bits,cost,util,cost<=cap))
            best=max(x[2] for x in local if x[3])
            winners=[x[0] for x in local if x[3] and x[2]==best]
            chosen=sorted(winners)[0]
            observed[r].append(best)
            for bits,cost,util,feasible in local:
                expected=dict(recoded=str(r),capacity=str(cap),bits=bits,
                              cost=str(cost),utility=str(util),feasible=str(int(feasible)),
                              chosen_bits=chosen,optimal_utility=str(best))
                assert rows[cursor]==expected,(cursor,rows[cursor],expected)
                cursor+=1
            expected_world=dict(recoded=r,capacity=cap,chosen_bits=chosen,optimal_utility=best,
                                feasible_count=sum(x[3] for x in local),
                                optimal_tie_count=len(winners))
            assert data["worlds"][r*7+cap]==expected_world
    assert cursor==112
    assert observed[0]==[0,1,3,4,5,7,8]
    assert observed[1]==[0,3,4,4,7,8,8]
    return True

def main():
    a,b=CSV.read_text(),JSON.read_text()
    audit(a,b)
    lines=a.splitlines(keepends=True)
    assert ",000,0,0,1," in lines[1]
    lines[1]=lines[1].replace(",000,0,0,1,",",000,1,0,1,",1)
    rejected=False
    try:audit("".join(lines),b)
    except (AssertionError,ValueError,KeyError):rejected=True
    assert rejected,"Tampered source accepted"
    print("R332 independent 112-row 14-world audit PASS; tamper rejected")
if __name__=="__main__":main()
