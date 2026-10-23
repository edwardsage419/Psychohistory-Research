#!/usr/bin/env python3
"""R331 independent no-import exact rational source audit."""
import csv
import io
import json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"R331"
CSV=ROOT/"R331_ALL_81_ARTIFICIAL_RETENTION_ATOMS.csv"
JSON=ROOT/"R331_EXACT_9_RETENTION_WORLDS.json"

def audit(csv_text,json_text):
    rows=list(csv.DictReader(io.StringIO(csv_text)))
    result=json.loads(json_text)
    assert len(rows)==81
    assert result["source_row_count"]==81
    assert result["world_count"]==len(result["worlds"])==9
    assert result["model"]=="R331_CONSTRUCTED_HETEROGENEOUS_RETENTION_E1"
    pairs=((F(1,4),F(1,2)),(F(1,4),F(3,4)),(F(1,2),F(3,4)))
    weights=(F(1,4),F(1,2),F(3,4))
    cursor=0
    for a,b in pairs:
        for w in weights:
            ident=f"W{cursor//9+1:02d}"
            vals={}
            for t in range(9):
                fast=w*pow(a,t)
                slow=(1-w)*pow(b,t)
                s=fast+slow
                q=pow(w*a+(1-w)*b,t)
                expected=dict(world_id=ident,a=str(a),b=str(b),w=str(w),t=str(t),
                              fast_contribution=str(fast),slow_contribution=str(slow),
                              mixture=str(s),homogeneous=str(q),gap=str(s-q))
                assert rows[cursor]==expected,(cursor,rows[cursor],expected)
                vals[t]=(s,q,s-q)
                cursor+=1
            s2,q2,g2=vals[2]
            s8,q8,g8=vals[8]
            world=dict(world_id=ident,a=str(a),b=str(b),w=str(w),
                       s2=str(s2),q2=str(q2),gap2=str(g2),
                       s8=str(s8),q8=str(q8),gap8=str(g8))
            assert result["worlds"][cursor//9-1]==world
            assert vals[0][2]==vals[1][2]==0
            assert g2==w*(1-w)*(b-a)**2>0
            assert all(vals[t][2]>0 for t in range(2,9))
    assert cursor==81
    return True

def main():
    a,b=CSV.read_text(encoding="utf-8"),JSON.read_text(encoding="utf-8")
    audit(a,b)
    lines=a.splitlines(keepends=True)
    assert "1/4" in lines[1]
    lines[1]=lines[1].replace("1/4","1/3",1)
    rejected=False
    try:audit("".join(lines),b)
    except (AssertionError,ValueError,KeyError):rejected=True
    assert rejected,"Tampered CSV accepted"
    print("R331 independent 81-row 9-world audit PASS; tamper rejected")

if __name__=="__main__":main()
