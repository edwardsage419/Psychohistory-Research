#!/usr/bin/env python3
"""R078 exact nonidentifiability + micro-to-group variance bridge (E1 ONLY).

No imports from prior real human datasets. Rational arithmetic gives exact
person-level observational equivalence; log loss alone uses stdlib math.log.
"""
from __future__ import annotations
import argparse, json, math
from fractions import Fraction as F
from pathlib import Path

OBS_PREVALENCE=F(1,2)
LOW=F(3,10)
HIGH=F(7,10)
Q={0:LOW,1:HIGH}
PROTOCOL="protocols/R078_PREDICTION_CAUSALITY_CROSS_SCALE_EQUIVALENCE_FREEZE_2026-10-17.md"

def bernoulli_prob(y:int,p:F)->F:
    if y not in (0,1):raise ValueError("ACTION_MUST_BE_BINARY")
    if p<0 or p>1:raise ValueError("INVALID_BERNOULLI_PROBABILITY")
    return p if y==1 else 1-p

def direct_observational_joint()->dict[tuple[int,int],F]:
    """Graph O->Y, with independently randomized O."""
    return {(o,y):bernoulli_prob(o,OBS_PREVALENCE)*bernoulli_prob(y,Q[o])
            for o in (0,1) for y in (0,1)}

def latent_observational_joint()->dict[tuple[int,int],F]:
    """Graph U->O and U->Y, deterministic observational O=shared U."""
    return {
        (o,y):sum(
            (bernoulli_prob(u,OBS_PREVALENCE)
             * (F(1) if o==u else F(0))
             * bernoulli_prob(y,Q[u])
            for u in (0,1)),F(0))
        for o in (0,1) for y in (0,1)
    }

def joint_conditional_on_own_prior(joint:dict[tuple[int,int],F],x:int):
    """Prior own action X is exogenous and independent in both toy SCMs."""
    if x not in (0,1):raise ValueError("OWN_PRIOR_MUST_BE_BINARY")
    return {(o,y):val for (o,y),val in joint.items()}

def full_observational_joint(joint:dict[tuple[int,int],F]):
    return {(x,o,y):bernoulli_prob(x,OBS_PREVALENCE)*joint[(o,y)]
            for x in (0,1) for o in (0,1) for y in (0,1)}

def expected_brier_with_history(joint:dict[tuple[int,int],F])->F:
    return sum(
        (p*(F(y)-Q[o])**2 for (o,y),p in joint.items()),F(0)
    )

def expected_brier_source_only_baseline(joint:dict[tuple[int,int],F])->F:
    """The no-O marginal 0.5 predictor, not any real R073 source baseline."""
    p=sum((v for (o,y),v in joint.items() if y==1),F(0))
    return sum((v*(F(y)-p)**2 for (o,y),v in joint.items()),F(0))

def expected_logloss_with_history(joint:dict[tuple[int,int],F])->float:
    return -sum(float(p)*math.log(float(bernoulli_prob(y,Q[o])))
                for (o,y),p in joint.items())

def expected_logloss_baseline(joint:dict[tuple[int,int],F])->float:
    p=sum((v for (o,y),v in joint.items() if y==1),F(0))
    return -sum(float(v)*math.log(float(bernoulli_prob(y,p)))
                for (o,y),v in joint.items())

def do_prob_direct(o:int)->F:
    if o not in (0,1):raise ValueError("INTERVENTION_MUST_BE_BINARY")
    return Q[o]

def do_prob_latent(o:int)->F:
    """O=do(o) severs U->O, Y unaffected since O not in Y equation."""
    if o not in (0,1):raise ValueError("INTERVENTION_MUST_BE_BINARY")
    return (LOW+HIGH)/2

def individual_causal_effect(which:str)->F:
    if which=="direct":return do_prob_direct(1)-do_prob_direct(0)
    if which=="latent":return do_prob_latent(1)-do_prob_latent(0)
    raise ValueError("UNKNOWN_CAUSAL_MODEL")

def variance_direct_group(n:int)->F:
    """Required design assumption: independent O_i across group members."""
    if not isinstance(n,int) or n<1:raise ValueError("GROUP_N_MUST_BE_POSITIVE_INT")
    p=(LOW+HIGH)/2
    return p*(1-p)/n

def covariance_latent_between_people()->F:
    """In latent model U is shared within the group, conditional Ys independent."""
    avg=(LOW+HIGH)/2
    return ((LOW-avg)**2+(HIGH-avg)**2)/2

def variance_latent_group(n:int)->F:
    if not isinstance(n,int) or n<1:raise ValueError("GROUP_N_MUST_BE_POSITIVE_INT")
    cond_var=(LOW*(1-LOW)+HIGH*(1-HIGH))/2
    return cond_var/n+covariance_latent_between_people()

def fraction_string(p:F)->str:
    return f"{p.numerator}/{p.denominator}"

def validate_exact_contract():
    a=direct_observational_joint()
    b=latent_observational_joint()
    expected={(0,0):F(7,20),(0,1):F(3,20),(1,0):F(3,20),(1,1):F(7,20)}
    if a!=b or a!=expected:
        raise AssertionError("SINGLE_ACTOR_OBSERVATIONAL_IDENTITY_FAILED")
    if sum(a.values(),F())!=1:raise AssertionError("INVALID_PERSON_PROBABILITY_MASS")
    if full_observational_joint(a)!=full_observational_joint(b):
        raise AssertionError("CONDITIONING_ON_OWN_PRIOR_CHANGED_EQUIVALENCE")
    if expected_brier_with_history(a)!=F(21,100):
        raise AssertionError("CONDITIONAL_BRIER_EXACT_FAIL")
    if expected_brier_source_only_baseline(a)!=F(1,4):
        raise AssertionError("MARGINAL_BRIER_BASELINE_FAIL")
    if individual_causal_effect("direct")!=F(2,5):
        raise AssertionError("SOCIAL_CAUSAL_MODEL_INTERVENTION_FAIL")
    if individual_causal_effect("latent")!=0:
        raise AssertionError("LATENT_COMMON_CAUSE_INTERVENTION_FAIL")
    if variance_direct_group(10)!=F(1,40):raise AssertionError("GROUP_A_VAR_FAIL")
    if variance_latent_group(10)!=F(61,1000):raise AssertionError("GROUP_B_VAR_FAIL")
    if variance_direct_group(1)!=variance_latent_group(1):
        raise AssertionError("SINGLE_ACTOR_GROUP_VARIANCE_MUST_MATCH")
    if abs(expected_logloss_with_history(a)-(-LOW*math.log(float(LOW))-(1-LOW)*math.log(float(1-LOW))))>1e-12:
        raise AssertionError("LOGLLOSS_IDENTITY_FAIL")
    return True

def build_result():
    validate_exact_contract()
    a=direct_observational_joint()
    b=latent_observational_joint()
    delta_brier=expected_brier_source_only_baseline(a)-expected_brier_with_history(a)
    log_with=expected_logloss_with_history(a)
    log_base=expected_logloss_baseline(a)
    return {
        "research_id":"R078",
        "stage":"PHASE_A_E1_EXACT_SYNTHETIC_OBSERVATIONAL_EQUIVALENCE",
        "protocol_frozen_before_any_R078_execution":PROTOCOL,
        "human_data_rows_consumed":0,
        "human_evidence_grade":"NONE_NEW",
        "synthetic_evidence_grade":"E1_EXACT_ENUMERATION",
        "random_seed_required":False,
        "model_setup":{
            "opponent_history_prevalence":fraction_string(OBS_PREVALENCE),
            "low_cooperation_given_opponent_0":fraction_string(LOW),
            "high_cooperation_given_opponent_1":fraction_string(HIGH),
            "own_prior_X":"Independent Bernoulli(1/2), tested but no extra effect",
            "mechanism_A":"Direct causal O->Y, O independent across group members",
            "mechanism_B":"Shared latent U->O and U->Y, observational O=U, group U common, no O->Y causal arrow",
        },
        "single_actor_joint_P_O_Y":{
            f"O{o}_Y{y}":fraction_string(v) for (o,y),v in sorted(a.items())
        },
        "same_person_joint_across_both_models":a==b,
        "same_joint_after_conditioning_on_own_previous_action":
            full_observational_joint(a)==full_observational_joint(b),
        "observational_prediction":{
            "Brier_with_prior_opponent":fraction_string(expected_brier_with_history(a)),
            "Brier_without_prior_opponent":fraction_string(expected_brier_source_only_baseline(a)),
            "Brier_improvement_shared_by_both_models":fraction_string(delta_brier),
            "log_loss_with_prior_opponent":log_with,
            "log_loss_without_prior_opponent":log_base,
            "log_loss_improvement_shared_by_both_models":log_base-log_with,
        },
        "intervention_do_O":{
            "A_direct_do0":fraction_string(do_prob_direct(0)),
            "A_direct_do1":fraction_string(do_prob_direct(1)),
            "A_direct_effect":fraction_string(individual_causal_effect("direct")),
            "B_latent_do0":fraction_string(do_prob_latent(0)),
            "B_latent_do1":fraction_string(do_prob_latent(1)),
            "B_latent_effect":fraction_string(individual_causal_effect("latent")),
            "causal_effect_identified_from_equal_observational_table":False,
        },
        "synthetic_group_variance":{
            "within_B_shared_U_group_covariance":fraction_string(covariance_latent_between_people()),
            "n1":{"A":fraction_string(variance_direct_group(1)),
                  "B":fraction_string(variance_latent_group(1))},
            "n10":{"A":fraction_string(variance_direct_group(10)),
                   "B":fraction_string(variance_latent_group(10))},
            "n100":{"A":fraction_string(variance_direct_group(100)),
                    "B":fraction_string(variance_latent_group(100))},
            "limit_as_n_grows":{"A":"0/1","B":fraction_string(covariance_latent_between_people())},
            "CRITICAL_ASSUMPTION":"A independent O per person; B common U across group. Different assumptions may erase difference.",
        },
        "unvalidated_projections":{
            "individual_human_psychology":"NOT_IDENTIFIED",
            "real_network_partner_assignment":"NOT_ESTABLISHED",
            "real_group_level_variance":"NOT_MEASURED",
            "institutional_dynamic_rules":"NOT_ESTIMATED",
            "historical_long_horizon_prediction":"NOT_VALIDATED",
        },
        "PESEN_v0.1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=build_result()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "research_id":"R078",
        "stage":result["stage"],
        "single_actor_joint_equal":result["same_person_joint_across_both_models"],
        "Brier_improvement_both":result["observational_prediction"]["Brier_improvement_shared_by_both_models"],
        "causal_effect_A":result["intervention_do_O"]["A_direct_effect"],
        "causal_effect_B":result["intervention_do_O"]["B_latent_effect"],
        "group_n10_var_A":result["synthetic_group_variance"]["n10"]["A"],
        "group_n10_var_B":result["synthetic_group_variance"]["n10"]["B"],
        "synthetic_only":True,
        "PESEN_v0.1":"FROZEN"
    },sort_keys=True))
if __name__=="__main__":
    main()
