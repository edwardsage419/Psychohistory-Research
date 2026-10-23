#!/usr/bin/env python3
"""R307 minority/private-public toy Bayesian evidence gates, exact Fraction E1, NOT author fitted."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FREEZE="4f74448e261ac61c65cd60926a056d6916a84e34"
ZERO,ONE=F(0),F(1)
PRIORS=(F(1,4),F(1,2))
STEPS=(0,1,2,3)
LEVELS=(ZERO,F(1,2),ONE)
MINORITY_SIZES=(1,2)
CHANNELS=("PRIVATE_BELIEF","PUBLIC_EXPRESSION")
WORLDS=tuple(itertools.product(PRIORS,STEPS,LEVELS,LEVELS,LEVELS,MINORITY_SIZES))
SOURCE_NAME="R307_ALL_864_ORIGINAL_MINORIT Y_PRIVATE_PUBLIC_SOURCES.csv".replace("MINORIT Y","MINORITY")
RESULT_NAME="R307_EXACT_MINORITY_INFLUENCE_RESULTS.json"
RECEIPT_NAME="R307_MACHINE_RECEIPT.json"

def worldid(prior,t,c,k,n,m):
    return f"prior={prior}|exposures={t}|consistency={c}|credibility={k}|norm_pressure={n}|minority={m}of6"

def evaluate(prior,t,c,k,n,m):
    if (prior,t,c,k,n,m) not in WORLDS:raise ValueError("outside frozen world grid")
    lr=ONE+c*k
    o0=prior/(ONE-prior)
    odds_trace=tuple(o0*(lr**u) for u in range(t+1))
    belief_trace=tuple(o/(ONE+o) for o in odds_trace)
    private=belief_trace[-1]
    majority=6-m
    pressure_factor=ONE-n*F(majority,6)
    public=prior+pressure_factor*(private-prior)
    if not ZERO<=prior<=public<=private<=ONE:raise AssertionError("range/private-public ordering")
    return {"prior_odds":o0,"per_exposure_likelihood_ratio":lr,
       "posterior_odds_path":odds_trace,"private_belief_path":belief_trace,
       "posterior_odds":odds_trace[-1],
       "private_endorsement_probability":private,
       "majority_size":majority,"majority_fraction":F(majority,6),
       "public_expression_retention_factor":pressure_factor,
       "public_endorsement_probability":public,
       "private_lift_vs_prior":private-prior,
       "public_lift_vs_prior":public-prior,
       "private_minus_public_gap":private-public}

def source(prior,t,c,k,n,m,channel):
    if channel not in CHANNELS:raise ValueError("unfrozen observation channel")
    v=evaluate(prior,t,c,k,n,m)
    return {"world":worldid(prior,t,c,k,n,m),
      "group_size":6,"minority_count":m,"majority_count":v["majority_size"],
      "minority_fraction":F(m,6),"majority_fraction":v["majority_fraction"],
      "initial_private_prior":prior,"minority_advocacy_exposures":t,
      "minority_behavioral_consistency":c,"source_credibility_gate":k,
      "public_normative_pressure":n,
      "per_signal_likelihood_multiplier":v["per_exposure_likelihood_ratio"],
      "initial_prior_odds":v["prior_odds"],
      "posterior_odds_path":";".join(str(z) for z in v["posterior_odds_path"]),
      "private_posterior_path":";".join(str(z) for z in v["private_belief_path"]),
      "private_posterior_after_exposures":v["private_endorsement_probability"],
      "public_suppression_retention":v["public_expression_retention_factor"],
      "public_expression_probability":v["public_endorsement_probability"],
      "private_lift":v["private_lift_vs_prior"],
      "public_lift":v["public_lift_vs_prior"],
      "private_public_difference":v["private_minus_public_gap"],
      "observation_channel":channel,
      "channel_endorsement_probability":v["private_endorsement_probability"] if channel=="PRIVATE_BELIEF" else v["public_endorsement_probability"],
      "probability_is_model_implied_not_real_human":True}

def originals():return tuple(source(*w,channel) for w in WORLDS for channel in CHANNELS)

def verify():
    assert len(WORLDS)==432 and len(originals())==864
    assert len({(x["world"],x["observation_channel"]) for x in originals()})==864
    for w in WORLDS:
        prior,t,c,k,n,m=w
        v=evaluate(*w)
        assert len(v["posterior_odds_path"])==len(v["private_belief_path"])==t+1
        assert v["private_belief_path"][0]==prior
        assert v["posterior_odds_path"][-1]==(prior/(ONE-prior))*((ONE+c*k)**t)
        if t==0 or c==ZERO or k==ZERO:
            assert v["private_endorsement_probability"]==v["public_endorsement_probability"]==prior
        if n==ZERO:assert v["private_endorsement_probability"]==v["public_endorsement_probability"]
        if t>0:
            assert v["private_belief_path"][-1]>=v["private_belief_path"][-2]
        assert v["majority_size"]==6-m
        assert v["public_expression_retention_factor"]==ONE-n*F(6-m,6)
        assert v["public_lift_vs_prior"]<=v["private_lift_vs_prior"]
        if m==1:
            cmp=evaluate(prior,t,c,k,n,2)
            assert v["private_endorsement_probability"]==cmp["private_endorsement_probability"]
            assert v["public_endorsement_probability"]<=cmp["public_endorsement_probability"]
    assert evaluate(F(1,4),3,ONE,ONE,ONE,2)["private_endorsement_probability"]==F(8,11)
    assert evaluate(F(1,4),3,ONE,ONE,ONE,2)["public_endorsement_probability"]==F(9,22)
    assert evaluate(F(1,4),3,ONE,ONE,ONE,1)["public_endorsement_probability"]==F(29,88)
    assert evaluate(F(1,4),3,ONE,ONE,ZERO,1)["public_endorsement_probability"]==F(8,11)
    assert evaluate(F(1,4),3,F(1,2),ONE,ONE,2)["private_endorsement_probability"]==F(9,17)
    assert evaluate(F(1,4),3,ONE,F(1,2),ONE,2)["private_endorsement_probability"]==F(9,17)
    assert evaluate(F(1,2),3,ONE,ONE,ONE,2)["private_endorsement_probability"]==F(8,9)
    return True

def emit():
    verify()
    cols=("world","group_size","minority_count","majority_count","minority_fraction","majority_fraction",
      "initial_private_prior","minority_advocacy_exposures","minority_behavioral_consistency",
      "source_credibility_gate","public_normative_pressure",
      "per_signal_likelihood_multiplier","initial_prior_odds","posterior_odds_path",
      "private_posterior_path","private_posterior_after_exposures",
      "public_suppression_retention","public_expression_probability",
      "private_lift","public_lift","private_public_difference","observation_channel",
      "channel_endorsement_probability","probability_is_model_implied_not_real_human")
    path=ROOT/SOURCE_NAME
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        writer.writeheader()
        for row in originals():writer.writerow({k:str(row[k]) for k in cols})
    results={"research_id":"R307","original_catalogue_id":"03-016",
      "freeze_commit":FREEZE,
      "scope":"E1_PROJECT_INVENTED_MINORITY_CONSISTENCY_CREDIBILITY_BAYES_EVIDENCE_AND_PUBLIC_NORM_SUPPRESSION",
      "synthetic_worlds":432,"all_labeled_original_source_rows":864,
      "minority_sizes":[1,2],"total_agents":6,"exposure_horizons":[0,1,2,3],
      "author1969_real_person_perception_data_replicated":False,
      "author1994_meta_analysis_effect_sizes_reproduced":False,
      "project_custom_evidence_lr_and_public_suppression_not_original_authors_equations":True,
      "new_real_human_E2":0,"new_real_animal_E2":0,"new_historical_E3":0,
      "R073":"FROZEN","PESEN_v0_1":"FROZEN",
      "frozen_reference":{
        "prior_quarter_three_consistent_credible_private":"8/11",
        "same_world_one_norm_two_of_six_public":"9/22",
        "same_world_one_norm_one_of_six_public":"29/88",
        "same_world_norm_zero_public":"8/11",
        "half_consistency_full_credibility_private":"9/17",
        "full_consistency_half_credibility_private":"9/17",
        "half_prior_full_evidence_three_exposures_private":"8/9",
        "no_exposure_zero_consistency_or_zero_credibility_changes_belief":False},
      "worlds":[]}
    for w in WORLDS:
        prior,t,c,k,n,m=w
        v=evaluate(*w)
        results["worlds"].append({"world":worldid(*w),
          "prior":str(prior),"exposures":t,
          "consistency":str(c),"credibility":str(k),
          "normative_pressure":str(n),"minority_count":m,"majority_count":6-m,
          "per_signal_likelihood_multiplier":str(v["per_exposure_likelihood_ratio"]),
          "posterior_odds_path":[str(x) for x in v["posterior_odds_path"]],
          "private_belief_path":[str(x) for x in v["private_belief_path"]],
          "private_probability":str(v["private_endorsement_probability"]),
          "public_retention_factor":str(v["public_expression_retention_factor"]),
          "public_probability":str(v["public_endorsement_probability"]),
          "private_minus_public_gap":str(v["private_minus_public_gap"]),
          "original_channel_rows":[{key:str(source(*w,channel)[key]) for key in cols if key!="world"} for channel in CHANNELS]})
    resultpath=ROOT/RESULT_NAME
    resultpath.write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"research_id":"R307","freeze_commit":FREEZE,"source_rows":864,
      "source_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
      "results_sha256":hashlib.sha256(resultpath.read_bytes()).hexdigest(),
      "new_real_E2":0,"new_historical_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_all(self):self.assertTrue(verify())
    def test_world_count(self):self.assertEqual(len(WORLDS),432)
    def test_source_count(self):self.assertEqual(len(originals()),864)
    def test_private(self):self.assertEqual(evaluate(F(1,4),3,ONE,ONE,ONE,2)["private_endorsement_probability"],F(8,11))
    def test_public_two(self):self.assertEqual(evaluate(F(1,4),3,ONE,ONE,ONE,2)["public_endorsement_probability"],F(9,22))
    def test_public_one(self):self.assertEqual(evaluate(F(1,4),3,ONE,ONE,ONE,1)["public_endorsement_probability"],F(29,88))
    def test_norm_zero(self):self.assertEqual(evaluate(F(1,4),3,ONE,ONE,ZERO,1)["public_endorsement_probability"],F(8,11))
    def test_half_consistency(self):self.assertEqual(evaluate(F(1,4),3,F(1,2),ONE,ONE,2)["private_endorsement_probability"],F(9,17))
    def test_confounded(self):self.assertEqual(evaluate(F(1,4),3,F(1,2),ONE,ONE,2)["private_endorsement_probability"],evaluate(F(1,4),3,ONE,F(1,2),ONE,2)["private_endorsement_probability"])
    def test_early_horizon(self):self.assertEqual(evaluate(F(1,4),0,ONE,ONE,ONE,2)["private_endorsement_probability"],F(1,4))
    def test_zero_consistency(self):self.assertEqual(evaluate(F(1,4),3,ZERO,ONE,ONE,2)["private_endorsement_probability"],F(1,4))
    def test_zero_credibility(self):self.assertEqual(evaluate(F(1,4),3,ONE,ZERO,ONE,2)["private_endorsement_probability"],F(1,4))
    def test_wrong_count(self):
        with self.assertRaises(ValueError):evaluate(F(1,4),3,ONE,ONE,ONE,3)
    def test_wrong_horizon(self):
        with self.assertRaises(ValueError):evaluate(F(1,4),4,ONE,ONE,ONE,2)
    def test_wrong_prior(self):
        with self.assertRaises(ValueError):evaluate(F(3,4),3,ONE,ONE,ONE,2)
    def test_wrong_channel(self):
        with self.assertRaises(ValueError):source(F(1,4),3,ONE,ONE,ONE,2,"INTERPERSONAL")

def generated(world,channel,kind):
    def check(self):
        row=source(*world,channel);v=evaluate(*world)
        if kind=="private":self.assertEqual(row["private_posterior_after_exposures"],v["private_endorsement_probability"])
        elif kind=="public":self.assertEqual(row["public_expression_probability"],v["public_endorsement_probability"])
        elif kind=="channel":self.assertEqual(row["channel_endorsement_probability"],v["private_endorsement_probability"] if channel==CHANNELS[0] else v["public_endorsement_probability"])
        else:raise AssertionError(kind)
    return check
for i,w in enumerate(WORLDS):
    for channel in CHANNELS:
        for kind in ("private","public","channel"):
            setattr(Tests,f"test_world{i}_{channel.lower()}_{kind}",generated(w,channel,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser();m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true");m.add_argument("--emit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R307"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
