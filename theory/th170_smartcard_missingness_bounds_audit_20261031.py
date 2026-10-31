#!/usr/bin/env python3
"""TH170 published-table arithmetic only. No personal or raw participant data.
Run: python3 theory/th170_smartcard_missingness_bounds_audit_20261031.py
"""
from fractions import Fraction as F
import unittest

DATA = {
    "NREGS": {"treated": (2014, 2152, 3353), "control": (493, 718, 1717),
              "total": (2507, 2870, 5070), "district7": (0, 0, 1425)},
    "SSP": {"treated": (987, 804, 959), "control": (206, 248, 628),
            "total": (1193, 1052, 1587), "district7": (2, 0, 555)},
}
A2_CASES = (10191, 10120, 3789, 3574, 14213, 7201, 14213, 7201)
B1_CASES = ((10120, 7294), (14165, 10383), (4915, 3545),
            (3131, 2219), (4915, 3545), (3131, 2219), (4717, 3406))

def group_bounds(row):
    yes, no, missing = row
    n = yes + no + missing
    return F(yes, n), F(yes + missing, n)

def diff_bounds(data):
    tl, tu = group_bounds(data["treated"])
    cl, cu = group_bounds(data["control"])
    return tl - cu, tu - cl

def observed_case_diff(data):
    a, b = data["treated"], data["control"]
    return F(a[0], a[0] + a[1]) - F(b[0], b[0] + b[1])

def zero_imputation_diff(data):
    a, b = data["treated"], data["control"]
    return F(a[0], sum(a)) - F(b[0], sum(b))

class PublishedTableAudit(unittest.TestCase):
    def test_nregs_group_partitions(self):
        d = DATA["NREGS"]
        self.assertEqual(sum(d["treated"]), 7519)
        self.assertEqual(sum(d["control"]), 2928)
        self.assertEqual(sum(d["total"]), 10447)
        self.assertEqual(tuple(a+b for a,b in zip(d["treated"], d["control"])), d["total"])

    def test_ssp_group_partitions(self):
        d = DATA["SSP"]
        self.assertEqual(sum(d["treated"]), 2750)
        self.assertEqual(sum(d["control"]), 1082)
        self.assertEqual(sum(d["total"]), 3832)
        self.assertEqual(tuple(a+b for a,b in zip(d["treated"], d["control"])), d["total"])

    def test_district7_missingness(self):
        self.assertEqual(DATA["NREGS"]["district7"], (0, 0, 1425))
        self.assertEqual(DATA["SSP"]["district7"], (2, 0, 555))
        self.assertEqual(sum(DATA["SSP"]["district7"]), 557)

    def test_nregs_exact_sharp_bounds(self):
        d = DATA["NREGS"]
        self.assertEqual(group_bounds(d["treated"]), (F(2014,7519), F(5367,7519)))
        self.assertEqual(group_bounds(d["control"]), (F(493,2928), F(2210,2928)))
        self.assertEqual(diff_bounds(d), (F(2014,7519)-F(2210,2928), F(5367,7519)-F(493,2928)))

    def test_ssp_exact_sharp_bounds(self):
        d = DATA["SSP"]
        self.assertEqual(group_bounds(d["treated"]), (F(987,2750), F(1946,2750)))
        self.assertEqual(group_bounds(d["control"]), (F(206,1082), F(834,1082)))
        self.assertEqual(diff_bounds(d), (F(987,2750)-F(834,1082), F(1946,2750)-F(206,1082)))

    def test_sign_nonidentification(self):
        for d in DATA.values():
            lower, upper = diff_bounds(d)
            self.assertLess(lower, 0)
            self.assertGreater(upper, 0)

    def test_missing_as_zero_is_lower_group_prevalence(self):
        for d in DATA.values():
            a, b = d["treated"], d["control"]
            self.assertEqual(zero_imputation_diff(d), group_bounds(a)[0]-group_bounds(b)[0])

    def test_complete_case_diff_is_distinct(self):
        for d in DATA.values():
            self.assertNotEqual(observed_case_diff(d), zero_imputation_diff(d))

    def test_a2_case_denominators(self):
        self.assertEqual(A2_CASES[:4], (10191,10120,3789,3574))
        self.assertEqual((A2_CASES[0]-A2_CASES[1],A2_CASES[2]-A2_CASES[3],
                          A2_CASES[4]-A2_CASES[5]), (71,215,7012))

    def test_b1_case_denominators(self):
        self.assertEqual(tuple(a-b for a,b in B1_CASES),
                         (2826,3782,1370,912,1370,912,1311))
        self.assertEqual(len(B1_CASES),7)

    def test_distinct_missingness_variables(self):
        self.assertNotEqual(DATA["NREGS"]["total"][2], A2_CASES[0]-A2_CASES[1])
        self.assertNotEqual(DATA["SSP"]["total"][2], A2_CASES[2]-A2_CASES[3])

if __name__ == "__main__":
    unittest.main(verbosity=2)
    for name, d in DATA.items():
        print(name, "missing_treated",float(F(d["treated"][2],sum(d["treated"]))),
              "missing_control",float(F(d["control"][2],sum(d["control"]))))
        print(name, "prevalence_treated",tuple(map(float,group_bounds(d["treated"]))),
              "prevalence_control",tuple(map(float,group_bounds(d["control"]))))
        print(name, "difference_bounds",tuple(map(float,diff_bounds(d))),
              "complete_case",float(observed_case_diff(d)),
              "missing_zero",float(zero_imputation_diff(d)))
