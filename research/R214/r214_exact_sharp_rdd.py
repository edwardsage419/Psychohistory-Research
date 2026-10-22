#!/usr/bin/env python3
"""R214 exact four-position artificial sharp RDD.
12 frozen worlds x all 16 iid Rademacher noise vectors: 192 original sources.
Identical observable distributions can reflect distinct threshold effects.
This is NOT a real causal RD, a density test, or a dense-support RDD estimator.
"""
import argparse,csv,itertools,json,hashlib,unittest
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
OUT=Path(__file__).resolve().parent
X=(-2,-1,1,2)
NOISE=tuple(itertools.product((-1,1),repeat=4))
COEFF={"GLOBAL":(F(-1,2),F(-1,2),F(1,2),F(1,2)),
"NEAREST":(F(0),F(-1),F(1),F(0)),
"TWO_SIDED_LINEAR":(F(1),F(-2),F(2),F(-1))}
# b,sL,sR,qL,qR,baseline jump, true tau
W={
"FLAT_NULL":(0,0,0,0,0,0,0),
"FLAT_TAU_TWO":(0,0,0,0,0,0,2),
"LINEAR_CAUSAL_TWO":(0,1,1,0,0,0,2),
"LINEAR_NULL_SLOPE_TWO":(0,2,2,0,0,0,0),
"BASELINE_STEP_FALSE_CAUSAL":(0,1,1,0,0,2,0),
"NEGATIVE_CAUSAL":(0,1,1,0,0,0,-2),
"RIGHT_QUADRATIC":(0,1,1,0,1,0,2),
"LEFT_QUADRATIC":(0,1,1,1,0,0,0),
"MATCHED_QUADRATIC":(0,1,1,1,1,0,2),
"DIFFERENT_SLOPES":(0,1,2,0,0,0,2),
"NEGATIVE_TAU_WITH_STEP":(0,1,1,0,0,3,-1),
"LEFT_CURVATURE_WITH_NEGATIVE_TAU":(0,2,2,1,0,0,-2),
}
def y0(p,x):
    b,sl,sr,ql,qr,jump,tau=p
    return F(b+(sl*x+ql*x*x if x<0 else sr*x+qr*x*x+jump))
def potential(p,x,d):
    return y0(p,x)+F(p[-1])*d
def clean(p):
    return tuple(potential(p,x,int(x>=0)) for x in X)
def estimator(y,coef):
    return sum((F(a)*b for a,b in zip(y,coef)),F(0))
def score_all(y):
    return {name:estimator(y,v) for name,v in COEFF.items()}
def source_noisy(p,eps):
    return tuple(v+e for v,e in zip(clean(p),eps))
def outcome_dist(p):
    c=Counter(source_noisy(p,eps) for eps in NOISE)
    return {"|".join(map(str,k)):str(F(v,16)) for k,v in sorted(c.items())}
def exact_results():
    if len(W)!=12 or len(NOISE)!=16:raise AssertionError("source universe")
    rows,worlds=[],[]
    for name,p in W.items():
        tau=F(p[-1]);jump=F(p[-2]);mean=clean(p)
        analytic=score_all(mean)
        accum={m:{"E":F(0),"E2":F(0),"MSE":F(0)} for m in COEFF}
        for eps in NOISE:
            y=source_noisy(p,eps); est=score_all(y)
            row={"world":name,"running_variable_points":"-2|-1|1|2",
                "observed_treatment_assignment":"0|0|1|1",
                "four_iid_original_noise_signs":"|".join(map(str,eps)),
                "full_original_source_probability":"1/16",
                "four_true_Y0_FOR_AUDIT_ONLY":"|".join(str(y0(p,x)) for x in X),
                "four_true_Y1_FOR_AUDIT_ONLY":"|".join(str(potential(p,x,1)) for x in X),
                "true_tau_FOR_AUDIT_ONLY":str(tau),"true_untreated_jump_FOR_AUDIT_ONLY":str(jump),
                "four_expected_observed_values":"|".join(map(str,mean)),
                "four_actual_observed_values":"|".join(map(str,y))}
            for m,v in est.items():
                row[m+"_estimate"]=str(v)
                row[m+"_squared_error"]=str((v-tau)**2)
                accum[m]["E"]+=v/16
                accum[m]["E2"]+=v*v/16
                accum[m]["MSE"]+=(v-tau)**2/16
            rows.append(row)
        out={"world":name,"params_b_sl_sr_ql_qr_baselinejump_tau":list(p),
             "full_source_count":16,"full_source_probability_sum":"1",
             "true_threshold_tau_exact":str(tau),
             "oracle_true_untreated_baseline_discontinuity":str(jump),
             "oracle_observed_mean_jump":str(tau+jump),
             "four_point_observed_mean":"|".join(map(str,mean)),
             "full_joint_observable_distribution":outcome_dist(p)}
        for m,d in accum.items():
            mu=d["E"]; var=d["E2"]-mu**2; bias=mu-tau
            independent=sum((v*v for v in COEFF[m]),F(0))
            if mu!=analytic[m] or var!=independent or d["MSE"]!=bias*bias+var:
                raise AssertionError("exact source mean, variance or Brier identity")
            out[m]={"expected_estimate":str(mu),"bias":str(bias),
                    "noise_variance":str(var),"independent_coefficient_variance":str(independent),
                    "MSE":str(d["MSE"]),"bias_squared_plus_variance":str(bias*bias+var)}
        worlds.append(out)
    a,b=W["LINEAR_CAUSAL_TWO"],W["BASELINE_STEP_FALSE_CAUSAL"]
    if outcome_dist(a)!=outcome_dist(b) or a[-1]==b[-1]:
        raise AssertionError("observational equivalence and causal contrast")
    if len(rows)!=192:raise AssertionError("original source count")
    return {"research_id":"R214","catalogue_id":"09-005",
      "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
      "complete_source_worlds":12,"original_full_noise_source_records":192,
      "running_variable_grid":list(X),"cutoff":0,
      "precommitted_estimator_noise_variance":{m:str(sum((z*z for z in c),F(0))) for m,c in COEFF.items()},
      "all_original_source_probabilities_sum_one_each_world":True,
      "all_MSEs_exact_bias_square_plus_noise_variance":True,
      "equal_full_observable_distribution_different_tau_pair":["LINEAR_CAUSAL_TWO","BASELINE_STEP_FALSE_CAUSAL"],
      "density_manipulation_test_performed":False,"no_observations_near_arbitrarily_small_cutoff_distance":True,
      "new_real_human_E2":0,"new_real_historical_E3":0,"worlds":worlds},rows
def emit():
    r,rows=exact_results()
    a=OUT/"R214_EXACT_RESULTS.json"; b=OUT/"R214_ALL_192_ORIGINAL_RDD_NOISE_SOURCES.csv"
    a.write_text(json.dumps(r,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    with b.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    acceptance={"research_id":"R214","catalogue_id":"09-005","worlds":12,
      "original_full_noise_source_records":192,"iid_noise_three_estimator_variances_verified":True,
      "observational_equivalence_and_different_true_causal_effect_verified":True,
      "new_E2":0,"new_E3":0,
      "result_sha256":hashlib.sha256(a.read_bytes()).hexdigest(),
      "source_sha256":hashlib.sha256(b.read_bytes()).hexdigest()}
    (OUT/"R214_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(acceptance,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(acceptance,indent=2))
class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(W),12)
    def test_four_x(self):self.assertEqual(X,(-2,-1,1,2))
    def test_no_cutoff_obs(self):self.assertNotIn(0,X)
    def test_noise_sixteen(self):self.assertEqual(len(NOISE),16)
    def test_noise_mean_zero(self):
        for i in range(4):self.assertEqual(sum(e[i] for e in NOISE),0)
    def test_noise_offdiag_zero(self):
        for i in range(4):
            for j in range(4):
                if i!=j:self.assertEqual(sum(e[i]*e[j] for e in NOISE),0)
    def test_noisy_source_192(self):self.assertEqual(12*len(NOISE),192)
    def test_global_variance_one(self):self.assertEqual(sum(c*c for c in COEFF["GLOBAL"]),1)
    def test_nearest_variance_two(self):self.assertEqual(sum(c*c for c in COEFF["NEAREST"]),2)
    def test_linear_variance_ten(self):self.assertEqual(sum(c*c for c in COEFF["TWO_SIDED_LINEAR"]),10)
    def test_coeff_sums_zero(self):
        for c in COEFF.values():self.assertEqual(sum(c),0)
    def test_equal_observations(self):
        self.assertEqual(clean(W["LINEAR_CAUSAL_TWO"]),clean(W["BASELINE_STEP_FALSE_CAUSAL"]))
    def test_equal_observational_distribution(self):
        self.assertEqual(outcome_dist(W["LINEAR_CAUSAL_TWO"]),outcome_dist(W["BASELINE_STEP_FALSE_CAUSAL"]))
    def test_different_causal_tau(self):self.assertNotEqual(W["LINEAR_CAUSAL_TWO"][-1],W["BASELINE_STEP_FALSE_CAUSAL"][-1])
    def test_right_curvature_linear_bias(self):
        p=W["RIGHT_QUADRATIC"]
        self.assertEqual(score_all(clean(p))["TWO_SIDED_LINEAR"]-p[-1],-2)
    def test_matching_curvature_cancel(self):
        p=W["MATCHED_QUADRATIC"]
        self.assertEqual(score_all(clean(p))["TWO_SIDED_LINEAR"]-p[-1],0)
    def test_different_slopes_linear_consistent(self):
        p=W["DIFFERENT_SLOPES"]
        self.assertEqual(score_all(clean(p))["TWO_SIDED_LINEAR"],p[-1])
    def test_full_all(self):
        a,b=exact_results()
        self.assertEqual((len(a["worlds"]),len(b)),(12,192))
    def test_replay(self):self.assertEqual(exact_results(),exact_results())
def _check_specific_source(ix):
    def test(self):
        p=W[list(W)[ix%12]]
        eps=NOISE[ix%16]
        vals=source_noisy(p,eps)
        self.assertEqual(tuple(vals[i]-clean(p)[i] for i in range(4)),eps)
        self.assertEqual(len(score_all(vals)),3)
    return test
# Each test validates a distinct original (world, disturbance) source.
for _idx in range(20):
    setattr(Tests,"test_source_%02d"%_idx,_check_specific_source(_idx))
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--test",action="store_true")
    ap.add_argument("--emit",action="store_true")
    o=ap.parse_args()
    if o.test:
        r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if r.wasSuccessful() else 1)
    if o.emit:emit()
    if not o.test and not o.emit:ap.print_help()
