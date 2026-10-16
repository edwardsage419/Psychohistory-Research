"""R068 heldout genuine 4-choice frequency predictor, synthetic tests only."""
import math,unittest
import r068_frequency_room_loro as m

class SocialFrequencyModelTests(unittest.TestCase):
    def test_uniform_probability(self):
        self.assertEqual(m.predict_probs("uniform",0,(1,2,3,4),{}),[.25]*4)

    def test_theta_zero_uniform(self):
        self.assertEqual(m.predict_probs("frequency_exponent",0,(1,2,3,4),{"theta":0.}),[.25]*4)

    def test_theta_one_matches_smoothed_linear_sampling(self):
        p=m.predict_probs("frequency_exponent",0,(1,2,3,4),{"theta":1.})
        self.assertAlmostEqual(p[3],4.1/10.4)
        self.assertAlmostEqual(sum(p),1)

    def test_theta_four_prefers_more_common(self):
        a=m.predict_probs("frequency_exponent",0,(1,2,3,4),{"theta":1.})
        b=m.predict_probs("frequency_exponent",0,(1,2,3,4),{"theta":4.})
        self.assertGreater(b[3],a[3])

    def test_inertia_zero_uniform(self):
        self.assertEqual(m.predict_probs("inertia",1,(1,0,0,0),{"rho":0.}),[.25]*4)

    def test_inertia_preserves_last_option_more(self):
        p=m.predict_probs("inertia",2,(1,1,1,1),{"rho":.9})
        self.assertGreater(p[2],p[1])

    def test_mixture_is_convex_combination(self):
        inp=(0,1,3,2)
        mix=m.predict_probs("inertia_frequency_mixture",0,inp,
                            {"rho":.5,"theta":2.,"weight":.25})
        inertia=m.predict_probs("inertia",0,inp,{"rho":.5})
        social=m.predict_probs("frequency_exponent",0,inp,{"theta":2.})
        for j in range(4):
            self.assertAlmostEqual(mix[j],.75*inertia[j]+.25*social[j])

    def test_every_candidate_strictly_inside_simplex(self):
        for family in m.FAMILIES:
            for name,params in m.params(family):
                probs=m.predict_probs(family,2,(0,0,2,1),params)
                self.assertTrue(all(0<p<1 for p in probs),(family,name))
                self.assertAlmostEqual(sum(probs),1)

    def test_frozen_candidate_counts(self):
        self.assertEqual([len(m.params(x)) for x in m.FAMILIES],[1,5,5,48])

    def test_negative_counts_fail(self):
        with self.assertRaises(ValueError):
            m.predict_probs("frequency_exponent",0,(-1,2,0,1),{"theta":1.})

    def test_all_zero_no_exposure_rejected(self):
        with self.assertRaises(ValueError):
            m.predict_probs("frequency_exponent",0,(0,0,0,0),{"theta":1.})

    def test_invalid_param_grid_rejected(self):
        with self.assertRaises(ValueError):
            m.predict_probs("frequency_exponent",0,(1,2,3,0),{"theta":3.})

    def test_invalid_option_code_rejected(self):
        with self.assertRaises(ValueError):
            m.predict_probs("frequency_exponent",4,(1,2,3,0),{"theta":1.})

    def test_heldout_outcome_cannot_change_model_choice(self):
        candidates={"theta=1":{"ROOM_A":1,"ROOM_B":2,"ROOM_C":3},
                    "theta=2":{"ROOM_A":2,"ROOM_B":1,"ROOM_C":-100}}
        a=m.choose_other_rooms(candidates,"ROOM_C")
        candidates["theta=2"]["ROOM_C"]=1000
        b=m.choose_other_rooms(candidates,"ROOM_C")
        self.assertEqual(a,b)

    def test_tie_choose_first_in_frozen_order(self):
        candidates={"first":{"ROOM_A":1,"ROOM_B":2},
                    "second":{"ROOM_A":1,"ROOM_B":2}}
        self.assertEqual(m.choose_other_rooms(candidates,"ROOM_A"),"first")

    def test_score_requires_all_rooms(self):
        with self.assertRaises(ValueError):
            m.score_rooms({},{})

    def test_unsupported_family_not_treated_as_success(self):
        with self.assertRaises(ValueError):
            m.params("invented")

    def test_truncated_experimental_source_cannot_be_scoreable(self):
        with self.assertRaises(OSError):
            m.evaluate(__import__("pathlib").Path("/not/a/real/R068/source"))

if __name__=="__main__":
    unittest.main()
