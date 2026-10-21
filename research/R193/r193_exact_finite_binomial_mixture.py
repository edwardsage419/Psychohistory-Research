"""R193: exact finite binomial-mixture identifiability and prediction.

Artificial 24 worlds, 512 complete independent-cluster training tables and
53 count-profile fits. Four frozen candidate laws: IID, symmetric S, skewed
A, wide W. S and A match E(Q), E(Q^2), and every n<=2 count PMF but have
distinct third moments and oracle latent class posterior interpretations.
No real human data, general continuous mixture MLE, or historical test.
"""
from __future__ import annotations

from collections import Counter,defaultdict
from decimal import Decimal,localcontext
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import product,combinations_with_replacement
from math import comb,log
from pathlib import Path
import csv,json,sys,unittest,zipfile

HERE=Path(__file__).resolve().parent
PROTO=HERE.parent.parent/"protocols/R193_FINITE_MIXTURE_24_WORLDS_512_TABLES_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R193_EXACT_RESULTS.json"
SAMPLES=HERE/"R193_ALL_512_ORDERED_TRAINING_TABLES.csv"
FITS=HERE/"R193_ALL_53_EXACT_MIXTURE_FITS.json"
ACCEPT=HERE/"R193_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R193_Exact_Finite_Mixtures_24_Worlds.zip"
MODELS=("IID","S","A","W")
N_VALUES=(1,2,3)
M_VALUES=(2,3)
COMPONENTS={
    "IID":((F(1,2),F(1,2)),(F(1,2),F(1,2))),
    "S":((F(1,2),F(1,4)),(F(1,2),F(3,4))),
    "A":((F(9,13),F(1,3)),(F(4,13),F(7,8))),
    "W":((F(1,2),F(1,8)),(F(1,2),F(7,8))),
}


def worlds():
    for source,n,m in product(MODELS,N_VALUES,M_VALUES):
        yield source,n,m


def validate(source,n):
    if source not in MODELS or n not in N_VALUES:
        raise ValueError("outside registered exact finite mixture")


def component_binomial_closed(n,k,p):
    return F(comb(n,k))*p**k*(1-p)**(n-k)


def component_binomial_dp(n,p):
    """Count-state recursion independent of binomial coefficient."""
    state={0:F(1)}
    for _ in range(n):
        nxt=defaultdict(F)
        for k,mass in state.items():
            nxt[k]+=mass*(1-p)
            nxt[k+1]+=mass*p
        state=nxt
    return tuple(state.get(k,F(0)) for k in range(n+1))


def pmf_closed(source,n):
    validate(source,n)
    return tuple(sum((w*component_binomial_closed(n,k,p)
                      for w,p in COMPONENTS[source]),F(0))
                 for k in range(n+1))


def pmf_dp(source,n):
    validate(source,n)
    pieces=tuple((w,component_binomial_dp(n,p)) for w,p in COMPONENTS[source])
    return tuple(sum((w*pmf[k] for w,pmf in pieces),F(0)) for k in range(n+1))


@lru_cache(maxsize=None)
def distribution(source,n):
    a=pmf_closed(source,n)
    b=pmf_dp(source,n)
    if a!=b or sum(a,F(0))!=1 or any(v<=0 for v in a):
        raise AssertionError("two independent source mixture algorithms diverge")
    return a


def latent_moment(source,r):
    if source not in MODELS or r not in (0,1,2,3):
        raise ValueError("bad moment")
    return sum((w*p**r for w,p in COMPONENTS[source]),F(0))


def count_factorial_moment(source,n,r):
    validate(source,n)
    if r>n or r<0:
        raise ValueError("cannot identify moment above number of trials")
    raw=F(0)
    for k,prob in enumerate(distribution(source,n)):
        descend=1
        for j in range(r):
            descend*=k-j
        raw+=prob*descend
    denom=1
    for j in range(r):
        denom*=n-j
    return raw/denom


def conditional_high_posterior(source,n,k):
    validate(source,n)
    if not 0<=k<=n:
        raise ValueError("observed count outside support")
    high_w,high_q=COMPONENTS[source][1]
    return high_w*component_binomial_closed(n,k,high_q)/distribution(source,n)[k]


def joint_latent_count(source,n,C,k):
    validate(source,n)
    if C not in (0,1) or not 0<=k<=n:
        raise ValueError("latent label or count out of range")
    weight,p=COMPONENTS[source][C]
    return weight*component_binomial_closed(n,k,p)


def label_swap_pmf(source,n):
    validate(source,n)
    components=tuple(reversed(COMPONENTS[source]))
    return tuple(sum((w*component_binomial_closed(n,k,p) for w,p in components),F(0))
                 for k in range(n+1))


def likelihood_ordered(data,pmf):
    v=F(1)
    for k in data:
        v*=pmf[k]
    return v


def likelihood_counter(data,pmf):
    v=F(1)
    for k,count in Counter(data).items():
        v*=pmf[k]**count
    return v


def fit_profile(n,profile):
    if (n not in N_VALUES or len(profile) not in M_VALUES
            or tuple(profile)!=tuple(sorted(profile))
            or any(k not in range(n+1) for k in profile)):
        raise ValueError("invalid registered fit sample")
    likes={}
    for name in MODELS:
        pmf=distribution(name,n)
        left=likelihood_ordered(profile,pmf)
        right=likelihood_counter(profile,pmf)
        if left!=right:
            raise AssertionError("two exact likelihood algorithms differ")
        likes[name]=left
    best=max(likes.values())
    selected=next(name for name in MODELS if likes[name]==best)
    return {
        "n":n,"m":len(profile),"sorted_profile":profile,
        "all_candidate_fraction_likelihoods":likes,
        "selected_candidate":selected,
        "selected_count_PMF":distribution(selected,n),
        "all_probability_and_likelihood_implementations_agree":True,
    }


@lru_cache(maxsize=None)
def fit_library():
    out={}
    for n,m in product(N_VALUES,M_VALUES):
        for profile in combinations_with_replacement(range(n+1),m):
            out[(n,profile)]=fit_profile(n,profile)
    if len(out)!=53:
        raise AssertionError("53 candidate profiles missing")
    return out


@lru_cache(maxsize=None)
def heldout_scores(source,selected,n):
    """Independent NEW group; latent source first sampled from scratch."""
    truth=distribution(source,n)
    estimate=distribution(selected,n)
    score=-sum(float(p)*log(float(q)) for p,q in zip(truth,estimate))
    with localcontext() as ctx:
        ctx.prec=60
        high=-sum((Decimal(p.numerator)/Decimal(p.denominator))*
                  (Decimal(q.numerator)/Decimal(q.denominator)).ln()
                  for p,q in zip(truth,estimate))
    if abs(score-float(high))>1e-12:
        raise AssertionError("independent float vs Decimal logloss differs")
    artificial_label_brier=F(0)
    oracle_brier=F(0)
    for k in range(n+1):
        q=conditional_high_posterior(selected,n,k)
        t=conditional_high_posterior(source,n,k)
        artificial_label_brier+=joint_latent_count(source,n,0,k)*q*q
        artificial_label_brier+=joint_latent_count(source,n,1,k)*(1-q)**2
        oracle_brier+=truth[k]*t*(1-t)
    if artificial_label_brier<oracle_brier:
        raise AssertionError("fitted assignment beats true-source oracle")
    return score,high,artificial_label_brier,oracle_brier


def evaluate_world(source,n,m,all_samples):
    truth=distribution(source,n)
    allmass=F(0)
    selected_mass={c:F(0) for c in MODELS}
    expected_logloss=0.0
    expected_logloss_high=Decimal(0)
    expected_brier=F(0)
    oracle_brier=None
    count=0
    for observed in product(range(n+1),repeat=m):
        weight=likelihood_ordered(observed,truth)
        profile=tuple(sorted(observed))
        fit=fit_library()[(n,profile)]
        selected=fit["selected_candidate"]
        scalar,decimal,oracle_label,best_label=heldout_scores(source,selected,n)
        allmass+=weight
        selected_mass[selected]+=weight
        expected_logloss+=float(weight)*scalar
        wdec=Decimal(weight.numerator)/Decimal(weight.denominator)
        expected_logloss_high+=wdec*decimal
        expected_brier+=weight*oracle_label
        oracle_brier=best_label if oracle_brier is None else oracle_brier
        if oracle_brier!=best_label:
            raise AssertionError("true source latent label risk changed with candidate fit")
        count+=1
        all_samples.append({
            "source":source,"n_events_per_cluster":n,"m_training_clusters":m,
            "ordered_cluster_count_training_data":",".join(map(str,observed)),
            "source_original_training_joint_probability":str(weight),
            "sorted_fit_profile":",".join(map(str,profile)),
            **{f"train_likelihood_{name}":str(fit["all_candidate_fraction_likelihoods"][name]) for name in MODELS},
            "chosen_observable_model":selected,
            "independent_new_cluster_test_logloss":format(scalar,".16g"),
            "artificial_ORACLE_true_latent_high_label_Brier":str(oracle_label),
        })
    if allmass!=1 or count!=(n+1)**m:
        raise AssertionError("full original training count source not normalized")
    if abs(expected_logloss-float(expected_logloss_high))>1e-12:
        raise AssertionError("full source new cluster loss numeric audit differs")
    if sum(selected_mass.values(),F(0))!=1 or expected_brier<oracle_brier:
        raise AssertionError("finite model-selection probability invalid")
    return {
        "true_source":source,"n_events_per_cluster":n,"training_clusters_m":m,
        "ordered_training_tables":count,
        "true_source_complete_count_PMF":[str(v) for v in truth],
        "latent_raw_moments_q1_q2_q3":[str(latent_moment(source,r)) for r in (1,2,3)],
        "source_observable_factorial_moments":[str(count_factorial_moment(source,n,r)) for r in range(1,n+1)],
        "model_selection_probabilities":{c:str(v) for c,v in selected_mass.items()},
        "true_candidate_selection_probability":str(selected_mass[source]),
        "expected_independent_NEW_group_logloss":format(expected_logloss,".16g"),
        "expected_artificial_ORACLE_high_component_Brier":str(expected_brier),
        "true_source_optimal_artificial_ORACLE_high_component_Brier":str(oracle_brier),
        "latent_oracle_excess_brier":str(expected_brier-oracle_brier),
        "all_independent_PMF_and_predictive_scores_double_verified":True,
    }


def serialize_fits(library):
    entries=[]
    for (n,profile),fit in sorted(library.items()):
        entries.append({
            "n":n,"m":len(profile),"sorted_training_count_profile":list(profile),
            "chosen_candidate":fit["selected_candidate"],
            "all_exact_training_likelihoods":{name:str(x) for name,x in fit["all_candidate_fraction_likelihoods"].items()},
            "chosen_candidate_full_new_group_PMF":[str(v) for v in fit["selected_count_PMF"]],
            "independent_PMF_and_likelihood_checks_passed":True,
        })
    return entries


def run():
    records=[]
    worlds_out=[evaluate_world(*spec,records) for spec in worlds()]
    if len(worlds_out)!=24 or len(records)!=512:
        raise AssertionError("frozen world or training source set was modified")
    if any(distribution(s,1)!=(F(1,2),F(1,2)) for s in MODELS):
        raise AssertionError("all candidates must have matching single-trial means")
    if any(distribution("S",n)!=distribution("A",n) for n in (1,2)):
        raise AssertionError("symmetric/skewed mixture first two moments diverged")
    if distribution("S",3)[3]!=F(7,32) or distribution("A",3)[3]!=F(89,384):
        raise AssertionError("frozen third-order mixture identification difference failed")
    if conditional_high_posterior("S",2,1)!=F(1,2) or conditional_high_posterior("A",2,1)!=F(7,39):
        raise AssertionError("frozen identical K distribution but incompatible high type posteriors failed")
    if latent_moment("A",3)-latent_moment("S",3)!=F(5,384):
        raise AssertionError("skewed mixture third-moment mechanism drift")
    for source in MODELS:
        for n in N_VALUES:
            if label_swap_pmf(source,n)!=distribution(source,n):
                raise AssertionError("latent component label swapping changed observable count PMF")
            for r in range(1,n+1):
                if count_factorial_moment(source,n,r)!=latent_moment(source,r):
                    raise AssertionError("observable group factorial moment differs from latent propensity moment")
    with SAMPLES.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(records)
    rows=serialize_fits(fit_library())
    FITS.write_text(json.dumps({
        "research_id":"R193","unique_finite_likelihood_profiles":len(rows),
        "four_candidates_frozen":list(MODELS),"profiles":rows
    },sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    focus=[w for w in worlds_out if w["true_source"] in ("S","A") and w["n_events_per_cluster"] in (2,3)]
    if len(focus)!=8:
        raise AssertionError("frozen identifiability contrast removed")
    for m in M_VALUES:
        left=next(x for x in focus if x["true_source"]=="S" and x["n_events_per_cluster"]==2 and x["training_clusters_m"]==m)
        right=next(x for x in focus if x["true_source"]=="A" and x["n_events_per_cluster"]==2 and x["training_clusters_m"]==m)
        if (left["true_source_complete_count_PMF"]!=right["true_source_complete_count_PMF"]
            or left["model_selection_probabilities"]!=right["model_selection_probabilities"]
            or left["expected_independent_NEW_group_logloss"]!=right["expected_independent_NEW_group_logloss"]):
            raise AssertionError("two-trial complete observational alias not preserved across m")
    result={
        "research_id":"R193",
        "status":"E1_ARTIFICIAL_EXACT_FINITE_BINOMIAL_MIXTURE_IDENTIFIABILITY",
        "world_count":24,"all_ordered_training_datasets":512,
        "unique_unordered_training_profiles":53,
        "all_source_PMF_closed_binomial_vs_Bernoulli_DP_equal":True,
        "all_source_count_factorial_moments_vs_latent_moments_equal":True,
        "n1_all_four_mixture_candidates_observationally_identical":True,
        "n2_symmetric_vs_asymmetric_full_observation_alias":True,
        "n3_third_moment_distinguishes_symmetric_vs_asymmetric":True,
        "n2_K1_identical_visible_counts_opposing_high_class_posterior":{"S":"1/2","A":"7/39"},
        "third_raw_moment_difference_A_minus_S":"5/384",
        "all_independent_new_cluster_logloss_math_decimal_equal":True,
        "all_true_latent_label_Brier_is_oracle_only_not_real_world_observable":True,
        "locked_identifiability_worlds":focus,
        "worlds":worlds_out,
        "complete_training_CSV_sha256":sha256(SAMPLES.read_bytes()).hexdigest(),
        "profile_library_SHA256":sha256(FITS.read_bytes()).hexdigest(),
        "real_human_or_history_data":False,"new_E2":0,"new_E3":0,
    }
    RESULT.write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    accept={
        "research_id":"R193","status":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_FINITE_MIXTURES",
        "world_count":24,"full_training_count_datasets":512,"unique_exact_fit_profiles":53,
        "PMF_two_independent_rational_algorithms_equal":True,
        "latent_moments_and_count_factorial_moments_verified":True,
        "n2_manifest_count_alias_and_divergent_hidden_class":True,
        "n3_identifiable_candidate_third_moment_difference":True,
        "train_likelihood_raw_and_count_histogram_equal":True,
        "new_independent_cluster_predictive_logloss_double_precision_agree":True,
        "true_latent_type_Brier_oracle_lower_bound_verified":True,
        "result_sha256":sha256(RESULT.read_bytes()).hexdigest(),
        "full_training_CSV_sha256":result["complete_training_CSV_sha256"],
        "fitted_library_sha256":result["profile_library_SHA256"],
        "new_E2":0,"new_E3":0,"real_human_or_history_data":False,
    }
    ACCEPT.write_text(json.dumps(accept,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R193_MACHINE_ACCEPTANCE",json.dumps(accept,sort_keys=True))
    print("R193_IDENTIFIABILITY_CONTRAST",json.dumps(focus,sort_keys=True))
    return result


def archive():
    names=[Path(__file__).name,RESULT.name,SAMPLES.name,FITS.name,ACCEPT.name]
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
    print("R193_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestFiniteBinomialMixtures(unittest.TestCase):
    def test_24_worlds(self):
        self.assertEqual(len(list(worlds())),24)
    def test_512_complete_training_samples(self):
        self.assertEqual(sum((n+1)**m for _,n,m in worlds()),512)
    def test_53_unique_profiles(self):
        self.assertEqual(len(fit_library()),53)
    def test_all_components_weights_sum_one(self):
        for model in MODELS:
            self.assertEqual(sum((w for w,q in COMPONENTS[model]),F(0)),1)
    def test_all_components_probabilities_strict_interior(self):
        for model in MODELS:
            self.assertTrue(all(F(0)<q<F(1) for w,q in COMPONENTS[model]))
    def test_all_source_two_algorithms_all_support_points(self):
        for source in MODELS:
            for n in N_VALUES:
                self.assertEqual(pmf_closed(source,n),pmf_dp(source,n))
    def test_each_PMF_normalizes(self):
        for source in MODELS:
            for n in N_VALUES:
                self.assertEqual(sum(distribution(source,n),F(0)),1)
    def test_exact_first_moment_all_models_half(self):
        for model in MODELS:
            self.assertEqual(latent_moment(model,1),F(1,2))
    def test_s_and_a_first_two_moments_equal(self):
        self.assertEqual(tuple(latent_moment("S",r) for r in (1,2)),
                         tuple(latent_moment("A",r) for r in (1,2)))
    def test_s_and_a_latent_variance_one_sixteenth(self):
        self.assertEqual(latent_moment("S",2)-latent_moment("S",1)**2,F(1,16))
        self.assertEqual(latent_moment("A",2)-latent_moment("A",1)**2,F(1,16))
    def test_all_models_n1_manifest_alias(self):
        self.assertTrue(all(distribution(model,1)==(F(1,2),F(1,2)) for model in MODELS))
    def test_s_vs_a_full_n2_observable_alias(self):
        self.assertEqual(distribution("S",2),distribution("A",2))
    def test_s_vs_a_n3_manifest_differ(self):
        self.assertNotEqual(distribution("S",3),distribution("A",3))
    def test_s_k3_7_over_32(self):
        self.assertEqual(distribution("S",3)[3],F(7,32))
    def test_a_k3_89_over_384(self):
        self.assertEqual(distribution("A",3)[3],F(89,384))
    def test_third_moment_difference_five_384(self):
        self.assertEqual(latent_moment("A",3)-latent_moment("S",3),F(5,384))
    def test_k1_n2_oracle_high_posterior_alias(self):
        self.assertEqual(conditional_high_posterior("S",2,1),F(1,2))
        self.assertEqual(conditional_high_posterior("A",2,1),F(7,39))
    def test_all_factorial_moments_match_hidden_moments(self):
        for model in MODELS:
            for n in N_VALUES:
                for r in range(1,n+1):
                    self.assertEqual(count_factorial_moment(model,n,r),latent_moment(model,r))
    def test_invalid_higher_moment_not_available_n2(self):
        with self.assertRaises(ValueError):
            count_factorial_moment("S",2,3)
    def test_label_switch_observable_invariant(self):
        for model in MODELS:
            for n in N_VALUES:
                self.assertEqual(label_swap_pmf(model,n),distribution(model,n))
    def test_true_joint_latent_marginalizes_to_observed(self):
        for model in MODELS:
            for n in N_VALUES:
                for k in range(n+1):
                    self.assertEqual(sum((joint_latent_count(model,n,c,k) for c in (0,1)),F(0)),
                                     distribution(model,n)[k])
    def test_two_likelihood_routes_every_full_training_sample(self):
        for source,n,m in worlds():
            pmf=distribution(source,n)
            for seq in product(range(n+1),repeat=m):
                self.assertEqual(likelihood_ordered(seq,pmf),likelihood_counter(seq,pmf))
    def test_each_full_training_source_probability_normalizes(self):
        for source,n,m in worlds():
            pmf=distribution(source,n)
            self.assertEqual(sum((likelihood_ordered(seq,pmf) for seq in product(range(n+1),repeat=m)),F(0)),1)
    def test_fit_tie_break_prefers_IID_n1(self):
        for m in M_VALUES:
            for k in combinations_with_replacement(range(2),m):
                self.assertEqual(fit_library()[(1,k)]["selected_candidate"],"IID")
    def test_n2_s_and_a_same_training_candidate_selection(self):
        for m in M_VALUES:
            for k in combinations_with_replacement(range(3),m):
                fit=fit_library()[(2,k)]
                self.assertEqual(fit["all_candidate_fraction_likelihoods"]["S"],
                                 fit["all_candidate_fraction_likelihoods"]["A"])
    def test_fit_library_all_full_positive(self):
        for fit in fit_library().values():
            self.assertTrue(all(v>0 for v in fit["selected_count_PMF"]))
    def test_independent_logloss_math_and_decimal(self):
        for source,n,m in worlds():
            for selected in MODELS:
                score,high,brier,oracle=heldout_scores(source,selected,n)
                self.assertAlmostEqual(score,float(high),places=12)
    def test_oracle_Brier_lower_bound_all_pairs(self):
        for source,n,m in worlds():
            for selected in MODELS:
                _,_,brier,oracle=heldout_scores(source,selected,n)
                self.assertGreaterEqual(brier,oracle)
    def test_oracle_true_candidate_minimum(self):
        for model in MODELS:
            for n in N_VALUES:
                _,_,brier,oracle=heldout_scores(model,model,n)
                self.assertEqual(brier,oracle)
    def test_bad_model_disallowed(self):
        with self.assertRaises(ValueError):
            distribution("NOT_A_MODEL",2)
    def test_invalid_n_disallowed(self):
        with self.assertRaises(ValueError):
            pmf_closed("S",4)
    def test_invalid_oracle_count_disallowed(self):
        with self.assertRaises(ValueError):
            conditional_high_posterior("S",2,3)
    def test_invalid_latent_class_disallowed(self):
        with self.assertRaises(ValueError):
            joint_latent_count("A",2,2,1)
    def test_invalid_unsorted_fit_disallowed(self):
        with self.assertRaises(ValueError):
            fit_profile(2,(2,0))
    def test_invalid_short_fit_disallowed(self):
        with self.assertRaises(ValueError):
            fit_profile(2,(0,))
    def test_invalid_moment_disallowed(self):
        with self.assertRaises(ValueError):
            latent_moment("A",4)
    def test_full_model_code_tie_order(self):
        self.assertEqual(MODELS,("IID","S","A","W"))


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("Use --test or --run-and-archive")
