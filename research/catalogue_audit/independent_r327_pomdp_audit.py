#!/usr/bin/env python3
"""R327 independent contingent-policy enumeration; never imports production code."""
import csv
import json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"R327"


def audit(rows,result):
    if len(rows)!=72 or len(result["worlds"])!=18:
        raise AssertionError("size")
    expected=[]
    worlds=[]
    for q in (F(1,2),F(3,4)):
        for k in range(9):
            b=F(k,8)
            p={}
            for h in (0,1):
                for y in (0,1):
                    p[h,y]=(b if h else 1-b)*(q if h==y else 1-q)
            if sum(p.values())!=1:
                raise AssertionError("mass")
            immediate=max(b,1-b)
            # Enumerate all four terminal contingent policies after sensing.
            sense=max(sum(p[h,y] for h in (0,1) for y in (0,1)
                          if h==(g0 if y==0 else g1))-F(1,8)
                      for g0 in (0,1) for g1 in (0,1))
            action="SENSE" if sense>immediate else ("GUESS_1" if b>F(1,2) else "GUESS_0")
            world=dict(belief=str(b),accuracy=str(q),immediate_value=str(immediate),
                       sense_value=str(sense),optimal_value=str(max(sense,immediate)),
                       chosen_action=action)
            worlds.append(world)
            for h in (0,1):
                for y in (0,1):
                    p0,p1=p[0,y],p[1,y]
                    obs=p0+p1
                    expected.append(dict(
                        belief=str(b),accuracy=str(q),hidden=str(h),observation=str(y),
                        joint_mass=str(p[h,y]),observation_mass=str(obs),
                        posterior_h1=str(p1/obs) if obs else "NULL",
                        terminal_guess=("1" if p1>p0 else "0") if obs else "NULL",
                        terminal_expected_reward=str(max(p0,p1)/obs) if obs else "NULL",
                        sense_value=world["sense_value"],immediate_value=world["immediate_value"],
                        optimal_value=world["optimal_value"],chosen_action=world["chosen_action"]))
    if expected!=rows or worlds!=result["worlds"]:
        raise AssertionError("exact independent source mismatch")
    if (result["source_row_count"],result["world_count"],result["model"])!=(72,18,"R327_FINITE_TWO_STATE_ONE_SENSE_POMDP_E1"):
        raise AssertionError("metadata")
    return True


def main():
    with (ROOT/"R327_ALL_72_ARTIFICIAL_HIDDEN_OBSERVATION_PATHS.csv").open(newline="") as f:
        rows=list(csv.DictReader(f))
    result=json.loads((ROOT/"R327_EXACT_18_BELIEF_WORLDS.json").read_text())
    audit(rows,result)
    tampered=[dict(x) for x in rows]
    tampered[0]["joint_mass"]="999"
    try:
        audit(tampered,result)
    except AssertionError:
        pass
    else:
        raise AssertionError("tampering undetected")
    print("PASS independent no-import audit: 72 rows, 18 worlds, 4 contingent policies, tamper rejected")


if __name__=="__main__":
    main()
