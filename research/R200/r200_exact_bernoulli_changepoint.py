"""R200: exact finite Bernoulli changepoint scan and heldout future risk.

Nine fixed constant, permanently shifted and one-period spike models
with 2^4/2^5 visible trajectories, m=1/2 independent training repeats:
36 source worlds, 11952 original ordered datasets, 712 complete fitted
observable profiles and 432 full source-weighted single-trajectory
scan records. No real observations, arbitrary continuous-rate MLE,
causal institutional rupture or externally evaluated historical signal.
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
PROTOCOL=HERE.parent.parent/"protocols/R200_CHANGEPOINT_36_WORLDS_11952_TRAINING_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R200_EXACT_RESULTS.json"
TRAIN=HERE/"R200_ALL_11952_ORDERED_TRAINING_DATASETS.csv"
FITS=HERE/"R200_ALL_712_EXACT_CHANGEPONT_FIT_PROFILES.json"
SCANS=HERE/"R200_ALL_432_SOURCE_WEIGHTED_SCAN_PROFILES.csv"
ACCEPT=HERE/"R200_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R200_Exact_36_Bernoulli_ChangePoint_Worlds.zip"

MODELS=("LOW","HIGH","MID","UP2","UP3","DOWN2","DOWN3","SPIKE2","SPIKE3")
ALTERNATIVES=("UP2","UP3","DOWN2","DOWN3")
L=F(1,4)
H=F(3,4)
U=F(1,2)
TS=(4,5)
M_COUNTS=(1,2)
THRESHOLD=F(4)


def validate(model,T):
    if model not in MODELS or T not in TS:
        raise ValueError("Outside frozen Bernoulli changepoint source")


def p_at(model,t):
    if model not in MODELS or not isinstance(t,int) or t<1:
        raise ValueError("Unknown model or observation time")
    if model=="LOW":return L
    if model=="HIGH":return H
    if model=="MID":return U
    if model.startswith("UP"):
        tau=int(model[-1])
        return L if t<tau else H
    if model.startswith("DOWN"):
        tau=int(model[-1])
        return H if t<tau else L
    if model.startswith("SPIKE"):
        tau=int(model[-1])
        return H if t==tau else L
    raise AssertionError("Unknown original candidate")


@lru_cache(maxsize=None)
def paths(T):
    if T not in TS:raise ValueError("Wrong observation history horizon")
    return tuple(product((0,1),repeat=T))


def likelihood_per_period(model,seq):
    """A: full exact time-aligned original Bernoulli likelihood product."""
    if model not in MODELS or len(seq) not in TS or any(x not in (0,1) for x in seq):
        raise ValueError("Wrong Bernoulli source/observed sequence")
    prob=F(1)
    for t,y in enumerate(seq,1):
        p=p_at(model,t)
        prob*=p if y else 1-p
    return prob


def likelihood_grouped_by_rate_and_observation(model,seq):
    """B: independent aggregation of counts by (emission probability, event)."""
    if model not in MODELS or len(seq) not in TS or any(x not in (0,1) for x in seq):
        raise ValueError("Wrong grouped observation source")
    groups=Counter((p_at(model,t),y) for t,y in enumerate(seq,1))
    product_mass=F(1)
    for (p,y),n in groups.items():
        product_mass*=(p if y else 1-p)**n
    return product_mass


@lru_cache(maxsize=None)
def pmf(model,T):
    validate(model,T)
    probs=tuple(likelihood_per_period(model,x) for x in paths(T))
    other=tuple(likelihood_grouped_by_rate_and_observation(model,x) for x in paths(T))
    if probs!=other or sum(probs,F(0))!=1 or any(x<=0 for x in probs):
        raise AssertionError("Two complete full Bernoulli trajectory source PMFs disagree")
    return probs


def training_raw(dataset,prob):
    out=F(1)
    for i in dataset:out*=prob[i]
    return out


def training_hist(dataset,prob):
    out=F(1)
    for i,count in Counter(dataset).items():out*=prob[i]**count
    return out


def fit_profile(T,profile):
    if (T not in TS or len(profile) not in M_COUNTS or
        tuple(profile)!=tuple(sorted(profile)) or
        any(x not in range(2**T) for x in profile)):
        raise ValueError("Bad original complete Bernoulli training fit profile")
    likes={}
    for candidate in MODELS:
        cand_pmf=pmf(candidate,T)
        a=training_raw(profile,cand_pmf)
        b=training_hist(profile,cand_pmf)
        if a!=b:raise AssertionError("Two source joint training likelihood methods differ")
        likes[candidate]=a
    maximum=max(likes.values())
    winner=next(k for k in MODELS if likes[k]==maximum)
    return {"T":T,"m":len(profile),"profile":profile,
            "complete_fixed_candidate_likelihoods":likes,
            "selected_model":winner}


@lru_cache(maxsize=None)
def fit_library():
    all_fit={}
    for T,m in product(TS,M_COUNTS):
        for profile in combinations_with_replacement(range(2**T),m):
            all_fit[(T,profile)]=fit_profile(T,profile)
    if len(all_fit)!=712:
        raise AssertionError("Frozen 712 unique fitted observation profiles missing")
    return all_fit


@lru_cache(maxsize=None)
def future_score(source,selected,T):
    validate(source,T)
    validate(selected,T)
    true_p=p_at(source,T+1)
    estimate=p_at(selected,T+1)
    brier=true_p*(1-estimate)**2+(1-true_p)*estimate**2
    bias_variance=true_p*(1-true_p)+(estimate-true_p)**2
    if brier!=bias_variance:
        raise AssertionError("Original new Bernoulli outcome expectation differs from analytic risk")
    logloss=-(float(true_p)*log(float(estimate))+
              float(1-true_p)*log(float(1-estimate)))
    with localcontext() as ctx:
        ctx.prec=70
        D=lambda q: Decimal(q.numerator)/Decimal(q.denominator)
        decimal_logloss=-(D(true_p)*D(estimate).ln()+
                         D(1-true_p)*D(1-estimate).ln())
    if abs(logloss-float(decimal_logloss))>1e-12:
        raise AssertionError("Independent Python and Decimal predictive logloss differ")
    if brier<true_p*(1-true_p):
        raise AssertionError("A fixed wrong model beat the actual oracle next-time risk")
    return brier,logloss,decimal_logloss


@lru_cache(maxsize=None)
def scan_ratios(T,seq):
    if T not in TS or len(seq)!=T:
        raise ValueError("Invalid original scan history")
    null=likelihood_per_period("MID",seq)
    alts={name:likelihood_per_period(name,seq)/null for name in ALTERNATIVES}
    best=max(alts.values())
    return alts,best,alts["UP2"]


def scan_source(source,T,rows):
    truth=pmf(source,T)
    mass=F(0);event=F(0);single_event=F(0)
    for observations,weight in zip(paths(T),truth):
        ratios,best,single=scan_ratios(T,observations)
        alarm=int(best>=THRESHOLD)
        single_alarm=int(single>=THRESHOLD)
        event+=weight*alarm
        single_event+=weight*single_alarm
        mass+=weight
        rows.append({
            "original_source":source,"T_observations":T,
            "visible_binary_sequence":"".join(map(str,observations)),
            "true_original_sequence_probability":str(weight),
            **{f"model_{name}_vs_MID_exact_likelihood_ratio":str(v) for name,v in ratios.items()},
            "scan_max_likelihood_ratio_vs_MID":str(best),
            "single_UP2_likelihood_ratio_vs_MID":str(single),
            "scan_alarm_LR_at_least_four":alarm,
            "single_UP2_alarm_LR_at_least_four":single_alarm
        })
    if mass!=1 or event<single_event:
        raise AssertionError("Scanning more alternatives cannot trigger fewer alarms")
    return {
        "source":source,"T":T,
        "full_original_visible_sequences":2**T,
        "threshold_at_least":str(THRESHOLD),
        "scan_alternatives":list(ALTERNATIVES),
        "full_scan_alarm_probability_exact":str(event),
        "single_preselected_UP2_alarm_probability_exact":str(single_event),
        "full_source_mass_one":True
    }


def evaluate_world(source,T,m,all_training):
    validate(source,T)
    if m not in M_COUNTS:
        raise ValueError("Frozen independent training session count must be 1 or 2")
    original=pmf(source,T)
    mass=F(0)
    selected_mass={name:F(0) for name in MODELS}
    true_future_brier=F(0)
    future_logloss=0.0
    future_logloss_high=Decimal(0)
    count=0
    for seq_indices in product(range(2**T),repeat=m):
        prob=training_raw(seq_indices,original)
        fitted=fit_library()[(T,tuple(sorted(seq_indices)))]
        chosen=fitted["selected_model"]
        brier,logloss,dlogloss=future_score(source,chosen,T)
        count+=1
        mass+=prob
        selected_mass[chosen]+=prob
        true_future_brier+=prob*brier
        future_logloss+=float(prob)*logloss
        with localcontext() as ctx:
            ctx.prec=70
            future_logloss_high+=(
                (Decimal(prob.numerator)/Decimal(prob.denominator))*dlogloss)
        all_training.append({
            "true_source_mechanism":source,"training_T":T,
            "independent_training_replicates_m":m,
            "ordered_original_visible_trajectory_indices":",".join(map(str,seq_indices)),
            "ordered_original_binary_observation_trajectories":";".join(
                "".join(map(str,paths(T)[i])) for i in seq_indices),
            "source_joint_training_probability_exact":str(prob),
            "sorted_complete_likelihood_profile":",".join(map(str,sorted(seq_indices))),
            **{f"model_{model}_train_likelihood_exact":str(fitted["complete_fixed_candidate_likelihoods"][model])
               for model in MODELS},
            "selected_visible_training_model":chosen,
            "true_NEXT_time_independent_event_probability":str(p_at(source,T+1)),
            "candidate_NEXT_time_forecast_probability":str(p_at(chosen,T+1)),
            "candidate_TRUE_independent_next_Brier":str(brier),
            "candidate_TRUE_independent_next_logloss":format(logloss,".16g"),
        })
    if mass!=1 or sum(selected_mass.values(),F(0))!=1 or count!=(2**T)**m:
        raise AssertionError("Full original ordered training data source not normalized")
    if abs(future_logloss-float(future_logloss_high))>1e-12:
        raise AssertionError("Full training weighted independent logloss numeric audit failed")
    optimal=future_score(source,source,T)[0]
    if true_future_brier<optimal:
        raise AssertionError("Fitting on observed training beat source-known conditional oracle")
    return {
        "true_source":source,"training_T":T,"m_independent_training_replicates":m,
        "full_ordered_original_training_dataset_count":count,
        "next_independent_replication_true_event_probability":str(p_at(source,T+1)),
        "all_nine_model_selection_probabilities":{k:str(v) for k,v in selected_mass.items()},
        "true_source_model_selected_probability":str(selected_mass[source]),
        "pretrained_selected_model_independent_NEXT_Brier_exact":str(true_future_brier),
        "fixed_MID_independent_NEXT_Brier_exact":str(future_score(source,"MID",T)[0]),
        "source_known_oracle_independent_NEXT_Brier_exact":str(optimal),
        "pretrained_selected_model_excess_Brier_above_oracle_exact":str(true_future_brier-optimal),
        "pretrained_selected_model_independent_NEXT_logloss_float":format(future_logloss,".16g"),
        "all_original_training_likelihood_and_new_test_oracle_identity_exact":True,
    }


def write_json(path,obj):
    path.write_text(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def run():
    training=[]
    world_results=[evaluate_world(s,T,m,training) for s,T,m in product(MODELS,TS,M_COUNTS)]
    if len(world_results)!=36 or len(training)!=11952:
        raise AssertionError("Original frozen 36-world 11952-training universe changed")
    scanrows=[]
    scanned=[scan_source(s,T,scanrows) for s,T in product(MODELS,TS)]
    if len(scanned)!=18 or len(scanrows)!=432:
        raise AssertionError("18 source scan evaluations or 432 raw scan records missing")
    for T in TS:
        # Exactly identical *first two time positions* under an impulse and a persistent shift.
        for first_two in product((0,1),repeat=2):
            a=F(1)
            b=F(1)
            for t,y in enumerate(first_two,1):
                p1=p_at("UP2",t);p2=p_at("SPIKE2",t)
                a*=p1 if y else 1-p1
                b*=p2 if y else 1-p2
            if a!=b:
                raise AssertionError("Frozen first-two-observations impulse/change alias failed")
        if p_at("UP2",T+1)!=H or p_at("SPIKE2",T+1)!=L:
            raise AssertionError("Persistent permanent change vs single anomalous pulse invalid")
    middles=[x for x in scanned if x["source"]=="MID"]
    if len(middles)!=2 or any(F(x["full_scan_alarm_probability_exact"])<=0 for x in middles):
        raise AssertionError("Original MID must exhibit positive exact finite-sample scan false alarm")
    with TRAIN.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(training[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(training)
    with SCANS.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(scanrows[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(scanrows)
    profile_library={
        "research_id":"R200","unique_exact_complete_fit_profiles":len(fit_library()),
        "model_tie_priority":list(MODELS),
        "profiles":[{
            "T":T,"m":len(seq),
            "sorted_complete_observable_trajectory_indices":list(seq),
            "fitted_max_visible_likelihood_candidate":fit["selected_model"],
            "all_nine_exact_training_candidate_likelihoods":{
                k:str(v) for k,v in fit["complete_fixed_candidate_likelihoods"].items()},
            "raw_sequence_product_vs_Counter_source_Fraction_equal":True
        } for (T,seq),fit in sorted(fit_library().items())]
    }
    write_json(FITS,profile_library)
    focus=[x for x in world_results if x["true_source"] in ("MID","LOW","UP2","SPIKE2")]
    result={
        "research_id":"R200",
        "status":"E1_ARTIFICIAL_EXACT_BERNOULLI_PERMANENT_SHIFT_VS_SINGLE_OUTLIER",
        "complete_source_worlds":36,"full_ordered_original_training_datasets":11952,
        "unique_exact_training_fit_profiles":712,
        "complete_source_weighted_single_sequence_scan_records":432,
        "separate_source_T_scan_worlds":18,
        "likelihood_from_independent_time_Bernoulli_vs_grouped_count_exact":True,
        "multi_replicate_training_likelihood_product_vs_Counter_Fraction_exact":True,
        "new_independent_future_Brier_vs_oracle_bias_variance_Fraction_equal":True,
        "new_independent_future_logloss_math_vs_Decimal_agree":True,
        "UP2_vs_SPIKE2_first_two_visible_observations_identical_but_future_differs":True,
        "scan_multiple_alternatives_false_alarm_at_MID_is_at_least_single_alternative":True,
        "full_original_single_sequence_scan_results":scanned,
        "frozen_no_shift_permanent_shift_and_spike_contrasts":focus,
        "all_full_source_worlds":world_results,
        "all_ordered_original_training_CSV_sha256":sha256(TRAIN.read_bytes()).hexdigest(),
        "all_exact_fit_profiles_SHA256":sha256(FITS.read_bytes()).hexdigest(),
        "all_source_weighted_scan_records_SHA256":sha256(SCANS.read_bytes()).hexdigest(),
        "new_E2":0,"new_E3":0,"real_human_or_historical_data":False
    }
    write_json(RESULT,result)
    accept={
        "research_id":"R200","status":"CLOSED_BOUNDED_E1_ARTIFICIAL_BERNOULLI_CHANGEPOINT",
        "worlds":36,"original_ordered_training_datasets":11952,
        "unique_complete_observable_fit_profiles":712,
        "source_weighted_exact_scan_records":432,
        "complete_two_source_observable_and_training_likelihoods_Fraction_equal":True,
        "exact_fixed_mid_null_false_alarm_and_shift_vs_spike_contrast":True,
        "true_independent_next_event_Brier_and_Decimal_logloss_double_verified":True,
        "complete_result_SHA256":sha256(RESULT.read_bytes()).hexdigest(),
        "original_source_training_CSV_SHA256":result["all_ordered_original_training_CSV_sha256"],
        "fitted_profiles_SHA256":result["all_exact_fit_profiles_SHA256"],
        "scan_original_CSV_SHA256":result["all_source_weighted_scan_records_SHA256"],
        "new_E2":0,"new_E3":0,"real_human_or_historical_data":False
    }
    write_json(ACCEPT,accept)
    print("R200_ACCEPTANCE",json.dumps(accept,sort_keys=True))
    print("R200_NULL_SCAN",json.dumps(middles,sort_keys=True))
    return result


def archive():
    names=[Path(__file__).name,RESULT.name,TRAIN.name,FITS.name,SCANS.name,ACCEPT.name]
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
    print("R200_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestExactChangePoint(unittest.TestCase):
    def test_nine_fixed_models(self):self.assertEqual(len(MODELS),9)
    def test_36_worlds(self):self.assertEqual(len(list(product(MODELS,TS,M_COUNTS))),36)
    def test_11952_source_training_sets(self):
        self.assertEqual(len(MODELS)*sum((2**T)+(2**T)**2 for T in TS),11952)
    def test_712_unique_profiles(self):self.assertEqual(len(fit_library()),712)
    def test_432_original_single_sequence_scans(self):
        self.assertEqual(len(MODELS)*sum(2**T for T in TS),432)
    def test_all_original_source_PMFS_normalize(self):
        for s in MODELS:
            for T in TS:self.assertEqual(sum(pmf(s,T),F(0)),1)
    def test_all_full_source_PMF_strict_positive(self):
        for s in MODELS:
            for T in TS:self.assertTrue(all(p>0 for p in pmf(s,T)))
    def test_two_complete_probability_methods_all_source_paths(self):
        for s in MODELS:
            for T in TS:
                for y in paths(T):
                    self.assertEqual(likelihood_per_period(s,y),
                                     likelihood_grouped_by_rate_and_observation(s,y))
    def test_original_time_specific_probabilities(self):
        self.assertEqual(tuple(p_at("UP2",t) for t in range(1,6)),(L,H,H,H,H))
        self.assertEqual(tuple(p_at("SPIKE2",t) for t in range(1,6)),(L,H,L,L,L))
    def test_downward_shift_remains_low_after_change(self):
        self.assertEqual(tuple(p_at("DOWN3",t) for t in range(1,6)),(H,H,L,L,L))
    def test_mid_null_every_step_half(self):
        self.assertTrue(all(p_at("MID",t)==U for t in range(1,7)))
    def test_up2_spike2_first_two_events_same(self):
        self.assertEqual(tuple(p_at("UP2",t) for t in (1,2)),
                         tuple(p_at("SPIKE2",t) for t in (1,2)))
    def test_up2_spike2_true_future_p_different(self):
        for T in TS:self.assertNotEqual(p_at("UP2",T+1),p_at("SPIKE2",T+1))
    def test_shift_versus_spike_pmf_diverge_at_T4(self):
        self.assertNotEqual(pmf("UP2",4),pmf("SPIKE2",4))
    def test_all_full_train_source_probabilities_normalize(self):
        for s,T,m in product(MODELS,TS,M_COUNTS):
            p=pmf(s,T)
            self.assertEqual(sum((training_raw(x,p) for x in product(range(2**T),repeat=m)),F(0)),1)
    def test_all_raw_training_vs_histogram_likelihoods(self):
        for T,m in product(TS,M_COUNTS):
            for x in product(range(2**T),repeat=m):
                for s in MODELS:
                    p=pmf(s,T)
                    self.assertEqual(training_raw(x,p),training_hist(x,p))
    def test_likelihood_all_profiles_positive(self):
        for fit in fit_library().values():
            self.assertTrue(all(v>0 for v in fit["complete_fixed_candidate_likelihoods"].values()))
    def test_fixed_lexicographic_tie_order_LOW_first(self):
        self.assertEqual(MODELS[0],"LOW")
    def test_nested_single_vs_scan_ratio(self):
        for T in TS:
            for path in paths(T):
                ratios,multi,single=scan_ratios(T,path)
                self.assertGreaterEqual(multi,single)
    def test_all_source_scans_finite_and_exact(self):
        for s in MODELS:
            for T in TS:
                x=scan_source(s,T,[])
                self.assertGreaterEqual(F(x["full_scan_alarm_probability_exact"]),
                                        F(x["single_preselected_UP2_alarm_probability_exact"]))
    def test_nonzero_MID_false_scan_alarms(self):
        for T in TS:self.assertGreater(F(scan_source("MID",T,[])["full_scan_alarm_probability_exact"]),0)
    def test_scan_alarm_threshold_is_four_inclusive(self):
        self.assertEqual(THRESHOLD,4)
    def test_full_Brier_bias_variance_all_true_future_pairs(self):
        for s in MODELS:
            for selected in MODELS:
                for T in TS:
                    b,fl,d=future_score(s,selected,T)
                    pt=p_at(s,T+1);pred=p_at(selected,T+1)
                    self.assertEqual(b,pt*(1-pt)+(pt-pred)**2)
    def test_math_vs_Decimal_logloss_all_candidates(self):
        for s in MODELS:
            for selected in MODELS:
                for T in TS:
                    b,fl,d=future_score(s,selected,T)
                    self.assertAlmostEqual(fl,float(d),places=12)
    def test_known_true_future_baseline_always_Brier_optimal(self):
        for s in MODELS:
            for selected in MODELS:
                for T in TS:
                    self.assertLessEqual(future_score(s,s,T)[0],future_score(s,selected,T)[0])
    def test_null_mid_is_Brier_quarter(self):
        for T in TS:self.assertEqual(future_score("MID","MID",T)[0],F(1,4))
    def test_unnecessary_change_model_can_hurt_mid_future(self):
        for T in TS:
            self.assertGreater(future_score("MID","UP2",T)[0],future_score("MID","MID",T)[0])
    def test_up2_future_forecast_good_SPIKE2_bad(self):
        for T in TS:
            self.assertEqual(future_score("UP2","UP2",T)[0],F(3,16))
            self.assertGreater(future_score("UP2","SPIKE2",T)[0],F(3,16))
    def test_SPIKE2_future_forecast_good_UP2_bad(self):
        for T in TS:
            self.assertEqual(future_score("SPIKE2","SPIKE2",T)[0],F(3,16))
            self.assertGreater(future_score("SPIKE2","UP2",T)[0],F(3,16))
    def test_all_models_future_next_rate_finite(self):
        for s in MODELS:
            for T in TS:self.assertTrue(0<p_at(s,T+1)<1)
    def test_wrong_model_rejected(self):
        with self.assertRaises(ValueError):p_at("OTHER",2)
    def test_negative_time_rejected(self):
        with self.assertRaises(ValueError):p_at("UP2",0)
    def test_wrong_training_horizon_rejected(self):
        with self.assertRaises(ValueError):pmf("LOW",6)
    def test_nonbinary_observed_rejected(self):
        with self.assertRaises(ValueError):likelihood_per_period("MID",(0,1,2,1))
    def test_bad_fit_profile_unsorted_rejected(self):
        with self.assertRaises(ValueError):fit_profile(4,(10,1))
    def test_bad_fit_profile_size_rejected(self):
        with self.assertRaises(ValueError):fit_profile(4,(1,1,1))
    def test_bad_scan_history_rejected(self):
        with self.assertRaises(ValueError):scan_ratios(4,(0,1))
    def test_bad_independent_train_count_rejected(self):
        with self.assertRaises(ValueError):evaluate_world("MID",4,3,[])
    def test_correct_true_rate_source_is_predeclared(self):
        for s in MODELS:
            for T in TS:
                for fit in MODELS:
                    self.assertIn(future_score(s,fit,T)[0],(F(3,16),F(1,4),F(7,16),F(5,16)))


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("Usage --test or --run-and-archive")
