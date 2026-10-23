#!/usr/bin/env python3
"""R251 finite one-dimensional discrete Lyapunov tests with exact rational sources.
Distinguish one-step V=x² certification, neutral stability, failure of a
specific candidate, and two-step nonhyperbolic local attraction proof.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
FREEZE="15568be1625414aa72a179c93f315535de704d73"
ZERO=F(0);ONE=F(1)
INITIALS=(F(-1,2),F(-1,4),F(-1,12),F(-1,24),ZERO,F(1,24),F(1,12),F(1,4),F(1,2))
TIMES=(0,1,2,3,4)
WORLDS=("HALF_CONTRACTION","NEGATIVE_HALF_CONTRACTION","ZERO_MAP",
"DOUBLE_EXPANSION","IDENTITY_NEUTRAL","SIGN_FLIP_NEUTRAL",
"CUBIC_LOCAL_INWARD","CUBIC_OUTWARD","LOGISTIC_R3_CENTERED")
LINEAR={"HALF_CONTRACTION":F(1,2),"NEGATIVE_HALF_CONTRACTION":F(-1,2),
"ZERO_MAP":ZERO,"DOUBLE_EXPANSION":F(2),
"IDENTITY_NEUTRAL":ONE,"SIGN_FLIP_NEUTRAL":F(-1)}
CLAIMS={
 "HALF_CONTRACTION":"GLOBAL_ASYMPTOTIC_ONE_STEP_STRICT",
 "NEGATIVE_HALF_CONTRACTION":"GLOBAL_ASYMPTOTIC_ONE_STEP_STRICT",
 "ZERO_MAP":"GLOBAL_FINITE_TIME_ONE_STEP_STRICT",
 "DOUBLE_EXPANSION":"UNSTABLE_V_STRICT_INCREASE",
 "IDENTITY_NEUTRAL":"LYAPUNOV_STABLE_NOT_ASYMPTOTIC",
 "SIGN_FLIP_NEUTRAL":"LYAPUNOV_STABLE_PERIOD2_NOT_ASYMPTOTIC",
 "CUBIC_LOCAL_INWARD":"LOCAL_ASYMPTOTIC_STRICT_ONE_STEP_ON_ABS_LESS_1",
 "CUBIC_OUTWARD":"UNSTABLE_STRICT_LOCAL_V_INCREASE",
 "LOGISTIC_R3_CENTERED":"LOCAL_ASYMPTOTIC_TWO_STEP_NOT_ONE_STEP_V_CERTIFICATE"
}
def check(w):
    if w not in WORLDS:raise ValueError("unfrozen map")
def f(w,x):
    check(w);x=F(x)
    if w in LINEAR:return LINEAR[w]*x
    if w=="CUBIC_LOCAL_INWARD":return x-x*x*x
    if w=="CUBIC_OUTWARD":return x+x*x*x
    return -x-3*x*x
def df(w,x):
    check(w);x=F(x)
    if w in LINEAR:return LINEAR[w]
    if w=="CUBIC_LOCAL_INWARD":return ONE-3*x*x
    if w=="CUBIC_OUTWARD":return ONE+3*x*x
    return -ONE-6*x
def direct_orbit(w,x,n):
    if x not in INITIALS or n not in TIMES:raise ValueError("unfrozen original source")
    y=x;D=ONE
    for _ in range(n):
        D*=df(w,y)
        y=f(w,y)
    return y,D
def trim(poly):
    p=list(poly)
    while len(p)>1 and p[-1]==ZERO:p.pop()
    return tuple(p)
def add(a,b):
    return trim(tuple((a[i] if i<len(a) else ZERO)+(b[i] if i<len(b) else ZERO)
         for i in range(max(len(a),len(b)))))
def scale(a,k):return trim(tuple(k*x for x in a))
def mul(a,b):
    v=[ZERO]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):v[i+j]+=x*y
    return trim(v)
def deriv(a):return trim(tuple(i*a[i] for i in range(1,len(a)))) if len(a)>1 else (ZERO,)
def horner(a,x):
    v=ZERO
    for z in reversed(a):v=v*x+z
    return v
def frozen_coefficients(w):
    check(w)
    if w in LINEAR:return (ZERO,LINEAR[w])
    if w=="CUBIC_LOCAL_INWARD":return (ZERO,ONE,ZERO,-ONE)
    if w=="CUBIC_OUTWARD":return (ZERO,ONE,ZERO,ONE)
    return (ZERO,-ONE,F(-3))
def composition(w,n):
    if n not in TIMES:raise ValueError("not frozen time")
    p=(ZERO,ONE)
    for _ in range(n):
        if w in LINEAR:p=scale(p,LINEAR[w])
        elif w in ("CUBIC_LOCAL_INWARD","CUBIC_OUTWARD"):
            p=add(p,scale(mul(mul(p,p),p),ONE if w=="CUBIC_OUTWARD" else -ONE))
        else:p=add(scale(p,-ONE),scale(mul(p,p),F(-3)))
    return p
def independent_state(w,x,n):
    pol=composition(w,n)
    return horner(pol,x),horner(deriv(pol),x)
def v(x):return x*x
def delta(w,x):return v(f(w,x))-v(x)
def certificate():
    out={}
    for w,a in LINEAR.items():
        expected=a*a-ONE
        for x in INITIALS:
            assert delta(w,x)==expected*x*x
        out[w]={"coefficient_deltaV_over_x2":str(expected),"classification":CLAIMS[w]}
    for x in (F(-1,2),F(-1,4),F(-1,12),F(1,12),F(1,4),F(1,2)):
        assert ZERO<abs(f("CUBIC_LOCAL_INWARD",x))<abs(x)
        assert abs(f("CUBIC_OUTWARD",x))>abs(x)
        assert delta("CUBIC_LOCAL_INWARD",x)<ZERO
        assert delta("CUBIC_OUTWARD",x)>ZERO
    w="LOGISTIC_R3_CENTERED"
    assert delta(w,F(1,12))>ZERO
    assert delta(w,F(-1,12))<ZERO
    assert composition(w,2)==(ZERO,ONE,ZERO,F(-18),F(-27))
    for y in (F(-1,12),F(-1,24),F(1,24),F(1,12)):
        factor=ONE-y*y*(F(18)+F(27)*y)
        assert ZERO<factor<ONE
        assert f(w,f(w,y))==y*factor
        assert v(f(w,f(w,y)))<v(y)
    assert F(1,12)**2*(F(18)+F(27,12))==F(9,64)
    assert df("CUBIC_LOCAL_INWARD",ZERO)==df("CUBIC_OUTWARD",ZERO)==ONE
    assert df(w,ZERO)==-ONE
    out["CUBIC_LOCAL_INWARD"]={"strict_interval":"0<abs(x)<1","classification":CLAIMS["CUBIC_LOCAL_INWARD"]}
    out["CUBIC_OUTWARD"]={"exact_deltaV":"x^4(2+x^2)","classification":CLAIMS["CUBIC_OUTWARD"]}
    out[w]={"one_step_deltaV":"6*x^3+9*x^4",
            "exact_second_iterate_shifted_coefficients":["0","1","0","-18","-27"],
            "strict_two_step_interval":"0<abs(x)<=1/12",
            "maximum_two_step_factor_deficit":"9/64",
            "one_step_V_increases_for_small_positive_x":True,
            "one_step_V_decreases_for_small_negative_x":True,
            "classification":CLAIMS[w]}
    return out
def source_atom(w,x,n):
    y,D=direct_orbit(w,x,n)
    other,DD=independent_state(w,x,n)
    if (y,D)!=(other,DD):raise AssertionError("independent polynomial orbit does not agree")
    return dict(world=w,original_initial_x0=x,original_time_n=n,
    observed_state_xn=y,observed_positive_candidate_Vn=v(y),
    observed_next_state_fx=f(w,y),
    observed_one_step_delta_V=delta(w,y),
    observed_local_derivative_fprime=df(w,y),
    observed_initial_sensitivity_Dn=D,
    original_structural_source_mass=F(1,45))
@lru_cache(maxsize=None)
def sources(w):
    check(w)
    r=tuple(source_atom(w,x,n) for x in INITIALS for n in TIMES)
    assert len(r)==45 and sum((z["original_structural_source_mass"] for z in r),ZERO)==ONE
    return r
def semigroup(w,x,m,n):
    if x not in INITIALS or m not in TIMES or n not in TIMES or m+n>4:
        raise ValueError("unfrozen semigroup")
    a=direct_orbit(w,x,m+n)[0]
    b=direct_orbit(w,x,m)[0]
    for _ in range(n):b=f(w,b)
    return a==b
def world_result(w):
    for x in INITIALS:
        for m in TIMES:
            for n in TIMES:
                if m+n<=4 and not semigroup(w,x,m,n):raise AssertionError("finite semigroup failed")
    rows=sources(w)
    return dict(world=w,complete_original_cohort_time_source_atoms=45,
        rigorous_classification=CLAIMS[w],
        initial_cohort_step4_values=[str(direct_orbit(w,x,4)[0]) for x in INITIALS],
        initial_cohort_step4_sensitivity=[str(direct_orbit(w,x,4)[1]) for x in INITIALS],
        exact_source_joint={"|".join((str(r["original_initial_x0"]),str(r["original_time_n"]))):
           dict(state=str(r["observed_state_xn"]),V=str(r["observed_positive_candidate_Vn"]),
               deltaV=str(r["observed_one_step_delta_V"])) for r in rows},
        independent_formal_polynomial_composition_and_derivative_verified=True,
        finite_cohort_autonomous_semigroup_verified=True)
def emit():
    cert=certificate()
    data=dict(research_id="R251",original_catalogue_id="11-011",prescore_freeze_commit=FREEZE,
        scientific_scope="FINITE_ARTIFICIAL_E1_DISCRETE_LYAPUNOV_CANDIDATE_AND_TWO_STEP_NONHYPERBOLIC_LOCAL_CERTIFICATES",
        frozen_worlds=9,complete_original_cohort_time_atoms=405,
        source_cohorts_per_world=9,time_points_per_cohort=5,
        one_step_vs_two_step_certificates=cert,
        no_actual_historical_stability_observations=True,
        new_real_human_E2=0,new_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",
        world_results=[world_result(w) for w in WORLDS])
    csvpath=HERE/"R251_ALL_405_ORIGINAL_LYAPUNOV_SOURCE_ATOMS.csv"
    keys=list(sources(WORLDS[0])[0])
    with csvpath.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=keys,lineterminator="\n");w.writeheader()
        for name in WORLDS:
            for r in sources(name):w.writerow({k:str(r[k]) for k in keys})
    result=HERE/"R251_EXACT_RESULTS.json"
    result.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R251",original_catalogue_id="11-011",frozen_worlds=9,
        all_complete_original_source_atoms=405,
        formal_polynomial_independent_state_sensitivity=True,
        nonhyperbolic_one_step_V_not_required_for_two_step_attraction=True,
        source_sha256=hashlib.sha256(csvpath.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(result.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R251_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_world_count(self):self.assertEqual(len(WORLDS),9)
    def test_total_source_count(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),405)
    def test_all_analytic_certificates(self):self.assertEqual(len(certificate()),9)
    def test_positive_candidate(self):
        for x in INITIALS:
            self.assertEqual(v(x),x*x)
            self.assertTrue(v(x)>=0)
    def test_linear_contractions(self):
        for w in ("HALF_CONTRACTION","NEGATIVE_HALF_CONTRACTION"):
            self.assertEqual(delta(w,F(1,4)),F(-3,64))
    def test_linear_expansion(self):self.assertEqual(delta("DOUBLE_EXPANSION",F(1,4)),F(3,16))
    def test_neutral_sign_flip(self):self.assertEqual(delta("SIGN_FLIP_NEUTRAL",F(1,2)),ZERO)
    def test_cubic_inward(self):self.assertLess(delta("CUBIC_LOCAL_INWARD",F(1,4)),ZERO)
    def test_cubic_outward(self):self.assertGreater(delta("CUBIC_OUTWARD",F(-1,4)),ZERO)
    def test_logistic_one_step_failure(self):
        self.assertGreater(delta("LOGISTIC_R3_CENTERED",F(1,12)),ZERO)
        self.assertLess(delta("LOGISTIC_R3_CENTERED",F(-1,12)),ZERO)
    def test_logistic_two_step(self):
        self.assertEqual(composition("LOGISTIC_R3_CENTERED",2),(ZERO,ONE,ZERO,F(-18),F(-27)))
    def test_unfrozen_initial(self):
        with self.assertRaises(ValueError):direct_orbit("HALF_CONTRACTION",F(1,3),4)

def _case(world,kind):
    def t(self):
        rows=sources(world)
        if kind=="mass":self.assertEqual(sum((r["original_structural_source_mass"] for r in rows),ZERO),ONE)
        elif kind=="unique":self.assertEqual(len({(r["original_initial_x0"],r["original_time_n"]) for r in rows}),45)
        elif kind=="positive":self.assertTrue(all(r["original_structural_source_mass"]==F(1,45) for r in rows))
        elif kind=="independent":
            for x in INITIALS:
                for n in TIMES:self.assertEqual(direct_orbit(world,x,n),independent_state(world,x,n))
        elif kind=="derivative":
            for r in rows:self.assertEqual(r["observed_initial_sensitivity_Dn"],
                independent_state(world,r["original_initial_x0"],r["original_time_n"])[1])
        elif kind=="V":
            for r in rows:
                self.assertEqual(r["observed_positive_candidate_Vn"],v(r["observed_state_xn"]))
                self.assertEqual(r["observed_one_step_delta_V"],delta(world,r["observed_state_xn"]))
        elif kind=="semigroup":
            for x in INITIALS:
                for m in TIMES:
                    for n in TIMES:
                        if m+n<=4:self.assertTrue(semigroup(world,x,m,n))
        elif kind=="summary":self.assertEqual(world_result(world)["complete_original_cohort_time_source_atoms"],45)
        else:raise AssertionError("unfrozen case")
    return t
for w in WORLDS:
    for kind in ("mass","unique","positive","independent","derivative","V","semigroup","summary"):
        setattr(Tests,"test_"+w.lower()+"_"+kind,_case(w,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r251"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
