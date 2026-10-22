#!/usr/bin/env python3
"""R218 propensity-score exact X-stratum many-to-many matching audit.

All 8 fixed synthetic units, 6 frozen assignment worlds (101 exact original
treatment allocations in total). Distinguish observed e(X) from privileged
unit-level inclusion p_i depending on unobserved U. Enumerate all assignments
with exact Fraction source probabilities; compare naive difference, exact
observed X/e(X) stratum matching, and privileged true-inclusion HT. Preserve
no-support outcomes as null (NOT a fake zero estimate).

No human, real observational, or historical evidence. The matching estimator
here is full within-X pairing + fixed stratum reweighting, NOT nearest-neighbor.
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
Z = F(0)
O = F(1)
N=8
UNITS=tuple(range(N))
WORLDS=(
    "RANDOM_X_CONFOUNDED",
    "HIDDEN_U_BIASED",
    "HIDDEN_ASSIGNMENT_NEG_CONTROL",
    "HETEROGENEOUS_EFFECT_X",
    "BALANCED_QUOTA_NEG_CONTROL",
    "POSITIVITY_FAILURE",
)
X=tuple(0 if i<4 else 1 for i in UNITS)
U=(0,0,1,1,0,0,1,1)
STRATA={0:tuple(range(4)),1:tuple(range(4,8))}
OUT=Path(__file__).resolve().parent


def check_world(world):
    if world not in WORLDS:
        raise ValueError("world outside frozen propensity source set")


def treatment_quota(world):
    check_world(world)
    if world=="BALANCED_QUOTA_NEG_CONTROL":
        return (2,2)
    if world=="POSITIVITY_FAILURE":
        return (0,4)
    return (1,3)


def weighted_by_hidden_U(world):
    return world in ("HIDDEN_U_BIASED","HIDDEN_ASSIGNMENT_NEG_CONTROL")


def potential_outcomes(world):
    check_world(world)
    useU=world in ("HIDDEN_U_BIASED","BALANCED_QUOTA_NEG_CONTROL")
    y0=tuple(F(2*X[i]+(3*U[i] if useU else 0)) for i in UNITS)
    tau=tuple(F(1+2*X[i]) if world=="HETEROGENEOUS_EFFECT_X"
              else F(2) for i in UNITS)
    y1=tuple(y0[i]+tau[i] for i in UNITS)
    return y0,y1


def true_ATE(world):
    y0,y1=potential_outcomes(world)
    return sum((y1[i]-y0[i] for i in UNITS),Z)/8


def stratum_subsets(x,k):
    if x not in STRATA or not (0<=k<=4):
        raise ValueError("invalid quota")
    return tuple(itertools.combinations(STRATA[x],k))


def assignment_probabilities(world):
    """One true assignment source probability for every exact allowed assignment."""
    k0,k1=treatment_quota(world)
    probabilities=[]
    strata_sources={}
    for x,k in ((0,k0),(1,k1)):
        opts=stratum_subsets(x,k)
        scores=tuple(F(3)**sum(U[i] for i in s) if weighted_by_hidden_U(world)
                     else O for s in opts)
        denom=sum(scores,Z)
        if denom<=0:
            raise AssertionError("nonpositive source probabilities")
        strata_sources[x]=tuple((set(opt),scores[i]/denom)
                                for i,opt in enumerate(opts))
    for s0,p0 in strata_sources[0]:
        for s1,p1 in strata_sources[1]:
            combined=tuple(sorted(s0|s1))
            if len(combined)!=4:
                raise AssertionError("four treated units across the two strata")
            probabilities.append((combined,p0*p1))
    if sum((p for a,p in probabilities),Z)!=O:
        raise AssertionError("all source assignment probabilities must sum to one")
    return tuple(probabilities)


def individual_true_inclusion_probs(source):
    p=[Z]*N
    for treatment,weight in source:
        for i in treatment:
            p[i]+=weight
    return tuple(p)


def observed_outcomes(world,treated):
    if len(treated)!=4 or len(set(treated))!=4:
        raise ValueError("must assign exactly four treated")
    y0,y1=potential_outcomes(world)
    assignment=set(treated)
    return tuple(y1[i] if i in assignment else y0[i] for i in UNITS)


def fraction_average(values):
    if not values:
        raise ValueError("empty observed treatment/control stratum")
    return sum((F(v) for v in values),Z)/len(values)


def observed_only_naive(treated,observed):
    if len(observed)!=8:
        raise ValueError("eight actually observed outcomes")
    t=set(treated)
    return fraction_average([observed[i] for i in UNITS if i in t])-fraction_average(
        [observed[i] for i in UNITS if i not in t])


def observed_only_exact_X_matching(world,treated,observed):
    """Complete WITH-REPLACEMENT many-to-many matching inside each observed X.

    Uses actual observed X only. Population X-strata reweighted 1/2 each.
    If e(X) values coincide, this is a FINER observed-X match, not something
    derived solely from scalar propensity equality.
    """
    quota=treatment_quota(world)
    if any(k in (0,4) for k in quota):
        return None
    treatment=set(treated)
    diff=Z
    for x in (0,1):
        treated_outcomes=[observed[i] for i in STRATA[x] if i in treatment]
        untreated_outcomes=[observed[i] for i in STRATA[x] if i not in treatment]
        if len(treated_outcomes)!=quota[x] or len(untreated_outcomes)!=4-quota[x]:
            raise AssertionError("assignment did not respect stratum treatment quota")
        diff+=(fraction_average(treated_outcomes)-fraction_average(untreated_outcomes))/2
    return diff


def true_inclusion_HT_oracle(world,treated,observed,inclusion):
    """Uses TRUE UNIT-specific p_i, possibly dependent on unobserved U.

    Never advertise as an observed-X-only matching estimator.
    """
    if any(not (Z<p<O) for p in inclusion):
        return None
    selected=set(treated)
    y_term=sum((
        observed[i]/inclusion[i] if i in selected
        else -observed[i]/(O-inclusion[i]) for i in UNITS),Z)
    return y_term/8


def independent_expectations_via_inclusion(world,inclusion):
    """Identity with no access to realized empirical assignment estimates."""
    y0,y1=potential_outcomes(world)
    k0,k1=treatment_quota(world)
    naive=sum((inclusion[i]*y1[i]-(O-inclusion[i])*y0[i] for i in UNITS),Z)/4
    matched=None
    if 0<k0<4 and 0<k1<4:
        matched=Z
        for x,k in ((0,k0),(1,k1)):
            treated_mean=sum((inclusion[i]*y1[i] for i in STRATA[x]),Z)/k
            untreated_mean=sum(((O-inclusion[i])*y0[i] for i in STRATA[x]),Z)/(4-k)
            matched+=(treated_mean-untreated_mean)/2
    return naive,matched


def weighted_moments(values):
    """values: (estimator, probability) with total probability one."""
    if not values:
        return None
    mass=sum((weight for val,weight in values),Z)
    if mass!=O:
        raise AssertionError("source probability did not normalize")
    mean=sum((v*p for v,p in values),Z)
    variance=sum((p*(v-mean)**2 for v,p in values),Z)
    return mean,variance


def compute():
    rows=[]
    worlds=[]
    total=0
    for world in WORLDS:
        source=assignment_probabilities(world)
        p=individual_true_inclusion_probs(source)
        y0,y1=potential_outcomes(world)
        oracle_ate=true_ATE(world)
        if oracle_ate!=2:
            raise AssertionError("all six source worlds expected finite ATE2")
        if any(sum(p[i] for i in STRATA[x])/4!=F(treatment_quota(world)[x],4)
               for x in (0,1)):
            raise AssertionError("observed propensity X group is not the frozen quota")
        vals_naive=[]
        vals_match=[]
        vals_HT=[]
        for assignment,prob in source:
            obs=observed_outcomes(world,assignment)
            estimate_naive=observed_only_naive(assignment,obs)
            estimate_match=observed_only_exact_X_matching(world,assignment,obs)
            estimate_HT=true_inclusion_HT_oracle(world,assignment,obs,p)
            vals_naive.append((estimate_naive,prob))
            if estimate_match is not None:
                vals_match.append((estimate_match,prob))
            if estimate_HT is not None:
                vals_HT.append((estimate_HT,prob))
            rows.append({
                "world":world,
                "original_8_unit_treatment_assignment":"|".join(str(int(i in assignment)) for i in UNITS),
                "original_assignment_true_probability_exact":str(prob),
                "observed_8_X":"|".join(map(str,X)),
                "hidden_8_U_ORACLE_ONLY":"|".join(map(str,U)),
                "true_8_individual_Y0_ORACLE_ONLY":"|".join(map(str,y0)),
                "true_8_individual_Y1_ORACLE_ONLY":"|".join(map(str,y1)),
                "observed_only_actual_8_outcomes":"|".join(map(str,obs)),
                "true_oracle_finite_ATE":"2",
                "public_X0_X1_stratum_treatment_quotas":"|".join(map(str,treatment_quota(world))),
                "observable_e_X0_e_X1":"|".join(str(F(k,4)) for k in treatment_quota(world)),
                "true_8_individual_inclusion_probabilities_PRIVILEGED":"|".join(map(str,p)),
                "naive_unmatched_observed_difference_exact":str(estimate_naive),
                "observed_X_complete_matching_estimator_exact":
                    str(estimate_match) if estimate_match is not None else "",
                "observed_X_complete_matching_status":
                    "OK" if estimate_match is not None else "NOT_IDENTIFIED_NO_COMMON_SUPPORT",
                "privileged_true_inclusion_HT_estimator_exact":
                    str(estimate_HT) if estimate_HT is not None else "",
                "privileged_true_inclusion_HT_status":
                    "ORACLE_ONLY" if estimate_HT is not None else "UNDEFINED_NO_POSITIVITY",
                "naive_squared_error_vs_true_ATE_exact":str((estimate_naive-oracle_ate)**2),
                "observed_X_matching_squared_error_exact":
                    str((estimate_match-oracle_ate)**2) if estimate_match is not None else "",
                "oracle_HT_squared_error_exact":
                    str((estimate_HT-oracle_ate)**2) if estimate_HT is not None else "",
            })
        total+=len(source)
        naive_m,var_naive=weighted_moments(vals_naive)
        matched=weighted_moments(vals_match) if vals_match else None
        ht=weighted_moments(vals_HT) if vals_HT else None
        moment_naive,moment_match=independent_expectations_via_inclusion(world,p)
        if moment_naive!=naive_m or (
            moment_match is None and matched is not None) or (
            moment_match is not None and (matched is None or moment_match!=matched[0])):
            raise AssertionError("full assignment source vs independent unit inclusion means mismatch")
        if ht is not None and ht[0]!=oracle_ate:
            raise AssertionError("true individual inclusion Horvitz-Thompson should be design unbiased")
        if any(k in (0,4) for k in treatment_quota(world)):
            if matched is not None or ht is not None:
                raise AssertionError("unsupported matching/HT must not be output as a numeric estimate")
        worlds.append({
            "world":world,
            "true_artificial_finite_ATE_exact":"2",
            "original_observational_treatment_assignment_histories":len(source),
            "full_assignment_probability_mass_exact":"1",
            "public_X0_X1_propensity_scores_exact":
                "|".join(str(F(k,4)) for k in treatment_quota(world)),
            "true_hidden_U_affects_treatment_selection":weighted_by_hidden_U(world),
            "true_hidden_U_affects_Y0":world in ("HIDDEN_U_BIASED","BALANCED_QUOTA_NEG_CONTROL"),
            "original_assignment_probabilities_nonuniform":len({prob for a,prob in source})>1,
            "naive_unmatched_expectation_exact":str(naive_m),
            "naive_unmatched_bias_exact":str(naive_m-oracle_ate),
            "naive_random_design_variance_exact":str(var_naive),
            "observed_X_matching_expectation_exact":str(matched[0]) if matched else None,
            "observed_X_matching_bias_exact":str(matched[0]-oracle_ate) if matched else None,
            "observed_X_matching_random_design_variance_exact":str(matched[1]) if matched else None,
            "privileged_true_inclusion_HT_expectation_exact":str(ht[0]) if ht else None,
            "privileged_true_inclusion_HT_variance_exact":str(ht[1]) if ht else None,
            "true_individual_inclusion_probs_oracle_only":"|".join(map(str,p)),
            "observed_X_match_status":"VALID_OVERLAP" if matched else "NOT_IDENTIFIED_NO_COMMON_SUPPORT",
            "oracle_HT_status":"VALID_ORACLE" if ht else "UNDEFINED_NO_POSITIVITY",
            "full_source_expectation_equals_independent_unit_inclusion_formula":True,
        })
    if total!=101 or len(rows)!=101 or len(worlds)!=6:
        raise AssertionError("complete 16*4+36+1 original observational histories required")
    return {
        "research_id":"R218",
        "source_catalogue_id":"09-009",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "total_synthetic_units":8,
        "true_design_worlds":6,
        "all_original_treatment_assignment_histories":101,
        "true_population_ATE_in_each_world":"2",
        "fully_observed_baseline_X_has_two_equal_size_strata":True,
        "hidden_U_not_used_by_matching":True,
        "frozen_matching_is_many_to_many_inside_X_stratum":True,
        "propensity_eX_scalar_alone_identifies_X_only_when_scores_distinct":True,
        "failure_of_overlap_returns_null_not_zero":True,
        "dual_fraction_source_vs_inclusion_moment_checks":True,
        "new_real_human_E2":0,
        "new_real_historical_E3":0,
        "worlds":worlds,
        "limits":[
            "Matching is complete with replacement within observed X with fixed population weights; not 1:1 nearest-neighbor caliper",
            "U and true individual propensity are hidden from observed-X matching, but available to privileged oracle audit",
            "Eight fixed artificial units and exactly enumerated assignments, not independent human RCTs",
            "No propensity score estimation, empirical standard error or real observational causal identification",
        ],
    },rows


def emit():
    result,raw=compute()
    result_path=OUT/"R218_EXACT_RESULTS.json"
    raw_path=OUT/"R218_ALL_101_ORIGINAL_PROPENSITY_ASSIGNMENT_SOURCES.csv"
    result_path.write_text(
        json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    with raw_path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(raw[0]))
        writer.writeheader()
        writer.writerows(raw)
    receipt={
        "research_id":"R218",
        "actual_239_catalogue_id":"09-009",
        "worlds":6,
        "full_original_assignment_source_rows":101,
        "observed_X_matched_outcome_only_no_hidden_U":True,
        "independent_unit_inclusion_expected_estimators_match_all_source_means":True,
        "privileged_HT_unbiased_when_full_unit_level_positivity":True,
        "zero_propensity_returns_null_not_fabricated_estimates":True,
        "new_E2":0,"new_E3":0,
        "results_sha256":hashlib.sha256(result_path.read_bytes()).hexdigest(),
        "source_sha256":hashlib.sha256(raw_path.read_bytes()).hexdigest(),
    }
    (OUT/"R218_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(receipt,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2))


class Tests(unittest.TestCase):
    def test_six_worlds(self): self.assertEqual(len(WORLDS),6)
    def test_eight_people(self): self.assertEqual(len(UNITS),8)
    def test_observed_X_four_each(self): self.assertEqual(X.count(0),4);self.assertEqual(X.count(1),4)
    def test_hidden_U_two_each_stratum(self):
        for x in (0,1): self.assertEqual(sum(U[i] for i in STRATA[x]),2)
    def test_true_ATE_all_two(self):
        for w in WORLDS: self.assertEqual(true_ATE(w),F(2))
    def test_quota_sums_four(self):
        for w in WORLDS: self.assertEqual(sum(treatment_quota(w)),4)
    def test_uniform_16_assignments(self):
        self.assertEqual(len(assignment_probabilities("RANDOM_X_CONFOUNDED")),16)
    def test_hidden_weighted_16_assignments(self):
        self.assertEqual(len(assignment_probabilities("HIDDEN_U_BIASED")),16)
    def test_balanced_36_assignments(self):
        self.assertEqual(len(assignment_probabilities("BALANCED_QUOTA_NEG_CONTROL")),36)
    def test_zero_overlap_one_assignment(self):
        self.assertEqual(len(assignment_probabilities("POSITIVITY_FAILURE")),1)
    def test_exact_all_assignment_count(self):
        self.assertEqual(sum(len(assignment_probabilities(w)) for w in WORLDS),101)
    def test_all_world_probability_mass_one(self):
        for w in WORLDS: self.assertEqual(sum((p for t,p in assignment_probabilities(w)),Z),O)
    def test_true_eX_quota(self):
        for w in WORLDS:
            inc=individual_true_inclusion_probs(assignment_probabilities(w))
            self.assertEqual(tuple(sum(inc[i] for i in STRATA[x])/4 for x in (0,1)),
                             tuple(F(k,4) for k in treatment_quota(w)))
    def test_uniform_assignment_source_probability(self):
        self.assertEqual(set(p for a,p in assignment_probabilities("RANDOM_X_CONFOUNDED")),{F(1,16)})
    def test_balanced_uniform_probability(self):
        self.assertEqual(set(p for a,p in assignment_probabilities("BALANCED_QUOTA_NEG_CONTROL")),{F(1,36)})
    def test_hidden_assignment_probabilities_not_uniform(self):
        self.assertGreater(len({p for a,p in assignment_probabilities("HIDDEN_U_BIASED")}),1)
    def test_balanced_total_match_equals_naive_per_assignment(self):
        w="BALANCED_QUOTA_NEG_CONTROL"
        for a,p in assignment_probabilities(w):
            obs=observed_outcomes(w,a)
            self.assertEqual(observed_only_naive(a,obs),observed_only_exact_X_matching(w,a,obs))
    def test_all_positive_support_or_valid_null(self):
        for w in WORLDS:
            inc=individual_true_inclusion_probs(assignment_probabilities(w))
            if w=="POSITIVITY_FAILURE":
                self.assertTrue(any(i in (0,1) for i in inc))
            else:
                self.assertTrue(all(Z<i<O for i in inc))
    def test_world_random_X_matched_expectation_two(self):
        w="RANDOM_X_CONFOUNDED"
        p=individual_true_inclusion_probs(assignment_probabilities(w))
        self.assertEqual(independent_expectations_via_inclusion(w,p),(F(3),F(2)))
    def test_world_hidden_X_matching_bias(self):
        w="HIDDEN_U_BIASED"
        p=individual_true_inclusion_probs(assignment_probabilities(w))
        self.assertEqual(independent_expectations_via_inclusion(w,p),(F(15,4),F(3)))
    def test_hidden_U_assignment_neg_control_matching_unbiased(self):
        w="HIDDEN_ASSIGNMENT_NEG_CONTROL"
        p=individual_true_inclusion_probs(assignment_probabilities(w))
        self.assertEqual(independent_expectations_via_inclusion(w,p)[1],F(2))
    def test_heterogeneous_outcome_matching_ATE(self):
        w="HETEROGENEOUS_EFFECT_X"
        p=individual_true_inclusion_probs(assignment_probabilities(w))
        self.assertEqual(independent_expectations_via_inclusion(w,p)[1],F(2))
    def test_positivity_failure_status_none(self):
        w="POSITIVITY_FAILURE"
        a,_=assignment_probabilities(w)[0]
        obs=observed_outcomes(w,a)
        self.assertIsNone(observed_only_exact_X_matching(w,a,obs))
    def test_positivity_failure_oracle_HT_none(self):
        w="POSITIVITY_FAILURE"
        a,_=assignment_probabilities(w)[0]
        p=individual_true_inclusion_probs(assignment_probabilities(w))
        self.assertIsNone(true_inclusion_HT_oracle(w,a,observed_outcomes(w,a),p))
    def test_positivity_failure_naive_four(self):
        w="POSITIVITY_FAILURE"
        a,_=assignment_probabilities(w)[0]
        self.assertEqual(observed_only_naive(a,observed_outcomes(w,a)),F(4))
    def test_oracle_true_inclusion_HT_design_unbiased_all_valid_worlds(self):
        for w in WORLDS[:-1]:
            source=assignment_probabilities(w)
            inc=individual_true_inclusion_probs(source)
            self.assertEqual(sum((p*true_inclusion_HT_oracle(w,a,observed_outcomes(w,a),inc)
                                  for a,p in source),Z),F(2))
    def test_random_subset_complement_size_four(self):
        for w in WORLDS:
            for a,p in assignment_probabilities(w):
                self.assertEqual(len(a),4)
    def test_true_outcomes_binary_U_effect(self):
        y0,y1=potential_outcomes("HIDDEN_U_BIASED")
        self.assertEqual(y0[2]-y0[0],F(3))
    def test_observed_matches_one_potential(self):
        for w in WORLDS:
            a,p=assignment_probabilities(w)[0]
            y0,y1=potential_outcomes(w)
            observed=observed_outcomes(w,a)
            self.assertTrue(all(observed[i]==(y1[i] if i in a else y0[i]) for i in UNITS))
    def test_invalid_world_rejected(self):
        with self.assertRaises(ValueError): treatment_quota("UNKNOWN")
    def test_invalid_treated_rejected(self):
        with self.assertRaises(ValueError): observed_outcomes("RANDOM_X_CONFOUNDED",(0,1))
    def test_invalid_stratum_rejected(self):
        with self.assertRaises(ValueError): stratum_subsets(3,2)
    def test_source_vs_inclusion_world_summary(self):
        r,rows=compute()
        self.assertEqual((len(r["worlds"]),len(rows)),(6,101))
        self.assertEqual(r["new_real_human_E2"],0)
        self.assertIsNone(next(x for x in r["worlds"] if x["world"]=="POSITIVITY_FAILURE")["observed_X_matching_expectation_exact"])
    def test_deterministic_source_replay(self):
        self.assertEqual(assignment_probabilities("HIDDEN_U_BIASED"),
                         assignment_probabilities("HIDDEN_U_BIASED"))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--test",action="store_true")
    ap.add_argument("--emit",action="store_true")
    args=ap.parse_args()
    if args.test:
        test=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if test.wasSuccessful() else 1)
    if args.emit:
        emit()
    if not args.test and not args.emit:
        ap.print_help()
