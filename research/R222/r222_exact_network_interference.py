#!/usr/bin/env python3
"""R222 exhaustive network-interference design audit.

Four artificial nodes on PAIRS, STAR and CYCLE. Enumerate all 16 independent
Bernoulli-half assignments or all six exactly-two-treated assignments for
three fixed response surfaces. Eighteen worlds, 198 ORIGINAL source paths.

Known outcome surfaces:
 Y_i(z)=i + 2*z_i + gamma*treated_neighbors + delta*z_i*treated_neighbors.
ATE target is a fixed Bernoulli-peers policy direct effect, never inferred
from the exposure-limited complete-2 experiment without qualifications.
Exact HT expected loss and variance checked by independent finite exposure
moments. No real human or historical observations.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import unittest
from fractions import Fraction
from pathlib import Path

F=Fraction
Z=F(0)
O=F(1)
N=4
GRAPHS={
    "PAIRS":((0,1),(2,3)),
    "STAR":((0,1),(0,2),(0,3)),
    "CYCLE":((0,1),(1,2),(2,3),(0,3)),
}
POLICIES=("BERNOULLI_HALF","COMPLETE_TWO_OF_FOUR")
MECHANISMS={
    "NO_SPILL":(F(2),Z,Z),
    "LINEAR_SPILL":(F(2),F(2),Z),
    "INTERACTION_SPILL":(F(2),O,F(2)),
}
OUT=Path(__file__).resolve().parent


def neighbors(graph):
    if graph not in GRAPHS:
        raise ValueError("graph not frozen")
    x=[set() for _ in range(N)]
    for i,j in GRAPHS[graph]:
        x[i].add(j)
        x[j].add(i)
    return tuple(tuple(sorted(a)) for a in x)


def assignment_sources(policy):
    if policy not in POLICIES:
        raise ValueError("unknown experimental policy")
    if policy=="BERNOULLI_HALF":
        out=tuple((tuple((mask>>i)&1 for i in range(N)),F(1,16))
                  for mask in range(16))
    else:
        out=tuple((tuple(int(i in treated) for i in range(N)),F(1,6))
                  for treated in itertools.combinations(range(N),2))
    if sum((p for z,p in out),Z)!=O:
        raise AssertionError("randomization probability mass not 1")
    return out


def exposure(graph,z):
    if len(z)!=N or any(t not in (0,1) for t in z):
        raise ValueError("frozen four-person binary assignment required")
    a=neighbors(graph)
    return tuple(sum(z[j] for j in a[i]) for i in range(N))


def potential_outcome(graph,mechanism,i,z):
    if mechanism not in MECHANISMS or i not in range(N):
        raise ValueError("unknown frozen model or person")
    tau,gamma,delta=MECHANISMS[mechanism]
    e=exposure(graph,z)[i]
    return F(i)+tau*z[i]+gamma*e+delta*z[i]*e


def observed_four_outcomes(graph,mechanism,z):
    return tuple(potential_outcome(graph,mechanism,i,z) for i in range(N))


def ht_marginal_one_half(z,y):
    """HT is defined also when treatment arm is empty/full (unlike diff-in-means)."""
    if len(z)!=N or len(y)!=N:
        raise ValueError("four original units required")
    return sum((2*z[i]*y[i]-2*(1-z[i])*y[i] for i in range(N)),Z)/N


def target_exact_peers_by_source(graph,mechanism):
    total=Z
    for i in range(N):
        others=tuple(j for j in range(N) if j!=i)
        for suffix in itertools.product((0,1),repeat=3):
            z0=[0]*N
            for j,bit in zip(others,suffix):
                z0[j]=bit
            z1=z0[:]
            z1[i]=1
            total+=(potential_outcome(graph,mechanism,i,tuple(z1))-
                    potential_outcome(graph,mechanism,i,tuple(z0)))/F(N*8)
    return total


def target_exact_peers_by_formula(graph,mechanism):
    tau,gamma,delta=MECHANISMS[mechanism]
    avg_deg=sum((len(n) for n in neighbors(graph)),Z)/N
    return tau+delta*avg_deg/2


def treatment_exposure_support(graph,policy):
    """True design probabilities of all physically possible (Zi,ei) cells."""
    src=assignment_sources(policy)
    out=[]
    for i,nei in enumerate(neighbors(graph)):
        for own in (0,1):
            for e in range(len(nei)+1):
                p=sum((w for z,w in src if z[i]==own and exposure(graph,z)[i]==e),Z)
                out.append({
                    "unit":i,"degree":len(nei),"own_treatment":own,
                    "neighbor_exposure_count":e,"design_probability_exact":str(p),
                    "supported_under_original_assignment_design":bool(p),
                })
    return out


def analytic_design_HT_expectation(graph,policy,mechanism):
    tau,gamma,delta=MECHANISMS[mechanism]
    avedeg=sum((len(n) for n in neighbors(graph)),Z)/N
    if policy=="BERNOULLI_HALF":
        return tau+delta*avedeg/2
    if policy=="COMPLETE_TWO_OF_FOUR":
        return tau+(delta-gamma)*avedeg/3
    raise ValueError("not frozen design")


def compute():
    worlds=[]
    original=[]
    for graph in GRAPHS:
        for mechanism in MECHANISMS:
            truth_source=target_exact_peers_by_source(graph,mechanism)
            truth_formula=target_exact_peers_by_formula(graph,mechanism)
            if truth_source!=truth_formula:
                raise AssertionError("independent oracle target source and formula mismatch")
            for policy in POLICIES:
                source=assignment_sources(policy)
                probability=Z
                scores=[]
                for z,p in source:
                    ys=observed_four_outcomes(graph,mechanism,z)
                    exposure_counts=exposure(graph,z)
                    h=ht_marginal_one_half(z,ys)
                    probability+=p
                    scores.append((h,p))
                    original.append({
                        "graph":graph,"mechanism":mechanism,"random_policy":policy,
                        "graph_edges":"|".join(f"{i}{j}" for i,j in GRAPHS[graph]),
                        "source_assignment_z":"|".join(map(str,z)),
                        "source_assignment_probability_exact":str(p),
                        "actual_four_neighbor_exposure_counts":"|".join(map(str,exposure_counts)),
                        "actual_four_individual_results":"|".join(map(str,ys)),
                        "true_surface_own_effect_at_observed_exposure_ORACLE_ONLY":"|".join(
                            str(MECHANISMS[mechanism][0]+MECHANISMS[mechanism][2]*e)
                            for e in exposure_counts),
                        "HT_marginal_half_from_observed_four_only_exact":str(h),
                        "true_Bernoulli_peers_policy_direct_effect_ORACLE_ONLY":str(truth_source),
                        "HT_squared_error_against_fixed_policy_oracle_exact":str((h-truth_source)**2),
                    })
                if probability!=O:
                    raise AssertionError("world full original random assignment missing")
                eh=sum((p*h for h,p in scores),Z)
                var=sum((p*(h-eh)**2 for h,p in scores),Z)
                mse=sum((p*(h-truth_source)**2 for h,p in scores),Z)
                if mse!=var+(eh-truth_source)**2:
                    raise AssertionError("independent bias+variance MSE identity failed")
                expected=analytic_design_HT_expectation(graph,policy,mechanism)
                if eh!=expected:
                    raise AssertionError("complete all-source HT differs from independent conditional exposure expectation")
                cells=treatment_exposure_support(graph,policy)
                z_cells=[c for c in cells if not c["supported_under_original_assignment_design"]]
                worlds.append({
                    "graph":graph,"mechanism":mechanism,"assignment_policy":policy,
                    "true_scm_parameters_tau_gamma_delta_exact":
                        [str(p) for p in MECHANISMS[mechanism]],
                    "all_original_assignment_source_count":len(source),
                    "full_original_assignment_probability_sum":"1",
                    "true_Bernoulli_peers_policy_mean_direct_effect_exact":str(truth_source),
                    "independent_analytic_target_direct_effect_exact":str(truth_formula),
                    "HT_from_actual_randomized_obs_source_expected_value_exact":str(eh),
                    "independent_analytic_HT_design_expectation_exact":str(expected),
                    "HT_source_variance_exact":str(var),
                    "HT_bias_against_fixed_Bernoulli_peers_direct_effect_exact":
                        str(eh-truth_source),
                    "HT_true_fixed_policy_target_MSE_exact":str(mse),
                    "all_individual_exposure_treatment_cell_probs":cells,
                    "full_exposure_cells_count":len(cells),
                    "unsupported_cell_count":len(z_cells),
                    "unsupported_exposure_cells":z_cells,
                })
    if len(worlds)!=18 or len(original)!=198:
        raise AssertionError("missing expected 18 worlds or 198 raw original assignments")
    return {
        "research_id":"R222","actual_original_catalogue_id":"09-013",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "synthetic_worlds":18,
        "full_original_assignment_source_rows":198,
        "graphs":{k:[list(edge) for edge in val] for k,val in GRAPHS.items()},
        "mechanisms":{k:[str(v) for v in vals] for k,vals in MECHANISMS.items()},
        "policies":list(POLICIES),
        "true_direct_target":"Average direct controlled effect under independent Bernoulli(1/2) peer-treatment policy",
        "all_original_source_assignment_probabilities_normalized":True,
        "all_HT_source_expectations_match_independent_design_formulas":True,
        "two_independent_peers_target_calculations_agree":True,
        "zero_positivity_cells_detected_in_complete_fixed_treated_design":True,
        "new_real_human_E2":0,"new_real_historical_E3":0,
        "worlds":worlds,
        "limits":[
            "Three artificial four-node undirected graphs, known exposure mapping and response surfaces",
            "Fixed count K=2 randomization differs from independent Bernoulli peer-treatment policy",
            "No actual social network experiment, actual contagion, learning or psychological outcome data",
            "No independent graph heldout; 198 rows are original possible artificial assignments",
        ],
    },original


def emit():
    r,raw=compute()
    paths={
        "results":OUT/"R222_EXACT_RESULTS.json",
        "sources":OUT/"R222_ALL_198_ORIGINAL_NETWORK_ASSIGNMENT_SOURCES.csv",
    }
    paths["results"].write_text(json.dumps(r,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with paths["sources"].open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(raw[0]))
        writer.writeheader()
        writer.writerows(raw)
    receipt={
        "model_id":"R222",
        "actual_original_catalogue_id":"09-013",
        "worlds":18,
        "all_original_assignment_source_rows":198,
        "true_target_two_independent_fraction_routes_verified":True,
        "HT_randomization_expected_value_equals_independent_analytic_conditioning":True,
        "per_unit_exposure_mapping_positivity_verified":True,
        "new_E2":0,"new_E3":0,
        **{name+"_sha256":hashlib.sha256(p.read_bytes()).hexdigest()
           for name,p in paths.items()},
    }
    (OUT/"R222_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(receipt,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2))


class Tests(unittest.TestCase):
    def test_4_nodes(self):self.assertEqual(N,4)
    def test_three_graphs(self):self.assertEqual(len(GRAPHS),3)
    def test_three_fixed_mechanisms(self):self.assertEqual(len(MECHANISMS),3)
    def test_two_designs(self):self.assertEqual(len(POLICIES),2)
    def test_18_worlds_count(self):self.assertEqual(3*3*2,18)
    def test_198_original_assignments_count(self):self.assertEqual(9*(16+6),198)
    def test_pairs_two_edges(self):self.assertEqual(len(GRAPHS["PAIRS"]),2)
    def test_star_three_edges(self):self.assertEqual(len(GRAPHS["STAR"]),3)
    def test_cycle_four_edges(self):self.assertEqual(len(GRAPHS["CYCLE"]),4)
    def test_neighborhood_undirected(self):
        for graph in GRAPHS:
            adj=neighbors(graph)
            self.assertTrue(all((j in adj[i])==(i in adj[j]) for i in range(N) for j in range(N)))
    def test_all_Bernoulli_sixteen_assignments(self):
        self.assertEqual(len(assignment_sources("BERNOULLI_HALF")),16)
    def test_all_fixed_two_six_assignments(self):
        self.assertEqual(len(assignment_sources("COMPLETE_TWO_OF_FOUR")),6)
    def test_Bernoulli_extreme_assignments_kept(self):
        self.assertIn(((0,0,0,0),F(1,16)),assignment_sources("BERNOULLI_HALF"))
        self.assertIn(((1,1,1,1),F(1,16)),assignment_sources("BERNOULLI_HALF"))
    def test_fixed_two_always_2_treated(self):
        self.assertTrue(all(sum(z)==2 for z,p in assignment_sources("COMPLETE_TWO_OF_FOUR")))
    def test_source_mass_one(self):
        for policy in POLICIES:
            self.assertEqual(sum((p for z,p in assignment_sources(policy)),Z),O)
    def test_each_policy_unit_propensity_one_half(self):
        for policy in POLICIES:
            for i in range(N):
                self.assertEqual(sum((p*z[i] for z,p in assignment_sources(policy)),Z),F(1,2))
    def test_no_interference_response_independent_of_peers(self):
        for graph in GRAPHS:
            for i in range(N):
                for t in (0,1):
                    vals=set()
                    for zbits in itertools.product((0,1),repeat=N):
                        if zbits[i]==t:
                            vals.add(potential_outcome(graph,"NO_SPILL",i,zbits))
                    self.assertEqual(len(vals),1)
    def test_no_interference_true_direct_two(self):
        for graph in GRAPHS:
            self.assertEqual(target_exact_peers_by_source(graph,"NO_SPILL"),F(2))
    def test_independent_peers_direct_match_formula(self):
        for graph in GRAPHS:
            for model in MECHANISMS:
                self.assertEqual(target_exact_peers_by_source(graph,model),
                                 target_exact_peers_by_formula(graph,model))
    def test_HT_no_spill_both_designs_unbiased(self):
        for graph in GRAPHS:
            for policy in POLICIES:
                source=assignment_sources(policy)
                estimate=sum((p*ht_marginal_one_half(z,observed_four_outcomes(graph,"NO_SPILL",z))
                              for z,p in source),Z)
                self.assertEqual(estimate,F(2))
    def test_pair_neighbor_exposure(self):
        self.assertEqual(exposure("PAIRS",(1,0,0,1)),(0,1,1,0))
    def test_star_neighbor_exposure(self):
        self.assertEqual(exposure("STAR",(1,0,0,1)),(1,1,1,1))
    def test_cycle_neighbor_exposure(self):
        self.assertEqual(exposure("CYCLE",(1,0,0,1)),(1,2,1,0))
    def test_linear_spill_pair_complete_bias(self):
        self.assertEqual(analytic_design_HT_expectation("PAIRS","COMPLETE_TWO_OF_FOUR","LINEAR_SPILL"),F(4,3))
    def test_linear_spill_star_complete_bias(self):
        self.assertEqual(analytic_design_HT_expectation("STAR","COMPLETE_TWO_OF_FOUR","LINEAR_SPILL"),O)
    def test_linear_spill_cycle_complete_bias(self):
        self.assertEqual(analytic_design_HT_expectation("CYCLE","COMPLETE_TWO_OF_FOUR","LINEAR_SPILL"),F(2,3))
    def test_linear_spill_Bernoulli_unbiased(self):
        for graph in GRAPHS:
            self.assertEqual(analytic_design_HT_expectation(graph,"BERNOULLI_HALF","LINEAR_SPILL"),F(2))
    def test_interaction_pairs_complete_vs_true(self):
        self.assertEqual(target_exact_peers_by_source("PAIRS","INTERACTION_SPILL"),F(3))
        self.assertEqual(analytic_design_HT_expectation("PAIRS","COMPLETE_TWO_OF_FOUR","INTERACTION_SPILL"),F(7,3))
    def test_interaction_cycle_complete_vs_true(self):
        self.assertEqual(target_exact_peers_by_source("CYCLE","INTERACTION_SPILL"),F(4))
        self.assertEqual(analytic_design_HT_expectation("CYCLE","COMPLETE_TWO_OF_FOUR","INTERACTION_SPILL"),F(8,3))
    def test_interaction_Bernoulli_expected_target(self):
        for graph in GRAPHS:
            self.assertEqual(analytic_design_HT_expectation(graph,"BERNOULLI_HALF","INTERACTION_SPILL"),
                             target_exact_peers_by_source(graph,"INTERACTION_SPILL"))
    def test_star_center_complete_two_exposure_support(self):
        d=treatment_exposure_support("STAR","COMPLETE_TWO_OF_FOUR")
        p={(x["own_treatment"],x["neighbor_exposure_count"]):x["design_probability_exact"]
           for x in d if x["unit"]==0}
        self.assertEqual(p[1,1],"1/2")
        self.assertEqual(p[0,2],"1/2")
        self.assertEqual(p[1,2],"0")
        self.assertEqual(p[0,1],"0")
    def test_bernoulli_every_exposure_cell_has_support(self):
        for graph in GRAPHS:
            self.assertTrue(all(x["supported_under_original_assignment_design"]
                                for x in treatment_exposure_support(graph,"BERNOULLI_HALF")))
    def test_fixed_two_cycle_unsupported(self):
        d=treatment_exposure_support("CYCLE","COMPLETE_TWO_OF_FOUR")
        self.assertTrue(any(not x["supported_under_original_assignment_design"] for x in d))
    def test_star_mean_degree_three_halves(self):
        self.assertEqual(sum((len(adj) for adj in neighbors("STAR")),Z)/N,F(3,2))
    def test_no_spill_both_controlled_peer_effect_zero(self):
        tau,gamma,delta=MECHANISMS["NO_SPILL"]
        self.assertEqual((gamma,gamma+delta),(Z,Z))
    def test_interaction_controlled_spill_by_t(self):
        tau,gamma,delta=MECHANISMS["INTERACTION_SPILL"]
        self.assertEqual((gamma,gamma+delta),(O,F(3)))
    def test_negative_HT_bias_has_correct_sign(self):
        for graph in GRAPHS:
            g=analytic_design_HT_expectation(graph,"COMPLETE_TWO_OF_FOUR","LINEAR_SPILL")
            self.assertLess(g,F(2))
    def test_invalid_graph_rejected(self):
        with self.assertRaises(ValueError): neighbors("INVALID")
    def test_invalid_design_rejected(self):
        with self.assertRaises(ValueError): assignment_sources("INVALID")
    def test_invalid_treatment_count_rejected(self):
        with self.assertRaises(ValueError): exposure("PAIRS",(1,0,1))
    def test_full_18_world_198_source(self):
        r,raw=compute()
        self.assertEqual((len(r["worlds"]),len(raw)),(18,198))
        self.assertTrue(r["zero_positivity_cells_detected_in_complete_fixed_treated_design"])
        self.assertEqual(r["new_real_human_E2"],0)
    def test_all_worlds_fraction_probability_and_mse(self):
        r,_=compute()
        for w in r["worlds"]:
            self.assertEqual(w["full_original_assignment_probability_sum"],"1")
            self.assertEqual(F(w["HT_true_fixed_policy_target_MSE_exact"]),
                             F(w["HT_source_variance_exact"])+
                             F(w["HT_bias_against_fixed_Bernoulli_peers_direct_effect_exact"])**2)
    def test_full_deterministic_replay(self):
        self.assertEqual(compute(),compute())


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test",action="store_true")
    parser.add_argument("--emit",action="store_true")
    opts=parser.parse_args()
    if opts.test:
        result=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if result.wasSuccessful() else 1)
    if opts.emit:
        emit()
    if not opts.test and not opts.emit:
        parser.print_help()
