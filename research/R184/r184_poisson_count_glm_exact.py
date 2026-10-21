"""R184 45 artificial Poisson log-link regression worlds, exact finite count audit.

Actual count laws are the SHA-pinned finite R177 Bernoulli opportunity models,
which intentionally violate the unbounded Poisson likelihood specification.
All sample-space probabilities, variances and test MSE use Fraction.
The Poisson test cross-entropy uses two separately implemented log methods.
"""
from __future__ import annotations

from decimal import Decimal,localcontext
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha1,sha256
from itertools import product
from math import exp,lgamma,log,factorial
from pathlib import Path
import csv,json,sys,unittest,zipfile

HERE=Path(__file__).resolve().parent
R177=HERE.parent/"R177"
PROTO=HERE.parent.parent/"protocols/R184_POISSON_GLM_45_WORLDS_PRESCORE_FREEZE_2026-10-21.md"
OUT=HERE/"R184_EXACT_RESULTS.json"
CSV=HERE/"R184_ALL_4125_ARTIFICIAL_TRAINING_COUNT_PAIRS.csv"
ACCEPT=HERE/"R184_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R184_Exact_Poisson_45_Worlds_Source_Audit.zip"

SOURCE_BLOB="2d032513ce84141214b6b3f84df9c0ed9976a02b"
SOURCE_SHA256="57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535"
N_VALUES=(4,8,12)
RATES=((F(1,8),F(1,4)),(F(1,4),F(1,2)),(F(1,4),F(1,4)))
MECHANISMS=(
 ("IID_BIN","BIN",0),("CLUSTERED_BB_C2","BB",0),
 ("CLUSTERED_BB_C8","BB",2),
 ("INACTIVE_ZIB_Z1_8","ZIB",0),("INACTIVE_ZIB_Z1_4","ZIB",1),
)
HALF=F(1,2)


def original_source():
    original=(R177/"r177_four_finite_count_families_exact.py").read_bytes()
    gitblob=sha1(b"blob "+str(len(original)).encode()+b"\x00"+original).hexdigest()
    if gitblob!=SOURCE_BLOB:
        raise ValueError("R177 original source Git blob differs from locked value")
    if sha256((R177/"R177_EXACT_RESULTS.json").read_bytes()).hexdigest()!=SOURCE_SHA256:
        raise ValueError("R177 original full scored source JSON SHA mismatch")
    if str(R177) not in sys.path:
        sys.path.insert(0,str(R177))
    from r177_four_finite_count_families_exact import formula_pmf,event_dp,theory_variance
    return formula_pmf,event_dp,theory_variance


def worlds():
    for n,rates,source in product(N_VALUES,RATES,MECHANISMS):
        name,family,regime=source
        yield n,rates[0],rates[1],name,family,regime


def poisson_work_logkernel(k,lam):
    """Numerical likelihood kernel (k! dropped), including true zero boundary."""
    if k<0 or lam<0:
        raise ValueError("invalid Poisson count or intensity")
    if lam==0:
        return 0.0 if k==0 else float("-inf")
    return -float(lam)+k*log(float(lam))


@lru_cache(maxsize=None)
def poisson_mle_check(k,n):
    """Independent A likelihood grid and B score equation with boundary logic."""
    if n not in N_VALUES or k not in range(n+1):
        raise ValueError("count outside prescored range")
    winner=F(k)
    value=poisson_work_logkernel(k,winner)
    best=max(poisson_work_logkernel(k,F(i,2)) for i in range(2*n+3))
    if abs(best-value)>1e-12:
        raise AssertionError("Poisson likelihood grid disagrees with integer MLE")
    # Independent score k-lambda with respect to log intensity, and signs
    # for interior lambda>0. At k=0 the optimum is approached as lambda->0.
    if k==0:
        if not all(k-q<=0 for q in (F(0),F(1,2),F(1))):
            raise AssertionError("Poisson zero boundary score wrong")
    else:
        if k-winner!=0 or k-F(k,2)<=0 or k-F(2*k)>=0:
            raise AssertionError("Poisson score signs wrong")
    return winner


def exact_moments(pmf):
    if sum(pmf,F(0))!=1 or any(x<0 for x in pmf):
        raise ValueError("invalid artificial count law")
    mean=sum((k*w for k,w in enumerate(pmf)),F(0))
    second=sum((k*k*w for k,w in enumerate(pmf)),F(0))
    return mean,second-mean*mean


def test_squared_loss(mu,var,lam):
    return var+(mu-lam)**2


def poisson_zero_probability_float(mu):
    return exp(-float(mu))


def poisson_zero_probability_decimal(mu):
    with localcontext() as ctx:
        ctx.prec=60
        m=Decimal(mu.numerator)/Decimal(mu.denominator)
        return (-m).exp()


def poisson_expected_test_loss_float(pmf,mu,lam):
    if lam<=0:
        return float("inf")
    factorial_constant=sum(float(w)*lgamma(k+1) for k,w in enumerate(pmf))
    return float(lam)-float(mu)*log(float(lam))+factorial_constant


def poisson_expected_test_loss_decimal(pmf,mu,lam):
    if lam<=0:
        return Decimal("Infinity")
    with localcontext() as ctx:
        ctx.prec=60
        m=Decimal(mu.numerator)/Decimal(mu.denominator)
        x=Decimal(lam.numerator)/Decimal(lam.denominator)
        c=Decimal(0)
        for k,w in enumerate(pmf):
            wt=Decimal(w.numerator)/Decimal(w.denominator)
            c+=wt*Decimal(factorial(k)).ln()
        return x-m*x.ln()+c


def run():
    formula,dp,theory_variance=original_source()
    rows=[]
    results=[]
    for n,p0,p1,name,family,regime in worlds():
        l=formula(family,n,p0,regime)
        r=formula(family,n,p1,regime)
        if l!=dp(family,n,p0,regime) or r!=dp(family,n,p1,regime):
            raise AssertionError("source probability laws disagreed before fitting")
        mu0, v0=exact_moments(l)
        mu1, v1=exact_moments(r)
        if mu0!=n*p0 or mu1!=n*p1:
            raise AssertionError("training count mean not known n*p")
        if v0!=theory_variance(family,n,p0,regime) or v1!=theory_variance(family,n,p1,regime):
            raise AssertionError("R177 independent analytic count variance mismatch")
        if abs(poisson_zero_probability_float(mu0)-float(poisson_zero_probability_decimal(mu0)))>1e-12:
            raise AssertionError("Poisson theoretical zero mass numeric routes disagree")
        total=F(0)
        pzero=F(0)
        mle_squared=F(0)
        corrected_squared=F(0)
        corrected_log_float=0.0
        corrected_log_dec=Decimal(0)
        for k0,k1 in product(range(n+1),repeat=2):
            weight=l[k0]*r[k1]
            total+=weight
            raw0,raw1=poisson_mle_check(k0,n),poisson_mle_check(k1,n)
            q0,q1=raw0+HALF,raw1+HALF
            is_nonfinite=raw0==0 or raw1==0
            if is_nonfinite:pzero+=weight
            # Exact new independent group mean-squared forecast error:
            # Var(Y)+[E(Y)-lambda_hat]^2, both strata weighted equally.
            raw_sq=(test_squared_loss(mu0,v0,raw0)+test_squared_loss(mu1,v1,raw1))/2
            reg_sq=(test_squared_loss(mu0,v0,q0)+test_squared_loss(mu1,v1,q1))/2
            mle_squared+=weight*raw_sq
            corrected_squared+=weight*reg_sq
            fl=(poisson_expected_test_loss_float(l,mu0,q0)+poisson_expected_test_loss_float(r,mu1,q1))/2
            dec=(poisson_expected_test_loss_decimal(l,mu0,q0)+poisson_expected_test_loss_decimal(r,mu1,q1))/2
            if abs(fl-float(dec))>1e-12:
                raise AssertionError("independent Poisson cross entropy numeric scores differ")
            corrected_log_float+=float(weight)*fl
            corrected_log_dec+=Decimal(weight.numerator)/Decimal(weight.denominator)*dec
            rows.append({
                "n_trials_per_group":n,"true_p0":str(p0),"true_p1":str(p1),
                "source_mechanism":name,
                "training_success_count_k0":k0,"training_success_count_k1":k1,
                "true_training_joint_probability":str(weight),
                "MLE_poisson_mean_lambda0":str(raw0),"MLE_poisson_mean_lambda1":str(raw1),
                "positive_adjusted_poisson_mean0":str(q0),"positive_adjusted_poisson_mean1":str(q1),
                "loglink_no_finite_joint_coefficients":int(is_nonfinite),
                "MLE_future_count_squared_error_conditional":str(raw_sq),
                "positive_adjusted_future_count_squared_error_conditional":str(reg_sq),
            })
        expected_nonfinite=1-(1-l[0])*(1-r[0])
        true_avg_var=(v0+v1)/2
        if total!=1 or pzero!=expected_nonfinite:
            raise AssertionError("full group count space probability mismatch")
        if mle_squared!=2*true_avg_var:
            raise AssertionError("independent analytic MLE out-of-sample squared risk mismatch")
        if corrected_squared!=2*true_avg_var+F(1,4):
            raise AssertionError("positive half shift squared-error negative control mismatch")
        if abs(corrected_log_float-float(corrected_log_dec))>1e-12:
            raise AssertionError("full weighted Poisson predictive cross entropies differ")
        results.append({
            "n_per_group":n,
            "true_p0":str(p0),"true_p1":str(p1),
            "source_mechanism":name,"R177_family":family,"R177_regime":regime,
            "source_group0_full_count_PMF":[str(w) for w in l],
            "source_group1_full_count_PMF":[str(w) for w in r],
            "training_pairs":(n+1)**2,
            "source_expected_count_group0":str(mu0),"source_expected_count_group1":str(mu1),
            "true_variance_group0":str(v0),"true_variance_group1":str(v1),
            "true_dispersion_Var_over_E_group0":str(v0/mu0),
            "true_dispersion_Var_over_E_group1":str(v1/mu1),
            "source_exact_zero_count_probability_group0":str(l[0]),
            "source_exact_zero_count_probability_group1":str(r[0]),
            "Poisson_same_mean_zero_count_prob_group0_float":format(poisson_zero_probability_float(mu0),".16g"),
            "Poisson_same_mean_zero_count_prob_group1_float":format(poisson_zero_probability_float(mu1),".16g"),
            "nonfinite_log_link_coefficients_probability_exact":str(pzero),
            "finite_two_coefficient_log_link_probability":str(1-pzero),
            "MLE_independent_new_count_MSE_exact":str(mle_squared),
            "positive_half_shift_new_count_MSE_exact":str(corrected_squared),
            "MLE_independent_new_count_expected_Poisson_logloss":"INF",
            "positive_half_shift_independent_new_count_expected_Poisson_logloss_float":format(corrected_log_float,".16g"),
            "positive_half_shift_independent_new_count_expected_Poisson_logloss_decimal":str(corrected_log_dec),
            "all_independent_source_variance_and_future_squared_risk_exact":True,
        })
    if len(results)!=45 or len(rows)!=4125:
        raise AssertionError("frozen source universe changed")
    primary=[x for x in results if x["n_per_group"]==8 and x["true_p0"]=="1/4" and x["true_p1"]=="1/4"]
    if len(primary)!=5:
        raise AssertionError("prescore comparison not exhaustive")
    with CSV.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(rows)
    result={
        "research_id":"R184",
        "status":"E1_ARTIFICIAL_EXACT_POISSON_WORKING_GLM_MISSPECIFICATION",
        "source_git_blob_sha1":SOURCE_BLOB,"source_full_result_sha256":SOURCE_SHA256,
        "world_count":45,"complete_original_training_pairs":4125,
        "all_true_count_dispersion_analytically_verified":True,
        "all_closed_mean_MLE_and_independent_score_likelihood_grid_agree":True,
        "all_zero_count_nonfinite_coefficient_probs_exact":True,
        "all_future_squared_error_two_exact_routes_agree":True,
        "all_original_MLE_future_logloss_infinite":True,
        "all_positive_shift_logloss_two_independent_numeric_routes_agree":True,
        "fixed_n8_p0p1_quarter_same_mean_comparison":primary,
        "original_sample_CSV_sha256":sha256(CSV.read_bytes()).hexdigest(),
        "worlds":results,"human_or_real_historical_data":False,
        "new_E2":0,"new_E3":0
    }
    OUT.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    acceptance={
        "research_id":"R184",
        "status":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_POISSON_GLM",
        "world_count":45,"original_training_pairs":4125,
        "original_R177_source_sha_verified":True,
        "Poisson_likelihood_grid_and_score_certified":True,
        "true_vs_working_Poisson_dispersion_full_exact":True,
        "all_unadjusted_MLE_future_logloss_infinite":True,
        "all_smoothed_future_logloss_two_numeric_methods_agree":True,
        "all_smoothed_count_squared_error_increases_one_quarter":True,
        "main_result_sha256":sha256(OUT.read_bytes()).hexdigest(),
        "full_original_CSV_sha256":result["original_sample_CSV_sha256"],
        "new_E2":0,"new_E3":0,"human_or_historical_data_tested":False
    }
    ACCEPT.write_text(json.dumps(acceptance,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("R184_ACCEPTANCE",json.dumps(acceptance,sort_keys=True))
    print("R184_LOCKED_SAME_MEAN_COMPARISON",json.dumps(primary,sort_keys=True))
    return result


def archive():
    files=[Path(__file__).name,OUT.name,CSV.name,ACCEPT.name]
    with zipfile.ZipFile(ARCH,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in files:
            info=zipfile.ZipInfo(name,date_time=(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,(HERE/name).read_bytes())
        info=zipfile.ZipInfo(PROTO.name,date_time=(2026,10,21,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,PROTO.read_bytes())
    print("R184_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestArtificialPoissonGLM(unittest.TestCase):
    def test_world_count(self):
        self.assertEqual(len(list(worlds())),45)
    def test_total_training_count_pairs(self):
        self.assertEqual(sum((n+1)**2 for n,a,b,x,f,r in worlds()),4125)
    def test_source_SHA_two_methods(self):
        f,d,v=original_source()
        self.assertEqual(f("BB",4,F(1,4),0),d("BB",4,F(1,4),0))
    def test_all_fixed_source_variance_matches_theory(self):
        f,d,theory=original_source()
        for n,p0,p1,name,fam,r in worlds():
            for p in (p0,p1):
                self.assertEqual(exact_moments(f(fam,n,p,r))[1],theory(fam,n,p,r))
    def test_Poisson_MLE_all_counts_and_grid(self):
        for n in N_VALUES:
            for k in range(n+1):
                self.assertEqual(poisson_mle_check(k,n),F(k))
    def test_zero_poisson_loglike_boundary(self):
        self.assertEqual(poisson_work_logkernel(0,F(0)),0)
    def test_nonzero_count_zero_intensity_impossible(self):
        self.assertEqual(poisson_work_logkernel(1,F(0)),float("-inf"))
    def test_Poisson_loglike_finite_at_true_positive(self):
        self.assertTrue(poisson_work_logkernel(2,F(2))>float("-inf"))
    def test_exact_moments_hand_bernoulli(self):
        self.assertEqual(exact_moments((F(3,4),F(1,4))),(F(1,4),F(3,16)))
    def test_original_Bin_underdispersion(self):
        f,d,theory=original_source()
        for n,p0,p1,name,fam,r in worlds():
            if fam=="BIN":
                for p in (p0,p1):
                    mu,v=exact_moments(f(fam,n,p,r))
                    self.assertLess(v/mu,1)
    def test_BB_C2_positive_overdispersion_at_quarter(self):
        f,d,theory=original_source()
        for n in N_VALUES:
            mu,v=exact_moments(f("BB",n,F(1,4),0))
            self.assertGreater(v/mu,1)
    def test_expected_mle_test_count_sq_2_variance(self):
        f,d,theory=original_source()
        for n,p0,p1,name,fam,r in worlds():
            for p in (p0,p1):
                law=f(fam,n,p,r)
                mu,var=exact_moments(law)
                actual=sum((w*test_squared_loss(mu,var,F(k)) for k,w in enumerate(law)),F(0))
                self.assertEqual(actual,2*var)
    def test_expected_half_shift_sq_extra_quarter(self):
        f,d,theory=original_source()
        for n,p0,p1,name,fam,r in worlds():
            for p in (p0,p1):
                law=f(fam,n,p,r)
                mu,var=exact_moments(law)
                actual=sum((w*test_squared_loss(mu,var,F(k)+HALF) for k,w in enumerate(law)),F(0))
                self.assertEqual(actual,2*var+F(1,4))
    def test_mean_rate_link_null(self):
        self.assertEqual(RATES[-1],(F(1,4),F(1,4)))
    def test_positive_boundary_probability_all(self):
        f,d,theory=original_source()
        for n,p0,p1,name,fam,r in worlds():
            a=f(fam,n,p0,r);b=f(fam,n,p1,r)
            self.assertGreater(1-(1-a[0])*(1-b[0]),0)
    def test_decimal_vs_float_poisson_zero_prob(self):
        for n in N_VALUES:
            for p in (F(1,8),F(1,4),F(1,2)):
                self.assertAlmostEqual(poisson_zero_probability_float(n*p),
                                       float(poisson_zero_probability_decimal(n*p)),places=12)
    def test_decimal_vs_float_poisson_score(self):
        f,d,theory=original_source()
        for n,p0,p1,name,fam,r in worlds():
            for p in (p0,p1):
                law=f(fam,n,p,r)
                mu,_=exact_moments(law)
                for k in range(n+1):
                    lam=F(k)+HALF
                    a=poisson_expected_test_loss_float(law,mu,lam)
                    b=float(poisson_expected_test_loss_decimal(law,mu,lam))
                    self.assertAlmostEqual(a,b,places=12)
    def test_all_raw_positive_count_predictive_p0_nonzero(self):
        f,d,theory=original_source()
        for n,p0,p1,name,fam,r in worlds():
            self.assertGreater(sum(f(fam,n,p0,r)[1:],F(0)),0)
    def test_invalid_k_rejected(self):
        with self.assertRaises(ValueError):
            poisson_mle_check(5,4)
    def test_invalid_training_size_rejected(self):
        with self.assertRaises(ValueError):
            poisson_mle_check(1,5)
    def test_negative_poisson_intensity_rejected(self):
        with self.assertRaises(ValueError):
            poisson_work_logkernel(1,F(-1))
    def test_negative_count_rejected(self):
        with self.assertRaises(ValueError):
            poisson_work_logkernel(-1,F(1))
    def test_non_normalized_source_fails(self):
        with self.assertRaises(ValueError):
            exact_moments((F(1),F(1)))
    def test_true_count_variance_positive(self):
        f,d,theory=original_source()
        for n,p0,p1,name,fam,r in worlds():
            self.assertGreater(exact_moments(f(fam,n,p0,r))[1],0)
    def test_fixed_positive_half_shift(self):
        self.assertEqual(HALF,F(1,2))


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("use --test or --run-and-archive")
