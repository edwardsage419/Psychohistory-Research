#!/usr/bin/env python3
"""R258 exact 3-stage finite-state stochastic control with policy information limits.

Nine artificial Bernoulli shock worlds, 3 initial states and all 64 original
six-bit disturbances, totaling 1728 original source atoms. Bellman feedback
is independently verified against all 512 deterministic time-state Markov
policies, and eight less-informed open-loop policies; no clairvoyant actions.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="62b3cff2023ec7f4d0a35dbb408a6b24c8d6f5ae"
ZERO=F(0);ONE=F(1)
BITS=(0,1)
INITIALS=(0,1,2)
SHOCK_BITS=tuple(itertools.product(BITS,repeat=6))
SHOCK_PATHS=tuple(itertools.product(BITS,repeat=3))
OPEN_ACTIONS=tuple(itertools.product(BITS,repeat=3))
POLICIES=tuple(itertools.product(BITS,repeat=9))
T=(0,1,2)
CONFIG={
 "NO_SHOCK_EXPENSIVE":(ZERO,F(2),ONE),
 "NO_SHOCK_CHEAP":(ZERO,F(1,4),ONE),
 "HALF_SHOCK_LOW_ACTION":(F(1,2),F(1,4),ONE),
 "HALF_SHOCK_MEDIUM":(F(1,2),ONE,ONE),
 "HALF_SHOCK_HIGH":(F(1,2),F(4),ONE),
 "QUARTER_SHOCK_MEDIUM":(F(1,4),ONE,ONE),
 "THREEQUARTER_SHOCK_MEDIUM":(F(3,4),ONE,ONE),
 "ALWAYS_SHOCK_MEDIUM":(ONE,ONE,ONE),
 "HALF_SHOCK_NO_TERMINAL":(F(1,2),ONE,ZERO)
}
WORLDS=tuple(CONFIG)
EXPECTED_VALUE={
 "NO_SHOCK_EXPENSIVE":("0","3","9"),
 "NO_SHOCK_CHEAP":("0","5/4","11/2"),
 "HALF_SHOCK_LOW_ACTION":("3/4","21/8","77/8"),
 "HALF_SHOCK_MEDIUM":("5/2","9/2","47/4"),
 "HALF_SHOCK_HIGH":("35/8","75/8","16"),
 "QUARTER_SHOCK_MEDIUM":("5/4","13/4","293/32"),
 "THREEQUARTER_SHOCK_MEDIUM":("11/4","45/8","949/64"),
 "ALWAYS_SHOCK_MEDIUM":("3","7","16"),
 "HALF_SHOCK_NO_TERMINAL":("3/2","7/2","10")
}
EXPECTED_OPEN={
 "NO_SHOCK_EXPENSIVE":("0","3","9"),
 "NO_SHOCK_CHEAP":("0","5/4","11/2"),
 "HALF_SHOCK_LOW_ACTION":("3/4","21/8","77/8"),
 "HALF_SHOCK_MEDIUM":("5/2","19/4","95/8"),
 "HALF_SHOCK_HIGH":("35/8","75/8","16"),
 "QUARTER_SHOCK_MEDIUM":("53/32","117/32","603/64"),
 "THREEQUARTER_SHOCK_MEDIUM":("11/4","367/64","959/64"),
 "ALWAYS_SHOCK_MEDIUM":("3","7","16"),
 "HALF_SHOCK_NO_TERMINAL":("3/2","15/4","10")
}
def check(w):
    if w not in CONFIG:raise ValueError("unfrozen finite control world")
def next_state(x,u,d):
    if x not in INITIALS or u not in BITS or d not in BITS:
        raise ValueError("not state/action/shock in frozen space")
    return min(2,max(0,x+d-u))
@lru_cache(None)
def dynamic_program(w):
    """First independent mathematical route: backward Bellman recursion."""
    check(w);p,k,tau=CONFIG[w]
    v={x:tau*x*x for x in INITIALS}
    Vs={3:v}
    pi={}
    for t in reversed(T):
        new={}
        for x in INITIALS:
            action_values={}
            for u in BITS:
                action_values[u]=F(x*x)+k*u+(ONE-p)*v[next_state(x,u,0)]+p*v[next_state(x,u,1)]
            ustar=min(BITS,key=lambda u:(action_values[u],u))
            pi[t,x]=ustar
            new[x]=action_values[ustar]
        v=new;Vs[t]=new
    return Vs,pi
def shocks_from_original(w,bits):
    check(w)
    if len(bits)!=6 or any(x not in BITS for x in bits):
        raise ValueError("requires six fair shock bits")
    p=CONFIG[w][0]
    return tuple(int(F(2*bits[2*t]+bits[2*t+1])<4*p) for t in T)
def simulate_bellman_original_source(w,x0,bits):
    if x0 not in INITIALS:raise ValueError("unknown original initial state")
    shock=shocks_from_original(w,bits)
    _,pi=dynamic_program(w)
    p,k,tau=CONFIG[w]
    x=x0;rows=[];total=ZERO
    for t,d in enumerate(shock):
        u=pi[t,x] # action selected before d; cannot read d
        stage=F(x*x)+k*u
        nx=next_state(x,u,d)
        rows.append((x,u,d,nx,stage))
        total+=stage;x=nx
    terminal=tau*x*x
    total+=terminal
    out={"world":w,"original_initial_state_x0":x0}
    for t in T:
        out["oracle_original_shock_R"+str(t)+"a"]=bits[2*t]
        out["oracle_original_shock_R"+str(t)+"b"]=bits[2*t+1]
        xt,u,d,after,cost=rows[t]
        out["observed_pre_action_state_x"+str(t)]=xt
        out["observed_chosen_feedback_action_u"+str(t)]=u
        out["oracle_realized_post_action_shock_d"+str(t)]=d
        out["observed_next_state_x"+str(t+1)]=after
        out["observed_stage_cost_c"+str(t)]=stage_strict(cost)
    out["observed_terminal_state_x3"]=x
    out["observed_terminal_cost"]=terminal
    out["observed_total_path_cost"]=total
    out["original_uniform_initial_and_sixbit_source_mass"]=F(1,192)
    return out
def stage_strict(cost):return cost
@lru_cache(None)
def sources(w):
    check(w)
    out=tuple(simulate_bellman_original_source(w,x0,b) for x0 in INITIALS for b in SHOCK_BITS)
    if len(out)!=192 or sum((r["original_uniform_initial_and_sixbit_source_mass"] for r in out),ZERO)!=ONE:
        raise AssertionError("192 complete initial and shock source combinations missing")
    return out
def exact_original_conditioned_costs(w):
    src=sources(w)
    return tuple(sum((r["observed_total_path_cost"]*3*r["original_uniform_initial_and_sixbit_source_mass"]
             for r in src if r["original_initial_state_x0"]==x0),ZERO) for x0 in INITIALS)
def noise_scenarios(w):
    """Independent three Bernoulli steps in the abstract shock space, not source bits."""
    p=CONFIG[w][0]
    scenarios=[]
    for ds in SHOCK_PATHS:
        mass=ONE
        for d in ds:mass*=p if d else (ONE-p)
        if mass>0:scenarios.append((ds,mass))
    assert sum((m for ds,m in scenarios),ZERO)==ONE
    return tuple(scenarios)
def evaluate_independent_policy(w,policy,x0,open_loop=False):
    """Second mathematical route: evaluate a full policy on 8 abstract shock histories."""
    check(w);p,k,tau=CONFIG[w]
    assert len(policy)==(3 if open_loop else 9)
    total=ZERO
    for ds,mass in noise_scenarios(w):
        x=x0;cost=ZERO
        for t,d in enumerate(ds):
            u=policy[t] if open_loop else policy[3*t+x]
            cost+=x*x+k*u
            x=min(2,max(0,x+d-u)) # no original source transition helper
        cost+=tau*x*x
        total+=mass*cost
    return total
@lru_cache(None)
def all_feedback_policy_exhaustive_min(w):
    """All 512 time×state feedback laws, fully independent from Bellman recursion."""
    check(w)
    minima=[None,None,None]
    for policy in POLICIES:
        for x0 in INITIALS:
            v=evaluate_independent_policy(w,policy,x0)
            if minima[x0] is None or v<minima[x0]:
                minima[x0]=v
    return tuple(minima)
@lru_cache(None)
def all_open_loop_exhaustive_min(w):
    check(w)
    return tuple(min(evaluate_independent_policy(w,policy,x0,open_loop=True)
                     for policy in OPEN_ACTIONS) for x0 in INITIALS)
def locked_claims():
    for w in WORLDS:
        Vs,pi=dynamic_program(w)
        dp=tuple(Vs[0][x] for x in INITIALS)
        full=all_feedback_policy_exhaustive_min(w)
        src=exact_original_conditioned_costs(w)
        opened=all_open_loop_exhaustive_min(w)
        expected=tuple(F(s) for s in EXPECTED_VALUE[w])
        ex_open=tuple(F(s) for s in EXPECTED_OPEN[w])
        if dp!=full or dp!=src or dp!=expected:
            raise AssertionError(f"{w} Bellman vs full 512 policy / original bit source mismatch {dp} {full} {src} {expected}")
        if opened!=ex_open or any(a>b for a,b in zip(dp,opened)):
            raise AssertionError(f"{w} open-loop restricted optimum mismatch {opened} {ex_open}")
    w="HALF_SHOCK_MEDIUM"
    val=tuple(dynamic_program(w)[0][0][x] for x in INITIALS)
    op=all_open_loop_exhaustive_min(w)
    assert tuple(o-v for o,v in zip(op,val))==(ZERO,F(1,4),F(1,8))
    w="QUARTER_SHOCK_MEDIUM"
    assert all_open_loop_exhaustive_min(w)[0]-dynamic_program(w)[0][0][0]==F(13,32)
    return True
def result_world(w):
    Vs,policy=dynamic_program(w)
    source=exact_original_conditioned_costs(w)
    other=all_feedback_policy_exhaustive_min(w)
    opened=all_open_loop_exhaustive_min(w)
    if source!=other or other!=tuple(Vs[0][x] for x in INITIALS):
        raise AssertionError("exact full source expectation not equal exhaustive control optimality")
    return dict(world=w,
      frozen_shock_probability=str(CONFIG[w][0]),
      frozen_action_cost_kappa=str(CONFIG[w][1]),
      frozen_terminal_weight_tau=str(CONFIG[w][2]),
      complete_original_initial_and_sixbit_source_atoms=192,
      Bellman_V0_by_initial_state=[str(v) for v in source],
      exhaustive_512_feedback_policy_global_min_by_initial_state=[str(v) for v in other],
      best_of_8_open_loop_action_sequence_values=[str(v) for v in opened],
      strictly_nonnegative_open_loop_value_gaps=[str(o-s) for o,s in zip(opened,source)],
      optimal_feedback_actions_by_time_and_state={
          str(t):[policy[t,x] for x in INITIALS] for t in T},
      all_Bellman_value_layers={
          str(t):[str(Vs[t][x]) for x in INITIALS] for t in (0,1,2,3)},
      oracle_original_source_policy_cost_parity=True,
      full_exhaustive_admissible_feedback_policy_parity=True,
      all_eight_open_loop_strategies_checked=True)
def emit():
    locked_claims()
    results=dict(research_id="R258",original_catalogue_id="11-018",
      prescore_freeze_commit=FREEZE,
      scientific_scope="FINITE_ARTIFICIAL_E1_THREE_STAGE_FINITE_STOCHASTIC_OPTIMAL_CONTROL",
      frozen_worlds=9,original_all_initial_sixbit_atom_types=1728,
      initial_states_per_world=3,sixbit_shock_paths_per_initial=64,
      distinct_legal_deterministic_Markov_feedback_policies_exhausted=512,
      distinct_open_loop_action_sequences_exhausted=8,
      decision_timing="action chosen after seeing current state and before seeing current/future shock",
      optimal_feedback_weakly_dominates_open_loop_under_identical_information_laws=True,
      no_actual_policy_data_or_empirical_causality_established=True,
      new_real_human_E2=0,new_real_historical_E3=0,
      R073="FROZEN",PESEN_v0_1="FROZEN",
      world_results=[result_world(w) for w in WORLDS])
    csvp=HERE/"R258_ALL_1728_ORIGINAL_THREESTEP_CONTROL_SOURCE_ATOMS.csv"
    keys=list(sources(WORLDS[0])[0])
    with csvp.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for row in sources(w):wr.writerow({k:str(row[k]) for k in keys})
    jp=HERE/"R258_EXACT_RESULTS.json"
    jp.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    rec=dict(research_id="R258",original_catalogue_id="11-018",frozen_worlds=9,
      full_original_sixbit_and_initial_atom_count=1728,
      exhaustive_512_noclaivoyance_feedback_policy_parity=True,
      original_full_source_vs_Bellman_parity=True,
      all_8_open_loop_controls_worse_or_equal=True,
      half_shock_medium_feedback_gaps=["0","1/4","1/8"],
      source_sha256=hashlib.sha256(csvp.read_bytes()).hexdigest(),
      results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
      new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R258_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
    return rec
class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_all_original_source_count(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),1728)
    def test_all_locked_values_and_independent_full_policies(self):self.assertTrue(locked_claims())
    def test_half_shock_medium_gap(self):
        w="HALF_SHOCK_MEDIUM"
        self.assertEqual(tuple(o-v for o,v in zip(all_open_loop_exhaustive_min(w),all_feedback_policy_exhaustive_min(w))),(ZERO,F(1,4),F(1,8)))
    def test_saturation(self):self.assertEqual(next_state(2,0,1),2)
    def test_preventive(self):self.assertEqual(next_state(0,1,1),0)
    def test_terminal(self):
        self.assertEqual(dynamic_program("HALF_SHOCK_NO_TERMINAL")[0][3][2],ZERO)
    def test_valid_policy_space(self):self.assertEqual(len(POLICIES),512)
    def test_valid_open_loop_space(self):self.assertEqual(len(OPEN_ACTIONS),8)
    def test_invalid(self):
        with self.assertRaises(ValueError):sources("ILLEGAL_CONTROL_WORLD")
def _case(w,k):
    def t(self):
        src=sources(w)
        if k=="mass":self.assertEqual(sum((r["original_uniform_initial_and_sixbit_source_mass"] for r in src),ZERO),ONE)
        elif k=="unique":
            cols=["original_initial_state_x0"]+["oracle_original_shock_R"+str(t)+s for t in T for s in ("a","b")]
            self.assertEqual(len({tuple(r[c] for c in cols) for r in src}),192)
        elif k=="positive":self.assertTrue(all(r["original_uniform_initial_and_sixbit_source_mass"]==F(1,192) for r in src))
        elif k=="cost":
            for r in src:
                total=sum((r["observed_stage_cost_c"+str(t)] for t in T),ZERO)+r["observed_terminal_cost"]
                self.assertEqual(total,r["observed_total_path_cost"])
        elif k=="law":
            for r in src:
                for n in T:self.assertEqual(r["observed_next_state_x"+str(n+1)],
                     next_state(r["observed_pre_action_state_x"+str(n)],
                          r["observed_chosen_feedback_action_u"+str(n)],
                          r["oracle_realized_post_action_shock_d"+str(n)]))
        elif k=="Bellman":self.assertEqual(exact_original_conditioned_costs(w),tuple(dynamic_program(w)[0][0][x] for x in INITIALS))
        elif k=="all512":self.assertEqual(all_feedback_policy_exhaustive_min(w),exact_original_conditioned_costs(w))
        elif k=="report":self.assertEqual(result_world(w)["complete_original_initial_and_sixbit_source_atoms"],192)
        else:raise AssertionError("not frozen")
    return t
for w in WORLDS:
    for k in ("mass","unique","positive","cost","law","Bellman","all512","report"):
        setattr(Tests,"test_"+w.lower()+"_"+k,_case(w,k))
if __name__=="__main__":
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    args=ap.parse_args()
    if args.test:unittest.main(argv=["r258"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
