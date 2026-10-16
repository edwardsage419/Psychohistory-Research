"""Synthetic R072 rule and exhaustive-population scientific boundaries."""
import unittest
from itertools import product
from r072_reputation_public_signals import (
    ROLES,NORMS,CHANNELS,SCHEDULE,EXPECTED_CASES,EXPECTED_DECISIONS,
    assess,true_action,reported_action,run,evaluate,validate,
)


class PublicReputationTests(unittest.TestCase):
    def test_4_agents_12_ordered_pairs_twice_no_self(self):
        self.assertEqual(len(SCHEDULE),24)
        self.assertEqual(SCHEDULE[:12],SCHEDULE[12:])
        self.assertEqual(len(set(SCHEDULE[:12])),12)
        self.assertTrue(all(a!=b for a,b in SCHEDULE))

    def test_role_universe_81(self):
        self.assertEqual(len(list(product(ROLES,repeat=4))),81)

    def test_binary_initial_reputation_universe_16(self):
        self.assertEqual(len(list(product((0,1),repeat=4))),16)

    def test_frozen_exact_case_count(self):
        self.assertEqual(EXPECTED_CASES,11664)
        self.assertEqual(EXPECTED_DECISIONS,279936)

    def test_image_scoring_refusing_bad_is_bad(self):
        self.assertEqual(assess(False,False,"IMAGE_SCORING"),0)

    def test_simple_standing_refusing_bad_is_good(self):
        self.assertEqual(assess(False,False,"SIMPLE_STANDING"),1)

    def test_stern_judging_refusing_bad_is_good(self):
        self.assertEqual(assess(False,False,"STERN_JUDGING"),1)

    def test_stern_judging_helping_bad_is_bad(self):
        self.assertEqual(assess(True,False,"STERN_JUDGING"),0)

    def test_standing_helping_bad_is_good(self):
        self.assertEqual(assess(True,False,"SIMPLE_STANDING"),1)

    def test_defecting_from_good_is_bad_all_three_norms(self):
        for norm in NORMS:
            self.assertEqual(assess(False,True,norm),0)

    def test_helping_good_is_good_all_three_norms(self):
        for norm in NORMS:
            self.assertEqual(assess(True,True,norm),1)

    def test_allc_help_all_possible(self):
        for initial in ((0,0,0,0),(1,0,1,0)):
            r=run(("ALLC",)*4,initial,"STERN_JUDGING","VERIFIED")
            self.assertEqual(r["true_help_count"],24)
            self.assertEqual(r["group_payoff_sum"],24)

    def test_alld_no_transaction(self):
        r=run(("ALLD",)*4,(1,1,1,1),"IMAGE_SCORING","VERIFIED")
        self.assertEqual(r["true_help_count"],0)
        self.assertEqual(r["group_payoff_sum"],0)

    def test_disc_sees_recipient_before_event_not_after(self):
        roles=("DISC","ALLC","ALLD","ALLD")
        data=run(roles,(1,0,0,0),"IMAGE_SCORING","VERIFIED",True)
        first=data["synthetic_trace"][0]
        self.assertEqual(first["donor"],0)
        self.assertEqual(first["recipient"],1)
        self.assertEqual(first["recipient_good_at_choice"],0)
        self.assertFalse(first["actual_help"])
        self.assertEqual(first["donor_reputation_after"],0)

    def test_no_observation_keeps_all_prior_reputations(self):
        source=(1,0,1,0)
        q=run(("DISC","ALLD","ALLC","DISC"),source,"STERN_JUDGING","NO_OBSERVATION")
        self.assertEqual(q["final_public_reputations"],list(source))
        self.assertEqual(q["public_reputation_changes"],0)

    def test_flip_every_fourth_preserves_actual_action_payoffs(self):
        roles=("ALLC",)*4
        v=run(roles,(0,)*4,"IMAGE_SCORING","VERIFIED",True)
        b=run(roles,(0,)*4,"IMAGE_SCORING","FLIP_EVERY_FOURTH",True)
        self.assertEqual([x["actual_help"] for x in v["synthetic_trace"]],
                         [x["actual_help"] for x in b["synthetic_trace"]])
        self.assertEqual(v["group_payoff_sum"],b["group_payoff_sum"])
        self.assertEqual(b["false_reports"],6)
        self.assertEqual([x["event"] for x in b["synthetic_trace"]
                          if x["reported_help"] != x["actual_help"]],
                         [4,8,12,16,20,24])

    def test_verified_reports_have_zero_flips(self):
        q=run(("ALLD",)*4,(1,)*4,"IMAGE_SCORING","VERIFIED")
        self.assertEqual(q["false_reports"],0)

    def test_no_observation_has_no_reported_actions(self):
        q=run(("DISC",)*4,(1,)*4,"IMAGE_SCORING","NO_OBSERVATION",True)
        self.assertTrue(all(e["reported_help"] is None for e in q["synthetic_trace"]))

    def test_no_disc_behavior_invariant_across_norms_and_channels(self):
        roles=("ALLC","ALLD","ALLC","ALLD")
        observations=[run(roles,(0,1,0,1),n,c) for n in NORMS for c in CHANNELS]
        self.assertEqual(len({x["true_help_count"] for x in observations}),1)

    def test_donor_payoff_is_minus_one_recipient_plus_two(self):
        first=run(("ALLC",)*4,(1,)*4,"IMAGE_SCORING","VERIFIED",True)["synthetic_trace"][0]
        self.assertEqual(first["balance_after"],[-1,2,0,0])

    def test_balance_invariant_over_all_24_events(self):
        for roles in (("ALLC",)*4,("DISC","ALLC","DISC","ALLD")):
            q=run(roles,(1,0,0,1),"SIMPLE_STANDING","FLIP_EVERY_FOURTH",True)
            for trace in q["synthetic_trace"]:
                self.assertEqual(sum(trace["balance_after"]),
                                 sum(e["actual_help"] for e in q["synthetic_trace"][:trace["event"]]))

    def test_invalid_strategy_rejected(self):
        with self.assertRaises(ValueError):
            validate(("DISC","ALLC","BAD","ALLD"),(1,1,1,1),"IMAGE_SCORING","VERIFIED")

    def test_invalid_reputation_array_rejected(self):
        for reputation in ((0,1,2,1),(0,1,True,1),(0,1,0)):
            with self.assertRaises(ValueError):
                validate(("DISC",)*4,reputation,"IMAGE_SCORING","VERIFIED")

    def test_invalid_norm_and_channel_rejected(self):
        with self.assertRaises(ValueError):
            run(("DISC",)*4,(1,)*4,"MORAL_VOTING","VERIFIED")
        with self.assertRaises(ValueError):
            run(("DISC",)*4,(1,)*4,"IMAGE_SCORING","UNLOGGED_INSTITUTION")

    def test_nonboolean_moral_score_input_fails_closed(self):
        with self.assertRaises(ValueError):
            assess(1,True,"SIMPLE_STANDING")

    def test_nonboolean_action_recipient_rejected(self):
        with self.assertRaises(ValueError):
            true_action("DISC",1)

    def test_bad_event_index_rejected(self):
        with self.assertRaises(ValueError):
            reported_action(True,0,"FLIP_EVERY_FOURTH")

    def test_complete_11664_case_exhaustion_and_9_model_cells(self):
        z=evaluate()
        self.assertEqual(z["complete_model_cases"],11664)
        self.assertEqual(z["actual_decision_events"],279936)
        for norm in NORMS:
            self.assertEqual(set(z["norm_channel_results"][norm]),set(CHANNELS))
            for channel in CHANNELS:
                self.assertEqual(z["norm_channel_results"][norm][channel]["cases"],1296)
                self.assertEqual(z["norm_channel_results"][norm][channel]["transactions"],31104)
                self.assertEqual(sum(x["cases"] for x in z["cooperation_by_DISC_role_count"][norm][channel].values()),1296)

    def test_complete_e1_does_not_claim_external_behavior_verification(self):
        z=evaluate()
        self.assertTrue(z["synthetic_only"])
        self.assertEqual(z["real_human_trust_signal_E2"],"NOT_ESTABLISHED")
        self.assertEqual(z["model_evolutionary_ESS"],"NOT_CALCULATED")

    def test_paired_comparisons_have_identical_frozen_state_denominators(self):
        z=evaluate()
        self.assertTrue(all(x["different_true_help_cases"]+x["equal_true_help_cases"]==1296
                            for x in z["paired_channel_counterfactuals"].values()))
        self.assertTrue(all(x["different_true_help_cases"]+x["equal_true_help_cases"]==1296
                            for x in z["paired_norm_counterfactuals"].values()))


if __name__=="__main__":
    unittest.main()
