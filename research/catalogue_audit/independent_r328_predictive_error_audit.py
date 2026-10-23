#!/usr/bin/env python3
"""Independent closed-form R328 precision-weighted prediction error audit."""
import csv
import json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"R328"


def verify(rows,result):
    if len(rows)!=120 or len(result["worlds"])!=24:
        raise AssertionError("size")
    expected=[]
    worlds=[]
    for m in (F(0),F(1)):
        for y in (F(0),F(1),F(2)):
            for r in (F(1),F(2)):
                for p in (F(1),F(2)):
                    optimum=(r*m+p*y)/(r+p)
                    factor=1-F(r+p,4)
                    values=[optimum+(m-optimum)*factor**t for t in range(5)]
                    energies=[(r*(v-m)**2+p*(y-v)**2)/2 for v in values]
                    world=dict(prior=str(m),target=str(y),prior_precision=str(r),
                               sensory_precision=str(p),analytic_optimum=str(optimum),
                               estimate_step4=str(values[4]),energy_step0=str(energies[0]),
                               energy_step4=str(energies[4]),
                               monotone=all(energies[t+1]<=energies[t] for t in range(4)))
                    worlds.append(world)
                    for t,v in enumerate(values):
                        expected.append(dict(prior=str(m),target=str(y),prior_precision=str(r),
                                             sensory_precision=str(p),step=str(t),estimate=str(v),
                                             sensory_error=str(y-v),prior_error=str(m-v),
                                             energy=str(energies[t]),analytic_optimum=str(optimum)))
    if rows!=expected or result["worlds"]!=worlds:
        raise AssertionError("independent closed form mismatch")
    if (result["model"],result["source_row_count"],result["world_count"])!=("R328_FINITE_SCALAR_PREDICTIVE_ERROR_E1",120,24):
        raise AssertionError("metadata mismatch")
    if not all(w["monotone"] for w in worlds):
        raise AssertionError("energy increased")
    return True


def main():
    with (ROOT/"R328_ALL_120_ARTIFICIAL_PREDICTION_ERROR_STATES.csv").open(newline="") as f:
        rows=list(csv.DictReader(f))
    result=json.loads((ROOT/"R328_EXACT_24_PRECISION_WORLDS.json").read_text())
    verify(rows,result)
    changed=[dict(x) for x in rows]
    changed[0]["energy"]="999"
    try:
        verify(changed,result)
    except AssertionError:
        pass
    else:
        raise AssertionError("tamper missed")
    print("R328 INDEPENDENT NO-IMPORT CLOSED-FORM AUDIT PASS 120 rows 24 worlds tamper rejected")


if __name__=="__main__":
    main()
