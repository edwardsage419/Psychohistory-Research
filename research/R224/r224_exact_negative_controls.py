#!/usr/bin/env python3
"""R224 exact negative control diagnostics on eight artificial SCMs.

Original protocol freezes eight worlds and four 4-valued exogenous sources.
Observational estimator only sees A,Z,W,Y and source weights. Oracle do(A)
and do(Z) are evaluated separately on complete artificial structural types.

Usage:
  python research/R224/r224_exact_negative_controls.py --test
  python research/R224/r224_exact_negative_controls.py --emit
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import unittest
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ZERO=F(0)
ONE=F(1)
Q=F(1,4)
WORLD_NAMES=(
    "RANDOMIZED_WITH_Z_SIGNAL",
    "HIDDEN_CONFOUNDED_NULL",
    "HIDDEN_CONFOUNDED_CAUSAL",
    "INSENSITIVE_VALID_CONTROLS",
    "INVALID_OUTCOME_DIRECT_A",
    "INVALID_EXPOSURE_DIRECT_Z",
    "CANCELLED_INVALID_OUTCOME",
    "MISMATCHED_VALID_OUTCOME",
)
FREEZE_COMMIT="0e6be85718a91939ee03e2be6bda0c344b903389"

def pa(world,u):
    if world not in WORLD_NAMES or u not in (0,1): raise ValueError("unfrozen world/U")
    return (1,3)[u] if world in (
        "HIDDEN_CONFOUNDED_NULL","HIDDEN_CONFOUNDED_CAUSAL",
        "INSENSITIVE_VALID_CONTROLS","CANCELLED_INVALID_OUTCOME",
        "MISMATCHED_VALID_OUTCOME") else 2

def pz(world,u):
    if world not in WORLD_NAMES or u not in (0,1): raise ValueError("unfrozen world/U")
    if world in ("INSENSITIVE_VALID_CONTROLS","INVALID_OUTCOME_DIRECT_A",
                 "INVALID_EXPOSURE_DIRECT_Z","CANCELLED_INVALID_OUTCOME"): return 2
    return (1,3)[u]

def cw(world,a,u):
    if world not in WORLD_NAMES or a not in (0,1) or u not in (0,1):
        raise ValueError("invalid frozen output control mechanism")
    if world=="INVALID_OUTCOME_DIRECT_A": return (1,3)[a]
    if world=="CANCELLED_INVALID_OUTCOME":
        return ((1,3),(0,2))[a][u]
    if world=="INSENSITIVE_VALID_CONTROLS" or world=="INVALID_EXPOSURE_DIRECT_Z":
        return 2
    if world=="MISMATCHED_VALID_OUTCOME": return (1,2)[u]
    return (1,3)[u]

def cy(world,a,u,z):
    if world not in WORLD_NAMES or a not in (0,1) or u not in (0,1) or z not in (0,1):
        raise ValueError("invalid frozen outcome mechanism")
    if world=="HIDDEN_CONFOUNDED_CAUSAL":
        return ((0,2),(1,3))[a][u]
    if world=="INVALID_EXPOSURE_DIRECT_Z":
        return (1,3)[z]
    return (1,3)[u]

def state(world,u,va,vz,vw,vy):
    if world not in WORLD_NAMES or u not in (0,1) or any(
            v not in range(4) for v in (va,vz,vw,vy)):
        raise ValueError("source outside frozen support")
    a=int(va<pa(world,u))
    z=int(vz<pz(world,u))
    w=int(vw<cw(world,a,u))
    y=int(vy<cy(world,a,u,z))
    return {
        "world":world,"oracle_U":u,
        "original_V_A":va,"original_V_Z":vz,"original_V_W":vw,"original_V_Y":vy,
        "observed_A":a,"observed_Z":z,"observed_W":w,"observed_Y":y,
        "true_original_probability":F(1,512),
        "oracle_W_doA0":int(vw<cw(world,0,u)),
        "oracle_W_doA1":int(vw<cw(world,1,u)),
        "oracle_Y_doA0":int(vy<cy(world,0,u,z)),
        "oracle_Y_doA1":int(vy<cy(world,1,u,z)),
        "oracle_Y_doZ0":int(vy<cy(world,a,u,0)),
        "oracle_Y_doZ1":int(vy<cy(world,a,u,1)),
    }

def sources(world):
    if world not in WORLD_NAMES: raise ValueError("unknown world")
    rows=tuple(state(world,u,*vals) for u in (0,1)
               for vals in itertools.product(range(4),repeat=4))
    assert len(rows)==512
    assert sum((r["true_original_probability"] for r in rows),ZERO)==ONE
    return rows

def joint_observed(rows):
    joint=defaultdict(F)
    for r in rows:
        joint[tuple(r[f"observed_{k}"] for k in ("A","Z","W","Y"))] += r["true_original_probability"]
    if sum(joint.values(),ZERO)!=ONE: raise AssertionError("mass lost")
    return {str(k):v for k,v in sorted(joint.items())}

def conditional_observed_difference(rows,exposure,outcome):
    if exposure not in ("A","Z") or outcome not in ("Y","W"):
        raise ValueError("invalid requested observed control comparison")
    # Only observed measurements and original frequencies, never latent U / oracle.
    numerator=defaultdict(F)
    denominator=defaultdict(F)
    for r in rows:
        x=r["observed_"+exposure]
        p=r["true_original_probability"]
        denominator[x]+=p
        numerator[x]+=p*r["observed_"+outcome]
    if denominator[0]==0 or denominator[1]==0: raise AssertionError("binary support missing")
    return numerator[1]/denominator[1]-numerator[0]/denominator[0]

def oracle_intervention_difference(rows,key0,key1):
    # Each complete exogenous source has both nested potential outcomes.
    return sum((r["true_original_probability"]*(r[key1]-r[key0]) for r in rows),ZERO)

def conditional_analytic(world, exposure, outcome):
    # Analytic independent route: integrates original threshold probabilities
    # by fixed U, without iterating or reading complete source rows.
    if exposure not in ("A","Z") or outcome not in ("Y","W"):
        raise ValueError("unsupported comparison")
    numer={0:ZERO,1:ZERO}
    den={0:ZERO,1:ZERO}
    for u in (0,1):
        pA=F(pa(world,u),4)
        pZ=F(pz(world,u),4)
        for a in (0,1):
            probA=pA if a else ONE-pA
            for z in (0,1):
                probZ=pZ if z else ONE-pZ
                p=F(1,2)*probA*probZ
                level=a if exposure=="A" else z
                den[level]+=p
                outcome_prob=(F(cw(world,a,u),4) if outcome=="W"
                              else F(cy(world,a,u,z),4))
                numer[level]+=p*outcome_prob
    if den[0]<=0 or den[1]<=0: raise AssertionError("missing analytic support")
    return numer[1]/den[1]-numer[0]/den[0]

def analytic_causal_effect(world, manipulated, outcome):
    if manipulated=="A" and outcome=="Y":
        return sum((F(1,2)*F(pz(world,u),4)*F(cy(world,1,u,1)-cy(world,0,u,1),4)
                 +F(1,2)*(1-F(pz(world,u),4))*F(cy(world,1,u,0)-cy(world,0,u,0),4)
                    for u in (0,1)),ZERO)
    if manipulated=="A" and outcome=="W":
        return sum((F(1,2)*F(cw(world,1,u)-cw(world,0,u),4) for u in (0,1)),ZERO)
    if manipulated=="Z" and outcome=="Y":
        return sum((F(1,2)*(
            F(pa(world,u),4)*F(cy(world,1,u,1)-cy(world,1,u,0),4)
            +(1-F(pa(world,u),4))*F(cy(world,0,u,1)-cy(world,0,u,0),4))
                    for u in (0,1)),ZERO)
    raise ValueError("unfrozen intervention")

def summary(world):
    rows=sources(world)
    observed={}
    for x,y in (("A","Y"),("A","W"),("Z","Y"),("Z","W")):
        s=conditional_observed_difference(rows,x,y)
        independently=conditional_analytic(world,x,y)
        if s!=independently: raise AssertionError("two independent observable routes differ")
        observed[f"D_{x}{y}"]=s
    oracle={}
    for x,y,k0,k1 in (
        ("A","Y","oracle_Y_doA0","oracle_Y_doA1"),
        ("A","W","oracle_W_doA0","oracle_W_doA1"),
        ("Z","Y","oracle_Y_doZ0","oracle_Y_doZ1")
    ):
        real=oracle_intervention_difference(rows,k0,k1)
        independently=analytic_causal_effect(world,x,y)
        if real!=independently: raise AssertionError("two independent oracle routes differ")
        oracle[f"true_do{x}_effect_on_{y}"]=real
    naive=observed["D_AY"]-observed["D_AW"]
    return {
        "world":world,
        "complete_original_source_atoms":len(rows),
        "full_source_probability_sum":"1",
        "observational_marginal_associations":{k:str(v) for k,v in observed.items()},
        "true_potential_outcome_oracles":{k:str(v) for k,v in oracle.items()},
        "naive_unjustified_subtract_D_AW_from_D_AY":str(naive),
        "naive_adjustment_bias_against_true_ATE":str(naive-oracle["true_doA_effect_on_Y"]),
        "negative_control_outcome_exclusion_valid":oracle["true_doA_effect_on_W"]==0,
        "negative_control_exposure_exclusion_valid":oracle["true_doZ_effect_on_Y"]==0,
        "associated_control_signal_AW_nonzero":observed["D_AW"]!=0,
        "associated_control_signal_ZY_nonzero":observed["D_ZY"]!=0,
    }

def generate():
    data={
        "research_id":"R224","catalogue_id":"09-015",
        "scientific_scope":"E1_FINITE_ARTIFICIAL_EXOGENOUS_SOURCE_ONLY",
        "frozen_protocol_commit":FREEZE_COMMIT,
        "worlds_count":8,"original_full_source_atoms":4096,
        "source_atoms_per_world":512,
        "true_R073_state":"FROZEN","true_PESEN_v0_1_state":"FROZEN",
        "new_human_E2":0,"new_historical_E3":0,
        "world_results":[summary(w) for w in WORLD_NAMES],
    }
    a=HERE/"R224_ALL_4096_ORIGINAL_NEGATIVE_CONTROL_SOURCE_ATOMS.csv"
    fieldnames=list(state(WORLD_NAMES[0],0,0,0,0,0))
    with a.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fieldnames,lineterminator="\n")
        writer.writeheader()
        for world in WORLD_NAMES:
            for r in sources(world):
                writer.writerow({key:str(value) for key,value in r.items()})
    b=HERE/"R224_EXACT_RESULTS.json"
    b.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt={
        "research_id":"R224","catalogue_id":"09-015",
        "full_original_source_atoms":4096,"worlds":8,
        "two_independent_observational_and_oracle_routes":True,
        "zero_new_real_E2":True,"zero_new_real_E3":True,
        "source_sha256":hashlib.sha256(a.read_bytes()).hexdigest(),
        "results_sha256":hashlib.sha256(b.read_bytes()).hexdigest(),
    }
    (HERE/"R224_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_eight_worlds(self):
        self.assertEqual(len(WORLD_NAMES),8)
    def test_total_source_count(self):
        self.assertEqual(sum(len(sources(w)) for w in WORLD_NAMES),4096)
    def test_no_direct_outcome_exclusion_in_invalid_W(self):
        self.assertEqual(summary("INVALID_OUTCOME_DIRECT_A")["true_potential_outcome_oracles"]["true_doA_effect_on_W"],"1/2")
    def test_no_direct_exposure_exclusion_in_invalid_Z(self):
        self.assertEqual(summary("INVALID_EXPOSURE_DIRECT_Z")["true_potential_outcome_oracles"]["true_doZ_effect_on_Y"],"1/2")
    def test_valid_insensitive_controls(self):
        s=summary("INSENSITIVE_VALID_CONTROLS")
        self.assertEqual(s["observational_marginal_associations"]["D_AY"],"1/4")
        self.assertEqual(s["observational_marginal_associations"]["D_AW"],"0")
        self.assertEqual(s["observational_marginal_associations"]["D_ZY"],"0")
        self.assertTrue(s["negative_control_outcome_exclusion_valid"])
        self.assertTrue(s["negative_control_exposure_exclusion_valid"])
    def test_random_A_and_Z_signal(self):
        s=summary("RANDOMIZED_WITH_Z_SIGNAL")
        self.assertEqual(s["observational_marginal_associations"]["D_AY"],"0")
        self.assertEqual(s["observational_marginal_associations"]["D_ZY"],"1/4")
    def test_confounding_null(self):
        s=summary("HIDDEN_CONFOUNDED_NULL")
        self.assertEqual(s["observational_marginal_associations"]["D_AY"],"1/4")
        self.assertEqual(s["observational_marginal_associations"]["D_AW"],"1/4")
        self.assertEqual(s["true_potential_outcome_oracles"]["true_doA_effect_on_Y"],"0")
    def test_confounding_causal(self):
        s=summary("HIDDEN_CONFOUNDED_CAUSAL")
        self.assertEqual(s["observational_marginal_associations"]["D_AY"],"1/2")
        self.assertEqual(s["true_potential_outcome_oracles"]["true_doA_effect_on_Y"],"1/4")
    def test_cancellation(self):
        s=summary("CANCELLED_INVALID_OUTCOME")
        self.assertEqual(s["observational_marginal_associations"]["D_AW"],"0")
        self.assertEqual(s["true_potential_outcome_oracles"]["true_doA_effect_on_W"],"-1/4")
    def test_mismatched_calibration(self):
        s=summary("MISMATCHED_VALID_OUTCOME")
        self.assertEqual(s["observational_marginal_associations"]["D_AW"],"1/8")
        self.assertEqual(s["naive_unjustified_subtract_D_AW_from_D_AY"],"1/8")
        self.assertEqual(s["true_potential_outcome_oracles"]["true_doA_effect_on_Y"],"0")
    def test_unknown_world_rejected(self):
        with self.assertRaises(ValueError): sources("UNKNOWN")
    def test_bad_input_rejected(self):
        with self.assertRaises(ValueError): state(WORLD_NAMES[0],0,4,0,0,0)

def _case(world,kind):
    def test(self):
        rows=sources(world)
        if kind=="mass":
            self.assertEqual(sum((r["true_original_probability"] for r in rows),ZERO),ONE)
        elif kind=="binary":
            self.assertTrue(all(r["observed_"+v] in (0,1) for r in rows for v in ("A","Z","W","Y")))
        elif kind=="original_source_uniqueness":
            self.assertEqual(len({(r["oracle_U"],r["original_V_A"],r["original_V_Z"],
                                   r["original_V_W"],r["original_V_Y"]) for r in rows}),512)
        elif kind=="observed_routes":
            for x,y in (("A","Y"),("A","W"),("Z","Y"),("Z","W")):
                self.assertEqual(conditional_observed_difference(rows,x,y),conditional_analytic(world,x,y))
        elif kind=="oracle_routes":
            for x,y,k0,k1 in (
                ("A","Y","oracle_Y_doA0","oracle_Y_doA1"),
                ("A","W","oracle_W_doA0","oracle_W_doA1"),
                ("Z","Y","oracle_Y_doZ0","oracle_Y_doZ1")
            ):
                self.assertEqual(oracle_intervention_difference(rows,k0,k1),
                                 analytic_causal_effect(world,x,y))
        elif kind=="source_truth":
            self.assertTrue(all(r["observed_W"]==(
                r["oracle_W_doA1"] if r["observed_A"] else r["oracle_W_doA0"]) and
                r["observed_Y"]==(r["oracle_Y_doA1"] if r["observed_A"] else r["oracle_Y_doA0"])
                for r in rows))
        else: raise AssertionError("invalid test")
    return test

for world in WORLD_NAMES:
    for kind in ("mass","binary","original_source_uniqueness","observed_routes",
                 "oracle_routes","source_truth"):
        setattr(Tests,"test_"+world.lower()+"_"+kind,_case(world,kind))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    options=parser.parse_args()
    if options.test:
        unittest.main(argv=["r224"],verbosity=2)
    else:
        print(json.dumps(generate(),ensure_ascii=False,indent=2))
