"""R161 exact finite-size conformist culture Markov chains, 48 frozen worlds."""
from __future__ import annotations

import json
import unittest
from fractions import Fraction as F
from pathlib import Path
from r161_finite_conformist_markov import (
    POPULATIONS, INITIAL_STATES, CONFORMITY, HORIZON,
    unit,checked_n,checked_k,copying_target,binomial_kernel,
    binary_enumerated_kernel,distribution_path_formula,
    distribution_path_enumerated,fixation_probabilities,
    expected_frequency,results_document
)


class TestR161(unittest.TestCase):
    def check_world(self,ni,ki,hi):
        n=POPULATIONS[ni];k=INITIAL_STATES[ni][ki];h=CONFORMITY[hi]
        a=distribution_path_formula(n,k,h)
        b=distribution_path_enumerated(n,k,h)
        self.assertEqual(a,b)
        self.assertEqual(len(a),HORIZON+1)
        self.assertEqual(a[0][k],1)
        P=binomial_kernel(n,h)
        self.assertEqual(a[1],P[k])
        fx=fixation_probabilities(n,h)
        for t,distribution in enumerate(a):
            self.assertEqual(len(distribution),n+1)
            self.assertTrue(all(isinstance(v,F) and v>=0 for v in distribution))
            self.assertEqual(sum(distribution,F(0)),1)
            expected=expected_frequency(distribution,n)
            self.assertTrue(0<=expected<=1)
            if h==0:
                self.assertEqual(expected,F(k,n))
        self.assertTrue(0<=fx[k]<=1)
        if k in (0,n):
            self.assertEqual(a,(a[0],)*(HORIZON+1))
        if h==0:
            self.assertEqual(fx[k],F(k,n))

    def test_frozen_48_scenarios(self):
        self.assertEqual(len(POPULATIONS)*len(CONFORMITY)*6,48)

    def test_all_transition_kernels_exactly_equal(self):
        for n in POPULATIONS:
            for h in CONFORMITY:
                self.assertEqual(binomial_kernel(n,h),binary_enumerated_kernel(n,h))

    def test_kernel_row_stochastic(self):
        for n in POPULATIONS:
            for h in CONFORMITY:
                for row in binomial_kernel(n,h):
                    self.assertTrue(all(0<=x<=1 for x in row))
                    self.assertEqual(sum(row,F(0)),1)

    def test_absorbing_zero_and_full(self):
        for n in POPULATIONS:
            for h in CONFORMITY:
                P=binomial_kernel(n,h)
                self.assertEqual(P[0][0],1)
                self.assertEqual(P[n][n],1)

    def test_interior_states_have_positive_absorption_chance_each_step(self):
        for n in POPULATIONS:
            for h in CONFORMITY:
                P=binomial_kernel(n,h)
                for k in range(1,n):
                    self.assertGreater(P[k][0],0)
                    self.assertGreater(P[k][n],0)

    def test_binomial_expected_count_matches_copying_target(self):
        for n in POPULATIONS:
            for h in CONFORMITY:
                P=binomial_kernel(n,h)
                for k in range(n+1):
                    self.assertEqual(expected_frequency(P[k],n),copying_target(n,k,h))

    def test_majority_copying_function_quarters(self):
        self.assertEqual(copying_target(5,2,1),F(44,125))
        self.assertEqual(copying_target(5,3,1),F(81,125))

    def test_finite_group_mean_gap_expands_under_full_conformity(self):
        self.assertEqual(copying_target(5,3,1)-copying_target(5,2,1),F(37,125))
        self.assertGreater(F(37,125),F(1,5))

    def test_neutral_copying_first_expectation_is_prevalence(self):
        for n in POPULATIONS:
            for k in range(n+1):
                self.assertEqual(copying_target(n,k,0),F(k,n))

    def test_neutral_copying_full_time_martingale_expectation(self):
        for ni,n in enumerate(POPULATIONS):
            for k in INITIAL_STATES[ni]:
                for dist in distribution_path_formula(n,k,0):
                    self.assertEqual(expected_frequency(dist,n),F(k,n))

    def test_neutral_absorption_equals_start_frequency(self):
        for n in POPULATIONS:
            self.assertEqual(fixation_probabilities(n,0),
                             tuple(F(k,n) for k in range(n+1)))

    def test_conformity_drift_relative_to_local_majority(self):
        for n in POPULATIONS:
            for k in range(1,n):
                p=F(k,n)
                for h in CONFORMITY[1:]:
                    q=copying_target(n,k,h)
                    if p<F(1,2): self.assertLess(q,p)
                    if p>F(1,2): self.assertGreater(q,p)

    def test_extreme_minorities_less_likely_to_fix_than_neutral(self):
        u=fixation_probabilities(5,1)
        self.assertLess(u[1],F(1,5))
        self.assertGreater(u[4],F(4,5))

    def test_exact_fixation_harmonic(self):
        for n in POPULATIONS:
            for h in CONFORMITY:
                P=binomial_kernel(n,h)
                u=fixation_probabilities(n,h)
                self.assertEqual(u[0],0)
                self.assertEqual(u[n],1)
                for k in range(1,n):
                    self.assertEqual(u[k],sum((P[k][j]*u[j] for j in range(n+1)),F(0)))

    def test_fixation_probability_mirror_symmetry(self):
        for n in POPULATIONS:
            for h in CONFORMITY:
                u=fixation_probabilities(n,h)
                for k in range(n+1):
                    self.assertEqual(u[k],1-u[n-k])

    def test_transition_mirror_symmetry(self):
        for n in POPULATIONS:
            for h in CONFORMITY:
                T=binomial_kernel(n,h)
                for k in range(n+1):
                    for j in range(n+1):
                        self.assertEqual(T[k][j],T[n-k][n-j])

    def test_finite_neutral_group_stochastically_disperses(self):
        path=distribution_path_formula(5,2,0)
        self.assertEqual(expected_frequency(path[0],5),F(2,5))
        self.assertEqual(expected_frequency(path[4],5),F(2,5))
        self.assertGreater(path[1][0],0)
        self.assertGreater(path[1][5],0)

    def test_finite_group_is_not_infinite_deterministic_repetition(self):
        d=results_document()["counterexamples"]
        self.assertNotEqual(d["finite_stochastic_vs_infinite_deterministic_t2_difference"],"0")

    def test_all_conditional_probabilities_rational(self):
        for n in POPULATIONS:
            for h in CONFORMITY:
                self.assertTrue(all(isinstance(v,F) for row in binomial_kernel(n,h) for v in row))

    def test_fixation_probabilities_in_unit_interval(self):
        for n in POPULATIONS:
            for h in CONFORMITY:
                self.assertTrue(all(0<=v<=1 for v in fixation_probabilities(n,h)))

    def test_terminal_A_fixation_monotone_in_starting_count(self):
        for n in POPULATIONS:
            for h in CONFORMITY:
                fx=fixation_probabilities(n,h)
                self.assertTrue(all(a<b for a,b in zip(fx,fx[1:])))

    def test_reject_invalid_population_sizes(self):
        for n in (0,1,4,6,9,False,5.0,"7"):
            with self.assertRaises(ValueError): checked_n(n)

    def test_reject_invalid_initial_counts(self):
        for k in (-1,8,F(1,2),0.5,True,"3"):
            with self.assertRaises(ValueError): checked_k(7,k)

    def test_reject_invalid_strengths(self):
        for h in (-1,F(11,10),0.5,True,"1/4"):
            with self.assertRaises(ValueError): unit(h,"h")

    def test_reject_invalid_horizons(self):
        for horizon in (-1,False,F(1,2),"4",3.5):
            with self.assertRaises(ValueError):
                distribution_path_formula(5,2,F(1,2),horizon)
            with self.assertRaises(ValueError):
                distribution_path_enumerated(5,2,F(1,2),horizon)

    def test_reject_bad_expected_distribution_dimension(self):
        with self.assertRaises(ValueError): expected_frequency((F(1),),5)

    def test_reject_non_normalized_expected_distribution(self):
        with self.assertRaises(ValueError): expected_frequency((F(0),)*6,5)

    def test_empirical_prediction_scope_restricted(self):
        d=results_document()
        self.assertTrue(d["evidence"].startswith("E1"))
        self.assertFalse(d["original_behavioral_data_used"])
        self.assertFalse(d["group_causal_prediction_claimed"])
        self.assertFalse(d["author_original_models_reproduced"])

    def test_full_48_world_ledger_and_eight_kernels(self):
        d=results_document()
        self.assertEqual(d["number_of_frozen_worlds"],48)
        self.assertEqual(len(d["worlds"]),48)
        self.assertEqual(len(d["kernel_receipts"]),8)
        self.assertEqual(len({w["id"] for w in d["worlds"]}),48)
        self.assertTrue(all(len(w["probability_distributions"])==5 for w in d["worlds"]))

    def test_canonical_json_byte_identity(self):
        p=Path(__file__).with_name("R161_EXACT_RESULTS.json")
        if not p.exists(): self.skipTest("CI creates full JSON before test run")
        canonical=(json.dumps(results_document(),sort_keys=True,indent=2,ensure_ascii=False)+"\n").encode()
        self.assertEqual(p.read_bytes(),canonical)


for ni in range(len(POPULATIONS)):
    for ki in range(len(INITIAL_STATES[ni])):
        for hi in range(len(CONFORMITY)):
            def build(ni=ni,ki=ki,hi=hi):
                def check(self): self.check_world(ni,ki,hi)
                return check
            setattr(TestR161,f"test_frozen_n{ni}_k{ki}_h{hi}",build())


if __name__=="__main__":
    unittest.main()
