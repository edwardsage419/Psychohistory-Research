#!/usr/bin/env python3
"""R231 exact CFA finite-population covariance and tetrad checks.

Eight prescore-frozen artificial worlds, 64 independent exogenous types each.
Observed covariance and tetrads never require latent U/T. Oracle conditional-T
residual covariance is evaluated separately and never treated as identified.
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
FREEZE="8e7924a2f14710440c78665a7e8ce35fe508b486"
WORLDS={
 "ONE_FACTOR_VALID":((1,0),(1,0),(1,0),(1,0)),
 "ONE_FACTOR_SIGNED":((1,0),(1,0),(-1,0),(1,0)),
 "TWO_FACTOR_BLOCK":((1,0),(1,0),(0,1),(0,1)),
 "CORRELATED_RESIDUAL_METHOD":((1,1),(1,1),(1,0),(1,0)),
 "SECOND_FACTOR_SEMANTIC_ALIAS":((1,1),(1,1),(1,0),(1,0)),
 "TETRAD_FALSE_REASSURANCE":((1,1),(1,1),(1,1),(1,1)),
 "CROSS_LOADING_CANCEL":((1,0),(1,0),(1,1),(1,-1)),
 "ONE_FACTOR_UNEQUAL_LOAD":((1,0),(2,0),(1,0),(2,0)),
}
TETRAD_VALID={
 "ONE_FACTOR_VALID","ONE_FACTOR_SIGNED",
 "TETRAD_FALSE_REASSURANCE","ONE_FACTOR_UNEQUAL_LOAD"
}
FROZEN_EXPECTED_TETRADS={
 "ONE_FACTOR_VALID":("0","0","0"),
 "ONE_FACTOR_SIGNED":("0","0","0"),
 "TWO_FACTOR_BLOCK":("1","1","0"),
 "CORRELATED_RESIDUAL_METHOD":("1","1","0"),
 "SECOND_FACTOR_SEMANTIC_ALIAS":("1","1","0"),
 "TETRAD_FALSE_REASSURANCE":("0","0","0"),
 "CROSS_LOADING_CANCEL":("-1","-1","0"),
 "ONE_FACTOR_UNEQUAL_LOAD":("0","0","0"),
}

def atom(world,t,u,e1,e2,e3,e4):
    if world not in WORLDS or any(v not in (-1,1) for v in (t,u,e1,e2,e3,e4)):
        raise ValueError("atom outside frozen source support")
    loads=WORLDS[world]
    E=(e1,e2,e3,e4)
    obs=tuple(F(loads[j][0]*t+loads[j][1]*u+E[j]) for j in range(4))
    d={
        "world":world,"hidden_T":t,"hidden_U":u,
        "independent_E1":e1,"independent_E2":e2,
        "independent_E3":e3,"independent_E4":e4,
        "original_probability":F(1,64),
    }
    for j in range(4):
        d[f"observed_X{j+1}"]=obs[j]
        d[f"oracle_residual_conditional_T_item{j+1}"]=F(loads[j][1]*u+E[j])
    return d

def sources(world):
    if world not in WORLDS:raise ValueError("unfrozen world")
    rows=tuple(atom(world,*bits) for bits in itertools.product((-1,1),repeat=6))
    assert len(rows)==64
    assert sum((r["original_probability"] for r in rows),ZERO)==ONE
    return rows

def covariance_from_original(rows,keys):
    weight=sum((r["original_probability"] for r in rows),ZERO)
    if weight!=ONE:raise AssertionError("unfrozen incomplete mass")
    mean={k:sum((r["original_probability"]*r[k] for r in rows),ZERO) for k in keys}
    cov=tuple(tuple(sum((r["original_probability"]*(r[x]-mean[x])*(r[y]-mean[y])
                     for r in rows),ZERO) for y in keys) for x in keys)
    return tuple(mean[k] for k in keys),cov

def predicted_covariance_from_loads(world):
    # Analytically independent route, no enumeration and no sample covariance.
    ll=WORLDS[world]
    return tuple(tuple(F(ll[i][0]*ll[j][0]+ll[i][1]*ll[j][1]+int(i==j))
                       for j in range(4)) for i in range(4))

def analytical_conditional_T_residual(world):
    ll=WORLDS[world]
    return tuple(tuple(F(ll[i][1]*ll[j][1]+int(i==j))
                       for j in range(4)) for i in range(4))

def observed_joint(world):
    # Uses only the four observed item columns, not T,U or oracle residuals.
    joint=defaultdict(F)
    for r in sources(world):
        joint[tuple(r[f"observed_X{i+1}"] for i in range(4))]+=r["original_probability"]
    return dict(sorted(joint.items()))

def tetrads(c):
    # Explicit 0-based form matching frozen 1-based notation.
    a=c[0][1]*c[2][3]
    b=c[0][2]*c[1][3]
    d=c[0][3]*c[1][2]
    return a-b,a-d,b-d

def strict_equal_loading_discrepancy(c):
    # Exactly prespecified equal loadings=1, Var(T)=1, unique variances=1.
    return sum((abs(c[i][j]-F(1+int(i==j))) for i in range(4) for j in range(i,4)),ZERO)

def sourcewise_alias_checks():
    a=sources("CORRELATED_RESIDUAL_METHOD")
    b=sources("SECOND_FACTOR_SEMANTIC_ALIAS")
    for aa,bb in zip(a,b):
        for i in range(4):
            if aa[f"observed_X{i+1}"]!=bb[f"observed_X{i+1}"]:
                raise AssertionError("semantic pair differ on observed source")
    # Two hidden primitive factors T and U can be reparameterized as W=T+U.
    for row in sources("TETRAD_FALSE_REASSURANCE"):
        w=row["hidden_T"]+row["hidden_U"]
        for j in range(4):
            assert row[f"observed_X{j+1}"]==w+row[f"independent_E{j+1}"]
    # Even if a single factor is true, its numerical scale is not identified.
    for row in sources("ONE_FACTOR_UNEQUAL_LOAD"):
        tprime=F(2*row["hidden_T"])
        new_loads=(F(1,2),ONE,F(1,2),ONE)
        for j in range(4):
            assert row[f"observed_X{j+1}"]==new_loads[j]*tprime+row[f"independent_E{j+1}"]
    assert observed_joint("CORRELATED_RESIDUAL_METHOD")==observed_joint("SECOND_FACTOR_SEMANTIC_ALIAS")
    return True

def world_result(world):
    rows=sources(world)
    keys=tuple(f"observed_X{j+1}" for j in range(4))
    means,c=covariance_from_original(rows,keys)
    a=predicted_covariance_from_loads(world)
    if c!=a or any(m!=0 for m in means):
        raise AssertionError("finite covariance differs from analytically fixed CFA covariance")
    residual_keys=tuple(f"oracle_residual_conditional_T_item{j+1}" for j in range(4))
    er,rc=covariance_from_original(rows,residual_keys)
    if any(m!=0 for m in er) or rc!=analytical_conditional_T_residual(world):
        raise AssertionError("conditional T oracle source vs analytic residual disagree")
    t=tetrads(c)
    if tuple(str(x) for x in t)!=FROZEN_EXPECTED_TETRADS[world]:
        raise AssertionError("frozen tetrad certificate changed")
    if (all(x==0 for x in t))!=(world in TETRAD_VALID):
        raise AssertionError("pre-frozen CFA necessary tetrad status changed")
    if (world=="ONE_FACTOR_VALID")!=(strict_equal_loading_discrepancy(c)==0):
        raise AssertionError("fixed equal load hypothesis unexpected pass/failure")
    nonzero_residual_offdiag=sum(int(rc[i][j]!=0) for i in range(4) for j in range(i+1,4))
    if world=="TETRAD_FALSE_REASSURANCE" and not nonzero_residual_offdiag:
        raise AssertionError("tetrad false reassurance example no longer confounded")
    return {
        "world":world,"original_complete_exogenous_sources":len(rows),
        "population_observed_covariance":[[str(x) for x in row] for row in c],
        "fixed_equal_loading_candidate_absolute_discrepancy":str(strict_equal_loading_discrepancy(c)),
        "three_exact_tetrad_constraints":[str(x) for x in t],
        "all_necessary_one_factor_tetrads_zero":all(x==0 for x in t),
        "oracle_conditional_T_residual_covariance":[[str(x) for x in row] for row in rc],
        "oracle_offdiagonal_conditional_T_residual_nonzero_pairs":nonzero_residual_offdiag,
        "original_observable_support_cells":sum(x>0 for x in observed_joint(world).values()),
        "full_observable_joint_signature":{
            ",".join(map(str,key)):str(v) for key,v in observed_joint(world).items()
        },
    }

def generate():
    sourcewise_alias_checks()
    worlds=[world_result(w) for w in WORLDS]
    result=dict(research_id="R231",original_catalogue_id="10-005",
       scientific_scope="BOUNDED_E1_ARTIFICIAL_EXACT_CFA_TETRAD_ONLY",
       prescore_freeze_commit=FREEZE,
       frozen_worlds=8,complete_original_source_atoms=512,
       correlated_method_vs_second_factor_observational_semantic_alias_verified=True,
       composite_factor_sourcewise_equivalence_verified=True,
       one_factor_numerical_scale_alias_verified=True,
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",world_results=worlds)
    out=HERE/"R231_ALL_512_ORIGINAL_CFA_STRUCTURAL_ATOMS.csv"
    keys=list(atom("ONE_FACTOR_VALID",1,1,1,1,1,1))
    with out.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=keys,lineterminator="\n")
        writer.writeheader()
        for world in WORLDS:
            for r in sources(world):
                writer.writerow({k:str(r[k]) for k in keys})
    results=HERE/"R231_EXACT_RESULTS.json"
    results.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={
        "research_id":"R231","original_catalogue_id":"10-005",
        "frozen_worlds":8,"complete_source_atoms":512,
        "full_source_vs_analytic_covariance_verified":True,
        "full_oracle_residual_vs_analytic_covariance_verified":True,
        "three_tetrad_polynomial_constraints_prescore_verified":True,
        "sourcewise_semantic_and_scale_aliases_verified":True,
        "source_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),
        "results_sha256":hashlib.sha256(results.read_bytes()).hexdigest(),
        "new_real_human_E2":0,"new_real_historical_E3":0
    }
    (HERE/"R231_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_world_count(self):self.assertEqual(len(WORLDS),8)
    def test_all_atoms(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),512)
    def test_alias(self):self.assertTrue(sourcewise_alias_checks())
    def test_fixed_hypothesis_pass(self):
        self.assertEqual(world_result("ONE_FACTOR_VALID")["fixed_equal_loading_candidate_absolute_discrepancy"],"0")
    def test_free_load_candidate(self):
        x=world_result("ONE_FACTOR_UNEQUAL_LOAD")
        self.assertNotEqual(x["fixed_equal_loading_candidate_absolute_discrepancy"],"0")
        self.assertTrue(x["all_necessary_one_factor_tetrads_zero"])
    def test_negative_load(self):
        self.assertEqual(world_result("ONE_FACTOR_SIGNED")["three_exact_tetrad_constraints"],["0","0","0"])
    def test_two_block_fails(self):
        self.assertEqual(world_result("TWO_FACTOR_BLOCK")["three_exact_tetrad_constraints"],["1","1","0"])
    def test_method_fails(self):
        self.assertEqual(world_result("CORRELATED_RESIDUAL_METHOD")["three_exact_tetrad_constraints"],["1","1","0"])
    def test_cancel_fails(self):
        self.assertEqual(world_result("CROSS_LOADING_CANCEL")["three_exact_tetrad_constraints"],["-1","-1","0"])
    def test_false_reassurance(self):
        x=world_result("TETRAD_FALSE_REASSURANCE")
        self.assertTrue(x["all_necessary_one_factor_tetrads_zero"])
        self.assertEqual(x["oracle_offdiagonal_conditional_T_residual_nonzero_pairs"],6)
    def test_unknown_world(self):
        with self.assertRaises(ValueError):sources("not-frozen")
    def test_invalid_source(self):
        with self.assertRaises(ValueError):atom("ONE_FACTOR_VALID",0,1,1,1,1,1)

def _case(world,kind):
    def t(self):
        data=sources(world)
        if kind=="mass":self.assertEqual(sum((r["original_probability"] for r in data),ZERO),ONE)
        elif kind=="keys":
            self.assertEqual(len({(r["hidden_T"],r["hidden_U"],r["independent_E1"],
                             r["independent_E2"],r["independent_E3"],r["independent_E4"]) for r in data}),64)
        elif kind=="cov":
            self.assertEqual(covariance_from_original(data,tuple(f"observed_X{i+1}" for i in range(4)))[1],
                             predicted_covariance_from_loads(world))
        elif kind=="oracle":
            self.assertEqual(covariance_from_original(data,tuple(f"oracle_residual_conditional_T_item{i+1}" for i in range(4)))[1],
                             analytical_conditional_T_residual(world))
        elif kind=="tetrads":
            self.assertEqual(tuple(map(str,tetrads(predicted_covariance_from_loads(world)))),
                             FROZEN_EXPECTED_TETRADS[world])
        elif kind=="result":
            self.assertEqual(world_result(world)["original_complete_exogenous_sources"],64)
        else:raise AssertionError("unknown test")
    return t
for _world in WORLDS:
    for _kind in ("mass","keys","cov","oracle","tetrads","result"):
        setattr(Tests,f"test_{_world.lower()}_{_kind}",_case(_world,_kind))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    opts=parser.parse_args()
    if opts.test:unittest.main(argv=["r231"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
