"""Independent postfreeze R185 artificial NB versus Poisson 95% central intervals.

Only standard library. Source R177 laws independently rebuilt with closed expressions
and sequential event-state dynamic programming. NB shapes are prespecified (2,6,8).
All NB probabilities and actual coverages use fractions.Fraction. Poisson CDF uses
80/110-digit Decimal crosschecks, and source counts are finite synthetic E1.
"""
from __future__ import annotations
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb, factorial
import json, argparse, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
N_VALUES=(4,8,12)
P_VALUES=(F(1,8),F(1,4),F(1,2))
SHAPES=(2,6,8)
MECHANISMS=(('BIN','BIN',0),('BB_C2','BB',2),('BB_C8','BB',8),('ZIB_1_8','ZIB',F(1,8)),('ZIB_1_4','ZIB',F(1,4)))
ALPHA=F(1,40)

def rising(x,k):
    v=F(1)
    for i in range(k): v*=x+i
    return v

def source_closed(n,p,kind,param):
    if n not in N_VALUES or p not in P_VALUES: raise ValueError('source grid')
    if kind=='BIN':
        return tuple(F(comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1))
    if kind=='BB':
        c=param
        return tuple(F(comb(n,k))*rising(p*c,k)*rising((1-p)*c,n-k)/rising(c,n) for k in range(n+1))
    if kind=='ZIB':
        z=param
        q=p/(1-z)
        if q>1: raise ValueError('invalid source rate')
        return tuple((z if k==0 else F(0))+(1-z)*F(comb(n,k))*q**k*(1-q)**(n-k) for k in range(n+1))
    raise ValueError('source kind')

def source_event_dp(n,p,kind,param):
    z=param if kind=='ZIB' else F(0)
    rate=p/(1-z) if kind=='ZIB' else p
    dist={0:F(1)}
    for i in range(n):
        nxt=defaultdict(F)
        for k,prob in dist.items():
            q=(p*param+k)/(param+i) if kind=='BB' else rate
            nxt[k]+=prob*(1-q)
            nxt[k+1]+=prob*q
        dist=nxt
    return tuple((z if k==0 else F(0))+(1-z)*dist.get(k,F(0)) for k in range(n+1))

def source_moments(law):
    mu=sum((k*q for k,q in enumerate(law)),F(0))
    var=sum(((k-mu)**2*q for k,q in enumerate(law)),F(0))
    return mu,var

def nb_closed(k,mu,r):
    if k<0 or mu<=0 or r not in SHAPES: raise ValueError('nb inputs')
    return F(comb(k+r-1,k))*F(r,r+mu)**r*F(mu,r+mu)**k

def nb_interval_direct(mu,r):
    # independent direct combinatorial method
    lo=hi=None; cdf=F(0)
    for k in range(300):
        cdf+=nb_closed(k,mu,r)
        if lo is None and cdf>=ALPHA: lo=k
        if hi is None and cdf>=1-ALPHA: hi=k;break
    if lo is None or hi is None: raise RuntimeError('unbounded NB quantile')
    return lo,hi

def nb_interval_recurrence(mu,r):
    # independent chain recurrence
    q=F(r,r+mu)**r
    cdf=F(0);lo=hi=None
    for k in range(300):
        cdf+=q
        if lo is None and cdf>=ALPHA:lo=k
        if hi is None and cdf>=1-ALPHA:hi=k;break
        q*=F(k+r,k+1)*F(mu,r+mu)
    if lo is None or hi is None:raise RuntimeError('NB recursion failed')
    return lo,hi

def poisson_cdf_dec(mu,k,prec):
    with localcontext() as ctx:
        ctx.prec=prec
        x=Decimal(mu.numerator)/Decimal(mu.denominator)
        prob=(-x).exp(); cdf=Decimal(0)
        for i in range(k+1):
            cdf+=prob
            prob*=x/Decimal(i+1)
        return +cdf

@lru_cache(maxsize=None)
def poisson_exp_rational_bounds(mu, order=64):
    """Rigorous rational bounds on exp(mu) for 0<mu<=6.

    Exponential Taylor remainder after term order is bounded by the first
    omitted term times a geometric tail with ratio at most mu/(order+2).
    """
    if not (F(0)<mu<=6 and order>=10 and F(mu,order+2)<1):
        raise ValueError('unsupported certified exponential bound')
    total=sum((mu**j / factorial(j) for j in range(order+1)),F(0))
    first=mu**(order+1)/factorial(order+1)
    upper=total+first/(1-F(mu,order+2))
    return total,upper

@lru_cache(maxsize=None)
def poisson_cdf_rational_bounds(mu,k):
    low_exp,high_exp=poisson_exp_rational_bounds(mu)
    poly=sum((mu**j / factorial(j) for j in range(k+1)),F(0))
    return poly/high_exp,poly/low_exp

@lru_cache(maxsize=None)
def poisson_interval(mu):
    # uses two independent Decimal precisions for all boundary comparisons
    lo=hi=None
    for k in range(150):
        c80=poisson_cdf_dec(mu,k,80)
        c110=poisson_cdf_dec(mu,k,110)
        if abs(c80-c110)>Decimal('1e-65'):raise ArithmeticError('Poisson high precision disagreement')
        c_low,c_high=poisson_cdf_rational_bounds(mu,k)
        for threshold in (ALPHA,1-ALPHA):
            if c_low<threshold<=c_high:
                raise ArithmeticError('Poisson CDF boundary not rationally certified')
        if lo is None and c_low>=ALPHA:lo=k
        if hi is None and c_low>=1-ALPHA:hi=k;break
    if lo is None or hi is None:raise RuntimeError('Poisson quantile not found')
    # verify both left and right endpoint transition
    for val,threshold in ((lo,ALPHA),(hi,1-ALPHA)):
        v_lower,v_upper=poisson_cdf_rational_bounds(mu,val)
        if v_lower<threshold:raise AssertionError('endpoint uncertified')
        if val>0:
            prev_lower,prev_upper=poisson_cdf_rational_bounds(mu,val-1)
            if prev_upper>=threshold:raise AssertionError('previous endpoint uncertified')
    return lo,hi

def source_interval(law):
    cumul=F(0);lo=hi=None
    for k,q in enumerate(law):
        cumul+=q
        if lo is None and cumul>=ALPHA:lo=k
        if hi is None and cumul>=1-ALPHA:hi=k;break
    return lo,hi

def coverage(law,interval):
    lo,hi=interval
    return sum(law[max(0,lo):min(len(law),hi+1)],F(0))

def interval_score_direct(law,interval):
    """Negatively oriented Gneiting-Raftery 2007 Eq43, alpha=1/20."""
    lo,hi=interval
    if lo<0 or hi<lo: raise ValueError('invalid interval')
    width=F(hi-lo)
    return sum((mass*(width+40*max(lo-y,0)+40*max(y-hi,0))
                for y,mass in enumerate(law)),F(0))

def interval_score_tail_moments(law,interval):
    """Independent sufficient-tail-moment formula, no direct per-observation score."""
    lo,hi=interval
    if lo<0 or hi<lo: raise ValueError('invalid interval')
    low_mass=sum(law[:lo],F(0))
    low_first=sum((i*q for i,q in enumerate(law[:lo])),F(0))
    high_mass=sum(law[hi+1:],F(0))
    high_first=sum((i*q for i,q in enumerate(law[hi+1:],hi+1)),F(0))
    return F(hi-lo)+40*(lo*low_mass-low_first+high_first-hi*high_mass)

def source_archive_fingerprint():
    """FNV1a64 over canonical 45 PMF rows; crosschecked with archived GitHub R177 JSON.

    Source authenticity additionally uses frozen Git blob SHA in provenance.
    This fast digest is for deterministic parity, not a cryptographic signature.
    """
    regime={'BIN':0,'BB_C2':0,'BB_C8':2,'ZIB_1_8':0,'ZIB_1_4':1}
    lines=[]
    for n,p,m in product(N_VALUES,P_VALUES,MECHANISMS):
        name,family,param=m
        law=source_closed(n,p,family,param)
        lines.append(f'{n}|{p}|{family}|{regime[name]}|'+ ';'.join(map(str,law))+'\n')
    buf=''.join(lines).encode('utf-8')
    h=0xcbf29ce484222325
    for b in buf:
        h^=b;h=(h*0x100000001b3)&((1<<64)-1)
    return format(h,'016x'),len(buf)

def run():
    allrows=[]
    for n,p,mechanism in product(N_VALUES,P_VALUES,MECHANISMS):
        name,kind,param=mechanism
        law=source_closed(n,p,kind,param)
        if law!=source_event_dp(n,p,kind,param) or sum(law,F(0))!=1:
            raise AssertionError('independent source probabilities failed')
        mu,var=source_moments(law)
        if mu!=n*p:raise AssertionError('source mean incorrect')
        pi=poisson_interval(mu)
        oi=source_interval(law)
        poc=coverage(law,pi);orc=coverage(law,oi)
        ps=interval_score_direct(law,pi);os=interval_score_direct(law,oi)
        if ps!=interval_score_tail_moments(law,pi) or os!=interval_score_tail_moments(law,oi):
            raise AssertionError('source and Poisson two interval-score paths disagree')
        if orc<F(19,20):raise AssertionError('oracle coverage missing')
        for r in SHAPES:
            ni=nb_interval_direct(mu,r)
            if ni!=nb_interval_recurrence(mu,r): raise AssertionError('NB quantiles disagree')
            c=coverage(law,ni)
            ns=interval_score_direct(law,ni)
            if ns!=interval_score_tail_moments(law,ni) or ns<os:
                raise AssertionError('NB score parity or oracle score bound failed')
            if ni[1]<ni[0]:raise AssertionError('invalid NB interval')
            momshape=mu**2/(var-mu) if var>mu else None
            row={"n":n,"p":str(p),"source":name,"mean":str(mu),"variance":str(var),"moment_shape":str(momshape) if momshape else None,
              "shape_r":r,"poisson_interval":list(pi),"NB_interval":list(ni),"source_oracle_interval":list(oi),
              "poisson_true_coverage":str(poc),"NB_true_coverage":str(c),"source_oracle_coverage":str(orc),
              "poisson_true_coverage_float":float(poc),"NB_true_coverage_float":float(c),
              "Poisson_expected_interval_score":str(ps),"NB_expected_interval_score":str(ns),
              "oracle_expected_interval_score":str(os),"NB_score_minus_Poisson":str(ns-ps),
              "NB_coverage_minus_Poisson":str(c-poc),"NB_under95":c<F(19,20),"Poisson_under95":poc<F(19,20),
              "NB_width":ni[1]-ni[0]+1,"Poisson_width":pi[1]-pi[0]+1,"oracle_width":oi[1]-oi[0]+1}
            allrows.append(row)
    summary={"study":"R185 postfreeze oracle mean fixed-shape NB vs Poisson equal-tail prediction interval calibration",
       "source":"R177 SHA-pinned synthetic finite count mechanisms and R185 original fixed shapes",
       "evidence":"internal synthetic E1 mathematical", "not_R185_frozen_rescore":True,"new_E2":0,"new_E3":0,
       "distinct_source_marginals":45,"NB_comparisons":len(allrows),"original_R185_135_worlds_two_group_marginals_with_repeats":270,
       "source_45_canonical_archive_FNV1a64":source_archive_fingerprint()[0],
       "source_45_canonical_bytes":source_archive_fingerprint()[1],
       "nominal":str(F(19,20)),"quantile_rule":"smallest k with model CDF >= 1/40 and 39/40",
       "Poisson_boundary":"independent 80/110 Decimal CDFs plus exact rational Taylor-order-64 upper/lower exponential certificates", 
       "shapes":{},"rows":allrows}
    for r in SHAPES:
        subset=[x for x in allrows if x['shape_r']==r]
        summary['shapes'][str(r)]={"source_count":len(subset),"NB_under95":sum(x['NB_under95'] for x in subset),
           "Poisson_under95":sum(x['Poisson_under95'] for x in subset),
           "NB_under_and_Poisson_not":sum(x['NB_under95'] and not x['Poisson_under95'] for x in subset),
           "NB_recovered_Poisson_undercoverage":sum((not x['NB_under95']) and x['Poisson_under95'] for x in subset),
           "NB_worse_coverage":sum(x['NB_true_coverage_float']<x['poisson_true_coverage_float']-1e-13 for x in subset),
           "NB_better_interval_score":sum(F(x['NB_score_minus_Poisson'])<0 for x in subset),
           "NB_worse_interval_score":sum(F(x['NB_score_minus_Poisson'])>0 for x in subset),
           "NB_tied_interval_score":sum(F(x['NB_score_minus_Poisson'])==0 for x in subset),
           "NB_mean_interval_score":str(sum((F(x['NB_expected_interval_score']) for x in subset),F(0))/len(subset)),
           "Poisson_mean_interval_score":str(sum((F(x['Poisson_expected_interval_score']) for x in subset),F(0))/len(subset)),
           "NB_wider":sum(x['NB_width']>x['Poisson_width'] for x in subset),
           "NB_equal_width":sum(x['NB_width']==x['Poisson_width'] for x in subset),
           "NB_narrower":sum(x['NB_width']<x['Poisson_width'] for x in subset),
           "NB_min_coverage":str(min((F(x['NB_true_coverage']) for x in subset))),
           "NB_max_coverage":str(max((F(x['NB_true_coverage']) for x in subset)))}
    return summary

class Tests(unittest.TestCase):
    def test_all_45_original_sources(self):
        self.assertEqual(len(list(product(N_VALUES,P_VALUES,MECHANISMS))),45)
    def test_formula_vs_event_dp(self):
        for n,p,m in product(N_VALUES,P_VALUES,MECHANISMS):
            self.assertEqual(source_closed(n,p,m[1],m[2]),source_event_dp(n,p,m[1],m[2]))
    def test_source_normalization(self):
        for n,p,m in product(N_VALUES,P_VALUES,MECHANISMS):
            self.assertEqual(sum(source_closed(n,p,m[1],m[2]),F(0)),1)
    def test_source_mean(self):
        for n,p,m in product(N_VALUES,P_VALUES,MECHANISMS):
            self.assertEqual(source_moments(source_closed(n,p,m[1],m[2]))[0],n*p)
    def test_nb_two_quantile_paths(self):
        for n,p,r in product(N_VALUES,P_VALUES,SHAPES):
            self.assertEqual(nb_interval_direct(n*p,r),nb_interval_recurrence(n*p,r))
    def test_nb_full_pmf_two_routes(self):
        for r in SHAPES:
            for mu in (F(1,2),F(2),F(6)):
                for k in range(30):
                    q=F(r,r+mu)**r
                    for y in range(k):q*=F(y+r,y+1)*F(mu,r+mu)
                    self.assertEqual(q,nb_closed(k,mu,r))
    def test_Poisson_95_condition(self):
        for n,p in product(N_VALUES,P_VALUES):
            mu=n*p;lo,hi=poisson_interval(mu)
            self.assertLessEqual(lo,hi)
            self.assertGreaterEqual(poisson_cdf_rational_bounds(mu,lo)[0],ALPHA)
            self.assertGreaterEqual(poisson_cdf_rational_bounds(mu,hi)[0],1-ALPHA)
            if lo:self.assertLess(poisson_cdf_rational_bounds(mu,lo-1)[1],ALPHA)
            if hi:self.assertLess(poisson_cdf_rational_bounds(mu,hi-1)[1],1-ALPHA)
    def test_rational_exp_bounds(self):
        for mu in (F(1,2),F(2),F(6)):
            low,high=poisson_exp_rational_bounds(mu)
            with localcontext() as ctx:
                ctx.prec=160
                exact=(Decimal(mu.numerator)/Decimal(mu.denominator)).exp()
                self.assertLess(Decimal(low.numerator)/Decimal(low.denominator),exact)
                self.assertGreater(Decimal(high.numerator)/Decimal(high.denominator),exact)
    def test_known_r185_equal_moments_different_zero(self):
        a=source_closed(8,F(1,4),'BB',8)
        b=source_closed(8,F(1,4),'ZIB',F(1,4))
        self.assertEqual(source_moments(a),(F(2),F(8,3)))
        self.assertEqual(source_moments(b),(F(2),F(8,3)))
        self.assertEqual(a[0],F(1,5));self.assertEqual(b[0],F(2443,8748))
    def test_oracle_interval_coverage(self):
        for n,p,m in product(N_VALUES,P_VALUES,MECHANISMS):
            law=source_closed(n,p,m[1],m[2]);self.assertGreaterEqual(coverage(law,source_interval(law)),F(19,20))
    def test_undercoverage_per_comparison(self):
        for x in run()['rows']:
            self.assertEqual(x['NB_under95'],F(x['NB_true_coverage'])<F(19,20))
            self.assertEqual(x['Poisson_under95'],F(x['poisson_true_coverage'])<F(19,20))
    def test_interval_score_dual_paths_all_sources(self):
        for n,p,m in product(N_VALUES,P_VALUES,MECHANISMS):
            law=source_closed(n,p,m[1],m[2])
            for interval in (poisson_interval(n*p),source_interval(law),
                             *(nb_interval_direct(n*p,r) for r in SHAPES)):
                self.assertEqual(interval_score_direct(law,interval),interval_score_tail_moments(law,interval))
    def test_true_source_interval_score_optimality(self):
        for n,p,m in product(N_VALUES,P_VALUES,MECHANISMS):
            law=source_closed(n,p,m[1],m[2])
            best=interval_score_direct(law,source_interval(law))
            for interval in (poisson_interval(n*p),*(nb_interval_direct(n*p,r) for r in SHAPES)):
                self.assertGreaterEqual(interval_score_direct(law,interval),best)
    def test_R177_source_45_crossarchive_digest(self):
        # Computed independently from the archived GitHub R177 world_data JSON.
        self.assertEqual(source_archive_fingerprint(),('3c59eec04a66770d',4946))
    def test_R184_poisson_original_fixed_counterexamples(self):
        a=source_closed(4,F(1,8),'BB',2)
        self.assertEqual(poisson_interval(F(1,2)),(0,2))
        self.assertEqual(coverage(a,(0,2)),F(1925,2048))
        b=source_closed(12,F(1,2),'ZIB',F(1,4))
        self.assertEqual(poisson_interval(F(6)),(2,11))
        self.assertEqual(coverage(b,(2,11)),F(131830,177147))
    def test_NB_lower_tail_structural_zero_failure(self):
        b=source_closed(12,F(1,2),'ZIB',F(1,4))
        self.assertEqual(nb_interval_direct(F(6),6),(1,14))
        self.assertEqual(nb_interval_direct(F(6),8),(1,13))
        self.assertEqual(coverage(b,(1,14)),F(132860,177147))
        self.assertLess(coverage(b,(1,14)),F(19,20))
    def test_equal_moments_different_NB_tail_coverages(self):
        a=source_closed(8,F(1,4),'BB',8)
        b=source_closed(8,F(1,4),'ZIB',F(1,4))
        self.assertEqual(source_moments(a),source_moments(b))
        self.assertEqual(nb_interval_direct(F(2),6),(0,6))
        self.assertEqual(coverage(a,(0,6)),F(2126,2145))
        self.assertEqual(coverage(b,(0,6)),F(8731,8748))
        self.assertNotEqual(source_interval(a),source_interval(b))
    def test_weak_shape_still_fails_heavy_tail(self):
        b=source_closed(12,F(1,8),'BB',2)
        self.assertEqual(nb_interval_direct(F(3,2),2),(0,6))
        self.assertEqual(coverage(b,(0,6)),F(8021048037,8589934592))
        self.assertLess(coverage(b,(0,6)),F(19,20))

    def test_invalid_source(self):
        with self.assertRaises(ValueError):source_closed(7,F(1,4),'BIN',0)
    def test_invalid_NB(self):
        with self.assertRaises(ValueError):nb_closed(-1,F(2),6)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--test',action='store_true');args=ap.parse_args()
    if args.test:
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
        result=unittest.TextTestRunner(verbosity=1).run(suite)
        if not result.wasSuccessful():raise SystemExit(1)
    else:
        print(json.dumps(run(),sort_keys=True,indent=2,ensure_ascii=False))
