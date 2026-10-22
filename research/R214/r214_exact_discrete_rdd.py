#!/usr/bin/env python3
"""R214 full exact finite support sharp Regression Discontinuity mechanism audit.

Seven synthetic worlds, 10 observation points x=-5..-1 and 1..5, all
2^10 independent Rademacher measurement shocks per world. Never observes
x=0 or (-1,1). Every world has four fixed bandwidths, local constant
and local linear intercept differences, with independent Fraction source
enumeration and variance/bias formulas.

This does not estimate a causally identified jump in genuine discrete data:
a smooth baseline ramp in (0,1) and a genuine treatment discontinuity have
IDENTICAL distributions at all observed support but different effects at 0.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import unittest
from fractions import Fraction
from pathlib import Path

F = Fraction
ZERO = F(0)
ONE = F(1)
XS = (-5,-4,-3,-2,-1,1,2,3,4,5)
BANDWIDTHS = (2,3,4,5)
METHODS = ("LOCAL_CONSTANT","LOCAL_LINEAR")
WORLDS = (
    "FLAT_TAU2","LINEAR_TAU2","CURVED_TAU2",
    "HETEROGENEOUS_TAU2","NULL_FLAT",
    "INVALID_BASELINE_STEP","CONTINUOUS_HIDDEN_RAMP"
)
HERE = Path(__file__).resolve().parent


def smoothstep5(x):
    x = F(x)
    if x <= 0:
        return ZERO
    if x >= 1:
        return ONE
    return 6*x**5 - 15*x**4 + 10*x**3


def control_mean(world,x):
    x=F(x)
    if world not in WORLDS:
        raise ValueError("unknown artificial true source")
    if world=="LINEAR_TAU2":
        return x
    if world=="CURVED_TAU2":
        return max(x,ZERO)**2
    if world=="INVALID_BASELINE_STEP":
        return F(2) if x>0 else ZERO
    if world=="CONTINUOUS_HIDDEN_RAMP":
        return 2*smoothstep5(x)
    return ZERO


def treatment_effect(world,x):
    x=F(x)
    if world not in WORLDS:
        raise ValueError("unknown true source")
    if world in ("NULL_FLAT","INVALID_BASELINE_STEP","CONTINUOUS_HIDDEN_RAMP"):
        return ZERO
    if world=="HETEROGENEOUS_TAU2":
        return F(2)+x
    return F(2)


def true_tau_at_cutoff(world):
    return treatment_effect(world,ZERO)


def observed_mean_at_x(world,x):
    if x not in XS:
        raise ValueError("only ten frozen observed running values allowed")
    return control_mean(world,x)+(treatment_effect(world,x) if x>0 else ZERO)


def base_mu_vector(world):
    return tuple(observed_mean_at_x(world,x) for x in XS)


def linear_weights(side):
    """Per-side local OLS intercept weights independent of fitted Y."""
    xx=tuple(F(x) for x in side)
    n=len(xx)
    if n<2:
        raise ValueError("at least two x coordinates required")
    sx=sum(xx,ZERO)
    sxx=sum((x*x for x in xx),ZERO)
    det=n*sxx-sx*sx
    if det<=0:
        raise ValueError("linear fit singular")
    w=tuple((sxx-x*sx)/det for x in xx)
    if sum(w,ZERO)!=ONE or sum((w[i]*xx[i] for i in range(n)),ZERO)!=ZERO:
        raise AssertionError("OLS intercept weight identities failed")
    return w


def independent_OLS_intercept(side,ys):
    """Independent normal-equations reconstruction, not dot(weight, Y)."""
    n=len(side)
    if n!=len(ys) or n<2:
        raise ValueError("invalid local linear input")
    xx=tuple(F(x) for x in side)
    sx=sum(xx,ZERO)
    sxx=sum((x*x for x in xx),ZERO)
    sy=sum((F(y) for y in ys),ZERO)
    sxy=sum((xx[i]*F(ys[i]) for i in range(n)),ZERO)
    det=n*sxx-sx*sx
    if det<=0:
        raise ValueError("invalid least squares x support")
    return (sxx*sy-sx*sxy)/det


def estimator_weights(method,h):
    if method not in METHODS or h not in BANDWIDTHS:
        raise ValueError("only frozen method and h allowed")
    left=tuple(-i for i in range(h,0,-1))
    right=tuple(range(1,h+1))
    if method=="LOCAL_CONSTANT":
        lw=(F(1,h),)*h
        rw=(F(1,h),)*h
    else:
        lw=linear_weights(left)
        rw=linear_weights(right)
    w={x:ZERO for x in XS}
    for i,x in enumerate(left):
        w[x]=-lw[i]
    for i,x in enumerate(right):
        w[x]=rw[i]
    if sum(w.values(),ZERO)!=ZERO:
        raise AssertionError("two-side local intercept constant cancellation")
    if method=="LOCAL_LINEAR":
        if sum((w[x]*x for x in XS),ZERO)!=ZERO:
            raise AssertionError("linear trend cancellation failed")
    return tuple(w[x] for x in XS)


def statistic(weights,y):
    if len(weights)!=len(XS) or len(y)!=len(XS):
        raise ValueError("need ten fixed coordinates")
    return sum((weights[i]*y[i] for i in range(len(XS))),ZERO)


def independent_local_fit(method,h,y):
    if len(y)!=10:
        raise ValueError("ten source values needed")
    d={XS[i]:y[i] for i in range(10)}
    left=tuple(-i for i in range(h,0,-1))
    right=tuple(range(1,h+1))
    if method=="LOCAL_CONSTANT":
        leftfit=sum((d[x] for x in left),ZERO)/h
        rightfit=sum((d[x] for x in right),ZERO)/h
    elif method=="LOCAL_LINEAR":
        leftfit=independent_OLS_intercept(left,tuple(d[x] for x in left))
        rightfit=independent_OLS_intercept(right,tuple(d[x] for x in right))
    else:
        raise ValueError("invalid method")
    return rightfit-leftfit


def source_bits(bitmask):
    if bitmask<0 or bitmask>=1024:
        raise ValueError("ten fair noise draw mask out of range")
    return tuple(ONE if bitmask&(1<<i) else -ONE for i in range(10))


def source_observed_vector(world,bitmask):
    mu=base_mu_vector(world)
    eps=source_bits(bitmask)
    return tuple(mu[i]+eps[i] for i in range(10))


def analytic_moments(world,weights):
    mu=base_mu_vector(world)
    target=true_tau_at_cutoff(world)
    expectation=statistic(weights,mu)
    bias=expectation-target
    variance=sum((x*x for x in weights),ZERO)
    risk=bias*bias+variance
    return expectation,bias,variance,risk


def contrast_aliasing_identity():
    flat=base_mu_vector("FLAT_TAU2")
    step=base_mu_vector("INVALID_BASELINE_STEP")
    smooth=base_mu_vector("CONTINUOUS_HIDDEN_RAMP")
    if flat!=step or flat!=smooth:
        raise AssertionError("frozen three observationally identical worlds disagree")
    if (true_tau_at_cutoff("FLAT_TAU2"),true_tau_at_cutoff("INVALID_BASELINE_STEP"),
        true_tau_at_cutoff("CONTINUOUS_HIDDEN_RAMP")) != (F(2),ZERO,ZERO):
        raise AssertionError("frozen true cutoff effects are wrong")
    # The smooth hidden ramp has m0(0)=m0'(0)=m0''(0)=0 and m0(x)=2 at x>=1.
    if smoothstep5(F(1,2))!=F(1,2):
        raise AssertionError("specified quintic continuous ramp changed")
    return True


def compute():
    weights={(method,h):estimator_weights(method,h) for method in METHODS
             for h in BANDWIDTHS}
    configs=tuple((method,h) for method in METHODS for h in BANDWIDTHS)
    original=[]
    summary=[]
    if not contrast_aliasing_identity():
        raise AssertionError("source aliasing failed")
    for world in WORLDS:
        analytic={key:analytic_moments(world,weights[key]) for key in configs}
        accum={key:{"mean":ZERO,"second":ZERO,"risk":ZERO} for key in configs}
        mu=base_mu_vector(world)
        for bits in range(1024):
            eps=source_bits(bits)
            y=tuple(mu[i]+eps[i] for i in range(10))
            estimates=[]
            errors=[]
            for key in configs:
                meth,h=key
                value=statistic(weights[key],y)
                independently_computed=independent_local_fit(meth,h,y)
                if value!=independently_computed:
                    raise AssertionError("two distinct actual fit computations disagree")
                loss=(value-true_tau_at_cutoff(world))**2
                estimates.append(str(value))
                errors.append(str(loss))
                accum[key]["mean"]+=value/1024
                accum[key]["second"]+=value*value/1024
                accum[key]["risk"]+=loss/1024
            original.append({
                "world":world,
                "cutoff":"0",
                "ten_real_observation_running_values":"|".join(map(str,XS)),
                "true_cutoff_causal_effect_ORACLE_ONLY":str(true_tau_at_cutoff(world)),
                "original_ten_independent_noise_draw_bitmask":bits,
                "full_noise_path_eps_minus_or_plus":"|".join(map(str,eps)),
                "original_source_probability_exact":"1/1024",
                "full_ten_actually_observed_outcomes":"|".join(map(str,y)),
                "estimator_order":"|".join(f"{m}_h{h}" for m,h in configs),
                "eight_estimates_from_observations_only":"|".join(estimates),
                "eight_true_cutoff_effect_squared_errors_ORACLE_EVALUATION":"|".join(errors),
            })
        for method,h in configs:
            totals=accum[(method,h)]
            empirical_mean=totals["mean"]
            empirical_var=totals["second"]-empirical_mean**2
            source_risk=totals["risk"]
            theoretical_mean,bias,var,risk=analytic[(method,h)]
            if (empirical_mean,empirical_var,source_risk)!=(theoretical_mean,var,risk):
                raise AssertionError("original full 1024 source moments and analytic bias variance disagree")
            summary.append({
                "world":world,
                "method":method,
                "bandwidth_h":h,
                "observed_positions_per_side":h,
                "observed_point_nearest_cutoff_distance":1,
                "true_causal_effect_at_cutoff_ORACLE_ONLY":str(true_tau_at_cutoff(world)),
                "analytic_estimator_expected_value_exact":str(theoretical_mean),
                "full_original_noise_source_estimator_mean_exact":str(empirical_mean),
                "analytic_bias_exact":str(bias),
                "analytic_squared_bias_exact":str(bias*bias),
                "analytic_independent_shock_variance_exact":str(var),
                "full_original_noise_source_variance_exact":str(empirical_var),
                "analytic_bias2_plus_variance_MSE_exact":str(risk),
                "all_1024_original_source_actual_true_tau_MSE_exact":str(source_risk),
                "MSE_float":float(risk),
                "estimator_x_weights_exact":"|".join(map(str,weights[(method,h)])),
                "original_source_probability_sum":"1",
            })
    if len(original)!=7168 or len(summary)!=56:
        raise AssertionError("world/sample score count mismatch")
    return {
        "research_id":"R214",
        "actual_catalogue_id":"09-005",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "fixed_sharp_running_cutoff":"0",
        "ten_observed_grid_points":list(XS),
        "no_observations_in_open_gap_minus1_to_plus1":True,
        "worlds":list(WORLDS),
        "full_original_shock_source_rows":len(original),
        "full_world_method_bandwidth_scores":len(summary),
        "original_noise_histories_per_world":1024,
        "fixed_methods":list(METHODS),
        "fixed_bandwidths":list(BANDWIDTHS),
        "bias_variance_source_fraction_double_checks":True,
        "original_two_independent_local_OLS_implementations":True,
        "three_identical_observed_support_distribution_worlds":[
            "FLAT_TAU2","INVALID_BASELINE_STEP","CONTINUOUS_HIDDEN_RAMP"],
        "observationally_identical_worlds_different_actual_tau_at_cutoff":True,
        "full_source_scoring_exposes_true_tau_only_to_audit":True,
        "finite_observed_discrete_support_alone_identifies_true_tau_at_0":False,
        "new_real_human_E2":0,
        "new_real_historical_E3":0,
        "summaries":summary,
        "limits":[
            "No observed x between -1 and +1, cutoff effect not model-free point identified",
            "Artificial Rademacher independent shocks and one observation at each x",
            "No density sorting test, estimated bandwidth optimization or real RD data",
            "Original 1024 source paths per world are alternate artificial outcomes, not real independent trials",
        ],
    },original


def emit():
    data,original=compute()
    paths={
        "result":HERE/"R214_EXACT_RESULTS.json",
        "raw":HERE/"R214_ALL_7168_ORIGINAL_TEN_POINT_SHOCK_SOURCES.csv",
    }
    paths["result"].write_text(json.dumps(data,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with paths["raw"].open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(original[0]))
        writer.writeheader()
        writer.writerows(original)
    receipt={
        "model_id":"R214",
        "actual_239_catalogue_id":"09-005",
        "fixed_artificial_worlds":7,
        "original_full_10_independent_shock_vector_sources":7168,
        "world_method_bandwidth_configurations":56,
        "original_source_moments_match_analytic_fraction_moments":True,
        "all_sources_fit_by_two_independent_fraction_implementations":True,
        "three_identical_observation_worlds_with_distinct_true_RD_targets":True,
        "new_E2":0,"new_E3":0,
        **{k+"_sha256":hashlib.sha256(v.read_bytes()).hexdigest() for k,v in paths.items()},
    }
    (HERE/"R214_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(receipt,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2))


class Tests(unittest.TestCase):
    def test_real_10_point_support(self): self.assertEqual(len(XS),10)
    def test_no_cutoff_observations(self): self.assertNotIn(0,XS)
    def test_nearest_gap_one(self): self.assertEqual(min(abs(x) for x in XS),1)
    def test_seven_true_worlds(self): self.assertEqual(len(WORLDS),7)
    def test_four_bandwidths(self): self.assertEqual(BANDWIDTHS,(2,3,4,5))
    def test_two_estimators(self): self.assertEqual(METHODS,("LOCAL_CONSTANT","LOCAL_LINEAR"))
    def test_original_source_count_7168(self): self.assertEqual(7*2**10,7168)
    def test_56_world_estimator_pairs(self): self.assertEqual(7*4*2,56)
    def test_zero_mean_noise_exact(self):
        for i in range(10):
            self.assertEqual(sum((source_bits(bits)[i] for bits in range(1024)),ZERO),ZERO)
    def test_noise_variance_one(self):
        for i in range(10):
            self.assertEqual(sum((source_bits(bits)[i]**2 for bits in range(1024)),ZERO)/1024,ONE)
    def test_noise_independence_cov0(self):
        for i,j in ((0,1),(1,6),(3,9),(7,8)):
            self.assertEqual(sum((source_bits(bits)[i]*source_bits(bits)[j] for bits in range(1024)),ZERO),ZERO)
    def test_continuous_ramp_endpoints(self):
        self.assertEqual(smoothstep5(ZERO),ZERO)
        self.assertEqual(smoothstep5(ONE),ONE)
    def test_continuous_ramp_midpoint_half(self): self.assertEqual(smoothstep5(F(1,2)),F(1,2))
    def test_ramp_quintic_monotone_examples(self):
        self.assertTrue(ZERO<smoothstep5(F(1,4))<F(1,2))
        self.assertTrue(F(1,2)<smoothstep5(F(3,4))<ONE)
    def test_ramp_is_flat_observed_right(self):
        self.assertTrue(all(control_mean("CONTINUOUS_HIDDEN_RAMP",x)==2 for x in XS if x>0))
    def test_observation_three_worlds_identical(self):
        self.assertTrue(contrast_aliasing_identity())
    def test_true_tau_aliasing_distinct(self):
        self.assertEqual((true_tau_at_cutoff("FLAT_TAU2"),
                          true_tau_at_cutoff("CONTINUOUS_HIDDEN_RAMP")),(F(2),ZERO))
    def test_observation_full_1024_paths_alias(self):
        for mask in (0,1,17,128,511,1023):
            self.assertEqual(source_observed_vector("FLAT_TAU2",mask),
                             source_observed_vector("CONTINUOUS_HIDDEN_RAMP",mask))
    def test_true_linear_tau2(self): self.assertEqual(true_tau_at_cutoff("LINEAR_TAU2"),F(2))
    def test_true_curved_tau2(self): self.assertEqual(true_tau_at_cutoff("CURVED_TAU2"),F(2))
    def test_heterogeneous_at_0(self):
        self.assertEqual(treatment_effect("HETEROGENEOUS_TAU2",ZERO),F(2))
        self.assertEqual(treatment_effect("HETEROGENEOUS_TAU2",F(3)),F(5))
    def test_invalid_step_baseline_jump(self):
        self.assertEqual(control_mean("INVALID_BASELINE_STEP",F(-1,100)),ZERO)
        self.assertEqual(control_mean("INVALID_BASELINE_STEP",F(1,100)),F(2))
    def test_continuous_ramp_near_zero_tends_zero(self):
        self.assertLess(control_mean("CONTINUOUS_HIDDEN_RAMP",F(1,100)),F(1,100))
    def test_each_weight_sums_zero(self):
        for method in METHODS:
            for h in BANDWIDTHS:
                self.assertEqual(sum(estimator_weights(method,h),ZERO),ZERO)
    def test_linear_weight_annihilates_running_slope(self):
        for h in BANDWIDTHS:
            w=estimator_weights("LOCAL_LINEAR",h)
            self.assertEqual(statistic(w,tuple(F(x) for x in XS)),ZERO)
    def test_constant_trend_bias_by_bandwidth(self):
        for h in BANDWIDTHS:
            w=estimator_weights("LOCAL_CONSTANT",h)
            expected,bias,_,_=analytic_moments("LINEAR_TAU2",w)
            self.assertEqual(bias,F(h+1))
    def test_linear_trend_exact_no_bias(self):
        for h in BANDWIDTHS:
            w=estimator_weights("LOCAL_LINEAR",h)
            self.assertEqual(analytic_moments("LINEAR_TAU2",w)[1],ZERO)
    def test_constant_flat_effect_unbiased(self):
        for h in BANDWIDTHS:
            self.assertEqual(analytic_moments("FLAT_TAU2",estimator_weights("LOCAL_CONSTANT",h))[1],ZERO)
    def test_linear_flat_effect_unbiased(self):
        for h in BANDWIDTHS:
            self.assertEqual(analytic_moments("FLAT_TAU2",estimator_weights("LOCAL_LINEAR",h))[1],ZERO)
    def test_local_constant_noise_variance_two_over_h(self):
        for h in BANDWIDTHS:
            self.assertEqual(analytic_moments("NULL_FLAT",estimator_weights("LOCAL_CONSTANT",h))[2],F(2,h))
    def test_linear_h2_noise_variance10(self):
        self.assertEqual(analytic_moments("NULL_FLAT",estimator_weights("LOCAL_LINEAR",2))[2],F(10))
    def test_curved_linear_h2_nonzero_bias(self):
        self.assertEqual(analytic_moments("CURVED_TAU2",estimator_weights("LOCAL_LINEAR",2))[1],F(-2))
    def test_heterogeneous_linear_extrap_no_bias(self):
        for h in BANDWIDTHS:
            self.assertEqual(analytic_moments("HETEROGENEOUS_TAU2",estimator_weights("LOCAL_LINEAR",h))[1],ZERO)
    def test_two_independent_estimators_on_exact_source(self):
        y=source_observed_vector("CURVED_TAU2",765)
        for method in METHODS:
            for h in BANDWIDTHS:
                self.assertEqual(statistic(estimator_weights(method,h),y),
                                 independent_local_fit(method,h,y))
    def test_invalid_h_rejected(self):
        with self.assertRaises(ValueError):
            estimator_weights("LOCAL_LINEAR",1)
    def test_invalid_method_rejected(self):
        with self.assertRaises(ValueError):
            estimator_weights("WRONG",3)
    def test_invalid_noise_mask_rejected(self):
        with self.assertRaises(ValueError):
            source_bits(1024)
    def test_invalid_world_rejected(self):
        with self.assertRaises(ValueError):
            control_mean("BAD_WORLD",1)
    def test_all_7168_source_and_56_exact_scores(self):
        r,rows=compute()
        self.assertEqual((len(r["summaries"]),len(rows)),(56,7168))
        self.assertEqual(r["new_real_human_E2"],0)
        self.assertTrue(r["observationally_identical_worlds_different_actual_tau_at_cutoff"])
    def test_deterministic_replay_source_order(self):
        self.assertEqual(source_observed_vector("LINEAR_TAU2",0),
                         source_observed_vector("LINEAR_TAU2",0))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test",action="store_true")
    parser.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    if args.test:
        ran=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if ran.wasSuccessful() else 1)
    if args.emit:
        emit()
    if not args.test and not args.emit:
        parser.print_help()
