#!/usr/bin/env python3
"""R312 independent midpoint-and-shrink Deffuant source reconstruction, no model import."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as Q
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/"research/R312"
CSV=ROOT/"R312_ALL_1152_ORIGINAL_DEFFUANT_PERSON_SOURCE_ROWS.csv"
RESULT=ROOT/"R312_EXACT_DEFFUANT_PAIR_EVENT_RESULTS.json"
RECEIPT=ROOT/"R312_MACHINE_RECEIPT.json"
ZERO,ONE=Q(0),Q(1)
PROFILES={"A":(ZERO,ZERO,ZERO,ZERO),"B":(ZERO,ZERO,ZERO,Q(1,2)),
 "C":(ZERO,ZERO,Q(1,2),ONE),"D":(ZERO,Q(1,2),Q(1,2),ONE),
 "E":(ZERO,ZERO,ONE,ONE),"F":(ZERO,Q(1,2),ONE,ONE),
 "G":(Q(1,2),Q(1,2),Q(1,2),ONE),"H":(ONE,ONE,ONE,ONE)}
EPS=(ZERO,Q(1,2),ONE);MU=(Q(1,4),Q(1,2))
PAIRS=tuple(itertools.combinations(range(4),2))
WORLDS=tuple((p,e,mu) for p in PROFILES for e in EPS for mu in MU)
FIELDS=("world","profile","initial_opinions","confidence_radius","compromise_mu",
 "pair_i","pair_j","uniform_pair_probability","person_index","person_pre_opinion",
 "person_after_selected_pair","expected_person_next_opinion","selected_pair_confidence_eligible",
 "selected_pair_gap_before","selected_pair_gap_after","updated_opinions",
 "initial_sum","updated_sum","sum_conserved","pair_opinion_gap_contraction")
def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def load():
    with CSV.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def wid(p,e,mu):return f"profile={p}|eps={e}|mu={mu}"
def independently_update(x,e,mu,pair):
    i,j=pair
    d=abs(x[i]-x[j]);eligible=d<=e
    if eligible:
        # Independent midpoint/contraction form instead of original additive step
        midpoint=(x[i]+x[j])/2
        half_difference=(x[i]-x[j])/2
        factor=ONE-2*mu
        updated=list(x)
        updated[i]=midpoint+factor*half_difference
        updated[j]=midpoint-factor*half_difference
        y=tuple(updated)
    else:y=tuple(x)
    return y,eligible,d,abs(y[i]-y[j])
def outcome(p,e,mu):
    x=PROFILES[p]
    possible=[independently_update(x,e,mu,pair) for pair in PAIRS]
    expected=tuple(sum((event[0][i] for event in possible),ZERO)/6 for i in range(4))
    return x,possible,expected
def row(p,e,mu,pair,i):
    x,all_events,expected=outcome(p,e,mu)
    k=PAIRS.index(pair)
    y,eligible,before,after=all_events[k]
    source={"world":wid(p,e,mu),"profile":p,
      "initial_opinions":";".join(map(str,x)),
      "confidence_radius":e,"compromise_mu":mu,
      "pair_i":pair[0],"pair_j":pair[1],"uniform_pair_probability":Q(1,6),
      "person_index":i,"person_pre_opinion":x[i],
      "person_after_selected_pair":y[i],
      "expected_person_next_opinion":expected[i],
      "selected_pair_confidence_eligible":eligible,
      "selected_pair_gap_before":before,"selected_pair_gap_after":after,
      "updated_opinions":";".join(map(str,y)),
      "initial_sum":sum(x,ZERO),"updated_sum":sum(y,ZERO),
      "sum_conserved":sum(y,ZERO)==sum(x,ZERO),
      "pair_opinion_gap_contraction":before-after}
    return {key:str(source[key]) for key in FIELDS}
def two_steps(x,first,second):
    return independently_update(independently_update(x,ONE,Q(1,2),first)[0],ONE,Q(1,2),second)[0]
def verify(rows,result):
    if len(rows)!=1152 or len(result["worlds"])!=48 or result["original_full_person_source_rows"]!=1152:
        raise AssertionError("incomplete source universe")
    known={(p,e,mu,pair,i) for p,e,mu in WORLDS for pair in PAIRS for i in range(4)}
    seen=set()
    for source in rows:
        try:
            p=source["profile"];e=Q(source["confidence_radius"]);mu=Q(source["compromise_mu"])
            pair=(int(source["pair_i"]),int(source["pair_j"]));i=int(source["person_index"])
        except (KeyError,ValueError,ZeroDivisionError) as err:raise AssertionError("invalid source identity") from err
        k=(p,e,mu,pair,i)
        if k not in known or k in seen:raise AssertionError("source duplicated/outside frozen grid")
        if source!=row(*k):raise AssertionError("original source differs from independent midpoint calculation")
        seen.add(k)
    if seen!=known:raise AssertionError("source missing")
    for index,(p,e,mu) in enumerate(WORLDS):
        x,events,expected=outcome(p,e,mu);z=result["worlds"][index]
        if z["world"]!=wid(p,e,mu) or z["profile"]!=p or z["epsilon"]!=str(e) or z["mu"]!=str(mu):
            raise AssertionError("world identity mismatch")
        if z["initial"]!=list(map(str,x)) or z["one_step_uniform_pair_expected"]!=list(map(str,expected)):
            raise AssertionError("world full original opinions mismatch")
        if z["mean_initial"]!=str(sum(x,ZERO)/4) or z["mean_expected"]!=str(sum(expected,ZERO)/4):
            raise AssertionError("expectation mean wrong")
        if len(z["six_original_pair_events"])!=6:raise AssertionError("six pairs required")
        for pair,(y,eligible,before,after),event in zip(PAIRS,events,z["six_original_pair_events"]):
            if event["pair"]!=list(pair) or event["probability"]!="1/6":
                raise AssertionError("pair selection probability")
            if event["after"]!=list(map(str,y)) or event["eligible"]!=eligible or event["gap_before"]!=str(before) or event["gap_after"]!=str(after):
                raise AssertionError("pair scenario mismatch")
            if event["four_original_person_sources"]!=[{k:v for k,v in row(p,e,mu,pair,i).items() if k!="world"} for i in range(4)]:
                raise AssertionError("original person source mismatch")
            if sum(x,ZERO)!=sum(y,ZERO):raise AssertionError("sum conservation violated")
            if eligible and after!=abs(ONE-2*mu)*before:raise AssertionError("gap shrink")
            if not eligible and y!=x:raise AssertionError("outside confidence changed")
    if result["reference"]!={"F_pair01_eps1_mu_half":["1/4","1/4","1","1"],
       "F_pair12_eps1_mu_half":["0","3/4","3/4","1"],
       "C_pair12_epshalf_mu_half":["0","1/4","1/4","1"],
       "C_pair03_epshalf_mu_half_unchanged":True,
       "F_two_step_01_then_12":["1/4","5/8","5/8","1"],
       "F_two_step_12_then_01":["3/8","3/8","3/4","1"],
       "order_depends_at_two_steps":True}:raise AssertionError("predefined examples modified")
    if two_steps(PROFILES["F"],(0,1),(1,2))==two_steps(PROFILES["F"],(1,2),(0,1)):
        raise AssertionError("finite order effect not reproduced")
    return {"finite_artificial_worlds":48,"all_original_pair_events":288,
      "original_person_sources":1152,"midpoint_reconstruction":"PASS",
      "mean_conserved_per_event":True,"order_effect_verified":True,
      "human_E2":0,"historical_E3":0}
def audit():
    r,j=obj(RECEIPT),obj(RESULT)
    if r["freeze_commit"]!="2c8c9bfd15a27574f0fffb02517eb5893aedfee9" or j["freeze_commit"]!=r["freeze_commit"]:
        raise AssertionError("unfrozen experiment")
    if j["research_id"]!="R312" or j["original_catalogue_id"]!="04-013":
        raise AssertionError("wrong original candidate")
    if j["real_human_E2"]!=0 or j["historical_E3"]!=0 or j["original_pair_events"]!=288 or r["new_human_E2"]!=0:
        raise AssertionError("unsupported empirical promotion")
    if r["artificial_person_source_rows"]!=1152:
        raise AssertionError("incomplete receipt")
    if r["source_sha256"]!=hashlib.sha256(CSV.read_bytes()).hexdigest():raise AssertionError("source SHA")
    if r["result_sha256"]!=hashlib.sha256(RESULT.read_bytes()).hexdigest():raise AssertionError("result SHA")
    return verify(load(),j)
class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["original_person_sources"],1152)
    def test_48(self):self.assertEqual(len(WORLDS),48)
    def test_order(self):self.assertTrue(audit()["order_effect_verified"])
    def test_conserve(self):self.assertTrue(audit()["mean_conserved_per_event"])
    def test_pair_example(self):self.assertEqual(independently_update(PROFILES["F"],ONE,Q(1,2),(0,1))[0][0],Q(1,4))
    def test_block(self):self.assertEqual(independently_update(PROFILES["C"],Q(1,2),Q(1,2),(0,3))[0],PROFILES["C"])
    def test_missing(self):
        with self.assertRaises(AssertionError):verify(load()[:-1],obj(RESULT))
    def test_duplicate(self):
        z=load();z[1]=dict(z[0])
        with self.assertRaises(AssertionError):verify(z,obj(RESULT))
    def test_bad_person(self):
        z=load();z[0]=dict(z[0]);z[0]["person_index"]="4"
        with self.assertRaises(AssertionError):verify(z,obj(RESULT))
    def test_bad_pair(self):
        z=load();z[0]=dict(z[0]);z[0]["pair_j"]="0"
        with self.assertRaises(AssertionError):verify(z,obj(RESULT))
    def test_bad_probability(self):
        z=load();z[0]=dict(z[0]);z[0]["uniform_pair_probability"]="1/5"
        with self.assertRaises(AssertionError):verify(z,obj(RESULT))
    def test_wrong_post(self):
        z=load();z[0]=dict(z[0]);z[0]["person_after_selected_pair"]="99"
        with self.assertRaises(AssertionError):verify(z,obj(RESULT))
    def test_result_corrupt(self):
        z=obj(RESULT);z["worlds"][0]["one_step_uniform_pair_expected"]=["bad"]*4
        with self.assertRaises(AssertionError):verify(load(),z)
    def test_bad_original_summary(self):
        z=obj(RESULT);z["reference"]["order_depends_at_two_steps"]=False
        with self.assertRaises(AssertionError):verify(load(),z)
    def test_source_sha(self):self.assertNotEqual(hashlib.sha256(CSV.read_bytes()+b"test").hexdigest(),obj(RECEIPT)["source_sha256"])
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R312 independent"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
