"""R156 117 genuine checks: 96 distinct AK/concave worlds and 21 edge cases."""
import json
import math
import unittest
from pathlib import Path
from r156_growth_pair import (
    ALPHAS,INITIAL_STOCKS,SAVINGS,DEPRECIATIONS,TIMES,analytic_k,rk4_grid,
    rk4_at,euler_step,flow_rhs,inputs,checked,result_document
)


class TestR156(unittest.TestCase):
    def check_world(self,ai,ki,si,di):
        alpha=ALPHAS[ai]; k0=INITIAL_STOCKS[ki]
        s=SAVINGS[si]; delta=DEPRECIATIONS[di]
        numeric=rk4_grid(k0,alpha,s,delta)
        expected=[analytic_k(t,k0,alpha,s,delta) for t in TIMES]
        self.assertEqual(len(numeric),len(TIMES))
        for t,a,b in zip(TIMES,expected,numeric):
            self.assertGreater(a,0)
            self.assertGreater(b,0)
            self.assertLess(abs(a-b),1e-7)
            self.assertTrue(math.isfinite(a**alpha))
            self.assertTrue(math.isfinite(flow_rhs(a,alpha,s,delta)))
        if alpha==1:
            for t,a in zip(TIMES[1:],expected[1:]):
                self.assertLess(abs(math.log(a/k0)/t-(s-delta)),1e-12)
        else:
            if delta>0:
                steady=(s/delta)**2
                if k0<steady-1e-10:
                    self.assertTrue(all(expected[i+1]>=expected[i] for i in range(3)))
                if k0>steady+1e-10:
                    self.assertTrue(all(expected[i+1]<=expected[i] for i in range(3)))

    def test_frozen_96_world_count(self):
        self.assertEqual(len(ALPHAS)*len(INITIAL_STOCKS)*len(SAVINGS)*len(DEPRECIATIONS),96)

    def test_identical_initial_stocks(self):
        for alpha in ALPHAS:
            self.assertEqual(analytic_k(0,9,alpha,.4,.1),9.0)

    def test_AK_constant_log_growth(self):
        for t in (1,5,10):
            k=analytic_k(t,4,1,.4,.2)
            self.assertAlmostEqual(math.log(k/4)/t,.2,places=12)

    def test_AK_exponential_decay_stays_positive(self):
        self.assertGreater(analytic_k(10,9,1,.1,.4),0)
        self.assertLess(analytic_k(10,9,1,.1,.4),9)

    def test_AK_zero_net_growth_is_stationary(self):
        for t in TIMES:
            self.assertEqual(analytic_k(t,4,1,.2,.2),4)

    def test_concave_exact_stationary_stock(self):
        for t in TIMES:
            self.assertEqual(analytic_k(t,4,.5,.2,.1),4)

    def test_concave_below_equilibrium_increases(self):
        a=[analytic_k(t,1,.5,.2,.1) for t in TIMES]
        self.assertTrue(all(x<y for x,y in zip(a,a[1:])))
        self.assertLess(a[-1],4)

    def test_concave_above_equilibrium_decreases(self):
        a=[analytic_k(t,9,.5,.2,.1) for t in TIMES]
        self.assertTrue(all(x>y for x,y in zip(a,a[1:])))
        self.assertGreater(a[-1],4)

    def test_concave_fixed_point_from_ratio(self):
        for s,delta,k0 in ((.1,.1,1),(.2,.1,4),(.6,.2,9)):
            self.assertAlmostEqual(analytic_k(10,k0,.5,s,delta),k0,places=12)

    def test_concave_zero_depreciation_sqrt_linear(self):
        for t in (0,1,5,10,100):
            k=analytic_k(t,9,.5,.2,0)
            self.assertAlmostEqual(math.sqrt(k),3+.1*t,places=12)

    def test_long_run_positive_AK_versus_concave_finite_equilibrium(self):
        ak=analytic_k(100,1,1,.2,.1)
        diminishing=analytic_k(100,1,.5,.2,.1)
        self.assertGreater(ak,20000)
        self.assertLess(diminishing,4.0)
        self.assertGreater(diminishing,3.9)

    def test_AK_s_and_delta_nonidentification_from_entire_path(self):
        for t in TIMES:
            a=analytic_k(t,1,1,.2,.1)
            b=analytic_k(t,1,1,.4,.3)
            self.assertLess(abs(a-b),1e-12)

    def test_concave_same_initial_derivative_different_later(self):
        self.assertAlmostEqual(flow_rhs(1,.5,.2,.1),
                               flow_rhs(1,.5,.4,.3),places=13)
        self.assertGreater(abs(analytic_k(5,1,.5,.2,.1)-
                               analytic_k(5,1,.5,.4,.3)),.01)

    def test_euler_overshoot_to_negative(self):
        self.assertEqual(euler_step(1,1,.1,.4,20),-5.000000000000001)
        self.assertGreater(analytic_k(20,1,1,.1,.4),0)

    def test_physical_exact_stock_never_negative(self):
        for alpha in ALPHAS:
            for k0 in INITIAL_STOCKS:
                self.assertGreater(analytic_k(100,k0,alpha,.1,.4),0)

    def test_invalid_negative_parameters(self):
        for k,a,s,d in ((-1,1,.2,.1),(0,.5,.2,.1),(1,1,-.1,.1),(1,.5,.2,-.1)):
            with self.assertRaises(ValueError): analytic_k(1,k,a,s,d)

    def test_invalid_nonfinite_and_type(self):
        for bad in (math.inf,math.nan,True,'4'):
            with self.subTest(value=str(bad)):
                with self.assertRaises(ValueError): checked(bad,'bad')

    def test_invalid_alpha_or_savings_range(self):
        with self.assertRaises(ValueError): analytic_k(1,1,.9,.2,.1)
        with self.assertRaises(ValueError): analytic_k(1,1,1.0,1.1,.1)

    def test_invalid_time(self):
        for t in (-1,math.inf,math.nan,False):
            with self.assertRaises(ValueError): analytic_k(t,1,1,.2,.1)

    def test_rk4_arbitrary_time(self):
        for t,a,k,s,d in ((1.35,.5,9,.2,.1),(3.9,1,4,.4,.2),(7.1,.5,1,.6,0)):
            self.assertLess(abs(rk4_at(t,k,a,s,d)-analytic_k(t,k,a,s,d)),1e-7)

    def test_frozen_machine_document_fields(self):
        d=result_document()
        self.assertEqual(d['scenario_count'],96)
        self.assertEqual(len(d['worlds']),96)
        self.assertEqual(len(set(x['scenario_id'] for x in d['worlds'])),96)
        self.assertLess(d['max_absolute_RK4_error'],1e-7)
        self.assertFalse(d['historical_data_forecasting'])
        self.assertFalse(d['author_original_full_model_reproduction'])

    def test_full_result_json_byte_identity(self):
        path=Path(__file__).with_name('R156_EXACT_RESULTS.json')
        if not path.exists(): self.skipTest('CI must generate canonical ledger before replay')
        expected=(json.dumps(result_document(),indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode('utf-8')
        self.assertEqual(path.read_bytes(),expected)


for ai in range(len(ALPHAS)):
    for ki in range(len(INITIAL_STOCKS)):
        for si in range(len(SAVINGS)):
            for di in range(len(DEPRECIATIONS)):
                def make(ai=ai,ki=ki,si=si,di=di):
                    def test(self): self.check_world(ai,ki,si,di)
                    return test
                setattr(TestR156,f'test_frozen_a{ai}_k{ki}_s{si}_d{di}',make())


if __name__=='__main__':
    unittest.main()
