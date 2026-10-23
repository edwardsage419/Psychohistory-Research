#!/usr/bin/env python3
"""Independent R316 verifier: no main module import, grouped combinatorics checks."""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"R316"
CSV=D/"R316_ALL_768_ORIGINAL_GRAPH_DYAD_PROBABILITY_ATOMS.csv"
OUT=D/"R316_EXACT_128_GRAPH_LIKELIHOODS.json"
PAIRS=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
GROUP=(0,0,1,1)
REGIMES=(("A",Fraction(3,4),Fraction(1,4)),("D",Fraction(1,4),Fraction(3,4)))
def audit():
    with CSV.open(encoding="utf-8",newline="") as f:rows=list(csv.DictReader(f))
    out=json.loads(OUT.read_text(encoding="utf-8"))
    assert len(rows)==768 and out["source_atom_count"]==768
    assert out["graph_count"]==128 and out["fixed_blocks"]==list(GROUP)
    assert out["dyads"]==[list(x) for x in PAIRS]
    assert len(out["regimes"])==2
    likelihood_sequences=[]
    for regime_index,(name,p_within,p_cross) in enumerate(REGIMES):
        reported=out["regimes"][regime_index]
        assert reported["regime"]==name
        assert reported["within_p"]==str(p_within) and reported["cross_p"]==str(p_cross)
        assert reported["expected_within_edges"]==str(2*p_within)
        assert reported["expected_cross_edges"]==str(4*p_cross)
        assert reported["expected_total_edges"]==str(2*p_within+4*p_cross)
        probs=[]
        empirical_expected_within=Fraction(0)
        empirical_expected_cross=Fraction(0)
        for mask in range(64):
            bitstring=f"{mask:06b}"
            selected=[int(c) for c in bitstring]
            factors=[]
            for i,(u,v) in enumerate(PAIRS):
                same=int(GROUP[u]==GROUP[v])
                p=p_within if same else p_cross
                factor=p if selected[i] else (Fraction(1)-p)
                factors.append(factor)
            chance=Fraction(1)
            for f in factors: chance*=f
            row=reported["complete_graphs"][mask]
            expected={"mask":mask,"edge_vector":bitstring,"within_edges":selected[0]+selected[5],
                      "cross_edges":sum(selected[1:5]),"probability":str(chance)}
            assert row==expected
            probs.append(chance)
            empirical_expected_within+=chance*expected["within_edges"]
            empirical_expected_cross+=chance*expected["cross_edges"]
            for i,(u,v) in enumerate(PAIRS):
                src=rows[regime_index*64*6+mask*6+i]
                p=p_within if GROUP[u]==GROUP[v] else p_cross
                expected_src=[name,mask,bitstring,i,u,v,int(GROUP[u]==GROUP[v]),selected[i],
                              str(p),str(factors[i]),str(chance)]
                if tuple(src.values())!=tuple(map(str,expected_src)):
                    raise AssertionError(f"source atom differs {name=} {mask=} {i=}")
        assert sum(probs)==1
        assert empirical_expected_within==2*p_within
        assert empirical_expected_cross==4*p_cross
        # Completely independent combinatorial multinomial reduction by two block classes.
        grouped_mass=sum(
            comb(2,a)*comb(4,b)*p_within**a*(1-p_within)**(2-a)*p_cross**b*(1-p_cross)**(4-b)
            for a in range(3) for b in range(5)
        )
        assert grouped_mass==1
        likelihood_sequences.append(probs)
    TV=sum(abs(a-b) for a,b in zip(*likelihood_sequences))/2
    assert TV==Fraction(203,256)
    assert out["total_variation_A_D"]==str(TV)
    within_only_A=likelihood_sequences[0][33]
    within_only_D=likelihood_sequences[1][33]
    assert within_only_A==Fraction(729,4096)
    assert within_only_D==Fraction(1,4096)
    assert within_only_A/within_only_D==729
    assert Counter(x["regime"] for x in rows)=={"A":384,"D":384}
    assert len({(x["regime"],x["mask"],x["dyad_index"]) for x in rows})==768
    return {"result":"PASS","atoms":768,"graphs":128,"total_variation":str(TV),"within_only_BF":729,"human_E2":0,"history_E3":0}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--audit",action="store_true");p.add_argument("--test",action="store_true")
    p.parse_args()
    print(json.dumps(audit(),sort_keys=True))
