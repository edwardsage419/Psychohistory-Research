"""R199 six exact binary HMMs: observable identification vs latent decoding.

Six fixed hidden transition / emission candidates, L in (3,4),
m in (1,2): 24 synthetic worlds, 2064 original ordered training
sets and 196 order-equivalent fit profiles. Independently validate
full hidden-path sums vs forward recursion, smoothing via alpha-beta
vs hidden paths, and Viterbi max-product vs path brute force.
Train on observed sequences ONLY; test on an independent NEW sequence.
Latent label scoring uses artificial ground truth, never real data.
"""
from __future__ import annotations

from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement,product
from math import log
from pathlib import Path
import csv,json,sys,unittest,zipfile

HERE=Path(__file__).resolve().parent
PROTOCOL=HERE.parent.parent/"protocols/R199_HMM_24_WORLDS_2064_TRAINS_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R199_EXACT_RESULTS.json"
TRAIN=HERE/"R199_ALL_2064_ORDERED_OBSERVED_TRAINING_SETS.csv"
FITS=HERE/"R199_ALL_196_OBSERVABLE_FIT_PROFILES.json"
DECODE=HERE/"R199_ALL_144_OBSERVABLE_HIDDEN_DECODINGS.json"
ACCEPT=HERE/"R199_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R199_Exact_24_HMM_Sequence_Worlds.zip"

MODELS=("BASE","LABEL_SWAPPED","IID_HIDDEN","SWITCH_HIDDEN","WEAK_SIGNAL","STRONG_SIGNAL")
PARAMETERS={
    "BASE":(F(3,4),F(3,4)),
    "LABEL_SWAPPED":(F(3,4),F(1,4)),
    "IID_HIDDEN":(F(1,2),F(3,4)),
    "SWITCH_HIDDEN":(F(1,4),F(3,4)),
    "WEAK_SIGNAL":(F(3,4),F(5,8)),
    "STRONG_SIGNAL":(F(3,4),F(7,8)),
}
LENGTHS=(3,4)
M_COUNTS=(1,2)


def validate(name,L):
    if name not in MODELS or L not in LENGTHS:
        raise ValueError("Invalid frozen HMM model or observed sequence length")


@lru_cache(maxsize=None)
def binary_paths(L):
    if L not in LENGTHS and L not in (1,2):
        raise ValueError("Out-of-protocol binary history length")
    return tuple(product((0,1),repeat=L))


def tr(a,old,new):
    return a if old==new else 1-a


def em(r,latent,obs):
    return r if latent==obs else 1-r


def joint_hidden_observed(name,visible,hidden):
    """Independent complete latent source path probability."""
    if name not in PARAMETERS or len(visible) not in LENGTHS:
        raise ValueError("Unsupported full observed sample")
    if len(visible)!=len(hidden) or any(x not in (0,1) for x in visible+hidden):
        raise ValueError("Invalid full observable/hidden sample")
    a,r=PARAMETERS[name]
    prob=F(1,2)*em(r,hidden[0],visible[0])
    for t in range(1,len(visible)):
        prob*=tr(a,hidden[t-1],hidden[t])*em(r,hidden[t],visible[t])
    return prob


def alpha_beta(name,visible):
    """Independent message passing; never call full latent-path enumeration."""
    if name not in MODELS or len(visible) not in LENGTHS and len(visible) not in (1,2):
        raise ValueError("No HMM messages outside recorded prefix support")
    if any(x not in (0,1) for x in visible):
        raise ValueError("Nonbinary observation")
    a,r=PARAMETERS[name]
    alpha=[(F(1,2)*em(r,0,visible[0]),F(1,2)*em(r,1,visible[0]))]
    for y in visible[1:]:
        previous=alpha[-1]
        alpha.append(tuple(
            em(r,j,y)*sum((previous[i]*tr(a,i,j) for i in (0,1)),F(0))
            for j in (0,1)
        ))
    beta=[None]*len(visible)
    beta[-1]=(F(1),F(1))
    for t in range(len(visible)-2,-1,-1):
        beta[t]=tuple(
            sum((tr(a,i,j)*em(r,j,visible[t+1])*beta[t+1][j]
                 for j in (0,1)),F(0))
            for i in (0,1)
        )
    likelihood=sum(alpha[-1],F(0))
    if likelihood<=0:
        raise AssertionError("HMM full observation should have positive evidence")
    return tuple(alpha),tuple(beta),likelihood


@lru_cache(maxsize=None)
def observable_pmf(name,L):
    validate(name,L)
    visible=binary_paths(L)
    pmf=tuple(alpha_beta(name,obs)[2] for obs in visible)
    check=tuple(sum((joint_hidden_observed(name,obs,h)
                     for h in binary_paths(L)),F(0)) for obs in visible)
    if check!=pmf or sum(pmf,F(0))!=1 or min(pmf)<=0:
        raise AssertionError("Independent complete hidden paths vs forward HMM likelihood differ")
    return pmf


@lru_cache(maxsize=None)
def smoothed_class1(name,visible):
    alpha,beta,evidence=alpha_beta(name,visible)
    post=tuple(alpha[t][1]*beta[t][1]/evidence for t in range(len(visible)))
    if len(visible) in LENGTHS:
        brute=tuple(
            sum((joint_hidden_observed(name,visible,h) for h in binary_paths(len(visible))
                 if h[t]==1),F(0))/evidence
            for t in range(len(visible))
        )
        if post!=brute:
            raise AssertionError("Forward-backward smoothing differs from hidden path enumeration")
    if any(not F(0)<=p<=F(1) for p in post):
        raise AssertionError("HMM smoothed class posterior out of range")
    return post


@lru_cache(maxsize=None)
def viterbi_best_path(name,visible):
    """Max-product DP, lexicographically first complete path on ties."""
    if name not in MODELS or len(visible) not in LENGTHS:
        raise ValueError("Viterbi only for full protocol length")
    a,r=PARAMETERS[name]
    best={s:(F(1,2)*em(r,s,visible[0]),(s,)) for s in (0,1)}
    for y in visible[1:]:
        new={}
        for j in (0,1):
            choices=[(mass*tr(a,i,j)*em(r,j,y),path+(j,))
                     for i,(mass,path) in best.items()]
            new[j]=min(choices,key=lambda x:(-x[0],x[1]))
        best=new
    weight,path=min(best.values(),key=lambda x:(-x[0],x[1]))
    # Independent joint enumerator, with same path-level tie rule.
    maximum= min(
        ((joint_hidden_observed(name,visible,h),h) for h in binary_paths(len(visible))),
        key=lambda x:(-x[0],x[1])
    )
    if (weight,path)!=maximum:
        raise AssertionError("Independent brute-force MAP path differs from Viterbi DP")
    return path,weight


@lru_cache(maxsize=None)
def decode(name,visible):
    post=smoothed_class1(name,visible)
    vpath,score=viterbi_best_path(name,visible)
    # Marginally most likely hidden state, tie always chooses 0.
    pointwise=tuple(int(p>F(1,2)) for p in post)
    return post,vpath,pointwise,score


def next_visible_one(name,prefix):
    if name not in MODELS or len(prefix) not in (2,3):
        raise ValueError("Last-step conditional requires true visible prefix")
    alpha,beta,evidence=alpha_beta(name,prefix)
    post=alpha[-1][1]/evidence
    a,r=PARAMETERS[name]
    predicted_hidden1=(1-a)+(2*a-1)*post
    return (1-r)+(2*r-1)*predicted_hidden1


def likelihood_raw(indices,pmf):
    out=F(1)
    for k in indices:
        out*=pmf[k]
    return out


def likelihood_hist(indices,pmf):
    out=F(1)
    for k,num in Counter(indices).items():
        out*=pmf[k]**num
    return out


def fit_profile(L,profile):
    if (L not in LENGTHS or len(profile) not in M_COUNTS or
        tuple(profile)!=tuple(sorted(profile)) or
        any(x not in range(2**L) for x in profile)):
        raise ValueError("Unexpected training profile")
    likes={}
    for candidate in MODELS:
        pmf=observable_pmf(candidate,L)
        a=likelihood_raw(profile,pmf)
        b=likelihood_hist(profile,pmf)
        if a!=b:
            raise AssertionError("Independent session product and histogram likelihood differ")
        likes[candidate]=a
    winner=next(name for name in MODELS if likes[name]==max(likes.values()))
    return {"L":L,"m":len(profile),"profile":profile,"candidate_likelihoods":likes,
            "selected":winner}


@lru_cache(maxsize=None)
def fit_library():
    all_fits={}
    for L,m in product(LENGTHS,M_COUNTS):
        for profile in combinations_with_replacement(range(2**L),m):
            all_fits[(L,profile)]=fit_profile(L,profile)
    if len(all_fits)!=196:
        raise AssertionError("Frozen 196 complete fitted observable profiles absent")
    return all_fits


@lru_cache(maxsize=None)
def heldout_metrics(true_name,fit_name,L):
    """Truly new visible sequence + optional artificial truth-labeled hidden path."""
    truth=observable_pmf(true_name,L)
    fit=observable_pmf(fit_name,L)
    score=-sum(float(p)*log(float(q)) for p,q in zip(truth,fit))
    with localcontext() as ctx:
        ctx.prec=70
        decimal_score=-sum(
            (Decimal(p.numerator)/Decimal(p.denominator))*
            (Decimal(q.numerator)/Decimal(q.denominator)).ln()
            for p,q in zip(truth,fit)
        )
    if abs(score-float(decimal_score))>1e-12:
        raise AssertionError("Independent math.log and high precision Decimal visible scoring disagree")

    # Independent source-weighted new LAST observation Brier.
    path_brier=F(0)
    prefix_mass={}
    prefix_prob_true={}
    for obs,pobs in zip(binary_paths(L),truth):
        prefix=obs[:-1]
        p_fit=next_visible_one(fit_name,prefix)
        path_brier+=pobs*(obs[-1]-p_fit)**2
        prefix_mass[prefix]=prefix_mass.get(prefix,F(0))+pobs
        if obs[-1]==1:
            prefix_prob_true[prefix]=prefix_prob_true.get(prefix,F(0))+pobs
    conditional_brier=F(0)
    for prefix,weight in prefix_mass.items():
        p_true=prefix_prob_true.get(prefix,F(0))/weight
        pred=next_visible_one(fit_name,prefix)
        conditional_brier+=weight*(p_true*(1-pred)**2+(1-p_true)*pred*pred)
        if p_true!=next_visible_one(true_name,prefix):
            raise AssertionError("Independent complete visible test-prefix conditional forecast differs")
    if path_brier!=conditional_brier:
        raise AssertionError("New-sequence path integration and prefix-conditional Brier differ")

    latent_complete_correct=F(0)
    token_marginal=F(0)
    token_viterbi=F(0)
    for obs in binary_paths(L):
        vpath=decode(fit_name,obs)[1]
        pointwise=decode(fit_name,obs)[2]
        latent_complete_correct+=joint_hidden_observed(true_name,obs,vpath)
        true_posterior=smoothed_class1(true_name,obs)
        pobs=truth[binary_paths(L).index(obs)]
        for t in range(L):
            token_marginal+=pobs*(true_posterior[t] if pointwise[t] else 1-true_posterior[t])/L
            token_viterbi+=pobs*(true_posterior[t] if vpath[t] else 1-true_posterior[t])/L
    if (true_name==fit_name and token_marginal<token_viterbi):
        raise AssertionError("Correct model marginal posterior decoding worse than Viterbi token accuracy")
    if not all(F(0)<=v<=1 for v in (latent_complete_correct,token_marginal,token_viterbi)):
        raise AssertionError("Invalid E1 oracle labeled decoding accuracy")

    return {
        "new_complete_visible_logloss_float":score,
        "new_complete_visible_logloss_Decimal":decimal_score,
        "new_last_observation_brier_exact":path_brier,
        "new_artificial_ORACLE_full_hidden_path_accuracy":latent_complete_correct,
        "new_artificial_ORACLE_each_hidden_state_marginal_decoder_accuracy":token_marginal,
        "new_artificial_ORACLE_each_hidden_state_Viterbi_decoder_accuracy":token_viterbi,
        "two_independent_new_visible_Brier_routes":True,
    }


def worlds():
    for source,L,m in product(MODELS,LENGTHS,M_COUNTS):
        yield source,L,m


def source_world(source,L,m,all_rows):
    truth=observable_pmf(source,L)
    selected_mass={name:F(0) for name in MODELS}
    total_mass=F(0)
    total_score=0.0
    total_decimal=Decimal(0)
    total_brier=F(0)
    total_path_correct=F(0)
    total_marginal_correct=F(0)
    total_viterbi_tokens=F(0)
    n=0
    for training in product(range(2**L),repeat=m):
        weight=likelihood_raw(training,truth)
        profile=tuple(sorted(training))
        fit=fit_library()[(L,profile)]
        selected=fit["selected"]
        metrics=heldout_metrics(source,selected,L)
        selected_mass[selected]+=weight
        total_mass+=weight
        total_score+=float(weight)*metrics["new_complete_visible_logloss_float"]
        with localcontext() as ctx:
            ctx.prec=70
            total_decimal+=(Decimal(weight.numerator)/Decimal(weight.denominator))*metrics["new_complete_visible_logloss_Decimal"]
        total_brier+=weight*metrics["new_last_observation_brier_exact"]
        total_path_correct+=weight*metrics["new_artificial_ORACLE_full_hidden_path_accuracy"]
        total_marginal_correct+=weight*metrics["new_artificial_ORACLE_each_hidden_state_marginal_decoder_accuracy"]
        total_viterbi_tokens+=weight*metrics["new_artificial_ORACLE_each_hidden_state_Viterbi_decoder_accuracy"]
        n+=1
        all_rows.append({
            "actual_source_HMM":source,
            "sequence_length_L":L,"independent_training_sequences_m":m,
            "ordered_training_visible_sequence_indices":",".join(map(str,training)),
            "ordered_training_observations":";".join("".join(map(str,binary_paths(L)[i])) for i in training),
            "true_original_training_source_probability":str(weight),
            "unordered_complete_fit_profile":",".join(map(str,profile)),
            **{f"candidate_{name}_exact_visible_train_likelihood":str(fit["candidate_likelihoods"][name]) for name in MODELS},
            "selected_visible_likelihood_model":selected,
            "independent_new_visible_sequence_logloss":format(metrics["new_complete_visible_logloss_float"],".16g"),
            "independent_new_last_observation_Brier_exact":str(metrics["new_last_observation_brier_exact"]),
            "synthetic_ORACLE_new_hidden_full_path_exact_accuracy":str(metrics["new_artificial_ORACLE_full_hidden_path_accuracy"]),
            "synthetic_ORACLE_new_hidden_marginal_token_accuracy":str(metrics["new_artificial_ORACLE_each_hidden_state_marginal_decoder_accuracy"]),
            "synthetic_ORACLE_new_hidden_Viterbi_token_accuracy":str(metrics["new_artificial_ORACLE_each_hidden_state_Viterbi_decoder_accuracy"]),
        })
    if total_mass!=1 or sum(selected_mass.values(),F(0))!=1 or n!=(2**L)**m:
        raise AssertionError("Real original finite HMM training observation source not normalized")
    if abs(total_score-float(total_decimal))>1e-12:
        raise AssertionError("Whole-world heldout sequence logloss precision disagreement")
    return {
        "true_source":source,"L":L,"training_independent_sequences_m":m,
        "complete_ordered_training_observations":n,
        "real_observed_sequence_probability_PMF":[str(x) for x in truth],
        "selected_candidate_probability":{name:str(w) for name,w in selected_mass.items()},
        "true_source_candidate_selected_probability":str(selected_mass[source]),
        "independent_new_complete_observation_logloss_float":format(total_score,".16g"),
        "independent_new_last_observed_state_Brier_exact":str(total_brier),
        "synthetic_ORACLE_true_hidden_full_path_accuracy":str(total_path_correct),
        "synthetic_ORACLE_hidden_marginal_decoder_per_time_accuracy":str(total_marginal_correct),
        "synthetic_ORACLE_hidden_Viterbi_decoder_per_time_accuracy":str(total_viterbi_tokens),
        "all_human_data_or_history_real":False,
    }


def write_json(path,obj):
    path.write_text(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def run():
    original=[]
    world_results=[source_world(source,L,m,original) for source,L,m in worlds()]
    if len(world_results)!=24 or len(original)!=2064:
        raise AssertionError("Frozen 24-world, 2064 original training HMM universe incomplete")

    # Probe all 144 specific candidate x observed sequence decodings.
    decodes=[]
    paths_different=0
    for name in MODELS:
        for L in LENGTHS:
            for obs in binary_paths(L):
                post,vpath,marginal,weight=decode(name,obs)
                paths_different+=int(vpath!=marginal)
                decodes.append({
                    "fitted_candidate":name,"L":L,"visible_sequence":"".join(map(str,obs)),
                    "full_visible_PMF":str(observable_pmf(name,L)[binary_paths(L).index(obs)]),
                    "smoothed_probability_hidden_1_every_time":[str(v) for v in post],
                    "Viterbi_full_joint_MAP_hidden_path":"".join(map(str,vpath)),
                    "Viterbi_max_complete_joint_probability":str(weight),
                    "pointwise_marginal_MAP_hidden_states":"".join(map(str,marginal)),
                    "whole_path_and_marginal_decode_different":vpath!=marginal
                })
    if len(decodes)!=144:
        raise AssertionError("All 144 observable-hidden decoding profiles not preserved")

    for L in LENGTHS:
        if observable_pmf("BASE",L)!=observable_pmf("LABEL_SWAPPED",L):
            raise AssertionError("Fixed observable HMM state-label alias failed")
        for obs in binary_paths(L):
            one=smoothed_class1("BASE",obs)
            two=smoothed_class1("LABEL_SWAPPED",obs)
            if any(p+q!=1 for p,q in zip(one,two)):
                raise AssertionError("True hidden posterior label swap did not complement")
            for latent in binary_paths(L):
                swapped=tuple(1-i for i in latent)
                if (joint_hidden_observed("BASE",obs,latent)!=
                    joint_hidden_observed("LABEL_SWAPPED",obs,swapped)):
                    raise AssertionError("Joint latent state name switching invalid")
    if any(observable_pmf("IID_HIDDEN",L)==observable_pmf("BASE",L) for L in LENGTHS):
        raise AssertionError("IID visible sequence should be distinguishable from persistent source")
    for L in LENGTHS:
        expected=(F(1,2**L),)*(2**L)
        if observable_pmf("IID_HIDDEN",L)!=expected:
            raise AssertionError("IID hidden must induce fully IID symmetric observed sequences")
    # A correct-source Viterbi path is Bayes-optimal for complete-path 0/1 scoring.
    for L in LENGTHS:
        for source in MODELS:
            own=heldout_metrics(source,source,L)["new_artificial_ORACLE_full_hidden_path_accuracy"]
            for fitted in MODELS:
                other=heldout_metrics(source,fitted,L)["new_artificial_ORACLE_full_hidden_path_accuracy"]
                if own<other:
                    raise AssertionError("True-source global MAP path worse than arbitrary alternative")
    with TRAIN.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(original[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(original)

    fit_json={
        "research_id":"R199","full_exact_fit_profiles":196,"fixed_training_label_tie_order":list(MODELS),
        "profiles":[{
            "L":L,"m":len(obs),"sorted_visible_training_indices":list(obs),
            "fitted_max_likelihood_candidate":x["selected"],
            "all_exact_observed_training_likelihoods":{k:str(v) for k,v in x["candidate_likelihoods"].items()},
            "session_probability_product_and_Counter_exact":True
        } for (L,obs),x in sorted(fit_library().items())]
    }
    write_json(FITS,fit_json)
    write_json(DECODE,{"research_id":"R199","complete_candidate_and_observation_decodings":len(decodes),
                      "Viterbi_MAP_path_differs_from_per_time_posterior_decoding_count":paths_different,
                      "all_observations":decodes})
    focus=[x for x in world_results if x["true_source"] in ("BASE","LABEL_SWAPPED")]

    result={
        "research_id":"R199",
        "research_stage":"E1_ARTIFICIAL_EXACT_OBSERVABLE_HMM_VS_TRUE_HIDDEN_PATH_DECODING",
        "artificial_worlds":24,"full_original_ordered_training_sets":2064,
        "unique_exact_visible_training_fit_profiles":196,
        "all_model_observed_full_sequence_decodings":144,
        "Viterbi_vs_marginal_MAP_different_full_visible_sequences":paths_different,
        "full_forward_message_vs_latent_path_evidence_Fraction_equal":True,
        "alpha_beta_smoothed_hidden_vs_full_bruteforce_Fraction_equal":True,
        "Viterbi_max_product_vs_complete_hidden_path_argmax_Fraction_equal":True,
        "session_training_likelihood_product_vs_histogram_Fraction_equal":True,
        "full_observed_new_sequence_logloss_math_and_Decimal_agree":True,
        "next_new_observation_Brier_full_path_vs_conditional_prefix_Fraction_equal":True,
        "BASE_vs_LABEL_SWAPPED_all_observations_identical_and_hidden_posteriors_complement":True,
        "known_true_source_Viterbi_full_path_accuracy_is_Bayes_optimal":True,
        "true_label_oracle_accuracy_only_on_artificial_latent_ground_truth":True,
        "prelocked_label_alias_worlds":focus,
        "all_original_worlds":world_results,
        "all_original_training_CSV_sha256":sha256(TRAIN.read_bytes()).hexdigest(),
        "all_196_fit_profile_SHA256":sha256(FITS.read_bytes()).hexdigest(),
        "all_144_decodings_SHA256":sha256(DECODE.read_bytes()).hexdigest(),
        "new_E2":0,"new_E3":0,"real_human_or_historical_data":False
    }
    write_json(RESULT,result)
    accept={
        "research_id":"R199","status":"CLOSED_BOUNDED_E1_ARTIFICIAL_HMM_SEQUENCE_DECODING",
        "artificial_worlds":24,"full_original_training_sets":2064,"full_fit_profiles":196,
        "observable_HMM_decodings":144,
        "all_evidence_posterior_and_Viterbi_independent_algorithms_exact":True,
        "label_switching_observable_PMF_alias_and_latent_complement":True,
        "all_independent_new_complete_sequence_logloss_and_last_measurement_Brier_checked":True,
        "artificial_truth_labeled_full_path_and_per_time_accuracy":True,
        "full_result_SHA256":sha256(RESULT.read_bytes()).hexdigest(),
        "original_training_CSV_SHA256":result["all_original_training_CSV_sha256"],
        "fitted_profile_SHA256":result["all_196_fit_profile_SHA256"],
        "decoder_profile_SHA256":result["all_144_decodings_SHA256"],
        "new_E2":0,"new_E3":0,"real_human_or_historical_data":False
    }
    write_json(ACCEPT,accept)
    print("R199_ACCEPTANCE",json.dumps(accept,sort_keys=True))
    print("R199_ALIAS_WORLDS",json.dumps(focus,sort_keys=True)[:6000])
    return result


def archive():
    names=[Path(__file__).name,RESULT.name,TRAIN.name,FITS.name,DECODE.name,ACCEPT.name]
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
    print("R199_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestFiniteHMMDecoding(unittest.TestCase):
    def test_six_models(self):self.assertEqual(len(MODELS),6)
    def test_twenty_four_worlds(self):self.assertEqual(len(list(worlds())),24)
    def test_all_2064_original_ordered_datasets(self):
        self.assertEqual(sum((2**L)**m for s,L,m in worlds()),2064)
    def test_196_complete_fitted_profiles(self):self.assertEqual(len(fit_library()),196)
    def test_144_visible_decoder_profiles(self):
        self.assertEqual(len(MODELS)*sum(2**L for L in LENGTHS),144)
    def test_all_params_strict_interior(self):
        self.assertTrue(all(0<a<1 and 0<r<1 for a,r in PARAMETERS.values()))
    def test_all_observed_PMFS_two_independent_algorithms(self):
        for s in MODELS:
            for L in LENGTHS:
                visible=observable_pmf(s,L)
                self.assertEqual(sum(visible,F(0)),1)
    def test_all_hidden_path_joint_marginalization(self):
        for s in MODELS:
            for L in LENGTHS:
                for obs in binary_paths(L):
                    self.assertEqual(sum((joint_hidden_observed(s,obs,h)
                                          for h in binary_paths(L)),F(0)),
                                     alpha_beta(s,obs)[2])
    def test_all_observation_PMFS_positive(self):
        for s in MODELS:
            for L in LENGTHS:self.assertTrue(all(x>0 for x in observable_pmf(s,L)))
    def test_smoothing_full_hidden_bruteforce_all(self):
        for s in MODELS:
            for L in LENGTHS:
                for obs in binary_paths(L):
                    smoothed_class1(s,obs)
    def test_every_smoothed_hidden_posterior_inside_unit_interval(self):
        for s in MODELS:
            for L in LENGTHS:
                for obs in binary_paths(L):
                    self.assertTrue(all(0<=x<=1 for x in smoothed_class1(s,obs)))
    def test_every_Viterbi_exact_brute_hidden_path(self):
        for s in MODELS:
            for L in LENGTHS:
                for obs in binary_paths(L):
                    viterbi_best_path(s,obs)
    def test_Viterbi_path_exactly_L_binary(self):
        for s in MODELS:
            for L in LENGTHS:
                for obs in binary_paths(L):
                    path,weight=viterbi_best_path(s,obs)
                    self.assertEqual(len(path),L)
                    self.assertTrue(all(x in (0,1) for x in path))
    def test_posterior_decoder_token_tie_rule(self):
        for s in MODELS:
            for obs in binary_paths(3):
                post,vpath,token,score=decode(s,obs)
                self.assertEqual(token,tuple(int(p>F(1,2)) for p in post))
    def test_label_swap_full_visible_alias_L3_L4(self):
        for L in LENGTHS:
            self.assertEqual(observable_pmf("BASE",L),observable_pmf("LABEL_SWAPPED",L))
    def test_label_swap_complete_hidden_joint(self):
        for L in LENGTHS:
            for obs in binary_paths(L):
                for h in binary_paths(L):
                    flipped=tuple(1-x for x in h)
                    self.assertEqual(joint_hidden_observed("BASE",obs,h),
                                     joint_hidden_observed("LABEL_SWAPPED",obs,flipped))
    def test_label_swap_posterior_complements(self):
        for L in LENGTHS:
            for obs in binary_paths(L):
                a=smoothed_class1("BASE",obs)
                b=smoothed_class1("LABEL_SWAPPED",obs)
                self.assertTrue(all(x+y==1 for x,y in zip(a,b)))
    def test_IID_hidden_emissions_generate_fair_independent_visible(self):
        for L in LENGTHS:self.assertEqual(observable_pmf("IID_HIDDEN",L),(F(1,2**L),)*(2**L))
    def test_persistent_HMM_observation_not_IID(self):
        for L in LENGTHS:self.assertNotEqual(observable_pmf("BASE",L),observable_pmf("IID_HIDDEN",L))
    def test_all_source_training_distributions_sum_one(self):
        for source,L,m in worlds():
            pmf=observable_pmf(source,L)
            self.assertEqual(sum((likelihood_raw(p,pmf)
                                  for p in product(range(2**L),repeat=m)),F(0)),1)
    def test_raw_vs_histogram_likelihood_all_training_samples(self):
        for L,m in product(LENGTHS,M_COUNTS):
            for xs in product(range(2**L),repeat=m):
                for candidate in MODELS:
                    pmf=observable_pmf(candidate,L)
                    self.assertEqual(likelihood_raw(xs,pmf),likelihood_hist(xs,pmf))
    def test_label_swap_equal_training_likelihood_all_profiles(self):
        for fit in fit_library().values():
            likes=fit["candidate_likelihoods"]
            self.assertEqual(likes["BASE"],likes["LABEL_SWAPPED"])
    def test_label_swapped_never_selected_in_tie(self):
        for fit in fit_library().values():
            self.assertNotEqual(fit["selected"],"LABEL_SWAPPED")
    def test_all_fit_profiles_have_positive_all_likelihoods(self):
        for fit in fit_library().values():
            self.assertTrue(all(x>0 for x in fit["candidate_likelihoods"].values()))
    def test_all_new_sequence_logloss_two_numeric_routes(self):
        for source in MODELS:
            for fit in MODELS:
                for L in LENGTHS:
                    metrics=heldout_metrics(source,fit,L)
                    self.assertAlmostEqual(metrics["new_complete_visible_logloss_float"],
                                           float(metrics["new_complete_visible_logloss_Decimal"]),places=12)
    def test_all_new_last_measurement_fraction_Brier_routes(self):
        for source in MODELS:
            for fit in MODELS:
                for L in LENGTHS:self.assertTrue(
                    heldout_metrics(source,fit,L)["two_independent_new_visible_Brier_routes"])
    def test_true_candidate_minimal_future_visible_logloss(self):
        for source in MODELS:
            for L in LENGTHS:
                best=heldout_metrics(source,source,L)["new_complete_visible_logloss_float"]
                for candidate in MODELS:
                    self.assertLessEqual(best,heldout_metrics(source,candidate,L)["new_complete_visible_logloss_float"]+1e-12)
    def test_true_candidate_minimal_future_last_Brier(self):
        for source in MODELS:
            for L in LENGTHS:
                best=heldout_metrics(source,source,L)["new_last_observation_brier_exact"]
                for candidate in MODELS:
                    self.assertLessEqual(best,heldout_metrics(source,candidate,L)["new_last_observation_brier_exact"])
    def test_true_marginal_posterior_token_optimality(self):
        for source in MODELS:
            for L in LENGTHS:
                m=heldout_metrics(source,source,L)
                self.assertGreaterEqual(
                    m["new_artificial_ORACLE_each_hidden_state_marginal_decoder_accuracy"],
                    m["new_artificial_ORACLE_each_hidden_state_Viterbi_decoder_accuracy"])
    def test_true_Viterbi_full_path_optimality(self):
        for source in MODELS:
            for L in LENGTHS:
                optimum=heldout_metrics(source,source,L)["new_artificial_ORACLE_full_hidden_path_accuracy"]
                for fit in MODELS:
                    self.assertGreaterEqual(optimum,heldout_metrics(source,fit,L)["new_artificial_ORACLE_full_hidden_path_accuracy"])
    def test_unknown_source_rejected(self):
        with self.assertRaises(ValueError):observable_pmf("INVALID",3)
    def test_invalid_sequence_length_rejected(self):
        with self.assertRaises(ValueError):observable_pmf("BASE",5)
    def test_nonbinary_hidden_state_rejected(self):
        with self.assertRaises(ValueError):joint_hidden_observed("BASE",(0,1,0),(0,2,0))
    def test_nonbinary_visible_state_rejected(self):
        with self.assertRaises(ValueError):joint_hidden_observed("BASE",(0,2,0),(0,1,0))
    def test_mismatched_hidden_length_rejected(self):
        with self.assertRaises(ValueError):joint_hidden_observed("BASE",(0,1,0),(0,1))
    def test_bad_fit_profile_unsorted_rejected(self):
        with self.assertRaises(ValueError):fit_profile(3,(7,1))
    def test_bad_fit_profile_length_rejected(self):
        with self.assertRaises(ValueError):fit_profile(3,(0,0,0))
    def test_bad_forecast_prefix_rejected(self):
        with self.assertRaises(ValueError):next_visible_one("BASE",(0,))
    def test_no_future_training_label_used_in_model_selection(self):
        for profile in fit_library().values():
            self.assertIn(profile["selected"],MODELS)
    def test_Bayes_path_probability_is_positive(self):
        for source in MODELS:
            for obs in binary_paths(3):
                path,score=viterbi_best_path(source,obs)
                self.assertGreater(score,0)


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("Usage --test or --run-and-archive")
