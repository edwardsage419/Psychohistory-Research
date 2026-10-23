#!/usr/bin/env python3
"""R320 independent no-import path audit with interior-mass DP crosscheck."""
import csv
import json
from collections import defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"R320"
FIELDS=("world_id","upper_bound","start","p_up","path_bits","up_steps","down_steps",
        "full_path_probability","first_hit_time","first_hit_side","censored")

def audit():
    with (ROOT/"R320_ALL_384_ORIGINAL_SIX_STEP_PATHS.csv").open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f);assert tuple(reader.fieldnames)==FIELDS;rows=list(reader)
    obj=json.loads((ROOT/"R320_EXACT_6_FIRST_HIT_WORLDS.json").read_text(encoding="utf-8"))
    assert len(rows)==384 and obj["world_count"]==6 and obj["original_path_source_rows"]==384
    assert obj["discrete_analogue_only"] is True and obj["original_catalogue_id"]=="01-009"
    expected=[];wid=0
    for upper in (4,6):
        for p in (Fraction(1,4),Fraction(1,2),Fraction(3,4)):
            # Independent first-passage DP: only interior mass is propagated.
            interior={upper//2:Fraction(1)}
            cells={(t,s):Fraction(0) for t in range(1,7) for s in ("lower","upper")}
            expected_truncated=Fraction(0)
            for t in range(1,7):
                expected_truncated+=sum(interior.values(),Fraction(0))
                nxt=defaultdict(Fraction)
                for x,mass in interior.items():
                    for step,prob in ((-1,1-p),(1,p)):
                        new=x+step
                        if new==0:cells[(t,"lower")]+=mass*prob
                        elif new==upper:cells[(t,"upper")]+=mass*prob
                        else:nxt[new]+=mass*prob
                interior=dict(nxt)
            survival=sum(interior.values(),Fraction(0))
            hit_total=sum(cells.values(),Fraction(0))
            weighted=sum((t*(cells[(t,"lower")]+cells[(t,"upper")])
                          for t in range(1,7)),Fraction(0))
            w=obj["worlds"][wid]
            assert w=={"world_id":wid,"upper_bound":upper,"start":upper//2,
                       "p_up":str(p),
                       "hit_by_time_and_side":[{"time":t,"lower":str(cells[(t,"lower")]),
                                                "upper":str(cells[(t,"upper")])} for t in range(1,7)],
                       "survival":str(survival),"hit_total":str(hit_total),
                       "conditional_mean_decision_steps_among_hits":str(weighted/hit_total),
                       "expected_truncated_steps":str(expected_truncated)}
            assert survival+hit_total==1
            # Audit each source path separately from the independent DP.
            for bits in product((0,1),repeat=6):
                pos=upper//2;t_hit=None;side="none"
                for t,bit in enumerate(bits,1):
                    pos+=2*bit-1
                    if pos==0 or pos==upper:
                        t_hit=t;side="lower" if pos==0 else "upper";break
                prob=p**sum(bits)*(1-p)**(6-sum(bits))
                expected.append(dict(zip(FIELDS,map(str,(
                    wid,upper,upper//2,p,"".join(map(str,bits)),sum(bits),
                    6-sum(bits),prob,"" if t_hit is None else t_hit,side,
                    str(t_hit is None).lower())))))
            wid+=1
    assert rows==expected,"R320_SOURCE_PATH_RECONSTRUCTION_MISMATCH"
    witness=obj["worlds"][1]
    assert witness["survival"]=="1/8" and witness["hit_total"]=="7/8"
    assert sum(Fraction(c["lower"]) for c in witness["hit_by_time_and_side"])==Fraction(7,16)
    assert sum(Fraction(c["upper"]) for c in witness["hit_by_time_and_side"])==Fraction(7,16)
    print("PASS R320 independent interior DP and 384 exact artificial paths; E2=0 E3=0")

if __name__=="__main__":
    audit()
