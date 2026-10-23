#!/usr/bin/env python3
"""R257 finite exact convex optimization KKT certificates versus 25-point grid.

Eight strongly convex Euclidean projections on a rational triangle and one
nonconvex counterexample with KKT stationary but nonglobal point. All source
grid candidates are preserved, even if infeasible. All computations Fraction.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
FREEZE="75b7f963eb850c9bc9e573d48877dab5f261a8ab"
ZERO=F(0);ONE=F(1)
GRID=(ZERO,F(1,4),F(1,2),F(3,4),ONE)
WORLDS={
 "INTERIOR_OFF_GRID":(ONE,F(3,5),F(1,5),True),
 "BINDING_SUM_BOTH":(ONE,F(3,4),F(3,4),True),
 "LOWER_X_ACTIVE":(ONE,F(-1,2),F(1,2),True),
 "LOWER_Y_ACTIVE":(ONE,F(1,2),F(-1,2),True),
 "VERTEX_ORIGIN":(ONE,F(-1,2),F(-1,2),True),
 "VERTEX_RIGHT":(ONE,F(2),F(1,4),True),
 "VERTEX_UPPER":(ONE,F(1,4),F(2),True),
 "CAPACITY_TWO_SLACK":(F(2),F(3,4),F(3,4),True),
 "NONCONVEX_KKT_NOT_SUFFICIENT":(ONE,F(1,2),F(1,2),False),
}
EXPECTED_POINTS={
 "INTERIOR_OFF_GRID":(F(3,5),F(1,5)),
 "BINDING_SUM_BOTH":(F(1,2),F(1,2)),
 "LOWER_X_ACTIVE":(ZERO,F(1,2)),
 "LOWER_Y_ACTIVE":(F(1,2),ZERO),
 "VERTEX_ORIGIN":(ZERO,ZERO),
 "VERTEX_RIGHT":(ONE,ZERO),
 "VERTEX_UPPER":(ZERO,ONE),
 "CAPACITY_TWO_SLACK":(F(3,4),F(3,4)),
 "NONCONVEX_KKT_NOT_SUFFICIENT":(ZERO,F(1,2))
}
def check(w):
    if w not in WORLDS:raise ValueError("unfrozen optimization world")
def feasible(x,y,C):return x>=ZERO and y>=ZERO and x+y<=C
def objective(w,x,y):
    check(w)
    C,a,b,convex=WORLDS[w]
    return (x-a)**2+(y-b)**2 if convex else -(x-a)**2+(y-b)**2
def grad(w,x,y):
    check(w)
    C,a,b,convex=WORLDS[w]
    return ((2*(x-a),2*(y-b)) if convex else (-2*(x-a),2*(y-b)))
def clamp(x,lo,hi):return max(lo,min(x,hi))
def grid_source(w,x,y):
    C,_,_,convex=WORLDS[w]
    fx=objective(w,x,y)
    dx,dy=grad(w,x,y)
    return dict(world=w,original_candidate_x=x,original_candidate_y=y,
        frozen_capacity_C=C,
        original_candidate_feasible=int(feasible(x,y,C)),
        original_objective_value=fx,
        original_grad_fx=dx,original_grad_fy=dy,
        original_capacity_slack=C-x-y,
        original_uniform_grid_design_mass=F(1,25),
        actual_math_world_is_convex=int(convex))
@lru_cache(None)
def sources(w):
    check(w)
    rows=tuple(grid_source(w,x,y) for x in GRID for y in GRID)
    assert len(rows)==25 and sum((r["original_uniform_grid_design_mass"] for r in rows),ZERO)==ONE
    return rows
def exact_grid_min(w):
    pts=[(r["original_candidate_x"],r["original_candidate_y"],r["original_objective_value"])
         for r in sources(w) if r["original_candidate_feasible"]]
    best=min(r[2] for r in pts)
    return best,tuple((x,y) for x,y,v in pts if v==best)
def continuous_convex_solution_by_faces(w):
    """Independent analytic projection to three edges and target interior."""
    C,a,b,convex=WORLDS[w]
    if not convex:raise ValueError("not convex")
    faces=[
      (clamp(a,ZERO,C),ZERO),
      (ZERO,clamp(b,ZERO,C))]
    t=clamp((C+a-b)/2,ZERO,C)
    faces.append((t,C-t))
    if feasible(a,b,C):faces.append((a,b))
    values=[(objective(w,*pt),pt) for pt in set(faces)]
    v=min(s for s,p in values)
    hits=[p for s,p in values if s==v]
    if len(hits)!=1:raise AssertionError("strict convex projection unique")
    return hits[0],v
def exact_kkt(w,x,y):
    C,a,b,convex=WORLDS[w]
    if not convex:raise ValueError("convex KKT certificate only")
    if not feasible(x,y,C):raise AssertionError("primal infeasible")
    if x+y<C:lmb=ZERO
    elif x>ZERO:lmb=2*(a-x)
    else:lmb=2*(b-y)
    mux=(2*(x-a)+lmb) if x==ZERO else ZERO
    muy=(2*(y-b)+lmb) if y==ZERO else ZERO
    gx,gy=grad(w,x,y)
    conditions=dict(
       primal_nonnegative=True,primal_capacity=True,
       dual_multipliers_nonnegative=lmb>=0 and mux>=0 and muy>=0,
       complementary_slackness=(lmb*(x+y-C)==0 and mux*x==0 and muy*y==0),
       stationary=(gx+lmb-mux==0 and gy+lmb-muy==0),
       hessian_is_2I_positive_definite=True,
       strict_slater_point_exists=(C>ZERO))
    if not all(conditions.values()):
        raise AssertionError(f"{w} proposed KKT not globally valid {conditions}")
    return dict(lambda_capacity=str(lmb),mu_lower_x=str(mux),mu_lower_y=str(muy),**conditions)
def nonconvex_counter():
    w="NONCONVEX_KKT_NOT_SUFFICIENT";C,a,b,_=WORLDS[w]
    local=(F(1,2),F(1,2));global_point=(ZERO,F(1,2))
    assert feasible(*local,C) and grad(w,*local)==(ZERO,ZERO)
    assert objective(w,*local)==ZERO
    assert feasible(*global_point,C) and objective(w,*global_point)==-F(1,4)
    assert all(objective(w,r["original_candidate_x"],r["original_candidate_y"])>=-F(1,4)
               for r in sources(w) if r["original_candidate_feasible"])
    # On whole triangle 0<=x<=1: -(x-1/2)^2>=-1/4; (y-1/2)^2>=0.
    # Thus global lower bound -1/4 is attained by (0,1/2).
    return dict(incorrect_KKT_sufficiency_claim=False,
       nonconvex_hessian_diagonal=["-2","2"],
       stationary_primal=["1/2","1/2"],stationary_objective="0",
       stationary_all_multipliers_zero_are_valid=True,
       feasible_strictly_better_point=["0","1/2"],feasible_better_value="-1/4",
       global_bound_proven_by_x_interval_and_nonnegative_y_square=True)
def locked_claims():
    for w in WORLDS:
        gridval,gridpts=exact_grid_min(w)
        if w!="NONCONVEX_KKT_NOT_SUFFICIENT":
            p,v=continuous_convex_solution_by_faces(w)
            if p!=EXPECTED_POINTS[w]:raise AssertionError(f"{w} unexpected true optimum {p}")
            exact_kkt(w,*p)
            assert gridval>=v
            if w=="INTERIOR_OFF_GRID":
                assert gridval==F(1,80) and v==ZERO and p not in gridpts
            else:assert gridval==v and p in gridpts
        else:
            assert gridval==-F(1,4) and EXPECTED_POINTS[w] in gridpts
            nonconvex_counter()
    return True
def world_result(w):
    C,a,b,convex=WORLDS[w]
    min_grid,gridpoints=exact_grid_min(w)
    if convex:
        p,v=continuous_convex_solution_by_faces(w)
        kkt=exact_kkt(w,*p)
        nonconvex=None
    else:
        p=EXPECTED_POINTS[w];v=objective(w,*p);kkt=None
        nonconvex=nonconvex_counter()
    return dict(world=w,capacity=str(C),target_a=str(a),target_b=str(b),
        globally_convex_and_strictly_positive_definite=convex,
        all_original_candidate_types=25,
        number_feasible_grid_candidates=sum(r["original_candidate_feasible"] for r in sources(w)),
        exact_grid_objective_minimum=str(min_grid),
        all_grid_optimum_points=[[str(z) for z in r] for r in gridpoints],
        exact_continuous_global_optimum=[str(x) for x in p],
        exact_continuous_global_optimum_value=str(v),
        exact_grid_suboptimality_gap=str(min_grid-v),
        exact_convex_KKT_primal_dual_complementary_certificate=kkt,
        nonconvex_KKT_not_sufficient_certified=nonconvex)
def emit():
    locked_claims()
    data=dict(research_id="R257",original_catalogue_id="11-017",prescore_freeze_commit=FREEZE,
       scientific_scope="FINITE_ARTIFICIAL_E1_STRICT_CONVEX_TRIANGLE_OPTIMIZATION_AND_NONCONVEX_KKT_COUNTEREXAMPLE",
       frozen_worlds=9,all_original_grid_candidate_source_atoms=225,
       grid_is_not_the_continuous_feasible_region=True,
       convex_worlds_have_exact_unique_KKT_optima=8,
       nonconvex_KKT_conditions_not_sufficient=True,
       offgrid_world_grid_gap="1/80",
       no_real_institutional_allocation_optimization_claim=True,
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[world_result(w) for w in WORLDS])
    src=HERE/"R257_ALL_225_ORIGINAL_GRID_CANDIDATE_SOURCE_ATOMS.csv"
    keys=list(sources(next(iter(WORLDS)))[0])
    with src.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for z in sources(w):wr.writerow({k:str(z[k]) for k in keys})
    result=HERE/"R257_EXACT_RESULTS.json"
    result.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    rec=dict(research_id="R257",original_catalogue_id="11-017",
       original_complete_grid_candidate_atoms=225,frozen_worlds=9,
       convex_KKT_eight_global_uniqueness_certificates=True,
       nonconvex_KKT_counterexample=True,
       off_grid_grid_approximation_gap="1/80",
       source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(result.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R257_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
    return rec
class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_sources(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),225)
    def test_locked(self):self.assertTrue(locked_claims())
    def test_off_grid(self):self.assertEqual(exact_grid_min("INTERIOR_OFF_GRID")[0],F(1,80))
    def test_nonconvex_saddle(self):self.assertFalse(nonconvex_counter()["incorrect_KKT_sufficiency_claim"])
    def test_vertex_right(self):self.assertEqual(exact_kkt("VERTEX_RIGHT",ONE,ZERO)["mu_lower_y"],"3/2")
    def test_binding_lambda(self):self.assertEqual(exact_kkt("BINDING_SUM_BOTH",F(1,2),F(1,2))["lambda_capacity"],"1/2")
    def test_origin_duals(self):self.assertEqual(exact_kkt("VERTEX_ORIGIN",ZERO,ZERO)["mu_lower_x"],"1")
    def test_nonconvex_certificate_fails(self):
        with self.assertRaises(ValueError):continuous_convex_solution_by_faces("NONCONVEX_KKT_NOT_SUFFICIENT")
    def test_invalid(self):
        with self.assertRaises(ValueError):sources("UNKNOWN_WORLD")
def _case(w,k):
    def t(self):
        rows=sources(w)
        if k=="mass":self.assertEqual(sum((r["original_uniform_grid_design_mass"] for r in rows),ZERO),ONE)
        elif k=="unique":self.assertEqual(len({(r["original_candidate_x"],r["original_candidate_y"]) for r in rows}),25)
        elif k=="positive":self.assertTrue(all(r["original_uniform_grid_design_mass"]==F(1,25) for r in rows))
        elif k=="candidate":
            for r in rows:self.assertEqual(r["original_objective_value"],objective(w,r["original_candidate_x"],r["original_candidate_y"]))
        elif k=="feasibility":
            for r in rows:self.assertEqual(r["original_candidate_feasible"],int(feasible(r["original_candidate_x"],r["original_candidate_y"],WORLDS[w][0])))
        elif k=="gradient":
            for r in rows:self.assertEqual((r["original_grad_fx"],r["original_grad_fy"]),grad(w,r["original_candidate_x"],r["original_candidate_y"]))
        elif k=="grid":
            value,points=exact_grid_min(w)
            self.assertTrue(all(feasible(x,y,WORLDS[w][0]) and objective(w,x,y)==value for x,y in points))
        elif k=="report":self.assertEqual(world_result(w)["all_original_candidate_types"],25)
        else:raise AssertionError("unknown case")
    return t
for w in WORLDS:
    for k in ("mass","unique","positive","candidate","feasibility","gradient","grid","report"):
        setattr(Tests,"test_"+w.lower()+"_"+k,_case(w,k))
if __name__=="__main__":
    a=argparse.ArgumentParser();g=a.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    args=a.parse_args()
    if args.test:unittest.main(argv=["r257"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
