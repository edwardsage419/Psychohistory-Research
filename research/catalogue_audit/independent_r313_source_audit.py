#!/usr/bin/env python3
"""R313 independent archive audit; intentionally does not import r313_exact_axelrod."""
from __future__ import annotations
import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "R313"
SRC = DIR / "R313_ALL_512_ORIGINAL_FEATURE_SOURCE_ATOMS.csv"
RESULT = DIR / "R313_EXACT_64_WORLD_ONE_STEP_RESULTS.json"

def independently_audit():
    rows=list(csv.DictReader(SRC.open(encoding="utf-8",newline="")))
    result=json.loads(RESULT.read_text(encoding="utf-8"))
    assert len(rows)==512 and len(result["worlds"])==64
    assert len({(r["world"],r["active"],r["neighbor"],r["feature"]) for r in rows}) == 512
    keys=["world","active","neighbor","feature","active_trait","neighbor_trait",
          "matches","differences","selection_weight","conditional_copy_probability",
          "unconditional_copy_probability","next_world"]
    assert rows and list(rows[0])==keys
    edges=((0,1),(1,0),(1,2),(2,1))
    positive=0
    absorbing=0
    for world in range(64):
        culture=[list(map(int,f"{world:06b}"[k:k+2])) for k in (0,2,4)]
        by_world=rows[8*world:8*(world+1)]
        target_mass=defaultdict(Fraction)
        target_mass[world]=Fraction(1)
        for pos,((actor,neighbor),feature) in enumerate(
            ( (edge,f) for edge in edges for f in (0,1))
        ):
            atom=by_world[pos]
            common=sum(x==y for x,y in zip(culture[actor],culture[neighbor]))
            differs=2-common
            chance=Fraction(common,2*differs) if differs and culture[actor][feature]!=culture[neighbor][feature] else Fraction(0)
            chosen=Fraction(1,3*len((1,) if actor!=1 else (0,2)))
            destination=[copy[:] for copy in culture]
            if chance: destination[actor][feature]=culture[neighbor][feature]
            next_world=int("".join(str(v) for pair in destination for v in pair),2)
            expected=(world,actor,neighbor,feature,culture[actor][feature],
                      culture[neighbor][feature],common,differs,str(chosen),
                      str(chance),str(chosen*chance),next_world)
            if tuple(atom.values())!=tuple(map(str,expected)):
                raise AssertionError(f"mismatched source atom: {world=} {actor=} {neighbor=} {feature=}")
            if chance:
                positive+=1
                target_mass[world]-=chosen*chance
                target_mass[next_world]+=chosen*chance
                assert sum(destination[actor][i]==destination[neighbor][i] for i in (0,1))==common+1
                assert destination[neighbor]==culture[neighbor]
        expected_dist=[{"world":k,"probability":str(p)} for k,p in sorted(target_mass.items()) if p]
        ref=result["worlds"][world]
        is_absorb=all(sum(culture[a][f]==culture[b][f] for f in (0,1)) in (0,2)
                      for a,b in ((0,1),(1,2)))
        absorbing+=is_absorb
        assert ref=={"world":world,"state":f"{world:06b}","absorbing":is_absorb,"next_world_probabilities":expected_dist}
        assert sum(target_mass.values())==1
        assert all(p>=0 for p in target_mass.values())
        if is_absorb: assert expected_dist==[{"world":world,"probability":"1"}]
    assert positive==128 and absorbing==16
    assert result["world_count"]==64 and result["directed_event_count"]==256
    assert result["potential_feature_source_count"]==512
    assert result["positive_copy_atom_count"]==128 and result["absorbing_world_count"]==16
    # An update at active middle node may make it less similar to its other neighbour.
    before=[[0,0],[0,0],[0,1]]
    after=[[0,0],[0,1],[0,1]]
    assert sum(x==y for x,y in zip(before[0],before[1]))==2
    assert sum(x==y for x,y in zip(after[0],after[1]))==1
    return {"source_atom_count":len(rows),"world_count":64,"positive_atom_count":positive,
            "absorbing_count":absorbing,"result":"PASS","empirical_subjects":0,"E2":0,"E3":0}

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--audit",action="store_true")
    parser.add_argument("--test",action="store_true")
    opts=parser.parse_args()
    print(json.dumps(independently_audit(),sort_keys=True))
