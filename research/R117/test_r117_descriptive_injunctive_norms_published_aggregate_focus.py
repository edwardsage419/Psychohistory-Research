"""R117 author-published rounded aggregates and separately synthetic exact toy tests."""
import unittest
from decimal import Decimal
from fractions import Fraction as F

import r117_descriptive_injunctive_norms_published_aggregate_focus as m


class PrimaryAggregateAndNormFocus(unittest.TestCase):
    def test_primary_paper_1990_doi(self):
        self.assertEqual(m.PAPER_1990_DOI,"10.1037/0022-3514.58.6.1015")

    def test_primary_paper_2007_doi(self):
        self.assertEqual(m.PAPER_2007_DOI,"10.1111/j.1467-9280.2007.01917.x")

    def test_original_1990_figure_row_order(self):
        self.assertEqual(m.CELLS_1990,(
            ("clean_high_focus",31,6),
            ("clean_low_focus",50,14),
            ("littered_high_focus",24,54),
            ("littered_low_focus",34,32)))

    def test_original_1990_study1_denominator_139(self):
        self.assertEqual(m.published_1990_figure1_arithmetic()["total_published_study1_people"],139)

    def test_original_1990_figure_all_four_exact_printed_percent(self):
        rows=m.published_1990_figure1_arithmetic()["published_groups"]
        self.assertEqual([x["printed_rounded_littering_percent"] for x in rows],[6,14,54,32])

    def test_reconstructed_unique_integer_counts_carefully_labeled(self):
        rows=m.published_1990_figure1_arithmetic()["published_groups"]
        self.assertEqual([x["integer_litter_count_uniquely_inferred_from_printed_rounding"] for x in rows],
                         [2,7,13,11])

    def test_source_published_clean_salience_contrast_minus_eight(self):
        x=m.published_1990_figure1_arithmetic()
        self.assertEqual(x["clean_high_minus_low_focus_published_percentage_points"],-8)

    def test_source_published_littered_salience_contrast_plus_twenty_two(self):
        x=m.published_1990_figure1_arithmetic()
        self.assertEqual(x["littered_high_minus_low_focus_published_percentage_points"],22)

    def test_original_1990_published_rounded_interaction_thirty(self):
        x=m.published_1990_figure1_arithmetic()
        self.assertEqual(x["printed_rounded_interaction_difference_in_differences_percentage_points"],30)

    def test_inferred_original_count_interaction_not_forced_to_rounding_contrast(self):
        x=m.published_1990_figure1_arithmetic()
        exact=(F(13,24)-F(11,34))-(F(2,31)-F(7,50))
        self.assertEqual(F(x["uniquely_inferred_integer_count_interaction_fraction_exact"]),exact)
        self.assertNotEqual(exact,F(3,10))

    def test_1990_statistical_original_significance_not_independently_computed(self):
        x=m.published_1990_figure1_arithmetic()
        self.assertTrue(x["original_article_reports_interaction_significant"])
        self.assertTrue(x["original_article_says_two_within_environment_simple_contrasts_not_significant"])
        self.assertFalse(x["independent_SPSS_loglinear_significance_reproduced"])
        self.assertFalse(x["original_person_level_experiment_CSV_accessed"])

    def test_round_half_up_uses_exact_rationals(self):
        self.assertEqual(m.nearest_whole_percent(1,200),1)
        self.assertEqual(m.nearest_whole_percent(0,200),0)
        self.assertEqual(m.nearest_whole_percent(200,200),100)

    def test_published_percent_reversal_ambiguous_fail_closed(self):
        with self.assertRaisesRegex(m.NormFocusAuditError,"NOT_UNIQUE"):
            m.infer_unique_count_from_rounded_percent(1000,50)

    def test_published_percent_reversal_impossible_fail_closed(self):
        with self.assertRaisesRegex(m.NormFocusAuditError,"NOT_UNIQUE"):
            m.infer_unique_count_from_rounded_percent(1,50)

    def test_rounded_group_zero_denominator_rejected(self):
        with self.assertRaises(m.NormFocusAuditError):
            m.infer_unique_count_from_rounded_percent(0,0)
        with self.assertRaises(m.NormFocusAuditError):
            m.nearest_whole_percent(1,0)

    def test_integer_count_more_than_n_rejected(self):
        with self.assertRaises(m.NormFocusAuditError):
            m.nearest_whole_percent(4,3)

    def test_rounded_source_input_float_bool_negative_over_100_denied(self):
        for bad in (True,False,0.,-1,101,"54"):
            with self.subTest(bad=bad),self.assertRaises(m.NormFocusAuditError):
                m.infer_unique_count_from_rounded_percent(24,bad)

    def test_2007_four_original_group_sample_sizes(self):
        x=m.published_2007_short_term_arithmetic()
        self.assertEqual([v["reported_households_n"] for v in x["source_short_term_4_cells"]],
                         [64,79,63,81])

    def test_2007_sample_total_290_minus_3_equals_287(self):
        x=m.published_2007_short_term_arithmetic()
        self.assertEqual(x["initial_eligible_households_reported"],290)
        self.assertEqual(x["source_households_withdrew"],3)
        self.assertEqual(x["analyzed_households_reported"],287)
        self.assertEqual(290-3,x["analyzed_households_reported"])

    def test_2007_descriptive_high_energy_short_term_minus_1_22(self):
        rows=m.published_2007_short_term_arithmetic()["source_short_term_4_cells"]
        self.assertEqual((rows[0]["published_daily_kwh_baseline_mean"],
                          rows[0]["published_daily_kwh_short_followup_mean"],
                          rows[0]["simple_difference_of_published_rounded_means_kwh_day"]),
                         ("21.47","20.25","-1.22"))

    def test_2007_descriptive_low_energy_boomerang_plus_0_89(self):
        rows=m.published_2007_short_term_arithmetic()["source_short_term_4_cells"]
        self.assertEqual((rows[1]["published_daily_kwh_baseline_mean"],
                          rows[1]["published_daily_kwh_short_followup_mean"],
                          rows[1]["simple_difference_of_published_rounded_means_kwh_day"]),
                         ("10.38","11.27","0.89"))

    def test_2007_combined_high_energy_minus_1_72(self):
        rows=m.published_2007_short_term_arithmetic()["source_short_term_4_cells"]
        self.assertEqual((rows[2]["published_daily_kwh_baseline_mean"],
                          rows[2]["published_daily_kwh_short_followup_mean"],
                          rows[2]["simple_difference_of_published_rounded_means_kwh_day"]),
                         ("20.63","18.91","-1.72"))

    def test_2007_combined_low_energy_plus_0_24_no_significance_claim(self):
        x=m.published_2007_short_term_arithmetic()
        self.assertEqual(x["source_short_term_4_cells"][3]["simple_difference_of_published_rounded_means_kwh_day"],"0.24")
        self.assertTrue(x["descriptive_plus_injunctive_below_group_change_reported_not_significant"])
        self.assertFalse(x["independent_statistical_uncertainty_computed"])

    def test_2007_group_mean_differences_are_decimal_exact(self):
        for name,n,start,end in m.CELLS_2007:
            with self.subTest(name=name):
                diff=Decimal(end)-Decimal(start)
                displayed=next(x["simple_difference_of_published_rounded_means_kwh_day"]
                               for x in m.published_2007_short_term_arithmetic()["source_short_term_4_cells"]
                               if x["anonymous_source_published_cell"]==name)
                self.assertEqual(diff,Decimal(displayed))

    def test_2007_decimal_parser_rejects_unpinned_float_missing_invalid_format(self):
        for invalid in ("10.3","10.333",10.34,True,"nan","inf","-0.01","10","text"):
            with self.subTest(value=invalid),self.assertRaises(m.NormFocusAuditError):
                m._fixed_published_decimal(invalid)

    def test_toy_baseline_half_when_both_focus_flags_off(self):
        self.assertEqual(m.toy_prosocial_action_probability(F(1,5),F(9,10)),F(1,2))

    def test_toy_descriptive_low_group_share_reduces_prosocial_probability(self):
        self.assertEqual(m.toy_prosocial_action_probability(F(1,5),F(9,10),focus_descriptive=True),F(7,20))

    def test_toy_injunctive_approval_increases_prosocial_probability(self):
        self.assertEqual(m.toy_prosocial_action_probability(F(1,5),F(9,10),focus_injunctive=True),F(7,10))

    def test_toy_conflicting_cues_both_focus_give_eleventwentieths(self):
        self.assertEqual(m.toy_prosocial_action_probability(
            F(1,5),F(9,10),focus_descriptive=True,focus_injunctive=True),F(11,20))

    def test_toy_injunctive_addition_inhibits_descriptive_only_boomerang(self):
        base=m.toy_prosocial_action_probability(F(1,5),F(9,10))
        descriptive=m.toy_prosocial_action_probability(F(1,5),F(9,10),focus_descriptive=True)
        combined=m.toy_prosocial_action_probability(F(1,5),F(9,10),focus_descriptive=True,focus_injunctive=True)
        self.assertLess(descriptive,base)
        self.assertGreater(combined,base)

    def test_observational_equivalence_d_and_i_channels_same_norm_levels(self):
        d=m.toy_prosocial_action_probability(F(4,5),F(4,5),focus_descriptive=True)
        i=m.toy_prosocial_action_probability(F(4,5),F(4,5),focus_injunctive=True)
        self.assertEqual(d,i)
        self.assertEqual(d,F(13,20))

    def test_discordant_norms_break_same_observation_equivalence(self):
        d=m.toy_prosocial_action_probability(F(1,5),F(4,5),focus_descriptive=True)
        i=m.toy_prosocial_action_probability(F(1,5),F(4,5),focus_injunctive=True)
        self.assertEqual((d,i),(F(7,20),F(13,20)))

    def test_toy_exact_lower_upper_limits_not_clipped(self):
        self.assertEqual(m.toy_prosocial_action_probability(F(0),F(0),focus_descriptive=True,focus_injunctive=True),F(0))
        self.assertEqual(m.toy_prosocial_action_probability(F(1),F(1),focus_descriptive=True,focus_injunctive=True),F(1))

    def test_toy_unbounded_probability_cannot_be_silently_clipped(self):
        with self.assertRaisesRegex(m.NormFocusAuditError,"OUT_OF_RANGE"):
            m.toy_prosocial_action_probability(
                F(0),F(0),baseline=F(0),focus_descriptive=True,focus_injunctive=True)

    def test_toy_fraction_values_only_no_float_bool_string(self):
        for bad in (0.2,1,True,False,None,"1/5",F(-1,5),F(6,5)):
            with self.subTest(bad=bad),self.assertRaises(m.NormFocusAuditError):
                m.toy_prosocial_action_probability(bad,F(9,10))

    def test_toy_focus_flags_require_bool(self):
        for bad in (0,1,F(1),None,"True"):
            with self.subTest(bad=bad),self.assertRaises(m.NormFocusAuditError):
                m.toy_prosocial_action_probability(F(1,5),F(9,10),focus_descriptive=bad)
            with self.subTest(bad=bad),self.assertRaises(m.NormFocusAuditError):
                m.toy_prosocial_action_probability(F(1,5),F(9,10),focus_injunctive=bad)

    def test_toy_wrong_weight_or_baseline_types_and_values_rejected(self):
        for bad in (-F(1,5),F(6,5),.5,True):
            with self.subTest(bad=bad),self.assertRaises(m.NormFocusAuditError):
                m.toy_prosocial_action_probability(F(1,5),F(9,10),weight_descriptive=bad)
            with self.subTest(bad=bad),self.assertRaises(m.NormFocusAuditError):
                m.toy_prosocial_action_probability(F(1,5),F(9,10),baseline=bad)

    def test_reproducible_single_toy_and_published_aggregate_receipt(self):
        self.assertEqual(m.public_aggregate_and_toy_receipt(),m.public_aggregate_and_toy_receipt())

    def test_emitted_receipt_does_not_claim_raw_human_reanalysis(self):
        x=m.public_aggregate_and_toy_receipt()
        self.assertTrue(x["no_original_human_individual_rows"])
        self.assertEqual(x["new_original_human_E2_scores"],0)
        self.assertFalse(x["causal_normative_mechanism_newly_estimated"])
        self.assertTrue(x["source_1990_published_figure_arithmetic"]["original_person_level_experiment_CSV_accessed"] is False)
        self.assertTrue(x["source_2007_published_shortterm_arithmetic"]["household_original_meter_readings_CSV_accessed"] is False)


if __name__ == "__main__":
    unittest.main()
