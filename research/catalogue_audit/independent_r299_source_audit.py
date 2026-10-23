#!/usr/bin/env python3
"""R299 independent TD0/MC complete original source audit; never imports production code."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research/R299"
CSV=ROOT/"R299_ALL_120_ORIGINAL_MODEL_FREE_TD_MC_STATES.csv"
JSON=ROOT/"R299_EXACT_MODEL_FREE_TD_MC_RESULTS.json"
RECEIPT=ROOT/"R299_MACHINE_RECEIPT.json"
Z,O=Q(0),Q(1)
REWARDS=(0,2)
GAMMAS=(Z,Q(1,2),O)
ALPHAS=(Q(1,2),O)
METHODS=("TD0_ONLINE","MC_FULL_RETURN")
TIMES=range(5)
WORLDS=list(itertools.product(REWARDS,GAMMAS,ALPHAS,METHODS))
COLUMNS=("epoch","prior_S0_value","prior_S1_value","S0_update_target",
         "S1_update_target","S0_update_error","S1_update_error",
         "learned_S0_value","learned_S1_value","oracle_S0_policy_return",
         "oracle_S1_policy_return","S0_abs_error","S1_abs_error")

def readjson(path):return json.loads(path.read_text(encoding="utf-8"))
def source():
    with CSV.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def label(w):
    r,g,a,kind=w
    return f"reward={r}|gamma={g}|alpha={a}|method={kind}"

def independently_reconstruct(w):
    reward,gamma,alpha,kind=w
    state0=state1=Z
    out=[]
    for t in TIMES:
        prev0,prev1=state0,state1
        if t==0:
            goal0=goal1=diff0=diff1=Z
        else:
            goal0=gamma*prev1 if kind=="TD0_ONLINE" else gamma*reward
            diff0=goal0-prev0
            state0=prev0+alpha*diff0
            goal1=Q(reward)
            diff1=goal1-prev1
            state1=prev1+alpha*diff1
        out.append({"epoch":t,"prior_S0_value":prev0,"prior_S1_value":prev1,
          "S0_update_target":goal0,"S1_update_target":goal1,
          "S0_update_error":diff0,"S1_update_error":diff1,
          "learned_S0_value":state0,"learned_S1_value":state1,
          "oracle_S0_policy_return":gamma*reward,"oracle_S1_policy_return":Q(reward),
          "S0_abs_error":abs(gamma*reward-state0),"S1_abs_error":abs(Q(reward)-state1)})
    return out

def independent_math(w,t):
    r,g,a,method=w
    q=O-a
    val1=r*(O-q**t)
    if method=="MC_FULL_RETURN":val0=g*r*(O-q**t)
    elif t==0:val0=Z
    else:val0=g*r*(O-q**t-a*t*q**(t-1))
    return val0,val1

def verify(rows,results):
    if len(rows)!=120 or len(results["worlds"])!=24:raise AssertionError("incomplete sources or worlds")
    if results["original_exact_source_rows"]!=120 or results["synthetic_worlds"]!=24:raise AssertionError("wrong frozen size")
    table=defaultdict(dict)
    for row in rows:
        try:
            key=(int(row["terminal_reward"]),Q(row["gamma"]),Q(row["alpha"]),row["algorithm"])
            t=int(row["epoch"])
        except (ValueError,KeyError,ZeroDivisionError) as e:raise AssertionError("invalid row dimension") from e
        if key not in WORLDS or t not in TIMES:raise AssertionError("unexpected source dimension")
        if t in table[key]:raise AssertionError("duplicate source")
        if row["world"]!=label(key):raise AssertionError("source label tamper")
        expected=independently_reconstruct(key)[t]
        if t!=expected["epoch"]:raise AssertionError("time index mismatch")
        if (expected["learned_S0_value"],expected["learned_S1_value"])!=independent_math(key,t):
            raise AssertionError("independent formula and recurrence conflict")
        for field in COLUMNS[1:]:
            if Q(row[field])!=expected[field]:raise AssertionError("source field tamper: "+field)
        table[key][t]=expected
    if set(table)!=set(WORLDS):raise AssertionError("world missing")
    for ix,w in enumerate(WORLDS):
        if set(table[w])!=set(TIMES):raise AssertionError("epoch missing")
        recorded=results["worlds"][ix]
        r,g,a,kind=w
        if (recorded["world"],recorded["terminal_reward"],recorded["gamma"],recorded["alpha"],recorded["algorithm"])!=(label(w),r,str(g),str(a),kind):
            raise AssertionError("result identity wrong")
        if recorded["source_epochs"]!=5 or len(recorded["epoch_results"])!=5:raise AssertionError("result epoch count")
        for t in TIMES:
            expect={x:str(table[w][t][x]) for x in COLUMNS}
            if recorded["epoch_results"][t]!=expect:raise AssertionError("results do not independently match original source")
    special=results["reference_reward2_gamma_half_alpha_half_epoch4"]
    if special!={"TD0_S0":"11/16","MC_S0":"15/16","common_S1":"15/8","oracle_S0":"1"}:
        raise AssertionError("special case mismatch")
    for reward,gamma,alpha in itertools.product(REWARDS,GAMMAS,ALPHAS):
        for t in TIMES:
            td=table[(reward,gamma,alpha,"TD0_ONLINE")][t]
            mc=table[(reward,gamma,alpha,"MC_FULL_RETURN")][t]
            if td["learned_S1_value"]!=mc["learned_S1_value"]:raise AssertionError("same terminal learning negative control")
            if td["learned_S0_value"]>mc["learned_S0_value"]:raise AssertionError("unexpected delayed credit ordering")
            if t==0 and (td["S0_update_target"]!=Z or mc["S0_update_target"]!=Z):
                raise AssertionError("epoch-zero behavior")
    return {"original_labeled_sources":120,"exact_model_free_worlds":24,
      "independent_recursion_and_closed_form_all_sources":"PASS",
      "original_R063_social_learning_not_appropriated_as_R299_E2":True,
      "real_human_E2_added":0,"real_animal_E2_added":0,"historical_E3_added":0}

def audit():
    receipt,result=readjson(RECEIPT),readjson(JSON)
    freeze="f8885c130b2d6d12280cd6ace30085b3ad90e835"
    if receipt["freeze_commit"]!=freeze or result["freeze_commit"]!=freeze:raise AssertionError("prescore source missing")
    if result["original_catalogue_id"]!="02-005":raise AssertionError("wrong candidate")
    if receipt["original_source_rows"]!=120:raise AssertionError("receipt source universe wrong")
    if any(receipt[k]!=0 for k in ("human_E2_added","animal_E2_added","historical_E3_added")):
        raise AssertionError("overclaimed synthetic evidence")
    if any(result[k]!=0 for k in ("real_human_E2_added","real_animal_E2_added","historical_E3_added")):
        raise AssertionError("overclaimed experiment")
    if result["existing_R063_human_metadata_cannot_be_reused_as_new_R299_E2"] is not True:
        raise AssertionError("prior R063 scope was stolen")
    if hashlib.sha256(CSV.read_bytes()).hexdigest()!=receipt["source_sha256"]:raise AssertionError("source sha")
    if hashlib.sha256(JSON.read_bytes()).hexdigest()!=receipt["results_sha256"]:raise AssertionError("result sha")
    return {**verify(source(),result),"source_sha256":receipt["source_sha256"],
            "results_sha256":receipt["results_sha256"]}

class Tests(unittest.TestCase):
    def test_full(self):self.assertEqual(audit()["original_labeled_sources"],120)
    def test_worlds(self):self.assertEqual(len(WORLDS),24)
    def test_reference_td(self):self.assertEqual(independently_reconstruct((2,Q(1,2),Q(1,2),"TD0_ONLINE"))[4]["learned_S0_value"],Q(11,16))
    def test_reference_mc(self):self.assertEqual(independently_reconstruct((2,Q(1,2),Q(1,2),"MC_FULL_RETURN"))[4]["learned_S0_value"],Q(15,16))
    def test_first_td_zero(self):self.assertEqual(independently_reconstruct((2,O,O,"TD0_ONLINE"))[1]["learned_S0_value"],Z)
    def test_second_td(self):self.assertEqual(independently_reconstruct((2,Q(1,2),O,"TD0_ONLINE"))[2]["learned_S0_value"],O)
    def test_source_delete(self):
        with self.assertRaises(AssertionError):verify(source()[:-1],readjson(JSON))
    def test_source_duplicate(self):
        d=source();d[1]=dict(d[0])
        with self.assertRaises(AssertionError):verify(d,readjson(JSON))
    def test_source_target(self):
        d=source();d[1]=dict(d[1]);d[1]["S0_update_target"]="777"
        with self.assertRaises(AssertionError):verify(d,readjson(JSON))
    def test_wrong_episode_old_state(self):
        d=source();d[1]=dict(d[1]);d[1]["prior_S1_value"]="3"
        with self.assertRaises(AssertionError):verify(d,readjson(JSON))
    def test_bad_reward(self):
        d=source();d[1]=dict(d[1]);d[1]["terminal_reward"]="10"
        with self.assertRaises(AssertionError):verify(d,readjson(JSON))
    def test_nonexistent_algorithm(self):
        d=source();d[1]=dict(d[1]);d[1]["algorithm"]="MODEL_BASED"
        with self.assertRaises(AssertionError):verify(d,readjson(JSON))
    def test_output_tamper(self):
        j=readjson(JSON);j["worlds"][0]["epoch_results"][1]["S1_update_target"]="888"
        with self.assertRaises(AssertionError):verify(source(),j)
    def test_fake_premature_td_credit(self):
        d=source()
        ix=next(i for i,r in enumerate(d) if r["terminal_reward"]=="2" and r["gamma"]=="1" and r["alpha"]=="1" and r["algorithm"]=="TD0_ONLINE" and r["epoch"]=="1")
        d[ix]=dict(d[ix]);d[ix]["learned_S0_value"]="2"
        with self.assertRaises(AssertionError):verify(d,readjson(JSON))
    def test_digest_tamper(self):self.assertNotEqual(hashlib.sha256(CSV.read_bytes()+b"fake").hexdigest(),readjson(RECEIPT)["source_sha256"])
    def test_prior_R063(self):self.assertTrue(audit()["original_R063_social_learning_not_appropriated_as_R299_E2"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R299 independent"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
