#!/usr/bin/env python3
"""R293 exact ten-slot value response style and centering counterexamples, synthetic E1 only."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from functools import lru_cache
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="44ede9c449b06fa221c51bdbbc2008c5492aed06"
LABELS=("Self-Direction","Stimulation","Hedonism","Achievement","Power",
        "Security","Conformity","Tradition","Benevolence","Universalism")
MODES=("INDEPENDENT","OPPOSED_PAIRS")
SHIFTS=(0,2)
K=10
ZERO,ONE=F(0),F(1)
CSV_NAME="R293_ALL_2112_ORIGINAL_TEN_VALUE_STYLE_SOURCES.csv"
RESULT_NAME="R293_EXACT_VALUE_CENTERING_RESULTS.json"
RECEIPT_NAME="R293_MACHINE_RECEIPT.json"

def sources(mode):
    if mode=="INDEPENDENT":return tuple(itertools.product((0,1),repeat=10))
    if mode=="OPPOSED_PAIRS":return tuple(itertools.product((0,1),repeat=5))
    raise ValueError("unfrozen value DGP")

def expand(mode,bits):
    if tuple(bits) not in sources(mode):raise ValueError("invalid original bit profile")
    if mode=="INDEPENDENT":return tuple(bits)
    return tuple(bits)+tuple(1-v for v in bits)

def record(mode,bits,shift):
    if shift not in SHIFTS:raise ValueError("unfrozen response style")
    vals=expand(mode,bits)
    raw=tuple(v+shift for v in vals)
    mean=sum(raw,F(0))/K
    ctr=tuple(F(v)-mean for v in raw)
    prob=F(1,2*len(sources(mode)))
    return {"mode":mode,"latent_bits":"".join(map(str,bits)),
      "shift":shift,"source_probability":prob,
      "latent_values":vals,"raw_scores":raw,"centered_scores":ctr}

@lru_cache(maxsize=2)
def all_rows(mode):
    return tuple(record(mode,b,shift) for b in sources(mode) for shift in SHIFTS)

@lru_cache(maxsize=4)
def moments(mode,transform):
    if transform not in ("raw","centered"):raise ValueError("wrong score transform")
    rows=all_rows(mode)
    vectors=[r["raw_scores" if transform=="raw" else "centered_scores"] for r in rows]
    means=tuple(sum((r["source_probability"]*v[i] for r,v in zip(rows,vectors)),ZERO) for i in range(K))
    matrix=tuple(tuple(sum((r["source_probability"]*F(v[i])*F(v[j]) for r,v in zip(rows,vectors)),ZERO)-means[i]*means[j] for j in range(K)) for i in range(K))
    return means,matrix

def expected_cov(mode,transform,i,j):
    if i not in range(K) or j not in range(K):raise ValueError("bad slot")
    if mode=="INDEPENDENT":
        if transform=="raw":return F(5,4) if i==j else ONE
        if transform=="centered":return F(9,40) if i==j else -F(1,40)
    elif mode=="OPPOSED_PAIRS":
        if transform=="raw":return F(5,4) if i==j else (F(3,4) if abs(i-j)==5 else ONE)
        if transform=="centered":return F(1,4) if i==j else (-F(1,4) if abs(i-j)==5 else ZERO)
    raise ValueError("unfrozen DGP or transform")

def verify():
    assert len(LABELS)==K and len(set(LABELS))==K
    assert sum(len(all_rows(mode)) for mode in MODES)==2112
    for mode in MODES:
        rows=all_rows(mode)
        assert len(rows)==(2048 if mode=="INDEPENDENT" else 64)
        assert sum((r["source_probability"] for r in rows),ZERO)==ONE
        assert len(set((r["latent_bits"],r["shift"]) for r in rows))==len(rows)
        for r in rows:
            assert sum(r["centered_scores"],ZERO)==ZERO
            assert all(F(x)-F(y)==F(a)-F(b) for x,y,a,b in zip(r["raw_scores"],r["raw_scores"][1:]+r["raw_scores"][:1],r["latent_values"],r["latent_values"][1:]+r["latent_values"][:1]))
            assert all(F(v)+r["shift"]==x for v,x in zip(r["latent_values"],r["raw_scores"]))
            assert all(F(r["raw_scores"][i])-F(r["raw_scores"][j])==r["centered_scores"][i]-r["centered_scores"][j] for i,j in ((0,5),(2,7)))
        for transform in ("raw","centered"):
            means,mat=moments(mode,transform)
            assert all(mat[i][j]==expected_cov(mode,transform,i,j) for i in range(K) for j in range(K))
            assert all(means[i]==(F(3,2) if transform=="raw" else ZERO) for i in range(K))
    assert moments("INDEPENDENT","raw")[1][0][1]/moments("INDEPENDENT","raw")[1][0][0]==F(4,5)
    assert moments("INDEPENDENT","centered")[1][0][1]/moments("INDEPENDENT","centered")[1][0][0]==-F(1,9)
    assert moments("OPPOSED_PAIRS","raw")[1][0][5]/moments("OPPOSED_PAIRS","raw")[1][0][0]==F(3,5)
    assert moments("OPPOSED_PAIRS","centered")[1][0][5]/moments("OPPOSED_PAIRS","centered")[1][0][0]==-ONE
    return True

def serial(v):return ";".join(str(x) for x in v)

def emit():
    verify()
    path=ROOT/CSV_NAME
    cols=("mode","latent_bits","shift","source_probability","latent_values","raw_scores","centered_scores")
    with path.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        writer.writeheader()
        for mode in MODES:
            for r in all_rows(mode):
                writer.writerow({key:(serial(r[key]) if key in ("latent_values","raw_scores","centered_scores") else str(r[key])) for key in cols})
    worlds=[]
    for mode in MODES:
        entry={"mode":mode,"source_rows":len(all_rows(mode)),"full_source_mass":"1"}
        for transform in ("raw","centered"):
            means,mat=moments(mode,transform)
            entry[transform+"_mean"]=list(map(str,means))
            entry[transform+"_covariance"]= [list(map(str,row)) for row in mat]
        entry["illustrative_pair_0_5_raw_correlation"]=str(moments(mode,"raw")[1][0][5]/moments(mode,"raw")[1][0][0])
        entry["illustrative_pair_0_5_centered_correlation"]=str(moments(mode,"centered")[1][0][5]/moments(mode,"centered")[1][0][0])
        worlds.append(entry)
    out={"research_id":"R293","original_catalogue_id":"01-016","freeze_commit":FREEZE,
      "scope":"SYNTHETIC_E1_10_VALUE_SLOT_RESPONSE_STYLE_AND_CENTERING_NOT_ESS_PVQ21_HUMAN_FIT",
      "theoretical_label_order":LABELS,"original_source_rows":2112,"worlds":worlds,
      "empirical_circle_validated":False,"new_human_E2":0,"new_historical_E3":0,"R073":"FROZEN","PESEN_v0_1":"FROZEN"}
    result=ROOT/RESULT_NAME
    result.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"research_id":"R293","freeze_commit":FREEZE,"original_source_rows":2112,
       "source_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
       "result_sha256":hashlib.sha256(result.read_bytes()).hexdigest(),
       "E2_added":0,"E3_added":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_claims(self):self.assertTrue(verify())
    def test_counts(self):self.assertEqual(sum(len(all_rows(m)) for m in MODES),2112)
    def test_independent_shift_raw_corr(self):self.assertEqual(F(4,5),moments("INDEPENDENT","raw")[1][0][1]/moments("INDEPENDENT","raw")[1][0][0])
    def test_artificial_negative_centered_corr(self):self.assertEqual(-F(1,9),moments("INDEPENDENT","centered")[1][0][1]/moments("INDEPENDENT","centered")[1][0][0])
    def test_opposing_pair_center(self):self.assertEqual(-ONE,moments("OPPOSED_PAIRS","centered")[1][0][5]/moments("OPPOSED_PAIRS","centered")[1][0][0])
    def test_reject_shift(self):
        with self.assertRaises(ValueError):record("INDEPENDENT",(0,)*10,1)
    def test_reject_mode(self):
        with self.assertRaises(ValueError):sources("MISSING")
    def test_reject_vector(self):
        with self.assertRaises(ValueError):expand("OPPOSED_PAIRS",(0,)*10)
    def test_reject_transform(self):
        with self.assertRaises(ValueError):moments("INDEPENDENT","normalized")
def _new(mode,transform,i,j):
    def fn(self):self.assertEqual(moments(mode,transform)[1][i][j],expected_cov(mode,transform,i,j))
    return fn
for mode in MODES:
    for trans in ("raw","centered"):
        for i,j in itertools.product((0,1,4,5,6,9),repeat=2):
            setattr(Tests,"test_"+mode.lower()+"_"+trans+"_"+str(i)+"_"+str(j),_new(mode,trans,i,j))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true")
    m.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R293"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
