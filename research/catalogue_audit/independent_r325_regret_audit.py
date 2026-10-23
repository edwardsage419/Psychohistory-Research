#!/usr/bin/env python3
"""R325 independent no-import full 1029-state regret audit."""
import csv
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"R325"
CSV=ROOT/"R325_ALL_1029_ARTIFICIAL_REGRET_STATES.csv"
RESULT=ROOT/"R325_EXACT_THREE_REGRET_WORLDS.json"
FIELDS=["world_id","policy","kappa","d1","d2","d3","weight","eu_advantage","regret_advantage","choice"]
POLICIES=[("linear_eu",F(0)),("mild_cubic",F(1,4)),("strong_cubic",F(1))]
expected=[];worlds=[]
for wid,(name,k) in enumerate(POLICIES):
    ca=cb=ct=flips=0
    for ds in itertools.product(range(-3,4),repeat=3):
        eu=F(sum(ds),3)
        reg=sum([F(d)+k*F(d**3) for d in ds],F(0))/3
        choice="A" if reg>0 else "B" if reg<0 else "TIE"
        ca+=int(choice=="A");cb+=int(choice=="B");ct+=int(choice=="TIE")
        flips+=int(eu*reg<0)
        expected.append(dict(zip(FIELDS,map(str,(wid,name,k,*ds,F(1,343),eu,reg,choice)))))
    witness=sum([F(d)+k*F(d**3) for d in (3,-2,-2)],F(0))/3
    worlds.append({"world_id":wid,"policy":name,"kappa":str(k),"state_count":343,
        "total_weight":"1","choice_A":ca,"choice_B":cb,"choice_TIE":ct,
        "strict_eu_regret_reversals":flips,"witness_regret_advantage":str(witness)})
with CSV.open(newline="",encoding="utf-8") as stream:
    reader=csv.DictReader(stream)
    assert reader.fieldnames==FIELDS
    observed=list(reader)
assert observed==expected,"independent CSV reconstruction mismatch"
assert len(observed)==1029
assert all(sum(F(r["weight"]) for r in observed if r["world_id"]==str(i))==1 for i in range(3))
obj=json.loads(RESULT.read_text(encoding="utf-8"))
assert obj["schema"]=="r325_constructed_statewise_regret_cubic_e1_v1"
assert obj["original_catalogue_id"]=="01-020" and obj["artificial_only"] is True
assert obj["original_source_rows"]==1029
assert obj["worlds"]==worlds
w=obj["witness"]
assert w=={"difference_vector":[3,-2,-2],"eu_advantage":"-1/3",
    "linear_regret_advantage":"-1/3","mild_regret_advantage":"7/12",
    "strong_regret_advantage":"10/3","mild_strict_reversal":True,
    "strong_strict_reversal":True,"sign_symmetry_all":True}
assert worlds[0]["strict_eu_regret_reversals"]==0
assert worlds[1]["strict_eu_regret_reversals"]>0 and worlds[2]["strict_eu_regret_reversals"]>0
print("R325_INDEPENDENT_NO_IMPORT_PASS",len(observed),"artificial rows",[(x["choice_A"],x["choice_B"],x["choice_TIE"],x["strict_eu_regret_reversals"]) for x in worlds])
