#!/usr/bin/env python3
"""R299 exact synthetic model-free fixed-policy state-value prediction: TD0 vs Monte Carlo."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="f8885c130b2d6d12280cd6ace30085b3ad90e835"
ZERO,ONE=F(0),F(1)
REWARDS=(0,2)
GAMMAS=(ZERO,F(1,2),ONE)
ALPHAS=(F(1,2),ONE)
METHODS=("TD0_ONLINE","MC_FULL_RETURN")
EPOCHS=range(5)
WORLDS=tuple(itertools.product(REWARDS,GAMMAS,ALPHAS,METHODS))
SOURCE_NAME="R299_ALL_120_ORIGINAL_MODEL_FREE_TD_MC_STATES.csv"
RESULT_NAME="R299_EXACT_MODEL_FREE_TD_MC_RESULTS.json"
RECEIPT_NAME="R299_MACHINE_RECEIPT.json"

def worldid(reward,gamma,alpha,method):
    return f"reward={reward}|gamma={gamma}|alpha={alpha}|method={method}"

def exact_form(reward,gamma,alpha,method,epoch):
    if (reward,gamma,alpha,method) not in WORLDS or epoch not in EPOCHS:
        raise ValueError("unfrozen state")
    q=ONE-alpha
    s1=F(reward)*(ONE-q**epoch)
    if method=="MC_FULL_RETURN":
        s0=gamma*reward*(ONE-q**epoch)
    elif epoch==0:
        s0=ZERO
    else:
        s0=gamma*reward*(ONE-q**epoch-alpha*epoch*q**(epoch-1))
    return s0,s1

def trajectory(reward,gamma,alpha,method):
    if (reward,gamma,alpha,method) not in WORLDS:raise ValueError("unfrozen world")
    a=b=ZERO
    allrows=[]
    for epoch in EPOCHS:
        old_a,old_b=a,b
        if epoch==0:
            target_a=target_b=delta_a=delta_b=ZERO
        else:
            # S0 observation precedes terminal reward: online TD bootstraps OLD S1.
            target_a=gamma*old_b if method=="TD0_ONLINE" else gamma*reward
            delta_a=target_a-old_a
            a=old_a+alpha*delta_a
            target_b=F(reward)
            delta_b=target_b-old_b
            b=old_b+alpha*delta_b
        assert (a,b)==exact_form(reward,gamma,alpha,method,epoch)
        allrows.append({"world":worldid(reward,gamma,alpha,method),
          "terminal_reward":reward,"gamma":gamma,"alpha":alpha,"algorithm":method,"epoch":epoch,
          "prior_S0_value":old_a,"prior_S1_value":old_b,
          "S0_update_target":target_a,"S1_update_target":target_b,
          "S0_update_error":delta_a,"S1_update_error":delta_b,
          "learned_S0_value":a,"learned_S1_value":b,
          "oracle_S0_policy_return":gamma*reward,
          "oracle_S1_policy_return":F(reward),
          "S0_abs_error":abs(gamma*reward-a),
          "S1_abs_error":abs(F(reward)-b)})
    return tuple(allrows)

def allrows():
    return tuple(r for w in WORLDS for r in trajectory(*w))

def check():
    assert len(WORLDS)==24 and len(allrows())==120
    assert len({(x["world"],x["epoch"]) for x in allrows()})==120
    for reward,gamma,alpha,method in WORLDS:
        sequence=trajectory(reward,gamma,alpha,method)
        for epoch,row in enumerate(sequence):
            assert row["learned_S0_value"]==exact_form(reward,gamma,alpha,method,epoch)[0]
            assert row["learned_S1_value"]==exact_form(reward,gamma,alpha,method,epoch)[1]
            assert row["learned_S0_value"]>=ZERO and row["learned_S1_value"]>=ZERO
            if epoch>=1:
                assert row["learned_S0_value"]==row["prior_S0_value"]+alpha*row["S0_update_error"]
                assert row["learned_S1_value"]==row["prior_S1_value"]+alpha*row["S1_update_error"]
                if method=="TD0_ONLINE":assert row["S0_update_target"]==gamma*row["prior_S1_value"]
                else:assert row["S0_update_target"]==gamma*reward
            if reward==0 or gamma==0:assert row["learned_S0_value"]==ZERO
            if reward==0:assert row["learned_S1_value"]==ZERO
    for reward,gamma,alpha in itertools.product(REWARDS,GAMMAS,ALPHAS):
        for epoch in EPOCHS:
            td=exact_form(reward,gamma,alpha,"TD0_ONLINE",epoch)
            mc=exact_form(reward,gamma,alpha,"MC_FULL_RETURN",epoch)
            assert td[1]==mc[1] and td[0]<=mc[0]
    assert exact_form(2,F(1,2),F(1,2),"TD0_ONLINE",4)==(F(11,16),F(15,8))
    assert exact_form(2,F(1,2),F(1,2),"MC_FULL_RETURN",4)==(F(15,16),F(15,8))
    assert exact_form(2,F(1,2),ONE,"TD0_ONLINE",1)[0]==ZERO
    assert exact_form(2,F(1,2),ONE,"TD0_ONLINE",2)[0]==ONE
    assert exact_form(2,F(1,2),ONE,"MC_FULL_RETURN",1)[0]==ONE
    return True

def emit():
    check()
    cols=("world","terminal_reward","gamma","alpha","algorithm","epoch",
      "prior_S0_value","prior_S1_value","S0_update_target","S1_update_target",
      "S0_update_error","S1_update_error","learned_S0_value","learned_S1_value",
      "oracle_S0_policy_return","oracle_S1_policy_return","S0_abs_error","S1_abs_error")
    path=ROOT/SOURCE_NAME
    with path.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        writer.writeheader()
        for r in allrows():writer.writerow({k:str(r[k]) for k in cols})
    result={"research_id":"R299","original_catalogue_id":"02-005","freeze_commit":FREEZE,
      "scope":"ARTIFICIAL_E1_FIXED_POLICY_TD0_VS_MONTE_CARLO_NO_TRANSITION_MODEL_OR_REAL_DATA",
      "synthetic_worlds":24,"original_exact_source_rows":120,
      "real_human_E2_added":0,"real_animal_E2_added":0,"historical_E3_added":0,
      "existing_R063_human_metadata_cannot_be_reused_as_new_R299_E2":True,
      "R073":"FROZEN","PESEN_v0_1":"FROZEN",
      "worlds":[]}
    for world in WORLDS:
        reward,gamma,alpha,method=world
        source=trajectory(*world)
        result["worlds"].append({
          "world":worldid(*world),"terminal_reward":reward,"gamma":str(gamma),
          "alpha":str(alpha),"algorithm":method,"source_epochs":5,
          "epoch_results":[{k:str(r[k]) for k in (
              "epoch","prior_S0_value","prior_S1_value",
              "S0_update_target","S1_update_target","S0_update_error","S1_update_error",
              "learned_S0_value","learned_S1_value","oracle_S0_policy_return",
              "oracle_S1_policy_return","S0_abs_error","S1_abs_error")} for r in source]})
    result["reference_reward2_gamma_half_alpha_half_epoch4"]={
       "TD0_S0":"11/16","MC_S0":"15/16","common_S1":"15/8","oracle_S0":"1"}
    rp=ROOT/RESULT_NAME
    rp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"research_id":"R299","freeze_commit":FREEZE,"original_source_rows":120,
      "source_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
      "results_sha256":hashlib.sha256(rp.read_bytes()).hexdigest(),
      "human_E2_added":0,"animal_E2_added":0,"historical_E3_added":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_claims(self):self.assertTrue(check())
    def test_source_count(self):self.assertEqual(len(allrows()),120)
    def test_worlds(self):self.assertEqual(len(WORLDS),24)
    def test_td_delayed_credit(self):self.assertEqual(exact_form(2,F(1,2),F(1,2),"TD0_ONLINE",4)[0],F(11,16))
    def test_mc_terminal_return(self):self.assertEqual(exact_form(2,F(1,2),F(1,2),"MC_FULL_RETURN",4)[0],F(15,16))
    def test_first_td_zero(self):self.assertEqual(exact_form(2,ONE,ONE,"TD0_ONLINE",1)[0],ZERO)
    def test_second_td(self):self.assertEqual(exact_form(2,F(1,2),ONE,"TD0_ONLINE",2)[0],ONE)
    def test_first_mc(self):self.assertEqual(exact_form(2,F(1,2),ONE,"MC_FULL_RETURN",1)[0],ONE)
    def test_discount_zero(self):self.assertEqual(exact_form(2,ZERO,ONE,"MC_FULL_RETURN",4)[0],ZERO)
    def test_no_reward(self):self.assertEqual(exact_form(0,ONE,ONE,"TD0_ONLINE",4),(ZERO,ZERO))
    def test_bad_method(self):
        with self.assertRaises(ValueError):trajectory(2,ONE,ONE,"NOT_A_METHOD")
    def test_bad_epoch(self):
        with self.assertRaises(ValueError):exact_form(2,ONE,ONE,"TD0_ONLINE",5)

def create_case(world,n,kind):
    def fn(self):
        r=trajectory(*world)[n]
        if kind=="formula":self.assertEqual((r["learned_S0_value"],r["learned_S1_value"]),exact_form(*world,n))
        elif kind=="conservation":self.assertEqual(r["S0_abs_error"],abs(r["oracle_S0_policy_return"]-r["learned_S0_value"]))
        elif kind=="lag":self.assertEqual(r["S0_update_target"],(ZERO if n==0 else (world[1]*r["prior_S1_value"] if world[3]=="TD0_ONLINE" else world[1]*world[0])))
        elif kind=="terminal":self.assertEqual(r["S1_update_error"],ZERO if n==0 else world[0]-r["prior_S1_value"])
        else:raise AssertionError(kind)
    return fn
for i,w in enumerate(WORLDS):
    for n in EPOCHS:
        for kind in ("formula","conservation","lag","terminal"):
            setattr(Tests,f"test_world{i}_epoch{n}_{kind}",create_case(w,n,kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R299"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
