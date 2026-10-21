"""R166 actual exact unittest controls for finite synthetic selection and change."""
import json
import sys
import unittest
from pathlib import Path
from fractions import Fraction as F

from r166_cultural_selection_transformation_exact import (
    N_GRID,START_K,REGIMES,MECHANISMS,HORIZON,checked,
    child_probability,child_probability_oracle,kernel,enumerated_kernel,
    path,independent_path,mean_frequency,total_variation,result_document
)

class TestR166(unittest.TestCase):
    def check_world(self,ni,ki,ri,mi):
        n=N_GRID[ni]
        k=START_K[ni][ki]
        mech=MECHANISMS[mi]
        a=path(n,k,ri,mech)
        b=independent_path(n,k,ri,mech)
        self.assertEqual(a,b)
        self.assertEqual(len(a),5)
        self.assertEqual(a[0][k],1)
        self.assertEqual(a[1],kernel(n,ri,mech)[k])
        self.assertEqual(kernel(n,ri,mech),enumerated_kernel(n,ri,mech))
        for dist in a:
            self.assertEqual(sum(dist),F(1))
            self.assertEqual(len(dist),n+1)
            self.assertTrue(all(isinstance(x,F) and 0<=x<=1 for x in dist))
            self.assertTrue(0<=mean_frequency(dist,n)<=1)
        if ri==0:
            self.assertTrue(all(mean_frequency(d,n)==F(k,n) for d in a))
        if mech=="selection" and k in (0,n):
            self.assertEqual(a,(a[0],)*5)

    def test_fixed_48_worlds(self):
        self.assertEqual(len(N_GRID)*4*len(REGIMES)*len(MECHANISMS),48)

    def test_frozen_regime_definitions(self):
        self.assertEqual(REGIMES[0],("neutral",1,1,F(0),F(0)))
        self.assertEqual(REGIMES[1],("toward_A",2,1,F(1,3),F(0)))
        self.assertEqual(REGIMES[2],("toward_B",1,2,F(0),F(1,3)))

    def test_binary_parameters_are_exact_fractions(self):
        for n in N_GRID:
            for ri in range(3):
                for mech in MECHANISMS:
                    for k in range(n+1):
                        self.assertIsInstance(child_probability(n,k,ri,mech),F)
                        self.assertIsInstance(child_probability_oracle(n,k,ri,mech),F)

    def test_two_child_probability_oracles_equal(self):
        for n in N_GRID:
            for ri in range(3):
                for mech in MECHANISMS:
                    for k in range(n+1):
                        self.assertEqual(child_probability(n,k,ri,mech),
                                         child_probability_oracle(n,k,ri,mech))

    def test_p_half_favor_A_mechanisms_equal_at_first_step(self):
        for n in N_GRID:
            self.assertEqual(child_probability(n,n//2,1,"selection"),F(2,3))
            self.assertEqual(child_probability(n,n//2,1,"transformation"),F(2,3))
            self.assertEqual(kernel(n,1,"selection")[n//2],
                             kernel(n,1,"transformation")[n//2])

    def test_p_half_favor_B_mechanisms_equal_at_first_step(self):
        for n in N_GRID:
            self.assertEqual(child_probability(n,n//2,2,"selection"),F(1,3))
            self.assertEqual(child_probability(n,n//2,2,"transformation"),F(1,3))
            self.assertEqual(kernel(n,2,"selection")[n//2],
                             kernel(n,2,"transformation")[n//2])

    def test_at_quarter_mechanisms_separate(self):
        for n,k in ((4,1),(8,2)):
            self.assertEqual(child_probability(n,k,1,"selection"),F(2,5))
            self.assertEqual(child_probability(n,k,1,"transformation"),F(1,2))
            self.assertNotEqual(kernel(n,1,"selection")[k],
                                kernel(n,1,"transformation")[k])

    def test_A_transformation_creates_missing_A_but_selection_does_not(self):
        for n in N_GRID:
            self.assertEqual(child_probability(n,0,1,"selection"),0)
            self.assertEqual(child_probability(n,0,1,"transformation"),F(1,3))

    def test_B_transformation_creates_missing_B_but_selection_does_not(self):
        for n in N_GRID:
            self.assertEqual(child_probability(n,n,2,"selection"),1)
            self.assertEqual(child_probability(n,n,2,"transformation"),F(2,3))

    def test_selection_preserves_absorbing_boundaries(self):
        for n in N_GRID:
            for ri in range(3):
                m=kernel(n,ri,"selection")
                self.assertEqual(m[0][0],1)
                self.assertEqual(m[n][n],1)

    def test_directed_A_transformation_opposite_endpoint_nonabsorbing(self):
        for n in N_GRID:
            m=kernel(n,1,"transformation")
            self.assertLess(m[0][0],1)
            self.assertEqual(m[n][n],1)

    def test_directed_B_transformation_opposite_endpoint_nonabsorbing(self):
        for n in N_GRID:
            m=kernel(n,2,"transformation")
            self.assertEqual(m[0][0],1)
            self.assertLess(m[n][n],1)

    def test_neutral_selection_and_transformation_identical(self):
        for n in N_GRID:
            self.assertEqual(kernel(n,0,"selection"),kernel(n,0,"transformation"))
            for k in range(n+1):
                self.assertEqual(path(n,k,0,"selection"),path(n,k,0,"transformation"))

    def test_neutral_matches_R165_archived_baseline(self):
        other=Path(__file__).resolve().parents[1]/"R165"
        self.assertTrue((other/"r165_neutral_drift_exact.py").exists())
        sys.path.insert(0,str(other))
        from r165_neutral_drift_exact import kernel as neutral_kernel
        for n in N_GRID:
            self.assertEqual(kernel(n,0,"selection"),neutral_kernel(n,F(0)))

    def test_binomial_rows_normalized(self):
        for n in N_GRID:
            for ri in range(3):
                for mech in MECHANISMS:
                    for row in kernel(n,ri,mech):
                        self.assertEqual(sum(row),1)
                        self.assertTrue(all(0<=x<=1 for x in row))

    def test_two_complete_transition_kernels_match(self):
        for n in N_GRID:
            for ri in range(3):
                for mech in MECHANISMS:
                    self.assertEqual(kernel(n,ri,mech),enumerated_kernel(n,ri,mech))

    def test_first_step_expected_frequency_equals_q(self):
        for n in N_GRID:
            for k in range(n+1):
                for ri in range(3):
                    for mech in MECHANISMS:
                        self.assertEqual(mean_frequency(kernel(n,ri,mech)[k],n),
                                         child_probability(n,k,ri,mech))

    def test_time1_full_distribution_unidentifiable_at_half(self):
        for n in N_GRID:
            for ri in (1,2):
                self.assertEqual(path(n,n//2,ri,"selection")[1],
                                 path(n,n//2,ri,"transformation")[1])

    def test_time2_full_distribution_differs_at_half(self):
        for n in N_GRID:
            for ri in (1,2):
                self.assertNotEqual(path(n,n//2,ri,"selection")[2],
                                    path(n,n//2,ri,"transformation")[2])

    def test_total_variation_positive_at_time2(self):
        a=path(4,2,1,"selection")
        b=path(4,2,1,"transformation")
        self.assertEqual(total_variation(a[1],b[1]),0)
        self.assertGreater(total_variation(a[2],b[2]),0)

    def test_total_variation_symmetric(self):
        a=path(8,4,1,"selection")[2]
        b=path(8,4,1,"transformation")[2]
        self.assertEqual(total_variation(a,b),total_variation(b,a))

    def test_reflection_of_selection_A_B_regimes(self):
        for n in N_GRID:
            for k in range(n+1):
                a=path(n,k,1,"selection")
                b=path(n,n-k,2,"selection")
                self.assertEqual(tuple(tuple(reversed(x)) for x in a),b)

    def test_reflection_of_transformation_A_B_regimes(self):
        for n in N_GRID:
            for k in range(n+1):
                a=path(n,k,1,"transformation")
                b=path(n,n-k,2,"transformation")
                self.assertEqual(tuple(tuple(reversed(x)) for x in a),b)

    def test_neutral_mean_a_martingale(self):
        for n in N_GRID:
            for k in range(n+1):
                for mech in MECHANISMS:
                    self.assertTrue(all(mean_frequency(x,n)==F(k,n)
                                    for x in path(n,k,0,mech)))

    def test_A_favoring_q_greater_than_p_in_interior(self):
        for n in N_GRID:
            for k in range(1,n):
                for mech in MECHANISMS:
                    self.assertGreater(child_probability(n,k,1,mech),F(k,n))

    def test_B_favoring_q_less_than_p_in_interior(self):
        for n in N_GRID:
            for k in range(1,n):
                for mech in MECHANISMS:
                    self.assertLess(child_probability(n,k,2,mech),F(k,n))

    def test_invalid_population(self):
        for n in (0,1,5,7,False,True,4.0,"4"):
            with self.assertRaises(ValueError): checked(n,0,0,"selection")

    def test_invalid_count(self):
        for k in (-1,9,True,False,F(1,2),0.5,"2"):
            with self.assertRaises(ValueError): checked(8,k,0,"selection")

    def test_invalid_regime(self):
        for regime in (-1,3,True,False,F(1,2),0.0,"1"):
            with self.assertRaises(ValueError): checked(4,2,regime,"selection")

    def test_invalid_mechanism(self):
        for mechanism in ("sel","mutation",True,False,None,0):
            with self.assertRaises(ValueError): checked(4,2,0,mechanism)

    def test_invalid_horizon(self):
        for v in (-1,False,True,F(1,2),3.0,"4"):
            with self.assertRaises(ValueError): path(4,2,0,"selection",v)
            with self.assertRaises(ValueError): independent_path(4,2,0,"selection",v)

    def test_invalid_total_variation_vectors(self):
        with self.assertRaises(ValueError): total_variation((F(1),),(F(1),F(0)))
        with self.assertRaises(ValueError): total_variation((F(0),F(0)),(F(1),F(0)))

    def test_R019_and_author_original_not_misrepresented(self):
        d=result_document()
        self.assertTrue(d["R019_is_not_selection_theory"])
        self.assertFalse(d["original_Mesoudi_2021_EMG_model_reproduced"])
        self.assertFalse(d["original_human_cultural_data_used"])

    def test_full_ledger_48_worlds_and_12_kernels(self):
        d=result_document()
        self.assertEqual(d["number_of_worlds"],48)
        self.assertEqual(d["total_kernel_count"],12)
        self.assertEqual(len(d["worlds"]),48)
        self.assertEqual(len(d["kernels"]),12)
        self.assertEqual(len({w["id"] for w in d["worlds"]}),48)
        self.assertTrue(all(len(w["points"])==5 for w in d["worlds"]))
        self.assertTrue(all(w["independent_exact_oracles_equal"] for w in d["worlds"]))

    def test_frozen_counterexamples(self):
        c=result_document()["counterexamples"]
        self.assertEqual(c["p_half_A_favored_both_one_step_q"],"2/3")
        self.assertEqual(c["p_half_B_favored_both_one_step_q"],"1/3")
        self.assertEqual(c["p_quarter_A_selection_one_step_q"],"2/5")
        self.assertEqual(c["p_quarter_A_transformation_one_step_q"],"1/2")
        self.assertTrue(c["N4_half_A_t1_complete_kernel_equal"])
        self.assertGreater(F(c["N4_half_A_t2_total_variation"]),0)

    def test_complete_saved_json_byte_replay(self):
        p=Path(__file__).with_name("R166_EXACT_RESULTS.json")
        if not p.exists(): self.skipTest("CI generates canonical JSON before unittest run")
        self.assertEqual(p.read_bytes(),
            (json.dumps(result_document(),indent=2,sort_keys=True,ensure_ascii=False)+"\n").encode())


for ni in range(len(N_GRID)):
    for ki in range(len(START_K[ni])):
        for ri in range(len(REGIMES)):
            for mi in range(len(MECHANISMS)):
                def builder(ni=ni,ki=ki,ri=ri,mi=mi):
                    def test(self): self.check_world(ni,ki,ri,mi)
                    return test
                setattr(TestR166,f"test_frozen_n{ni}_k{ki}_r{ri}_m{mi}",builder())


if __name__=="__main__":
    unittest.main()
