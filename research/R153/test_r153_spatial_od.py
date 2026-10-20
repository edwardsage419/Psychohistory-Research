"""R153 real executable checks of all frozen 60 scenarios and adversarial controls."""
import json
import math
import unittest
from fractions import Fraction
from pathlib import Path
from r153_spatial_od import (ROW_PAIRS, COL_FIRST, WEIGHTS, origin_only,
                             solve_scalar, solve_ipf, support_interval, scenario_results)


def close_table(test, left, right, tol=1e-9):
    for i in range(2):
        for j in range(2): test.assertLess(abs(left[i][j]-right[i][j]),tol)


class TestR153(unittest.TestCase):
    def check_case(self, ri, ci, wi):
        rows=ROW_PAIRS[ri]; cols=(COL_FIRST[ci],8-COL_FIRST[ci]); w=WEIGHTS[wi]
        t=solve_ipf(rows,cols,w); s=solve_scalar(rows,cols,w)
        close_table(self,t,s)
        for i in range(2): self.assertLess(abs(sum(t[i])-rows[i]),1e-10)
        for j in range(2): self.assertLess(abs(sum(t[i][j] for i in range(2))-cols[j]),1e-10)
        self.assertLess(abs(t[0][0]*t[1][1]*w[0][1]*w[1][0]-
                            t[0][1]*t[1][0]*w[0][0]*w[1][1]),1e-9)

    def test_frozen_count(self):
        self.assertEqual(len(ROW_PAIRS)*len(COL_FIRST)*len(WEIGHTS),60)

    def test_exact_uniform_fraction(self):
        for rows in ROW_PAIRS:
            for c in COL_FIRST:
                cols=(c,8-c); tab=solve_ipf(rows,cols,WEIGHTS[0]);
                target=[[Fraction(r*cl,8) for cl in cols] for r in rows]
                close_table(self,tab,target)

    def test_singly_doubly_contrast(self):
        single=origin_only((3,5),((1,1),(1,1)))
        doubled=solve_ipf((3,5),(2,6),((1,1),(1,1)))
        self.assertAlmostEqual(sum(single[i][0] for i in range(2)),4.0)
        self.assertAlmostEqual(sum(doubled[i][0] for i in range(2)),2.0)
        close_table(self,doubled,((.75,2.25),(1.25,3.75)))

    def test_kernel_row_column_scaling_invariance(self):
        for w in WEIGHTS:
            orig=solve_ipf((3,5),(2,6),w)
            scaled=tuple(tuple(w[i][j] * (2 if i==0 else 3) * (5 if j==0 else 7) for j in range(2)) for i in range(2))
            close_table(self,orig,solve_ipf((3,5),(2,6),scaled))

    def test_origin_only_responds_to_destination_bias(self):
        w=((1,1),(1,1)); modified=((5,1),(5,1))
        self.assertGreater(origin_only((3,5),modified)[0][0],origin_only((3,5),w)[0][0])

    def test_structural_zero_exact_unique(self):
        w=((0,1),(1,1))
        self.assertEqual(support_interval((3,5),(4,4),w),(Fraction(0),Fraction(0)))
        close_table(self,solve_scalar((3,5),(4,4),w),((0,3),(4,1)))

    def test_structural_zero_rejected_by_strict_ipf(self):
        with self.assertRaises(ValueError): solve_ipf((3,5),(4,4),((0,1),(1,1)))

    def test_structural_zero_infeasible(self):
        with self.assertRaises(ValueError): support_interval((3,5),(4,4),((1,0),(0,1)))
        with self.assertRaises(ValueError): solve_scalar((3,5),(4,4),((1,0),(0,1)))

    def test_mismatched_totals_rejected(self):
        with self.assertRaises(ValueError): solve_ipf((3,5),(3,6),WEIGHTS[0])
        with self.assertRaises(ValueError): solve_scalar((3,5),(3,6),WEIGHTS[0])

    def test_nonfinite_and_negative_rejected(self):
        for bad in (float('nan'), float('inf'),-1, True):
            with self.subTest(bad=str(bad)):
                with self.assertRaises(ValueError): solve_ipf((3,5),(2,6),((bad,1),(1,1)))

    def test_zero_row_and_column_rejected(self):
        for w in (((0,0),(1,1)),((0,1),(0,1)),((1,0),(1,0))):
            with self.subTest(w=w):
                with self.assertRaises(ValueError): solve_scalar((3,5),(4,4),w)

    def test_support_symmetric_bounds(self):
        self.assertEqual(support_interval((3,5),(4,4),((1,1),(1,1))),
                         (Fraction(0),Fraction(3)))
        self.assertEqual(support_interval((3,5),(2,6),((1,1),(1,1))),
                         (Fraction(0),Fraction(2)))

    def test_serialized_result_ledger(self):
        doc=scenario_results()
        self.assertEqual(doc['frozen_scenarios'],60)
        self.assertEqual(len(doc['results']),60)
        self.assertEqual(len(set(x['case_id'] for x in doc['results'])),60)
        self.assertEqual(doc['evidence_level'],'E1_SYNTHETIC_ONLY')
        self.assertEqual(doc['exact_uniform_benchmark']['cells'],[['3/4','9/4'],['5/4','15/4']])

    def test_replay_matches_pinned_json_bytes(self):
        p=Path(__file__).with_name('R153_EXACT_RESULTS.json')
        if not p.exists(): self.skipTest('archive created in final publication step')
        output=(json.dumps(scenario_results(),ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8')
        self.assertEqual(p.read_bytes(),output)


# Distinct, named test methods for each frozen scenario, not repeated one-case invocations.
for ri in range(len(ROW_PAIRS)):
    for ci in range(len(COL_FIRST)):
        for wi in range(len(WEIGHTS)):
            name=f'test_scenario_r{ri}_c{ci}_w{wi}'
            def build_test(ri=ri,ci=ci,wi=wi):
                def case(self): self.check_case(ri,ci,wi)
                return case
            setattr(TestR153,name,build_test())


if __name__ == '__main__':
    unittest.main()
