#!/usr/bin/env python3
"""R232: complete finite structural equation and measurement path counterexamples.

All coefficient models were frozen before results. Every original exogenous
U,R,EM,EY,EW,EZ1,EZ2 type is retained. Observed A/W/Y/Z1/Z2 moments never
consume oracle potentials or unmeasured mediators. Intervention truth is
independently recomputed from fixed structural coefficients.
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
FREEZE="d04ae67b1cdb1a94a783da3df36f88080a65fa70"
SOURCES=("U","R","EM","EY","EW","EZ1","EZ2")
OBS=("A","W","Y","Z1","Z2")
# (source for treatment A, m_A, m_U, y_M, y_A, y_U, measurement error on W)
WORLDS={
 "RANDOMIZED_MEDIATED":("R",1,0,1,0,0,0),
 "RANDOMIZED_NULL":("R",0,1,1,0,0,0),
 "LATENT_CAUSAL_ALIAS":("U",1,0,1,0,0,0),
 "LATENT_COMMON_ALIAS":("U",0,1,1,0,0,0),
 "RANDOMIZED_DIRECT_AND_MEDIATED":("R",1,0,1,1,0,0),
 "RANDOMIZED_MEDIATOR_CONFOUNDED":("R",1,1,1,0,1,0),
 "RANDOMIZED_DIRECT_ONLY":("R",0,1,1,1,0,0),
 "RANDOMIZED_MEDIATOR_MEASUREMENT_ERROR":("R",1,0,1,0,0,1),
}
FROZEN_ORACLE={
 "RANDOMIZED_MEDIATED":("1","0","1"),
 "RANDOMIZED_NULL":("0","0","0"),
 "LATENT_CAUSAL_ALIAS":("1","0","1"),
 "LATENT_COMMON_ALIAS":("0","0","0"),
 "RANDOMIZED_DIRECT_AND_MEDIATED":("2","1","1"),
 "RANDOMIZED_MEDIATOR_CONFOUNDED":("1","0","1"),
 "RANDOMIZED_DIRECT_ONLY":("1","1","0"),
 "RANDOMIZED_MEDIATOR_MEASUREMENT_ERROR":("1","0","1"),
}
def model(world):
    if world not in WORLDS:raise ValueError("unfrozen SEM world")
    return WORLDS[world]

def atom(world,*source_bits):
    p=model(world)
    if len(source_bits)!=7 or any(v not in (-1,1) for v in source_bits):
        raise ValueError("invalid original exogenous source")
    source=dict(zip(SOURCES,source_bits))
    u=source["U"]
    a=source[p[0]]
    m=p[1]*a+p[2]*u+source["EM"]
    y=p[3]*m+p[4]*a+p[5]*u+source["EY"]
    w=m+p[6]*source["EW"]
    z1=u+source["EZ1"]
    z2=u+source["EZ2"]
    m0=-p[1]+p[2]*u+source["EM"]
    m1=p[1]+p[2]*u+source["EM"]
    y0=p[3]*m0-p[4]+p[5]*u+source["EY"]
    y1=p[3]*m1+p[4]+p[5]*u+source["EY"]
    # Controlled direct at actual M; mediator path holds the factual A.
    direct_0=p[3]*m-p[4]+p[5]*u+source["EY"]
    direct_1=p[3]*m+p[4]+p[5]*u+source["EY"]
    indirect_0=p[3]*m0+p[4]*a+p[5]*u+source["EY"]
    indirect_1=p[3]*m1+p[4]*a+p[5]*u+source["EY"]
    row={"world":world}
    for key,val in source.items():row["oracle_original_"+key]=val
    row.update(observed_A=a,observed_W=w,observed_Y=y,observed_Z1=z1,observed_Z2=z2,
               oracle_true_M=m,oracle_M_doAminus1=m0,oracle_M_doAplus1=m1,
               oracle_Y_doAminus1=y0,oracle_Y_doAplus1=y1,
               oracle_Y_at_fixedM_Aminus1=direct_0,oracle_Y_at_fixedM_Aplus1=direct_1,
               oracle_Y_at_actualA_MdoMinus1=indirect_0,
               oracle_Y_at_actualA_MdoPlus1=indirect_1,
               original_source_probability=F(1,128))
    return row

def sources(world):
    rows=tuple(atom(world,*bits) for bits in itertools.product((-1,1),repeat=7))
    if len(rows)!=128 or sum((r["original_source_probability"] for r in rows),ZERO)!=ONE:
        raise AssertionError("original full structural source mass invalid")
    return rows

def observable_covariance(rows):
    # Only actual five observed variables and source weights. No true M.
    mean={k:sum((r["original_source_probability"]*r["observed_"+k]
                  for r in rows),ZERO) for k in OBS}
    cov={(x,y):sum((r["original_source_probability"]*
                 (r["observed_"+x]-mean[x])*(r["observed_"+y]-mean[y])
                 for r in rows),ZERO) for x in OBS for y in OBS}
    return mean,cov

def analytical_vectors(world):
    """Independent SEM path tracing via seven fixed exogenous coefficients."""
    p=model(world)
    e={k:tuple(F(int(i==j)) for i in range(7)) for j,k in enumerate(SOURCES)}
    def combine(*terms):
        return tuple(sum((F(c)*v[j] for c,v in terms),ZERO) for j in range(7))
    a=e[p[0]]
    m=combine((p[1],a),(p[2],e["U"]),(1,e["EM"]))
    y=combine((p[3],m),(p[4],a),(p[5],e["U"]),(1,e["EY"]))
    w=combine((1,m),(p[6],e["EW"]))
    z1=combine((1,e["U"]),(1,e["EZ1"]))
    z2=combine((1,e["U"]),(1,e["EZ2"]))
    return dict(A=a,W=w,Y=y,Z1=z1,Z2=z2)

def analytic_covariance(world):
    vect=analytical_vectors(world)
    return {(a,b):sum((vect[a][j]*vect[b][j] for j in range(7)),ZERO)
            for a in OBS for b in OBS}

def observed_paths(c):
    va=c["A","A"]; vw=c["W","W"]
    am=c["A","W"]; ay=c["A","Y"]; my=c["W","Y"]
    det=va*vw-am**2
    if va<=0 or det<=0:raise AssertionError("prescore OLS covariance singular")
    total=ay/va
    proxy_a_w=am/va
    conditional_w=(my*va-ay*am)/det
    conditional_a=(ay*vw-my*am)/det
    proxy_indirect=proxy_a_w*conditional_w
    if conditional_a+proxy_indirect!=total:
        raise AssertionError("observed path OLS algebra inconsistent")
    return dict(
       observational_total_A_to_Y=total,
       observational_A_to_measured_W=proxy_a_w,
       observational_Y_on_measured_W_control_A=conditional_w,
       observational_Y_on_A_control_measured_W=conditional_a,
       observational_product_proxy_mediation=proxy_indirect,
       observational_sum_direct_plus_proxy_mediation=conditional_a+proxy_indirect,
       observed_covariance_A_Z1=c["A","Z1"],
       observed_covariance_Z1_Z2=c["Z1","Z2"]
    )

def oracle_truth(rows):
    def avg_half(a,b):
        return sum((r["original_source_probability"]*
                    F(r[b]-r[a],2) for r in rows),ZERO)
    results={
      "true_total_doA_slope":avg_half("oracle_Y_doAminus1","oracle_Y_doAplus1"),
      "true_direct_at_fixed_M":avg_half("oracle_Y_at_fixedM_Aminus1","oracle_Y_at_fixedM_Aplus1"),
      "true_mediated_at_actual_A":avg_half("oracle_Y_at_actualA_MdoMinus1","oracle_Y_at_actualA_MdoPlus1")
    }
    if results["true_total_doA_slope"]!=results["true_direct_at_fixed_M"]+results["true_mediated_at_actual_A"]:
        raise AssertionError("true direct + mediated != total under frozen structural world")
    return results

def independent_oracle_coefficients(world):
    p=model(world)
    return {
      "true_total_doA_slope":F(p[4]+p[3]*p[1]),
      "true_direct_at_fixed_M":F(p[4]),
      "true_mediated_at_actual_A":F(p[3]*p[1])
    }

def observed_joint(world):
    out=defaultdict(F)
    for r in sources(world):
        out[tuple(r["observed_"+k] for k in OBS)]+=r["original_source_probability"]
    return dict(sorted(out.items()))

def sourcewise_alias():
    one=sources("LATENT_CAUSAL_ALIAS")
    two=sources("LATENT_COMMON_ALIAS")
    for a,b in zip(one,two):
        for key in OBS:
            if a["observed_"+key]!=b["observed_"+key]:
                raise AssertionError("two causal SEM worlds differ in observed measurements")
    if observed_joint("LATENT_CAUSAL_ALIAS")!=observed_joint("LATENT_COMMON_ALIAS"):
        raise AssertionError("complete SEM observational alias failed")
    return True

def world_result(world):
    rows=sources(world)
    mu,c=observable_covariance(rows)
    independent=analytic_covariance(world)
    if c!=independent or any(v!=0 for v in mu.values()):
        raise AssertionError("observed source and independent path tracing disagree")
    obs=observed_paths(c)
    true=oracle_truth(rows)
    if true!=independent_oracle_coefficients(world):
        raise AssertionError("sourcewise oracle not equal structural coefficient effects")
    if tuple(map(str,(true["true_total_doA_slope"],true["true_direct_at_fixed_M"],
                      true["true_mediated_at_actual_A"])))!=FROZEN_ORACLE[world]:
        raise AssertionError("frozen true mediation effects changed")
    if world=="RANDOMIZED_MEDIATOR_CONFOUNDED":
        assert obs["observational_Y_on_measured_W_control_A"]==F(3,2)
        assert obs["observational_Y_on_A_control_measured_W"]==F(-1,2)
    if world=="RANDOMIZED_MEDIATOR_MEASUREMENT_ERROR":
        assert obs["observational_Y_on_measured_W_control_A"]==F(1,2)
        assert obs["observational_Y_on_A_control_measured_W"]==F(1,2)
    return dict(
      world=world,all_original_complete_source_atoms=len(rows),
      true_structural_coefficients=list(model(world)),
      true_structural_effects={k:str(v) for k,v in true.items()},
      observed_linear_path_regression={k:str(v) for k,v in obs.items()},
      actual_observed_covariance=[
        [str(c[a,b]) for b in OBS] for a in OBS],
      observed_joint_support_cells=sum(v>0 for v in observed_joint(world).values()),
      full_five_variable_observed_joint={
          ",".join(map(str,k)):str(v) for k,v in observed_joint(world).items()
      }
    )

def generate():
    sourcewise_alias()
    all_worlds=[world_result(w) for w in WORLDS]
    dataset=dict(
      research_id="R232",original_catalogue_id="10-006",
      prescore_freeze_commit=FREEZE,
      scientific_scope="FINITE_ARTIFICIAL_E1_SEM_MEDIATION_AND_MEASUREMENT",
      original_worlds=8,original_full_exogenous_source_atoms=1024,
      entire_observed_joint_alias_and_different_intervention_truth=True,
      independent_structural_path_tracing_and_oracle_checks=True,
      new_real_human_E2=0,new_real_historical_E3=0,
      R073="FROZEN",PESEN_v0_1="FROZEN",
      world_results=all_worlds
    )
    outfile=HERE/"R232_ALL_1024_ORIGINAL_SEM_EXOGENOUS_SOURCES.csv"
    fields=list(atom("RANDOMIZED_MEDIATED",*([1]*7)))
    with outfile.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        writer.writeheader()
        for world in WORLDS:
            for row in sources(world):
                writer.writerow({k:str(row[k]) for k in fields})
    rpath=HERE/"R232_EXACT_RESULTS.json"
    rpath.write_text(json.dumps(dataset,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    machine=dict(
      research_id="R232",original_catalogue_id="10-006",
      worlds=8,all_full_original_source_atoms=1024,
      independent_observed_covariance_path_tracing_verified=True,
      independent_structural_intervention_oracle_verified=True,
      fully_matching_observed_five_variable_alias=True,
      sources_sha256=hashlib.sha256(outfile.read_bytes()).hexdigest(),
      results_sha256=hashlib.sha256(rpath.read_bytes()).hexdigest(),
      new_real_human_E2=0,new_real_historical_E3=0
    )
    (HERE/"R232_FINAL_MACHINE_ACCEPTANCE.json").write_text(
      json.dumps(machine,indent=2)+"\n",encoding="utf-8")
    return machine

class Tests(unittest.TestCase):
    def test_eight_worlds(self):self.assertEqual(len(WORLDS),8)
    def test_total_atoms(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),1024)
    def test_full_observation_alias(self):self.assertTrue(sourcewise_alias())
    def test_distinct_true_effect(self):
        self.assertEqual(oracle_truth(sources("LATENT_CAUSAL_ALIAS"))["true_total_doA_slope"],1)
        self.assertEqual(oracle_truth(sources("LATENT_COMMON_ALIAS"))["true_total_doA_slope"],0)
    def test_mediation_bias_with_random_treatment(self):
        p=observed_paths(observable_covariance(sources("RANDOMIZED_MEDIATOR_CONFOUNDED"))[1])
        self.assertEqual((p["observational_total_A_to_Y"],p["observational_product_proxy_mediation"],
                          p["observational_Y_on_A_control_measured_W"]),(1,F(3,2),F(-1,2)))
    def test_proxy_measurement_error(self):
        p=observed_paths(observable_covariance(sources("RANDOMIZED_MEDIATOR_MEASUREMENT_ERROR"))[1])
        self.assertEqual((p["observational_product_proxy_mediation"],
                          p["observational_Y_on_A_control_measured_W"]),(F(1,2),F(1,2)))
    def test_direct_plus_mediated(self):
        p=oracle_truth(sources("RANDOMIZED_DIRECT_AND_MEDIATED"))
        self.assertEqual(tuple(map(str,p.values())),("2","1","1"))
    def test_randomized_null(self):
        self.assertEqual(oracle_truth(sources("RANDOMIZED_NULL"))["true_total_doA_slope"],0)
    def test_random_source_marker_cov_zero(self):
        p=observed_paths(observable_covariance(sources("RANDOMIZED_MEDIATED"))[1])
        self.assertEqual(p["observed_covariance_A_Z1"],0)
    def test_alias_source_marker_cov_one(self):
        p=observed_paths(observable_covariance(sources("LATENT_COMMON_ALIAS"))[1])
        self.assertEqual(p["observed_covariance_A_Z1"],1)
    def test_marker_crosscov_one(self):
        for w in WORLDS:
            self.assertEqual(analytic_covariance(w)["Z1","Z2"],1)
    def test_unknown_world(self):
        with self.assertRaises(ValueError):sources("NONEXISTENT")

def _case(world,kind):
    def test(self):
        rows=sources(world)
        if kind=="mass":
            self.assertEqual(sum((r["original_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({tuple(r["oracle_original_"+k] for k in SOURCES) for r in rows}),128)
        elif kind=="covariance":
            self.assertEqual(observable_covariance(rows)[1],analytic_covariance(world))
        elif kind=="structural_oracle":
            self.assertEqual(oracle_truth(rows),independent_oracle_coefficients(world))
        elif kind=="observed_path":
            self.assertEqual(observed_paths(observable_covariance(rows)[1])["observational_sum_direct_plus_proxy_mediation"],
                             observed_paths(observable_covariance(rows)[1])["observational_total_A_to_Y"])
        elif kind=="result":
            self.assertEqual(world_result(world)["all_original_complete_source_atoms"],128)
        else:raise AssertionError("unfrozen test")
    return test

for _w in WORLDS:
    for _kind in ("mass","unique","covariance","structural_oracle","observed_path","result"):
        setattr(Tests,"test_"+_w.lower()+"_"+_kind,_case(_w,_kind))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    opts=parser.parse_args()
    if opts.test:unittest.main(argv=["r232"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
