"""R114 independently check pure synthetic factorial math; NO human records."""
import math
import unittest
from dataclasses import FrozenInstanceError

import r114_conditional_norm_compliance_discordant_expectations as m


class FrozenConditionalNormFactorial(unittest.TestCase):
    def test_logistic_zero_is_half(self):
        self.assertEqual(m.logistic(0), 0.5)

    def test_logistic_negative_positive_symmetry(self):
        for v in (.2,1,10,40):
            self.assertAlmostEqual(m.logistic(v)+m.logistic(-v),1,places=14)

    def test_logistic_extreme_finite_logodds_stable(self):
        self.assertEqual(m.logistic(1000),1)
        self.assertEqual(m.logistic(-1000),0)

    def test_logistic_monotonicity(self):
        self.assertLess(m.logistic(-1),m.logistic(0))
        self.assertLess(m.logistic(0),m.logistic(1))

    def test_logistic_rejects_nan_infinite_bool_text(self):
        for x in (True,False,"1",float("nan"),float("inf"),-float("inf")):
            with self.subTest(x=x),self.assertRaises(m.NormMechanismError):
                m.logistic(x)

    def test_interior_logit_inverse(self):
        for z in (-4,-1,0,2,4):
            self.assertAlmostEqual(m.logit(m.logistic(z)),z,places=12)

    def test_logit_rejects_boundary_and_nonprobabilities(self):
        for p in (0,1,-1,2,True,"0.5",float("nan"),float("inf")):
            with self.subTest(p=p),self.assertRaises(m.NormMechanismError):
                m.logit(p)

    def test_logit_tiny_interior_remains_finite(self):
        self.assertTrue(math.isfinite(m.logit(1e-200)))
        self.assertAlmostEqual(m.logit(.5),0)

    def test_parameters_validation(self):
        for bad in (True,"1",float("nan"),float("inf"),-float("inf")):
            with self.subTest(bad=bad),self.assertRaises(m.NormMechanismError):
                m.SyntheticBeliefModel(bad,0,0,0)

    def test_params_immutable_after_construction(self):
        model=m.SyntheticBeliefModel(-1,2,0,0)
        with self.assertRaises(FrozenInstanceError):
            model.intercept=1

    def test_belief_inputs_must_be_exact_integer_zero_one(self):
        model=m.MODELS["DESCRIPTIVE"]
        for v in (True,False,0.0,1.0,-1,2,"1",None,float("nan")):
            with self.subTest(v=v),self.assertRaises(m.NormMechanismError):
                model.probability(v,1)
            with self.subTest(v=v),self.assertRaises(m.NormMechanismError):
                model.probability(1,v)

    def test_four_named_cells_and_finite_probabilities(self):
        for model in m.MODELS.values():
            grid=model.grid()
            self.assertEqual(set(grid),set(m.CELLS))
            self.assertTrue(all(0<p<1 for p in grid.values()))

    def test_model_definitions_exact_preregistered_coefficients(self):
        params={
            "DESCRIPTIVE":(-1,2,0,0),
            "NORMATIVE_ONLY":(-1,0,2,0),
            "BOTH_ADDITIVE":(-1,1,1,0),
            "INTERACTION":(-1,1,1,1),
        }
        for name,values in params.items():
            model=m.MODELS[name]
            self.assertEqual((model.intercept,model.empirical_effect,
                              model.normative_effect,model.interaction_effect),values)

    def test_aligned_low_worlds_indistinguishable(self):
        a=m.MODELS["DESCRIPTIVE"].grid()
        b=m.MODELS["NORMATIVE_ONLY"].grid()
        self.assertEqual(a["E0N0"],b["E0N0"])

    def test_aligned_high_worlds_indistinguishable(self):
        a=m.MODELS["DESCRIPTIVE"].grid()
        b=m.MODELS["NORMATIVE_ONLY"].grid()
        self.assertEqual(a["E1N1"],b["E1N1"])

    def test_E_high_N_low_breaks_equivalence(self):
        a=m.MODELS["DESCRIPTIVE"].grid()
        b=m.MODELS["NORMATIVE_ONLY"].grid()
        self.assertGreater(a["E1N0"],b["E1N0"])

    def test_E_low_N_high_opposite_direction(self):
        a=m.MODELS["DESCRIPTIVE"].grid()
        b=m.MODELS["NORMATIVE_ONLY"].grid()
        self.assertLess(a["E0N1"],b["E0N1"])

    def test_descriptive_model_is_independent_of_normative_belief(self):
        a=m.MODELS["DESCRIPTIVE"]
        for e in (0,1):
            self.assertEqual(a.probability(e,0),a.probability(e,1))

    def test_normative_only_model_is_independent_of_empirical_belief(self):
        a=m.MODELS["NORMATIVE_ONLY"]
        for n in (0,1):
            self.assertEqual(a.probability(0,n),a.probability(1,n))

    def test_additive_both_model_has_half_probabilities_at_discordant_cells(self):
        g=m.MODELS["BOTH_ADDITIVE"].grid()
        self.assertEqual(g["E1N0"],0.5)
        self.assertEqual(g["E0N1"],0.5)

    def test_additive_both_responds_to_each_expectation_alone(self):
        a=m.MODELS["BOTH_ADDITIVE"]
        self.assertGreater(a.probability(1,0),a.probability(0,0))
        self.assertGreater(a.probability(0,1),a.probability(0,0))

    def test_three_no_interaction_models_exact_zero_contrast(self):
        for name in ("DESCRIPTIVE","NORMATIVE_ONLY","BOTH_ADDITIVE"):
            self.assertAlmostEqual(m.log_odds_interaction_contrast(m.MODELS[name].grid()),0,places=12)

    def test_interaction_model_exact_one_logodds_interaction(self):
        self.assertAlmostEqual(m.log_odds_interaction_contrast(m.MODELS["INTERACTION"].grid()),1,places=12)

    def test_all_four_cells_recover_preregistered_coefficients(self):
        for model in m.MODELS.values():
            recovered=m.exact_factorial_logit_coefficients(model.grid())
            self.assertAlmostEqual(recovered.intercept,model.intercept,places=12)
            self.assertAlmostEqual(recovered.empirical_effect,model.empirical_effect,places=12)
            self.assertAlmostEqual(recovered.normative_effect,model.normative_effect,places=12)
            self.assertAlmostEqual(recovered.interaction_effect,model.interaction_effect,places=12)

    def test_missing_cell_cannot_identify_unrestricted_interaction(self):
        incomplete=m.MODELS["INTERACTION"].grid()
        del incomplete["E0N1"]
        with self.assertRaisesRegex(m.NormMechanismError,"FOUR"):
            m.exact_factorial_logit_coefficients(incomplete)

    def test_unexpected_cell_or_wrong_container_is_rejected(self):
        extra=m.MODELS["INTERACTION"].grid()
        extra["E9N9"]=0.5
        with self.assertRaises(m.NormMechanismError):
            m.exact_factorial_logit_coefficients(extra)
        with self.assertRaises(m.NormMechanismError):
            m.exact_factorial_logit_coefficients(list(extra.values()))

    def test_invalid_probability_cell_fails_closed(self):
        for bad in (0,1,-1,2,True,float("nan"),"0.5"):
            cells=m.MODELS["BOTH_ADDITIVE"].grid()
            cells["E1N0"]=bad
            with self.subTest(bad=bad),self.assertRaises(m.NormMechanismError):
                m.exact_factorial_logit_coefficients(cells)

    def test_counterexample_same_diagonal_and_discordant_difference(self):
        x=m.aligned_conditions_counterexample()
        self.assertTrue(x["aligned_E0N0_identical"])
        self.assertTrue(x["aligned_E1N1_identical"])
        self.assertNotEqual(x["discordant_E1N0_descriptive"],x["discordant_E1N0_normative"])
        self.assertNotEqual(x["discordant_E0N1_descriptive"],x["discordant_E0N1_normative"])

    def test_no_claims_of_human_estimation_or_causal_effect(self):
        out=m.factorial_math_receipt()
        self.assertTrue(out["toy_model_is_authored_here_not_in_primary_paper"])
        self.assertEqual(out["observed_real_human_choices"],0)
        self.assertEqual(out["estimated_human_psychological_coefficients"],0)
        self.assertFalse(out["causal_norm_effect_demonstrated"])
        self.assertEqual(out["PESEN_v0_1"],"FROZEN")

    def test_repeatable_machine_model_output(self):
        self.assertEqual(m.factorial_math_receipt(),m.factorial_math_receipt())


if __name__=="__main__":
    unittest.main()
