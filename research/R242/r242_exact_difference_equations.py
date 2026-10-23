#!/usr/bin/env python3
"""R242 exact discrete recurrences, nine artificial worlds, 180 complete atoms.

Independent polynomial-composition reference recovers the finite recurrence
trajectory and initial sensitivity, separate from stepwise state transitions.
Observed sensors and oracle hidden states are intentionally not conflated.
"""
from __future__ import annotations
import csv,hashlib,itertools,json,argparse,unittest
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="89a2a8d3a4166541bf34ed9a0fdf5fda52cc7762"
ZERO=F(0);ONE=F(1)
INITIALS=(F(1,4),F(1,2),F(3,4),ONE)
STEPS=(0,1,2,3,4)
WORLDS=(
"CONTRACTION_HALF","CONTRACTION_SENSOR_ALIAS",
"CONTRACTION_DOUBLE_COORDINATE_ALIAS","EXPANSION_DOUBLE",
"EXPANSION_SENSOR_ALIAS","SIGN_FLIP_SQUARED_SENSOR",
"STATIONARY_SQUARED_SENSOR","LOGISTIC_R2","LOGISTIC_R4")
ALIASES=(
("CONTRACTION_HALF","CONTRACTION_SENSOR_ALIAS","CONTRACTION_DOUBLE_COORDINATE_ALIAS"),
("EXPANSION_DOUBLE","EXPANSION_SENSOR_ALIAS"),
("SIGN_FLIP_SQUARED_SENSOR","STATIONARY_SQUARED_SENSOR"))
LINEAR={
"CONTRACTION_HALF":F(1,2),
"CONTRACTION_SENSOR_ALIAS":ONE,
"CONTRACTION_DOUBLE_COORDINATE_ALIAS":F(1,2),
"EXPANSION_DOUBLE":F(2),
"EXPANSION_SENSOR_ALIAS":ONE,
"SIGN_FLIP_SQUARED_SENSOR":-ONE,
"STATIONARY_SQUARED_SENSOR":ONE,
}
LOGISTIC={"LOGISTIC_R2":F(2),"LOGISTIC_R4":F(4)}
def require(world):
    if world not in WORLDS:raise ValueError("not frozen world")

def start(world,x):
    require(world)
    if x not in INITIALS:raise ValueError("not frozen initial condition")
    return 2*x if world=="CONTRACTION_DOUBLE_COORDINATE_ALIAS" else x

def initial_derivative(world):
    require(world)
    return F(2) if world=="CONTRACTION_DOUBLE_COORDINATE_ALIAS" else ONE

def transition(world,h):
    require(world)
    return LINEAR[world]*h if world in LINEAR else LOGISTIC[world]*h*(ONE-h)

def transition_derivative(world,h):
    require(world)
    return LINEAR[world] if world in LINEAR else LOGISTIC[world]*(ONE-2*h)

def sensor(world,n,h):
    require(world)
    if n not in STEPS:raise ValueError("not frozen observed time")
    if world=="CONTRACTION_SENSOR_ALIAS":return F(1,2)**n*h
    if world=="CONTRACTION_DOUBLE_COORDINATE_ALIAS":return h/2
    if world=="EXPANSION_SENSOR_ALIAS":return F(2)**n*h
    if world in ("SIGN_FLIP_SQUARED_SENSOR","STATIONARY_SQUARED_SENSOR"):return h*h
    return h

def sensor_initial_sensitivity(world,n,h,D):
    if world=="CONTRACTION_SENSOR_ALIAS":return F(1,2)**n*D
    if world=="CONTRACTION_DOUBLE_COORDINATE_ALIAS":return D/2
    if world=="EXPANSION_SENSOR_ALIAS":return F(2)**n*D
    if world in ("SIGN_FLIP_SQUARED_SENSOR","STATIONARY_SQUARED_SENSOR"):return 2*h*D
    return D

def iterative_state(world,x,n):
    require(world)
    if n not in STEPS:raise ValueError("not frozen finite iteration")
    h=start(world,x);D=initial_derivative(world)
    for _ in range(n):
        D=transition_derivative(world,h)*D
        h=transition(world,h)
    return h,D

# polynomial coefficients for p(X)=sum c_i X^i; exact algebra.
def poly_add(a,b):
    n=max(len(a),len(b))
    return tuple((a[i] if i<len(a) else ZERO)+(b[i] if i<len(b) else ZERO) for i in range(n))
def poly_scale(a,c):return tuple(c*x for x in a)
def poly_mul(a,b):
    out=[ZERO]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return tuple(out)
def poly_eval(coeff,x):
    v=ZERO
    for c in reversed(coeff):v=v*x+c
    return v
def poly_derivative(p):return tuple(i*p[i] for i in range(1,len(p))) or (ZERO,)
def independently_composed_polynomial(world,n):
    require(world)
    if n not in STEPS:raise ValueError("unfrozen polynomial degree")
    p=(ZERO,ONE)  # identity variable H0
    for _ in range(n):
        if world in LINEAR:p=poly_scale(p,LINEAR[world])
        else:p=poly_add(poly_scale(p,LOGISTIC[world]),
                        poly_scale(poly_mul(p,p),-LOGISTIC[world]))
    return p
def independently_composed_state(world,x,n):
    poly=independently_composed_polynomial(world,n)
    h0=start(world,x)
    return poly_eval(poly,h0),poly_eval(poly_derivative(poly),h0)*initial_derivative(world)

def source_atom(world,x,n):
    h,d=iterative_state(world,x,n)
    other,otherd=independently_composed_state(world,x,n)
    if (h,d)!=(other,otherd):
        raise AssertionError("state recurrence and polynomial composition mismatch")
    y=sensor(world,n,h)
    dy=sensor_initial_sensitivity(world,n,h,d)
    return dict(
       world=world,observed_initial_cohort=x,observed_step_n=n,
       observed_output_y=y,
       observed_initial_cohort_sensitivity=dy,
       oracle_hidden_initial_h0=start(world,x),
       oracle_hidden_state_h=h,
       oracle_hidden_initial_derivative=d,
       oracle_hidden_true_one_step_next=transition(world,h),
       oracle_hidden_change_from_start=h-start(world,x),
       original_source_probability=F(1,20)
    )
def sources(world):
    require(world)
    rows=tuple(source_atom(world,x,n) for x in INITIALS for n in STEPS)
    if len(rows)!=20 or sum((r["original_source_probability"] for r in rows),ZERO)!=ONE:
        raise AssertionError("complete original source universe invalid")
    return rows
def visible_joint(world):
    d=defaultdict(F)
    for r in sources(world):
        key=(r["observed_initial_cohort"],r["observed_step_n"],r["observed_output_y"])
        d[key]+=r["original_source_probability"]
    return dict(sorted(d.items()))
def visible_sensitivity_joint(world):
    d={}
    for r in sources(world):
        d[(r["observed_initial_cohort"],r["observed_step_n"])]=r["observed_initial_cohort_sensitivity"]
    return d

def hidden_semigroup(world,x,m,n):
    if m<0 or n<0 or m+n>4:raise ValueError("outside frozen verification horizon")
    a,_=iterative_state(world,x,m+n)
    b,_=iterative_state(world,x,m)
    for _ in range(n):b=transition(world,b)
    return a==b

def alias_certificates():
    for group in ALIASES:
        for a,b in itertools.combinations(group,2):
            if visible_joint(a)!=visible_joint(b) or visible_sensitivity_joint(a)!=visible_sensitivity_joint(b):
                raise AssertionError("full observed trajectory/sensitivity alias broken")
    assert iterative_state("CONTRACTION_HALF",ONE,4)[0]==F(1,16)
    assert iterative_state("CONTRACTION_SENSOR_ALIAS",ONE,4)[0]==ONE
    assert iterative_state("EXPANSION_DOUBLE",ONE,4)[0]==F(16)
    assert iterative_state("EXPANSION_SENSOR_ALIAS",ONE,4)[0]==ONE
    assert iterative_state("SIGN_FLIP_SQUARED_SENSOR",ONE,1)[0]==-ONE
    assert iterative_state("STATIONARY_SQUARED_SENSOR",ONE,1)[0]==ONE
    return True

def world_result(world):
    data=sources(world)
    for x in INITIALS:
        for m in STEPS:
            for n in STEPS:
                if m+n<=4 and not hidden_semigroup(world,x,m,n):
                    raise AssertionError("autonomous discrete semigroup violated")
    if world=="LOGISTIC_R2":
        assert [iterative_state(world,F(1,2),n)[0] for n in STEPS]==[F(1,2)]*5
    if world=="LOGISTIC_R4":
        assert [iterative_state(world,F(1,2),n)[0] for n in STEPS]==[F(1,2),ONE,ZERO,ZERO,ZERO]
        assert [iterative_state(world,F(1,4),n)[0] for n in STEPS]==[F(1,4)]+[F(3,4)]*4
        assert iterative_state(world,F(1,2),1)[1]==ZERO
    return dict(
        world=world,full_original_cohort_time_atoms=20,
        exact_visible_joint={"|".join(map(str,k)):str(v) for k,v in visible_joint(world).items()},
        observed_output_for_initial_one_by_steps=[
            str(sensor(world,n,iterative_state(world,ONE,n)[0])) for n in STEPS
        ],
        oracle_true_hidden_for_initial_one_by_steps=[
            str(iterative_state(world,ONE,n)[0]) for n in STEPS
        ],
        observed_initial_sensitivity_for_initial_one_by_steps=[
            str(source_atom(world,ONE,n)["observed_initial_cohort_sensitivity"]) for n in STEPS
        ],
        observed_initial_half_trajectory=[
            str(source_atom(world,F(1,2),n)["observed_output_y"]) for n in STEPS
        ],
        observed_initial_quarter_trajectory=[
            str(source_atom(world,F(1,4),n)["observed_output_y"]) for n in STEPS
        ],
        full_20_original_source_rows=[
            {k:str(v) if isinstance(v,F) else v for k,v in r.items()} for r in data
        ],
        polynomial_composition_vs_recursion_verified=True,
        full_hidden_semigroup_horizon4_verified=True
    )
def generate():
    alias_certificates()
    results=dict(
        research_id="R242",original_catalogue_id="11-002",
        prescore_freeze_commit=FREEZE,
        scientific_scope="FINITE_ARTIFICIAL_E1_EXACT_DISCRETE_DIFFERENCE_MAP_AND_SENSOR_NONIDENTIFICATION",
        frozen_worlds=9,original_source_cohort_time_atoms=180,
        full_observation_and_sensitivity_alias_families=[list(a) for a in ALIASES],
        exact_polynomial_composition_and_derivative_agreement=True,
        exact_hidden_semigroup=True,
        new_real_human_E2=0,new_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",
        world_results=[world_result(w) for w in WORLDS]
    )
    csvpath=HERE/"R242_ALL_180_ORIGINAL_DIFFERENCE_EQUATION_ATOMS.csv"
    fields=list(sources("CONTRACTION_HALF")[0])
    with csvpath.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        writer.writeheader()
        for w in WORLDS:
            for r in sources(w):writer.writerow({k:str(r[k]) for k in fields})
    out=HERE/"R242_EXACT_RESULTS.json"
    out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    machine=dict(research_id="R242",original_catalogue_id="11-002",
        frozen_worlds=9,original_full_cohort_time_atoms=180,
        three_full_observation_sensor_alias_families=True,
        independent_polynomial_and_derivative_certificates=True,
        logistic_exact_fixed_points_4step=True,
        source_sha256=hashlib.sha256(csvpath.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R242_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(machine,indent=2)+"\n",encoding="utf-8")
    return machine

class Tests(unittest.TestCase):
    def test_all_nine(self):self.assertEqual(len(WORLDS),9)
    def test_all_180(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),180)
    def test_observation_aliases(self):self.assertTrue(alias_certificates())
    def test_contraction_one_four(self):
        self.assertEqual(sensor("CONTRACTION_HALF",4,iterative_state("CONTRACTION_HALF",ONE,4)[0]),F(1,16))
    def test_expansion_one_four(self):
        self.assertEqual(iterative_state("EXPANSION_DOUBLE",ONE,4)[0],F(16))
    def test_logistic_two_fixed(self):
        self.assertEqual([iterative_state("LOGISTIC_R2",F(1,2),n)[0] for n in STEPS],[F(1,2)]*5)
    def test_logistic_four_transient(self):
        self.assertEqual([iterative_state("LOGISTIC_R4",F(1,2),n)[0] for n in STEPS],[F(1,2),ONE,ZERO,ZERO,ZERO])
    def test_logistic_four_other_fixed(self):
        self.assertEqual([iterative_state("LOGISTIC_R4",F(1,4),n)[0] for n in STEPS],[F(1,4)]+[F(3,4)]*4)
    def test_logistic_zero_derivative(self):
        self.assertEqual(iterative_state("LOGISTIC_R4",F(1,2),1)[1],ZERO)
    def test_square_alias_reveals_hidden_difference(self):
        self.assertEqual(visible_joint("SIGN_FLIP_SQUARED_SENSOR"),visible_joint("STATIONARY_SQUARED_SENSOR"))
        self.assertNotEqual(iterative_state("SIGN_FLIP_SQUARED_SENSOR",ONE,1)[0],iterative_state("STATIONARY_SQUARED_SENSOR",ONE,1)[0])
    def test_poly_diff(self):
        self.assertEqual(poly_derivative((ONE,F(2),F(3))),(F(2),F(6)))
    def test_missing_initial(self):
        with self.assertRaises(ValueError):start("CONTRACTION_HALF",F(2))
    def test_unknown(self):
        with self.assertRaises(ValueError):sources("UNKNOWN")

def _test(world,kind):
    def t(self):
        rows=sources(world)
        if kind=="mass":
            self.assertEqual(sum((r["original_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({(r["observed_initial_cohort"],r["observed_step_n"]) for r in rows}),20)
        elif kind=="positive":
            self.assertTrue(all(r["original_source_probability"]>0 for r in rows))
        elif kind=="polynomial":
            for x in INITIALS:
                for n in STEPS:
                    self.assertEqual(iterative_state(world,x,n),independently_composed_state(world,x,n))
        elif kind=="derivative":
            for r in rows:
                self.assertEqual(r["observed_initial_cohort_sensitivity"],
                    sensor_initial_sensitivity(world,r["observed_step_n"],r["oracle_hidden_state_h"],
                                               r["oracle_hidden_initial_derivative"]))
        elif kind=="semigroup":
            for x in INITIALS:
                for m in STEPS:
                    for n in STEPS:
                        if m+n<=4:self.assertTrue(hidden_semigroup(world,x,m,n))
        elif kind=="observed":
            self.assertEqual(sum(visible_joint(world).values(),ZERO),ONE)
        elif kind=="report":
            self.assertEqual(world_result(world)["full_original_cohort_time_atoms"],20)
        else:raise AssertionError("wrong test kind")
    return t
for _w in WORLDS:
    for _kind in ("mass","unique","positive","polynomial","derivative","semigroup","observed","report"):
        setattr(Tests,f"test_{_w.lower()}_{_kind}",_test(_w,_kind))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=parser.parse_args()
    if a.test:unittest.main(argv=["r242"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
