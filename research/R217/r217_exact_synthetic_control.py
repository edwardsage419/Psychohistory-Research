#!/usr/bin/env python3
"""R217 synthetic control, full finite pre-training and independent post shock audit.

Eight fixed artificial design worlds, one treated series, three donors, 3
preperiods and two postperiods. Optimize 15 quarter-grid convex donor weights
ONLY on noisy pre-period T values, then evaluate genuinely independently drawn
post-period T and D1 shocks for the SAME artificial treated/donor units.

All source-weighted causal effect errors use the TRUE ARTIFICIAL counterfactual
solely as an auditor. Not real human or historical evidence; no unrestricted
continuous synthetic-control optimization or original authors' data.
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
PRE = (0,1,2)
POST = (3,4)
WORLDS = (
    "VALID_TAU2",
    "VALID_ZERO",
    "VALID_MINUS2",
    "VALID_DYNAMIC",
    "DONOR_POST_CONTAMINATION",
    "UNTREATED_POST_SHOCK_MIMIC",
    "UNTREATED_POST_DRIFT",
    "PRE_FIT_MISMATCH",
)
DONOR_PRE = ((F(0),F(0),F(0)),(F(0),F(2),F(4)),(F(2),F(1),F(0)))
DONOR_POST_CLEAN = ((F(0),F(0)),(F(6),F(8)),(F(-2),F(-2)))
WEIGHTS = tuple((F(a,4),F(b,4),F(c,4))
                for a in range(5) for b in range(5-a) for c in range(5-a-b)
                if a+b+c==4)
STRUCTURAL_ORACLE_WEIGHTS = (F(1,2),F(1,2),ZERO)
SINGLE_D0 = (ONE,ZERO,ZERO)
OUT = Path(__file__).resolve().parent


def valid_world(world):
    if world not in WORLDS:
        raise ValueError("not a frozen synthetic control world")


def treatment_pre_base(world):
    valid_world(world)
    return (ZERO,ONE,F(3)) if world=="PRE_FIT_MISMATCH" else (ZERO,ONE,F(2))


def counterfactual_post(world):
    valid_world(world)
    if world=="UNTREATED_POST_SHOCK_MIMIC":
        return (F(5),F(6))
    if world=="UNTREATED_POST_DRIFT":
        return (F(4),F(6))
    return (F(3),F(4))


def true_treatment_effect_post(world):
    valid_world(world)
    if world in ("VALID_ZERO","UNTREATED_POST_SHOCK_MIMIC",
                 "UNTREATED_POST_DRIFT","PRE_FIT_MISMATCH"):
        return (ZERO,ZERO)
    if world=="VALID_MINUS2":
        return (F(-2),F(-2))
    if world=="VALID_DYNAMIC":
        return (ONE,F(3))
    return (F(2),F(2))


def donor_post_mean(world):
    valid_world(world)
    base=list(DONOR_POST_CLEAN)
    if world=="DONOR_POST_CONTAMINATION":
        base[1]=(F(8),F(10))
    return tuple(base)


def noise_source(bits,n):
    if type(bits) is not int or type(n) is not int or not 0<=bits<2**n:
        raise ValueError("finite independent sign source outside grid")
    return tuple(F(1,4) if bits&(1<<i) else F(-1,4)
                 for i in range(n))


def training_values(world,bits):
    eps=noise_source(bits,3)
    base=treatment_pre_base(world)
    return tuple(base[i]+eps[i] for i in range(3))


def convex_predict(weights, donor_vectors, period_ix):
    if len(weights)!=3 or len(donor_vectors)!=3:
        raise ValueError("three donors and three weights required")
    return sum((weights[j]*donor_vectors[j][period_ix] for j in range(3)),ZERO)


def train_loss(weights,t_obs):
    if len(t_obs)!=3:
        raise ValueError("three fixed pre outcomes")
    return sum((t_obs[k]-convex_predict(weights,DONOR_PRE,k))**2 for k in range(3))


def chosen_pre_weights(observed_pre):
    """Global optimum of all 15 QUARTER-GRID candidate combinations only."""
    if len(observed_pre)!=3:
        raise ValueError("pre history must contain three values")
    best=min(WEIGHTS,key=lambda w:(train_loss(w,observed_pre),w))
    if any(train_loss(w,observed_pre)<train_loss(best,observed_pre) for w in WEIGHTS):
        raise AssertionError("not actual global grid-optimal pre fit")
    return best


def post_sample(world,bits):
    epsT3,epsT4,epsD3,epsD4=noise_source(bits,4)
    true_y0=counterfactual_post(world)
    tau=true_treatment_effect_post(world)
    actual_T=(true_y0[0]+tau[0]+epsT3,true_y0[1]+tau[1]+epsT4)
    donors=list(donor_post_mean(world))
    donors[1]=(donors[1][0]+epsD3,donors[1][1]+epsD4)
    return actual_T,tuple(donors)


def estimated_effect(weights,t_post,donor_post):
    return tuple(t_post[k]-convex_predict(weights,donor_post,k) for k in range(2))


def squared_causal_error(world,estimated):
    tau=true_treatment_effect_post(world)
    return sum(((estimated[k]-tau[k])**2 for k in range(2)),ZERO)/2


def analytic_independent_new_shock_risk(world,weights):
    """Conditioned on frozen training-only weights: unrelated heldout shock."""
    target_y0=counterfactual_post(world)
    donor_mu=donor_post_mean(world)
    bias=(target_y0[0]-convex_predict(weights,donor_mu,0),
          target_y0[1]-convex_predict(weights,donor_mu,1))
    variance=(ONE+weights[1]*weights[1])/16
    return ((bias[0]*bias[0]+bias[1]*bias[1])/2+variance,
            (bias[0]+bias[1])/2,variance)


def source_aliasing():
    # All actual measured treatment and donor outcomes are IDENTICAL
    # under two causal counterfactuals with different true effects.
    if (treatment_pre_base("VALID_TAU2") !=
        treatment_pre_base("UNTREATED_POST_SHOCK_MIMIC")):
        raise AssertionError("source observed pre distributions are not aliases")
    if (donor_post_mean("VALID_TAU2") !=
        donor_post_mean("UNTREATED_POST_SHOCK_MIMIC")):
        raise AssertionError("observed donor post mismatch")
    for bits in range(16):
        if post_sample("VALID_TAU2",bits)!=post_sample("UNTREATED_POST_SHOCK_MIMIC",bits):
            raise AssertionError("complete observed joint future sources are not equal")
    if (true_treatment_effect_post("VALID_TAU2") ==
        true_treatment_effect_post("UNTREATED_POST_SHOCK_MIMIC")):
        raise AssertionError("true effect should differ under same visible data")
    return True


def compute():
    source_aliasing()
    records=[]
    worlds=[]
    for world in WORLDS:
        totals={name:ZERO for name in
                ("TRAINING_SSE","SYNTH_CAUSAL_MSE",
                 "FIXED_ORACLE_W_CAUSAL_MSE","SINGLE_D0_CAUSAL_MSE")}
        exact_train_zero=ZERO
        selected_weights={}
        for pre_bits in range(8):
            train_obs=training_values(world,pre_bits)
            w=chosen_pre_weights(train_obs)
            train_sse=train_loss(w,train_obs)
            totals["TRAINING_SSE"]+=train_sse/8
            if train_sse==0:
                exact_train_zero+=F(1,8)
            selected_weights["|".join(map(str,w))]=(
                selected_weights.get("|".join(map(str,w)),ZERO)+F(1,8))
            future_risk=ZERO
            for post_bits in range(16):
                t_post,donor_post=post_sample(world,post_bits)
                pred=estimated_effect(w,t_post,donor_post)
                oracle_pred=estimated_effect(STRUCTURAL_ORACLE_WEIGHTS,t_post,donor_post)
                d0pred=estimated_effect(SINGLE_D0,t_post,donor_post)
                loss=squared_causal_error(world,pred)
                loss_oracle=squared_causal_error(world,oracle_pred)
                loss_d0=squared_causal_error(world,d0pred)
                future_risk+=loss/16
                totals["SYNTH_CAUSAL_MSE"]+=loss/128
                totals["FIXED_ORACLE_W_CAUSAL_MSE"]+=loss_oracle/128
                totals["SINGLE_D0_CAUSAL_MSE"]+=loss_d0/128
                records.append({
                    "world":world,
                    "original_training_three_signs_bitmask":pre_bits,
                    "independent_new_four_signs_bitmask":post_bits,
                    "true_joint_train_independent_new_source_probability":"1/128",
                    "actual_pre_T_observed_three_values":"|".join(map(str,train_obs)),
                    "fixed_pre_donor_D0":"|".join(map(str,DONOR_PRE[0])),
                    "fixed_pre_donor_D1":"|".join(map(str,DONOR_PRE[1])),
                    "fixed_pre_donor_D2":"|".join(map(str,DONOR_PRE[2])),
                    "training_only_selected_three_convex_weights":"|".join(map(str,w)),
                    "actual_fitted_training_pre_SSE_exact":str(train_sse),
                    "independent_future_true_T_observed":"|".join(map(str,t_post)),
                    "independent_future_actual_three_donor_series":"|".join(
                        "/".join(map(str,series)) for series in donor_post),
                    "independent_future_hidden_counterfactual_T0_ORACLE_ONLY":
                        "|".join(map(str,counterfactual_post(world))),
                    "independent_future_actual_true_causal_effect_ORACLE_ONLY":
                        "|".join(map(str,true_treatment_effect_post(world))),
                    "independent_future_SCM_both_effect_estimates":"|".join(map(str,pred)),
                    "independent_future_SC_effect_estimation_MSE_exact":str(loss),
                    "independent_future_fixed_oracle_half_half_effect_MSE_exact":str(loss_oracle),
                    "independent_future_simple_D0_effect_MSE_exact":str(loss_d0),
                })
            analytic_risk,bias,variance=analytic_independent_new_shock_risk(world,w)
            if future_risk!=analytic_risk:
                raise AssertionError("independent 16-source full risk != analytic risk for pre-selected weights")
        if sum(selected_weights.values(),ZERO)!=ONE:
            raise AssertionError("incomplete train sample weighting")
        fixed_oracle_analytic=analytic_independent_new_shock_risk(
            world,STRUCTURAL_ORACLE_WEIGHTS)[0]
        fixed_d0_analytic=analytic_independent_new_shock_risk(world,SINGLE_D0)[0]
        if (totals["FIXED_ORACLE_W_CAUSAL_MSE"]!=fixed_oracle_analytic or
            totals["SINGLE_D0_CAUSAL_MSE"]!=fixed_d0_analytic):
            raise AssertionError("fixed donors double source risk check failed")
        worlds.append({
            "world":world,
            "independent_training_source_paths":8,
            "new_source_outcomes_per_training_history":16,
            "full_original_joint_source_probability_sum":"1",
            "actual_true_t3_t4_effect_ORACLE_ONLY":
                "|".join(map(str,true_treatment_effect_post(world))),
            "actual_hidden_t3_t4_counterfactual_ORACLE_ONLY":
                "|".join(map(str,counterfactual_post(world))),
            "mean_training_SSE_exact":str(totals["TRAINING_SSE"]),
            "probability_training_SSE_exactly_zero":str(exact_train_zero),
            "selected_weight_probabilities_exact":{
                k:str(v) for k,v in sorted(selected_weights.items())},
            "independent_future_selected_SC_effect_MSE_exact":
                str(totals["SYNTH_CAUSAL_MSE"]),
            "independent_future_fixed_half_half_effect_MSE_exact":
                str(totals["FIXED_ORACLE_W_CAUSAL_MSE"]),
            "independent_future_single_D0_effect_MSE_exact":
                str(totals["SINGLE_D0_CAUSAL_MSE"]),
            "independent_future_selected_SC_effect_MSE":
                float(totals["SYNTH_CAUSAL_MSE"]),
        })
    if len(records)!=1024 or len(worlds)!=8:
        raise AssertionError("incomplete 8world x8pre x16post original sources")
    return {
        "research_id":"R217",
        "source_catalogue_id":"09-008",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "source_reference_doi":"10.1198/jasa.2009.ap08746",
        "true_world_count":len(WORLDS),
        "true_source_training_noise_paths":8,
        "true_source_future_noise_paths":16,
        "full_original_train_independent_future_source_pairs":len(records),
        "preperiods":[0,1,2],
        "postperiods":[3,4],
        "donor_count":3,
        "full_fixed_quarter_weight_grid_count":len(WEIGHTS),
        "conditional_new_source_MSE_vs_independent_analytic_Fraction_check":True,
        "fully_identical_actual_source_joint_distributions_but_different_true_effects":
            ["VALID_TAU2","UNTREATED_POST_SHOCK_MIMIC"],
        "future_true_effect_is_hidden_from_pre_weight_selection":True,
        "oracle_weights_are_fixed_structural_prior_not_result_selected":True,
        "future_outcomes_are_independent_noise_for_same_fixed_groups":True,
        "new_real_human_E2":0,
        "new_real_historical_E3":0,
        "worlds":worlds,
        "limits":[
            "Only 15 quarter-grid convex donor weight hypotheses, not a continuous optimizer",
            "Treated t3/t4 no-treatment outcomes are oracle artificial facts, never real observed causal data",
            "New shocks independent of pre; fixed groups and donor structural paths persist",
            "No full original synthetic-control algorithms nor original author case studies",
        ],
    },records


def emit():
    r,rows=compute()
    p_json=OUT/"R217_EXACT_RESULTS.json"
    p_csv=OUT/"R217_ALL_1024_ORIGINAL_INDEPENDENT_PRE_POST_SOURCE_PAIRS.csv"
    p_json.write_text(
        json.dumps(r,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    with p_csv.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    receipt={
        "research_id":"R217",
        "real_original_catalogue_id":"09-008",
        "artificial_worlds":8,
        "complete_training_sources_per_world":8,
        "independent_new_source_per_training":16,
        "complete_original_independent_pre_post_source_pairs":1024,
        "all_eight_worlds_source_prob_sum_one":True,
        "independent_new_full_source_MSE_equals_fraction_analytic_expected_risk":True,
        "actual_observed_joint_equivalence_different_true_effects":True,
        "new_E2":0,"new_E3":0,
        "results_sha256":hashlib.sha256(p_json.read_bytes()).hexdigest(),
        "all_source_sha256":hashlib.sha256(p_csv.read_bytes()).hexdigest(),
    }
    (OUT/"R217_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(receipt,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2))


class Tests(unittest.TestCase):
    def test_eight_true_worlds(self): self.assertEqual(len(WORLDS),8)
    def test_three_donors(self): self.assertEqual(len(DONOR_PRE),3)
    def test_three_train_periods(self): self.assertEqual(len(PRE),3)
    def test_two_new_periods(self): self.assertEqual(len(POST),2)
    def test_fifteen_convex_candidates(self): self.assertEqual(len(WEIGHTS),15)
    def test_all_candidate_weights_nonnegative(self):
        self.assertTrue(all(min(w)>=0 for w in WEIGHTS))
    def test_all_candidate_weights_sum_one(self):
        self.assertTrue(all(sum(w,ZERO)==ONE for w in WEIGHTS))
    def test_oracle_half_half_on_grid(self):
        self.assertIn(STRUCTURAL_ORACLE_WEIGHTS,WEIGHTS)
    def test_unique_pre_no_noise_half_half(self):
        self.assertEqual(chosen_pre_weights((ZERO,ONE,F(2))),STRUCTURAL_ORACLE_WEIGHTS)
    def test_zero_sse_without_noise_exact(self):
        self.assertEqual(train_loss(STRUCTURAL_ORACLE_WEIGHTS,(ZERO,ONE,F(2))),ZERO)
    def test_three_sources_pre_signs(self):
        self.assertEqual(len(noise_source(0,3)),3)
    def test_four_sources_new_signs(self):
        self.assertEqual(len(noise_source(0,4)),4)
    def test_noise_plus_minus_quarter(self):
        self.assertEqual(noise_source(0,3),(F(-1,4),)*3)
        self.assertEqual(noise_source(7,3),(F(1,4),)*3)
    def test_all_training_source_count(self):
        self.assertEqual(8*2**3*2**4,1024)
    def test_valid_tau2_true(self):
        self.assertEqual(true_treatment_effect_post("VALID_TAU2"),(F(2),F(2)))
    def test_valid_zero_true(self):
        self.assertEqual(true_treatment_effect_post("VALID_ZERO"),(ZERO,ZERO))
    def test_valid_negative_effect(self):
        self.assertEqual(true_treatment_effect_post("VALID_MINUS2"),(F(-2),F(-2)))
    def test_valid_dynamic_effect(self):
        self.assertEqual(true_treatment_effect_post("VALID_DYNAMIC"),(ONE,F(3)))
    def test_clean_oracle_counterfactual(self):
        self.assertEqual(counterfactual_post("VALID_TAU2"),(F(3),F(4)))
    def test_hidden_post_shock_counterfactual(self):
        self.assertEqual(counterfactual_post("UNTREATED_POST_SHOCK_MIMIC"),(F(5),F(6)))
    def test_full_observation_identical_true_effects_different(self):
        self.assertTrue(source_aliasing())
    def test_donor_contamination_new_D1_means(self):
        self.assertEqual(donor_post_mean("DONOR_POST_CONTAMINATION")[1],(F(8),F(10)))
    def test_other_donor_clean(self):
        self.assertEqual(donor_post_mean("VALID_TAU2")[1],(F(6),F(8)))
    def test_baseline_selected_training_only(self):
        for bits in range(8):
            w=chosen_pre_weights(training_values("VALID_TAU2",bits))
            self.assertIn(w,WEIGHTS)
            self.assertEqual(train_loss(w,training_values("VALID_TAU2",bits)),
                             min(train_loss(v,training_values("VALID_TAU2",bits)) for v in WEIGHTS))
    def test_independent_full_future_risk_two_routes(self):
        for world in WORLDS:
            for bits in range(8):
                w=chosen_pre_weights(training_values(world,bits))
                actual=sum((squared_causal_error(world,estimated_effect(w,*post_sample(world,j)))
                            for j in range(16)),ZERO)/16
                self.assertEqual(actual,analytic_independent_new_shock_risk(world,w)[0])
    def test_oracle_fraction_future_shock_variance(self):
        self.assertEqual(analytic_independent_new_shock_risk(
            "VALID_TAU2",STRUCTURAL_ORACLE_WEIGHTS)[2],F(5,64))
    def test_single_D0_fraction_future_shock_variance(self):
        self.assertEqual(analytic_independent_new_shock_risk(
            "VALID_TAU2",SINGLE_D0)[2],F(1,16))
    def test_future_independent_same_pre(self):
        w=chosen_pre_weights(training_values("VALID_TAU2",3))
        self.assertEqual(w,chosen_pre_weights(training_values("VALID_TAU2",3)))
    def test_invalid_training_bits(self):
        with self.assertRaises(ValueError): training_values("VALID_TAU2",8)
    def test_invalid_future_bits(self):
        with self.assertRaises(ValueError): post_sample("VALID_TAU2",16)
    def test_invalid_world(self):
        with self.assertRaises(ValueError): counterfactual_post("BAD")
    def test_invalid_convex_predict(self):
        with self.assertRaises(ValueError): convex_predict((ONE,ZERO),DONOR_PRE,0)
    def test_invalid_training_length(self):
        with self.assertRaises(ValueError): chosen_pre_weights((ZERO,ONE))
    def test_full_worlds_and_source_rows(self):
        r,rows=compute()
        self.assertEqual((len(r["worlds"]),len(rows)),(8,1024))
        self.assertEqual(r["new_real_human_E2"],0)
    def test_deterministic_two_replays(self):
        self.assertEqual(training_values("VALID_TAU2",5),training_values("VALID_TAU2",5))


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--test",action="store_true")
    ap.add_argument("--emit",action="store_true")
    args=ap.parse_args()
    if args.test:
        r=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if r.wasSuccessful() else 1)
    if args.emit:
        emit()
    if not args.test and not args.emit:
        ap.print_help()
