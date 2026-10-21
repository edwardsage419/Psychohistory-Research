"""R185 negative binomial versus Poisson prediction on fixed artificial sources.

Source laws are SHA pinned to R177. NB predictive probability is constructed
by both a closed Fraction formula and independent exact recurrence. The NB
shape is prespecified, never chosen using observed test scores. All numeric
log scores are checked by math and 60-digit Decimal implementations.
"""
from __future__ import annotations

from decimal import Decimal,localcontext
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha1,sha256
from itertools import product
from math import comb, factorial, lgamma,log
from pathlib import Path
import csv,json,sys,unittest,zipfile

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/"R177"
PROTO=HERE.parent.parent/"protocols/R185_NEGATIVE_BINOMIAL_135_WORLDS_PRESCORE_FREEZE_2026-10-21.md"
OUT=HERE/"R185_EXACT_RESULTS.json"
TRAIN=HERE/"R185_ALL_12375_SOURCE_WEIGHTED_TRAINING_PAIRS.csv"
ACCEPT=HERE/"R185_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R185_135_Negative_Binomial_Exact_Count_Worlds.zip"
R177_BLOB="2d032513ce84141214b6b3f84df9c0ed9976a02b"
R177_JSON_SHA="57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535"
N_VALUES=(4,8,12)
RATE_PAIRS=((F(1,8),F(1,4)),(F(1,4),F(1,2)),(F(1,4),F(1,4)))
SOURCE_MECHANISMS=(
 ("IID_BIN","BIN",0),
 ("CLUSTERED_BB_C2","BB",0),
 ("CLUSTERED_BB_C8","BB",2),
 ("INACTIVE_ZIB_Z1_8","ZIB",0),
 ("INACTIVE_ZIB_Z1_4","ZIB",1),
)
SHAPES=(2,6,8)


def source():
    raw=(SOURCE/"r177_four_finite_count_families_exact.py").read_bytes()
    blob=sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()
    if blob!=R177_BLOB:
        raise ValueError("R177 program not the frozen Git blob")
    if sha256((SOURCE/"R177_EXACT_RESULTS.json").read_bytes()).hexdigest()!=R177_JSON_SHA:
        raise ValueError("R177 original full source result SHA mismatch")
    if str(SOURCE) not in sys.path:
        sys.path.insert(0,str(SOURCE))
    from r177_four_finite_count_families_exact import formula_pmf,event_dp,theory_variance
    return formula_pmf,event_dp,theory_variance


def worlds():
    for n,pair,mechanism,r in product(N_VALUES,RATE_PAIRS,SOURCE_MECHANISMS,SHAPES):
        name,family,regime=mechanism
        yield n,pair[0],pair[1],name,family,regime,r


def validate(y,lam,r):
    if not (isinstance(y,int) and y>=0 and isinstance(r,int) and r>0 and lam>0):
        raise ValueError("invalid NB shape/count/positive intensity")


def nb_closed_pmf(y,lam,r):
    """Method A: exact count PMF of untruncated NB(mean lam, shape r)."""
    validate(y,lam,r)
    return F(comb(y+r-1,y))*F(r,r+lam)**r*F(lam,r+lam)**y


def nb_recurrence_probabilities(lam,r,max_y):
    """Method B: initial P0 and independent NB event-count recursion."""
    validate(0,lam,r)
    if max_y<0:
        raise ValueError("negative source support")
    p0=F(r,r+lam)**r
    results=[p0]
    for y in range(max_y):
        results.append(results[-1]*F(y+r,y+1)*F(lam,r+lam))
    return tuple(results)


def true_moments(count_pmf):
    if sum(count_pmf,F(0))!=1 or any(q<0 for q in count_pmf):
        raise ValueError("invalid original count PMF")
    mu=sum((k*q for k,q in enumerate(count_pmf)),F(0))
    variance=sum((q*(k-mu)**2 for k,q in enumerate(count_pmf)),F(0))
    return mu,variance


def shape_moment(mu,var):
    if var<=mu:
        return None
    return mu*mu/(var-mu)


def poisson_future_float(law,lam):
    mu,_=true_moments(law)
    return float(lam)-float(mu)*log(float(lam))+sum(float(w)*lgamma(y+1) for y,w in enumerate(law))


def poisson_future_decimal(law,lam):
    with localcontext() as ctx:
        ctx.prec=60
        mu,_=true_moments(law)
        m=Decimal(mu.numerator)/Decimal(mu.denominator)
        intensity=Decimal(lam.numerator)/Decimal(lam.denominator)
        return intensity-m*intensity.ln()+sum(
            (Decimal(w.numerator)/Decimal(w.denominator))*Decimal(factorial(y)).ln()
            for y,w in enumerate(law)
        )


def nb_future_float(law,lam,r):
    predictions=nb_recurrence_probabilities(lam,r,len(law)-1)
    return sum(float(w)*(-log(float(v))) for w,v in zip(law,predictions))


def nb_future_decimal(law,lam,r):
    with localcontext() as ctx:
        ctx.prec=60
        mass=nb_recurrence_probabilities(lam,r,len(law)-1)
        return sum(
            (Decimal(w.numerator)/Decimal(w.denominator))*
            -(Decimal(q.numerator)/Decimal(q.denominator)).ln()
            for w,q in zip(law,mass)
        )


@lru_cache(maxsize=None)
def conditional_scores(law,lam,r):
    for y,q in enumerate(nb_recurrence_probabilities(lam,r,len(law)-1)):
        if nb_closed_pmf(y,lam,r)!=q:
            raise AssertionError("NB full PMF direct formula and recursion differ")
    pf=poisson_future_float(law,lam)
    pd=poisson_future_decimal(law,lam)
    nf=nb_future_float(law,lam,r)
    nd=nb_future_decimal(law,lam,r)
    if abs(pf-float(pd))>1e-12 or abs(nf-float(nd))>1e-12:
        raise AssertionError("independent numeric Poisson or NB cross entropy disagreed")
    return pf,pd,nf,nd


def run():
    formula,events,theory=source()
    all_rows=[]
    result_worlds=[]
    for n,p0,p1,name,family,regime,r in worlds():
        l=formula(family,n,p0,regime)
        right=formula(family,n,p1,regime)
        if l!=events(family,n,p0,regime) or right!=events(family,n,p1,regime):
            raise AssertionError("source formula and iterative event DP differ")
        mu0,var0=true_moments(l)
        mu1,var1=true_moments(right)
        if mu0!=n*p0 or mu1!=n*p1:
            raise AssertionError("original source rate not as specified")
        if var0!=theory(family,n,p0,regime) or var1!=theory(family,n,p1,regime):
            raise AssertionError("original source variance does not match R177 formula")
        joint=F(0)
        boundary=F(0)
        poisson_total_float=0.
        nb_total_float=0.
        poisson_total_dec=Decimal(0)
        nb_total_dec=Decimal(0)
        for k0,k1 in product(range(n+1),repeat=2):
            weight=l[k0]*right[k1]
            joint+=weight
            if k0==0 or k1==0:
                boundary+=weight
            lam0=F(k0)+F(1,2)
            lam1=F(k1)+F(1,2)
            pf0,pd0,nf0,nd0=conditional_scores(l,lam0,r)
            pf1,pd1,nf1,nd1=conditional_scores(right,lam1,r)
            ps=(pf0+pf1)/2
            ns=(nf0+nf1)/2
            pdecimal=(pd0+pd1)/2
            ndecimal=(nd0+nd1)/2
            poisson_total_float+=float(weight)*ps
            nb_total_float+=float(weight)*ns
            factor=Decimal(weight.numerator)/Decimal(weight.denominator)
            poisson_total_dec+=factor*pdecimal
            nb_total_dec+=factor*ndecimal
            all_rows.append({
                "source":name,"n":n,"true_p0":str(p0),"true_p1":str(p1),
                "NB_fixed_shape_r":r,
                "training_group0_K":k0,"training_group1_K":k1,
                "true_original_training_joint_mass":str(weight),
                "positive_predictive_mean_group0":str(lam0),
                "positive_predictive_mean_group1":str(lam1),
                "unadjusted_glm_boundary_indicator":int(k0==0 or k1==0),
                "independent_new_Poisson_expected_logloss_given_training":format(ps,".16g"),
                "independent_new_NB_expected_logloss_given_training":format(ns,".16g"),
            })
        if joint!=1 or boundary!=1-(1-l[0])*(1-right[0]):
            raise AssertionError("source pair space probabilities and boundary mismatch")
        if abs(poisson_total_float-float(poisson_total_dec))>1e-12:
            raise AssertionError("weighted Poisson numeric methods differ")
        if abs(nb_total_float-float(nb_total_dec))>1e-12:
            raise AssertionError("weighted NB numeric methods differ")
        result_worlds.append({
            "n_per_group":n,
            "true_p0":str(p0),"true_p1":str(p1),
            "source":name,"R177_family":family,"R177_regime":regime,
            "fixed_NB_shape_r":r,
            "true_source_expected_group0":str(mu0),"true_source_expected_group1":str(mu1),
            "true_source_variance_group0":str(var0),"true_source_variance_group1":str(var1),
            "true_zero_probability_group0":str(l[0]),"true_zero_probability_group1":str(right[0]),
            "moment_implied_NB_shape_group0":str(shape_moment(mu0,var0)) if shape_moment(mu0,var0) is not None else "NOT_POSITIVE_OVERDISPERSED",
            "moment_implied_NB_shape_group1":str(shape_moment(mu1,var1)) if shape_moment(mu1,var1) is not None else "NOT_POSITIVE_OVERDISPERSED",
            "NB_zero_probability_if_model_mean_set_true_group0":str(F(r,r+mu0)**r),
            "NB_zero_probability_if_model_mean_set_true_group1":str(F(r,r+mu1)**r),
            "probability_unregularized_nonfinite_loglink_MLE":str(boundary),
            "unregularized_NB_expected_independent_test_logloss":"INF",
            "fixed_positive_intensity_Poisson_expected_heldout_logloss":format(poisson_total_float,".16g"),
            "fixed_positive_intensity_NB_expected_heldout_logloss":format(nb_total_float,".16g"),
            "NB_minus_Poisson_positive_intensity_expected_loss":format(nb_total_float-poisson_total_float,".16g"),
            "all_exact_PMF_methods_and_numeric_scores_agreed":True,
            "training_pairs":(n+1)**2,
        })
    if len(result_worlds)!=135 or len(all_rows)!=12375:
        raise AssertionError("frozen 135 NB world or 12375 source pair count drifted")
    matching=[w for w in result_worlds
              if w["n_per_group"]==8 and w["true_p0"]=="1/4"
              and w["true_p1"]=="1/4" and w["fixed_NB_shape_r"]==6
              and w["source"] in ("CLUSTERED_BB_C8","INACTIVE_ZIB_Z1_4")]
    if len(matching)!=2:
        raise AssertionError("fixed moment match source pair missing")
    by={x["source"]:x for x in matching}
    bb=by["CLUSTERED_BB_C8"]
    zi=by["INACTIVE_ZIB_Z1_4"]
    if not (bb["true_source_expected_group0"]==zi["true_source_expected_group0"]=="2"
            and bb["true_source_variance_group0"]==zi["true_source_variance_group0"]=="8/3"
            and bb["moment_implied_NB_shape_group0"]==zi["moment_implied_NB_shape_group0"]=="6"
            and bb["true_zero_probability_group0"]=="1/5"
            and bb["true_zero_probability_group0"]!=zi["true_zero_probability_group0"]
            and F(bb["NB_zero_probability_if_model_mean_set_true_group0"])==F(3,4)**6):
        raise AssertionError("prespecified same-moments-different-zero alias failed")
    selected=[w for w in result_worlds if w["n_per_group"]==8 and w["true_p0"]=="1/4" and w["true_p1"]=="1/4"]
    if len(selected)!=15:
        raise AssertionError("missing fixed full fifteen-model comparison")
    with TRAIN.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(all_rows[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(all_rows)
    out={
        "research_id":"R185",
        "status":"E1_ARTIFICIAL_EXACT_NEGATIVE_BINOMIAL_PREDICTION",
        "source_code_git_blob_sha1":R177_BLOB,
        "source_result_sha256":R177_JSON_SHA,
        "NB_fixed_shapes":list(SHAPES),
        "worlds":135,"complete_original_training_pairs":12375,
        "full_NB_probability_closed_and_independent_recurrence_parity":True,
        "all_source_normalization_and_true_dispersion_analytic_parity":True,
        "all_independent_Poisson_and_NB_future_scores_numeric_parity":True,
        "all_unadjusted_NB_logloss_infinite_due_to_zero_training":True,
        "fixed_n8_equal_true_rates_15_worlds":selected,
        "same_moments_different_zero_source_alias":matching,
        "original_training_pairs_CSV_sha256":sha256(TRAIN.read_bytes()).hexdigest(),
        "full_results":result_worlds,
        "real_human_or_historical_evidence":False,
        "new_E2":0,"new_E3":0,
    }
    OUT.write_text(json.dumps(out,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    a={
        "research_id":"R185",
        "status":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_NEGATIVE_BINOMIAL",
        "worlds":135,"source_weighted_training_pairs":12375,
        "full_NB_PMF_independent_Fraction_identity":True,
        "same_moments_different_zero_PMF_counterexample":True,
        "source_R177_sha_verified":True,
        "all_fixed_shape_NB_and_Poisson_holdout_scores_two_numeric_routes":True,
        "exact_world_result_sha256":sha256(OUT.read_bytes()).hexdigest(),
        "source_pairs_CSV_sha256":out["original_training_pairs_CSV_sha256"],
        "real_human_or_history_tested":False,
        "new_E2":0,"new_E3":0,
    }
    ACCEPT.write_text(json.dumps(a,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R185_MACHINE_ACCEPTANCE",json.dumps(a,sort_keys=True))
    print("R185_LOCKED_MOMENT_ALIAS",json.dumps(matching,sort_keys=True))
    return out


def archive():
    names=[Path(__file__).name,OUT.name,TRAIN.name,ACCEPT.name]
    with zipfile.ZipFile(ARCH,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in names:
            info=zipfile.ZipInfo(name,date_time=(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,(HERE/name).read_bytes())
        info=zipfile.ZipInfo(PROTO.name,date_time=(2026,10,21,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,PROTO.read_bytes())
    print("R185_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestNegativeBinomial(unittest.TestCase):
    def test_all_world_count(self):
        self.assertEqual(len(list(worlds())),135)
    def test_all_training_pairs(self):
        self.assertEqual(sum((n+1)**2 for n,a,b,x,f,reg,r in worlds()),12375)
    def test_three_prespecified_shapes(self):
        self.assertEqual(SHAPES,(2,6,8))
    def test_source_SHA(self):
        a,b,theory=source()
        self.assertEqual(a("BB",4,F(1,4),0),b("BB",4,F(1,4),0))
    def test_all_source_PMF_dual(self):
        a,b,theory=source()
        for n,p0,p1,name,f,reg,r in worlds():
            for p in (p0,p1):
                self.assertEqual(a(f,n,p,reg),b(f,n,p,reg))
    def test_NB_P0_closed(self):
        self.assertEqual(nb_closed_pmf(0,F(2),6),F(3,4)**6)
    def test_NB_recursion_closed_exact_all(self):
        for n in N_VALUES:
            for lam in (F(1,2),F(3,2),F(5,2),F(7,2)):
                for r in SHAPES:
                    seq=nb_recurrence_probabilities(lam,r,n)
                    self.assertEqual(seq,tuple(nb_closed_pmf(y,lam,r) for y in range(n+1)))
    def test_NB_support_is_not_truncated_and_renormalized(self):
        seq=nb_recurrence_probabilities(F(2),6,8)
        self.assertLess(sum(seq,F(0)),1)
    def test_NB_shapes_under_current_source(self):
        a,b,theory=source()
        for n,p0,p1,name,f,reg,r in worlds():
            for p in (p0,p1):
                mu,var=true_moments(a(f,n,p,reg))
                self.assertEqual(var,theory(f,n,p,reg))
    def test_strong_BB_source_positive_excess_dispersion(self):
        a,b,theory=source()
        mu,var=true_moments(a("BB",8,F(1,4),0))
        self.assertGreater(var,mu)
    def test_IID_binomial_is_not_overdispersed(self):
        a,b,theory=source()
        mu,var=true_moments(a("BIN",8,F(1,4),0))
        self.assertIsNone(shape_moment(mu,var))
    def test_alias_mean_two(self):
        a,b,theory=source()
        for name,f,reg in (SOURCE_MECHANISMS[2],SOURCE_MECHANISMS[4]):
            mu,var=true_moments(a(f,8,F(1,4),reg))
            self.assertEqual(mu,2)
    def test_alias_variance_eight_thirds(self):
        a,b,theory=source()
        for name,f,reg in (SOURCE_MECHANISMS[2],SOURCE_MECHANISMS[4]):
            mu,var=true_moments(a(f,8,F(1,4),reg))
            self.assertEqual(var,F(8,3))
    def test_alias_implied_shape_six(self):
        a,b,theory=source()
        for name,f,reg in (SOURCE_MECHANISMS[2],SOURCE_MECHANISMS[4]):
            mu,var=true_moments(a(f,8,F(1,4),reg))
            self.assertEqual(shape_moment(mu,var),6)
    def test_alias_zero_probability_distinct(self):
        a,b,theory=source()
        q0=a("BB",8,F(1,4),2)[0]
        q1=a("ZIB",8,F(1,4),1)[0]
        self.assertEqual(q0,F(1,5))
        self.assertNotEqual(q0,q1)
    def test_matching_NB_P0_different_from_both_sources(self):
        a,b,theory=source()
        p0=nb_closed_pmf(0,F(2),6)
        self.assertNotEqual(p0,a("BB",8,F(1,4),2)[0])
        self.assertNotEqual(p0,a("ZIB",8,F(1,4),1)[0])
    def test_all_source_PMF_normalized(self):
        a,b,theory=source()
        for n,p0,p1,name,f,reg,r in worlds():
            self.assertEqual(sum(a(f,n,p0,reg),F(0)),1)
    def test_all_numeric_future_scores_agree(self):
        a,b,theory=source()
        for n,p0,p1,name,f,reg,r in worlds():
            for p in (p0,p1):
                law=a(f,n,p,reg)
                for k in (0,1,n):
                    vals=conditional_scores(law,F(k)+F(1,2),r)
                    self.assertAlmostEqual(vals[0],float(vals[1]),places=12)
                    self.assertAlmostEqual(vals[2],float(vals[3]),places=12)
    def test_NB_future_score_finite(self):
        a,b,theory=source()
        pmf=a("BB",8,F(1,4),0)
        self.assertGreater(nb_future_float(pmf,F(1,2),6),0)
    def test_Poisson_future_score_finite(self):
        a,b,theory=source()
        pmf=a("BIN",8,F(1,4),0)
        self.assertGreater(poisson_future_float(pmf,F(1,2)),0)
    def test_zero_training_positive_future_probability(self):
        a,b,theory=source()
        for n,p0,p1,name,f,reg,r in worlds():
            pmf=a(f,n,p0,reg)
            self.assertTrue(pmf[0]>0 and sum(pmf[1:],F(0))>0)
    def test_invalid_negative_lambda_fails(self):
        with self.assertRaises(ValueError):
            nb_closed_pmf(0,F(-1),6)
    def test_invalid_zero_lambda_fails_for_smoothed_model(self):
        with self.assertRaises(ValueError):
            nb_closed_pmf(0,F(0),6)
    def test_invalid_noninteger_shape_fails(self):
        with self.assertRaises(ValueError):
            nb_closed_pmf(2,F(1),F(3,2))
    def test_invalid_negative_count_fails(self):
        with self.assertRaises(ValueError):
            nb_closed_pmf(-1,F(1),6)
    def test_source_shape_fixed_not_chosen_from_test_scores(self):
        self.assertEqual(len(SHAPES),3)
    def test_true_rational_moments_hand(self):
        self.assertEqual(true_moments((F(3,4),F(1,4))),(F(1,4),F(3,16)))


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("Use --test or --run-and-archive")
