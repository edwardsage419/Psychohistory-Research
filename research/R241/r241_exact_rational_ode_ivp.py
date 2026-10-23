#!/usr/bin/env python3
"""R241 finite exact rational ordinary differential equation source worlds.

No numerical time integrator: all paths are mathematically explicit Fraction
solutions. Independent IVP flow/derivative/measurement-chain/initial-sensitivity
certificates distinguish true state dynamics from time-varying observation maps.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ZERO=F(0);ONE=F(1)
FREEZE="65ca4f2cd300e911d68b624f7d7678936eafe50f"
INITIALS=(F(1,4),F(1,2),F(3,4),ONE)
TIMES=(ZERO,F(1,8),F(1,4),F(3,8),F(1,2))
WORLDS=(
 "DECAY_L1",
 "DECAY_L2",
 "DECAY_HIDDEN_DOUBLE_COORDINATE",
 "CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY",
 "GROWTH_L1",
 "CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH",
 "STATIONARY",
 "CONSTANT_RATE_PLUS1",
 "DECAY_NONLINEAR_SENSOR"
)
DECAY_VIEW_ALIASES=(
 "DECAY_L1","DECAY_HIDDEN_DOUBLE_COORDINATE",
 "CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY")
GROWTH_VIEW_ALIASES=("GROWTH_L1","CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH")

def domain(world):
    if world not in WORLDS:raise ValueError("world not prescore frozen")
    return True

def hidden_initial(world,x):
    domain(world)
    if x not in INITIALS:raise ValueError("unfrozen initial state cohort")
    return 2*x if world=="DECAY_HIDDEN_DOUBLE_COORDINATE" else x

def scalar_lambda(world):
    domain(world)
    if world=="DECAY_L2":return F(2)
    if world=="DECAY_HIDDEN_DOUBLE_COORDINATE":return F(1,2)
    if world=="GROWTH_L1":return -ONE
    if world in ("CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY",
                 "CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH",
                 "STATIONARY","CONSTANT_RATE_PLUS1"):return ZERO
    return ONE

def state_flow(world,h,t):
    domain(world)
    h,t=F(h),F(t)
    if t<0:raise ValueError("no negative experimental time")
    if world=="CONSTANT_RATE_PLUS1":return h+t
    lam=scalar_lambda(world)
    denom=ONE+lam*h*t
    if denom<=0:raise ValueError("finite-time blow-up outside growth solution domain")
    return h/denom

def hidden_state(world,x,t):
    return state_flow(world,hidden_initial(world,x),t)

def sensor(world,t,h):
    domain(world)
    t,h=F(t),F(h)
    if world=="DECAY_HIDDEN_DOUBLE_COORDINATE":return h/2
    if world=="CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY":
        return h/(ONE+h*t)
    if world=="CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH":
        if ONE-h*t<=0:raise ValueError("growth sensor singularity")
        return h/(ONE-h*t)
    if world=="DECAY_NONLINEAR_SENSOR":return h*h
    return h

def observed_from_state(world,x,t):
    return sensor(world,t,hidden_state(world,x,t))

def independent_observed_solution(world,x,t):
    """No state-flow or sensor functions; direct frozen rational visible formula."""
    domain(world)
    x,t=F(x),F(t)
    if world=="DECAY_L2":return x/(ONE+2*x*t)
    if world in DECAY_VIEW_ALIASES:return x/(ONE+x*t)
    if world in GROWTH_VIEW_ALIASES:
        if ONE-x*t<=0:raise ValueError("finite growth solution pole")
        return x/(ONE-x*t)
    if world=="STATIONARY":return x
    if world=="CONSTANT_RATE_PLUS1":return x+t
    if world=="DECAY_NONLINEAR_SENSOR":return (x/(ONE+x*t))**2
    raise AssertionError("unfrozen observed formula")

def rhs(world,h):
    domain(world)
    h=F(h)
    if world=="CONSTANT_RATE_PLUS1":return ONE
    return -scalar_lambda(world)*h*h

def analytic_hidden_derivative(world,x,t):
    h0=hidden_initial(world,x)
    lam=scalar_lambda(world)
    if world=="CONSTANT_RATE_PLUS1":return ONE
    return -lam*h0*h0/(ONE+lam*h0*F(t))**2

def sensor_chain_time_derivative(world,t,h,dh):
    t,h,dh=F(t),F(h),F(dh)
    if world=="DECAY_HIDDEN_DOUBLE_COORDINATE":return dh/2
    if world=="CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY":
        denom=(ONE+h*t)**2
        return -h*h/denom+dh/denom
    if world=="CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH":
        denom=(ONE-h*t)**2
        return h*h/denom+dh/denom
    if world=="DECAY_NONLINEAR_SENSOR":return 2*h*dh
    return dh

def independent_observed_derivative(world,x,t):
    """Closed-form differentiated observable trajectory; no chain-rule helper."""
    domain(world)
    x,t=F(x),F(t)
    if world=="DECAY_L2":return -2*x*x/(ONE+2*x*t)**2
    if world in DECAY_VIEW_ALIASES:return -x*x/(ONE+x*t)**2
    if world in GROWTH_VIEW_ALIASES:return x*x/(ONE-x*t)**2
    if world=="STATIONARY":return ZERO
    if world=="CONSTANT_RATE_PLUS1":return ONE
    if world=="DECAY_NONLINEAR_SENSOR":return -2*x**3/(ONE+x*t)**3
    raise AssertionError("no direct derivative formula")

def observed_initial_sensitivity(world,x,t):
    """Derivative wrt original displayed cohort x0, not hidden state scale."""
    domain(world)
    x,t=F(x),F(t)
    if world=="DECAY_L2":return ONE/(ONE+2*x*t)**2
    if world in DECAY_VIEW_ALIASES:return ONE/(ONE+x*t)**2
    if world in GROWTH_VIEW_ALIASES:return ONE/(ONE-x*t)**2
    if world in ("STATIONARY","CONSTANT_RATE_PLUS1"):return ONE
    if world=="DECAY_NONLINEAR_SENSOR":return 2*x/(ONE+x*t)**3
    raise AssertionError("no sensitivity")

def source_atom(world,x,t):
    if x not in INITIALS or t not in TIMES:raise ValueError("not frozen cohort/time source")
    h0=hidden_initial(world,x)
    h=hidden_state(world,x,t)
    y=observed_from_state(world,x,t)
    dy=sensor_chain_time_derivative(world,t,h,rhs(world,h))
    if rhs(world,h)!=analytic_hidden_derivative(world,x,t):
        raise AssertionError("exact IVP derivative vs right side violated")
    if dy!=independent_observed_derivative(world,x,t):
        raise AssertionError("observable derivative violates independent analytic formula")
    if y!=independent_observed_solution(world,x,t):
        raise AssertionError("observed sensor and direct rational formula disagree")
    return dict(
        world=world,observed_cohort_x0=x,observed_time=t,
        observed_y=y,observed_y_time_derivative=dy,
        observed_y_sensitivity_to_initial_x0=observed_initial_sensitivity(world,x,t),
        oracle_hidden_initial_h0=h0,oracle_hidden_h=h,
        oracle_state_ODE_rhs=rhs(world,h),
        oracle_hidden_dhdt=analytic_hidden_derivative(world,x,t),
        oracle_hidden_change_from_initial=h-h0,
        original_source_probability=F(1,20)
    )

def sources(world):
    domain(world)
    out=tuple(source_atom(world,x,t) for x in INITIALS for t in TIMES)
    if len(out)!=20 or sum((r["original_source_probability"] for r in out),ZERO)!=ONE:
        raise AssertionError("all exact rational trajectory sources not complete")
    return out

def observed_joint(world):
    result=defaultdict(F)
    for r in sources(world):
        key=(r["observed_cohort_x0"],r["observed_time"],r["observed_y"])
        result[key]+=r["original_source_probability"]
    return dict(sorted(result.items()))

def state_flow_semigroup(world,x,t,s):
    if t not in TIMES or s not in TIMES or t+s>F(1,2):raise ValueError("not prescore domain")
    h0=hidden_initial(world,x)
    one=state_flow(world,h0,t+s)
    two=state_flow(world,state_flow(world,h0,t),s)
    return one==two

def full_alias_certificates():
    for a,b in itertools.combinations(DECAY_VIEW_ALIASES,2):
        if observed_joint(a)!=observed_joint(b):
            raise AssertionError("decay hidden dynamics vs time-drifted measurement not observationally equivalent")
    if observed_joint(GROWTH_VIEW_ALIASES[0])!=observed_joint(GROWTH_VIEW_ALIASES[1]):
        raise AssertionError("growth vs stationary sensor alias not valid")
    for x in INITIALS:
        for t in TIMES:
            if t>0:
                if hidden_state("DECAY_L1",x,t)==hidden_state("CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY",x,t):
                    raise AssertionError("two aliased hidden states unexpectedly same for positive t")
                if hidden_state("GROWTH_L1",x,t)==hidden_state("CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH",x,t):
                    raise AssertionError("growth aliased stationary hidden state unexpectedly same")
    return True

def world_result(world):
    data=sources(world)
    for x in INITIALS:
        for t in TIMES:
            for s in TIMES:
                if t+s<=F(1,2) and not state_flow_semigroup(world,x,t,s):
                    raise AssertionError("autonomous hidden state flow semigroup violated")
    if world=="GROWTH_L1" and min(ONE/x for x in INITIALS)!=ONE:
        raise AssertionError("frozen first pole not time 1")
    result={
        "world":world,
        "complete_original_ivp_source_atoms":20,
        "minimum_finite_hidden_or_sensor_growth_pole_time":
             "1" if world in GROWTH_VIEW_ALIASES else None,
        "initial_cohorts":[str(x) for x in INITIALS],
        "exact_observed_times":[str(t) for t in TIMES],
        "time0_to_time_half_true_hidden_change_by_cohort":[str(hidden_state(world,x,F(1,2))-hidden_initial(world,x)) for x in INITIALS],
        "time0_to_time_half_observed_change_by_cohort":[str(observed_from_state(world,x,F(1,2))-observed_from_state(world,x,ZERO)) for x in INITIALS],
        "observed_time_half_initial_sensitivity_by_cohort":[str(observed_initial_sensitivity(world,x,F(1,2))) for x in INITIALS],
        "exact_observed_joint_with_cohort_and_time":{
            "|".join(map(str,k)):str(v) for k,v in observed_joint(world).items()
        },
        "all_exact_original_trajectory_points":[
            {k:str(v) if isinstance(v,F) else v for k,v in row.items()} for row in data
        ],
        "all_prescore_half_horizon_flow_semigroup_checks_passed":True,
        "all_analytic_hidden_and_observed_chain_derivatives_passed":True
    }
    if world in ("CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY","CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH","STATIONARY"):
        assert all(x=="0" for x in result["time0_to_time_half_true_hidden_change_by_cohort"])
    if world=="DECAY_L1":
        assert all(F(y)<0 for y in result["time0_to_time_half_observed_change_by_cohort"])
    if world=="GROWTH_L1":
        assert all(F(y)>0 for y in result["time0_to_time_half_observed_change_by_cohort"])
        assert all(F(y)>1 for y in result["observed_time_half_initial_sensitivity_by_cohort"])
    return result

def generate():
    full_alias_certificates()
    allresults=[world_result(w) for w in WORLDS]
    data=dict(
        research_id="R241",original_catalogue_id="11-001",
        prescore_freeze_commit=FREEZE,
        scientific_scope="FINITE_ARTIFICIAL_E1_EXACT_RATIONAL_ODE_INITIAL_VALUE_FLOW_AND_MEASUREMENT",
        frozen_worlds=9,original_ivp_time_source_atoms=180,
        cohort_initial_count=4,exact_time_support_size=5,
        exact_full_observed_joint_decay_alias_count=3,
        exact_full_observed_joint_growth_alias_count=2,
        independent_explicit_solution_vs_observation_and_chain_derivatives=True,
        true_hidden_autonomous_flow_semigroup=True,
        new_real_human_E2=0,new_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",
        world_results=allresults
    )
    out=HERE/"R241_ALL_180_EXACT_ODE_IVP_TIME_SOURCES.csv"
    fields=list(sources("DECAY_L1")[0])
    with out.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for row in sources(w):wr.writerow({k:str(row[k]) for k in fields})
    path=HERE/"R241_EXACT_RESULTS.json"
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(
        research_id="R241",original_catalogue_id="11-001",
        frozen_worlds=9,full_original_ivp_time_source_atoms=180,
        exact_state_ode_rhs_and_sensor_chain_rule_verified=True,
        exact_4cohort_5time_hidden_flow_semigroup=True,
        two_full_observation_alias_families=True,
        source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0
    )
    (HERE/"R241_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_nine_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_total_180_sources(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),180)
    def test_two_alias_families(self):self.assertTrue(full_alias_certificates())
    def test_decay_cohort(self):
        self.assertEqual(observed_from_state("DECAY_L1",ONE,F(1,2)),F(2,3))
    def test_hidden_measurement_stationary(self):
        self.assertEqual(hidden_state("CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY",ONE,F(1,2)),ONE)
        self.assertEqual(observed_from_state("CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY",ONE,F(1,2)),F(2,3))
    def test_growth_pole(self):
        with self.assertRaises(ValueError):observed_from_state("GROWTH_L1",ONE,ONE)
    def test_growth_sensor_pole(self):
        with self.assertRaises(ValueError):sensor("CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH",ONE,ONE)
    def test_constant_rate(self):
        self.assertEqual(observed_from_state("CONSTANT_RATE_PLUS1",ONE,F(1,2)),F(3,2))
    def test_double_state_reparam(self):
        self.assertEqual(hidden_state("DECAY_HIDDEN_DOUBLE_COORDINATE",ONE,F(1,2)),F(4,3))
        self.assertEqual(observed_from_state("DECAY_HIDDEN_DOUBLE_COORDINATE",ONE,F(1,2)),F(2,3))
    def test_nonlinear_sensor(self):
        self.assertEqual(observed_from_state("DECAY_NONLINEAR_SENSOR",ONE,F(1,2)),F(4,9))
        self.assertEqual(independent_observed_derivative("DECAY_NONLINEAR_SENSOR",ONE,F(1,2)),F(-16,27))
    def test_semigroup(self):
        for w in WORLDS:
            self.assertTrue(state_flow_semigroup(w,ONE,F(1,4),F(1,4)))
    def test_sensitivity_growth(self):
        self.assertEqual(observed_initial_sensitivity("GROWTH_L1",ONE,F(1,2)),F(4))
    def test_unknown_world(self):
        with self.assertRaises(ValueError):sources("NOT_FROZEN")

def _case(world,kind):
    def t(self):
        rows=sources(world)
        if kind=="mass":
            self.assertEqual(sum((r["original_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({(r["observed_cohort_x0"],r["observed_time"]) for r in rows}),20)
        elif kind=="direct_solution":
            for x in INITIALS:
                for tm in TIMES:
                    self.assertEqual(observed_from_state(world,x,tm),independent_observed_solution(world,x,tm))
        elif kind=="state_ode":
            for r in rows:self.assertEqual(r["oracle_state_ODE_rhs"],r["oracle_hidden_dhdt"])
        elif kind=="observed_chain":
            for r in rows:
                self.assertEqual(r["observed_y_time_derivative"],
                                 independent_observed_derivative(world,r["observed_cohort_x0"],r["observed_time"]))
        elif kind=="semigroup":
            for x in INITIALS:
                for tm in TIMES:
                    for dt in TIMES:
                        if tm+dt<=F(1,2):
                            self.assertTrue(state_flow_semigroup(world,x,tm,dt))
        elif kind=="joint":
            self.assertEqual(sum(observed_joint(world).values(),ZERO),ONE)
        elif kind=="report":
            self.assertEqual(world_result(world)["complete_original_ivp_source_atoms"],20)
        else:raise AssertionError("not a prescore test")
    return t
for _w in WORLDS:
    for _kind in ("mass","unique","direct_solution","state_ode","observed_chain","semigroup","joint","report"):
        setattr(Tests,"test_"+_w.lower()+"_"+_kind,_case(_w,_kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    arg=p.parse_args()
    if arg.test:unittest.main(argv=["r241"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
