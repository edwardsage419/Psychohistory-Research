#!/usr/bin/env python3
"""Independent R319 audit. Does not import R319 implementation."""
import csv
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]/"R319"
SETS=((0,1),(0,1,2),(0,1,1),(0,2,1),(0,2,2))
QS=(Fraction(1,4),Fraction(1,2),Fraction(3,4))
FIELDS=("world_id","choice_set_id","features","q_plus","beta","alternative_index",
        "feature_x","conditional_probability","mixing_mass","weighted_contribution","mixed_probability")

def audit():
    with (BASE/"R319_ALL_84_ORIGINAL_CONDITIONAL_MIXTURE_SOURCE_ATOMS.csv").open(
        encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        assert tuple(reader.fieldnames)==FIELDS
        rows=list(reader)
    results=json.loads((BASE/"R319_EXACT_15_MIXED_LOGIT_WORLDS.json").read_text(encoding="utf-8"))
    assert len(rows)==84 and len(results["worlds"])==15
    assert results["original_source_atoms"]==84 and results["marginal_alternative_probabilities"]==42
    assert results["original_catalogue_id"]=="01-007" and results["synthetic_only"] is True
    expected=[]
    world_id=0
    for s,features in enumerate(SETS):
        for q in QS:
            parts={}
            for beta in (-1,1):
                # Independent integer-power reconstruction; no R319 import.
                powers=([2**x for x in features] if beta==1
                        else [2**(max(features)-x) for x in features])
                den=sum(powers)
                parts[beta]=[Fraction(z,den) for z in powers]
            mixed=[q*parts[1][j]+(1-q)*parts[-1][j] for j in range(len(features))]
            w=results["worlds"][world_id]
            assert w=={"world_id":world_id,"choice_set_id":f"S{s}",
                       "features":list(features),"q_plus":str(q),
                       "marginal_probabilities":[str(p) for p in mixed]}
            assert sum(mixed)==1
            for beta in (-1,1):
                mass=q if beta==1 else 1-q
                for j,x in enumerate(features):
                    p=parts[beta][j]
                    expected.append(dict(zip(FIELDS,map(str,(
                        world_id,f"S{s}","|".join(map(str,features)),q,beta,j,x,
                        p,mass,p*mass,mixed[j])))))
            world_id+=1
    assert rows==expected, "R319_INDEPENDENT_SOURCE_RECONSTRUCTION_FAILED"
    binary=tuple(Fraction(v) for v in results["worlds"][1]["marginal_probabilities"])
    triple=tuple(Fraction(v) for v in results["worlds"][4]["marginal_probabilities"])
    assert binary==(Fraction(1,2),Fraction(1,2))
    assert triple==(Fraction(5,14),Fraction(2,7),Fraction(5,14))
    assert binary[0]/binary[1]==1 and triple[0]/triple[1]==Fraction(5,4)
    return {"status":"PASS_INDEPENDENT_FINITE_E1_SOURCE_AUDIT",
            "source_atoms":len(rows),"choice_worlds":world_id,
            "marginal_probabilities":42,"real_human_E2":0,"historical_E3":0}

if __name__=="__main__":
    print(json.dumps(audit(),sort_keys=True))
