"""Synthetic no-lookahead tests for R069 daily RT activity conditional prediction."""
import gzip
import hashlib
import io
import math
import unittest
from unittest.mock import patch
import r069_higgs_forward_day_rt as m


def synthetic_week():
    # Fabricated account IDs never published in actual research outputs.
    return [
        [(987654321,55555,"MT"),(999999,987654321,"RT")],
        [(987654321,999999,"RT"),(999999,55555,"MT"),(55555,987654321,"RT")],
        [(987654321,999999,"RT"),(55555,999999,"RE"),(44444,987654321,"RT")],
        [(987654321,44444,"RT"),(999999,55555,"RT"),(44444,987654321,"RT")],
        [(987654321,999999,"MT"),(44444,999999,"RE")],
        [(55555,987654321,"RT"),(44444,999999,"RT")],
        [(987654321,55555,"RT"),(999999,987654321,"RT")],
    ]


class ForwardTimeTests(unittest.TestCase):
    def test_activity_bins(self):
        self.assertEqual([m.activity_bin(x) for x in (1,2,4,5,500)], [0,1,1,2,2])

    def test_invalid_activity_count_fails(self):
        for x in (0,-1,1.5,True):
            with self.assertRaises(ValueError):
                m.activity_bin(x)

    def test_source_real_SHA_is_always_required(self):
        with self.assertRaisesRegex(ValueError,"SHA_OR_LENGTH"):
            m.validate_source(gzip.compress(b"0 1 1341100800 RT\n"))

    def test_previous_only_risk_account_excludes_new_actor(self):
        daily=synthetic_week()
        hist=m.create_cohorts(daily)
        jul2=hist[0]
        self.assertEqual(jul2["risk_accounts"],2)
        self.assertEqual(jul2["RT_accounts_first_appearing_today_excluded"],1)
        self.assertEqual(jul2["RT_accounts_in_at_risk_cohort"],1)

    def test_yesterday_target_signal_uses_prefix_contacts(self):
        h=m.create_cohorts(synthetic_week())
        jul2=h[0]
        # The two previous-day actors are known, but no one has ever
        # previously contacted a target who RT'd yesterday except the MT
        # user contacting an unobserved target.
        self.assertEqual(jul2["peer_activity_proxy_true_risk_accounts"],0)
        self.assertGreaterEqual(h[1]["peer_activity_proxy_true_risk_accounts"],0)

    def test_changes_in_today_RT_do_not_change_atrisk_or_social_exposure(self):
        a=synthetic_week()
        b=synthetic_week()
        b[3]=[(999999,55555,"RE"),(11111,55555,"RT")]
        old=m.create_cohorts(a)[2]
        new=m.create_cohorts(b)[2]
        self.assertEqual(old["risk_accounts"],new["risk_accounts"])
        self.assertEqual(old["peer_activity_proxy_true_risk_accounts"],
                         new["peer_activity_proxy_true_risk_accounts"])
        self.assertEqual({k:v[0] for k,v in old["social"].items()},
                         {k:v[0] for k,v in new["social"].items()})

    def test_future_events_do_not_affect_past_predictions(self):
        a=synthetic_week()
        b=synthetic_week()
        b[5]=[(999999,999999,"RT"),(111111111,44444,"RT")]
        A=m.create_cohorts(a)
        B=m.create_cohorts(b)
        self.assertEqual(m.daily_prediction(A,3),m.daily_prediction(B,3))
        self.assertEqual(m.daily_prediction(A,4),m.daily_prediction(B,4))

    def test_training_day_count_strictly_before_score(self):
        q=m.daily_prediction(m.create_cohorts(synthetic_week()),3)
        self.assertEqual(q["training_days"],2)
        self.assertEqual(q["UTC_day"],"2012-07-04")

    def test_all_models_share_exact_same_risk_denominator(self):
        q=m.evaluate_day_cohorts(m.create_cohorts(synthetic_week()))
        self.assertEqual(set(q["model_summary"]),set(m.FAMILIES))
        for day in q["scored_UTC_days"]:
            self.assertEqual(len({s["scored_account_days"] for s in day["model_scores"].values()}),1)

    def test_four_UTC_holdout_days_preserved(self):
        result=m.evaluate_day_cohorts(m.create_cohorts(synthetic_week()))
        self.assertEqual([x["UTC_day"] for x in result["scored_UTC_days"]],
                         ["2012-07-04","2012-07-05","2012-07-06","2012-07-07"])

    def test_all_predictions_bounded_and_scores_finite(self):
        result=m.evaluate_day_cohorts(m.create_cohorts(synthetic_week()))
        for model,v in result["model_summary"].items():
            self.assertTrue(math.isfinite(v["primary_four_UTC_days_equal_binary_logloss_nats"]),model)
            self.assertGreaterEqual(v["primary_four_days_equal_Brier"],0)

    def test_beta_prior_open_unit_interval(self):
        self.assertAlmostEqual(m.rate(0,1),1/3)
        self.assertAlmostEqual(m.rate(1,1),2/3)

    def test_shrinkage_to_prior_when_missing_bin(self):
        self.assertAlmostEqual(m.shrink(("unseen",),{},0.12),0.12)

    def test_shrinkage_not_silent_zero_probability(self):
        self.assertGreater(m.shrink(("x",),{("x",):(100,0)},0.2),0)

    def test_beta_invalid_denominators_rejected(self):
        for pos,n in ((1,0),(-1,2),(3,2)):
            with self.assertRaises(ValueError):m.rate(pos,n)

    def test_bad_training_windows_cannot_be_selected(self):
        cohorts=m.create_cohorts(synthetic_week())
        with self.assertRaises(ValueError):m.daily_prediction(cohorts,2)

    def test_no_lookahead_through_full_RT_aggregate(self):
        result=m.evaluate_day_cohorts(m.create_cohorts(synthetic_week()))
        self.assertFalse(result["source_person_ID_or_event_records_exported"])
        self.assertNotIn("987654321",str(result))
        self.assertNotIn("999999",str(result))

    def test_future_accounts_not_backfilled_into_early_cohort(self):
        a=synthetic_week()
        a[6].append((888888888,55555,"RT"))
        h=m.create_cohorts(a)
        self.assertEqual(h[5]["risk_accounts"],m.create_cohorts(synthetic_week())[5]["risk_accounts"])
        self.assertNotIn("888888888",str(h[5]))

    def test_exact_seven_days_required(self):
        with self.assertRaisesRegex(ValueError,"SEVEN"):
            m.create_cohorts(synthetic_week()[:-1])

    def test_source_window_comment_is_not_sample_id(self):
        self.assertEqual(m.SCORE_DAYS,(3,4,5,6))
        self.assertEqual(m.TOTAL_EVENTS,563069)

    def test_brier_and_logloss_zero_if_impossible_not_allowed(self):
        for p in (0.,1.):
            self.assertFalse(0<m.shrink(("x",),{},p)<1)
            # The real trainer has Beta(1,1), so it cannot return 0 or 1.

    def test_risk_cohort_not_based_on_ever_future_actor(self):
        c=m.create_cohorts(synthetic_week())
        self.assertLess(c[0]["risk_accounts"],c[-1]["risk_accounts"])


if __name__=="__main__":
    unittest.main()
