#!/usr/bin/env python3
"""R249 finite exact logistic-transcritical and discrete fold bifurcation cases.

Nine frozen rational parameter worlds; 9 initial cohorts x 5 time points
each (405 original structural atoms). All exact Fraction. Linear fixed-point
multipliers, branch mergers, one-sided semistability and two nonhyperbolic
second-iterate local attraction certificates are independently verified.
No real historical threshold or bifurcation parameter is inferred.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="1c1d22cf0cc89ad759cee32a28425d3877b56b2b"
ZERO=F(0);ONE=F(1)
INITIALS=(F(-1),F(-1,2),F(-1,4),ZERO,F(1,4),F(1,2),F(2,3),F(3,4),ONE)
TIMES=(0,1,2,3,4)
LOGISTIC={
"LOGISTIC_R_HALF":F(1,2),"LOGISTIC_R_ONE":ONE,
"LOGISTIC_R_TWO":F(2),"LOGISTIC_R_THREE":F(3),"LOGISTIC_R_FOUR":F(4)}
FOLD={
"FOLD_NEG_QUARTER":F(-1,4),"FOLD_ZERO":ZERO,
"FOLD_POS_QUARTER":F(1,4),"FOLD_POS_ONE":ONE}
WORLDS=tuple(LOGISTIC)+tuple(FOLD)

def check_world(world):
    if world not in WORLDS:raise ValueError("not prescore frozen parameter")

def direct_map(world,x):
    check_world(world);x=F(x)
    if world in LOGISTIC:return LOGISTIC[world]*x*(ONE-x)
    return x+FOLD[world]-x*x

def direct_derivative(world,x):
    check_world(world);x=F(x)
    if world in LOGISTIC:return LOGISTIC[world]*(ONE-2*x)
    return ONE-2*x

def stepwise(world,x,n):
    if x not in INITIALS or n not in TIMES:raise ValueError("unfrozen cohort/time")
    state=x;sensitivity=ONE
    for _ in range(n):
        sensitivity*=direct_derivative(world,state)
        state=direct_map(world,state)
    return state,sensitivity

def trimmed(a):
    p=list(a)
    while len(p)>1 and p[-1]==ZERO:p.pop()
    return tuple(p)
def poly_add(a,b):
    return trimmed(tuple((a[i] if i<len(a) else ZERO)+(b[i] if i<len(b) else ZERO)
                         for i in range(max(len(a),len(b)))))
def poly_scale(a,s):return trimmed(tuple(x*s for x in a))
def poly_mul(a,b):
    c=[ZERO]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trimmed(c)
def poly_derivative(a):return trimmed(tuple(i*a[i] for i in range(1,len(a)))) if len(a)>1 else (ZERO,)
def poly_eval(a,x):
    result=ZERO
    for coeff in reversed(a):result=result*x+coeff
    return result

def formal_map(world):
    check_world(world)
    if world in LOGISTIC:
        r=LOGISTIC[world]
        return (ZERO,r,-r)
    return (FOLD[world],ONE,-ONE)

def formal_iterate(world,n):
    if n not in TIMES:raise ValueError("outside frozen iteration")
    q=(ZERO,ONE)
    coeff=formal_map(world)
    for _ in range(n):
        q=poly_add((coeff[0],),
          poly_add(poly_scale(q,coeff[1]),poly_scale(poly_mul(q,q),coeff[2])))
    return q

def independent_symbolic_state(world,x,n):
    p=formal_iterate(world,n)
    return poly_eval(p,x),poly_eval(poly_derivative(p),x)

def fixed_points(world):
    check_world(world)
    if world in LOGISTIC:
        r=LOGISTIC[world]
        other=ONE-ONE/r
        roots=((ZERO,2),) if other==ZERO else ((ZERO,1),(other,1))
    else:
        mu=FOLD[world]
        if mu<0:roots=()
        elif mu==0:roots=((ZERO,2),)
        elif mu==F(1,4):roots=((F(-1,2),1),(F(1,2),1))
        elif mu==ONE:roots=((F(-1),1),(ONE,1))
        else:raise AssertionError("frozen fold root not known")
    points=[]
    for root,multiplicity in roots:
        if direct_map(world,root)!=root:raise AssertionError("nonfixed closed-form root")
        multiplier=direct_derivative(world,root)
        if abs(multiplier)<1:
            stability="HYPERBOLIC_LOCAL_ATTRACTOR"
        elif abs(multiplier)>1:
            stability="HYPERBOLIC_LOCAL_REPELLER"
        elif world in ("LOGISTIC_R_ONE","FOLD_ZERO"):
            stability="NONHYPERBOLIC_SEMISTABLE_RIGHT_ATTRACTING_LEFT_REPELLING"
        elif (world=="LOGISTIC_R_THREE" and root==F(2,3)):
            stability="NONHYPERBOLIC_LOCAL_ATTRACTOR_SECOND_ITERATE"
        elif (world=="FOLD_POS_ONE" and root==ONE):
            stability="NONHYPERBOLIC_LOCAL_ATTRACTOR_SECOND_ITERATE"
        else:stability="NONHYPERBOLIC_MULTIPLIER_INCONCLUSIVE"
        points.append(dict(root=str(root),root_multiplicity=multiplicity,
                           exact_multiplier=str(multiplier),local_stability=stability))
    return points

def shifted_formal_polynomial(world,center,n=2):
    p=formal_iterate(world,n)
    translation=(center,ONE)
    power=(ONE,)
    expanded=(ZERO,)
    for coeff in p:
        expanded=poly_add(expanded,poly_scale(power,coeff))
        power=poly_mul(power,translation)
    return poly_add(expanded,(-center,))

def local_bifurcation_certificates():
    # Boundary -1 multipliers require nonlinear second iteration.
    expected_r3=(ZERO,ONE,ZERO,F(-18),F(-27))
    expected_fold1=(ZERO,ONE,ZERO,F(-2),F(-1))
    if shifted_formal_polynomial("LOGISTIC_R_THREE",F(2,3))!=expected_r3:
        raise AssertionError("wrong logistic r3 nonhyperbolic two-iterate polynomial")
    if shifted_formal_polynomial("FOLD_POS_ONE",ONE)!=expected_fold1:
        raise AssertionError("wrong fold mu=1 nonhyperbolic two-iterate polynomial")
    for world,center,bound,k in (("LOGISTIC_R_THREE",F(2,3),F(1,12),F(18)),
                                  ("FOLD_POS_ONE",ONE,F(1,4),F(2))):
        for y in (-bound,-bound/2,-bound/3,bound/3,bound/2,bound):
            factor=ONE-y*y*(k+(F(27) if world=="LOGISTIC_R_THREE" else ONE)*y)
            if not ZERO<factor<ONE:raise AssertionError("second iterate strict inward factor failed")
            if direct_map(world,direct_map(world,center+y))!=center+y*factor:
                raise AssertionError("second iterate exact direct reference failed")
    assert F(1,12)**2*(F(18)+F(27,12))==F(9,64)
    assert F(1,4)**2*(F(2)+F(1,4))==F(9,64)
    for world in ("LOGISTIC_R_ONE","FOLD_ZERO"):
        assert direct_map(world,F(1,4))<F(1,4)
        assert ZERO<direct_map(world,F(1,4))
        assert direct_map(world,F(-1,4))<F(-1,4)
        assert direct_map(world,ZERO)==ZERO
        assert direct_derivative(world,ZERO)==ONE
    # Mathematical branch collision is exact, not fitted.
    assert fixed_points("LOGISTIC_R_ONE")==[
        dict(root="0",root_multiplicity=2,exact_multiplier="1",
             local_stability="NONHYPERBOLIC_SEMISTABLE_RIGHT_ATTRACTING_LEFT_REPELLING")]
    assert len(fixed_points("FOLD_NEG_QUARTER"))==0
    assert len(fixed_points("FOLD_ZERO"))==1
    assert len(fixed_points("FOLD_POS_QUARTER"))==2
    return dict(
      logistic_fixed_branch_formula="0 and 1-1/r (coincident at r=1)",
      logistic_root_collision_r="1",
      logistic_zero_multiplier_across_r=["1/2","1","2","3","4"],
      logistic_nonzero_multiplier_formula="2-r",
      logistic_r1_double_fixed_root="0",
      logistic_r1_semistable_right_and_repelling_left=True,
      fold_fixed_equation="mu-x^2=0",
      fold_real_fixed_counts_mu_negative_zero_quarter_one=[0,1,2,2],
      fold_mu0_double_fixed_root="0",
      fold_mu0_semistable_right_and_repelling_left=True,
      logistic_r3_second_iterate_shifted_polynomial=[str(z) for z in expected_r3],
      logistic_r3_neighborhood_abs_y_le="1/12",
      logistic_r3_upper_strict_deficit="9/64",
      fold_mu1_second_iterate_shifted_polynomial=[str(z) for z in expected_fold1],
      fold_mu1_neighborhood_abs_y_le="1/4",
      fold_mu1_upper_strict_deficit="9/64",
      both_multiplier_minus_one_nonhyperbolic_fixed_are_proven_locally_attracting=True,
      no_claim_full_bifurcation_diagram_or_chaos=True
    )

def atom(world,x,n):
    state,D=stepwise(world,x,n)
    other,DD=independent_symbolic_state(world,x,n)
    if (state,D)!=(other,DD):raise AssertionError("direct and independent polynomial/derivative mismatch")
    return dict(
       world=world,model_family="LOGISTIC" if world in LOGISTIC else "FOLD",
       frozen_control_parameter=LOGISTIC[world] if world in LOGISTIC else FOLD[world],
       original_cohort_x0=x,original_time_n=n,
       observed_state_xn=state,
       observed_next_f_xn=direct_map(world,state),
       observed_local_derivative_fprime=direct_derivative(world,state),
       observed_cohort_sensitivity_dxndx0=D,
       original_source_probability=F(1,45)
    )

@lru_cache(maxsize=None)
def sources(world):
    check_world(world)
    rows=tuple(atom(world,x,n) for x in INITIALS for n in TIMES)
    if len(rows)!=45 or sum((z["original_source_probability"] for z in rows),ZERO)!=ONE:
        raise AssertionError("incomplete original 45 source atoms")
    return rows

def semigroup(world,x,m,n):
    if x not in INITIALS or m not in TIMES or n not in TIMES or m+n>4:
        raise ValueError("not frozen finite semigroup support")
    left=stepwise(world,x,m+n)[0]
    right=stepwise(world,x,m)[0]
    for _ in range(n):right=direct_map(world,right)
    return left==right

def world_result(world):
    for x in INITIALS:
        for m in TIMES:
            for n in TIMES:
                if m+n<=4 and not semigroup(world,x,m,n):
                    raise AssertionError("finite semigroup failed")
    src=sources(world)
    points=fixed_points(world)
    return dict(world=world,
       parameter_family="LOGISTIC" if world in LOGISTIC else "FOLD",
       exact_control_parameter=str(LOGISTIC[world] if world in LOGISTIC else FOLD[world]),
       original_complete_cohort_time_source_atoms=45,
       complete_real_fixed_points_and_root_multiplicities=points,
       count_distinct_real_fixed_points=len(points),
       nine_cohort_step4_exact_observed=[str(stepwise(world,x,4)[0]) for x in INITIALS],
       nine_cohort_step4_sensitivities=[str(stepwise(world,x,4)[1]) for x in INITIALS],
       full_original_observed_source_joint={
           "|".join((str(z["original_cohort_x0"]),str(z["original_time_n"]),
                     str(z["observed_state_xn"]))):str(z["original_source_probability"])
           for z in src},
       independent_symbolic_composition_and_formal_derivative_parity=True,
       all_finite_semigroup_source_constraints_passed=True
    )

def generate():
    cert=local_bifurcation_certificates()
    data=dict(
       research_id="R249",original_catalogue_id="11-009",
       prescore_freeze_commit=FREEZE,
       scientific_scope="FINITE_ARTIFICIAL_E1_EXACT_LOGISTIC_AND_FOLD_FIXED_POINT_BIFURCATION",
       frozen_parameter_worlds=9,full_original_cohort_time_atoms=405,
       exact_analytic_branch_and_nonhyperbolic_certificates=cert,
       sourcewise_polynomial_and_formal_derivative_exact=True,
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[world_result(w) for w in WORLDS]
    )
    csvpath=HERE/"R249_ALL_405_ORIGINAL_BIFURCATION_PARAMETER_SOURCE_ATOMS.csv"
    fields=list(sources("LOGISTIC_R_HALF")[0])
    with csvpath.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");wr.writeheader()
        for world in WORLDS:
            for row in sources(world):wr.writerow({k:str(row[k]) for k in fields})
    output=HERE/"R249_EXACT_RESULTS.json"
    output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    rec=dict(
       research_id="R249",original_catalogue_id="11-009",
       frozen_worlds=9,all_original_cohort_time_source_atoms=405,
       fixed_root_collision_and_two_family_stability_exchange_verified=True,
       distinct_fold_branch_counts_and_root_multiplicities_verified=True,
       two_nonhyperbolic_multiplier_minus_one_local_proofs_verified=True,
       source_sha256=hashlib.sha256(csvpath.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0
    )
    (HERE/"R249_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
    return rec

class Tests(unittest.TestCase):
    def test_nine_frozen(self):self.assertEqual(len(WORLDS),9)
    def test_405(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),405)
    def test_all_theorem_certificates(self):self.assertTrue(local_bifurcation_certificates())
    def test_logistic_rhalf_outside_ecological_domain(self):
        self.assertEqual(fixed_points("LOGISTIC_R_HALF")[1]["root"],"-1")
    def test_logistic_rone_double_root(self):
        self.assertEqual(fixed_points("LOGISTIC_R_ONE")[0]["root_multiplicity"],2)
    def test_logistic_rtwo_positive_branch(self):
        self.assertEqual(fixed_points("LOGISTIC_R_TWO")[1]["exact_multiplier"],"0")
    def test_logistic_r3_border(self):
        self.assertEqual(fixed_points("LOGISTIC_R_THREE")[1]["exact_multiplier"],"-1")
    def test_logistic_r4_repeller(self):
        self.assertEqual(fixed_points("LOGISTIC_R_FOUR")[1]["exact_multiplier"],"-2")
    def test_fold_negative_no_real(self):self.assertEqual(fixed_points("FOLD_NEG_QUARTER"),[])
    def test_fold_zero_double(self):
        self.assertEqual(fixed_points("FOLD_ZERO")[0]["root_multiplicity"],2)
    def test_fold_quarter_two_roots(self):
        self.assertEqual([p["root"] for p in fixed_points("FOLD_POS_QUARTER")],["-1/2","1/2"])
    def test_fold_one_minus_one_proof(self):
        self.assertEqual(fixed_points("FOLD_POS_ONE")[1]["exact_multiplier"],"-1")
    def test_unfrozen_initial_rejected(self):
        with self.assertRaises(ValueError):stepwise("LOGISTIC_R_HALF",F(1,3),4)

def _case(world,kind):
    def t(self):
        src=sources(world)
        if kind=="mass":self.assertEqual(sum((x["original_source_probability"] for x in src),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({(x["original_cohort_x0"],x["original_time_n"]) for x in src}),45)
        elif kind=="positive":
            self.assertTrue(all(x["original_source_probability"]==F(1,45) for x in src))
        elif kind=="polynomial":
            for x in INITIALS:
                for n in TIMES:self.assertEqual(stepwise(world,x,n),independent_symbolic_state(world,x,n))
        elif kind=="semigroup":
            for x in INITIALS:
                for m in TIMES:
                    for n in TIMES:
                        if m+n<=4:self.assertTrue(semigroup(world,x,m,n))
        elif kind=="fixed":
            for p in fixed_points(world):
                root=F(p["root"])
                self.assertEqual(direct_map(world,root),root)
                self.assertEqual(direct_derivative(world,root),F(p["exact_multiplier"]))
        elif kind=="derivative":
            for r in src:
                self.assertEqual(r["observed_cohort_sensitivity_dxndx0"],
                    independent_symbolic_state(world,r["original_cohort_x0"],r["original_time_n"])[1])
        elif kind=="report":
            self.assertEqual(world_result(world)["original_complete_cohort_time_source_atoms"],45)
        else:raise AssertionError("unfrozen test")
    return t

for _w in WORLDS:
    for _kind in ("mass","unique","positive","polynomial","semigroup","fixed","derivative","report"):
        setattr(Tests,"test_"+_w.lower()+"_"+_kind,_case(_w,_kind))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=ap.parse_args()
    if a.test:unittest.main(argv=["r249"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
