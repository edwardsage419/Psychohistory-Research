"""R071 E1: mathematical accounting, lag, sanction and full-factorial tests."""
import math
import unittest
from r071_norm_cooperation_punishment import (
    N, STEPS, EXPECTED_CASES, EXPECTED_COMPOSITIONS, INSTITUTIONS,
    THRESHOLDS, INITIAL_NORMS, compositions, check_config,
    calculate_round, run, evaluate, fixed_synthetic_witnesses,
)


class NormInstitutionE1Tests(unittest.TestCase):
    def test_all_56_abstract_compositions_unique(self):
        a=list(compositions())
        self.assertEqual(len(a),56)
        self.assertEqual(len(set(a)),56)

    def test_every_composition_exactly_five_people(self):
        for group in compositions():
            self.assertEqual(sum(group),N)
            self.assertTrue(all(x>=0 for x in group))

    def test_pure_conditional_norm_initial_zero_remains_none(self):
        r=run((0,0,0,5),.5,0.,"NONE")
        self.assertEqual([x["contributor_count"] for x in r["trajectory"]],[0]*8)

    def test_pure_conditional_norm_initial_one_remains_everyone(self):
        r=run((0,0,0,5),.5,1.,"NONE")
        self.assertEqual([x["contributor_count"] for x in r["trajectory"]],[5]*8)

    def test_prior_norm_lag_not_current_endogenous_action(self):
        r=run((3,0,0,2),.5,0.,"NONE",2)
        self.assertEqual([x["contributor_count"] for x in r["trajectory"]],[3,5])
        self.assertEqual(r["trajectory"][0]["prior_coop_fraction"],0.)
        self.assertEqual(r["trajectory"][1]["prior_coop_fraction"],.6)

    def test_higher_threshold_prevents_second_round_switch(self):
        r=run((3,0,0,2),.75,0.,"NONE",2)
        self.assertEqual([x["contributor_count"] for x in r["trajectory"]],[3,3])

    def test_one_sanctioner_deters_all_four_conditional(self):
        r=run((0,0,1,4),.5,0.,"VARIABLE_PUNISHMENT")
        self.assertEqual(r["end_contributor_count"],5)
        self.assertAlmostEqual(r["trajectory"][0]["marginal_payoff_N_coop_vs_defect"],.2)

    def test_same_conditional_group_without_sanction_has_one(self):
        self.assertEqual(run((0,0,1,4),.5,0.,"NONE")["end_contributor_count"],1)

    def test_institution_without_sanctioning_agent_cannot_change_N_choice(self):
        group=(0,0,0,5)
        outcomes=[run(group,.5,0.,policy)["end_contributor_count"]
                  for policy in INSTITUTIONS]
        self.assertEqual(outcomes,[0,0,0])

    def test_unconditional_defectors_do_not_respond_to_fines(self):
        group=(0,4,1,0)
        for policy in INSTITUTIONS:
            self.assertEqual(run(group,.5,0.,policy)["end_contributor_count"],1)

    def test_no_cooperators_five_defectors(self):
        group=(0,5,0,0)
        for policy in INSTITUTIONS:
            r=run(group,.5,0.,policy)
            self.assertTrue(all(x["contributor_count"]==0 for x in r["trajectory"]))

    def test_monitor_cost_is_payoff_disadvantage_even_with_everyone_cooperating(self):
        group=(1,0,1,3)
        fixed=calculate_round(group,1.,.5,"FIXED_MONITORING")
        variable=calculate_round(group,1.,.5,"VARIABLE_PUNISHMENT")
        self.assertEqual(fixed["contributor_count"],5)
        self.assertAlmostEqual(
            fixed["per_role_payoff"]["C"]-fixed["per_role_payoff"]["P"],1.2)
        self.assertAlmostEqual(
            variable["per_role_payoff"]["C"]-variable["per_role_payoff"]["P"],0.)

    def test_monitor_is_costly_even_without_defection(self):
        e=calculate_round((0,0,5,0),1.,.5,"FIXED_MONITORING")
        self.assertEqual(e["noncontributor_count"],0)
        self.assertEqual(e["sanction_event_count"],0)
        self.assertAlmostEqual(e["monitoring_cost_total"],6.)

    def test_defector_penalty_is_count_of_punishers(self):
        q=calculate_round((0,4,1,0),0.,.5,"VARIABLE_PUNISHMENT")
        self.assertEqual(q["noncontributor_count"],4)
        self.assertAlmostEqual(q["per_role_payoff"]["D"],2/5-.8)

    def test_punishment_variable_cost_is_per_target_and_punisher(self):
        q=calculate_round((0,3,2,0),0.,.5,"VARIABLE_PUNISHMENT")
        self.assertAlmostEqual(q["variable_sanction_cost_total"],.2*2*3)
        self.assertAlmostEqual(q["destructive_fines_total"],.8*2*3)

    def test_punishment_fines_are_destruction_not_income_transfer(self):
        q=calculate_round((0,4,1,0),0.,.5,"VARIABLE_PUNISHMENT")
        self.assertAlmostEqual(q["group_total_payoff"],2.-1.-(.8+.2)*4)

    def test_every_round_has_exact_payoff_accounting_in_full_grid(self):
        for group in compositions():
            for policy in INSTITUTIONS:
                q=calculate_round(group,.5,.75,policy)
                self.assertTrue(math.isclose(
                    q["group_total_payoff"],q["accounting_expected_total"],
                    abs_tol=1e-9))

    def test_all_group_roles_hold_fixed_with_time(self):
        q=run((1,1,1,2),.5,0.,"VARIABLE_PUNISHMENT")
        self.assertEqual(q["composition_by_C_D_P_N"],[1,1,1,2])
        self.assertEqual(len(q["trajectory"]),8)

    def test_bad_population_count_fails(self):
        for group in ((1,1,1,1),(1,1,1,1,1),(-1,1,1,4),(True,1,1,2)):
            with self.assertRaises(ValueError):
                run(group,.5,0.,"NONE")

    def test_invalid_theta_rejected(self):
        for t in (-.01,1.01,math.inf,math.nan,".5"):
            with self.assertRaises(ValueError):
                run((1,1,1,2),t,0.,"NONE")

    def test_invalid_prior_norm_rejected(self):
        for t in (-1.,.5,2.,math.nan,True):
            with self.assertRaises(ValueError):
                run((1,1,1,2),.5,t,"NONE")

    def test_invalid_institution_rejected(self):
        with self.assertRaises(ValueError):
            run((1,1,1,2),.5,0.,"ILLEGAL_POLICY")

    def test_invalid_num_rounds_rejected(self):
        for t in (0,41,-1,1.5,True):
            with self.assertRaises(ValueError):
                run((1,1,1,2),.5,0.,"NONE",t)

    def test_invalid_historical_coop_fraction_rejected(self):
        for x in (-.1,1.1,math.nan,math.inf):
            with self.assertRaises(ValueError):
                calculate_round((1,1,1,2),x,.5,"NONE")

    def test_fixed_known_witnesses_pass(self):
        z=fixed_synthetic_witnesses()
        self.assertEqual(z["P_one_N_four_fixed_monitoring"]["end_contributor_count"],5)
        self.assertEqual(z["P_one_D_four_variable_punishment"]["end_contributor_count"],1)

    def test_exact_full_factorial_672_conditions_and_5376_group_rounds(self):
        result=evaluate()
        self.assertEqual(result["status"],"E1_SYNTHETIC_NORM_INSTITUTION_MECHANISMS_PASS")
        self.assertEqual(result["full_factorial_cases"],EXPECTED_CASES)
        self.assertEqual(result["full_factorial_cases"],672)
        self.assertEqual(result["all_verified_group_rounds"],5376)
        for policy in INSTITUTIONS:
            self.assertEqual(len(result["aggregate"][policy]),4)
            for x in result["aggregate"][policy].values():
                self.assertEqual(x["cases"],56)
                self.assertEqual(x["round_count"],448)

    def test_seed_path_dependence_actual_not_labeled_causal_human(self):
        e=evaluate()
        self.assertGreater(
            e["initial_norm_path_dependence"][
                "theta=0.5,institution=NONE"]["distinct_compositions_with_different_final_outcome_by_seed"],
            0)
        self.assertEqual(e["causal_human_institutional_mechanisms"],"NOT_ESTABLISHED")

    def test_no_real_data_model_match_assumed_from_R047(self):
        q=evaluate()
        self.assertFalse(q["R047_CPR_extraction_direct_model_match"])
        self.assertEqual(q["E3_independent_new_cohort"],"OPEN")


if __name__=="__main__":
    unittest.main()
