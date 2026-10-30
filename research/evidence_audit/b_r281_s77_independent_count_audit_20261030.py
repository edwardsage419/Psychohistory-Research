#!/usr/bin/env python3
"""R281 S77 independent binomial-count oracle; Python standard library only."""
import argparse
import csv
import json
from collections import Counter
from fractions import Fraction as F
from math import comb
from pathlib import Path

PS=(F(1,4),F(1,2),F(3,4))
EPS=(F(1,16),F(1,4))
def sym(q,y):
    table={F(1,16):((4,-1,-1),(4,0,0)),
           F(15,16):((4,0,0),(4,-1,-1)),
           F(1,4):((2,-1,0),(2,0,0)),
           F(3,4):((2,0,0),(2,-1,0)),
           F(1,2):((1,0,0),(1,0,0))}
    return tuple(map(F,table[q][y]))
def oracle():
    out={}
    for p in PS:
        for b in (0,1):
            for eps in EPS:
                q=eps if b==0 else 1-eps
                c0,c1=sym(q,0),sym(q,1)
                risk=tuple((1-p)*c0[j]+p*c1[j] for j in range(3))
                win=sum((F(comb(4,k))*p**k*(1-p)**(4-k)
                         for k in range(5) if q**k*(1-q)**(4-k)>p**k*(1-p)**(4-k)),F(0))
                tie=sum((F(comb(4,k))*p**k*(1-p)**(4-k)
                         for k in range(5) if q**k*(1-q)**(4-k)==p**k*(1-p)**(4-k)),F(0))
                out[(str(p),str(b),str(eps))]=(tuple(map(str,risk)),str(win),str(tie))
    return out
def verify(csvpath,jsonpath):
    obj=json.loads(Path(jsonpath).read_text(encoding="utf-8"))
    if obj.get("evidence")!="E1_INTERNAL_NONBLIND_EXPLORATORY" or obj.get("world_count")!=12 or obj.get("source_count")!=192:
        raise ValueError("evidence or count")
    rows=list(csv.DictReader(Path(csvpath).open(encoding="utf-8",newline="")))
    if len(rows)!=192: raise ValueError("missing or duplicate rows")
    seen=set();counts=Counter();mass_sum=Counter();O=oracle()
    for r in rows:
        key=(r["p"],r["boundary"],r["epsilon"])
        full=key+(r["bits"],)
        if full in seen or key not in O: raise ValueError("duplicate or unknown source")
        seen.add(full)
        if len(r["bits"])!=4 or any(c not in "01" for c in r["bits"]): raise ValueError("bits")
        p,b,e=F(key[0]),int(key[1]),F(key[2]);q=e if b==0 else 1-e
        k=r["bits"].count("1");m=p**k*(1-p)**(4-k)
        c0,c1=sym(q,0),sym(q,1)
        cs=tuple((k*c1[j]+(4-k)*c0[j])/4 for j in range(3))
        expected={"q":str(q),"k":str(k),"mass":str(m),
                  "ln2":str(cs[0]),"ln3":str(cs[1]),"ln5":str(cs[2]),
                  "strict_win":str(int(q**k*(1-q)**(4-k)>p**k*(1-p)**(4-k))),
                  "tie":str(int(q**k*(1-q)**(4-k)==p**k*(1-p)**(4-k)))}
        if any(r.get(x)!=v for x,v in expected.items()): raise ValueError("source field mismatch")
        counts[key]+=1;mass_sum[key]+=m
    if len(counts)!=12 or any(v!=16 or mass_sum[k]!=1 for k,v in counts.items()):
        raise ValueError("universe or probability mass")
    if len(obj.get("worlds",[]))!=12: raise ValueError("world count")
    seenw=set()
    for r in obj["worlds"]:
        key=(r["p"],r["boundary"],r["epsilon"])
        if key in seenw or key not in O: raise ValueError("duplicate world")
        seenw.add(key)
        risk,win,tie=O[key]
        if tuple(r["risk_coefficients"])!=risk or r["strict_win_probability"]!=win or r["tie_probability"]!=tie:
            raise ValueError("analytic count mismatch")
        p,b=F(key[0]),int(key[1])
        inf=1-(1-p)**4 if b==0 else 1-p**4
        if r.get("original_unclipped_expected_risk")!="INF" or r.get("original_unclipped_infinite_probability")!=str(inf):
            raise ValueError("boundary infinity replaced")
    return True
def selftest():
    O=oracle()
    assert len(O)==12
    assert O[("1/4","0","1/16")]==(("4","-3/4","-3/4"),"81/256","0")
    assert O[("1/4","1","1/4")]==(("2","-1/4","0"),"13/256","27/128")
    assert O[("1/2","0","1/4")]==(("2","-1/2","0"),"5/16","0")
    assert O[("3/4","1","1/4")]==(("2","-3/4","0"),"0","1")
    print("B_COUNT_ORACLE_PASS worlds=12 cells=60; FROZEN_ZERO_TIE_ASSERTION_FAIL tie=27/128")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--csv");p.add_argument("--json")
    a=p.parse_args();selftest()
    if bool(a.csv)!=bool(a.json):p.error("both --csv and --json required")
    if a.csv:
        verify(a.csv,a.json)
        print("B_PERSISTED_RECEIPT_PASS 192 rows")
