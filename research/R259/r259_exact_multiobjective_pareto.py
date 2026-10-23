#!/usr/bin/env python3
"""R259 finite two-objective Pareto/weighted-sum support with exact rational intervals.

Nine independent artificial five-decision objective worlds. Every decision
at every frozen weight belongs to the complete source space: 9*5*5=225.
Continuous supported intervals are derived independently by intersection of
pairwise affine-weight inequalities, never inferred from 5-point weight grid.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="e40857bc7fe4ea2040791042cbe24f3e902c9ba2"
ZERO=F(0);ONE=F(1)
DECISIONS=("A","B","C","D","E")
WEIGHTS=(ZERO,F(1,4),F(1,2),F(3,4),ONE)
BASE=((0,4),(1,3),(2,2),(3,1),(4,0))
CONFIG={
 "LINEAR_FIVE_ALL_SUPPORTED":BASE,
 "CONCAVE_THREE_UNSUPPORTED":((0,4),(1,F(7,2)),(2,3),(3,2),(4,0)),
 "DOMINATED_EXTRAS":((0,4),(1,5),(2,2),(5,1),(4,0)),
 "OBJECTIVE1_MULTIPLY10":((0,4),(10,3),(20,2),(30,1),(40,0)),
 "DUPLICATE_TIE":((0,4),(0,4),(2,2),(4,0),(5,5)),
 "STRICTLY_CONVEX_DISCRETE_FRONT":((0,4),(1,F(9,4)),(2,1),(3,F(1,4)),(4,0)),
 "OBJECTIVE2_MULTIPLY10":((0,40),(1,30),(2,20),(3,10),(4,0)),
 "REVERSE_LABELS":((4,0),(3,1),(2,2),(1,3),(0,4)),
 "LINEAR_COST2_STEEPER":((0,8),(1,6),(2,4),(3,2),(4,0))}
CONFIG={w:tuple((F(a),F(b)) for a,b in costs) for w,costs in CONFIG.items()}
WORLDS=tuple(CONFIG)
def check(w):
    if w not in CONFIG:raise ValueError("unfrozen biobjective world")
def cost(w,decision):
    check(w)
    if decision not in DECISIONS:raise ValueError("not frozen decision")
    return CONFIG[w][DECISIONS.index(decision)]
def weighted_cost(w,decision,lmb):
    if lmb not in WEIGHTS:raise ValueError("not frozen original weight source")
    f1,f2=cost(w,decision)
    return lmb*f1+(ONE-lmb)*f2
def direct_dominates(w,other,chosen):
    a,b=cost(w,other)
    c,d=cost(w,chosen)
    return a<=c and b<=d and (a<c or b<d)
def pareto_labels(w):
    check(w)
    return tuple(d for d in DECISIONS if not any(direct_dominates(w,z,d) for z in DECISIONS if z!=d))
def direct_finite_grid_winners(w,lmb):
    scores={d:weighted_cost(w,d,lmb) for d in DECISIONS}
    best=min(scores.values())
    return tuple(d for d in DECISIONS if scores[d]==best)
def selected_by_some_frozen_grid_weight(w):
    return tuple(d for d in DECISIONS if any(d in direct_finite_grid_winners(w,lmb) for lmb in WEIGHTS))
def continuous_supported_interval(w,chosen):
    """Second independent symbolic route: all 4 pairwise linear halfspace cuts."""
    check(w)
    a,b=cost(w,chosen)
    lo=ZERO;hi=ONE
    for competitor in DECISIONS:
        if competitor==chosen:continue
        c,d=cost(w,competitor)
        # ((a-c)-(b-d))*lambda + (b-d) <= 0
        slope=(a-c)-(b-d)
        intercept=b-d
        if slope==ZERO:
            if intercept>ZERO:return None
        elif slope>ZERO:
            hi=min(hi,-intercept/slope)
        else:
            lo=max(lo,-intercept/slope)
        if lo>hi:return None
    if lo<ZERO or hi>ONE:raise AssertionError("support range outside normalized weights")
    witness=(lo+hi)/2
    def score(z):
        c,d=cost(w,z)
        return witness*c+(ONE-witness)*d
    if any(score(chosen)>score(z) for z in DECISIONS):
        raise AssertionError("analytic supporting interval has invalid rational witness")
    return lo,hi
def supported_labels(w):
    return tuple(d for d in DECISIONS if continuous_supported_interval(w,d) is not None)
def eps_constraint(w,epsilon):
    check(w)
    admissible=[d for d in DECISIONS if cost(w,d)[0]<=epsilon]
    best=min(cost(w,d)[1] for d in admissible)
    return tuple(d for d in admissible if cost(w,d)[1]==best)
def source_atom(w,d,lmb):
    f1,f2=cost(w,d)
    interval=continuous_supported_interval(w,d)
    return dict(world=w,original_decision_label=d,
        original_scalar_weight_lambda=lmb,
        original_objective_f1=f1,
        original_objective_f2=f2,
        original_weighted_objective_score=weighted_cost(w,d,lmb),
        original_decision_is_Pareto=int(d in pareto_labels(w)),
        original_decision_supported_any_continuous_weight=int(interval is not None),
        original_decision_wins_this_weight=int(d in direct_finite_grid_winners(w,lmb)),
        original_uniform_decision_weight_design_mass=F(1,25))
@lru_cache(None)
def sources(w):
    check(w)
    src=tuple(source_atom(w,d,l) for d in DECISIONS for l in WEIGHTS)
    assert len(src)==25 and sum((r["original_uniform_decision_weight_design_mass"] for r in src),ZERO)==ONE
    return src
def locked_claims():
    assert pareto_labels("LINEAR_FIVE_ALL_SUPPORTED")==DECISIONS
    assert supported_labels("LINEAR_FIVE_ALL_SUPPORTED")==DECISIONS
    assert direct_finite_grid_winners("LINEAR_FIVE_ALL_SUPPORTED",F(1,2))==DECISIONS
    w="CONCAVE_THREE_UNSUPPORTED"
    assert pareto_labels(w)==DECISIONS
    assert supported_labels(w)==("A","E")
    assert all(continuous_supported_interval(w,d) is None for d in ("B","C","D"))
    assert eps_constraint(w,F(2))==("C",)
    assert pareto_labels("DOMINATED_EXTRAS")==("A","C","E")
    assert supported_labels("DOMINATED_EXTRAS")==("A","C","E")
    assert pareto_labels("DUPLICATE_TIE")==("A","B","C","D")
    assert supported_labels("DUPLICATE_TIE")==("A","B","C","D")
    assert pareto_labels("OBJECTIVE1_MULTIPLY10")==DECISIONS
    assert continuous_supported_interval("OBJECTIVE1_MULTIPLY10","B")==(F(1,11),F(1,11))
    assert continuous_supported_interval("OBJECTIVE2_MULTIPLY10","B")==(F(10,11),F(10,11))
    assert continuous_supported_interval("LINEAR_COST2_STEEPER","C")==(F(2,3),F(2,3))
    w="STRICTLY_CONVEX_DISCRETE_FRONT"
    assert supported_labels(w)==DECISIONS
    assert continuous_supported_interval(w,"B")== (F(5,9),F(7,11))
    assert "B" not in selected_by_some_frozen_grid_weight(w)
    assert direct_finite_grid_winners(w,F(1,4))==("D",)
    assert direct_finite_grid_winners(w,F(1,2))==("C",)
    assert direct_finite_grid_winners(w,F(3,4))==("A",)
    assert pareto_labels("OBJECTIVE1_MULTIPLY10")==pareto_labels("LINEAR_FIVE_ALL_SUPPORTED")
    assert pareto_labels("OBJECTIVE2_MULTIPLY10")==pareto_labels("LINEAR_FIVE_ALL_SUPPORTED")
    assert direct_finite_grid_winners("LINEAR_FIVE_ALL_SUPPORTED",F(1,4))==("E",)
    assert direct_finite_grid_winners("OBJECTIVE1_MULTIPLY10",F(1,4))==("A",)
    assert sorted(CONFIG["REVERSE_LABELS"])==sorted(CONFIG["LINEAR_FIVE_ALL_SUPPORTED"])
    for world in WORLDS:
        for d in selected_by_some_frozen_grid_weight(world):
            if d not in pareto_labels(world):
                raise AssertionError("frozen finite-grid winner is dominated (strict positive weights caveat)")
    return True
def world_result(w):
    pareto=pareto_labels(w)
    supported=supported_labels(w)
    grid=selected_by_some_frozen_grid_weight(w)
    return dict(world=w,original_complete_decision_weight_source_atoms=25,
       all_decision_objective_pairs={d:[str(v) for v in cost(w,d)] for d in DECISIONS},
       Pareto_decision_labels=list(pareto),
       supported_by_some_continuous_normalized_weight=list(supported),
       Pareto_unsupported_by_any_continuous_weight=[d for d in pareto if d not in supported],
       all_continuous_weight_support_closed_intervals={
          d:([str(z) for z in v] if (v:=continuous_supported_interval(w,d)) is not None else None)
          for d in DECISIONS},
       selected_by_frozen_five_weight_grid=list(grid),
       supported_but_missed_by_frozen_weight_grid=[d for d in supported if d not in grid],
       complete_weight_grid_scalar_winner_ties={
          str(l):list(direct_finite_grid_winners(w,l)) for l in WEIGHTS},
       exact_epsilon_f1_le_2_f2_minimizers=list(eps_constraint(w,F(2))),
       full_Pareto_dominance_and_continuous_support_interval_certificate=True)
def emit():
    locked_claims()
    dat=dict(research_id="R259",original_catalogue_id="11-019",
      prescore_freeze_commit=FREEZE,
      scientific_scope="FINITE_ARTIFICIAL_E1_FIVE_DECISION_MULTI_OBJECTIVE_PARETO_VS_SUPPORTED_SOLUTION_IDENTIFICATION",
      frozen_worlds=9,complete_original_decision_weight_atoms=225,
      continuous_supported_weights_not_inferred_from_five_weight_grid=True,
      nonconvex_frontier_Pareto_but_unsupported_decisions=["B","C","D"],
      epsilon_f1_at_most_2_recovers_unsupported_C=True,
      strictly_convex_finite_front_support_B_interval=["5/9","7/11"],
      lambda_quarter_linear_world_winner=["E"],
      lambda_quarter_objective1_scaled_world_winner=["A"],
      no_human_preferences_or_institutional_welfare_estimated=True,
      new_real_human_E2=0,new_real_historical_E3=0,
      R073="FROZEN",PESEN_v0_1="FROZEN",
      world_results=[world_result(w) for w in WORLDS])
    out=HERE/"R259_ALL_225_ORIGINAL_DECISION_WEIGHT_SOURCE_ATOMS.csv"
    keys=list(sources(WORLDS[0])[0])
    with out.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for r in sources(w):wr.writerow({k:str(r[k]) for k in keys})
    jp=HERE/"R259_EXACT_RESULTS.json"
    jp.write_text(json.dumps(dat,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    rec=dict(research_id="R259",original_catalogue_id="11-019",
       frozen_worlds=9,all_complete_decision_weight_original_atoms=225,
       Pareto_vs_continuous_supported_certificates=True,
       epsilon_method_recovers_finite_unsupported_Pareto=True,
       exact_weight_grid_misses_continuously_supported_witness=True,
       source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R259_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
    return rec
class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_all_225(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),225)
    def test_frozen_support_claims(self):self.assertTrue(locked_claims())
    def test_pareto_vs_supported(self):
        self.assertEqual(pareto_labels("CONCAVE_THREE_UNSUPPORTED"),DECISIONS)
        self.assertEqual(supported_labels("CONCAVE_THREE_UNSUPPORTED"),("A","E"))
    def test_epsilon(self):self.assertEqual(eps_constraint("CONCAVE_THREE_UNSUPPORTED",F(2)),("C",))
    def test_grid_misses_supported(self):
        self.assertEqual(continuous_supported_interval("STRICTLY_CONVEX_DISCRETE_FRONT","B"),(F(5,9),F(7,11)))
    def test_positive_scale(self):
        self.assertEqual(direct_finite_grid_winners("OBJECTIVE1_MULTIPLY10",F(1,4)),("A",))
    def test_same_objectives_independent_labels(self):
        self.assertEqual(sorted(CONFIG["REVERSE_LABELS"]),sorted(CONFIG["LINEAR_FIVE_ALL_SUPPORTED"]))
    def test_duplicate_pareto(self):self.assertEqual(pareto_labels("DUPLICATE_TIE"),("A","B","C","D"))
    def test_not_frozen(self):
        with self.assertRaises(ValueError):sources("NO_WORLD")
def _case(w,k):
    def t(self):
        s=sources(w)
        if k=="mass":self.assertEqual(sum((r["original_uniform_decision_weight_design_mass"] for r in s),ZERO),ONE)
        elif k=="unique":self.assertEqual(len({(r["original_decision_label"],r["original_scalar_weight_lambda"]) for r in s}),25)
        elif k=="positive":self.assertTrue(all(r["original_uniform_decision_weight_design_mass"]==F(1,25) for r in s))
        elif k=="score":
            for r in s:self.assertEqual(r["original_weighted_objective_score"],weighted_cost(w,r["original_decision_label"],r["original_scalar_weight_lambda"]))
        elif k=="Pareto":
            for r in s:self.assertEqual(r["original_decision_is_Pareto"],int(r["original_decision_label"] in pareto_labels(w)))
        elif k=="interval":
            for d in DECISIONS:
                I=continuous_supported_interval(w,d)
                self.assertEqual(d in supported_labels(w),I is not None)
        elif k=="winners":
            for l in WEIGHTS:
                for r in s:
                    if r["original_scalar_weight_lambda"]==l:
                        self.assertEqual(r["original_decision_wins_this_weight"],int(r["original_decision_label"] in direct_finite_grid_winners(w,l)))
        elif k=="report":self.assertEqual(world_result(w)["original_complete_decision_weight_source_atoms"],25)
        else:raise AssertionError("unknown frozen test")
    return t
for w in WORLDS:
    for k in ("mass","unique","positive","score","Pareto","interval","winners","report"):
        setattr(Tests,"test_"+w.lower()+"_"+k,_case(w,k))
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r259"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
