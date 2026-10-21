"""R179 exact Beta posterior audit under three priors and five count processes.

All observable counts come from the pinned artificial R177 source distributions.
Beta posteriors use an IID working Bernoulli likelihood, potentially misspecified.
Two independent Fraction computations verify posterior moments and exact Beta CDF
at the true marginal rate. Only synthetic E1, no real subject data.
"""
from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as F
from hashlib import sha1,sha256
from itertools import product
from math import comb, factorial, log
from pathlib import Path
import json
import sys
import unittest
import zipfile

HERE=Path(__file__).resolve().parent
R177=HERE.parent/"R177"
PROTO=HERE.parent.parent/"protocols/R179_BETA_POSTERIOR_90_COUNT_WORLDS_PRESCORE_FREEZE_2026-10-21.md"
OUT=HERE/"R179_EXACT_RESULTS.json"
ACCEPT=HERE/"R179_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R179_Beta_Posterior_90_Exact_Count_Worlds.zip"
R177_SOURCE_BLOB="2d032513ce84141214b6b3f84df9c0ed9976a02b"
R177_RESULT_SHA256="57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535"
N_VALUES=(4,8,12)
P_VALUES=(F(1,4),F(1,2))
SOURCES=(
 ("IID_BIN","BIN",0),
 ("CLUSTERED_BB_C2","BB",0),
 ("CLUSTERED_BB_C8","BB",2),
 ("INACTIVE_ZIB_Z1_8","ZIB",0),
 ("INACTIVE_ZIB_Z1_4","ZIB",1),
)
PRIORS=(("U",1,1),("S",2,2),("A",1,3))
LOWER=F(1,40)
UPPER=F(39,40)


def verify_source():
    filename=R177/"r177_four_finite_count_families_exact.py"
    raw=filename.read_bytes()
    blob=sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()
    if blob!=R177_SOURCE_BLOB:
        raise ValueError("original R177 computational source identity changed")
    if sha256((R177/"R177_EXACT_RESULTS.json").read_bytes()).hexdigest()!=R177_RESULT_SHA256:
        raise ValueError("original R177 result SHA changed")
    sys.path.insert(0,str(R177))
    from r177_four_finite_count_families_exact import formula_pmf,event_dp
    return formula_pmf,event_dp


def worlds():
    for n,p,source,prior in product(N_VALUES,P_VALUES,SOURCES,PRIORS):
        name,family,regime=source
        label,a,b=prior
        yield n,p,name,family,regime,label,a,b


def beta_integral(A,B):
    """Independent exact Beta(A,B) normalization for positive integers."""
    if not (isinstance(A,int) and isinstance(B,int) and A>=1 and B>=1):
        raise ValueError("integer positive beta shape parameters required")
    return F(factorial(A-1)*factorial(B-1),factorial(A+B-1))


def posterior_shapes(a,b,n,k):
    if any(not isinstance(v,int) for v in (a,b,n,k)):
        raise ValueError("noninteger beta prior or sample size")
    if a<1 or b<1 or n<1 or k<0 or k>n:
        raise ValueError("invalid Bayesian posterior parameters")
    return a+k,b+n-k


def posterior_formula(a,b,n,k,p):
    """Method A: closed-form Beta moments and binomial-tail CDF identity."""
    A,B=posterior_shapes(a,b,n,k)
    mean=F(A,A+B)
    var=F(A*B,(A+B)**2*(A+B+1))
    cdf=sum((F(comb(A+B-1,j))*p**j*(1-p)**(A+B-1-j)
             for j in range(A,A+B)),F(0))
    return mean,var,cdf


def posterior_integral(a,b,n,k,p):
    """Method B: factorial Beta integrals and termwise polynomial integration."""
    A,B=posterior_shapes(a,b,n,k)
    norm=beta_integral(A,B)
    mean=beta_integral(A+1,B)/norm
    second=beta_integral(A+2,B)/norm
    var=second-mean**2
    integral=sum((F((-1)**i*comb(B-1,i))*p**(A+i)/F(A+i)
                  for i in range(B)),F(0))
    cdf=integral/norm
    return mean,var,cdf


def posterior_predictive_loss_float(pmf,n,p,a,b):
    truth=float(p)
    return sum(float(w)*(-truth*log(float(F(a+k,a+b+n)))
                         -(1-truth)*log(float(F(b+n-k,a+b+n))))
               for k,w in enumerate(pmf))


def posterior_predictive_loss_decimal(pmf,n,p,a,b):
    with localcontext() as ctx:
        ctx.prec=60
        truth=Decimal(p.numerator)/Decimal(p.denominator)
        acc=Decimal(0)
        for k,w in enumerate(pmf):
            q=Decimal(a+k)/Decimal(a+b+n)
            wt=Decimal(w.numerator)/Decimal(w.denominator)
            acc+=wt*(-truth*q.ln()-(1-truth)*(1-q).ln())
        return acc


def evaluate(pmf,n,p,a,b):
    if sum(pmf,F(0))!=1 or len(pmf)!=n+1:
        raise ValueError("invalid frozen count distribution")
    rows=[]
    mean_predictive=F(0)
    mse=F(0)
    posterior_uncertainty=F(0)
    coverage=F(0)
    for k,w in enumerate(pmf):
        r1=posterior_formula(a,b,n,k,p)
        r2=posterior_integral(a,b,n,k,p)
        if r1!=r2:
            raise AssertionError("independent posterior Beta routes diverge")
        mu,var,cdf=r1
        if not 0<mu<1 or not 0<var or not 0<=cdf<=1:
            raise AssertionError("invalid Bayesian posterior statistic")
        accepted=LOWER<=cdf<=UPPER
        mean_predictive+=w*mu
        mse+=w*(mu-p)**2
        posterior_uncertainty+=w*var
        if accepted:
            coverage+=w
        rows.append({
            "success_count":k,"source_weight":str(w),
            "posterior_shape_A":a+k,"posterior_shape_B":b+n-k,
            "posterior_predictive_mean":str(mu),
            "posterior_parameter_variance":str(var),
            "exact_posterior_cdf_at_true_p":str(cdf),
            "truth_inside_central_95_credible_interval":accepted,
            "independent_posterior_integral_parity":True,
        })
    if mean_predictive!=(a+n*p)/F(a+b+n):
        raise AssertionError("prior and true marginal expected posterior mean mismatch")
    floating=posterior_predictive_loss_float(pmf,n,p,a,b)
    decimal=posterior_predictive_loss_decimal(pmf,n,p,a,b)
    if abs(floating-float(decimal))>1e-12:
        raise AssertionError("independent posterior predictive score discrepancy")
    return {
       "expected_posterior_predictive_mean":str(mean_predictive),
       "expected_bias_to_true_marginal":str(mean_predictive-p),
       "true_expected_posterior_predictive_mean_MSE":str(mse),
       "expected_working_posterior_parameter_variance":str(posterior_uncertainty),
       "true_MSE_over_expected_working_variance":str(mse/posterior_uncertainty),
       "central_95_Beta_credible_interval_true_frequentist_coverage":str(coverage),
       "expected_independent_future_event_logloss_numeric":format(floating,".16g"),
       "independent_decimal_future_event_logloss":str(decimal),
       "training_count_posteriors":rows,
    }


def run():
    formula,dp=verify_source()
    cases=[]
    for n,p,name,family,regime,label,a,b in worlds():
        pmf=formula(family,n,p,regime)
        if pmf!=dp(family,n,p,regime):
            raise AssertionError("R177 pinned generator failed independent source parity")
        row={
            "sample_size":n,"true_marginal_p":str(p),
            "training_mechanism":name,"source_R177_family":family,
            "source_R177_regime":regime,
            "prior_label":label,"prior_a":a,"prior_b":b,
            "working_iid_beta_posterior_under_misspecification":True,
            "source_PMF":[str(x) for x in pmf],
            **evaluate(pmf,n,p,a,b)
        }
        cases.append(row)
    if len(cases)!=90 or sum(len(x["source_PMF"]) for x in cases)!=810:
        raise AssertionError("frozen 90 posterior world grid drifted")
    selected=[r for r in cases if r["sample_size"]==8 and r["true_marginal_p"]=="1/4"]
    if len(selected)!=15:
        raise AssertionError("fixed 15-configuration illustration incomplete")
    out={
        "research_id":"R179",
        "status":"E1_ARTIFICIAL_EXACT_IID_WORKING_BETA_POSTERIOR",
        "prior_grid":[{"label":lab,"a":a,"b":b} for lab,a,b in PRIORS],
        "source_frozen_python_git_blob":R177_SOURCE_BLOB,
        "source_frozen_result_sha256":R177_RESULT_SHA256,
        "source_count_mechanism_worlds":30,"prior_by_source_worlds":90,
        "full_source_count_PMF_cells":810,
        "all_two_independent_posterior_Beta_integral_and_CDF_routes_equal":True,
        "all_central_credible_interval_frequentist_coverages_exact":True,
        "fixed_n8_p_quarter_15_cases":selected,
        "worlds":cases,"true_real_human_or_historical_data_scored":False,
        "new_E2":0,"new_E3":0
    }
    OUT.write_text(json.dumps(out,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    acc={
       "research_id":"R179","state":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_BETA_POSTERIOR",
       "source_mechanism_worlds":30,"posterior_worlds":90,
       "source_PMF_cells":810,
       "R177_git_blob_and_results_SHA_authentic":True,
       "independent_Beta_posterior_moment_and_CDF_90_world_parity":True,
       "exact_equal_tailed_95_credible_frequentist_coverage":True,
       "independent_posterior_prediction_numeric_score_parity":True,
       "real_human_or_historical_research":False,"new_E2":0,"new_E3":0,
       "exact_results_sha256":sha256(OUT.read_bytes()).hexdigest()
    }
    ACCEPT.write_text(json.dumps(acc,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R179_MACHINE_ACCEPTANCE",json.dumps(acc,sort_keys=True))
    print("R179_LOCKED_15_MODEL_COMPARISON",json.dumps([
        {"source":x["training_mechanism"],"prior":x["prior_label"],
         "coverage":x["central_95_Beta_credible_interval_true_frequentist_coverage"],
         "MSE":x["true_expected_posterior_predictive_mean_MSE"],
         "posterior_variance":x["expected_working_posterior_parameter_variance"]}
        for x in selected],sort_keys=True))
    return out


def archive():
    with zipfile.ZipFile(ARCH,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for filename in (Path(__file__).name,OUT.name,ACCEPT.name):
            zi=zipfile.ZipInfo(filename,date_time=(2026,10,21,0,0,0))
            zi.compress_type=zipfile.ZIP_DEFLATED
            zi.external_attr=0o644<<16
            z.writestr(zi,(HERE/filename).read_bytes())
        zi=zipfile.ZipInfo(PROTO.name,date_time=(2026,10,21,0,0,0))
        zi.compress_type=zipfile.ZIP_DEFLATED
        zi.external_attr=0o644<<16
        z.writestr(zi,PROTO.read_bytes())
    print("R179_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestExactBetaPosterior(unittest.TestCase):
    def test_90_scenarios(self):
        self.assertEqual(len(list(worlds())),90)
    def test_PMF_cells_810(self):
        self.assertEqual(sum(n+1 for n,p,name,f,r,lab,a,b in worlds()),810)
    def test_prior_three(self):
        self.assertEqual(len(PRIORS),3)
    def test_source_sha_and_two_routes(self):
        a,b=verify_source()
        self.assertEqual(a("BIN",8,F(1,4),0),b("BIN",8,F(1,4),0))
    def test_beta_integral_uniform(self):
        self.assertEqual(beta_integral(1,1),F(1))
    def test_beta_integral_two_two(self):
        self.assertEqual(beta_integral(2,2),F(1,6))
    def test_uniform_prior_no_success(self):
        self.assertEqual(posterior_formula(1,1,4,0,F(1,4))[0],F(1,6))
    def test_uniform_prior_all_success(self):
        self.assertEqual(posterior_formula(1,1,4,4,F(1,4))[0],F(5,6))
    def test_uniform_prior_CDF_hand(self):
        self.assertEqual(posterior_formula(1,1,4,0,F(1,4))[2],
                         1-(1-F(1,4))**5)
    def test_beta_1_1_identity_CDF(self):
        self.assertEqual(posterior_integral(1,1,1,0,F(1,2))[2],F(3,4))
    def test_beta_posterior_symmetric_integrals(self):
        self.assertEqual(posterior_formula(2,2,4,2,F(1,2)),
                         posterior_integral(2,2,4,2,F(1,2)))
    def test_independent_all_prior_count_posteriors(self):
        for n,p,name,f,r,lab,a,b in worlds():
            for k in range(n+1):
                self.assertEqual(posterior_formula(a,b,n,k,p),
                                 posterior_integral(a,b,n,k,p))
    def test_every_source_distribution_parity(self):
        a,b=verify_source()
        for n,p,name,f,r,lab,aa,bb in worlds():
            self.assertEqual(a(f,n,p,r),b(f,n,p,r))
    def test_true_coverage_fraction_all(self):
        a,_=verify_source()
        for n,p,name,f,r,lab,aa,bb in worlds():
            cov=F(evaluate(a(f,n,p,r),n,p,aa,bb)["central_95_Beta_credible_interval_true_frequentist_coverage"])
            self.assertGreaterEqual(cov,0)
            self.assertLessEqual(cov,1)
    def test_positive_predictive_p_all(self):
        for n,p,name,f,r,lab,a,b in worlds():
            for k in range(n+1):
                mean=posterior_formula(a,b,n,k,p)[0]
                self.assertTrue(0<mean<1)
    def test_prior_asymmetric_point25_matches_expected_bias(self):
        a,b=verify_source()
        r=evaluate(a("BIN",8,F(1,4),0),8,F(1,4),1,3)
        self.assertEqual(r["expected_bias_to_true_marginal"],"0")
    def test_mismatched_prior_not_zero_bias(self):
        a,b=verify_source()
        r=evaluate(a("BIN",8,F(1,4),0),8,F(1,4),2,2)
        self.assertNotEqual(r["expected_bias_to_true_marginal"],"0")
    def test_nonnegative_Beta_variance(self):
        for A in range(1,8):
            for B in range(1,8):
                norm=beta_integral(A,B)
                var=beta_integral(A+2,B)/norm-(beta_integral(A+1,B)/norm)**2
                self.assertGreater(var,0)
    def test_decimal_log_parity(self):
        a,_=verify_source()
        p=F(1,4);pmf=a("BB",12,p,0)
        self.assertAlmostEqual(posterior_predictive_loss_float(pmf,12,p,1,1),
                               float(posterior_predictive_loss_decimal(pmf,12,p,1,1)),places=12)
    def test_all_90_scores_finite(self):
        a,_=verify_source()
        for n,p,name,f,r,lab,aa,bb in worlds():
            val=posterior_predictive_loss_float(a(f,n,p,r),n,p,aa,bb)
            self.assertTrue(val>0 and val<float("inf"))
    def test_invalid_zero_prior(self):
        with self.assertRaises(ValueError):
            posterior_shapes(0,1,4,0)
    def test_invalid_count(self):
        with self.assertRaises(ValueError):
            posterior_shapes(1,1,4,5)
    def test_invalid_integral(self):
        with self.assertRaises(ValueError):
            beta_integral(0,2)
    def test_exact_95_tail_thresholds(self):
        self.assertEqual((LOWER,UPPER),(F(1,40),F(39,40)))
    def test_source_counts_match_reference(self):
        self.assertEqual(len(SOURCES),5)
    def test_asym_prior_predictive_hand(self):
        self.assertEqual(posterior_formula(1,3,8,2,F(1,4))[0],F(3,12))


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run()
        archive()
    else:
        raise SystemExit("Use --test or --run-and-archive")
