#!/usr/bin/env python3
"""R234: exact longitudinal three-item, two-wave measurement-invariance worlds.

Nine frozen artificial worlds with 256 equally weighted paired exogenous source
states each. Six-item observed joint probabilities are distinct from the hidden
stable trait, innovation, true change and frozen measurement parameters.
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
Z=F(0)
ONE=F(1)
FREEZE="90f38f8a922650e2084d5ba64ce938aaf7754afa"
SOURCE_NAMES=("T","H","E01","E02","E03","E11","E12","E13")
OBS_KEYS=tuple(f"observed_X{t}{j}" for t in (0,1) for j in (1,2,3))
BASE=dict(scale=1,innovation=0,shift=0,intercept=(0,0,0),
          loading=(1,1,1),error=(1,1,1),persist_first=False)
WORLD_OVERRIDES={
 "STABLE_BASE":{},
 "TRUE_LATENT_SHIFT":{"shift":1},
 "UNIFORM_INTERCEPT_DRIFT_ALIAS":{"intercept":(1,1,1)},
 "LATENT_INNOVATION":{"innovation":1},
 "SINGLE_ITEM_INTERCEPT_DRIFT":{"intercept":(1,0,0)},
 "METRIC_ITEM1_DRIFT":{"loading":(2,1,1)},
 "ERROR_VARIANCE_DRIFT":{"error":(2,1,1)},
 "PERSISTENT_FIRST_ITEM_ERROR":{"persist_first":True},
 "LATENT_SCALE_REANCHOR_ALIAS":{"scale":2,"loading":(F(1,2),F(1,2),F(1,2))}
}

def config(world):
    if world not in WORLD_OVERRIDES:raise ValueError("unfrozen world")
    d=dict(BASE)
    d.update(WORLD_OVERRIDES[world])
    return d

def atom(world,*bits):
    if len(bits)!=8 or any(v not in (-1,1) for v in bits):
        raise ValueError("invalid original paired source")
    cfg=config(world)
    q=dict(zip(SOURCE_NAMES,bits))
    f0=F(q["T"])
    f1=F(cfg["scale"])*q["T"]+F(cfg["innovation"])*q["H"]+F(cfg["shift"])
    x0=tuple(f0+q[f"E0{j}"] for j in (1,2,3))
    x1=tuple(F(cfg["intercept"][j-1])+F(cfg["loading"][j-1])*f1+
             F(cfg["error"][j-1])*q[f"E0{j}" if j==1 and cfg["persist_first"] else f"E1{j}"]
             for j in (1,2,3))
    row={"world":world}
    for k in SOURCE_NAMES:row["oracle_"+k]=q[k]
    row.update(oracle_F0=f0,oracle_F1=f1,
               oracle_true_individual_latent_change=f1-f0,
               original_source_probability=F(1,256))
    for j in (1,2,3):
        row[f"observed_X0{j}"]=x0[j-1]
        row[f"observed_X1{j}"]=x1[j-1]
        row[f"observed_paired_difference_item{j}"]=x1[j-1]-x0[j-1]
    row["observed_composite_S0"]=sum(x0,Z)/3
    row["observed_composite_S1"]=sum(x1,Z)/3
    row["observed_composite_change"]=row["observed_composite_S1"]-row["observed_composite_S0"]
    return row

def sources(world):
    c=config(world)
    del c
    rows=tuple(atom(world,*xs) for xs in itertools.product((-1,1),repeat=8))
    if len(rows)!=256 or sum((r["original_source_probability"] for r in rows),Z)!=ONE:
        raise AssertionError("missing full paired original source probability")
    return rows

def mean_covariance(rows,keys):
    if sum((r["original_source_probability"] for r in rows),Z)!=ONE:
        raise AssertionError("incomplete source mass")
    mu={k:sum((r["original_source_probability"]*r[k] for r in rows),Z) for k in keys}
    cov={(a,b):sum((r["original_source_probability"]*(r[a]-mu[a])*(r[b]-mu[b])
                    for r in rows),Z) for a in keys for b in keys}
    return mu,cov

def linear_coefficients(world):
    """Entirely independent of source enumeration: 8D coefficient vectors."""
    c=config(world)
    vectors={}
    means={}
    for j in (1,2,3):
        v=[Z]*8
        v[0]=ONE
        v[1+j]=ONE # E01 is index2.
        vectors[f"observed_X0{j}"]=tuple(v)
        means[f"observed_X0{j}"]=Z
        z=[Z]*8
        lam=F(c["loading"][j-1])
        z[0]=lam*F(c["scale"])
        z[1]=lam*F(c["innovation"])
        error_index=(1+j) if j==1 and c["persist_first"] else 4+j
        z[error_index]+=F(c["error"][j-1])
        vectors[f"observed_X1{j}"]=tuple(z)
        means[f"observed_X1{j}"]=F(c["intercept"][j-1])+lam*F(c["shift"])
    return means,vectors

def analytic_mean_covariance(world):
    mu,v=linear_coefficients(world)
    cov={(a,b):sum((v[a][i]*v[b][i] for i in range(8)),Z)
         for a in OBS_KEYS for b in OBS_KEYS}
    return mu,cov

def analytic_true_change(world):
    c=config(world)
    return (F(c["shift"]),
            (F(c["scale"])-1)**2+F(c["innovation"])**2,
            F(c["scale"]),F(c["scale"])**2+F(c["innovation"])**2)

def source_true_change(world):
    rows=sources(world)
    keys=("oracle_F0","oracle_F1","oracle_true_individual_latent_change")
    mu,cov=mean_covariance(rows,keys)
    return (mu[keys[2]],cov[keys[2],keys[2]],
            cov[keys[0],keys[1]],cov[keys[1],keys[1]])

def observable_joint(world):
    out=defaultdict(F)
    for r in sources(world):
        out[tuple(r[k] for k in OBS_KEYS)]+=r["original_source_probability"]
    if sum(out.values(),Z)!=ONE:raise AssertionError("observable probability mass mismatch")
    return dict(sorted(out.items()))

def sourcewise_aliases():
    for w,v in (("TRUE_LATENT_SHIFT","UNIFORM_INTERCEPT_DRIFT_ALIAS"),
                ("STABLE_BASE","LATENT_SCALE_REANCHOR_ALIAS")):
        for a,b in zip(sources(w),sources(v)):
            if any(a[k]!=b[k] for k in OBS_KEYS):
                raise AssertionError("frozen identical observed paired source alias changed")
        if observable_joint(w)!=observable_joint(v):
            raise AssertionError("full six dimensional observable alias broken")
    assert source_true_change("TRUE_LATENT_SHIFT")[0]==ONE
    assert source_true_change("UNIFORM_INTERCEPT_DRIFT_ALIAS")[0]==Z
    return True

def world_result(world):
    rows=sources(world)
    mu,cv=mean_covariance(rows,OBS_KEYS)
    analyt_mu,analyt_cv=analytic_mean_covariance(world)
    if mu!=analyt_mu or cv!=analyt_cv:
        raise AssertionError("source-level 6x6 observed covariance not equal independent 8D path coefficients")
    true=source_true_change(world)
    if true!=analytic_true_change(world):
        raise AssertionError("analytic latent change does not match complete source oracle")
    key="observed_composite_change"
    c_mu,c_cv=mean_covariance(rows,(key,))
    change_mean=c_mu[key]
    change_var=c_cv[key,key]
    signs={f"observed_X0{j}":F(-1,3) for j in (1,2,3)}
    signs.update({f"observed_X1{j}":F(1,3) for j in (1,2,3)})
    independent_change_mean=sum((signs[k]*analyt_mu[k] for k in OBS_KEYS),Z)
    independent_change_var=sum((signs[a]*signs[b]*analyt_cv[a,b]
                                for a in OBS_KEYS for b in OBS_KEYS),Z)
    if (change_mean,change_var)!=(independent_change_mean,independent_change_var):
        raise AssertionError("paired composite observed change independently disagrees")
    differences=tuple(mu[f"observed_X1{j}"]-mu[f"observed_X0{j}"] for j in (1,2,3))
    if world=="TRUE_LATENT_SHIFT":
        assert differences==(ONE,ONE,ONE) and true[0]==ONE
    if world=="UNIFORM_INTERCEPT_DRIFT_ALIAS":
        assert differences==(ONE,ONE,ONE) and true[0]==Z
    if world=="SINGLE_ITEM_INTERCEPT_DRIFT":
        assert differences==(ONE,Z,Z)
    if world=="LATENT_INNOVATION":
        assert true[0]==Z and true[1]==ONE and cv["observed_X11","observed_X12"]==2
    if world=="ERROR_VARIANCE_DRIFT":
        assert cv["observed_X11","observed_X11"]==5
        assert cv["observed_X11","observed_X12"]==ONE
    if world=="PERSISTENT_FIRST_ITEM_ERROR":
        assert cv["observed_X01","observed_X11"]==2
        assert cv["observed_X01","observed_X12"]==ONE
    raw_c=config(world)
    raw_metric=tuple(F(x) for x in raw_c["loading"])==(ONE,ONE,ONE)
    raw_scalar=tuple(F(x) for x in raw_c["intercept"])==(Z,Z,Z)
    raw_residual=tuple(F(x)**2 for x in raw_c["error"])==(ONE,ONE,ONE)
    if world=="LATENT_SCALE_REANCHOR_ALIAS":
        assert not raw_metric and differences==(Z,Z,Z)
    return dict(
        world=world,
        full_original_paired_source_atoms=256,
        all_observed_six_variable_means=[str(mu[k]) for k in OBS_KEYS],
        all_observed_six_by_six_covariance=[[str(cv[a,b]) for b in OBS_KEYS] for a in OBS_KEYS],
        observed_per_item_time1_minus_time0_means=[str(x) for x in differences],
        observed_composite_change_mean=str(change_mean),
        observed_composite_change_variance=str(change_var),
        oracle_true_individual_latent_change_mean=str(true[0]),
        oracle_true_individual_latent_change_variance=str(true[1]),
        oracle_true_time0_time1_latent_covariance=str(true[2]),
        oracle_true_time1_latent_variance=str(true[3]),
        raw_parameter_invariance={
            "raw_loading_equal_to_time0":raw_metric,
            "raw_item_intercept_equal_to_time0":raw_scalar,
            "raw_item_error_variance_equal_to_time0":raw_residual,
            "cross_wave_first_item_error_independent":not raw_c["persist_first"]
        },
        exact_full_paired_observed_joint={
            ",".join(map(str,k)):str(v) for k,v in observable_joint(world).items()
        }
    )

def generate():
    sourcewise_aliases()
    result={
        "research_id":"R234","original_catalogue_id":"10-008",
        "prescore_protocol_commit":FREEZE,
        "scientific_scope":"FINITE_ARTIFICIAL_E1_PAIRED_LONGITUDINAL_MEASUREMENT",
        "worlds":9,"original_paired_exogenous_source_rows":2304,
        "full_six_item_sourcewise_aliases_verified":True,
        "independent_observed_covariance_and_true_change_verified":True,
        "new_real_human_E2":0,"new_real_historical_E3":0,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN",
        "world_results":[world_result(w) for w in WORLD_OVERRIDES]
    }
    outfile=HERE/"R234_ALL_2304_ORIGINAL_TWO_WAVE_SOURCES.csv"
    keys=list(atom("STABLE_BASE",*([1]*8)))
    with outfile.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=keys,lineterminator="\n")
        writer.writeheader()
        for w in WORLD_OVERRIDES:
            for row in sources(w):
                writer.writerow({k:str(row[k]) for k in keys})
    outfile2=HERE/"R234_EXACT_RESULTS.json"
    outfile2.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={
        "research_id":"R234","original_catalogue_id":"10-008",
        "worlds":9,"original_full_paired_source_atoms":2304,
        "independent_eight_basis_covariance_parity":True,
        "independent_latent_change_oracle_parity":True,
        "paired_sixdimensional_observation_aliases":2,
        "source_sha256":hashlib.sha256(outfile.read_bytes()).hexdigest(),
        "results_sha256":hashlib.sha256(outfile2.read_bytes()).hexdigest(),
        "new_real_human_E2":0,"new_real_historical_E3":0
    }
    (HERE/"R234_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_nine_worlds(self):self.assertEqual(len(WORLD_OVERRIDES),9)
    def test_2304_sources(self):
        self.assertEqual(sum(len(sources(w)) for w in WORLD_OVERRIDES),2304)
    def test_sourcewise_alias(self):self.assertTrue(sourcewise_aliases())
    def test_true_shift_distinguished(self):
        a=world_result("TRUE_LATENT_SHIFT")
        b=world_result("UNIFORM_INTERCEPT_DRIFT_ALIAS")
        self.assertEqual(a["exact_full_paired_observed_joint"],b["exact_full_paired_observed_joint"])
        self.assertEqual([a["oracle_true_individual_latent_change_mean"],
                          b["oracle_true_individual_latent_change_mean"]],["1","0"])
    def test_scale_reanchoring(self):
        a=world_result("STABLE_BASE")
        b=world_result("LATENT_SCALE_REANCHOR_ALIAS")
        self.assertEqual(a["exact_full_paired_observed_joint"],b["exact_full_paired_observed_joint"])
        self.assertFalse(b["raw_parameter_invariance"]["raw_loading_equal_to_time0"])
    def test_latent_innovation(self):
        x=world_result("LATENT_INNOVATION")
        self.assertEqual(x["oracle_true_individual_latent_change_variance"],"1")
        self.assertEqual(x["oracle_true_individual_latent_change_mean"],"0")
    def test_error_variance(self):
        x=world_result("ERROR_VARIANCE_DRIFT")
        self.assertEqual(x["all_observed_six_by_six_covariance"][3][3],"5")
        self.assertEqual(x["all_observed_six_by_six_covariance"][3][4],"1")
    def test_error_persistence(self):
        x=world_result("PERSISTENT_FIRST_ITEM_ERROR")
        self.assertEqual(x["all_observed_six_by_six_covariance"][0][3],"2")
        self.assertEqual(x["all_observed_six_by_six_covariance"][0][4],"1")
    def test_one_item_change(self):
        self.assertEqual(world_result("SINGLE_ITEM_INTERCEPT_DRIFT")[
            "observed_per_item_time1_minus_time0_means"],["1","0","0"])
    def test_stable_composite_variance(self):
        self.assertEqual(world_result("STABLE_BASE")["observed_composite_change_variance"],"2/3")
    def test_persistent_composite_variance(self):
        self.assertEqual(world_result("PERSISTENT_FIRST_ITEM_ERROR")["observed_composite_change_variance"],"4/9")
    def test_bad_world(self):
        with self.assertRaises(ValueError):config("UNKNOWN")

def _case(world,kind):
    def check(self):
        rows=sources(world)
        if kind=="source_mass":
            self.assertEqual(sum((r["original_source_probability"] for r in rows),Z),ONE)
        elif kind=="source_uniqueness":
            self.assertEqual(len({tuple(r["oracle_"+k] for k in SOURCE_NAMES) for r in rows}),256)
        elif kind=="observed_moments":
            self.assertEqual(mean_covariance(rows,OBS_KEYS),analytic_mean_covariance(world))
        elif kind=="oracle_moments":
            self.assertEqual(source_true_change(world),analytic_true_change(world))
        elif kind=="observed_joint_mass":
            self.assertEqual(sum(observable_joint(world).values(),Z),ONE)
        elif kind=="world_output":
            self.assertEqual(world_result(world)["full_original_paired_source_atoms"],256)
        else:raise AssertionError("unfrozen test")
    return check
for _w in WORLD_OVERRIDES:
    for _kind in ("source_mass","source_uniqueness","observed_moments","oracle_moments",
                  "observed_joint_mass","world_output"):
        setattr(Tests,f"test_{_w.lower()}_{_kind}",_case(_w,_kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["r234"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
