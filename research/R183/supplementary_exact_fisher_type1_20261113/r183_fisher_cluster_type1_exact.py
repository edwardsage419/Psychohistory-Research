"""Post-freeze R183: exact false-positive probabilities for 2x2 Fisher tests.

Standalone Python 3.11+ standard-library study. The two groups are independent
clusters; n observations within a group may share a latent success propensity.
Original R183 45-world synthetic specifications are retained. Only the 15
zero-contrast worlds (p0=p1=1/4) are evaluated for Type I error.

Reference identities:
  R177 original blob 2d032513ce84141214b6b3f84df9c0ed9976a02b
  R183 original results blob 81f8fa790f0dea2715d99e1384ec33a6d2cf7a64
  R183 frozen protocol blob e01003e1899739b42b2ed746f1837b8591e870b6

No real subjects, observations, or new empirical scores are used.
"""
from __future__ import annotations

import argparse
import json
import unittest
from fractions import Fraction as F
from functools import lru_cache
from math import comb
from pathlib import Path

N_VALUES = (4, 8, 12)
P = F(1, 4)
ALPHA = F(1, 20)
MECHANISMS = ("IID_BIN", "CLUSTERED_BB_C2", "CLUSTERED_BB_C8", "INACTIVE_ZIB_Z1_8", "INACTIVE_ZIB_Z1_4")
SOURCES = {
    "R177_source_git_blob": "2d032513ce84141214b6b3f84df9c0ed9976a02b",
    "R183_source_git_blob": "d3aba985f8f7c7de21ca12f318f73abaa7fb3b0d",
    "R183_results_git_blob": "81f8fa790f0dea2715d99e1384ec33a6d2cf7a64",
    "R183_original_frozen_protocol_git_blob": "e01003e1899739b42b2ed746f1837b8591e870b6",
}


def rising(x: F, k: int) -> F:
    result = F(1)
    for i in range(k):
        result *= x+i
    return result


def source_parameters(mechanism: str):
    if mechanism == "IID_BIN":
        return "BIN", F(0)
    if mechanism == "CLUSTERED_BB_C2":
        return "BB", F(2)
    if mechanism == "CLUSTERED_BB_C8":
        return "BB", F(8)
    if mechanism == "INACTIVE_ZIB_Z1_8":
        return "ZIB", F(1,8)
    if mechanism == "INACTIVE_ZIB_Z1_4":
        return "ZIB", F(1,4)
    raise ValueError("unknown frozen R183 mechanism")


def exact_closed_pmf(mechanism: str, n: int, p: F=P) -> tuple[F,...]:
    """First route: R177's closed binomial, beta-binomial and ZIB mass formulas."""
    if n not in N_VALUES or not isinstance(p,F) or not 0<p<1:
        raise ValueError("unsupported sample size or marginal")
    family, param = source_parameters(mechanism)
    if family == "BIN":
        masses = tuple(F(comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1))
    elif family == "BB":
        c=param
        masses = tuple(F(comb(n,k))*rising(p*c,k)*rising((1-p)*c,n-k)/rising(c,n)
                       for k in range(n+1))
    else:
        z=param
        q=p/(1-z)
        if not 0<q<1:
            raise ValueError("invalid zero-inflated adjustment")
        masses = tuple((z if k==0 else F(0))+(1-z)*F(comb(n,k))*q**k*(1-q)**(n-k)
                       for k in range(n+1))
    if sum(masses,F(0))!=1 or min(masses)<0:
        raise ArithmeticError("source masses invalid")
    return masses


def exact_sequential_pmf(mechanism: str,n: int,p: F=P) -> tuple[F,...]:
    """Second route: event-by-event sequential probability dynamic programming.

    No use of binomial coefficients or rising factorials.
    """
    if n not in N_VALUES or not isinstance(p,F) or not 0<p<1:
        raise ValueError("unsupported sample size or marginal")
    family, param=source_parameters(mechanism)
    active_p=p/(1-param) if family=="ZIB" else p
    if not 0<active_p<1:
        raise ValueError("invalid source probability")
    dist={0:F(1)}
    for t in range(n):
        nxt={}
        for k,mass in dist.items():
            q=(p*param+k)/(param+t) if family=="BB" else active_p
            nxt[k]=nxt.get(k,F(0))+mass*(1-q)
            nxt[k+1]=nxt.get(k+1,F(0))+mass*q
        dist=nxt
    if family=="ZIB":
        dist={k:(F(param) if k==0 else F(0))+(1-param)*dist.get(k,F(0))
              for k in range(n+1)}
    values=tuple(dist.get(k,F(0)) for k in range(n+1))
    if sum(values,F(0))!=1 or min(values)<0:
        raise ArithmeticError("dynamic masses invalid")
    return values


@lru_cache(maxsize=None)
def table_pvalue(n: int, k0: int,k1: int) -> F:
    """Probability-ordering two-sided conditional Fisher p-value.

    For each feasible table with the same margins, include its hypergeometric
    mass when that mass is <= mass of the observed table. No mid-p correction.
    """
    if n not in N_VALUES or min(k0,k1)<0 or max(k0,k1)>n:
        raise ValueError("invalid 2x2 table")
    total=k0+k1
    bottom=comb(2*n,total)
    obs=F(comb(n,k0)*comb(n,total-k0),bottom)
    pvalue=F(0)
    for j in range(max(0,total-n),min(n,total)+1):
        mass=F(comb(n,j)*comb(n,total-j),bottom)
        # Independent combinatorial derivation: label successes then choose n units.
        alternative=F(comb(total,j)*comb(2*n-total,n-j),comb(2*n,n))
        if mass!=alternative:
            raise ArithmeticError("two hypergeometric derivations disagree")
        if mass<=obs:
            pvalue+=mass
    if not 0<pvalue<=1:
        raise ArithmeticError("Fisher p-value not normalized")
    return pvalue


def variance_and_icc(masses: tuple[F,...],n: int,p: F=P):
    mean=sum((F(k)*v for k,v in enumerate(masses)),F(0))
    var=sum(((F(k)-mean)**2*v for k,v in enumerate(masses)),F(0))
    if mean!=n*p:
        raise ArithmeticError("wrong marginal probability")
    standard=n*p*(1-p)
    icc=(var/standard-1)/F(n-1)
    return var,icc


def rejection_probability(masses: tuple[F,...], n:int, alpha:F=ALPHA) -> F:
    if not 0<alpha<1 or len(masses)!=n+1 or sum(masses,F(0))!=1:
        raise ValueError("invalid rejection inputs")
    return sum((masses[k0]*masses[k1] for k0 in range(n+1) for k1 in range(n+1)
                if table_pvalue(n,k0,k1)<=alpha),F(0))


def oracle_rejection_probability(masses: tuple[F,...],n:int,alpha:F=ALPHA)->F:
    """Theoretical oracle: exact |K1-K0| p-value under the known true null PMF.

    This benchmark is unattainable in ordinary applied research where the
    nuisance success probability and intra-cluster mechanism are unknown.
    """
    gap_mass={g:F(0) for g in range(n+1)}
    for a,v0 in enumerate(masses):
        for b,v1 in enumerate(masses):
            gap_mass[abs(b-a)]+=v0*v1
    if sum(gap_mass.values(),F(0))!=1:
        raise ArithmeticError("oracle gap distribution invalid")
    tail={g:sum((mass for gg,mass in gap_mass.items() if gg>=g),F(0)) for g in gap_mass}
    return sum((mass for g,mass in gap_mass.items() if tail[g]<=alpha),F(0))


def direct_null_probability_check(n:int, masses:tuple[F,...], threshold:F)->F:
    """Independent expectation path: sum over realized |K1-K0| frequency."""
    return sum((masses[a]*masses[b] for a in range(n+1) for b in range(n+1)
                if table_pvalue(n,a,b)<=threshold),F(0))


def run():
    rows=[]
    for n in N_VALUES:
        for mechanism in MECHANISMS:
            exact=exact_closed_pmf(mechanism,n)
            seq=exact_sequential_pmf(mechanism,n)
            if exact!=seq:
                raise ArithmeticError("closed and event-DP distributions diverge")
            var,icc=variance_and_icc(exact,n)
            failure=rejection_probability(exact,n)
            independent=direct_null_probability_check(n,seq,ALPHA)
            if failure!=independent:
                raise ArithmeticError("independent null expectation mismatched")
            oracle=oracle_rejection_probability(exact,n)
            if oracle>ALPHA:
                raise ArithmeticError("oracle exceeded nominal type I")
            rows.append({
                "n_per_group":n,"mechanism":mechanism,"true_p0":"1/4","true_p1":"1/4",
                "null_true":True,"total_independent_clusters":2,"events_in_each_cluster":n,
                "exact_count_variance":str(var),"exact_intracluster_correlation":str(icc),
                "assumed_independent_Fisher_alpha":"1/20",
                "actual_null_Fisher_rejection_probability":str(failure),
                "actual_null_Fisher_rejection_pct":round(100*float(failure),6),
                "nominal_rate_multiple":round(float(failure/ALPHA),8),
                "known_full_null_PMF_oracle_type1":str(oracle),
                "known_full_null_PMF_oracle_type1_pct":round(100*float(oracle),6),
                "exact_Fisher_pvalues_checked":(n+1)**2,
                "independent_closed_and_event_DP_PMF_agree":True,
                "two_hypergeom_combinatorial_routes_agree":True,
            })
    ref={r["mechanism"]:r for r in rows if r["n_per_group"]==12}
    if ref["CLUSTERED_BB_C8"]["exact_intracluster_correlation"]!="1/9" or ref["INACTIVE_ZIB_Z1_4"]["exact_intracluster_correlation"]!="1/9":
        raise ArithmeticError("equal-ICC counterexample invalid")
    if ref["CLUSTERED_BB_C8"]["actual_null_Fisher_rejection_probability"]==ref["INACTIVE_ZIB_Z1_4"]["actual_null_Fisher_rejection_probability"]:
        raise ArithmeticError("equal-ICC distinct-tail counterexample disappeared")
    total=sum((n+1)**2*len(MECHANISMS) for n in N_VALUES)
    return {
        "research_id":"R183","date":"2026-11-13",
        "study":"post-freeze exact null false-positive test under R177/R183 dependency",
        "evidence_level":"INTERNAL_E1_ARTIFICIAL_EXACT",
        "sources":SOURCES,
        "original_R183_frozen_data_or_protocol_modified":False,
        "original_45_worlds":45,
        "null_worlds":len(rows),
        "full_training_count_pairs":total,
        "nominal_alpha":"1/20",
        "test":"two-sided probability-ordered Fisher conditional hypergeometric, p<=alpha",
        "true_null":"p0=p1=1/4 in each world; independent group units; within-group mechanism varies",
        "rows":rows,
        "negative_control":"same ICC 1/9 at n12 for BB concentration8 vs ZIB weight1/4, unequal rejection tails",
        "validity":"full finite source PMF under model assumptions; not repeated randomized trials or an estimated real-world false-positive rate",
        "new_E2":0,"new_E3":0,"outside_team_replication":False,
        "R073":"FROZEN","PESEN_v0.1":"FROZEN"}


class TestExactTypeOne(unittest.TestCase):
    def test_frozen_n_and_mechanism_grid(self):
        self.assertEqual(len(N_VALUES)*len(MECHANISMS),15)
    def test_source_mass_formula_and_event_dp(self):
        for n in N_VALUES:
            for m in MECHANISMS:
                self.assertEqual(exact_closed_pmf(m,n),exact_sequential_pmf(m,n))
    def test_source_manual_pmf_n4(self):
        self.assertEqual(exact_closed_pmf("IID_BIN",4),tuple(F(k,256) for k in (81,108,54,12,1)))
        self.assertEqual(exact_closed_pmf("CLUSTERED_BB_C2",4),tuple(F(k,128) for k in (63,28,18,12,7)))
    def test_two_hypergeometric_routes_each_feasible_table(self):
        for n in N_VALUES:
            for a in range(n+1):
                for b in range(n+1):
                    self.assertTrue(F(0)<table_pvalue(n,a,b)<=1)
    def test_probability_order_is_symmetric_in_groups(self):
        for n in N_VALUES:
            for a in range(n+1):
                for b in range(n+1):
                    self.assertEqual(table_pvalue(n,a,b),table_pvalue(n,b,a))
    def test_n4_reject_exactly_opposite_boundary(self):
        n=4
        sig={(a,b) for a in range(n+1) for b in range(n+1) if table_pvalue(n,a,b)<=ALPHA}
        self.assertEqual(sig,{(0,4),(4,0)})
    def test_main_n12_bb_c2_overrejection(self):
        p=rejection_probability(exact_closed_pmf("CLUSTERED_BB_C2",12),12)
        self.assertEqual(p,F(2459701310851,8796093022208))
        self.assertGreater(p,F(1,4))
    def test_n4_fisher_equals_original_R183_complete_separation(self):
        # Exact values independently extracted from archived R183_EXACT_RESULTS.json.
        expected={
            "IID_BIN": F(81,32768),
            "CLUSTERED_BB_C2": F(441,8192),
            "CLUSTERED_BB_C8": F(7,605),
            "INACTIVE_ZIB_Z1_8": F(484,117649),
            "INACTIVE_ZIB_Z1_4": F(43,5832),
        }
        for name,original in expected.items():
            self.assertEqual(rejection_probability(exact_closed_pmf(name,4),4),original)

    def test_iid_is_conservative(self):
        for n in N_VALUES:
            self.assertLess(rejection_probability(exact_closed_pmf("IID_BIN",n),n),ALPHA)
    def test_oracle_never_exceeds_nominal(self):
        for n in N_VALUES:
            for m in MECHANISMS:
                self.assertLessEqual(oracle_rejection_probability(exact_closed_pmf(m,n),n),ALPHA)
    def test_same_icc_different_false_positive(self):
        n=12
        a=exact_closed_pmf("CLUSTERED_BB_C8",n)
        b=exact_closed_pmf("INACTIVE_ZIB_Z1_4",n)
        self.assertEqual(variance_and_icc(a,n),variance_and_icc(b,n))
        self.assertNotEqual(rejection_probability(a,n),rejection_probability(b,n))
    def test_optimized_source_invariants_are_runtime_checks(self):
        self.assertRaises(ValueError,exact_closed_pmf,"UNSUPPORTED",4)
        self.assertRaises(ValueError,table_pvalue,4,-1,0)
        self.assertRaises(ValueError,rejection_probability,(F(1),),4)
    def test_all_15_worlds_reported_and_accounted(self):
        d=run()
        self.assertEqual(len(d["rows"]),15)
        self.assertEqual(d["full_training_count_pairs"],sum(5*(n+1)**2 for n in (4,8,12)))


def main():
    arg=argparse.ArgumentParser()
    arg.add_argument("--test",action="store_true",help="run built-in unittest suite")
    arg.add_argument("--output",type=Path,help="write deterministic result JSON to path")
    opts=arg.parse_args()
    if opts.test:
        unittest.main(argv=[__file__],verbosity=2,exit=False)
    else:
        text=json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2)+"\n"
        if opts.output:
            opts.output.write_text(text,encoding="utf-8")
        else:
            print(text,end="")

if __name__=="__main__":
    main()
