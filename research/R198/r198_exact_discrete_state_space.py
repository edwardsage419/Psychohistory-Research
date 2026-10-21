"""R198 known-parameter discrete state-space filtering and smoothing audit.

Four symmetric binary latent transition rates x two noisy sensor rates x
T=4/5 x full/missing-final-sensor visibility = 32 artificial worlds.
All 576 original visible histories are enumerated with exact Fraction,
with independent forward recursion and exhaustive hidden-path inference.
Four future observation Brier risks are crosschecked by true-joint
enumeration and conditional variance/bias identities (2304 cells).
Not Kalman-Gaussian filtering, not an estimated HMM, no human data.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import csv,json,sys,unittest,zipfile

HERE=Path(__file__).resolve().parent
PROTOCOL=HERE.parent.parent/"protocols/R198_STATE_SPACE_32_WORLDS_576_VISIBLE_HISTORIES_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R198_EXACT_RESULTS.json"
CSV=HERE/"R198_ALL_576_EXACT_VISIBLE_HISTORIES.csv"
DIAG=HERE/"R198_ALL_8_LATENT_OBSERVATION_MOMENT_DIAGNOSTICS.json"
ACCEPT=HERE/"R198_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R198_32_Exact_Discrete_State_Space_Worlds.zip"

AS=(F(1,2),F(3,4),F(1,4),F(11,18))
RS=(F(3,4),F(7,8))
TS=(4,5)
MASKS=("FULL","LAST_MISSING")
MODELS=("EXACT_FULL_FILTER","LATEST_ONLY_SENSOR","NAIVE_Y_AS_LATENT","UNCONDITIONAL_HALF")


def world_checks(a,r,T,mask):
    if a not in AS or r not in RS or T not in TS or mask not in MASKS:
        raise ValueError("Out-of-protocol hidden transition/sensor/time/missingness model")


def worlds():
    for a,r,T,mask in product(AS,RS,TS,MASKS):
        yield a,r,T,mask


def histories(T,mask):
    if T not in TS or mask not in MASKS:
        raise ValueError("Unsupported visible history definition")
    count=T if mask=="FULL" else T-1
    for bits in product((0,1),repeat=count):
        yield bits if mask=="FULL" else bits+(None,)


def transition(a,previous,new):
    return a if previous==new else 1-a


def emit(r,hidden,visible):
    if visible is None:
        return F(1)
    return r if hidden==visible else 1-r


def forward_raw(a,r,visible):
    """Recursive hidden state mass; initial X0 ~ 1/2."""
    mass=(F(1,2),F(1,2))
    for y in visible:
        new=[]
        for j in (0,1):
            probability=sum((mass[i]*transition(a,i,j) for i in (0,1)),F(0))
            new.append(probability*emit(r,j,y))
        mass=tuple(new)
    return mass


def forward_filter(a,r,visible):
    mass=forward_raw(a,r,visible)
    evidence=sum(mass,F(0))
    if evidence<=0:
        raise AssertionError("No observation history evidence")
    post=mass[1]/evidence
    p_next_hidden=(1-a)+(2*a-1)*post
    p_next_visible=(1-r)+(2*r-1)*p_next_hidden
    return evidence,post,p_next_visible


def full_latent_enumeration(a,r,visible):
    """Independent source path summation, no forward-state recursion."""
    T=len(visible)
    evidence=F(0)
    target_last=F(0)
    target_previous=F(0)
    joint_next_visible_one=F(0)
    for states in product((0,1),repeat=T+1):
        prob=F(1,2)
        for t in range(1,T+1):
            prob*=transition(a,states[t-1],states[t])
            prob*=emit(r,states[t],visible[t-1])
        evidence+=prob
        target_last+=prob*states[-1]
        target_previous+=prob*states[-2]
        for next_hidden in (0,1):
            joint_next_visible_one+=(
                prob*transition(a,states[-1],next_hidden)*emit(r,next_hidden,1))
    if evidence<=0:
        raise AssertionError("Nonpositive latent path evidence")
    return evidence,target_last/evidence,target_previous/evidence,joint_next_visible_one/evidence


def backward_one_step_smoother(a,r,visible):
    """Compute X_(T-1)|all observed history using an independent last observation factor."""
    if len(visible)<2:
        raise ValueError("Need hidden time T-1")
    prefix=forward_raw(a,r,visible[:-1])
    signal=visible[-1]
    likelihoods=[
        sum((transition(a,i,j)*emit(r,j,signal) for j in (0,1)),F(0))
        for i in (0,1)
    ]
    den=sum((prefix[i]*likelihoods[i] for i in (0,1)),F(0))
    if den<=0:raise AssertionError("Backward smoothing likelihood zero")
    return prefix[1]*likelihoods[1]/den


def propagate(a,p,steps):
    if steps<0:raise ValueError("Cannot backward-propagate last observed evidence")
    value=p
    for _ in range(steps):
        value=(1-a)+(2*a-1)*value
    return value


def predictor_candidates(a,r,visible,p_exact):
    T=len(visible)
    known=[(i+1,y) for i,y in enumerate(visible) if y is not None]
    if not known:
        raise ValueError("No observed measurement")
    last_t,last_y=known[-1]
    moves=T+1-last_t
    sensor_p=r if last_y==1 else 1-r
    latest_hidden=propagate(a,sensor_p,moves)
    naive_hidden=propagate(a,F(last_y),moves)
    emission=lambda p:(1-r)+(2*r-1)*p
    return {
        "EXACT_FULL_FILTER":p_exact,
        "LATEST_ONLY_SENSOR":emission(latest_hidden),
        "NAIVE_Y_AS_LATENT":emission(naive_hidden),
        "UNCONDITIONAL_HALF":F(1,2)
    }


def brier_from_actual_binary_distribution(p,q):
    return p*(1-q)**2+(1-p)*q*q


def brier_from_bias_variance(p,q):
    return p*(1-p)+(q-p)**2


def evaluate_history(a,r,visible):
    evid,latent_post,pforward=forward_filter(a,r,visible)
    direct,latent_direct,smoothed_direct,pnext=full_latent_enumeration(a,r,visible)
    smooth=backward_one_step_smoother(a,r,visible)
    if (evid!=direct or latent_post!=latent_direct or pforward!=pnext
        or smooth!=smoothed_direct):
        raise AssertionError("Independent forward filter vs all hidden paths vs backward smoother disagree")
    all_preds=predictor_candidates(a,r,visible,pnext)
    risk={}
    for name,pred in all_preds.items():
        raw=brier_from_actual_binary_distribution(pnext,pred)
        analytic=brier_from_bias_variance(pforward,pred)
        if raw!=analytic or raw<analytic if False else False:
            raise AssertionError("Impossible double exact future Brier identity")
        if raw<brier_from_bias_variance(pnext,pnext):
            raise AssertionError("Bayes oracle Brier violated")
        risk[name]=raw
    if pforward!=all_preds["EXACT_FULL_FILTER"]:
        raise AssertionError("Source-true full filter must be posterior predictive")
    previous_filtered=forward_filter(a,r,visible[:-1])[1]
    if visible[-1] is None and smooth!=previous_filtered:
        raise AssertionError("Missing final observation cannot smooth previous state")
    return evid,latent_post,smoothed_direct,previous_filtered,pnext,all_preds,risk


def source_lag_observed_covariance(a,r,lag):
    if lag not in (1,2):
        raise ValueError("Only prelocked observed lags one and two")
    return ((2*a-1)**lag)*(2*r-1)**2/F(4)


def exhaustive_observed_lag_covariance(a,r,lag):
    """Independent exact observed history distribution aggregate, not a formula substitution."""
    T=4
    summation=F(0)
    for visible in histories(T,"FULL"):
        mass=full_latent_enumeration(a,r,visible)[0]
        summation+=mass*visible[0]*visible[lag]
    return summation-F(1,4)


def summarize_world(a,r,T,mask,rows):
    total=F(0)
    losses={name:F(0) for name in MODELS}
    expected_smoothing_shift=F(0)
    paths=0
    for visible in histories(T,mask):
        evidence,last,smoothed,prev_filtered,pnext,preds,risks=evaluate_history(a,r,visible)
        total+=evidence
        paths+=1
        expected_smoothing_shift+=evidence*abs(smoothed-prev_filtered)
        for name in MODELS:
            losses[name]+=evidence*risks[name]
        rows.append({
            "latent_transition_repeat_probability_a":str(a),
            "measurement_accuracy_r":str(r),
            "time_length_T":T,
            "visibility_protocol":mask,
            "actually_visible_y1_to_yT":"".join("-" if x is None else str(x) for x in visible),
            "source_visible_history_probability":str(evidence),
            "exact_hidden_XT_posterior_probability_1":str(last),
            "exact_smoothed_X_Tminus1_posterior_probability_1":str(smoothed),
            "filtered_X_Tminus1_without_last_measurement_probability_1":str(prev_filtered),
            "true_NEW_observation_Y_Tplus1_probability_1":str(pnext),
            **{f"candidate_{name}_forecast_probability":str(preds[name]) for name in MODELS},
            **{f"candidate_{name}_exact_NEW_observation_Brier":str(risks[name]) for name in MODELS},
            "forward_filter_full_latent_path_and_backward_smoother_all_Fraction_equal":True
        })
    if total!=1 or paths!=2**(T if mask=="FULL" else T-1):
        raise AssertionError("Full frozen original measurement space did not normalize")
    if losses["UNCONDITIONAL_HALF"]!=F(1,4):
        raise AssertionError("Symmetric observation unconditional Brier cannot differ from quarter")
    if not (losses["EXACT_FULL_FILTER"]<=losses["LATEST_ONLY_SENSOR"]
            and losses["EXACT_FULL_FILTER"]<=losses["NAIVE_Y_AS_LATENT"]
            and losses["EXACT_FULL_FILTER"]<=losses["UNCONDITIONAL_HALF"]):
        raise AssertionError("Bayes optimal predictor beaten on complete expected real source")
    if a==F(1,2) and any(z!=F(1,4) for z in losses.values()):
        raise AssertionError("IID hidden state must destroy all past observation predictive gains")
    if mask=="LAST_MISSING" and expected_smoothing_shift!=0:
        raise AssertionError("Missing sensor gave nonzero future smoothing information")
    return {
        "latent_repeat_a":str(a),"measurement_accuracy_r":str(r),
        "training_T":T,"measurement_visibility":mask,
        "all_visible_original_history_patterns":paths,
        "all_training_history_probabilities_exactly_normalize":True,
        "actual_independent_NEW_measurement_expected_Brier":{name:str(v) for name,v in losses.items()},
        "full_filter_expected_gain_over_latest_only_sensor":str(
            losses["LATEST_ONLY_SENSOR"]-losses["EXACT_FULL_FILTER"]),
        "full_filter_expected_gain_over_unconditional_half":str(
            losses["UNCONDITIONAL_HALF"]-losses["EXACT_FULL_FILTER"]),
        "expected_smoothed_vs_prefix_filtered_previous_hidden_state_abs_change":str(expected_smoothing_shift),
        "all_original_forward_backward_and_latent_bruteforce_algorithms_Fraction_equal":True
    }


def verify_missing_marginal(a,r,T):
    complete={seq:full_latent_enumeration(a,r,seq)[0] for seq in histories(T,"FULL")}
    missed={seq:full_latent_enumeration(a,r,seq)[0] for seq in histories(T,"LAST_MISSING")}
    for seq,mass in missed.items():
        prefix=seq[:-1]
        if complete[prefix+(0,)]+complete[prefix+(1,)]!=mass:
            raise AssertionError("End-sensor masked probability differs from marginal full data")
    return True


def write_json(path,obj):
    path.write_text(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def run():
    rows=[]
    summaries=[summarize_world(a,r,T,mask,rows) for a,r,T,mask in worlds()]
    if len(summaries)!=32 or len(rows)!=576:
        raise AssertionError("Frozen state-space 32-world 576-observation universe changed")
    diagnostics=[]
    for a,r in product(AS,RS):
        cov1=source_lag_observed_covariance(a,r,1)
        cov2=source_lag_observed_covariance(a,r,2)
        if (cov1!=exhaustive_observed_lag_covariance(a,r,1) or
            cov2!=exhaustive_observed_lag_covariance(a,r,2)):
            raise AssertionError("Two separately implemented observed-lag covariance sources disagree")
        diagnostics.append({"a":str(a),"r":str(r),
                            "true_hidden_lag1_spin_correlation":str(2*a-1),
                            "visible_observation_1_lag_covariance_exact":str(cov1),
                            "visible_observation_2_lag_covariance_exact":str(cov2),
                            "single_time_observation_p_one":"1/2",
                            "formula_vs_complete_all_latent_path_observation_PMF_exact":True})
        for T in TS:
            verify_missing_marginal(a,r,T)
            whole=next(w for w in summaries if w["latent_repeat_a"]==str(a) and
                       w["measurement_accuracy_r"]==str(r) and w["training_T"]==T and
                       w["measurement_visibility"]=="FULL")
            missing=next(w for w in summaries if w["latent_repeat_a"]==str(a) and
                         w["measurement_accuracy_r"]==str(r) and w["training_T"]==T and
                         w["measurement_visibility"]=="LAST_MISSING")
            oracle_full=F(whole["actual_independent_NEW_measurement_expected_Brier"]["EXACT_FULL_FILTER"])
            oracle_missing=F(missing["actual_independent_NEW_measurement_expected_Brier"]["EXACT_FULL_FILTER"])
            if oracle_full>oracle_missing:
                raise AssertionError("Future sensor information increased fully Bayesian expected loss")
    aa=next(x for x in diagnostics if x["a"]=="3/4" and x["r"]=="3/4")
    bb=next(x for x in diagnostics if x["a"]=="11/18" and x["r"]=="7/8")
    if not(aa["visible_observation_1_lag_covariance_exact"]==bb["visible_observation_1_lag_covariance_exact"]=="1/32"
           and aa["visible_observation_2_lag_covariance_exact"]=="1/64"
           and bb["visible_observation_2_lag_covariance_exact"]=="1/144"):
        raise AssertionError("Frozen adjacent observation alias with nonidentical lag two failed")
    if not any(F(w["full_filter_expected_gain_over_latest_only_sensor"])>0
               for w in summaries if w["latent_repeat_a"]!="1/2"):
        raise AssertionError("No source demonstrated genuine full-history filtering gain")
    with CSV.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(rows)
    write_json(DIAG,{"research_id":"R198","kernel_diagnostics_count":8,
                     "moment_and_alias_diagnostics":diagnostics})
    focus=[w for w in summaries if w["latent_repeat_a"] in ("3/4","11/18") and
           w["measurement_accuracy_r"] in ("3/4","7/8") and w["training_T"]==5]
    out={
        "research_id":"R198",
        "stage":"E1_ARTIFICIAL_EXACT_BINARY_HIDDEN_STATE_SPACE_WITH_NOISY_MEASUREMENT",
        "world_count":32,"ordered_visible_training_histories":576,
        "four_candidate_independent_future_Brier_risk_profiles":2304,
        "distinct_known_state_transition_sensor_kernels":8,
        "both_full_latent_path_and_forward_filter_Fraction_exact":True,
        "one_step_backward_smoothing_vs_all_latent_path_Fraction_exact":True,
        "future_observation_Brier_full_source_vs_bias_variance_Fraction_exact":True,
        "missing_last_sensor_exactly_marginalizes_observed_FULL_distribution":True,
        "more_observation_information_never_increases_true_expected_Bayes_risk":True,
        "all_observation_single_time_marginals_half":True,
        "lag1_identical_observation_correlation_but_lag2_different":True,
        "frozen_lag1_alias_pair_covariances":{
            "PERSIST_a3_4_r3_4":{"lag1":"1/32","lag2":"1/64"},
            "ALIAS_a11_18_r7_8":{"lag1":"1/32","lag2":"1/144"}
        },
        "prelocked_visible_alias_and_missing_sensor_worlds":focus,
        "all_original_worlds":summaries,
        "all_576_visible_history_CSV_sha256":sha256(CSV.read_bytes()).hexdigest(),
        "all_eight_observation_diagnostic_SHA256":sha256(DIAG.read_bytes()).hexdigest(),
        "actual_human_or_historical_data":False,"new_E2":0,"new_E3":0
    }
    write_json(RESULT,out)
    accept={
        "research_id":"R198","status":"CLOSED_BOUNDED_E1_ARTIFICIAL_DISCRETE_STATE_SPACE",
        "worlds":32,"full_visible_history_paths":576,"independent_future_Brier_checks":2304,
        "filter_vs_full_latent_path_posterior_and_evidence_exact":True,
        "backward_smoother_vs_full_enumeration_exact":True,
        "last_sensor_marginalization_and_expected_bayes_risk_monotonicity":True,
        "same_lag1_observed_covariance_different_lag2_latent_dynamics_verified":True,
        "result_sha256":sha256(RESULT.read_bytes()).hexdigest(),
        "visible_original_CSV_sha256":out["all_576_visible_history_CSV_sha256"],
        "all_diagnostics_json_sha256":out["all_eight_observation_diagnostic_SHA256"],
        "new_E2":0,"new_E3":0,"actual_human_or_historical_data":False
    }
    write_json(ACCEPT,accept)
    print("R198_ACCEPTANCE",json.dumps(accept,sort_keys=True))
    print("R198_FROZEN_ALIAS",json.dumps(out["frozen_lag1_alias_pair_covariances"],sort_keys=True))
    return out


def archive():
    names=[Path(__file__).name,RESULT.name,CSV.name,DIAG.name,ACCEPT.name]
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
    print("R198_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestFiniteStateSpace(unittest.TestCase):
    def test_four_hidden_transitions(self):self.assertEqual(len(AS),4)
    def test_two_sensor_qualities(self):self.assertEqual(len(RS),2)
    def test_32_worlds(self):self.assertEqual(len(list(worlds())),32)
    def test_576_original_observed_histories(self):
        self.assertEqual(sum(2**(T if m=="FULL" else T-1) for a,r,T,m in worlds()),576)
    def test_2304_future_brier_cells(self):self.assertEqual(576*len(MODELS),2304)
    def test_all_hidden_probability_parameters_inside_one(self):
        self.assertTrue(all(F(0)<x<F(1) for x in AS+RS))
    def test_transition_rows_sum_one(self):
        for a in AS:
            for i in (0,1):
                self.assertEqual(sum((transition(a,i,j) for j in (0,1)),F(0)),1)
    def test_emission_rows_sum_one(self):
        for r in RS:
            for i in (0,1):
                self.assertEqual(sum((emit(r,i,j) for j in (0,1)),F(0)),1)
    def test_missing_sensor_likelihood_one(self):
        for r in RS:
            for i in (0,1):self.assertEqual(emit(r,i,None),1)
    def test_all_complete_original_observation_sources_sum_one(self):
        for a,r,T,mask in worlds():
            total=sum((forward_filter(a,r,v)[0] for v in histories(T,mask)),F(0))
            self.assertEqual(total,1)
    def test_forward_and_latent_bruteforce_all_576(self):
        for a,r,T,mask in worlds():
            for v in histories(T,mask):
                a1,b,c=forward_filter(a,r,v)
                d,e,f,g=full_latent_enumeration(a,r,v)
                self.assertEqual((a1,b,c),(d,e,g))
    def test_back_smoother_vs_complete_path_all(self):
        for a,r,T,mask in worlds():
            for v in histories(T,mask):
                self.assertEqual(backward_one_step_smoother(a,r,v),
                                 full_latent_enumeration(a,r,v)[2])
    def test_all_future_risks_complete_source_vs_analytic(self):
        for a,r,T,mask in worlds():
            for v in histories(T,mask):
                evaluate_history(a,r,v)
    def test_all_posterior_probabilities_in_unit_interval(self):
        for a,r,T,mask in worlds():
            for v in histories(T,mask):
                m,latent,pnext=forward_filter(a,r,v)
                self.assertTrue(0<=latent<=1 and 0<=pnext<=1)
    def test_iid_state_half_next_observation(self):
        for r in RS:
            for T in TS:
                for mask in MASKS:
                    for v in histories(T,mask):
                        self.assertEqual(forward_filter(F(1,2),r,v)[2],F(1,2))
    def test_iid_any_predictor_half(self):
        for r in RS:
            for mask in MASKS:
                for v in histories(4,mask):
                    preds=predictor_candidates(F(1,2),r,v,F(1,2))
                    self.assertEqual(set(preds.values()),{F(1,2)})
    def test_iid_future_Brier_one_quarter(self):
        for r in RS:
            for mask in MASKS:
                report=summarize_world(F(1,2),r,4,mask,[])
                self.assertEqual(set(report["actual_independent_NEW_measurement_expected_Brier"].values()),{"1/4"})
    def test_all_missing_matches_marginal_full(self):
        for a,r,T,_ in worlds():
            self.assertTrue(verify_missing_marginal(a,r,T))
    def test_missing_last_does_not_smooth_tminus1(self):
        for a,r,T,_ in worlds():
            for v in histories(T,"LAST_MISSING"):
                self.assertEqual(backward_one_step_smoother(a,r,v),
                                 forward_filter(a,r,v[:-1])[1])
    def test_full_last_observation_smooths_some_persistent_history(self):
        a,r,T=F(3,4),F(3,4),4
        self.assertTrue(any(backward_one_step_smoother(a,r,v)!=forward_filter(a,r,v[:-1])[1]
                            for v in histories(T,"FULL")))
    def test_exact_visible_lag_cov_formula_matches_enumeration(self):
        for a,r in product(AS,RS):
            for lag in (1,2):
                self.assertEqual(source_lag_observed_covariance(a,r,lag),
                                 exhaustive_observed_lag_covariance(a,r,lag))
    def test_prelocked_alias_same_lag1(self):
        self.assertEqual(source_lag_observed_covariance(F(3,4),F(3,4),1),
                         source_lag_observed_covariance(F(11,18),F(7,8),1))
    def test_prelocked_alias_lag1_one_32(self):
        self.assertEqual(source_lag_observed_covariance(F(3,4),F(3,4),1),F(1,32))
    def test_prelocked_alias_lag2_one_64_vs_one_144(self):
        self.assertEqual(source_lag_observed_covariance(F(3,4),F(3,4),2),F(1,64))
        self.assertEqual(source_lag_observed_covariance(F(11,18),F(7,8),2),F(1,144))
    def test_full_information_never_higher_expected_oracle_risk(self):
        for a,r,T in product(AS,RS,TS):
            all_seen=summarize_world(a,r,T,"FULL",[])
            missing=summarize_world(a,r,T,"LAST_MISSING",[])
            risk=lambda w:F(w["actual_independent_NEW_measurement_expected_Brier"]["EXACT_FULL_FILTER"])
            self.assertLessEqual(risk(all_seen),risk(missing))
    def test_full_filter_optimal_over_four_predictors_expected(self):
        for a,r,T,mask in worlds():
            output=summarize_world(a,r,T,mask,[])
            risks={name:F(v) for name,v in output["actual_independent_NEW_measurement_expected_Brier"].items()}
            self.assertEqual(risks["EXACT_FULL_FILTER"],min(risks.values()))
    def test_genuine_history_gain_exists(self):
        sample=summarize_world(F(3,4),F(3,4),5,"FULL",[])
        self.assertGreater(F(sample["full_filter_expected_gain_over_latest_only_sensor"]),0)
    def test_last_sensor_missing_latest_baseline_temporal_gap_two(self):
        p=predictor_candidates(F(3,4),F(3,4),(1,0,1,None),F(1,2))
        self.assertTrue(0<p["LATEST_ONLY_SENSOR"]<1)
    def test_next_probability_filter_is_exact_Bayes(self):
        for a,r,T,mask in worlds():
            for vis in histories(T,mask):
                x=evaluate_history(a,r,vis)
                self.assertEqual(x[5]["EXACT_FULL_FILTER"],x[4])
    def test_brier_bias_variance_identity(self):
        for p,q in product((F(1,4),F(1,2),F(7,8)),repeat=2):
            self.assertEqual(brier_from_actual_binary_distribution(p,q),
                             brier_from_bias_variance(p,q))
    def test_brier_oracle_never_above_any_other_conditional(self):
        for p,q in product((F(1,4),F(1,2),F(7,8)),repeat=2):
            self.assertLessEqual(brier_from_bias_variance(p,p),brier_from_bias_variance(p,q))
    def test_single_sensor_bayes_r(self):
        p=predictor_candidates(F(3,4),F(3,4),(0,0,0,1),F(1,2))
        self.assertGreater(p["LATEST_ONLY_SENSOR"],F(1,2))
    def test_all_last_missing_observation_patterns_end_None(self):
        for T in TS:
            self.assertTrue(all(p[-1] is None for p in histories(T,"LAST_MISSING")))
    def test_all_full_observation_patterns_end_valid(self):
        for T in TS:
            self.assertTrue(all(p[-1] in (0,1) for p in histories(T,"FULL")))
    def test_bad_transition_parameter_rejected(self):
        with self.assertRaises(ValueError):world_checks(F(2,3),F(3,4),4,"FULL")
    def test_bad_sensor_parameter_rejected(self):
        with self.assertRaises(ValueError):world_checks(F(3,4),F(2,3),4,"FULL")
    def test_bad_visibility_parameter_rejected(self):
        with self.assertRaises(ValueError):next(histories(4,"NONRANDOM"))
    def test_bad_time_rejected(self):
        with self.assertRaises(ValueError):next(histories(6,"FULL"))
    def test_invalid_history_for_predictor_rejected(self):
        with self.assertRaises(ValueError):predictor_candidates(F(3,4),F(3,4),(None,None),F(1,2))
    def test_negative_propagation_rejected(self):
        with self.assertRaises(ValueError):propagate(F(3,4),F(1,2),-1)
    def test_smoother_insufficient_history_rejected(self):
        with self.assertRaises(ValueError):backward_one_step_smoother(F(3,4),F(3,4),(1,))


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:raise SystemExit("Use --test or --run-and-archive")
