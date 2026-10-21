"""R197 fixed-parameter finite ARIMA mechanism and strictly future-innovation risk.

6 discrete time-series sources, T=4/5, h=1/2: 24 worlds, 1944
complete weighted training paths, 3888 source-horizon forecast profiles,
23328 full conditional candidate risks, all exact Fraction. The training
candidate is chosen ONLY with t=2..T prequential squared errors.
Not general ARIMA MLE and not real social or historical time series.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import csv,json,sys,unittest,zipfile

HERE=Path(__file__).resolve().parent
PROTO=HERE.parent.parent/"protocols/R197_ARIMA_24_WORLDS_1944_TRAINING_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R197_EXACT_RESULTS.json"
TRAIN=HERE/"R197_ALL_1944_ORDERED_TRAINING_PATHS.csv"
RISKS=HERE/"R197_ALL_3888_INDEPENDENT_HELDOUT_RISK_PROFILES.csv"
ACCEPT=HERE/"R197_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R197_Exact_24_Prequential_ARIMA_Worlds.zip"
SOURCES=("WHITE","AR1","RW","DRIFT","DIFF_AR1","DIFF_MA1")
T_VALUES=(4,5)
HORIZONS=(1,2)
NOISE=(-1,0,1)
NOISE_PROBS={-1:F(1,4),0:F(1,2),1:F(1,4)}
PHI=F(1,2)
THETA=F(1,2)
VAR_E=F(1,2)


def source_validate(source):
    if source not in SOURCES:
        raise ValueError("Source or candidate must be from the original frozen catalog")


def noise_mass(innovations):
    mass=F(1)
    for e in innovations:
        if e not in NOISE_PROBS:
            raise ValueError("Innovation outside frozen three point distribution")
        mass*=NOISE_PROBS[e]
    return mass


def trajectory(source,innovations):
    """Full original structural generator; y0=0 and eps0=0."""
    source_validate(source)
    original=tuple(innovations)
    noise_mass(original)
    y=[F(0)]
    for index,e in enumerate(original,1):
        e=F(e)
        if source=="WHITE":
            next_y=e
        elif source=="AR1":
            next_y=PHI*y[-1]+e
        elif source=="RW":
            next_y=y[-1]+e
        elif source=="DRIFT":
            next_y=y[-1]+1+e
        elif source=="DIFF_AR1":
            last_delta=y[-1]-y[-2] if index>=2 else F(0)
            next_y=y[-1]+PHI*last_delta+e
        elif source=="DIFF_MA1":
            earlier=F(original[index-2]) if index>=2 else F(0)
            next_y=y[-1]+e+THETA*earlier
        else:
            raise AssertionError("Unsupported original process")
        y.append(next_y)
    return tuple(y)


def history_validate(history,h):
    if h not in HORIZONS or len(history)<2 or history[0]!=0:
        raise ValueError("Forecast requires original y0 and at least one observed step")
    if any(not isinstance(value,F) for value in history):
        raise ValueError("Forecast state must be exact rational numbers")


def forecast(source,history,h):
    """Working forecast conditional only on visible y0..yT."""
    source_validate(source)
    history_validate(history,h)
    y=history[-1]
    if source=="WHITE":
        return F(0)
    if source=="AR1":
        return PHI**h*y
    if source=="RW":
        return y
    if source=="DRIFT":
        return y+h
    if source=="DIFF_AR1":
        d=history[-1]-history[-2]
        return y+sum((PHI**j*d for j in range(1,h+1)),F(0))
    # Work-model invertible MA innovation reconstruction via observed differences.
    past_e=F(0)
    for last,now in zip(history[:-1],history[1:]):
        past_e=(now-last)-THETA*past_e
    return y+THETA*past_e


def prequential_direct(history):
    """Training A: each next response predicted from STRICT prefix."""
    result={name:F(0) for name in SOURCES}
    for t in range(2,len(history)):
        seen=history[:t]
        true_next=history[t]
        for name in SOURCES:
            result[name]+=(true_next-forecast(name,seen,1))**2
    return result


def prequential_recursion(history):
    """Training B: independent online updates for each model's conditional state."""
    if len(history)<3:
        raise ValueError("Need at least two observed responses")
    scores={name:F(0) for name in SOURCES}
    # epsilon_1 under MA work model is y1-y0.
    ma_prev_error=history[1]-history[0]
    for t in range(2,len(history)):
        last=history[t-1]
        previous=history[t-2]
        d=last-previous
        predictions={
            "WHITE":F(0),
            "AR1":PHI*last,
            "RW":last,
            "DRIFT":last+F(1),
            "DIFF_AR1":last+PHI*d,
            "DIFF_MA1":last+THETA*ma_prev_error,
        }
        for model,pred in predictions.items():
            scores[model]+=(history[t]-pred)**2
        ma_prev_error=(history[t]-history[t-1])-THETA*ma_prev_error
    return scores


def training_fit(history):
    a=prequential_direct(history)
    b=prequential_recursion(history)
    if a!=b:
        raise AssertionError("Independent prequential prefix forecasts and direct online recursion differ")
    best=min(a.values())
    selected=next(name for name in SOURCES if a[name]==best)
    return selected,a


def oracle_truth(source,history,original_innovations,h):
    """Source-knowledge-only conditional mean and variance. NOT model selection."""
    source_validate(source)
    history_validate(history,h)
    if len(original_innovations)!=len(history)-1:
        raise ValueError("True latent innovations length does not match observed training")
    if trajectory(source,original_innovations)!=history:
        raise ValueError("Oracle innovations must reproduce complete training exactly")
    last=history[-1]
    if source=="WHITE":
        mu=F(0)
        var=VAR_E
    elif source=="AR1":
        mu=PHI**h*last
        var=VAR_E*sum((PHI**(2*j) for j in range(h)),F(0))
    elif source in ("RW","DRIFT"):
        mu=last+(h if source=="DRIFT" else 0)
        var=VAR_E*h
    elif source=="DIFF_AR1":
        delta=history[-1]-history[-2]
        mu=last+delta*sum((PHI**j for j in range(1,h+1)),F(0))
        coefficients=tuple(sum((PHI**j for j in range(h-l+1)),F(0)) for l in range(1,h+1))
        var=VAR_E*sum((c*c for c in coefficients),F(0))
    else:
        mu=last+THETA*F(original_innovations[-1])
        # at horizon 2, epsilon_(T+1) influences both new increments.
        var=VAR_E if h==1 else VAR_E*((1+THETA)**2+1)
    return mu,var


def conditional_test_risks(source,history,innovations,h):
    """Independent future-innovation enumeration versus analytic bias variance."""
    history_validate(history,h)
    mu,var=oracle_truth(source,history,innovations,h)
    fitted={name:forecast(name,history,h) for name in SOURCES}
    exact_sum={name:F(0) for name in SOURCES}
    future_mu=F(0)
    future_second=F(0)
    complete_mass=F(0)
    for future_eps in product(NOISE,repeat=h):
        weight=noise_mass(future_eps)
        actual=trajectory(source,tuple(innovations)+future_eps)[-1]
        complete_mass+=weight
        future_mu+=weight*actual
        future_second+=weight*actual**2
        for name,pred in fitted.items():
            exact_sum[name]+=weight*(actual-pred)**2
    if complete_mass!=1 or future_mu!=mu or future_second-mu*mu!=var:
        raise AssertionError("Original future innovations do not agree with independent analytic true mean/variance")
    analytic={name:var+(mu-pred)**2 for name,pred in fitted.items()}
    if analytic!=exact_sum or any(r<var for r in analytic.values()):
        raise AssertionError("Out-of-time all-candidate MSE differs from oracle bias+variance")
    if fitted[source]!=mu or analytic[source]!=var:
        raise AssertionError("True known source not oracle-optimal at this training history")
    return fitted,analytic,mu,var


def training_cases(source,T):
    source_validate(source)
    if T not in T_VALUES:
        raise ValueError("Frozen training length only 4 or 5")
    for innov in product(NOISE,repeat=T):
        yield innov,noise_mass(innov),trajectory(source,innov)


def full_world(source,T,h,all_risks,training_cache):
    source_validate(source)
    if T not in T_VALUES or h not in HORIZONS:
        raise ValueError("Frozen source world outside universe")
    total_mass=F(0)
    selected={name:F(0) for name in SOURCES}
    candidate_MSE={name:F(0) for name in SOURCES}
    selected_MSE=F(0)
    count=0
    for innov,weight,history,fit,scores in training_cache[(source,T)]:
        predicts,risk,mu,var=conditional_test_risks(source,history,innov,h)
        selected[fit]+=weight
        selected_MSE+=weight*risk[fit]
        total_mass+=weight
        count+=1
        for candidate in SOURCES:
            candidate_MSE[candidate]+=weight*risk[candidate]
        all_risks.append({
            "source":source,"training_time_steps_T":T,"future_horizon_h":h,
            "ordered_innovation_training_path":",".join(map(str,innov)),
            "visible_training_y0_to_yT":",".join(map(str,history)),
            "true_original_training_mass":str(weight),
            "selected_prequential_model":fit,
            "true_conditional_test_mean_oracle":str(mu),
            "true_conditional_test_variance_oracle":str(var),
            **{f"candidate_{name}_forecast":str(predicts[name]) for name in SOURCES},
            **{f"candidate_{name}_true_independent_future_MSE":str(risk[name]) for name in SOURCES},
            "fitted_model_true_independent_future_MSE":str(risk[fit]),
        })
    if total_mass!=1 or sum(selected.values(),F(0))!=1 or count!=3**T:
        raise AssertionError("Complete original training ensemble does not normalize")
    true_noise=oracle_truth(source,training_cache[(source,T)][0][2],
                            training_cache[(source,T)][0][0],h)[1]
    if candidate_MSE[source]!=true_noise or selected_MSE<true_noise:
        raise AssertionError("Oracle baseline or model-selection risk identity failed")
    return {
        "original_source":source,"training_T":T,"future_test_horizon_h":h,
        "complete_training_trajectories":count,
        "candidate_prequential_selection_probability":{m:str(v) for m,v in selected.items()},
        "true_source_chosen_probability":str(selected[source]),
        "selected_model_expected_independent_future_MSE":str(selected_MSE),
        "always_RW_expected_independent_future_MSE":str(candidate_MSE["RW"]),
        "oracle_true_source_expected_independent_future_MSE":str(true_noise),
        "selected_model_expected_excess_MSE_over_oracle":str(selected_MSE-true_noise),
        "all_fixed_candidates_expected_independent_future_MSE":{m:str(v) for m,v in candidate_MSE.items()},
        "all_source_forecast_moments_and_independent_future_enumeration_exact":True,
    }


def write_csv(path,rows):
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        w.writeheader();w.writerows(rows)


def write_json(path,data):
    path.write_text(json.dumps(data,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def run():
    train=[]
    cache={}
    for source,T in product(SOURCES,T_VALUES):
        out=[]
        msum=F(0)
        for innov,p,history in training_cases(source,T):
            fit,scores=training_fit(history)
            msum+=p
            out.append((innov,p,history,fit,scores))
            train.append({
                "original_source":source,"training_steps_T":T,
                "ordered_innovations":",".join(map(str,innov)),
                "exact_source_probability":str(p),
                "observed_y0_to_yT":",".join(map(str,history)),
                "fitted_prequential_candidate":fit,
                **{f"prequential_T2_to_T_squared_training_error_{model}":str(v) for model,v in scores.items()}
            })
        if msum!=1 or len(out)!=3**T:
            raise AssertionError("Complete source innovation enumeration changed")
        cache[(source,T)]=out
    all_risks=[]
    outputs=[full_world(source,T,h,all_risks,cache)
             for source,T,h in product(SOURCES,T_VALUES,HORIZONS)]
    if len(outputs)!=24 or len(train)!=1944 or len(all_risks)!=3888:
        raise AssertionError("Frozen source and evaluation universe mismatch")
    if 6*len(all_risks)!=23328:
        raise AssertionError("Six fixed model candidate future risk universe mismatch")
    oracle_vars={
        "WHITE":("1/2","1/2"),"AR1":("1/2","5/8"),
        "RW":("1/2","1"),"DRIFT":("1/2","1"),
        "DIFF_AR1":("1/2","13/8"),"DIFF_MA1":("1/2","13/8"),
    }
    for world in outputs:
        if world["oracle_true_source_expected_independent_future_MSE"] != oracle_vars[world["original_source"]][world["future_test_horizon_h"]-1]:
            raise AssertionError("Frozen six ARIMA source future oracle innovation variances drifted")
    write_csv(TRAIN,train)
    write_csv(RISKS,all_risks)
    fixed=[w for w in outputs if w["original_source"] in ("WHITE","AR1","RW","DIFF_AR1","DIFF_MA1") and w["future_test_horizon_h"]==2]
    result={
        "research_id":"R197",
        "state":"E1_ARTIFICIAL_FIXED_PARAMETER_DISCRETE_ARIMA_SQUARED_RISK",
        "frozen_candidate_processes":list(SOURCES),
        "worlds":24,"full_original_training_paths":1944,
        "raw_training_and_horizon_risk_profiles":3888,
        "full_independent_future_conditional_candidate_risks":23328,
        "source_probability_full_enumeration_exact":True,
        "two_independent_prefix_vs_online_prequential_squared_losses_Fraction_exact":True,
        "all_candidates_truly_heldout_new_innovations_vs_analytic_bias_variance_Fraction_exact":True,
        "all_future_oracle_risks_match_frozen_mechanism_variances":True,
        "true_model_not_chosen_with_future_test_information":True,
        "fixed_integrated_vs_stationary_dynamic_process_contrasts":fixed,
        "all_24_original_worlds":outputs,
        "training_source_CSV_sha256":sha256(TRAIN.read_bytes()).hexdigest(),
        "conditional_heldout_profile_CSV_sha256":sha256(RISKS.read_bytes()).hexdigest(),
        "new_E2":0,"new_E3":0,"real_human_or_historical_data":False,
    }
    write_json(RESULT,result)
    accept={
        "research_id":"R197","status":"CLOSED_BOUNDED_E1_ARTIFICIAL_PREQUENTIAL_ARIMA",
        "artificial_source_worlds":24,"all_original_training_paths":1944,
        "full_conditional_horizon_profiles":3888,"all_candidate_independent_risk_checks":23328,
        "two_prequential_training_methods_Fraction_exact":True,
        "future_independent_noise_enumeration_equals_analytic_risk_Fraction_exact":True,
        "oracle_known_source_future_variance_frozen":True,
        "full_results_sha256":sha256(RESULT.read_bytes()).hexdigest(),
        "original_training_CSV_sha256":result["training_source_CSV_sha256"],
        "all_heldout_profile_CSV_sha256":result["conditional_heldout_profile_CSV_sha256"],
        "real_human_or_historical_data":False,"new_E2":0,"new_E3":0,
    }
    write_json(ACCEPT,accept)
    print("R197_MACHINE_ACCEPTANCE",json.dumps(accept,sort_keys=True))
    print("R197_ORACLE_AND_SELECTION_EXAMPLES",json.dumps(fixed[:5],sort_keys=True))
    return result


def archive():
    files=[Path(__file__).name,RESULT.name,TRAIN.name,RISKS.name,ACCEPT.name]
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
    print("R197_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestFixedARIMA(unittest.TestCase):
    def test_six_sources(self):self.assertEqual(len(SOURCES),6)
    def test_world_count(self):self.assertEqual(len(list(product(SOURCES,T_VALUES,HORIZONS))),24)
    def test_1944_paths(self):self.assertEqual(len(SOURCES)*sum(3**t for t in T_VALUES),1944)
    def test_3888_horizon_profiles(self):self.assertEqual(1944*len(HORIZONS),3888)
    def test_23328_risks(self):self.assertEqual(3888*len(SOURCES),23328)
    def test_noise_pmf_normalized(self):self.assertEqual(sum(NOISE_PROBS.values(),F(0)),1)
    def test_noise_mean_zero(self):self.assertEqual(sum((x*prob for x,prob in NOISE_PROBS.items()),F(0)),0)
    def test_noise_variance_half(self):self.assertEqual(sum((x*x*prob for x,prob in NOISE_PROBS.items()),F(0)),VAR_E)
    def test_every_source_first_y1_excluding_drift_same(self):
        for noise in NOISE:
            values=[trajectory(s,(noise,))[1] for s in SOURCES if s!="DRIFT"]
            self.assertEqual(len(set(values)),1)
    def test_drift_first_response(self):
        for noise in NOISE:self.assertEqual(trajectory("DRIFT",(noise,))[1],noise+1)
    def test_all_sources_y0_zero(self):
        for model in SOURCES:self.assertEqual(trajectory(model,(-1,0,1))[0],0)
    def test_true_source_forecast_mean_from_structural_generator(self):
        for s in SOURCES:
            for innov,p,hist in training_cases(s,4):
                for h in HORIZONS:
                    mu,v=oracle_truth(s,hist,innov,h)
                    self.assertEqual(forecast(s,hist,h),mu)
    def test_all_training_probabilities_source_specific_one(self):
        for s,T in product(SOURCES,T_VALUES):
            self.assertEqual(sum((p for i,p,y in training_cases(s,T)),F(0)),1)
    def test_all_train_prefix_vs_online_recursion_agree(self):
        for s,T in product(SOURCES,T_VALUES):
            for i,p,hist in training_cases(s,T):
                self.assertEqual(prequential_direct(hist),prequential_recursion(hist))
    def test_prequential_t2_not_t1(self):
        hist=trajectory("DRIFT",(0,0,0,0))
        self.assertEqual(prequential_direct(hist)["DRIFT"],0)
    def test_tie_priority_first_white(self):
        hist=trajectory("WHITE",(0,0,0,0))
        self.assertEqual(training_fit(hist)[0],"WHITE")
    def test_diff_ma_innovation_invertible(self):
        hist=trajectory("DIFF_MA1",(-1,0,1,1))
        self.assertEqual(forecast("DIFF_MA1",hist,1),hist[-1]+F(1,2))
    def test_ma_horizon_one_and_two_same_mean(self):
        for s in SOURCES:
            for innov,p,hist in training_cases(s,4):
                self.assertEqual(forecast("DIFF_MA1",hist,1),forecast("DIFF_MA1",hist,2))
    def test_AR1_horizon_two_halves(self):
        hist=trajectory("AR1",(1,1,0,0))
        self.assertEqual(forecast("AR1",hist,2),F(1,4)*hist[-1])
    def test_RW_forecast_constant_horizons(self):
        hist=trajectory("RW",(1,-1,0,1))
        self.assertEqual(forecast("RW",hist,1),forecast("RW",hist,2))
    def test_DRIFT_future_horizon_increments(self):
        hist=trajectory("DRIFT",(1,-1,0,1))
        self.assertEqual(forecast("DRIFT",hist,2)-forecast("DRIFT",hist,1),1)
    def test_I1AR_forecast_h2_3quarters_delta(self):
        hist=trajectory("DIFF_AR1",(1,0,1,0))
        self.assertEqual(forecast("DIFF_AR1",hist,2),
                         hist[-1]+F(3,4)*(hist[-1]-hist[-2]))
    def test_fixed_true_horizon_one_variance_half(self):
        for s in SOURCES:
            innov,p,hist=next(training_cases(s,4))
            self.assertEqual(oracle_truth(s,hist,innov,1)[1],F(1,2))
    def test_true_two_step_variances(self):
        checks={"WHITE":F(1,2),"AR1":F(5,8),"RW":F(1),
                "DRIFT":F(1),"DIFF_AR1":F(13,8),"DIFF_MA1":F(13,8)}
        for s,v in checks.items():
            innov,p,hist=next(training_cases(s,4))
            self.assertEqual(oracle_truth(s,hist,innov,2)[1],v)
    def test_independent_future_enum_vs_analytic_each_source_horizon(self):
        for s,T in product(SOURCES,T_VALUES):
            for innov,p,hist in training_cases(s,T):
                for h in HORIZONS:
                    forecasts,risk,mu,var=conditional_test_risks(s,hist,innov,h)
                    self.assertEqual(risk[s],var)
                    self.assertTrue(all(k>=var for k in risk.values()))
    def test_first_one_step_ar1_wrong_model_can_hurt_RW(self):
        s="RW";innov=(1,1,0,0)
        hist=trajectory(s,innov)
        f,r,mu,v=conditional_test_risks(s,hist,innov,1)
        self.assertGreater(r["AR1"],r["RW"])
    def test_first_one_step_diff_ar_works_for_true_source(self):
        s="DIFF_AR1";innov=(1,1,0,0)
        hist=trajectory(s,innov)
        f,r,mu,v=conditional_test_risks(s,hist,innov,2)
        self.assertEqual(r["DIFF_AR1"],F(13,8))
    def test_true_future_no_leak_from_work_training_selection(self):
        hist=trajectory("DIFF_MA1",(1,0,-1,1))
        choice,scores=training_fit(hist)
        for future in product(NOISE,repeat=2):
            _=trajectory("DIFF_MA1",(1,0,-1,1)+future)
            self.assertEqual((choice,scores),training_fit(hist))
    def test_invalid_source_fails(self):
        with self.assertRaises(ValueError):trajectory("ARIMA_ANY",(-1,0))
    def test_invalid_noise_fails(self):
        with self.assertRaises(ValueError):trajectory("RW",(2,))
    def test_invalid_training_steps_fails(self):
        with self.assertRaises(ValueError):next(training_cases("RW",3))
    def test_invalid_forecast_horizon_fails(self):
        with self.assertRaises(ValueError):forecast("RW",(F(0),F(1)),3)
    def test_invalid_forecast_no_history_fails(self):
        with self.assertRaises(ValueError):forecast("RW",(F(0),),1)
    def test_invalid_forecast_float_fails(self):
        with self.assertRaises(ValueError):forecast("RW",(F(0),1.0),1)
    def test_invalid_original_oracle_hidden_noise_fails(self):
        hist=trajectory("RW",(1,-1,0,1))
        with self.assertRaises(ValueError):oracle_truth("RW",hist,(1,0,0,1),1)
    def test_independent_future_only_3_to_power_h(self):
        self.assertEqual(sum(noise_mass(x) for x in product(NOISE,repeat=2)),1)
    def test_no_true_test_selected_without_prequential(self):
        for s in SOURCES:
            for i,p,hist in training_cases(s,4):
                name,score=training_fit(hist)
                self.assertEqual(score[name],min(score.values()))

if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:raise SystemExit("Use --test or --run-and-archive")
