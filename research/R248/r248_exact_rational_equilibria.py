#!/usr/bin/env python3
"""R248 nine rational autonomous maps and exact local equilibrium certificates.

Original finite 9-cohort x 5-time source points per world, 405 total.
State iteration is checked against independent polynomial composition,
formal differentiation, algebraic fixed-point roots, and strict
nonhyperbolic two-iterate local attraction certificates.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="86c2e256ab098283d0cc56989ccbb2bc44f3aefb"
ZERO=F(0);ONE=F(1)
INITIALS=(F(-1,2),F(-1,4),ZERO,F(1,4),F(1,2),F(2,3),F(3,4),ONE,F(5,4))
TIMES=(0,1,2,3,4)
WORLDS=(
 "AFFINE_CONTRACT_ZERO","AFFINE_CONTRACT_ONE","AFFINE_ALTERNATE_CONTRACT",
 "AFFINE_EXPAND_ZERO","IDENTITY_EVERY_POINT_FIXED",
 "LOGISTIC_R2","LOGISTIC_R3_BORDER","LOGISTIC_R4_REPELLER",
 "CUBIC_NONHYPERBOLIC_ATTRACTOR")
AFFINE={
 "AFFINE_CONTRACT_ZERO":(F(1,2),ZERO),
 "AFFINE_CONTRACT_ONE":(F(1,2),F(1,2)),
 "AFFINE_ALTERNATE_CONTRACT":(F(-1,2),ZERO),
 "AFFINE_EXPAND_ZERO":(F(2),ZERO),
 "IDENTITY_EVERY_POINT_FIXED":(ONE,ZERO),
}
LOGISTIC={"LOGISTIC_R2":F(2),"LOGISTIC_R3_BORDER":F(3),"LOGISTIC_R4_REPELLER":F(4)}
NONHYPER=("LOGISTIC_R3_BORDER","CUBIC_NONHYPERBOLIC_ATTRACTOR")

def check(world):
    if world not in WORLDS:raise ValueError("unfrozen map")

def map_direct(world,x):
    check(world);x=F(x)
    if world in AFFINE:
        a,b=AFFINE[world]
        return a*x+b
    if world in LOGISTIC:return LOGISTIC[world]*x*(ONE-x)
    return x-x*x*x

def derivative_direct(world,x):
    check(world);x=F(x)
    if world in AFFINE:return AFFINE[world][0]
    if world in LOGISTIC:return LOGISTIC[world]*(ONE-2*x)
    return ONE-3*x*x

def orbit_stepwise(world,x,n):
    if x not in INITIALS or n not in TIMES:raise ValueError("unfrozen source")
    state=x;d=ONE
    for _ in range(n):
        d*=derivative_direct(world,state)
        state=map_direct(world,state)
    return state,d

def trim(p):
    p=list(p)
    while len(p)>1 and p[-1]==ZERO:p.pop()
    return tuple(p)
def add(a,b):
    return trim(tuple((a[i] if i<len(a) else ZERO)+(b[i] if i<len(b) else ZERO)
                    for i in range(max(len(a),len(b)))))
def mul(a,b):
    out=[ZERO]*(len(a)+len(b)-1)
    for i,v in enumerate(a):
        for j,w in enumerate(b):out[i+j]+=v*w
    return trim(out)
def scale(p,a):return trim(tuple(a*x for x in p))
def diff(p):return trim(tuple(i*p[i] for i in range(1,len(p)))) if len(p)>1 else (ZERO,)
def evalpoly(p,x):
    result=ZERO
    for c in reversed(p):result=result*x+c
    return result

def formal_map_coeff(world):
    if world in AFFINE:
        a,b=AFFINE[world]
        return (b,a)
    if world in LOGISTIC:
        r=LOGISTIC[world]
        return (ZERO,r,-r)
    if world=="CUBIC_NONHYPERBOLIC_ATTRACTOR":
        return (ZERO,ONE,ZERO,-ONE)
    raise ValueError("unknown formal map")

def formal_composition(world,n):
    if n not in TIMES:raise ValueError("outside horizon")
    q=(ZERO,ONE)
    for _ in range(n):
        if world in AFFINE:
            a,b=AFFINE[world]
            q=add((b,),scale(q,a))
        elif world in LOGISTIC:
            r=LOGISTIC[world]
            q=scale(add(q,scale(mul(q,q),-ONE)),r)
        else:
            q=add(q,scale(mul(mul(q,q),q),-ONE))
    return q

def independent_polynomial_orbit(world,x,n):
    p=formal_composition(world,n)
    return evalpoly(p,x),evalpoly(diff(p),x)

def fixed_point_certificates(world):
    check(world)
    if world=="IDENTITY_EVERY_POINT_FIXED":
        return [{"root":"ALL_REAL","multiplier":"1","linear_test":"INDETERMINATE_ALL_REAL_FIXED"}]
    if world in AFFINE:
        a,b=AFFINE[world]
        if a==ONE:raise AssertionError("unexpected nonidentity affine")
        root=b/(ONE-a)
        roots=(root,)
    elif world in LOGISTIC:
        r=LOGISTIC[world]
        roots=(ZERO,ONE-ONE/r)
    else:
        roots=(ZERO,)
    out=[]
    for x in roots:
        if map_direct(world,x)!=x:raise AssertionError("not an exact fixed point")
        mult=derivative_direct(world,x)
        if abs(mult)<1:kind="HYPERBOLIC_LOCAL_ATTRACTOR"
        elif abs(mult)>1:kind="HYPERBOLIC_LOCAL_REPELLER"
        elif world=="LOGISTIC_R3_BORDER" and x==F(2,3):
            kind="NONHYPERBOLIC_LOCAL_ATTRACTOR_SECOND_ITERATE_PROOF"
        elif world=="CUBIC_NONHYPERBOLIC_ATTRACTOR":
            kind="NONHYPERBOLIC_LOCAL_ATTRACTOR_STRICT_MAGNITUDE_PROOF"
        else:kind="NONHYPERBOLIC_MULTIPLIER_INCONCLUSIVE"
        out.append({"root":str(x),"multiplier":str(mult),"linear_test":kind})
    return out

def independent_nonhyperbolic_certificates():
    world="LOGISTIC_R3_BORDER"
    center=F(2,3)
    # Independent symbolic composition f^2 with shifted formal variable y.
    p=formal_composition(world,2)
    shifted=(center,ONE)
    substituted=(ZERO,)
    power=(ONE,)
    for coeff in p:
        substituted=add(substituted,scale(power,coeff))
        power=mul(power,shifted)
    diff_fixed=add(substituted,(-center,))
    expected=(ZERO,ONE,ZERO,F(-18),F(-27))
    if diff_fixed!=expected:
        raise AssertionError("logistic r3 second-iterate normal form is wrong")
    for y in (F(-1,12),F(-1,24),F(-1,36),F(1,36),F(1,24),F(1,12)):
        factor=ONE-y*y*(18+27*y)
        if not (ZERO<factor<ONE):raise AssertionError("f^2 not locally strictly attracting")
        if map_direct(world,map_direct(world,center+y))!=center+y*factor:
            raise AssertionError("2nd iteration direct map not matched formal normal form")
    # Bound |y| <= 1/12: 18+27y in [63/4,81/4],
    # y²*(18+27y) ≤ (1/144)*(81/4)=9/64 < 1,
    # and >0 away from y=0. Thus even subsequence contracts to zero;
    # continuous f makes odd subsequence approach zero as well.
    if F(1,144)*F(81,4)!=F(9,64):raise AssertionError("strict multiplier bound arithmetic")
    # cubic: |x-x^3| = |x|(1-x²) strictly below |x| on 0<|x|<1.
    cubic="CUBIC_NONHYPERBOLIC_ATTRACTOR"
    for x in (F(-3,4),F(-1,2),F(-1,4),F(1,4),F(1,2),F(3,4)):
        if not (ZERO<abs(map_direct(cubic,x))<abs(x)):
            raise AssertionError("cubic local inward map certificate failed")
    # derivative +1 also occurs for identity without attraction.
    if derivative_direct(cubic,ZERO)!=derivative_direct("IDENTITY_EVERY_POINT_FIXED",ZERO):
        raise AssertionError("identical inconclusive multiplier contrast broken")
    if map_direct("IDENTITY_EVERY_POINT_FIXED",F(1,4))!=F(1,4):
        raise AssertionError("identity is not attracting its neighbors")
    # Preimage of a repeller: logistic r4 maps 1/4 to fixed 3/4 exactly.
    assert map_direct("LOGISTIC_R4_REPELLER",F(1,4))==F(3,4)
    assert map_direct("LOGISTIC_R4_REPELLER",F(3,4))==F(3,4)
    assert abs(derivative_direct("LOGISTIC_R4_REPELLER",F(3,4)))==F(2)
    return dict(
        logistic_r3_fixed_point="2/3",
        logistic_r3_nonhyperbolic_multiplier="-1",
        logistic_r3_second_iterate_y_polynomial_coefficients=[str(x) for x in expected],
        logistic_r3_bound_y_abs_le="1/12",
        logistic_r3_upper_bound_strict_factor_deficit="9/64",
        logistic_r3_second_iterate_strict_inward_and_local_asymptotic=True,
        cubic_fixed_point="0",cubic_multiplier="1",
        cubic_inward_interval="(-1,1)",
        cubic_strict_magnitude_decrease_except_fixed_zero=True,
        identity_every_real_is_fixed_no_single_point_attractor=True,
        logistic_r4_repeller_fixed_point="3/4",
        logistic_r4_repeller_multiplier="-2",
        logistic_r4_special_initial_preimage="1/4",
        logistic_r4_preimage_hits_repeller_at_step1_exact=True
    )

def source_atom(world,x,n):
    s,d=orbit_stepwise(world,x,n)
    s2,d2=independent_polynomial_orbit(world,x,n)
    if (s,d)!=(s2,d2):
        raise AssertionError("stepwise and independent exact polynomial orbit mismatch")
    return dict(world=world,observed_initial_x0=x,observed_time_step_n=n,
        observed_state_xn=s,observed_next_state_f_xn=map_direct(world,s),
        observed_local_map_derivative_fprime_xn=derivative_direct(world,s),
        observed_sensitivity_dxndx0=d,
        original_cohort_time_source_probability=F(1,45))

@lru_cache(maxsize=None)
def sources(world):
    check(world)
    rows=tuple(source_atom(world,x,n) for x in INITIALS for n in TIMES)
    if len(rows)!=45 or sum((r["original_cohort_time_source_probability"] for r in rows),ZERO)!=ONE:
        raise AssertionError("original finite initial-time source space incorrect")
    return rows

def semigroup(world,x,m,n):
    if x not in INITIALS or m not in TIMES or n not in TIMES or m+n>4:
        raise ValueError("not prescore permitted cohort and time")
    a=orbit_stepwise(world,x,m+n)[0]
    b=orbit_stepwise(world,x,m)[0]
    for _ in range(n):b=map_direct(world,b)
    return a==b

def world_result(world):
    for x in INITIALS:
        for m in TIMES:
            for n in TIMES:
                if m+n<=4 and not semigroup(world,x,m,n):
                    raise AssertionError("discrete autonomous map semigroup not exact")
    certificate=fixed_point_certificates(world)
    last=[orbit_stepwise(world,x,4)[0] for x in INITIALS]
    out=dict(world=world,
        original_full_cohort_time_source_rows=45,
        algebraic_fixed_point_and_local_multiplier_certificates=certificate,
        nine_cohort_step4_exact_state=[str(x) for x in last],
        nine_cohort_step4_initial_sensitivities=[str(orbit_stepwise(world,x,4)[1]) for x in INITIALS],
        observed_source_joint={
            "|".join([str(r["observed_initial_x0"]),str(r["observed_time_step_n"]),
                      str(r["observed_state_xn"])]):
                     str(r["original_cohort_time_source_probability"]) for r in sources(world)
        },
        exact_all_stepwise_vs_polynomial_and_formal_derivative_certified=True,
        all_finite_cohort_step4_flow_semigroup_certified=True
    )
    if world=="IDENTITY_EVERY_POINT_FIXED":
        assert last==list(INITIALS)
    if world=="LOGISTIC_R4_REPELLER":
        assert orbit_stepwise(world,F(1,4),4)[0]==F(3,4)
    return out

def generate():
    nonhyper=independent_nonhyperbolic_certificates()
    data=dict(research_id="R248",original_catalogue_id="11-008",
       prescore_freeze_commit=FREEZE,
       scientific_scope="FINITE_ARTIFICIAL_E1_EXACT_RATIONAL_MAP_EQUILIBRIA_AND_LOCAL_NONHYPERBOLIC_CERTIFICATES",
       frozen_worlds=9,complete_original_cohort_time_atoms=405,
       nine_unique_initial_cohorts_per_world=9,five_time_points_per_cohort=5,
       exact_independent_polynomial_composition_and_derivative=True,
       finite_discrete_autonomous_semigroup=True,
       nonhyperbolic_local_theorem_certificates=nonhyper,
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[world_result(w) for w in WORLDS])
    out=HERE/"R248_ALL_405_EXACT_MAP_IVP_TIME_SOURCES.csv"
    fields=list(sources("AFFINE_CONTRACT_ZERO")[0])
    with out.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        wr.writeheader()
        for w in WORLDS:
            for r in sources(w):wr.writerow({k:str(r[k]) for k in fields})
    result=HERE/"R248_EXACT_RESULTS.json"
    result.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    machine=dict(research_id="R248",original_catalogue_id="11-008",
        frozen_worlds=9,all_original_cohort_time_atoms=405,
        nonhyperbolic_second_iterate_r3_and_cubic_certified=True,
        independent_formal_polynomial_iteration_and_derivative=True,
        local_repeller_has_exact_preimage_counterexample=True,
        source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(result.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R248_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(machine,indent=2)+"\n",encoding="utf-8")
    return machine

class Tests(unittest.TestCase):
    def test_nine_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_405_sources(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),405)
    def test_nonhyperbolic_algebra(self):self.assertTrue(independent_nonhyperbolic_certificates())
    def test_logistic_r3_border(self):
        self.assertEqual(derivative_direct("LOGISTIC_R3_BORDER",F(2,3)),-ONE)
    def test_cubic_unit_multiplier(self):
        self.assertEqual(derivative_direct("CUBIC_NONHYPERBOLIC_ATTRACTOR",ZERO),ONE)
    def test_identity_all_fixed(self):
        self.assertEqual(fixed_point_certificates("IDENTITY_EVERY_POINT_FIXED")[0]["root"],"ALL_REAL")
    def test_logistic_r4_exact_repeller_preimage(self):
        self.assertEqual(orbit_stepwise("LOGISTIC_R4_REPELLER",F(1,4),4)[0],F(3,4))
    def test_logistic_r2_half_multiplier_zero(self):
        self.assertEqual(derivative_direct("LOGISTIC_R2",F(1,2)),ZERO)
    def test_affine_half(self):
        self.assertEqual(orbit_stepwise("AFFINE_CONTRACT_ZERO",ONE,4)[0],F(1,16))
    def test_cubic_sign(self):
        self.assertTrue(0<map_direct("CUBIC_NONHYPERBOLIC_ATTRACTOR",F(1,2))<F(1,2))
    def test_all_initials(self):self.assertEqual(len(INITIALS),9)
    def test_invalid_source(self):
        with self.assertRaises(ValueError):orbit_stepwise("LOGISTIC_R2",F(9,10),4)

def _case(world,kind):
    def t(self):
        rows=sources(world)
        if kind=="mass":self.assertEqual(sum((r["original_cohort_time_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({(r["observed_initial_x0"],r["observed_time_step_n"]) for r in rows}),45)
        elif kind=="positive":
            self.assertTrue(all(r["original_cohort_time_source_probability"]>0 for r in rows))
        elif kind=="poly":
            for x in INITIALS:
                for n in TIMES:self.assertEqual(orbit_stepwise(world,x,n),independent_polynomial_orbit(world,x,n))
        elif kind=="semigroup":
            for x in INITIALS:
                for m in TIMES:
                    for n in TIMES:
                        if m+n<=4:self.assertTrue(semigroup(world,x,m,n))
        elif kind=="fixed":
            for root in fixed_point_certificates(world):
                if root["root"]!="ALL_REAL":
                    self.assertEqual(map_direct(world,F(root["root"])),F(root["root"]))
                    self.assertEqual(derivative_direct(world,F(root["root"])),F(root["multiplier"]))
        elif kind=="sensitivity":
            for r in rows:
                self.assertEqual(r["observed_sensitivity_dxndx0"],
                    independent_polynomial_orbit(world,r["observed_initial_x0"],r["observed_time_step_n"])[1])
        elif kind=="report":
            self.assertEqual(world_result(world)["original_full_cohort_time_source_rows"],45)
        else:raise AssertionError("unfrozen test")
    return t

for _world in WORLDS:
    for _kind in ("mass","unique","positive","poly","semigroup","fixed","sensitivity","report"):
        setattr(Tests,"test_"+_world.lower()+"_"+_kind,_case(_world,_kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["r248"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
