#!/usr/bin/env python3
"""R321 independent no-import state-mass audit of original CSV and result JSON."""
import csv,itertools,json
from collections import defaultdict
from fractions import Fraction as F
from math import comb
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]/"R321"
source=HERE/"R321_ALL_1024_ORIGINAL_SEVEN_BIT_PATHS.csv"
result=HERE/"R321_EXACT_8_WORLDS.json"
pairs=((F(1,4),F(3,4)),(F(1,3),F(2,3)))
def independent():
    rows=list(csv.DictReader(source.open(encoding="utf-8",newline="")))
    summary=json.loads(result.read_text(encoding="utf-8"))
    assert len(rows)==1024 and len(summary["worlds"])==8
    assert summary["original_catalogue_id"]=="01-010"
    for wid,w in enumerate(summary["worlds"]):
        p0,p1=pairs[wid//4];k=2+(wid%4)//2;truth=("H0","H1")[wid%2];p=p0 if truth=="H0" else p1
        assert (w["world_id"],w["p0"],w["p1"],w["K"],w["true_hypothesis"])==(wid,str(p0),str(p1),k,truth)
        block=rows[wid*128:(wid+1)*128]
        outcomes={"H0":F(0),"H1":F(0),"none":F(0)}
        for row,bits in zip(block,itertools.product((0,1),repeat=7)):
            b="".join(map(str,bits));m=p**sum(bits)*(1-p)**(7-sum(bits))
            s=0;decision="none";stop=None
            for t,bit in enumerate(bits,1):
                s+=1 if bit else -1
                if s>=k:decision="H1";stop=t;break
                if s<=-k:decision="H0";stop=t;break
            assert row==dict(zip(row.keys(),(str(wid),str(p0),str(p1),str(k),truth,str(p),b,str(sum(bits)),str(m),"" if stop is None else str(stop),decision,str(stop is None).lower())))
            outcomes[decision]+=m
        assert sum(outcomes.values())==1
        # Distinct method: propagate only surviving states, never enumerate full paths.
        alive={0:F(1)};absorbed={"H0":F(0),"H1":F(0)};cells=[];expected=F(0)
        for t in range(1,8):
            nxt=defaultdict(F);c0=c1=F(0)
            for s,m in alive.items():
                for delta,weight in ((-1,1-p),(1,p)):
                    ss=s+delta;mm=m*weight
                    if ss<=-k:c0+=mm
                    elif ss>=k:c1+=mm
                    else:nxt[ss]+=mm
            absorbed["H0"]+=c0;absorbed["H1"]+=c1
            expected+=t*(c0+c1)
            cells.append({"time":t,"accept_H0":str(c0),"accept_H1":str(c1)})
            alive=nxt
        censor=sum(alive.values(),F(0));expected+=7*censor
        fixed=sum((F(comb(7,j))*p**j*(1-p)**(7-j) for j in range(4,8)),F(0))
        assert absorbed["H0"]==outcomes["H0"] and absorbed["H1"]==outcomes["H1"] and censor==outcomes["none"]
        assert (w["accept_H0"],w["accept_H1"],w["censored"],w["expected_truncated_samples"],w["fixed7_majority_choose_H1"])==(str(absorbed["H0"]),str(absorbed["H1"]),str(censor),str(expected),str(fixed))
        assert w["first_stop_cells"]==cells
    print("R321_INDEPENDENT_DP_AUDIT_PASS 1024 paths 8 worlds no generator import")
if __name__=="__main__":independent()
