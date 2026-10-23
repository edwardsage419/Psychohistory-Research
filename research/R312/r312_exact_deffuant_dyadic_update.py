#!/usr/bin/env python3
"""R312 exact bounded-confidence Deffuant one-step dyad update, artificial finite E1."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FREEZE="2c8c9bfd15a27574f0fffb02517eb5893aedfee9"
Z,O=F(0),F(1)
PROFILES={"A":(Z,Z,Z,Z),"B":(Z,Z,Z,F(1,2)),"C":(Z,Z,F(1,2),O),
 "D":(Z,F(1,2),F(1,2),O),"E":(Z,Z,O,O),
 "F":(Z,F(1,2),O,O),"G":(F(1,2),F(1,2),F(1,2),O),"H":(O,O,O,O)}
EPS=(Z,F(1,2),O);MU=(F(1,4),F(1,2))
PAIRS=tuple(itertools.combinations(range(4),2))
WORLDS=tuple((p,e,mu) for p in PROFILES for e in EPS for mu in MU)
CSVNAME="R312_ALL_1152_ORIGINAL_DEFFUANT_PERSON_SOURCE_ROWS.csv"
JSONNAME="R312_EXACT_DEFFUANT_PAIR_EVENT_RESULTS.json"
RECEIPT="R312_MACHINE_RECEIPT.json"
FIELDS=("world","profile","initial_opinions","confidence_radius","compromise_mu",
 "pair_i","pair_j","uniform_pair_probability","person_index","person_pre_opinion",
 "person_after_selected_pair","expected_person_next_opinion","selected_pair_confidence_eligible",
 "selected_pair_gap_before","selected_pair_gap_after","updated_opinions",
 "initial_sum","updated_sum","sum_conserved","pair_opinion_gap_contraction")
def wid(p,e,mu):return f"profile={p}|eps={e}|mu={mu}"
def update(x,e,mu,pair):
    if pair not in PAIRS or e not in EPS or mu not in MU:raise ValueError("outside frozen pair update")
    i,j=pair
    if not all(Z<=v<=O for v in x) or len(x)!=4:raise ValueError("opinion vector outside [0,1]")
    before=abs(x[i]-x[j])
    eligible=before<=e
    new=list(x)
    if eligible:
        new[i]=x[i]+mu*(x[j]-x[i])
        new[j]=x[j]+mu*(x[i]-x[j])
    new=tuple(new)
    if sum(new,Z)!=sum(x,Z):raise AssertionError("pair sum changed")
    return {"after":new,"eligible":eligible,"gap_before":before,"gap_after":abs(new[i]-new[j])}
def world(p,e,mu):
    if (p,e,mu) not in WORLDS:raise ValueError("not frozen world")
    x=PROFILES[p]
    events=[update(x,e,mu,pair) for pair in PAIRS]
    expected=tuple(sum((z["after"][i] for z in events),Z)/len(PAIRS) for i in range(4))
    assert sum(expected,Z)==sum(x,Z)
    return {"initial":x,"expected":expected,"events":events}
def row(p,e,mu,pair,i):
    if i not in range(4):raise ValueError("person not frozen")
    if pair not in PAIRS:raise ValueError("pair not frozen")
    w=world(p,e,mu);k=PAIRS.index(pair)
    v=w["events"][k]
    out=v["after"]
    return {"world":wid(p,e,mu),"profile":p,
      "initial_opinions":";".join(map(str,w["initial"])),
      "confidence_radius":e,"compromise_mu":mu,
      "pair_i":pair[0],"pair_j":pair[1],"uniform_pair_probability":F(1,6),
      "person_index":i,"person_pre_opinion":w["initial"][i],
      "person_after_selected_pair":out[i],
      "expected_person_next_opinion":w["expected"][i],
      "selected_pair_confidence_eligible":v["eligible"],
      "selected_pair_gap_before":v["gap_before"],
      "selected_pair_gap_after":v["gap_after"],
      "updated_opinions":";".join(map(str,out)),
      "initial_sum":sum(w["initial"],Z),"updated_sum":sum(out,Z),
      "sum_conserved":sum(out,Z)==sum(w["initial"],Z),
      "pair_opinion_gap_contraction":v["gap_before"]-v["gap_after"]}
def all_sources():return tuple(row(p,e,mu,pair,i) for p,e,mu in WORLDS for pair in PAIRS for i in range(4))
def two_step(x,e,mu,first,second):
    return update(update(x,e,mu,first)["after"],e,mu,second)["after"]
def verify():
    assert len(PROFILES)==8 and len(WORLDS)==48 and len(all_sources())==1152
    assert len({(s["world"],s["pair_i"],s["pair_j"],s["person_index"]) for s in all_sources()})==1152
    for p,e,mu in WORLDS:
        w=world(p,e,mu)
        assert len(w["events"])==6
        assert sum(w["expected"],Z)==sum(w["initial"],Z)
        for pair,v in zip(PAIRS,w["events"]):
            assert sum(v["after"],Z)==sum(w["initial"],Z)
            if v["eligible"]:
                assert v["gap_after"]==abs(O-2*mu)*v["gap_before"]
            else:
                assert v["after"]==w["initial"]
            if e==Z:
                assert v["after"]==w["initial"]
            if p in ("A","H"):
                assert v["after"]==w["initial"]
    x=PROFILES["F"]
    assert update(x,O,F(1,2),(0,1))["after"]==(F(1,4),F(1,4),O,O)
    assert update(x,O,F(1,2),(1,2))["after"]==(Z,F(3,4),F(3,4),O)
    y=PROFILES["C"]
    assert update(y,F(1,2),F(1,2),(1,2))["after"]==(Z,F(1,4),F(1,4),O)
    assert update(y,F(1,2),F(1,2),(0,3))["after"]==y
    assert two_step(x,O,F(1,2),(0,1),(1,2))==(F(1,4),F(5,8),F(5,8),O)
    assert two_step(x,O,F(1,2),(1,2),(0,1))==(F(3,8),F(3,8),F(3,4),O)
    return True
def emit():
    verify()
    csvpath=ROOT/CSVNAME
    with csvpath.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=FIELDS,lineterminator="\n");wr.writeheader()
        for src in all_sources():wr.writerow({k:str(src[k]) for k in FIELDS})
    j={"research_id":"R312","original_catalogue_id":"04-013","freeze_commit":FREEZE,
       "scope":"E1_EXACT_ARTIFICIAL_DEFFUANT_SELECTED_PAIR_ONE_STEP_NOT_LONG_RUN_OR_REAL_PEOPLE",
       "eight_artificial_profiles":8,"complete_artificial_worlds":48,
       "original_pair_events":288,"original_full_person_source_rows":1152,
       "all_pairs_equiprobable":True,"pair_selection_probability":"1/6",
       "real_human_E2":0,"real_animal_E2":0,"historical_E3":0,
       "R066_HK_and_FJ_existing_scopes_unchanged":True,
       "R311_static_relation_geometry_unchanged":True,
       "R073":"FROZEN","PESEN_v0_1":"FROZEN",
       "reference":{"F_pair01_eps1_mu_half":["1/4","1/4","1","1"],
          "F_pair12_eps1_mu_half":["0","3/4","3/4","1"],
          "C_pair12_epshalf_mu_half":["0","1/4","1/4","1"],
          "C_pair03_epshalf_mu_half_unchanged":True,
          "F_two_step_01_then_12":["1/4","5/8","5/8","1"],
          "F_two_step_12_then_01":["3/8","3/8","3/4","1"],
          "order_depends_at_two_steps":True},"worlds":[]}
    for p,e,mu in WORLDS:
        w=world(p,e,mu)
        j["worlds"].append({"world":wid(p,e,mu),"profile":p,"epsilon":str(e),"mu":str(mu),
            "initial":[str(v) for v in w["initial"]],
            "one_step_uniform_pair_expected":[str(v) for v in w["expected"]],
            "mean_initial":str(sum(w["initial"],Z)/4),
            "mean_expected":str(sum(w["expected"],Z)/4),
            "six_original_pair_events":[{"pair":list(pair),"probability":"1/6",
               "after":[str(v) for v in event["after"]],"eligible":event["eligible"],
               "gap_before":str(event["gap_before"]),"gap_after":str(event["gap_after"]),
               "four_original_person_sources":[{k:str(row(p,e,mu,pair,i)[k]) for k in FIELDS if k!="world"} for i in range(4)]}
                for pair,event in zip(PAIRS,w["events"])]})
    rp=ROOT/JSONNAME
    rp.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"research_id":"R312","freeze_commit":FREEZE,"artificial_person_source_rows":1152,
       "source_sha256":hashlib.sha256(csvpath.read_bytes()).hexdigest(),
       "result_sha256":hashlib.sha256(rp.read_bytes()).hexdigest(),"new_human_E2":0,"new_historical_E3":0}
    (ROOT/RECEIPT).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt
class Tests(unittest.TestCase):
    def test_all(self):self.assertTrue(verify())
    def test_worlds(self):self.assertEqual(len(WORLDS),48)
    def test_originals(self):self.assertEqual(len(all_sources()),1152)
    def test_pairs(self):self.assertEqual(len(PAIRS),6)
    def test_F_first(self):self.assertEqual(update(PROFILES["F"],O,F(1,2),(0,1))["after"][0],F(1,4))
    def test_C_block(self):self.assertEqual(update(PROFILES["C"],F(1,2),F(1,2),(0,3))["after"],PROFILES["C"])
    def test_C_boundary(self):self.assertEqual(update(PROFILES["C"],F(1,2),F(1,2),(1,2))["after"][1],F(1,4))
    def test_sequence_order(self):self.assertNotEqual(two_step(PROFILES["F"],O,F(1,2),(0,1),(1,2)),two_step(PROFILES["F"],O,F(1,2),(1,2),(0,1)))
    def test_zero_eps(self):self.assertEqual(update(PROFILES["F"],Z,F(1,2),(0,1))["after"],PROFILES["F"])
    def test_no_human(self):self.assertEqual(sum(world(*w)["expected"] for w in []),0)
    def test_bad_pair(self):
        with self.assertRaises(ValueError):update(PROFILES["F"],O,F(1,2),(0,0))
    def test_bad_mu(self):
        with self.assertRaises(ValueError):update(PROFILES["F"],O,F(1,3),(0,1))
    def test_bad_person(self):
        with self.assertRaises(ValueError):row("F",O,F(1,2),(0,1),4)
def generated(w,pair,i,k):
    def f(self):
        p,e,mu=w;v=row(p,e,mu,pair,i)
        o=update(PROFILES[p],e,mu,pair)
        if k=="post":self.assertEqual(v["person_after_selected_pair"],o["after"][i])
        elif k=="mean":self.assertEqual(v["updated_sum"],v["initial_sum"])
        elif k=="expected":self.assertEqual(v["expected_person_next_opinion"],world(p,e,mu)["expected"][i])
        else:raise AssertionError(k)
    return f
for index,w in enumerate(WORLDS):
    for pair in PAIRS:
        for i in range(4):
            for k in ("post","mean","expected"):
                setattr(Tests,f"test_world{index}_pair{pair[0]}_{pair[1]}_person{i}_{k}",generated(w,pair,i,k))
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R312"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
