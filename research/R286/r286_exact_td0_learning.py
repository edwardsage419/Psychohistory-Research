#!/usr/bin/env python3
"""R286: exact temporal-difference credit assignment versus complete returns.

Original 239 catalogue P0 02-002. Purely artificial sixbit source worlds.
Never use held-out Y6 when fitting V(A) from five earlier episodes.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
FREEZE="d055e14831565571ca9e953d311b55e7eed9ef42"
P=(F(1,4),F(1,2),F(3,4))
POLICIES=("TD0_ONLINE_CORRECT","MC_COMPLETE_RETURN","B_THEN_A_UPDATED_BOOTSTRAP")
ORIGINAL=tuple("".join(s) for s in itertools.product("01",repeat=6))
ZERO,ONE=F(0),F(1)
COEFFS={
 "TD0_ONLINE_CORRECT":(F(1,8),F(3,16),F(1,4),F(1,4),F(0)),
 "MC_COMPLETE_RETURN":(F(1,32),F(1,16),F(1,8),F(1,4),F(1,2)),
 "B_THEN_A_UPDATED_BOOTSTRAP":(F(5,64),F(1,8),F(3,16),F(1,4),F(1,4))
}
LOCKED={
(F(1,4),"TD0_ONLINE_CORRECT"):F(57,256),
(F(1,4),"MC_COMPLETE_RETURN"):F(1,4),
(F(1,4),"B_THEN_A_UPDATED_BOOTSTRAP"):F(3643,16384),
(F(1,2),"TD0_ONLINE_CORRECT"):F(155,512),
(F(1,2),"MC_COMPLETE_RETURN"):F(683,2048),
(F(1,2),"B_THEN_A_UPDATED_BOOTSTRAP"):F(2445,8192),
(F(3,4),"TD0_ONLINE_CORRECT"):F(123,512),
(F(3,4),"MC_COMPLETE_RETURN"):F(513,2048),
(F(3,4),"B_THEN_A_UPDATED_BOOTSTRAP"):F(3741,16384)
}
def validate(p,policy):
    if p not in P or policy not in POLICIES:raise ValueError("not a frozen 3x3 world")
def read_source(s):
    if not isinstance(s,str) or len(s)!=6 or any(x not in "01" for x in s):
        raise ValueError("require exactly five past reward bits and one future bit")
    return tuple(map(int,s))
def episodes(training,policy):
    if policy not in POLICIES:raise ValueError("unfrozen TD algorithm")
    if len(training)!=5 or any(type(x) is not int or x not in (0,1) for x in training):
        raise ValueError("five binary train rewards required")
    va=vb=ZERO
    out=[]
    for reward in training:
        r=F(reward)
        if policy=="TD0_ONLINE_CORRECT":
            # Must process A->B with reward zero before seeing terminal Y.
            va=va+(vb-va)/2
            vb=vb+(r-vb)/2
        elif policy=="MC_COMPLETE_RETURN":
            va=va+(r-va)/2
            vb=vb+(r-vb)/2
        else:
            vb=vb+(r-vb)/2
            va=va+(vb-va)/2
        out.append((va,vb))
    return tuple(out)
def independent_coefficients(policy):
    """Independent symbolic route: no calls to per-episode learner."""
    if policy not in POLICIES:raise ValueError("unknown")
    n=5
    if policy=="TD0_ONLINE_CORRECT":
        return tuple(F(n-j,2**(n-j+1)) for j in range(1,n+1))
    if policy=="MC_COMPLETE_RETURN":
        return tuple(F(1,2**(n-j+1)) for j in range(1,n+1))
    return tuple(F(n-j+1,2**(n-j+2)) for j in range(1,n+1))
def original_source_mass(p,s):
    if p not in P:raise ValueError("truth outside frozen set")
    ys=read_source(s);k=sum(ys)
    return p**k*(ONE-p)**(6-k)
def source_row(p,policy,s):
    validate(p,policy);ys=read_source(s)
    trajectory=episodes(ys[:5],policy)
    v=trajectory[-1][0]
    return dict(world="P"+str(p).replace("/","of")+"_"+policy,
      true_p=p,policy=policy,ordered_all_original_Y1_Y2_Y3_Y4_Y5_Y6=s,
      original_5_train_bits=s[:5],future_heldout_Y6=ys[5],
      complete_source_probability=original_source_mass(p,s),
      train_A_value_after_each_episode=";".join(str(z[0]) for z in trajectory),
      train_B_value_after_each_episode=";".join(str(z[1]) for z in trajectory),
      train_A_value_after_episode5=v,
      future_Brier_squared_error=(F(ys[5])-v)**2)
def source_rows(p,policy):
    validate(p,policy)
    for s in ORIGINAL:yield source_row(p,policy,s)
def full_source_risk(p,policy):
    allrows=tuple(source_rows(p,policy))
    assert len(allrows)==64 and len({z["ordered_all_original_Y1_Y2_Y3_Y4_Y5_Y6"] for z in allrows})==64
    assert sum((z["complete_source_probability"] for z in allrows),ZERO)==ONE
    return sum((z["complete_source_probability"]*z["future_Brier_squared_error"] for z in allrows),ZERO)
def independent_analytic_risk(p,policy):
    """Second method: independent Bernoulli moments on coefficient vector."""
    validate(p,policy)
    cs=independent_coefficients(policy)
    s=sum(cs,ZERO);v=sum((x*x for x in cs),ZERO)
    return p*(ONE-p)+p*p*(ONE-s)**2+p*(ONE-p)*v
def frozen_claims():
    assert len(ORIGINAL)==64 and len(P)==3 and len(POLICIES)==3
    for policy in POLICIES:
        assert COEFFS[policy]==independent_coefficients(policy)
        for s in ORIGINAL:
            ys=read_source(s)
            val=episodes(ys[:5],policy)[-1][0]
            expected=sum((w*F(ys[i]) for i,w in enumerate(COEFFS[policy])),ZERO)
            assert val==expected,(policy,s,val,expected)
    for p in P:
        for policy in POLICIES:
            assert full_source_risk(p,policy)==independent_analytic_risk(p,policy)==LOCKED[p,policy]
    assert episodes((1,0,0,0,0),"TD0_ONLINE_CORRECT")[0][0]==ZERO
    assert episodes((1,0,0,0,0),"MC_COMPLETE_RETURN")[0][0]==F(1,2)
    assert episodes((1,0,0,0,0),"B_THEN_A_UPDATED_BOOTSTRAP")[0][0]==F(1,4)
    return True
def emit():
    frozen_claims()
    source=ROOT/"R286_ALL_576_ORIGINAL_TD0_SIXBIT_FUTURE_SOURCES.csv"
    columns=("world","true_p","policy","ordered_all_original_Y1_Y2_Y3_Y4_Y5_Y6",
      "original_5_train_bits","future_heldout_Y6","complete_source_probability",
      "train_A_value_after_each_episode","train_B_value_after_each_episode",
      "train_A_value_after_episode5","future_Brier_squared_error")
    with source.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=columns,lineterminator="\n")
        writer.writeheader()
        for p in P:
            for policy in POLICIES:
                for item in source_rows(p,policy):
                    writer.writerow({k:str(item[k]) for k in columns})
    result=dict(research_id="R286",catalogue_original_id="02-002",
       prescore_freeze_commit=FREEZE,
       scope="BOUNDED_E1_SYNTHETIC_TD0_TRAINING_TIME_VS_MC_AND_REORDERING",
       original_worlds=9,model_labeled_complete_source_types=576,
       no_real_experimental_E2=0,no_real_historical_E3=0,
       actual_train_episodes=5,heldout_future_episodes=1,
       no_heldout_bit_ever_used_for_training=True,
       reverse_order_is_separate_offline_schedule_not_online_TD0=True,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       results=[dict(true_p=str(p),policy=policy,original_source_count=64,
         exact_mean_heldout_Brier=str(full_source_risk(p,policy)),
         independent_coefficient_moment_risk=str(independent_analytic_risk(p,policy)),
         train_A_reward_coefficients=list(map(str,independent_coefficients(policy))),
         independent_method_agreement=True)
         for p in P for policy in POLICIES])
    target=ROOT/"R286_EXACT_TD0_RESULTS.json"
    target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R286",original_catalogue_id="02-002",prescore_freeze_commit=FREEZE,
       original_labeled_sixbit_source_types=576,
       source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
       real_human_E2=0,real_historical_E3=0)
    (ROOT/"R286_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt
class Tests(unittest.TestCase):
    def test_all(self):self.assertTrue(frozen_claims())
    def test_counts(self):self.assertEqual(len(ORIGINAL),64)
    def test_regimes(self):self.assertEqual(len(P),3)
    def test_policies(self):self.assertEqual(len(POLICIES),3)
    def test_zero(self):self.assertEqual(episodes((0,0,0,0,0),"TD0_ONLINE_CORRECT")[-1],(ZERO,ZERO))
    def test_immediate_A_td(self):self.assertEqual(episodes((1,0,0,0,0),"TD0_ONLINE_CORRECT")[0][0],ZERO)
    def test_first_A_mc(self):self.assertEqual(episodes((1,0,0,0,0),"MC_COMPLETE_RETURN")[0][0],F(1,2))
    def test_first_A_reverse(self):self.assertEqual(episodes((1,0,0,0,0),"B_THEN_A_UPDATED_BOOTSTRAP")[0][0],F(1,4))
    def test_five_train_one_future(self):self.assertEqual(source_row(F(1,2),POLICIES[0],"000001")["train_A_value_after_episode5"],ZERO)
    def test_invalid(self):
        with self.assertRaises(ValueError):read_source("101")
    def test_invalid_truth(self):
        with self.assertRaises(ValueError):list(source_rows(F(1,3),POLICIES[0]))
    def test_invalid_policy(self):
        with self.assertRaises(ValueError):episodes((1,0,0,0,0),"WRONG")
def case(p,policy,kind):
    def test(self):
        records=tuple(source_rows(p,policy))
        if kind=="count":self.assertEqual(len(records),64)
        elif kind=="mass":self.assertEqual(sum((r["complete_source_probability"] for r in records),ZERO),ONE)
        elif kind=="unique":self.assertEqual(len({r["ordered_all_original_Y1_Y2_Y3_Y4_Y5_Y6"] for r in records}),64)
        elif kind=="closed":self.assertEqual(full_source_risk(p,policy),LOCKED[p,policy])
        elif kind=="independent":self.assertEqual(full_source_risk(p,policy),independent_analytic_risk(p,policy))
        elif kind=="coef":self.assertEqual(COEFFS[policy],independent_coefficients(policy))
        elif kind=="source":
            for r in records:
                self.assertEqual(r["complete_source_probability"],original_source_mass(p,r["ordered_all_original_Y1_Y2_Y3_Y4_Y5_Y6"]))
        elif kind=="future":
            for r in records:
                ss=r["ordered_all_original_Y1_Y2_Y3_Y4_Y5_Y6"]
                self.assertEqual(r["train_A_value_after_episode5"],episodes(read_source(ss)[:5],policy)[-1][0])
        elif kind=="score":
            for r in records:
                self.assertEqual(r["future_Brier_squared_error"],(F(r["future_heldout_Y6"])-r["train_A_value_after_episode5"])**2)
        else:raise AssertionError("unknown case")
    return test
for p in P:
    for policy in POLICIES:
        for kind in ("count","mass","unique","closed","independent","coef","source","future","score"):
            setattr(Tests,"test_p"+str(p).replace("/","of")+"_"+policy.lower()+"_"+kind,case(p,policy,kind))
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    if args.test:unittest.main(argv=["r286"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
