#!/usr/bin/env python3
"""R233: exact cross-group measurement invariance of three-item latent scores.

Eight prescore frozen finite measurement populations. Source-level observed
aliases separate latent means from item intercept shifts; a second alias is
caused by unanchored factor rescaling. Raw parameter equalities and observable
evidence are kept distinct. No real human or historical group is represented.
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
FREEZE="da25e50497f41ab416e34c6a18ca4f6a74ff93bd"
BASE={"intercept":(0,0,0),"loading":(1,1,1),"error":(1,1,1),
      "latent_scale":1,"latent_shift":0}
WORLD_GROUP1={
 "FULL_STRICT_INVARIANT":{},
 "TRUE_LATENT_MEAN_SHIFT":{"latent_shift":1},
 "INTERCEPT_SHIFT_ALIAS":{"intercept":(1,1,1)},
 "METRIC_LOADING_CHANGE":{"loading":(2,1,1)},
 "PARTIAL_SCALAR_ITEM1":{"intercept":(1,0,0)},
 "STRICT_RESIDUAL_VARIANCE_CHANGE":{"error":(2,1,1)},
 "LATENT_SCALE_ALIAS":{"latent_scale":2,"loading":(F(1,2),F(1,2),F(1,2))},
 "CONFIGURAL_ITEM3_DETACHED":{"loading":(1,1,0)}
}

def params(world,group):
    if world not in WORLD_GROUP1 or group not in (0,1):
        raise ValueError("unfrozen group measurement world")
    z=dict(BASE)
    if group:
        z.update(WORLD_GROUP1[world])
    return z

def atom(world,g,t,e1,e2,e3):
    if world not in WORLD_GROUP1 or g not in (0,1) or any(v not in (-1,1) for v in (t,e1,e2,e3)):
        raise ValueError("unfrozen exogenous source")
    p=params(world,g)
    hidden=F(p["latent_scale"]*t+p["latent_shift"])
    obs=tuple(F(p["intercept"][i])+F(p["loading"][i])*hidden+F(p["error"][i]*(e1,e2,e3)[i]) for i in range(3))
    return dict(world=world,observed_group_G=g,oracle_original_T=t,
                independent_E1=e1,independent_E2=e2,independent_E3=e3,
                oracle_actual_latent_F=hidden,
                observed_X1=obs[0],observed_X2=obs[1],observed_X3=obs[2],
                original_probability=F(1,32))

def sources(world):
    if world not in WORLD_GROUP1: raise ValueError("unknown world")
    data=tuple(atom(world,g,*v) for g in (0,1)
               for v in itertools.product((-1,1),repeat=4))
    assert len(data)==32
    assert sum((r["original_probability"] for r in data),ZERO)==ONE
    return data

def group_stats_from_observed_source(world,g):
    # Explicitly never reads actual latent F, true loadings or item intercepts.
    obs=[r for r in sources(world) if r["observed_group_G"]==g]
    mass=sum((r["original_probability"] for r in obs),ZERO)
    assert len(obs)==16 and mass==F(1,2)
    means=tuple(sum((r["original_probability"]*r[f"observed_X{i+1}"] for r in obs),ZERO)/mass
                for i in range(3))
    c=tuple(tuple(
        sum((r["original_probability"]*(r[f"observed_X{i+1}"]-means[i])*
             (r[f"observed_X{j+1}"]-means[j]) for r in obs),ZERO)/mass
        for j in range(3)) for i in range(3))
    return means,c

def independent_analytic_group_stats(world,g):
    # Direct coefficient formula from fixed model; never reads source rows.
    p=params(world,g)
    mean=tuple(F(p["intercept"][i])+F(p["loading"][i]*p["latent_shift"]) for i in range(3))
    cov=tuple(tuple(F(p["loading"][i]*p["loading"][j]*p["latent_scale"]**2)
          +(F(p["error"][i]**2) if i==j else ZERO)
          for j in range(3)) for i in range(3))
    return mean,cov

def observable_joint(world):
    data=defaultdict(F)
    for r in sources(world):
        k=(r["observed_group_G"],r["observed_X1"],r["observed_X2"],r["observed_X3"])
        data[k]+=r["original_probability"]
    return dict(sorted(data.items()))

def raw_invariance(world):
    a=params(world,0);b=params(world,1)
    conf=tuple(v!=0 for v in a["loading"])==tuple(v!=0 for v in b["loading"])
    metric=tuple(a["loading"])==tuple(b["loading"])
    scalar=tuple(a["intercept"])==tuple(b["intercept"])
    strict=tuple(F(x)**2 for x in a["error"])==tuple(F(x)**2 for x in b["error"])
    return dict(raw_configural_equal=conf,raw_metric_equal=metric,
                raw_scalar_intercepts_equal=scalar,
                raw_strict_residual_variances_equal=strict)

def alias_certificates():
    for a,b in (("TRUE_LATENT_MEAN_SHIFT","INTERCEPT_SHIFT_ALIAS"),
                ("FULL_STRICT_INVARIANT","LATENT_SCALE_ALIAS")):
        xx=sources(a);yy=sources(b)
        for x,y in zip(xx,yy):
            assert x["observed_group_G"]==y["observed_group_G"]
            for i in range(1,4):
                if x[f"observed_X{i}"]!=y[f"observed_X{i}"]:
                    raise AssertionError("frozen metric/intercept source alias mismatch")
        assert observable_joint(a)==observable_joint(b)
    assert F(params("TRUE_LATENT_MEAN_SHIFT",1)["latent_shift"])==1
    assert F(params("INTERCEPT_SHIFT_ALIAS",1)["latent_shift"])==0
    assert tuple(params("LATENT_SCALE_ALIAS",1)["loading"])!=(1,1,1)
    return True

def world_result(world):
    data=sources(world)
    a,b=group_stats_from_observed_source(world,0),group_stats_from_observed_source(world,1)
    assert a==independent_analytic_group_stats(world,0)
    assert b==independent_analytic_group_stats(world,1)
    delta=tuple(b[0][i]-a[0][i] for i in range(3))
    flags=raw_invariance(world)
    if world=="TRUE_LATENT_MEAN_SHIFT":
        assert delta==(ONE,ONE,ONE) and all(flags.values())
    if world=="INTERCEPT_SHIFT_ALIAS":
        assert delta==(ONE,ONE,ONE) and not flags["raw_scalar_intercepts_equal"]
    if world=="STRICT_RESIDUAL_VARIANCE_CHANGE":
        assert b[1][0][0]==5 and a[1][0][0]==2
        assert flags["raw_configural_equal"] and flags["raw_metric_equal"] and flags["raw_scalar_intercepts_equal"]
        assert not flags["raw_strict_residual_variances_equal"]
    if world=="PARTIAL_SCALAR_ITEM1":
        assert delta==(ONE,ZERO,ZERO)
    if world=="LATENT_SCALE_ALIAS":
        assert a==b and not flags["raw_metric_equal"]
    if world=="CONFIGURAL_ITEM3_DETACHED":
        assert not flags["raw_configural_equal"]
    return dict(world=world,original_complete_exogenous_source_atoms=len(data),
       group_conditional_means={str(g):[str(x) for x in group_stats_from_observed_source(world,g)[0]] for g in (0,1)},
       group_conditional_covariances={str(g):[[str(x) for x in row] for row in group_stats_from_observed_source(world,g)[1]] for g in (0,1)},
       group_observed_mean_differences=[str(x) for x in delta],
       oracle_group_true_latent_mean_difference=str(F(params(world,1)["latent_shift"])-F(params(world,0)["latent_shift"])),
       oracle_group_true_latent_variances=[str(F(params(world,g)["latent_scale"])**2) for g in (0,1)],
       raw_structural_parameter_invariance=flags,
       all_observed_joint_mass_cells=sum(x>0 for x in observable_joint(world).values()),
       full_observed_group_item_joint={",".join(str(x) for x in k):str(v) for k,v in observable_joint(world).items()})

def generate():
    alias_certificates()
    results=[world_result(w) for w in WORLD_GROUP1]
    out=dict(research_id="R233",original_catalogue_id="10-007",
        prescore_protocol_commit=FREEZE,scientific_scope="FINITE_ARTIFICIAL_E1_CROSS_GROUP_MEASUREMENT_INVARIANCE",
        frozen_worlds=8,full_original_exogenous_source_atoms=256,
        full_observable_distribution_mean_vs_intercept_alias=True,
        full_observable_distribution_scale_reanchoring_alias=True,
        new_real_human_E2=0,new_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",world_results=results)
    src=HERE/"R233_ALL_256_ORIGINAL_TWO_GROUP_MEASUREMENT_SOURCES.csv"
    fields=list(atom("FULL_STRICT_INVARIANT",0,1,1,1,1))
    with src.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");wr.writeheader()
        for w in WORLD_GROUP1:
            for row in sources(w):
                wr.writerow({k:str(row[k]) for k in fields})
    res=HERE/"R233_EXACT_RESULTS.json"
    res.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(research_id="R233",original_catalogue_id="10-007",
        frozen_worlds=8,original_source_atoms=256,
        independent_source_means_and_analytic_parameter_moments=True,
        full_observation_mean_and_intercept_alias=True,
        full_observation_coordinate_scale_alias=True,
        source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
        result_sha256=hashlib.sha256(res.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R233_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(WORLD_GROUP1),8)
    def test_source_count(self):self.assertEqual(sum(len(sources(w)) for w in WORLD_GROUP1),256)
    def test_aliases(self):self.assertTrue(alias_certificates())
    def test_real_mean_different(self):
        a=world_result("TRUE_LATENT_MEAN_SHIFT")
        b=world_result("INTERCEPT_SHIFT_ALIAS")
        self.assertEqual(a["full_observed_group_item_joint"],b["full_observed_group_item_joint"])
        self.assertEqual([a["oracle_group_true_latent_mean_difference"],b["oracle_group_true_latent_mean_difference"]],["1","0"])
    def test_strict_residual(self):
        x=world_result("STRICT_RESIDUAL_VARIANCE_CHANGE")
        self.assertEqual(x["group_conditional_covariances"]["1"][0][0],"5")
    def test_configural(self):
        self.assertFalse(raw_invariance("CONFIGURAL_ITEM3_DETACHED")["raw_configural_equal"])
    def test_metric(self):
        self.assertFalse(raw_invariance("METRIC_LOADING_CHANGE")["raw_metric_equal"])
    def test_metric_scale_alias(self):
        a=world_result("LATENT_SCALE_ALIAS")
        self.assertFalse(a["raw_structural_parameter_invariance"]["raw_metric_equal"])
        self.assertEqual(a["group_conditional_covariances"]["0"],a["group_conditional_covariances"]["1"])
    def test_partial_scalar(self):
        self.assertEqual(world_result("PARTIAL_SCALAR_ITEM1")["group_observed_mean_differences"],["1","0","0"])
    def test_invariant_shift(self):
        a=world_result("TRUE_LATENT_MEAN_SHIFT")
        self.assertTrue(all(a["raw_structural_parameter_invariance"].values()))
    def test_unknown_world(self):
        with self.assertRaises(ValueError):sources("UNKNOWN")
    def test_bad_source(self):
        with self.assertRaises(ValueError):atom("FULL_STRICT_INVARIANT",0,1,0,1,1)

def _case(world,kind):
    def t(self):
        rows=sources(world)
        if kind=="mass":
            self.assertEqual(sum((r["original_probability"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({(r["observed_group_G"],r["oracle_original_T"],r["independent_E1"],r["independent_E2"],r["independent_E3"]) for r in rows}),32)
        elif kind=="conditional":
            for g in (0,1):
                self.assertEqual(sum((r["original_probability"] for r in rows if r["observed_group_G"]==g),ZERO),F(1,2))
        elif kind=="analytic":
            for g in (0,1):
                self.assertEqual(group_stats_from_observed_source(world,g),independent_analytic_group_stats(world,g))
        elif kind=="joint":
            self.assertEqual(sum(observable_joint(world).values(),ZERO),ONE)
        elif kind=="summary":
            self.assertEqual(world_result(world)["original_complete_exogenous_source_atoms"],32)
        else:raise AssertionError("invalid test")
    return t

for _world in WORLD_GROUP1:
    for _kind in ("mass","unique","conditional","analytic","joint","summary"):
        setattr(Tests,"test_"+_world.lower()+"_"+_kind,_case(_world,_kind))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    opts=parser.parse_args()
    if opts.test:unittest.main(argv=["r233"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
