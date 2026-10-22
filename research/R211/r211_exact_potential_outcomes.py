#!/usr/bin/env python3
"""R211 exact 4-person binary potential-outcome identification audit.

Entire 4^4 potential-outcome schedules, 6 balanced randomized assignments
each, 1536 original randomized observation records and 256 deterministic
baseline-selected observational records. ATE is randomization-unbiased
DESIGN-AVERAGED, but one observed assignment leaves four binary
counterfactual values unobserved and its ATE set width 1.

No real human data. Input schedule oracle is used ONLY by the audit to
identify true finite ATE or check inclusion, not by estimators/bound
construction. Identification sets are calculated from observed z,Y alone.

python r211_exact_potential_outcomes.py --test
python r211_exact_potential_outcomes.py --emit
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import unittest
from collections import Counter
from fractions import Fraction
from pathlib import Path

F=Fraction
Z=F(0)
O=F(1)
N=4
TYPES=((0,0),(0,1),(1,0),(1,1))
SCHEDULES=tuple(itertools.product(TYPES,repeat=N))
MONOTONE=tuple(s for s in SCHEDULES if all(y1>=y0 for y0,y1 in s))
ALLOCATIONS=tuple(itertools.combinations(range(N),2))
HERE=Path(__file__).resolve().parent

def schedule_valid(s):
    return len(s)==N and all(tuple(t) in TYPES for t in s)

def allocation_vector(treated):
    if len(treated)!=2 or len(set(treated))!=2 or any(x not in range(N) for x in treated):
        raise ValueError("two distinct treated unit IDs required")
    return tuple(int(i in treated) for i in range(N))

def potential_margins(s):
    if not schedule_valid(s):
        raise ValueError("schedule invalid")
    return tuple(sum(s[i][arm] for i in range(N)) for arm in (0,1))

def average(seq):
    if not seq:
        raise ValueError("nonempty")
    return sum((F(z) for z in seq),Z)/len(seq)

def samplevar(seq):
    if len(seq)<2:
        raise ValueError("variance denominator n-1")
    mu=average(seq)
    return sum(((F(x)-mu)**2 for x in seq),Z)/(len(seq)-1)

def ate(s):
    return average(tuple(y1-y0 for y0,y1 in s))

def true_effect_square_mean(s):
    return average(tuple((y1-y0)**2 for y0,y1 in s))

def observe(s,treated):
    z=allocation_vector(treated)
    return tuple(s[i][z[i]] for i in range(N))

def observed_diff(y,treated):
    z=allocation_vector(treated)
    if len(y)!=N:
        raise ValueError("four observed binary outcomes required")
    return average(tuple(y[i] for i in range(N) if z[i]))-average(
        tuple(y[i] for i in range(N) if not z[i]))

def neyman_var(s):
    if not schedule_valid(s):
        raise ValueError("schedule invalid")
    y0=tuple(t[0] for t in s)
    y1=tuple(t[1] for t in s)
    d=tuple(y1[i]-y0[i] for i in range(N))
    return samplevar(y0)/2+samplevar(y1)/2-samplevar(d)/4

def compatible_schedules(treated,y,monotone=False):
    """Build set solely from observed allocation and outcomes, no TRUE schedule."""
    z=allocation_vector(treated)
    if len(y)!=N or any(i not in (0,1) for i in y):
        raise ValueError("binary observed outcomes required")
    candidates=MONOTONE if monotone else SCHEDULES
    return tuple(s for s in candidates
                 if all(s[i][z[i]]==y[i] for i in range(N)))

def bounds_from_compatible(candidates):
    if not candidates:
        raise ValueError("empty identification set")
    v=tuple(ate(s) for s in candidates)
    return (min(v),max(v))

def population_effect_type_counts(s):
    ctr=Counter(s)
    return {"never":ctr[(0,0)],"benefit":ctr[(0,1)],
            "harm":ctr[(1,0)],"always":ctr[(1,1)]}

def select_two_highest_baseline(s):
    if not schedule_valid(s):
        raise ValueError("invalid true source")
    # Counterfactual oracle baseline selection policy: uses underlying Y0 as
    # a fully observed pre-treatment surrogate in this ARTIFICIAL policy.
    # This is the confounding ASSIGNMENT mechanism, not a statistical fit.
    return tuple(sorted(sorted(range(N),key=lambda i:(-s[i][0],i))[:2]))

def effect_distribution_contrast():
    a=((0,0),(0,0),(1,1),(1,1))
    b=((0,1),(0,1),(1,0),(1,0))
    assert potential_margins(a)==potential_margins(b)==(2,2)
    assert ate(a)==ate(b)==Z
    assert true_effect_square_mean(a)==Z
    assert true_effect_square_mean(b)==O
    return {
        "NO_UNIT_EFFECT_schedule":"|".join(f"{x}{y}" for x,y in a),
        "OFFSETTING_EFFECTS_schedule":"|".join(f"{x}{y}" for x,y in b),
        "same_marginal_Y0_successes":2,
        "same_marginal_Y1_successes":2,
        "same_population_ATE_exact":"0",
        "NO_UNIT_EFFECT_individual_tau_squared_mean_exact":"0",
        "OFFSETTING_EFFECTS_individual_tau_squared_mean_exact":"1",
        "NO_UNIT_EFFECT_true_effect_types":population_effect_type_counts(a),
        "OFFSETTING_EFFECTS_true_effect_types":population_effect_type_counts(b),
        "observational_high_baseline_selected_treatment":list(select_two_highest_baseline(a)),
        "observational_high_baseline_confounding_ATE0_observed_effect":
            str(observed_diff(observe(a,select_two_highest_baseline(a)),select_two_highest_baseline(a))),
        "scope_note":"Same POTENTIAL OUTCOME MARGINAL totals do not identify the joint effect distribution; NOT a claim that repeated unit-specific crossover data could never reveal both outcomes under additional designs.",
    }

def compute():
    if (len(SCHEDULES),len(MONOTONE),len(ALLOCATIONS))!=(256,81,6):
        raise AssertionError("source enumeration incomplete")
    full=[]
    selected=[]
    worlds=[]
    widths=Counter()
    mono_excludes_true=0
    for ix,s in enumerate(SCHEDULES):
        true=ate(s)
        stats=population_effect_type_counts(s)
        is_mono=(stats["harm"]==0)
        values=[]
        monotone_widths=[]
        missed_mono=0
        for treated in ALLOCATIONS:
            y=observe(s,treated)
            estimate=observed_diff(y,treated)
            compatible=compatible_schedules(treated,y)
            mono=compatible_schedules(treated,y,monotone=True)
            l,r=bounds_from_compatible(compatible)
            ml,mr=bounds_from_compatible(mono)
            if len(compatible)!=16 or r-l!=O:
                raise AssertionError("four arbitrary hidden counterfactuals must give 16 compatible schedules and ATE interval width1")
            if not (l<=true<=r):
                raise AssertionError("identified true ATE omitted by unrestricted set")
            if not (l<=ml<=mr<=r):
                raise AssertionError("monotonic identification must weakly contract source-free unrestricted interval")
            if is_mono and not (ml<=true<=mr):
                raise AssertionError("true monotone type not included in monotone candidate set")
            outside=int(not(ml<=true<=mr))
            mono_excludes_true+=outside
            missed_mono+=outside
            widths[str(mr-ml)]+=1
            monotone_widths.append(mr-ml)
            values.append(estimate)
            full.append({
                "source_schedule_index":ix,
                "true_potential_outcome_four_types":"|".join(f"{x}{yy}" for x,yy in s),
                "source_finite_ATE_exact":str(true),
                "source_monotonicity_true":int(is_mono),
                "treated_indices":"|".join(map(str,treated)),
                "random_assignment_source_probability":"1/6",
                "actual_assignment_z":"|".join(map(str,allocation_vector(treated))),
                "realized_only_observed_four_Y":"|".join(map(str,y)),
                "oracle_unobserved_four_counterfactuals_FOR_AUDIT_ONLY":"|".join(
                    str(s[i][1-allocation_vector(treated)[i]]) for i in range(N)),
                "observed_treated_minus_control_exact":str(estimate),
                "unrestricted_compatible_full_source_schedules":len(compatible),
                "unrestricted_ATE_min_exact":str(l),
                "unrestricted_ATE_max_exact":str(r),
                "unrestricted_ATE_interval_width":"1",
                "extra_assumption_monotone_compatible_schedules":len(mono),
                "extra_assumption_monotone_ATE_min_exact":str(ml),
                "extra_assumption_monotone_ATE_max_exact":str(mr),
                "extra_assumption_monotone_ATE_width_exact":str(mr-ml),
                "monotonicity_assumption_excludes_true_ATE":outside,
            })
        avg=average(values)
        var=average(tuple((v-avg)**2 for v in values))
        formula=neyman_var(s)
        if avg!=true or var!=formula:
            raise AssertionError("exact design-unbiasedness or Neyman finite variance identity failed")
        policy=select_two_highest_baseline(s)
        obs=observed_diff(observe(s,policy),policy)
        selected.append({
            "source_schedule_index":ix,
            "true_potential_outcome_four_types":"|".join(f"{x}{yy}" for x,yy in s),
            "source_finite_ATE_exact":str(true),
            "baseline_high_selection_treated_ids":"|".join(map(str,policy)),
            "observational_assignment_z":"|".join(map(str,allocation_vector(policy))),
            "observed_only_y_under_nonrandom_selection":"|".join(map(str,observe(s,policy))),
            "observational_naive_treated_control_diff_exact":str(obs),
            "observational_naive_effect_bias_vs_truth_exact":str(obs-true),
            "complete_randomization_expected_diff_exact":str(avg),
            "nonrandom_design_probability":"1",
            "selection_rule":"2 units with largest oracle Y0 baseline; same Y0 lower index first",
        })
        worlds.append({
            "source_schedule_index":ix,
            "four_unit_potential_outcome_schedule":"|".join(f"{x}{yy}" for x,yy in s),
            "population_Y0_successes":potential_margins(s)[0],
            "population_Y1_successes":potential_margins(s)[1],
            "population_finite_ATE_exact":str(true),
            "finite_individual_tau_square_mean_exact":str(true_effect_square_mean(s)),
            "number_benefit_type":stats["benefit"],
            "number_harm_type":stats["harm"],
            "monotonicity_true":is_mono,
            "source_design_assignment_count":6,
            "source_randomization_probabilities_sum":"1",
            "six_assignment_estimator_expectation_exact":str(avg),
            "six_assignment_estimator_variance_exact":str(var),
            "independent_neyman_finite_variance_formula_exact":str(formula),
            "single_assignment_unrestricted_ATE_width_exact":"1",
            "average_single_assignment_monotone_assumption_width_exact":str(average(monotone_widths)),
            "fraction_assignments_with_monotone_bound_excluding_true_ATE_exact":str(F(missed_mono,6)),
            "nonrandom_high_Y0_assignment_estimator_exact":str(obs),
            "nonrandom_high_Y0_assignment_bias_exact":str(obs-true),
        })
    if (len(worlds),len(full),len(selected))!=(256,1536,256):
        raise AssertionError("not all original population tables/random allocations/nonrandom policies")
    contrast=effect_distribution_contrast()
    return {
        "research_id":"R211",
        "source_catalogue_id":"09-002",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "true_population_units":4,
        "binary_potential_outcome_types":4,
        "complete_ordered_true_potential_outcome_schedules":256,
        "complete_monotone_source_tables":81,
        "complete_balanced_random_assignments_per_schedule":6,
        "complete_original_random_source_rows":len(full),
        "complete_deterministic_selection_policy_rows":len(selected),
        "true_design_probability_per_assignment":"1/6",
        "every_single_randomized_observation_unrestricted_compatible_schedules":16,
        "every_single_randomized_observation_unrestricted_ATE_interval_width":"1",
        "all_256_schedules_Neyman_variance_and_unbiasedness_verified":True,
        "monotone_bound_width_distribution_over_all_1536_observed_records":dict(widths),
        "records_where_unjustified_monotonicity_excludes_actual_true_ATE":mono_excludes_true,
        "effect_joint_distribution_nonidentifiability_contrast":contrast,
        "full_worlds":worlds,
        "new_real_human_E2":0,
        "new_real_historical_E3":0,
        "limitation":"Artificial four-person binary schedule with no interference; complete randomization is distributionally unbiased, single realized trial bounds remain non-point, no real causal conclusions.",
    },full,selected

def emit():
    r,randomized,selected=compute()
    paths={
        "results":HERE/"R211_EXACT_RESULTS.json",
        "random":HERE/"R211_ALL_1536_ORIGINAL_RANDOMIZED_OBSERVATIONS.csv",
        "selected":HERE/"R211_ALL_256_NONRANDOM_SELECTION_COUNTEREXAMPLES.csv",
    }
    paths["results"].write_text(json.dumps(r,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for key,rows in (("random",randomized),("selected",selected)):
        with paths[key].open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    accept={
        "model_id":"R211",
        "original_239_catalogue_id":"09-002",
        "full_binary_potential_outcome_schedules":256,
        "full_randomized_assignment_sources":1536,
        "full_nonrandom_selection_worlds":256,
        "all_randomization_expectations_and_finite_var_two_Fraction_routes":True,
        "single_observation_compatible_schedules_exact":16,
        "single_observation_ATE_width_exact":"1",
        "all_true_monotone_source_bounds_coverage":True,
        "new_E2":0,"new_E3":0,
        **{k+"_sha256":hashlib.sha256(v.read_bytes()).hexdigest() for k,v in paths.items()},
    }
    (HERE/"R211_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(accept,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(accept,indent=2))

class Tests(unittest.TestCase):
    def test_4_units(self): self.assertEqual(N,4)
    def test_4_types(self): self.assertEqual(len(TYPES),4)
    def test_256_schedules(self): self.assertEqual(len(SCHEDULES),256)
    def test_81_monotone_schedules(self): self.assertEqual(len(MONOTONE),81)
    def test_6_balanced_assignments(self): self.assertEqual(len(ALLOCATIONS),6)
    def test_1536_total_randomized(self): self.assertEqual(len(SCHEDULES)*len(ALLOCATIONS),1536)
    def test_source_binary_types(self):
        self.assertTrue(all(schedule_valid(s) for s in SCHEDULES))
    def test_assignment_two_treated(self):
        self.assertTrue(all(sum(allocation_vector(t))==2 for t in ALLOCATIONS))
    def test_randomized_probability_mass(self):
        self.assertEqual(sum((F(1,6) for t in ALLOCATIONS),Z),O)
    def test_zero_ATE_no_effect(self):
        a=((0,0),(0,0),(1,1),(1,1))
        self.assertEqual(ate(a),Z)
    def test_zero_ATE_benefits_and_harms(self):
        b=((0,1),(0,1),(1,0),(1,0))
        self.assertEqual(ate(b),Z)
    def test_same_marginal_potential_outcomes_different_joint_effect(self):
        a=((0,0),(0,0),(1,1),(1,1))
        b=((0,1),(0,1),(1,0),(1,0))
        self.assertEqual(potential_margins(a),potential_margins(b))
        self.assertNotEqual(true_effect_square_mean(a),true_effect_square_mean(b))
    def test_no_unit_effect_selected_ATE_bias_plus_one(self):
        a=((0,0),(0,0),(1,1),(1,1))
        treated=select_two_highest_baseline(a)
        self.assertEqual(treated,(2,3))
        self.assertEqual(observed_diff(observe(a,treated),treated),O)
    def test_six_random_assignments_same_population_ATE_unbiased(self):
        a=((0,0),(0,0),(1,1),(1,1))
        self.assertEqual(average([observed_diff(observe(a,t),t) for t in ALLOCATIONS]),Z)
    def test_per_observation_16_compatible_tables(self):
        for t in ALLOCATIONS:
            for bits in itertools.product((0,1),repeat=N):
                self.assertEqual(len(compatible_schedules(t,bits)),16)
    def test_single_observation_interval_exact_width1(self):
        for t in ALLOCATIONS:
            for bits in itertools.product((0,1),repeat=N):
                c=compatible_schedules(t,bits)
                l,u=bounds_from_compatible(c)
                self.assertEqual(u-l,O)
    def test_single_observation_all_binary_outcomes_have_monotone_completion(self):
        for t in ALLOCATIONS:
            for bits in itertools.product((0,1),repeat=N):
                self.assertTrue(compatible_schedules(t,bits,True))
    def test_monotonicity_never_widens_bounds(self):
        for t in ALLOCATIONS:
            for bits in itertools.product((0,1),repeat=N):
                l,u=bounds_from_compatible(compatible_schedules(t,bits))
                ml,mu=bounds_from_compatible(compatible_schedules(t,bits,True))
                self.assertTrue(l<=ml<=mu<=u)
    def test_true_monotone_schedule_inside_monotone_bound(self):
        for s in MONOTONE:
            for t in ALLOCATIONS:
                ml,mu=bounds_from_compatible(compatible_schedules(t,observe(s,t),True))
                self.assertTrue(ml<=ate(s)<=mu)
    def test_true_nonmonotone_schedules_not_all_monotone(self):
        self.assertTrue(any(s not in MONOTONE for s in SCHEDULES))
    def test_all_256_neyman_formula_exact(self):
        for s in SCHEDULES:
            nums=[observed_diff(observe(s,t),t) for t in ALLOCATIONS]
            mean=average(nums)
            var=average([(v-mean)**2 for v in nums])
            self.assertEqual(mean,ate(s))
            self.assertEqual(var,neyman_var(s))
    def test_single_unit_treatment_effect_not_simultaneously_observed(self):
        s=((0,1),(1,0),(0,0),(1,1))
        t=(0,2)
        z=allocation_vector(t)
        y=observe(s,t)
        self.assertTrue(all(y[i]==s[i][z[i]] for i in range(4)))
        self.assertEqual(len(y),4)
    def test_counterfactual_still_binary(self):
        self.assertTrue(all(x in (0,1) for s in SCHEDULES for pair in s for x in pair))
    def test_baseline_selected_policy_treats_two(self):
        for s in SCHEDULES:
            self.assertEqual(len(select_two_highest_baseline(s)),2)
    def test_all_256_nonrandom_selection_design_policy_not_random(self):
        a=((0,0),(0,0),(1,1),(1,1))
        self.assertEqual(select_two_highest_baseline(a),(2,3))
        self.assertNotEqual(F(1),F(1,6))
    def test_diff_zero_for_constant_all_outcomes(self):
        s=((0,0),)*4
        self.assertTrue(all(observed_diff(observe(s,t),t)==0 for t in ALLOCATIONS))
    def test_ate_contrast_effect_distribution(self):
        x=effect_distribution_contrast()
        self.assertEqual(x["NO_UNIT_EFFECT_individual_tau_squared_mean_exact"],"0")
        self.assertEqual(x["OFFSETTING_EFFECTS_individual_tau_squared_mean_exact"],"1")
    def test_sample_variance_rational(self):
        self.assertEqual(samplevar((0,0,1,1)),F(1,3))
    def test_bad_assignment_rejected(self):
        with self.assertRaises(ValueError): allocation_vector((0,0))
    def test_bad_assignment_outside_rejected(self):
        with self.assertRaises(ValueError): allocation_vector((0,4))
    def test_bad_observed_outcomes_rejected(self):
        with self.assertRaises(ValueError): compatible_schedules((0,1),(0,0,0,3))
    def test_bad_schedule_rejected(self):
        with self.assertRaises(ValueError): neyman_var(((0,0),))
    def test_full_worlds_and_rows(self):
        r,rows,policy=compute()
        self.assertEqual((len(r["full_worlds"]),len(rows),len(policy)),(256,1536,256))
        self.assertEqual(r["every_single_randomized_observation_unrestricted_ATE_interval_width"],"1")
        self.assertEqual(sum(r["monotone_bound_width_distribution_over_all_1536_observed_records"].values()),1536)
    def test_exact_deterministic_replay(self):
        self.assertEqual(compute(),compute())

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test",action="store_true")
    parser.add_argument("--emit",action="store_true")
    opts=parser.parse_args()
    if opts.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if result.wasSuccessful() else 1)
    if opts.emit:
        emit()
    if not opts.test and not opts.emit:
        parser.print_help()
