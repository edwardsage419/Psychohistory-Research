"""R154 reproducible 100-case Fraction tests and separately named controls."""
import json
import unittest
from fractions import Fraction as F
from pathlib import Path
from r154_stock_flow_exact import (
    SHARES,INITIAL_A,TOTAL,HORIZON,as_fraction,checked_stocks,closed_step,
    direct_history,analytical_history,forward_euler_step,delayed_withdrawal_step,
    open_step,result_document
)

class TestStockFlow(unittest.TestCase):
    def check_world(self,ai,pi,qi):
        a0,p,q=INITIAL_A[ai],SHARES[pi],SHARES[qi]
        states,flows=direct_history(a0,p,q)
        closed=analytical_history(a0,p,q)
        self.assertEqual(states,closed)
        self.assertEqual(len(states),13)
        self.assertEqual(len(flows),12)
        for k in range(13):
            a,b=states[k]
            self.assertEqual(a+b,TOTAL)
            self.assertGreaterEqual(a,0)
            self.assertGreaterEqual(b,0)
            if k < 12:
                ab,ba=flows[k]
                self.assertEqual(ab,p*a)
                self.assertEqual(ba,q*b)
                self.assertEqual(states[k+1],(a-ab+ba,b+ab-ba))

    def test_world_count(self):
        self.assertEqual(len(INITIAL_A)*len(SHARES)**2,100)

    def test_static_zero_rates(self):
        for a0 in INITIAL_A:
            states,_=direct_history(a0,0,0)
            self.assertTrue(all(v == (F(a0),TOTAL-F(a0)) for v in states))

    def test_equilibrium_after_one_step(self):
        for a0 in INITIAL_A:
            for p in SHARES:
                q=1-p
                states,_=direct_history(a0,p,q)
                self.assertTrue(all(state==states[1] for state in states[1:]))

    def test_period_two_swap(self):
        states,_=direct_history(10,1,1)
        self.assertEqual(states[0],states[2])
        self.assertEqual(states[1],states[3])
        self.assertNotEqual(states[0],states[1])

    def test_absorbing_B_after_one_step(self):
        states,_=direct_history(10,1,0)
        self.assertEqual(states[1],(F(0),F(10)))
        self.assertEqual(states[-1],(F(0),F(10)))

    def test_total_does_not_identify_transfer_rate(self):
        a,_=direct_history(10,0,0)
        b,_=direct_history(10,F(1,2),0)
        self.assertNotEqual(a[1],b[1])
        self.assertEqual([sum(x) for x in a],[sum(x) for x in b])

    def test_feedback_eigenvalue_exact(self):
        a0,p,q=6,F(3,4),F(3,4)
        states,_=direct_history(a0,p,q)
        star=TOTAL*q/(p+q)
        self.assertEqual(states[4][0]-star,(1-p-q)**4*(F(a0)-star))

    def test_conserved_opposed_flows(self):
        (na,nb),(ab,ba)=closed_step(7,3,F(1,4),F(3,4))
        self.assertEqual((na,nb),(F(15,2),F(5,2)))
        self.assertEqual(ab,F(7,4))
        self.assertEqual(ba,F(9,4))

    def test_euler_large_step_negative(self):
        self.assertEqual(forward_euler_step(10,0,F(3,4),F(3,4),2),(F(-5),F(15)))

    def test_euler_small_step_nonnegative(self):
        self.assertEqual(forward_euler_step(10,0,F(3,4),F(3,4),1),(F(5,2),F(15,2)))

    def test_delayed_unbounded_can_go_negative(self):
        self.assertEqual(delayed_withdrawal_step(0,10,10,1,strict=False),(F(-10),F(20)))

    def test_delayed_strict_guard(self):
        with self.assertRaises(ValueError): delayed_withdrawal_step(0,10,10,1)

    def test_open_system_ledger(self):
        (a,b),flows=open_step(5,5,F(1,2),F(1,2),2,1)
        self.assertEqual((a,b),(F(7),F(4)))
        self.assertEqual(a+b,F(10)+2-1)

    def test_open_system_withdrawal_guard(self):
        with self.assertRaises(ValueError): open_step(5,5,0,0,2,6)

    def test_invalid_shares_and_stocks(self):
        for p,q in ((-1,0),(2,0),(0,F(3,2))):
            with self.assertRaises(ValueError): closed_step(5,5,p,q)
        with self.assertRaises(ValueError): checked_stocks(-1,11)

    def test_invalid_types_and_horizon(self):
        for x in (True,1.25,'1'):
            with self.assertRaises(ValueError): as_fraction(x,'x')
        for h in (-1,False,3.1):
            with self.assertRaises(ValueError): direct_history(5,0,0,h)

    def test_outside_initial_budget_rejected(self):
        for x in (-1,11):
            with self.assertRaises(ValueError): direct_history(x,0,0)

    def test_rational_string_identity(self):
        self.assertEqual(str(F(1,4)),'1/4')
        r=result_document()
        self.assertEqual(r['scenario_count'],100)
        self.assertEqual(len(r['cases']),100)
        self.assertEqual(len(set(x['id'] for x in r['cases'])),100)

    def test_complete_json_replay(self):
        p=Path(__file__).with_name('R154_EXACT_RESULTS.json')
        # CI must build result before tests; absence is a failed archive or run ordering.
        self.assertTrue(p.exists())
        actual=(json.dumps(result_document(),sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
        self.assertEqual(p.read_bytes(),actual)

for ai in range(len(INITIAL_A)):
    for pi in range(len(SHARES)):
        for qi in range(len(SHARES)):
            def build(ai=ai,pi=pi,qi=qi):
                def case(self): self.check_world(ai,pi,qi)
                return case
            setattr(TestStockFlow,f'test_frozen_a{ai}_p{pi}_q{qi}',build())

if __name__=='__main__':
    unittest.main()
