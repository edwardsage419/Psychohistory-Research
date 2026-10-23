#!/usr/bin/env python3
"""Independent R297 Q-learning original 120-vector, 24-world audit, no main-model imports."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research/R297"
SOURCE=ROOT/"R297_ALL_120_ORIGINAL_Q_LEARNING_Q_VECTOR_SOURCES.csv"
RESULT=ROOT/"R297_EXACT_Q_LEARNING_OFF_POLICY_RESULTS.json"
RECEIPT=ROOT/"R297_MACHINE_RECEIPT.json"
GAMMAS=(Q(0),Q(1,2),Q(1))
ALPHAS=(Q(1,2),Q(1))
COVERAGES=("FULL","GOOD_MISSING")
BACKUPS=("OFF_POLICY_MAX","BEHAVIOR_BAD")
EPOCHS=range(5)
WORLDS=list(itertools.product(GAMMAS,ALPHAS,COVERAGES,BACKUPS))
QFIELDS=("Q_S0_SAFE","Q_S0_EXPLORE","Q_S1_GOOD","Q_S1_BAD","target_S0_EXPLORE",
         "oracle_Qstar_S0_SAFE","oracle_Qstar_S0_EXPLORE")
META=("epoch","chosen_S0","oracle_best_S0","oracle_action_agreement")
Z,O=Q(0),Q(1)

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def load():
    with SOURCE.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def ident(gamma,alpha,coverage,bootstrap):
    return f"gamma={gamma}|alpha={alpha}|coverage={coverage}|bootstrap={bootstrap}"
def counterfactual_optimal(gamma):
    safe=O
    explore=Q(3)*gamma
    return safe,explore,"EXPLORE" if explore>safe else "SAFE"

def independent_trajectory(gamma,alpha,coverage,bootstrap):
    safe=explore=good=bad=Z
    seq=[]
    for m in EPOCHS:
        if m:
            # Samples from S1 and S0 have rewards 3,0,1,0 respectively.
            if coverage=="FULL":
                good=(O-alpha)*good+alpha*Q(3)
            bad=(O-alpha)*bad
            safe=(O-alpha)*safe+alpha*O
            if bootstrap=="OFF_POLICY_MAX":
                target=gamma*(good if good>=bad else bad)
            else:
                # Forced bad continuation is a different behavior action,
                # not an estimate of max future return.
                target=gamma*bad
            explore=(O-alpha)*explore+alpha*target
        else:target=Z
        opt_safe,opt_explore,opt_action=counterfactual_optimal(gamma)
        policy="EXPLORE" if explore>safe else "SAFE"
        seq.append({"epoch":m,"Q_S0_SAFE":safe,"Q_S0_EXPLORE":explore,
                    "Q_S1_GOOD":good,"Q_S1_BAD":bad,"target_S0_EXPLORE":target,
                    "chosen_S0":policy,"oracle_Qstar_S0_SAFE":opt_safe,
                    "oracle_Qstar_S0_EXPLORE":opt_explore,"oracle_best_S0":opt_action,
                    "oracle_action_agreement":str(policy==opt_action)})
    return seq

def independent_analytic(gamma,alpha,coverage,bootstrap,m):
    remain=(O-alpha)**m
    safe=O-remain
    good=Q(3)*(O-remain) if coverage=="FULL" else Z
    if coverage=="FULL" and bootstrap=="OFF_POLICY_MAX":
        exp=Q(3)*gamma*(O-remain-alpha*m*remain)
        target=gamma*good
    else:
        exp=target=Z
    return (safe,exp,good,Z,target)

def verify(rows,result):
    if len(rows)!=120 or result["world_count"]!=24 or len(result["worlds"])!=24:raise AssertionError("world/source count")
    if result["full_original_Q_vector_source_rows"]!=120 or result["epochs_each"]!=5:raise AssertionError("wrong epoch metadata")
    observed=defaultdict(dict)
    for row in rows:
        try:
            gamma,alpha=Q(row["gamma"]),Q(row["alpha"])
            coverage,bootstrap=row["coverage"],row["backup_rule"]
            epoch=int(row["epoch"])
        except (KeyError,ValueError,ZeroDivisionError) as err:raise AssertionError("bad row schema") from err
        w=(gamma,alpha,coverage,bootstrap)
        if w not in WORLDS or epoch not in EPOCHS:raise AssertionError("unfrozen parameter")
        if epoch in observed[w]:raise AssertionError("duplicate original source")
        if row["world"]!=ident(*w):raise AssertionError("incorrect world label")
        expected=independent_trajectory(*w)[epoch]
        formula=independent_analytic(*w,epoch)
        if tuple(expected[k] for k in QFIELDS[:5])!=formula:raise AssertionError("recurrence disagrees independent formula")
        for key in QFIELDS:
            if Q(row[key])!=expected[key]:raise AssertionError("corrupt value "+key)
        for key in ("chosen_S0","oracle_best_S0","oracle_action_agreement"):
            if row[key]!=expected[key]:raise AssertionError("wrong policy/oracle flag "+key)
        observed[w][epoch]=expected
    if len(observed)!=24:raise AssertionError("missing world")
    agreements=0
    total_disagreements=0
    for i,w in enumerate(WORLDS):
        if set(observed[w])!=set(EPOCHS):raise AssertionError("missing epoch")
        world=result["worlds"][i]
        gamma,alpha,coverage,bootstrap=w
        if world["world"]!=ident(*w) or world["gamma"]!=str(gamma) or world["alpha"]!=str(alpha):raise AssertionError("result world identity")
        if world["coverage"]!=coverage or world["backup_rule"]!=bootstrap or world["full_source_rows"]!=5:raise AssertionError("result config")
        if len(world["epoch_records"])!=5:raise AssertionError("result incomplete")
        for epoch in EPOCHS:
            source=observed[w][epoch]
            correct={k:str(value) for k,value in source.items()}
            if world["epoch_records"][epoch]!=correct:raise AssertionError("result state differs from source")
        last=observed[w][4]
        ok=last["oracle_action_agreement"]=="True"
        agreements+=int(ok)
        total_disagreements+=int(not ok)
        if world["epoch4_action"]!=last["chosen_S0"] or world["epoch4_oracle_agreement"]!=ok:raise AssertionError("result verdict wrong")
    if agreements!=12 or total_disagreements!=12:raise AssertionError("oracle alignment counts wrong")
    if result["epoch4_oracle_correct_worlds"]!=12 or result["epoch4_oracle_disagreement_worlds"]!=12:raise AssertionError("summary mismatch")
    reference=result["reference_gamma_half_alpha_half_FULL_MAX_epoch4"]
    if reference!={"Q_S0_SAFE":"15/16","Q_S0_EXPLORE":"39/32","Q_S1_GOOD":"45/16",
                  "epoch1_action":"SAFE","epoch2_tie_choose":"SAFE","epoch4_action":"EXPLORE"}:raise AssertionError("frozen special case wrong")
    return {"R297_independent_source_audit":"PASS","exact_original_Q_vectors":120,
            "artificial_worlds":24,"full_recursion_and_closed_form_states":120,
            "epoch4_agrees_with_unconstrained_optimal_policy":12,
            "epoch4_disagrees_with_unconstrained_optimal_policy":12,
            "human_E2":0,"animal_E2":0,"historical_E3":0}

def audit():
    receipt,result=obj(RECEIPT),obj(RESULT)
    freeze="fd66badd5a110b36cc97564f7e1a29daba4298ba"
    if receipt["freeze_commit"]!=freeze or result["freeze_commit"]!=freeze:raise AssertionError("not prospectively frozen")
    if result["original_catalogue_id"]!="02-003" or result["human_E2"]!=0 or result["real_animal_E2"]!=0 or result["historical_E3"]!=0:raise AssertionError("scientific provenance false")
    if receipt["original_source_rows"]!=120 or receipt["real_human_E2"]!=0 or receipt["real_animal_E2"]!=0 or receipt["historical_E3"]!=0:raise AssertionError("receipt false")
    if receipt["sources_sha256"]!=hashlib.sha256(SOURCE.read_bytes()).hexdigest():raise AssertionError("source byte checksum")
    if receipt["results_sha256"]!=hashlib.sha256(RESULT.read_bytes()).hexdigest():raise AssertionError("result byte checksum")
    return {**verify(load(),result),"source_sha256":receipt["sources_sha256"],"results_sha256":receipt["results_sha256"]}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["exact_original_Q_vectors"],120)
    def test_world_count(self):self.assertEqual(len(WORLDS),24)
    def test_epoch_count(self):self.assertEqual(len(EPOCHS),5)
    def test_closed_form(self):self.assertEqual(independent_analytic(Q(1,2),Q(1,2),"FULL","OFF_POLICY_MAX",4)[1],Q(39,32))
    def test_no_good_coverage(self):self.assertEqual(independent_trajectory(O,O,"GOOD_MISSING","OFF_POLICY_MAX")[4]["Q_S1_GOOD"],Z)
    def test_full_max(self):self.assertEqual(independent_trajectory(O,O,"FULL","OFF_POLICY_MAX")[4]["Q_S0_EXPLORE"],Q(3))
    def test_behavior_bad(self):self.assertEqual(independent_trajectory(O,O,"FULL","BEHAVIOR_BAD")[4]["Q_S0_EXPLORE"],Z)
    def test_missing_source(self):
        with self.assertRaises(AssertionError):verify(load()[:-1],obj(RESULT))
    def test_duplicate_source(self):
        x=load();x[1]=dict(x[0])
        with self.assertRaises(AssertionError):verify(x,obj(RESULT))
    def test_wrong_bootstrap(self):
        x=load();x[0]=dict(x[0]);x[0]["target_S0_EXPLORE"]="999"
        with self.assertRaises(AssertionError):verify(x,obj(RESULT))
    def test_wrong_action(self):
        x=load();x[0]=dict(x[0]);x[0]["chosen_S0"]="EXPLORE"
        with self.assertRaises(AssertionError):verify(x,obj(RESULT))
    def test_wrong_state(self):
        x=load();x[0]=dict(x[0]);x[0]["Q_S1_GOOD"]="4"
        with self.assertRaises(AssertionError):verify(x,obj(RESULT))
    def test_wrong_oracle(self):
        x=load();x[0]=dict(x[0]);x[0]["oracle_Qstar_S0_EXPLORE"]="42"
        with self.assertRaises(AssertionError):verify(x,obj(RESULT))
    def test_result_tamper(self):
        x=obj(RESULT);x["worlds"][0]["epoch_records"][0]["Q_S0_SAFE"]="8"
        with self.assertRaises(AssertionError):verify(load(),x)
    def test_invalid_param(self):
        x=load();x[0]=dict(x[0]);x[0]["gamma"]="1/3"
        with self.assertRaises(AssertionError):verify(x,obj(RESULT))
    def test_digest_tamper(self):
        self.assertNotEqual(hashlib.sha256(SOURCE.read_bytes()+b"fake").hexdigest(),obj(RECEIPT)["sources_sha256"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R297audit"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
