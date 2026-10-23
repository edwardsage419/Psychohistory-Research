#!/usr/bin/env python3
"""R305 exact toy SCT comparative fit, norm/readiness and PERSONAL fallback; NOT Turner fitted math."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="a4dfc1f582c9a58eec6cf45b63a34f577800e0eb"
ZERO,ONE=F(0),F(1)
CONTEXTS={"X":(F(0),F(1),F(4),F(5)),
          "MID":(F(0),F(5,2),F(5,2),F(5)),
          "Y":(F(0),F(4),F(1),F(5))}
PARTITIONS={"P":(0,0,1,1),"Q":(0,1,0,1)}
LEVELS=(ZERO,F(1,2),ONE)
BASELINES=(ZERO,ONE,F(2))
WORLD_GRID=tuple(itertools.product(CONTEXTS,LEVELS,LEVELS,LEVELS,BASELINES))
SOURCE_NAME="R305_ALL_486_ORIGINAL_SELF_CATEGORIZATION_SOURCE_CELLS.csv"
RESULT_NAME="R305_EXACT_SCT_COMPARATIVE_FIT_RESULTS.json"
RECEIPT_NAME="R305_MACHINE_RECEIPT.json"

def pairsets(category):
    if category not in PARTITIONS:raise ValueError("nonfrozen category")
    labels=PARTITIONS[category]
    pairs=list(itertools.combinations(range(4),2))
    within=tuple((i,j) for i,j in pairs if labels[i]==labels[j])
    across=tuple((i,j) for i,j in pairs if labels[i]!=labels[j])
    if len(within)!=2 or len(across)!=4:raise AssertionError("pair sets malformed")
    return within,across

def fit(context,category):
    if context not in CONTEXTS:raise ValueError("nonfrozen context")
    values=CONTEXTS[context]
    within,across=pairsets(category)
    W=sum((abs(values[i]-values[j]) for i,j in within),ZERO)/len(within)
    B=sum((abs(values[i]-values[j]) for i,j in across),ZERO)/len(across)
    if W<=ZERO:raise AssertionError("zero within-distance not permitted")
    return {"within_mean":W,"across_mean":B,"metacontrast":B/W,
            "within_pair_ids":";".join(f"{i}-{j}" for i,j in within),
            "across_pair_ids":";".join(f"{i}-{j}" for i,j in across)}

def worldid(ctx,ready,np,nq,baseline):
    return f"context={ctx}|readiness={ready}|norm_P={np}|norm_Q={nq}|personal_baseline={baseline}"

def outcome(ctx,ready,np,nq,baseline):
    if (ctx,ready,np,nq,baseline) not in WORLD_GRID:raise ValueError("outside frozen grid")
    sP=ready*np*fit(ctx,"P")["metacontrast"]
    sQ=ready*nq*fit(ctx,"Q")["metacontrast"]
    choice="P" if sP>sQ and sP>baseline else ("Q" if sQ>sP and sQ>baseline else "PERSONAL")
    return {"P":sP,"Q":sQ,"PERSONAL":baseline,"chosen_self_category":choice}

def source(ctx,ready,np,nq,baseline,category):
    if category not in PARTITIONS:raise ValueError("outside frozen candidate category")
    vals=outcome(ctx,ready,np,nq,baseline)
    fitdata=fit(ctx,category)
    features=CONTEXTS[ctx]
    sc=vals[category]
    other=vals["Q" if category=="P" else "P"]
    return {"world":worldid(ctx,ready,np,nq,baseline),
       "context":ctx,"feature_values":";".join(str(v) for v in features),
       "readiness":ready,"normative_fit_P":np,"normative_fit_Q":nq,
       "personal_baseline":baseline,"candidate_category":category,
       "category_labels":";".join(str(x) for x in PARTITIONS[category]),
       **fitdata,
       "candidate_normative_fit":np if category=="P" else nq,
       "candidate_social_score":sc,"competing_social_score":other,
       "chosen_self_category":vals["chosen_self_category"],
       "this_category_wins":vals["chosen_self_category"]==category,
       "personal_identity_wins":vals["chosen_self_category"]=="PERSONAL"}

def originals():return tuple(source(*w,c) for w in WORLD_GRID for c in PARTITIONS)

def verify():
    assert len(WORLD_GRID)==243 and len(originals())==486
    assert len({(r["world"],r["candidate_category"]) for r in originals()})==486
    for context,mcP,mcQ in (("X",F(4),F(5,8)),("MID",ONE,ONE),("Y",F(5,8),F(4))):
        assert fit(context,"P")["metacontrast"]==mcP
        assert fit(context,"Q")["metacontrast"]==mcQ
    for w in WORLD_GRID:
        ctx,r,np,nq,b=w
        x=outcome(*w)
        assert x["chosen_self_category"] in ("P","Q","PERSONAL")
        if r==ZERO or (np==ZERO and nq==ZERO):
            assert x["chosen_self_category"]=="PERSONAL"
        for c in PARTITIONS:
            z=source(*w,c)
            assert z["candidate_social_score"]==x[c]
            assert z["within_mean"]*z["metacontrast"]==z["across_mean"]
            assert z["personal_baseline"]==b
    assert outcome("X",ONE,ONE,ONE,ONE)["chosen_self_category"]=="P"
    assert outcome("Y",ONE,ONE,ONE,ONE)["chosen_self_category"]=="Q"
    assert outcome("MID",ONE,ONE,ONE,ONE)["chosen_self_category"]=="PERSONAL"
    assert outcome("X",ONE,ZERO,ONE,ZERO)["chosen_self_category"]=="Q"
    assert outcome("X",ZERO,ONE,ONE,ZERO)["chosen_self_category"]=="PERSONAL"
    return True

def emit():
    verify()
    cols=("world","context","feature_values","readiness","normative_fit_P","normative_fit_Q",
      "personal_baseline","candidate_category","category_labels",
      "within_mean","across_mean","metacontrast","within_pair_ids","across_pair_ids",
      "candidate_normative_fit","candidate_social_score","competing_social_score",
      "chosen_self_category","this_category_wins","personal_identity_wins")
    csvpath=ROOT/SOURCE_NAME
    with csvpath.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n");w.writeheader()
        for z in originals():w.writerow({key:str(z[key]) for key in cols})
    data={"research_id":"R305","original_catalogue_id":"03-004",
      "freeze_commit":FREEZE,
      "scope":"E1_PROJECT_INVENTED_SYNTHETIC_SCT_COMPARATIVE_NORMATIVE_FIT_READINESS_PERSONAL_FALLBACK",
      "artificial_worlds":243,"complete_labeled_original_source_rows":486,
      "context_count":3,"synthetic_objects":4,"competing_categorizations":2,
      "model_scoring_rule_project_invented_not_Turner_1985_author_equation":True,
      "Turner_original_human_self_categorization_data_replayed":False,
      "no_real_human_E2_added":0,"no_real_animal_E2_added":0,"no_historical_E3_added":0,
      "R073":"FROZEN","PESEN_v0_1":"FROZEN","worlds":[]}
    for world in WORLD_GRID:
        ctx,ready,np,nq,baseline=world
        result=outcome(*world)
        data["worlds"].append({"world":worldid(*world),"context":ctx,
          "readiness":str(ready),"normative_fit_P":str(np),"normative_fit_Q":str(nq),
          "personal_baseline":str(baseline),"social_score_P":str(result["P"]),
          "social_score_Q":str(result["Q"]),"chosen_self_category":result["chosen_self_category"],
          "original_option_source_rows":2,
          "category_sources":[{key:str(source(*world,c)[key]) for key in cols if key!="world"} for c in PARTITIONS]})
    data["frozen_reference"]={
        "X_comparative_fit_P":"4","X_comparative_fit_Q":"5/8",
        "MID_both_comparative_fit":"1",
        "Y_comparative_fit_P":"5/8","Y_comparative_fit_Q":"4",
        "X_full_ready_norm_personal1":"P",
        "Y_full_ready_norm_personal1":"Q",
        "MID_full_ready_norm_personal1":"PERSONAL",
        "X_normP0_normQ1_personal0":"Q",
        "readiness0_all_personal":True}
    rp=ROOT/RESULT_NAME
    rp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"research_id":"R305","freeze_commit":FREEZE,"source_rows":486,
      "source_sha256":hashlib.sha256(csvpath.read_bytes()).hexdigest(),
      "results_sha256":hashlib.sha256(rp.read_bytes()).hexdigest(),
      "new_real_E2":0,"new_historical_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_full(self):self.assertTrue(verify())
    def test_worlds(self):self.assertEqual(len(WORLD_GRID),243)
    def test_originals(self):self.assertEqual(len(originals()),486)
    def test_X_P(self):self.assertEqual(fit("X","P")["metacontrast"],F(4))
    def test_X_Q(self):self.assertEqual(fit("X","Q")["metacontrast"],F(5,8))
    def test_Y_Q(self):self.assertEqual(fit("Y","Q")["metacontrast"],F(4))
    def test_MID(self):self.assertEqual(fit("MID","P")["metacontrast"],ONE)
    def test_context_reversal(self):self.assertEqual(outcome("Y",ONE,ONE,ONE,ONE)["chosen_self_category"],"Q")
    def test_mid_fallback(self):self.assertEqual(outcome("MID",ONE,ONE,ONE,ONE)["chosen_self_category"],"PERSONAL")
    def test_normative_reversal(self):self.assertEqual(outcome("X",ONE,ZERO,ONE,ZERO)["chosen_self_category"],"Q")
    def test_unready_negative(self):self.assertEqual(outcome("X",ZERO,ONE,ONE,ZERO)["chosen_self_category"],"PERSONAL")
    def test_bad_context(self):
        with self.assertRaises(ValueError):fit("DIFFERENT","P")
    def test_bad_category(self):
        with self.assertRaises(ValueError):fit("X","R")
    def test_bad_grid(self):
        with self.assertRaises(ValueError):outcome("X",F(1,4),ONE,ONE,ONE)
    def test_bad_source_cat(self):
        with self.assertRaises(ValueError):source("X",ONE,ONE,ONE,ONE,"OTHER")

def generated(w,cat,kind):
    def case(self):
        row=source(*w,cat)
        r=outcome(*w)
        f=fit(w[0],cat)
        if kind=="fit":self.assertEqual(row["metacontrast"],f["metacontrast"])
        elif kind=="choice":self.assertEqual(row["chosen_self_category"],r["chosen_self_category"])
        elif kind=="score":self.assertEqual(row["candidate_social_score"],r[cat])
        else:raise AssertionError(kind)
    return case
for i,w in enumerate(WORLD_GRID):
    for cat in PARTITIONS:
        for kind in ("fit","choice","score"):
            setattr(Tests,f"test_source{i}_{cat}_{kind}",generated(w,cat,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R305"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
