#!/usr/bin/env python3
"""R309 frozen project-defined 5-agent discrete SIR Markov one-step transition E1. No real epidemic observations."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from math import comb
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="aec096d72f66c44ac1b13dd5ed1ce9d169f21aac"
N=5
Z,O=F(0),F(1)
PARAMS=(Z,F(1,2),O)
STATES=tuple((s,i,N-s-i) for s in range(N+1) for i in range(N-s+1))
WORLDS=tuple((s,i,r,p,q) for s,i,r in STATES for p,q in itertools.product(PARAMS,repeat=2))
SOURCE_NAME="R309_ALL_1134_ORIGINAL_SIR_TRANSITION_SOURCES.csv"
RESULT_NAME="R309_EXACT_FIVE_AGENT_SIR_RESULTS.json"
RECEIPT_NAME="R309_MACHINE_RECEIPT.json"

def valid(s,i,r,p,q):
    return (s,i,r,p,q) in WORLDS
def worldid(s,i,r,p,q):
    return f"S={s}|I={i}|R={r}|contact_p={p}|recovery_q={q}"
def attack_rate(i,p):
    return O-(O-p)**i

def binom_mass(n,k,p):
    if not 0<=k<=n:raise ValueError("event outside support")
    return F(comb(n,k))*p**k*(O-p)**(n-k)

def expectation(s,i,r,p,q):
    if not valid(s,i,r,p,q):raise ValueError("not frozen world")
    attack=attack_rate(i,p)
    infected=F(s)*attack
    recovered=F(i)*q
    return {"attack_rate":attack,"expected_new_infections":infected,
      "expected_old_recoveries":recovered,
      "expected_next_S":F(s)-infected,
      "expected_next_I":F(i)+infected-recovered,
      "expected_next_R":F(r)+recovered}

def event(s,i,r,p,q,new,old_recovered):
    if not valid(s,i,r,p,q):raise ValueError("not frozen world")
    if not (0<=new<=s and 0<=old_recovered<=i):raise ValueError("event not possible")
    ex=expectation(s,i,r,p,q)
    mass=binom_mass(s,new,ex["attack_rate"])*binom_mass(i,old_recovered,q)
    ns,ni,nr=s-new,i+new-old_recovered,r+old_recovered
    if ns+ni+nr!=N or min(ns,ni,nr)<0:raise AssertionError("SIR conservation")
    return {"world":worldid(s,i,r,p,q),"S":s,"I":i,"R":r,
      "contact_p":p,"old_recovery_q":q,"one_susceptible_attack_probability":ex["attack_rate"],
      "newly_infected_susceptibles":new,"recovered_old_infectives":old_recovered,
      "next_S":ns,"next_I":ni,"next_R":nr,"joint_transition_probability":mass,
      "expected_next_S":ex["expected_next_S"],"expected_next_I":ex["expected_next_I"],
      "expected_next_R":ex["expected_next_R"],"next_population_total":ns+ni+nr,
      "is_positive_probability":mass>Z}

def worlds():
    return tuple((w,tuple(event(*w,x,y) for x in range(w[0]+1) for y in range(w[1]+1))) for w in WORLDS)

def sources():
    return tuple(v for _,events in worlds() for v in events)

def verify():
    assert len(STATES)==21 and len(WORLDS)==189 and len(sources())==1134
    assert len({(z["world"],z["newly_infected_susceptibles"],z["recovered_old_infectives"]) for z in sources()})==1134
    for world,rows in worlds():
        s,i,r,p,q=world
        total=sum((v["joint_transition_probability"] for v in rows),Z)
        assert total==O
        ex=expectation(*world)
        for key,column in (("expected_next_S","next_S"),("expected_next_I","next_I"),("expected_next_R","next_R")):
            assert sum((v["joint_transition_probability"]*v[column] for v in rows),Z)==ex[key]
        assert ex["expected_next_S"]+ex["expected_next_I"]+ex["expected_next_R"]==N
        assert all(v["next_S"]<=s and v["next_R"]>=r and v["next_population_total"]==N for v in rows)
        if i==0:
            assert sum((v["joint_transition_probability"] for v in rows if
                 (v["next_S"],v["next_I"],v["next_R"])==(s,i,r)),Z)==O
        if p==Z:
            assert all(v["joint_transition_probability"]==Z or v["newly_infected_susceptibles"]==0 for v in rows)
        if q==Z:
            assert all(v["joint_transition_probability"]==Z or v["recovered_old_infectives"]==0 for v in rows)
        if q==O:
            assert all(v["joint_transition_probability"]==Z or v["recovered_old_infectives"]==i for v in rows)
    w=(3,2,0,F(1,2),F(1,2))
    assert attack_rate(2,F(1,2))==F(3,4)
    assert expectation(*w)["expected_next_S"]==F(3,4)
    assert expectation(*w)["expected_next_I"]==F(13,4)
    assert expectation(*w)["expected_next_R"]==O
    assert event(*w,0,2)["joint_transition_probability"]==F(1,256)
    assert (event(*w,0,2)["next_S"],event(*w,0,2)["next_I"],event(*w,0,2)["next_R"])==(3,0,2)
    assert (event(3,2,0,O,O,3,2)["next_S"],event(3,2,0,O,O,3,2)["next_I"],event(3,2,0,O,O,3,2)["next_R"])==(0,3,2)
    assert event(3,2,0,O,O,3,2)["joint_transition_probability"]==O
    return True

def emit():
    verify()
    cols=("world","S","I","R","contact_p","old_recovery_q",
      "one_susceptible_attack_probability","newly_infected_susceptibles",
      "recovered_old_infectives","next_S","next_I","next_R",
      "joint_transition_probability","expected_next_S","expected_next_I","expected_next_R",
      "next_population_total","is_positive_probability")
    spath=ROOT/SOURCE_NAME
    with spath.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n");w.writeheader()
        for x in sources():w.writerow({k:str(x[k]) for k in cols})
    j={"research_id":"R309","original_catalogue_id":"04-006","freeze_commit":FREEZE,
       "scope":"E1_NEW_PROJECT_DISCRETE_5_AGENT_SIR_MARKOV_TRANSITIONS_NOT_ORIGINAL_1927_ODE_OR_REAL_DISEASE",
       "population_N":N,"original_artificial_initial_count_states":21,
       "synthetic_worlds":189,"complete_original_transition_source_rows":1134,
       "all_source_events_including_zero_probability":True,
       "project_discrete_independent_contact_assumption_not_exact_Kermack_McKendrick_1927_equation":True,
       "no_real_human_clinical_or_social_E2":0,"no_historical_E3":0,
       "R073":"FROZEN","PESEN_v0_1":"FROZEN","worlds":[]}
    for w,rows in worlds():
        e=expectation(*w)
        j["worlds"].append({"world":worldid(*w),"S":w[0],"I":w[1],"R":w[2],
           "contact_p":str(w[3]),"recovery_q":str(w[4]),
           "attack_rate":str(e["attack_rate"]),"expected_next_S":str(e["expected_next_S"]),
           "expected_next_I":str(e["expected_next_I"]),"expected_next_R":str(e["expected_next_R"]),
           "sum_transition_probabilities":str(sum((v["joint_transition_probability"] for v in rows),Z)),
           "original_source_event_count":len(rows),
           "events":[{k:str(v[k]) for k in cols if k!="world"} for v in rows]})
    j["frozen_reference"]={
        "S3_I2_p_half_attack_rate":"3/4",
        "S3_I2_p_half_q_half_expected_next":"3/4,13/4,1",
        "S3_I2_p_half_q_half_extinction_without_all_susceptibles_infected":"1/256",
        "S3_I2_p1_q1_simultaneous_next_state":"0,3,2",
        "S0_I5_q1_complete_recovery_next_state":"0,0,5",
        "I_zero_absorbing":True,
        "sum_over_all_world_one_step_microstate_assignments_per_nine_parameters":11664}
    out=ROOT/RESULT_NAME
    out.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"research_id":"R309","freeze_commit":FREEZE,"source_rows":1134,
       "source_sha256":hashlib.sha256(spath.read_bytes()).hexdigest(),
       "results_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),
       "new_real_E2":0,"new_historical_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_full(self):self.assertTrue(verify())
    def test_worlds(self):self.assertEqual(len(WORLDS),189)
    def test_states(self):self.assertEqual(len(STATES),21)
    def test_sources(self):self.assertEqual(len(sources()),1134)
    def test_zero_infected(self):self.assertEqual(event(4,0,1,F(1,2),F(1,2),0,0)["joint_transition_probability"],O)
    def test_zero_contact(self):self.assertEqual(event(3,2,0,Z,F(1,2),1,1)["joint_transition_probability"],Z)
    def test_zero_recovery(self):self.assertEqual(event(3,2,0,F(1,2),Z,1,1)["joint_transition_probability"],Z)
    def test_all_old_recovery_new_remains(self):self.assertEqual(event(3,2,0,O,O,3,2)["next_I"],3)
    def test_expected_infect(self):self.assertEqual(expectation(3,2,0,F(1,2),F(1,2))["expected_next_I"],F(13,4))
    def test_extinction(self):self.assertEqual(event(3,2,0,F(1,2),F(1,2),0,2)["joint_transition_probability"],F(1,256))
    def test_no_reinfection(self):self.assertEqual(event(0,0,5,O,O,0,0)["next_R"],5)
    def test_bad_state(self):
        with self.assertRaises(ValueError):expectation(2,2,0,Z,Z)
    def test_bad_new(self):
        with self.assertRaises(ValueError):event(3,2,0,Z,Z,4,0)
    def test_bad_recovery(self):
        with self.assertRaises(ValueError):event(3,2,0,Z,Z,0,3)
    def test_bad_parameter(self):
        with self.assertRaises(ValueError):expectation(3,2,0,F(1,4),O)
def generated(w,x,y,kind):
    def test(self):
        r=event(*w,x,y)
        if kind=="total":self.assertEqual(r["next_population_total"],5)
        elif kind=="joint":self.assertEqual(r["joint_transition_probability"],binom_mass(w[0],x,attack_rate(w[1],w[3]))*binom_mass(w[1],y,w[4]))
        elif kind=="bounds":self.assertTrue(r["next_S"]<=w[0] and r["next_R"]>=w[2])
        else:raise AssertionError(kind)
    return test
for idx,w in enumerate(WORLDS):
    for x in range(w[0]+1):
        for y in range(w[1]+1):
            for kind in ("total","joint","bounds"):
                setattr(Tests,f"test_world{idx}_new{x}_recover{y}_{kind}",generated(w,x,y,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R309"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
