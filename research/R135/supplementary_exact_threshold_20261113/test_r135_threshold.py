#!/usr/bin/env python3
"""Standard-library checks for postfreeze R135 analytical boundary reproduction."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json
import unittest

HERE=Path(__file__).resolve().parent

def load(filename,name):
    spec=importlib.util.spec_from_file_location(name,str(HERE/filename))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

scan=load('r135_threshold_scan.py','r135_scan')
cert=load('r135_threshold_interval.py','r135_cert')

class R135BoundaryTests(unittest.TestCase):
    def test_original_published_benefit_counts_recomputed(self):
        expected={4:73,3:59,2:25,1.2:15,1.1:13}
        for b,n in expected.items():
            with self.subTest(benefit=b):
                r=scan.scan_one(.02,b=b)
                self.assertEqual(r['cooperative_mirror_orbits'],n)
                self.assertEqual(r['raw_alld'],256)

    def test_fixed_postfreeze_grid(self):
        expected={.02:25,.08:25,.12:23,.2:9,.24:7,.25:2,.28:2,.282:2,.283:0,.29:0,.5:0}
        for a,n in expected.items():
            with self.subTest(assignment_error=a):
                r=scan.scan_one(a)
                self.assertEqual(r['cooperative_mirror_orbits'],n)

    def test_threshold_exact_stationarity_and_allD_ties(self):
        a=F(2401,8502);h=F(49,74)
        norm=cert.NORMS[152];resident=cert.RESIDENTS[10]
        tp=cert.source_t(norm,resident,a)
        station=tp[0]*h*h+(tp[1]+tp[2])*h*(1-h)+tp[3]*(1-h)*(1-h)
        self.assertEqual(station,h)
        for m in (0,2,8):
            mutant=cert.RESIDENTS[m]
            tm=cert.source_t(norm,mutant,a)
            tg=tm[0]*h+tm[1]*(1-h)
            tb=tm[2]*h+tm[3]*(1-h)
            hm=tb/(1-tg+tb)
            margin=cert.help_prob(resident,h,h)-2*cert.help_prob(resident,h,hm)+cert.help_prob(mutant,hm,h)
            self.assertEqual(margin,F(0))

    def test_fraction_covering_receipt(self):
        receipt=json.loads((HERE/'R135_THRESHOLD_INTERVAL_CERTIFICATE_20261113.json').read_text())
        self.assertEqual(receipt['exact_fraction_evaluations'],48*(256*15-8))
        self.assertLess(F(receipt['maximum_certified_upper_resident_margin']),0)
        self.assertEqual(receipt['candidate_exact_threshold'],'2401/8502')

    def test_symbolic_witness_receipt(self):
        receipt=json.loads((HERE/'R135_THRESHOLD_SYMBOLIC_CERTIFICATE_20261113.json').read_text())
        self.assertEqual(receipt['number_mutants_checked'],15)
        self.assertEqual(receipt['number_mutants_with_roots_strictly_between_baseline_and_a0'],0)
        self.assertEqual(receipt['zero_payoff_mutant_ids_at_a0'],[0,2,8])

    def test_mirror_invariance_on_exception_set(self):
        exc={(di,pi) for di,pi in cert.EXCEPTIONS}
        for di,pi in exc:
            nd,pp=scan.mirror_pair(cert.NORMS[di],cert.RESIDENTS[pi])
            self.assertIn((cert.NORMS.index(nd),cert.RESIDENTS.index(pp)),exc)

    def test_derivative_bounds_are_sufficient(self):
        a=cert.A0
        denominator=1-2*(1-2*a)*(1-a)
        xbound=1/denominator
        L=(2+1/a)*xbound+1/a
        self.assertGreater(denominator,0)
        self.assertLess(L,19)
        self.assertLess(2+1/a,6)

if __name__=='__main__':unittest.main(verbosity=2)
