"""R191 exact finite random-intercept prediction, BLUP versus Bayes.

The U prior has two equally likely labeled states (-tau,+tau); repeated
within-cluster errors have a symmetric three-point non-Gaussian distribution.
All oracle variance components are known from design, not estimated.
Two independent posterior-likelihood algorithms and exact independent
heldout risk calculations verify 24 worlds / 1440 latent training paths.
"""
from __future__ import annotations

from collections import Counter,defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import csv,json,sys,unittest,zipfile

HERE=Path(__file__).resolve().parent
PROTO=HERE.parent.parent/"protocols/R191_MIXED_EFFECTS_24_WORLDS_1440_PATHS_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R191_EXACT_RESULTS.json"
RAW=HERE/"R191_ALL_1440_LATENT_TRAINING_PATHS.csv"
PROFILES=HERE/"R191_ALL_OBSERVABLE_POSTERIOR_PROFILES.json"
ACCEPT=HERE/"R191_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R191_Exact_24_Mixed_Effect_Worlds.zip"
TAUS=(F(0),F(1,2),F(1))
SIGMAS=(F(1,2),F(1))
N_VALUES=(1,2,3,4)
ERROR_LABELS=(-1,0,1)
ERROR_PROBS=(F(1,4),F(1,2),F(1,4))
PREDICTORS=("GLOBAL","RAW_GROUP_MEAN","LINEAR_BLUP","EXACT_DISCRETE_POSTERIOR")


def worlds():
    for tau,sigma,n in product(TAUS,SIGMAS,N_VALUES):
        yield tau,sigma,n


def validate(tau,sigma,n):
    if tau not in TAUS or sigma not in SIGMAS or n not in N_VALUES:
        raise ValueError("source parameter outside frozen R191 grid")


def latent_states(tau):
    return (-tau,tau)


def noise_law(sigma):
    return {-2*sigma:F(1,4),F(0):F(1,2),2*sigma:F(1,4)}


def labeled_source_paths(tau,sigma,n):
    validate(tau,sigma,n)
    noise=(-2*sigma,F(0),2*sigma)
    for latent_label,u in enumerate(latent_states(tau)):
        for error_indices in product(range(3),repeat=n):
            errors=tuple(noise[i] for i in error_indices)
            observations=tuple(u+eps for eps in errors)
            probability=F(1,2)
            for i in error_indices:
                probability*=ERROR_PROBS[i]
            yield latent_label,u,error_indices,observations,probability


def likelihood_sequence(observed,u,noise_pmf):
    """Posterior evidence path A: multiply source event probabilities in order."""
    value=F(1)
    for y in observed:
        value*=noise_pmf.get(y-u,F(0))
    return value


def likelihood_histogram(observed,u,noise_pmf):
    """Posterior evidence path B: collapse order to full observed-value counts."""
    value=F(1)
    for y,c in Counter(observed).items():
        value*=noise_pmf.get(y-u,F(0))**c
    return value


def posterior(observed,tau,sigma):
    if not observed or len(observed) not in N_VALUES:
        raise ValueError("unsupported observed group length")
    noise_pmf=noise_law(sigma)
    values=latent_states(tau)
    likelihoods=tuple(likelihood_sequence(observed,u,noise_pmf) for u in values)
    hist=tuple(likelihood_histogram(observed,u,noise_pmf) for u in values)
    if likelihoods!=hist:
        raise AssertionError("posterior raw-sequence and histogram paths differ")
    denominator=(likelihoods[0]+likelihoods[1])/2
    if denominator<=0:
        raise ValueError("off-source impossible observed group sequence")
    estimate=(values[0]*likelihoods[0]+values[1]*likelihoods[1])/(likelihoods[0]+likelihoods[1])
    if estimate < -tau or estimate >tau:
        raise AssertionError("posterior must lie in latent support convex hull")
    return estimate,denominator,likelihoods


def group_mean(observed):
    if not observed:
        raise ValueError("no repeated measures")
    return sum(observed,F(0))/len(observed)


def blup_coefficient(tau,sigma,n):
    validate(tau,sigma,n)
    tau2=tau*tau
    error_variance=2*sigma*sigma
    return tau2/(tau2+error_variance/F(n))


def predictor_values(observed,tau,sigma):
    n=len(observed)
    validate(tau,sigma,n)
    mean=group_mean(observed)
    post,p_obs,likelihoods=posterior(observed,tau,sigma)
    return {
        "GLOBAL":F(0),
        "RAW_GROUP_MEAN":mean,
        "LINEAR_BLUP":blup_coefficient(tau,sigma,n)*mean,
        "EXACT_DISCRETE_POSTERIOR":post,
    }


def independent_risk_formula(tau,sigma,n,post_second,blup_second):
    """Independent second-moment identities, no latent training paths."""
    tau2=tau*tau
    v=2*sigma*sigma
    return {
        "GLOBAL":tau2+v,
        "RAW_GROUP_MEAN":v+v/F(n),
        "LINEAR_BLUP":v+(tau2*v)/(F(n)*tau2+v),
        "EXACT_DISCRETE_POSTERIOR":v+tau2-post_second,
        "NEW_GROUP_GLOBAL":tau2+v,
        "NEW_GROUP_INCORRECTLY_REUSE_OLD_BLUP":tau2+v+blup_second
    }


def analyze_world(tau,sigma,n,raw_records,posterior_profiles):
    latent_total=F(0)
    empirical={model:F(0) for model in PREDICTORS}
    grouped_original_probability=defaultdict(F)
    visible={}

    for latent_label,u,indices,observed,weight in labeled_source_paths(tau,sigma,n):
        latent_total+=weight
        grouped_original_probability[observed]+=weight
        pred=predictor_values(observed,tau,sigma)
        posterior_pred=pred["EXACT_DISCRETE_POSTERIOR"]
        eps_var=2*sigma*sigma
        per_predictor={}
        for name,value in pred.items():
            independent_test_loss=eps_var+(u-value)**2
            empirical[name]+=weight*independent_test_loss
            per_predictor[name]=str(independent_test_loss)
        raw_records.append({
            "tau":str(tau),"sigma":str(sigma),"n":n,
            "latent_u_sign_label":latent_label,"actual_hidden_U":str(u),
            "primitive_error_indices":",".join(map(str,indices)),
            "observed_group_repeated_measurements":",".join(map(str,observed)),
            "source_exact_probability_of_labeled_latent_path":str(weight),
            "source_visible_observation_probability":str(posterior(observed,tau,sigma)[1]),
            **{name+"_estimate":str(value) for name,value in pred.items()},
            **{name+"_independent_NEW_same_group_test_MSE":v for name,v in per_predictor.items()},
        })
        if observed not in visible:
            visible[observed]=pred

    if latent_total!=1 or len(grouped_original_probability)>(2*3**n):
        raise AssertionError("original latent training source sample invalid")

    expected_post_square=F(0)
    expected_blup_square=F(0)
    for observations,probability in grouped_original_probability.items():
        estimate,evidence,posterior_lik=posterior(observations,tau,sigma)
        if evidence!=probability:
            raise AssertionError("original latent path enumeration does not match independent observation marginalization")
        pred=visible[observations]
        expected_post_square+=probability*estimate**2
        expected_blup_square+=probability*pred["LINEAR_BLUP"]**2
        posterior_profiles.append({
            "tau":str(tau),"sigma":str(sigma),"n":n,
            "observable_training_vector":[str(z) for z in observations],
            "true_training_observation_probability":str(probability),
            "posterior_hidden_U_minus_state_likelihood":str(posterior_lik[0]),
            "posterior_hidden_U_plus_state_likelihood":str(posterior_lik[1]),
            "posterior_expected_hidden_U":str(estimate),
            "oracle_LINEAR_BLUP":str(pred["LINEAR_BLUP"]),
            "posterior_exact_sequence_and_histogram_agree":True,
        })
    analytic=independent_risk_formula(tau,sigma,n,expected_post_square,expected_blup_square)
    for name in PREDICTORS:
        if empirical[name]!=analytic[name]:
            raise AssertionError("whole-world enumerated heldout risk and independent known-moment risk differ: "+name)
    if not (empirical["EXACT_DISCRETE_POSTERIOR"]<=empirical["LINEAR_BLUP"]
            <=empirical["RAW_GROUP_MEAN"] and
            empirical["LINEAR_BLUP"]<=empirical["GLOBAL"]):
        raise AssertionError("Bayes-optimal versus BLUP versus group mean bounded loss ordering invalid")
    if tau==0 and not(
            empirical["LINEAR_BLUP"]==empirical["EXACT_DISCRETE_POSTERIOR"]==empirical["GLOBAL"]):
        raise AssertionError("zero random intercept negative control failed")
    if tau>0 and not(analytic["NEW_GROUP_INCORRECTLY_REUSE_OLD_BLUP"]>analytic["NEW_GROUP_GLOBAL"]):
        raise AssertionError("reuse of old group BLUP must harm unseen group prediction")
    return {
        "tau":str(tau),"sigma":str(sigma),"n":n,
        "true_group_intercept_variance":str(tau*tau),
        "true_one_response_error_variance":str(2*sigma*sigma),
        "true_same_group_repeated_measure_covariance":str(tau*tau),
        "labeled_original_training_paths":2*3**n,
        "distinct_observable_training_vectors":len(grouped_original_probability),
        "oracle_linear_shrink_coefficient":str(blup_coefficient(tau,sigma,n)),
        "E_visible_posterior_squared_exact":str(expected_post_square),
        "E_visible_BLUP_squared_exact":str(expected_blup_square),
        "same_seen_group_independent_future_MSE":{key:str(empirical[key]) for key in PREDICTORS},
        "fully_new_group_correct_GLOBAL_future_MSE":str(analytic["NEW_GROUP_GLOBAL"]),
        "fully_new_group_incorrect_old_BLUP_future_MSE":str(analytic["NEW_GROUP_INCORRECTLY_REUSE_OLD_BLUP"]),
        "Bayes_minus_linear_BLUP_future_MSE":str(empirical["EXACT_DISCRETE_POSTERIOR"]-empirical["LINEAR_BLUP"]),
        "all_original_probability_and_independent_moment_risks_exact":True
    }


def run():
    raw=[]
    profiles=[]
    output=[analyze_world(tau,sigma,n,raw,profiles) for tau,sigma,n in worlds()]
    if len(output)!=24 or len(raw)!=1440:
        raise AssertionError("frozen full latent path universe count changed")
    origin_tauzero=[w for w in output if w["tau"]=="0"]
    if len(origin_tauzero)!=8:
        raise AssertionError("zero intercept source count unexpected")
    focus=[w for w in output if w["tau"]=="1/2" and w["sigma"]=="1/2" and w["n"] in (1,2)]
    if len(focus)!=2:
        raise AssertionError("prelocked discrete non-Gaussian posterior anchor absent")
    if not any(F(w["Bayes_minus_linear_BLUP_future_MSE"])<0 for w in focus):
        raise AssertionError("prelocked discrete latent posterior strictly beating linear projection absent")
    with RAW.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(raw[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(raw)
    PROFILES.write_text(json.dumps({
        "research_id":"R191","observable_profile_count":len(profiles),
        "all_posterior_marginalization_exact_two_methods":True,
        "profiles":profiles
    },sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    result={
        "research_id":"R191",
        "status":"E1_ARTIFICIAL_KNOWN_VARIANCE_DISCRETE_RANDOM_INTERCEPT",
        "world_count":24,"full_labeled_source_training_paths":1440,
        "unique_observable_posterior_profiles":len(profiles),
        "all_visible_observation_source_probabilities_two_routes_equal":True,
        "all_world_independent_future_seen_group_errors_exact_by_two_methods":True,
        "all_unseen_group_transfer_losses_exact":True,
        "all_true_Bayes_not_worse_than_linear_BLUP_and_mean":True,
        "frozen_no_random_effect_worlds":origin_tauzero,
        "frozen_nonGaussian_discrete_posterior_vs_linear_examples":focus,
        "worlds":output,
        "training_original_CSV_sha256":sha256(RAW.read_bytes()).hexdigest(),
        "posterior_profile_json_sha256":sha256(PROFILES.read_bytes()).hexdigest(),
        "real_human_or_historical_data":False,"new_E2":0,"new_E3":0
    }
    RESULT.write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    acceptance={
        "research_id":"R191",
        "status":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_MIXED_EFFECTS",
        "world_count":24,"full_source_labeled_training_paths":1440,
        "unique_visible_training_profiles":len(profiles),
        "source_two_independent_observation_PMF_paths_exact":True,
        "posterior_likelihood_raw_and_histogram_exact":True,
        "full_future_risk_enumeration_vs_analytic_Fraction_exact":True,
        "BLUP_best_linear_not_always_nonGaussian_Bayes":True,
        "new_group_is_not_a_seen_group_transfer_test":True,
        "result_sha256":sha256(RESULT.read_bytes()).hexdigest(),
        "source_training_CSV_sha256":result["training_original_CSV_sha256"],
        "posterior_profile_SHA256":result["posterior_profile_json_sha256"],
        "new_E2":0,"new_E3":0,"real_human_or_historical_data":False
    }
    ACCEPT.write_text(json.dumps(acceptance,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R191_ACCEPTANCE",json.dumps(acceptance,sort_keys=True))
    print("R191_FIXED_NON_GAUSSIAN_ANCHORS",json.dumps(focus,sort_keys=True))
    return result


def archive():
    files=[Path(__file__).name,RESULT.name,RAW.name,PROFILES.name,ACCEPT.name]
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
    print("R191_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestFiniteMixedEffects(unittest.TestCase):
    def test_24_worlds(self):
        self.assertEqual(len(list(worlds())),24)
    def test_1440_labeled_training_paths(self):
        self.assertEqual(sum(2*3**n for tau,sigma,n in worlds()),1440)
    def test_error_mass_exact(self):
        for s in SIGMAS:
            self.assertEqual(sum(noise_law(s).values(),F(0)),1)
    def test_error_moments_exact(self):
        for s in SIGMAS:
            law=noise_law(s)
            self.assertEqual(sum((e*p for e,p in law.items()),F(0)),0)
            self.assertEqual(sum((e*e*p for e,p in law.items()),F(0)),2*s*s)
    def test_source_probability_total_each_world(self):
        for tau,sigma,n in worlds():
            self.assertEqual(sum((row[-1] for row in labeled_source_paths(tau,sigma,n)),F(0)),1)
    def test_complete_events_two_latent_labels(self):
        for tau,sigma,n in worlds():
            labels=Counter(row[0] for row in labeled_source_paths(tau,sigma,n))
            self.assertEqual(labels[0],3**n)
            self.assertEqual(labels[1],3**n)
    def test_visible_marginal_two_source_routes(self):
        for tau,sigma,n in worlds():
            source=defaultdict(F)
            for label,u,index,obs,prob in labeled_source_paths(tau,sigma,n):
                source[obs]+=prob
            for observed,mass in source.items():
                self.assertEqual(mass,posterior(observed,tau,sigma)[1])
    def test_posterior_histogram_equals_sequence(self):
        for tau,sigma,n in worlds():
            for label,u,index,obs,prob in labeled_source_paths(tau,sigma,n):
                for v in latent_states(tau):
                    self.assertEqual(likelihood_sequence(obs,v,noise_law(sigma)),
                                     likelihood_histogram(obs,v,noise_law(sigma)))
    def test_all_posteriors_within_bounds(self):
        for tau,sigma,n in worlds():
            for label,u,index,obs,prob in labeled_source_paths(tau,sigma,n):
                self.assertTrue(-tau<=posterior(obs,tau,sigma)[0]<=tau)
    def test_global_prediction_zero(self):
        for tau,sigma,n in worlds():
            seq=next(labeled_source_paths(tau,sigma,n))[3]
            self.assertEqual(predictor_values(seq,tau,sigma)["GLOBAL"],0)
    def test_tauzero_BLUP_and_bayes_exact_zero(self):
        for sigma in SIGMAS:
            for n in N_VALUES:
                for label,u,index,obs,prob in labeled_source_paths(F(0),sigma,n):
                    p=predictor_values(obs,F(0),sigma)
                    self.assertEqual(p["LINEAR_BLUP"],0)
                    self.assertEqual(p["EXACT_DISCRETE_POSTERIOR"],0)
    def test_linear_shrink_between_zero_one(self):
        for tau,sigma,n in worlds():
            self.assertTrue(0<=blup_coefficient(tau,sigma,n)<1)
    def test_correct_model_risk_formula_normalization(self):
        for tau,sigma,n in worlds():
            v=2*sigma*sigma
            d=independent_risk_formula(tau,sigma,n,F(0),F(0))
            self.assertEqual(d["GLOBAL"],tau*tau+v)
            self.assertEqual(d["RAW_GROUP_MEAN"],v+v/n)
    def test_no_intercept_raw_overfits_independent_future(self):
        for sigma in SIGMAS:
            for n in N_VALUES:
                v=2*sigma*sigma
                r=independent_risk_formula(F(0),sigma,n,F(0),F(0))
                self.assertEqual(r["RAW_GROUP_MEAN"]-r["GLOBAL"],v/n)
    def test_true_strictly_positive_same_group_covariance(self):
        self.assertTrue(all(tau*tau>0 for tau in TAUS[1:]))
    def test_known_variance_blup_risk_formula(self):
        tau,sigma,n=F(1),F(1),2
        v=2*sigma*sigma
        self.assertEqual(independent_risk_formula(tau,sigma,n,F(0),F(0))["LINEAR_BLUP"],
                         v+tau*tau*v/(n*tau*tau+v))
    def test_all_world_exact_risks_and_prediction_ranking(self):
        for tau,sigma,n in worlds():
            rows=[];profiles=[]
            w=analyze_world(tau,sigma,n,rows,profiles)
            self.assertTrue(w["all_original_probability_and_independent_moment_risks_exact"])
            self.assertEqual(len(rows),2*3**n)
    def test_new_group_reused_blup_higher_for_nonzero_tau(self):
        for tau,sigma,n in worlds():
            if tau>0:
                w=analyze_world(tau,sigma,n,[],[])
                self.assertGreater(F(w["fully_new_group_incorrect_old_BLUP_future_MSE"]),
                                   F(w["fully_new_group_correct_GLOBAL_future_MSE"]))
    def test_prescored_tau_half_sigma_half_discrete_posterior(self):
        for n in (1,2):
            world=analyze_world(F(1,2),F(1,2),n,[],[])
            self.assertLess(F(world["Bayes_minus_linear_BLUP_future_MSE"]),0)
    def test_observable_posterior_exact_when_unique_to_U(self):
        p,_mass,_like=posterior((F(-3,2),),F(1,2),F(1,2))
        self.assertEqual(p,F(-1,2))
    def test_ambiguous_posterior_not_at_edge(self):
        p,_mass,_like=posterior((F(-1,2),),F(1,2),F(1,2))
        self.assertTrue(-F(1,2)<p<F(1,2))
    def test_mixed_error_group_mean(self):
        seq=(F(-1),F(1),F(2))
        self.assertEqual(group_mean(seq),F(2,3))
    def test_not_gaussian_Bayes_must_stay_in_latent_support(self):
        for tau,sigma,n in worlds():
            u=next(labeled_source_paths(tau,sigma,n))[3]
            estimate=posterior(u,tau,sigma)[0]
            self.assertTrue(-tau<=estimate<=tau)
    def test_off_source_observation_rejected(self):
        with self.assertRaises(ValueError):
            posterior((F(100),),F(1,2),F(1,2))
    def test_empty_training_group_rejected(self):
        with self.assertRaises(ValueError):
            group_mean(())
    def test_invalid_tau_rejected(self):
        with self.assertRaises(ValueError):
            blup_coefficient(F(1,3),F(1),2)
    def test_invalid_sigma_rejected(self):
        with self.assertRaises(ValueError):
            blup_coefficient(F(1),F(1,3),2)
    def test_invalid_repeat_count_rejected(self):
        with self.assertRaises(ValueError):
            blup_coefficient(F(1),F(1),5)
    def test_posterior_observation_marginal_positive(self):
        result=posterior((F(1),),F(1),F(1))
        self.assertGreater(result[1],0)
    def test_source_truth_hidden_U_is_exact(self):
        for tau,sigma,n in worlds():
            for label,u,index,obs,prob in labeled_source_paths(tau,sigma,n):
                self.assertEqual(u,latent_states(tau)[label])


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("Usage: --test or --run-and-archive")
