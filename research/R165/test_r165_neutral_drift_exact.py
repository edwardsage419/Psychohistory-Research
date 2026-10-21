"""R165 authentic exact tests for artificial neutral copying and innovation."""
import json
import unittest
from fractions import Fraction as F
from pathlib import Path
from r165_neutral_drift_exact import (
    NS, STARTS, MUS, validate, prob, kernel, enumerate_kernel,
    path_binomial, path_enumerated, absorption, stationary,
    mean, heterogeneity, mean_formula, document
)

class TestNeutralDrift(unittest.TestCase):
    def check_world(self,ni,ki,mi):
        n=NS[ni];k=STARTS[ni][ki];mu=MUS[mi]
        direct=path_binomial(n,k,mu)
        enumerated=path_enumerated(n,k,mu)
        self.assertEqual(direct,enumerated)
        self.assertEqual(len(direct),5)
        self.assertEqual(direct[0][k],1)
        for t,dist in enumerate(direct):
            self.assertEqual(len(dist),n+1)
            self.assertEqual(sum(dist),1)
            self.assertTrue(all(isinstance(v,F) and 0<=v<=1 for v in dist))
            self.assertEqual(mean(dist,n),mean_formula(n,k,mu,t))
            if mu==0:
                h0=2*F(k,n)*(1-F(k,n))
                self.assertEqual(heterogeneity(dist,n),h0*(1-F(1,n))**t)
        if mu==0:
            self.assertEqual(direct[0][k],1)
            self.assertEqual(absorption(n)[0],0)
            self.assertEqual(absorption(n)[n],0)

    def test_48_world_factorial_count(self):
        self.assertEqual(len(NS)*4*len(MUS),48)

    def test_binomial_exact_equals_full_sequence_enumeration(self):
        for n in NS:
            for mu in MUS:
                self.assertEqual(kernel(n,mu),enumerate_kernel(n,mu))

    def test_all_rows_normalize(self):
        for n in NS:
            for mu in MUS:
                for row in kernel(n,mu):
                    self.assertEqual(sum(row),1)

    def test_neutral_one_step_expected_frequency(self):
        for n in NS:
            for k in range(n+1):
                self.assertEqual(mean(kernel(n,0)[k],n),F(k,n))

    def test_all_mu_expected_frequency_closed_form(self):
        for n in NS:
            for k in range(n+1):
                for mu in MUS:
                    self.assertEqual(mean(kernel(n,mu)[k],n),prob(n,k,mu))

    def test_neutral_average_frequency_constant_across_generations(self):
        for n in NS:
            for k in range(n+1):
                for dist in path_binomial(n,k,0):
                    self.assertEqual(mean(dist,n),F(k,n))

    def test_neutral_diversity_decay_rate_exact(self):
        for n in NS:
            for k in (1,n//2,n-1):
                p=F(k,n);h0=2*p*(1-p)
                for t,dist in enumerate(path_binomial(n,k,0)):
                    self.assertEqual(heterogeneity(dist,n),h0*(1-F(1,n))**t)

    def test_same_half_frequency_different_noise_variances(self):
        def var(n):
            P=kernel(n,0)[n//2]
            return sum((P[k]*(F(k,n)-F(1,2))**2 for k in range(n+1)),F(0))
        self.assertEqual(var(4),F(1,16))
        self.assertEqual(var(8),F(1,32))
        self.assertGreater(var(4),var(8))

    def test_larger_N_maintains_neutral_diversity_better_per_step(self):
        self.assertGreater(F(1)-F(1,8),F(1)-F(1,4))

    def test_neutral_absorbing_boundaries(self):
        for n in NS:
            P=kernel(n,0)
            self.assertEqual(P[0][0],1)
            self.assertEqual(P[n][n],1)

    def test_positive_innovation_breaks_boundary_absorption(self):
        for n in NS:
            for mu in MUS[1:]:
                P=kernel(n,mu)
                self.assertLess(P[0][0],1)
                self.assertLess(P[n][n],1)

    def test_positive_innovation_boundary_mean_moves_inward(self):
        for n in NS:
            for mu in MUS[1:]:
                self.assertEqual(prob(n,0,mu),mu/2)
                self.assertEqual(prob(n,n,mu),1-mu/2)

    def test_positive_innovation_ensemble_mean_toward_half(self):
        for n in NS:
            for k in (0,1,n-1,n):
                for mu in MUS[1:]:
                    path=path_binomial(n,k,mu)
                    for t,dist in enumerate(path):
                        self.assertEqual(mean(dist,n),
                            F(1,2)+(1-mu)**t*(F(k,n)-F(1,2)))

    def test_neutral_mean_constant_does_not_mean_stationary_distribution(self):
        path=path_binomial(4,2,0)
        self.assertEqual(mean(path[0],4),mean(path[4],4))
        self.assertNotEqual(path[0],path[4])

    def test_expected_absorption_is_zero_at_endpoints(self):
        for n in NS:
            tau=absorption(n)
            self.assertEqual(tau[0],0)
            self.assertEqual(tau[n],0)

    def test_interior_absorption_times_are_positive(self):
        for n in NS:
            tau=absorption(n)
            self.assertTrue(all(v>0 for v in tau[1:n]))

    def test_absorption_time_harmonic_exact(self):
        for n in NS:
            P=kernel(n,0);tau=absorption(n)
            for k in range(1,n):
                self.assertEqual(tau[k],1+sum((P[k][j]*tau[j] for j in range(n+1)),F(0)))

    def test_absorption_time_mirror_symmetry(self):
        for n in NS:
            tau=absorption(n)
            self.assertTrue(all(tau[k]==tau[n-k] for k in range(n+1)))

    def test_larger_equal_prevalence_population_takes_longer_to_absorb(self):
        self.assertGreater(absorption(8)[4],absorption(4)[2])

    def test_unique_stationary_positive_innovation_normalized(self):
        for n in NS:
            for mu in MUS[1:]:
                pi=stationary(n,mu)
                self.assertEqual(sum(pi),1)
                self.assertTrue(all(x>0 for x in pi))

    def test_stationary_exact_distribution_equations(self):
        for n in NS:
            for mu in MUS[1:]:
                P=kernel(n,mu);pi=stationary(n,mu)
                for j in range(n+1):
                    self.assertEqual(pi[j],sum((pi[i]*P[i][j] for i in range(n+1)),F(0)))

    def test_stationary_symmetry(self):
        for n in NS:
            for mu in MUS[1:]:
                pi=stationary(n,mu)
                self.assertEqual(tuple(reversed(pi)),pi)

    def test_stationary_mean_is_half(self):
        for n in NS:
            for mu in MUS[1:]:
                self.assertEqual(mean(stationary(n,mu),n),F(1,2))

    def test_positive_innovation_stationary_boundaries_nonzero(self):
        for n in NS:
            for mu in MUS[1:]:
                pi=stationary(n,mu)
                self.assertGreater(pi[0],0)
                self.assertGreater(pi[n],0)

    def test_no_unique_stationary_when_mu_zero(self):
        for n in NS:
            with self.assertRaises(ValueError): stationary(n,0)

    def test_neutral_reflection_symmetry(self):
        for n in NS:
            for mu in MUS:
                for k in range(n+1):
                    a=path_binomial(n,k,mu)
                    b=path_binomial(n,n-k,mu)
                    for left,right in zip(a,b):
                        self.assertEqual(left,tuple(reversed(right)))

    def test_invalid_population_sizes(self):
        for v in (0,1,3,5,False,True,4.0,"4"):
            with self.assertRaises(ValueError): validate(v,0,0)

    def test_invalid_initial_counts(self):
        for v in (-1,9,False,True,F(1,2),1.0,"1"):
            with self.assertRaises(ValueError): validate(8,v,0)

    def test_invalid_innovation_rates_and_types(self):
        for v in (-1,F(1,32),F(1,2),0.25,True,False,"1/4"):
            with self.assertRaises(ValueError): validate(4,2,v)

    def test_invalid_horizon_in_both_routes(self):
        for v in (-1,F(1,2),False,True,2.0,"4"):
            with self.assertRaises(ValueError): path_binomial(4,2,0,v)
            with self.assertRaises(ValueError): path_enumerated(4,2,0,v)

    def test_invalid_mean_distribution(self):
        for x in ((F(1),),(F(0),)*5):
            with self.assertRaises(ValueError): mean(x,4)
            with self.assertRaises(ValueError): heterogeneity(x,4)

    def test_original_multi_variant_studies_not_replayed(self):
        d=document()
        self.assertFalse(d["original_multi_allele_model_reproduced"])
        self.assertFalse(d["empirical_name_pottery_patent_data_used"])
        self.assertFalse(d["historical_predictions_made"])

    def test_48_full_worlds_and_12_stored_kernels(self):
        d=document()
        self.assertEqual(d['world_count'],48)
        self.assertEqual(len(d['worlds']),48)
        self.assertEqual(len({w['id'] for w in d['worlds']}),48)
        self.assertEqual(len(d['kernels']),12)
        self.assertTrue(all(len(w['points'])==5 for w in d['worlds']))

    def test_complete_JSON_byte_replay(self):
        p=Path(__file__).with_name('R165_EXACT_RESULTS.json')
        if not p.exists(): self.skipTest("CI generates canonical JSON before testing")
        expected=(json.dumps(document(),indent=2,sort_keys=True,ensure_ascii=False)+"\n").encode()
        self.assertEqual(p.read_bytes(),expected)


for ni in range(len(NS)):
    for ki in range(len(STARTS[ni])):
        for mi in range(len(MUS)):
            def maker(ni=ni,ki=ki,mi=mi):
                def test(self): self.check_world(ni,ki,mi)
                return test
            setattr(TestNeutralDrift,f"test_frozen_n{ni}_k{ki}_m{mi}",maker())


if __name__=="__main__":
    unittest.main()
