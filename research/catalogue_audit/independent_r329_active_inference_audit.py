#!/usr/bin/env python3
"""R329 independent source audit: no production module import."""
import csv
import io
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"R329"
CSV=ROOT/"R329_ALL_144_ARTIFICIAL_JOINT_ATOMS.csv"
RESULT=ROOT/"R329_EXACT_18_EFE_WORLDS.json"

def audit(csv_text,json_text):
    rows=list(csv.DictReader(io.StringIO(csv_text)))
    data=json.loads(json_text)
    assert len(rows)==144 and len(data["worlds"])==18
    assert data["source_row_count"]==144 and data["world_count"]==18
    cursor=0
    for b in (Fraction(1,4),Fraction(1,2),Fraction(3,4)):
        for c in (Fraction(1,2),Fraction(3,4)):
            for k in (Fraction(0),Fraction(1,8),Fraction(1,4)):
                world=data["worlds"][(cursor//8)]
                assert (world["belief"],world["preference_one"],world["precise_cost"])==(str(b),str(c),str(k))
                computed={}
                for policy in ("PRECISE","NOISY"):
                    a=Fraction(3,4) if policy=="PRECISE" else Fraction(1,2)
                    joint={(s,o):(b if s else 1-b)*(a if s==o else 1-a)
                           for s in (0,1) for o in (0,1)}
                    marg={o:joint[0,o]+joint[1,o] for o in (0,1)}
                    risk=sum(float(marg[o])*math.log(float(marg[o]/(c if o else 1-c)))
                             for o in (0,1))
                    ambiguity=sum(float((b if s else 1-b))*
                         (-float(a)*math.log(float(a))-float(1-a)*math.log(float(1-a)))
                         for s in (0,1))
                    g=risk+ambiguity+(float(k) if policy=="PRECISE" else 0)
                    info=sum(float(joint[s,o])*math.log(float((a if s==o else 1-a)/marg[o]))
                             for s in (0,1) for o in (0,1))
                    computed[policy]=(g,info)
                    for s in (0,1):
                        for o in (0,1):
                            row=rows[cursor]
                            expected={"belief":str(b),"preference_one":str(c),"precise_cost":str(k),
                                      "policy":policy,"hidden":str(s),"observation":str(o),
                                      "likelihood":str(a if s==o else 1-a),
                                      "joint_mass":str(joint[s,o]),"observation_mass":str(marg[o])}
                            for key,val in expected.items():
                                assert row[key]==val,(cursor,key,row[key],val)
                            assert abs(float(row["expected_free_energy"])-g)<5.1e-10
                            cursor+=1
                choice="PRECISE" if computed["PRECISE"][0]<computed["NOISY"][0]-1e-14 else "NOISY"
                assert world["chosen_policy"]==choice
                for row in rows[cursor-8:cursor]:
                    assert row["selected_policy"]==choice
                for policy,prefix in (("PRECISE","precise"),("NOISY","noisy")):
                    assert abs(float(world[prefix+"_efe"])-computed[policy][0])<5.1e-10
                    assert abs(float(world[prefix+"_information"])-computed[policy][1])<5.1e-10
                assert abs(float(world["identity_error"]))<1e-12
    assert cursor==len(rows)
    return True

def main():
    source=CSV.read_text()
    worlds=RESULT.read_text()
    audit(source,worlds)
    tampered=source.replace(",1/4,",",1/3,",1)
    assert tampered!=source
    rejected=False
    try: audit(tampered,worlds)
    except (AssertionError,ValueError): rejected=True
    assert rejected,"tamper rejection failed"
    print("R329 independent no-import audit PASS: 144 rows, 18 worlds, tamper rejected")

if __name__=="__main__":
    main()
