#!/usr/bin/env python3
"""Independent R324 no-import reconstruction of 64 artificial source states."""
import csv
import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"R324"
CSV=ROOT/"R324_ALL_64_ARTIFICIAL_RISK_STATES.csv"
RESULT=ROOT/"R324_EXACT_FOUR_SCORING_WORLDS.json"
FIELDS=["world_id","policy","dread1","dread2","unknown1","unknown2","weight","D","U","score"]
WORLDS=[("dread_weighted",3,1),("unknown_weighted",1,3),("balanced",1,1),("scaled_balanced",2,2)]
expected=[]
expected_worlds=[]
for world_id,(name,a,b) in enumerate(WORLDS):
    vals=[]
    for s in itertools.product((0,1),repeat=4):
        dread=sum(s[:2]); unknown=sum(s[2:])
        score=a*dread+b*unknown
        vals.append(score)
        expected.append(dict(zip(FIELDS,map(str,(world_id,name,*s,Fraction(1,16),dread,unknown,score)))))
    expected_worlds.append({"world_id":world_id,"policy":name,"a":a,"b":b,
        "state_count":16,"total_weight":"1","min_score":min(vals),"max_score":max(vals),
        "mean_score":str(Fraction(sum(vals),16)),"dread_only_score":2*a,"unknown_only_score":2*b})
with CSV.open(newline="",encoding="utf-8") as stream:
    reader=csv.DictReader(stream)
    assert reader.fieldnames==FIELDS,"unexpected CSV columns"
    observed=list(reader)
assert observed==expected,"independent state-by-state CSV mismatch"
assert len(observed)==64
assert all(sum(Fraction(r["weight"]) for r in observed if r["world_id"]==str(i))==1 for i in range(4))
obj=json.loads(RESULT.read_text(encoding="utf-8"))
assert obj["schema"]=="r324_constructed_two_axis_psychometric_risk_e1_v1"
assert obj["original_catalogue_id"]=="01-017"
assert obj["artificial_only"] is True
assert obj["original_source_rows"]==64
assert obj["worlds"]==expected_worlds,"independent world summary mismatch"
w=obj["witness"]
assert w=={"dread_only":"1100","unknown_only":"0011","w0_dread_gt_unknown":True,
    "w1_unknown_gt_dread":True,"w2_equal":True,"w3_double_w2_all_states":True}
assert expected_worlds[0]["dread_only_score"]==6 and expected_worlds[0]["unknown_only_score"]==2
assert expected_worlds[1]["dread_only_score"]==2 and expected_worlds[1]["unknown_only_score"]==6
print("R324_INDEPENDENT_NO_IMPORT_PASS",len(observed),"rows",len(expected_worlds),"worlds")
