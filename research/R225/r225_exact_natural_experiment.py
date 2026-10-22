#!/usr/bin/env python3
"""R225: exact six-world finite natural-experiment credibility audit.

Under genuine as-if random assignments, equal-quota designs identify fixed
sample-average treatment effects in expectation. A hidden post-period shock
world is observationally identical to a valid-effect world while the true
effect is zero. All observations are artificial E1, not real experiments.
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
SCHEMES=tuple(tuple(int(i in chosen) for i in range(4))
              for chosen in itertools.combinations(range(4),2))
WORLDS=(
    "AS_IF_RANDOM_VALID",
    "ENDOGENOUS_FUTURE_SHOCK_ALIAS",
    "AS_IF_RANDOM_NULL",
    "AS_IF_RANDOM_HETEROGENEOUS",
    "ENDOGENOUS_VISIBLE_SELECTION",
    "ANTICIPATORY_PRE_RESPONSE",
)
ORIGINAL_FREEZE="7fb54ef2158bb5e3934e5d7a72bbd135ad891ac9"

def endogenous(world):
    return world in ("ENDOGENOUS_FUTURE_SHOCK_ALIAS","ENDOGENOUS_VISIBLE_SELECTION")

def tau(world,i):
    if world not in WORLDS or i not in range(4):
        raise ValueError("outside frozen world/unit")
    if world=="AS_IF_RANDOM_HETEROGENEOUS": return F(i)
    if world in ("AS_IF_RANDOM_VALID","ANTICIPATORY_PRE_RESPONSE"): return ONE
    return ZERO

def before(world,i,z,u):
    if world=="ENDOGENOUS_VISIBLE_SELECTION": return ONE+F(u)
    if world=="ANTICIPATORY_PRE_RESPONSE": return ONE+F(z,2)
    return ONE

def untreated_after(world,i,z,u,eps):
    if world in ("ENDOGENOUS_FUTURE_SHOCK_ALIAS","ENDOGENOUS_VISIBLE_SELECTION"):
        return ONE+F(u)+eps
    return ONE+eps

def noise_source(mask):
    if mask not in range(16): raise ValueError("unfrozen noise vector")
    return tuple(F(1,4) if mask&(1<<i) else F(-1,4) for i in range(4))

def original_source(world,scheme_id,noise_id):
    if world not in WORLDS or scheme_id not in range(6): raise ValueError("invalid structural source")
    z=SCHEMES[scheme_id]
    # In selected worlds an exogenous latent future type produces the same
    # observed schedule; intervention on D holds U constant.
    u=z if endogenous(world) else (0,0,0,0)
    eps=noise_source(noise_id)
    pre=tuple(before(world,i,z[i],u[i]) for i in range(4))
    y0=tuple(untreated_after(world,i,z[i],u[i],eps[i]) for i in range(4))
    y1=tuple(y0[i]+tau(world,i) for i in range(4))
    obs=tuple(y1[i] if z[i] else y0[i] for i in range(4))
    return dict(world=world,original_schedule_index=scheme_id,
                original_noise_mask=noise_id,latent_U=u,observed_Z=z,
                observed_D=z,observed_pre=pre,observed_post=obs,
                oracle_post_Y0=y0,oracle_post_Y1=y1,
                exogenous_noise=eps,original_probability=F(1,96))

def sources(world):
    if world not in WORLDS: raise ValueError("unknown world")
    rows=tuple(original_source(world,j,k) for j in range(6) for k in range(16))
    assert len(rows)==96
    assert sum((r["original_probability"] for r in rows),ZERO)==ONE
    return rows

def mean_select(values,z,treat):
    if len(values)!=4 or len(z)!=4 or sum(z)!=2:
        raise ValueError("frozen four-unit two-treated design")
    chosen=tuple(values[i] for i in range(4) if z[i]==treat)
    assert len(chosen)==2
    return sum(chosen,ZERO)/2

def observed_estimators(row):
    # Only the actual assignment and actual observed pre/post records.
    z=row["observed_Z"]
    pre=row["observed_pre"]
    post=row["observed_post"]
    dpost=mean_select(post,z,1)-mean_select(post,z,0)
    dpre=mean_select(pre,z,1)-mean_select(pre,z,0)
    diff=mean_select(tuple(post[i]-pre[i] for i in range(4)),z,1) \
         -mean_select(tuple(post[i]-pre[i] for i in range(4)),z,0)
    assert diff==dpost-dpre
    return {"post_group_difference":dpost,"pre_balance_placebo":dpre,
            "two_period_DiD":diff}

def true_ATE(row):
    return sum((row["oracle_post_Y1"][i]-row["oracle_post_Y0"][i] for i in range(4)),ZERO)/4

def observational_signature(world):
    distribution=defaultdict(F)
    for row in sources(world):
        # Full joint observed schedule, all individual pre and post outcomes.
        k=(row["observed_Z"],row["observed_pre"],row["observed_post"])
        distribution[k]+=row["original_probability"]
    return distribution

def analytic_noiseless_estimators(world,scheme_id):
    z=SCHEMES[scheme_id]
    u=z if endogenous(world) else (0,0,0,0)
    pre=tuple(before(world,i,z[i],u[i]) for i in range(4))
    # Independent of all sixteen measurement shocks, expectation eps=0.
    post=tuple(untreated_after(world,i,z[i],u[i],ZERO)+z[i]*tau(world,i)
               for i in range(4))
    dp=mean_select(post,z,1)-mean_select(post,z,0)
    pl=mean_select(pre,z,1)-mean_select(pre,z,0)
    return dict(post_group_difference=dp,pre_balance_placebo=pl,two_period_DiD=dp-pl)

def moments(values):
    e=sum(values,ZERO)/len(values)
    var=sum(((v-e)**2 for v in values),ZERO)/len(values)
    return e,var

def finite_results(world):
    rows=sources(world)
    actual_ate=tuple(true_ATE(r) for r in rows)
    if len(set(actual_ate))!=1:
        raise AssertionError("frozen oracle target must be fixed")
    truth=actual_ate[0]
    ana=[analytic_noiseless_estimators(world,j) for j in range(6)]
    estimators={}
    for method in ("post_group_difference","pre_balance_placebo","two_period_DiD"):
        observed=[observed_estimators(r)[method] for r in rows]
        source_mu,source_var=moments(observed)
        fixed_mu,fixed_var=moments([a[method] for a in ana])
        assert source_mu==fixed_mu
        # Each of the 4 independent eps_i has variance (1/4)^2,
        # with +/-1/2 group contrast coefficient. Total = 1/16.
        expected_var=fixed_var+(ZERO if method=="pre_balance_placebo" else F(1,16))
        if source_var!=expected_var:
            raise AssertionError("independent conditional noise risk mismatch")
        target=ZERO if method=="pre_balance_placebo" else truth
        estimators[method]=dict(
            expectation=str(source_mu),
            fixed_schedule_component_variance=str(fixed_var),
            independent_shock_variance=str(expected_var-fixed_var),
            variance=str(source_var),
            bias_from_true_target=str(source_mu-target),
            mean_squared_error=str(source_var+(source_mu-target)**2))
    sig=observational_signature(world)
    return dict(world=world,original_full_sources=96,truth_ATE=str(truth),
                assignment_rule="LATENT_FUTURE_TYPE_U_SELECTED" if endogenous(world)
                                else "EXTERNAL_UNIFORM_SIX_QUOTA_SCHEDULES",
                observed_joint_support_cells=len(sig),
                all_source_probabilities_sum="1",
                observed_methods=estimators)

def generation():
    summary=[finite_results(w) for w in WORLDS]
    if observational_signature(WORLDS[0])!=observational_signature(WORLDS[1]):
        raise AssertionError("valid and endogenous full observable joint distributions must coincide")
    if (summary[0]["truth_ATE"],summary[1]["truth_ATE"])!=("1","0"):
        raise AssertionError("true causal alias broken")
    out=dict(research_id="R225",original_catalogue_id="09-016",
             scientific_scope="FINITE_ARTIFICIAL_E1_ONLY",
             prescore_protocol_commit=ORIGINAL_FREEZE,
             original_world_count=6,complete_original_source_atoms=576,
             original_source_atoms_per_world=96,
             hidden_endogenous_and_valid_full_observation_identical=True,
             new_human_E2=0,new_historical_E3=0,
             R073="FROZEN",PESEN_v0_1="FROZEN",
             world_results=summary)
    sourcefile=HERE/"R225_ALL_576_ORIGINAL_NATURAL_ASSIGNMENT_SOURCES.csv"
    fields=("world","original_schedule_index","original_noise_mask",
            "latent_U","observed_Z","observed_D","observed_pre","observed_post",
            "oracle_post_Y0","oracle_post_Y1","exogenous_noise",
            "original_probability")
    with sourcefile.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        writer.writeheader()
        for world in WORLDS:
            for row in sources(world):
                writer.writerow({k:str(row[k]) for k in fields})
    resultfile=HERE/"R225_EXACT_RESULTS.json"
    resultfile.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(research_id="R225",catalogue_id="09-016",
                 full_worlds=6,all_original_sources=576,
                 full_observational_joint_alias_confirmed=True,
                 independent_fraction_moment_routes=True,
                 new_real_human_E2=0,new_real_historical_E3=0,
                 sources_sha256=hashlib.sha256(sourcefile.read_bytes()).hexdigest(),
                 results_sha256=hashlib.sha256(resultfile.read_bytes()).hexdigest())
    (HERE/"R225_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_six_schedules(self): self.assertEqual(len(SCHEMES),6)
    def test_two_treated(self): self.assertTrue(all(sum(z)==2 for z in SCHEMES))
    def test_six_worlds(self): self.assertEqual(len(WORLDS),6)
    def test_sources_count(self): self.assertEqual(sum(len(sources(w)) for w in WORLDS),576)
    def test_valid_alias_joint(self):
        self.assertEqual(observational_signature(WORLDS[0]),observational_signature(WORLDS[1]))
    def test_valid_alias_true(self):
        self.assertEqual((finite_results(WORLDS[0])["truth_ATE"],
                          finite_results(WORLDS[1])["truth_ATE"]),("1","0"))
    def test_qualitative_pre(self):
        self.assertEqual(finite_results("ENDOGENOUS_FUTURE_SHOCK_ALIAS")[
            "observed_methods"]["pre_balance_placebo"]["expectation"],"0")
    def test_visible_selection(self):
        x=finite_results("ENDOGENOUS_VISIBLE_SELECTION")["observed_methods"]
        self.assertEqual(x["pre_balance_placebo"]["expectation"],"1")
        self.assertEqual(x["two_period_DiD"]["expectation"],"0")
    def test_anticipation(self):
        x=finite_results("ANTICIPATORY_PRE_RESPONSE")["observed_methods"]
        self.assertEqual(x["pre_balance_placebo"]["expectation"],"1/2")
        self.assertEqual(x["two_period_DiD"]["expectation"],"1/2")
    def test_heterogeneous_unbiased(self):
        x=finite_results("AS_IF_RANDOM_HETEROGENEOUS")
        self.assertEqual(x["truth_ATE"],"3/2")
        self.assertEqual(x["observed_methods"]["post_group_difference"]["expectation"],"3/2")
    def test_var_shock(self):
        self.assertEqual(finite_results("AS_IF_RANDOM_VALID")[
            "observed_methods"]["two_period_DiD"]["variance"],"1/16")
    def test_invalid_source(self):
        with self.assertRaises(ValueError): original_source("AS_IF_RANDOM_VALID",6,0)
    def test_invalid_noise(self):
        with self.assertRaises(ValueError): noise_source(16)

def _world_case(world,aspect):
    def test(self):
        rows=sources(world)
        if aspect=="mass":
            self.assertEqual(sum((r["original_probability"] for r in rows),ZERO),ONE)
        elif aspect=="unique":
            self.assertEqual(len({(r["original_schedule_index"],r["original_noise_mask"]) for r in rows}),96)
        elif aspect=="oracle":
            self.assertEqual(len({true_ATE(r) for r in rows}),1)
        elif aspect=="observed":
            for row in rows:
                self.assertEqual(observed_estimators(row)["two_period_DiD"],
                                 observed_estimators(row)["post_group_difference"]-
                                 observed_estimators(row)["pre_balance_placebo"])
        elif aspect=="independent_expected":
            r=finite_results(world)
            self.assertEqual(len(r["observed_methods"]),3)
        elif aspect=="latent":
            for row in rows:
                self.assertEqual(row["latent_U"]==row["observed_Z"],endogenous(world)
                                 or row["observed_Z"]==(0,0,0,0))
        else: raise AssertionError("unexpected test")
    return test
for _world in WORLDS:
    for _aspect in ("mass","unique","oracle","observed","independent_expected"):
        setattr(Tests,"test_"+_world.lower()+"_"+_aspect,_world_case(_world,_aspect))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    args=p.parse_args()
    if args.test: unittest.main(argv=["r225"],verbosity=2)
    else: print(json.dumps(generation(),ensure_ascii=False,indent=2))
