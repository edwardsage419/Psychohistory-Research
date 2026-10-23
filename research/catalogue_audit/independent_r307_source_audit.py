#!/usr/bin/env python3
"""R307 independent sequential Bayesian likelihood verification, 864 full sources; no production imports."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as Q
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/"research/R307"
CSV=ROOT/"R307_ALL_864_ORIGINAL_MINORITY_PRIVATE_PUBLIC_SOURCES.csv"
RESULT=ROOT/"R307_EXACT_MINORITY_INFLUENCE_RESULTS.json"
RECEIPT=ROOT/"R307_MACHINE_RECEIPT.json"
ZERO,ONE=Q(0),Q(1)
PRIORS=(Q(1,4),Q(1,2))
STEPS=(0,1,2,3)
LEVELS=(ZERO,Q(1,2),ONE)
MINORITY=(1,2)
CHANNELS=("PRIVATE_BELIEF","PUBLIC_EXPRESSION")
WORLDS=tuple(itertools.product(PRIORS,STEPS,LEVELS,LEVELS,LEVELS,MINORITY))
FIELDS=("group_size","minority_count","majority_count","minority_fraction","majority_fraction",
      "initial_private_prior","minority_advocacy_exposures","minority_behavioral_consistency",
      "source_credibility_gate","public_normative_pressure",
      "per_signal_likelihood_multiplier","initial_prior_odds","posterior_odds_path",
      "private_posterior_path","private_posterior_after_exposures",
      "public_suppression_retention","public_expression_probability",
      "private_lift","public_lift","private_public_difference","observation_channel",
      "channel_endorsement_probability","probability_is_model_implied_not_real_human")

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def load():
    with CSV.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def world_name(world):
    p,t,c,k,n,m=world
    return f"prior={p}|exposures={t}|consistency={c}|credibility={k}|norm_pressure={n}|minority={m}of6"

def independent(world):
    p,t,c,k,n,m=world
    # Independent explicitly normalized update, not odds-power formula.
    lr=ONE+c*k
    likelihood_under_alt=lr/(ONE+lr)
    likelihood_under_non_alt=ONE/(ONE+lr)
    observations=[p]
    for _ in range(t):
        before=observations[-1]
        numerator=before*likelihood_under_alt
        denominator=numerator+(ONE-before)*likelihood_under_non_alt
        observations.append(numerator/denominator)
    belief=observations[-1]
    odds=tuple(b/(ONE-b) for b in observations)
    retain=ONE-n*Q(6-m,6)
    public=retain*belief+(ONE-retain)*p
    return {"LR":lr,"prior_odds":odds[0],"odds_trace":odds,"belief_trace":tuple(observations),
      "private":belief,"public":public,"retention":retain,"gap":belief-public,
      "minority":m,"majority":6-m}

def expected_row(world,channel):
    p,t,c,k,n,m=world
    v=independent(world)
    values={"group_size":6,"minority_count":m,"majority_count":6-m,
      "minority_fraction":Q(m,6),"majority_fraction":Q(6-m,6),
      "initial_private_prior":p,"minority_advocacy_exposures":t,
      "minority_behavioral_consistency":c,"source_credibility_gate":k,
      "public_normative_pressure":n,"per_signal_likelihood_multiplier":v["LR"],
      "initial_prior_odds":v["prior_odds"],
      "posterior_odds_path":";".join(str(z) for z in v["odds_trace"]),
      "private_posterior_path":";".join(str(z) for z in v["belief_trace"]),
      "private_posterior_after_exposures":v["private"],
      "public_suppression_retention":v["retention"],
      "public_expression_probability":v["public"],
      "private_lift":v["private"]-p,"public_lift":v["public"]-p,
      "private_public_difference":v["gap"],"observation_channel":channel,
      "channel_endorsement_probability":v["private"] if channel==CHANNELS[0] else v["public"],
      "probability_is_model_implied_not_real_human":True}
    return {k:str(values[k]) for k in FIELDS}

def verify(rows,result):
    if len(rows)!=864 or len(result["worlds"])!=432 or result["all_labeled_original_source_rows"]!=864:
        raise AssertionError("full artificial source and result worlds required")
    if result["synthetic_worlds"]!=432 or result["total_agents"]!=6:
        raise AssertionError("wrong original frozen universe")
    valid={(w,channel) for w in WORLDS for channel in CHANNELS}
    seen={}
    for s in rows:
        try:
            w=(Q(s["initial_private_prior"]),int(s["minority_advocacy_exposures"]),
               Q(s["minority_behavioral_consistency"]),Q(s["source_credibility_gate"]),
               Q(s["public_normative_pressure"]),int(s["minority_count"]))
            channel=s["observation_channel"]
        except (KeyError,ValueError,ZeroDivisionError) as err:raise AssertionError("invalid source dimensions") from err
        key=(w,channel)
        if key not in valid or key in seen:raise AssertionError("missing, duplicate or out-of-grid original source")
        if s["world"]!=world_name(w):raise AssertionError("world identity mismatch")
        for k,v in expected_row(w,channel).items():
            if s[k]!=v:raise AssertionError("synthetic data tamper: "+k)
        seen[key]=s
    if set(seen)!=valid:raise AssertionError("incomplete source universe")
    for i,w in enumerate(WORLDS):
        rec=result["worlds"][i]
        p,t,c,k,n,m=w
        v=independent(w)
        if rec["world"]!=world_name(w):raise AssertionError("result world order")
        for name,val in (("prior",str(p)),("exposures",t),("consistency",str(c)),
                         ("credibility",str(k)),("normative_pressure",str(n)),
                         ("minority_count",m),("majority_count",6-m),
                         ("per_signal_likelihood_multiplier",str(v["LR"])),
                         ("posterior_odds_path",[str(x) for x in v["odds_trace"]]),
                         ("private_belief_path",[str(x) for x in v["belief_trace"]]),
                         ("private_probability",str(v["private"])),
                         ("public_retention_factor",str(v["retention"])),
                         ("public_probability",str(v["public"])),
                         ("private_minus_public_gap",str(v["gap"]))):
            if rec[name]!=val:raise AssertionError("result mismatch "+name)
        if rec["original_channel_rows"]!=[expected_row(w,channel) for channel in CHANNELS]:
            raise AssertionError("result/source channel inconsistencies")
    expected={"prior_quarter_three_consistent_credible_private":"8/11",
      "same_world_one_norm_two_of_six_public":"9/22",
      "same_world_one_norm_one_of_six_public":"29/88",
      "same_world_norm_zero_public":"8/11",
      "half_consistency_full_credibility_private":"9/17",
      "full_consistency_half_credibility_private":"9/17",
      "half_prior_full_evidence_three_exposures_private":"8/9",
      "no_exposure_zero_consistency_or_zero_credibility_changes_belief":False}
    if result["frozen_reference"]!=expected:raise AssertionError("frozen exemplar tampered")
    for p,t,c,k,n,m in WORLDS:
        v=independent((p,t,c,k,n,m))
        if not p<=v["public"]<=v["private"]<=ONE:raise AssertionError("private-public ordering")
        if t==0 or c==ZERO or k==ZERO:
            if v["private"]!=p or v["public"]!=p:raise AssertionError("information zero negative controls")
        if n==ZERO and v["private"]!=v["public"]:raise AssertionError("norm zero channels")
        if m==1 and v["public"]>independent((p,t,c,k,n,2))["public"]:
            raise AssertionError("majority share monotonicity")
    return {"reconstructed_original_864_source_rows":864,
       "worlds":432,"independent_sequential_Bayes_6agent_public_gate":"PASS",
       "zero_evidence_and_zero_norm_negative_controls":"PASS",
       "consistency_credibility_identifiability":"CONFOUNDED_C_TIMES_K",
       "new_real_human_E2":0,"new_historical_E3":0}

def audit():
    r,j=obj(RECEIPT),obj(RESULT)
    frozen="4f74448e261ac61c65cd60926a056d6916a84e34"
    if r["freeze_commit"]!=frozen or j["freeze_commit"]!=frozen:raise AssertionError("not prescore frozen")
    if j["research_id"]!="R307" or j["original_catalogue_id"]!="03-016":raise AssertionError("research id")
    if j["project_custom_evidence_lr_and_public_suppression_not_original_authors_equations"] is not True:
        raise AssertionError("false author attribution")
    if j["author1969_real_person_perception_data_replicated"] is not False or j["author1994_meta_analysis_effect_sizes_reproduced"] is not False:
        raise AssertionError("false original human evidence")
    if any(j[k]!=0 for k in ("new_real_human_E2","new_real_animal_E2","new_historical_E3")):
        raise AssertionError("synthetic promoted to humans/history")
    if r["source_rows"]!=864 or r["new_real_E2"]!=0 or r["new_historical_E3"]!=0:
        raise AssertionError("wrong receipts")
    if hashlib.sha256(CSV.read_bytes()).hexdigest()!=r["source_sha256"]:raise AssertionError("CSV SHA256")
    if hashlib.sha256(RESULT.read_bytes()).hexdigest()!=r["results_sha256"]:raise AssertionError("JSON SHA256")
    return {**verify(load(),j),"source_sha256":r["source_sha256"],
       "results_sha256":r["results_sha256"]}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["reconstructed_original_864_source_rows"],864)
    def test_worlds(self):self.assertEqual(len(WORLDS),432)
    def test_private_full(self):self.assertEqual(independent((Q(1,4),3,ONE,ONE,ONE,2))["private"],Q(8,11))
    def test_public_minority2(self):self.assertEqual(independent((Q(1,4),3,ONE,ONE,ONE,2))["public"],Q(9,22))
    def test_public_minority1(self):self.assertEqual(independent((Q(1,4),3,ONE,ONE,ONE,1))["public"],Q(29,88))
    def test_public_no_norm(self):self.assertEqual(independent((Q(1,4),3,ONE,ONE,ZERO,1))["public"],Q(8,11))
    def test_confounded(self):
        self.assertEqual(independent((Q(1,4),3,Q(1,2),ONE,ONE,2))["private"],
                         independent((Q(1,4),3,ONE,Q(1,2),ONE,2))["private"])
    def test_horizon0(self):self.assertEqual(independent((Q(1,4),0,ONE,ONE,ONE,2))["private"],Q(1,4))
    def test_no_credibility(self):self.assertEqual(independent((Q(1,4),3,ONE,ZERO,ONE,2))["private"],Q(1,4))
    def test_wrong_length(self):
        with self.assertRaises(AssertionError):verify(load()[:-1],obj(RESULT))
    def test_duplicate(self):
        s=load();s[1]=dict(s[0])
        with self.assertRaises(AssertionError):verify(s,obj(RESULT))
    def test_bad_channel(self):
        s=load();s[1]=dict(s[1]);s[1]["observation_channel"]="UNKNOWN"
        with self.assertRaises(AssertionError):verify(s,obj(RESULT))
    def test_bad_consistency(self):
        s=load();s[1]=dict(s[1]);s[1]["minority_behavioral_consistency"]="1/3"
        with self.assertRaises(AssertionError):verify(s,obj(RESULT))
    def test_bad_public(self):
        s=load();s[1]=dict(s[1]);s[1]["public_expression_probability"]="9"
        with self.assertRaises(AssertionError):verify(s,obj(RESULT))
    def test_bad_history(self):
        s=load();s[1]=dict(s[1]);s[1]["private_posterior_path"]="9;9"
        with self.assertRaises(AssertionError):verify(s,obj(RESULT))
    def test_result_tamper(self):
        r=obj(RESULT);r["worlds"][0]["public_probability"]="9"
        with self.assertRaises(AssertionError):verify(load(),r)
    def test_science_claim_tamper(self):
        r=obj(RESULT);r["frozen_reference"]["same_world_one_norm_two_of_six_public"]="9"
        with self.assertRaises(AssertionError):verify(load(),r)
    def test_sha_tamper(self):
        self.assertNotEqual(hashlib.sha256(CSV.read_bytes()+b"tamper").hexdigest(),obj(RECEIPT)["source_sha256"])

if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R307 audit"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
