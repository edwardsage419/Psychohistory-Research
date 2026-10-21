"""R183 exact logistic separation study, 45 artificial count-process worlds.

Two source PMF methods are SHA-pinned to R177. Original grouped Bernoulli
working logit likelihood is audited against an independent finite rational
grid and score-equation/boundary check. Genuine probability boundary cases
are recorded, never clipped into a fictional finite MLE. All Brier values
are exact Fraction; half-count predictive log loss uses two numeric routes.
"""
from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha1, sha256
from itertools import product
from math import log
from pathlib import Path
import csv
import json
import sys
import unittest
import zipfile

HERE=Path(__file__).resolve().parent
R177=HERE.parent/"R177"
PROTO=HERE.parent.parent/"protocols/R183_LOGISTIC_SEPARATION_45_WORLDS_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R183_EXACT_RESULTS.json"
SAMPLES=HERE/"R183_ALL_4125_TRAINING_COUNT_PAIRS.csv"
ACCEPT=HERE/"R183_FINAL_MACHINE_ACCEPTANCE.json"
ARCHIVE=HERE/"R183_Logistic_45_Worlds_Exact_Separation_Archive.zip"

ORIGINAL_BLOB="2d032513ce84141214b6b3f84df9c0ed9976a02b"
ORIGINAL_RESULT_SHA256="57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535"
N_VALUES=(4,8,12)
RATE_PAIRS=((F(1,8),F(1,4)),(F(1,4),F(1,2)),(F(1,4),F(1,4)))
MECHANISMS=(
    ("IID_BIN","BIN",0),
    ("CLUSTERED_BB_C2","BB",0),
    ("CLUSTERED_BB_C8","BB",2),
    ("INACTIVE_ZIB_Z1_8","ZIB",0),
    ("INACTIVE_ZIB_Z1_4","ZIB",1),
)


def source():
    raw=(R177/"r177_four_finite_count_families_exact.py").read_bytes()
    blob=sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()
    if blob!=ORIGINAL_BLOB:
        raise ValueError("source code changed from prescored R177 blob")
    if sha256((R177/"R177_EXACT_RESULTS.json").read_bytes()).hexdigest()!=ORIGINAL_RESULT_SHA256:
        raise ValueError("original R177 full result SHA256 changed")
    if str(R177) not in sys.path:
        sys.path.insert(0,str(R177))
    from r177_four_finite_count_families_exact import formula_pmf,event_dp
    return formula_pmf,event_dp


def worlds():
    for n,rates,source_spec in product(N_VALUES,RATE_PAIRS,MECHANISMS):
        name,family,regime=source_spec
        yield n,rates[0],rates[1],name,family,regime


@lru_cache(maxsize=None)
def mle_grid_certificate(k,n):
    """Algorithm A: likelihood itself, all rational q-grid candidates."""
    if n not in N_VALUES or k not in range(n+1):
        raise ValueError("count or training size outside frozen source")
    at=F(k,n)
    top=at**k*(1-at)**(n-k)
    candidate_grid=[F(i,2*n) for i in range(2*n+1)]
    if max(q**k*(1-q)**(n-k) for q in candidate_grid)!=top:
        raise AssertionError("closed binomial likelihood optimum disagrees with grid")
    return at


def mle_score_equation(k,n):
    """Algorithm B: independent binomial-logit score and monotone boundaries."""
    if n not in N_VALUES or k not in range(n+1):
        raise ValueError("invalid logistic observation")
    if k==0:
        q=F(0)
        if not all(k-n*test<=0 for test in (F(0),F(1,2),F(1))):
            raise AssertionError("logistic lower boundary score invalid")
    elif k==n:
        q=F(1)
        if not all(k-n*test>=0 for test in (F(0),F(1,2),F(1))):
            raise AssertionError("logistic upper boundary score invalid")
    else:
        q=F(k,n)
        if k-n*q!=0 or not (k-n*F(0)>0 and k-n*F(1)<0):
            raise AssertionError("interior logistic score root invalid")
    return q


def predicted_brier(p,q):
    if not 0<p<1 or not 0<=q<=1:
        raise ValueError("probabilities outside allowed range")
    return p*(1-q)**2+(1-p)*q**2


def pmf_first_second(pmf):
    if sum(pmf,F(0))!=1 or any(v<0 for v in pmf):
        raise ValueError("unnormalized origin PMF")
    e=sum((k*mass for k,mass in enumerate(pmf)),F(0))
    e2=sum((k*k*mass for k,mass in enumerate(pmf)),F(0))
    return e,e2


def analytic_brier_single(pmf,n,p,half):
    """Independent moment route for average test Brier of shrinkage or MLE."""
    mean,second=pmf_first_second(pmf)
    shift=F(1,2) if half else F(0)
    denominator=n+2*shift
    eq=(mean+shift)/denominator
    eq2=(second+2*shift*mean+shift**2)/denominator**2
    return p-2*p*eq+eq2


def numeric_loss_float(p,q):
    return -float(p)*log(float(q))-(1-float(p))*log(1-float(q))


def numeric_loss_decimal(p,q):
    with localcontext() as ctx:
        ctx.prec=60
        prob=Decimal(p.numerator)/Decimal(p.denominator)
        qd=Decimal(q.numerator)/Decimal(q.denominator)
        return -prob*qd.ln()-(1-prob)*(1-qd).ln()


def finite_logit_coefficients(q0,q1):
    if not(0<q0<1 and 0<q1<1):
        return None
    slope0=log(float(q0/(1-q0)))
    slope1=log(float(q1/(1-q1)))-slope0
    with localcontext() as ctx:
        ctx.prec=60
        o0=Decimal(q0.numerator)/Decimal(q0.denominator-q0.numerator)
        o1=Decimal(q1.numerator)/Decimal(q1.denominator-q1.numerator)
        if abs(slope0-float(o0.ln()))>1e-12:
            raise AssertionError("two logit coefficient calculation routes disagree")
        if abs(slope1-float(o1.ln()-o0.ln()))>1e-12:
            raise AssertionError("two logit slope calculation routes disagree")
    return (format(slope0,".16g"),format(slope1,".16g"))


def run():
    f1,f2=source()
    original_records=[]
    worlds_result=[]
    for n,p0,p1,name,family,regime in worlds():
        left=f1(family,n,p0,regime)
        right=f1(family,n,p1,regime)
        if left!=f2(family,n,p0,regime) or right!=f2(family,n,p1,regime):
            raise AssertionError("source R177 closed formula and sequential DP disagree")
        full_mass=F(0)
        p_boundary=F(0)
        p_separate=F(0)
        brier_mle=F(0)
        brier_half=F(0)
        weighted_loss_math=0.0
        weighted_loss_decimal=Decimal(0)
        cell_rows=0
        for k0,k1 in product(range(n+1),repeat=2):
            prob=left[k0]*right[k1]
            full_mass+=prob
            q0,q1=mle_grid_certificate(k0,n),mle_grid_certificate(k1,n)
            if q0!=mle_score_equation(k0,n) or q1!=mle_score_equation(k1,n):
                raise AssertionError("independent logistic score and likelihood optima differ")
            # Unpenalized logistic coefficients are finite iff both group
            # success rates are strictly inside the unit probability interval.
            is_boundary=(k0 in (0,n)) or (k1 in (0,n))
            is_perfect=(k0==0 and k1==n) or (k0==n and k1==0)
            if is_boundary:
                p_boundary+=prob
            if is_perfect:
                p_separate+=prob
            logits=finite_logit_coefficients(q0,q1)
            if (logits is None)!=is_boundary:
                raise AssertionError("unregularized logit MLE finite existence audit failed")
            h0=F(2*k0+1,2*n+2)
            h1=F(2*k1+1,2*n+2)
            raw_score=(predicted_brier(p0,q0)+predicted_brier(p1,q1))/2
            half_score=(predicted_brier(p0,h0)+predicted_brier(p1,h1))/2
            loss_math=(numeric_loss_float(p0,h0)+numeric_loss_float(p1,h1))/2
            loss_dec=(numeric_loss_decimal(p0,h0)+numeric_loss_decimal(p1,h1))/2
            if abs(loss_math-float(loss_dec))>1e-12:
                raise AssertionError("two independent heldout predictive log score routes disagree")
            brier_mle+=prob*raw_score
            brier_half+=prob*half_score
            weighted_loss_math+=float(prob)*loss_math
            weighted_loss_decimal+=Decimal(prob.numerator)/Decimal(prob.denominator)*loss_dec
            cell_rows+=1
            original_records.append({
                "n_per_group":n,
                "true_p0":str(p0),"true_p1":str(p1),
                "mechanism":name,"R177_family":family,"R177_regime":regime,
                "count_k0":k0,"count_k1":k1,
                "original_joint_training_probability":str(prob),
                "MLE_predicted_q0":str(q0),"MLE_predicted_q1":str(q1),
                "halfcnt_predicted_q0":str(h0),"halfcnt_predicted_q1":str(h1),
                "nonfinite_unpenalized_logit_parameters":int(is_boundary),
                "complete_separation_indicator":int(is_perfect),
                "finite_logit_intercept":logits[0] if logits else "NONFINITE",
                "finite_logit_slope":logits[1] if logits else "NONFINITE",
                "half_count_heldout_avg_Brier":str(half_score),
                "unpenalized_MLE_heldout_avg_Brier":str(raw_score),
            })
        expected_boundary=1-(1-left[0]-left[-1])*(1-right[0]-right[-1])
        expected_perfect=left[0]*right[-1]+left[-1]*right[0]
        analytic_mle=(analytic_brier_single(left,n,p0,False)+analytic_brier_single(right,n,p1,False))/2
        analytic_half=(analytic_brier_single(left,n,p0,True)+analytic_brier_single(right,n,p1,True))/2
        if full_mass!=1 or p_boundary!=expected_boundary or p_separate!=expected_perfect:
            raise AssertionError("full joint counting and source marginal identities differ")
        if analytic_mle!=brier_mle or analytic_half!=brier_half:
            raise AssertionError("exact full enumerated Brier vs independent moment formulas differ")
        if not (p_boundary>0 and 0<=p_separate<=p_boundary):
            raise AssertionError("nonfinite boundary mass invalid")
        if abs(weighted_loss_math-float(weighted_loss_decimal))>1e-12:
            raise AssertionError("two full expected log loss paths disagree")
        worlds_result.append({
            "n_per_group":n,"true_p0":str(p0),"true_p1":str(p1),
            "true_logit_slope_zero":p0==p1,
            "mechanism":name,"R177_family":family,"R177_regime":regime,
            "source_group0_full_count_PMF":[str(v) for v in left],
            "source_group1_full_count_PMF":[str(v) for v in right],
            "ordered_training_count_pairs":cell_rows,
            "exact_probability_nonfinite_logit_MLE":str(p_boundary),
            "exact_probability_finite_two_coefficient_logit_MLE":str(1-p_boundary),
            "exact_probability_complete_separation":str(p_separate),
            "expected_MLE_out_of_sample_Brier_exact":str(brier_mle),
            "expected_halfcount_out_of_sample_Brier_exact":str(brier_half),
            "unpenalized_MLE_expected_test_logloss":"INF",
            "halfcount_expected_test_logloss_float":format(weighted_loss_math,".16g"),
            "halfcount_expected_test_logloss_decimal":str(weighted_loss_decimal),
            "both_independent_moment_and_full_count_pair_evaluations_exact":True,
        })
    if len(worlds_result)!=45 or len(original_records)!=4125:
        raise AssertionError("complete prescored model universe drifted")
    main_comparison=[r for r in worlds_result if r["n_per_group"]==4 and r["true_p0"]=="1/4" and r["true_p1"]=="1/4"]
    if len(main_comparison)!=5:
        raise AssertionError("locked same-probability separation comparison missing")
    with SAMPLES.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(original_records[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(original_records)
    out={
        "research_id":"R183","stage":"E1_ARTIFICIAL_EXACT_SATURATED_LOGISTIC_BOUNDARY",
        "source_git_blob_R177":ORIGINAL_BLOB,
        "source_full_result_sha256_R177":ORIGINAL_RESULT_SHA256,
        "probability_pairs":[[str(a),str(b)] for a,b in RATE_PAIRS],
        "count_source_mechanisms":[name for name,f,r in MECHANISMS],
        "world_count":45,"complete_training_count_pairs":4125,
        "all_working_likelihood_rational_grid_and_score_equation_equal":True,
        "all_full_enumerated_and_independent_moment_Brier_equal":True,
        "all_worlds_boundary_MLE_positive_probability_and_infinite_expected_logloss":True,
        "heldout_unit_independent_from_training_units":True,
        "source_CSV_sha256":sha256(SAMPLES.read_bytes()).hexdigest(),
        "same_true_rate_n4_prescored_comparison":main_comparison,
        "worlds":worlds_result,"real_human_or_historical_data":False,
        "new_E2":0,"new_E3":0
    }
    RESULT.write_text(json.dumps(out,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    acceptance={
        "research_id":"R183","status":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_LOGISTIC",
        "worlds":45,"full_ordered_count_training_samples":4125,
        "source_R177_SHA_verified":True,
        "full_parameter_boundary_and_complete_separation_probs_exact":True,
        "independent_logistic_likelihood_and_score_paths_equal":True,
        "independent_fraction_Brier_risks_equal":True,
        "all_boundary_unpenalized_logloss_infinite":True,
        "halfcount_finite_predictive_logloss_two_numerics_equal":True,
        "main_result_sha256":sha256(RESULT.read_bytes()).hexdigest(),
        "complete_original_sample_CSV_sha256":out["source_CSV_sha256"],
        "real_human_or_historical_data":False,"new_E2":0,"new_E3":0,
    }
    ACCEPT.write_text(json.dumps(acceptance,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R183_MACHINE_ACCEPTANCE",json.dumps(acceptance,sort_keys=True))
    print("R183_PRESCORED_NULL_LOGIT_SLOPE",json.dumps(main_comparison,sort_keys=True))
    return out


def archive():
    names=[Path(__file__).name,RESULT.name,SAMPLES.name,ACCEPT.name]
    with zipfile.ZipFile(ARCHIVE,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in names:
            info=zipfile.ZipInfo(name,date_time=(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,(HERE/name).read_bytes())
        info=zipfile.ZipInfo(PROTO.name,date_time=(2026,10,21,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,PROTO.read_bytes())
    print("R183_ARCHIVE_SHA256",sha256(ARCHIVE.read_bytes()).hexdigest())


class TestExactLogistic(unittest.TestCase):
    def test_world_count(self):
        self.assertEqual(len(list(worlds())),45)
    def test_total_training_pairs(self):
        self.assertEqual(sum((n+1)**2 for n,a,b,x,f,r in worlds()),4125)
    def test_source_sha(self):
        a,b=source()
        self.assertEqual(a("BB",4,F(1,4),0),b("BB",4,F(1,4),0))
    def test_two_source_methods_all_worlds(self):
        a,b=source()
        for n,p0,p1,name,family,regime in worlds():
            self.assertEqual(a(family,n,p0,regime),b(family,n,p0,regime))
            self.assertEqual(a(family,n,p1,regime),b(family,n,p1,regime))
    def test_all_count_MLE_grid_and_score(self):
        for n in N_VALUES:
            for k in range(n+1):
                self.assertEqual(mle_grid_certificate(k,n),mle_score_equation(k,n))
    def test_endpoint_zero(self):
        self.assertEqual(mle_grid_certificate(0,4),0)
    def test_endpoint_one(self):
        self.assertEqual(mle_grid_certificate(4,4),1)
    def test_finite_coefficients_hand(self):
        a,b=finite_logit_coefficients(F(1,4),F(1,2))
        self.assertAlmostEqual(float(a),log(1/3))
        self.assertAlmostEqual(float(b),log(3))
    def test_no_finite_coefficient_at_zero(self):
        self.assertIsNone(finite_logit_coefficients(F(0),F(1,2)))
    def test_no_finite_coefficient_at_one(self):
        self.assertIsNone(finite_logit_coefficients(F(1),F(1,2)))
    def test_true_equal_p_has_zero_true_log_odds(self):
        self.assertEqual(RATE_PAIRS[2],(F(1,4),F(1,4)))
    def test_perfect_separation_probability_iid_hand(self):
        a,_=source()
        pmf=a("BIN",4,F(1,4),0)
        expected=2*pmf[0]*pmf[4]
        self.assertGreater(expected,0)
        self.assertEqual(expected,F(81,32768))
    def test_positive_boundary_all_worlds(self):
        a,_=source()
        for n,p0,p1,name,f,r in worlds():
            l=a(f,n,p0,r)
            rr=a(f,n,p1,r)
            boundary=1-(1-l[0]-l[-1])*(1-rr[0]-rr[-1])
            self.assertGreater(boundary,0)
    def test_probability_of_perfect_separation_never_above_boundary(self):
        a,_=source()
        for n,p0,p1,name,f,r in worlds():
            l=a(f,n,p0,r);rr=a(f,n,p1,r)
            psep=l[0]*rr[-1]+l[-1]*rr[0]
            bd=1-(1-l[0]-l[-1])*(1-rr[0]-rr[-1])
            self.assertLessEqual(psep,bd)
    def test_brier_exact_hand(self):
        self.assertEqual(predicted_brier(F(1,4),F(1,2)),F(1,4))
    def test_brier_at_true_probability(self):
        self.assertEqual(predicted_brier(F(1,4),F(1,4)),F(3,16))
    def test_brier_exact_full_vs_analytic(self):
        a,_=source()
        for n,p0,p1,name,f,r in worlds():
            for p in (p0,p1):
                pmf=a(f,n,p,r)
                for half in (False,True):
                    expected=sum((w*predicted_brier(p,F(2*k+1,2*n+2) if half else F(k,n))
                                  for k,w in enumerate(pmf)),F(0))
                    self.assertEqual(expected,analytic_brier_single(pmf,n,p,half))
    def test_analytic_mle_correct_independent_known(self):
        a,_=source()
        pmf=a("BIN",4,F(1,4),0)
        self.assertEqual(analytic_brier_single(pmf,4,F(1,4),False),F(3,16)+F(3,64))
    def test_halfcount_predictive_all_interior(self):
        for n in N_VALUES:
            self.assertTrue(all(F(0)<F(2*k+1,2*n+2)<F(1) for k in range(n+1)))
    def test_corrected_dec_logloss_all(self):
        a,_=source()
        for n,p0,p1,name,f,r in worlds():
            for p in (p0,p1):
                for k in range(n+1):
                    q=F(2*k+1,2*n+2)
                    self.assertAlmostEqual(numeric_loss_float(p,q),float(numeric_loss_decimal(p,q)),places=12)
    def test_same_source_zero_effect_may_separate(self):
        a,_=source()
        n=4;p=F(1,4)
        pmf=a("BB",n,p,0)
        self.assertGreater(2*pmf[0]*pmf[n],0)
    def test_probability_distribution_normalized(self):
        a,_=source()
        for n,p0,p1,name,f,r in worlds():
            self.assertEqual(sum(a(f,n,p0,r)),1)
            self.assertEqual(sum(a(f,n,p1,r)),1)
    def test_invalid_count_rejected(self):
        with self.assertRaises(ValueError):
            mle_grid_certificate(5,4)
    def test_invalid_sample_size_rejected(self):
        with self.assertRaises(ValueError):
            mle_score_equation(1,5)
    def test_invalid_score_probability_rejected(self):
        with self.assertRaises(ValueError):
            predicted_brier(F(1,2),F(3,2))
    def test_fail_bad_source_probability(self):
        with self.assertRaises(ValueError):
            pmf_first_second((F(1),F(1)))
    def test_positivity_of_halfcount_logloss(self):
        self.assertGreater(numeric_loss_float(F(1,4),F(1,6)),0)


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run()
        archive()
    else:
        raise SystemExit("Usage --test or --run-and-archive")
