#!/usr/bin/env python3
"""R215 finite three-period two-group difference-in-differences audit.

12 frozen toy untreated-trend/anticipation/postshock worlds and all
2^6 independent group-period Rademacher shock sources per world.
Each source is one POSSIBLE panel of 6 group-time observed values,
not 6 independent subjects or a set of empirical interventions.
"""
import argparse,csv,itertools,json,hashlib,unittest
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
OUT=Path(__file__).resolve().parent
TIMES=(-1,0,1)
CELLS=("T_-1","T_0","T_1","C_-1","C_0","C_1")
NOISE=tuple(itertools.product((-1,1),repeat=6))
# name -> (bT,bC,sT,sC,qT,qC,anticip,tau)
W={
"PARALLEL_NULL":(3,0,1,1,0,0,0,0),
"PARALLEL_TAU_TWO":(3,0,1,1,0,0,0,2),
"PARALLEL_NEGATIVE":(3,0,1,1,0,0,0,-2),
"LEVEL_GAP_ONLY":(10,0,1,1,0,0,0,0),
"DIFFERENTIAL_SLOPE_FALSE":(3,0,2,1,0,0,0,0),
"DIFFERENTIAL_SLOPE_TAU_TWO":(3,0,2,1,0,0,0,2),
"POST_SHOCK_FALSE":(3,0,1,1,2,0,0,0),
"POST_SHOCK_WITH_TAU_MINUS_ONE":(3,0,1,1,3,0,0,-1),
"ANTICIPATION_TAU_TWO":(3,0,1,1,0,0,1,2),
"ANTICIPATION_NULL":(3,0,1,1,0,0,1,0),
"CONTROL_POST_SHOCK":(3,0,1,1,0,2,0,0),
"LARGE_DIFF_SLOPE":(3,0,3,0,0,0,0,0),
}
COEFS={
"STANDARD_DID":(F(0),F(-1),F(1),F(0),F(1),F(-1)),
"PRE_TREND_PLACEBO":(F(-1),F(1),F(0),F(1),F(-1),F(0)),
"LINEAR_PRETREND_CORRECTED":(F(1),F(-2),F(1),F(-1),F(2),F(-1)),
}
def control_potential(world,g,t):
    bT,bC,sT,sC,qT,qC,anticip,tau=world
    if g not in ("T","C") or t not in TIMES:
        raise ValueError("only fixed two groups and three periods")
    b,s,q=(bT,sT,qT) if g=="T" else (bC,sC,qC)
    return F(b+s*t+q*(t==1))
def observed_mean(world):
    out=[]
    for g in ("T","C"):
        for t in TIMES:
            y=control_potential(world,g,t)
            if g=="T":
                if t==0:y+=world[6]
                if t==1:y+=world[7]
            out.append(y)
    return tuple(out)
def observed_real(world,eps):
    if len(eps)!=6 or any(e not in (-1,1) for e in eps):
        raise ValueError("six independent signs required")
    return tuple(y+e for y,e in zip(observed_mean(world),eps))
def score(y):
    if len(y)!=6:raise ValueError("exactly six visible outcomes needed")
    return {k:sum((F(c)*F(v) for c,v in zip(coeff,y)),F(0))
            for k,coeff in COEFS.items()}
def variance_coeff(k):
    return sum((c*c for c in COEFS[k]),F(0))
def source_observable_distribution(w):
    c=Counter(observed_real(w,eps) for eps in NOISE)
    return {"|".join(map(str,key)):str(F(n,64)) for key,n in sorted(c.items())}
def analytical_means(w):
    _,_,st,sc,qt,qc,anticip,tau=w
    slope=F(st-sc);q=F(qt-qc);a=F(anticip);effect=F(tau)
    return {"STANDARD_DID":effect+slope+q-a,
            "PRE_TREND_PLACEBO":slope+a,
            "LINEAR_PRETREND_CORRECTED":effect+q-2*a}
def audit():
    if len(W)!=12 or len(NOISE)!=64:raise AssertionError("source contract changed")
    allrows,worlds=[],[]
    for name,w in W.items():
        tau=F(w[-1]);ana=analytical_means(w)
        noiseless=observed_mean(w)
        theoretical_score=score(noiseless)
        accum={k:{"mean":F(0),"sq":F(0),"mse":F(0)} for k in COEFS}
        for eps in NOISE:
            real=observed_real(w,eps);vals=score(real)
            row={"world":name,"original_source_probability":"1/64",
                "original_six_group_period_shocks":"|".join(map(str,eps)),
                "group_period_cells":"|".join(CELLS),
                "six_true_untreated_counterfactual_group_means_FOR_AUDIT_ONLY":"|".join(
                    str(control_potential(w,g,t)) for g in ("T","C") for t in TIMES),
                "true_treated_post_ATT_FOR_AUDIT_ONLY":str(tau),
                "actual_pre_anticipation_FOR_AUDIT_ONLY":str(F(w[6])),
                "expected_six_observed_group_period_means":"|".join(map(str,noiseless)),
                "actual_six_observed_group_period_means":"|".join(map(str,real))}
            for k,v in vals.items():
                row[k+"_estimate"]=str(v)
                if k!="PRE_TREND_PLACEBO":
                    row[k+"_squared_error_to_true_ATT"]=str((v-tau)**2)
                    accum[k]["mse"]+=(v-tau)**2/64
                accum[k]["mean"]+=v/64
                accum[k]["sq"]+=v*v/64
            allrows.append(row)
        out={"world":name,"frozen_params_bT_bC_sT_sC_qT_qC_anticip_tau":list(w),
             "complete_original_sign_sources":64,"original_source_probability_sum":"1",
             "true_structural_post_treated_ATT_exact":str(tau),
             "true_unexposed_treated_minus_control_post_shock_exact":str(F(w[4]-w[5])),
             "anticipation_before_actual_treatment":str(F(w[6])),
             "counterfactual_untreated_parallel_trends_all_three_periods":
                 bool(w[2]==w[3] and w[4]==w[5]),
             "no_anticipation":bool(w[6]==0),
             "complete_six_observed_mean_vector":"|".join(map(str,noiseless)),
             "complete_joint_actual_observed_distribution":source_observable_distribution(w)}
        for k,d in accum.items():
            mean=d["mean"];var=d["sq"]-mean**2;vco=variance_coeff(k)
            if mean!=ana[k] or mean!=theoretical_score[k] or var!=vco:
                raise AssertionError("source expectation/variance differs from independent structure")
            item={"full_source_expected_estimate_exact":str(mean),
                  "precommitted_independent_structure_prediction_exact":str(ana[k]),
                  "original_noise_variance_exact":str(var),
                  "independent_source_weight_square_variance_exact":str(vco)}
            if k!="PRE_TREND_PLACEBO":
                bias=mean-tau;mse=d["mse"]
                if mse!=bias*bias+var:
                    raise AssertionError("original source MSE not equal to bias squared + variance")
                item.update({"true_ATT_bias_exact":str(bias),
                             "source_EXPECTED_squared_error_to_true_ATT_exact":str(mse),
                             "bias_squared_plus_variance_exact":str(bias*bias+var)})
            else:
                item["diagnostic_only_not_an_ATT_estimator"]=True
            out[k]=item
        worlds.append(out)
    if len(allrows)!=768:
        raise AssertionError("incomplete source universe")
    indexed={v["world"]:v for v in worlds}
    pair=("PARALLEL_TAU_TWO","POST_SHOCK_FALSE","POST_SHOCK_WITH_TAU_MINUS_ONE")
    if not all(indexed[pair[0]]["complete_joint_actual_observed_distribution"]==
               indexed[k]["complete_joint_actual_observed_distribution"] for k in pair[1:]):
        raise AssertionError("full observable panel distribution equality failed")
    if len({indexed[k]["true_structural_post_treated_ATT_exact"] for k in pair})!=3:
        raise AssertionError("different true ATT values disappeared")
    return {"research_id":"R215","catalogue_id":"09-006",
        "scientific_status":"ARTIFICIAL_E1_AWAIT_CI",
        "two_artificial_groups":["T","C"],"pre_periods":[-1,0],"post_period":1,
        "frozen_group_time_noise_independent":True,
        "all_worlds":12,"full_original_panel_source_rows":768,
        "source_probability_mass_each_world":"1",
        "fixed_independent_source_method_variances":{k:str(variance_coeff(k)) for k in COEFS},
        "three_observationally_equivalent_worlds_different_true_ATT":list(pair),
        "entire_six_cell_panel_observable_joint_distribution_identical":True,
        "post_only_untreated_shock_not_detectable_by_population_pretrend":True,
        "no_real_cluster_robust_or_serial_correlation_inference":True,
        "new_real_human_E2":0,"new_real_historical_E3":0,"worlds":worlds},allrows
def emit():
    r,rows=audit()
    a=OUT/"R215_EXACT_RESULTS.json"
    b=OUT/"R215_ALL_768_ORIGINAL_GROUP_TIME_SHOCK_PANELS.csv"
    a.write_text(json.dumps(r,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    with b.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    c={"model_id":"R215","catalogue_id":"09-006","worlds":12,
       "original_complete_group_time_panel_sources":768,
       "six_independent_noise_cells_all_complete":True,
       "source_MSE_bias_variance_two_routes_consistent":True,
       "three_observationally_identical_panels_distinct_ATT":True,
       "new_E2":0,"new_E3":0,
       "result_sha256":hashlib.sha256(a.read_bytes()).hexdigest(),
       "sources_sha256":hashlib.sha256(b.read_bytes()).hexdigest()}
    (OUT/"R215_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(c,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(c,indent=2))
class Tests(unittest.TestCase):
    def test_twelve_worlds(self):self.assertEqual(len(W),12)
    def test_six_cells(self):self.assertEqual(len(CELLS),6)
    def test_three_periods(self):self.assertEqual(TIMES,(-1,0,1))
    def test_noise_64(self):self.assertEqual(len(NOISE),64)
    def test_768_source_total(self):self.assertEqual(len(W)*len(NOISE),768)
    def test_eps_each_cell_mean_zero(self):
        for i in range(6):self.assertEqual(sum(e[i] for e in NOISE),0)
    def test_eps_cross_covariance_zero(self):
        for i in range(6):
            for j in range(6):
                if i!=j:self.assertEqual(sum(e[i]*e[j] for e in NOISE),0)
    def test_standard_DID_variance_four(self):self.assertEqual(variance_coeff("STANDARD_DID"),4)
    def test_pretrend_placebo_variance_four(self):self.assertEqual(variance_coeff("PRE_TREND_PLACEBO"),4)
    def test_linear_pretrend_corrected_variance_twelve(self):self.assertEqual(variance_coeff("LINEAR_PRETREND_CORRECTED"),12)
    def test_corrected_is_DID_minus_placebo(self):
        for v in (observed_mean(W["PARALLEL_TAU_TWO"]),observed_mean(W["POST_SHOCK_FALSE"])):
            x=score(v)
            self.assertEqual(x["LINEAR_PRETREND_CORRECTED"],x["STANDARD_DID"]-x["PRE_TREND_PLACEBO"])
    def test_parallel_tau_two_DID_two(self):
        self.assertEqual(analytical_means(W["PARALLEL_TAU_TWO"])["STANDARD_DID"],2)
    def test_differential_slope_false_DID_one(self):
        self.assertEqual(analytical_means(W["DIFFERENTIAL_SLOPE_FALSE"])["STANDARD_DID"],1)
    def test_differential_slope_pretrend_one(self):
        self.assertEqual(analytical_means(W["DIFFERENTIAL_SLOPE_FALSE"])["PRE_TREND_PLACEBO"],1)
    def test_differential_slope_correction_zero(self):
        self.assertEqual(analytical_means(W["DIFFERENTIAL_SLOPE_FALSE"])["LINEAR_PRETREND_CORRECTED"],0)
    def test_postshock_false_pretrend_zero(self):
        self.assertEqual(analytical_means(W["POST_SHOCK_FALSE"])["PRE_TREND_PLACEBO"],0)
    def test_postshock_false_DID_two(self):
        self.assertEqual(analytical_means(W["POST_SHOCK_FALSE"])["STANDARD_DID"],2)
    def test_anticipation_tautwo_DID_one(self):
        self.assertEqual(analytical_means(W["ANTICIPATION_TAU_TWO"])["STANDARD_DID"],1)
    def test_anticipation_tautwo_adjusted_zero(self):
        self.assertEqual(analytical_means(W["ANTICIPATION_TAU_TWO"])["LINEAR_PRETREND_CORRECTED"],0)
    def test_three_same_observed_expectations(self):
        a=W["PARALLEL_TAU_TWO"]
        for k in ("POST_SHOCK_FALSE","POST_SHOCK_WITH_TAU_MINUS_ONE"):
            self.assertEqual(observed_mean(a),observed_mean(W[k]))
    def test_three_different_ATT(self):
        self.assertEqual([W[k][-1] for k in ("PARALLEL_TAU_TWO","POST_SHOCK_FALSE","POST_SHOCK_WITH_TAU_MINUS_ONE")],[2,0,-1])
    def test_all_complete_obs_distribution_equiv(self):
        a=source_observable_distribution(W["PARALLEL_TAU_TWO"])
        self.assertEqual(a,source_observable_distribution(W["POST_SHOCK_FALSE"]))
        self.assertEqual(a,source_observable_distribution(W["POST_SHOCK_WITH_TAU_MINUS_ONE"]))
    def test_invalid_group(self):
        with self.assertRaises(ValueError):control_potential(W["PARALLEL_TAU_TWO"],"X",0)
    def test_invalid_period(self):
        with self.assertRaises(ValueError):control_potential(W["PARALLEL_TAU_TWO"],"T",9)
    def test_invalid_noise(self):
        with self.assertRaises(ValueError):observed_real(W["PARALLEL_TAU_TWO"],(0,)*6)
    def test_invalid_score(self):
        with self.assertRaises(ValueError):score((0,))
    def test_complete_audit_all(self):
        r,rows=audit()
        self.assertEqual((len(r["worlds"]),len(rows)),(12,768))
        self.assertEqual(r["fixed_independent_source_method_variances"],{
            "STANDARD_DID":"4","PRE_TREND_PLACEBO":"4","LINEAR_PRETREND_CORRECTED":"12"})
    def test_replay(self):self.assertEqual(audit(),audit())
def _test_world_specific(key):
    def test(self):
        w=W[key]
        self.assertEqual(score(observed_mean(w)),analytical_means(w))
        self.assertEqual(len(source_observable_distribution(w)),64)
    return test
for _key in W:
    setattr(Tests,"test_world_"+_key.lower(),_test_world_specific(_key))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true")
    p.add_argument("--emit",action="store_true")
    z=p.parse_args()
    if z.test:
        result=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if result.wasSuccessful() else 1)
    if z.emit:emit()
    if not z.test and not z.emit:p.print_help()
