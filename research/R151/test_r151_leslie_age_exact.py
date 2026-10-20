"""R151 exact Fraction cohort tests (separate frozen parameter examples).
50 dynamically named UNIQUE age compositions + independent boundary audits.
"""
import unittest
from fractions import Fraction as F
from itertools import product
import r151_leslie_age_exact as m

class TestR151(unittest.TestCase):
    def test_001_catalogue_combinatorics(self):
        self.assertEqual(len(m.COHORTS),91)
        self.assertEqual(len(set(m.COHORTS)),91)

    def test_002_exact_baseline_stable_vector(self):
        self.assertEqual(m.matrix_step(m.STABLE_SHARE,*m.BASELINE),m.STABLE_SHARE)

    def test_003_normalized_left_eigenvector(self):
        self.assertEqual(sum((a*b for a,b in zip(m.REPRODUCTIVE_VALUE,m.STABLE_SHARE)),F(0)),1)

    def test_004_left_invariant_91_cohorts(self):
        for x in m.COHORTS:
            self.assertEqual(m.reproductive_value(x),m.reproductive_value(m.matrix_step(x,*m.BASELINE)))

    def test_005_stationary_absolute(self):
        seq,_=m.run((400,300,200),*m.BASELINE)
        self.assertTrue(all(z==(F(400),F(300),F(200)) for z in seq))

    def test_006_same_first_total(self):
        x,_=m.run((400,300,200),*m.BASELINE)
        y,_=m.run((120,360,420),*m.BASELINE)
        self.assertEqual((sum(x[0]),sum(x[1])),(900,900))
        self.assertEqual((sum(y[0]),sum(y[1])),(900,900))

    def test_007_hidden_age_divergence_year2(self):
        p,_=m.run((120,360,420),*m.BASELINE)
        self.assertEqual(sum(p[2]),F(1395,2))
        self.assertNotEqual(sum(p[2]),900)

    def test_008_hidden_age_distinct_limit(self):
        self.assertEqual(m.reproductive_value((400,300,200)),900)
        self.assertEqual(m.reproductive_value((120,360,420)),810)

    def test_009_young_limit(self):
        self.assertEqual(m.reproductive_value((900,0,0)),900)

    def test_010_adult_limit(self):
        self.assertEqual(m.reproductive_value((0,900,0)),1200)

    def test_011_old_limit(self):
        self.assertEqual(m.reproductive_value((0,0,900)),450)

    def test_012_three_initial_totals(self):
        for x in ((900,0,0),(0,900,0),(0,0,900)):
            self.assertEqual(sum(x),900)

    def test_013_closed_polynomial_all_91(self):
        for x in m.COHORTS:
            path,_=m.run(x,*m.BASELINE)
            for t,z in enumerate(path):
                self.assertEqual(m.exact_closed_total(x,t),sum(z))

    def test_014_at_24_nontrivial_relaxation(self):
        x=(0,900,0)
        a=m.exact_closed_total(x,12)
        b=m.exact_closed_total(x,24)
        c=m.reproductive_value(x)
        self.assertLess(abs(b-c),abs(a-c))

    def test_015_zero_fertility_extinction_91_by_3(self):
        for x in m.COHORTS:
            path,_=m.run(x,F(0),F(3,4),F(2,3),3)
            self.assertEqual(path[-1],(0,0,0))

    def test_016_migration_zero_case(self):
        p,_=m.run((400,300,200),*m.BASELINE,migration=(0,0,0))
        self.assertEqual(p[1],(F(400),F(300),F(200)))

    def test_017_migration_young_first(self):
        p,l=m.run((400,300,200),*m.BASELINE,migration=(2,0,0))
        self.assertEqual(p[1],(F(402),F(300),F(200)))
        self.assertEqual(l[0]["net_immigration"],2)

    def test_018_migration_adult_first(self):
        p,l=m.run((400,300,200),*m.BASELINE,migration=(0,2,0))
        self.assertEqual(p[1],(F(400),F(302),F(200)))
        self.assertEqual(l[0]["net_immigration"],2)

    def test_019_migration_limit_increments(self):
        a,_=m.run((400,300,200),*m.BASELINE,migration=(2,0,0))
        b,_=m.run((400,300,200),*m.BASELINE,migration=(0,2,0))
        self.assertEqual(m.reproductive_value(a[1])-900,2)
        self.assertEqual(m.reproductive_value(b[1])-900,F(8,3))

    def test_020_migration_one_step_only(self):
        _,ledger=m.run((400,300,200),*m.BASELINE,migration=(0,2,0))
        self.assertEqual([z["net_immigration"] for z in ledger],[F(2)]+[F(0)]*11)

    def test_021_older_migrants_limit_increment(self):
        p,_=m.run((400,300,200),*m.BASELINE,migration=(0,0,2))
        self.assertEqual(m.reproductive_value(p[1])-900,1)

    def test_022_no_old_survival(self):
        self.assertEqual(m.matrix_step((0,0,5),*m.BASELINE),(F(5,2),F(0),F(0)))

    def test_023_births_only_adults(self):
        n,d=m.accounts_step((0,12,0),*m.BASELINE)
        self.assertEqual(d["births"],12)
        self.assertEqual(n,(F(12),F(0),F(8)))

    def test_024_births_older_half(self):
        n,d=m.accounts_step((0,0,12),*m.BASELINE)
        self.assertEqual(d["births"],6)
        self.assertEqual(n,(F(6),F(0),F(0)))

    def test_025_juvenile_survivors(self):
        n,d=m.accounts_step((12,0,0),*m.BASELINE)
        self.assertEqual(n,(F(0),F(9),F(0)))
        self.assertEqual(d["deaths"],3)

    def test_026_zero_cohorts_remain_zero(self):
        self.assertEqual(m.matrix_step((0,0,0),*m.BASELINE),(0,0,0))

    def test_027_cohort_state_invalid_bool(self):
        with self.assertRaises(TypeError):m.state_vector((True,0,0))

    def test_028_cohort_state_invalid_float(self):
        with self.assertRaises(TypeError):m.state_vector((1.0,0,0))

    def test_029_cohort_state_negative(self):
        with self.assertRaises(ValueError):m.state_vector((-1,0,0))

    def test_030_cohort_state_wrong_length(self):
        with self.assertRaises(ValueError):m.state_vector((1,0))

    def test_031_cohort_state_wrong_type(self):
        with self.assertRaises(ValueError):m.state_vector("100")

    def test_032_bad_fertility_negative(self):
        with self.assertRaises(ValueError):m.params(-1,F(3,4),F(2,3))

    def test_033_bad_survival_excess(self):
        with self.assertRaises(ValueError):m.params(1,F(5,4),F(2,3))

    def test_034_bad_survival_negative(self):
        with self.assertRaises(ValueError):m.params(1,F(3,4),F(-1,3))

    def test_035_bad_fertility_bool(self):
        with self.assertRaises(TypeError):m.params(True,F(3,4),F(2,3))

    def test_036_bad_survival_float(self):
        with self.assertRaises(TypeError):m.params(1,0.75,F(2,3))

    def test_037_bad_horizon_bool(self):
        with self.assertRaises(ValueError):m.run((12,0,0),horizon=True)

    def test_038_bad_horizon_negative(self):
        with self.assertRaises(ValueError):m.run((12,0,0),horizon=-1)

    def test_039_bad_horizon_excess(self):
        with self.assertRaises(ValueError):m.run((12,0,0),horizon=129)

    def test_040_bad_migration_negative(self):
        with self.assertRaises(ValueError):m.run((12,0,0),migration=(0,-2,0))

    def test_041_matrix_vs_accounts_all_rates_at_edge(self):
        for k,sj,sa in product(m.MULTIPLIERS,m.JUVENILE_SURVIVALS,m.ADULT_SURVIVALS):
            x=(F(12),F(0),F(0))
            self.assertEqual(m.matrix_step(x,k,sj,sa),m.accounts_step(x,k,sj,sa)[0])

    def test_042_all_1092_synthetic_scenarios(self):
        d=m.output_data()
        self.assertEqual(d["cases_count"],1092)
        self.assertEqual(len(d["all_1092_full_trajectories"]),1092)
        self.assertEqual(len({(tuple(x["initial"]),x["fertility_multiplier"],
                x["juvenile_survival"],x["adult_survival"]) for x in d["all_1092_full_trajectories"]}),1092)

    def test_043_all_paths_full_13_snapshots(self):
        d=m.output_data()
        self.assertTrue(all(len(v["age_trace"])==13 and len(v["yearly_births"])==12
                            for v in d["all_1092_full_trajectories"]))

    def test_044_every_full_case_independent_ledger(self):
        d=m.output_data()
        self.assertTrue(all(m.ledger_recheck(v) for v in d["all_1092_full_trajectories"]))

    def test_045_each_total_matches_cohort_sum(self):
        for age in m.COHORTS:
            p,l=m.run(age,*m.BASELINE)
            self.assertEqual([sum(z) for z in p],
                             [sum(m.state_vector(z)) for z in p])

    def test_046_births_equals_first_next_cohort(self):
        for age in m.COHORTS:
            n,a=m.accounts_step(age,*m.BASELINE)
            self.assertEqual(n[0],a["births"])

    def test_047_no_negative_with_nonnegative_rates(self):
        for initial in m.COHORTS:
            for k,sj,sa in product(m.MULTIPLIERS,m.JUVENILE_SURVIVALS,m.ADULT_SURVIVALS):
                p,_=m.run(initial,k,sj,sa)
                self.assertTrue(all(all(z>=0 for z in state) for state in p))

    def test_048_json_deterministic(self):
        self.assertEqual(m.canonical_json(),m.canonical_json())

    def test_049_metadata_not_history(self):
        d=m.output_data()
        self.assertFalse(d["original_data_reproduced"])
        self.assertEqual((d["new_E2"],d["new_E3"]),(0,0))

    def test_050_exact_replacement_characteristic(self):
        # lambda^3 - 3/4 lambda - 1/4 == (lambda-1)(lambda+1/2)^2
        for t in (F(-3),F(-1,2),F(0),F(1),F(2),F(5,3)):
            self.assertEqual(t**3-F(3,4)*t-F(1,4),(t-1)*(t+F(1,2))**2)

    def test_051_stable_share_total_one(self):
        self.assertEqual(sum(m.STABLE_SHARE),1)

    def test_052_reproductive_value_unchanged_after_12(self):
        for c in m.COHORTS:
            path,_=m.run(c,*m.BASELINE)
            self.assertEqual(m.reproductive_value(path[-1]),m.reproductive_value(c))

    def test_053_replacement_count_not_for_all_parameters(self):
        initial=(0,12,0)
        p,_=m.run(initial,F(3,2),F(3,4),F(2,3))
        self.assertNotEqual(m.reproductive_value(p[-1]),m.reproductive_value(initial))

    def test_054_ledger_migration_identity(self):
        initial=(400,300,200)
        nxt,acct=m.accounts_step(initial,*m.BASELINE,imm=(2,0,0))
        self.assertEqual(sum(nxt)-sum(initial),
                         acct["births"]-acct["deaths"]+acct["net_immigration"])

    def test_055_baseline_juvenile_difference(self):
        young,_=m.run((900,0,0),*m.BASELINE)
        old,_=m.run((0,0,900),*m.BASELINE)
        self.assertNotEqual(sum(young[2]),sum(old[2]))

def _make_unique_cohort_test(initial):
    def test(self):
        x=m.state_vector(initial)
        k,sj,sa=m.BASELINE
        age=x
        for t in range(12):
            expected=m.matrix_step(age,k,sj,sa)
            actual,acct=m.accounts_step(age,k,sj,sa)
            self.assertEqual(expected,actual)
            self.assertEqual(sum(actual),sum(age)+acct["births"]-acct["deaths"])
            self.assertEqual(m.reproductive_value(actual),m.reproductive_value(x))
            age=actual
        self.assertEqual(sum(age),m.exact_closed_total(x,12))
    return test

for ordinal,initial in enumerate(m.COHORTS[:50]):
    setattr(TestR151,f"test_1{ordinal:02d}_distinct_age_{initial[0]}_{initial[1]}_{initial[2]}",
            _make_unique_cohort_test(initial))

if __name__=="__main__":
    unittest.main()
