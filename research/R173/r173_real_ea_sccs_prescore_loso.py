"""R173 cross-societal prescore-frozen observational LOSO test.

Uses authentic D-PLACE commit already SHA-verified by source loader. Two
independent implementations of exact leave-one-society-out predictions.
No model fitting, model selection, temporal forecasting or causal claims.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
from pathlib import Path
import csv
import io
import json
import math
import random
import sys
import unittest
import zipfile

from r173_original_dplace_source_audit import COMMIT, HERE, rows
from r173_real_ea_coverage_mapping_gate import VALID, VARIABLES, four_digit_year, mappings

OUT = HERE / "R173_REAL_EA_SCCS_LOSO_EXACT_RESULTS.json"
PRED = HERE / "R173_REAL_EA_SCCS_LOSO_HELDOUT_PREDICTIONS.csv"
ARCHIVE = HERE / "R173_Real_EA_SCCS_Observational_LOSO_Archive.zip"
PROTO = "R173_REAL_EA_SCCS_EA005_EA006_LOSO_ASSOCIATION_PRESCORE_FREEZE_2026-10-21.md"
K = tuple("1234567")
SHRINK = 10.0
BS = 2048
PERMS = 199
SEED = 173


def load_records():
    _, data = rows("datasets/EA/data.csv")
    _, societies = rows("datasets/EA/societies.csv")
    _, fwd = rows("datasets/EA/societies_mapping.csv")
    _, rev = rows("datasets/SCCS/societies_mapping.csv")
    bysoc = {r["id"]:r for r in societies}
    if len(bysoc) != len(societies):
        raise ValueError("duplicate EA societies")
    mapping = mappings(fwd,rev,set(bysoc))
    if mapping["accepted_exact_reciprocal_bijective_pairs"] != 186:
        raise ValueError("failed original reciprocal SCCS acceptance")
    if any(mapping[k] for k in ("EA_only_pairs","SCCS_only_pairs",
                                "ambiguous_agreed_EA_ids","ambiguous_agreed_SCCS_ids",
                                "missing_EA_society_ids")):
        raise ValueError("source SCCS map not losslessly reconciled")
    sid_sccs = {d["EA_id"] for d in mapping["accepted_pairs"]}
    selected = {}
    multiple = set()
    for r in data:
        key=(r.get("soc_id"),r.get("var_id"))
        if key[0] in bysoc and key[1] in VALID:
            if key in selected:
                multiple.add(key)
            else:
                selected[key]=r
    records=[]
    for sid in sorted(bysoc):
        ks=[(sid,var) for var in VARIABLES]
        if any(k in multiple or k not in selected for k in ks):
            continue
        a,b = (selected[k] for k in ks)
        x,y = a.get("code","").strip(),b.get("code","").strip()
        if x not in VALID["EA005"] or y not in VALID["EA006"]:
            continue
        year_fields=(a.get("year"),b.get("year"),bysoc[sid].get("main_focal_year"))
        records.append({"id":sid,"x":x,"y":y,"sccs":sid in sid_sccs,
                        "year_complete":all(four_digit_year(v) is not None for v in year_fields)})
    if len(records)!=1271 or sum(r["sccs"] for r in records)!=186:
        raise ValueError("eligible primary EA/SCCS population drifted")
    return records


def exact_naive(rows_):
    """Independent method A: reconstruct each fold from actual training rows."""
    answer=[]
    for i,row in enumerate(rows_):
        train=[item for j,item in enumerate(rows_) if i!=j]
        n=len(train)
        if not n: raise ValueError("cannot score singleton sample")
        nk=Counter(r["y"] for r in train)
        group=[r for r in train if r["x"]==row["x"]]
        nx=len(group)
        nxk=Counter(r["y"] for r in group)
        p0={k:(nk[k]+1)/(n+7) for k in K}
        p1={k:(nxk[k]+SHRINK*p0[k])/(nx+SHRINK) for k in K}
        answer.append((p0,p1))
    return answer


def exact_subtractive(rows_):
    """Independent method B: subtract the held-out row from global tallies."""
    n=len(rows_)
    if n<2:raise ValueError("cannot score singleton sample")
    ny=Counter(r["y"] for r in rows_)
    nx=Counter(r["x"] for r in rows_)
    nxy=Counter((r["x"],r["y"]) for r in rows_)
    answer=[]
    for row in rows_:
        ntr=n-1
        xx,yy=row["x"],row["y"]
        size=nx[xx]-1
        p0={k:(ny[k]-int(yy==k)+1)/(ntr+7) for k in K}
        p1={k:(nxy[(xx,k)]-int(yy==k)+SHRINK*p0[k])/(size+SHRINK) for k in K}
        answer.append((p0,p1))
    return answer


def score(rows_,name):
    if len(rows_)<2:raise ValueError("need at least two scored societies")
    a=exact_naive(rows_)
    b=exact_subtractive(rows_)
    individual=[]
    predictions=[]
    for r,(p0,p1),(q0,q1) in zip(rows_,a,b):
        if any(abs(p0[k]-q0[k])>1e-12 or abs(p1[k]-q1[k])>1e-12 for k in K):
            raise AssertionError("two LOSO implementations disagree")
        if any(v<=0 for v in (*p0.values(),*p1.values())):
            raise AssertionError("invalid probability")
        if abs(sum(p0.values())-1)>1e-12 or abs(sum(p1.values())-1)>1e-12:
            raise AssertionError("probabilities not normalized")
        loss0,loss1=-math.log(p0[r["y"]]),-math.log(p1[r["y"]])
        individual.append((loss0,loss1))
        predictions.append({
            "sample":name,"society_id":r["id"],"agriculture_code_EA005":r["x"],
            "observed_marriage_code_EA006":r["y"],
            "source_years_complete":int(r["year_complete"]),
            "sccs_bidirectional_matched":int(r["sccs"]),
            "loss_M0":format(loss0,".16g"),"loss_M1":format(loss1,".16g"),
            **{f"M0_p{k}":format(p0[k],".16g") for k in K},
            **{f"M1_p{k}":format(p1[k],".16g") for k in K},
        })
    return individual,predictions


def interval(diffs,seed=SEED,count=BS):
    rng=random.Random(seed)
    n=len(diffs)
    samples=sorted(sum(diffs[rng.randrange(n)] for _ in range(n))/n
                   for _ in range(count))
    return [samples[max(0,math.ceil(0.025*count)-1)],
            samples[max(0,math.ceil(0.975*count)-1)]]


def empirical_perm(rows_,true_delta):
    rng=random.Random(SEED)
    original=[r["y"] for r in rows_]
    observed=[]
    for _ in range(PERMS):
        labels=original.copy()
        rng.shuffle(labels)
        shuffled=[{**r,"y":lab} for r,lab in zip(rows_,labels)]
        losses,_=score(shuffled,"permutation_internal")
        observed.append(sum(z0-z1 for z0,z1 in losses)/len(losses))
    ordered=sorted(observed)
    return {
      "replicates":PERMS,"seed":SEED,
      "permuted_delta_min":ordered[0],
      "permuted_delta_median":ordered[len(ordered)//2],
      "permuted_delta_max":ordered[-1],
      "fraction_permuted_delta_below_observed":sum(z<true_delta for z in observed)/PERMS,
      "upper_tail_empirical_benchmark":(1+sum(z>=true_delta for z in observed))/(1+PERMS),
      "valid_inference_under_shared_ancestry_or_spatial_dependence":False,
    }


def run():
    records=load_records()
    subsets={
       "SCCS_186": [r for r in records if r["sccs"]],
       "EA_1271": records,
       "SCCS_COMPLETE_SOURCE_YEARS": [r for r in records if r["sccs"] and r["year_complete"]],
       "EA_COMPLETE_SOURCE_YEARS": [r for r in records if r["year_complete"]],
    }
    results={}
    preds=[]
    for name,rs in subsets.items():
        losses,pp=score(rs,name)
        preds.extend(pp)
        deltas=[x-y for x,y in losses]
        m0=sum(x for x,y in losses)/len(losses)
        m1=sum(y for x,y in losses)/len(losses)
        delta=m0-m1
        lo,hi=interval(deltas)
        res={"sample_size":len(rs),"mean_log_loss_M0":m0,"mean_log_loss_M1":m1,
             "delta_M0_minus_M1":delta,
             "naive_society_paired_bootstrap_95percent": [lo,hi],
             "bootstrap_draws":BS,"bootstrap_seed":SEED,
             "two_independent_fold_methods_agreed":True}
        if name=="SCCS_186":
            res["naive_label_shuffle"]=empirical_perm(rs,delta)
        results[name]=res
        print("R173_REAL_LOSO",name,json.dumps(res,sort_keys=True))
    headings=["sample","society_id","agriculture_code_EA005","observed_marriage_code_EA006",
              "source_years_complete","sccs_bidirectional_matched","loss_M0","loss_M1"] + \
             [f"M0_p{k}" for k in K]+[f"M1_p{k}" for k in K]
    with PRED.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=headings,lineterminator="\n")
        w.writeheader()
        w.writerows(preds)
    artifact={
      "research_id":"R173","stage":"BOUNDED_REAL_OBSERVATIONAL_CROSS_SOCIAL_LOSO",
      "prescoring_protocol":"protocols/"+PROTO,
      "pinned_source_commit":COMMIT,"EA005":"ordinal_0_9_used_as_nominal_strata",
      "EA006":"nominal_1_7","models":{"M0_alpha_each":1,"M1_shrinkage":10},
      "metrics":results,"all_samples_overlap":True,"new_E2":0,"new_E3":0,
      "independent_external_history_prediction":False,
      "causal_or_phylogenetic_adjustment_established":False,
      "historical_focal_years_synchronized":False,
      "heldout_predictions_csv_sha256":sha256(PRED.read_bytes()).hexdigest(),
      "prediction_rows":len(preds)
    }
    OUT.write_text(json.dumps(artifact,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R173_RESULT_JSON_SHA256",sha256(OUT.read_bytes()).hexdigest())
    print("R173_PREDICTION_CSV_SHA256",artifact["heldout_predictions_csv_sha256"])
    return artifact


def archive():
    files=[
      "r173_original_dplace_source_audit.py",
      "r173_real_ea_coverage_mapping_gate.py",
      Path(__file__).name,
      "R173_REAL_EA005_EA006_COVERAGE_AND_RECIPROCAL_MAPPING.json",
      OUT.name,PRED.name,
      "../../protocols/"+PROTO,
    ]
    with zipfile.ZipFile(ARCHIVE,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in files:
            file=(HERE/name).resolve()
            arcname="protocols/"+PROTO if name.startswith("../../") else name
            zi=zipfile.ZipInfo(arcname,date_time=(2026,10,21,0,0,0))
            zi.compress_type=zipfile.ZIP_DEFLATED
            zi.external_attr=0o644<<16
            z.writestr(zi,file.read_bytes())
    print("R173_ARCHIVE_SHA256",sha256(ARCHIVE.read_bytes()).hexdigest())


class TestFrozenMathematics(unittest.TestCase):
    def test_fold_count(self):
        self.assertEqual(len(exact_naive([{"x":"1","y":"1"},{"x":"2","y":"2"}])),2)
    def test_singleton_fails(self):
        with self.assertRaises(ValueError):
            exact_naive([{"x":"1","y":"1"}])
    def test_baseline_train_only(self):
        x=[{"x":"0","y":"1"},{"x":"0","y":"2"},{"x":"2","y":"2"}]
        self.assertAlmostEqual(exact_naive(x)[0][0]["1"],1/9)
    def test_conditional_shrink_manual(self):
        x=[{"x":"0","y":"1"},{"x":"0","y":"2"},{"x":"2","y":"2"}]
        a=exact_naive(x)[0][1]["2"]
        self.assertAlmostEqual(a,(1+10*(3/9))/11)
    def test_two_methods_full_distribution(self):
        x=[{"x":str(i%3),"y":str(i%7+1)} for i in range(24)]
        self.assertEqual(exact_naive(x),exact_subtractive(x))
    def test_probability_positive(self):
        x=[{"x":str(i%3),"y":str(i%7+1),"id":str(i),"sccs":False,"year_complete":True}
           for i in range(24)]
        res,_=score(x,"artificial")
        self.assertTrue(all(math.isfinite(v) for pair in res for v in pair))
    def test_prediction_reorder(self):
        x=[{"x":str(i%3),"y":str(i%7+1),"id":str(i),"sccs":False,"year_complete":True}
           for i in range(16)]
        a,_=score(x,"artificial")
        b,_=score(list(reversed(x)),"artificial")
        self.assertAlmostEqual(sum(p-q for p,q in a),sum(p-q for p,q in b))
    def test_bootstrap_determinism(self):
        self.assertEqual(interval([0.2,-0.1,0.4],count=50),
                         interval([0.2,-0.1,0.4],count=50))
    def test_zero_difference_ci(self):
        self.assertEqual(interval([0.0]*7,count=25),[0.0,0.0])
    def test_rejected_nonpositive_n(self):
        with self.assertRaises(ValueError):
            exact_subtractive([])
    def test_model_reverts_when_all_x_unique(self):
        x=[{"x":"1","y":"1"},{"x":"2","y":"2"}]
        a=exact_naive(x)
        for p0,p1 in a:
            self.assertEqual(p0,p1)
    def test_permutation_preserves_labels(self):
        x=[{"x":"0","y":"1"},{"x":"1","y":"2"},{"x":"2","y":"2"}]
        labels=[r["y"] for r in x]
        rng=random.Random(SEED)
        rng.shuffle(labels)
        self.assertEqual(Counter(labels),Counter(r["y"] for r in x))


if __name__=="__main__":
    if sys.argv[1:]==["--score-and-archive"]:run();archive()
    elif sys.argv[1:]==["--self-test"]:unittest.main(argv=[sys.argv[0]],verbosity=2)
    else:raise SystemExit("use --score-and-archive or --self-test")
