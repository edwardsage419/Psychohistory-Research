#!/usr/bin/env python3
"""Independent nonblind binomial oracle for R288 S84. Standard library only.
CLI: python b_r288_s84_independent_binomial_20261030.py [RESULT_JSON]
"""
import copy
import json
import math
import sys
from fractions import Fraction

REFERENCES = (-2, 0, 2)
LOSSES = (1, 2, 3)

def value(x, r, loss):
    d = x-r
    return d if d >= 0 else loss*d

def oracle():
    result = []
    for r in REFERENCES:
        for loss in LOSSES:
            sure = value(0, r, loss)
            high = value(3, r, loss)-sure
            low = value(-2, r, loss)-sure
            population = Fraction(high+low, 2)
            if not population:
                raise AssertionError("population tie")
            counts = dict(correct=0, wrong=0, tie=0)
            for k in range(7):
                total = k*high+(6-k)*low
                weight = math.comb(6, k)
                if total == 0:
                    counts["tie"] += weight
                elif (total > 0) == (population > 0):
                    counts["correct"] += weight
                else:
                    counts["wrong"] += weight
            assert sum(counts.values()) == 64
            result.append(dict(reference=r, loss_multiplier=loss,
                population_difference=str(population), **counts,
                p_correct=str(Fraction(counts["correct"],64)),
                p_wrong=str(Fraction(counts["wrong"],64)),
                p_tie=str(Fraction(counts["tie"],64)),
                p_wrong_given_non_tie=str(Fraction(counts["wrong"],64-counts["tie"]))))
    return result

def verify_receipt(receipt):
    if receipt.get("research_id") != "R288" or receipt.get("substudy") != "S84":
        raise ValueError("identity")
    if receipt.get("evidence") != "E1_ONLY" or receipt.get("new_E2") != 0 or receipt.get("new_E3") != 0:
        raise ValueError("evidence grade")
    if receipt.get("R073") != "FROZEN" or receipt.get("PESEN_v0_1") != "FROZEN":
        raise ValueError("freeze")
    if receipt.get("source_atoms") != 576:
        raise ValueError("coverage")
    actual = receipt.get("results")
    if not isinstance(actual,list) or len(actual) != 9:
        raise ValueError("world count")
    keys = [(x.get("reference"),x.get("loss_multiplier")) for x in actual]
    if len(set(keys)) != 9 or actual != oracle():
        raise ValueError("independent binomial mismatch")
    return True

def negative_controls(receipt):
    mutations = []
    tests = [
        ("duplicate",lambda x:x["results"].__setitem__(1,x["results"][0])),
        ("missing",lambda x:x["results"].pop()),
        ("wrong_count",lambda x:x["results"][0].__setitem__("wrong",23)),
        ("wrong_probability",lambda x:x["results"][0].__setitem__("p_wrong","1/2")),
        ("evidence_upgrade",lambda x:x.__setitem__("evidence","E2")),
        ("freeze_upgrade",lambda x:x.__setitem__("R073","UNFROZEN")),
    ]
    for name,mutate in tests:
        z=copy.deepcopy(receipt)
        mutate(z)
        try:
            verify_receipt(z)
        except (ValueError,AssertionError,KeyError):
            mutations.append(name)
        else:
            raise AssertionError("mutant accepted: "+name)
    return mutations

if __name__ == "__main__":
    if len(sys.argv)>2:
        raise SystemExit("usage: SCRIPT [RESULT_JSON]")
    receipt = dict(research_id="R288",substudy="S84",evidence="E1_ONLY",
        source_atoms=576,new_E2=0,new_E3=0,R073="FROZEN",PESEN_v0_1="FROZEN",results=oracle())
    if len(sys.argv)==2:
        with open(sys.argv[1],encoding="utf8") as f:
            receipt=json.load(f)
    verify_receipt(receipt)
    rejected=negative_controls(receipt)
    print(json.dumps(dict(worlds=len(oracle()),binomial_cells=63,results=oracle(),
        mutations_rejected=rejected),indent=2,ensure_ascii=False))
