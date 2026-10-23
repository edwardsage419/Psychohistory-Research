#!/usr/bin/env python3
"""Independent original 2112-source mathematical audit, never imports R293 model."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research/R293"
CSV_PATH=ROOT/"R293_ALL_2112_ORIGINAL_TEN_VALUE_STYLE_SOURCES.csv"
RESULT=ROOT/"R293_EXACT_VALUE_CENTERING_RESULTS.json"
RECEIPT=ROOT/"R293_MACHINE_RECEIPT.json"
MODES=("INDEPENDENT","OPPOSED_PAIRS")
Z,O=Q(0),Q(1)
N=10

def parsevec(text):return tuple(Q(z) for z in text.split(";"))
def loadobj(path):return json.loads(path.read_text(encoding="utf-8"))
def load():
    with CSV_PATH.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def algebraic_cov(mode,which,i,j):
    if mode=="INDEPENDENT":
        if which=="raw":return Q(5,4) if i==j else O
        if which=="centered":return Q(9,40) if i==j else -Q(1,40)
    if mode=="OPPOSED_PAIRS":
        if which=="raw":return Q(5,4) if i==j else (Q(3,4) if abs(i-j)==5 else O)
        if which=="centered":return Q(1,4) if i==j else (-Q(1,4) if abs(i-j)==5 else Z)
    raise AssertionError("unexpected mode or transform")

def source_audit(rows, result):
    if len(rows)!=2112:raise AssertionError("wrong source row count")
    if result["original_source_rows"]!=2112 or len(result["worlds"])!=2:raise AssertionError("wrong result scope")
    grouped=defaultdict(list)
    seen=set()
    for row in rows:
        mode=row["mode"]
        if mode not in MODES:raise AssertionError("invalid model")
        bits=row["latent_bits"]
        required=10 if mode=="INDEPENDENT" else 5
        if len(bits)!=required or any(ch not in "01" for ch in bits):raise AssertionError("invalid latent bits")
        s=int(row["shift"])
        if s not in (0,2):raise AssertionError("unfrozen style")
        key=(mode,bits,s)
        if key in seen:raise AssertionError("duplicate source")
        seen.add(key)
        latent=tuple(Q(int(ch)) for ch in bits)
        if mode=="OPPOSED_PAIRS":latent+=tuple(O-v for v in latent)
        raw=tuple(v+s for v in latent)
        mean=sum(raw,Z)/N
        center=tuple(v-mean for v in raw)
        expected_mass=Q(1,2048) if mode=="INDEPENDENT" else Q(1,64)
        if Q(row["source_probability"])!=expected_mass:raise AssertionError("mass tamper")
        if parsevec(row["latent_values"])!=latent:raise AssertionError("latent score tamper")
        if parsevec(row["raw_scores"])!=raw:raise AssertionError("raw score tamper")
        if parsevec(row["centered_scores"])!=center:raise AssertionError("centered score tamper")
        if sum(center,Z)!=Z:raise AssertionError("zero sum violation")
        if raw[0]-raw[5]!=center[0]-center[5]:raise AssertionError("pair difference violation")
        grouped[mode].append((raw,center,expected_mass))
    for idx,mode in enumerate(MODES):
        group=grouped[mode]
        expected_n=2048 if mode=="INDEPENDENT" else 64
        if len(group)!=expected_n:raise AssertionError("incomplete source world")
        if sum((w for raw,ctr,w in group),Z)!=O:raise AssertionError("total mass violation")
        output=result["worlds"][idx]
        if output["mode"]!=mode or output["source_rows"]!=expected_n or output["full_source_mass"]!="1":raise AssertionError("world metadata mismatch")
        for kind,pos in (("raw",0),("centered",1)):
            means=[sum((w*(raw if pos==0 else ctr)[i] for raw,ctr,w in group),Z) for i in range(N)]
            cov=[[sum((w*(raw if pos==0 else ctr)[i]*(raw if pos==0 else ctr)[j] for raw,ctr,w in group),Z)-means[i]*means[j]
                  for j in range(N)] for i in range(N)]
            if output[kind+"_mean"]!=[str(v) for v in means]:raise AssertionError("stored mean mismatch")
            if output[kind+"_covariance"]!=[[str(v) for v in line] for line in cov]:raise AssertionError("stored covariance mismatch")
            for i in range(N):
                for j in range(N):
                    if cov[i][j]!=algebraic_cov(mode,kind,i,j):raise AssertionError("independent analytic covariance mismatch")
        r0=algebraic_cov(mode,"raw",0,5)/algebraic_cov(mode,"raw",0,0)
        c0=algebraic_cov(mode,"centered",0,5)/algebraic_cov(mode,"centered",0,0)
        if output["illustrative_pair_0_5_raw_correlation"]!=str(r0):raise AssertionError("correlation raw mismatch")
        if output["illustrative_pair_0_5_centered_correlation"]!=str(c0):raise AssertionError("correlation centered mismatch")
    return {"research_id":"R293","source_rows":2112,"full_worlds":2,
        "all_raw_centered_covariance_elements_checked":400,
        "independent_style_covariance":"PASS","independent_centering_artifact":"PASS",
        "R013_prior_zip_not_independent_Schwartz_reproduction":True,
        "human_E2_added":0,"historical_E3_added":0}

def audit():
    r=loadobj(RECEIPT)
    j=loadobj(RESULT)
    if j["freeze_commit"]!=r["freeze_commit"]!="44ede9c449b06fa221c51bdbbc2008c5492aed06":raise AssertionError("prescore freeze mismatch")
    if j["original_catalogue_id"]!="01-016" or r["original_source_rows"]!=2112:raise AssertionError("catalogue binding")
    if r["E2_added"]!=r["E3_added"]!=0 or j["empirical_circle_validated"]:raise AssertionError("scientific overclaim")
    if hashlib.sha256(CSV_PATH.read_bytes()).hexdigest()!=r["source_sha256"]:raise AssertionError("CSV hash mismatch")
    if hashlib.sha256(RESULT.read_bytes()).hexdigest()!=r["result_sha256"]:raise AssertionError("result hash mismatch")
    return {**source_audit(load(),j),"original_source_sha256":r["source_sha256"],"result_sha256":r["result_sha256"]}

class Tests(unittest.TestCase):
    def test_full(self):self.assertEqual(audit()["source_rows"],2112)
    def test_model_types(self):self.assertEqual(len(MODES),2)
    def test_cov_independent_raw(self):self.assertEqual(algebraic_cov("INDEPENDENT","raw",0,1),O)
    def test_cov_independent_center(self):self.assertEqual(algebraic_cov("INDEPENDENT","centered",0,1),-Q(1,40))
    def test_cov_opposed_pair(self):self.assertEqual(algebraic_cov("OPPOSED_PAIRS","centered",0,5),-Q(1,4))
    def test_reject_missing(self):
        with self.assertRaises(AssertionError):source_audit(load()[:-1],loadobj(RESULT))
    def test_reject_modified_raw(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["raw_scores"]="1;"+";".join(rows[0]["raw_scores"].split(";")[1:])
        with self.assertRaises(AssertionError):source_audit(rows,loadobj(RESULT))
    def test_reject_centered(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["centered_scores"]="5;"+";".join(rows[0]["centered_scores"].split(";")[1:])
        with self.assertRaises(AssertionError):source_audit(rows,loadobj(RESULT))
    def test_reject_duplicate(self):
        rows=load();rows[1]=dict(rows[0])
        with self.assertRaises(AssertionError):source_audit(rows,loadobj(RESULT))
    def test_reject_result_cov(self):
        result=loadobj(RESULT);result["worlds"][0]["raw_covariance"][0][1]="0"
        with self.assertRaises(AssertionError):source_audit(load(),result)
    def test_reject_added_style(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["shift"]="3"
        with self.assertRaises(AssertionError):source_audit(rows,loadobj(RESULT))
    def test_digest_modification(self):self.assertNotEqual(hashlib.sha256(CSV_PATH.read_bytes()+b"x").hexdigest(),loadobj(RECEIPT)["source_sha256"])
    def test_style_latent_independence(self):self.assertEqual(Q(1,2048),Q(load()[0]["source_probability"]))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R293audit"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
