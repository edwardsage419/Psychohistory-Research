#!/usr/bin/env python3
"""R309 independent literal 5-agent SIR contact-mask and old-recovery-mask enumeration; no model imports."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research/R309"
SOURCE=ROOT/"R309_ALL_1134_ORIGINAL_SIR_TRANSITION_SOURCES.csv"
RESULT=ROOT/"R309_EXACT_FIVE_AGENT_SIR_RESULTS.json"
RECEIPT=ROOT/"R309_MACHINE_RECEIPT.json"
Z,O=F(0),F(1)
PARAMS=(Z,F(1,2),O)
STATES=[(s,i,5-s-i) for s in range(6) for i in range(6-s)]
WORLDS=[(s,i,r,p,q) for s,i,r in STATES for p,q in itertools.product(PARAMS,repeat=2)]
FIELDS=("S","I","R","contact_p","old_recovery_q",
      "one_susceptible_attack_probability","newly_infected_susceptibles",
      "recovered_old_infectives","next_S","next_I","next_R",
      "joint_transition_probability","expected_next_S","expected_next_I","expected_next_R",
      "next_population_total","is_positive_probability")
def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def originals():
    with SOURCE.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def worldid(w):
    s,i,r,p,q=w
    return f"S={s}|I={i}|R={r}|contact_p={p}|recovery_q={q}"

def brute(world):
    """Enumerate EACH independent infectious-contact and old-recovery bit assignment directly."""
    s,i,r,p,q=world
    n_contacts=s*i
    probabilities=defaultdict(F)
    count=0
    for bits in itertools.product((0,1),repeat=n_contacts+i):
        contact_bits=bits[:n_contacts]
        recover_bits=bits[n_contacts:]
        infected_count=sum(any(contact_bits[person*i:(person+1)*i]) for person in range(s)) if i else 0
        old_recoveries=sum(recover_bits)
        mass=O
        for v in contact_bits:mass*=p if v else O-p
        for v in recover_bits:mass*=q if v else O-q
        probabilities[(infected_count,old_recoveries)]+=mass
        count+=1
    assert count==2**(s*i+i)
    return probabilities,count

def expected(world,brute_prob,x,y):
    s,i,r,p,q=world
    attack=O-(O-p)**i
    # Compute moments independently from unconditional elementary event weights.
    EX=sum((prob*x0 for (x0,_),prob in brute_prob.items()),Z)
    EY=sum((prob*y0 for (_,y0),prob in brute_prob.items()),Z)
    nextS=s-x
    nextI=i+x-y
    nextR=r+y
    vals={
      "S":s,"I":i,"R":r,"contact_p":p,"old_recovery_q":q,
      "one_susceptible_attack_probability":attack,
      "newly_infected_susceptibles":x,"recovered_old_infectives":y,
      "next_S":nextS,"next_I":nextI,"next_R":nextR,
      "joint_transition_probability":brute_prob[(x,y)],
      "expected_next_S":F(s)-EX,
      "expected_next_I":F(i)+EX-EY,
      "expected_next_R":F(r)+EY,
      "next_population_total":nextS+nextI+nextR,
      "is_positive_probability":brute_prob[(x,y)]>Z}
    return {k:str(vals[k]) for k in FIELDS}

def verify(csv_rows,result):
    if len(csv_rows)!=1134 or len(result["worlds"])!=189:
        raise AssertionError("source or world universe incomplete")
    if result["complete_original_transition_source_rows"]!=1134 or result["synthetic_worlds"]!=189:
        raise AssertionError("frozen world counts changed")
    unique={}
    for row in csv_rows:
        try:
            w=(int(row["S"]),int(row["I"]),int(row["R"]),F(row["contact_p"]),F(row["old_recovery_q"]))
            x,y=int(row["newly_infected_susceptibles"]),int(row["recovered_old_infectives"])
        except (KeyError,ValueError,ZeroDivisionError) as e:raise AssertionError("invalid source keys") from e
        if w not in WORLDS or x not in range(w[0]+1) or y not in range(w[1]+1):
            raise AssertionError("source dimension outside model")
        key=(w,x,y)
        if key in unique:raise AssertionError("duplicate artificial outcome")
        if row["world"]!=worldid(w):raise AssertionError("source world ID false")
        unique[key]=row
    if len(unique)!=1134:raise AssertionError("wrong unique full source")
    total_micro=0
    for index,w in enumerate(WORLDS):
        probabilities,n=brute(w)
        total_micro+=n
        if sum(probabilities.values(),Z)!=O:
            raise AssertionError("independent contact microstate probabilities not normalized")
        source_events=[]
        for x in range(w[0]+1):
            for y in range(w[1]+1):
                row=unique.get((w,x,y))
                if row is None:raise AssertionError("missing source event")
                values=expected(w,probabilities,x,y)
                for field in FIELDS:
                    if row[field]!=values[field]:raise AssertionError("source corrupted "+field)
                source_events.append(values)
        j=result["worlds"][index]
        if j["world"]!=worldid(w):raise AssertionError("result world ordering")
        s,i,r,p,q=w
        if (j["S"],j["I"],j["R"],j["contact_p"],j["recovery_q"])!=(s,i,r,str(p),str(q)):
            raise AssertionError("world initial conditions")
        first=source_events[0]
        for f,key in (("attack_rate","one_susceptible_attack_probability"),
            ("expected_next_S","expected_next_S"),("expected_next_I","expected_next_I"),("expected_next_R","expected_next_R")):
            if j[f]!=first[key]:raise AssertionError("world aggregate "+f)
        if j["sum_transition_probabilities"]!="1":raise AssertionError("world not normalized")
        if j["original_source_event_count"]!=len(source_events):raise AssertionError("world event count")
        expected_nested=[{key:row[key] for key in FIELDS} for row in source_events]
        if j["events"]!=expected_nested:raise AssertionError("complete nested results mismatch")
    if total_micro!=11664:raise AssertionError("microstate sample-space size mismatch")
    expected_frozen={
       "S3_I2_p_half_attack_rate":"3/4",
       "S3_I2_p_half_q_half_expected_next":"3/4,13/4,1",
       "S3_I2_p_half_q_half_extinction_without_all_susceptibles_infected":"1/256",
       "S3_I2_p1_q1_simultaneous_next_state":"0,3,2",
       "S0_I5_q1_complete_recovery_next_state":"0,0,5",
       "I_zero_absorbing":True,
       "sum_over_all_world_one_step_microstate_assignments_per_nine_parameters":11664}
    if result["frozen_reference"]!=expected_frozen:raise AssertionError("frozen checks drifted")
    return {"artificial_worlds":189,"original_full_transition_sources":1134,
      "independently_enumerated_elementary_contact_recovery_bit_patterns":total_micro,
      "exact_full_source_independent_event_weight_audit":"PASS",
      "actual_disease_patient_data_E2":0,"human_social_diffusion_E2":0,"historical_E3":0}

def audit():
    r,j=obj(RECEIPT),obj(RESULT)
    freeze="aec096d72f66c44ac1b13dd5ed1ce9d169f21aac"
    if r["freeze_commit"]!=freeze or j["freeze_commit"]!=freeze:raise AssertionError("wrong freeze")
    if j["research_id"]!="R309" or j["original_catalogue_id"]!="04-006":raise AssertionError("wrong original model")
    if j["project_discrete_independent_contact_assumption_not_exact_Kermack_McKendrick_1927_equation"] is not True:
        raise AssertionError("original continuous model misattributed")
    if j["no_real_human_clinical_or_social_E2"]!=0 or j["no_historical_E3"]!=0:
        raise AssertionError("artificial model misrepresented empirical")
    if r["source_rows"]!=1134 or r["new_real_E2"]!=0 or r["new_historical_E3"]!=0:raise AssertionError("receipt incorrect")
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=r["source_sha256"]:
        raise AssertionError("CSV corrupted")
    if hashlib.sha256(RESULT.read_bytes()).hexdigest()!=r["results_sha256"]:
        raise AssertionError("JSON corrupted")
    return {**verify(originals(),j),"source_sha256":r["source_sha256"],"results_sha256":r["results_sha256"]}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["original_full_transition_sources"],1134)
    def test_micro(self):self.assertEqual(audit()["independently_enumerated_elementary_contact_recovery_bit_patterns"],11664)
    def test_count_worlds(self):self.assertEqual(len(WORLDS),189)
    def test_independent_prob_sum(self):self.assertEqual(sum(brute((3,2,0,F(1,2),F(1,2)))[0].values(),Z),O)
    def test_extinction(self):self.assertEqual(brute((3,2,0,F(1,2),F(1,2)))[0][(0,2)],F(1,256))
    def test_simultaneous(self):self.assertEqual(brute((3,2,0,O,O))[0][(3,2)],O)
    def test_no_contact(self):self.assertEqual(brute((3,2,0,Z,O))[0][(0,2)],O)
    def test_no_infected(self):self.assertEqual(brute((5,0,0,O,O))[0][(0,0)],O)
    def test_susceptible_zero(self):self.assertEqual(sum(brute((0,5,0,O,O))[0].values(),Z),O)
    def test_missing(self):
        with self.assertRaises(AssertionError):verify(originals()[:-1],obj(RESULT))
    def test_duplicate(self):
        s=originals();s[1]=dict(s[0])
        with self.assertRaises(AssertionError):verify(s,obj(RESULT))
    def test_event_prob(self):
        s=originals();s[1]=dict(s[1]);s[1]["joint_transition_probability"]="9"
        with self.assertRaises(AssertionError):verify(s,obj(RESULT))
    def test_new_recovers_same_step(self):
        s=originals()
        k=next(i for i,row in enumerate(s) if row["newly_infected_susceptibles"]=="1" and row["recovered_old_infectives"]=="0")
        s[k]=dict(s[k]);s[k]["next_I"]="0"
        with self.assertRaises(AssertionError):verify(s,obj(RESULT))
    def test_expected_next(self):
        s=originals();s[0]=dict(s[0]);s[0]["expected_next_I"]="123"
        with self.assertRaises(AssertionError):verify(s,obj(RESULT))
    def test_result_tamper(self):
        j=obj(RESULT);j["worlds"][0]["events"][0]["next_population_total"]="4"
        with self.assertRaises(AssertionError):verify(originals(),j)
    def test_result_summary_tamper(self):
        j=obj(RESULT);j["frozen_reference"]["I_zero_absorbing"]=False
        with self.assertRaises(AssertionError):verify(originals(),j)
    def test_SHA_tamper(self):
        self.assertNotEqual(hashlib.sha256(SOURCE.read_bytes()+b"X").hexdigest(),obj(RECEIPT)["source_sha256"])
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R309 independent"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
