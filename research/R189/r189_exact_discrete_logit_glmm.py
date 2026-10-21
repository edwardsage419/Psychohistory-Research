"""R189 exact two-point random-intercept binomial/logit GLMM.

Four independent groups per source world (two per x); conditionally
independent trials within each group, with an unobserved common symmetric
two-point log-odds multiplier. Train with exact count marginal likelihood,
predict independent NEW clusters with the random effect integrated out.
No Gaussian GLMM estimation, no historical or human data.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import product, combinations_with_replacement
from math import comb, factorial, log
from pathlib import Path
import csv, json, sys, unittest, zipfile

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE.parent.parent / "protocols/R189_DISCRETE_GLMM_24_WORLDS_8472_TABLES_PRESCORE_FREEZE_2026-10-21.md"
OUT = HERE / "R189_EXACT_RESULTS.json"
SAMPLES = HERE / "R189_ALL_8472_ORDERED_CLUSTER_TRAINING_TABLES.csv"
PROFILES = HERE / "R189_ALL_261_CLUSTER_FIT_PROFILES.json"
ACCEPT = HERE / "R189_FINAL_MACHINE_ACCEPTANCE.json"
ARCH = HERE / "R189_Exact_Two_Point_GLMM_24_Worlds.zip"

N_VALUES = (2, 4)
SOURCE_O = (F(1,3), F(1))
O_GRID = (F(1,9), F(1,3), F(1), F(3))
T_GRID = (F(1,3), F(1), F(3))
SOURCE_H = (1, 3)
H_GRID = (1, 3, 9)
GROUPS_PER_X = 2


def worlds():
    for n,o,t,h in product(N_VALUES,SOURCE_O,T_GRID,SOURCE_H):
        yield n,o,t,h


def validate(n, o, t, h):
    if n not in N_VALUES or o not in O_GRID or t not in T_GRID or h not in H_GRID:
        raise ValueError("parameters outside prescored finite GLMM grid")


def bernoulli_probability(odds):
    if odds <= 0:
        raise ValueError("nonpositive conditional odds")
    return odds / (1 + odds)


def latent_rates(o,t,h,x):
    if x not in (0,1):
        raise ValueError("condition group outside {0,1}")
    odds = o * (t if x else F(1))
    return bernoulli_probability(odds * h), bernoulli_probability(odds / h)


def source_pmf_closed(n,o,t,h,x):
    """Method A: closed Binomial mixture over both symmetric latent points."""
    validate(n,o,t,h)
    high,low=latent_rates(o,t,h,x)
    return tuple(
        F(comb(n,k),2) * (high**k * (1-high)**(n-k)
                        +low**k * (1-low)**(n-k))
        for k in range(n+1)
    )


def bernoulli_count_dp(n,p):
    """Sequential dynamic program, no binomial combinatorial coefficients."""
    state={0:F(1)}
    for _ in range(n):
        nxt=defaultdict(F)
        for k,mass in state.items():
            nxt[k]+=mass*(1-p)
            nxt[k+1]+=mass*p
        state=nxt
    return tuple(state.get(k,F(0)) for k in range(n+1))


def source_pmf_events(n,o,t,h,x):
    """Method B: two independent latent-specific primitive event DPs."""
    validate(n,o,t,h)
    hi,lo=latent_rates(o,t,h,x)
    a,b=bernoulli_count_dp(n,hi),bernoulli_count_dp(n,lo)
    return tuple((u+v)/2 for u,v in zip(a,b))


@lru_cache(maxsize=None)
def two_condition_pmfs(n,o,t,h):
    f0=source_pmf_closed(n,o,t,h,0)
    f1=source_pmf_closed(n,o,t,h,1)
    if (f0!=source_pmf_events(n,o,t,h,0) or
        f1!=source_pmf_events(n,o,t,h,1) or
        sum(f0,F(0))!=1 or sum(f1,F(0))!=1 or
        any(v<=0 for v in f0+f1)):
        raise AssertionError("two-point exact count PMF construction failed")
    return f0,f1


def source_moments(n,o,t,h,x):
    p_hi,p_lo=latent_rates(o,t,h,x)
    marginal=(p_hi+p_lo)/2
    cov=(p_hi-p_lo)**2 / 4
    count_pmf=two_condition_pmfs(n,o,t,h)[x]
    from_count=sum((k*pr for k,pr in enumerate(count_pmf)),F(0))
    var_count=sum(((F(k)-from_count)**2*pr for k,pr in enumerate(count_pmf)),F(0))
    theoretical=n*marginal*(1-marginal)+n*(n-1)*cov
    if from_count!=n*marginal or var_count!=theoretical:
        raise AssertionError("independent primitive moments vs count PMF differ")
    return marginal,cov,var_count


@lru_cache(maxsize=None)
def candidate_grid():
    candidates=[]
    for o,t,h in product(O_GRID,T_GRID,H_GRID):
        f0,f1=two_condition_pmfs(N_VALUES[0],o,t,h)
        candidates.append((o,t,h))
    pooled=tuple(v for v in candidates if v[2]==1)
    if len(candidates)!=36 or len(pooled)!=12:
        raise AssertionError("original finite grid not as registered")
    return tuple(candidates),pooled


def raw_likelihood(counts,pmfs):
    k00,k01,k10,k11=counts
    return pmfs[0][k00]*pmfs[0][k01]*pmfs[1][k10]*pmfs[1][k11]


def histogram_likelihood(counts,pmfs):
    value=F(1)
    for observations,pmf in ((counts[:2],pmfs[0]),(counts[2:],pmfs[1])):
        for k,count in Counter(observations).items():
            value*=pmf[k]**count
    return value


def fit_training_profile(n,profile):
    if n not in N_VALUES or len(profile)!=4 or tuple(profile[:2])!=tuple(sorted(profile[:2])) or tuple(profile[2:])!=tuple(sorted(profile[2:])) or any(k not in range(n+1) for k in profile):
        raise ValueError("invalid unordered-within-condition count profile")
    candidates,pooled=candidate_grid()
    best_glmm=None
    best_pooled=None
    for o,t,h in candidates:
        pmfs=two_condition_pmfs(n,o,t,h)
        like=raw_likelihood(profile,pmfs)
        if like!=histogram_likelihood(profile,pmfs):
            raise AssertionError("ordered vs histogram cluster likelihood differs")
        if best_glmm is None or like>best_glmm[0]:
            best_glmm=(like,o,t,h,pmfs)
        if h==1 and (best_pooled is None or like>best_pooled[0]):
            best_pooled=(like,o,t,h,pmfs)
    if best_glmm is None or best_pooled is None or best_glmm[0]<best_pooled[0]:
        raise AssertionError("hierarchical mixture grid does not nest fixed effect grid")
    return {
        "n":n,"profile":profile,
        "GLMM_selected_parameters":best_glmm[1:4],
        "POOLED_selected_parameters":best_pooled[1:4],
        "GLMM_exact_training_likelihood":best_glmm[0],
        "POOLED_exact_training_likelihood":best_pooled[0],
        "GLMM_heldout_cluster_count_PMFS":best_glmm[4],
        "POOLED_heldout_cluster_count_PMFS":best_pooled[4],
        "independent_likelihood_and_count_PMF_algorithms_agree":True,
    }


@lru_cache(maxsize=None)
def fit_library():
    lib={}
    for n in N_VALUES:
        pairs=tuple(combinations_with_replacement(range(n+1),GROUPS_PER_X))
        for left,right in product(pairs,repeat=2):
            profile=left+right
            lib[(n,profile)]=fit_training_profile(n,profile)
    if len(lib)!=261:
        raise AssertionError("unique within-condition sorted profile count not 261")
    return lib


def profile_for_ordered(k):
    return tuple(sorted(k[:2])+sorted(k[2:]))


@lru_cache(maxsize=None)
def test_loss_double(source_pair,predicted_pair):
    """Average independent heldout NEW cluster expected logloss, two methods."""
    math_val=-sum(float(p)*log(float(q)) for true,pred in zip(source_pair,predicted_pair)
                  for p,q in zip(true,pred))/2
    with localcontext() as ctx:
        ctx.prec=60
        decimal_val=-sum(
            (Decimal(p.numerator)/Decimal(p.denominator))*
            (Decimal(q.numerator)/Decimal(q.denominator)).ln()/2
            for true,pred in zip(source_pair,predicted_pair)
            for p,q in zip(true,pred)
        )
    if abs(math_val-float(decimal_val))>1e-12:
        raise AssertionError("two independent heldout whole-group scores disagree")
    return math_val,decimal_val


def fit_for_csv(fit):
    return {
        "pooled_o_t_h":",".join(map(str,fit["POOLED_selected_parameters"])),
        "glmm_o_t_h":",".join(map(str,fit["GLMM_selected_parameters"])),
        "pooled_exact_likelihood":str(fit["POOLED_exact_training_likelihood"]),
        "glmm_exact_likelihood":str(fit["GLMM_exact_training_likelihood"]),
    }


def run_world(n,o,t,h,fits,sample_rows):
    true=two_condition_pmfs(n,o,t,h)
    moments0=source_moments(n,o,t,h,0)
    moments1=source_moments(n,o,t,h,1)
    true_marginal_or=(
        moments1[0]/(1-moments1[0])
        / (moments0[0]/(1-moments0[0]))
    )
    total=F(0)
    selected_h_gt1=F(0)
    strict_gain=F(0)
    pooled_risk=0.0
    glmm_risk=0.0
    pooled_dec=Decimal(0)
    glmm_dec=Decimal(0)
    sample_count=0
    for observed in product(range(n+1),repeat=4):
        weight=raw_likelihood(observed,true)
        fit=fits[(n,profile_for_ordered(observed))]
        lp,dp=test_loss_double(true,fit["POOLED_heldout_cluster_count_PMFS"])
        lg,dg=test_loss_double(true,fit["GLMM_heldout_cluster_count_PMFS"])
        total+=weight
        selected_h_gt1+=weight*int(fit["GLMM_selected_parameters"][2]>1)
        strict_gain+=weight*int(fit["GLMM_exact_training_likelihood"]>fit["POOLED_exact_training_likelihood"])
        pooled_risk+=float(weight)*lp
        glmm_risk+=float(weight)*lg
        wdec=Decimal(weight.numerator)/Decimal(weight.denominator)
        pooled_dec+=wdec*dp
        glmm_dec+=wdec*dg
        sample_count+=1
        sample_rows.append({
            "n_per_cluster":n,"source_base_odds_o":str(o),
            "source_conditional_odds_multiplier_t":str(t),
            "source_random_intercept_multiplier_h":h,
            "ordered_cluster_counts":",".join(map(str,observed)),
            "source_exact_four_cluster_joint_probability":str(weight),
            "sorted_within_condition_fit_profile":",".join(map(str,profile_for_ordered(observed))),
            **fit_for_csv(fit),
            "heldout_NEW_cluster_pooled_expected_logloss":format(lp,".16g"),
            "heldout_NEW_cluster_discrete_GLMM_expected_logloss":format(lg,".16g"),
        })
    if total!=1 or sample_count!=(n+1)**4:
        raise AssertionError("source joint cluster probability not normalized")
    if abs(pooled_risk-float(pooled_dec))>1e-12 or abs(glmm_risk-float(glmm_dec))>1e-12:
        raise AssertionError("world-weighted independent test logloss methods disagree")
    return {
        "n_per_cluster":n,
        "source_base_odds_o":str(o),
        "source_conditional_odds_multiplier_t":str(t),
        "source_latent_odds_multiplier_h":h,
        "full_ordered_training_four_cluster_tables":sample_count,
        "true_cluster0_count_PMF":[str(v) for v in true[0]],
        "true_cluster1_count_PMF":[str(v) for v in true[1]],
        "true_single_event_marginal_p0":str(moments0[0]),
        "true_single_event_marginal_p1":str(moments1[0]),
        "true_same_cluster_event_cov_x0":str(moments0[1]),
        "true_same_cluster_event_cov_x1":str(moments1[1]),
        "true_count_variance_x0":str(moments0[2]),
        "true_count_variance_x1":str(moments1[2]),
        "true_conditional_odds_ratio":str(t),
        "true_marginal_odds_ratio":str(true_marginal_or),
        "probability_GLMM_selected_h_above_one":str(selected_h_gt1),
        "probability_GLMM_training_likelihood_strict_gain":str(strict_gain),
        "pooled_model_independent_NEW_cluster_expected_logloss":format(pooled_risk,".16g"),
        "two_point_GLMM_independent_NEW_cluster_expected_logloss":format(glmm_risk,".16g"),
        "GLMM_minus_pooled_independent_NEW_cluster_loss":format(glmm_risk-pooled_risk,".16g"),
        "independent_source_fraction_moments_and_heldout_log_scores_verified":True
    }


def serialize_fits(library):
    rows=[]
    for (n,k),fit in sorted(library.items()):
        rows.append({
            "n_per_cluster":n,"sorted_within_x_cluster_count_profile":list(k),
            "pooled_o_t_h":[str(v) for v in fit["POOLED_selected_parameters"]],
            "glmm_o_t_h":[str(v) for v in fit["GLMM_selected_parameters"]],
            "pooled_exact_training_likelihood":str(fit["POOLED_exact_training_likelihood"]),
            "glmm_exact_training_likelihood":str(fit["GLMM_exact_training_likelihood"]),
            "pooled_predicted_NEW_cluster_PMFS":[[str(v) for v in pmf] for pmf in fit["POOLED_heldout_cluster_count_PMFS"]],
            "glmm_predicted_NEW_cluster_PMFS":[[str(v) for v in pmf] for pmf in fit["GLMM_heldout_cluster_count_PMFS"]],
            "two_probability_and_likelihood_routes_verified":True
        })
    return rows


def run():
    fits=fit_library()
    sample_rows=[]
    worlds_output=[run_world(n,o,t,h,fits,sample_rows) for n,o,t,h in worlds()]
    if len(worlds_output)!=24 or len(sample_rows)!=8472:
        raise AssertionError("frozen 24-world 8472-training-table universe changed")
    anchors=[w for w in worlds_output if w["source_base_odds_o"]=="1/3"
             and w["source_conditional_odds_multiplier_t"]=="3"
             and w["source_latent_odds_multiplier_h"]==3]
    if len(anchors)!=2 or any(not (
        x["true_single_event_marginal_p0"]=="3/10" and
        x["true_single_event_marginal_p1"]=="1/2" and
        x["true_conditional_odds_ratio"]=="3" and
        x["true_marginal_odds_ratio"]=="7/3" and
        x["true_same_cluster_event_cov_x0"]=="1/25"
    ) for x in anchors):
        raise AssertionError("frozen cluster-specific vs marginal logit example invalid")
    n2=next(x for x in anchors if x["n_per_cluster"]==2)
    if n2["true_cluster0_count_PMF"][2]!="13/100":
        raise AssertionError("true correlated two-event group count differs from fixed 13/100")
    with SAMPLES.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(sample_rows[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(sample_rows)
    entries=serialize_fits(fits)
    PROFILES.write_text(json.dumps({
        "research_id":"R189","unique_training_profiles":len(entries),
        "candidate_pooled":12,"candidate_two_point_glmm":36,
        "all_candidate_count_PMF_and_likelihood_implementations_verified":True,
        "profiles":entries
    },sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    report={
        "research_id":"R189",
        "stage":"E1_ARTIFICIAL_EXACT_DISCRETE_LOGISTIC_RANDOM_INTERCEPT",
        "world_count":24,"complete_ordered_training_tables":8472,
        "unique_exact_profile_fits":261,
        "four_independent_clusters_two_per_condition":True,
        "two_point_random_intercept_integrated_before_test_scoring":True,
        "all_exact_closed_binomial_mixture_and_event_count_DP_equal":True,
        "all_independent_likelihood_raw_and_histogram_equal":True,
        "all_population_v_cluster_odds_and_covariance_verified":True,
        "all_heldout_new_cluster_math_and_decimal_score_equal":True,
        "prelocked_marginal_vs_conditional_odds_ratio_anchor":anchors,
        "all_worlds":worlds_output,
        "full_original_table_CSV_sha256":sha256(SAMPLES.read_bytes()).hexdigest(),
        "full_fitted_profile_library_sha256":sha256(PROFILES.read_bytes()).hexdigest(),
        "real_human_or_historical_data":False,"new_E2":0,"new_E3":0,
    }
    OUT.write_text(json.dumps(report,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    accept={
        "research_id":"R189","status":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_DISCRETE_GLMM",
        "world_count":24,"ordered_cluster_training_tables":8472,
        "unique_model_fit_profiles":261,
        "both_exact_discrete_random_intercept_probability_routes_equal":True,
        "raw_cluster_and_histogram_likelihood_routes_equal":True,
        "cluster_specific_vs_population_marginal_odds_difference_proven":True,
        "heldout_independent_NEW_cluster_prediction_loss_double_checked":True,
        "result_sha256":sha256(OUT.read_bytes()).hexdigest(),
        "complete_training_CSV_sha256":report["full_original_table_CSV_sha256"],
        "fit_profile_library_sha256":report["full_fitted_profile_library_sha256"],
        "real_human_or_historical_data":False,"new_E2":0,"new_E3":0,
    }
    ACCEPT.write_text(json.dumps(accept,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R189_MACHINE_ACCEPTANCE",json.dumps(accept,sort_keys=True))
    print("R189_ODDS_RATIO_ANCHORS",json.dumps(anchors,sort_keys=True))
    return report


def archive():
    names=[Path(__file__).name,OUT.name,SAMPLES.name,PROFILES.name,ACCEPT.name]
    with zipfile.ZipFile(ARCH,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in names:
            info=zipfile.ZipInfo(name,date_time=(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,(HERE/name).read_bytes())
        info=zipfile.ZipInfo(PROTOCOL.name,date_time=(2026,10,21,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,PROTOCOL.read_bytes())
    print("R189_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestDiscreteGLMM(unittest.TestCase):
    def test_24_worlds(self):
        self.assertEqual(len(list(worlds())),24)
    def test_8472_ordered_training_tables(self):
        self.assertEqual(sum((n+1)**4 for n,o,t,h in worlds()),8472)
    def test_261_unordered_condition_profiles(self):
        self.assertEqual(len(fit_library()),261)
    def test_pooled_12_candidates(self):
        self.assertEqual(len(candidate_grid()[1]),12)
    def test_glmm_36_candidates(self):
        self.assertEqual(len(candidate_grid()[0]),36)
    def test_all_pooled_nested(self):
        self.assertTrue(all(x in candidate_grid()[0] for x in candidate_grid()[1]))
    def test_true_two_point_closed_vs_event_dp(self):
        for n,o,t,h in worlds():
            for x in (0,1):
                self.assertEqual(source_pmf_closed(n,o,t,h,x),source_pmf_events(n,o,t,h,x))
    def test_all_candidate_two_algorithms(self):
        for n in N_VALUES:
            for o,t,h in candidate_grid()[0]:
                self.assertEqual(source_pmf_closed(n,o,t,h,0),source_pmf_events(n,o,t,h,0))
                self.assertEqual(source_pmf_closed(n,o,t,h,1),source_pmf_events(n,o,t,h,1))
    def test_all_source_mass_one(self):
        for n,o,t,h in worlds():
            p0,p1=two_condition_pmfs(n,o,t,h)
            self.assertEqual(sum(p0,F(0)),1)
            self.assertEqual(sum(p1,F(0)),1)
            self.assertEqual(sum((p0[a]*p0[b]*p1[c]*p1[d]
                for a,b,c,d in product(range(n+1),repeat=4)),F(0)),1)
    def test_exact_group_count_moments(self):
        for n,o,t,h in worlds():
            for x in (0,1):
                source_moments(n,o,t,h,x)
    def test_no_random_effect_no_covariance(self):
        for n,o,t,h in worlds():
            if h==1:
                self.assertEqual(source_moments(n,o,t,h,0)[1],0)
                self.assertEqual(source_moments(n,o,t,h,1)[1],0)
    def test_positive_covariance_all_random_effect(self):
        for n,o,t,h in worlds():
            if h==3:
                self.assertGreater(source_moments(n,o,t,h,0)[1],0)
                self.assertGreater(source_moments(n,o,t,h,1)[1],0)
    def test_conditional_vs_marginal_ratio(self):
        p0,_,_=source_moments(2,F(1,3),F(3),3,0)
        p1,_,_=source_moments(2,F(1,3),F(3),3,1)
        self.assertEqual((p0,p1),(F(3,10),F(1,2)))
        self.assertEqual((p1/(1-p1))/(p0/(1-p0)),F(7,3))
    def test_no_random_effect_ratio_same(self):
        p0,_,_=source_moments(2,F(1,3),F(3),1,0)
        p1,_,_=source_moments(2,F(1,3),F(3),1,1)
        self.assertEqual((p1/(1-p1))/(p0/(1-p0)),3)
    def test_exact_cluster_covariance_anchor(self):
        self.assertEqual(source_moments(2,F(1,3),F(3),3,0)[1],F(1,25))
    def test_count_K2_anchor(self):
        self.assertEqual(two_condition_pmfs(2,F(1,3),F(3),3)[0][2],F(13,100))
    def test_iid_K2_incorrect_n2(self):
        self.assertEqual(F(3,10)**2,F(9,100))
    def test_likelihood_direct_histogram(self):
        n=2
        for profile in product(range(n+1),repeat=4):
            pmfs=two_condition_pmfs(n,F(1,3),F(3),3)
            self.assertEqual(raw_likelihood(profile,pmfs),histogram_likelihood(profile,pmfs))
    def test_nested_training_likelihood_all_profiles(self):
        for fit in fit_library().values():
            self.assertGreaterEqual(fit["GLMM_exact_training_likelihood"],fit["POOLED_exact_training_likelihood"])
    def test_all_model_predictions_strictly_positive(self):
        for fit in fit_library().values():
            for model in ("GLMM_heldout_cluster_count_PMFS","POOLED_heldout_cluster_count_PMFS"):
                for pmf in fit[model]:
                    self.assertEqual(sum(pmf,F(0)),1)
                    self.assertTrue(all(v>0 for v in pmf))
    def test_test_loss_double_math_decimal(self):
        for n,o,t,h in worlds():
            source=two_condition_pmfs(n,o,t,h)
            for profile in fit_library():
                if profile[0]!=n:continue
                for model in ("GLMM_heldout_cluster_count_PMFS","POOLED_heldout_cluster_count_PMFS"):
                    test_loss_double(source,fit_library()[profile][model])
    def test_profile_invariance_to_cluster_order(self):
        self.assertEqual(profile_for_ordered((1,0,2,0)),profile_for_ordered((0,1,0,2)))
    def test_invalid_n(self):
        with self.assertRaises(ValueError):
            source_pmf_closed(3,F(1,3),F(1),1,0)
    def test_invalid_odds(self):
        with self.assertRaises(ValueError):
            source_pmf_closed(2,F(1,7),F(1),1,0)
    def test_invalid_t(self):
        with self.assertRaises(ValueError):
            source_pmf_events(2,F(1,3),F(1,2),1,1)
    def test_invalid_h(self):
        with self.assertRaises(ValueError):
            source_pmf_events(2,F(1,3),F(1),4,0)
    def test_invalid_condition(self):
        with self.assertRaises(ValueError):
            source_pmf_events(2,F(1,3),F(1),1,2)
    def test_invalid_profile_fail_closed(self):
        with self.assertRaises(ValueError):
            fit_training_profile(2,(2,0,0,0))
    def test_invalid_zero_odds(self):
        with self.assertRaises(ValueError):
            bernoulli_probability(F(0))
    def test_new_cluster_marginal_zero_latent_correction(self):
        p=two_condition_pmfs(2,F(1,3),F(3),3)[0]
        self.assertEqual(p[2],F(13,100))


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("Use --test or --run-and-archive")
