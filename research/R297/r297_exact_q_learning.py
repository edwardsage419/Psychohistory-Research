#!/usr/bin/env python3
"""R297 exact deterministic Watkins–Dayan Q-learning synthetic E1; no empirical observations."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="fd66badd5a110b36cc97564f7e1a29daba4298ba"
ZERO,ONE=F(0),F(1)
GAMMAS=(ZERO,F(1,2),ONE)
ALPHAS=(F(1,2),ONE)
COVERAGES=("FULL","GOOD_MISSING")
BOOTSTRAPS=("OFF_POLICY_MAX","BEHAVIOR_BAD")
EPOCHS=tuple(range(5))
WORLDS=tuple(itertools.product(GAMMAS,ALPHAS,COVERAGES,BOOTSTRAPS))
CSV_NAME="R297_ALL_120_ORIGINAL_Q_LEARNING_Q_VECTOR_SOURCES.csv"
RESULT_NAME="R297_EXACT_Q_LEARNING_OFF_POLICY_RESULTS.json"
RECEIPT_NAME="R297_MACHINE_RECEIPT.json"

def worldid(gamma,alpha,coverage,backup):
    return f"gamma={gamma}|alpha={alpha}|coverage={coverage}|bootstrap={backup}"

def expected_oracle(gamma):
    if gamma not in GAMMAS:raise ValueError("unsupported discount")
    return {"safe":ONE,"explore":3*gamma,
       "optimal_action":"EXPLORE" if 3*gamma>ONE else "SAFE"}

def get_trajectory(gamma,alpha,coverage,backup):
    if (gamma,alpha,coverage,backup) not in WORLDS:raise ValueError("unfrozen world")
    safe=explore=good=bad=ZERO
    out=[]
    for epoch in EPOCHS:
        if epoch:
            if coverage=="FULL":
                # terminal successor = zero: no gamma continuation.
                good+=alpha*(F(3)-good)
            bad+=alpha*(ZERO-bad)
            safe+=alpha*(ONE-safe)
            explore_target=gamma*(max(good,bad) if backup=="OFF_POLICY_MAX" else bad)
            explore+=alpha*(explore_target-explore)
        else:
            explore_target=ZERO
        oracle=expected_oracle(gamma)
        chosen="EXPLORE" if explore>safe else "SAFE"
        out.append({"world":worldid(gamma,alpha,coverage,backup),
          "gamma":gamma,"alpha":alpha,"coverage":coverage,"backup_rule":backup,
          "epoch":epoch,"Q_S0_SAFE":safe,"Q_S0_EXPLORE":explore,
          "Q_S1_GOOD":good,"Q_S1_BAD":bad,
          "target_S0_EXPLORE":explore_target,
          "chosen_S0":"EXPLORE" if explore>safe else "SAFE",
          "oracle_Qstar_S0_SAFE":oracle["safe"],
          "oracle_Qstar_S0_EXPLORE":oracle["explore"],
          "oracle_best_S0":oracle["optimal_action"],
          "oracle_action_agreement":chosen==oracle["optimal_action"]})
    return tuple(out)

def closed_form(gamma,alpha,coverage,backup,epoch):
    if (gamma,alpha,coverage,backup) not in WORLDS or epoch not in EPOCHS:raise ValueError("unfrozen state")
    remain=(ONE-alpha)**epoch
    safe=ONE-remain
    good=F(3)*(ONE-remain) if coverage=="FULL" else ZERO
    if coverage=="FULL" and backup=="OFF_POLICY_MAX":
        explore=3*gamma*(ONE-remain-alpha*epoch*remain)
        target=gamma*good
    else:
        explore=ZERO
        target=ZERO
    return {"Q_S0_SAFE":safe,"Q_S0_EXPLORE":explore,"Q_S1_GOOD":good,"Q_S1_BAD":ZERO,
      "target_S0_EXPLORE":target}

def all_sources():
    return tuple(r for args in WORLDS for r in get_trajectory(*args))

def validate():
    assert len(WORLDS)==24 and len(all_sources())==120
    assert len(set((r["world"],r["epoch"]) for r in all_sources()))==120
    for args in WORLDS:
        records=get_trajectory(*args)
        for t,r in enumerate(records):
            c=closed_form(*args,t)
            assert all(r[k]==c[k] for k in c)
            assert all(ZERO<=r[k]<=3 for k in ("Q_S0_SAFE","Q_S0_EXPLORE","Q_S1_GOOD","Q_S1_BAD"))
            assert r["Q_S1_BAD"]==ZERO
            assert r["chosen_S0"]==("EXPLORE" if r["Q_S0_EXPLORE"]>r["Q_S0_SAFE"] else "SAFE")
            assert r["oracle_best_S0"]==expected_oracle(args[0])["optimal_action"]
            assert r["oracle_action_agreement"]==(r["chosen_S0"]==r["oracle_best_S0"])
            if t:
                previous=records[t-1]
                assert r["Q_S0_EXPLORE"]-previous["Q_S0_EXPLORE"]==args[1]*(r["target_S0_EXPLORE"]-previous["Q_S0_EXPLORE"])
                assert r["Q_S0_SAFE"]-previous["Q_S0_SAFE"]==args[1]*(ONE-previous["Q_S0_SAFE"])
    final=[get_trajectory(*a)[-1] for a in WORLDS]
    assert sum(x["oracle_action_agreement"] for x in final)==12
    assert all(x["chosen_S0"]=="SAFE" for x in final if x["gamma"]==ZERO)
    assert all(x["chosen_S0"]=="EXPLORE" for x in final if x["gamma"]>ZERO and x["coverage"]=="FULL" and x["backup_rule"]=="OFF_POLICY_MAX")
    assert all(x["chosen_S0"]=="SAFE" for x in final if x["gamma"]>ZERO and (x["coverage"]=="GOOD_MISSING" or x["backup_rule"]=="BEHAVIOR_BAD"))
    ref=get_trajectory(F(1,2),F(1,2),"FULL","OFF_POLICY_MAX")
    assert (ref[1]["Q_S0_SAFE"],ref[1]["Q_S0_EXPLORE"])==(F(1,2),F(3,8))
    assert (ref[2]["Q_S0_SAFE"],ref[2]["Q_S0_EXPLORE"])==(F(3,4),F(3,4))
    assert ref[2]["chosen_S0"]=="SAFE"
    assert (ref[4]["Q_S0_SAFE"],ref[4]["Q_S1_GOOD"],ref[4]["Q_S0_EXPLORE"])==(F(15,16),F(45,16),F(39,32))
    assert ref[4]["chosen_S0"]=="EXPLORE"
    return True

def emit():
    validate()
    p=ROOT/CSV_NAME
    cols=("world","gamma","alpha","coverage","backup_rule","epoch","Q_S0_SAFE",
      "Q_S0_EXPLORE","Q_S1_GOOD","Q_S1_BAD","target_S0_EXPLORE","chosen_S0",
      "oracle_Qstar_S0_SAFE","oracle_Qstar_S0_EXPLORE","oracle_best_S0","oracle_action_agreement")
    with p.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        writer.writeheader()
        for row in all_sources():writer.writerow({k:str(row[k]) for k in cols})
    res={"research_id":"R297","original_catalogue_id":"02-003","freeze_commit":FREEZE,
      "scope":"E1_FINITE_DETERMINISTIC_Q_LEARNING_OFF_POLICY_AND_ACTION_COVERAGE_NOT_CONVERGENCE_PROOF",
      "world_count":24,"full_original_Q_vector_source_rows":120,"epochs_each":5,
      "real_subjects":0,"real_animal_E2":0,"human_E2":0,"historical_E3":0,
      "R073":"FROZEN","PESEN_v0_1":"FROZEN","worlds":[]}
    for args in WORLDS:
        gamma,alpha,coverage,backup=args
        seq=get_trajectory(*args)
        res["worlds"].append({"world":worldid(*args),"gamma":str(gamma),"alpha":str(alpha),
          "coverage":coverage,"backup_rule":backup,"full_source_rows":5,
          "epoch_records":[{k:str(v) for k,v in r.items() if k not in ("world","gamma","alpha","coverage","backup_rule")}
               for r in seq],
          "epoch4_action":seq[-1]["chosen_S0"],"epoch4_oracle_agreement":seq[-1]["oracle_action_agreement"]})
    final=[get_trajectory(*args)[-1] for args in WORLDS]
    res["epoch4_oracle_correct_worlds"]=sum(x["oracle_action_agreement"] for x in final)
    res["epoch4_oracle_disagreement_worlds"]=sum(not x["oracle_action_agreement"] for x in final)
    res["reference_gamma_half_alpha_half_FULL_MAX_epoch4"]={
       "Q_S0_SAFE":"15/16","Q_S0_EXPLORE":"39/32","Q_S1_GOOD":"45/16",
       "epoch1_action":"SAFE","epoch2_tie_choose":"SAFE","epoch4_action":"EXPLORE"}
    resultp=ROOT/RESULT_NAME
    resultp.write_text(json.dumps(res,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt={"research_id":"R297","freeze_commit":FREEZE,"original_source_rows":120,
      "sources_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
      "results_sha256":hashlib.sha256(resultp.read_bytes()).hexdigest(),
      "real_human_E2":0,"real_animal_E2":0,"historical_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_validate(self):self.assertTrue(validate())
    def test_source_count(self):self.assertEqual(len(all_sources()),120)
    def test_worlds(self):self.assertEqual(len(WORLDS),24)
    def test_reference(self):self.assertEqual(get_trajectory(F(1,2),F(1,2),"FULL","OFF_POLICY_MAX")[4]["Q_S0_EXPLORE"],F(39,32))
    def test_missing_good(self):self.assertEqual(get_trajectory(ONE,ONE,"GOOD_MISSING","OFF_POLICY_MAX")[-1]["Q_S1_GOOD"],ZERO)
    def test_offpolicy_bootstrap(self):self.assertEqual(get_trajectory(ONE,ONE,"FULL","OFF_POLICY_MAX")[-1]["Q_S0_EXPLORE"],F(3))
    def test_behavior_bad_bootstrap(self):self.assertEqual(get_trajectory(ONE,ONE,"FULL","BEHAVIOR_BAD")[-1]["Q_S0_EXPLORE"],ZERO)
    def test_gamma_zero(self):self.assertEqual(get_trajectory(ZERO,ONE,"FULL","OFF_POLICY_MAX")[-1]["chosen_S0"],"SAFE")
    def test_bad_gamma(self):
        with self.assertRaises(ValueError):get_trajectory(F(1,3),ONE,"FULL","OFF_POLICY_MAX")
    def test_bad_coverage(self):
        with self.assertRaises(ValueError):closed_form(ONE,ONE,"UNFROZEN","OFF_POLICY_MAX",4)
    def test_bad_epoch(self):
        with self.assertRaises(ValueError):closed_form(ONE,ONE,"FULL","OFF_POLICY_MAX",5)

def build_case(args,t,kind):
    def case(self):
        r=get_trajectory(*args)[t];c=closed_form(*args,t)
        if kind=="closed":self.assertEqual({k:r[k] for k in c},c)
        elif kind=="action":self.assertEqual(r["chosen_S0"],"EXPLORE" if r["Q_S0_EXPLORE"]>r["Q_S0_SAFE"] else "SAFE")
        elif kind=="terminal":self.assertEqual(r["Q_S1_BAD"],ZERO)
        elif kind=="oracle":self.assertEqual(r["oracle_action_agreement"],r["chosen_S0"]==r["oracle_best_S0"])
        elif kind=="safe":self.assertEqual(r["Q_S0_SAFE"],ONE-(ONE-args[1])**t)
        else:raise AssertionError(kind)
    return case
for i,args in enumerate(WORLDS):
    for t in EPOCHS:
        for kind in ("closed","action","terminal","oracle","safe"):
            setattr(Tests,f"test_world{i}_epoch{t}_{kind}",build_case(args,t,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R297"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
