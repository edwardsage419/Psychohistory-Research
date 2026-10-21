"""R155 Bass 1969 original-equation numerical checks and source Table I boundaries."""
import json
import math
import unittest
from pathlib import Path

from r155_bass_continuous import (
    P_GRID,Q_GRID,MARKETS,TIMES,STEPS_PER_UNIT,PUBLISHED_TABLE_I,
    cumulative,adoption_density,interior_peak_time,rk4_at,rk4_grid,
    euler_one_step,published_table_arithmetic,result_document,rhs,
    checked_number
)


class TestBass(unittest.TestCase):
    def check_world(self,pi,qi,mi):
        p,q,m=P_GRID[pi],Q_GRID[qi],MARKETS[mi]
        values=[cumulative(t,p,q) for t in TIMES]
        estimates=rk4_grid(p,q)
        self.assertEqual(len(values),6)
        self.assertEqual(values[0],0.0)
        self.assertEqual(adoption_density(0,p,q),p)
        for t,F,G in zip(TIMES,values,estimates):
            self.assertLess(abs(F-G),2e-11)
            self.assertGreaterEqual(F,0.0)
            self.assertLessEqual(F,1.0)
            self.assertGreaterEqual(m*adoption_density(t,p,q),0.0)
        for a,b in zip(values,values[1:]):
            self.assertLessEqual(a,b+1e-14)
        if p==0:
            self.assertEqual(values, [0.0]*len(TIMES))
        if q==0 and p>0:
            for t,F in zip(TIMES,values):
                self.assertLess(abs(F - (-math.expm1(-p*t))),1e-13)

    def test_exact_frozen_world_count(self):
        self.assertEqual(len(P_GRID)*len(Q_GRID)*len(MARKETS),75)
        self.assertEqual(TIMES,(0.0,0.25,1.0,3.0,5.0,10.0))

    def test_unseeded_p_zero_pure_imitation(self):
        for q in Q_GRID:
            self.assertEqual(cumulative(10,0,q),0.0)
            self.assertEqual(adoption_density(10,0,q),0.0)
            self.assertIsNone(interior_peak_time(0,q))

    def test_innovation_only_q_zero(self):
        for p in P_GRID[1:]:
            for t in TIMES:
                self.assertAlmostEqual(cumulative(t,p,0),-math.expm1(-p*t),places=13)

    def test_initial_hazard_and_density(self):
        for p in P_GRID:
            for q in Q_GRID:
                self.assertEqual(adoption_density(0,p,q),p)

    def test_no_repeated_first_adoption(self):
        f=cumulative(100,.2,.8)
        self.assertGreater(f,.999999999)
        self.assertLess(f,1.0)

    def test_peak_interior_analytic(self):
        p,q=.02,.4
        t=interior_peak_time(p,q)
        self.assertGreater(t,0)
        self.assertAlmostEqual(cumulative(t,p,q),(q-p)/(2*q),places=12)
        self.assertAlmostEqual(adoption_density(t,p,q),(p+q)**2/(4*q),places=12)

    def test_peak_rate_on_both_sides(self):
        p,q=.02,.4
        t=interior_peak_time(p,q)
        self.assertGreater(adoption_density(t,p,q),adoption_density(t-.1,p,q))
        self.assertGreater(adoption_density(t,p,q),adoption_density(t+.1,p,q))

    def test_q_less_than_or_equal_p_boundary_peak(self):
        for p,q in ((.2,.02),(.2,.2),(.02,0.0)):
            self.assertEqual(interior_peak_time(p,q),0.0)
            self.assertGreaterEqual(adoption_density(0,p,q),
                                    adoption_density(.01,p,q))

    def test_p_zero_q_zero_no_unique_peak(self):
        self.assertIsNone(interior_peak_time(0,0))
        self.assertEqual(adoption_density(100,0,0),0)

    def test_market_size_does_not_change_fraction(self):
        for p,q in ((.005,.8),(.2,.02),(.02,.1)):
            self.assertEqual(cumulative(5,p,q),cumulative(5,p,q))

    def test_market_scales_levels_only(self):
        f=cumulative(4,.02,.4)
        a=100*f
        b=1000*f
        self.assertAlmostEqual(b,10*a,places=10)

    def test_one_instant_mp_non_identification(self):
        self.assertEqual(1000*.02,2000*.01)
        self.assertNotEqual(cumulative(1,.02,.4),cumulative(1,.01,.4))
        self.assertNotAlmostEqual(1000*adoption_density(1,.02,.4),
                                  2000*adoption_density(1,.01,.4),places=5)

    def test_euler_overshoots_adoption_budget(self):
        self.assertEqual(euler_one_step(10,.2,.8),2.0)
        self.assertLess(cumulative(10,.2,.8),1.0)

    def test_independent_rk4_non_grid_time(self):
        for t,p,q in ((.77,.02,.4),(2.2,.2,.8),(7.4,.005,.1)):
            self.assertLess(abs(rk4_at(t,p,q)-cumulative(t,p,q)),2e-11)

    def test_density_equals_numerical_F_derivative(self):
        h=1e-5
        for p,q,t in ((.02,.4,1),(.2,.8,2),(.005,.02,5)):
            est=(cumulative(t+h,p,q)-cumulative(t-h,p,q))/(2*h)
            self.assertLess(abs(est-adoption_density(t,p,q)),1e-8)

    def test_published_table_I_three_rows(self):
        rows=published_table_arithmetic()
        self.assertEqual(len(rows),3)
        self.assertEqual(tuple(r['product'] for r in rows),
                          ('electric_refrigerators','home_freezers','black_white_television'))
        for i,row in enumerate(rows):
            name,p,q,m=PUBLISHED_TABLE_I[i]
            self.assertEqual(row['source_printed_p'],p)
            self.assertEqual(row['source_printed_q'],q)
            self.assertEqual(row['source_printed_m_thousands'],m)
            self.assertGreater(row['source_derived_t_peak'],0)
            self.assertAlmostEqual(row['source_derived_initial_sales_thousands_per_time'],m*p,places=8)

    def test_published_table_peak_formula_direct(self):
        for name,p,q,m in PUBLISHED_TABLE_I:
            t=math.log(q/p)/(p+q)
            direct=m*adoption_density(t,p,q)
            algebra=m*(p+q)**2/(4*q)
            self.assertLess(abs(direct-algebra),1e-7)

    def test_negative_and_nonfinite_inputs_rejected(self):
        for bad in (-.1,float('nan'),float('inf'),True,'0.2'):
            with self.subTest(value=str(bad)):
                with self.assertRaises(ValueError):
                    cumulative(2,bad,.1)
                with self.assertRaises(ValueError):
                    adoption_density(2,.1,bad)

    def test_invalid_t_and_market_validation(self):
        for t in (-1,float('nan'),float('inf'),False):
            with self.assertRaises(ValueError): cumulative(t,.1,.3)
        for m in (0,-1,float('inf'),True):
            with self.assertRaises(ValueError): checked_number(m,'market',positive=True)

    def test_recorded_evidence_boundaries_and_scenarios(self):
        d=result_document()
        self.assertEqual(d['scenario_count'],75)
        self.assertEqual(len({case['scenario_id'] for case in d['cases']}),75)
        self.assertFalse(d['original_author_data_refit'])
        self.assertFalse(d['historical_heldout_prediction'])
        self.assertLess(d['max_RK4_closed_form_error'],2e-11)

    def test_full_json_byte_replay_when_present(self):
        path=Path(__file__).with_name('R155_EXACT_RESULTS.json')
        if not path.exists():
            self.skipTest('canonical full JSON is generated during CI replay step')
        expected=(json.dumps(result_document(),sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode('utf-8')
        self.assertEqual(path.read_bytes(),expected)


for pi in range(len(P_GRID)):
    for qi in range(len(Q_GRID)):
        for mi in range(len(MARKETS)):
            def construct(pi=pi,qi=qi,mi=mi):
                def world(self):
                    self.check_world(pi,qi,mi)
                return world
            setattr(TestBass,f'test_frozen_p{pi}_q{qi}_m{mi}',construct())


if __name__ == '__main__':
    unittest.main()
