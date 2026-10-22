#!/usr/bin/env python3
"""R213 exact binary encouragement instrumental-variable/LATE source audit.

Eight frozen artificial eight-latent-person populations, each with two
possible instrument assignments. Enumerate all 128 population-instrument
source atoms, conditional outcome and first stage, exact Wald ratio,
known principal stratum local treatment effects and four assumption failures.

This is a full finite probability source computation, not an 8-person RCT
or an empirical estimate on actual human subjects.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

F=Fraction
Z=F(0)
O=F(1)
N=8
WORLDS=("FULL_COMPLY","MONOTONE_MIX","WEAK_COMPLIERS",
        "NO_COMPLIERS","WITH_DEFIERS","EXCLUSION_VIOLATION",
        "WEAK_EXCLUSION","Z_CONFOUNDING")
COMPLIANCE={
    "COMPLIER":(0,1),
    "ALWAYS":(1,1),
    "NEVER":(0,0),
    "DEFIER":(1,0),
}
BASE=Path(__file__).resolve().parent


def build_population(world):
    if world not in WORLDS:
        raise ValueError("invalid artificial IV source")
    items=[]
    for i in range(N):
        if world=="FULL_COMPLY":
            typ="COMPLIER";base=i%3;tau=1+(i%4)
        elif world=="NO_COMPLIERS":
            typ="ALWAYS" if i<4 else "NEVER"
            base=i%2;tau=2
        elif world=="WITH_DEFIERS":
            typ="COMPLIER" if i<4 else ("DEFIER" if i<6 else "NEVER")
            base=i%2;tau=2 if i<4 else (4 if i<6 else 0)
        elif world in ("WEAK_COMPLIERS","WEAK_EXCLUSION"):
            typ="COMPLIER" if i==0 else ("ALWAYS" if i<=4 else "NEVER")
            base=i%2;tau=4 if i==0 else 0
        else:
            typ="COMPLIER" if i<4 else ("ALWAYS" if i<6 else "NEVER")
            base=(10 if i<4 else 0) if world=="Z_CONFOUNDING" else i%2
            tau=(2,2,4,4)[i] if i<4 else 0
        items.append((typ,F(base),F(tau)))
    return tuple(items)


def direct_instrument_effect(world):
    return O if world in ("EXCLUSION_VIOLATION","WEAK_EXCLUSION") else Z


def z_probability(world,i):
    if i not in range(N) or world not in WORLDS:
        raise ValueError("unrecognized artificial individual or world")
    if world=="Z_CONFOUNDING":
        return F(3,4) if i<4 else F(1,4)
    return F(1,2)


def d_potential(typ,z):
    if typ not in COMPLIANCE or z not in (0,1):
        raise ValueError("invalid compliance type or Z")
    return COMPLIANCE[typ][z]


def observed(world,i,z):
    if z not in (0,1) or i not in range(N):
        raise ValueError("invalid source atom")
    typ,y0,tau=build_population(world)[i]
    d=d_potential(typ,z)
    y=y0+tau*d+direct_instrument_effect(world)*z
    return d,y


def original_source_rows(world):
    pop=build_population(world)
    rows=[]
    for i,(typ,y0,tau) in enumerate(pop):
        q=z_probability(world,i)
        for z in (0,1):
            prob=F(1,N)*(q if z else O-q)
            d,y=observed(world,i,z)
            rows.append({
                "world":world,"latent_source_person_i":i,
                "principal_stratum_type":typ,
                "potential_D_if_Z0":d_potential(typ,0),
                "potential_D_if_Z1":d_potential(typ,1),
                "potential_Y_if_D0_without_direct_Z_exact":str(y0),
                "potential_Y_if_D1_without_direct_Z_exact":str(y0+tau),
                "source_unit_treatment_effect_exact":str(tau),
                "direct_outcome_effect_of_Z_exact":str(direct_instrument_effect(world)),
                "instrument_assignment_Z":z,
                "person_specific_instrument_propensity_exact":str(q),
                "joint_source_probability_exact":str(prob),
                "observed_actual_D":d,
                "observed_actual_Y_exact":str(y),
            })
    if len(rows)!=16 or sum((F(r["joint_source_probability_exact"]) for r in rows),Z)!=O:
        raise AssertionError("complete source count or probability mass invalid")
    return tuple(rows)


def conditional_mean(rows,z,key):
    p=sum((F(r["joint_source_probability_exact"]) for r in rows
           if r["instrument_assignment_Z"]==z),Z)
    if p<=0:
        raise ValueError("instrument arm not observed")
    numer=sum((F(r["joint_source_probability_exact"])*F(r[key])
               for r in rows if r["instrument_assignment_Z"]==z),Z)
    return numer/p


def population_ATE(world):
    return sum((r[2] for r in build_population(world)),Z)/N


def complier_LATE(world):
    comps=[tau for typ,y0,tau in build_population(world) if typ=="COMPLIER"]
    return sum(comps,Z)/len(comps) if comps else None


def reduced_form_identity(world):
    # This identity uses an INSTRUMENT INDEPENDENCE assumption; invalid on
    # Z_CONFOUNDING by construction.
    pop=build_population(world)
    fs=sum((F(d_potential(typ,1)-d_potential(typ,0))
            for typ,y0,tau in pop),Z)/N
    itt=sum((F(d_potential(typ,1)-d_potential(typ,0))*tau
             for typ,y0,tau in pop),Z)/N + direct_instrument_effect(world)
    return fs,itt


def source_world(world):
    pop=build_population(world)
    rows=original_source_rows(world)
    pz0=sum((F(r["joint_source_probability_exact"]) for r in rows
             if r["instrument_assignment_Z"]==0),Z)
    pz1=O-pz0
    d0=conditional_mean(rows,0,"observed_actual_D")
    d1=conditional_mean(rows,1,"observed_actual_D")
    y0=conditional_mean(rows,0,"observed_actual_Y_exact")
    y1=conditional_mean(rows,1,"observed_actual_Y_exact")
    fs=d1-d0
    ity=y1-y0
    wald=ity/fs if fs else None
    comps=sum(t=="COMPLIER" for t,base,tau in pop)
    defiers=sum(t=="DEFIER" for t,base,tau in pop)
    alw=sum(t=="ALWAYS" for t,base,tau in pop)
    never=sum(t=="NEVER" for t,base,tau in pop)
    independently_assigned=world!="Z_CONFOUNDING"
    exclusion_valid=direct_instrument_effect(world)==Z
    monotonic=defiers==0
    strong=abs(fs)>=F(1,2)
    structural_fs,structural_ity=reduced_form_identity(world)
    if independently_assigned and (fs,ity)!=(structural_fs,structural_ity):
        raise AssertionError("independent source probabilities disagree with principal strata")
    late=complier_LATE(world)
    all_assumptions_valid=independently_assigned and exclusion_valid and monotonic and fs!=0
    if all_assumptions_valid and wald!=late:
        raise AssertionError("valid IV Wald must match complier average treatment effect")
    if fs==0 and wald is not None:
        raise AssertionError("Wald has undefined denominator")
    result={
        "world":world,
        "complete_population_types":8,
        "complete_original_instrument_outcomes":16,
        "original_joint_source_probability_sum_exact":"1",
        "instrument_is_as_if_independent_of_latent_type":independently_assigned,
        "instrument_exclusion_no_direct_Z_to_Y":exclusion_valid,
        "monotonicity_no_defiers":monotonic,
        "relevance_nonzero_first_stage":fs!=0,
        "instrument_first_stage_at_least_one_half":strong,
        "n_compliers":comps,"n_always":alw,"n_never":never,"n_defiers":defiers,
        "P_instrument_Z0_exact":str(pz0),
        "P_instrument_Z1_exact":str(pz1),
        "E_D_given_Z0_exact":str(d0),
        "E_D_given_Z1_exact":str(d1),
        "E_Y_given_Z0_exact":str(y0),
        "E_Y_given_Z1_exact":str(y1),
        "first_stage_exact":str(fs),
        "ITT_reduced_form_Y_exact":str(ity),
        "wald_ratio_exact":str(wald) if wald is not None else "UNDEFINED_ZERO_FIRST_STAGE",
        "oracle_population_ATE_exact":str(population_ATE(world)),
        "oracle_complier_LATE_exact":str(late) if late is not None else "UNDEFINED_NO_COMPLIERS",
        "structural_compliance_net_first_stage_for_independent_Z_exact":
            str(structural_fs),
        "structural_exclusion_plus_direct_effect_reduced_form_if_independent_Z_exact":
            str(structural_ity),
        "independent_source_structural_identity_applicable":independently_assigned,
        "four_core_LATE_identification_conditions_hold":all_assumptions_valid,
        "wald_minus_oracle_complier_effect_exact":
            str(wald-late) if wald is not None and late is not None else "UNDEFINED",
        "wald_minus_oracle_population_ATE_exact":
            str(wald-population_ATE(world)) if wald is not None else "UNDEFINED",
    }
    return result,rows


def compute():
    results=[]
    raw=[]
    for w in WORLDS:
        r,rows=source_world(w)
        results.append(r)
        raw.extend(rows)
    if len(results)!=8 or len(raw)!=128:
        raise AssertionError("incomplete artificial IV world enumeration")
    lookup={v["world"]:v for v in results}
    asserted={
        "FULL_COMPLY":("1","5/2"),
        "MONOTONE_MIX":("1/2","3"),
        "WEAK_COMPLIERS":("1/8","4"),
        "NO_COMPLIERS":("0","UNDEFINED_ZERO_FIRST_STAGE"),
        "WITH_DEFIERS":("1/4","0"),
        "EXCLUSION_VIOLATION":("1/2","5"),
        "WEAK_EXCLUSION":("1/8","12"),
        "Z_CONFOUNDING":("1/2","29/2"),
    }
    for w,(first,wald) in asserted.items():
        if (lookup[w]["first_stage_exact"],lookup[w]["wald_ratio_exact"])!=(first,wald):
            raise AssertionError("pre-frozen IV counterexample failed: "+w)
    return {
        "research_id":"R213",
        "catalogue_id":"09-004",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "artificial_population_worlds":8,
        "latent_person_types_per_world":8,
        "original_source_atoms_per_world":16,
        "all_original_population_instrument_atoms":128,
        "full_exact_probability_and_conditioning_routes":True,
        "nonrandom_instrument_principal_stratum_independence_failure_flagged":True,
        "zero_first_stage_ratio_not_falsely_reported_as_numeric":True,
        "summary_worlds":results,
        "new_real_human_E2":0,
        "new_real_historical_E3":0,
        "scope":"Artificial finite binary instrument world; never claims real human validity or finite sample weak IV distribution.",
    },raw


def emit():
    r,rows=compute()
    paths={"results":BASE/"R213_EXACT_RESULTS.json",
           "sources":BASE/"R213_ALL_128_ORIGINAL_INSTRUMENT_SOURCE_ATOMS.csv"}
    paths["results"].write_text(json.dumps(r,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    with paths["sources"].open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    acceptance={
        "model_id":"R213","catalogue_id":"09-004","worlds":8,
        "original_population_instrument_source_atoms":128,
        "all_exact_source_conditional_probabilities_and_LATE_identification_checks":True,
        "source_validation_random_IV_identity_rejected_when_nonrandom":True,
        "new_E2":0,"new_E3":0,
        **{k+"_sha256":hashlib.sha256(v.read_bytes()).hexdigest() for k,v in paths.items()},
    }
    (BASE/"R213_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(acceptance,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(acceptance,indent=2))


class Tests(unittest.TestCase):
    def test_8_worlds(self): self.assertEqual(len(WORLDS),8)
    def test_8_people(self): self.assertEqual(N,8)
    def test_compliance_types_four(self): self.assertEqual(len(COMPLIANCE),4)
    def test_complier_assignment(self):
        self.assertEqual(tuple(d_potential("COMPLIER",z) for z in (0,1)),(0,1))
    def test_defier_assignment(self):
        self.assertEqual(tuple(d_potential("DEFIER",z) for z in (0,1)),(1,0))
    def test_always_assignment(self):
        self.assertEqual(tuple(d_potential("ALWAYS",z) for z in (0,1)),(1,1))
    def test_never_assignment(self):
        self.assertEqual(tuple(d_potential("NEVER",z) for z in (0,1)),(0,0))
    def test_8_latent_individual_records(self):
        self.assertTrue(all(len(build_population(w))==8 for w in WORLDS))
    def test_population_each_true_source_tau_rational(self):
        self.assertTrue(all(isinstance(tau,F) for w in WORLDS for typ,y0,tau in build_population(w)))
    def test_all_probabilities_positive(self):
        self.assertTrue(all(F(r["joint_source_probability_exact"])>0
                            for w in WORLDS for r in original_source_rows(w)))
    def test_each_world_source_probabilities_sum_one(self):
        self.assertTrue(all(sum((F(r["joint_source_probability_exact"])
                          for r in original_source_rows(w)),Z)==O for w in WORLDS))
    def test_128_original_atoms(self):
        self.assertEqual(sum(len(original_source_rows(w)) for w in WORLDS),128)
    def test_independent_instrument_arms_equal(self):
        for w in WORLDS:
            r,_=source_world(w)
            self.assertEqual((r["P_instrument_Z0_exact"],r["P_instrument_Z1_exact"]),("1/2","1/2"))
    def test_valid_full_compliance_first_stage_one(self):
        self.assertEqual(source_world("FULL_COMPLY")[0]["first_stage_exact"],"1")
    def test_all_compliers_late_equals_ate(self):
        self.assertEqual(complier_LATE("FULL_COMPLY"),population_ATE("FULL_COMPLY"))
    def test_monotone_mixed_late_three(self):
        self.assertEqual(complier_LATE("MONOTONE_MIX"),F(3))
    def test_monotone_mixed_ate_three_halves(self):
        self.assertEqual(population_ATE("MONOTONE_MIX"),F(3,2))
    def test_valid_monotone_wald_late(self):
        for w in ("FULL_COMPLY","MONOTONE_MIX","WEAK_COMPLIERS"):
            r,_=source_world(w)
            self.assertEqual(r["wald_ratio_exact"],r["oracle_complier_LATE_exact"])
    def test_weak_first_stage_one_eighth(self):
        self.assertEqual(source_world("WEAK_COMPLIERS")[0]["first_stage_exact"],"1/8")
    def test_weak_wald_still_late_if_valid(self):
        self.assertEqual(source_world("WEAK_COMPLIERS")[0]["wald_ratio_exact"],"4")
    def test_zero_first_stage_ratio_undefined(self):
        r,_=source_world("NO_COMPLIERS")
        self.assertEqual(r["wald_ratio_exact"],"UNDEFINED_ZERO_FIRST_STAGE")
    def test_zero_compliers_late_undefined(self):
        self.assertEqual(source_world("NO_COMPLIERS")[0]["oracle_complier_LATE_exact"],
                         "UNDEFINED_NO_COMPLIERS")
    def test_no_compliers_ate_nonzero(self):
        self.assertEqual(population_ATE("NO_COMPLIERS"),F(2))
    def test_defiers_invalid_monotonicity(self):
        self.assertFalse(source_world("WITH_DEFIERS")[0]["monotonicity_no_defiers"])
    def test_defiers_wald_zero(self):
        self.assertEqual(source_world("WITH_DEFIERS")[0]["wald_ratio_exact"],"0")
    def test_defiers_true_complier_effect_two(self):
        self.assertEqual(complier_LATE("WITH_DEFIERS"),F(2))
    def test_strong_direct_exclusion_bias(self):
        r,_=source_world("EXCLUSION_VIOLATION")
        self.assertEqual((r["wald_ratio_exact"],r["oracle_complier_LATE_exact"]),("5","3"))
    def test_weak_direct_exclusion_bias_eight(self):
        r,_=source_world("WEAK_EXCLUSION")
        self.assertEqual((r["wald_ratio_exact"],r["oracle_complier_LATE_exact"]),("12","4"))
    def test_nonrandom_z_outcome_confounds(self):
        r,_=source_world("Z_CONFOUNDING")
        self.assertEqual((r["wald_ratio_exact"],r["oracle_complier_LATE_exact"]),("29/2","3"))
    def test_nonrandom_independence_flagged(self):
        self.assertFalse(source_world("Z_CONFOUNDING")[0]
                         ["instrument_is_as_if_independent_of_latent_type"])
    def test_all_independent_z_source_identity(self):
        for w in WORLDS:
            if w=="Z_CONFOUNDING":
                continue
            r,_=source_world(w)
            self.assertEqual(r["first_stage_exact"],
                             r["structural_compliance_net_first_stage_for_independent_Z_exact"])
            self.assertEqual(r["ITT_reduced_form_Y_exact"],
                             r["structural_exclusion_plus_direct_effect_reduced_form_if_independent_Z_exact"])
    def test_direct_exclusion_coefficient_one(self):
        self.assertEqual(direct_instrument_effect("EXCLUSION_VIOLATION"),O)
    def test_no_direct_effect_valid_world(self):
        self.assertEqual(direct_instrument_effect("MONOTONE_MIX"),Z)
    def test_observed_treatment_binary(self):
        self.assertTrue(all(observed(w,i,z)[0] in (0,1) for w in WORLDS for i in range(N) for z in (0,1)))
    def test_invalid_world_rejected(self):
        with self.assertRaises(ValueError): build_population("MISSING")
    def test_invalid_instrument_rejected(self):
        with self.assertRaises(ValueError): observed("FULL_COMPLY",0,3)
    def test_invalid_compliance_rejected(self):
        with self.assertRaises(ValueError): d_potential("COMPLEX",0)
    def test_full_results_count(self):
        r,rows=compute()
        self.assertEqual((len(r["summary_worlds"]),len(rows)),(8,128))
        self.assertEqual(r["new_real_human_E2"],0)
    def test_replay_deterministic(self):
        self.assertEqual(compute(),compute())

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true")
    p.add_argument("--emit",action="store_true")
    v=p.parse_args()
    if v.test:
        result=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if result.wasSuccessful() else 1)
    if v.emit: emit()
    if not v.test and not v.emit: p.print_help()
