#!/usr/bin/env python3
"""R326 independent enumeration of global regimes and local theta assignments."""
import csv
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"R326"
CSV=ROOT/"R326_ALL_64_ARTIFICIAL_GROUP_HISTORIES.csv"
RESULT=ROOT/"R326_EXACT_HIERARCHICAL_PREDICTIONS.json"
FIELDS=["history_id","h11","h12","h21","h22","h31","h32","enumeration_weight",
    "posterior_global_high","hier_predict_g1","hier_predict_g2","hier_predict_g3",
    "independent_predict_g1","independent_predict_g2","independent_predict_g3"]
def posterior(h):
    groups=(h[:2],h[2:4],h[4:])
    masses=[]
    for z in (0,1):
        for ts in itertools.product((0,1),repeat=3):
            m=F(1,2)
            for g,t in enumerate(ts):
                theta=F(3,4) if t else F(1,4)
                wt=F(3,4) if z else F(1,4)
                m*=wt if t else 1-wt
                for bit in groups[g]:m*=theta if bit else 1-theta
            masses.append((z,ts,m))
    norm=sum([m for _,_,m in masses],F(0))
    pz=sum([m for z,_,m in masses if z==1],F(0))/norm
    pp=[]
    for g in range(3):
        pp.append(sum([m*(F(3,4) if ts[g] else F(1,4)) for _,ts,m in masses],F(0))/norm)
    flat=[]
    for obs in groups:
        likelihoods=[]
        for theta in (F(1,4),F(3,4)):
            x=F(1,2)
            for bit in obs:x*=theta if bit else 1-theta
            likelihoods.append(x)
        flat.append(sum([x*t for x,t in zip(likelihoods,(F(1,4),F(3,4)))],F(0))/sum(likelihoods))
    return pz,tuple(pp),tuple(flat)
expected=[];global_probs=[]
for i,h in enumerate(itertools.product((0,1),repeat=6)):
    p,v,f=posterior(h);global_probs.append(p)
    expected.append(dict(zip(FIELDS,map(str,(i,*h,F(1,64),p,*v,*f)))))
with CSV.open(newline="",encoding="utf-8") as stream:
    reader=csv.DictReader(stream)
    assert reader.fieldnames==FIELDS
    observed=list(reader)
assert observed==expected,"independent 64-history reconstruction mismatch"
assert sum([F(r["enumeration_weight"]) for r in observed],F(0))==1
hi=posterior((0,1,1,1,1,1));lo=posterior((0,1,0,0,0,0))
w={"high_other_groups":"011111","low_other_groups":"010000",
    "high_global_posterior":str(hi[0]),"low_global_posterior":str(lo[0]),
    "high_group1_hier_prediction":str(hi[1][0]),"low_group1_hier_prediction":str(lo[1][0]),
    "independent_group1_both":"1/2","strict_cross_group_borrowing":hi[1][0]>lo[1][0]}
symmetry=all(posterior(tuple(1-x for x in h))[0]==1-posterior(h)[0]
    and all(a==1-b for a,b in zip(posterior(tuple(1-x for x in h))[1],posterior(h)[1]))
    and all(a==1-b for a,b in zip(posterior(tuple(1-x for x in h))[2],posterior(h)[2]))
    for h in itertools.product((0,1),repeat=6))
permute=all(posterior(h[2:4]+h[:2]+h[4:])[0]==posterior(h)[0]
    and posterior(h[2:4]+h[:2]+h[4:])[1]==(posterior(h)[1][1],posterior(h)[1][0],posterior(h)[1][2])
    for h in itertools.product((0,1),repeat=6))
obj=json.loads(RESULT.read_text(encoding="utf-8"))
assert obj["schema"]=="r326_finite_hierarchical_bayes_three_group_e1_v1"
assert obj["original_catalogue_id"]=="02-007" and obj["artificial_only"] is True
assert obj["original_source_rows"]==64
assert obj["witness"]==w
assert obj["summary"]=={"history_count":64,"group_count":3,
    "min_global_posterior":str(min(global_probs)),"max_global_posterior":str(max(global_probs)),
    "distinct_global_posteriors":len(set(global_probs)),
    "complement_symmetry_verified":symmetry,"group_permutation_verified":permute}
assert symmetry and permute and w["strict_cross_group_borrowing"]
print("R326_INDEPENDENT_NO_IMPORT_PASS",len(observed),"histories",w)
