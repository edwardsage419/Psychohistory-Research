"""R158 60 artificial event histories and bounded source-aware controls."""
import json
import math
import unittest
from fractions import Fraction as F
from pathlib import Path

from r158_poisson_count_process import (
    MU_GRID,ALPHA_GRID,ARTIFICIAL_HISTORIES,EXPECTATION_HORIZON,
    params,valid_counts,intensities,log_score_gamma,log_score_factorial,
    expectation_recurrence,expectation_geometric,stationary_mean,full_result
)


class TestR158(unittest.TestCase):
    def check_world(self,hi,mi,ai):
        history=ARTIFICIAL_HISTORIES[hi]
        mu,alpha=MU_GRID[mi],ALPHA_GRID[ai]
        lam=intensities(history,mu,alpha)
        self.assertEqual(len(lam),8)
        self.assertEqual(lam[0],mu)
        for t,val in enumerate(lam):
            expected=mu+(alpha*history[t-1] if t else 0)
            self.assertEqual(val,expected)
            self.assertGreater(val,0)
        a,terms=log_score_gamma(history,mu,alpha)
        b,terms_b=log_score_factorial(history,mu,alpha)
        self.assertLess(abs(a-b),1e-12)
        self.assertEqual(len(terms),8)
        for x,y in zip(terms,terms_b):
            self.assertLess(abs(x-y),1e-12)
            self.assertTrue(math.isfinite(x))
        if alpha==0:
            self.assertTrue(all(x==mu for x in lam))
        e=expectation_recurrence(mu,alpha)
        g=expectation_geometric(mu,alpha)
        self.assertEqual(e,g)
        self.assertEqual(len(e),13)
        self.assertEqual(e[0],mu)

    def test_frozen_parameter_case_count(self):
        self.assertEqual(len(ARTIFICIAL_HISTORIES)*len(MU_GRID)*len(ALPHA_GRID),60)

    def test_first_intensity_is_exogenous_baseline(self):
        for h in ARTIFICIAL_HISTORIES:
            self.assertEqual(intensities(h,1,F(1,2))[0],1)

    def test_lagged_not_simultaneous_update(self):
        self.assertEqual(intensities(ARTIFICIAL_HISTORIES[1],1,F(1,2)),
                         (F(1),F(3,2),F(1),F(2),F(1),F(5,2),F(1),F(2)))

    def test_zero_feedback_is_constant_poisson(self):
        for h in ARTIFICIAL_HISTORIES:
            self.assertTrue(all(x==1 for x in intensities(h,1,0)))

    def test_burst_increases_next_mean_by_four_alpha(self):
        self.assertEqual(intensities((4,1),1,F(1,2))[1],3)
        self.assertEqual(intensities((4,1),1,0)[1],1)

    def test_all_zero_history_cannot_recover_feedback(self):
        h=ARTIFICIAL_HISTORIES[0]
        for mu in MU_GRID:
            base=log_score_gamma(h,mu,0)[0]
            for a in ALPHA_GRID:
                self.assertEqual(log_score_gamma(h,mu,a)[0],base)

    def test_feedback_loses_for_alternating_sequence(self):
        h=ARTIFICIAL_HISTORIES[1]
        self.assertLess(log_score_gamma(h,1,F(1,2))[0],log_score_gamma(h,1,0)[0])

    def test_feedback_wins_for_clustered_sequence_at_low_baseline(self):
        h=ARTIFICIAL_HISTORIES[2]
        self.assertGreater(log_score_gamma(h,F(1,2),F(1,2))[0],
                           log_score_gamma(h,F(1,2),0)[0])

    def test_no_universal_feedback_score_preference(self):
        a=full_result()['negative_controls']
        self.assertLess(a['history_H1_mu1_feedback_point5_log_score_difference'],0)
        self.assertGreater(a['history_H2_mu_point5_feedback_point5_log_score_difference'],0)

    def test_poisson_pmf_sums_to_one(self):
        for mu in (F(1,2),F(1),F(2)):
            for alpha in ALPHA_GRID:
                for prior in (0,2,4):
                    lam=float(mu+alpha*prior)
                    mass=sum(math.exp(-lam)*lam**n/math.factorial(n) for n in range(41))
                    self.assertLess(abs(mass-1),1e-12)

    def test_lgamma_equals_factorial_at_small_counts(self):
        for n in range(10):
            self.assertLess(abs(math.lgamma(n+1)-math.log(math.factorial(n))),1e-12)

    def test_exact_mean_recurrence_and_geometric_all_grid(self):
        for mu in MU_GRID:
            for alpha in ALPHA_GRID:
                self.assertEqual(expectation_recurrence(mu,alpha),
                                 expectation_geometric(mu,alpha))

    def test_mean_zero_feedback_is_constant(self):
        self.assertEqual(expectation_geometric(F(1,2),0),
                         (F(1,2),)*13)

    def test_mean_alpha_one_grows_linearly(self):
        self.assertEqual(expectation_geometric(1,1),tuple(F(t+1) for t in range(13)))
        self.assertEqual(expectation_geometric(F(1,2),1)[-1],F(13,2))

    def test_no_stationary_limit_at_alpha_one(self):
        for mu in MU_GRID:
            self.assertIsNone(stationary_mean(mu,1))

    def test_stationary_mean_for_subcritical_alpha(self):
        self.assertEqual(stationary_mean(1,F(3,4)),4)
        self.assertEqual(stationary_mean(F(1,2),F(1,2)),1)

    def test_expected_count_no_dependence_on_selected_history(self):
        a=expectation_recurrence(1,F(1,2))
        for h in ARTIFICIAL_HISTORIES:
            self.assertEqual(a,expectation_geometric(1,F(1,2)))
            self.assertEqual(len(intensities(h,1,F(1,2))),8)

    def test_negative_baseline_rejected(self):
        for value in (-1,0):
            with self.assertRaises(ValueError): params(value,F(1,2))

    def test_feedback_range_rejected(self):
        for value in (F(-1,10),F(11,10),3):
            with self.assertRaises(ValueError): params(1,value)

    def test_invalid_parameter_types_rejected(self):
        for value in (True,0.1,"1/2",None,math.inf,math.nan):
            with self.assertRaises(ValueError): params(value,F(1,2))
            with self.assertRaises(ValueError): params(1,value)

    def test_invalid_event_counts_rejected(self):
        for history in ((-1,0),(True,1),(1,F(1,2)),(0.2,1),("1",),None):
            with self.assertRaises(ValueError): valid_counts(history)

    def test_empty_sequence_log_score_is_zero(self):
        self.assertEqual(log_score_gamma([],1,F(1,2)),(0,()))
        self.assertEqual(log_score_factorial([],1,F(1,2)),(0,()))

    def test_invalid_expected_horizon_rejected(self):
        for horizon in (-1,False,2.2,"12"):
            with self.assertRaises(ValueError): expectation_recurrence(1,F(1,2),horizon)
            with self.assertRaises(ValueError): expectation_geometric(1,F(1,2),horizon)

    def test_published_source_causal_claim_restricted(self):
        d=full_result()
        self.assertTrue(d['not_exact_hawkes_or_original_INGARCH'])
        self.assertFalse(d['historical_conflict_data_used'])
        self.assertFalse(d['real_event_predictive_accuracy_tested'])
        self.assertFalse(d['causal_self_excitation_established'])

    def test_world_ledger_has_correct_count_and_identification(self):
        d=full_result()
        self.assertEqual(d['world_count'],60)
        self.assertEqual(len(d['worlds']),60)
        self.assertEqual(len({w['case_id'] for w in d['worlds']}),60)
        self.assertEqual(len(d['independent_expectation_paths']),15)
        self.assertTrue(d['negative_controls']['all_zero_history_is_alpha_independent'])

    def test_log_scores_are_prespecified_only(self):
        d=full_result()
        for w in d['worlds']:
            self.assertEqual(len(w['observed_artificial_counts']),8)
            self.assertEqual(len(w['conditional_lambdas']),8)
            self.assertEqual(len(w['log_score_terms']),8)
            self.assertTrue(w['factorial_score_matches_gamma'])

    def test_saved_full_json_replay(self):
        path=Path(__file__).with_name('R158_EXACT_RESULTS.json')
        if not path.exists(): self.skipTest("CI regenerates full result before tests")
        target=(json.dumps(full_result(),indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode()
        self.assertEqual(path.read_bytes(),target)


for hi in range(len(ARTIFICIAL_HISTORIES)):
    for mi in range(len(MU_GRID)):
        for ai in range(len(ALPHA_GRID)):
            def make(hi=hi,mi=mi,ai=ai):
                def check(self): self.check_world(hi,mi,ai)
                return check
            setattr(TestR158,f'test_frozen_h{hi}_m{mi}_a{ai}',make())


if __name__=='__main__':
    unittest.main()
