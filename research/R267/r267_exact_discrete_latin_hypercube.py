#!/usr/bin/env python3
"""R267: full finite 3x3 discrete LHS versus IID design, 6885 artificial atoms.

Route A enumerates all original primitive configurations. Route B independently
convolves IID one-point outputs and uses relative LHS permutations. An ANOVA
residual formula provides a third variance calculation. No observed human data.
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
FREEZE="8943746fab2b7f23256ff537007c9fc902bda386"
LEVELS=(0,1,2)
GRID=tuple(itertools.product(LEVELS, repeat=2))
PERMS=tuple(itertools.permutations(LEVELS))
DESIGNS=("IID","LHS")
WORLDS=("ADD_X","ADD_X_PLUS_Y","ADD_SQUARES","PRODUCT_XY",
        "CENTERED_INTERACTION","EQUAL_INDICATOR","MODULAR_SUM",
        "THRESHOLD_SUM_GE2","CORNER_22")
ZERO,ONE=F(0),F(1)
LOCKED={
 "ADD_X":("1","2/9","0","0"),
 "ADD_X_PLUS_Y":("2","4/9","0","0"),
 "ADD_SQUARES":("10/3","52/27","0","0"),
 "PRODUCT_XY":("1","16/27","2/9","3/8"),
 "CENTERED_INTERACTION":("0","4/27","2/9","3/2"),
 "EQUAL_INDICATOR":("1/3","2/27","1/9","3/2"),
 "MODULAR_SUM":("1","2/9","1/3","3/2"),
 "THRESHOLD_SUM_GE2":("2/3","2/27","1/27","1/2"),
 "CORNER_22":("1/9","8/243","2/81","3/4")}


def integrand(name,x,y):
    if name not in WORLDS or x not in LEVELS or y not in LEVELS:
        raise ValueError("unfrozen LHS world/level")
    if name=="ADD_X":return F(x)
    if name=="ADD_X_PLUS_Y":return F(x+y)
    if name=="ADD_SQUARES":return F(x*x+y*y)
    if name=="PRODUCT_XY":return F(x*y)
    if name=="CENTERED_INTERACTION":return F((x-1)*(y-1))
    if name=="EQUAL_INDICATOR":return F(x==y)
    if name=="MODULAR_SUM":return F((x+y)%3)
    if name=="THRESHOLD_SUM_GE2":return F(x+y>=2)
    if name=="CORNER_22":return F(x==2 and y==2)
    raise AssertionError("unreachable")


def validate(name,design):
    if name not in WORLDS or design not in DESIGNS:
        raise ValueError("unfrozen world/design")


def true_mean(name):
    if name not in WORLDS:raise ValueError("unfrozen world")
    return sum((integrand(name,x,y) for x,y in GRID),ZERO)/9


def source_atoms(name,design):
    """Route A: direct enumeration of each actual primitive design configuration."""
    validate(name,design)
    truth=true_mean(name)
    if design=="IID":
        origins=itertools.product(GRID,repeat=3)
        mass=F(1,729)
    else:
        origins=(tuple(zip(px,py)) for px in PERMS for py in PERMS)
        mass=F(1,36)
    for points in origins:
        values=tuple(integrand(name,x,y) for x,y in points)
        estimate=sum(values,ZERO)/3
        yield dict(world=name,design=design,
                   original_source_coordinate_triplet="|".join(f"{x}:{y}" for x,y in points),
                   original_three_integrand_values=";".join(str(v) for v in values),
                   original_source_probability=mass,
                   original_three_evaluation_average=estimate,
                   true_grid_expectation=truth,
                   squared_error=(estimate-truth)**2)


def enumerated_pmf(name,design):
    pmf=defaultdict(lambda:ZERO)
    count=0
    for row in source_atoms(name,design):
        pmf[row["original_three_evaluation_average"]]+=row["original_source_probability"]
        count+=1
    assert count==(729 if design=="IID" else 36)
    assert sum(pmf.values(),ZERO)==ONE
    return dict(pmf),count


def independent_pmf(name,design):
    """Route B: probability algebra; no calls to source_atoms or enumerated_pmf."""
    validate(name,design)
    if design=="IID":
        one=defaultdict(lambda:ZERO)
        for x in LEVELS:
            for y in LEVELS:
                one[integrand(name,x,y)]+=F(1,9)
        sums={ZERO:ONE}
        for _ in range(3):
            after=defaultdict(lambda:ZERO)
            for so,p in sums.items():
                for v,q in one.items():
                    after[so+v]+=p*q
            sums=dict(after)
        return {k/3:v for k,v in sums.items() if v}
    # All 36 independent x/y permutations induce one of 6 relative y permutations.
    # We intentionally use only six permutation-algebra classes in this path.
    pmf=defaultdict(lambda:ZERO)
    for pi in PERMS:
        estimate=sum((integrand(name,x,pi[x]) for x in LEVELS),ZERO)/3
        pmf[estimate]+=F(1,6)
    return dict(pmf)


def moments(pmf,truth):
    mean=sum((x*p for x,p in pmf.items()),ZERO)
    var=sum(((x-mean)**2*p for x,p in pmf.items()),ZERO)
    bias=mean-truth
    mse=sum(((x-truth)**2*p for x,p in pmf.items()),ZERO)
    assert mse==var+bias*bias
    return mean,var,bias,mse


def analytical_variances(name):
    """Third route: 3x3 population moment and row/column centered interaction."""
    if name not in WORLDS:raise ValueError("unfrozen world")
    a=[[integrand(name,i,j) for j in LEVELS] for i in LEVELS]
    overall=sum((v for row in a for v in row),ZERO)/9
    rowmeans=[sum(row,ZERO)/3 for row in a]
    colmeans=[sum((a[i][j] for i in LEVELS),ZERO)/3 for j in LEVELS]
    iid=sum(((v-overall)**2 for row in a for v in row),ZERO)/27
    interaction=sum(((a[i][j]-rowmeans[i]-colmeans[j]+overall)**2
                     for i in LEVELS for j in LEVELS),ZERO)
    lhs=interaction/18
    return overall,iid,lhs,interaction


def result_world(name):
    mean,iid,lhs,residual=analytical_variances(name)
    designs={}
    for design in DESIGNS:
        pa,src=enumerated_pmf(name,design)
        pb=independent_pmf(name,design)
        if pa!=pb:raise AssertionError("enumeration and independent exact PMFs disagree")
        observed=moments(pa,mean)
        predicted=iid if design=="IID" else lhs
        if observed!=(mean,predicted,ZERO,predicted):
            raise AssertionError("independent variance formula mismatch")
        designs[design]=dict(source_atoms=src,function_evaluations=3,
             exact_mean=str(observed[0]),exact_variance=str(observed[1]),
             exact_bias=str(observed[2]),exact_MSE=str(observed[3]),
             complete_exact_estimator_PMF={str(k):str(v) for k,v in sorted(pa.items())},
             independently_verified_PMF=True)
    return dict(world=name,original_grid="two independent 3-level uniform coordinates",
        target_grid_expectation=str(mean),
        exact_ANOVA_squared_interaction_residual=str(residual),
        LHS_over_IID_variance_ratio=str(lhs/iid),
        designs=designs)


def frozen_claims():
    assert len(WORLDS)==len(LOCKED)==9
    for w in WORLDS:
        r=result_world(w)
        actual=(r["target_grid_expectation"],r["designs"]["IID"]["exact_variance"],
                r["designs"]["LHS"]["exact_variance"],r["LHS_over_IID_variance_ratio"])
        assert actual==LOCKED[w],(w,actual)
        assert r["designs"]["IID"]["source_atoms"]==729
        assert r["designs"]["LHS"]["source_atoms"]==36
    assert sum(729+36 for _ in WORLDS)==6885
    return True


def emit():
    frozen_claims()
    csv_path=HERE/"R267_ALL_6885_ORIGINAL_GRID_SAMPLE_SOURCES.csv"
    cols=("world","design","original_source_coordinate_triplet",
          "original_three_integrand_values","original_source_probability",
          "original_three_evaluation_average","true_grid_expectation","squared_error")
    with csv_path.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        writer.writeheader()
        for name in WORLDS:
            for design in DESIGNS:
                for row in source_atoms(name,design):
                    writer.writerow({k:str(row[k]) for k in cols})
    results=dict(research_id="R267",original_catalogue_id="11-027",
       prescore_freeze_commit=FREEZE,
       scope="E1_EXACT_DISCRETE_3x3_TWO_COORDINATE_3_EVALUATION_LHS",
       world_count=9,source_types_IID=6561,source_types_LHS=324,
       all_6885_source_types_archived=True,all_18_independent_PMFs_verified=True,
       three_additive_worlds_zero_LHS_variance=True,
       three_non_additive_worlds_LHS_higher_variance=True,
       no_continuous_intra_stratum_jitter_or_real_random_trials=True,
       no_real_human_E2=0,no_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[result_world(w) for w in WORLDS])
    p=HERE/"R267_EXACT_RESULTS.json"
    p.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R267",prescore_freeze_commit=FREEZE,
       frozen_worlds=9,source_types=6885,independent_exact_PMFs=18,
       source_sha256=hashlib.sha256(csv_path.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
       no_real_human_E2=0,no_real_historical_E3=0)
    (HERE/"R267_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt


class Tests(unittest.TestCase):
    def test_all_locked(self):self.assertTrue(frozen_claims())
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_source_count(self):self.assertEqual(9*(729+36),6885)
    def test_permutations(self):self.assertEqual(len(PERMS),6)
    def test_levels(self):self.assertEqual(len(GRID),9)
    def test_invalid_world(self):
        with self.assertRaises(ValueError):true_mean("NONEXISTENT")
    def test_invalid_source(self):
        with self.assertRaises(ValueError):integrand("ADD_X",3,1)
    def test_invalid_design(self):
        with self.assertRaises(ValueError):list(source_atoms("ADD_X","NONE"))
    def test_exact_additive(self):self.assertEqual(analytical_variances("ADD_SQUARES")[2],ZERO)
    def test_positive_interaction(self):self.assertEqual(analytical_variances("EQUAL_INDICATOR")[2],F(1,9))


def check_world(name,design,kind):
    def test(self):
        rows=list(source_atoms(name,design))
        pmf,total=enumerated_pmf(name,design)
        truth,iid,lhs,_=analytical_variances(name)
        if kind=="count":self.assertEqual(total,729 if design=="IID" else 36)
        elif kind=="unique":
            self.assertEqual(len({r["original_source_coordinate_triplet"] for r in rows}),total)
        elif kind=="mass":
            self.assertEqual(sum((r["original_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="pmf":self.assertEqual(pmf,independent_pmf(name,design))
        elif kind=="moment":
            target=iid if design=="IID" else lhs
            self.assertEqual(moments(pmf,truth),(truth,target,ZERO,target))
        elif kind=="values":
            self.assertTrue(all(r["original_three_evaluation_average"]==
                sum((F(v) for v in r["original_three_integrand_values"].split(";")),ZERO)/3 for r in rows))
        elif kind=="square":
            self.assertTrue(all(r["squared_error"]==
                (r["original_three_evaluation_average"]-truth)**2 for r in rows))
        else:raise AssertionError("bad test")
    return test


for name in WORLDS:
    for design in DESIGNS:
        for kind in ("count","unique","mass","pmf","moment","values","square"):
            setattr(Tests,f"test_{name.lower()}_{design.lower()}_{kind}",check_world(name,design,kind))


if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r267"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
