#!/usr/bin/env python3
"""R216 exact staggered event-study with 3 cohorts E,L,N and 4 periods.

E adopts at t2; L adopts at t3; never-treated N. Each group-time has an
independent +/-1 artificial outcome shock. All 2^12 source vectors for each
of six precommitted worlds are enumerated and retained, with 36 exact score
cells. A deliberately WRONG already-treated-L control contrast is NOT
claimed to be a TWFE regression coefficient.

Pure standard library and Fraction:
 python r216_exact_staggered_event_study.py --test
 python r216_exact_staggered_event_study.py --emit
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
Z = F(0)
O = F(1)
GROUPS = ("E","L","N")
TIMES = (0,1,2,3)
CELLS = tuple((g,t) for g in GROUPS for t in TIMES)
WORLDS = (
    "VALID_CONSTANT",
    "VALID_HETEROGENEOUS",
    "VALID_DYNAMIC",
    "POST_EVENT_SHOCK_MIMIC",
    "DIFFERENTIAL_PRETREND",
    "LATE_ANTICIPATION",
)
NAMES = (
    "E_pre_placebo",
    "L_pre_placebo",
    "E_k0_clean",
    "E_k1_clean",
    "L_k0_clean",
    "E_k1_BAD_L_ALREADY_TREATED",
)
HERE = Path(__file__).resolve().parent


def treated(g,t):
    if g not in GROUPS or t not in TIMES:
        raise ValueError("only frozen group and period allowed")
    return int((g=="E" and t>=2) or (g=="L" and t>=3))


def causal_effect(world,g,t):
    if world not in WORLDS or (g,t) not in CELLS:
        raise ValueError("unknown artificial world or group-time")
    if not treated(g,t):
        return Z
    if world=="VALID_CONSTANT":
        return F(2)
    if world=="VALID_HETEROGENEOUS":
        return {("E",2):F(1),("E",3):F(1),("L",3):F(3)}[(g,t)]
    if world=="VALID_DYNAMIC":
        return {("E",2):F(2),("E",3):F(4),("L",3):F(1)}[(g,t)]
    if world=="LATE_ANTICIPATION":
        return {("E",2):F(1),("E",3):F(2),("L",3):F(3)}[(g,t)]
    return Z


def untreated_extra(world,g,t):
    if world not in WORLDS or (g,t) not in CELLS:
        raise ValueError("unknown artificial world or group-time")
    if world=="POST_EVENT_SHOCK_MIMIC":
        return {("E",2):F(2),("E",3):F(4),("L",3):F(1)}.get((g,t),Z)
    if world=="DIFFERENTIAL_PRETREND" and g=="E":
        return F(t)
    return Z


def anticipation(world,g,t):
    if world not in WORLDS or (g,t) not in CELLS:
        raise ValueError("unknown artificial world or group-time")
    if world=="LATE_ANTICIPATION" and (g,t)==("L",2):
        return O
    return Z


def observed_mu(world,g,t):
    intercept={"E":O,"L":-O,"N":Z}[g]
    return intercept+F(t)+untreated_extra(world,g,t)+causal_effect(world,g,t)+anticipation(world,g,t)


def cell_mean_vector(world):
    return tuple(observed_mu(world,*cell) for cell in CELLS)


def coefficient_dict(name):
    """Completely fixed group-time differences, no future/model tuning."""
    if name=="E_pre_placebo":
        return {("E",1):O,("E",0):-O,("N",1):-O,("N",0):O}
    if name=="L_pre_placebo":
        return {("L",2):O,("L",1):-O,("N",2):-O,("N",1):O}
    if name=="E_k0_clean":
        return {("E",2):O,("E",1):-O,("N",2):-O,("N",1):O}
    if name=="E_k1_clean":
        return {("E",3):O,("E",1):-O,("N",3):-O,("N",1):O}
    if name=="L_k0_clean":
        return {("L",3):O,("L",2):-O,("N",3):-O,("N",2):O}
    if name=="E_k1_BAD_L_ALREADY_TREATED":
        return {("E",3):O,("E",1):-O,("L",3):-O,("L",1):O}
    raise ValueError("unknown fixed event study estimator")


def weights(name):
    w=coefficient_dict(name)
    if len(w)!=4 or set(w.values())!={-O,O}:
        raise AssertionError("all estimators must have four distinct ±1 coefficients")
    if sum(w.values(),Z)!=Z:
        raise AssertionError("group time contrast must sum zero")
    return tuple(w.get(cell,Z) for cell in CELLS)


def actual_contrast(name,observed_values):
    if len(observed_values)!=len(CELLS):
        raise ValueError("12 group time observed outcomes required")
    d={CELLS[i]:observed_values[i] for i in range(12)}
    coefficients=coefficient_dict(name)
    return sum((coef*d[cell] for cell,coef in coefficients.items()),Z)


def independent_linear_contrast(name,observed_values):
    w=weights(name)
    return sum((w[i]*observed_values[i] for i in range(12)),Z)


def target_policy_effect(world,name):
    if name.endswith("placebo"):
        return Z
    if name in ("E_k0_clean",):
        return causal_effect(world,"E",2)
    if name in ("E_k1_clean","E_k1_BAD_L_ALREADY_TREATED"):
        return causal_effect(world,"E",3)
    if name=="L_k0_clean":
        return causal_effect(world,"L",3)
    raise ValueError("unknown causal scoring target")


def source_eps(mask):
    if not isinstance(mask,int) or mask<0 or mask>=4096:
        raise ValueError("12-bit shock history only")
    return tuple(O if mask&(1<<i) else -O for i in range(12))


def observed_source(world,mask):
    mu=cell_mean_vector(world)
    eps=source_eps(mask)
    return tuple(mu[i]+eps[i] for i in range(12))


def analytic_moments(world,name):
    target=target_policy_effect(world,name)
    w=weights(name)
    expected=independent_linear_contrast(name,cell_mean_vector(world))
    bias=expected-target
    variance=sum((x*x for x in w),Z)
    return expected,bias,variance,bias*bias+variance


def audit_observation_alias():
    return cell_mean_vector("VALID_DYNAMIC")==cell_mean_vector("POST_EVENT_SHOCK_MIMIC") and (
        causal_effect("VALID_DYNAMIC","E",2),causal_effect("VALID_DYNAMIC","E",3),
        causal_effect("VALID_DYNAMIC","L",3)
    )==(F(2),F(4),O) and (
        causal_effect("POST_EVENT_SHOCK_MIMIC","E",2),
        causal_effect("POST_EVENT_SHOCK_MIMIC","E",3),
        causal_effect("POST_EVENT_SHOCK_MIMIC","L",3)
    )==(Z,Z,Z)


def compute():
    if not audit_observation_alias():
        raise AssertionError("indistinguishable source design incorrectly implemented")
    original=[]
    summary=[]
    for world in WORLDS:
        means=cell_mean_vector(world)
        agg={name:{"mean":Z,"second":Z,"loss":Z} for name in NAMES}
        for source in range(4096):
            noise=source_eps(source)
            observed=tuple(means[i]+noise[i] for i in range(12))
            estimates=[]
            squared_losses=[]
            for name in NAMES:
                fit=actual_contrast(name,observed)
                if fit!=independent_linear_contrast(name,observed):
                    raise AssertionError("independent two implementations of actual DID contrast differ")
                target=target_policy_effect(world,name)
                risk=(fit-target)**2
                estimates.append(str(fit))
                squared_losses.append(str(risk))
                agg[name]["mean"]+=fit/4096
                agg[name]["second"]+=fit*fit/4096
                agg[name]["loss"]+=risk/4096
            original.append({
                "true_artificial_world":world,
                "early_cohort_policy_from_t2":"yes",
                "late_cohort_policy_from_t3":"yes",
                "never_treated_group":"N",
                "source_twelve_independent_group_time_shock_bitmask":source,
                "source_all_twelve_eps_plus_or_minus":"|".join(map(str,noise)),
                "complete_artificial_original_source_probability":"1/4096",
                "fixed_group_time_order":"|".join(f"{g}{t}" for g,t in CELLS),
                "all_twelve_actually_observed_group_time_outcomes":"|".join(map(str,observed)),
                "fixed_six_estimator_order":"|".join(NAMES),
                "six_estimates_using_actual_observed_only":"|".join(estimates),
                "six_true_oracle_target_MSE_contributions":"|".join(squared_losses),
            })
        for name in NAMES:
            m=agg[name]
            empirical_var=m["second"]-m["mean"]**2
            em,bias,var,theoretical_mse=analytic_moments(world,name)
            if (m["mean"],empirical_var,m["loss"])!=(em,var,theoretical_mse):
                raise AssertionError("all 4096 random source moments differ from independent bias-variance formula")
            summary.append({
                "true_world":world,
                "event_contrast":name,
                "uses_already_treated_late_group_as_control":name=="E_k1_BAD_L_ALREADY_TREATED",
                "true_target_policy_effect_ORACLE_ONLY":str(target_policy_effect(world,name)),
                "exact_expected_observed_contrast":str(em),
                "full_4096_original_noise_source_mean":str(m["mean"]),
                "actual_effect_bias_exact":str(bias),
                "analytic_independent_eps_variance_exact":str(var),
                "full_4096_original_eps_variance_exact":str(empirical_var),
                "analytic_true_target_MSE_exact":str(theoretical_mse),
                "full_4096_original_eps_MSE_exact":str(m["loss"]),
                "source_noise_probability_sum":"1",
                "fixed_12_cell_weights":"|".join(map(str,weights(name))),
            })
    if (len(original),len(summary))!=(24576,36):
        raise AssertionError("missing original 6×4096 histories or 36 fixed score configurations")
    return {
        "research_id":"R216",
        "actual_original_239_catalogue_id":"09-007",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "six_artificial_scm_worlds":list(WORLDS),
        "four_observed_periods":list(TIMES),
        "three_exposure_cohorts":list(GROUPS),
        "original_complete_twelve_shock_source_histories":len(original),
        "fixed_six_event_estimators":list(NAMES),
        "source_probability_per_world":"1/4096",
        "exact_independent_two_Fraction_contrast_routes":True,
        "exact_independent_full_source_bias_variance_routes":True,
        "whole_observed_panel_aliases_true_causal_world_vs_postshock_false_world":True,
        "valid_heterogeneous_E_k1_true_positive_but_bad_L_already_treated_expected_negative":True,
        "this_specific_BAD_contrast_is_actual_TWFE_event_study_coefficient":False,
        "new_real_human_E2":0,
        "new_real_historical_E3":0,
        "summaries":summary,
        "limitations":[
            "Six completely synthetic three-cohort/four-period worlds, no real units",
            "One observation per cohort-time, no population standard errors or empirical inference",
            "The bad already-treated comparator is a fixed naïve DiD contrast; NOT the full TWFE regression",
            "Parallel trends and absence of anticipation not identified from observed pre-period placebo alone",
        ],
    },original


def emit():
    r,source_rows=compute()
    paths={
        "results":HERE/"R216_EXACT_RESULTS.json",
        "source":HERE/"R216_ALL_24576_ORIGINAL_STAGGERED_GROUP_TIME_SHOCK_PANELS.csv",
    }
    paths["results"].write_text(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    with paths["source"].open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=list(source_rows[0]))
        wr.writeheader()
        wr.writerows(source_rows)
    acceptance={
        "model_id":"R216",
        "actual_239_catalogue_id":"09-007",
        "complete_artificial_worlds":6,
        "full_original_group_time_shock_histories":24576,
        "full_fixed_contrast_risk_configs":36,
        "actual_estimators_two_independent_Fraction_program_paths":True,
        "all_full_source_noise_risks_analytically_matched":True,
        "dynamic_treatment_vs_noncausal_postshock_full_panel_distributions_identical":True,
        "new_E2":0,"new_E3":0,
        **{k+"_sha256":hashlib.sha256(v.read_bytes()).hexdigest() for k,v in paths.items()},
    }
    (HERE/"R216_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(acceptance,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(acceptance,indent=2))


class Tests(unittest.TestCase):
    def test_cohorts_three(self): self.assertEqual(len(GROUPS),3)
    def test_periods_four(self): self.assertEqual(len(TIMES),4)
    def test_cells_twelve(self): self.assertEqual(len(CELLS),12)
    def test_worlds_six(self): self.assertEqual(len(WORLDS),6)
    def test_contrasts_six(self): self.assertEqual(len(NAMES),6)
    def test_original_24576(self): self.assertEqual(len(WORLDS)*4096,24576)
    def test_e_treats_at2(self):
        self.assertEqual([treated("E",t) for t in TIMES],[0,0,1,1])
    def test_l_treats_at3(self):
        self.assertEqual([treated("L",t) for t in TIMES],[0,0,0,1])
    def test_n_never_treated(self):
        self.assertEqual([treated("N",t) for t in TIMES],[0,0,0,0])
    def test_valid_constant_all_true_effects2(self):
        self.assertEqual([causal_effect("VALID_CONSTANT",*cell) for cell in
                          (("E",2),("E",3),("L",3))],[F(2)]*3)
    def test_heterogeneous_lag1_positive(self):
        self.assertEqual(causal_effect("VALID_HETEROGENEOUS","E",3),O)
    def test_heterogeneous_late_lag0_three(self):
        self.assertEqual(causal_effect("VALID_HETEROGENEOUS","L",3),F(3))
    def test_noncausal_postshock_effectszero(self):
        self.assertEqual([causal_effect("POST_EVENT_SHOCK_MIMIC",*cell) for cell in
                          (("E",2),("E",3),("L",3))],[Z]*3)
    def test_postshock_observed_alias_all_twelve(self):
        self.assertTrue(audit_observation_alias())
    def test_postshock_same_full_noise_source_panel(self):
        for mask in (0,1,29,1007,4095):
            self.assertEqual(observed_source("VALID_DYNAMIC",mask),
                             observed_source("POST_EVENT_SHOCK_MIMIC",mask))
    def test_differential_pretrend_extra(self):
        self.assertEqual([untreated_extra("DIFFERENTIAL_PRETREND","E",t) for t in TIMES],
                         list(map(F,TIMES)))
    def test_late_anticipation_pre_policy_t2(self):
        self.assertEqual(treated("L",2),0)
        self.assertEqual(anticipation("LATE_ANTICIPATION","L",2),O)
    def test_valid_worlds_no_anticipation(self):
        self.assertTrue(all(anticipation(world,g,t)==0
                            for world in WORLDS if world!="LATE_ANTICIPATION" for g,t in CELLS))
    def test_all_contrast_weights_four(self):
        self.assertTrue(all(sum(int(w!=0) for w in weights(name))==4 for name in NAMES))
    def test_all_contrast_weight_sum_zero(self):
        self.assertTrue(all(sum(weights(name),Z)==0 for name in NAMES))
    def test_all_contrast_independent_shock_variance_four(self):
        for world in WORLDS:
            for name in NAMES:
                self.assertEqual(analytic_moments(world,name)[2],F(4))
    def test_valid_constant_clean_unbiased(self):
        for name in ("E_k0_clean","E_k1_clean","L_k0_clean"):
            self.assertEqual(analytic_moments("VALID_CONSTANT",name)[1],Z)
    def test_valid_constant_bad_treated_control_bias_minus_two(self):
        self.assertEqual(analytic_moments("VALID_CONSTANT","E_k1_BAD_L_ALREADY_TREATED")[1],F(-2))
    def test_heterogeneous_bad_negative_even_though_E_true_positive(self):
        em,bias,var,mse=analytic_moments("VALID_HETEROGENEOUS","E_k1_BAD_L_ALREADY_TREATED")
        self.assertEqual(em,F(-2))
        self.assertEqual(target_policy_effect("VALID_HETEROGENEOUS","E_k1_BAD_L_ALREADY_TREATED"),O)
    def test_valid_dynamic_bad_expected_three_vs_true_four(self):
        self.assertEqual(analytic_moments("VALID_DYNAMIC","E_k1_BAD_L_ALREADY_TREATED")[:2],
                         (F(3),F(-1)))
    def test_valid_dynamic_clean_expected_four(self):
        self.assertEqual(analytic_moments("VALID_DYNAMIC","E_k1_clean")[0],F(4))
    def test_postshock_pre_placebos_zero(self):
        for name in ("E_pre_placebo","L_pre_placebo"):
            self.assertEqual(analytic_moments("POST_EVENT_SHOCK_MIMIC",name)[0],Z)
    def test_postshock_false_event_effect_observed_four(self):
        self.assertEqual(analytic_moments("POST_EVENT_SHOCK_MIMIC","E_k1_clean")[:2],
                         (F(4),F(4)))
    def test_pretrend_E_placebo_one(self):
        self.assertEqual(analytic_moments("DIFFERENTIAL_PRETREND","E_pre_placebo")[0],O)
    def test_anticipation_late_placebo_one(self):
        self.assertEqual(analytic_moments("LATE_ANTICIPATION","L_pre_placebo")[0],O)
    def test_anticipation_late_event_contrast_two_vs_true_three(self):
        self.assertEqual(analytic_moments("LATE_ANTICIPATION","L_k0_clean")[:2],
                         (F(2),F(-1)))
    def test_source_all_signs_4096(self):
        self.assertEqual(len({source_eps(x) for x in range(4096)}),4096)
    def test_source_bit_one(self):
        self.assertEqual(source_eps(1)[0],O)
        self.assertEqual(source_eps(0)[0],-O)
    def test_source_eps_mean_exact_zero(self):
        self.assertEqual(sum((source_eps(mask)[0] for mask in range(4096)),Z),Z)
    def test_source_eps_cross_cov_exact_zero(self):
        self.assertEqual(sum((source_eps(mask)[1]*source_eps(mask)[10]
                              for mask in range(4096)),Z),Z)
    def test_two_independent_actual_contrast_programs(self):
        y=observed_source("VALID_HETEROGENEOUS",1007)
        self.assertTrue(all(actual_contrast(name,y)==independent_linear_contrast(name,y)
                            for name in NAMES))
    def test_invalid_name_rejected(self):
        with self.assertRaises(ValueError): weights("NOT_A_MODEL")
    def test_invalid_noise_mask_rejected(self):
        with self.assertRaises(ValueError): source_eps(4096)
    def test_invalid_world_rejected(self):
        with self.assertRaises(ValueError): causal_effect("WRONG","E",2)
    def test_complete_all_original_and_double_fraction_scoring(self):
        r,raw=compute()
        self.assertEqual((len(r["summaries"]),len(raw)),(36,24576))
        self.assertTrue(r["whole_observed_panel_aliases_true_causal_world_vs_postshock_false_world"])
        self.assertEqual(r["new_real_human_E2"],0)
    def test_deterministic_original_source_replay(self):
        self.assertEqual(observed_source("VALID_CONSTANT",3971),
                         observed_source("VALID_CONSTANT",3971))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--test",action="store_true")
    ap.add_argument("--emit",action="store_true")
    flags=ap.parse_args()
    if flags.test:
        ran=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if ran.wasSuccessful() else 1)
    if flags.emit:
        emit()
    if not flags.test and not flags.emit:
        ap.print_help()
