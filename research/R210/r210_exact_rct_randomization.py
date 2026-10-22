#!/usr/bin/env python3
"""R210 09-001 finite-population RCT randomization inference.

Six fixed artificial units, complete balance with 3 treated and 3 control:
all 20 assignment sources equiprobable. Six predeclared no-interference
potential-outcome worlds and one disjoint-pair interference world.

Exact finite Neyman expectation and variance with heterogeneous-effect
correction, conservative observable variance, Fisher sharp-null two-sided
randomization p-values, granularity 1/10, and a direct/spillover bias example.
No observed people, no historical causal identification.
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

F = Fraction
N = 6
Z = F(0)
O = F(1)
ALL_ASSIGNMENTS = tuple(itertools.combinations(range(N), 3))
RAMP = (0, 1, 2, 3, 4, 5)
OUTLIER = (0, 0, 0, 0, 0, 12)
SUTVA_WORLDS = {
    "RAMP_NULL": (RAMP, (0, 0, 0, 0, 0, 0)),
    "OUTLIER_NULL": (OUTLIER, (0, 0, 0, 0, 0, 0)),
    "RAMP_CONST_TWO": (RAMP, (2, 2, 2, 2, 2, 2)),
    "RAMP_SINGLE_HET": (RAMP, (0, 0, 0, 0, 0, 6)),
    "RAMP_ZERO_ATE_HET": (RAMP, (3, -3, 2, -2, 1, -1)),
    "OUTLIER_HET": (OUTLIER, (0, 1, 2, 3, 4, 5)),
}
INTERFERENCE_NAME = "PAIR_INTERFERENCE"
ALPHAS = (F(1, 20), F(1, 10))
OUT = Path(__file__).resolve().parent


def assignment_vector(treated):
    if len(treated) != 3 or len(set(treated)) != 3 or any(i not in range(N) for i in treated):
        raise ValueError("exactly 3 distinct valid treated indices required")
    return tuple(int(i in treated) for i in range(N))


def complement_treated(treated):
    return tuple(i for i in range(N) if i not in treated)


def source_assignment_prob(treated):
    assignment_vector(treated)
    return F(1, len(ALL_ASSIGNMENTS))


def average(xs):
    if not xs:
        raise ValueError("nonempty values")
    return sum((F(x) for x in xs), Z) / len(xs)


def pop_var_sample_denominator(xs):
    """Finite-population variance with denominator n-1 (6->5, 3->2)."""
    if len(xs) < 2:
        raise ValueError("at least two outcomes required")
    avg = average(xs)
    return sum(((F(v) - avg)**2 for v in xs), Z) / (len(xs)-1)


def fixed_potential_outcomes(world):
    if world not in SUTVA_WORLDS:
        raise ValueError("unknown no-interference finite world")
    y0, tau = SUTVA_WORLDS[world]
    return tuple(F(v) for v in y0), tuple(F(v+t) for v,t in zip(y0,tau))


def observed_sutva(world, treated):
    y0, y1 = fixed_potential_outcomes(world)
    z = assignment_vector(treated)
    return tuple(y1[i] if z[i] else y0[i] for i in range(N))


def observed_interference(treated):
    z = assignment_vector(treated)
    # Three disjoint pairs: 0-1, 2-3, 4-5.
    return tuple(F(i + 2*z[i] + 3*z[i^1]) for i in range(N))


def observed(world, treated):
    return observed_interference(treated) if world == INTERFERENCE_NAME \
        else observed_sutva(world, treated)


def diff_in_means(observed_y, treated):
    z = assignment_vector(treated)
    if len(observed_y) != N:
        raise ValueError("six outcomes required")
    return average(tuple(observed_y[i] for i in range(N) if z[i])) - \
        average(tuple(observed_y[i] for i in range(N) if not z[i]))


def observable_neyman_variance(observed_y, treated):
    z = assignment_vector(treated)
    ys1 = tuple(observed_y[i] for i in range(N) if z[i])
    ys0 = tuple(observed_y[i] for i in range(N) if not z[i])
    return pop_var_sample_denominator(ys1)/3 + pop_var_sample_denominator(ys0)/3


def fisher_sharp_zero_p_value(observed_y, treated):
    """Reference distribution for SHARP no-effect hypothesis only."""
    actual = abs(diff_in_means(observed_y, treated))
    complete_null_reference = tuple(abs(diff_in_means(observed_y, new_t))
                                    for new_t in ALL_ASSIGNMENTS)
    if complete_null_reference.count(actual) < 2:
        raise AssertionError("balanced design complementary allocation symmetry failed")
    # Verify complement: with fixed observed outcomes, T(zc) = -T(z).
    for alt in ALL_ASSIGNMENTS:
        if diff_in_means(observed_y, alt) != \
                -diff_in_means(observed_y, complement_treated(alt)):
            raise AssertionError("two-sided complementary assignment symmetry broken")
    p = F(sum(x >= actual for x in complete_null_reference),
          len(ALL_ASSIGNMENTS))
    if p < F(1, 10):
        raise AssertionError("20 balanced assignments cannot yield two-sided p<0.1")
    return p


def analytic_neyman_components(world):
    y0, y1 = fixed_potential_outcomes(world)
    treatment_differences = tuple(y1[i]-y0[i] for i in range(N))
    ate = average(treatment_differences)
    s0 = pop_var_sample_denominator(y0)
    s1 = pop_var_sample_denominator(y1)
    stau = pop_var_sample_denominator(treatment_differences)
    conservative_expected = s0/3 + s1/3
    real_design_var = conservative_expected - stau/N
    if real_design_var < 0:
        raise AssertionError("impossible variance")
    return {
        "population_ATE":ate,
        "finite_pop_s0_squared":s0,
        "finite_pop_s1_squared":s1,
        "finite_pop_stau_squared":stau,
        "true_randomization_variance":real_design_var,
        "design_expected_observable_neyman_variance":conservative_expected,
        "expected_naive_conservatism_gap":stau/N,
    }


def analytic_interference_bias():
    # From conditional treatment in a random balanced assignment:
    # P(peer treated | own treated)=2/5; if own untreated=3/5.
    return {
        "held_peers_fixed_direct_treatment_effect":F(2),
        "peer_exposure_when_own_treated":F(2,5),
        "peer_exposure_when_own_control":F(3,5),
        "peer_spillover_coefficient":F(3),
        "expected_observed_difference_from_assignment_formula":
            F(2)+F(3)*(F(2,5)-F(3,5)),
    }


def compute():
    if len(ALL_ASSIGNMENTS)!=20 or len(SUTVA_WORLDS)!=6:
        raise AssertionError("incorrect frozen source space")
    rows=[]
    summaries=[]
    for world in tuple(SUTVA_WORLDS) + (INTERFERENCE_NAME,):
        valid_no_interference=world in SUTVA_WORLDS
        analytic=analytic_neyman_components(world) if valid_no_interference else None
        per_assignment=[]
        for treated in ALL_ASSIGNMENTS:
            z=assignment_vector(treated)
            values=observed(world, treated)
            est=diff_in_means(values,treated)
            v_est=observable_neyman_variance(values,treated) if valid_no_interference else None
            exact_sharp_p=fisher_sharp_zero_p_value(values,treated) \
                if valid_no_interference else None
            if valid_no_interference and exact_sharp_p < F(1,10):
                raise AssertionError("exact Fisher p-value granularity broken")
            exposure_treated=average(tuple(z[i^1] for i in range(N) if z[i])) if not valid_no_interference else None
            exposure_control=average(tuple(z[i^1] for i in range(N) if not z[i])) if not valid_no_interference else None
            per_assignment.append((treated,values,est,v_est,exact_sharp_p,
                                   exposure_treated,exposure_control))
            rows.append({
                "synthetic_world":world,
                "SUTVA_no_interference_assumption_holds":int(valid_no_interference),
                "ordered_treated_three_ids":"|".join(map(str,treated)),
                "complete_treatment_assignment_z":"|".join(map(str,z)),
                "original_random_assignment_probability":"1/20",
                "true_observed_six_artificial_outcomes":"|".join(map(str,values)),
                "observed_difference_in_means_exact":str(est),
                "observable_neyman_variance_exact":str(v_est) if v_est is not None else "NOT_DEFINED_UNDER_INTERFERENCE",
                "fisher_sharp_zero_two_sided_p_exact":str(exact_sharp_p) if exact_sharp_p is not None else "NOT_VALID_UNDER_INTERFERENCE",
                "pair_exposure_mean_treated":str(exposure_treated) if exposure_treated is not None else "NOT_APPLICABLE",
                "pair_exposure_mean_control":str(exposure_control) if exposure_control is not None else "NOT_APPLICABLE",
            })
        means=tuple(a[2] for a in per_assignment)
        random_mean=average(means)
        empirical_var=average(tuple((v-random_mean)**2 for v in means))
        summary={
            "world":world,
            "SUTVA_no_interference":valid_no_interference,
            "all_assignment_count":20,
            "source_random_assignment_probability_sum":"1",
            "actual_expected_difference_in_means_exact":str(random_mean),
            "actual_randomization_variance_exact":str(empirical_var),
            "randomization_estimator_sign_range":[str(min(means)),str(max(means))],
        }
        if valid_no_interference:
            assert analytic is not None
            if random_mean != analytic["population_ATE"]:
                raise AssertionError("random assignment estimator unbiasedness violated")
            if empirical_var != analytic["true_randomization_variance"]:
                raise AssertionError("finite Neyman randomization variance exact identity broken")
            observable_expected=average(tuple(a[3] for a in per_assignment))
            if observable_expected!=analytic["design_expected_observable_neyman_variance"]:
                raise AssertionError("expected sample conservative Neyman variance differs")
            if observable_expected-empirical_var!=analytic["expected_naive_conservatism_gap"]:
                raise AssertionError("heterogeneous effects variance conservatism identity differs")
            ps=tuple(a[4] for a in per_assignment)
            summary.update({
                **{k:str(v) for k,v in analytic.items()},
                "sample_imbalance_mean_absolute_estimation_error":str(
                    average(tuple(abs(v-random_mean) for v in means))),
                "minimum_exact_two_sided_fisher_sharp_null_p":str(min(ps)),
                "rejection_rate_two_sided_alpha_0_05":str(F(sum(x<=ALPHAS[0] for x in ps),20)),
                "rejection_rate_two_sided_alpha_0_10":str(F(sum(x<=ALPHAS[1] for x in ps),20)),
                "sharp_null_actually_true":all(t==0 for t in
                                               (F(t) for t in SUTVA_WORLDS[world][1])),
                "observed_sample_neyman_variance_expectation":str(observable_expected),
                "warning":"Fisher sharp-null p for no-unit-effect hypothesis; heterogeneous ATE=0 is not sharp-null.",
            })
            if summary["sharp_null_actually_true"]:
                for alpha in ALPHAS:
                    reject=F(sum(x<=alpha for x in ps),20)
                    if reject>alpha:
                        raise AssertionError("true sharp-null design type-I error bound broken")
        else:
            theory=analytic_interference_bias()
            if random_mean!=theory["expected_observed_difference_from_assignment_formula"]:
                raise AssertionError("interference expected treatment effect contamination does not match")
            summary.update({
                "direct_treatment_effect_holding_other_assignments_fixed":"2",
                "analytical_peer_exposure_given_treated":"2/5",
                "analytical_peer_exposure_given_control":"3/5",
                "peer_spillover_coefficient":"3",
                "target_direct_effect_minus_randomization_estimator_expectation":str(F(2)-random_mean),
                "finite_Neyman_no_interference_variance_formula":"NOT_DEFINED_UNDER_INTERFERENCE",
                "Fisher_sharp_null_p_value":"NOT_VALID_UNDER_INTERFERENCE",
                "warning":"No well-defined separate potential outcomes Y_i(1) and Y_i(0) independent of peers; estimator mean 7/5 is NOT direct causal effect 2.",
            })
        summaries.append(summary)
    if len(rows)!=140 or len(summaries)!=7:
        raise AssertionError("not all full finite randomized assignment source records included")
    return {
        "research_id":"R210",
        "original_239_catalogue_id":"09-001",
        "original_239_catalogue_name":"Randomized Controlled Experiment",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "fixed_population_units":6,
        "balanced_treated":3,
        "balanced_control":3,
        "complete_distinct_treatment_assignments":20,
        "source_worlds":7,
        "SUTVA_true_worlds":6,
        "interference_counterexample_worlds":1,
        "original_world_and_complete_assignment_records":len(rows),
        "source_assignment_probability_each":"1/20",
        "two_sided_minimal_exact_p":"1/10",
        "two_sided_alpha05_cannot_reject_any_assignment":True,
        "entire_20_assignment_enumeration_exact_vs_independent_finite_variance":True,
        "finite_pop_neyman_variance_and_observable_estimator_both_checked":True,
        "assumption_interference_world_excluded_from_SUTVA_inference":True,
        "new_real_human_E2":0,
        "new_real_historical_E3":0,
        "worlds":summaries,
    },rows


def emit():
    result,records=compute()
    result_file=OUT/"R210_EXACT_RESULTS.json"
    csv_file=OUT/"R210_ALL_140_COMPLETE_RANDOM_ASSIGNMENT_SOURCES.csv"
    result_file.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    with csv_file.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    rec={
        "model_id":"R210","catalogue_id":"09-001","SUTVA_true_worlds":6,
        "counterexample_interference_worlds":1,
        "balanced_complete_assignments_per_world":20,
        "complete_original_assignment_source_records":140,
        "all_Neyman_formula_and_six_SUTVA_randomized_variances_exact":True,
        "true_sharp_null_Fisher_two_sided_size_exact":True,
        "interference_expected_contamination_checked":"7/5",
        "new_E2":0,"new_E3":0,
        "results_sha256":hashlib.sha256(result_file.read_bytes()).hexdigest(),
        "all_original_assignments_sha256":hashlib.sha256(csv_file.read_bytes()).hexdigest(),
    }
    (OUT/"R210_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(rec,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(rec,indent=2))


class Tests(unittest.TestCase):
    def test_original_20_treat_assignments(self):
        self.assertEqual(len(ALL_ASSIGNMENTS),20)
    def test_six_SUTVA_worlds(self):
        self.assertEqual(len(SUTVA_WORLDS),6)
    def test_seven_worlds_total(self):
        self.assertEqual(len(SUTVA_WORLDS)+1,7)
    def test_140_original_assignment_sources(self):
        self.assertEqual((len(SUTVA_WORLDS)+1)*len(ALL_ASSIGNMENTS),140)
    def test_all_treated_three_unique(self):
        self.assertTrue(all(len(set(a))==3 for a in ALL_ASSIGNMENTS))
    def test_all_treatment_masks_sum_three(self):
        self.assertTrue(all(sum(assignment_vector(a))==3 for a in ALL_ASSIGNMENTS))
    def test_all_assignments_unique(self):
        self.assertEqual(len(set(ALL_ASSIGNMENTS)),20)
    def test_all_assignment_source_weights_one(self):
        self.assertEqual(sum((source_assignment_prob(a) for a in ALL_ASSIGNMENTS),Z),O)
    def test_each_unit_treated_probability_half(self):
        for i in range(N):
            self.assertEqual(F(sum(i in a for a in ALL_ASSIGNMENTS),20),F(1,2))
    def test_peer_exposure_treated_conditional(self):
        a=tuple(
            F(sum((assignment_vector(t)[i^1] for i in range(N) if assignment_vector(t)[i])),3)
            for t in ALL_ASSIGNMENTS)
        self.assertEqual(average(a),F(2,5))
    def test_peer_exposure_control_conditional(self):
        a=tuple(
            F(sum((assignment_vector(t)[i^1] for i in range(N) if not assignment_vector(t)[i])),3)
            for t in ALL_ASSIGNMENTS)
        self.assertEqual(average(a),F(3,5))
    def test_potential_outcomes_correct_constant_effect(self):
        y0,y1=fixed_potential_outcomes("RAMP_CONST_TWO")
        self.assertTrue(all(y1[i]-y0[i]==2 for i in range(N)))
    def test_potential_outcomes_nonnegative_null(self):
        y0,y1=fixed_potential_outcomes("RAMP_NULL")
        self.assertEqual(y0,y1)
    def test_heterogeneous_zero_ATE(self):
        self.assertEqual(analytic_neyman_components("RAMP_ZERO_ATE_HET")["population_ATE"],Z)
    def test_hetero_single_ATE(self):
        self.assertEqual(analytic_neyman_components("RAMP_SINGLE_HET")["population_ATE"],O)
    def test_outlier_ATE(self):
        self.assertEqual(analytic_neyman_components("OUTLIER_HET")["population_ATE"],F(5,2))
    def test_finite_variance_ramp_sample(self):
        self.assertEqual(pop_var_sample_denominator(tuple(map(F,RAMP))),F(7,2))
    def test_const_effect_var_tau_zero(self):
        self.assertEqual(analytic_neyman_components("RAMP_CONST_TWO")["finite_pop_stau_squared"],Z)
    def test_single_hetero_var_tau_positive(self):
        self.assertGreater(analytic_neyman_components("RAMP_SINGLE_HET")["finite_pop_stau_squared"],Z)
    def test_ramp_null_exact_randomization_variance(self):
        self.assertEqual(analytic_neyman_components("RAMP_NULL")["true_randomization_variance"],F(7,3))
    def test_sharp_null_p_two_sided_min_tenth(self):
        for t in ALL_ASSIGNMENTS:
            o=observed_sutva("RAMP_NULL",t)
            self.assertGreaterEqual(fisher_sharp_zero_p_value(o,t),F(1,10))
    def test_sharp_null_observations_permuted_fixed(self):
        t=ALL_ASSIGNMENTS[0]
        y=observed("RAMP_NULL",t)
        self.assertEqual(y,tuple(map(F,RAMP)))
    def test_complements_never_same(self):
        self.assertTrue(all(set(t).isdisjoint(complement_treated(t)) for t in ALL_ASSIGNMENTS))
    def test_complements_sign_reversal_under_null(self):
        y=tuple(map(F,RAMP))
        self.assertTrue(all(diff_in_means(y,t)==-diff_in_means(y,complement_treated(t))
                            for t in ALL_ASSIGNMENTS))
    def test_randomized_estimator_centered_under_null(self):
        values=[diff_in_means(observed("RAMP_NULL",t),t) for t in ALL_ASSIGNMENTS]
        self.assertEqual(average(values),Z)
    def test_randomized_estimator_centered_at_constant_effect(self):
        values=[diff_in_means(observed("RAMP_CONST_TWO",t),t) for t in ALL_ASSIGNMENTS]
        self.assertEqual(average(values),F(2))
    def test_nuisance_outlier_null_sample_variance_positive(self):
        y=observed("OUTLIER_NULL",ALL_ASSIGNMENTS[0])
        self.assertGreater(observable_neyman_variance(y,ALL_ASSIGNMENTS[0]),0)
    def test_interference_peer_formula(self):
        expected=analytic_interference_bias()
        self.assertEqual(expected["expected_observed_difference_from_assignment_formula"],F(7,5))
    def test_interference_own_direct_fixed_peers_two(self):
        z=list(assignment_vector(ALL_ASSIGNMENTS[0]))
        for i in range(N):
            z0=z.copy();z0[i]=0
            z1=z.copy();z1[i]=1
            f=lambda x:F(i+2*x[i]+3*x[i^1])
            self.assertEqual(f(z1)-f(z0),2)
    def test_interference_not_a_single_world_potential_outcome_vector(self):
        # Keeping own assignment fixed but switching peer changes true outcome.
        z=(0,0,0,0,0,0)
        za=(0,1,0,0,0,0)
        self.assertEqual(F(0+2*z[0]+3*z[1]),0)
        self.assertEqual(F(0+2*za[0]+3*za[1]),3)
    def test_invalid_assignment_fewer_treated(self):
        with self.assertRaises(ValueError):
            assignment_vector((0,1))
    def test_invalid_assignment_duplicate(self):
        with self.assertRaises(ValueError):
            assignment_vector((1,1,2))
    def test_invalid_unknown_SUTVA_world(self):
        with self.assertRaises(ValueError):
            fixed_potential_outcomes("UNKNOWN")
    def test_pop_variance_reject_single(self):
        with self.assertRaises(ValueError):
            pop_var_sample_denominator((O,))
    def test_complete_source_results(self):
        r,rows=compute()
        self.assertEqual((len(r["worlds"]),len(rows)),(7,140))
        self.assertEqual(r["original_239_catalogue_id"],"09-001")
        self.assertEqual(r["new_real_human_E2"],0)
        self.assertEqual(r["new_real_historical_E3"],0)
    def test_all_no_interference_expected_bias_zero(self):
        r,_=compute()
        for w in r["worlds"]:
            if w["SUTVA_no_interference"]:
                self.assertEqual(w["actual_expected_difference_in_means_exact"],w["population_ATE"])
    def test_all_worlds_exact_source_normalized(self):
        r,rows=compute()
        self.assertTrue(all(w["source_random_assignment_probability_sum"]=="1" for w in r["worlds"]))
        self.assertTrue(all(row["original_random_assignment_probability"]=="1/20" for row in rows))
    def test_interference_diff_mean_not_direct_two(self):
        r,_=compute()
        w=next(x for x in r["worlds"] if x["world"]==INTERFERENCE_NAME)
        self.assertEqual(w["actual_expected_difference_in_means_exact"],"7/5")
        self.assertEqual(w["finite_Neyman_no_interference_variance_formula"],"NOT_DEFINED_UNDER_INTERFERENCE")
        self.assertEqual(w["Fisher_sharp_null_p_value"],"NOT_VALID_UNDER_INTERFERENCE")
    def test_true_sharp_null_both_levels_exact(self):
        r,_=compute()
        for w in r["worlds"]:
            if w["world"] in ("RAMP_NULL","OUTLIER_NULL"):
                self.assertEqual(w["rejection_rate_two_sided_alpha_0_05"],"0")
                self.assertLessEqual(F(w["rejection_rate_two_sided_alpha_0_10"]),F(1,10))
    def test_complete_deterministic_replay(self):
        self.assertEqual(compute(),compute())

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--test",action="store_true")
    ap.add_argument("--emit",action="store_true")
    a=ap.parse_args()
    if a.test:
        ok=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if ok.wasSuccessful() else 1)
    if a.emit:
        emit()
    if not a.test and not a.emit:
        ap.print_help()
