"""R184 post-freeze oracle-mean Poisson 95% prediction interval coverage.

All artificial count source probabilities and actual coverages are exact Fraction.
Poisson CDF cutoffs are proven with rational Taylor bounds on exp(mu), not
floating point approximations. Two independent source-law implementations:
closed form and sequential count-state dynamic programming.
No dependencies outside the Python standard library. No source data is fetched.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb, factorial
import argparse
import json
import unittest

SOURCE_R177_BLOB = "2d032513ce84141214b6b3f84df9c0ed9976a02b"
SOURCE_R184_RESULTS_BLOB = "f7d8ee20f9885594097de9cb6284bb48e7b6642b"
N_VALUES = (4, 8, 12)
P_VALUES = (F(1,8), F(1,4), F(1,2))
MECHANISMS = ("BIN", "BB_C2", "BB_C8", "ZIB_1_8", "ZIB_1_4")
LOW = F(1,40)
HIGH = F(39,40)
N_TAYLOR = 56


def model(family):
    if family == "BIN": return "BIN", F(0)
    if family == "BB_C2": return "BB", F(2)
    if family == "BB_C8": return "BB", F(8)
    if family == "ZIB_1_8": return "ZIB", F(1,8)
    if family == "ZIB_1_4": return "ZIB", F(1,4)
    raise ValueError("unknown family")


def rise(q, n):
    out = F(1)
    for i in range(n): out *= q + i
    return out


def source_closed(n, p, family):
    if n not in N_VALUES or p not in P_VALUES: raise ValueError("outside original 45 marginal designs")
    group, a = model(family)
    if group == "BIN":
        return tuple(F(comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1))
    if group == "BB":
        return tuple(F(comb(n,k))*rise(p*a,k)*rise((1-p)*a,n-k)/rise(a,n) for k in range(n+1))
    q = p/(1-a)
    return tuple((a if k==0 else F(0))+(1-a)*F(comb(n,k))*q**k*(1-q)**(n-k) for k in range(n+1))


def source_dp(n, p, family):
    """Independent sequential elementary-event implementation, no comb/rising."""
    group, a = model(family)
    if n not in N_VALUES or p not in P_VALUES: raise ValueError("bad grid")
    active = {0:F(1)}
    q0 = p/(1-a) if group == "ZIB" else p
    for t in range(n):
        nxt=defaultdict(F)
        for successes,prob in active.items():
            q=(p*a+successes)/(a+t) if group == "BB" else q0
            nxt[successes] += prob*(1-q)
            nxt[successes+1] += prob*q
        active=nxt
    if group == "ZIB":
        return tuple((a if k==0 else F(0))+(1-a)*active.get(k,F(0)) for k in range(n+1))
    return tuple(active.get(k,F(0)) for k in range(n+1))


@lru_cache(maxsize=None)
def exp_mu_bounds(mu):
    """Exact rational S <= exp(mu) <= S + next/(1-mu/(K+2))."""
    if not F(0) < mu <= 6: raise ValueError("mu outside supported model")
    s=sum((mu**i/F(factorial(i)) for i in range(N_TAYLOR+1)),F(0))
    first=mu**(N_TAYLOR+1)/F(factorial(N_TAYLOR+1))
    ratio=mu/F(N_TAYLOR+2)
    if not 0 < ratio < 1: raise ValueError("invalid tail ratio")
    return s,s+first/(1-ratio)


@lru_cache(maxsize=None)
def poisson_cdf_bounds(mu,k):
    if k<0: return F(0),F(0)
    numerator=sum((mu**j/F(factorial(j)) for j in range(k+1)),F(0))
    loexp,hiexp=exp_mu_bounds(mu)
    return numerator/hiexp,numerator/loexp


def poisson_quantile(mu, p):
    if p not in (LOW,HIGH): raise ValueError("cutoff not prespecified")
    for k in range(40):
        lo,hi=poisson_cdf_bounds(mu,k)
        if hi<p: continue
        if lo>=p:
            if k>0 and not poisson_cdf_bounds(mu,k-1)[1]<p:
                raise AssertionError("preceding Poisson cutpoint not ruled out")
            return k
        raise AssertionError("Taylor interval cannot certify Poisson quantile")
    raise AssertionError("Poisson quantile missing")


def empirical_quantile(mass, p):
    total=F(0)
    for k,weight in enumerate(mass):
        total += weight
        if total>=p:return k
    raise AssertionError("PMF unnormalized")


def fraction_stats(mass):
    s=sum(mass,F(0))
    mean=sum((k*q for k,q in enumerate(mass)),F(0))
    var=sum(((k-mean)**2*q for k,q in enumerate(mass)),F(0))
    return s,mean,var


def oracle_poisson_interval(mu):
    return poisson_quantile(mu,LOW),poisson_quantile(mu,HIGH)


def compute():
    rows=[]
    for n,p,f in product(N_VALUES,P_VALUES,MECHANISMS):
        mass=source_closed(n,p,f)
        dp=source_dp(n,p,f)
        if mass!=dp: raise AssertionError(f"independent source count law disagreement: {n,p,f}")
        total,mu,var=fraction_stats(mass)
        if total!=1 or mu!=n*p: raise AssertionError("source moment failed")
        L,U=oracle_poisson_interval(mu)
        true_coverage=sum(mass[L:U+1],F(0))
        OL,OU=empirical_quantile(mass,LOW),empirical_quantile(mass,HIGH)
        oracle_coverage=sum(mass[OL:OU+1],F(0))
        pblo=poisson_cdf_bounds(mu,U)[0]-poisson_cdf_bounds(mu,L-1)[1]
        pbhi=poisson_cdf_bounds(mu,U)[1]-poisson_cdf_bounds(mu,L-1)[0]
        if not pblo>=F(19,20) or not oracle_coverage>=F(19,20):
            raise AssertionError("oracle Poisson/source percentile invariant failed")
        rows.append({
            "n":n,"p":str(p),"family":f,"true_mean":str(mu),"true_variance":str(var),
            "dispersion":str(var/mu),"poisson_interval":[L,U],
            "poisson_interval_true_coverage":str(true_coverage),
            "poisson_interval_true_coverage_float":round(float(true_coverage),12),
            "nominal_95_undercovered":true_coverage<F(19,20),
            "source_oracle_interval":[OL,OU],"source_oracle_coverage":str(oracle_coverage),
            "poisson_assumed_coverage_rational_lower_bound":str(pblo),
            "poisson_assumed_coverage_rational_upper_bound":str(pbhi),
            "source_P0":str(mass[0]),"source_closed_vs_DP_exact":True
        })
    by_family={f:{"undercovered":sum(x["nominal_95_undercovered"] for x in rows if x["family"]==f),
                  "min_coverage":str(min(F(x["poisson_interval_true_coverage"]) for x in rows if x["family"]==f))}
               for f in MECHANISMS}
    worst=min(rows,key=lambda x:F(x["poisson_interval_true_coverage"]))
    results={"study":"R184 post-freeze oracle Poisson prediction interval calibration",
             "date":"2026-11-14", "evidence_grade":"INTERNAL_SYNTHETIC_MATHEMATICAL_E1",
             "frozen_protocol_changed":False,"new_E2":0,"new_E3":0,
             "source_R177_git_blob_sha1":SOURCE_R177_BLOB,
             "source_R184_results_git_blob_sha1":SOURCE_R184_RESULTS_BLOB,
             "interval_rule":"[smallest k with CDF_Pois(np)(k)>=1/40, smallest k with CDF_Pois(np)(k)>=39/40]",
             "oracle_mean_known":True,"future_event_source":"one independent finite count source unit",
             "total_distinct_marginal_designs":len(rows),"original_R184_two_group_marginals_with_repeats":90,
             "n_taylor_exponential_certificate_terms":N_TAYLOR+1,
             "Poisson_CDF_bound_method":"positive rational Taylor partial sum plus geometric-tail bound for exp(mu)",
             "undercovered_total":sum(x["nominal_95_undercovered"] for x in rows),
             "undercovered_by_family":by_family,"worst_case":worst,
             "all_source_true_oracle_coverage_at_least_95":True,
             "all_assumed_Poisson_coverage_certified_at_least_95":True,
             "rows":rows}
    return results


class TestCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.result=compute()
    def test_45_unique_source_marginals(self): self.assertEqual(len(self.result["rows"]),45)
    def test_source_closed_equals_sequential_45(self):
        for n,p,f in product(N_VALUES,P_VALUES,MECHANISMS):
            self.assertEqual(source_closed(n,p,f),source_dp(n,p,f))
    def test_pmf_normalized_45(self):
        for n,p,f in product(N_VALUES,P_VALUES,MECHANISMS):
            s,mu,_=fraction_stats(source_closed(n,p,f));self.assertEqual((s,mu),(1,n*p))
    def test_original_R184_n8_quarter_zero_masses(self):
        expected={"BIN":F(6561,65536),"BB_C2":F(12155,32768),"BB_C8":F(1,5),"ZIB_1_4":F(2443,8748)}
        for fam,q in expected.items():self.assertEqual(source_closed(8,F(1,4),fam)[0],q)
    def test_taylor_exponential_bounds(self):
        for mu in sorted(set(F(n)*p for n,p in product(N_VALUES,P_VALUES))):
            lo,hi=exp_mu_bounds(mu);self.assertLess(lo,hi)
            self.assertLess((hi-lo)/lo,F(1,10**30))
    def test_quantile_crossing_certified(self):
        for mu in sorted(set(F(n)*p for n,p in product(N_VALUES,P_VALUES))):
            for alpha in (LOW,HIGH):
                k=poisson_quantile(mu,alpha)
                self.assertGreaterEqual(poisson_cdf_bounds(mu,k)[0],alpha)
                if k:self.assertLess(poisson_cdf_bounds(mu,k-1)[1],alpha)
    def test_assumed_poisson_coverage_meets_95(self):
        for row in self.result["rows"]:
            self.assertGreaterEqual(F(row["poisson_assumed_coverage_rational_lower_bound"]),F(19,20))
    def test_true_oracle_coverage_meets_95(self):
        for row in self.result["rows"]:
            self.assertGreaterEqual(F(row["source_oracle_coverage"]),F(19,20))
    def test_own_source_variance_counterexample(self):
        row=next(r for r in self.result["rows"] if r["n"]==8 and r["p"]=="1/4" and r["family"]=="ZIB_1_8")
        self.assertEqual(row["dispersion"],"1")
        self.assertNotEqual(row["source_P0"],"1/8")
    def test_forced_example_zero_inflation(self):
        r=next(r for r in self.result["rows"] if r["n"]==12 and r["p"]=="1/2" and r["family"]=="ZIB_1_4")
        self.assertTrue(r["nominal_95_undercovered"])
        self.assertGreater(r["poisson_interval"][0],0)
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): source_closed(10,F(1,4),"BIN")
        with self.assertRaises(ValueError): source_dp(4,F(1,4),"UNKNOWN")
        with self.assertRaises(ValueError): poisson_quantile(F(2),F(1,2))
    def test_result_determinism(self):
        a=json.dumps(compute(),ensure_ascii=False,sort_keys=True,separators=(",",":"))
        b=json.dumps(compute(),ensure_ascii=False,sort_keys=True,separators=(",",":"))
        self.assertEqual(a,b)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test",action="store_true",help="Run all independent tests")
    args=parser.parse_args()
    if args.test:
        unittest.main(argv=[__file__],verbosity=2)
    else:
        print(json.dumps(compute(),ensure_ascii=False,indent=2,sort_keys=True))
