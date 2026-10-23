#!/usr/bin/env python3
"""R260 complete finite two-bit scenario robustness, nine artificial worlds.

5 action labels x 4 complete binary scenario types x three hard uncertainty
budgets Gamma=0,1,2 per world: 540 original source atoms. Source design mass
is *not* the shock probability; only the separately frozen iid fair shock
distribution gives a risk-neutral expected cost. Minimax cost and minimax
regret are distinct optimization problems.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,itertools,unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="e04a1601506367fb54f4f3db70a763f96f53102e"
ZERO=F(0);ONE=F(1)
ACTIONS=tuple("ABCDE")
SHOCKS=((0,0),(0,1),(1,0),(1,1))
BUDGETS=(0,1,2)
CONFIG={
"ALIGNED_DOMINANCE":((1,2,2,3),(2,3,3,4),(3,4,4,5),(4,5,5,6),(5,6,6,7)),
"HIDDEN_JOINT_TAIL":((0,0,0,12),(2,3,3,4),(3,3,3,3),(4,4,4,4),(5,5,5,5)),
"REGRET_VS_WORST":((0,0,0,8),(2,2,2,5),(4,4,4,4),(5,5,5,5),(6,6,6,6)),
"NONMONOTONE_SHOCK_COST":((4,1,1,0),(2,2,2,2),(3,1,2,3),(5,0,0,5),(6,6,6,6)),
"TWO_SHOCK_INTERACTION":((0,0,0,10),(1,4,4,5),(3,3,3,3),(4,4,4,4),(6,6,6,6)),
"ADDITIVE_COMMON_SHOCK":((0,1,2,3),(2,3,4,5),(3,4,5,6),(4,5,6,7),(5,6,7,8)),
"HIDDEN_TAIL_ALIAS":((0,0,0,0),(2,3,3,4),(3,3,3,3),(4,4,4,4),(5,5,5,5)),
"TIED_WORST_CASE":((0,2,2,2),(1,1,1,3),(2,2,2,2),(3,3,3,3),(4,4,4,4)),
"HEDGE_VS_NOMINAL":((0,6,6,6),(2,2,4,4),(3,3,3,3),(1,5,5,5),(4,4,4,4)),
}
WORLDS=tuple(CONFIG)
EXPECTED={
"ALIGNED_DOMINANCE":((1,"A",0,"A"),(2,"A",0,"A"),(3,"A",0,"A")),
"HIDDEN_JOINT_TAIL":((0,"A",0,"A"),(0,"A",0,"A"),(3,"C",3,"BC")),
"REGRET_VS_WORST":((0,"A",0,"A"),(0,"A",0,"A"),(4,"C",2,"B")),
"NONMONOTONE_SHOCK_COST":((2,"B",0,"B"),(2,"B",2,"ABC"),(2,"B",2,"AB")),
"TWO_SHOCK_INTERACTION":((0,"A",0,"A"),(0,"A",0,"A"),(3,"C",3,"C")),
"ADDITIVE_COMMON_SHOCK":((0,"A",0,"A"),(2,"A",0,"A"),(3,"A",0,"A")),
"HIDDEN_TAIL_ALIAS":((0,"A",0,"A"),(0,"A",0,"A"),(0,"A",0,"A")),
"TIED_WORST_CASE":((0,"A",0,"A"),(1,"B",1,"AB"),(2,"AC",1,"AB")),
"HEDGE_VS_NOMINAL":((0,"A",0,"A"),(3,"C",2,"B"),(3,"C",2,"B")),
}
EXPECTED_FAIR={
"ALIGNED_DOMINANCE":("2","A"),
"HIDDEN_JOINT_TAIL":("3","ABC"),
"REGRET_VS_WORST":("2","A"),
"NONMONOTONE_SHOCK_COST":("3/2","A"),
"TWO_SHOCK_INTERACTION":("5/2","A"),
"ADDITIVE_COMMON_SHOCK":("3/2","A"),
"HIDDEN_TAIL_ALIAS":("0","A"),
"TIED_WORST_CASE":("3/2","AB"),
"HEDGE_VS_NOMINAL":("3","BC"),
}
def check(w):
    if w not in CONFIG:raise ValueError("not in frozen scenario worlds")
def original_cost(w,a,s):
    check(w)
    if a not in ACTIONS or s not in SHOCKS:raise ValueError("not a frozen action/shock")
    return F(CONFIG[w][ACTIONS.index(a)][SHOCKS.index(s)])
def allowed(s,g):
    return s[0]+s[1]<=g
def source_atom(w,a,s,g):
    return dict(world=w,original_action=a,original_shock_bit_1=s[0],
       original_shock_bit_2=s[1],original_uncertainty_budget_Gamma=g,
       original_scenario_is_budget_eligible=int(allowed(s,g)),
       original_action_scenario_loss=original_cost(w,a,s),
       original_complete_action_scenario_budget_design_mass=F(1,60),
       oracle_independent_fair_two_shock_probability=F(1,4))
@lru_cache(None)
def sources(w):
    check(w)
    rows=tuple(source_atom(w,a,s,g) for a in ACTIONS for s in SHOCKS for g in BUDGETS)
    assert len(rows)==60 and sum((r["original_complete_action_scenario_budget_design_mass"] for r in rows),ZERO)==ONE
    return rows
def source_minimax(w,g):
    """First route: read all *original* source rows and filter budget explicitly."""
    if g not in BUDGETS:raise ValueError("bad uncertainty budget")
    rows=sources(w)
    worst={a:max(r["original_action_scenario_loss"] for r in rows
                 if r["original_action"]==a and r["original_uncertainty_budget_Gamma"]==g and r["original_scenario_is_budget_eligible"])
           for a in ACTIONS}
    regret={}
    for a in ACTIONS:
        eligible=[r for r in rows if r["original_action"]==a and
                  r["original_uncertainty_budget_Gamma"]==g and r["original_scenario_is_budget_eligible"]]
        margins=[]
        for r in eligible:
            min_scenario=min(z["original_action_scenario_loss"] for z in rows
                if z["original_shock_bit_1"]==r["original_shock_bit_1"] and
                z["original_shock_bit_2"]==r["original_shock_bit_2"] and
                z["original_uncertainty_budget_Gamma"]==g)
            margins.append(r["original_action_scenario_loss"]-min_scenario)
        regret[a]=max(margins)
    best_w=min(worst.values());best_r=min(regret.values())
    return (best_w,"".join(a for a in ACTIONS if worst[a]==best_w),
            best_r,"".join(a for a in ACTIONS if regret[a]==best_r),
            worst,regret)
def analytic_epigraph_certificates(w,g):
    """Independent source-free pair-bit mask minimax and epigraph witnesses."""
    check(w)
    scen=[j for j,s in enumerate(SHOCKS) if sum(s)<=g]
    if not scen:raise AssertionError("empty hard shock set")
    values=CONFIG[w]
    each_worst=[];each_regret=[]
    clairvoyant=[min(values[i][j] for i in range(5)) for j in range(4)]
    witness=[]
    for i in range(5):
        c=[F(values[i][j]) for j in scen]
        bound=max(c)
        assert all(v<=bound for v in c) and any(v==bound for v in c)
        r=[F(values[i][j]-clairvoyant[j]) for j in scen]
        rb=max(r)
        assert all(v<=rb for v in r) and any(v==rb for v in r)
        each_worst.append(bound);each_regret.append(rb)
        witness.append((SHOCKS[scen[c.index(bound)]],SHOCKS[scen[r.index(rb)]]))
    mw=min(each_worst);mr=min(each_regret)
    return (mw,"".join(ACTIONS[i] for i,c in enumerate(each_worst) if c==mw),
            mr,"".join(ACTIONS[i] for i,c in enumerate(each_regret) if c==mr),
            dict(zip(ACTIONS,each_worst)),dict(zip(ACTIONS,each_regret)),dict(zip(ACTIONS,witness)))
def fair_expected(w):
    rows=sources(w)
    by_action={a:sum((r["original_action_scenario_loss"]/4 for r in rows
                      if r["original_action"]==a and r["original_uncertainty_budget_Gamma"]==2),ZERO)
               for a in ACTIONS}
    best=min(by_action.values())
    return best,"".join(a for a in ACTIONS if by_action[a]==best),by_action
def locked_claims():
    for w in WORLDS:
        for g in BUDGETS:
            a=source_minimax(w,g);b=analytic_epigraph_certificates(w,g)
            expected=EXPECTED[w][g]
            if a[:4]!=b[:4] or a[:4]!=(F(expected[0]),expected[1],F(expected[2]),expected[3]):
                raise AssertionError(f"{w} Gamma{g} original vs analytic hard uncertainty mismatch {a[:4]} {b[:4]} {expected}")
        f=fair_expected(w)
        if (str(f[0]),f[1])!=EXPECTED_FAIR[w]:
            raise AssertionError(f"iid fair mean mismatch in {w}: {f[:2]}")
        for a in ACTIONS:
            worst=[source_minimax(w,g)[4][a] for g in BUDGETS]
            assert worst[0]<=worst[1]<=worst[2]
    for g in (0,1):
        for a in ACTIONS:
            for s in SHOCKS:
                if allowed(s,g):
                    assert original_cost("HIDDEN_JOINT_TAIL",a,s)==original_cost("HIDDEN_TAIL_ALIAS",a,s)
    assert source_minimax("HIDDEN_JOINT_TAIL",2)[1]=="C"
    assert source_minimax("HIDDEN_TAIL_ALIAS",2)[1]=="A"
    assert source_minimax("REGRET_VS_WORST",2)[1:4]==("C",F(2),"B")
    assert original_cost("NONMONOTONE_SHOCK_COST","A",(1,1))<original_cost("NONMONOTONE_SHOCK_COST","A",(0,0))
    return True
def world_result(w):
    by_budget={}
    for g in BUDGETS:
        sw,sws,sr,srs,ww,rr=source_minimax(w,g)
        proof=analytic_epigraph_certificates(w,g)
        if (sw,sws,sr,srs)!=(proof[0],proof[1],proof[2],proof[3]):
            raise AssertionError("independent epigraph mismatch")
        by_budget[str(g)]=dict(minimum_worst_case_loss=str(sw),
            all_minimax_cost_actions=list(sws),
            minimum_maximum_regret=str(sr),
            all_minimax_regret_actions=list(srs),
            all_action_worst_case_losses={a:str(ww[a]) for a in ACTIONS},
            all_action_worst_case_regrets={a:str(rr[a]) for a in ACTIONS},
            independent_scenario_epigraph_witnesses={
                a:{"worst_cost_scenario":"".join(map(str,proof[6][a][0])),
                   "worst_regret_scenario":"".join(map(str,proof[6][a][1]))} for a in ACTIONS},
            count_budget_eligible_shocks=sum(allowed(s,g) for s in SHOCKS),
            analytic_nonstatistical_uncertainty_set_verified=True)
    avg,wins,means=fair_expected(w)
    return dict(world=w,all_original_action_scenario_budget_source_atoms=60,
       frozen_cost_matrix_by_action={a:[str(original_cost(w,a,s)) for s in SHOCKS] for a in ACTIONS},
       exact_hard_uncertainty_budget_0_1_2=by_budget,
       fair_iid_two_bit_risk_neutral_best_expected_cost=str(avg),
       fair_iid_risk_neutral_all_optimal_actions=list(wins),
       fair_iid_all_action_expected_costs={a:str(means[a]) for a in ACTIONS},
       all_hard_budget_scenarios_preserved_in_original_source=True)
def emit():
    locked_claims()
    result=dict(research_id="R260",original_catalogue_id="11-020",
      prescore_freeze_commit=FREEZE,
      scientific_scope="FINITE_ARTIFICIAL_E1_HARD_TWO_SHOCK_BUDGET_ROBUST_MINIMAX_AND_REGRET",
      frozen_worlds=9,all_original_complete_source_atoms=540,
      source_structure="5 actions times 4 exogenous two-bit shock scenarios times 3 hard uncertainty budgets",
      scenario_design_mass_is_not_statistical_probability=True,
      fair_iid_shock_probability_separately_frozen="1/4 each scenario",
      full_minimax_cost_vs_minimax_regret_independent_certificates=True,
      observed_U_Gamma_le_one_sourcewise_alias_hidden_tail_breaks_Gamma_two=True,
      no_real_extreme_events_or_policy_preferences_identified=True,
      new_real_human_E2=0,new_real_historical_E3=0,
      R073="FROZEN",PESEN_v0_1="FROZEN",
      world_results=[world_result(w) for w in WORLDS])
    out=HERE/"R260_ALL_540_ORIGINAL_SCENARIO_BUDGET_SOURCE_ATOMS.csv"
    cols=list(sources(WORLDS[0])[0])
    with out.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=cols,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for r in sources(w):wr.writerow({k:str(r[k]) for k in cols})
    jp=HERE/"R260_EXACT_RESULTS.json"
    jp.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R260",original_catalogue_id="11-020",frozen_worlds=9,
      all_original_action_shock_budget_atoms=540,
      minmax_epigraph_and_max_regret_witnesses_independently_verified=True,
      Gamma_hard_nested_uncertainty_verified=True,
      sourcewise_U_one_hidden_tail_alias_and_U_two_reversal_verified=True,
      source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
      results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
      new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R260_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt
class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_sources(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),540)
    def test_complete_frozen(self):self.assertTrue(locked_claims())
    def test_shock_alias(self):self.assertEqual(source_minimax("HIDDEN_TAIL_ALIAS",1)[:4],source_minimax("HIDDEN_JOINT_TAIL",1)[:4])
    def test_worst_regret_difference(self):self.assertEqual(source_minimax("REGRET_VS_WORST",2)[:4],(F(4),"C",F(2),"B"))
    def test_explicit_fair_average(self):self.assertEqual(fair_expected("HIDDEN_JOINT_TAIL")[:2],(F(3),"ABC"))
    def test_U0(self):self.assertEqual(source_minimax("TIED_WORST_CASE",0)[:4],(ZERO,"A",ZERO,"A"))
    def test_budget_eligibility(self):self.assertEqual(sum(allowed(s,1) for s in SHOCKS),3)
    def test_bad(self):
        with self.assertRaises(ValueError):sources("NOT_FROZEN")
def _case(w,k):
    def t(self):
        rows=sources(w)
        if k=="mass":self.assertEqual(sum((r["original_complete_action_scenario_budget_design_mass"] for r in rows),ZERO),ONE)
        elif k=="unique":
            key=lambda r:(r["original_action"],r["original_shock_bit_1"],r["original_shock_bit_2"],r["original_uncertainty_budget_Gamma"])
            self.assertEqual(len({key(r) for r in rows}),60)
        elif k=="positive":self.assertTrue(all(r["original_complete_action_scenario_budget_design_mass"]==F(1,60) for r in rows))
        elif k=="eligible":
            self.assertTrue(all(r["original_scenario_is_budget_eligible"]==int(r["original_shock_bit_1"]+r["original_shock_bit_2"]<=r["original_uncertainty_budget_Gamma"]) for r in rows))
        elif k=="exact_cost":
            self.assertTrue(all(r["original_action_scenario_loss"]==original_cost(w,r["original_action"],(r["original_shock_bit_1"],r["original_shock_bit_2"])) for r in rows))
        elif k=="independent":
            for g in BUDGETS:self.assertEqual(source_minimax(w,g)[:4],analytic_epigraph_certificates(w,g)[:4])
        elif k=="monotone":
            for a in ACTIONS:
                vals=[source_minimax(w,g)[4][a] for g in BUDGETS]
                self.assertEqual(vals,sorted(vals))
        elif k=="report":self.assertEqual(world_result(w)["all_original_action_scenario_budget_source_atoms"],60)
        else:raise AssertionError("unfrozen test")
    return t
for w in WORLDS:
    for k in ("mass","unique","positive","eligible","exact_cost","independent","monotone","report"):
        setattr(Tests,"test_"+w.lower()+"_"+k,_case(w,k))
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r260"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
