"""R192 exact two-class binary-indicator latent structure identifiability audit.

Two model orientations A vs B are observationally identical with only two
binary indicators, but their latent class posteriors differ. A third fixed
informative indicator distinguishes these specific orientations. Global class
name switching remains non-identifiable. Training and future test use only
visible features; class Brier is expressly oracle-labeled synthetic E1 data.
"""
from __future__ import annotations

from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations,combinations_with_replacement,product
from math import factorial,log
from pathlib import Path
import csv,json,sys,unittest,zipfile

HERE=Path(__file__).resolve().parent
PROTO=HERE.parent.parent/"protocols/R192_LATENT_CLASS_8_WORLDS_1312_TRAINING_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R192_EXACT_RESULTS.json"
RAW=HERE/"R192_ALL_1312_OBSERVABLE_TRAINING_DATASETS.csv"
FITS=HERE/"R192_ALL_186_LATENT_CLASS_FIT_PROFILES.json"
ACCEPT=HERE/"R192_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R192_Exact_8_Latent_Class_Worlds.zip"
ORIENTATIONS=("A","B")
J_VALUES=(2,3)
M_VALUES=(2,3)
Q_PAIR={
    "A":(F(3,4),F(5,6)),
    "B":(F(5,6),F(3,4)),
}


def worlds():
    for source,J,m in product(ORIENTATIONS,J_VALUES,M_VALUES):
        yield source,J,m


def probabilities(orientation,J):
    if orientation not in ORIENTATIONS or J not in J_VALUES:
        raise ValueError("latent class model outside original candidate registry")
    vals=Q_PAIR[orientation]
    return vals if J==2 else vals+(F(3,4),)


@lru_cache(maxsize=None)
def patterns(J):
    if J not in J_VALUES:
        raise ValueError("invalid manifest indicator count")
    return tuple(product((0,1),repeat=J))


def class_feature_likelihood(pattern,q,C):
    """Finite conditional independence of visible variables given latent class."""
    if C not in (0,1) or len(pattern)!=len(q) or any(x not in (0,1) for x in pattern):
        raise ValueError("bad latent class or observed indicator")
    conditional_q=q if C==1 else tuple(1-v for v in q)
    score=F(1)
    for x,p in zip(pattern,conditional_q):
        score*=p if x==1 else 1-p
    return score


def joint_observed_class(pattern,q,C):
    return F(1,2)*class_feature_likelihood(pattern,q,C)


def full_visible_mixture(pattern,q):
    """Algorithm A: exact direct mixture over two latent classes."""
    return joint_observed_class(pattern,q,0)+joint_observed_class(pattern,q,1)


def even_spin_mixture(pattern,q):
    """Algorithm B: independently expand even-order sign interactions."""
    J=len(pattern)
    signed=[(2*x-1)*(2*v-1) for x,v in zip(pattern,q)]
    coefficient=F(1)
    for subset_size in range(2,J+1,2):
        for subset in combinations(range(J),subset_size):
            term=F(1)
            for j in subset:
                term*=signed[j]
            coefficient+=term
    return coefficient/F(2**J)


@lru_cache(maxsize=None)
def observed_distribution(orientation,J):
    q=probabilities(orientation,J)
    direct=tuple(full_visible_mixture(bits,q) for bits in patterns(J))
    spin=tuple(even_spin_mixture(bits,q) for bits in patterns(J))
    if direct!=spin or sum(direct,F(0))!=1 or any(p<=0 for p in direct):
        raise AssertionError("two independent latent mixture PMF methods disagree")
    return direct


def posterior_class1(pattern,q):
    c1=joint_observed_class(pattern,q,1)
    pobs=full_visible_mixture(pattern,q)
    if pobs<=0:
        raise ValueError("zero probability source observation")
    return c1/pobs


def swapped_label_distribution(pattern,q):
    """Rename C=0 and C=1 and switch all per-class indicator probabilities."""
    swapped=tuple(1-p for p in q)
    return full_visible_mixture(pattern,swapped)


def training_raw_likelihood(observations,model_pmf):
    score=F(1)
    for i in observations:
        score*=model_pmf[i]
    return score


def training_hist_likelihood(observations,model_pmf):
    score=F(1)
    for i,k in Counter(observations).items():
        score*=model_pmf[i]**k
    return score


def fit_profile(J,profile):
    if J not in J_VALUES or len(profile) not in M_VALUES or tuple(profile)!=tuple(sorted(profile)) or any(i not in range(2**J) for i in profile):
        raise ValueError("invalid observed training response profile")
    scores={}
    for candidate in ORIENTATIONS:
        pmf=observed_distribution(candidate,J)
        direct=training_raw_likelihood(profile,pmf)
        by_counts=training_hist_likelihood(profile,pmf)
        if direct!=by_counts:
            raise AssertionError("individual-sequence and frequency likelihood differ")
        scores[candidate]=direct
    winner="A" if scores["A"]>=scores["B"] else "B"
    return {"J":J,"m":len(profile),"profile":profile,
            "A_source_model_likelihood":scores["A"],
            "B_source_model_likelihood":scores["B"],
            "selected_model_with_A_tie_break":winner,
            "two_full_likelihood_and_two_PMF_methods_agree":True}


@lru_cache(maxsize=None)
def fit_library():
    fits={}
    for J,m in product(J_VALUES,M_VALUES):
        for profile in combinations_with_replacement(range(2**J),m):
            fits[(J,profile)]=fit_profile(J,profile)
    if len(fits)!=186:
        raise AssertionError("frozen 186 sorted profile universe changed")
    return fits


@lru_cache(maxsize=None)
def independent_future_scores(source,J,selected):
    true_pmf=observed_distribution(source,J)
    predicted=observed_distribution(selected,J)
    float_visible=-sum(float(p)*log(float(q)) for p,q in zip(true_pmf,predicted))
    with localcontext() as ctx:
        ctx.prec=60
        dec_visible=-sum(
            Decimal(p.numerator)/Decimal(p.denominator)*
            (Decimal(q.numerator)/Decimal(q.denominator)).ln()
            for p,q in zip(true_pmf,predicted)
        )
    if abs(float_visible-float(dec_visible))>1e-12:
        raise AssertionError("independent float and decimal manifest predictive scores disagree")
    truth_q=probabilities(source,J)
    fit_q=probabilities(selected,J)
    oracle_brier=F(0)
    true_best_brier=F(0)
    for bits in patterns(J):
        estimate=posterior_class1(bits,fit_q)
        truth_post=posterior_class1(bits,truth_q)
        pobs=full_visible_mixture(bits,truth_q)
        true_best_brier+=pobs*truth_post*(1-truth_post)
        oracle_brier+=joint_observed_class(bits,truth_q,1)*(1-estimate)**2
        oracle_brier+=joint_observed_class(bits,truth_q,0)*estimate**2
    if oracle_brier<true_best_brier:
        raise AssertionError("fitted class prediction beats oracle truth posterior")
    return float_visible,dec_visible,oracle_brier,true_best_brier


def analyze_world(source,J,m,library,samples):
    true=observed_distribution(source,J)
    p_total=F(0)
    winnerA=F(0)
    winnerCorrect=F(0)
    visible=0.0
    visible_decimal=Decimal(0)
    class_brier=F(0)
    oracle_brier=None
    n_tables=0
    for seq in product(range(2**J),repeat=m):
        weight=training_raw_likelihood(seq,true)
        fit=library[(J,tuple(sorted(seq)))]
        selected=fit["selected_model_with_A_tie_break"]
        lfloat,ldec,brier,best=independent_future_scores(source,J,selected)
        p_total+=weight
        n_tables+=1
        winnerA+=weight*int(selected=="A")
        winnerCorrect+=weight*int(selected==source)
        visible+=float(weight)*lfloat
        visible_decimal+=Decimal(weight.numerator)/Decimal(weight.denominator)*ldec
        class_brier+=weight*brier
        if oracle_brier is None:
            oracle_brier=best
        elif oracle_brier!=best:
            raise AssertionError("true Bayes Brier inconsistent with fit choice")
        samples.append({
            "source_class_mechanism":source,
            "number_of_observed_binary_indicators_J":J,
            "training_individual_count_m":m,
            "ordered_visible_individual_patterns":",".join(map(str,seq)),
            "true_joint_training_probability":str(weight),
            "unordered_exact_fit_profile":",".join(map(str,sorted(seq))),
            "exact_likelihood_model_A":str(fit["A_source_model_likelihood"]),
            "exact_likelihood_model_B":str(fit["B_source_model_likelihood"]),
            "chosen_manifest_only_model":selected,
            "independent_new_visible_individual_logloss":format(lfloat,".16g"),
            "independent_new_ORACLE_latent_class_Brier":str(brier),
        })
    if p_total!=1 or n_tables!=(2**J)**m:
        raise AssertionError("full training source not normalized")
    if abs(visible-float(visible_decimal))>1e-12:
        raise AssertionError("weighted full-source float vs decimal predictive logloss failed")
    if class_brier<oracle_brier:
        raise AssertionError("latent class oracle Brier cannot exceed fitted Brier")
    return {
        "true_source_orientation":source,
        "binary_indicator_count_J":J,"training_people_m":m,
        "complete_ordered_training_datasets":n_tables,
        "true_visible_full_PMF":[str(p) for p in true],
        "probability_fitted_A":str(winnerA),
        "probability_fitted_truth_orientation":str(winnerCorrect),
        "expected_new_visible_person_logloss_float":format(visible,".16g"),
        "expected_new_ORACLE_labeled_person_Brier":str(class_brier),
        "truth_orientation_ideal_ORACLE_labeled_person_Brier":str(oracle_brier),
        "excess_oracle_class_Brier_due_to_wrong_fitted_orientation":str(class_brier-oracle_brier),
        "full_source_probability_and_independent_numeric_loss_agree":True
    }


def run():
    fits=fit_library()
    samples=[]
    output=[analyze_world(source,J,m,fits,samples) for source,J,m in worlds()]
    if len(output)!=8 or len(samples)!=1312:
        raise AssertionError("prescored full latent class source/sample counts changed")
    manifest_alias=[x for x in output if x["binary_indicator_count_J"]==2]
    if len(manifest_alias)!=4:
        raise AssertionError("two-indicator full observational alias not included")
    for m in M_VALUES:
        a=next(w for w in manifest_alias if w["true_source_orientation"]=="A" and w["training_people_m"]==m)
        b=next(w for w in manifest_alias if w["true_source_orientation"]=="B" and w["training_people_m"]==m)
        if not (a["true_visible_full_PMF"]==b["true_visible_full_PMF"]
                and a["probability_fitted_A"]==b["probability_fitted_A"]=="1"
                and a["expected_new_visible_person_logloss_float"]==b["expected_new_visible_person_logloss_float"]
                and F(b["excess_oracle_class_Brier_due_to_wrong_fitted_orientation"])>0
                and a["excess_oracle_class_Brier_due_to_wrong_fitted_orientation"]=="0"):
            raise AssertionError("exact two-indicator manifest alias and latent label scoring contradiction failed")
    if posterior_class1((1,0),probabilities("A",2))!=F(3,8) or posterior_class1((1,0),probabilities("B",2))!=F(5,8):
        raise AssertionError("fixed 3/8 versus 5/8 latent class attribution does not hold")
    if observed_distribution("A",3)==observed_distribution("B",3):
        raise AssertionError("third indicator failed to distinguish fixed parameter orientations")
    for source,J,m in worlds():
        q=probabilities(source,J)
        for bits in patterns(J):
            if full_visible_mixture(bits,q)!=swapped_label_distribution(bits,q):
                raise AssertionError("class name swapping changed observable evidence")
            switched=posterior_class1(bits,tuple(1-v for v in q))
            if posterior_class1(bits,q)+switched!=1:
                raise AssertionError("class label swap did not reverse posterior")
    with RAW.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(samples[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(samples)
    profile_lib={
        "research_id":"R192",
        "unique_training_profiles":len(fits),
        "two_candidate_models_are_fixed_not_fit_using_labels":True,
        "profiles":[{
            "J":J,"m":len(observed),"ordered_equivalent_profile":list(observed),
            "likelihood_A":str(v["A_source_model_likelihood"]),
            "likelihood_B":str(v["B_source_model_likelihood"]),
            "selected_manifest_only_model":v["selected_model_with_A_tie_break"],
            "two_independent_PMF_and_likelihood_methods_equal":True,
        } for (J,observed),v in sorted(fits.items())]
    }
    FITS.write_text(json.dumps(profile_lib,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    result={
        "research_id":"R192",
        "stage":"E1_ARTIFICIAL_EXACT_TWO_LATENT_CLASSES_2_VS_3_BINARY_INDICATORS",
        "world_count":8,"complete_ordered_training_datasets":1312,
        "unique_manifest_only_training_profiles":186,
        "two_indicator_A_B_all_observable_distributions_identical":True,
        "third_indicator_differentiates_fixed_A_B_manifest_distribution":True,
        "latent_class_label_switching_observationally_invariant_even_at_three_indicators":True,
        "frozen_two_indicator_attribution_posteriors":{"A_P_C1_given_1_0":"3/8","B_P_C1_given_1_0":"5/8"},
        "all_8_worlds_tested_with_independent_new_person_visible_loss_and_oracle_class_Brier":True,
        "fixed_full_manifest_aliases":manifest_alias,
        "worlds":output,
        "full_original_training_CSV_sha256":sha256(RAW.read_bytes()).hexdigest(),
        "all_fitted_manifest_only_profiles_sha256":sha256(FITS.read_bytes()).hexdigest(),
        "new_E2":0,"new_E3":0,"real_human_or_historical_data":False
    }
    RESULT.write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    accept={
        "research_id":"R192","status":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_LATENT_CLASS",
        "worlds":8,"full_ordered_training_records":1312,
        "unique_manifest_training_fits":186,
        "two_independent_latent_mixture_PMF_methods":True,
        "manifest_likelihood_raw_and_histogram_Fraction_exact":True,
        "two_indicator_full_observable_alias_and_opposing_true_posteriors":True,
        "third_indicator_A_B_discrimination_and_global_label_swap_limits":True,
        "external_new_person_logloss_math_and_decimal_double_checked":True,
        "artificial_true_label_Brier_and_oracle_lower_bound_Fraction":True,
        "result_sha256":sha256(RESULT.read_bytes()).hexdigest(),
        "source_CSV_sha256":result["full_original_training_CSV_sha256"],
        "manifest_profile_SHA256":result["all_fitted_manifest_only_profiles_sha256"],
        "new_E2":0,"new_E3":0,"real_human_or_historical_data":False
    }
    ACCEPT.write_text(json.dumps(accept,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R192_MACHINE_ACCEPTANCE",json.dumps(accept,sort_keys=True))
    print("R192_LOCKED_ALIAS",json.dumps(manifest_alias,sort_keys=True))
    return result


def archive():
    files=[Path(__file__).name,RESULT.name,RAW.name,FITS.name,ACCEPT.name]
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
    print("R192_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestTwoClassLatentIdentifiability(unittest.TestCase):
    def test_eight_source_worlds(self):
        self.assertEqual(len(list(worlds())),8)
    def test_full_1312_ordered_training_count(self):
        self.assertEqual(sum((2**J)**m for source,J,m in worlds()),1312)
    def test_full_profile_library_186(self):
        self.assertEqual(len(fit_library()),186)
    def test_all_source_mixture_and_even_spin_exact(self):
        for source,J,m in worlds():
            q=probabilities(source,J)
            for bits in patterns(J):
                self.assertEqual(full_visible_mixture(bits,q),even_spin_mixture(bits,q))
    def test_full_candidate_observed_PMF_normalized(self):
        for source in ORIENTATIONS:
            for J in J_VALUES:
                self.assertEqual(sum(observed_distribution(source,J),F(0)),1)
    def test_all_candidates_strict_positive(self):
        for source in ORIENTATIONS:
            for J in J_VALUES:
                self.assertTrue(all(p>0 for p in observed_distribution(source,J)))
    def test_full_J2_manifest_alias(self):
        self.assertEqual(observed_distribution("A",2),observed_distribution("B",2))
    def test_full_J3_manifest_nonalias(self):
        self.assertNotEqual(observed_distribution("A",3),observed_distribution("B",3))
    def test_exact_opposing_posteriors_for_same_two_indicator_pattern(self):
        self.assertEqual(posterior_class1((1,0),probabilities("A",2)),F(3,8))
        self.assertEqual(posterior_class1((1,0),probabilities("B",2)),F(5,8))
    def test_two_indicator_training_likelihood_both_orientations_identical(self):
        for m in M_VALUES:
            for obs in product(range(4),repeat=m):
                q=tuple(sorted(obs))
                fit=fit_library()[(2,q)]
                self.assertEqual(fit["A_source_model_likelihood"],fit["B_source_model_likelihood"])
                self.assertEqual(fit["selected_model_with_A_tie_break"],"A")
    def test_three_indicator_likelihood_can_prefer_B(self):
        self.assertTrue(any(v["selected_model_with_A_tie_break"]=="B" for (J,k),v in fit_library().items() if J==3))
    def test_exact_sequence_vs_hist_likelihood(self):
        for J,m in product(J_VALUES,M_VALUES):
            for seq in product(range(2**J),repeat=m):
                for orientation in ORIENTATIONS:
                    q=observed_distribution(orientation,J)
                    self.assertEqual(training_raw_likelihood(seq,q),training_hist_likelihood(seq,q))
    def test_m2_and_m3_full_source_probability_one(self):
        for source,J,m in worlds():
            laws=observed_distribution(source,J)
            self.assertEqual(sum((training_raw_likelihood(obs,laws) for obs in product(range(2**J),repeat=m)),F(0)),1)
    def test_latent_swap_manifest_distribution_invariant(self):
        for source,J,m in worlds():
            q=probabilities(source,J)
            for bits in patterns(J):
                self.assertEqual(full_visible_mixture(bits,q),swapped_label_distribution(bits,q))
    def test_latent_swap_posteriors_complement(self):
        for source,J,m in worlds():
            q=probabilities(source,J)
            for bits in patterns(J):
                self.assertEqual(posterior_class1(bits,q)+posterior_class1(bits,tuple(1-v for v in q)),1)
    def test_model_fit_not_using_hidden_class(self):
        for fit in fit_library().values():
            self.assertIn(fit["selected_model_with_A_tie_break"],ORIENTATIONS)
    def test_no_misspecified_prediction_beats_oracle_labeled_Brier(self):
        for source,J,fit in product(ORIENTATIONS,J_VALUES,ORIENTATIONS):
            _,_,brier,best=independent_future_scores(source,J,fit)
            self.assertGreaterEqual(brier,best)
    def test_oracle_Brier_is_zero_only_if_perfect_classes(self):
        _,_,brier,_=independent_future_scores("A",2,"A")
        self.assertGreater(brier,0)
    def test_all_visible_logloss_two_numeric_routes(self):
        for source,J,fit in product(ORIENTATIONS,J_VALUES,ORIENTATIONS):
            score,dec,_,_=independent_future_scores(source,J,fit)
            self.assertAlmostEqual(score,float(dec),places=12)
    def test_labeled_truth_Brier_strictly_worse_when_wrong_J2(self):
        _,_,a,besta=independent_future_scores("A",2,"A")
        _,_,b,bestb=independent_future_scores("B",2,"A")
        self.assertEqual(a,besta)
        self.assertGreater(b,bestb)
    def test_visible_predictive_loss_same_under_J2_alias(self):
        la,_,_,_=independent_future_scores("A",2,"A")
        lb,_,_,_=independent_future_scores("B",2,"A")
        self.assertEqual(la,lb)
    def test_true_visible_source_label_fraction(self):
        q=probabilities("A",2)
        self.assertEqual(sum(joint_observed_class(bits,q,1) for bits in patterns(2)),F(1,2))
    def test_true_class_prior_half(self):
        q=probabilities("B",3)
        self.assertEqual(sum(joint_observed_class(bits,q,0) for bits in patterns(3)),F(1,2))
    def test_invalid_orientation(self):
        with self.assertRaises(ValueError):
            probabilities("C",2)
    def test_invalid_J(self):
        with self.assertRaises(ValueError):
            patterns(4)
    def test_invalid_class(self):
        with self.assertRaises(ValueError):
            class_feature_likelihood((1,0),probabilities("A",2),2)
    def test_invalid_indicator_binary_value(self):
        with self.assertRaises(ValueError):
            class_feature_likelihood((2,0),probabilities("A",2),1)
    def test_invalid_fit_profile_unsorted(self):
        with self.assertRaises(ValueError):
            fit_profile(2,(3,1))
    def test_invalid_fit_profile_length(self):
        with self.assertRaises(ValueError):
            fit_profile(2,(0,))
    def test_two_indicators_are_conditionally_independent_given_C(self):
        q=probabilities("A",2)
        self.assertEqual(class_feature_likelihood((1,0),q,1),q[0]*(1-q[1]))
    def test_one_full_world_exact_sample_logloss(self):
        result=analyze_world("B",2,2,fit_library(),[])
        self.assertEqual(result["probability_fitted_A"],"1")


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("Usage --test or --run-and-archive")
