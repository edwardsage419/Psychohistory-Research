#!/usr/bin/env python3
"""R330 independent exact rational audit, no production imports."""
import csv
import io
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"R330"
CSV=ROOT/"R330_ALL_256_ARTIFICIAL_MEMORY_ATOMS.csv"
RESULT=ROOT/"R330_EXACT_64_RETRIEVAL_WORLDS.json"

def audit(csv_text,json_text):
    rows=list(csv.DictReader(io.StringIO(csv_text)))
    data=json.loads(json_text)
    assert len(rows)==256 and len(data["worlds"])==64
    assert data["source_row_count"]==256 and data["world_count"]==64
    index=0
    for outcomes in product((0,1),repeat=4):
        history="".join(map(str,outcomes))
        for cue in (0,1):
            for decay in (0,1):
                memories=[(1,"A",0,outcomes[0]),(2,"B",1,outcomes[1]),
                          (3,"A",1,outcomes[2]),(4,"B",0,outcomes[3])]
                weights=[(F(1) if instance_cue==cue else F(1,2))/
                         (F(5-time)**decay) for time,_,instance_cue,_ in memories]
                numer={a:sum((weights[i]*m[3] for i,m in enumerate(memories) if m[1]==a),F(0)) for a in ("A","B")}
                denom={a:sum((weights[i] for i,m in enumerate(memories) if m[1]==a),F(0)) for a in ("A","B")}
                scores={a:numer[a]/denom[a] for a in ("A","B")}
                choice="A" if scores["A"]>=scores["B"] else "B"
                world=data["worlds"][index//4]
                assert world==dict(history=history,query_cue=cue,decay=decay,
                                   score_a=str(scores["A"]),score_b=str(scores["B"]),chosen_action=choice)
                for i,(time,action,instance_cue,utility) in enumerate(memories):
                    expected=dict(history=history,query_cue=str(cue),decay=str(decay),
                                  time=str(time),action=action,instance_cue=str(instance_cue),
                                  utility=str(utility),weight=str(weights[i]),
                                  action_score=str(scores[action]),chosen_action=choice)
                    assert rows[index]==expected,(index,rows[index],expected)
                    index+=1
    assert index==256
    return True

def main():
    a,b=CSV.read_text(),RESULT.read_text()
    audit(a,b)
    altered=a.replace(",1/2,",",1/3,",1)
    assert altered!=a
    rejected=False
    try:audit(altered,b)
    except (AssertionError,ValueError):rejected=True
    assert rejected
    print("R330 independent exact 256-row 64-world audit PASS; tamper rejected")

if __name__=="__main__":main()
