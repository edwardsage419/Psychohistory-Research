"""R152 real tests: 54 distinct full-param settings, non-identifiability, guards."""
import unittest
from fractions import Fraction as F
from itertools import product
import json
import r152_gravity_od_exact as m

class TestR152(unittest.TestCase):
    def test_001_declared_54_scenarios(self):
        self.assertEqual(len(list(m.ordered_scenarios())),54)
        self.assertEqual(len(set(m.ordered_scenarios())),54)

    def test_002_documented_city_population(self):
        self.assertEqual(m.POPULATIONS,(2,3,5,7))

    def test_003_near_location_grid(self):
        self.assertEqual(m.LAYOUTS["near"],(0,1,3,6))

    def test_004_far_grid(self):
        self.assertEqual(m.LAYOUTS["far"],(0,1,3,9))

    def test_005_origin_budget_tenth(self):
        self.assertEqual(m.outflows(m.POPULATIONS,"pop_10"),(F(1,5),F(3,10),F(1,2),F(7,10)))

    def test_006_origin_budget_fifth(self):
        self.assertEqual(m.outflows(m.POPULATIONS,"pop_5"),(F(2,5),F(3,5),F(1),F(7,5)))

    def test_007_origin_budget_half(self):
        self.assertEqual(m.outflows(m.POPULATIONS,"half"),(F(1,2),)*4)

    def test_008_source_budget_doubles_matrix(self):
        for layout,alpha,attraction in product(m.LAYOUTS,m.EXPONENTS,m.ATTRACTIONS):
            a=m.flows_direct(m.POPULATIONS,m.LAYOUTS[layout],m.ATTRACTIONS[attraction],alpha,"pop_10")
            b=m.flows_direct(m.POPULATIONS,m.LAYOUTS[layout],m.ATTRACTIONS[attraction],alpha,"pop_5")
            self.assertEqual(tuple(tuple(2*x for x in row) for row in a),b)

    def test_009_source_budget_doubles_probabilities_unchanged(self):
        a=m.scenario("near",2,"flat","pop_10")
        b=m.scenario("near",2,"flat","pop_5")
        self.assertEqual(a["route_probabilities"],b["route_probabilities"])

    def test_010_zero_exponent_location_invariance(self):
        for attractiveness,budget in product(m.ATTRACTIONS,m.BUDGETS):
            near=m.scenario("near",0,attractiveness,budget)
            far=m.scenario("far",0,attractiveness,budget)
            self.assertEqual(near["flow_matrix"],far["flow_matrix"])

    def test_011_zero_exponent_unweighted_distance_metric_varies(self):
        a=m.scenario("near",0,"flat","pop_10")
        b=m.scenario("far",0,"flat","pop_10")
        self.assertNotEqual(a["mean_distance_weighted_by_flow"],b["mean_distance_weighted_by_flow"])

    def test_012_positive_exponent_move_last_city_farther_reduces_last_share(self):
        for alpha,attract,budget in product((1,2),m.ATTRACTIONS,m.BUDGETS):
            near=m.scenario("near",alpha,attract,budget)
            far=m.scenario("far",alpha,attract,budget)
            for i in (0,1,2):
                self.assertGreater(F(near["route_probabilities"][i][3]),F(far["route_probabilities"][i][3]))

    def test_013_increase_last_attractiveness_increases_share(self):
        for layout,alpha,budget in product(m.LAYOUTS,m.EXPONENTS,m.BUDGETS):
            regular=m.scenario(layout,alpha,"flat",budget)
            extra=m.scenario(layout,alpha,"last_bonus",budget)
            for i in (0,1,2):
                self.assertGreater(F(extra["route_probabilities"][i][3]),F(regular["route_probabilities"][i][3]))

    def test_014_increase_middle_attractiveness_increases_share(self):
        for layout,alpha,budget in product(m.LAYOUTS,m.EXPONENTS,m.BUDGETS):
            regular=m.scenario(layout,alpha,"flat",budget)
            extra=m.scenario(layout,alpha,"mid_bonus",budget)
            for i in (0,1,3):
                self.assertGreater(F(extra["route_probabilities"][i][2]),F(regular["route_probabilities"][i][2]))

    def test_015_self_migration_zero(self):
        for v in m.ordered_scenarios():
            x=m.scenario(*v)
            for i in range(4):
                self.assertEqual(F(x["flow_matrix"][i][i]),0)

    def test_016_every_origin_share_sums_to_one(self):
        for v in m.ordered_scenarios():
            x=m.scenario(*v)
            self.assertTrue(all(sum(map(F,row))==1 for row in x["route_probabilities"]))

    def test_017_flow_conservation_all_54(self):
        for v in m.ordered_scenarios():
            x=m.scenario(*v)
            self.assertEqual(sum(map(F,x["row_outflow"])),
                             sum(map(F,x["destination_inflow"])))

    def test_018_direct_integer_two_implementations_all_54(self):
        for layout,alpha,attr,budget in m.ordered_scenarios():
            cfg=(m.POPULATIONS,m.LAYOUTS[layout],m.ATTRACTIONS[attr],alpha,budget)
            self.assertEqual(m.flows_direct(*cfg),m.flows_integer_route(*cfg))

    def test_019_output_contains_complete_cases(self):
        o=m.output()
        self.assertEqual(o["scenarios_count"],54)
        self.assertEqual(len(o["scenarios"]),54)
        self.assertTrue(all(len(r["flow_matrix"])==4 for r in o["scenarios"]))

    def test_020_no_real_histories_claimed(self):
        z=m.output()
        self.assertTrue(z["all_project_synthetic"])
        self.assertFalse(z["historical_migration_data_replayed"])
        self.assertEqual((z["new_E2"],z["new_E3"]),(0,0))

    def test_021_zipf_kernel_symmetric(self):
        for alpha in m.EXPONENTS:
            k=m.raw_gravity(m.POPULATIONS,m.LAYOUTS["near"],alpha)
            for i in range(4):
                for j in range(4):
                    self.assertEqual(k[i][j],k[j][i])

    def test_022_zipf_raw_not_equal_origin_budget(self):
        k=m.raw_gravity(m.POPULATIONS,m.LAYOUTS["near"],1)
        self.assertNotEqual(sum(k[0]),m.outflows(m.POPULATIONS,"pop_10")[0])

    def test_023_alpha1_k01_equals_population_product(self):
        self.assertEqual(m.raw_gravity(m.POPULATIONS,m.LAYOUTS["near"],1)[0][1],6)

    def test_024_alpha2_k02_correct(self):
        self.assertEqual(m.raw_gravity(m.POPULATIONS,m.LAYOUTS["near"],2)[0][2],F(10,9))

    def test_025_directional_tables_enumeration_exact_two(self):
        self.assertEqual(len(m.od_exact_tables_enumeration()),2)

    def test_026_directional_tables_independent_symbolic_same(self):
        self.assertEqual(m.od_exact_tables_enumeration(),m.od_exact_tables_symbolic())

    def test_027_OD_total_nine(self):
        for tab in m.od_exact_tables_enumeration():
            self.assertEqual(sum(map(sum,tab)),9)

    def test_028_OD_identical_margins(self):
        for tab in m.od_exact_tables_enumeration():
            self.assertEqual(tuple(map(sum,tab)),(2,3,4))
            self.assertEqual(tuple(sum(tab[i][j] for i in range(3)) for j in range(3)),(2,3,4))

    def test_029_two_tables_distinct_directions(self):
        a,b=m.od_exact_tables_enumeration()
        self.assertNotEqual(a,b)

    def test_030_two_tables_equal_symmetric_pair_sums(self):
        a,b=m.od_exact_tables_enumeration()
        self.assertEqual(m.od_undirected_pair_totals(a),m.od_undirected_pair_totals(b))
        self.assertEqual(m.od_undirected_pair_totals(a),(1,3,5))

    def test_031_gravity_scores_equal_every_exponent(self):
        a,b=m.od_exact_tables_enumeration()
        for alpha in m.EXPONENTS:
            self.assertEqual(m.od_score(a,alpha),m.od_score(b,alpha))

    def test_032_asymmetric_direction_bonus_diverges(self):
        a,b=m.od_exact_tables_enumeration()
        self.assertNotEqual(m.od_direction_reward(a),m.od_direction_reward(b))
        self.assertEqual(set((m.od_direction_reward(a),m.od_direction_reward(b))),{16,32})

    def test_033_score_alpha0_positive(self):
        self.assertGreater(m.od_score(m.od_exact_tables_enumeration()[0],0),0)

    def test_034_od_symbolic_no_self(self):
        for tab in m.od_exact_tables_symbolic():
            self.assertTrue(all(tab[i][i]==0 for i in range(3)))

    def test_035_canonical_json_deterministic(self):
        self.assertEqual(m.canonical_json(),m.canonical_json())

    def test_036_json_parse_replay(self):
        d=json.loads(m.canonical_json())
        self.assertEqual(d["scenarios_count"],54)

    def test_037_different_exponents_matter(self):
        x=m.scenario("near",0,"flat","pop_10")
        y=m.scenario("near",2,"flat","pop_10")
        self.assertNotEqual(x["flow_matrix"],y["flow_matrix"])

    def test_038_budget_invalid(self):
        with self.assertRaises(ValueError):m.outflows(m.POPULATIONS,"bad")

    def test_039_population_zero_rejected(self):
        with self.assertRaises(ValueError):m.population_vector((2,0,5,7))

    def test_040_population_negative_rejected(self):
        with self.assertRaises(ValueError):m.population_vector((-2,3,5,7))

    def test_041_population_bool_rejected(self):
        with self.assertRaises(TypeError):m.population_vector((True,3,5,7))

    def test_042_population_float_rejected(self):
        with self.assertRaises(TypeError):m.population_vector((2.0,3,5,7))

    def test_043_population_length_rejected(self):
        with self.assertRaises(ValueError):m.population_vector((2,3,5))

    def test_044_coords_duplicate_rejected(self):
        with self.assertRaises(ValueError):m.positions((0,0,3,6))

    def test_045_coords_float_rejected(self):
        with self.assertRaises(TypeError):m.positions((0,1.0,3,6))

    def test_046_coords_bool_rejected(self):
        with self.assertRaises(TypeError):m.positions((False,1,3,6))

    def test_047_coords_length_rejected(self):
        with self.assertRaises(ValueError):m.positions((0,1,3))

    def test_048_attraction_zero_rejected(self):
        with self.assertRaises(ValueError):m.attraction_vector((1,0,1,1))

    def test_049_attraction_negative_rejected(self):
        with self.assertRaises(ValueError):m.attraction_vector((1,1,-2,1))

    def test_050_attraction_float_rejected(self):
        with self.assertRaises(TypeError):m.attraction_vector((1,1,1.0,1))

    def test_051_attraction_bool_rejected(self):
        with self.assertRaises(TypeError):m.attraction_vector((1,1,True,1))

    def test_052_alpha_negative_rejected(self):
        with self.assertRaises(ValueError):m.exponent(-1)

    def test_053_alpha_excess_rejected(self):
        with self.assertRaises(ValueError):m.exponent(3)

    def test_054_alpha_bool_rejected(self):
        with self.assertRaises(TypeError):m.exponent(True)

    def test_055_alpha_float_rejected(self):
        with self.assertRaises(TypeError):m.exponent(1.0)

    def test_056_self_distance_rejected(self):
        with self.assertRaises(ValueError):m.distance(m.LAYOUTS["near"],1,1)

    def test_057_city_index_negative_rejected(self):
        with self.assertRaises(ValueError):m.distance(m.LAYOUTS["near"],-1,1)

    def test_058_city_index_large_rejected(self):
        with self.assertRaises(ValueError):m.distance(m.LAYOUTS["near"],0,4)

    def test_059_city_index_bool_rejected(self):
        with self.assertRaises(TypeError):m.distance(m.LAYOUTS["near"],True,1)

    def test_060_OD_bad_margin_negative(self):
        with self.assertRaises(ValueError):m.od_exact_tables_enumeration((2,-3,4))

    def test_061_OD_symbolic_bad_margin_bool(self):
        with self.assertRaises(TypeError):m.od_exact_tables_symbolic((True,3,4))

    def test_062_OD_invalid_table_negative(self):
        a=m.od_exact_tables_enumeration()[0]
        t=[list(z) for z in a];t[0][1]=-1
        with self.assertRaises(ValueError):m.od_score(t,1)

    def test_063_OD_invalid_self_flow(self):
        a=m.od_exact_tables_enumeration()[0]
        t=[list(z) for z in a];t[0][0]=1
        with self.assertRaises(ValueError):m.od_score(t,1)

    def test_064_OD_invalid_table_bool(self):
        a=m.od_exact_tables_enumeration()[0]
        t=[list(z) for z in a];t[0][1]=True
        with self.assertRaises(TypeError):m.od_score(t,1)

    def test_065_OD_invalid_shape(self):
        with self.assertRaises(ValueError):m.od_score(((0,1),(1,0)),1)

    def test_066_wrong_layout_rejected(self):
        with self.assertRaises(ValueError):m.scenario("not-real",1,"flat","pop_10")

    def test_067_wrong_attraction_rejected(self):
        with self.assertRaises(ValueError):m.scenario("near",1,"not-real","pop_10")

    def test_068_every_row_allocation_54(self):
        for z in m.ordered_scenarios():
            r=m.scenario(*z)
            q=m.outflows(m.POPULATIONS,z[3])
            self.assertEqual(tuple(map(F,r["row_outflow"])),q)

    def test_069_pair_counts_direction_invariant(self):
        ans=m.output()
        self.assertEqual(ans["od_undirected_pair_counts"],[[1,3,5],[1,3,5]])

    def test_070_gravity_score_symmetry_in_outputs(self):
        ans=m.output()
        self.assertTrue(all(len(set(z))==1 for z in ans["three_city_gravity_scores"].values()))

    def test_071_total_expected_budget(self):
        for budget,total in (("pop_10",F(17,10)),("pop_5",F(17,5)),("half",F(2))):
            self.assertEqual(sum(m.outflows(m.POPULATIONS,budget)),total)

    def test_072_no_OD_empirical_likelihood_claim(self):
        self.assertTrue(m.output()["caveat_od_gravity_score_not_full_individual_likelihood"])

def create_dedicated_case_test(spec):
    def check(self):
        layout,alpha,attract,budget=spec
        params=(m.POPULATIONS,m.LAYOUTS[layout],m.ATTRACTIONS[attract],alpha,budget)
        flow1=m.flows_direct(*params)
        flow2=m.flows_integer_route(*params)
        self.assertEqual(flow1,flow2)
        out=m.outflows(m.POPULATIONS,budget)
        for i in range(4):
            self.assertEqual(sum(flow1[i]),out[i])
            self.assertEqual(flow1[i][i],0)
            self.assertEqual(sum((flow1[i][j]/out[i] for j in range(4)),F(0)),1)
        all_in=sum((sum((flow1[i][j] for i in range(4)),F(0)) for j in range(4)),F(0))
        self.assertEqual(all_in,sum(out))
    return check

for index,params in enumerate(m.ordered_scenarios()):
    setattr(TestR152,f"test_2{index:03d}_spec_{params[0]}_a{params[1]}_{params[2]}_{params[3]}",
            create_dedicated_case_test(params))

if __name__=="__main__":
    unittest.main()
