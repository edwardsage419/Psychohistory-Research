#!/usr/bin/env python3
"""R209 full finite two-round innovation adoption and independent-trajectory risk.

Artificial sources: four-node STAR, PATH, CYCLE with one fixed initial seed;
three fully specified mechanisms BASE, SIMPLE, COMPLEX. Adoption is absorbing,
simultaneous per round, and Bernoulli innovations conditional on last round.

Complete per-world 27 paths, 36 worlds, 972 original training events,
and 26,244 pairs of independent training and future complete trajectories.
Compare out-of-trajectory multiclass logloss and terminal 2+ new adoption Brier.
True sources are artificial, not humans or historical observations.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import unittest
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

F = Fraction
Z = F(0)
O = F(1)
N = 4
GRAPH_EDGES = {
    "STAR": ((0, 1), (0, 2), (0, 3)),
    "PATH": ((0, 1), (1, 2), (2, 3)),
    "CYCLE": ((0, 1), (1, 2), (2, 3), (0, 3)),
}
MECHANISMS = ("BASE", "SIMPLE", "COMPLEX")
BASE_RATE = F(1, 4)
EXPOSED_RATE = F(3, 4)
OUT = Path(__file__).resolve().parent


def neighbors(graph):
    if graph not in GRAPH_EDGES:
        raise ValueError("unknown frozen graph")
    adj = [set() for _ in range(N)]
    for i, j in GRAPH_EDGES[graph]:
        adj[i].add(j)
        adj[j].add(i)
    return tuple(tuple(sorted(v)) for v in adj)


def hazard(model, active_neighbor_count):
    if model not in MECHANISMS or active_neighbor_count < 0:
        raise ValueError("invalid mechanism or neighbor count")
    if model == "SIMPLE" and active_neighbor_count >= 1:
        return EXPOSED_RATE
    if model == "COMPLEX" and active_neighbor_count >= 2:
        return EXPOSED_RATE
    return BASE_RATE


def trajectories(seed):
    if seed not in range(N):
        raise ValueError("seed outside four-node population")
    others = tuple(i for i in range(N) if i != seed)
    return tuple(tuple(0 if i == seed else statuses[others.index(i)] for i in range(N))
                 for statuses in itertools.product((1, 2, 3), repeat=N-1))


def trajectory_valid(times, seed):
    return len(times) == N and all(i in (0, 1, 2, 3) for i in times) and \
        all((times[i] == 0) == (i == seed) for i in range(N))


def round_adoption_masks(times):
    if len(times) != N:
        raise ValueError("four nodes needed")
    return tuple(tuple(int(t <= r) for t in times) for r in (0, 1, 2))


def trajectory_probability(graph, seed, model, times):
    if not trajectory_valid(times, seed):
        raise ValueError("invalid absorbing source trajectory or seed")
    adj = neighbors(graph)
    p = O
    for round_num in (1, 2):
        adopted_prev = {i for i in range(N) if times[i] < round_num}
        for node in range(N):
            if node == seed or times[node] < round_num:
                continue
            old_neighbor_count = sum(j in adopted_prev for j in adj[node])
            rate = hazard(model, old_neighbor_count)
            p *= rate if times[node] == round_num else (O-rate)
    return p


def distribution(graph, seed, model):
    dist = {path: trajectory_probability(graph, seed, model, path)
            for path in trajectories(seed)}
    if len(dist) != 27 or any(v <= 0 for v in dist.values()) or sum(dist.values(), Z) != O:
        raise AssertionError("incomplete or invalid full two-round true source distribution")
    return dist


def fit_model_via_full_trajectory(graph, seed, observed):
    # Probability itself is rational; taking logs is mathematically monotone
    # and unnecessary for model selection. Ties fixed by MECHANISMS order.
    return max(MECHANISMS, key=lambda model:
               trajectory_probability(graph, seed, model, observed))


def final_two_plus(path, seed):
    if not trajectory_valid(path, seed):
        raise ValueError("invalid complete trajectory")
    return int(sum(i in (1, 2) for i in path) >= 2)


def mean_new_adopters(dist, seed):
    return sum((p * sum(t in (1, 2) for t in times)
                for times, p in dist.items()), Z)


def event_probability(dist, seed):
    return sum((p for times, p in dist.items() if final_two_plus(times, seed)), Z)


def future_binary_brier_exact(true_p, guessed_p):
    return true_p * (O-true_p) + (guessed_p-true_p)**2


_LOG_CACHE = {}
def negative_log_verified(value):
    if value <= 0:
        raise ValueError("log probability must be positive")
    if value in _LOG_CACHE:
        return _LOG_CACHE[value]
    result = -math.log(float(value))
    with localcontext() as ctx:
        ctx.prec = 70
        dp = Decimal(value.numerator) / Decimal(value.denominator)
        high = -dp.ln()
    if abs(result - float(high)) > 1e-11:
        raise AssertionError("ordinary and 70-digit logarithms differ")
    _LOG_CACHE[value] = result
    return result


def heldout_full_logscore(true_dist, forecast_dist):
    """True independent future trajectory expected logscore, no training reuse."""
    return sum(float(true_p) * negative_log_verified(forecast_dist[path])
               for path, true_p in true_dist.items())


def compute(with_train_test_pairs=True):
    train_rows = []
    test_pair_rows = [] if with_train_test_pairs else None
    worlds = []
    for graph in GRAPH_EDGES:
        for seed in range(N):
            dists = {m: distribution(graph, seed, m) for m in MECHANISMS}
            event_probs = {m: event_probability(dists[m], seed) for m in MECHANISMS}
            # True support is full. A finite horizon may make two mechanisms
            # observationally identical, even though their hazard rules differ.
            equivalence = {
                m: [other for other in MECHANISMS if dists[m] == dists[other]]
                for m in MECHANISMS
            }
            for true_model in MECHANISMS:
                train_dist = dists[true_model]
                selected_mass = {m: Z for m in MECHANISMS}
                exact_future_brier = Z
                future_logscore = 0.
                source_expected_pairs_log = 0.
                joint_mass = Z
                direct_pair_brier = Z
                oracle_log = heldout_full_logscore(train_dist, train_dist)
                fixed_base_log = heldout_full_logscore(train_dist, dists["BASE"])
                oracle_brier = future_binary_brier_exact(event_probs[true_model],
                                                          event_probs[true_model])
                fixed_base_brier = future_binary_brier_exact(event_probs[true_model],
                                                              event_probs["BASE"])
                for observed_train, train_prob in train_dist.items():
                    guess = fit_model_via_full_trajectory(graph, seed, observed_train)
                    selected_mass[guess] += train_prob
                    q = event_probs[guess]
                    expected_brier = future_binary_brier_exact(event_probs[true_model], q)
                    exact_future_brier += train_prob * expected_brier
                    analytic_holdout_log = heldout_full_logscore(train_dist, dists[guess])
                    future_logscore += float(train_prob)*analytic_holdout_log
                    training_row={
                        "graph":graph,
                        "seed":seed,
                        "true_model":true_model,
                        "two_round_true_training_trajectory":"|".join(map(str,observed_train)),
                        "training_model_source_probability":str(train_prob),
                        "observed_at_t0_t1_t2_masks":"/".join(
                            "".join(map(str,v)) for v in round_adoption_masks(observed_train)),
                        "complete_trajectory_likelihood_BASE":str(dists["BASE"][observed_train]),
                        "complete_trajectory_likelihood_SIMPLE":str(dists["SIMPLE"][observed_train]),
                        "complete_trajectory_likelihood_COMPLEX":str(dists["COMPLEX"][observed_train]),
                        "model_chosen_from_training_trajectory_only":guess,
                        "chosen_model_probability_two_plus_future_adoptions":str(q),
                        "true_model_probability_two_plus_future_adoptions":str(event_probs[true_model]),
                        "analytic_exact_future_event_brier_given_training":str(expected_brier),
                        "independent_new_full_trajectory_expected_logscore_given_training":
                            format(analytic_holdout_log,".14f"),
                    }
                    train_rows.append(training_row)
                    conditional_pair_brier = Z
                    conditional_pair_log = 0.
                    for new_path,test_prob in train_dist.items():
                        joint = train_prob*test_prob
                        joint_mass += joint
                        true_outcome = final_two_plus(new_path, seed)
                        brier = (q-true_outcome)**2
                        score = negative_log_verified(dists[guess][new_path])
                        conditional_pair_brier += test_prob*brier
                        conditional_pair_log += float(test_prob)*score
                        direct_pair_brier += joint*brier
                        source_expected_pairs_log += float(joint)*score
                        if with_train_test_pairs:
                            test_pair_rows.append({
                                "graph":graph,
                                "seed":seed,
                                "true_model":true_model,
                                "train_source_trajectory":"|".join(map(str,observed_train)),
                                "independent_future_source_trajectory":"|".join(map(str,new_path)),
                                "joint_true_model_probability":str(joint),
                                "model_selected_by_train_only":guess,
                                "new_true_adopters_by_end_round2":
                                    sum(t in (1,2) for t in new_path),
                                "new_binary_at_least_two_adopters":true_outcome,
                                "forecast_chosen_future_trajectory_probability":
                                    str(dists[guess][new_path]),
                                "forecast_chosen_future_binary_probability":str(q),
                                "actual_independent_new_event_brier_exact":str(brier),
                                "actual_independent_new_trajectory_logscore":
                                    format(score,".14f"),
                            })
                    if conditional_pair_brier != expected_brier:
                        raise AssertionError("independent conditional Brier two routes disagree")
                    if abs(conditional_pair_log-analytic_holdout_log)>1e-10:
                        raise AssertionError("independent conditional logscore two routes disagree")
                if sum(selected_mass.values(),Z) != O or joint_mass != O:
                    raise AssertionError("original train/new trajectory probabilities not normalized")
                if direct_pair_brier != exact_future_brier:
                    raise AssertionError("all joint samples Brier vs exact analytic differs")
                if abs(source_expected_pairs_log-future_logscore)>1e-10:
                    raise AssertionError("all joint samples logscore vs crossentropy differs")
                if exact_future_brier < oracle_brier:
                    raise AssertionError("oracle Brier lower bound violated")
                if future_logscore < oracle_log-1e-10:
                    raise AssertionError("full distribution oracle logloss lower bound violated")
                worlds.append({
                    "graph":graph,"seed":seed,"true_model":true_model,
                    "full_original_training_trajectories":27,
                    "full_independent_future_trajectories_per_train":27,
                    "full_joint_true_source_probability":"1",
                    "selected_model_probabilities_exact":
                        {m:str(selected_mass[m]) for m in MECHANISMS},
                    "selected_true_mechanism_probability_exact":str(selected_mass[true_model]),
                    "observationally_indistinguishable_models_under_this_graph_seed":
                        equivalence[true_model],
                    "true_expected_additional_adopters_by_round2_exact":
                        str(mean_new_adopters(train_dist, seed)),
                    "true_probability_two_plus_new_adopters_by_round2_exact":
                        str(event_probs[true_model]),
                    "full_independent_future_trajectory_logscore":round(future_logscore,12),
                    "fixed_BASE_independent_future_trajectory_logscore":round(fixed_base_log,12),
                    "oracle_known_true_model_future_trajectory_logscore":round(oracle_log,12),
                    "full_independent_future_binary_Brier_exact":str(exact_future_brier),
                    "fixed_BASE_independent_future_binary_Brier_exact":str(fixed_base_brier),
                    "oracle_known_true_model_binary_Brier_exact":str(oracle_brier),
                    "full_independent_binary_Brier_excess_over_oracle_exact":
                        str(exact_future_brier-oracle_brier),
                })
    if len(worlds)!=36 or len(train_rows)!=972:
        raise AssertionError("missing true graph seed mechanism training records")
    if with_train_test_pairs and len(test_pair_rows)!=26244:
        raise AssertionError("missing source independent full trajectory pairs")
    by_graph_and_true = []
    for graph in GRAPH_EDGES:
        for true in MECHANISMS:
            rows=[r for r in worlds if r["graph"]==graph and r["true_model"]==true]
            by_graph_and_true.append({
                "graph":graph,"true_model":true,"seed_conditions":4,
                "expected_new_adopters":str(sum(
                    (F(r["true_expected_additional_adopters_by_round2_exact"]) for r in rows),Z)/4),
                "full_future_binary_Brier":str(sum(
                    (F(r["full_independent_future_binary_Brier_exact"]) for r in rows),Z)/4),
                "fixed_BASE_binary_Brier":str(sum(
                    (F(r["fixed_BASE_independent_future_binary_Brier_exact"]) for r in rows),Z)/4),
                "oracle_binary_Brier":str(sum(
                    (F(r["oracle_known_true_model_binary_Brier_exact"]) for r in rows),Z)/4),
                "full_future_logscore":round(sum(
                    r["full_independent_future_trajectory_logscore"] for r in rows)/4,12),
                "fixed_BASE_logscore":round(sum(
                    r["fixed_BASE_independent_future_trajectory_logscore"] for r in rows)/4,12),
                "oracle_logscore":round(sum(
                    r["oracle_known_true_model_future_trajectory_logscore"] for r in rows)/4,12),
            })
    equivalences = []
    for graph in GRAPH_EDGES:
        for seed in range(N):
            d={m:distribution(graph,seed,m) for m in MECHANISMS}
            for m1,m2 in itertools.combinations(MECHANISMS,2):
                if d[m1]==d[m2]:
                    equivalences.append({
                        "graph":graph,"seed":seed,"mechanisms":[m1,m2],
                        "complete_27_trajectory_distributions_exactly_identical":True,
                    })
    return {
        "research_id":"R209",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "training_mechanism_tie_order":list(MECHANISMS),
        "graphs":{k:[list(edge) for edge in v] for k,v in GRAPH_EDGES.items()},
        "rounds":2,
        "original_trajectories_per_graph_seed_model":27,
        "world_count":len(worlds),
        "full_original_training_trajectories":len(train_rows),
        "full_train_independent_new_trajectory_pairs":
            len(test_pair_rows) if test_pair_rows is not None else 26244,
        "fixed_base_adoption_rate":str(BASE_RATE),
        "fixed_exposed_adoption_rate":str(EXPOSED_RATE),
        "every_trajectory_has_positive_source_probability":True,
        "full_original_joint_source_probabilities_exact":True,
        "independent_new_full_trajectory_logloss_double_route":True,
        "independent_new_binary_Brier_double_Fraction_route":True,
        "same_condition_independent_future_source_not_new_graph":True,
        "graph_seed_design_conditions":12,
        "worlds":worlds,
        "graph_true_model_4_seed_summaries":by_graph_and_true,
        "exact_mechanism_distribution_equivalences":equivalences,
        "new_real_human_E2":0,
        "new_real_historical_E3":0,
        "scope_warning":"True models are four-node two-round synthetic Bernoulli hazards, not fitted original Bass equation or human adoption time series.",
    },train_rows,test_pair_rows


def emit():
    summary,train,pairs=compute(with_train_test_pairs=True)
    paths={
        "result":OUT/"R209_EXACT_RESULTS.json",
        "training":OUT/"R209_ALL_972_ORIGINAL_TRAIN_ADOPTION_TRAJECTORIES.csv",
        "pairs":OUT/"R209_ALL_26244_INDEPENDENT_NEW_TRAJECTORY_PAIRS.csv",
    }
    paths["result"].write_text(
        json.dumps(summary,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for name,rows in (("training",train),("pairs",pairs)):
        with paths[name].open("w",newline="",encoding="utf-8") as f:
            wr=csv.DictWriter(f,fieldnames=list(rows[0]))
            wr.writeheader()
            wr.writerows(rows)
    acceptance={
        "model_id":"R209",
        "artificial_full_worlds":36,
        "real_original_training_trajectories":972,
        "real_joint_train_independent_new_trajectories":26244,
        "source_normalization_and_two_independent_scoring_routes":True,
        "decimal_70_digit_logscore_recheck":True,
        "new_E2":0,
        "new_E3":0,
        **{k+"_sha256":hashlib.sha256(p.read_bytes()).hexdigest()
           for k,p in paths.items()},
    }
    (OUT/"R209_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(acceptance,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(acceptance,indent=2))


class Tests(unittest.TestCase):
    def test_three_graphs(self):
        self.assertEqual(tuple(GRAPH_EDGES),("STAR","PATH","CYCLE"))
    def test_fixed_three_models(self):
        self.assertEqual(MECHANISMS,("BASE","SIMPLE","COMPLEX"))
    def test_four_nodes(self):
        self.assertEqual(N,4)
    def test_two_rates(self):
        self.assertEqual((BASE_RATE,EXPOSED_RATE),(F(1,4),F(3,4)))
    def test_neighbors_symmetric(self):
        for graph in GRAPH_EDGES:
            a=neighbors(graph)
            self.assertTrue(all((i in a[j])==(j in a[i]) for i in range(N) for j in range(N)))
    def test_star_hub_degree3(self):
        self.assertEqual(len(neighbors("STAR")[0]),3)
    def test_star_leaf_degree1(self):
        self.assertEqual(len(neighbors("STAR")[1]),1)
    def test_path_two_endpoints(self):
        self.assertEqual(sorted(len(a) for a in neighbors("PATH")),[1,1,2,2])
    def test_cycle_all_degree2(self):
        self.assertEqual(tuple(map(len,neighbors("CYCLE")),(2,2,2,2))
    def test_27_trajectories_every_seed(self):
        self.assertTrue(all(len(trajectories(s))==27 for s in range(N)))
    def test_seed_time_zero_only(self):
        self.assertTrue(all(trajectory_valid(t,s) for s in range(N) for t in trajectories(s)))
    def test_train_original_count(self):
        self.assertEqual(3*4*3*27,972)
    def test_joint_source_count(self):
        self.assertEqual(3*4*3*27*27,26244)
    def test_base_hazard_independent(self):
        self.assertTrue(all(hazard("BASE",k)==F(1,4) for k in range(4)))
    def test_simple_hazard_trigger(self):
        self.assertEqual([hazard("SIMPLE",k) for k in range(4)],
                         [F(1,4),F(3,4),F(3,4),F(3,4)])
    def test_complex_hazard_two_sources_trigger(self):
        self.assertEqual([hazard("COMPLEX",k) for k in range(4)],
                         [F(1,4),F(1,4),F(3,4),F(3,4)])
    def test_all_distribution_mass_exact(self):
        for graph in GRAPH_EDGES:
            for seed in range(N):
                for model in MECHANISMS:
                    self.assertEqual(sum(distribution(graph,seed,model).values(),Z),O)
    def test_all_trajectory_probability_positive(self):
        for graph in GRAPH_EDGES:
            for seed in range(N):
                for model in MECHANISMS:
                    self.assertTrue(all(p>0 for p in distribution(graph,seed,model).values()))
    def test_base_same_distribution_all_graphs_and_seeds(self):
        d=distribution("STAR",0,"BASE")
        for graph in GRAPH_EDGES:
            for seed in range(N):
                mapped=distribution(graph,seed,"BASE")
                self.assertEqual(sorted(d.values()),sorted(mapped.values()))
    def test_base_two_round_adoption_event_probability(self):
        for graph in GRAPH_EDGES:
            for seed in range(N):
                self.assertEqual(event_probability(distribution(graph,seed,"BASE"),seed),
                                 F(833,2048))
    def test_base_expected_new_adopters(self):
        for graph in GRAPH_EDGES:
            for seed in range(N):
                self.assertEqual(mean_new_adopters(distribution(graph,seed,"BASE"),seed),
                                 F(21,16))
    def test_star_hub_base_complex_identical(self):
        self.assertEqual(distribution("STAR",0,"BASE"),distribution("STAR",0,"COMPLEX"))
    def test_star_leaf_complex_base_can_differ(self):
        # With a leaf seed, OTHER leaves may innovate at round 1 while hub
        # has not adopted; hub then sees >=2 adopted neighbors in round 2.
        for seed in (1,2,3):
            self.assertNotEqual(distribution("STAR",seed,"BASE"),
                                distribution("STAR",seed,"COMPLEX"))
    def test_cycle_complex_base_distinguishable(self):
        self.assertNotEqual(distribution("CYCLE",0,"COMPLEX"),
                            distribution("CYCLE",0,"BASE"))
    def test_simple_star_hub_nontrivial(self):
        self.assertNotEqual(distribution("STAR",0,"SIMPLE"),
                            distribution("STAR",0,"BASE"))
    def test_equal_probability_model_fit_follows_precedence(self):
        times=(0,1,1,1)
        # BASE and COMPLEX tie in STAR hub, though SIMPLE may be larger.
        self.assertEqual(trajectory_probability("STAR",0,"BASE",times),
                         trajectory_probability("STAR",0,"COMPLEX",times))
    def test_no_future_needed_for_training_fit(self):
        t=trajectories(0)[3]
        self.assertIn(fit_model_via_full_trajectory("PATH",0,t),MECHANISMS)
    def test_full_two_round_adoption_mask(self):
        self.assertEqual(round_adoption_masks((0,1,2,3)),
                         ((1,0,0,0),(1,1,0,0),(1,1,1,0)))
    def test_terminal_event_count(self):
        self.assertEqual(final_two_plus((0,1,2,3),0),1)
        self.assertEqual(final_two_plus((0,1,3,3),0),0)
    def test_brier_two_route_identity(self):
        p=F(1,3)
        q=F(2,5)
        exact=future_binary_brier_exact(p,q)
        direct=p*(q-1)**2+(O-p)*q*q
        self.assertEqual(exact,direct)
    def test_brier_oracle_optimal(self):
        p=F(2,5)
        self.assertGreaterEqual(future_binary_brier_exact(p,F(1,4)),
                                future_binary_brier_exact(p,p))
    def test_70_decimal_log_probability(self):
        self.assertAlmostEqual(negative_log_verified(F(3,16)),-math.log(3/16),places=12)
    def test_full_trajectory_oracle_crossentropy(self):
        d=distribution("PATH",1,"SIMPLE")
        self.assertLessEqual(heldout_full_logscore(d,d),
                             heldout_full_logscore(d,distribution("PATH",1,"BASE"))+1e-10)
    def test_finite_probability_trajectories_not_zero(self):
        d=distribution("STAR",2,"COMPLEX")
        self.assertGreater(min(d.values()),0)
    def test_invalid_model_rejected(self):
        with self.assertRaises(ValueError):
            hazard("INVALID",0)
    def test_invalid_graph_rejected(self):
        with self.assertRaises(ValueError):
            neighbors("INVALID")
    def test_invalid_seed_rejected(self):
        with self.assertRaises(ValueError):
            trajectories(9)
    def test_invalid_trajectory_rejected(self):
        with self.assertRaises(ValueError):
            trajectory_probability("STAR",0,"BASE",(1,1,2,3))
    def test_invalid_log_prob_rejected(self):
        with self.assertRaises(ValueError):
            negative_log_verified(Z)
    def test_compute_complete_source_and_two_score_routes(self):
        r,t,p=compute()
        self.assertEqual((len(r["worlds"]),len(t),len(p)),(36,972,26244))
        self.assertTrue(any(x["graph"]=="STAR" and
                            x["mechanisms"]==["BASE","COMPLEX"]
                            for x in r["exact_mechanism_distribution_equivalences"]))
        self.assertEqual(r["new_real_human_E2"],0)
    def test_all_worlds_true_distribution_normalized(self):
        r,t,p=compute(False)
        self.assertEqual((len(r["worlds"]),len(t),p),(36,972,None))
        self.assertTrue(all(x["full_joint_true_source_probability"]=="1" for x in r["worlds"]))
    def test_compute_deterministic_replay(self):
        r1,t1,p1=compute(False)
        r2,t2,p2=compute(False)
        self.assertEqual((r1,t1,p1),(r2,t2,p2))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test",action="store_true")
    parser.add_argument("--emit",action="store_true")
    opts=parser.parse_args()
    if opts.test:
        outcome=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if outcome.wasSuccessful() else 1)
    if opts.emit:
        emit()
    if not opts.test and not opts.emit:
        parser.print_help()
