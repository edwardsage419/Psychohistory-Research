#!/usr/bin/env python3
"""R207 exact positive rank-one 3x3 matrix completion, ALL 5-entry masks.

Four heldout entries from the SAME matrix are concealed from each predictor;
they are not a new independent matrix or a real historical forecast.

Generative prior: six independent equally likely {1,2} factors, 64 original
latent sources (including different factor configurations with identical M).
Compare an explicitly informed finite Bayes posterior mean, mean imputation,
and zero imputation. Check 5-edge observation graph connectivity by BFS and
union-find, 64-source empirical risk vs grouped conditional variance, and
continuous nonidentification for a disconnected mask.

python r207_exact_matrix_completion.py --test
python r207_exact_matrix_completion.py --emit
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import unittest
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

F = Fraction
Z = F(0)
ONE = F(1)
N = 3
POSITIONS = tuple((i,j) for i in range(N) for j in range(N))
MASKS = tuple(itertools.combinations(POSITIONS,5))
SOURCES = tuple(itertools.product((1,2), repeat=6))
OUTPUT = Path(__file__).resolve().parent

def source_matrix(factors):
    if len(factors)!=6 or any(i not in (1,2) for i in factors):
        raise ValueError("six row/col factors in 1 or 2 required")
    rows, cols=factors[:N],factors[N:]
    return tuple(tuple(F(rows[i]*cols[j]) for j in range(N)) for i in range(N))

def arbitrary_outer(a,b):
    if len(a)!=N or len(b)!=N:
        raise ValueError("length3 factors required")
    return tuple(tuple(a[i]*b[j] for j in range(N)) for i in range(N))

def flat_matrix(matrix):
    return tuple(matrix[i][j] for i,j in POSITIONS)

def mask_valid(mask):
    if len(mask)!=5 or len(set(mask))!=5 or any(pos not in POSITIONS for pos in mask):
        raise ValueError("five distinct 3x3 positions required")

def missing(mask):
    mask_valid(mask)
    return tuple(p for p in POSITIONS if p not in mask)

def mask_id(mask):
    return "|".join(f"{i}{j}" for i,j in mask)

def observed_signature(matrix,mask):
    return tuple(matrix[i][j] for i,j in mask)

def graph_connected_bfs(mask):
    mask_valid(mask)
    adj={k:set() for k in range(6)}
    for i,j in mask:
        adj[i].add(j+3)
        adj[j+3].add(i)
    visited={0}
    stack=[0]
    while stack:
        v=stack.pop()
        for w in adj[v]:
            if w not in visited:
                visited.add(w)
                stack.append(w)
    return len(visited)==6

def graph_connected_union_find(mask):
    mask_valid(mask)
    parent=list(range(6))
    def find(k):
        while parent[k]!=k:
            k=parent[k]
        return k
    for i,j in mask:
        a,b=find(i),find(j+3)
        if a!=b:
            parent[b]=a
    return len(set(find(i) for i in range(6)))==1

def mean_values(values):
    if not values:
        raise ValueError("nonempty")
    return sum(values,Z)/len(values)

def mse(values):
    return mean_values(values)

def retained_candidate_groups(mask):
    """Observed values alone select posterior candidates, not heldout entries."""
    groups=defaultdict(list)
    for factors in SOURCES:
        mat=source_matrix(factors)
        groups[observed_signature(mat,mask)].append(mat)
    assert sum(len(v) for v in groups.values())==64
    return dict(groups)

def bayes_completion(candidates, holdout):
    if not candidates:
        raise ValueError("no source-compatible matrices")
    return tuple(mean_values([mat[i][j] for mat in candidates]) for i,j in holdout)

def posterior_variance_oracle_risk(candidates, holdout):
    """Exact conditional source variance independent of loss-to-prediction evaluation."""
    variances=[]
    for i,j in holdout:
        nums=[mat[i][j] for mat in candidates]
        variances.append(mean_values([val*val for val in nums])-mean_values(nums)**2)
    return mean_values(variances)

def distinct_completions(candidates):
    return len(set(flat_matrix(mat) for mat in candidates))

def positive_continuous_counterexample():
    mask=((0,0),(0,1),(1,0),(1,1),(2,2))
    a=arbitrary_outer((F(1),F(1),F(1)),(F(1),F(1),F(1)))
    b=arbitrary_outer((F(1),F(1),F(2)),(F(1),F(1),F(1,2)))
    assert observed_signature(a,mask)==observed_signature(b,mask)
    assert a!=b
    assert all(x>0 for x in flat_matrix(a)+flat_matrix(b))
    return mask,a,b

def compute():
    if len(MASKS)!=126 or len(SOURCES)!=64:
        raise AssertionError("source size wrong")
    details=[]
    worlds=[]
    connected_count=0
    disconnected_count=0
    for mask in MASKS:
        is_conn=graph_connected_bfs(mask)
        if is_conn!=graph_connected_union_find(mask):
            raise AssertionError("independent connectivity algorithms disagree")
        connected_count+=int(is_conn)
        disconnected_count+=int(not is_conn)
        holdout=missing(mask)
        groups=retained_candidate_groups(mask)
        # Match only on five visible observations.
        group_predictions={
            key:bayes_completion(mats,holdout) for key,mats in groups.items()
        }
        group_conditional_risk=sum(
            (F(len(mats),len(SOURCES))*posterior_variance_oracle_risk(mats,holdout)
             for mats in groups.values()),Z)
        bayes_risk=Z
        mean_risk=Z
        zero_risk=Z
        unique_completion_probability=Z
        posterior_support_sum=Z
        max_completion_candidates=0
        for factors in SOURCES:
            truth=source_matrix(factors)
            key=observed_signature(truth,mask)
            candidates=groups[key]
            pred_b=group_predictions[key]
            observed_mean=mean_values(key)
            pred_mean=(observed_mean,)*4
            pred_zero=(Z,)*4
            true_missing=tuple(truth[i][j] for i,j in holdout)
            errs_b=tuple((true_missing[k]-pred_b[k])**2 for k in range(4))
            errs_mean=tuple((true_missing[k]-pred_mean[k])**2 for k in range(4))
            errs_zero=tuple((true_missing[k]-pred_zero[k])**2 for k in range(4))
            local_b=mean_values(errs_b)
            local_mean=mean_values(errs_mean)
            local_zero=mean_values(errs_zero)
            bayes_risk+=local_b/64
            mean_risk+=local_mean/64
            zero_risk+=local_zero/64
            unique=distinct_completions(candidates)==1
            unique_completion_probability+=F(int(unique),64)
            max_completion_candidates=max(max_completion_candidates,distinct_completions(candidates))
            posterior_support_sum+=F(len(candidates),64)
            if is_conn and (not unique or local_b!=0):
                raise AssertionError("connected five-edge rank one tree did not recover exact")
            details.append({
                "mask_id":mask_id(mask),
                "observed_entry_coordinates":mask_id(mask),
                "unobserved_entry_coordinates":mask_id(holdout),
                "five_edge_bipartite_graph_connected":int(is_conn),
                "source_row_factors":"|".join(map(str,factors[:3])),
                "source_col_factors":"|".join(map(str,factors[3:])),
                "source_original_probability":"1/64",
                "true_full_matrix_row_major":"|".join(map(str,flat_matrix(truth))),
                "observed_five_values":"|".join(map(str,key)),
                "true_four_heldout_values":"|".join(map(str,true_missing)),
                "finite_posterior_source_factor_count":len(candidates),
                "distinct_supported_full_rank1_completions":distinct_completions(candidates),
                "finite_posterior_completion_unique":int(unique),
                "informed_bayes_four_predictions":"|".join(map(str,pred_b)),
                "visible_mean_baseline_four_predictions":"|".join(map(str,pred_mean)),
                "zero_baseline_four_predictions":"|".join(map(str,pred_zero)),
                "informed_bayes_four_heldout_squared_errors":"|".join(map(str,errs_b)),
                "visible_mean_four_heldout_squared_errors":"|".join(map(str,errs_mean)),
                "zero_four_heldout_squared_errors":"|".join(map(str,errs_zero)),
                "informed_bayes_average_missing_mse":str(local_b),
                "visible_mean_average_missing_mse":str(local_mean),
                "zero_average_missing_mse":str(local_zero),
            })
        if group_conditional_risk!=bayes_risk:
            raise AssertionError("actual missing source risk != separately grouped conditional variance")
        if bayes_risk>mean_risk or bayes_risk>zero_risk:
            raise AssertionError("Bayes optimal conditional mean expected loss violated")
        worlds.append({
            "mask_id":mask_id(mask),
            "observed_count":5,
            "heldout_count":4,
            "graph_connected":is_conn,
            "source_count":64,
            "full_source_probability_sum":"1",
            "number_observable_signatures":len(groups),
            "expected_number_of_matching_factor_sources":str(posterior_support_sum),
            "max_distinct_supported_rankone_completions":max_completion_candidates,
            "probability_finite_prior_unique_completion":str(unique_completion_probability),
            "bayes_source_expected_heldout_mse_exact":str(bayes_risk),
            "visible_mean_expected_heldout_mse_exact":str(mean_risk),
            "zero_expected_heldout_mse_exact":str(zero_risk),
            "independent_grouped_conditional_variance_exact":str(group_conditional_risk),
        })
    assert connected_count==81 and disconnected_count==45
    assert len(worlds)==126 and len(details)==8064
    def summarize(conn):
        rows=[w for w in worlds if w["graph_connected"]==conn]
        out={}
        for k in (
            "bayes_source_expected_heldout_mse_exact",
            "visible_mean_expected_heldout_mse_exact",
            "zero_expected_heldout_mse_exact",
            "probability_finite_prior_unique_completion",
        ):
            out[k]=str(mean_values([F(w[k]) for w in rows]))
        out["mask_count"]=len(rows)
        return out
    mask,example_a,example_b=positive_continuous_counterexample()
    diagnostics={
        "all_true_rankone_positive_nonzero":True,
        "full_five_entry_mask_count":126,
        "full_original_factor_source_count":64,
        "full_original_mask_and_factor_pair_count":8064,
        "four_heldout_entries_per_original_source":4,
        "individual_heldout_entry_losses":32256,
        "connected_trees_count":connected_count,
        "disconnected_masks_count":disconnected_count,
        "graph_connectivity_two_independent_routes":True,
        "posterior_mse_equals_grouped_conditional_variance_all_masks":True,
        "continuous_nonidentification_example_observed_mask":mask_id(mask),
        "continuous_nonidentification_example_mat_A":[str(v) for v in flat_matrix(example_a)],
        "continuous_nonidentification_example_mat_B":[str(v) for v in flat_matrix(example_b)],
        "continuous_example_two_positive_rankone_matrices_same_observations":True,
        "true_source": "six independent {1,2} row/col factors with equal probability; 64 original paths",
        "heldout_description": "four unseen coordinates from same matrix, NOT independent future matrix",
        "method_scope":"Known finite rank-one factor prior Bayesian oracle, not nuclear norm optimization or noisy general matrix completion",
    }
    return {
        "research_id":"R207",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "reference_doi":"10.1007/s10208-009-9045-5",
        "full_masks":126,
        "full_original_mask_factor_source_records":8064,
        "full_heldout_entry_squared_errors":32256,
        "new_real_human_E2":0,
        "new_real_historical_E3":0,
        "connected_graph_masks":summarize(True),
        "disconnected_graph_masks":summarize(False),
        "diagnostics":diagnostics,
        "worlds":worlds,
    },details

def emit():
    r,detail=compute()
    result_path=OUTPUT/"R207_EXACT_RESULTS.json"
    detail_path=OUTPUT/"R207_ALL_8064_ORIGINAL_MASK_AND_FACTOR_SOURCES.csv"
    result_path.write_text(json.dumps(r,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    with detail_path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(detail[0]))
        writer.writeheader()
        writer.writerows(detail)
    accept={
        "model_id":"R207",
        "masks":126,
        "connected":81,
        "disconnected":45,
        "full_original_mask_and_factor_sources":8064,
        "full_heldout_squared_errors":32256,
        "two_graph_connectivity_methods_agree":True,
        "two_independent_fraction_posterior_risks_agree":True,
        "new_E2":0,
        "new_E3":0,
        "result_sha256":hashlib.sha256(result_path.read_bytes()).hexdigest(),
        "full_source_sha256":hashlib.sha256(detail_path.read_bytes()).hexdigest(),
    }
    (OUTPUT/"R207_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(accept,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(accept,indent=2))

class Tests(unittest.TestCase):
    def test_positions_nine(self):
        self.assertEqual(len(POSITIONS),9)

    def test_masks_126(self):
        self.assertEqual(len(MASKS),126)

    def test_sources_64(self):
        self.assertEqual(len(SOURCES),64)

    def test_sources_factor_six(self):
        self.assertTrue(all(len(s)==6 for s in SOURCES))

    def test_source_positive(self):
        for s in SOURCES:
            self.assertTrue(all(v>0 for v in flat_matrix(source_matrix(s))))

    def test_source_rankone_minors_zero(self):
        for s in SOURCES:
            a=source_matrix(s)
            for i1,i2 in itertools.combinations(range(3),2):
                for j1,j2 in itertools.combinations(range(3),2):
                    self.assertEqual(a[i1][j1]*a[i2][j2],
                                     a[i1][j2]*a[i2][j1])

    def test_5_obs_4_missing(self):
        for mask in MASKS:
            self.assertEqual(len(missing(mask)),4)

    def test_every_mask_unique(self):
        self.assertEqual(len(set(MASKS)),126)

    def test_graph_methods_all(self):
        for mask in MASKS:
            self.assertEqual(graph_connected_bfs(mask),graph_connected_union_find(mask))

    def test_graph_connected_81(self):
        self.assertEqual(sum(graph_connected_bfs(m) for m in MASKS),81)

    def test_graph_disconnected_45(self):
        self.assertEqual(sum(not graph_connected_bfs(m) for m in MASKS),45)

    def test_connected_tree_example(self):
        m=((0,0),(0,1),(1,1),(1,2),(2,2))
        self.assertTrue(graph_connected_bfs(m))

    def test_disconnected_full_coverage_example(self):
        m=((0,0),(0,1),(1,0),(1,1),(2,2))
        self.assertFalse(graph_connected_bfs(m))
        self.assertEqual(len({i for i,j in m}),3)
        self.assertEqual(len({j for i,j in m}),3)

    def test_zero_values_not_in_source(self):
        self.assertTrue(all(v in (1,2,4) for s in SOURCES for v in flat_matrix(source_matrix(s))))

    def test_posterior_groups_sum_sources(self):
        for mask in MASKS:
            self.assertEqual(sum(map(len,retained_candidate_groups(mask).values())),64)

    def test_posterior_finds_truth(self):
        mask=MASKS[0]
        groups=retained_candidate_groups(mask)
        for s in SOURCES:
            m=source_matrix(s)
            self.assertIn(m,groups[observed_signature(m,mask)])

    def test_group_posterior_mean_exact(self):
        candidates=(source_matrix((1,1,1,1,1,1)),
                    source_matrix((2,2,2,1,1,1)))
        self.assertEqual(bayes_completion(candidates,((0,0),(0,1),(1,0),(1,1))),
                         (F(3,2),)*4)

    def test_grouped_variance_never_negative(self):
        mask=MASKS[0]
        for mats in retained_candidate_groups(mask).values():
            self.assertGreaterEqual(posterior_variance_oracle_risk(mats,missing(mask)),0)

    def test_rankone_connected_sources_unique(self):
        for mask in MASKS:
            if graph_connected_bfs(mask):
                self.assertTrue(all(distinct_completions(mats)==1
                                    for mats in retained_candidate_groups(mask).values()))

    def test_disconnected_has_nonunique_finite_case(self):
        m=((0,0),(0,1),(1,0),(1,1),(2,2))
        self.assertTrue(any(distinct_completions(c)>1
                            for c in retained_candidate_groups(m).values()))

    def test_continuous_counterexample_same_visible(self):
        m,a,b=positive_continuous_counterexample()
        self.assertEqual(observed_signature(a,m),observed_signature(b,m))

    def test_continuous_counterexample_missing_differ(self):
        m,a,b=positive_continuous_counterexample()
        self.assertNotEqual(tuple(a[i][j] for i,j in missing(m)),
                            tuple(b[i][j] for i,j in missing(m)))

    def test_continuous_counterexample_rank_one(self):
        m,a,b=positive_continuous_counterexample()
        for mat in (a,b):
            self.assertEqual(mat[0][0]*mat[2][2],mat[0][2]*mat[2][0])

    def test_observed_signature_5(self):
        m=MASKS[0]
        self.assertEqual(len(observed_signature(source_matrix(SOURCES[0]),m)),5)

    def test_source_mean_correct(self):
        self.assertEqual(mean_values((F(1),F(2),F(4))),F(7,3))

    def test_posterior_oracle_variance_identity(self):
        m=((0,0),(0,1),(1,0),(1,1),(2,2))
        missed=missing(m)
        for group in retained_candidate_groups(m).values():
            pred=bayes_completion(group,missed)
            direct=mean_values([
                mean_values([(matrix[i][j]-pred[k])**2
                             for k,(i,j) in enumerate(missed)])
                for matrix in group
            ])
            self.assertEqual(direct,posterior_variance_oracle_risk(group,missed))

    def test_finite_prior_nonuniform_full_matrices(self):
        unique_matrices={flat_matrix(source_matrix(s)) for s in SOURCES}
        self.assertLess(len(unique_matrices),64)

    def test_missing_mask_order_canonical(self):
        m=MASKS[0]
        self.assertEqual(missing(m),tuple(pos for pos in POSITIONS if pos not in m))

    def test_known_individual_disconnected_component_example(self):
        m=((0,0),(0,1),(1,0),(1,1),(2,2))
        groups=retained_candidate_groups(m)
        true=source_matrix((1,1,1,1,1,1))
        group=groups[observed_signature(true,m)]
        self.assertGreaterEqual(len(group),1)

    def test_invalid_mask_repeat_rejected(self):
        with self.assertRaises(ValueError):
            missing(((0,0),)*5)

    def test_invalid_mask_short_rejected(self):
        with self.assertRaises(ValueError):
            missing(((0,0),))

    def test_invalid_source_values_rejected(self):
        with self.assertRaises(ValueError):
            source_matrix((0,1,1,1,1,1))

    def test_invalid_candidate_list_rejected(self):
        with self.assertRaises(ValueError):
            bayes_completion((),((0,0),))

    def test_all_original_sources_and_risks(self):
        r,rows=compute()
        self.assertEqual((len(r["worlds"]),len(rows)),(126,8064))
        self.assertEqual(r["connected_graph_masks"]["mask_count"],81)
        self.assertEqual(r["disconnected_graph_masks"]["mask_count"],45)
        self.assertTrue(all(w["bayes_source_expected_heldout_mse_exact"]=="0"
                            for w in r["worlds"] if w["graph_connected"]))
        self.assertTrue(all(w["full_source_probability_sum"]=="1" for w in r["worlds"]))

    def test_deterministic_full_replay(self):
        self.assertEqual(compute(),compute())

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--test",action="store_true")
    ap.add_argument("--emit",action="store_true")
    opts=ap.parse_args()
    if opts.test:
        ok=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if ok.wasSuccessful() else 1)
    if opts.emit:
        emit()
    if not opts.test and not opts.emit:
        ap.print_help()
