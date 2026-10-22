#!/usr/bin/env python3
"""R221 exact finite potential-outcome causal mediation identification.

Six precommitted SCMs; treatment T assigned independently and fairly to
four equiprobable latent U types; 48 complete original randomized observation
sources (8 per world). Observational mediation formula uses ONLY T,M,Y,source
probabilities. Oracle nested and controlled potential outcomes use hidden U
for scientific auditing, never as observable estimation input.

Run: python research/R221/r221_exact_causal_mediation.py --test
     python research/R221/r221_exact_causal_mediation.py --emit
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import unittest
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

F=Fraction
ZERO=F(0)
ONE=F(1)
WORLD_NAMES=(
    "PURE_INDIRECT",
    "LATENT_COMMON_CAUSE_NO_MEDIATION",
    "PURE_DIRECT",
    "ZERO_CAUSAL_EFFECT",
    "ADDITIVE_BOTH",
    "TREATMENT_MEDIATOR_INTERACTION",
)
US=(0,1,2,3)
TS=(0,1)
OUT=Path(__file__).resolve().parent
MEDIATOR_NO_CHANGE=(0,1,0,1)
MEDIATOR0=(0,0,1,1)
MEDIATOR1=(0,1,1,1)


def mediator(world,t,u):
    if world not in WORLD_NAMES or t not in TS or u not in US:
        raise ValueError("bad world/t/u")
    if world in ("PURE_DIRECT","ZERO_CAUSAL_EFFECT"):
        return MEDIATOR_NO_CHANGE[u]
    return (MEDIATOR0 if t==0 else MEDIATOR1)[u]


def outcome(world,t,m,u):
    if world not in WORLD_NAMES or t not in TS or m not in (0,1) or u not in US:
        raise ValueError("invalid structural potential result")
    if world=="PURE_INDIRECT":
        return F(m)
    if world=="LATENT_COMMON_CAUSE_NO_MEDIATION":
        # Exogenous U and T determine Y. Intervening on M alone does nothing.
        return F(mediator(world,t,u))
    if world=="PURE_DIRECT":
        return F(t)
    if world=="ZERO_CAUSAL_EFFECT":
        return ZERO
    if world=="ADDITIVE_BOTH":
        return F(t+m)
    if world=="TREATMENT_MEDIATOR_INTERACTION":
        return F(t*m)
    raise AssertionError("unexpected true model")


def nested(world,t,tprime,u):
    """Oracle potential Y(t, M(tprime,U)) under SAME U source."""
    return outcome(world,t,mediator(world,tprime,u),u)


def original_sources(world):
    if world not in WORLD_NAMES:
        raise ValueError("unknown world")
    rows=[]
    for u in US:
        for t in TS:
            m=mediator(world,t,u)
            y=outcome(world,t,m,u)
            rows.append({
                "world":world, "latent_U_audit_only":u,"random_T":t,
                "observed_M":m,"observed_Y":y,"probability":F(1,8),
                "m0":mediator(world,0,u),"m1":mediator(world,1,u),
                "y00":outcome(world,0,0,u),"y01":outcome(world,0,1,u),
                "y10":outcome(world,1,0,u),"y11":outcome(world,1,1,u),
                "nested_0_M0":nested(world,0,0,u),
                "nested_0_M1":nested(world,0,1,u),
                "nested_1_M0":nested(world,1,0,u),
                "nested_1_M1":nested(world,1,1,u),
            })
    if sum((r["probability"] for r in rows),ZERO)!=ONE:
        raise AssertionError("source weights fail")
    return tuple(rows)


def observational_signature(rows):
    """Only observable T,M,Y and probability; must not read U or potential Y."""
    d=defaultdict(lambda:ZERO)
    for row in rows:
        d[(row["random_T"],row["observed_M"],row["observed_Y"])]+=row["probability"]
    if sum(d.values(),ZERO)!=ONE:
        raise AssertionError("observation joint mass failed")
    return dict(sorted(d.items()))


def observable_only_summaries(rows):
    """Nonparametric 2x2 table from ONLY observed T,M,Y,weight."""
    obs=tuple((r["random_T"],r["observed_M"],r["observed_Y"],r["probability"])
              for r in rows)
    p_t={t:sum((p for tt,m,y,p in obs if tt==t),ZERO) for t in TS}
    if any(p_t[t]!=F(1,2) for t in TS):
        raise AssertionError("frozen randomized assignment failure")
    p_m_given_t={}
    e_y_given_tm={}
    for t in TS:
        for m in (0,1):
            joint_mass=sum((p for tt,mm,y,p in obs if tt==t and mm==m),ZERO)
            if joint_mass<=0:
                raise AssertionError("all four T/M cells have positivity by design")
            p_m_given_t[(t,m)]=joint_mass/p_t[t]
            e_y_given_tm[(t,m)]=sum((p*y for tt,mm,y,p in obs
                                     if tt==t and mm==m),ZERO)/joint_mass
    e_y_given_t={
        t:sum((p*y for tt,m,y,p in obs if tt==t),ZERO)/p_t[t] for t in TS
    }
    # Formula evaluating hypothesized natural effects under extra sequential
    # ignorability. With mediator-outcome latent common cause this FAILS.
    gnde=sum((p_m_given_t[(0,m)]*(e_y_given_tm[(1,m)]-e_y_given_tm[(0,m)])
              for m in (0,1)),ZERO)
    gnie=sum((e_y_given_tm[(1,m)]*(p_m_given_t[(1,m)]-p_m_given_t[(0,m)])
              for m in (0,1)),ZERO)
    te=e_y_given_t[1]-e_y_given_t[0]
    if gnde+gnie!=te:
        raise AssertionError("observable g decomposition algebra failed")
    return {
        "observable_T_Y_mean_difference":te,
        "gformula_NDE_at_M0":gnde,
        "gformula_NIE_at_T1":gnie,
        "observable_m_probability_by_t":{
            f"T{t}_M{m}":p_m_given_t[(t,m)] for t in TS for m in (0,1)
        },
        "observable_outcome_conditional_TM":{
            f"T{t}_M{m}":e_y_given_tm[(t,m)] for t in TS for m in (0,1)
        },
    }


def oracle_natural_effects(world):
    """True cross-world nested outcomes from the four latent types, not data."""
    vals=[]
    for u in US:
        y00=nested(world,0,0,u)
        y01=nested(world,0,1,u)
        y10=nested(world,1,0,u)
        y11=nested(world,1,1,u)
        vals.append((y00,y01,y10,y11))
    mean=lambda terms:sum(terms,ZERO)/4
    te=mean(v[3]-v[0] for v in vals)
    nde0=mean(v[2]-v[0] for v in vals)
    nie1=mean(v[3]-v[2] for v in vals)
    nie0=mean(v[1]-v[0] for v in vals)
    nde1=mean(v[3]-v[1] for v in vals)
    if te!=nde0+nie1 or te!=nie0+nde1:
        raise AssertionError("both cross-world mediation decompositions failed")
    do0=mean(v[0] for v in vals)
    do1=mean(v[3] for v in vals)
    if te!=do1-do0:
        raise AssertionError("two oracle total-effect routes disagree")
    return {
        "true_total_effect":te,"true_NDE_at_M0":nde0,
        "true_NIE_at_T1":nie1,"true_NIE_at_T0":nie0,
        "true_NDE_at_M1":nde1,
        "oracle_natural_Y0_mean":do0,"oracle_natural_Y1_mean":do1,
    }


def compute():
    worlds=[]
    full_raw=[]
    for world in WORLD_NAMES:
        raw=original_sources(world)
        estimated=observable_only_summaries(raw)
        oracle=oracle_natural_effects(world)
        if estimated["observable_T_Y_mean_difference"]!=oracle["true_total_effect"]:
            raise AssertionError("randomized total effect not recovered")
        worlds.append({
            "world":world,
            "original_true_exogenous_U_types":4,
            "complete_randomized_observation_source_atoms":len(raw),
            "complete_joint_original_source_probability":"1",
            "true_oracle_nested_effects":{k:str(v) for k,v in oracle.items()},
            "observable_only_gformula_results":{
                k:({kk:str(vv) for kk,vv in v.items()} if isinstance(v,dict)
                   else str(v)) for k,v in estimated.items()},
            "gformula_minus_true_NDE_bias_exact":
                str(estimated["gformula_NDE_at_M0"]-oracle["true_NDE_at_M0"]),
            "gformula_minus_true_NIE_bias_exact":
                str(estimated["gformula_NIE_at_T1"]-oracle["true_NIE_at_T1"]),
            "latent_mediator_outcome_common_cause_present":
                world=="LATENT_COMMON_CAUSE_NO_MEDIATION",
        })
        for r in raw:
            full_raw.append({
                "true_world":world,
                "true_exogenous_U_ORACLE_ONLY":r["latent_U_audit_only"],
                "realized_random_T":r["random_T"],
                "true_original_source_probability":str(r["probability"]),
                "realized_observable_M":r["observed_M"],
                "realized_observable_Y":str(r["observed_Y"]),
                "potential_M0_ORACLE_ONLY":r["m0"],
                "potential_M1_ORACLE_ONLY":r["m1"],
                "controlled_Y_t0_m0_ORACLE_ONLY":str(r["y00"]),
                "controlled_Y_t0_m1_ORACLE_ONLY":str(r["y01"]),
                "controlled_Y_t1_m0_ORACLE_ONLY":str(r["y10"]),
                "controlled_Y_t1_m1_ORACLE_ONLY":str(r["y11"]),
                "nested_Y_0_M0_ORACLE_ONLY":str(r["nested_0_M0"]),
                "nested_Y_0_M1_ORACLE_ONLY":str(r["nested_0_M1"]),
                "nested_Y_1_M0_ORACLE_ONLY":str(r["nested_1_M0"]),
                "nested_Y_1_M1_ORACLE_ONLY":str(r["nested_1_M1"]),
            })
    if len(worlds)!=6 or len(full_raw)!=48:
        raise AssertionError("incomplete worlds/sources")
    first=original_sources("PURE_INDIRECT")
    second=original_sources("LATENT_COMMON_CAUSE_NO_MEDIATION")
    if observational_signature(first)!=observational_signature(second):
        raise AssertionError("two pre-frozen SCMs are not observationally equivalent")
    if oracle_natural_effects("PURE_INDIRECT")==oracle_natural_effects(
            "LATENT_COMMON_CAUSE_NO_MEDIATION"):
        raise AssertionError("true decomposition did not differ")
    return {
        "research_id":"R221",
        "original_239_catalogue_id":"09-012",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "artificial_scm_worlds":6,
        "full_original_exogenous_U_types_each_world":4,
        "full_original_randomized_T_by_U_observations":48,
        "true_random_treatment_assignment_probability":"1/2",
        "gformula_reads_only_observed_T_M_Y":True,
        "true_nested_effects_require_ORACLE_U":True,
        "perfect_observational_T_M_Y_equivalence_pair":[
            "PURE_INDIRECT","LATENT_COMMON_CAUSE_NO_MEDIATION"],
        "identical_observation_law_but_different_natural_effects":True,
        "randomized_T_identifies_total_effect_not_natural_decomposition":True,
        "new_real_human_E2":0,"new_real_historical_E3":0,
        "worlds":worlds,
        "limitations":[
            "All six mechanisms are artificial 4-latent-type SCMs with eight original observation atoms each",
            "Mediation g-formula needs extra sequential ignorability including mediator-outcome exchangeability",
            "T was truly randomized but M was NOT separately randomized",
            "Cross-world potential outcomes known only to artificial scientific auditor",
            "No actual human psychological, social or historical causal mediation evidence",
        ],
    },full_raw


def emit():
    result,raw=compute()
    paths={
        "results":OUT/"R221_EXACT_RESULTS.json",
        "sources":OUT/"R221_ALL_48_ORIGINAL_MEDIATION_SCM_SOURCES.csv",
    }
    paths["results"].write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with paths["sources"].open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(raw[0]))
        writer.writeheader()
        writer.writerows(raw)
    receipt={
        "research_id":"R221",
        "original_catalogue_id":"09-012",
        "complete_synthetic_scm_worlds":6,
        "full_original_randomized_T_by_U_atoms":48,
        "observation_equivalence_vs_nested_mediation_counterexample":True,
        "Fraction_randomization_gformula_and_two_natural_effect_decompositions":True,
        "new_E2":0,"new_E3":0,
        **{key+"_sha256":hashlib.sha256(path.read_bytes()).hexdigest()
           for key,path in paths.items()},
    }
    (OUT/"R221_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(receipt,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2))


class Tests(unittest.TestCase):
    def test_6_frozen_worlds(self):
        self.assertEqual(len(WORLD_NAMES),6)
    def test_source_types_four(self):
        self.assertEqual(len(US),4)
    def test_treatment_two_values(self):
        self.assertEqual(TS,(0,1))
    def test_true_source_count_48(self):
        self.assertEqual(len(WORLD_NAMES)*len(US)*len(TS),48)
    def test_shared_base_mediator0(self):
        self.assertEqual(tuple(mediator("PURE_INDIRECT",0,u) for u in US),MEDIATOR0)
    def test_shared_base_mediator1(self):
        self.assertEqual(tuple(mediator("PURE_INDIRECT",1,u) for u in US),MEDIATOR1)
    def test_med_prob_t0_one_half(self):
        self.assertEqual(sum((mediator("PURE_INDIRECT",0,u) for u in US),ZERO)/4,F(1,2))
    def test_med_prob_t1_three_quarters(self):
        self.assertEqual(sum((mediator("PURE_INDIRECT",1,u) for u in US),ZERO)/4,F(3,4))
    def test_mediator_unchanged_in_direct(self):
        self.assertTrue(all(mediator("PURE_DIRECT",0,u)==mediator("PURE_DIRECT",1,u) for u in US))
    def test_all_sources_positive(self):
        for w in WORLD_NAMES:
            self.assertTrue(all(r["probability"]>0 for r in original_sources(w)))
    def test_all_sources_probability_one(self):
        for w in WORLD_NAMES:
            self.assertEqual(sum((r["probability"] for r in original_sources(w)),ZERO),ONE)
    def test_random_T_independent_U(self):
        for w in WORLD_NAMES:
            source=original_sources(w)
            self.assertTrue(all(sum((r["probability"] for r in source if r["latent_U_audit_only"]==u and r["random_T"]==t),ZERO)==F(1,8) for u in US for t in TS))
    def test_all_four_t_m_cells_positive(self):
        for w in WORLD_NAMES:
            r=original_sources(w)
            self.assertTrue(all(sum((a["probability"] for a in r if a["random_T"]==t and a["observed_M"]==m),ZERO)>0 for t in TS for m in (0,1)))
    def test_pure_indirect_observed_Y_equals_M(self):
        self.assertTrue(all(r["observed_Y"]==r["observed_M"] for r in original_sources("PURE_INDIRECT")))
    def test_latent_source_observed_Y_equals_M(self):
        self.assertTrue(all(r["observed_Y"]==r["observed_M"] for r in original_sources("LATENT_COMMON_CAUSE_NO_MEDIATION")))
    def test_equal_observational_signature_two_models(self):
        self.assertEqual(observational_signature(original_sources("PURE_INDIRECT")),
                         observational_signature(original_sources("LATENT_COMMON_CAUSE_NO_MEDIATION")))
    def test_offpath_intervention_differs_between_equivalent_models(self):
        w="LATENT_COMMON_CAUSE_NO_MEDIATION"
        self.assertEqual(outcome(w,1,0,2),outcome(w,1,1,2))
        self.assertNotEqual(outcome("PURE_INDIRECT",1,0,2),outcome("PURE_INDIRECT",1,1,2))
    def test_pure_indirect_oracle(self):
        x=oracle_natural_effects("PURE_INDIRECT")
        self.assertEqual((x["true_total_effect"],x["true_NDE_at_M0"],x["true_NIE_at_T1"]),
                         (F(1,4),ZERO,F(1,4)))
    def test_latent_same_TE_different_natural(self):
        x=oracle_natural_effects("LATENT_COMMON_CAUSE_NO_MEDIATION")
        self.assertEqual((x["true_total_effect"],x["true_NDE_at_M0"],x["true_NIE_at_T1"]),
                         (F(1,4),F(1,4),ZERO))
    def test_pure_direct_oracle(self):
        x=oracle_natural_effects("PURE_DIRECT")
        self.assertEqual((x["true_total_effect"],x["true_NDE_at_M0"],x["true_NIE_at_T1"]),
                         (ONE,ONE,ZERO))
    def test_zero_world_oracle(self):
        x=oracle_natural_effects("ZERO_CAUSAL_EFFECT")
        self.assertTrue(all(v==ZERO for v in x.values()))
    def test_additive_both_oracle(self):
        x=oracle_natural_effects("ADDITIVE_BOTH")
        self.assertEqual((x["true_total_effect"],x["true_NDE_at_M0"],x["true_NIE_at_T1"]),
                         (F(5,4),ONE,F(1,4)))
    def test_interaction_oracle_first_decomposition(self):
        x=oracle_natural_effects("TREATMENT_MEDIATOR_INTERACTION")
        self.assertEqual((x["true_total_effect"],x["true_NDE_at_M0"],x["true_NIE_at_T1"]),
                         (F(3,4),F(1,2),F(1,4)))
    def test_interaction_oracle_second_decomposition(self):
        x=oracle_natural_effects("TREATMENT_MEDIATOR_INTERACTION")
        self.assertEqual((x["true_NIE_at_T0"],x["true_NDE_at_M1"]),(ZERO,F(3,4)))
    def test_every_world_both_exact_natural_decompositions(self):
        for w in WORLD_NAMES:
            x=oracle_natural_effects(w)
            self.assertEqual(x["true_total_effect"],x["true_NDE_at_M0"]+x["true_NIE_at_T1"])
            self.assertEqual(x["true_total_effect"],x["true_NIE_at_T0"]+x["true_NDE_at_M1"])
    def test_total_randomized_observable_equals_oracle(self):
        for w in WORLD_NAMES:
            observed=observable_only_summaries(original_sources(w))
            oracle=oracle_natural_effects(w)
            self.assertEqual(observed["observable_T_Y_mean_difference"],oracle["true_total_effect"])
    def test_observational_gformula_agrees_with_pure_mediation(self):
        obs=observable_only_summaries(original_sources("PURE_INDIRECT"))
        self.assertEqual((obs["gformula_NDE_at_M0"],obs["gformula_NIE_at_T1"]),(ZERO,F(1,4)))
    def test_gformula_wrong_for_latent_mediation(self):
        obs=observable_only_summaries(original_sources("LATENT_COMMON_CAUSE_NO_MEDIATION"))
        oracle=oracle_natural_effects("LATENT_COMMON_CAUSE_NO_MEDIATION")
        self.assertNotEqual(obs["gformula_NDE_at_M0"],oracle["true_NDE_at_M0"])
        self.assertNotEqual(obs["gformula_NIE_at_T1"],oracle["true_NIE_at_T1"])
    def test_pure_direct_gformula(self):
        o=observable_only_summaries(original_sources("PURE_DIRECT"))
        self.assertEqual((o["gformula_NDE_at_M0"],o["gformula_NIE_at_T1"]),(ONE,ZERO))
    def test_gformula_algebra_TE_all(self):
        for w in WORLD_NAMES:
            o=observable_only_summaries(original_sources(w))
            self.assertEqual(o["observable_T_Y_mean_difference"],
                             o["gformula_NDE_at_M0"]+o["gformula_NIE_at_T1"])
    def test_treatment_mediator_interaction_not_unique_components(self):
        x=oracle_natural_effects("TREATMENT_MEDIATOR_INTERACTION")
        self.assertNotEqual(x["true_NDE_at_M0"],x["true_NDE_at_M1"])
    def test_full_joint_probability_signature(self):
        for w in WORLD_NAMES:
            self.assertEqual(sum(observational_signature(original_sources(w)).values(),ZERO),ONE)
    def test_oracle_controls_values(self):
        for w in WORLD_NAMES:
            for u in US:
                for t in TS:
                    for m in (0,1):
                        self.assertIsInstance(outcome(w,t,m,u),F)
    def test_nested_source_individual_identity(self):
        for w in WORLD_NAMES:
            for u in US:
                for t in TS:
                    self.assertEqual(nested(w,t,t,u),outcome(w,t,mediator(w,t,u),u))
    def test_invalid_mediator_world(self):
        with self.assertRaises(ValueError):
            mediator("UNLISTED",0,0)
    def test_invalid_outcome_mediator(self):
        with self.assertRaises(ValueError):
            outcome("PURE_DIRECT",0,2,0)
    def test_invalid_latent_u(self):
        with self.assertRaises(ValueError):
            mediator("PURE_INDIRECT",0,4)
    def test_full_computed_source_and_results(self):
        r,raw=compute()
        self.assertEqual((r["artificial_scm_worlds"],len(r["worlds"]),len(raw)),(6,6,48))
        self.assertTrue(r["identical_observation_law_but_different_natural_effects"])
        self.assertEqual(r["new_real_human_E2"],0)
    def test_full_compute_deterministic(self):
        self.assertEqual(compute(),compute())


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test",action="store_true")
    parser.add_argument("--emit",action="store_true")
    opts=parser.parse_args()
    if opts.test:
        result=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if result.wasSuccessful() else 1)
    if opts.emit:
        emit()
    if not opts.test and not opts.emit:
        parser.print_help()
